"""Séparation code / données : une installation du code sert plusieurs bases (DATA_MODEL §11).

Une base est un dossier qui contient `base.json` (axes du domaine, règles de classement), plus
papers/, inbox/, benchmarks.csv, profile.md… Le code (bin/, lib/, .venv) reste dans CODE ; les
bases versionnées avec lui vivent dans CODE/bases/<nom>/.

Racine des données, dans l'ordre :
1. $PDB_ROOT s'il est défini (`pdb --base <nom>` le fixe) ;
2. $PDB_BASE, nom d'une base du registre (lib/registry.py) ;
3. le premier dossier contenant base.json, en remontant depuis le répertoire courant ;
4. la base par défaut du registre ;
5. REFERENCE, la base de référence livrée avec le dépôt (bases/fpga).

Un dossier sans base.json (corpus de test, `pdb synth`) prend la configuration de REFERENCE.
"""
import json
import os
import re
from pathlib import Path

from lib import registry

CODE = Path(__file__).resolve().parent.parent
REFERENCE = CODE / "bases" / "fpga"
MARKER = "base.json"

REQUIRED = ("name", "axes")
# Clés facultatives : une base neuve n'a que son nom et ses axes ; /base-profile complète
# le reste. topic_re et title_topic_re vides : tout candidat est « dans le sujet ».
DEFAULTS = {"axis_rules": {}, "axis_queries": {}, "hardware_axes": [], "topic_re": "",
            "title_topic_re": "", "topic_min_hits": 2, "tag_rules": [], "plot_tasks": [],
            "plot": {}}

# Bloc `plot` (DATA_MODEL §11.2.1) : réglages de pdb plot propres à la base. Les noms de
# figures et les classes de tâches par défaut vivent ici (pas dans lib/plotdata, qui importe
# schema, qui importe ce module) ; lib/plotfig vérifie que ses FIGURES y correspondent.
PLOT_KEYS = ("tasks", "families", "split_task", "skip", "min_rows", "max_other", "auto")
PLOT_FIGURES = (
    "bench_fps_power", "bench_gops_per_watt", "bench_fpga_resources", "bench_accuracy_fps",
    "bench_accuracy_latency", "bench_quantization", "eval_retrieval", "eval_verify",
    "eval_extraction", "eval_latency", "eval_history", "corpus_years", "corpus_axes",
    "corpus_bench_coverage", "corpus_citations", "corpus_gaps")
# Ordre des règles : la première qui correspond l'emporte (« anomaly detection » → anomalie).
DEFAULT_PLOT_TASKS = (
    ("apprentissage continu", r"continual|incremental"),
    ("anomalie", r"anomaly"),
    ("compression / AE", r"compression|autoencoder"),
    ("détection", r"detection"),
    ("classification", r"classification"),
)


def data_root(env=None, cwd=None):
    env = os.environ if env is None else env
    if env.get("PDB_ROOT"):
        return Path(env["PDB_ROOT"]).expanduser().resolve()
    if env.get("PDB_BASE"):
        d = registry.resolve(env["PDB_BASE"], env)
        if d is None:
            raise SystemExit(f"base inconnue du registre : {env['PDB_BASE']} (pdb base list)")
        return d.resolve()
    here = Path(cwd or Path.cwd()).resolve()
    for d in (here, *here.parents):
        if (d / MARKER).is_file():
            return d
    return (registry.default(env) or REFERENCE).resolve()


def load_config(root, path=None):
    """Configuration de la base `root` (ou du fichier `path`, pour éprouver une proposition)."""
    path = Path(path) if path else Path(root) / MARKER
    if not path.is_file():
        path = REFERENCE / MARKER
    cfg = json.loads(path.read_text(encoding="utf-8"))
    missing = set(REQUIRED) - set(cfg)
    if missing:
        raise ValueError(f"{path} : clés manquantes {sorted(missing)}")
    cfg = {**DEFAULTS, **cfg}
    unknown = (set(cfg["axis_rules"]) | set(cfg["axis_queries"]) | set(cfg["hardware_axes"])) - set(cfg["axes"])
    if unknown:
        raise ValueError(f"{path} : axes non déclarés dans \"axes\" : {sorted(unknown)}")
    rules = [*cfg["axis_rules"].values(), cfg["topic_re"], cfg["title_topic_re"],
             *(r[0] for r in cfg["tag_rules"])]
    for rx in rules:
        try:
            re.compile(rx)
        except re.error as e:
            raise ValueError(f"{path} : regex invalide {rx!r} : {e}") from None
    cfg["plot"] = _plot_config(path, cfg)
    return cfg


def _plot_config(path, cfg):
    """Bloc `plot` validé ; l'ancienne clé plot_tasks tient lieu de plot.tasks."""
    plot = {} if cfg.get("plot") is None else cfg["plot"]
    if not isinstance(plot, dict):
        raise ValueError(f"{path} : plot doit être un objet")
    plot = dict(plot)
    unknown = set(plot) - set(PLOT_KEYS)
    if unknown:
        raise ValueError(f"{path} : clés inconnues dans plot : {sorted(unknown)} "
                         f"(attendues : {', '.join(PLOT_KEYS)})")
    if not plot.get("tasks") and cfg.get("plot_tasks"):
        plot["tasks"] = cfg["plot_tasks"]
    for key in ("tasks", "families"):
        for rule in plot.get(key) or ():
            if not (isinstance(rule, (list, tuple)) and len(rule) == 2):
                raise ValueError(f"{path} : plot.{key} : [libellé, regex] attendu, pas {rule!r}")
            try:
                re.compile(rule[1])
            except re.error as e:
                raise ValueError(f"{path} : plot.{key} : regex invalide {rule[1]!r} : {e}") from None
    figs = [*(plot.get("skip") or ()), *(plot.get("min_rows") or {})]
    bad = [f for f in figs if f not in PLOT_FIGURES]
    if bad:
        raise ValueError(f"{path} : plot : figure(s) inconnue(s) {bad} (pdb plot --list)")
    labels = [label for label, _ in plot.get("tasks") or DEFAULT_PLOT_TASKS]
    if "split_task" in plot and plot["split_task"] not in labels:
        raise ValueError(f"{path} : plot.split_task {plot['split_task']!r} n'est pas une classe "
                         f"de tâche ({', '.join(labels)})")
    if not isinstance(plot.get("auto", True), bool):
        raise ValueError(f"{path} : plot.auto doit valoir true ou false")
    mo = plot.get("max_other", 0.10)
    if not isinstance(mo, (int, float)) or not 0 <= mo <= 1:
        raise ValueError(f"{path} : plot.max_other doit être une part entre 0 et 1")
    return plot


# --- classement d'un texte selon les règles d'une base --------------------------------

SURVEY_RE = r"\bsurvey|\breview\b|\boverview\b|state of the art\b"  # titre et mots-clés seulement
# La version de YOLO est commune à toutes les bases ; les autres étiquettes viennent de base.json.
YOLO_TAG = (r"\byolo ?v?(\d+)(-?tiny)?", lambda m: f"yolov{m.group(1)}" + ("-tiny" if m.group(2) else ""))


def classify(cfg, text, title_kw=""):
    """(axes, tags) d'un texte (titre + résumé) selon axis_rules et tag_rules de cfg."""
    axes = [a for a, rx in cfg["axis_rules"].items() if re.search(rx, text, re.IGNORECASE)]
    if "surveys" in cfg["axes"] and re.search(SURVEY_RE, title_kw, re.IGNORECASE):
        axes.insert(0, "surveys")
    tags = []
    for rx, name in (YOLO_TAG, *(tuple(r) for r in cfg["tag_rules"])):
        for m in re.finditer(rx, text, re.IGNORECASE):
            t = name(m) if callable(name) else name
            if t not in tags:
                tags.append(t)
            if not callable(name):
                break
    return axes, tags


def in_topic(cfg, title, text, axes):
    """Dans le sujet de la base : axe « matériel », titre explicite, ou mentions répétées de
    topic_re (DATA_MODEL §10). Sans topic_re ni title_topic_re, tout est dans le sujet."""
    if not (cfg["topic_re"] or cfg["title_topic_re"] or cfg["hardware_axes"]):
        return True
    return (bool(set(axes) & set(cfg["hardware_axes"]))
            or bool(cfg["title_topic_re"] and re.search(cfg["title_topic_re"], title or "", re.IGNORECASE))
            or bool(cfg["topic_re"]
                    and len(re.findall(cfg["topic_re"], text, re.IGNORECASE)) >= cfg["topic_min_hits"]))


ROOT = data_root()
CONFIG = load_config(ROOT)
