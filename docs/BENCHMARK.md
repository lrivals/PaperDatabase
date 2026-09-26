# Synthetic benchmark

The benchmark lives in `.cache/bench/`, separate from the working paper library.
`bin/pdb synth` acquires and freezes 200 papers, generates source-grounded questions,
validates them without human labels, and runs retrieval and Claude Code workflow ablations.
The expanded collection includes neighboring topics as distractors. Question anchors
are conservatively screened for FPGA, embedded/edge AI, and hardware acceleration;
generic introductions and background passages are excluded.

## Local generator

The tested machine has an RTX 5090 with 32 GB VRAM. The selected model is
[Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B), using
[Unsloth's Q6_K_XL GGUF](https://huggingface.co/unsloth/Qwen3.8-27B-GGUF).
The file is 25.30 GB. It runs with all layers on the GPU and a 16,384-token context.

Larger parameter counts do not establish better question-generation quality. The
shortlist also included [Qwen3.6-35B-A3B](https://huggingface.co/Qwen/Qwen3.6-35B-A3B),
[Gemma 4 31B](https://huggingface.co/google/gemma-4-31B-it),
[GLM-4.7-Flash](https://huggingface.co/zai-org/GLM-4.7-Flash), and
[Nemotron 3.5 Lightning](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16).
Qwen3.8 has the strongest developer-reported scientific-reasoning result among this
shortlist. Those results use different evaluation settings and unquantized models;
they motivate the choice rather than prove a universal ranking or the Q6 model's score.

Pinned model revision: `4ca720788d1e01f1bff70c033e0d0028fd02e502`.
File: `Qwen3.8-27B-UD-Q6_K_XL.gguf`.
SHA-256: `701d8fa9ed214ab21bfc130cd2a7df19ca89bbef7713e2dfb19f3c63696aa917`.
Runtime: [llama.cpp b11191](https://github.com/ggml-org/llama.cpp/releases/tag/b11191),
Ubuntu CUDA 12.8 binaries and their companion CUDA runtime archive.

Download the pinned model with the existing Hugging Face dependency:

```python
from huggingface_hub import hf_hub_download
print(hf_hub_download(
    "unsloth/Qwen3.8-27B-GGUF",
    "Qwen3.8-27B-UD-Q6_K_XL.gguf",
    revision="4ca720788d1e01f1bff70c033e0d0028fd02e502"))
```

Start the downloaded `llama-server` with its CUDA libraries on `LD_LIBRARY_PATH`:

```bash
llama-server -m /path/to/Qwen3.8-27B-UD-Q6_K_XL.gguf \
  -c 16384 -ngl 99 -fa on --reasoning off \
  --host 127.0.0.1 --port 8787 --no-ui
bin/pdb synth generate --limit 200
bin/pdb synth validate --limit 200
```

Generation uses schema-constrained JSON, temperature 0.7, top-p 0.8, top-k 20,
and seeded sampling. Each batch uses one language. The server model identity and
every quotation are checked; malformed or unsupported candidates are discarded.
`PDB_BENCH_LOCAL_URL` can change the localhost endpoint. Two independent validator
sessions check each answerable candidate. The 200 canonical questions were validated
with Codex (`gpt-6-sol`); from 26/09/2026 every model call (validation, enrichment,
variants, agents, judge) uses headless Claude Code (`claude -p`, default model
`claude-opus-5-5`, override with `PDB_BENCH_CLAUDE_MODEL`; binary with `PDB_BENCH_CLAUDE`).
The CLI must be logged in once (`claude`, then `/login`); its credentials file is copied
into each sandboxed agent run. Validation, enrichment, variants and judging run without
tools and return schema-checked JSON. Agents run in bubblewrap with `Bash`, `Read`,
`Grep` and `Glob` only, a read-only corpus and no project files.
Enrichment keeps a benchmark row only if each number occurs in its cited section,
compared as numbers (`41200` matches "41,200"). Only frozen corpus copies are evaluated:
the enriched copy joins retrieval and agent runs once `enrich` has frozen it. Run generation and validation again
to replace rejected candidates until `questions.jsonl` contains 200 accepted cases.
Missing-paper cases use deterministic templates and frozen-corpus membership checks.

## Dataset and evaluation

The canonical quotas are 40 single-passage, 40 numerical, 50 cross-paper,
30 within-paper, 20 table, and 20 missing-evidence questions. Each category is split
40% development / 60% test, with English/French balance in each split. Answerable
development and test questions draw from disjoint paper sets determined by a hash
of the paper ID. Forty canonical questions receive translated and terse variants.

Artifacts include `source-freeze.json`, `generation.json`, `generator-runtime.json`, audited generation
batches, `candidates.jsonl`, validated `questions.jsonl`, and rejection records.
Each accepted question carries exact original-paper locators and quotations.
Automatically generated fiches and numerical transcriptions form a separate
`enriched/` corpus; they are never used to generate reference answers.

```bash
bin/pdb synth corpus --target 200
bin/pdb synth enrich --limit 200
bin/pdb synth variants --limit 40
bin/pdb synth retrieval --mode lexical
bin/pdb synth retrieval --mode dense
bin/pdb synth retrieval --mode hybrid
bin/pdb synth retrieval --mode reranked
bin/pdb synth retrieval --mode cpu-hybrid     # pdb search (bge-small), same questions
bin/pdb synth retrieval --mode cpu-reranked
bin/pdb synth agent --variant native --split development --limit 20
bin/pdb synth agent --variant hybrid --split development --limit 20
bin/pdb synth judge --limit 200
bin/pdb synth report
```

Screen agent variants on development questions before selecting three finalists
for the same 60 held-out questions. Keep generator, agent, and judge models fixed
across comparisons. Report evidence completeness/recall, supported answer accuracy,
citation validity, missing-evidence behavior, latency, context usage, and tool calls.
Synthetic question and LLM-judge biases remain limitations; the results measure this
frozen corpus and task distribution, not all research work.

## Retrieval results (26/09/2026, source corpus, 180 answerable questions)

`bin/pdb synth retrieval --mode …` then `bin/pdb synth report`. Recall@20 is the share of
gold evidence passages found in the top 20 (a hit must be original text from the right
section and contain the evidence quote); MRR uses the first gold hit. Missing-evidence
questions are excluded. Both engines ran on the RTX 5090 (bge-small also uses CUDA when
available, hence its low latency here).

| Mode | Recall@20 | MRR | EN recall | FR recall | Cross-paper recall | Mean latency |
|---|---:|---:|---:|---:|---:|---:|
| Qwen lexical (FTS5) | 0.48 | 0.40 | 0.68 | 0.28 | 0.21 | 0.05 s |
| Qwen dense | 0.67 | 0.57 | 0.70 | 0.63 | 0.42 | 0.82 s |
| Qwen hybrid | 0.67 | 0.55 | 0.71 | 0.63 | 0.39 | 0.85 s |
| **Qwen hybrid + reranker** | **0.77** | **0.73** | **0.80** | **0.74** | **0.49** | 3.39 s |
| bge-small hybrid (`pdb search`) | 0.65 | 0.47 | 0.77 | 0.54 | 0.35 | 0.04 s |
| bge-small + MiniLM rerank | 0.69 | 0.50 | 0.80 | 0.58 | 0.38 | 0.09 s |

Reading:
- The Qwen reranker is the best route on every slice (development and test alike);
  its gain over bge-small is mostly ranking (MRR 0.73 vs 0.50) and French queries
  (0.74 vs 0.58). In English, recall is tied (0.80).
- Cross-paper questions are the weak spot for every engine (≤ 0.49): top-20 search
  rarely returns both papers' passages. Table and numeric questions are near solved.
- The match rule slightly favours bge-small: its hits are checked against the whole
  parent section, Qwen hits only against their own 512-token chunk.
- These are synthetic questions anchored on single passages; agent and judge stages
  measure answer quality.

## Retrieval with enriched notes and query variants (26/09/2026, 23:53)

Same protocol, both frozen corpus copies, 200 canonical questions plus 80 variants
(a translation and a terse rewording of 40 questions, written and checked by Claude).
Cells are recall@20 / MRR over answerable questions.

| Slice | Qwen lexical | Qwen dense | Qwen hybrid | Qwen + reranker | bge-small | bge-small + rerank |
|---|---|---|---|---|---|---|
| source, canonical (180) | 0.46 / 0.40 | 0.67 / 0.57 | 0.67 / 0.55 | **0.77 / 0.73** | 0.65 / 0.47 | 0.69 / 0.50 |
| enriched, canonical (180) | 0.37 / 0.36 | 0.65 / 0.54 | 0.65 / 0.44 | **0.73 / 0.70** | 0.65 / 0.47 | 0.69 / 0.50 |
| source, 40 questions, original | 0.57 / 0.56 | 0.78 / 0.70 | 0.76 / 0.71 | **0.82 / 0.84** | 0.74 / 0.58 | 0.76 / 0.61 |
| same, translated | 0.46 / 0.39 | 0.78 / 0.73 | 0.76 / 0.61 | **0.81 / 0.82** | 0.69 / 0.44 | 0.71 / 0.40 |
| same, terse | 0.65 / 0.54 | 0.76 / 0.68 | 0.78 / 0.73 | **0.82 / 0.82** | 0.75 / 0.51 | 0.74 / 0.58 |

Reading:
- **Automatic notes hurt Qwen retrieval of original evidence** (reranker 0.77 → 0.73,
  hybrid MRR 0.55 → 0.44): notes and benchmark-row records compete with the original
  passages for the top 20 and for the three-results-per-paper cap. bge-small only
  indexes original sections, so its scores are unchanged. Whether notes help *answers*
  is for the agent stage.
- **Translation**: the Qwen reranker loses nothing (0.82 → 0.81); bge-small loses
  recall and most of its ranking (MRR 0.61 → 0.40 with rerank). Terse rewording costs
  neither engine much.
- The ranking of modes on the held-out test split matches the whole set.
