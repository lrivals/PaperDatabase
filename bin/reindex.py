#!/usr/bin/env python3
"""Régénère INDEX.md et external_refs.csv depuis papers/ et vérifie la cohérence de la base.

Ne modifie jamais benchmarks.csv, les fiches ni claims.jsonl. Code de sortie 1 si une incohérence est trouvée.
"""
import csv
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib import base, claims, refs, schema  # noqa: E402

ROOT = base.ROOT

PAPERS = ROOT / "papers"
BENCH = ROOT / "benchmarks.csv"
INDEX = ROOT / "INDEX.md"
EXTERNAL = ROOT / "external_refs.csv"

AXIS_TITLES = dict(base.CONFIG["axes"])
UNCLASSIFIED = "Non classé"

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


def load_papers(problems, notes, root=ROOT):
    papers = []
    for folder in sorted(p for p in (root / "papers").iterdir() if p.is_dir()):
        if not (folder / "metadata.json").exists():
            problems.append(f"{folder.name} : metadata.json absent")
    for path in sorted((root / "papers").glob("*/metadata.json")):
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


def load_benchmarks(problems, root=ROOT):
    bench = root / "benchmarks.csv"
    if not bench.exists():
        problems.append("benchmarks.csv absent")
        return []
    with open(bench, newline="") as f:
        reader = csv.DictReader(f)
        for err in schema.check_header(reader.fieldnames):
            problems.append(f"benchmarks.csv : {err}")
        rows = list(reader)
    for i, row in enumerate(rows, start=2):
        for err in schema.validate_benchmark_row(row):
            problems.append(f"benchmarks.csv ligne {i} ({row.get('paper_id')}) : {err}")
    return rows


def render(papers, rows=()):
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
    own = {}
    for r in rows:
        if schema.is_own_id(r["paper_id"]):
            own[r["paper_id"]] = own.get(r["paper_id"], 0) + 1
    if own:
        out += ["## Mesures propres", "", "| id | protocole | lignes de benchmark |", "|---|---|---|"]
        for pid in sorted(own):
            src = schema.own_source(pid)
            out.append(f"| {pid} | [{src}]({src}) | {own[pid]} |")
        out.append("")
    return "\n".join(out)


def write_external(path, rows):
    """Travaux absents de la base cités par au moins deux papiers (DATA_MODEL §9)."""
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=refs.EXTERNAL_FIELDS, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: (schema.NR if r[k] in (None, "") else r[k]) for k in refs.EXTERNAL_FIELDS})


def bench_notes(papers, rows, fronts):
    """Notes sur les fiches done sans ligne de benchmark. fronts : paper_id → front-matter de
    fiche.md. `benchmarks: none` (DATA_MODEL §8) marque une absence justifiée ; un survey
    n'a jamais de ligne."""
    notes = []
    with_bench = {r["paper_id"] for r in rows}
    for p in papers:
        none = (fronts.get(p["id"]) or {}).get("benchmarks") == schema.NO_BENCHMARKS
        if none and p["id"] in with_bench:
            notes.append(f"{p['id']} : fiche.md dit benchmarks: none, mais benchmarks.csv a des lignes")
        elif (p.get("status", {}).get("fiche") == "done" and p["id"] not in with_bench
              and not none and "surveys" not in p.get("axes", [])):
            notes.append(f"{p['id']} : fiche done sans ligne dans benchmarks.csv (oubli ? "
                         "sinon benchmarks: none dans le front-matter de fiche.md)")
    return notes


def check_claims(root, problems, notes):
    """claims.jsonl (DATA_MODEL §12) : schéma et excerpts vérifiés contre leur passage.
    Rien à charger si aucun papier n'en a."""
    results, summary = claims.check(root)
    for r in results:
        msg = f"{r['paper_id']} : claims.jsonl ligne {r['line']} : {r['msg']}"
        (problems if r["level"] == claims.ERROR else notes).append(msg)
    if summary["papers"]:
        print(f"claims.jsonl : {summary['claims']} claims dans {summary['papers']} papier(s), "
              f"{summary['verified']} excerpts vérifiés.")


def gpu_indexes(root):
    """Route GPU (pdb gpu) : vecteurs Qwen de pdb search et index de pdb rag, s'il existe.
    Route désactivée : rien n'est encodé ; un index pdb rag existant est seulement signalé
    s'il est périmé. Renvoie des notes."""
    from lib import rag_models
    sqlite = Path(root) / ".cache" / "rag" / "index.sqlite3"
    ok, reason = rag_models.enabled()
    if not ok:
        if rag_models.wanted():
            return [f"route GPU demandée mais indisponible ({reason}) : vecteurs Qwen non mis à jour"]
        if sqlite.exists():
            from lib import rag_qwen
            try:
                rag_qwen.open_index(root)[0].close()
            except RuntimeError:
                return ["index pdb rag (route GPU) périmé : bin/pdb rag index sur une machine avec GPU"]
        return []
    notes = []
    try:
        from lib import rag
        m = rag.build_index(root, model=rag.GPU_MODEL)
        print(f"Index de passages (GPU) : {m['encoded']} passages (ré)encodés ({m['model']}).")
    except Exception as e:
        notes.append(f"vecteurs Qwen non reconstruits : {e}")
    if sqlite.exists():
        try:
            from lib import rag_qwen
            r = rag_qwen.build(root, mode="hybrid")
            print(f"Index pdb rag : {'inchangé' if r['unchanged'] else str(r['records']) + ' preuves'}.")
        except Exception as e:
            notes.append(f"index pdb rag non reconstruit : {e}")
    return notes


def refresh_figures(root):
    """Figures de pdb plot périmées par ce changement (groupes bench et corpus) : régénérées
    si la base les utilise déjà et que plot.auto / PDB_NO_PLOT le permettent, signalées
    sinon (lib/plotrun.auto_refresh). Jamais bloquant."""
    from lib import plotrun
    lines, notes = plotrun.auto_refresh(root, groups=("bench", "corpus"))
    for line in lines:
        print(line)
    return notes


def run(root=ROOT):
    """Régénère INDEX.md et external_refs.csv. Retourne 1 si une incohérence est trouvée."""
    root = Path(root).resolve()
    problems, notes = [], []
    papers = load_papers(problems, notes, root)
    rows = load_benchmarks(problems, root)

    ids_ = {p["id"] for p in papers if "id" in p}
    for pid in sorted({r["paper_id"] for r in rows} - ids_):
        src = schema.own_source(pid)
        if src is None:
            problems.append(f"benchmarks.csv : paper_id inconnu dans papers/ : {pid}")
        elif not (ROOT / src).exists():
            problems.append(f"benchmarks.csv : mesure propre {pid} sans protocole {src}")
    fronts = {}
    for p in papers:
        path = root / "papers" / p["id"] / "fiche.md"
        fronts[p["id"]] = schema.read_front_matter(path.read_text()) if path.exists() else {}
    notes += bench_notes(papers, rows, fronts)
    check_claims(root, problems, notes)

    (root / "INDEX.md").write_text(render(papers, rows) + "\n")
    ext = refs.external_ranking(refs.load_papers(root))
    write_external(root / "external_refs.csv", ext)
    todo = sum(1 for p in papers if p.get("status", {}).get("fiche") != "done")
    print(f"INDEX.md régénéré : {len(papers)} papiers, {todo} fiches à faire, {len(rows)} lignes de benchmark.")
    print(f"external_refs.csv régénéré : {len(ext)} travaux hors base cités par au moins 2 papiers.")
    if root == ROOT:  # un corpus isolé (pdb synth) n'a pas d'index de passages
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
        notes += gpu_indexes(ROOT)
    if root == ROOT:  # pas les corpus isolés (pdb synth, tests)
        notes += refresh_figures(root)
    for n in notes:
        print(f"note    {n}")
    for pb in problems:
        print(f"erreur  {pb}")
    return 1 if problems else 0


def main():
    if "--no-plot" in sys.argv[1:]:          # figures non régénérées (lots, sous-agents)
        os.environ["PDB_NO_PLOT"] = "1"
    sys.exit(run())


if __name__ == "__main__":
    main()
