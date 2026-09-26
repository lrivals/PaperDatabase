#!/usr/bin/env python3
"""Découverte de papiers candidats via OpenAlex → candidates.csv et candidates_arxiv.txt.

usage : discover.py [--forward] [--backward] [--related] [--query "…"] [--axis AXE]
                    [--since ANNÉE] [--limit N] [--min-links N] [--top N]

Modes (combinables ; sans mode : --forward --backward) :
  --forward   travaux qui citent des papiers du corpus (les plus cités d'abord) ;
  --backward  travaux cités par au moins --min-links papiers du corpus ;
  --related   travaux « liés » selon OpenAlex ;
  --query     recherche par mots-clés ;
  --axis      recherche avec la requête par défaut d'un axe (ingest.AXIS_QUERIES).

Les papiers déjà en base sont exclus. Un candidat est « dans le sujet » s'il relève d'un axe
de ingest.HARDWARE_AXES, si son titre évoque le matériel (ingest.TITLE_TOPIC_RE) ou si son
résumé le fait au moins deux fois (ingest.TOPIC_RE). Rien n'est ajouté à la base : relire
candidates_arxiv.txt, puis `bin/pdb add --from candidates_arxiv.txt`. Voir docs/GUIDE.md.
"""
import argparse
import csv
import math
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "bin"))

import ingest  # noqa: E402
from lib import openalex, refs, schema  # noqa: E402

CANDIDATES = ROOT / "candidates.csv"
ARXIV_LIST = ROOT / "candidates_arxiv.txt"
FIELDS = ("rank", "score", "in_topic", "reasons", "title", "year", "venue", "doi", "arxiv_id",
          "oa_url", "cited_by_count", "axes_guess", "openalex_id")


class Pool:
    """Candidats indexés par titre normalisé (à défaut, identifiant OpenAlex), papiers du
    corpus exclus."""

    def __init__(self, papers, corpus_works):
        self.corpus_keys = {k for p in papers for k in refs.ref_keys(p)}
        self.corpus_oa = {openalex.short_id(w["id"]) for ws in corpus_works.values() for w in ws}
        self.items = {}

    def in_base(self, s):
        return s["openalex_id"] in self.corpus_oa or bool(set(refs.ref_keys(s)) & self.corpus_keys)

    def add(self, work, cites=0, cited_by=0, related=0, query=None):
        s = openalex.summary(work)
        if not s["title"] or self.in_base(s):
            return
        # versions arXiv et éditeur : deux travaux OpenAlex, un seul candidat
        key = refs.title_key(s["title"]) or s["openalex_id"]
        e = self.items.setdefault(key, {**s, "cites": 0, "cited_by": 0, "related": 0, "queries": []})
        for k in ("doi", "arxiv_id", "oa_url", "venue", "abstract"):
            e[k] = e[k] or s[k]
        if s["arxiv_id"] and e["venue"] and "arxiv" in e["venue"].lower() and s["venue"]:
            e["venue"] = s["venue"]
        e["cited_by_count"] = max(e["cited_by_count"], s["cited_by_count"])
        e["cites"] = max(e["cites"], cites)
        e["cited_by"] = max(e["cited_by"], cited_by)
        e["related"] = max(e["related"], related)
        if query and query not in e["queries"]:
            e["queries"].append(query)


def reasons(e):
    out = []
    if e["cites"]:
        out.append(f"cite {e['cites']} papier(s) du corpus")
    if e["cited_by"]:
        out.append(f"cité par {e['cited_by']} papiers du corpus")
    if e["related"]:
        out.append(f"lié à {e['related']} papier(s) du corpus (OpenAlex)")
    out += e["queries"]
    return " ; ".join(out)


def in_topic_of(title, text, axes):
    """Contexte matériel : axe matériel, titre explicite, ou mentions répétées (ingest.py).
    Un axe thématique seul (« autoencoder », « yolo ») ne suffit pas."""
    return (bool(set(axes) & set(ingest.HARDWARE_AXES))
            or bool(re.search(ingest.TITLE_TOPIC_RE, title or "", re.IGNORECASE))
            or len(re.findall(ingest.TOPIC_RE, text, re.IGNORECASE)) >= ingest.TOPIC_MIN_HITS)


def assess(e):
    """Axes devinés, pertinence et score d'un candidat."""
    text = " ".join(filter(None, (e["title"], e["abstract"])))
    axes, _ = ingest.classify(text, e["title"])
    in_topic = in_topic_of(e["title"], text, axes)
    score = (3 * max(e["cites"], e["cited_by"]) + e["related"] + 2 * bool(e["queries"])
             + 2 * len([a for a in axes if a != "surveys"])
             + math.log10(e["cited_by_count"] + 1))
    return axes, in_topic, round(score, 1)


def ranked(pool):
    rows = []
    for e in pool.items.values():
        axes, in_topic, score = assess(e)
        rows.append({**{k: e[k] for k in ("title", "year", "venue", "doi", "arxiv_id", "oa_url",
                                          "cited_by_count", "openalex_id")},
                     "score": score, "in_topic": "oui" if in_topic else "non",
                     "reasons": reasons(e), "axes_guess": ";".join(axes)})
    rows.sort(key=lambda r: (r["in_topic"] != "oui", -r["score"], -(r["year"] or 0)))
    for i, r in enumerate(rows, 1):
        r["rank"] = i
    return rows


def _corpus_ids(corpus_works):
    """{identifiant OpenAlex court: paper_id} pour toutes les versions des papiers."""
    return {openalex.short_id(w["id"]): pid for pid, ws in corpus_works.items() for w in ws}


def forward(client, pool, corpus_works, since, limit):
    ids_ = _corpus_ids(corpus_works)
    for pid, ws in corpus_works.items():
        for w in ws:
            flt = f"cites:{openalex.short_id(w['id'])}" + (f",from_publication_date:{since}-01-01" if since else "")
            for c in client.works(filter=flt, sort="cited_by_count:desc", limit=limit):
                cited = {ids_[r] for r in map(openalex.short_id, c.get("referenced_works") or []) if r in ids_}
                n = max(1, len(cited))
                pool.add(c, cites=n)


def backward(client, pool, corpus_works, min_links):
    citers = defaultdict(set)
    for pid, ws in corpus_works.items():
        for w in ws:
            for r in w.get("referenced_works") or []:
                citers[openalex.short_id(r)].add(pid)
    wanted = {r: c for r, c in citers.items() if len(c) >= min_links}
    for w in client.works_by_ids(wanted):
        n = len(wanted.get(openalex.short_id(w["id"]), ()))
        pool.add(w, cited_by=n)


def related(client, pool, corpus_works):
    near = defaultdict(set)
    for pid, ws in corpus_works.items():
        for w in ws:
            for r in w.get("related_works") or []:
                near[openalex.short_id(r)].add(pid)
    for w in client.works_by_ids(near):
        n = len(near.get(openalex.short_id(w["id"]), ()))
        pool.add(w, related=n)


def query(client, pool, q, since, limit, label=None):
    flt = f"from_publication_date:{since}-01-01" if since else None
    for w in client.works(search=q, filter=flt, limit=limit):
        pool.add(w, query=label or f"requête « {q} »")


def write_outputs(rows, top):
    with open(CANDIDATES, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: (schema.NR if r[k] in (None, "") else r[k]) for k in FIELDS})
    picks = [r for r in rows if r["in_topic"] == "oui" and r["arxiv_id"]][:top]
    lines = ["# Généré par bin/discover.py — candidats dans le sujet, disponibles sur arXiv.",
             "# Relire, supprimer les lignes non pertinentes, puis : bin/pdb add --from candidates_arxiv.txt",
             ""]
    lines += [f"{r['arxiv_id']:<14}# {r['title']} ({r['year']}) — {r['reasons']}" for r in picks]
    ARXIV_LIST.write_text("\n".join(lines) + "\n")
    return picks


def run(argv=None, client=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--forward", action="store_true")
    ap.add_argument("--backward", action="store_true")
    ap.add_argument("--related", action="store_true")
    ap.add_argument("--query", action="append", default=[], metavar="MOTS-CLÉS")
    ap.add_argument("--axis", action="append", default=[], choices=schema.AXES)
    ap.add_argument("--since", type=int, help="année de publication minimale (forward, query)")
    ap.add_argument("--limit", type=int, default=50, help="résultats par requête (défaut 50)")
    ap.add_argument("--min-links", type=int, default=2, help="backward : papiers citants minimum")
    ap.add_argument("--top", type=int, default=30, help="lignes de candidates_arxiv.txt (défaut 30)")
    args = ap.parse_args(argv)
    if not (args.forward or args.backward or args.related or args.query or args.axis):
        args.forward = args.backward = True

    client = client or openalex.Client()
    papers = refs.load_papers(ROOT)
    try:
        corpus_works = openalex.resolve_corpus(client, papers)
    except openalex.OpenAlexError as e:
        print(f"erreur  {e}", file=sys.stderr)
        return 1
    missing = [pid for pid, ws in corpus_works.items() if not ws]
    print(f"Corpus : {len(papers)} papiers, {len(papers) - len(missing)} retrouvés dans OpenAlex.")
    for pid in missing:
        print(f"  absent d'OpenAlex : {pid}")

    pool = Pool(papers, corpus_works)
    steps = []
    if args.forward:
        steps.append(("forward", lambda: forward(client, pool, corpus_works, args.since, args.limit)))
    if args.backward:
        steps.append(("backward", lambda: backward(client, pool, corpus_works, args.min_links)))
    if args.related:
        steps.append(("related", lambda: related(client, pool, corpus_works)))
    for q in args.query:
        steps.append((f"query « {q} »", lambda q=q: query(client, pool, q, args.since, args.limit)))
    for a in args.axis:
        steps.append((f"axis {a}", lambda a=a: query(client, pool, ingest.AXIS_QUERIES[a], args.since,
                                                      args.limit, label=f"axe {a}")))
    failed = 0
    for name, step in steps:
        try:
            step()
        except openalex.OpenAlexError as e:
            failed += 1
            print(f"erreur  {name} : {e}", file=sys.stderr)
    if not pool.items:
        print("Aucun candidat : candidates.csv inchangé.")
        return 1 if failed else 0

    rows = ranked(pool)
    picks = write_outputs(rows, args.top)
    n_in = sum(r["in_topic"] == "oui" for r in rows)
    print(f"candidates.csv : {len(rows)} candidats, {n_in} dans le sujet.")
    print(f"candidates_arxiv.txt : {len(picks)} candidats dans le sujet disponibles sur arXiv.\n")
    for r in [r for r in rows if r["in_topic"] == "oui"][:15]:
        where = f"arXiv {r['arxiv_id']}" if r["arxiv_id"] else (f"DOI {r['doi']}" if r["doi"] else "sans identifiant")
        print(f"{r['score']:5}  {r['year'] or '?'}  {(r['title'] or '')[:80]:<80}  {where}")
    return 1 if failed else 0


def main():
    sys.exit(run())


if __name__ == "__main__":
    main()
