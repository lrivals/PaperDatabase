# Synthetic benchmark dataset

Versioned export of `.cache/bench/`, the working directory of `bin/pdb synth`
([docs/BENCHMARK.md](../docs/BENCHMARK.md)). PDFs, GROBID output, caches, logs and the
generator model are not included; `corpus.json` gives each added paper's source URL and
PDF SHA-256.

## Contents

| Path | Content |
|---|---|
| `questions.jsonl` | The 200 validated questions: `id`, `question`, reference `answer`, `evidence` (`paper_id`, section `id`, verbatim `quote`), `forbidden` conclusions, `category`, `language`, `split`, `source_papers`, generator and usage, the two validator `validation` votes. Missing-evidence cases carry `absent_identity` / `absent_title` instead of evidence. |
| `variants.jsonl` | For 40 questions: `translated` (other language) and `short` rewordings, checked by Claude. |
| `candidates.jsonl` | All 329 generated candidates, accepted or not. |
| `validation-errors.jsonl` | The 129 rejected candidates with both validator judgments. |
| `generation.json`, `generator-runtime.json`, `response-schema.json` | Generator identity (model file, revision, SHA-256), sampling settings, llama.cpp runtime, anchor-paper list, output schema. |
| `generation-batches.jsonl` | Every generation prompt and raw output (audit trail). |
| `corpus.json` | Corpus construction: topic queries, 172 accepted papers (URL, SHA-256, topic), 162 rejected candidates with reasons (the pool for missing-evidence questions). |
| `source/` | The frozen 200-paper corpus: `papers/<id>/{metadata.json, sections.jsonl, fiche.md}` and an empty `benchmarks.csv`. Evidence `id`s point into `sections.jsonl`. |
| `source-freeze.json` | Freeze record: fingerprint (verifiable on `source/` with `lib/rag_qwen.fingerprint`), per-document hashes, code hash, git revision. |
| `enriched/`, `enrichment.jsonl`, `enriched-freeze.json` | The enriched copy: automatic notes (`fiche.md`) and 262 benchmark rows written by Claude. Its `sections.jsonl` files are identical to `source/`. |
| `retrieval-<mode>.jsonl` | Per-query retrieval results for the six modes on both copies (280 queries each): ranks of gold evidence, recall@20, reciprocal rank, latency. |
| `report.json` | `bin/pdb synth report` summary. |

Agent and judge results will be added once those stages run.

## Restore into the working directory

```bash
mkdir -p .cache/bench && cp -r benchmark/. .cache/bench/ && rm .cache/bench/README.md
for d in .cache/bench/source/papers/*/; do cp "$d/sections.jsonl" ".cache/bench/enriched/papers/$(basename "$d")/"; done
```

`bin/pdb synth` then resumes from the saved state (retrieval rebuilds its indexes).

## Re-export after new runs

```bash
B=.cache/bench
cp $B/{questions,variants,candidates,validation-errors,generation-batches,enrichment}.jsonl $B/retrieval-*.jsonl \
   $B/{corpus,source-freeze,enriched-freeze,generation,generator-runtime,response-schema,report}.json benchmark/
rsync -a --include='*/' --include='metadata.json' --include='sections.jsonl' --include='fiche.md' --exclude='*' $B/source/papers/ benchmark/source/papers/
rsync -a --include='*/' --include='metadata.json' --include='fiche.md' --exclude='*' $B/enriched/papers/ benchmark/enriched/papers/
cp $B/source/benchmarks.csv benchmark/source/ && cp $B/enriched/benchmarks.csv benchmark/enriched/
```

The corpus contains text extracted from third-party papers: keep this repository private
unless each paper's licence allows redistribution.
