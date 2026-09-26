"""Recherche GPU (lib/rag_qwen) sur les jeux de pdb eval (docs/EVAL.md §8).

Usage : .venv/bin/python eval/qwen_on_eval.py <racine> <sortie.json> (après bin/pdb rag index).
"""
import json, sys, time
from pathlib import Path
root = Path(sys.argv[1]); sys.path.insert(0, str(root))
from lib import evaluation as ev, rag_qwen, rag_models
fx = root / "tests" / "fixtures"
ORIGINAL = ("abstract", "section", "table", "figure")

def hits(q, mode, rerank, original_only):
    res = rag_qwen.search(root, q, mode=mode, limit=40 if original_only else 10, reranking=rerank)["results"]
    if original_only:
        res = [r for r in res if r["kind"] in ORIGINAL]
    return [{"section_id": r["locator"], "paper_id": r["paper_id"]} for r in res[:10]], res

out = {}
configs = [("lexical", False, False), ("dense", False, False), ("hybrid", False, False),
           ("hybrid", True, False), ("hybrid", True, True)]
for name in ev.RAG_SETS:
    qs = ev.load_jsonl(fx / f"{name}.jsonl")
    for mode, rr, orig in configs:
        per, misses, t = [], [], time.time()
        for q in qs:
            h, _ = hits(q["q"], mode, rr, orig)
            m = ev.ranking_metrics(h, q["expect"]); per.append(m)
            if not m["recall@5"]: misses.append(q["q"])
        key = f"{name}\t{mode}{'+rerank' if rr else ''}{' (original text only)' if orig else ''}"
        agg = {k: sum(m[k] for m in per) / len(per) for k in ("recall@5", "recall@10", "mrr", "ndcg@10", "paper@5")}
        agg["s_per_q"] = (time.time() - t) / len(qs); agg["misses"] = misses
        out[key] = agg
        print(key, " ".join(f"{k}={v:.2f}" for k, v in agg.items() if k != "misses"), flush=True)

# low relevance: best Qwen reranker score over top 3 hybrid passages (same protocol as main)
def score(q):
    res = rag_qwen.search(root, q, mode="hybrid", limit=3, reranking=True)["results"]
    return max((r["rerank_score"] for r in res), default=0.0)
sets = {n: [q for q in ev.load_jsonl(fx / f"{n}.jsonl") if not q.get("ambiguous")]
        for n in ("rag_eval", "rag_eval_neg", "rag_eval_holdout", "rag_eval_neg_holdout")}
sc = {n: [score(q["q"]) for q in qs] for n, qs in sets.items()}
t = ev.best_threshold(sc["rag_eval"], sc["rag_eval_neg"])
val = ev._rates(sc["rag_eval_holdout"], sc["rag_eval_neg_holdout"], t)
out["low_relevance"] = {"threshold": t, "calibration": ev._rates(sc["rag_eval"], sc["rag_eval_neg"], t),
                        "validation": val, "scores": sc,
                        "adopted": val["flagged_negatives"] >= .8 and val["flagged_positives"] <= .05}
print(json.dumps({k: v for k, v in out["low_relevance"].items() if k != "scores"}))
Path(sys.argv[2]).write_text(json.dumps(out, indent=1))
