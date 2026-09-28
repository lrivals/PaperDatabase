"""Banc d'évaluation du logiciel : extraction, recherche de passages, vérification, temps.

Sans LLM ni réseau, sur le corpus réel ; rien n'est écrit dans papers/ ni dans .cache/rag/.
Chaque volet renvoie un dict de métriques ; `flatten` les met à plat (clés pointées) pour
l'enregistrement dans eval/results/ et la comparaison entre deux runs. Protocole et lecture
des résultats : docs/EVAL.md.

- extraction : couverture du texte (couche texte PyMuPDF vs fulltext.md), ligatures,
  tableaux, structure ; en-tête GROBID vs metadata.json ; valeurs de benchmarks.csv
  retrouvées dans le tableau cité.
- rag : recall@5/@10, MRR, nDCG@10, paper@5 par mode et par jeu (dev, holdout, fr) ;
  alerte « pertinence faible » sur questions hors corpus ; vérification de citations.
- speed : extraction hors GROBID, encodage, recherche à chaud, commandes CLI à froid.
"""
import csv
import json
import math
import random
import re
import statistics
import subprocess
import sys
import time
import unicodedata
from collections import Counter
from pathlib import Path

from lib import docling_tables, tables

RAG_SETS = ("rag_eval", "rag_eval_holdout", "rag_eval_fr")
# questions hors corpus : calibration du seuil de pertinence faible, puis validation
NEG_SETS = ("rag_eval_neg", "rag_eval_neg_holdout")
K = 5
# Colonnes numériques de benchmarks.csv cherchées dans le tableau cité.
BENCH_VALUES = ("accuracy_value", "fps", "gops", "latency_ms", "power_w", "luts", "dsps", "bram")


# ------------------------------------------------------------------ emplacements

def paths(root, code):
    """(fixtures, results, thresholds) du banc pour la base `root`.

    Une base qui a ses propres questions les met dans eval/fixtures/ ; sinon (base fpga) les
    jeux de tests/fixtures/ du code. Les runs sont enregistrés dans
    eval/results/ de la base ; les seuils viennent de son eval/thresholds.json, à défaut de
    celui du code.
    """
    root, code = Path(root), Path(code)
    fixtures = root / "eval" / "fixtures"
    thresholds = root / "eval" / "thresholds.json"
    return (fixtures if fixtures.is_dir() else code / "tests" / "fixtures",
            root / "eval" / "results",
            thresholds if thresholds.is_file() else code / "eval" / "thresholds.json")


# ------------------------------------------------------------------ utilitaires

def load_jsonl(path):
    return [json.loads(l) for l in Path(path).read_text().splitlines() if l.strip()]


def _papers(root):
    return sorted(p for p in (Path(root) / "papers").iterdir() if (p / "metadata.json").exists())


def _sections(folder):
    path = folder / "sections.jsonl"
    return load_jsonl(path) if path.exists() else []


def fold(s):
    """Minuscules, sans accents ni ligatures (NFKD)."""
    s = unicodedata.normalize("NFKD", s or "")
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


_WORD4 = re.compile(r"[a-z]{4,}")


def word_counts(text):
    return Counter(_WORD4.findall(fold(text)))


def coverage(reference, candidate):
    """Part des occurrences de mots (≥ 4 lettres) de `reference` retrouvées dans `candidate`."""
    ref, cand = word_counts(reference), word_counts(candidate)
    total = sum(ref.values())
    return sum(min(n, cand[w]) for w, n in ref.items()) / total if total else None


_TABLE_REF = re.compile(r"(?i)\btables?\s+([A-Z]?\d+|[IVXL]+)\b")
_NOT_TABLE = re.compile(r"§|fig|abstract|section|text|eq", re.I)
_TABLE_LABEL = re.compile(r"(?i)^\s*table\s*([A-Z]?\d+|[IVXL]+)\b")


def cited_tables(source_section):
    """« Table 3, Table 4, §5.2 » → {3, 4} ; « Table II » → {2}."""
    return {n for n in (tables.number(m) for m in _TABLE_REF.findall(source_section or "")) if n}


_NUM = re.compile(r"(?<![\w.])-?\d[\d,  ]*(?:\.\d+)?")


def numbers(text):
    """Nombres d'un texte, séparateurs de milliers retirés (« 12,345 » → 12345.0)."""
    out = set()
    for m in _NUM.finditer(text or ""):
        raw = m.group().strip().replace(" ", "").replace(" ", "")
        if re.fullmatch(r"-?\d{1,3}(,\d{3})+(\.\d+)?", raw):
            raw = raw.replace(",", "")
        for part in raw.split(","):
            try:
                out.add(float(part))
            except ValueError:
                pass
    return out


def value_in(value, found):
    try:
        v = float(value)
    except (TypeError, ValueError):
        return None
    return any(math.isclose(v, x, rel_tol=1e-9, abs_tol=1e-9) for x in found)


def _mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None


# ------------------------------------------------------------------ extraction

SPACED = re.compile(r"\b(?:[A-Z] ){4,}[A-Z]\b")
REFS_HEADING = re.compile(r"(?im)^\s*([\dIVX]+\.?\s*)?(r ?e ?f ?e ?r ?e ?n ?c ?e ?s|bibliography)\s*$")
FIRST_REF = re.compile(r"(?m)^\[1\]\s")


def strip_bibliography(text):
    """Texte sans la bibliographie : coupé au dernier titre « References » (lettres espacées
    comprises), sinon à une ligne « [1] » dans la seconde moitié du texte (liste sans titre)."""
    heads = list(REFS_HEADING.finditer(text))
    if heads:
        return text[:heads[-1].start()]
    firsts = [m for m in FIRST_REF.finditer(text) if m.start() > len(text) / 2]
    return text[:firsts[-1].start()] if firsts else text


def pdf_text(pdf):
    """Couche texte du PDF (PyMuPDF), sans la bibliographie."""
    import pymupdf
    with pymupdf.open(pdf) as doc:
        return strip_bibliography("\n".join(page.get_text() for page in doc))


def extraction_quality(root):
    """Métriques intrinsèques, par papier puis agrégées."""
    from lib import ligatures
    per = {}
    for folder in _papers(root):
        meta = json.loads((folder / "metadata.json").read_text())
        rows = _sections(folder)
        body = "\n".join(r["text"] for r in rows)
        words = sum(len(r["text"].split()) for r in rows)
        tab = [r for r in rows if r["kind"] == "table"]
        with_body = [r for r in tab if len("\n\n".join(r["text"].split("\n\n")[1:])) >= tables.MIN_BODY_CHARS]
        pdf = folder / "paper.pdf"
        cov = None
        if pdf.exists() and (folder / "fulltext.md").exists():
            cov = coverage(pdf_text(pdf), (folder / "fulltext.md").read_text())
        warns = meta.get("extraction", {}).get("warnings", [])
        per[folder.name] = {
            "backend": meta.get("extraction", {}).get("backend"),
            "coverage": cov,
            "words": words,
            "sections": sum(r["kind"] == "section" for r in rows),
            "tables": len(tab),
            "tables_with_body": len(with_body),
            "tables_recovered": sum(tables.RECOVERED_MARK in r["text"] for r in tab),
            "tables_docling": sum(docling_tables.MARK in r["text"] for r in tab),
            "ligature_leftover_per_10k": 1e4 * ligatures.leftover(body) / words if words else None,
            "missed_numbered_sections": any("sections numérotées non détectées" in w for w in warns),
            # titres lettre par lettre (« I N T R O D U C T I O N ») : mise en page mal lue
            "spaced_headings": any(SPACED.search(r["section"] or "") for r in rows),
            "warnings": len([w for w in warns if not w.startswith("axes déduits")]),
        }
    covs = {k: v["coverage"] for k, v in per.items() if v["coverage"] is not None}
    n_tab = sum(v["tables"] for v in per.values())
    worst = sorted(covs, key=covs.get)[:3]
    return {
        "papers": len(per),
        "grobid": sum(v["backend"] == "grobid" for v in per.values()),
        "coverage_mean": _mean(covs.values()),
        "coverage_min": min(covs.values()) if covs else None,
        "coverage_worst": [f"{k} {covs[k]:.3f}" for k in worst],
        "words": sum(v["words"] for v in per.values()),
        "tables": n_tab,
        "tables_with_body_rate": sum(v["tables_with_body"] for v in per.values()) / n_tab if n_tab else None,
        "tables_recovered": sum(v["tables_recovered"] for v in per.values()),
        "tables_docling": sum(v["tables_docling"] for v in per.values()),
        "ligature_leftover_per_10k": _mean(v["ligature_leftover_per_10k"] for v in per.values()),
        "papers_missed_sections": sum(v["missed_numbered_sections"] for v in per.values()),
        "papers_spaced_headings": sum(v["spaced_headings"] for v in per.values()),
        "warnings_per_paper": _mean(v["warnings"] for v in per.values()),
        "per_paper": per,
    }


def _norm_title(s):
    return re.sub(r"[^a-z0-9]", "", fold(s))


def _family(a):
    return re.sub(r"[^a-z]", "", fold(a.get("family") or ""))


def header_accuracy(root):
    """En-tête brut GROBID (lib/tei.parse_header, nettoyage compris) vs metadata.json, qui
    est la référence (vérifié à la main, arXiv, Crossref ou export éditeur)."""
    from lib import tei
    scores = {"title": [], "year": [], "doi": [], "arxiv_id": [], "authors_f1": []}
    errors = []
    for folder in _papers(root):
        path = folder / "grobid.tei.xml"
        if not path.exists():
            continue
        meta = json.loads((folder / "metadata.json").read_text())
        h = tei.parse_header(tei.load(str(path)))
        ok = _norm_title(h["title"]) == _norm_title(meta.get("title"))
        scores["title"].append(ok)
        if not ok:
            errors.append(f"{folder.name} titre : {h['title']!r}")
        if meta.get("year"):
            scores["year"].append(h["year"] == meta["year"])
        for key in ("doi", "arxiv_id"):
            if meta.get(key):
                scores[key].append((h[key] or "").lower() == meta[key].lower())
        gold = Counter(_family(a) for a in meta.get("authors") or [])
        got = Counter(_family(a) for a in h["authors"])
        if gold:
            tp = sum((gold & got).values())
            p = tp / sum(got.values()) if got else 0.0
            r = tp / sum(gold.values())
            scores["authors_f1"].append(2 * p * r / (p + r) if p + r else 0.0)
    out = {k: _mean(map(float, v)) for k, v in scores.items()}
    out["n"] = {k: len(v) for k, v in scores.items()}
    out["title_errors"] = errors
    return out


def table_values(root):
    """Valeurs de benchmarks.csv (relevées à la main dans les papiers) retrouvées telles
    quelles dans le tableau cité par source_section, et ailleurs dans le texte. Une valeur
    convertie par l'auteur de la fiche (unités, moyenne) manque dans les deux.

    Une ligne dont source_section cite aussi de la prose ou une figure (« Table 3, §5.2 »)
    peut tenir sa valeur de là : `table_only` restreint le calcul aux lignes qui ne citent
    que des tableaux, et mesure mieux l'extraction des tableaux (docs/EVAL.md §2)."""
    from lib import query
    short = query.short_ids(query.load_papers(root))
    tables_by_paper, text_by_paper = {}, {}
    for folder in _papers(root):
        rows = _sections(folder)
        text_by_paper[folder.name] = numbers("\n".join(r["text"] for r in rows))
        tabs = {}
        for r in rows:
            m = _TABLE_LABEL.match(r["text"]) if r["kind"] == "table" else None
            n = tables.number(m.group(1)) if m else None
            if n:
                tabs.setdefault(n, set()).update(numbers(r["text"]))
        tables_by_paper[folder.name] = tabs
    n = in_table = in_text = cited_missing = 0
    only = Counter()
    lost = Counter()
    with open(Path(root) / "benchmarks.csv", newline="") as f:
        for row in csv.DictReader(f):
            cited = cited_tables(row["source_section"])
            pid = row["paper_id"]
            if not cited or pid not in tables_by_paper:
                continue
            found = set().union(*(tables_by_paper[pid].get(t, set()) for t in cited))
            if not any(t in tables_by_paper[pid] for t in cited):
                cited_missing += 1
            tables_only = not _NOT_TABLE.search(_TABLE_REF.sub("", row["source_section"]))
            for col in BENCH_VALUES:
                hit = value_in(row.get(col), found)
                if hit is None:
                    continue
                n += 1
                in_table += hit
                anywhere = hit or bool(value_in(row[col], text_by_paper[pid]))
                in_text += anywhere
                if anywhere and not hit:
                    lost[short.get(pid, pid)] += 1
                if tables_only:
                    only["n"] += 1
                    only["hit"] += hit
    return {
        "values": n,
        "in_cited_table": in_table / n if n else None,
        "in_text": in_text / n if n else None,
        "table_only_values": only["n"],
        "table_only_in_cited_table": only["hit"] / only["n"] if only["n"] else None,
        "rows_cited_table_absent": cited_missing,
        "found_outside_table": dict(lost.most_common()),
    }


# ------------------------------------------------------------------------ RAG

def expect_from_pattern(root, papers, pattern, kinds=None):
    """Sections (paper#order) des papiers cibles dont le texte contient le motif : la façon
    dont les attentes des jeux d'évaluation sont construites (docs/RAG.md §10)."""
    rx = re.compile(pattern, re.I)
    out = []
    for folder in _papers(root):
        if not any(p in folder.name for p in papers):
            continue
        for r in _sections(folder):
            if (kinds is None or r["kind"] in kinds) and rx.search(r["text"]):
                out.append(r["id"])
    return out


def ranking_metrics(results, expected, k=K):
    """Pour une question : rang de la 1re section attendue, recall@k, recall@10, nDCG@10
    (gain binaire par section attendue, chaque section comptée une fois)."""
    exp = set(expected)
    seen, gains = set(), []
    for h in results[:10]:
        sid = h["section_id"]
        gains.append(1.0 if sid in exp and sid not in seen else 0.0)
        seen.add(sid)
    ranks = [r for r, h in enumerate(results, 1) if h["section_id"] in exp]
    first = ranks[0] if ranks else None
    dcg = sum(g / math.log2(i + 2) for i, g in enumerate(gains))
    ideal = sum(1 / math.log2(i + 2) for i in range(min(len(exp), 10)))
    exp_papers = {e.split("#")[0] for e in exp}
    return {
        "first": first,
        f"recall@{k}": float(bool(first and first <= k)),
        "recall@10": float(bool(first and first <= 10)),
        "mrr": 1 / first if first else 0.0,
        "ndcg@10": dcg / ideal if ideal else 0.0,
        f"paper@{k}": float(any(h["paper_id"] in exp_papers for h in results[:k])),
    }


def evaluate_set(index, questions, modes, k=K):
    """Métriques moyennes par mode ; misses = questions sans section attendue dans les k."""
    out = {}
    for mode in modes:
        base, _, rr = mode.partition("+")
        if base != "lexical" and not index.dense:
            continue
        per, misses = [], []
        for q in questions:
            res = index.search(q["q"], k=10, mode=base, rerank=bool(rr))
            m = ranking_metrics(res, q["expect"], k)
            per.append(m)
            if not m[f"recall@{k}"]:
                misses.append(q["q"])
        n = len(per) or 1
        out[mode] = {key: sum(m[key] for m in per) / n
                     for key in (f"recall@{k}", "recall@10", "mrr", "ndcg@10", f"paper@{k}")}
        out[mode]["misses"] = misses
    return out


def best_threshold(pos, neg):
    """Seuil t (alerte si score < t) qui maximise l'exactitude équilibrée entre questions du
    corpus (pos) et hors corpus (neg) ; à égalité, le milieu de la plage des seuils optimaux."""
    xs = sorted(set(pos + neg))
    cands = [xs[0] - 1e-6] + [(x + y) / 2 for x, y in zip(xs, xs[1:])] + [xs[-1] + 1e-6]
    acc = [sum(c < t for c in neg) / len(neg) + sum(c >= t for c in pos) / len(pos) for t in cands]
    best = [t for t, a in zip(cands, acc) if a == max(acc)]
    return best[len(best) // 2]


def _rates(pos, neg, t):
    return {"flagged_negatives": sum(c < t for c in neg) / len(neg) if neg else None,
            "flagged_positives": sum(c < t for c in pos) / len(pos) if pos else None}


def relevance_scores(index, questions):
    """Pour chaque question : meilleur cosinus (recherche dense, comme l'alerte actuelle de
    pdb search) et meilleur score du cross-encoder sur les 3 premiers passages hybrides."""
    from lib import rag
    out = {"cos": [], "rerank": []}
    for q in questions:
        hits = index.search(q["q"], k=1, mode="dense")
        out["cos"].append(hits[0]["cos"] if hits else 0.0)
        out["rerank"].append(rag.relevance_score(index, q["q"]))
    return out


def low_relevance(index, cal_pos, cal_neg, val_pos, val_neg, adopt=(0.8, 0.05)):
    """Alerte « pertinence faible » : pour chaque signal (cos, rerank), seuil choisi sur la
    calibration (cal_*), puis taux mesurés sur la validation (val_*), jamais utilisée pour
    choisir. adopt = (hors corpus signalés au moins, questions du corpus signalées au plus),
    en validation : la règle d'adoption fixée avant la mesure (docs/EVAL.md §3)."""
    from lib import rag
    if not index.dense:
        return {"available": False}
    cal_neg = [q for q in cal_neg if not q.get("ambiguous")]
    val_neg = [q for q in val_neg if not q.get("ambiguous")]
    sc = {name: relevance_scores(index, qs) for name, qs in
          (("cal_pos", cal_pos), ("cal_neg", cal_neg), ("val_pos", val_pos), ("val_neg", val_neg))}
    current = {"cos": getattr(rag, "LOW_COS", None), "rerank": getattr(rag, "LOW_RERANK", None)}
    out = {"n": {k: len(v["cos"]) for k, v in sc.items()}}
    for sig in ("cos", "rerank"):
        cp, cn, vp, vn = (sc[k][sig] for k in ("cal_pos", "cal_neg", "val_pos", "val_neg"))
        t = best_threshold(cp, cn)
        val = _rates(vp, vn, t)
        out[sig] = {
            "threshold": t,
            "calibration": _rates(cp, cn, t),
            "validation": val,
            "adopted": val["flagged_negatives"] >= adopt[0] and val["flagged_positives"] <= adopt[1],
            "neg_max": max(cn + vn), "pos_min": min(cp + vp),
            "pos_median": statistics.median(cp + vp), "neg_median": statistics.median(cn + vn),
            "val_negatives_missed": [q["q"] for q, c in zip(val_neg, vn) if c >= t],
            "val_positives_flagged": [q["q"] for q, c in zip(val_pos, vp) if c < t],
        }
        if current[sig] is not None:
            out[sig]["current"] = {"threshold": current[sig], **_rates(cp + vp, cn + vn, current[sig])}
    return out


_SENT = re.compile(r"(?<=[.!?])\s+(?=[A-Z])")


def _sentences(text):
    return [s.strip() for s in _SENT.split(text) if 12 <= len(s.split()) <= 40]


def _swap_digit(s, rng):
    pos = [i for i, c in enumerate(s) if c.isdigit()]
    if not pos:
        return None
    i = rng.choice(pos)
    return s[:i] + str((int(s[i]) + rng.randint(1, 8)) % 10) + s[i + 1:]


def _swap_word(s, rng, vocab):
    ws = s.split()
    idx = [i for i, w in enumerate(ws) if len(w) >= 6 and w.isalpha()]
    if not idx:
        return None
    i = rng.choice(idx)
    ws[i] = rng.choice([v for v in vocab if v.lower() != ws[i].lower()])
    return " ".join(ws)


def verify_cases(index, n=40, seed=0):
    """Citations de test tirées de passages réels : (cas, chunk_id, citation, attendu).
    attendu = True si la citation doit être acceptée (OK ou APPROX dans ce passage)."""
    rng = random.Random(seed)
    pool = [c for c in index.chunks if c["kind"] in ("section", "abstract") and _sentences(c["text"])]
    vocab = ["accuracy", "latency", "throughput", "memory", "bandwidth", "pipeline", "dataset",
             "gradient", "detector", "quantized", "platform", "hardware"]
    cases = []
    for c in rng.sample(pool, min(n, len(pool))):
        s = rng.choice(_sentences(c["text"]))
        cases.append(("exact", c["chunk_id"], s, True))
        cases.append(("mot remplacé", c["chunk_id"], _swap_word(s, rng, vocab), False))
        num = [x for x in _sentences(c["text"]) if re.search(r"\d", x)]
        if num:
            cases.append(("chiffre modifié", c["chunk_id"], _swap_digit(rng.choice(num), rng), False))
        others = [o for o in pool if o["paper_id"] != c["paper_id"]]
        if others:
            other = rng.choice(others)
            cases.append(("autre papier", c["chunk_id"], rng.choice(_sentences(other["text"])), False))
    return [x for x in cases if x[2]]


def verify_accuracy(index, n=40, seed=0):
    """Statuts de rag.verify par type de cas. « accepté » = ce que pdb verify renvoie avec le
    code 0 : OK ou APPROX, dans le passage indiqué."""
    from lib import rag
    by_case = {}
    for case, cid, quote, _ in verify_cases(index, n, seed):
        status, _, where = rag.verify(index, cid, quote)
        accepted = status in ("OK", "APPROX") and where == cid
        d = by_case.setdefault(case, {"n": 0, "accepted": 0, "status": Counter()})
        d["n"] += 1
        d["accepted"] += accepted
        d["status"][status] += 1
    return {case: {"n": d["n"], "accepted_rate": d["accepted"] / d["n"], "status": dict(d["status"])}
            for case, d in by_case.items()}


def rag_quality(root, fixtures, modes=None, verify_n=40):
    from lib import rag
    modes = modes or rag.MODES + ("hybrid+rerank",)
    index = rag.Index(root, rerank="hybrid+rerank" in modes)
    out = {"passages": len(index.chunks), "model": index.model, "dense": index.dense, "sets": {}}
    sets = {}
    for name in RAG_SETS + NEG_SETS:
        path = Path(fixtures) / f"{name}.jsonl"
        if path.exists():
            sets[name] = load_jsonl(path)
    for name in RAG_SETS:
        if name in sets:
            out["sets"][name] = {"n": len(sets[name]), **evaluate_set(index, sets[name], modes)}
    if all(name in sets for name in ("rag_eval", "rag_eval_holdout") + NEG_SETS):
        out["low_relevance"] = low_relevance(index, sets["rag_eval"], sets[NEG_SETS[0]],
                                             sets["rag_eval_holdout"], sets[NEG_SETS[1]])
    out["verify"] = verify_accuracy(index, n=verify_n)
    return out


# ---------------------------------------------------------------------- temps

def _timed(fn, repeat=3):
    ts = []
    for _ in range(repeat):
        t = time.perf_counter()
        fn()
        ts.append(time.perf_counter() - t)
    return statistics.median(ts)


def _pct(xs, p):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(round(p / 100 * (len(xs) - 1))))]


def speed(root, fixtures, encode_n=200, cli=True):
    """Temps médians (s). L'extraction est rejouée en mémoire (TEI → blocs, ligatures,
    tableaux, rendu) sans rien écrire ; GROBID lui-même n'est pas chronométré (serveur)."""
    from lib import doc, embed, ligatures, pdftext, query, rag, tei
    root = Path(root)
    short = query.short_ids(query.load_papers(root))
    out = {}
    folders = [f for f in _papers(root) if (f / "grobid.tei.xml").exists() and (f / "paper.pdf").exists()]
    folders.sort(key=lambda f: (f / "paper.pdf").stat().st_size)
    sample = [folders[0], folders[len(folders) // 2], folders[-1]] if folders else []
    vocab = ligatures.corpus_vocabulary(root)

    def extract(folder):
        header, blocks, refs = tei.parse(str(folder / "grobid.tei.xml"))
        ligatures.repair_blocks(blocks, vocab)
        tables.recover(folder / "paper.pdf", blocks)
        doc.render_fulltext({"id": folder.name, "title": header["title"], "year": header["year"],
                             "extraction": {"backend": "grobid"}}, blocks)
        doc.to_sections(folder.name, blocks)

    out["extract_s"] = {short.get(f.name, f.name): _timed(lambda f=f: extract(f)) for f in sample}
    out["pymupdf_fallback_s"] = {short.get(f.name, f.name): _timed(lambda f=f: pdftext.extract(f / "paper.pdf"))
                                 for f in sample}

    t = time.perf_counter()
    index = rag.Index(root, rerank=True)
    out["index_load_s"] = time.perf_counter() - t
    out["passages"] = len(index.chunks)
    cache = rag._cache_path(root, index.model)
    out["cache_mb"] = cache.stat().st_size / 1e6 if cache.exists() else None

    if index.dense:
        texts = [rag.encoded_text(c) for c in index.chunks[:encode_n]]
        embed._encode(texts[:4], index.model)  # chargement du modèle hors mesure
        t = time.perf_counter()
        embed._encode(texts, index.model)
        dt = time.perf_counter() - t
        out["encode_passages_per_s"] = len(texts) / dt
        out["full_encode_estimate_s"] = len(index.chunks) * dt / len(texts)

    qs = [q["q"] for q in load_jsonl(Path(fixtures) / "rag_eval.jsonl")]
    for mode in (rag.MODES + ("hybrid+rerank",) if index.dense else ("lexical",)):
        base, _, rr = mode.partition("+")
        index.search(qs[0], mode=base, rerank=bool(rr))  # préchauffage
        lat = []
        for q in qs:
            t = time.perf_counter()
            index.search(q, k=8, mode=base, rerank=bool(rr))
            lat.append(time.perf_counter() - t)
        out[f"search_{mode}_ms"] = {"p50": 1e3 * _pct(lat, 50), "p95": 1e3 * _pct(lat, 95)}

    cid = index.chunks[len(index.chunks) // 2]["chunk_id"]
    quote = index.chunks[len(index.chunks) // 2]["text"][:120]
    out["verify_ms"] = 1e3 * _timed(lambda: rag.verify(index, cid, quote + " altered"))

    if cli:
        pdb = [sys.executable, str(root / "bin" / "pdb.py")]
        first_paper = next(iter(sorted(short.values())), None)
        commands = {
            "status": ["status"],
            "bench": ["bench", "--cols", "model,fps,power_w", "-n", "5"],
            "paper": ["paper", first_paper] if first_paper else ["paper", "-h"],
            "search": ["search", qs[0]],
            "show": ["show", index.short_chunk_id(cid)],
        }

        def run(a):
            r = subprocess.run(pdb + a, cwd=root, capture_output=True, text=True)
            if r.returncode:
                raise RuntimeError(f"pdb {' '.join(a)} : code {r.returncode}\n{r.stderr[-500:]}")

        out["cli_s"] = {name: _timed(lambda a=a: run(a)) for name, a in commands.items()}
    return out


# ------------------------------------------------------- rapport et comparaison

def flatten(d, prefix=""):
    """{'a': {'b': 1}} → {'a.b': 1}, nombres seulement (listes et textes ignorés)."""
    out = {}
    for k, v in d.items():
        key = f"{prefix}{k}"
        if isinstance(v, dict):
            out.update(flatten(v, key + "."))
        elif isinstance(v, bool):
            out[key] = float(v)
        elif isinstance(v, (int, float)):
            out[key] = v
    return out


def check_thresholds(flat, thresholds):
    """Seuils non atteints : liste de (clé, valeur, borne)."""
    fails = []
    for key, bound in thresholds.items():
        if key.startswith("_"):
            continue
        v = flat.get(key)
        if v is None:
            fails.append((key, None, bound))
        elif "min" in bound and v < bound["min"]:
            fails.append((key, v, bound))
        elif "max" in bound and v > bound["max"]:
            fails.append((key, v, bound))
    return fails


def compare(old, new, ignore=("speed.",), tol=1e-9):
    """Écarts entre deux runs aplatis : [(clé, ancien, nouveau)]. Les temps sont ignorés par
    défaut (bruités) ; les métriques par papier aussi, résumées par les agrégats."""
    diffs = []
    for key in sorted(set(old) | set(new)):
        if key.startswith(ignore) or ".per_paper." in key:
            continue
        a, b = old.get(key), new.get(key)
        if a is None or b is None or abs(a - b) > tol:
            diffs.append((key, a, b))
    return diffs
