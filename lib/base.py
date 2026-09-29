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
            "title_topic_re": "", "topic_min_hits": 2, "tag_rules": [], "plot_tasks": []}


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
             *(r[0] for r in cfg["tag_rules"]), *(r[1] for r in cfg["plot_tasks"])]
    for rx in rules:
        try:
            re.compile(rx)
        except re.error as e:
            raise ValueError(f"{path} : regex invalide {rx!r} : {e}") from None
    return cfg


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
