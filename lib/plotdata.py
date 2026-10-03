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

from lib import base, query, schema

NR = schema.NR

# ------------------------------------------------------------ familles de plateformes

# Ordre = ordre des couleurs dans les figures (la couleur suit l'entité, jamais le rang).
# Le premier motif qui correspond l'emporte : Hailo / NCS2 avant « Raspberry Pi ».
FAMILIES = ("FPGA", "GPU embarqué", "NPU / VPU", "MCU", "CPU", "GPU bureau", "ASIC", "SoC mobile")
OTHER = "autre"                     # plateforme nommée mais non classée
PLATFORM_NR = "plateforme non rapportée"   # platform n/r : papier algorithmique, simulation…
_FAMILY_RULES = (
    ("NPU / VPU", r"hailo|myriad|\bncs2?\b|movidius|edge ?tpu|coral"),
    ("GPU embarqué", r"jetson|\borin\b|\bxavier\b"),
    ("FPGA", r"zynq|pynq|virtex|kintex|artix|alveo|kria|\bkv260\b|\bzcu\d|ultra96|"
             r"\bvcu\d|aws f1|polarfire|stratix|arria|agilex|cyclone|versal|"
             r"\bxc[a-z0-9]|\bxcu\d|ultrascale"),
    ("MCU", r"stm32|cortex-m|\bgap\d|apollo\d|max78000|pulp|\bmcu\b|nrf52|esp32"),
    ("ASIC", r"\basic\b"),
    ("GPU bureau", r"geforce|\brtx\b|\bgtx\b|tesla|a100|v100|quadro|nvidia t4\b|\bmx\d{3}\b|colab"),
    ("SoC mobile", r"snapdragon|pixel|android|hexagon|smartphone|exynos|helio"),
    ("CPU", r"core i\d|\bi[3579][- ]\d|xeon|epyc|ryzen|raspberry pi|cortex-a"),
)


def family_rules(cfg):
    """Règles du code, puis celles de la base (plot.families) : une règle de base ne classe
    que ce que le code laisse en « autre »."""
    return (*_FAMILY_RULES, *(tuple(r) for r in (cfg.get("plot") or {}).get("families") or ()))


def families(rules=None):
    """Libellés des familles dans l'ordre des légendes : celles du code, puis les nouvelles
    de la base (sans OTHER ni PLATFORM_NR)."""
    extra = [f for f, _ in rules or () if f not in FAMILIES]
    return (*FAMILIES, *dict.fromkeys(extra))


def platform_family(platform, rules=None):
    """Famille matérielle d'une plateforme décrite en texte libre (« autre » sinon ;
    PLATFORM_NR quand la plateforme n'est pas rapportée, même précisée : « n/r (PC) »)."""
    s = (platform or "").lower().strip()
    if not s or s.startswith(NR):
        return PLATFORM_NR
    for family, pattern in rules or _FAMILY_RULES:
        if re.search(pattern, s, re.IGNORECASE):
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


# Classes de tâches par défaut (lib/base) ; une base peut donner les siennes (plot.tasks).
DEFAULT_TASKS = base.DEFAULT_PLOT_TASKS
TASKS = ("détection", "classification", "anomalie", "compression / AE", "apprentissage continu")


def task_rules(cfg):
    """Règles de tâches d'une base : plot.tasks (ou l'ancien plot_tasks), sinon DEFAULT_TASKS."""
    rules = (cfg.get("plot") or {}).get("tasks") or cfg.get("plot_tasks") or ()
    return tuple((label, rx) for label, rx in rules) or DEFAULT_TASKS


def task_labels(tasks=None):
    """Libellés des classes de tâches, dans l'ordre d'affichage."""
    return TASKS if tasks is None or tasks == DEFAULT_TASKS else tuple(label for label, _ in tasks)


def task_bucket(task, tasks=None):
    s = task or ""
    for label, rx in tasks or DEFAULT_TASKS:
        if re.search(rx, s, re.IGNORECASE):
            return label
    return OTHER


# ------------------------------------------------------------ benchmarks.csv

def numeric(rows, *cols, rules=None):
    """Lignes dont toutes les colonnes données sont chiffrées, avec ces valeurs en float.

    Renvoie (points, n_gardées, n_total) ; chaque point est la ligne complétée de
    `_v` (dict col → float) et `_family` (familles selon `rules`, family_rules d'une base)."""
    points = []
    for r in rows:
        vals = {c: query.to_float(r.get(c)) for c in cols}
        if all(v is not None for v in vals.values()):
            points.append({**r, "_v": vals, "_family": platform_family(r.get("platform"), rules)})
    return points, len(points), len(rows)


def nr_rates(rows, cols):
    """Part des valeurs n/r (ou vides) par colonne, dans l'ordre des colonnes."""
    n = len(rows) or 1
    return {c: sum(1 for r in rows if (r.get(c) or NR).strip() in (NR, "")) / n for c in cols}


def count_by(rows, key):
    return Counter(key(r) for r in rows)


def accuracy_panels(rows, x="fps", min_rows=4, max_panels=4, rules=None):
    """Métriques de précision assez fréquentes (avec la colonne x chiffrée) pour un panneau
    chacune.

    Une métrique = un panneau : on ne compare jamais des métriques différentes sur un même
    axe. Les « métriques » qui n'en sont pas (confiance moyenne) sont écartées."""
    points, _, _ = numeric(rows, "accuracy_value", x, rules=rules)
    by_metric = defaultdict(list)
    for p in points:
        m = p["accuracy_metric"]
        if m == NR or "pas une précision" in m or "non définie" in m:
            continue
        by_metric[m].append(p)
    ranked = sorted(by_metric.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    return [(m, pts) for m, pts in ranked if len(pts) >= min_rows][:max_panels]


# ------------------------------------------------------------ pdb plot --check

MAX_OTHER = 0.10            # part « autre » tolérée par défaut (plot.max_other)
MIN_SUGGEST = 3             # lignes minimales pour proposer une règle
MAX_SUGGEST = 8             # au-delà, /base-profile regroupe à la main
# Mots trop vagues pour nommer une classe de tâche.
_STOP = set("""a an and the of for with on in to via by from per using based
de du des la le les et en sur par pour avec un une au aux
task tasks dense single multi object objects real time real-time onboard on-device
drone drones uav uavs aerial image images video model models
inference test end""".split())
# Familles reconnaissables à un mot générique : proposées pour ce que le code laisse en
# « autre » (une règle de base ne passe qu'après celles du code, elle ne vole rien).
_FAMILY_HINTS = (
    ("neuromorphique", r"neuromorph|loihi|spinnaker|truenorth|akida|dynap"),
    ("GPU bureau", r"\bgpu\b"),
    ("CPU", r"\bcpu\b|\bintel\b|\bamd\b|\barm\b"),
)


def _stem(word):
    for suf in ("ation", "ing", "ion", "es", "s"):
        if word.endswith(suf) and len(word) - len(suf) >= 4:
            return word[: -len(suf)]
    return word


def suggest_task_rules(tasks):
    """Classes de tâches proposées pour des libellés « autre » ({libellé: lignes}).

    Glouton, sans LLM : le mot significatif qui couvre le plus de lignes donne une classe
    (regex = sa racine en début de mot), on retire les lignes couvertes, on recommence.
    Le mot est cherché hors parenthèses (« tracking (SOT) » et « single-object tracking »
    → tracking). Une classe doit couvrir MIN_SUGGEST lignes."""
    left = Counter(tasks)
    out = []
    while left and len(out) < MAX_SUGGEST:
        words = Counter()
        for task, n in left.items():
            core = re.sub(r"\([^)]*\)", " ", task.lower())
            for w in set(re.findall(r"[a-zà-ÿ][a-zà-ÿ0-9]+", core)):
                if w not in _STOP and len(w) > 2:
                    words[_stem(w)] += n
        if not words:
            break
        stem, n = max(words.items(), key=lambda kv: (kv[1], len(kv[0]), kv[0]))
        if n < MIN_SUGGEST:
            break
        rx = r"\b" + re.escape(stem)
        covered = [t for t in left if re.search(rx, re.sub(r"\([^)]*\)", " ", t), re.IGNORECASE)]
        label = Counter({w: c for t in covered for w, c in [(m, left[t]) for m in
                         re.findall(rx + r"[a-zà-ÿ]*", t.lower())]}).most_common(1)
        out.append([label[0][0] if label else stem, rx])
        for t in covered:
            del left[t]
    return out


def suggest_family_rules(platforms):
    """[[famille, regex], …] pour des plateformes « autre » ({libellé: lignes}), et les
    libellés qu'aucun indice ne rattache (à nommer par /base-profile)."""
    out, rest = [], {}
    for plat, n in platforms.items():
        for fam, rx in _FAMILY_HINTS:
            if re.search(rx, plat, re.IGNORECASE):
                if [fam, rx] not in out:
                    out.append([fam, rx])
                break
        else:
            rest[plat] = n
    return out, rest


def bench_figure_rows(rows, cfg):
    """{figure bench_*: lignes qu'elle tracerait} : 0 = figure ignorée faute de données."""
    rules = family_rules(cfg)
    min_rows = (cfg.get("plot") or {}).get("min_rows") or {}
    fpga = [p for p in numeric(rows, "luts", "dsps", rules=rules)[0] if p["_family"] == "FPGA"]
    acc = {name: sum(len(p) for _, p in accuracy_panels(rows, x, min_rows.get(name, dflt),
                                                        rules=rules))
           for name, x, dflt in (("bench_accuracy_fps", "fps", 4),
                                 ("bench_accuracy_latency", "latency_ms", 3))}
    return {"bench_fps_power": numeric(rows, "fps", "power_w")[1],
            "bench_gops_per_watt": numeric(rows, "gops", "power_w")[1],
            "bench_fpga_resources": len(fpga), **acc, "bench_quantization": len(rows)}


def plot_check(rows, cfg, paper=None):
    """Classement des lignes de benchmarks.csv pour les figures d'une base (pdb plot --check).

    `paper` : ne regarder que les lignes de ce papier (fin de /paper-fiche). Renvoie les parts
    « autre » (plateforme, tâche) et n/r, les libellés non classés, les figures bench sans
    données ou écartées (plot.skip), les alertes au-delà de plot.max_other et un bloc `plot`
    proposé (règles actuelles + règles suggérées ; classes de tâches seulement au-delà du
    seuil)."""
    plot = cfg.get("plot") or {}
    rules, tasks = family_rules(cfg), task_rules(cfg)
    sel = [r for r in rows if paper is None or r.get("paper_id") == paper]
    n = len(sel)
    fam = Counter(platform_family(r.get("platform"), rules) for r in sel)
    plat_other = Counter(r["platform"] for r in sel if platform_family(r.get("platform"), rules) == OTHER)
    task_other = Counter(r.get("task") or NR for r in sel if task_bucket(r.get("task"), tasks) == OTHER)
    rate = {"platform_other": fam[OTHER] / n if n else 0.0,
            "platform_nr": fam[PLATFORM_NR] / n if n else 0.0,
            "task_other": sum(task_other.values()) / n if n else 0.0}
    max_other = plot.get("max_other", MAX_OTHER)
    alerts = []
    if paper is None:
        for key, what in (("platform_other", "plateformes"), ("task_other", "tâches")):
            if rate[key] > max_other:
                alerts.append(f"{rate[key]:.0%} des lignes ont des {what} classées « autre » "
                              f"(seuil plot.max_other {max_other:.0%})")
    else:
        alerts += [f"plateforme « {p} » classée « autre » ({c} ligne(s))" for p, c in plat_other.items()]
        alerts += [f"tâche « {t} » classée « autre » ({c} ligne(s))" for t, c in task_other.items()]
    sugg_tasks = suggest_task_rules(task_other)
    sugg_fams, unmatched = suggest_family_rules(plat_other)
    figs = bench_figure_rows(rows, cfg)
    skip = list(plot.get("skip") or ())
    proposed = dict(plot)
    if sugg_tasks and rate["task_other"] > max_other and paper is None:
        current = [list(r) for r in tasks]
        # nouvelles classes avant « détection » / « classification » : plus spécifiques
        generic = [r for r in current if r[0] in ("détection", "classification")]
        proposed["tasks"] = [r for r in current if r not in generic] + sugg_tasks + generic
    if sugg_fams and paper is None:
        proposed["families"] = [list(r) for r in plot.get("families") or ()] + sugg_fams
    if fam.get("FPGA", 0) == 0 and "bench_fpga_resources" not in skip and paper is None:
        proposed["skip"] = skip + ["bench_fpga_resources"]
    return {"rows": n, "families": dict(fam), "rates": rate, "max_other": max_other,
            "platform_other": dict(plat_other.most_common()),
            "task_other": dict(task_other.most_common()),
            "unmatched_platforms": unmatched, "suggest_tasks": sugg_tasks,
            "suggest_families": sugg_fams, "bench_figures": figs, "skip": skip,
            "alerts": alerts, "proposed": proposed}


def config_hash(cfg):
    """Empreinte des réglages qui changent les figures (bloc plot, axes) : manifest.json."""
    import hashlib
    blob = json.dumps({"plot": cfg.get("plot") or {}, "axes": cfg.get("axes")},
                      sort_keys=True, ensure_ascii=False)
    return hashlib.sha1(blob.encode()).hexdigest()[:10]


# Sources de chaque groupe de figures (relatives à la base) : leur date fixe la péremption.
GROUP_SOURCES = {"bench": ("benchmarks.csv", "base.json"),
                 "eval": ("eval/results", "base.json"),
                 "corpus": ("benchmarks.csv", "base.json", "papers")}
# external_refs.csv n'y est pas : reindex le réécrit à chaque passage, depuis papers/.


def _mtime(path):
    """Date de modification la plus récente d'un fichier, ou d'un dossier et de ses fichiers
    de premier et second niveau (papers/<id>/metadata.json)."""
    path = Path(path)
    if not path.exists():
        return 0.0
    if path.is_file():
        return path.stat().st_mtime
    stamps = [path.stat().st_mtime]
    for child in path.iterdir():
        stamps.append(child.stat().st_mtime)
        if child.is_dir():
            stamps += [g.stat().st_mtime for g in child.iterdir() if g.is_file()]
    return max(stamps)


def stale_figures(root, out, manifest, figures, cfg):
    """{figure: raison} des figures à régénérer : jamais tentée, fichier absent, réglages
    changés (config_hash) ou source plus récente que la figure. Une figure ignorée faute de
    données (entrée `skipped` du manifest) est datée par son `checked`. `figures` :
    {nom: groupe}."""
    root, out, h = Path(root), Path(out), config_hash(cfg)
    stamps = {g: max(_mtime(root / s) for s in srcs) for g, srcs in GROUP_SOURCES.items()}
    stale = {}
    for name, group in figures.items():
        entry = manifest.get(name) or {}
        path = out / entry["file"] if entry.get("file") else None
        if not entry:
            stale[name] = "jamais générée"
        elif entry.get("config_hash") != h:
            stale[name] = "réglages de base.json changés"
        elif path is not None and not path.exists():
            stale[name] = "fichier absent"
        elif stamps[group] > (path.stat().st_mtime if path is not None else entry.get("checked", 0)):
            stale[name] = "source plus récente"
    return stale


def plot_json(block):
    """Bloc plot en JSON lisible : une règle [libellé, regex] par ligne."""
    lines = []
    for k, v in block.items():
        if isinstance(v, list) and v and isinstance(v[0], list):
            inner = ",\n".join("      " + json.dumps(r, ensure_ascii=False) for r in v)
            lines.append(f'    "{k}": [\n{inner}\n    ]')
        else:
            lines.append(f'    "{k}": {json.dumps(v, ensure_ascii=False)}')
    return '{\n  "plot": {\n' + ",\n".join(lines) + "\n  }\n}"


# ------------------------------------------------------------ corpus

def corpus_by_year(papers):
    """{année: Counter(type)} ; année inconnue → None."""
    out = defaultdict(Counter)
    for m in papers:
        out[m.get("year")][m.get("type") or NR] += 1
    return dict(out)


def corpus_by_axis(papers, axes=None):
    """{axe: Counter(statut de fiche)} ; un papier compte dans chacun de ses axes."""
    out = {a: Counter() for a in (schema.AXES if axes is None else axes)}
    for m in papers:
        for a in m.get("axes") or []:
            out.setdefault(a, Counter())[(m.get("status") or {}).get("fiche", "todo")] += 1
    return out


def coverage_matrix(rows, papers, col="axis", axes=None, tasks=None, rules=None):
    """Nombre de papiers distincts ayant des benchmarks, par famille × (axe | tâche).

    col="axis" : axes du papier (metadata.json) ; col="task" : classe de tâche de la ligne.
    Renvoie (lignes, colonnes, matrice) ; une cellule à 0 est un gap candidat. Axes et
    tâches : ceux de la base (schema.AXES, DEFAULT_TASKS par défaut)."""
    axes = schema.AXES if axes is None else axes
    axes_of = {m["id"]: m.get("axes") or [] for m in papers}
    cells = defaultdict(set)
    for r in rows:
        fam = platform_family(r.get("platform"), rules)
        keys = axes_of.get(r["paper_id"], []) if col == "axis" else [task_bucket(r.get("task"), tasks)]
        for k in keys:
            cells[(fam, k)].add(r["paper_id"])
    # surveys : pas de mesures propres, une case à 0 n'y serait pas un gap
    cols = [a for a in axes if a != "surveys"] if col == "axis" else list(task_labels(tasks))
    if col == "task" and any(k == OTHER for _, k in cells):
        cols.append(OTHER)
    fams = [f for f in families(rules) if any((f, c) in cells for c in cols)]
    fams += [f for f in (OTHER, PLATFORM_NR) if any((f, c) in cells for c in cols)]
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
