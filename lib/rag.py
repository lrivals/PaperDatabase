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

Deux moteurs pour les mêmes passages (mêmes chunk_id, même pdb show / verify) :
- CPU, par défaut : bge-small (dense) et MiniLM (rerank), sentence-transformers optionnel ;
- GPU, sur demande : Qwen3-Embedding-4B et Qwen3-Reranker-4B (lib/rag_models), utilisés
  seulement si l'utilisateur active la route GPU (bin/pdb gpu on, ou PDB_GPU=1) et qu'un GPU
  CUDA est présent. Vecteurs dans .cache/rag/Qwen_Qwen3-Embedding-4B.npz, à côté de ceux du
  CPU ; sans eux (base pas encore réindexée), la recherche reste sur le moteur CPU.
"""
import difflib
import hashlib
import json
import math
import re
import unicodedata
from collections import Counter
from pathlib import Path

from lib import embed, query, rag_models

DEFAULT_MODEL = "BAAI/bge-small-en-v1.5"
GPU_MODEL, GPU_RERANK_MODEL = rag_models.EMBED, rag_models.RERANK
# Préfixe recommandé par le modèle pour encoder une requête (pas les passages).
QUERY_PREFIX = {"BAAI/bge-small-en-v1.5": "Represent this sentence for searching relevant passages: "}
SPLIT_OVER, WINDOW, OVERLAP = 250, 200, 40
RRF_K = 60
BM25_K1, BM25_B = 1.5, 0.75
SNIPPET = 160
VERIFY_MIN = 0.85
# Pas de seuil de « pertinence faible » : ni le cosinus ni le cross-encoder ne séparent les
# questions hors corpus des questions du corpus (docs/EVAL.md §5, 26/09/2026).
MODES = ("hybrid", "dense", "lexical")
RERANK_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
RERANK_TOP = 30

_rerankers = {}


def _cross_scores(q, texts, model=RERANK_MODEL):
    """Scores du cross-encoder ; séparé pour être remplacé dans les tests."""
    if model == GPU_RERANK_MODEL:
        return [float(x) for x in rag_models.rerank(q, texts)]
    if model not in _rerankers:
        from sentence_transformers import CrossEncoder
        _rerankers[model] = CrossEncoder(model)
    return [float(x) for x in _rerankers[model].predict([(q, t) for t in texts])]


def encode(texts, model, query=False):
    """Vecteurs normalisés des textes (requête : préfixe ou instruction du modèle)."""
    if model == GPU_MODEL:
        return rag_models.embed_texts(texts, query=query)
    if query:
        texts = [QUERY_PREFIX.get(model, "") + t for t in texts]
    return embed._encode(texts, model)


def dense_available(model):
    """Le modèle peut-il encoder ici ? GPU : torch + CUDA ; CPU : sentence-transformers."""
    return rag_models.unavailable() is None if model == GPU_MODEL else embed.available()


_TOKEN = re.compile(r"[a-z0-9]+")


def sha1(text):
    return hashlib.sha1(text.encode()).hexdigest()


def tokenize(text):
    return _TOKEN.findall(text.lower())


def quiet_model_loading(*models):
    """Hors ligne si tous les modèles sont déjà en cache (pas de requête au Hub à chaque
    recherche), et sans barre de progression : la sortie des commandes reste propre.

    Le mode hors ligne vaut pour tout le processus : déclarer d'avance tous les modèles
    qu'il chargera, sinon un modèle absent du cache ne pourra plus être téléchargé."""
    import os
    os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
    os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    hub = Path(os.environ.get("HF_HOME", Path.home() / ".cache" / "huggingface")) / "hub"
    names = [m if "/" in m else f"sentence-transformers/{m}" for m in models]
    if names and all((hub / f"models--{n.replace('/', '--')}").exists() for n in names):
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
    model=GPU_MODEL : vecteurs Qwen (route GPU), si torch et CUDA sont présents.
    """
    chunks = chunks if chunks is not None else load_chunks(root)
    manifest = {"chunks": len(chunks), "papers": len({c["paper_id"] for c in chunks}),
                "model": model, "dense": dense_available(model), "encoded": 0}
    if not manifest["dense"]:
        return manifest
    if model != GPU_MODEL:
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
        vecs = np.asarray(encode([encoded_text(chunks[i]) for i in missing], model),
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
    """Passages + BM25 + vecteurs (si disponibles). Chargé une fois par commande.

    gpu=True : moteur Qwen (route GPU) si ses vecteurs existent pour cette base et que CUDA
    est présent ; sinon moteur CPU, et self.note dit pourquoi. gpu=None : réglage de la
    machine (rag_models.enabled : bin/pdb gpu on, ou PDB_GPU=1)."""

    def __init__(self, root, model=DEFAULT_MODEL, chunks=None, rerank=False, gpu=False):
        self.root = Path(root)
        self.chunks = chunks if chunks is not None else load_chunks(root)
        self.by_id = {c["chunk_id"]: i for i, c in enumerate(self.chunks)}
        self.bm25 = BM25([encoded_text(c) for c in self.chunks])
        self.note = None
        if gpu is None:
            gpu = rag_models.wanted()
        self.vecs = None
        if gpu:
            reason = rag_models.unavailable()
            if reason is None:
                self.vecs = _load_vectors(root, self.chunks, GPU_MODEL)
                reason = None if self.vecs is not None else \
                    "vecteurs GPU absents ou périmés pour cette base (bin/pdb reindex)"
            if reason:
                self.note = f"route GPU indisponible : {reason} ; moteur CPU"
        self.gpu = self.vecs is not None
        self.model = GPU_MODEL if self.gpu else model
        self.rerank_model = GPU_RERANK_MODEL if self.gpu else RERANK_MODEL
        if not self.gpu:
            self.vecs = _load_vectors(root, self.chunks, model) if embed.available() else None
            if self.vecs is not None:
                quiet_model_loading(model, *([RERANK_MODEL] if rerank else []))
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

    def search(self, q, k=8, mode="hybrid", paper_ids=None, axis=None, kind=None, section=None,
               rerank=False):
        """Liste de hits (dicts du passage + score + rangs), du meilleur au moins bon.

        rerank : les RERANK_TOP premiers de la fusion sont reclassés par un cross-encoder
        (expérimental, docs/RAG.md §11)."""
        if rerank:
            pool = self.search(q, k=RERANK_TOP, mode=mode, paper_ids=paper_ids, axis=axis,
                               kind=kind, section=section)
            ce = _cross_scores(q, [encoded_text(h) for h in pool], self.rerank_model)
            order = sorted(range(len(pool)), key=lambda i: (-ce[i], pool[i]["chunk_id"]))
            return [{**pool[i], "rerank": round(ce[i], 3)} for i in order[:k]]
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
            qv = encode([q], self.model, query=True)[0]
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


def relevance_score(index, q, hits=None, top=3):
    """Meilleur score du cross-encoder entre la question et les `top` premiers passages
    (recherche hybride si hits n'est pas fourni) : signal de pertinence, docs/EVAL.md §5."""
    hits = hits if hits is not None else index.search(q, k=top)
    if not hits:
        return float("-inf")
    return max(_cross_scores(q, [encoded_text(h) for h in hits[:top]], index.rerank_model))


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


_NUMBER = re.compile(r"\d+(?:[.,]\d+)*")
_THOUSANDS = re.compile(r"(?<![\d.,])(\d{1,3})((?:[    ]\d{3})+)(?![\d.,])")
_ELISION = re.compile(r"…|\.\.\.|\[\.\.\.\]")


def number_tokens(text):
    """Nombres d'un texte, dans l'ordre : « 143,927 » et « 143 927 » → « 143927 »."""
    for a, b in _LIGATURES.items():
        text = text.replace(a, b)
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"(\d)-\s+(\d)", r"\1\2", text)  # césure au milieu d'un nombre
    text = _THOUSANDS.sub(lambda m: m.group(1) + re.sub(r"\D", "", m.group(2)), text)
    out = []
    for tok in _NUMBER.findall(text):
        if re.fullmatch(r"\d{1,3}(,\d{3})+(\.\d+)?", tok):
            tok = tok.replace(",", "")
        out.append(tok)
    return out


def numbers_match(text, quote):
    """Les nombres de la citation sont-ils ceux du passage, dans le même ordre ?

    La citation est découpée sur les ellipses (« … ») ; les nombres de chaque morceau doivent
    former une suite contiguë des nombres du passage. Un morceau peut commencer ou finir au
    milieu d'un nombre (« 5 W » tiré de « 3.5 W ») : suffixe et préfixe tolérés aux bords."""
    ref = number_tokens(text)
    for part in _ELISION.split(quote):
        toks = number_tokens(part)
        if not toks:
            continue
        n = len(toks)
        # un nombre n'est peut-être coupé que s'il touche le bord du morceau
        cut_start = part.strip()[:1].isdigit()
        cut_end = part.strip().rstrip(".,;:)»\"'")[-1:].isdigit()

        def same(tok, full, first, last):
            return (tok == full or (first and cut_start and full.endswith(tok))
                    or (last and cut_end and full.startswith(tok)))

        def fits(i):
            window = ref[i:i + n]
            return len(window) == n and all(same(t, w, j == 0, j == n - 1)
                                            for j, (t, w) in enumerate(zip(toks, window)))

        if not any(fits(i) for i in range(len(ref))):
            return False
        # chaque nombre avec ses mots voisins : « Section 2 reviews » ne vaut pas « Section 3
        # reviews », même si le passage contient un 3 ailleurs
        words = part.split()
        norm = normalize(text)
        for i, w in enumerate(words):
            if any(ch.isdigit() for ch in w) and normalize(" ".join(words[max(0, i - 1):i + 2])) not in norm:
                return False
    return True


def verify(index, chunk_id, quote, expect_sha=None):
    """Statut d'une citation : OK, APPROX, ABSENT ; NOMBRES si le texte ressemble mais que ses
    nombres diffèrent de ceux du passage ; MODIFIÉ si le sha1 attendu ne correspond pas.

    Renvoie (statut, ratio, chunk_id où la citation est trouvée). Une citation absente du
    passage indiqué (ou dont les nombres n'y correspondent pas) est cherchée dans le reste du
    papier : le chunk_id renvoyé le dit.
    """
    c = index.chunks[index.by_id[chunk_id]]
    if expect_sha and not c["sha1"].startswith(expect_sha):
        return "MODIFIÉ", 0.0, chunk_id
    r = match_ratio(c["text"], quote)
    same_numbers = numbers_match(c["text"], quote)
    if r < VERIFY_MIN or not same_numbers:
        for other in index.chunks:
            if other["paper_id"] == c["paper_id"] and other["chunk_id"] != chunk_id:
                r2 = match_ratio(other["text"], quote)
                if r2 >= VERIFY_MIN and (r2 > r or not same_numbers) and numbers_match(other["text"], quote):
                    return ("OK" if r2 == 1.0 else "APPROX"), r2, other["chunk_id"]
    if r >= VERIFY_MIN and not same_numbers:
        return "NOMBRES", r, chunk_id
    status = "OK" if r == 1.0 else "APPROX" if r >= VERIFY_MIN else "ABSENT"
    return status, r, chunk_id


# ----------------------------------------------------------------- évaluation

def evaluate(index, questions, k=5, modes=MODES):
    """recall@k (au moins une section attendue dans les k premiers), MRR, paper@k."""
    out = {}
    for mode in modes:
        base, _, rr_flag = mode.partition("+")
        if base != "lexical" and not index.dense:
            continue
        hits = rr = paper_hits = 0
        misses = []
        for q in questions:
            exp = set(q["expect"])
            res = index.search(q["q"], k=max(k, 10), mode=base, rerank=bool(rr_flag))
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
