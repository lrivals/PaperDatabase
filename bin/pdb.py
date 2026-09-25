#!/usr/bin/env python3
"""PaperDatabase — point d'entrée unique. Lancer via bin/pdb.

  status                    état de la base et prochaines actions
  add <id|doi|pdf>… [--from liste.txt] [--start-grobid]
                            ajoute des articles (arXiv, DOI, PDF local), ingère, réindexe
  ingest [--force] [pdf…]   ingère inbox/ (ou les PDF donnés), réindexe
  reindex                   régénère INDEX.md et external_refs.csv, vérifie la cohérence
  discover [options]        cherche des papiers candidats (OpenAlex) → candidates.csv
  grobid start|stop|status  pilote le conteneur GROBID
  bench [filtres] [--cols a,b] [--sort col [--desc]] [-n N] [--format tsv|md|json]
                            filtre benchmarks.csv (sans LLM) ; bench -h pour les filtres
  paper <id|court|mot> [--fields a,b] [--bench]
                            fiche d'identité d'un papier (métadonnées, statut, benchmarks)
  viz [--port N]            visualisation du corpus (http://127.0.0.1:8050)
  test                      lance les tests

Guide : docs/GUIDE.md. Détail des scripts : SETUP.md §5. Requêtes : docs/RAG.md.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "bin"))

GROBID_SH = ["bash", str(ROOT / "bin" / "grobid.sh")]


def ensure_grobid(start):
    """Démarre GROBID si demandé (ou si l'utilisateur accepte) ; sinon prévient du repli."""
    import ingest
    if ingest.grobid_alive():
        return
    if not start and sys.stdin.isatty():
        answer = input("GROBID est arrêté. Le démarrer (extraction plus fiable) ? [O/n] ").strip().lower()
        start = answer in ("", "o", "oui", "y", "yes")
    if start:
        subprocess.run(GROBID_SH + ["start"])
    else:
        print("Poursuite sans GROBID : repli PyMuPDF, métadonnées à vérifier.")


def cmd_status(args):
    from lib import status
    print(status.render(status.collect(ROOT)))
    return 0


def cmd_add(args):
    import add
    import reindex
    start = "--start-grobid" in args
    args = [a for a in args if a != "--start-grobid"]
    if not args or args[0] in ("-h", "--help"):
        print(add.__doc__)
        return 0 if args else 2
    ensure_grobid(start)
    failed = add.run(args)
    print()
    return 1 if (reindex.run() or failed) else 0


def cmd_ingest(args):
    import ingest
    import reindex
    if args and args[0] in ("-h", "--help"):
        print(ingest.__doc__)
        return 0
    ensure_grobid("--start-grobid" in args)
    force = "--force" in args
    pdfs = [a for a in args if a not in ("--force", "--start-grobid")]
    failed = ingest.run(pdfs, force=force)
    print()
    return 1 if (reindex.run() or failed) else 0


def cmd_reindex(args):
    import reindex
    return reindex.run()


def cmd_discover(args):
    import discover
    return discover.run(args)


def cmd_grobid(args):
    return subprocess.run(GROBID_SH + (args or ["status"])).returncode


def cmd_viz(args):
    return subprocess.run([sys.executable, str(ROOT / "bin" / "viz.py"), *args]).returncode


def _pairs(items, number):
    """["col=val", …] → {col: val} ; val converti en float si number."""
    out = {}
    for item in items or []:
        col, sep, val = item.partition("=")
        if not sep:
            raise ValueError(f"{item!r} : col=valeur attendu")
        out[col.strip()] = float(val) if number else val
    return out


BENCH_SHORTCUTS = ("platform", "model", "task", "toolflow", "dataset")


def cmd_bench(args):
    import argparse
    from lib import query
    p = argparse.ArgumentParser(prog="pdb bench", description=(
        "Filtre benchmarks.csv. Filtres texte : sous-chaîne insensible à la casse. "
        "paper_id, source_section et confidence sont toujours affichés ; "
        "power_scope aussi quand power_w l'est. ! = confidence low."))
    for c in BENCH_SHORTCUTS:
        p.add_argument(f"--{c}", metavar="TEXTE")
    p.add_argument("--quant", metavar="TEXTE", help="filtre sur quantization")
    p.add_argument("--paper", metavar="ID", help="id complet, court, ou mot du titre")
    p.add_argument("--where", action="append", metavar="COL=TEXTE", help="filtre texte, répétable")
    p.add_argument("--min", action="append", metavar="COL=X", help="COL ≥ X (n/r exclu), répétable")
    p.add_argument("--max", action="append", metavar="COL=X", help="COL ≤ X (n/r exclu), répétable")
    p.add_argument("--has", action="append", default=[], metavar="COL", help="COL renseignée")
    p.add_argument("--cols", help="colonnes à afficher, séparées par des virgules")
    p.add_argument("--sort", metavar="COL", help="tri croissant (n/r en dernier)")
    p.add_argument("--desc", action="store_true", help="tri décroissant")
    p.add_argument("-n", type=int, help="nombre maximal de lignes")
    p.add_argument("--format", choices=("tsv", "md", "json"), default="tsv")
    p.add_argument("--max-chars", type=int)
    a = p.parse_args(args)

    header, rows = query.load_benchmarks(ROOT)
    metas = query.load_papers(ROOT)
    short = query.short_ids(metas)
    try:
        contains = _pairs(a.where, number=False)
        contains.update({c: getattr(a, c) for c in BENCH_SHORTCUTS if getattr(a, c)})
        if a.quant:
            contains["quantization"] = a.quant
        minimum, maximum = _pairs(a.min, number=True), _pairs(a.max, number=True)
        cols = query.select_columns([c.strip() for c in a.cols.split(",")] if a.cols else [], header)
        for c in [*contains, *minimum, *maximum, *a.has, *([a.sort] if a.sort else [])]:
            if c not in header:
                raise ValueError(f"colonne inconnue : {c}. Valides : {', '.join(header)}")
    except ValueError as e:
        print(f"pdb bench : {e}", file=sys.stderr)
        return 2
    if a.paper:
        found = query.resolve(a.paper, metas)
        if not found:
            print(f"pdb bench : aucun papier ne correspond à {a.paper!r}", file=sys.stderr)
            return 1
        ids = {m["id"] for m in found}
        rows = [r for r in rows if r["paper_id"] in ids]

    rows = query.filter_rows(rows, contains, minimum, maximum, a.has)
    if a.sort:
        rows = query.sort_rows(rows, a.sort, desc=a.desc)
    if a.n:
        rows = rows[:a.n]
    if not rows:
        print("# aucune ligne", file=sys.stderr)
        return 1
    print(query.render(rows, cols, short, a.format, a.max_chars))
    return 0


def cmd_paper(args):
    import argparse
    from lib import query
    p = argparse.ArgumentParser(prog="pdb paper", description=(
        "Fiche d'identité d'un papier : id complet, id court (arXiv ou année-auteur) "
        "ou mot du titre. Plusieurs correspondances → liste des candidats."))
    p.add_argument("query")
    p.add_argument("--fields", help=f"champs parmi : {','.join(query.CARD_FIELDS)}")
    p.add_argument("--bench", action="store_true", help="ajoute les lignes de benchmarks.csv")
    p.add_argument("--format", choices=("tsv", "md", "json"), default="tsv",
                   help="format des lignes de benchmark")
    a = p.parse_args(args)

    metas = query.load_papers(ROOT)
    short = query.short_ids(metas)
    found = query.resolve(a.query, metas)
    if not found:
        print(f"pdb paper : aucun papier ne correspond à {a.query!r}", file=sys.stderr)
        return 1
    if len(found) > 1:
        print(f"# {len(found)} papiers correspondent ; préciser avec l'id court :")
        for m in found:
            print(f"{short[m['id']]}\t{m.get('year') or 'n/r'}\t{m.get('title') or 'n/r'}")
        return 1
    meta = found[0]
    header, rows = query.load_benchmarks(ROOT)
    rows = [r for r in rows if r["paper_id"] == meta["id"]]
    fields = [f.strip() for f in a.fields.split(",")] if a.fields else None
    try:
        print(query.paper_card(meta, len(rows), short[meta["id"]], fields))
    except ValueError as e:
        print(f"pdb paper : {e}", file=sys.stderr)
        return 2
    if a.bench and rows:
        print()
        print(query.render(rows, header, short, a.format))
    return 0


def cmd_test(args):
    return subprocess.run([sys.executable, "-m", "unittest", "discover", "tests", *args],
                          cwd=ROOT).returncode


COMMANDS = {
    "status": cmd_status, "add": cmd_add, "ingest": cmd_ingest, "reindex": cmd_reindex,
    "discover": cmd_discover, "grobid": cmd_grobid, "viz": cmd_viz, "test": cmd_test,
    "bench": cmd_bench, "paper": cmd_paper,
}


def main():
    argv = sys.argv[1:]
    if not argv or argv[0] in ("-h", "--help", "help"):
        print(__doc__)
        return 0
    cmd = COMMANDS.get(argv[0])
    if cmd is None:
        print(f"commande inconnue : {argv[0]}\n{__doc__}", file=sys.stderr)
        return 2
    return cmd(argv[1:])


if __name__ == "__main__":
    sys.exit(main())
