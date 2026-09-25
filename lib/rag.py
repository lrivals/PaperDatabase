"""Recherche de passages (niveau N1 de docs/RAG.md) : découpage, BM25, embeddings, fusion RRF.

Aucun LLM : la recherche est déterministe (même index, même requête, même classement) et
chaque passage renvoyé porte son chunk_id, sa section, sa page et le sha1 de son texte.

- Passages : une entrée de sections.jsonl ; au-delà de SPLIT_OVER mots, fenêtres de
  WINDOW mots avec OVERLAP mots de recouvrement. chunk_id = <id de section>.<k>.
- Lexical : BM25 recalculé à chaque chargement (moins d'une seconde pour le corpus).
- Dense : lib/embed._encode (sentence-transformers, optionnel). Vecteurs en cache dans
  .cache/rag/<modèle>.npz, indexés par chunk_id:sha1 : seuls les passages nouveaux ou
  modifiés sont réencodés. Sans sentence-transformers, recherche lexicale seule.
- Fusion : Reciprocal Rank Fusion, score = Σ 1 / (RRF_K + rang).
"""
import difflib
import hashlib
import json
import math
import re
import unicodedata
from collections import Counter
from pathlib import Path

from lib import embed, query

DEFAULT_MODEL = "BAAI/bge-small-en-v1.5"
# Préfixe recommandé par le modèle pour encoder une requête (pas les passages).
QUERY_PREFIX = {"BAAI/bge-small-en-v1.5": "Represent this sentence for searching relevant passages: "}
SPLIT_OVER, WINDOW, OVERLAP = 250, 200, 40
RRF_K = 60
BM25_K1, BM25_B = 1.5, 0.75
SNIPPET = 160
VERIFY_MIN = 0.85
# Sous ce cosinus (bge-small), le meilleur passage est probablement hors sujet. Calibré à la
# main sur quelques requêtes (hors sujet 0,45-0,55, pertinentes 0,73-0,90) : indicatif.
LOW_COS = 0.60
MODES = ("hybrid", "dense", "lexical")

_TOKEN = re.compile(r"[a-z0-9]+")


def sha1(text):
    return hashlib.sha1(text.encode()).hexdigest()


def tokenize(text):
    return _TOKEN.findall(text.lower())


def quiet_model_loading(model):
    """Hors ligne si le modèle est déjà en cache (pas de requête au Hub à chaque recherche),
    et sans barre de progression : la sortie des commandes reste propre."""
    import os
    os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
    os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    hub = Path(os.environ.get("HF_HOME", Path.home() / ".cache" / "huggingface")) / "hub"
    name = model if "/" in model else f"sentence-transformers/{model}"
    if (hub / f"models--{name.replace('/', '--')}").exists():
        os.environ.setdefault("HF_HUB_OFFLINE", "1")


# ------------------------------------------------------------------- passages

def split_text(text, window=WINDOW, overlap=OVERLAP, split_over=SPLIT_OVER):
    words = text.split()
    if len(words) <= split_over:
        return [text]
    step = window - overlap
    out = []
    for start in range(0, len(words), step):
        out.append(" ".join(words[start:start + window]))
        if start + window >= len(words):
            break
    return out


def load_chunks(root):
    """Passages du corpus, dans l'ordre des papiers puis des sections."""
    chunks = []
    for path in sorted((Path(root) / "papers").glob("*/sections.jsonl")):
        for line in path.read_text().splitlines():
            if not line.strip():
                continue
            s = json.loads(line)
            for k, text in enumerate(split_text(s["text"])):
                chunks.append({
                    "chunk_id": f"{s['id']}.{k}", "section_id": s["id"],
                    "paper_id": s["paper_id"], "kind": s["kind"], "section": s["section"],
                    "subsection": s.get("subsection"), "page": s.get("page"),
                    "text": text, "sha1": sha1(text),
                })
    return chunks


def encoded_text(c):
    """Texte encodé : titre de section en préfixe, pour donner du contexte au vecteur."""
    head = " — ".join(x for x in (c["section"], c.get("subsection")) if x)
    return f"{head} — {c['text']}"


# ----------------------------------------------------------------------- BM25

class BM25:
    def __init__(self, docs):
        self.tf = [Counter(tokenize(d)) for d in docs]
        self.len = [sum(tf.values()) for tf in self.tf]
        self.avg = (sum(self.len) / len(self.len)) if self.len else 0
        df = Counter(t for tf in self.tf for t in tf)
        n = len(docs)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}

    def scores(self, q):
        terms = [t for t in set(tokenize(q)) if t in self.idf]
        out = []
        for tf, dl in zip(self.tf, self.len):
            s = 0.0
            for t in terms:
                f = tf.get(t)
                if f:
                    s += self.idf[t] * f * (BM25_K1 + 1) / (
                        f + BM25_K1 * (1 - BM25_B + BM25_B * dl / (self.avg or 1)))
            out.append(s)
        return out


# ------------------------------------------------------------------ vecteurs

def _cache_path(root, model):
    return Path(root) / ".cache" / "rag" / f"{model.replace('/', '_')}.npz"


def build_index(root, chunks=None, model=DEFAULT_MODEL, force=False):
    """Encode les passages absents du cache ; renvoie un manifeste (dict).

    Sans sentence-transformers : aucun vecteur, mode lexical seul (manifest["dense"] = False).
    """
    chunks = chunks if chunks is not None else load_chunks(root)
    manifest = {"chunks": len(chunks), "papers": len({c["paper_id"] for c in chunks}),
                "model": model, "dense": embed.available(), "encoded": 0}
    if not manifest["dense"]:
        return manifest
    quiet_model_loading(model)
    import numpy as np
    path = _cache_path(root, model)
    cache = {}
    if path.exists() and not force:
        with np.load(path) as f:
            cache = dict(zip(f["keys"].tolist(), f["vecs"]))
    keys = [f"{c['chunk_id']}:{c['sha1']}" for c in chunks]
    missing = [i for i, k in enumerate(keys) if k not in cache]
    if missing:
        vecs = np.asarray(embed._encode([encoded_text(chunks[i]) for i in missing], model),
                          dtype=np.float32)
        for i, v in zip(missing, vecs):
            cache[keys[i]] = v
    if missing or set(cache) != set(keys):
        path.parent.mkdir(parents=True, exist_ok=True)
        np.savez(path, keys=np.array(keys), vecs=np.vstack([cache[k] for k in keys]))
    manifest["encoded"] = len(missing)
    return manifest


def _load_vectors(root, chunks, model):
    import numpy as np
    path = _cache_path(root, model)
    if not path.exists():
        return None
    with np.load(path) as f:
        cache = dict(zip(f["keys"].tolist(), f["vecs"]))
    keys = [f"{c['chunk_id']}:{c['sha1']}" for c in chunks]
    if any(k not in cache for k in keys):
        return None  # index périmé : reconstruire (bin/pdb reindex)
    return np.vstack([cache[k] for k in keys])


# ------------------------------------------------------------------ recherche

class Index:
    """Passages + BM25 + vecteurs (si disponibles). Chargé une fois par commande."""

    def __init__(self, root, model=DEFAULT_MODEL, chunks=None):
        self.root = Path(root)
        self.model = model
        self.chunks = chunks if chunks is not None else load_chunks(root)
        self.by_id = {c["chunk_id"]: i for i, c in enumerate(self.chunks)}
        self.bm25 = BM25([encoded_text(c) for c in self.chunks])
        self.vecs = _load_vectors(root, self.chunks, model) if embed.available() else None
        if self.vecs is not None:
            quiet_model_loading(model)
        self.metas = query.load_papers(root)
        self.short = query.short_ids(self.metas)
        self._axes = {m["id"]: set(m.get("axes") or []) for m in self.metas}

    @property
    def dense(self):
        return self.vecs is not None

    def _candidates(self, paper_ids=None, axis=None, kind=None, section=None):
        out = []
        for i, c in enumerate(self.chunks):
            if paper_ids is not None and c["paper_id"] not in paper_ids:
                continue
            if axis and axis not in self._axes.get(c["paper_id"], ()):
                continue
            if kind and c["kind"] != kind:
                continue
            if section and section.lower() not in (c["section"] or "").lower() + " " + \
                    (c.get("subsection") or "").lower():
                continue
            out.append(i)
        return out

    def search(self, q, k=8, mode="hybrid", paper_ids=None, axis=None, kind=None, section=None):
        """Liste de hits (dicts du passage + score + rangs), du meilleur au moins bon."""
        if mode not in MODES:
            raise ValueError(f"mode {mode!r} : {' | '.join(MODES)}")
        if mode != "lexical" and not self.dense:
            mode = "lexical"
        cand = self._candidates(paper_ids, axis, kind, section)
        ranks, sim = [], None
        if mode in ("hybrid", "lexical"):
            s = self.bm25.scores(q)
            lex = sorted((i for i in cand if s[i] > 0), key=lambda i: (-s[i], self.chunks[i]["chunk_id"]))
            ranks.append({i: r for r, i in enumerate(lex, 1)})
        if mode in ("hybrid", "dense"):
            qv = embed._encode([QUERY_PREFIX.get(self.model, "") + q], self.model)[0]
            sim = self.vecs @ qv
            den = sorted(cand, key=lambda i: (-float(sim[i]), self.chunks[i]["chunk_id"]))
            ranks.append({i: r for r, i in enumerate(den, 1)})
        score = Counter()
        for rk in ranks:
            for i, r in rk.items():
                score[i] += 1.0 / (RRF_K + r)
        best = sorted(score, key=lambda i: (-score[i], self.chunks[i]["chunk_id"]))[:k]
        return [{**self.chunks[i], "score": round(score[i], 5), "mode": mode,
                 "cos": None if sim is None else round(float(sim[i]), 3)} for i in best]

    # ------------------------------------------------------- identifiants
    def short_chunk_id(self, chunk_id):
        pid, _, rest = chunk_id.partition("#")
        return f"{self.short.get(pid, pid)}#{rest}"

    def resolve_chunk(self, cid):
        """chunk_id complet ou court (1612.07119#019.0) → chunk_id complet, ou None.
        Un id de section sans .k (…#019) désigne son premier passage."""
        pid, sep, rest = cid.partition("#")
        if not sep:
            return None
        if "." not in rest:
            rest += ".0"
        if f"{pid}#{rest}" in self.by_id:
            return f"{pid}#{rest}"
        full = [p for p, s in self.short.items() if s == pid]
        if full and f"{full[0]}#{rest}" in self.by_id:
            return f"{full[0]}#{rest}"
        return None

    def get(self, chunk_id, context=0):
        """Le passage et ses voisins du même papier (± context)."""
        i = self.by_id[chunk_id]
        pid = self.chunks[i]["paper_id"]
        return [self.chunks[j] for j in range(max(0, i - context), min(len(self.chunks), i + context + 1))
                if self.chunks[j]["paper_id"] == pid]


# ------------------------------------------------------------------ extraits

def snippet(text, q, idf=None, width=SNIPPET):
    """Extrait de ~width caractères centré sur le terme de la requête le plus rare présent."""
    terms = sorted(set(tokenize(q)), key=lambda t: -(idf or {}).get(t, len(t)))
    low = text.lower()
    pos = -1
    for t in terms:
        m = re.search(rf"\b{re.escape(t)}", low)
        if m:
            pos = m.start()
            break
    start = max(0, pos - width // 3) if pos >= 0 else 0
    cut = text[start:start + width].replace("\n", " ").replace("\t", " ")
    marked = {t for t in terms if len(t) > 2 and (idf or {}).get(t, 1) > 1}
    if marked:
        cut = re.sub(r"\b(" + "|".join(re.escape(t) for t in sorted(marked, key=len, reverse=True)) + r")\w*",
                     lambda m: f"«{m.group(0)}»", cut, flags=re.I)
    return ("…" if start > 0 else "") + cut.strip() + ("…" if start + width < len(text) else "")


# --------------------------------------------------------------- vérification

_LIGATURES = {"ﬁ": "fi", "ﬂ": "fl", "ﬀ": "ff", "ﬃ": "ffi", "ﬄ": "ffl"}


def normalize(text):
    """Pour comparer une citation au texte : ligatures, casse, ponctuation et espaces ignorés."""
    for a, b in _LIGATURES.items():
        text = text.replace(a, b)
    text = unicodedata.normalize("NFKC", text).lower()
    text = re.sub(r"(\w)-\s+(\w)", r"\1\2", text)  # césure
    return re.sub(r"[^\w]+", "", text)


def match_ratio(text, quote):
    """(ratio, extrait) de la meilleure fenêtre de `text` pour `quote`, après normalisation."""
    t, q = normalize(text), normalize(quote)
    if not q:
        return 0.0
    if q in t:
        return 1.0
    sm = difflib.SequenceMatcher(None, t, q, autojunk=False)
    best = 0.0
    for a, b, size in sm.get_matching_blocks():
        if size < 3:
            continue
        start = max(0, a - b)
        for s in (start, max(0, start - 3), start + 3):
            r = difflib.SequenceMatcher(None, t[s:s + len(q)], q, autojunk=False).ratio()
            best = max(best, r)
    return best


def verify(index, chunk_id, quote, expect_sha=None):
    """Statut d'une citation : OK, APPROX, ABSENT ; MODIFIÉ si le sha1 attendu ne correspond pas.

    Renvoie (statut, ratio, chunk_id où la citation est trouvée). Une citation absente du
    passage indiqué est cherchée dans le reste du papier : le chunk_id renvoyé le dit.
    """
    c = index.chunks[index.by_id[chunk_id]]
    if expect_sha and not c["sha1"].startswith(expect_sha):
        return "MODIFIÉ", 0.0, chunk_id
    r = match_ratio(c["text"], quote)
    if r < VERIFY_MIN:
        for other in index.chunks:
            if other["paper_id"] == c["paper_id"] and other["chunk_id"] != chunk_id:
                r2 = match_ratio(other["text"], quote)
                if r2 >= VERIFY_MIN and r2 > r:
                    return ("OK" if r2 == 1.0 else "APPROX"), r2, other["chunk_id"]
    status = "OK" if r == 1.0 else "APPROX" if r >= VERIFY_MIN else "ABSENT"
    return status, r, chunk_id


# ----------------------------------------------------------------- évaluation

def evaluate(index, questions, k=5, modes=MODES):
    """recall@k (au moins une section attendue dans les k premiers), MRR, paper@k."""
    out = {}
    for mode in modes:
        if mode != "lexical" and not index.dense:
            continue
        hits = rr = paper_hits = 0
        misses = []
        for q in questions:
            exp = set(q["expect"])
            res = index.search(q["q"], k=max(k, 10), mode=mode)
            ranks = [r for r, h in enumerate(res, 1) if h["section_id"] in exp]
            first = ranks[0] if ranks else None
            if first and first <= k:
                hits += 1
            else:
                misses.append(q["q"])
            rr += 1 / first if first else 0
            exp_papers = {e.split("#")[0] for e in exp}
            paper_hits += any(h["paper_id"] in exp_papers for h in res[:k])
        n = len(questions) or 1
        out[mode] = {"recall": hits / n, "mrr": rr / n, "paper": paper_hits / n, "misses": misses}
    return out
