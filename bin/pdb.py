#!/usr/bin/env python3
"""PaperDatabase — point d'entrée unique. Lancer via bin/pdb.

  pdb [--base NOM] <commande> …   agit sur la base NOM du registre (défaut : base du
                            répertoire courant, sinon base par défaut ; DATA_MODEL §11)

  base <command>            gère les bases : list, new, register, forget, use, info, check,
                            scan (articles utiles dans les autres bases), import ; base -h
  status                    état de la base et prochaines actions
  add <id|doi|pdf>… [--from liste.txt] [--start-grobid]
                            ajoute des articles (arXiv, DOI, PDF local), ingère, réindexe
  ingest [--force] [pdf…]   ingère inbox/ (ou les PDF donnés), réindexe
  ingest --reparse [--tables docling [--ocr]] [id…]
                            ré-extrait les papiers déjà ingérés depuis leur TEI (sans GROBID) ;
                            --tables docling : Docling sur les tableaux restés sans corps
  reindex [--no-plot]       régénère INDEX.md et external_refs.csv, vérifie la cohérence,
                            refait les figures périmées (add, ingest : --no-plot aussi)
  discover [options]        cherche des papiers candidats (OpenAlex) → candidates.csv
  grobid start|stop|status  pilote le conteneur GROBID
  bench [filtres] [--cols a,b] [--sort col [--desc]] [-n N] [--format tsv|md|json]
                            filtre benchmarks.csv (sans LLM) ; bench -h pour les filtres
  paper <id|court|mot>… [--fields a,b] [--bench]
                            fiche d'identité d'un papier (métadonnées, statut, benchmarks) ;
                            plusieurs ids → une ligne par papier
  cites <id> [--external]   références du papier présentes dans la base (et hors base)
  cited-by <id>             papiers de la base qui le citent
  search "<question>" [-k 8] [--paper ID] [--section S] [--mode M] [--rerank] [--gpu|--cpu]
                            passages pertinents, avec chunk_id, section, page (sans LLM) ;
                            moteur CPU par défaut, Qwen sur GPU si la route GPU est active
  show <chunk_id>… [--context N]
                            texte exact d'un passage (id court accepté : 1612.07119#019.0)
  verify <chunk_id> "<citation>" [--sha1 X]
                            la citation figure-t-elle dans le passage ? OK | APPROX | NOMBRES | ABSENT
  viz [--port N]            visualisation du corpus (http://127.0.0.1:8050)
  plot [bench|eval|corpus|all] [--only a,b] [--out DIR] [--format png|pdf|svg] [--list] [--stale]
  plot --check [--brief] [--paper ID]
                            figures statiques : benchmarks, évaluation, statistiques du corpus
  eval [--extract|--rag|--speed] [--gpu] [--save] [--compare [JSON]]
                            banc d'évaluation du logiciel (docs/EVAL.md)
  eval --answers DIR… | --questions [JEU]
                            note les réponses enregistrées d'un run / liste les questions
                            à poser (docs/EVAL.md §10)
  gpu [status|on|off|download]
                            route GPU optionnelle (Qwen3, CUDA) : état, activation, modèles
  rag <command>             outils de la route GPU : index SQLite, preuves, acquisition
                            open access (/paper-research) ; rag -h
  synth <command>           benchmark synthétique (docs/BENCHMARK.md)
  test [--rag]              lance les tests (--rag : pdb eval --rag)

Guide : docs/GUIDE.md. Détail des scripts : SETUP.md §5. Requêtes : docs/RAG.md.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

CODE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(CODE))
sys.path.insert(0, str(CODE / "bin"))


def _select_base(argv):
    """`--base NOM` avant la commande : fixe PDB_ROOT avant l'import de lib.base (qui fige la
    base active) ; les sous-processus en héritent."""
    if argv[:1] == ["--base"] and len(argv) >= 2 or argv[:1] and argv[0].startswith("--base="):
        name = argv[1] if argv[0] == "--base" else argv[0].split("=", 1)[1]
        from lib import registry
        root = registry.resolve(name)
        if root is None:
            sys.exit(f"base inconnue du registre : {name} (pdb base list)")
        os.environ["PDB_ROOT"] = str(root)
        del sys.argv[1:3 if argv[0] == "--base" else 2]


_select_base(sys.argv[1:])

from lib import base  # noqa: E402

ROOT = base.ROOT  # base de données active (lib/base.py) ; CODE = le dépôt du logiciel
GROBID_SH = ["bash", str(CODE / "bin" / "grobid.sh")]


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


def cmd_base(args):
    import bases
    return bases.run(args)


def cmd_status(args):
    from lib import bases, registry, status
    name = registry.name_of(ROOT)
    print(f"Base : {base.CONFIG['name']}" + (f" ({name})" if name else " (non enregistrée)")
          + f"\n  {ROOT}")
    n = len(bases.pending_suggestions(ROOT))
    if n:
        print(f"  {n} suggestion(s) de profil en attente : /base-profile")
    print()
    print(status.render(status.collect(ROOT)))
    return 0


def _refresh_figures(groups):
    """Fin d'une commande qui change les sources des figures sans passer par reindex
    (pdb eval --save, pdb bench --add-columns) : figures périmées refaites ou signalées."""
    from lib import plotrun
    lines, notes = plotrun.auto_refresh(ROOT, groups=groups)
    for line in [*lines, *(f"note    {n}" for n in notes)]:
        print(line)


def _no_plot(args):
    """--no-plot : la réindexation finale ne régénère pas les figures (PDB_NO_PLOT)."""
    if "--no-plot" in args:
        os.environ["PDB_NO_PLOT"] = "1"
    return [a for a in args if a != "--no-plot"]


def cmd_add(args):
    import add
    import reindex
    args = _no_plot(args)
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
    args = _no_plot(args)
    if args and args[0] in ("-h", "--help"):
        print(ingest.__doc__)
        return 0
    if "--reparse" in args:
        docling = "--tables" in args and args[args.index("--tables") + 1:][:1] == ["docling"]
        ids = [a for a in args if a not in ("--reparse", "--tables", "docling", "--ocr")]
        failed = ingest.reparse(ids, docling=docling, ocr="--ocr" in args)
        print()
        return 1 if (reindex.run() or failed) else 0
    ensure_grobid("--start-grobid" in args)
    force = "--force" in args
    pdfs = [a for a in args if a not in ("--force", "--start-grobid")]
    failed = ingest.run(pdfs, force=force)
    print()
    return 1 if (reindex.run() or failed) else 0


def cmd_reindex(args):
    import reindex
    _no_plot(args)
    return reindex.run()


def cmd_discover(args):
    import discover
    return discover.run(args)


def cmd_grobid(args):
    return subprocess.run(GROBID_SH + (args or ["status"])).returncode


def cmd_viz(args):
    return subprocess.run([sys.executable, str(CODE / "bin" / "viz.py"), *args]).returncode


def cmd_plot(args):
    import argparse
    p = argparse.ArgumentParser(prog="pdb plot", description=(
        "Figures statiques (matplotlib) : benchmarks.csv, eval/results, statistiques du "
        "corpus. Écrit aussi manifest.json (sources et effectifs de chaque figure). "
        "Réglages par base : bloc plot de base.json (DATA_MODEL §11.2.1)."))
    p.add_argument("group", nargs="?", default="all", choices=("bench", "eval", "corpus", "all"))
    p.add_argument("--only", help="noms de figures séparés par des virgules (voir --list) ; "
                                  "passe outre plot.skip")
    p.add_argument("--out", default=str(ROOT / "figures"), help="dossier de sortie (figures/)")
    p.add_argument("--format", choices=("png", "pdf", "svg"),
                   help="png par défaut ; sans --format, une figure garde son format du manifest")
    p.add_argument("--list", action="store_true", help="liste les figures sans rien générer")
    p.add_argument("--stale", action="store_true",
                   help="ne régénère que les figures périmées (source ou réglages plus récents)")
    p.add_argument("--check", action="store_true",
                   help="classement des plateformes et tâches pour les figures, bloc plot proposé "
                        "(sans matplotlib, n'écrit rien)")
    p.add_argument("--brief", action="store_true", help="avec --check : alertes seulement")
    p.add_argument("--paper", help="avec --check : seulement les lignes de ce papier")
    a = p.parse_args(args)
    from lib import base, plotdata, plotrun
    try:
        cfg = base.load_config(ROOT)
    except ValueError as e:
        print(f"pdb plot : {e}", file=sys.stderr)
        return 1
    if a.check:
        return _plot_check(cfg, a.brief, a.paper)

    group_of = {n: plotrun.group_of(n) for n in base.PLOT_FIGURES}
    names = [n for n in base.PLOT_FIGURES if a.group in ("all", group_of[n])]
    skip = set(cfg["plot"].get("skip") or ())
    if a.only:
        wanted = [n.strip() for n in a.only.split(",") if n.strip()]
        unknown = [n for n in wanted if n not in group_of]
        if unknown:
            print(f"pdb plot : figure(s) inconnue(s) : {', '.join(unknown)} (voir --list)",
                  file=sys.stderr)
            return 2
        names, skip = wanted, set()
    if a.list:
        try:
            from lib import plotfig
            desc = {n: d for n, (_, _, d) in plotfig.FIGURES.items()}
        except ImportError:
            desc = {}
        for n in names:
            print(f"{group_of[n]}\t{n}\t{desc.get(n, '')}" + ("\t(plot.skip)" if n in skip else ""))
        return 0

    for n in [n for n in names if n in skip]:
        print(f"-  {n} : écartée par base.json (plot.skip)")
    names = [n for n in names if n not in skip]
    if a.stale:
        stale = plotdata.stale_figures(ROOT, Path(a.out), plotrun.load_manifest(a.out),
                                       {n: group_of[n] for n in names}, cfg)
        names = [n for n in names if n in stale]
        if not names:
            print("figures à jour")
            return 0
    try:
        res = plotrun.render(ROOT, names, out=a.out, fmt=a.format,
                             err=lambda m: print(m, file=sys.stderr))
    except ImportError as e:
        print(f"pdb plot : {e}. Installer : .venv/bin/pip install -r requirements-plot.txt",
              file=sys.stderr)
        return 1
    return 1 if res["failed"] else 0


def _plot_check(cfg, brief=False, paper=None):
    """pdb plot --check : classement des lignes de benchmarks.csv pour les figures."""
    from lib import plotdata, query
    _, rows = query.load_benchmarks(ROOT)
    r = plotdata.plot_check(rows, cfg, paper)
    if brief:
        for line in r["alerts"]:
            print(f"plot : {line}")
        if r["alerts"]:
            print("plot : à proposer dans profile.md (Suggestions en attente), "
                  "détail : bin/pdb plot --check")
        return 0
    n = r["rows"]
    rates = r["rates"]
    print(f"{n} lignes de benchmarks.csv" + (f" (papier {paper})" if paper else ""))
    print(f"  plateforme « autre » : {rates['platform_other']:.0%}   plateforme n/r : "
          f"{rates['platform_nr']:.0%}   tâche « autre » : {rates['task_other']:.0%}   "
          f"(seuil plot.max_other {r['max_other']:.0%})")
    print("  familles : " + ", ".join(f"{f} {c}" for f, c in
                                      sorted(r["families"].items(), key=lambda kv: -kv[1])))
    for title, key in (("Plateformes « autre »", "platform_other"), ("Tâches « autre »", "task_other")):
        if r[key]:
            print(f"\n{title} :")
            for label, c in list(r[key].items())[:15]:
                print(f"  {c:>3}  {label}")
    print("\nFigures de benchmarks (lignes tracées ; 0 = ignorée faute de données) :")
    for name, c in r["bench_figures"].items():
        print(f"  {name:<24} {c:>4}" + ("  écartée (plot.skip)" if name in r["skip"] else ""))
    for line in r["alerts"]:
        print(f"\nALERTE {line}")
    if r["unmatched_platforms"]:
        print("\nPlateformes sans indice de famille (à nommer) : "
              + ", ".join(r["unmatched_platforms"]))
    if r["proposed"] != cfg["plot"]:
        print("\nBloc plot proposé (règles déduites des libellés « autre » : à relire, regrouper "
              "et renommer avant de l'éprouver par bin/pdb base check --config) :")
        print(plotdata.plot_json(r["proposed"]))
    else:
        print("\nAucun changement à proposer.")
    return 0


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
    from lib import query, schema
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
    own = p.add_mutually_exclusive_group()
    own.add_argument("--own", action="store_true", help="mesures propres seulement (paper_id own-…)")
    own.add_argument("--no-own", action="store_true", help="littérature seulement")
    p.add_argument("--cols", help="colonnes à afficher, séparées par des virgules")
    p.add_argument("--count", metavar="COL,COL", help="synthèse : nombre de lignes par combinaison de ces colonnes")
    p.add_argument("--sort", metavar="COL", help="tri croissant (n/r en dernier)")
    p.add_argument("--desc", action="store_true", help="tri décroissant")
    p.add_argument("-n", type=int, help="nombre maximal de lignes")
    p.add_argument("--format", choices=("tsv", "md", "json"), default="tsv")
    p.add_argument("--max-chars", type=int)
    p.add_argument("--check", action="store_true", help=(
        "lignes filtrées qui ont un chunk_id : chaque valeur numérique est-elle dans le passage "
        "cité ? code 1 si une valeur manque (sans original_value lu) ou si un chunk_id est introuvable"))
    p.add_argument("--comparable", nargs="?", const="accuracy", choices=("accuracy", "power"),
                   help=("regroupe les lignes filtrées par conditions de comparaison (task, dataset, "
                         "dataset_split, métrique ; + power_scope en mode power) et signale les "
                         "comparaisons impossibles ; accuracy par défaut"))
    p.add_argument("--add-columns", metavar="COL,…|all", help=(
        "ajoute à l'en-tête ces colonnes optionnelles (n/r dans les lignes existantes) : "
        + ", ".join(schema.OPTIONAL_COLUMNS)))
    a = p.parse_args(args)

    if a.add_columns:
        cols = (list(schema.OPTIONAL_COLUMNS) if a.add_columns.strip() == "all"
                else [c.strip() for c in a.add_columns.split(",") if c.strip()])
        try:
            added = query.add_columns(ROOT, cols)
        except ValueError as e:
            print(f"pdb bench : {e}", file=sys.stderr)
            return 2
        print(f"colonnes ajoutées : {', '.join(added)}" if added else "rien à ajouter")
        if added:
            _refresh_figures(("bench", "corpus"))
        return 0

    header, rows = query.load_benchmarks(ROOT)
    line_of = {id(r): i for i, r in enumerate(rows, start=2)}
    metas = query.load_papers(ROOT)
    short = query.short_ids(metas)
    try:
        contains = _pairs(a.where, number=False)
        contains.update({c: getattr(a, c) for c in BENCH_SHORTCUTS if getattr(a, c)})
        if a.quant:
            contains["quantization"] = a.quant
        minimum, maximum = _pairs(a.min, number=True), _pairs(a.max, number=True)
        cols = query.select_columns([c.strip() for c in a.cols.split(",")] if a.cols else [], header)
        count_cols = [c.strip() for c in a.count.split(",")] if a.count else []
        for c in [*contains, *minimum, *maximum, *a.has, *([a.sort] if a.sort else []), *count_cols]:
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

    if a.own or a.no_own:
        rows = [r for r in rows if schema.is_own_id(r["paper_id"]) == a.own]
    rows = query.filter_rows(rows, contains, minimum, maximum, a.has)
    if a.sort:
        rows = query.sort_rows(rows, a.sort, desc=a.desc)
    if a.n and not a.comparable:  # avec --comparable, -n porte sur les groupes
        rows = rows[:a.n]
    if not rows:
        print("# aucune ligne", file=sys.stderr)
        return 1
    if a.check:
        results = query.check_rows(ROOT, [(line_of[id(r)], r) for r in rows])
        if not results:
            print("# aucune ligne filtrée n'a de chunk_id", file=sys.stderr)
            return 0
        print(query.render_check(results, short))
        return int(any(x["status"] in ("absent", "introuvable") for x in results))
    if a.comparable:
        groups = query.comparable_groups(rows, a.comparable)
        if not groups:
            print(f"# aucune ligne filtrée n'a de {query.COMPARE_VALUE[a.comparable]}", file=sys.stderr)
            return 1
        print(query.render_comparable(groups, short, a.comparable, a.format, a.max_chars, a.n))
        return 0
    if count_cols:
        print(query.count_rows(rows, count_cols, short))
        return 0
    print(query.render(rows, cols, short, a.format, a.max_chars))
    return 0


MULTI_FIELDS = ("short", "year", "type", "title")


def _one_paper(prog, q, found, short):
    """Le papier unique désigné par q ; sinon message (candidats si ambigu) et None."""
    if not found:
        print(f"{prog} : aucun papier ne correspond à {q!r}", file=sys.stderr)
        return None
    if len(found) > 1:
        print(f"# {len(found)} papiers correspondent ; préciser avec l'id court :")
        for m in found:
            print(f"{short[m['id']]}\t{m.get('year') or 'n/r'}\t{m.get('title') or 'n/r'}")
        return None
    return found[0]


def _paper_many(a, metas, short, fields):
    """pdb paper id1 id2 … : une ligne par papier ; un argument ambigu ou inconnu est
    signalé sur stderr sans empêcher les autres (code 1 à la fin)."""
    from lib import query
    if a.bench:
        print("pdb paper : --bench ne s'utilise qu'avec un seul papier", file=sys.stderr)
        return 2
    _, rows = query.load_benchmarks(ROOT)
    n_bench = {}
    for r in rows:
        n_bench[r["paper_id"]] = n_bench.get(r["paper_id"], 0) + 1
    cards, rc = [], 0
    for q in a.query:
        found = query.resolve(q, metas)
        if len(found) != 1:
            what = "aucun papier" if not found else "ambigu : " + ", ".join(short[m["id"]] for m in found)
            print(f"# {q} : {what}", file=sys.stderr)
            rc = 1
            continue
        m = found[0]
        try:
            cards.append(query.card_values(m, n_bench.get(m["id"], 0), short[m["id"]], fields))
        except ValueError as e:
            print(f"pdb paper : {e}", file=sys.stderr)
            return 2
    if cards:
        print(query.paper_table(cards))
    return rc


def cmd_cites(args, reverse=False):
    import argparse
    from lib import query, refs
    prog = "pdb cited-by" if reverse else "pdb cites"
    p = argparse.ArgumentParser(prog=prog, description=(
        "Papiers de la base qui citent ce papier (rapprochement de refs.jsonl, lib/refs.py)."
        if reverse else
        "Références de ce papier présentes dans la base (rapprochement de refs.jsonl, "
        "lib/refs.py). --external : aussi les travaux hors base, avec leur nombre de "
        "citants dans le corpus."))
    p.add_argument("query", help="id complet, court, ou mot du titre")
    if not reverse:
        p.add_argument("--external", action="store_true",
                       help="ajoute les références hors base (ext, n_citants, année, titre, id)")
    a = p.parse_args(args)

    papers = refs.load_papers(ROOT)
    short = query.short_ids(papers)
    meta = _one_paper(prog, a.query, query.resolve(a.query, papers), short)
    if meta is None:
        return 1
    cites, citers, groups = refs.citations(papers)
    by_id = {m["id"]: m for m in papers}
    targets = citers.get(meta["id"], set()) if reverse else cites.get(meta["id"], set())
    external = not reverse and a.external
    lines = query.citation_lines(targets, by_id, short, groups if external else None, citers)
    n_int = sum(1 for t in targets if t in by_id)
    if reverse:
        print(f"# {n_int} papier(s) de la base citent {short[meta['id']]}")
    else:
        n_ext = sum(1 for t in targets if t not in by_id)
        print(f"# {short[meta['id']]} cite {n_int} papier(s) de la base et {n_ext} travaux hors base"
              + ("" if external else " (--external pour les lister)"))
    if lines:
        print("\n".join(lines))
    used = sorted(t for t in targets if t in by_id and short[t] != t)
    if used:
        print("# ids: " + " ".join(f"{short[t]}={t}" for t in used))
    return 0


def cmd_cited_by(args):
    return cmd_cites(args, reverse=True)


def cmd_paper(args):
    import argparse
    from lib import query
    p = argparse.ArgumentParser(prog="pdb paper", description=(
        "Fiche d'identité d'un papier : id complet, id court (arXiv ou année-auteur) "
        "ou mot du titre. Plusieurs correspondances → liste des candidats. Plusieurs "
        "arguments → une ligne TSV par papier (champs par défaut : "
        f"{','.join(MULTI_FIELDS)})."))
    p.add_argument("query", nargs="+")
    p.add_argument("--fields", help=f"champs parmi : {','.join(query.CARD_FIELDS)}")
    p.add_argument("--bench", action="store_true", help="ajoute les lignes de benchmarks.csv")
    p.add_argument("--format", choices=("tsv", "md", "json"), default="tsv",
                   help="format des lignes de benchmark")
    a = p.parse_args(args)

    metas = query.load_papers(ROOT)
    short = query.short_ids(metas)
    fields = [f.strip() for f in a.fields.split(",")] if a.fields else None
    if len(a.query) > 1:
        return _paper_many(a, metas, short, fields or list(MULTI_FIELDS))
    found = query.resolve(a.query[0], metas)
    meta = _one_paper("pdb paper", a.query[0], found, short)
    if meta is None:
        return 1
    header, rows = query.load_benchmarks(ROOT)
    rows = [r for r in rows if r["paper_id"] == meta["id"]]
    try:
        print(query.paper_card(meta, len(rows), short[meta["id"]], fields))
    except ValueError as e:
        print(f"pdb paper : {e}", file=sys.stderr)
        return 2
    if a.bench and rows:
        print()
        print(query.render(rows, header, short, a.format))
    return 0


def _rag_index(rerank=False, gpu=False):
    from lib import rag
    return rag, rag.Index(ROOT, rerank=rerank, gpu=gpu)


def cmd_search(args):
    import argparse
    from lib import query
    p = argparse.ArgumentParser(prog="pdb search", description=(
        "Passages pertinents (BM25 + embeddings, fusion RRF). Sortie : chunk_id court, "
        "section, page, score, extrait. Le corpus est en anglais : formuler en anglais. "
        "Lire ensuite un passage avec pdb show <chunk_id>."))
    p.add_argument("query")
    p.add_argument("-k", type=int, default=8)
    p.add_argument("--paper", metavar="ID", help="id complet, court, ou mot du titre")
    p.add_argument("--axis")
    p.add_argument("--section", help="sous-chaîne du titre de section")
    p.add_argument("--kind", choices=("abstract", "section", "figure", "table"))
    p.add_argument("--mode", choices=("hybrid", "dense", "lexical"), default="hybrid")
    p.add_argument("--rerank", action="store_true", help=(
        "reclasse les 30 premiers par un cross-encoder (anglais) : meilleur en anglais, "
        "un peu moins bon en français (docs/RAG.md §10)"))
    engine = p.add_mutually_exclusive_group()
    engine.add_argument("--gpu", dest="gpu", action="store_const", const=True, help=(
        "moteur Qwen3 sur GPU CUDA (route GPU, pdb gpu) ; défaut : le réglage de pdb gpu"))
    engine.add_argument("--cpu", dest="gpu", action="store_const", const=False,
                        help="moteur CPU (bge-small, MiniLM) même si la route GPU est active")
    p.add_argument("--ids-only", action="store_true")
    p.add_argument("--format", choices=("tsv", "json"), default="tsv")
    a = p.parse_args(args)

    rag, ix = _rag_index(rerank=a.rerank, gpu=a.gpu)
    if ix.note:
        print(f"# {ix.note}", file=sys.stderr)
    ids = None
    if a.paper:
        found = query.resolve(a.paper, ix.metas)
        if not found:
            print(f"pdb search : aucun papier ne correspond à {a.paper!r}", file=sys.stderr)
            return 1
        ids = {m["id"] for m in found}
    hits = ix.search(a.query, k=a.k, mode=a.mode, paper_ids=ids, axis=a.axis,
                     kind=a.kind, section=a.section, rerank=a.rerank)
    if not hits:
        print("# aucun passage", file=sys.stderr)
        return 1
    if a.format == "json":
        print(json.dumps([{**{k: h[k] for k in ("chunk_id", "paper_id", "section", "subsection",
                                                 "page", "score", "cos", "sha1")},
                           "model": ix.model if h["mode"] != "lexical" else None} for h in hits],
                         ensure_ascii=False, indent=1))
        return 0
    if hits[0]["mode"] != a.mode:
        print(f"# mode: {hits[0]['mode']} seul (embeddings indisponibles ou index à reconstruire : bin/pdb reindex)")
    if a.ids_only:
        print("\n".join(ix.short_chunk_id(h["chunk_id"]) for h in hits))
    else:
        print("chunk\tsection\tpage\tcos\tsnippet")
        for h in hits:
            sec = " / ".join(x for x in (h["section"], h.get("subsection")) if x)
            cos = "n/r" if h["cos"] is None else f"{h['cos']:.2f}"
            print(f"{ix.short_chunk_id(h['chunk_id'])}\t{sec}\t{h['page'] or 'n/r'}\t"
                  f"{cos}\t{rag.snippet(h['text'], a.query, ix.bm25.idf)}")
    used = sorted({h["paper_id"] for h in hits if ix.short.get(h["paper_id"]) != h["paper_id"]})
    if used:
        print("# ids: " + " ".join(f"{ix.short[p]}={p}" for p in used))
    return 0


def cmd_show(args):
    import argparse
    p = argparse.ArgumentParser(prog="pdb show", description=(
        "Texte exact d'un ou plusieurs passages. En-tête : chunk_id, section, page, "
        "sha1 (8 caractères, pour pdb verify --sha1)."))
    p.add_argument("chunk_ids", nargs="+")
    p.add_argument("--context", type=int, default=0, help="passages voisins de part et d'autre")
    a = p.parse_args(args)
    rag, ix = _rag_index()
    rc = 0
    for cid in a.chunk_ids:
        full = ix.resolve_chunk(cid)
        if not full:
            print(f"pdb show : passage inconnu : {cid}", file=sys.stderr)
            rc = 1
            continue
        for c in ix.get(full, a.context):
            sec = " / ".join(x for x in (c["section"], c.get("subsection")) if x)
            mark = "" if c["chunk_id"] == full else " (contexte)"
            print(f"## {ix.short_chunk_id(c['chunk_id'])} — {sec} — p. {c['page'] or 'n/r'} "
                  f"— sha1:{c['sha1'][:8]}{mark}")
            print(c["text"])
            print()
    return rc


def cmd_verify(args):
    import argparse
    p = argparse.ArgumentParser(prog="pdb verify", description=(
        "Vérifie qu'une citation figure dans un passage (casse, espaces, ponctuation, "
        "ligatures et césures ignorées). OK = exacte, APPROX = ressemblance ≥ 0,85, "
        "NOMBRES = ressemblance ≥ 0,85 mais nombres différents du passage, ABSENT sinon. "
        "Une citation trouvée ailleurs dans le papier est signalée. Code 0 : OK ou APPROX."))
    p.add_argument("chunk_id")
    p.add_argument("quote")
    p.add_argument("--sha1", help="préfixe du sha1 relevé par pdb show : MODIFIÉ s'il a changé")
    a = p.parse_args(args)
    rag, ix = _rag_index()
    full = ix.resolve_chunk(a.chunk_id)
    if not full:
        print(f"pdb verify : passage inconnu : {a.chunk_id}", file=sys.stderr)
        return 2
    status, ratio, where = rag.verify(ix, full, a.quote, a.sha1)
    elsewhere = f"\ttrouvée dans {ix.short_chunk_id(where)}" if where != full else ""
    print(f"{status}\t{ratio:.2f}\t{ix.short_chunk_id(full)}{elsewhere}")
    return 0 if status in ("OK", "APPROX") and where == full else 1


def cmd_gpu(args):
    import argparse
    from lib import rag_models
    p = argparse.ArgumentParser(prog="pdb gpu", description=(
        "Route GPU optionnelle : Qwen3-Embedding-4B et Qwen3-Reranker-4B sur GPU CUDA. "
        "Désactivée par défaut : pdb search, /paper-ask et pdb eval restent sur le moteur CPU. "
        "Activée (réglage de la machine, ou PDB_GPU=1), pdb search et pdb reindex utilisent "
        "Qwen ; pdb rag et /paper-research (acquisition open access) en dépendent."))
    p.add_argument("action", nargs="?", default="status", choices=("status", "on", "off", "download"))
    a = p.parse_args(args)
    if a.action == "off":
        rag_models.set_wanted(False)
        print("route GPU désactivée : moteur CPU (pdb search, /paper-ask)")
        return 0
    reason = rag_models.unavailable()
    if a.action in ("on", "download"):
        if reason:
            print(f"pdb gpu {a.action} : {reason} ; la route CPU reste utilisée", file=sys.stderr)
            return 1
        if a.action == "on":
            rag_models.set_wanted(True)
        if a.action == "download" or not rag_models.models_cached():
            print("téléchargement des modèles Qwen épinglés (≈ 16 Go, une seule fois)…")
            rag_models.download_models()
        if a.action == "on":
            print("route GPU activée ; encodage des passages de la base active (pdb reindex)…")
            return cmd_reindex([])
        return 0
    env = os.environ.get("PDB_GPU")
    print(f"demandée\t{'oui' if rag_models.wanted() else 'non'}"
          f"{f' (PDB_GPU={env})' if env else f' ({rag_models.config_path()})'}")
    if reason:
        print(f"disponible\tnon : {reason}")
    else:
        import torch
        print(f"disponible\toui : {torch.cuda.get_device_name(0)}")
    print(f"modèles\t{'en cache' if rag_models.models_cached() else 'absents (pdb gpu download)'}"
          f"\t{rag_models.EMBED}, {rag_models.RERANK}")
    from lib import rag
    gpu_vecs = rag._cache_path(ROOT, rag.GPU_MODEL).exists()
    sqlite = (ROOT / ".cache" / "rag" / "index.sqlite3").exists()
    print(f"base {ROOT.name}\tvecteurs Qwen : {'oui' if gpu_vecs else 'non'} ; "
          f"index pdb rag : {'oui' if sqlite else 'non'}")
    ok, _ = rag_models.enabled()
    print(f"route utilisée\t{'GPU (Qwen3)' if ok and gpu_vecs else 'CPU (bge-small)'}")
    return 0


def cmd_test(args):
    if "--rag" in args:
        return cmd_eval(["--rag"])
    return subprocess.run([sys.executable, "-m", "unittest", "discover", "tests", *args],
                          cwd=CODE).returncode


def cmd_rag(args):
    import rag_cli
    return rag_cli.run(args)


def cmd_synth(args):
    import bench_cli
    return bench_cli.run(args)


def _fmt(v):
    return "n/r" if v is None else f"{v:.2f}" if isinstance(v, float) else str(v)


def _print_eval(res):
    """Résumé lisible d'un run de pdb eval (le détail complet est dans le JSON)."""
    ex = res.get("extraction")
    if ex:
        q, h, t = ex["quality"], ex["header"], ex["tables"]
        print(f"## Extraction ({q['papers']} papiers, {q['grobid']} par GROBID, {q['words']} mots)")
        print(f"couverture du texte PDF\tmoy. {_fmt(q['coverage_mean'])}\tmin. {_fmt(q['coverage_min'])}"
              f"\t({', '.join(q['coverage_worst'])})")
        print(f"tableaux avec corps\t{_fmt(q['tables_with_body_rate'])}\t({q['tables']} tableaux, "
              f"reconstruits : {q['tables_recovered']} PyMuPDF, {q.get('tables_docling', 0)} Docling)")
        print(f"ligatures restantes / 10k mots\t{_fmt(q['ligature_leftover_per_10k'])}")
        print(f"papiers : sections non détectées\t{q['papers_missed_sections']}\t"
              f"titres espacés\t{q['papers_spaced_headings']}")
        print(f"avertissements / papier\t{_fmt(q['warnings_per_paper'])}")
        print(f"en-tête GROBID\ttitre {_fmt(h['title'])}\tannée {_fmt(h['year'])}\tDOI {_fmt(h['doi'])}"
              f"\tarXiv {_fmt(h['arxiv_id'])}\tauteurs F1 {_fmt(h['authors_f1'])}")
        print(f"valeurs de benchmarks.csv\tdans le tableau cité {_fmt(t['in_cited_table'])}\t"
              f"dans le texte {_fmt(t['in_text'])}\t({t['values']} valeurs)\t"
              f"lignes « tableaux seuls » : {_fmt(t.get('table_only_in_cited_table'))} ({t.get('table_only_values')} valeurs)\t"
              f"dans le passage cité (chunk_id) : {_fmt(t.get('in_cited_chunk'))} ({t.get('cited_chunk_values', 0)} valeurs)")
        print()
    rg = res.get("rag")
    if rg:
        print(f"## Recherche de passages ({rg['passages']} passages, {rg['model']})")
        print("jeu\tmode\trecall@5\trecall@10\tMRR\tnDCG@10\tpaper@5")
        for name, st in rg["sets"].items():
            for mode, m in st.items():
                if mode == "n":
                    continue
                print(f"{name} ({st['n']} q.)\t{mode}\t{m['recall@5']:.2f}\t{m['recall@10']:.2f}\t"
                      f"{m['mrr']:.2f}\t{m['ndcg@10']:.2f}\t{m['paper@5']:.2f}")
                for q in m["misses"]:
                    print(f"#   manqué : {q}")
        lr = rg.get("low_relevance", {})
        if lr.get("n"):
            n = lr["n"]
            print(f"pertinence faible\tseuil (calibration : {n['cal_pos']} + {n['cal_neg']} q.)\t"
                  f"validation ({n['val_pos']} + {n['val_neg']} q.) : hors corpus signalés\tdu corpus signalés"
                  "\tadopté")
            for sig in ("cos", "rerank"):
                d = lr[sig]
                v = d["validation"]
                print(f"\t{sig}\t{d['threshold']:.2f}\t{v['flagged_negatives']:.2f}\t{v['flagged_positives']:.2f}"
                      f"\t{'oui' if d['adopted'] else 'non'}")
                if "current" in d:
                    c = d["current"]
                    print(f"\t{sig} (seuil en place {c['threshold']})\t\t{c['flagged_negatives']:.2f}"
                          f"\t{c['flagged_positives']:.2f}")
        print("verify\tcas\tacceptés\tstatuts")
        for case, v in rg["verify"].items():
            print(f"\t{case} ({v['n']})\t{v['accepted_rate']:.2f}\t{v['status']}")
        print()
    sp = res.get("speed")
    if sp:
        print("## Temps (médianes)")
        print("extraction hors GROBID (s)\t" + "\t".join(f"{k} {v:.2f}" for k, v in sp["extract_s"].items()))
        print("repli PyMuPDF (s)\t" + "\t".join(f"{k} {v:.2f}" for k, v in sp["pymupdf_fallback_s"].items()))
        print(f"chargement de l'index (s)\t{sp['index_load_s']:.2f}\t({sp['passages']} passages, cache {_fmt(sp['cache_mb'])} Mo)")
        if "encode_passages_per_s" in sp:
            print(f"encodage\t{sp['encode_passages_per_s']:.0f} passages/s\tindex complet ≈ {sp['full_encode_estimate_s']:.0f} s")
        for k, v in sp.items():
            if k.startswith("search_"):
                print(f"{k[7:-3]} (ms)\tp50 {v['p50']:.0f}\tp95 {v['p95']:.0f}")
        print(f"verify (ms)\t{sp['verify_ms']:.0f}")
        if "cli_s" in sp:
            print("commandes à froid (s)\t" + "\t".join(f"{k} {v:.2f}" for k, v in sp["cli_s"].items()))
    an = res.get("answers")
    if an:
        print(f"## Réponses finales ({an['records']} enregistrements, {an['run']})")
        for name, p in an["invalid"].items():
            print(f"# non conforme : {name} : {'; '.join(p)}")
        if an["unknown_ids"]:
            print(f"# ids hors jeux : {', '.join(an['unknown_ids'])}")
        cols = ("verdict_accuracy", "citation_accept_rate", "unsupported_claim_rate",
                "gold_source_recall", "gold_value_recall")
        print("jeu / catégorie\tn\tverdict juste\tcitations acceptées\taffirmations non soutenues"
              "\tsources attendues\tvaleurs attendues")
        for name, s in an["sets"].items():
            print(f"{name} ({s['answered']}/{s['cases']} répondues)\t{s['n']}\t" + "\t".join(_fmt(s[c]) for c in cols))
            for cat, c in s["by_category"].items():
                print(f"\t{cat}\t{c['n']}\t" + "\t".join(_fmt(c[k]) for k in cols))
            print(f"\thors corpus reconnu (absent ou partiel)\t{_fmt(s['absent_recognized'])}"
                  f"\t« absent » à tort\t{_fmt(s['false_absent'])}")
            if "human" in s:
                h = s["human"]
                print(f"\tnotes humaines ({h['n']} réponses, /1)\t" +
                      "\t".join(f"{c} {_fmt(v)}" for c, v in h.items() if c != "n"))
            if s["missing"]:
                print(f"#   sans réponse : {', '.join(s['missing'])}")
            for qid, q in s["per_question"].items():
                if not q["verdict_ok"] or q["unsupported_claims"]:
                    print(f"#   {qid} : verdict {q['verdict']}{'' if q['verdict_ok'] else ' (attendu autre)'}"
                          f", {q['unsupported_claims']} affirmation(s) non soutenue(s), citations {q['citation_status']}")


def cmd_eval(args):
    import argparse
    import datetime
    from lib import evaluation as ev
    p = argparse.ArgumentParser(prog="pdb eval", description=(
        "Banc d'évaluation (docs/EVAL.md) : qualité d'extraction, recherche de passages, "
        "vérification de citations, temps. Sans option : tous les volets."))
    p.add_argument("--extract", action="store_true", help="qualité de l'extraction")
    p.add_argument("--rag", action="store_true", help="recherche de passages, pertinence faible, verify")
    p.add_argument("--speed", action="store_true", help="temps d'exécution")
    p.add_argument("--gpu", action="store_true",
                   help="volet --rag avec le moteur Qwen (route GPU, pdb gpu) au lieu du moteur CPU")
    p.add_argument("--no-cli", action="store_true", help="--speed sans chronométrer les commandes à froid")
    p.add_argument("--answers", metavar="DIR", nargs="+",
                   help="note les réponses enregistrées d'un run (dossier de JSON, docs/EVAL.md §10) ; "
                        "seul volet lancé s'il est le seul demandé")
    p.add_argument("--questions", nargs="?", const="answers", metavar="JEU",
                   help="affiche id et question d'un jeu de réponses (answers, answers_holdout), "
                        "sans les attentes, puis s'arrête")
    p.add_argument("--save", action="store_true", help="enregistre eval/results/<date>-<commit>.json")
    p.add_argument("--compare", nargs="?", const="last", metavar="JSON",
                   help="écarts avec un run enregistré (défaut : le dernier) ; code 1 si un seuil n'est pas atteint")
    a = p.parse_args(args)
    fixtures, results, thresholds_path = ev.paths(ROOT, CODE)
    if a.questions:
        if a.questions not in ev.ANSWER_SETS:
            p.error(f"--questions : {' | '.join(ev.ANSWER_SETS)}")
        qs = ev.answer_questions(fixtures, a.questions)
        if not qs:
            print(f"pdb eval : aucun jeu {a.questions}.jsonl dans {fixtures}", file=sys.stderr)
            return 1
        for qid, q in qs:
            print(f"{qid}\t{q}")
        return 0
    records = []
    for d in a.answers or ():
        path = Path(d).expanduser()
        if not path.exists() and (ROOT / d).exists():
            path = ROOT / d
        if not path.exists():
            p.error(f"--answers : introuvable : {d}")
        records.append(path)
    if not (a.extract or a.rag or a.speed or a.answers):
        a.extract = a.rag = a.speed = True
    # le banc porte sur la base active : ses questions (eval/fixtures/, à défaut celles du
    # code, écrites pour la base fpga), ses seuils et ses runs enregistrés (evaluation.paths)
    print(f"# base : {base.CONFIG['name']} ({ROOT}) ; questions : {fixtures}\n")
    res = {}
    if a.extract:
        res["extraction"] = {"quality": ev.extraction_quality(ROOT), "header": ev.header_accuracy(ROOT),
                             "tables": ev.table_values(ROOT)}
    if a.rag:
        try:
            res["rag"] = ev.rag_quality(ROOT, fixtures, gpu=a.gpu)
        except RuntimeError as e:
            print(f"pdb eval --gpu : {e}", file=sys.stderr)
            return 1
    if a.speed:
        res["speed"] = ev.speed(ROOT, fixtures, cli=not a.no_cli)
    if a.answers:
        res["answers"] = {"run": ", ".join(map(str, records)), **ev.answers_quality(ROOT, fixtures, records)}
    _print_eval(res)

    flat = ev.flatten(res)
    thresholds = json.loads(thresholds_path.read_text())
    fails = [f for f in ev.check_thresholds(flat, thresholds) if f[0].split(".")[0] in res]
    if a.compare:
        runs = sorted(results.glob("*.json"))
        ref = Path(a.compare) if a.compare != "last" else (runs[-1] if runs else None)
        if ref is None:
            print("\n# aucun run enregistré à comparer (pdb eval --save)")
        else:
            old = ev.flatten({k: v for k, v in json.loads(ref.read_text())["results"].items() if k in res})
            diffs = ev.compare(old, flat)
            print(f"\n## Écarts avec {ref.name} ({len(diffs)})")
            for key, x, y in diffs:
                arrow = "" if x is None or y is None else "▲" if y > x else "▼"
                print(f"{key}\t{_fmt(x)} → {_fmt(y)}\t{arrow}")
    for key, v, bound in fails:
        print(f"# seuil non atteint : {key} = {_fmt(v)} ({bound})")
    if a.save:
        sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=CODE,
                             capture_output=True, text=True).stdout.strip() or "nogit"
        dirty = subprocess.run(["git", "status", "--porcelain", "--", "lib", "bin"], cwd=CODE,
                               capture_output=True, text=True).stdout.strip()
        stamp = datetime.datetime.now().strftime("%Y-%m-%dT%H%M")
        results.mkdir(parents=True, exist_ok=True)
        out = results / f"{stamp}-{sha}{'-dirty' if dirty else ''}{'-gpu' if a.gpu else ''}.json"
        out.write_text(json.dumps({"date": stamp, "commit": sha, "dirty": bool(dirty),
                                   "base": base.CONFIG["name"], "volets": sorted(res), "results": res},
                                  ensure_ascii=False, indent=1, default=str) + "\n")
        print(f"\nenregistré : {out.relative_to(ROOT)}")
        _refresh_figures(("eval",))
    return 1 if (a.compare and fails) else 0


COMMANDS = {
    "base": cmd_base, "status": cmd_status, "add": cmd_add, "ingest": cmd_ingest, "reindex": cmd_reindex,
    "discover": cmd_discover, "grobid": cmd_grobid, "viz": cmd_viz, "test": cmd_test,
    "eval": cmd_eval, "bench": cmd_bench, "paper": cmd_paper, "search": cmd_search, "show": cmd_show,
    "verify": cmd_verify, "cites": cmd_cites, "cited-by": cmd_cited_by,
    "rag": cmd_rag, "gpu": cmd_gpu, "synth": cmd_synth, "plot": cmd_plot,
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
