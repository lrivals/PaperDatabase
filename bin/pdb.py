#!/usr/bin/env python3
"""PaperDatabase — point d'entrée unique. Lancer via bin/pdb.

  status                    état de la base et prochaines actions
  add <id|doi|pdf>… [--from liste.txt] [--start-grobid]
                            ajoute des articles (arXiv, DOI, PDF local), ingère, réindexe
  ingest [--force] [pdf…]   ingère inbox/ (ou les PDF donnés), réindexe
  reindex                   régénère INDEX.md et external_refs.csv, vérifie la cohérence
  discover [options]        cherche des papiers candidats (OpenAlex) → candidates.csv
  grobid start|stop|status  pilote le conteneur GROBID
  viz [--port N]            visualisation du corpus (http://127.0.0.1:8050)
  rag <command>             recherche, preuves, benchmarks et acquisition scientifique
  test                      lance les tests

Guide : docs/GUIDE.md. Détail des scripts : SETUP.md §5.
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


def cmd_test(args):
    return subprocess.run([sys.executable, "-m", "unittest", "discover", "tests", *args],
                          cwd=ROOT).returncode


def cmd_rag(args):
    import rag_cli
    return rag_cli.run(args)


COMMANDS = {
    "status": cmd_status, "add": cmd_add, "ingest": cmd_ingest, "reindex": cmd_reindex,
    "discover": cmd_discover, "grobid": cmd_grobid, "viz": cmd_viz, "test": cmd_test,
    "rag": cmd_rag,
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
