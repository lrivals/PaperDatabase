"""Reproducible synthetic benchmark over an isolated PaperDatabase corpus.

  bin/pdb synth corpus [--target 200]
  bin/pdb synth enrich [--limit N]
  bin/pdb synth generate [--limit N]
  bin/pdb synth validate [--limit N]
  bin/pdb synth retrieval [--mode lexical|dense|hybrid|reranked|cpu-hybrid|cpu-reranked]
  bin/pdb synth agent [--limit N]
  bin/pdb synth report

All large or generated artifacts live under .cache/bench/.
"""

import argparse
import csv
import difflib
import hashlib
import json
import os
import random
import re
import shutil
import subprocess
import tempfile
import time
import urllib.request
from collections import Counter
from pathlib import Path

from lib import evaluation, rag_qwen as rag, rag_external, schema
from bin import ingest, reindex

ROOT = Path(__file__).resolve().parent.parent
HOME = ROOT / ".cache" / "bench"
SOURCE = HOME / "source"
ENRICHED = HOME / "enriched"
LOCAL_MODEL = "Qwen3.8-27B-UD-Q6_K_XL.gguf"
LOCAL_MODEL_REPO = "unsloth/Qwen3.8-27B-GGUF"
LOCAL_MODEL_REVISION = "4ca720788d1e01f1bff70c033e0d0028fd02e502"
LOCAL_MODEL_SHA256 = "701d8fa9ed214ab21bfc130cd2a7df19ca89bbef7713e2dfb19f3c63696aa917"
LOCAL_URL = os.environ.get("PDB_BENCH_LOCAL_URL", "http://127.0.0.1:8787/v1/chat/completions")
GENERATION_MAX_TOKENS = 6000
# Validator, enricher, judge and agent under test: headless Claude Code (`claude -p`).
CLAUDE = os.environ.get("PDB_BENCH_CLAUDE") or shutil.which("claude") or "claude"
CLAUDE_MODEL = os.environ.get("PDB_BENCH_CLAUDE_MODEL", "claude-opus-5-5")
QUOTAS = {
    "single": 40, "numeric": 40, "cross": 50,
    "within": 30, "table": 20, "missing": 20,
}
CATEGORY_INSTRUCTIONS = {
    "single": "Ask about this paper's specific method, finding, or limitation.",
    "numeric": "Ask for a reported experimental metric with its units and configuration. "
               "Do not ask about a publication year, a reference number, or a generic definition.",
    "cross": "Compare or synthesize the two named papers. Both passages must be essential "
             "to the answer. Do not rank measurements made under different conditions.",
    "within": "Connect findings from both sections of this paper. Both passages must be "
              "essential to the answer.",
    "table": "Ask about a table result and identify its configuration and measurement scope.",
}
TOPICS = {
    "yolo-fpga": ("FPGA YOLO object detection accelerator", 45),
    "autoencoder-fpga": ("FPGA autoencoder anomaly detection", 35),
    "continual-learning": ("embedded continual learning hardware accelerator", 35),
    "toolflows": ("FINN hls4ml Vitis AI FPGA toolflow", 35),
    "platforms": ("Zynq Kria Versal edge AI accelerator", 30),
    "surveys": ("FPGA edge artificial intelligence accelerator survey", 20),
}
EXTRA_QUERIES = {
    "yolo-fpga": ("YOLO FPGA", "YOLO Zynq", "YOLO hardware accelerator"),
    "toolflows": ("FINN FPGA", "hls4ml FPGA", "Vitis AI FPGA", "FPGA neural network toolflow"),
    "platforms": ("Zynq neural accelerator", "Kria edge AI", "Versal AI accelerator",
                  "PYNQ deep learning", "Jetson FPGA comparison"),
}


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
    os.replace(temp, path)


def read(path, default):
    return json.loads(path.read_text()) if path.exists() else default


def append(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as f:
        f.write(json.dumps(value, ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())


def lines(path):
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def sources(root):
    return sorted((root / "papers").glob("*/metadata.json"))


def sections(folder):
    return [json.loads(line) for line in (folder / "sections.jsonl").read_text().splitlines()
            if line.strip()]


def prepare():
    if SOURCE.exists():
        return
    (SOURCE / "papers").mkdir(parents=True)
    for path in sources(ROOT):
        target = SOURCE / "papers" / path.parent.name
        target.mkdir()
        meta = json.loads(path.read_text())
        meta["status"]["fiche"] = "todo"
        for name in ("sections.jsonl", "fulltext.md", "refs.jsonl"):
            shutil.copy2(path.parent / name, target / name)
        save(target / "metadata.json", meta)
        (target / "fiche.md").write_text(schema.render_fiche(meta))
    with (SOURCE / "benchmarks.csv").open("w", newline="") as f:
        csv.writer(f).writerow(schema.BENCHMARK_COLUMNS)
    if reindex.run(SOURCE):
        raise RuntimeError("initial benchmark source corpus is invalid")
    rag.build(SOURCE, mode="lexical")
    save(HOME / "corpus.json", {"target": 200, "accepted": [], "rejected": [],
                               "attempts": 0, "bytes": 0, "queries": TOPICS,
                               "seed_papers": [p.parent.name for p in sources(SOURCE)]})


def frozen(root):
    record = read(HOME / f"{root.name}-freeze.json", None)
    if record is None:
        raise RuntimeError(f"{root.name} benchmark corpus has not been frozen")
    if rag.fingerprint(root) != record["fingerprint"]:
        raise RuntimeError(f"{root.name} benchmark corpus changed after freeze")
    return record


def corpora():
    """Frozen corpus copies to evaluate; the enriched copy is frozen once complete."""
    return [(label, root) for label, root in (("source", SOURCE), ("enriched", ENRICHED))
            if (HOME / f"{root.name}-freeze.json").exists() and frozen(root)]


def freeze(root):
    documents = {}
    for path in sources(root):
        folder = path.parent
        documents[folder.name] = {
            name: hashlib.sha256((folder / name).read_bytes()).hexdigest()
            if (folder / name).exists() else None
            for name in ("metadata.json", "sections.jsonl", "paper.pdf")}
    code_hash = hashlib.sha256(
        b"".join((ROOT / p).read_bytes() for p in
                 ("bin/bench_cli.py", "lib/rag_qwen.py", "lib/rag_external.py",
                  "bin/ingest.py", "bin/reindex.py"))).hexdigest()
    record = {"fingerprint": rag.fingerprint(root),
              "papers": len(sources(root)), "created": time.time(),
              "model": CLAUDE_MODEL,
              "code_hash": code_hash, "documents": documents,
              "git_revision": subprocess.check_output(
                  ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()}
    save(HOME / f"{root.name}-freeze.json", record)
    return record


def identity(candidate):
    return (candidate.get("arxiv_id") or candidate.get("doi") or
            candidate.get("title") or "").casefold().strip()


def topic(candidate):
    words = " ".join(str(candidate.get(k) or "") for k in ("title", "abstract"))
    axes, _ = ingest.classify(words, candidate.get("title") or "")
    return next((a for a in TOPICS if a in axes), None)


def topics(candidate):
    words = " ".join(str(candidate.get(k) or "") for k in ("title", "abstract"))
    axes, _ = ingest.classify(words, candidate.get("title") or "")
    return set(axes)


def corpus(target=200):
    prepare()
    state_path = HOME / "corpus.json"
    state = read(state_path, {})
    if target != state["target"]:
        state["target"] = target
    existing = {identity(json.loads(p.read_text())) for p in sources(SOURCE)}
    tried = {r["identity"] for r in state["accepted"] + state["rejected"]}
    count = Counter()
    for paper_id in state["seed_papers"]:
        p = SOURCE / "papers" / paper_id / "metadata.json"
        if p.exists():
            axes = json.loads(p.read_text()).get("axes", [])
            key = next((a for a in TOPICS if a in axes), None)
            if key:
                count[key] += 1
    count.update(r["topic"] for r in state["accepted"])
    existing_titles = {
        re.sub(r"\W+", "", (json.loads(p.read_text()).get("title") or "").casefold())
        for p in sources(SOURCE)}
    known_hashes = {hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in (SOURCE / "papers").glob("*/paper.pdf")}
    if len(existing) >= target:
        if target == 200 and not (HOME / "source-freeze.json").exists():
            freeze(SOURCE)
        return {"papers": len(existing), "target": target, "complete": True}
    candidates = []
    for axis, (query, _) in TOPICS.items():
        if count[axis] >= TOPICS[axis][1]:
            continue
        for phrase in (query, *EXTRA_QUERIES.get(axis, ())):
            try:
                found = rag_external._arxiv_candidates(phrase, limit=150)
                for item in found:
                    item["requested_topic"] = axis
                    item["pdf_urls"] = [item["pdf_url"]]
                candidates += found
            except Exception as e:
                append(HOME / "corpus-errors.jsonl", {"query": phrase, "provider": "arxiv",
                                                       "error": str(e)})
            try:
                found = rag_external._openalex_candidates(
                    phrase, HOME / "openalex-cache", limit=150)
                for item in found:
                    item["requested_topic"] = axis
                candidates += found
            except Exception as e:
                append(HOME / "corpus-errors.jsonl", {"query": phrase, "error": str(e)})
    # Higher-ranked OpenAlex results are consumed first, while topic caps protect balance.
    seen = set(existing) | tried
    for c in candidates:
        if len(existing) >= target or state["attempts"] >= 600 or state["bytes"] >= 5_000_000_000:
            break
        key = identity(c)
        if not key or key in seen:
            continue
        seen.add(key)
        title_key = re.sub(r"\W+", "", (c.get("title") or "").casefold())
        if title_key and title_key in existing_titles:
            continue
        requested = c["requested_topic"]
        if requested not in topics(c) or count[requested] >= TOPICS[requested][1]:
            continue
        folder = HOME / "staging" / hashlib.sha256(key.encode()).hexdigest()[:16]
        folder.mkdir(parents=True, exist_ok=True)
        pdf = folder / "source.pdf"
        reason = None
        for url in c.get("pdf_urls", [])[:3]:
            if state["attempts"] >= 600 or state["bytes"] >= 5_000_000_000:
                break
            state["attempts"] += 1
            try:
                size, resolved = rag_external._download(url, pdf, 0)
                state["bytes"] += size
                c["retrieved_url"] = resolved
                break
            except Exception as e:
                state["bytes"] += pdf.stat().st_size if pdf.exists() else 0
                pdf.unlink(missing_ok=True)
                reason = f"{type(e).__name__}: {e}"
        if pdf.exists():
            try:
                pdf_hash = hashlib.sha256(pdf.read_bytes()).hexdigest()
                if pdf_hash in known_hashes:
                    raise ValueError("PDF already in isolated benchmark corpus")
                stage = folder / "papers"
                stage.mkdir(exist_ok=True)
                status, detail = ingest.process(pdf, papers_dir=stage, source_meta=c,
                                                citation_dirs=(folder,), use_grobid=False)
                if status != "ingéré":
                    raise ValueError(detail)
                paper = next(stage.iterdir())
                meta = json.loads((paper / "metadata.json").read_text())
                problems, notes = [], []
                reindex.check_paper_files(paper, meta, problems, notes)
                if problems or sum(len(r["text"]) for r in sections(paper)) < 2000:
                    raise ValueError("; ".join(problems) or "too little extracted text")
                if requested not in set(meta.get("axes", [])):
                    raise ValueError("parsed paper is outside requested topic")
                if (SOURCE / "papers" / paper.name).exists():
                    raise ValueError("paper ID collision")
                meta["status"]["fiche"] = "todo"
                save(paper / "metadata.json", meta)
                (paper / "fiche.md").write_text(schema.render_fiche(meta))
                shutil.move(str(paper), SOURCE / "papers" / paper.name)
                existing.add(key)
                existing_titles.add(title_key)
                known_hashes.add(pdf_hash)
                count[requested] += 1
                state["accepted"].append({"identity": key, "paper_id": paper.name,
                                          "topic": requested, "url": c["retrieved_url"],
                                          "sha256": pdf_hash})
            except Exception as e:
                reason = f"{type(e).__name__}: {e}"
        if reason:
            state["rejected"].append({"identity": key, "title": c.get("title"),
                                      "topic": requested, "reason": reason})
        save(state_path, state)
    if reindex.run(SOURCE):
        raise RuntimeError("expanded benchmark corpus failed validation")
    rag.build(SOURCE, mode="lexical")
    if len(existing) >= target and target == 200:
        freeze(SOURCE)
    return {"papers": len(existing), "target": target, "complete": len(existing) >= target,
            "attempts": state["attempts"], "bytes": state["bytes"],
            "topics": dict(count)}


def output_schema(expected):
    props = {}
    evidence_item = {
        "type": "object", "additionalProperties": False,
        "properties": {name: {"type": "string"} for name in ("paper_id", "id", "quote")},
        "required": ["paper_id", "id", "quote"]}
    for key, kind in expected.items():
        if kind != "array":
            props[key] = {"type": kind}
        elif key == "evidence":
            props[key] = {"type": "array", "items": evidence_item}
        elif key == "cases":
            props[key] = {"type": "array", "items": {
                "type": "object", "additionalProperties": False,
                "properties": {"slot": {"type": "string"}, "question": {"type": "string"},
                               "answer": {"type": "string"},
                               "evidence": {"type": "array", "items": evidence_item},
                               "forbidden": {"type": "array", "items": {"type": "string"}}},
                "required": ["slot", "question", "answer", "evidence", "forbidden"]}}
        elif key == "judgments":
            props[key] = {"type": "array", "items": {
                "type": "object", "additionalProperties": False,
                "properties": {"id": {"type": "string"}, "valid": {"type": "boolean"},
                               "answer": {"type": "string"}, "reason": {"type": "string"}},
                "required": ["id", "valid", "answer", "reason"]}}
        elif key == "rows":
            props[key] = {"type": "array", "items": {
                "type": "object", "additionalProperties": False,
                "properties": {name: {"type": "string"} for name in schema.BENCHMARK_COLUMNS},
                "required": list(schema.BENCHMARK_COLUMNS)}}
        else:
            props[key] = {"type": "array", "items": {"type": "string"}}
    return {"type": "object", "additionalProperties": False,
            "properties": props, "required": list(expected)}


def claude_result(stdout):
    """Structured answer and usage from `claude -p --output-format json|stream-json`."""
    events = [json.loads(line) for line in stdout.splitlines() if line.startswith("{")]
    final = next((e for e in reversed(events) if e.get("type") == "result"), None)
    if final is None or final.get("is_error"):
        raise RuntimeError((final or {}).get("result") or stdout[-1200:])
    data = final.get("structured_output")
    if data is None:
        data = json.loads(final["result"])
    return data, final.get("usage", {}), events


def claude(prompt, expected, timeout=480):
    """One tool-less Claude session answering with JSON that matches `expected`."""
    command = [CLAUDE, "-p", "--output-format", "json", "--model", CLAUDE_MODEL,
               "--json-schema", json.dumps(output_schema(expected)),
               "--tools", "", "--no-session-persistence", "--setting-sources", "",
               "--strict-mcp-config"]
    with tempfile.TemporaryDirectory(prefix="pdb-bench-") as d:
        result = subprocess.run(command, input=prompt, text=True, capture_output=True,
                                timeout=timeout, cwd=d)
    data, _, _ = claude_result(result.stdout or result.stderr)
    if set(data) != set(expected):
        raise ValueError("Claude output schema mismatch")
    return data


def local_generate(prompt, seed, count):
    shape = output_schema({"cases": "array"})
    shape["properties"]["cases"].update({"minItems": count, "maxItems": count})
    shape["properties"]["cases"]["items"]["properties"]["slot"]["enum"] = [
        str(i) for i in range(count)]
    body = {"model": LOCAL_MODEL,
            "messages": [{"role": "system", "content":
                          "Return only JSON grounded in the supplied original-paper passages. "
                          "Copy evidence quotations exactly, without paraphrasing."},
                         {"role": "user", "content": prompt}],
            "response_format": {"type": "json_schema", "json_schema": {
                "name": "cases", "strict": True, "schema": shape}},
            "temperature": 0.7, "top_p": 0.8, "top_k": 20,
            "max_tokens": GENERATION_MAX_TOKENS, "seed": seed, "stream": False}
    request = urllib.request.Request(LOCAL_URL, data=json.dumps(body).encode(),
                                     headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=480) as response:
        result = json.load(response)
    if Path(result.get("model", "")).name != LOCAL_MODEL:
        raise RuntimeError("local server is not running the frozen generation model")
    data = json.loads(result["choices"][0]["message"]["content"])
    if set(data) != {"cases"} or not isinstance(data["cases"], list):
        raise ValueError("local generation output schema mismatch")
    return data["cases"], result.get("usage", {})


def paper_rows():
    out = []
    for p in sources(SOURCE):
        meta = json.loads(p.read_text())
        # ponytail: title screening is intentionally conservative; curate paper IDs if recall matters.
        if not re.search(r"\b(?:FPGAs?|embedded|edge|accelerat\w*|hardware|on.device|"
                         r"tinyML|microcontroller|Zynq|PYNQ|Kria|Versal|FINN|hls4ml|"
                         r"reconfigurab\w*|resource.constrain\w*)\b", meta["title"], re.I):
            continue
        rows = [r for r in sections(p.parent)
                if r["kind"] in ("abstract", "section", "table")
                and not (r["kind"] == "section" and re.search(
                    r"introduction|related work|background|fundamentals|prior work|préambule",
                    r["section"], re.I))
                and 250 <= len(r["text"]) <= 12000]
        if rows:
            out.append((meta, rows))
    return out


def packet(category, rng, papers):
    first = rng.choice(papers)
    a = first[0]
    if category == "table":
        eligible = [(m, [r for r in rows if r["kind"] == "table"]) for m, rows in papers]
        eligible = [(m, rows) for m, rows in eligible if rows]
        if not eligible:
            return None
        a, rows = rng.choice(eligible)
        chosen = [rng.choice(rows)]
    elif category == "numeric":
        eligible = [(m, [r for r in rows if re.search(
            r"\d+(?:\.\d+)?\s*(?:%|fps\b|MHz\b|GHz\b|ms\b|ns\b|mW\b|W\b|GOPS\b|TOPS\b)"
            r"|\b(?:latency|throughput|accuracy|mAP|LUTs?|DSPs?|BRAM|power|energy)\b.{0,80}\d",
            r["text"], re.I)])
                    for m, rows in papers]
        a, rows = rng.choice([pair for pair in eligible if pair[1]])
        chosen = [rng.choice(rows)]
    elif category == "cross":
        compatible = [(m, rows) for m, rows in papers
                      if m["id"] != a["id"] and set(m.get("axes", [])) & set(a.get("axes", []))]
        if not compatible:
            return None
        b = rng.choice(compatible)
        chosen = [rng.choice(first[1]), rng.choice(b[1])]
    elif category == "within":
        if len(first[1]) < 2:
            return None
        chosen = rng.sample(first[1], 2)
    else:
        chosen = [rng.choice(first[1])]
    by_id = {m["id"]: m for m, _ in papers}
    result = []
    for row in chosen:
        meta = by_id[row["paper_id"]]
        result.append({"paper_id": row["paper_id"], "title": meta["title"],
                       "id": row["id"], "section": row["section"],
                       "kind": row["kind"], "text": row["text"][:6500]})
    return result


def generation_group(active, category):
    cases = [c for c in active if c["category"] == category]
    targets = {"development": round(QUOTAS[category] * .4)}
    targets["test"] = QUOTAS[category] - targets["development"]
    split_counts = Counter(c["split"] for c in cases)
    split = next(s for s in targets if split_counts[s] < targets[s])
    language_counts = Counter(c["language"] for c in cases if c["split"] == split)
    language = min(("en", "fr"), key=lambda lang: language_counts[lang])
    # Two-source packets need more input and output space; keep them within context.
    batch_size = 3 if category in ("cross", "within") else 6
    return split, language, min(batch_size, targets[split] // 2 - language_counts[language])


def absent_candidates():
    metadata = [json.loads(p.read_text()) for p in sources(SOURCE)]
    identifiers = {str(m[k]).casefold().strip() for m in metadata
                   for k in ("arxiv_id", "doi") if m.get(k)}
    normalize = lambda title: re.sub(r"\W+", "", title.casefold())
    titles = [normalize(m["title"]) for m in metadata]
    out = []
    for row in read(HOME / "corpus.json", {})["rejected"]:
        title = row.get("title") or ""
        candidate = normalize(title)
        if len(title) < 30 or row["identity"] in identifiers:
            continue
        if any(candidate.startswith(t) or t.startswith(candidate) or
               difflib.SequenceMatcher(None, candidate, t).ratio() >= .85 for t in titles):
            continue
        out.append(row)
    return out


def generate(limit=200):
    frozen(SOURCE)
    if len(sources(SOURCE)) < 200:
        raise RuntimeError("freeze 200 papers before generating benchmark questions")
    path = HOME / "candidates.jsonl"
    current = lines(path)
    if any(x.get("generator") not in (LOCAL_MODEL, "deterministic missing-corpus template")
           for x in current):
        raise RuntimeError("archive earlier non-local candidates before local generation")
    papers = paper_rows()
    save(HOME / "generation.json", {
        "provider": "local GPU", "model": LOCAL_MODEL,
        "repo": LOCAL_MODEL_REPO, "revision": LOCAL_MODEL_REVISION,
        "gguf_sha256": LOCAL_MODEL_SHA256, "source_fingerprint": frozen(SOURCE)["fingerprint"],
        "server": LOCAL_URL, "seed": 73021,
        "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "eligible_anchor_papers": sorted(m["id"] for m, _ in papers),
        "sampling": {"temperature": 0.7, "top_p": 0.8, "top_k": 20,
                     "max_tokens": GENERATION_MAX_TOKENS, "reasoning": False}})
    invalid = {r["id"] for r in lines(HOME / "validation-errors.jsonl")}
    active = [x for x in current if x["id"] not in invalid]
    counts = Counter(x["category"] for x in active)
    rng = random.Random(73021 + len(current))
    attempts = 0
    absent = None
    while len(active) < min(limit, 200) and attempts < 600:
        attempts += 1
        invalid = {r["id"] for r in lines(HOME / "validation-errors.jsonl")}
        active = [x for x in current if x["id"] not in invalid]
        counts = Counter(x["category"] for x in active)
        if len(active) >= min(limit, 200):
            break
        category = next((k for k, n in QUOTAS.items() if counts[k] < n), None)
        if not category:
            break
        split, language, remaining = generation_group(active, category)
        if category == "missing":
            if absent is None:
                absent = absent_candidates()
            if not absent:
                raise RuntimeError("no rejected real-paper candidates for missing-evidence questions")
            choice = absent[counts[category] % len(absent)]
            case = {"category": category, "question": f"Within this frozen paper corpus, "
                    f"what experimental result does {choice['title']} report?"
                    if language == "en" else
                    f"Dans ce corpus figé, quel résultat expérimental rapporte l'article "
                    f"« {choice['title']} » ?",
                    "answer": "This paper is absent from the frozen corpus; its result is not available here."
                    if language == "en" else
                    "Cet article est absent du corpus figé ; son résultat n'est pas disponible ici.",
                    "evidence": [], "forbidden": ["A numeric result unsupported by this corpus"],
                    "language": language, "source_papers": [],
                    "absent_identity": choice["identity"], "absent_title": choice["title"]}
        else:
            eligible = [(m, rows) for m, rows in papers
                        if ("development" if int(hashlib.sha256(m["id"].encode()).hexdigest(), 16) % 5 < 2
                            else "test") == split]
            remaining = min(remaining, QUOTAS[category] - counts[category],
                            limit - len(active), 200 - len(active))
            batch = []
            for offset in range(remaining):
                evidence = packet(category, rng, eligible)
                if evidence:
                    batch.append({"slot": str(offset), "language":
                                  language,
                                  "evidence": evidence})
            if not batch:
                continue
            prompt = ("For EACH numbered packet, write one realistic, self-contained scientific "
                      "research question and a concise answer using only that packet. "
                      "Ask about the paper's own method, result, or limitation, never a generic "
                      "definition or background fact. "
                      "Category: " + category + ". " + CATEGORY_INSTRUCTIONS[category] +
                      " Write ALL questions and answers in " +
                      ("French" if language == "fr" else "English") + ". Return a cases array "
                      "with one item per slot, each containing slot, question, answer, evidence "
                      "(paper_id, id, verbatim quote), and forbidden unsupported conclusions. "
                      "Use short evidence quotes: one or two complete sentences per passage. "
                      "Never mix sources between slots. For numeric or cross-paper claims preserve "
                      "experimental conditions and avoid unjustified comparisons. Packets:\n" +
                      json.dumps(batch, ensure_ascii=False))
            try:
                generated, usage = local_generate(prompt, 73021 + attempts, len(batch))
                append(HOME / "generation-batches.jsonl", {
                    "attempt": attempts, "category": category,
                    "seed": 73021 + attempts, "prompt": prompt,
                    "requested_slots": [b["slot"] for b in batch],
                    "cases": generated, "usage": usage})
            except Exception as e:
                append(HOME / "generation-errors.jsonl",
                       {"category": category, "error": str(e), "attempt": attempts})
                continue
            by_slot = {b["slot"]: b for b in batch}
            for got in generated:
                packet_ = by_slot.get(str(got["slot"]).strip(" >"))
                if not packet_:
                    continue
                evidence = packet_["evidence"]
                lookup = {r["id"]: r for r in evidence}
                try:
                    if not got["evidence"] or any(
                        e["id"] not in lookup or e["paper_id"] != lookup[e["id"]]["paper_id"]
                        or not e["quote"].strip() or e["quote"] not in lookup[e["id"]]["text"]
                        for e in got["evidence"]):
                        raise ValueError("generated evidence does not match source passages")
                    if category in ("cross", "within") and (
                        len({e["id"] for e in got["evidence"]}) < 2 or
                        (category == "cross" and
                         len({e["paper_id"] for e in got["evidence"]}) < 2)):
                        raise ValueError("multi-source question needs multiple passages")
                    if category == "numeric" and not re.search(r"\d", got["answer"]):
                        raise ValueError("numeric question has no numeric answer")
                    if any(got["question"].casefold() == r["question"].casefold()
                           for r in current):
                        raise ValueError("duplicate question")
                except ValueError as e:
                    append(HOME / "generation-errors.jsonl",
                           {"category": category, "error": str(e), "attempt": attempts})
                    continue
                case = {k: got[k] for k in ("question", "answer", "evidence", "forbidden")}
                case.update({"category": category, "language": packet_["language"],
                             "generator": LOCAL_MODEL, "generation_usage": usage,
                             "source_papers": sorted({r["paper_id"] for r in evidence}),
                             "id": f"q{len(current) + 1:04d}",
                             "split": split})
                append(path, case)
                current.append(case)
                active.append(case)
                counts[category] += 1
            continue
        case["id"] = f"q{len(current) + 1:04d}"
        case["generator"] = "deterministic missing-corpus template"
        case["split"] = split
        append(path, case)
        current.append(case)
        active.append(case)
        counts[category] += 1
    return {"candidates": len(current), "by_category": dict(counts), "attempts": attempts}


def validate(limit=200):
    frozen(SOURCE)
    candidates = lines(HOME / "candidates.jsonl")
    accepted = {r["id"] for r in lines(HOME / "questions.jsonl")}
    rejected = {r["id"] for r in lines(HOME / "validation-errors.jsonl")}
    pending = []
    for case in candidates:
        if len(pending) >= limit:
            break
        if case["id"] in accepted or case["id"] in rejected:
            continue
        pending.append(case)
    absent = {(r["identity"], r["title"]) for r in absent_candidates()} if any(
        c["category"] == "missing" for c in pending) else set()
    for start in range(0, len(pending), 6):
        batch = pending[start:start + 6]
        packets = []
        for case in batch:
            if case["category"] == "missing":
                if (case.get("absent_identity"), case.get("absent_title")) in absent:
                    append(HOME / "questions.jsonl", case)
                else:
                    append(HOME / "validation-errors.jsonl", {
                        "id": case["id"], "reason": "missing-paper identity not verified"})
                continue
            anchor = []
            for e in case["evidence"]:
                folder = SOURCE / "papers" / e["paper_id"]
                row = next((r for r in sections(folder) if r["id"] == e["id"]), None)
                if row is None or not e["quote"].strip() or e["quote"] not in row["text"]:
                    append(HOME / "validation-errors.jsonl",
                           {"id": case["id"], "reason": "source quotation invalid"})
                    break
                anchor.append({"paper_id": e["paper_id"], "id": e["id"],
                               "text": row["text"][:7000]})
            else:
                packets.append({"id": case["id"], "question": case["question"],
                                "language": case["language"], "category": case["category"],
                                "proposed": case["answer"], "passages": anchor})
        if not packets:
            continue
        prompt = ("Independently answer EACH question only from its supplied original-paper "
                  "passages, then judge whether its proposed answer is fully supported. "
                  "Check numbers, units, conditions, and limitations. Do not use outside "
                  "knowledge or mix packets. Reject generic textbook/background questions, "
                  "questions that do not match their declared language or category, and "
                  "cross/within questions answerable from only one supplied passage. "
                  "Return one judgment per id with valid, answer, "
                  "and reason. Packets:\n" + json.dumps(packets, ensure_ascii=False))
        try:
            votes = [claude(prompt, {"judgments": "array"})["judgments"] for _ in range(2)]
            maps = [{r["id"]: r for r in vote} for vote in votes]
            for case in batch:
                if case["id"] not in {r["id"] for r in packets}:
                    continue
                pair = [m.get(case["id"]) for m in maps]
                if all(p and p["valid"] for p in pair):
                    append(HOME / "questions.jsonl", {**case, "validation": pair})
                else:
                    append(HOME / "validation-errors.jsonl",
                           {"id": case["id"], "reason": "validator rejected or omitted",
                            "judgments": pair})
        except Exception as e:
            for case in batch:
                if case["id"] in {r["id"] for r in packets}:
                    append(HOME / "validation-run-errors.jsonl",
                           {"id": case["id"], "reason": str(e)})
    return {"accepted": len(lines(HOME / "questions.jsonl")),
            "rejected": len(lines(HOME / "validation-errors.jsonl"))}


def variants(limit=40):
    frozen(SOURCE)
    cases = lines(HOME / "questions.jsonl")
    if len(cases) != 200:
        raise RuntimeError("validate all 200 canonical questions first")
    selected = sample(cases, "development", 20) + sample(cases, "test", 20)
    existing = {r["id"] for r in lines(HOME / "variants.jsonl")}
    for case in selected[:limit]:
        if case["id"] in existing:
            continue
        prompt = ("Write two alternative phrasings of this exact research question: translated "
                  "into the other language (French or English), and a terse question in the "
                  "original language. Preserve the scope and answer; do not add assumptions. "
                  "Return JSON translated (string), short (string).\n" +
                  json.dumps({"question": case["question"], "language": case["language"],
                              "answer": case["answer"]}, ensure_ascii=False))
        try:
            pair = claude(prompt, {"translated": "string", "short": "string"})
            check = claude("Do both paraphrases ask the same answerable question, with no "
                          "new conditions? Return JSON valid (boolean), reason (string).\n" +
                          json.dumps({"original": case["question"], **pair},
                                     ensure_ascii=False),
                          {"valid": "boolean", "reason": "string"})
            if not check["valid"]:
                raise ValueError(check["reason"])
            append(HOME / "variants.jsonl", {"id": case["id"], **pair})
            existing.add(case["id"])
        except Exception as e:
            append(HOME / "variant-errors.jsonl", {"id": case["id"], "error": str(e)})
    return {"question_groups": len(existing), "variants": 2 * len(existing)}


def enrich(limit=200):
    frozen(SOURCE)
    if not ENRICHED.exists():
        shutil.copytree(SOURCE, ENRICHED,
                        ignore=shutil.ignore_patterns("paper.pdf", "grobid.tei.xml", ".cache"))
    completed = {r["paper_id"] for r in lines(HOME / "enrichment.jsonl")}
    papers = sources(ENRICHED)
    rows_written = []
    for path in papers:
        if path.parent.name in completed:
            continue
        if len(completed) >= limit:
            break
        meta = json.loads(path.read_text())
        available = [r for r in sections(path.parent)
                     if r["kind"] in ("abstract", "section", "table")]
        available.sort(key=lambda r: (
            0 if r["kind"] == "table" else
            1 if re.search(r"result|performance|evaluation|experiment|implementation|"
                           r"resource|latency|power", r["section"], re.I) else
            2 if r["kind"] == "abstract" else 3, r["order"]))
        available = available[:25]
        pack = [{"id": r["id"], "section": r["section"], "text": r["text"][:2500]}
                for r in available]
        prompt = ("Create a concise critical reading note and up to two experimental benchmark "
                  "rows from these original-paper passages only. If a supplied passage reports "
                  "a measured hardware result, include at least one row. Copy numerical values "
                  "as bare numbers (for example 98.9 rather than 98.9%), without converting "
                  "units; otherwise write n/r. "
                  "Use an exact supplied section heading for source_section; set confidence to "
                  "high, medium, or low. Set power_scope to n/r when power_w is n/r. "
                  "Return JSON note (string) and rows (array of objects with keys "
                  "from the PaperDatabase benchmark schema). Each row must include a source_section "
                  "matching a supplied section. Schema columns: " +
                  ", ".join(schema.BENCHMARK_COLUMNS) + ". Paper: " +
                  json.dumps({"metadata": meta, "passages": pack}, ensure_ascii=False))
        try:
            got = claude(prompt, {"note": "string", "rows": "array"})
            valid = []
            rejected_rows = []
            section_names = {r["section"] for r in available}
            for row in got["rows"][:2]:
                row = {k: str(row.get(k, schema.NR) or schema.NR) for k in schema.BENCHMARK_COLUMNS}
                row["paper_id"] = meta["id"]
                for key in schema.NUMERIC_COLUMNS:
                    row[key] = re.sub(r"\s*(?:%|fps|gops|ms|w|luts?|dsps?|brams?)$", "",
                                      row[key], flags=re.I)
                source_text = " ".join(r["text"] for r in available
                                       if r["section"] == row["source_section"])
                found = evaluation.numbers(source_text)
                numbers_present = all(row[k] == schema.NR or evaluation.value_in(row[k], found)
                                      for k in schema.NUMERIC_COLUMNS)
                problems = schema.validate_benchmark_row(row)
                if row["source_section"] not in section_names:
                    problems.append("source section not supplied")
                if not numbers_present:
                    problems.append("numerical value missing from source section")
                if not problems:
                    valid.append(row)
                else:
                    rejected_rows.append({"row": row, "problems": problems})
            meta["status"]["fiche"] = "done"
            note = schema.render_fiche(meta).replace("fiche: todo", "fiche: done", 1)
            (path.parent / "fiche.md").write_text(note + "\n## Lecture automatique\n\n" +
                                                    got["note"] + "\n")
            save(path, meta)
            rows_written += valid
            append(HOME / "enrichment.jsonl", {"paper_id": meta["id"], "rows": valid,
                                                "rejected_rows": rejected_rows,
                                                "note": got["note"]})
            completed.add(meta["id"])
        except Exception as e:
            append(HOME / "enrichment-errors.jsonl", {"paper_id": meta["id"],
                                                       "error": str(e)})
    with (ENRICHED / "benchmarks.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=schema.BENCHMARK_COLUMNS)
        writer.writeheader()
        for item in lines(HOME / "enrichment.jsonl"):
            writer.writerows(item["rows"])
    if reindex.run(ENRICHED):
        raise RuntimeError("enriched benchmark corpus failed validation")
    rag.build(ENRICHED, mode="lexical")
    if len(completed) == len(sources(SOURCE)):
        freeze(ENRICHED)
    return {"enriched_papers": len(completed),
            "benchmark_rows": sum(len(r["rows"]) for r in lines(HOME / "enrichment.jsonl"))}


def retrieved_match(result, evidence):
    return (result["paper_id"] == evidence["paper_id"]
            and result["kind"] in ("abstract", "section", "table", "figure")
            and result["locator"] == evidence["id"]
            and (evidence["quote"] in result["text"] or
                 evidence["quote"] in result.get("parent_text", "")))


# "cpu-*": main's bge-small search (lib/rag.py, pdb search) on the same questions.
RETRIEVAL_MODES = ("lexical", "dense", "hybrid", "reranked", "cpu-hybrid", "cpu-reranked")


def cpu_search(index, query, reranking, parents):
    """pdb search hits, shaped like rag_qwen results for retrieved_match."""
    return [{"paper_id": h["paper_id"], "kind": h["kind"], "locator": h["section_id"],
             "text": h["text"], "parent_text": parents[h["section_id"]]}
            for h in index.search(query, k=20, mode="hybrid", rerank=reranking)]


def retrieval(mode):
    frozen(SOURCE)
    if mode not in RETRIEVAL_MODES:
        raise ValueError("invalid retrieval mode")
    cases = lines(HOME / "questions.jsonl")
    if not cases:
        raise RuntimeError("no validated benchmark questions")
    output = []
    query_cases = [(case, "canonical", case["question"]) for case in cases]
    by_id = {case["id"]: case for case in cases}
    for row in lines(HOME / "variants.jsonl"):
        if row["id"] in by_id:
            query_cases += [(by_id[row["id"]], label, row[label])
                            for label in ("translated", "short")]
    for label, root in corpora():
        if mode.startswith("cpu-"):
            from lib import rag as rag_cpu
            rag_cpu.build_index(root)
            index = rag_cpu.Index(root, rerank=mode == "cpu-reranked")
            parents = {r["id"]: r["text"] for m in sources(root) for r in sections(m.parent)}
        else:
            rag.build(root, mode="lexical" if mode == "lexical" else "hybrid")
        for case, variant, query in query_cases:
            started = time.monotonic()
            if mode.startswith("cpu-"):
                hits = cpu_search(index, query, mode == "cpu-reranked", parents)
            else:
                route = "hybrid" if mode == "reranked" else mode
                hits = rag.search(root, query, mode=route, limit=20,
                                  reranking=mode == "reranked")["results"]
            elapsed = time.monotonic() - started
            needed = case["evidence"]
            matched = []
            for item in needed:
                matched.append(next((rank for rank, hit in enumerate(hits, 1)
                                     if retrieved_match(hit, item)), None))
            output.append({"id": case["id"], "corpus": label, "mode": mode,
                           "query_variant": variant,
                           "category": case["category"], "split": case["split"],
                           "recall20": sum(x is not None for x in matched) / len(needed)
                           if needed else None,
                           "complete20": all(x is not None for x in matched)
                           if needed else None,
                           "reciprocal_rank": 1 / min(x for x in matched if x is not None)
                           if any(x is not None for x in matched) else 0,
                           "latency_s": elapsed, "ranks": matched,
                           "returned_tokens": sum(len(h["text"].split()) for h in hits)})
    path = HOME / f"retrieval-{mode}.jsonl"
    path.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in output))
    return {"cases": len(output), "path": str(path)}


def sample(cases, split, limit):
    cases = [c for c in cases if c["split"] == split]
    groups = {name: [c for c in cases if c["category"] == name] for name in QUOTAS}
    picked = []
    while len(picked) < limit and any(groups.values()):
        for name in QUOTAS:
            if groups[name] and len(picked) < limit:
                picked.append(groups[name].pop(0))
    return picked


def answer_schema():
    return {"type": "object", "additionalProperties": False,
            "properties": {
                "answer": {"type": "string"},
                "citations": {"type": "array", "items": {
                    "type": "object", "additionalProperties": False,
                    "properties": {k: {"type": "string"} for k in
                                   ("paper_id", "id", "quote")},
                    "required": ["paper_id", "id", "quote"]}}},
            "required": ["answer", "citations"]}


def agent_variant(case, corpus_name, variant):
    root = SOURCE if corpus_name == "source" else ENRICHED
    if variant not in ("native", "lexical", "dense", "hybrid", "reranked",
                       "structured", "feedback", "oracle"):
        raise ValueError("unknown agent variant")
    if not root.exists():
        raise ValueError("corpus version missing")
    key = f"{case['id']}-{corpus_name}-{variant}"
    output = HOME / "agent" / key
    if (output / "result.json").exists():
        return read(output / "result.json", {})
    output.mkdir(parents=True, exist_ok=True)
    # Claude Code sees a private config dir holding only a copy of the CLI login.
    auth = Path(os.environ.get("CLAUDE_CONFIG_DIR", Path.home() / ".claude")) / ".credentials.json"
    claude_home = output / "claude_home"
    claude_home.mkdir(exist_ok=True)
    if auth.exists():
        shutil.copy2(auth, claude_home / ".credentials.json")
        (claude_home / ".credentials.json").chmod(0o600)
    protocol = {
        "native": "Use rg and read original files under /tmp/bench/papers. Do not call RAG commands.",
        "lexical": "Search with /tmp/project/bin/pdb rag search QUERY --mode lexical. Read selected original passages with rag evidence ID --parent.",
        "dense": "Search with /tmp/project/bin/pdb rag search QUERY --mode dense --no-rerank. Read selected original passages with rag evidence ID --parent.",
        "hybrid": "Search with /tmp/project/bin/pdb rag search QUERY --mode hybrid --no-rerank. Read selected original passages with rag evidence ID --parent.",
        "reranked": "Search with /tmp/project/bin/pdb rag search QUERY --mode hybrid. Read selected original passages with rag evidence ID --parent.",
        "structured": "Use lexical RAG search and, for numbers, /tmp/project/bin/pdb rag benchmarks --filter-json FILTERS. Verify benchmark rows in original sections.",
        "feedback": "Use hybrid RAG search, draft an answer, identify up to three evidence gaps, search those gaps, then revise and verify original passages.",
        "oracle": "Answer only from the supplied evidence. Do not call tools.",
    }[variant]
    oracle = []
    if variant == "oracle":
        for e in case["evidence"]:
            row = next(r for r in sections(root / "papers" / e["paper_id"])
                       if r["id"] == e["id"])
            oracle.append({"paper_id": e["paper_id"], "id": e["id"],
                           "text": row["text"][:7000]})
    prompt = ("Answer this scientific question using only this frozen paper corpus. "
              "Keep original-paper evidence distinct from notes and numeric transcriptions. "
              "For comparisons, check task, metric, dataset, platform, precision, and power scope. "
              "If the corpus does not support an answer, say so. No web or acquisition. "
              "Return JSON matching the given schema, with citations quoting original sections. "
              + protocol + "\nQuestion: " + case["question"] +
              ("\nEvidence: " + json.dumps(oracle, ensure_ascii=False) if oracle else ""))
    project = ROOT
    cmd = ["bwrap", "--ro-bind", "/", "/", "--tmpfs", str(ROOT),
           "--tmpfs", "/tmp", "--dir", "/tmp/bench", "--dir", "/tmp/project",
           "--dir", "/tmp/output", "--dev", "/dev", "--proc", "/proc",
           "--ro-bind", str(root), "/tmp/bench",
           "--ro-bind", str(project / "bin"), "/tmp/project/bin",
           "--ro-bind", str(project / "lib"), "/tmp/project/lib",
           "--ro-bind", str(project / ".venv"), "/tmp/project/.venv",
           "--bind", str(output), "/tmp/output",
           "--chdir", "/tmp/bench", "--setenv", "PDB_RAG_ROOT", "/tmp/bench",
           "--setenv", "CLAUDE_CONFIG_DIR", "/tmp/output/claude_home",
           "--setenv", "HOME", "/tmp/output/claude_home",
           "--", CLAUDE, "-p", "--model", CLAUDE_MODEL,
           "--output-format", "stream-json", "--verbose",
           "--json-schema", json.dumps(answer_schema()),
           "--tools", "Bash,Read,Grep,Glob", "--permission-mode", "bypassPermissions",
           "--no-session-persistence", "--setting-sources", "", "--strict-mcp-config"]
    started = time.monotonic()
    try:
        result = subprocess.run(cmd, input=prompt, text=True, capture_output=True,
                                timeout=480)
        (output / "events.jsonl").write_text(result.stdout)
        (output / "stderr.txt").write_text(result.stderr[-5000:])
        try:
            answer, usage, events = claude_result(result.stdout)
            save(output / "answer.json", answer)
        except (RuntimeError, ValueError, KeyError) as e:
            answer, usage, events = None, {}, []
            result.stderr += f"\n{e}"
        calls = [block for e in events if e.get("type") == "assistant"
                 for block in e.get("message", {}).get("content", [])
                 if block.get("type") == "tool_use"]
        commands = [c["input"].get("command", "") for c in calls if c["name"] == "Bash"]
        violations = [c for c in commands if re.search(
            r"\b(?:curl|wget|rag acquire|requests\.get|urllib\.request)\b", c)]
        if variant == "native":
            violations += [c for c in commands if re.search(r"\brag\s+(?:search|benchmarks)\b", c)]
        state = {"id": case["id"], "corpus": corpus_name, "variant": variant,
                 "elapsed_s": time.monotonic() - started, "returncode": result.returncode,
                 "answer": answer, "error": None if answer is not None else
                 result.stderr[-1000:], "usage": usage, "tool_calls": len(calls),
                 "protocol_violations": violations}
    except subprocess.TimeoutExpired:
        state = {"id": case["id"], "corpus": corpus_name, "variant": variant,
                 "elapsed_s": time.monotonic() - started, "returncode": -1,
                 "answer": None, "error": "timeout"}
    save(output / "result.json", state)
    return state


def agent(variant, split="test", limit=60):
    cases = sample(lines(HOME / "questions.jsonl"), split, limit)
    if not cases:
        raise RuntimeError("no validated questions for selected split")
    completed = []
    for case in cases:
        for corpus_name, _ in corpora():
            completed.append(agent_variant(case, corpus_name, variant))
    return {"runs": len(completed), "success": sum(r["returncode"] == 0 for r in completed),
            "variant": variant, "split": split}


def judge(limit=60):
    cases = {c["id"]: c for c in lines(HOME / "questions.jsonl")}
    results = sorted((HOME / "agent").glob("*/result.json")) if (HOME / "agent").exists() else []
    judged = 0
    for path in results:
        if judged >= limit:
            break
        trial = read(path, {})
        if (path.parent / "judgment.json").exists() or trial["answer"] is None:
            continue
        case = cases[trial["id"]]
        citations = trial["answer"].get("citations", [])
        verified = []
        for citation in citations:
            p = SOURCE / "papers" / citation.get("paper_id", "")
            row = next((r for r in sections(p) if r["id"] == citation.get("id")),
                       None) if p.is_dir() else None
            verified.append(bool(row and citation.get("quote") in row["text"]))
        evidence = []
        for e in case["evidence"]:
            row = next(r for r in sections(SOURCE / "papers" / e["paper_id"])
                       if r["id"] == e["id"])
            evidence.append({"paper_id": e["paper_id"], "id": e["id"],
                             "text": row["text"][:7000]})
        prompt = ("Evaluate this answer only against the original paper evidence and the "
                  "reference answer. Treat citation identity validity as separate from "
                  "semantic support. Return JSON correct (boolean), supported (boolean), "
                  "reason (string). For a missing-paper question, the answer should clearly "
                  "state the limitation rather than invent a result.\n" +
                  json.dumps({"question": case["question"], "reference": case["answer"],
                              "answer": trial["answer"], "evidence": evidence,
                              "citation_ids_valid": verified}, ensure_ascii=False))
        try:
            votes = [claude(prompt, {"correct": "boolean", "supported": "boolean",
                                    "reason": "string"}) for _ in range(2)]
            save(path.parent / "judgment.json",
                 {"votes": votes, "citation_ids_valid": verified,
                  "agreement": votes[0]["correct"] == votes[1]["correct"] and
                  votes[0]["supported"] == votes[1]["supported"]})
        except Exception as e:
            save(path.parent / "judgment.json", {"error": str(e)})
        judged += 1
    return {"judged": judged}


def report():
    rows = [r for mode in RETRIEVAL_MODES
            for r in lines(HOME / f"retrieval-{mode}.jsonl")]
    summary = {}
    for key in sorted({(r["corpus"], r["mode"]) for r in rows}):
        group = [r for r in rows if (r["corpus"], r["mode"]) == key]
        answerable = [r for r in group if r["complete20"] is not None]
        summary[f"{key[0]}/{key[1]}"] = {
            "questions": len(group),
            "complete20": sum(r["complete20"] for r in answerable) / len(answerable)
            if answerable else None,
            "recall20": sum(r["recall20"] for r in answerable) / len(answerable)
            if answerable else None,
            "mean_latency_s": sum(r["latency_s"] for r in group) / len(group),
            "p95_latency_s": sorted(r["latency_s"] for r in group)[
                min(len(group) - 1, int(.95 * len(group)))],
        }
    result = {"papers": len(sources(SOURCE)) if SOURCE.exists() else 0,
              "candidates": len(lines(HOME / "candidates.jsonl")),
              "validated": len(lines(HOME / "questions.jsonl")),
              "retrieval": summary}
    trials = [read(p, {}) for p in (HOME / "agent").glob("*/result.json")] if (
        HOME / "agent").exists() else []
    agent_summary = {}
    for key in sorted({(r["corpus"], r["variant"]) for r in trials}):
        group = [r for r in trials if (r["corpus"], r["variant"]) == key]
        judgments = [read(HOME / "agent" /
                          f"{r['id']}-{r['corpus']}-{r['variant']}" / "judgment.json", {})
                     for r in group]
        agreed = [j for j in judgments if j.get("agreement")]
        sound = [j for j in agreed if all(j.get("citation_ids_valid", []))]
        agent_summary[f"{key[0]}/{key[1]}"] = {
            "runs": len(group), "completed": sum(r["returncode"] == 0 for r in group),
            "agreed_judgments": len(agreed),
            "correct_rate": sum(j["votes"][0]["correct"] for j in agreed) / len(agreed)
            if agreed else None,
            "supported_rate": sum(j["votes"][0]["supported"] for j in sound) / len(agreed)
            if agreed else None,
            "mean_elapsed_s": sum(r["elapsed_s"] for r in group) / len(group),
            "p95_elapsed_s": sorted(r["elapsed_s"] for r in group)[
                min(len(group) - 1, int(.95 * len(group)))],
            "mean_input_tokens": sum(sum(r.get("usage", {}).get(k, 0) for k in (
                "input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"))
                for r in group) / len(group),
            "mean_tool_calls": sum(r.get("tool_calls", 0) for r in group) / len(group),
            "protocol_violations": sum(bool(r.get("protocol_violations")) for r in group)}
    result["agents"] = agent_summary
    save(HOME / "report.json", result)
    return result


def run(argv):
    parser = argparse.ArgumentParser(prog="bin/pdb synth", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("corpus", "enrich", "generate", "validate", "variants", "retrieval",
                 "agent", "judge", "report"):
        sub.add_parser(name)
    sub.choices["corpus"].add_argument("--target", type=int, default=200)
    for name in ("enrich", "generate", "validate"):
        sub.choices[name].add_argument("--limit", type=int, default=200)
    sub.choices["variants"].add_argument("--limit", type=int, default=40)
    sub.choices["retrieval"].add_argument("--mode", required=True,
                                           choices=RETRIEVAL_MODES)
    sub.choices["agent"].add_argument("--variant", required=True,
                                      choices=("native", "lexical", "dense", "hybrid",
                                               "reranked", "structured", "feedback", "oracle"))
    sub.choices["agent"].add_argument("--split", choices=("development", "test"),
                                      default="test")
    sub.choices["agent"].add_argument("--limit", type=int, default=60)
    sub.choices["judge"].add_argument("--limit", type=int, default=60)
    args = parser.parse_args(argv)
    try:
        if args.command == "corpus":
            result = corpus(args.target)
        elif args.command == "enrich":
            result = enrich(args.limit)
        elif args.command == "generate":
            result = generate(args.limit)
        elif args.command == "validate":
            result = validate(args.limit)
        elif args.command == "variants":
            result = variants(args.limit)
        elif args.command == "retrieval":
            result = retrieval(args.mode)
        elif args.command == "agent":
            result = agent(args.variant, args.split, args.limit)
        elif args.command == "judge":
            result = judge(args.limit)
        else:
            result = report()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as e:
        print(f"bench: {type(e).__name__}: {e}", file=os.sys.stderr)
        return 1
