#!/usr/bin/env python3
"""Régénère INDEX.md et external_refs.csv depuis papers/ et vérifie la cohérence de la base.

Ne modifie jamais benchmarks.csv ni les fiches. Code de sortie 1 si une incohérence est trouvée.
"""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from lib import refs, schema  # noqa: E402

PAPERS = ROOT / "papers"
BENCH = ROOT / "benchmarks.csv"
INDEX = ROOT / "INDEX.md"
EXTERNAL = ROOT / "external_refs.csv"

AXIS_TITLES = {
    "surveys": "Surveys et toolflows généraux",
    "yolo-fpga": "YOLO sur FPGA",
    "autoencoder-fpga": "Autoencodeurs sur FPGA",
    "continual-learning": "Apprentissage continu / incrémental embarqué",
    "toolflows": "Toolflows",
    "platforms": "Plateformes",
}
UNCLASSIFIED = "Non classé"
assert set(AXIS_TITLES) == set(schema.AXES), "AXIS_TITLES à aligner sur schema.AXES"

REQUIRED_FILES = ("metadata.json", "fulltext.md", "sections.jsonl", "refs.jsonl", "fiche.md")


def cell(v):
    return str(v if v not in (None, "") else "n/r").replace("|", "\\|").replace("\n", " ")


def _jsonl(path, problems, pid):
    rows = []
    for i, line in enumerate(path.read_text().splitlines(), start=1):
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as e:
            problems.append(f"{pid} : {path.name} ligne {i} illisible ({e})")
    return rows


def check_paper_files(folder, meta, problems, notes):
    """Conformité des fichiers d'un papier à DATA_MODEL §1, §4, §5, §6 et §8."""
    pid = folder.name
    missing = [f for f in REQUIRED_FILES if not (folder / f).exists()]
    for f in missing:
        problems.append(f"{pid} : {f} absent")
    if not (folder / "paper.pdf").exists():
        notes.append(f"{pid} : paper.pdf absent (gitignoré : normal dans un clone neuf)")
    for err in schema.validate_paper_id(pid, meta):
        problems.append(f"{pid} : {err}")

    if "fulltext.md" not in missing:
        fm = schema.read_front_matter((folder / "fulltext.md").read_text())
        expected = {
            "id": pid,
            "year": None if meta.get("year") is None else str(meta["year"]),
            "backend": (meta.get("extraction") or {}).get("backend"),
        }
        for k, v in expected.items():
            if fm.get(k) != v:
                problems.append(f"{pid} : fulltext.md, front-matter {k} = {fm.get(k)!r}, {v!r} attendu")

    if "sections.jsonl" not in missing:
        for order, row in enumerate(_jsonl(folder / "sections.jsonl", problems, pid)):
            for err in schema.validate_section_row(row, pid, order):
                problems.append(f"{pid} : sections.jsonl ligne {order + 1} : {err}")

    if "refs.jsonl" not in missing:
        for i, row in enumerate(_jsonl(folder / "refs.jsonl", problems, pid), start=1):
            for err in schema.validate_ref_row(row, pid):
                problems.append(f"{pid} : refs.jsonl ligne {i} : {err}")

    if "fiche.md" not in missing:
        text = (folder / "fiche.md").read_text()
        fiche = schema.read_front_matter(text).get("fiche")
        status = (meta.get("status") or {}).get("fiche")
        if fiche != status:
            problems.append(f"{pid} : fiche.md dit fiche: {fiche}, metadata.json dit status.fiche: {status}")
        if "\n## Statut de lecture" not in text:
            problems.append(f"{pid} : fiche.md sans section « Statut de lecture » (obligatoire)")


def load_papers(problems, notes):
    papers = []
    for folder in sorted(p for p in PAPERS.iterdir() if p.is_dir()):
        if not (folder / "metadata.json").exists():
            problems.append(f"{folder.name} : metadata.json absent")
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
        check_paper_files(path.parent, meta, problems, notes)
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


def write_external(path, rows):
    """Travaux absents de la base cités par au moins deux papiers (DATA_MODEL §9)."""
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=refs.EXTERNAL_FIELDS, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: (schema.NR if r[k] in (None, "") else r[k]) for k in refs.EXTERNAL_FIELDS})


def run():
    """Régénère INDEX.md et external_refs.csv. Retourne 1 si une incohérence est trouvée."""
    problems, notes = [], []
    papers = load_papers(problems, notes)
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
    ext = refs.external_ranking(refs.load_papers(ROOT))
    write_external(EXTERNAL, ext)
    todo = sum(1 for p in papers if p.get("status", {}).get("fiche") != "done")
    print(f"INDEX.md régénéré : {len(papers)} papiers, {todo} fiches à faire, {len(rows)} lignes de benchmark.")
    print(f"external_refs.csv régénéré : {len(ext)} travaux hors base cités par au moins 2 papiers.")
    try:
        from lib import rag
        m = rag.build_index(ROOT)
        if m["dense"]:
            print(f"Index de passages : {m['chunks']} passages, {m['encoded']} (ré)encodés ({m['model']}).")
        else:
            print(f"Index de passages : {m['chunks']} passages, lexical seul "
                  "(requirements-embed.txt absent).")
    except Exception as e:  # l'index est dérivé : son échec ne bloque pas le reste
        notes.append(f"index de passages non reconstruit : {e}")
    for n in notes:
        print(f"note    {n}")
    for pb in problems:
        print(f"erreur  {pb}")
    return 1 if problems else 0


def main():
    sys.exit(run())


if __name__ == "__main__":
    main()
