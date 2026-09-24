#!/usr/bin/env python3
"""Régénère INDEX.md depuis papers/*/metadata.json et vérifie la cohérence de la base.

Ne modifie jamais benchmarks.csv ni les fiches. Code de sortie 1 si une incohérence est trouvée.
"""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from lib import schema  # noqa: E402

PAPERS = ROOT / "papers"
BENCH = ROOT / "benchmarks.csv"
INDEX = ROOT / "INDEX.md"

AXIS_TITLES = {
    "surveys": "Surveys et toolflows généraux",
    "yolo-fpga": "YOLO sur FPGA",
    "autoencoder-fpga": "Autoencodeurs sur FPGA",
    "continual-learning": "Apprentissage continu / incrémental embarqué",
    "toolflows": "Toolflows",
    "platforms": "Plateformes",
}
UNCLASSIFIED = "Non classé"


def cell(v):
    return str(v if v not in (None, "") else "n/r").replace("|", "\\|").replace("\n", " ")


def load_papers(problems):
    papers = []
    for path in sorted(PAPERS.glob("*/metadata.json")):
        try:
            meta = json.loads(path.read_text())
        except json.JSONDecodeError as e:
            problems.append(f"{path.parent.name} : metadata.json illisible ({e})")
            continue
        for err in schema.validate_metadata(meta):
            problems.append(f"{path.parent.name} : {err}")
        if meta.get("id") != path.parent.name:
            problems.append(f"{path.parent.name} : id ≠ nom du dossier ({meta.get('id')})")
        papers.append(meta)
    return papers


def load_benchmarks(problems):
    if not BENCH.exists():
        problems.append("benchmarks.csv absent")
        return []
    with open(BENCH, newline="") as f:
        reader = csv.DictReader(f)
        if tuple(reader.fieldnames or ()) != schema.BENCHMARK_COLUMNS:
            problems.append("benchmarks.csv : en-tête différent de schema.BENCHMARK_COLUMNS")
        rows = list(reader)
    for i, row in enumerate(rows, start=2):
        for err in schema.validate_benchmark_row(row):
            problems.append(f"benchmarks.csv ligne {i} ({row.get('paper_id')}) : {err}")
    return rows


def render(papers):
    todo = sum(1 for p in papers if p.get("status", {}).get("fiche") != "done")
    out = [
        "# Index des papiers",
        "",
        "<!-- GÉNÉRÉ par bin/reindex.py — ne pas éditer à la main -->",
        "",
        f"**{len(papers)} papiers, {todo} fiches à faire.**",
        "",
        "Un papier peut apparaître sous plusieurs axes.",
        "",
    ]
    groups = [(a, AXIS_TITLES[a]) for a in schema.AXES] + [(None, UNCLASSIFIED)]
    for axis, title in groups:
        members = [p for p in papers if (axis in p.get("axes", [])) or (axis is None and not p.get("axes"))]
        if not members:
            continue
        members.sort(key=lambda p: (-(p.get("year") or 0), p["id"]))
        out += [f"## {title} (`{axis}`)" if axis else f"## {title}", "",
                "| id | titre | auteurs | année | venue | type | fiche |",
                "|---|---|---|---|---|---|---|"]
        for p in members:
            fiche = p.get("status", {}).get("fiche", "todo")
            link = f"[{p['id']}](papers/{p['id']}/fiche.md)"
            out.append("| " + " | ".join([
                link,
                cell(p.get("title")),
                cell(schema.format_authors(p.get("authors") or [], max_n=3)),
                cell(p.get("year")),
                cell(p.get("venue")),
                cell(p.get("type")),
                fiche,
            ]) + " |")
        out.append("")
    return "\n".join(out)


def main():
    problems, notes = [], []
    papers = load_papers(problems)
    rows = load_benchmarks(problems)

    ids_ = {p["id"] for p in papers if "id" in p}
    for pid in sorted({r["paper_id"] for r in rows} - ids_):
        problems.append(f"benchmarks.csv : paper_id inconnu dans papers/ : {pid}")
    with_bench = {r["paper_id"] for r in rows}
    for p in papers:
        if p.get("status", {}).get("fiche") == "done" and p["id"] not in with_bench:
            if "surveys" in p.get("axes", []):
                continue
            notes.append(f"{p['id']} : fiche done sans ligne dans benchmarks.csv (oubli ?)")

    INDEX.write_text(render(papers) + "\n")
    todo = sum(1 for p in papers if p.get("status", {}).get("fiche") != "done")
    print(f"INDEX.md régénéré : {len(papers)} papiers, {todo} fiches à faire, {len(rows)} lignes de benchmark.")
    for n in notes:
        print(f"note    {n}")
    for pb in problems:
        print(f"erreur  {pb}")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
