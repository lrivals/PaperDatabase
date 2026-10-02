---
description: Answer a research question with the GPU (Qwen3) index and open-access acquisition
argument-hint: <research question>
allowed-tools: Read, Write, Grep, Glob, Bash(bin/pdb rag *), Bash(bin/pdb gpu), Bash(bin/pdb reindex)
---

Answer: $ARGUMENTS

**GPU route only** (docs/RAG.md §13). The default route is `/paper-ask` (CPU). First run
`bin/pdb gpu`: if it reports no CUDA GPU or missing torch/transformers, do not use
`bin/pdb rag`; say so in one line and answer with the `/paper-ask` workflow instead
(`.claude/commands/paper-ask.md`). Use this skill only when the user invoked it or asked for
the GPU route or for open-access acquisition. Answer in French, with technical terms in English.

**Sufficiency (same rule as `/paper-ask`, steps 0, 6 and 7).** Before searching, list 2 to 5 requirements: what a complete answer must establish (a value, its platform, a measurement condition, a comparison, a method), taken from the question and no finer. After checking sources, mark each one `couvert` (verified source passage), `partiel` (only a neighbouring passage: other platform, batch, precision, power scope or dataset) or `absent`. Verdict: `suffisant` if all are `couvert`, `absent` if all are `absent`, `partiel` otherwise. Open the answer with the verdict and the requirement list, then **Lu / Déduit / Non trouvé dans la base** (the `absent` requirements and what the `partiel` ones lack). An `absent` verdict means the searched corpus does not cover the topic, not that the literature does not: say so, then offer acquisition (below) or `/paper-discover`.

Follow `CLAUDE.md` and `DATA_MODEL.md`. Use `bin/pdb rag index` when the index is missing or stale. Use `bin/pdb rag search "$ARGUMENTS"`; route questions about a paper's contribution through `--kind abstract` and numerical configurations through `--kind benchmark` plus exhaustive `bin/pdb rag benchmarks --filter-json ...`. Search both English and French formulations when appropriate. Results label original text, benchmark transcription, and curated notes. Treat notes as navigation and interpretation. For a selected benchmark or fiche, search its `paper_id` again with `--kind section` or `--kind table` and read the original source using `bin/pdb rag evidence ID --parent` before reporting the fact.

Draft an answer with evidence IDs. Make one prioritized list of at most three unsupported claims, missing conditions, or gaps in paper coverage. For each information gap, search a self-contained follow-up query. When the local corpus is insufficient, call `bin/pdb rag acquire "QUERY" --run RUN_ID` to discover open-access full texts. Validated papers are only staged: show the user each staged paper (title, year, excerpt) and wait for their answer. Run `bin/pdb rag approve RUN_ID PAPER_ID...` only for the papers they accept, then report the new paper IDs. A staged paper is not in the library and must not be cited. Use at most three acquisition/follow-up rounds and respect the command's shared budget. Unavailable PDFs and failed extraction are limitations, not evidence of absence.

Check every final claim against its exact source passage, including claims in the initial draft. Compare task, metric, dataset, platform, precision, timing and power scope before numerical comparisons. A value marked `n/r` stays unknown; a computed FPS/W must name the source inputs and power scope. Record `snapshot`, `verdict`, `requirements: [{text, status}]`, `claims: [{text, citations: [{id, excerpt}]}]` in a JSON answer record (same fields as the `/paper-ask --record` format) and run `bin/pdb rag check-answer RECORD.json` when writing a research artifact. Each excerpt must occur in its cited passage. The checker verifies source identities/excerpts; assess semantic support yourself. Narrow, qualify, or remove unsupported claims. State when the answer is limited to the searched corpus and newly acquired papers.
