"""Registre des bases de l'utilisateur : nom → dossier (DATA_MODEL §11).

Fichier ~/.config/pdb/bases.json (ou $PDB_REGISTRY) :
  {"default": "fpga", "bases": {"fpga": "/…/PaperDatabase/bases/fpga", "drone": "/…/PaperDatabase/bases/drone"}}
Le registre ne contient que des chemins ; oublier une base ne supprime aucun fichier.
"""
import json
import os
import re
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9][a-z0-9_-]*$")


def path(env=None):
    env = os.environ if env is None else env
    if env.get("PDB_REGISTRY"):
        return Path(env["PDB_REGISTRY"]).expanduser()
    return Path(env.get("XDG_CONFIG_HOME") or Path.home() / ".config") / "pdb" / "bases.json"


def load(env=None):
    p = path(env)
    if not p.is_file():
        return {"default": None, "bases": {}}
    d = json.loads(p.read_text(encoding="utf-8"))
    return {"default": d.get("default"), "bases": dict(d.get("bases") or {})}


def save(reg, env=None):
    p = path(env)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(reg, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def resolve(name, env=None):
    """Dossier de la base `name`, ou None si elle n'est pas enregistrée."""
    d = load(env)["bases"].get(name)
    return Path(d) if d else None


def default(env=None):
    reg = load(env)
    return Path(reg["bases"][reg["default"]]) if reg["default"] in reg["bases"] else None


def name_of(root, env=None):
    """Nom enregistré d'un dossier de base, ou None."""
    root = Path(root).resolve()
    return next((n for n, d in load(env)["bases"].items() if Path(d).resolve() == root), None)


def all_bases(env=None):
    return [(n, Path(d)) for n, d in sorted(load(env)["bases"].items())]


def register(name, root, env=None):
    if not NAME_RE.match(name):
        raise ValueError(f"nom de base invalide : {name!r} (minuscules, chiffres, - et _)")
    root = Path(root).expanduser().resolve()
    if not (root / "base.json").is_file():
        raise ValueError(f"{root} n'est pas une base (base.json absent)")
    reg = load(env)
    other = name_of(root, env)
    if other and other != name:
        raise ValueError(f"{root} est déjà enregistrée sous le nom {other!r}")
    reg["bases"][name] = str(root)
    if reg["default"] not in reg["bases"]:
        reg["default"] = name
    save(reg, env)
    return root


def forget(name, env=None):
    reg = load(env)
    if name not in reg["bases"]:
        raise KeyError(name)
    del reg["bases"][name]
    if reg["default"] == name:
        reg["default"] = next(iter(sorted(reg["bases"])), None)
    save(reg, env)


def set_default(name, env=None):
    reg = load(env)
    if name not in reg["bases"]:
        raise KeyError(name)
    reg["default"] = name
    save(reg, env)
