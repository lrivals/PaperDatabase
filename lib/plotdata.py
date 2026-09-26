"""Données des figures de bin/pdb plot : benchmarks.csv, eval/results/*.json, corpus.

Bibliothèque standard seulement (plus lib/query, lib/schema) : tout ce qui se calcule ici
se teste sans matplotlib (tests/test_plot.py). Les figures sont dans lib/plotfig.py.

Règle commune : une valeur n/r n'est jamais tracée ni remplacée ; chaque sélection renvoie
aussi le nombre de lignes gardées sur le total, que la figure affiche.
"""
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from lib import query, schema

NR = schema.NR

# ------------------------------------------------------------ familles de plateformes

# Ordre = ordre des couleurs dans les figures (la couleur suit l'entité, jamais le rang).
# Le premier motif qui correspond l'emporte : Hailo / NCS2 avant « Raspberry Pi ».
FAMILIES = ("FPGA", "GPU embarqué", "NPU / VPU", "MCU", "CPU", "GPU bureau", "ASIC")
OTHER = "autre"
_FAMILY_RULES = (
    ("NPU / VPU", r"hailo|myriad|\bncs2?\b|movidius|edge ?tpu|coral"),
    ("GPU embarqué", r"jetson"),
    ("FPGA", r"zynq|pynq|virtex|kintex|artix|alveo|kria|\bkv260\b|\bzcu\d|ultra96|"
             r"\bvcu\d|aws f1|polarfire|stratix|arria|agilex|cyclone|versal|"
             r"\bxc[a-z0-9]|\bxcu\d|ultrascale"),
    ("MCU", r"stm32|cortex-m|\bgap\d|apollo\d|max78000|pulp|\bmcu\b|nrf52|esp32"),
    ("ASIC", r"\basic\b"),
    ("GPU bureau", r"geforce|\brtx\b|\bgtx\b|tesla|a100|v100|quadro"),
    ("CPU", r"core i\d|xeon|epyc|ryzen|raspberry pi|cortex-a"),
)


def platform_family(platform):
    """Famille matérielle d'une plateforme décrite en texte libre (« autre » sinon)."""
    s = (platform or "").lower()
    if not s or s == NR:
        return OTHER
    for family, pattern in _FAMILY_RULES:
        if re.search(pattern, s):
            return family
    return OTHER


# ------------------------------------------------------------ regroupements de colonnes

QUANT_BUCKETS = ("FP32", "FP16", "≥ 9 bits (fixe)", "8 bits", "3–7 bits", "1–2 bits",
                 "mixte", NR)


def quant_bucket(q):
    """Classe de précision d'une quantification décrite en texte libre (heuristique)."""
    s = (q or "").lower().strip()
    if not s or s.startswith(NR):
        return NR
    s = s.replace("binary hv", "")          # hypervecteurs binaires ≠ poids binaires
    if re.search(r"hgq|hawq|mixed|mixte|hétérogène|heterogene|block-circulant", s) or \
            ("fp" in s and "int" in s):
        return "mixte"
    if "fp32" in s or "float32" in s:
        return "FP32"
    if "fp16" in s:
        return "FP16"
    if re.search(r"\bw1|1-bit|bina(i)?r|ternary|ternaire", s):
        return "1–2 bits"
    # premier nombre de bits cité : celui des tableaux quand le texte en donne un second
    m = re.search(r"(?:int|uint-?|fix|ap_fixed<|\bw)(\d+)|(\d+)(?:[ -]?bits?\b|b\b)", s)
    if not m:
        return "mixte"
    b = int(m.group(1) or m.group(2))
    if b >= 9:
        return "≥ 9 bits (fixe)"
    if b == 8:
        return "8 bits"
    if b >= 3:
        return "3–7 bits"
    return "1–2 bits"


TASKS = ("détection", "classification", "anomalie", "compression / AE", "apprentissage continu")


def task_bucket(task):
    s = (task or "").lower()
    if "continual" in s or "incremental" in s:
        return "apprentissage continu"
    if "anomaly" in s:
        return "anomalie"
    if "compression" in s or "autoencoder" in s:
        return "compression / AE"
    if "detection" in s:
        return "détection"
    if "classification" in s:
        return "classification"
    return OTHER


# ------------------------------------------------------------ benchmarks.csv

def numeric(rows, *cols):
    """Lignes dont toutes les colonnes données sont chiffrées, avec ces valeurs en float.

    Renvoie (points, n_gardées, n_total) ; chaque point est la ligne complétée de
    `_v` (dict col → float) et `_family`."""
    points = []
    for r in rows:
        vals = {c: query.to_float(r.get(c)) for c in cols}
        if all(v is not None for v in vals.values()):
            points.append({**r, "_v": vals, "_family": platform_family(r.get("platform"))})
    return points, len(points), len(rows)


def nr_rates(rows, cols):
    """Part des valeurs n/r (ou vides) par colonne, dans l'ordre des colonnes."""
    n = len(rows) or 1
    return {c: sum(1 for r in rows if (r.get(c) or NR).strip() in (NR, "")) / n for c in cols}


def count_by(rows, key):
    return Counter(key(r) for r in rows)


def accuracy_panels(rows, min_rows=4, max_panels=4):
    """Métriques de précision assez fréquentes (avec FPS) pour un panneau chacune.

    Une métrique = un panneau : on ne compare jamais des métriques différentes sur un même
    axe. Les « métriques » qui n'en sont pas (confiance moyenne) sont écartées."""
    points, _, _ = numeric(rows, "accuracy_value", "fps")
    by_metric = defaultdict(list)
    for p in points:
        m = p["accuracy_metric"]
        if m == NR or "pas une précision" in m or "non définie" in m:
            continue
        by_metric[m].append(p)
    ranked = sorted(by_metric.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    return [(m, pts) for m, pts in ranked if len(pts) >= min_rows][:max_panels]


# ------------------------------------------------------------ corpus

def corpus_by_year(papers):
    """{année: Counter(type)} ; année inconnue → None."""
    out = defaultdict(Counter)
    for m in papers:
        out[m.get("year")][m.get("type") or NR] += 1
    return dict(out)


def corpus_by_axis(papers):
    """{axe: Counter(statut de fiche)} ; un papier compte dans chacun de ses axes."""
    out = {a: Counter() for a in schema.AXES}
    for m in papers:
        for a in m.get("axes") or []:
            out.setdefault(a, Counter())[(m.get("status") or {}).get("fiche", "todo")] += 1
    return out


def coverage_matrix(rows, papers, col="axis"):
    """Nombre de papiers distincts ayant des benchmarks, par famille × (axe | tâche).

    col="axis" : axes du papier (metadata.json) ; col="task" : classe de tâche de la ligne.
    Renvoie (lignes, colonnes, matrice) ; une cellule à 0 est un gap candidat."""
    axes_of = {m["id"]: m.get("axes") or [] for m in papers}
    cells = defaultdict(set)
    for r in rows:
        fam = platform_family(r.get("platform"))
        keys = axes_of.get(r["paper_id"], []) if col == "axis" else [task_bucket(r.get("task"))]
        for k in keys:
            cells[(fam, k)].add(r["paper_id"])
    # surveys : pas de mesures propres, une case à 0 n'y serait pas un gap
    cols = [a for a in schema.AXES if a != "surveys"] if col == "axis" else list(TASKS)
    if col == "task" and any(k == OTHER for _, k in cells):
        cols.append(OTHER)
    fams = [f for f in FAMILIES if any((f, c) in cells for c in cols)]
    if any((OTHER, c) in cells for c in cols):
        fams.append(OTHER)
    matrix = [[len(cells.get((f, c), ())) for c in cols] for f in fams]
    return fams, cols, matrix


def cited_by_counts(papers, citations):
    """[(paper_id, n citants internes)] décroissant, à partir de lib/refs.citations()."""
    _, citers, _ = citations
    ids = {m["id"] for m in papers}
    counts = [(pid, len(citers.get(pid, ()))) for pid in ids]
    return sorted([c for c in counts if c[1] > 0], key=lambda c: (-c[1], c[0]))


def load_external_refs(root, n=15):
    """Les n premières lignes de external_refs.csv (titre, année, n_citers)."""
    import csv
    path = Path(root) / "external_refs.csv"
    if not path.exists():
        return []
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))[:n]
    return [{"title": r["title"], "year": r["year"], "n": int(r["n_citers"])} for r in rows]


# ------------------------------------------------------------ eval/results

VOLETS = ("extraction", "rag", "speed")


def load_eval_runs(results_dir):
    """Runs de pdb eval --save, du plus ancien au plus récent (tri sur date puis nom)."""
    runs = []
    for p in sorted(Path(results_dir).glob("*.json")):
        try:
            d = json.loads(p.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(d.get("results"), dict):
            d["_file"] = p.name
            runs.append(d)
    return sorted(runs, key=lambda d: (d.get("date") or "", d["_file"]))


def latest_eval(runs):
    """{volet: (résultats du volet, run)} pour le run le plus récent qui contient ce volet.

    Les runs sont souvent partiels (--rag seul, --extract seul) : on ne prend pas le dernier
    fichier mais le dernier qui mesure chaque volet."""
    out = {}
    for run in runs:
        for v, res in run["results"].items():
            if res:
                out[v] = (res, run)
    return out


def run_label(run):
    """« 2026-09-26T0140 · 80aa05e (dirty) » : légende de provenance d'une figure."""
    return f"{run.get('date', '?')} · {run.get('commit', '?')}" + (" (dirty)" if run.get("dirty") else "")


def dig(d, path):
    for k in path.split("."):
        if not isinstance(d, dict) or k not in d:
            return None
        d = d[k]
    return d


def eval_history(runs, series):
    """{nom: [(date, valeur)]} pour chaque chemin pointé de `series` ({nom: chemin})."""
    out = {name: [] for name in series}
    for run in runs:
        for name, path in series.items():
            v = dig(run["results"], path)
            if isinstance(v, (int, float)):
                out[name].append((run.get("date") or run["_file"], float(v)))
    return out


def load_thresholds(path):
    try:
        return json.loads(Path(path).read_text())
    except (OSError, json.JSONDecodeError):
        return {}
