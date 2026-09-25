# RAG implementation on `dev`

The first release adds local evidence retrieval to the existing assistant. It follows the OpenScholar pattern: retrieve, draft, list up to three evidence gaps, search those gaps, revise, and verify citations. External open-access papers used as evidence are added to the library with a `todo` fiche.

1. Build a rebuildable SQLite FTS5 and Qwen3-Embedding-4B passage index over abstracts, sections, figures, tables, finished fiches, and benchmark configurations. Preserve exact source text, source hash, section, page hint, source type, and extraction warnings. Use BM25, dense cosine, reciprocal-rank fusion, and Qwen3-Reranker-4B. Keep derived data in `.cache/rag/` and existing corpus schemas intact.
2. Expose `bin/pdb rag index|search|evidence|benchmarks|acquire|check-answer|evaluate` as JSON-capable tools. Benchmark filters preserve `n/r`, units, metric names, and power scope; no top-k cap applies to structured exhaustive queries.
3. Discover relevant open-access papers with OpenAlex and arXiv, download and parse publicly available PDFs in a private staging directory, and deduplicate by DOI/arXiv/document hash. Import validated papers selected as answer evidence; never overwrite a curated paper. Reindex once after each batch. Preserve discovery query, URL, version/hash, extraction warnings, and source spans. Default run budget: eight searches, eight PDFs, 50 MB each, 200 MB total, 15 minutes acquisition time.
4. Teach the existing assistant a `/paper-ask` workflow: retain initial draft, make a single feedback list of up to three issues, perform at most one follow-up search per issue, collect evidence across all rounds, and check every final citation. Unsupported claims are qualified or removed. Existing fiche creation still reads the complete extracted paper.
5. Add fixture tests for provenance, chunking, FTS punctuation, ranking, unknown benchmark values, import/deduplication/failures, and CLI JSON. Smoke-test real Qwen models on the RTX 5090. Establish 30 checked pilot questions, then 100 questions split 40 development/60 held-out; compare retrieval and assistant workflow ablations, numerical reliability, citation support, and latency.

Runtime: Python 3.14; pinned `torch==2.14.0`, `transformers==5.17.0`, `numpy==2.5.3`; Qwen3 Embedding 4B revision `5cf2132abc99cad020ac570b19d031efec650f2b`, Qwen3 Reranker 4B revision `22e683669bc0f0bd69640a1354a6d0aebcfeede5`. Models use BF16, native Transformers formatting, and local inference after explicit setup. Research rationale and primary literature are in [the review](research/rag-improvement-study-2026-09-25.md).

## Implementation and measured pilot, 25 September 2026

The local index, typed retrieval, structured benchmark filters, citation identity/excerpt
checker, bounded staged open-access import, and `/paper-ask` prompt are implemented on
`dev`. The current corpus builds to 1,990 evidence records. A live isolated acquisition
of the SATAY arXiv PDF succeeded through discovery, download, PyMuPDF extraction, passage
relevance selection, library import, and index rebuild; it did not alter the real corpus.
The models ran on the local RTX 5090. The source files and existing schemas remain the
authoritative store; only `.cache/rag/` is derived.

`tests/fixtures/rag_pilot.jsonl` contains 30 manually worded questions with checked gold
source IDs: 15 abstract-level questions and 15 exact benchmark configurations, including
unknown power/FPS. Each case specifies its source type, reflecting the `/paper-ask` route
for contribution versus numeric questions. To reproduce the retrieval ablation:

```bash
bin/pdb rag evaluate tests/fixtures/rag_pilot.jsonl --mode lexical
bin/pdb rag evaluate tests/fixtures/rag_pilot.jsonl --mode dense
bin/pdb rag evaluate tests/fixtures/rag_pilot.jsonl --mode hybrid
bin/pdb rag evaluate tests/fixtures/rag_pilot.jsonl --mode hybrid --rerank
```

| Route | Exact gold recall@20 | Mean reciprocal rank | Mean query latency |
|---|---:|---:|---:|
| FTS5 lexical | 30/30 | 0.983 | 0.005 s |
| Qwen dense | 29/30 | 0.911 | 0.641 s |
| BM25+dense RRF | 30/30 | 0.983 | 0.643 s |
| RRF+Qwen reranker | 30/30 | 0.970 | 2.056 s |

These are small, type-directed retrieval smoke results, not an answer-quality or
generalization claim. In this pilot the dense channel and reranker do not improve over
lexical retrieval. The next evidence gate is 100 independently written and reviewed
questions, split 40 development / 60 held-out. It must include multi-paper synthesis,
paraphrased and multilingual queries, ambiguous numerical conditions, unavailable
evidence, citation support, and end-to-end answer judgments. Do not tune the system on
the held-out 60. Until then, keep lexical and typed benchmark search available as the
reliable route, and treat Qwen retrieval as an optional aid for vocabulary mismatch.
