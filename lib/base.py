"""Séparation code / données : une installation du code sert plusieurs bases (DATA_MODEL §11).

Une base est un dossier qui contient `base.json` (axes du domaine, règles de classement), plus
papers/, inbox/, benchmarks.csv… Le code (bin/, lib/, .venv) reste dans CODE.

Racine des données, dans l'ordre :
1. $PDB_ROOT s'il est défini ;
2. le premier dossier contenant base.json, en remontant depuis le répertoire courant ;
3. CODE (la base livrée avec le dépôt).

Un dossier sans base.json (corpus de test, `pdb synth`) prend la configuration de CODE.
"""
import json
import os
from pathlib import Path

CODE = Path(__file__).resolve().parent.parent
MARKER = "base.json"


def data_root(env=None, cwd=None):
    env = os.environ if env is None else env
    if env.get("PDB_ROOT"):
        return Path(env["PDB_ROOT"]).expanduser().resolve()
    here = Path(cwd or Path.cwd()).resolve()
    for d in (here, *here.parents):
        if (d / MARKER).is_file():
            return d
    return CODE


def load_config(root):
    path = Path(root) / MARKER
    if not path.is_file():
        path = CODE / MARKER
    cfg = json.loads(path.read_text(encoding="utf-8"))
    missing = {"name", "axes", "axis_rules", "axis_queries", "hardware_axes", "topic_re",
               "title_topic_re", "tag_rules"} - set(cfg)
    if missing:
        raise ValueError(f"{path} : clés manquantes {sorted(missing)}")
    unknown = (set(cfg["axis_rules"]) | set(cfg["axis_queries"]) | set(cfg["hardware_axes"])) - set(cfg["axes"])
    if unknown:
        raise ValueError(f"{path} : axes non déclarés dans \"axes\" : {sorted(unknown)}")
    return cfg


ROOT = data_root()
CONFIG = load_config(ROOT)
