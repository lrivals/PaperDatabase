"""Evidence search and acquisition tools for the existing research assistant."""

import argparse
import contextlib
import json
import os
import sys
import time
from pathlib import Path

from lib import base, rag_qwen as rag

ROOT = Path(os.environ.get("PDB_RAG_ROOT", base.ROOT)).resolve()


def run(argv):
    parser = argparse.ArgumentParser(prog="bin/pdb rag", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    index = sub.add_parser("index")
    index.add_argument("--mode", choices=("lexical", "hybrid"), default="hybrid")
    index.add_argument("--download", action="store_true", help="download pinned local models")
    search = sub.add_parser("search")
    search.add_argument("query")
    search.add_argument("--mode", choices=("lexical", "dense", "hybrid"), default="hybrid")
    search.add_argument("--limit", type=int, default=12)
    search.add_argument("--paper")
    search.add_argument("--kind")
    search.add_argument("--no-rerank", action="store_true")
    evidence = sub.add_parser("evidence")
    evidence.add_argument("id")
    evidence.add_argument("--parent", action="store_true")
    benchmark = sub.add_parser("benchmarks")
    benchmark.add_argument("--filter-json", default="[]")
    acquire = sub.add_parser("acquire")
    acquire.add_argument("query")
    acquire.add_argument("--run", required=True)
    acquire.add_argument("--limit", type=int, default=3)
    approve = sub.add_parser("approve", help="import staged papers the user accepted")
    approve.add_argument("run")
    approve.add_argument("paper_ids", nargs="+")
    check = sub.add_parser("check-answer")
    check.add_argument("path", type=Path)
    evaluate = sub.add_parser("evaluate")
    evaluate.add_argument("path", type=Path)
    evaluate.add_argument("--mode", choices=("lexical", "dense", "hybrid"), default="hybrid")
    evaluate.add_argument("--rerank", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "index":
            result = rag.build(ROOT, mode=args.mode, download=args.download)
        elif args.command == "search":
            if not 1 <= args.limit <= 100:
                raise ValueError("limit must be 1..100")
            result = rag.search(ROOT, args.query, args.mode, args.limit,
                                args.paper, args.kind, False if args.no_rerank else None)
        elif args.command == "evidence":
            result = rag.evidence(ROOT, args.id, args.parent)
        elif args.command == "benchmarks":
            result = rag.benchmarks(ROOT, json.loads(args.filter_json))
        elif args.command == "acquire":
            if not 1 <= args.limit <= 8:
                raise ValueError("limit must be 1..8")
            from lib import rag_external
            with contextlib.redirect_stdout(sys.stderr):
                result = rag_external.acquire(ROOT, args.query, args.run, args.limit)
        elif args.command == "approve":
            from lib import rag_external
            with contextlib.redirect_stdout(sys.stderr):
                result = rag_external.approve(ROOT, args.run, args.paper_ids)
        elif args.command == "check-answer":
            result = rag.check_answer(ROOT, json.loads(args.path.read_text()))
        else:
            items = [json.loads(line) for line in args.path.read_text().splitlines() if line.strip()]
            db, _ = rag.open_index(ROOT)
            try:
                available = {r[0] for r in db.execute("SELECT id FROM evidence")}
            finally:
                db.close()
            for item in items:
                if not item.get("evidence_ids") or set(item["evidence_ids"]) - available:
                    raise ValueError("evaluation case has missing or unknown evidence_ids")
            cases = []
            for item in items:
                started = time.monotonic()
                hit = rag.search(ROOT, item["question"], args.mode, 20,
                                 kind=item.get("kind"), reranking=args.rerank)
                latency = time.monotonic() - started
                actual = [r["id"] for r in hit["results"]]
                wanted = set(item["evidence_ids"])
                ranks = [actual.index(eid) + 1 for eid in wanted if eid in actual]
                cases.append({"question": item["question"], "category": item.get("category"),
                              "kind": item.get("kind"),
                              "complete": wanted <= set(actual),
                              "recall_at_5": len(wanted & set(actual[:5])) / len(wanted),
                              "recall_at_10": len(wanted & set(actual[:10])) / len(wanted),
                              "recall_at_20": len(ranks) / len(wanted),
                              "reciprocal_rank": 1 / min(ranks) if ranks else 0,
                              "latency_s": round(latency, 3)})
            result = {"mode": args.mode, "rerank": args.rerank, "cases": cases,
                      "count": len(cases),
                      **{key: sum(x[key] for x in cases) / len(cases) if cases else None
                         for key in ("complete", "recall_at_5", "recall_at_10",
                                     "recall_at_20", "reciprocal_rank", "latency_s")}}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError, RuntimeError, json.JSONDecodeError) as e:
        print(f"rag: {type(e).__name__}: {e}", file=sys.stderr)
        return 1
