"""État de la base et prochaines actions, pour `bin/pdb status`.

collect() lit l'environnement et le corpus ; next_actions() est une fonction pure (testée)
qui en déduit au plus trois actions, par ordre de priorité. Le contrôle de conformité
reste le travail de bin/reindex.py.
"""
import csv
import importlib.util
import json
import re
import shutil
import subprocess
from pathlib import Path

import requests

from lib import schema

GROBID_ALIVE = "http://localhost:8070/api/isalive"
THIN_AXIS = 3          # un axe sous ce nombre de papiers est signalé comme maigre
GAPS_STALE_AFTER = 3   # fiches done plus récentes que gaps.md avant de suggérer /paper-gaps


def _grobid_alive():
    try:
        return requests.get(GROBID_ALIVE, timeout=2).text.strip() == "true"
    except requests.RequestException:
        return False


def _git_dirty(root):
    try:
        r = subprocess.run(["git", "status", "--porcelain"], cwd=root, capture_output=True,
                           text=True, timeout=10)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return len(r.stdout.splitlines()) if r.returncode == 0 else None


def read_gaps(path):
    """(nombre de gaps, nombre au statut « étayé ») d'après les entrées `### ` de gaps.md."""
    if not path.exists():
        return 0, 0
    body = path.read_text().split("\n---\n", 1)[-1]
    entries = re.split(r"^### ", body, flags=re.MULTILINE)[1:]
    backed = sum(1 for e in entries if re.search(r"Statut\s*:\s*étayé", e))
    return len(entries), backed


def collect(root, check_services=True):
    root = Path(root)
    papers = []
    for path in sorted((root / "papers").glob("*/metadata.json")):
        try:
            papers.append(json.loads(path.read_text()))
        except json.JSONDecodeError:
            papers.append({"id": path.parent.name, "broken": True})
    bench = root / "benchmarks.csv"
    n_bench = 0
    if bench.exists():
        with open(bench, newline="") as f:
            n_bench = sum(1 for _ in csv.DictReader(f))
    gaps = root / "gaps.md"
    gaps_mtime = gaps.stat().st_mtime if gaps.exists() else 0
    done = [p for p in papers if (p.get("status") or {}).get("fiche") == "done"]
    done_after_gaps = sum(1 for p in done
                          if (root / "papers" / p["id"] / "fiche.md").exists()
                          and (root / "papers" / p["id"] / "fiche.md").stat().st_mtime > gaps_mtime)
    n_gaps, n_backed = read_gaps(gaps)
    return {
        "venv": (root / ".venv" / "bin" / "python").exists(),
        "viz_deps": importlib.util.find_spec("dash") is not None,
        "embed_deps": importlib.util.find_spec("sentence_transformers") is not None,
        "docker": shutil.which("docker") is not None,
        "grobid": _grobid_alive() if check_services else None,
        "inbox": sorted(p.name for p in (root / "inbox").glob("*.pdf")),
        "n_papers": len(papers),
        "axes": {a: sum(1 for p in papers if a in (p.get("axes") or [])) for a in schema.AXES},
        "todo": sorted(p["id"] for p in papers if (p.get("status") or {}).get("fiche") != "done"),
        "n_done": len(done),
        "extraction_issues": sorted(
            (p["id"], len((p.get("extraction") or {}).get("warnings") or []))
            for p in papers
            if p.get("broken") or not (p.get("extraction") or {}).get("ok", True)),
        "n_bench": n_bench,
        "n_gaps": n_gaps,
        "n_gaps_backed": n_backed,
        "done_after_gaps": done_after_gaps,
        "candidates": (root / "candidates.csv").exists(),
        "git_dirty": _git_dirty(root) if check_services else None,
    }


def next_actions(s, max_n=3):
    """Actions suggérées, de la plus urgente à la moins urgente : (commande, raison)."""
    acts = []
    if not s["venv"]:
        acts.append(("bash bin/setup.sh", "l'environnement Python n'est pas installé"))
    if s["grobid"] is False and s["docker"]:
        acts.append(("bin/pdb grobid start",
                     "GROBID est arrêté : sans lui, l'ingestion passe en repli PyMuPDF (moins fiable)"))
    if s["inbox"]:
        acts.append(("bin/pdb ingest", f"{len(s['inbox'])} PDF en attente dans inbox/"))
    if s["todo"]:
        more = f" (et {len(s['todo']) - 1} autre(s))" if len(s["todo"]) > 1 else ""
        acts.append((f"/paper-fiche {s['todo'][0]}", f"fiche de lecture à rédiger{more}"))
    if s["done_after_gaps"] >= GAPS_STALE_AFTER:
        acts.append(("/paper-gaps", f"{s['done_after_gaps']} fiches rédigées depuis la dernière mise à jour de gaps.md"))
    thin = [a for a, n in s["axes"].items() if n < THIN_AXIS]
    if thin:
        acts.append((f"/paper-discover {thin[0]}",
                     f"axe{'s' if len(thin) > 1 else ''} peu couvert{'s' if len(thin) > 1 else ''} : "
                     + ", ".join(f"{a} ({s['axes'][a]})" for a in thin)))
    elif not s["todo"]:
        acts.append(("/paper-discover", "toutes les fiches sont faites : chercher de nouveaux papiers"))
    if s["git_dirty"]:
        acts.append(("git add -A && git commit", f"{s['git_dirty']} fichier(s) modifié(s) non commité(s)"))
    return acts[:max_n]


def render(s):
    yes = lambda b: "oui" if b else ("?" if b is None else "non")  # noqa: E731
    out = ["Environnement",
           f"  venv .venv            {yes(s['venv'])}",
           f"  Docker                {yes(s['docker'])}",
           f"  GROBID (port 8070)    {'actif' if s['grobid'] else ('?' if s['grobid'] is None else 'arrêté')}",
           f"  visualisation (dash)  {yes(s['viz_deps'])}   embeddings  {yes(s['embed_deps'])}",
           "",
           "Corpus",
           f"  papiers               {s['n_papers']}   fiches faites {s['n_done']}   à faire {len(s['todo'])}",
           f"  benchmarks.csv        {s['n_bench']} ligne(s)",
           f"  gaps.md               {s['n_gaps']} gap(s), dont {s['n_gaps_backed']} étayé(s)",
           f"  inbox/                {len(s['inbox'])} PDF en attente",
           "  par axe               " + ", ".join(
               f"{a} {n}" + (" ⚠" if n < THIN_AXIS else "") for a, n in s["axes"].items())]
    for pid in s["todo"]:
        out.append(f"  fiche à faire         {pid}")
    for pid, n in s["extraction_issues"]:
        out.append(f"  extraction à vérifier {pid} ({n} avertissement(s))")
    if s["git_dirty"]:
        out.append(f"  git                   {s['git_dirty']} fichier(s) non commité(s)")
    acts = next_actions(s)
    out += ["", "À faire ensuite"]
    for i, (cmd, why) in enumerate(acts, 1):
        out += [f"  {i}. {cmd}", f"     {why}"]
    if not acts:
        out.append("  rien d'urgent")
    return "\n".join(out)
