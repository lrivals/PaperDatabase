#!/usr/bin/env python3
"""pdb base — gérer plusieurs bases séparées (DATA_MODEL §11).

usage : pdb base list
        pdb base new <nom> --theme "…" [--title "…"] [--path DIR]
        pdb base register <dossier> [--name NOM]  |  forget <nom>  |  use <nom>
        pdb base info [<nom>]           profil, axes et effectifs, suggestions en attente
        pdb base check [<nom>] [--config FICHIER]
                                        effet des règles de base.json (ou d'une proposition)
                                        sur les papiers, sans rien écrire
        pdb base scan [--from a,b|all] [--kind cited_here,in_base,ref_elsewhere] [-n N]
                                        articles utiles à la base active dans les autres bases
                                        → xbase_candidates.csv
        pdb base import <base>:<paper_id>… [--no-pdf]
                                        copie des articles d'une autre base dans la base active

La base active est celle de `pdb --base NOM`, sinon du répertoire courant, sinon la base par
défaut du registre. `forget` n'efface aucun fichier.
"""
import argparse
import sys
from pathlib import Path

CODE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(CODE))

from lib import base, bases, registry, xbase  # noqa: E402

ROOT = base.ROOT


def _root_of(name):
    if not name:
        return ROOT
    root = registry.resolve(name)
    if root is None:
        sys.exit(f"base inconnue du registre : {name} (pdb base list)")
    return root


def cmd_list(a):
    rows = bases.all_stats()
    if not rows:
        print("aucune base enregistrée : pdb base register <dossier> ou pdb base new <nom> --theme …")
        return 0
    active = ROOT.resolve()
    print(f"{'':2}{'nom':<12}{'papiers':>8}{'fiches':>8}{'bench':>7}{'axes':>6}{'sugg.':>6}  {'modifiée':<17}titre")
    for r in rows:
        mark = ("*" if r["default"] else " ") + (">" if Path(r["path"]).resolve() == active else " ")
        if not r["exists"]:
            print(f"{mark}{r['name']:<12}  dossier introuvable : {r['path']}")
            continue
        print(f"{mark}{r['name']:<12}{r['papers']:>8}{r['done']:>8}{r['benchmarks']:>7}{r['axes']:>6}"
              f"{r['suggestions']:>6}  {r['modified']:<17}{r['title']}")
    print("\n* base par défaut   > base active")
    return 0


def cmd_new(a):
    try:
        root = bases.create(a.name, a.theme, a.path, a.title)
    except (bases.BaseError, ValueError) as e:
        sys.exit(f"erreur  {e}")
    print(f"\nbase {a.name!r} créée : {root}")
    print(f"Suite : cd {root} puis /base-profile dans Claude Code (axes et règles à partir du thème),\n"
          f"        puis /paper-discover ou bin/pdb base scan pour les premiers articles.")
    return 0


def cmd_register(a):
    path = Path(a.path).expanduser().resolve()
    name = a.name or path.name.lower().replace(" ", "-")
    try:
        registry.register(name, path)
    except ValueError as e:
        sys.exit(f"erreur  {e}")
    print(f"enregistrée : {name} → {path}")
    if not (path / bases.PROFILE).exists():
        print(f"note    {bases.PROFILE} absent : /base-profile le crée depuis base.json et CLAUDE.md")
    return 0


def cmd_forget(a):
    try:
        registry.forget(a.name)
    except KeyError:
        sys.exit(f"base inconnue du registre : {a.name}")
    print(f"{a.name} retirée du registre (aucun fichier supprimé)")
    return 0


def cmd_use(a):
    try:
        registry.set_default(a.name)
    except KeyError:
        sys.exit(f"base inconnue du registre : {a.name}")
    print(f"base par défaut : {a.name} (hors de tout dossier de base)")
    return 0


def cmd_info(a):
    root = _root_of(a.name)
    i = bases.info(root)
    print(f"{i['title']}\n{i['path']}\n\nThème (utilisateur) :\n  " + i["theme"].replace("\n", "\n  "))
    print("\nAxes (effectif, règle d'ingestion) :")
    for ax, title, n, rule in i["axes"]:
        print(f"  {ax:<24}{n:>4}  {'règle' if rule or ax == 'surveys' else 'SANS RÈGLE'}  {title}")
    if not i["has_topic"]:
        print("  (pas de topic_re : discover considère tout candidat comme dans le sujet)")
    print(f"\nPapiers sans axe : {len(i['unclassified'])}" + (
        "  " + ", ".join(i["unclassified"][:8]) + ("…" if len(i["unclassified"]) > 8 else "")
        if i["unclassified"] else ""))
    if i["imported"]:
        print(f"Papiers importés d'autres bases : {len(i['imported'])}")
    print(f"\nSuggestions de profil en attente : {len(i['suggestions'])}")
    for s in i["suggestions"]:
        print("  " + s)
    if i["suggestions"] or i["unclassified"]:
        print("\n→ /base-profile pour les examiner.")
    return 0


def cmd_check(a):
    root = _root_of(a.name)
    r = bases.check(root, a.config)
    for e in r["errors"]:
        print(f"erreur  {e}")
    if r["errors"]:
        return 1
    print(f"{a.config or 'base.json'} valide.")
    for ax, pids in r["undeclared"].items():
        print(f"ATTENTION axe {ax!r} non déclaré mais porté par {len(pids)} papier(s) : "
              + ", ".join(pids[:5]) + ("…" if len(pids) > 5 else "")
              + " — reindex échouera tant que leurs metadata.json le portent")
    if r["axes_without_rule"]:
        print("Axes sans règle d'ingestion (jamais devinés) : " + ", ".join(r["axes_without_rule"]))
    print(f"\nAxes que les règles actuelles donneraient ≠ axes enregistrés : {len(r['changes'])} papier(s)")
    for pid, fiche, cur, new in r["changes"]:
        add, rem = sorted(set(new) - set(cur)), sorted(set(cur) - set(new))
        detail = " ".join([*(f"+{x}" for x in add), *(f"-{x}" for x in rem)])
        print(f"  {pid[:60]:<60} {fiche or '?':<5} {detail}")
    if r["changes"]:
        print("  (fiche done : axes confirmés à la lecture, ils priment ; sinon ils sont devinés)")
    print(f"\nHors sujet selon topic_re/title_topic_re : {len(r['out_of_topic'])} papier(s)")
    for pid in r["out_of_topic"][:20]:
        print(f"  {pid}")
    if r["plot"]:
        b, f = r["plot"]["before"], r["plot"]["after"]
        print(f"\nFigures (pdb plot, {f['rows']} lignes de benchmarks.csv ; seuil "
              f"plot.max_other {f['max_other']:.0%}) :")
        for key, label in (("platform_other", "plateforme « autre »"),
                           ("task_other", "tâche « autre »"), ("platform_nr", "plateforme n/r")):
            change = "" if b is f else f"{b['rates'][key]:.0%} → "
            print(f"  {label:<22} {change}{f['rates'][key]:.0%}")
        for (x, y), n in sorted(r["plot"]["moved"].items(), key=lambda kv: -kv[1]):
            print(f"  {n:>3} ligne(s) de tâche déplacée(s) : « {x} » → « {y} »")
        if f["skip"]:
            print("  écartées (plot.skip) : " + ", ".join(f["skip"]))
        for line in f["alerts"]:
            print(f"  ALERTE {line} — détail : bin/pdb plot --check")
    return 0


def cmd_scan(a):
    reg = registry.all_bases()
    names = [n for n, _ in reg] if a.src in (None, "all") else a.src.split(",")
    unknown = [n for n in names if registry.resolve(n) is None]
    if unknown:
        sys.exit(f"base(s) inconnue(s) : {', '.join(unknown)} (pdb base list)")
    sources = [(n, d) for n, d in reg if n in names and d.resolve() != ROOT.resolve()]
    if not sources:
        sys.exit("aucune autre base à parcourir (pdb base list)")
    kinds = tuple(a.kind.split(",")) if a.kind else xbase.KINDS
    bad = set(kinds) - set(xbase.KINDS)
    if bad:
        sys.exit(f"--kind inconnu : {', '.join(sorted(bad))} ({', '.join(xbase.KINDS)})")
    rows = xbase.scan(ROOT, sources, kinds)
    out = ROOT / xbase.OUT
    xbase.write(rows, out)
    here = registry.name_of(ROOT) or ROOT.name
    print(f"{here} ← {', '.join(n for n, _ in sources)} : {len(rows)} candidats → {xbase.OUT}")
    for kind in kinds:
        sel = [r for r in rows if r["kind"] == kind]
        print(f"\n## {kind} ({len(sel)})")
        for r in sel[:a.n]:
            ref = f"{r['source_base']}:{r['paper_id']}" if r["paper_id"] else (
                r["arxiv_id"] or r["doi"] or "(sans identifiant)")
            print(f"  {r['score']:>5}  {(r['title'] or '')[:70]:<70} {r['year'] or '':<5} {ref}")
            print(f"         {r['reasons']}")
    print("\nImporter : bin/pdb base import <base>:<paper_id> …   "
          "ref_elsewhere : /paper-add <arxiv|doi>")
    return 0


def cmd_import(a):
    done, failed = [], 0
    for spec in a.items:
        name, sep, pid = spec.partition(":")
        if not sep or not pid:
            print(f"erreur  {spec} : format <base>:<paper_id> attendu", file=sys.stderr)
            failed += 1
            continue
        src = registry.resolve(name)
        if src is None:
            print(f"erreur  {spec} : base inconnue du registre", file=sys.stderr)
            failed += 1
            continue
        try:
            r = xbase.import_paper(src, pid, ROOT, name, with_pdf=not a.no_pdf)
        except xbase.ImportError_ as e:
            print(f"erreur  {spec} : {e}", file=sys.stderr)
            failed += 1
            continue
        done.append(r)
        print(f"importé {pid} depuis {name} : axes {r['axes'] or 'aucun'}, "
              f"{r['benchmarks']} ligne(s) de benchmark ; fiche repassée à todo")
    if done:
        print()
        failed += bool(bases.reindex(ROOT))
        print("Fiches à réévaluer pour cette base : /paper-fiche <paper_id>.")
    return 1 if failed else 0


def run(args):
    p = argparse.ArgumentParser(prog="pdb base", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    s = sub.add_parser("new")
    s.add_argument("name")
    s.add_argument("--theme", required=True, help="thème en quelques phrases (profile.md)")
    s.add_argument("--title", help="intitulé (base.json name) ; défaut : le nom")
    s.add_argument("--path", help=f"dossier ; défaut : {CODE}/bases/<nom> (versionné avec le dépôt)")
    s = sub.add_parser("register")
    s.add_argument("path")
    s.add_argument("--name")
    for c in ("forget", "use"):
        sub.add_parser(c).add_argument("name")
    sub.add_parser("info").add_argument("name", nargs="?")
    s = sub.add_parser("check")
    s.add_argument("name", nargs="?")
    s.add_argument("--config", help="base.json proposé, à éprouver avant de l'appliquer")
    s = sub.add_parser("scan")
    s.add_argument("--from", dest="src", help="bases sources, séparées par des virgules (défaut : all)")
    s.add_argument("--kind", help=",".join(xbase.KINDS))
    s.add_argument("-n", type=int, default=15, help="lignes affichées par sorte (le CSV a tout)")
    s = sub.add_parser("import")
    s.add_argument("items", nargs="+", metavar="base:paper_id")
    s.add_argument("--no-pdf", action="store_true", help="ne pas copier paper.pdf")
    a = p.parse_args(args)
    return globals()["cmd_" + a.cmd](a)


if __name__ == "__main__":
    sys.exit(run(sys.argv[1:]))
