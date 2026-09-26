# Synthetic benchmark

The benchmark lives in `.cache/bench/`, separate from the working paper library.
`bin/pdb synth` acquires and freezes 200 papers, generates source-grounded questions,
validates them without human labels, and runs retrieval and Codex workflow ablations.
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
`PDB_BENCH_LOCAL_URL` can change the localhost endpoint. Two independent Codex
sessions validate each answerable candidate. Run generation and validation again
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
