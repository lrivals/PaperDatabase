#!/usr/bin/env python3
"""PaperDatabase — point d'entrée unique. Lancer via bin/pdb.

  status                    état de la base et prochaines actions
  add <id|doi|pdf>… [--from liste.txt] [--start-grobid]
                            ajoute des articles (arXiv, DOI, PDF local), ingère, réindexe
  ingest [--force] [pdf…]   ingère inbox/ (ou les PDF donnés), réindexe
  ingest --reparse [--tables docling [--ocr]] [id…]
                            ré-extrait les papiers déjà ingérés depuis leur TEI (sans GROBID) ;
                            --tables docling : Docling sur les tableaux restés sans corps
  reindex                   régénère INDEX.md et external_refs.csv, vérifie la cohérence
  discover [options]        cherche des papiers candidats (OpenAlex) → candidates.csv
  grobid start|stop|status  pilote le conteneur GROBID
  bench [filtres] [--cols a,b] [--sort col [--desc]] [-n N] [--format tsv|md|json]
                            filtre benchmarks.csv (sans LLM) ; bench -h pour les filtres
  paper <id|court|mot>… [--fields a,b] [--bench]
                            fiche d'identité d'un papier (métadonnées, statut, benchmarks) ;
                            plusieurs ids → une ligne par papier
  cites <id> [--external]   références du papier présentes dans la base (et hors base)
  cited-by <id>             papiers de la base qui le citent
  search "<question>" [-k 8] [--paper ID] [--section S] [--mode M] [--rerank]
                            passages pertinents, avec chunk_id, section, page (sans LLM)
  show <chunk_id>… [--context N]
                            texte exact d'un passage (id court accepté : 1612.07119#019.0)
  verify <chunk_id> "<citation>" [--sha1 X]
                            la citation figure-t-elle dans le passage ? OK | APPROX | NOMBRES | ABSENT
  viz [--port N]            visualisation du corpus (http://127.0.0.1:8050)
  plot [bench|eval|corpus|all] [--only a,b] [--out DIR] [--format png|pdf|svg] [--list]
                            figures statiques : benchmarks, évaluation, statistiques du corpus
  eval [--extract|--rag|--speed] [--save] [--compare [JSON]]
                            banc d'évaluation du logiciel (docs/EVAL.md)
  rag <command>             recherche GPU (Qwen3), preuves, acquisition open access
  synth <command>           benchmark synthétique (docs/BENCHMARK.md)
  test [--rag]              lance les tests (--rag : pdb eval --rag)

Guide : docs/GUIDE.md. Détail des scripts : SETUP.md §5. Requêtes : docs/RAG.md.
"""
import json
import subprocess
import sys
from pathlib import Path

CODE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(CODE))
sys.path.insert(0, str(CODE / "bin"))

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
    from datetime import datetime
    p = argparse.ArgumentParser(prog="pdb plot", description=(
        "Figures statiques (matplotlib) : benchmarks.csv, eval/results, statistiques du "
        "corpus. Écrit aussi manifest.json (sources et effectifs de chaque figure)."))
    p.add_argument("group", nargs="?", default="all", choices=("bench", "eval", "corpus", "all"))
    p.add_argument("--only", help="noms de figures séparés par des virgules (voir --list)")
    p.add_argument("--out", default=str(ROOT / "figures"), help="dossier de sortie (figures/)")
    p.add_argument("--format", default="png", choices=("png", "pdf", "svg"))
    p.add_argument("--list", action="store_true", help="liste les figures sans rien générer")
    a = p.parse_args(args)
    try:
        from lib import plotfig
    except ImportError as e:
        print(f"pdb plot : {e}. Installer : .venv/bin/pip install -r requirements-plot.txt",
              file=sys.stderr)
        return 1
    import matplotlib.pyplot as plt

    names = [n for n, (g, _, _) in plotfig.FIGURES.items() if a.group in ("all", g)]
    if a.only:
        wanted = [n.strip() for n in a.only.split(",") if n.strip()]
        unknown = [n for n in wanted if n not in plotfig.FIGURES]
        if unknown:
            print(f"pdb plot : figure(s) inconnue(s) : {', '.join(unknown)} (voir --list)",
                  file=sys.stderr)
            return 2
        names = wanted
    if a.list:
        for n in names:
            g, _, desc = plotfig.FIGURES[n]
            print(f"{g}\t{n}\t{desc}")
        return 0

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    manifest_path = out / "manifest.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    ctx = plotfig.Context(ROOT)
    failed = 0
    for n in names:
        g, fn, desc = plotfig.FIGURES[n]
        try:
            fig, info = fn(ctx)
        except LookupError as e:
            print(f"-  {n} : ignorée ({e})")
            continue
        except Exception as e:  # une figure cassée n'empêche pas les autres
            print(f"!  {n} : échec ({type(e).__name__}: {e})", file=sys.stderr)
            failed += 1
            continue
        path = out / f"{n}.{a.format}"
        fig.savefig(path, dpi=200 if a.format == "png" else None, bbox_inches="tight")
        plt.close(fig)
        manifest[n] = {"file": path.name, "group": g, "description": desc,
                       "generated": datetime.now().isoformat(timespec="seconds"), **info}
        try:
            shown = path.relative_to(ROOT)
        except ValueError:
            shown = path
        print(f"ok {shown}")
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + "\n")
    return 1 if failed else 0


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
    if a.n:
        rows = rows[:a.n]
    if not rows:
        print("# aucune ligne", file=sys.stderr)
        return 1
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


def _rag_index(rerank=False):
    from lib import rag
    return rag, rag.Index(ROOT, rerank=rerank)


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
    p.add_argument("--ids-only", action="store_true")
    p.add_argument("--format", choices=("tsv", "json"), default="tsv")
    a = p.parse_args(args)

    rag, ix = _rag_index(rerank=a.rerank)
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
        print(json.dumps([{k: h[k] for k in ("chunk_id", "paper_id", "section", "subsection",
                                              "page", "score", "cos", "sha1")} for h in hits],
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
              f"lignes « tableaux seuls » : {_fmt(t.get('table_only_in_cited_table'))} ({t.get('table_only_values')} valeurs)")
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
    p.add_argument("--no-cli", action="store_true", help="--speed sans chronométrer les commandes à froid")
    p.add_argument("--save", action="store_true", help="enregistre eval/results/<date>-<commit>.json")
    p.add_argument("--compare", nargs="?", const="last", metavar="JSON",
                   help="écarts avec un run enregistré (défaut : le dernier) ; code 1 si un seuil n'est pas atteint")
    a = p.parse_args(args)
    if not (a.extract or a.rag or a.speed):
        a.extract = a.rag = a.speed = True
    # le banc porte sur la base de référence livrée avec le code (questions des fixtures)
    fixtures = CODE / "tests" / "fixtures"
    res = {}
    if a.extract:
        res["extraction"] = {"quality": ev.extraction_quality(CODE), "header": ev.header_accuracy(CODE),
                             "tables": ev.table_values(CODE)}
    if a.rag:
        res["rag"] = ev.rag_quality(CODE, fixtures)
    if a.speed:
        res["speed"] = ev.speed(CODE, fixtures, cli=not a.no_cli)
    _print_eval(res)

    flat = ev.flatten(res)
    results = CODE / "eval" / "results"
    thresholds = json.loads((CODE / "eval" / "thresholds.json").read_text())
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
        out = results / f"{stamp}-{sha}{'-dirty' if dirty else ''}.json"
        out.write_text(json.dumps({"date": stamp, "commit": sha, "dirty": bool(dirty),
                                   "volets": sorted(res), "results": res},
                                  ensure_ascii=False, indent=1, default=str) + "\n")
        print(f"\nenregistré : {out.relative_to(CODE)}")
    return 1 if (a.compare and fails) else 0


COMMANDS = {
    "status": cmd_status, "add": cmd_add, "ingest": cmd_ingest, "reindex": cmd_reindex,
    "discover": cmd_discover, "grobid": cmd_grobid, "viz": cmd_viz, "test": cmd_test,
    "eval": cmd_eval, "bench": cmd_bench, "paper": cmd_paper, "search": cmd_search, "show": cmd_show,
    "verify": cmd_verify, "cites": cmd_cites, "cited-by": cmd_cited_by,
    "rag": cmd_rag, "synth": cmd_synth, "plot": cmd_plot,
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
