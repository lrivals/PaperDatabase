"""Génération des figures de pdb plot et mise à jour de figures/manifest.json.

Partagé par `bin/pdb plot` et par la régénération automatique des figures périmées
(`bin/reindex.py` après un ajout d'article, `pdb eval --save`). matplotlib n'est importé
qu'au moment de tracer : `render` lève ImportError s'il manque.
"""
import json
import os
import time
from datetime import datetime
from pathlib import Path

from lib import base, plotdata


def group_of(name):
    return name.split("_")[0]


def load_manifest(out):
    path = Path(out) / "manifest.json"
    try:
        return json.loads(path.read_text()) if path.exists() else {}
    except (OSError, json.JSONDecodeError):
        return {}


def render(root, names, out=None, fmt=None, log=print, err=print):
    """Trace les figures `names` de la base `root` dans `out` (figures/ par défaut).

    fmt : png | pdf | svg ; None = le format déjà enregistré pour la figure dans le manifest,
    sinon png. Une figure sans données (LookupError) est inscrite au manifest comme
    `skipped` ; une figure cassée n'empêche pas les autres. Renvoie
    {"ok": [noms], "skipped": {nom: raison}, "failed": {nom: erreur}}."""
    from lib import plotfig
    import matplotlib.pyplot as plt

    root = Path(root)
    out = Path(out) if out else root / "figures"
    out.mkdir(parents=True, exist_ok=True)
    manifest = load_manifest(out)
    ctx = plotfig.Context(root)
    h = plotdata.config_hash(ctx.cfg)
    res = {"ok": [], "skipped": {}, "failed": {}}
    for n in names:
        g, fn, desc = plotfig.FIGURES[n]
        try:
            fig, info = fn(ctx)
        except LookupError as e:
            log(f"-  {n} : ignorée ({e})")
            manifest[n] = {"group": g, "description": desc, "skipped": str(e),
                           "checked": time.time(), "config_hash": h}
            res["skipped"][n] = str(e)
            continue
        except Exception as e:  # noqa: BLE001  une figure cassée n'empêche pas les autres
            err(f"!  {n} : échec ({type(e).__name__}: {e})")
            res["failed"][n] = f"{type(e).__name__}: {e}"
            continue
        ext = fmt or Path((manifest.get(n) or {}).get("file") or f"{n}.png").suffix[1:] or "png"
        path = out / f"{n}.{ext}"
        fig.savefig(path, dpi=200 if ext == "png" else None, bbox_inches="tight")
        plt.close(fig)
        manifest[n] = {"file": path.name, "group": g, "description": desc,
                       "generated": datetime.now().isoformat(timespec="seconds"),
                       "config_hash": h, **info}
        try:
            shown = path.relative_to(root)
        except ValueError:
            shown = path
        log(f"ok {shown}")
        res["ok"].append(n)
    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + "\n")
    return res


def stale(root, groups=None, cfg=None):
    """{figure: raison} des figures périmées de la base (hors plot.skip), limitées à `groups`."""
    root = Path(root)
    cfg = cfg or base.load_config(root)
    skip = set(cfg["plot"].get("skip") or ())
    names = {n: group_of(n) for n in base.PLOT_FIGURES
             if n not in skip and (groups is None or group_of(n) in groups)}
    out = root / "figures"
    return plotdata.stale_figures(root, out, load_manifest(out), names, cfg)


def auto_enabled(root, cfg=None, env=None):
    """(oui/non, raison) : régénérer automatiquement les figures de cette base ?

    Il faut que la base utilise déjà les figures (figures/manifest.json), que plot.auto ne
    soit pas false et que PDB_NO_PLOT ne soit pas défini (lots, sous-agents)."""
    env = os.environ if env is None else env
    root = Path(root)
    if not (root / "figures" / "manifest.json").exists():
        return False, "pas de figures/manifest.json (premier tracé : bin/pdb plot)"
    if env.get("PDB_NO_PLOT"):
        return False, "PDB_NO_PLOT défini"
    cfg = cfg or base.load_config(root)
    if cfg["plot"].get("auto") is False:
        return False, "plot.auto vaut false dans base.json"
    return True, ""


def refresh(root, groups=None, log=print, err=print):
    """Régénère les figures périmées (de `groups`, toutes par défaut). Renvoie le résultat
    de `render`, avec "stale" ({nom: raison}) ; rien à faire → listes vides."""
    todo = stale(root, groups)
    if not todo:
        return {"ok": [], "skipped": {}, "failed": {}, "stale": {}}
    res = render(root, list(todo), log=log, err=err)
    return {**res, "stale": todo}


def summary(res):
    """« 9 régénérées (bench_fps_power, …), 2 ignorées faute de données, 1 en échec »."""
    parts = []
    if res["ok"]:
        names = ", ".join(res["ok"][:4]) + ("…" if len(res["ok"]) > 4 else "")
        parts.append(f"{len(res['ok'])} régénérée(s) ({names})")
    if res["skipped"]:
        parts.append(f"{len(res['skipped'])} ignorée(s) faute de données")
    if res["failed"]:
        parts.append(f"{len(res['failed'])} en échec ({', '.join(res['failed'])})")
    return ", ".join(parts) or "à jour"


def auto_refresh(root, groups=None, env=None):
    """Après un changement de la base (reindex, pdb eval --save) : régénère les figures
    périmées si auto_enabled, sinon les signale. Ne lève jamais : les figures sont dérivées.

    Renvoie (lignes à afficher, notes) ; les journaux de `render` sont tus."""
    root = Path(root)
    try:
        todo = stale(root, groups)
        if not todo:
            return [], []
        hint = (f"{len(todo)} figure(s) périmée(s) ({', '.join(sorted(todo)[:4])}"
                + ("…" if len(todo) > 4 else "") + ") : bin/pdb plot --stale")
        ok, why = auto_enabled(root, env=env)
        if not (root / "figures" / "manifest.json").exists():
            return [], []                   # base sans figures : rien à signaler
        if not ok:
            return [], [f"{hint} (régénération auto désactivée : {why})"]
        try:
            res = render(root, list(todo), log=lambda m: None, err=lambda m: None)
        except ImportError as e:
            return [], [f"{hint} — matplotlib absent ({e}) : requirements-plot.txt"]
        notes = [f"figure {n} en échec : {e}" for n, e in res["failed"].items()]
        return [f"Figures : {summary(res)}."], notes
    except Exception as e:  # noqa: BLE001
        return [], [f"figures non régénérées : {type(e).__name__}: {e}"]
