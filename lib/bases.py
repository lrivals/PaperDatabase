"""Cycle de vie des bases : création, statistiques, profil, contrôle des règles (DATA_MODEL §11).

Partagé par `pdb base` (bin/bases.py) et l'onglet Bases de bin/viz.py. Toutes les fonctions
prennent le dossier de la base en argument : elles marchent sur une base autre que la base
active. La réindexation passe par un sous-processus, parce que bin/reindex.py et lib/schema.py
figent la base active à l'import.
"""
import csv
import datetime as _dt
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from lib import base, registry, schema, xbase

CODE = base.CODE
TEMPLATES = CODE / "templates"
PROFILE = "profile.md"
GITIGNORE = """**/paper.pdf
**/grobid.tei.xml
inbox/*.pdf
inbox/*.meta.json
inbox/*.bib
inbox/*.ris
__pycache__/
.cache/
candidates.csv
candidates_arxiv.txt
xbase_candidates.csv
# liens vers le code partagé
/.venv
"""


class BaseError(Exception):
    pass


# ---------------------------------------------------------------- création

BASES_DIR = CODE / "bases"   # bases versionnées avec le code (un seul dépôt git)


def default_path(name):
    """Dossier proposé pour une nouvelle base : bases/<nom> du dépôt."""
    return BASES_DIR / name


def create(name, theme, root=None, title=None, env=None, reindex_after=True):
    """Crée une base vide au thème donné et l'enregistre. Retourne son dossier."""
    if not registry.NAME_RE.match(name):
        raise BaseError(f"nom invalide : {name!r} (minuscules, chiffres, - et _)")
    if registry.resolve(name, env):
        raise BaseError(f"une base s'appelle déjà {name!r} (pdb base list)")
    theme = (theme or "").strip()
    if not theme:
        raise BaseError("thème vide : décrire en quelques phrases le sujet de la base")
    root = Path(root).expanduser().resolve() if root else default_path(name)
    if root.exists() and any(root.iterdir()):
        raise BaseError(f"{root} existe et n'est pas vide")
    if (root == CODE or CODE in root.parents) and BASES_DIR not in root.parents:
        raise BaseError(f"dans le dépôt du code, une base se crée sous {BASES_DIR}/")

    title = (title or "").strip() or name
    today = _dt.date.today().isoformat()
    (root / "papers").mkdir(parents=True)
    (root / "inbox").mkdir()
    (root / ".claude").mkdir()
    for link, target in ((root / "bin", CODE / "bin"), (root / ".venv", CODE / ".venv"),
                         (root / ".claude" / "commands", CODE / ".claude" / "commands")):
        link.symlink_to(os.path.relpath(target, link.parent))

    with open(root / "benchmarks.csv", "w", newline="") as f:
        csv.writer(f, lineterminator="\n").writerow(schema.BENCHMARK_COLUMNS)
    (root / "base.json").write_text(json.dumps({"name": title, "axes": {"surveys": "Surveys"}},
                                               ensure_ascii=False, indent=2) + "\n")
    code = os.path.relpath(CODE, root)
    fill = {"name": title, "theme": theme, "date": today, "code": code}
    for tpl, out in (("CLAUDE.base.md", "CLAUDE.md"), ("profile.md", PROFILE)):
        (root / out).write_text((TEMPLATES / tpl).read_text().format(**fill))
    (root / "gaps.md").write_text(f"# Gaps — {title}\n\n_À remplir par `/paper-gaps`._\n")
    (root / "labs.md").write_text(f"# Laboratoires et équipes — {title}\n")
    (root / ".gitignore").write_text(GITIGNORE)

    registry.register(name, root, env)
    if reindex_after:
        reindex(root)
    return root


def reindex(root, quiet=False):
    """bin/reindex.py sur la base `root`, dans un sous-processus (base active = root)."""
    sys.stdout.flush()
    env = {**os.environ, "PDB_ROOT": str(Path(root).resolve())}
    env.pop("PDB_BASE", None)
    r = subprocess.run([sys.executable, str(CODE / "bin" / "reindex.py")], cwd=root, env=env,
                       capture_output=quiet, text=True)
    return r.returncode


# ---------------------------------------------------------------- lecture

def _metas(root):
    out = []
    for p in sorted(Path(root, "papers").glob("*/metadata.json")):
        try:
            out.append(json.loads(p.read_text()))
        except json.JSONDecodeError:
            continue
    return out


def _bench_count(root):
    path = Path(root) / "benchmarks.csv"
    if not path.exists():
        return 0
    with open(path, newline="") as f:
        return sum(1 for _ in csv.DictReader(f))


def pending_suggestions(root):
    """Lignes de la section « Suggestions en attente » de profile.md."""
    return [l.strip() for l in _profile_section(root, "Suggestions en attente").splitlines()
            if l.strip().startswith("- ")]


def _profile_section(root, heading):
    path = Path(root) / PROFILE
    if not path.exists():
        return ""
    m = re.search(rf"^## {re.escape(heading)}[^\n]*\n(.*?)(?=^## |\Z)", path.read_text(),
                  re.MULTILINE | re.DOTALL)
    return m.group(1) if m else ""


def theme(root):
    """Thème donné par l'utilisateur (profile.md), ou le nom de base.json à défaut."""
    t = _profile_section(root, "Thème").strip()
    return t or base.load_config(root)["name"]


def stats(name, root):
    root = Path(root)
    ok = (root / "base.json").is_file()
    cfg = base.load_config(root) if ok else {"name": "?", "axes": {}}
    metas = _metas(root) if ok else []
    stamps = [p.stat().st_mtime for p in (root / "papers").glob("*/metadata.json")] if ok else []
    stamps += [(root / f).stat().st_mtime for f in ("benchmarks.csv", "base.json", PROFILE)
               if (root / f).exists()]
    return {
        "name": name, "title": cfg["name"], "path": str(root), "exists": ok,
        "papers": len(metas),
        "done": sum(1 for m in metas if (m.get("status") or {}).get("fiche") == "done"),
        "imported": sum(1 for m in metas if m.get("imported_from")),
        "benchmarks": _bench_count(root) if ok else 0,
        "axes": len(cfg["axes"]),
        "rules": len(cfg.get("axis_rules") or {}),
        "suggestions": len(pending_suggestions(root)) if ok else 0,
        "profile": (root / PROFILE).exists(),
        "modified": _dt.datetime.fromtimestamp(max(stamps)).strftime("%Y-%m-%d %H:%M") if stamps else "",
    }


def all_stats(env=None):
    reg = registry.load(env)
    return [{**stats(n, Path(d)), "default": n == reg["default"]} for n, d in sorted(reg["bases"].items())]


def info(root):
    """Profil, axes et leurs effectifs, papiers sans axe, suggestions en attente."""
    root = Path(root)
    cfg = base.load_config(root)
    metas = _metas(root)
    counts = {a: sum(1 for m in metas if a in (m.get("axes") or [])) for a in cfg["axes"]}
    return {
        "title": cfg["name"], "path": str(root),
        "theme": theme(root),
        "axes": [(a, t, counts[a], a in cfg["axis_rules"]) for a, t in cfg["axes"].items()],
        "unclassified": [m["id"] for m in metas if not m.get("axes")],
        "imported": [(m["id"], m["imported_from"].get("base")) for m in metas if m.get("imported_from")],
        "suggestions": pending_suggestions(root),
        "has_topic": bool(cfg["topic_re"] or cfg["title_topic_re"]),
    }


def check(root, config=None):
    """Effet des règles de base.json (ou du fichier `config`, une proposition) sur les papiers
    existants, sans rien écrire.

    Retourne {"errors": [...], "changes": [(paper_id, fiche, axes actuels, axes devinés)],
    "axes_without_rule": [...], "out_of_topic": [paper_id…],
    "undeclared": {axe: [paper_id…]}} ; undeclared : axes utilisés par des papiers mais absents
    de la configuration (reindex échouerait : renommer l'axe dans leurs metadata.json)."""
    root = Path(root)
    try:
        if config and not Path(config).is_file():
            raise ValueError(f"{config} introuvable")
        cfg = base.load_config(root, config)
    except (ValueError, json.JSONDecodeError) as e:
        return {"errors": [str(e)], "changes": [], "axes_without_rule": [], "out_of_topic": [],
                "undeclared": {}, "plot": {}}
    changes, out, undeclared = [], [], {}
    for m in _metas(root):
        text = " ".join(filter(None, (m.get("title"), xbase.abstract_of(root / "papers" / m["id"]))))
        axes, _ = base.classify(cfg, text, m.get("title") or "")
        cur = m.get("axes") or []
        for a in cur:
            if a not in cfg["axes"]:
                undeclared.setdefault(a, []).append(m["id"])
        if set(axes) != set(cur):
            changes.append((m["id"], (m.get("status") or {}).get("fiche"), cur, axes))
        if not base.in_topic(cfg, m.get("title"), text, axes):
            out.append(m["id"])
    no_rule = [a for a in cfg["axes"] if a != "surveys" and a not in cfg["axis_rules"]]
    return {"errors": [], "changes": changes, "axes_without_rule": no_rule, "out_of_topic": out,
            "undeclared": undeclared, "plot": _plot_effect(root, cfg, config)}


def _plot_effect(root, cfg, config):
    """Parts « autre » des figures (plotdata.plot_check) avec base.json, et avec la
    proposition `config` s'il y en a une : {"before": …, "after": …, "moved": …} ; moved :
    {(classe avant, classe après): lignes} des tâches déjà classées que la proposition
    déplace (les lignes sorties de « autre » n'y sont pas)."""
    from lib import plotdata, query
    if not (root / "benchmarks.csv").is_file():
        return {}
    _, rows = query.load_benchmarks(root)
    after = plotdata.plot_check(rows, cfg)
    if not config:
        return {"before": after, "after": after, "moved": {}}
    try:
        old = base.load_config(root)
    except ValueError:
        return {"before": after, "after": after, "moved": {}}
    t0, t1 = plotdata.task_rules(old), plotdata.task_rules(cfg)
    moved = {}
    for r in rows:
        a, b = plotdata.task_bucket(r.get("task"), t0), plotdata.task_bucket(r.get("task"), t1)
        if a != b and a != plotdata.OTHER:
            moved[(a, b)] = moved.get((a, b), 0) + 1
    return {"before": plotdata.plot_check(rows, old), "after": after, "moved": moved}
