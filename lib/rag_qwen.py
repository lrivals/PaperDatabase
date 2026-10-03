"""Rebuildable evidence index over PaperDatabase's authoritative files (`bin/pdb rag`).

GPU route (Qwen3, opt-in): the default route is `pdb search` (lib/rag.py, CPU). Lexical
mode (SQLite FTS5) runs without a GPU; dense and hybrid modes need CUDA (lib/rag_models).
"""

import csv
import hashlib
import json
import math
import os
import re
import sqlite3
from pathlib import Path

from lib import schema
from lib import rag_models

FILES = ("metadata.json", "sections.jsonl", "fiche.md")
INDEX_VERSION = "2"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def file_hash(path):
    return digest(path.read_bytes())


def paths(root):
    root = Path(root)
    out = [root / "benchmarks.csv"]
    for d in sorted((root / "papers").iterdir()):
        if d.is_dir():
            out += [d / name for name in FILES]
    return out


def fingerprint(root):
    h = hashlib.sha256()
    for p in paths(root):
        h.update(str(p.relative_to(root)).encode())
        h.update(p.read_bytes())
    return h.hexdigest()


def index_path(root):
    return Path(root) / ".cache" / "rag" / "index.sqlite3"


def _chunks(text, token, kind):
    if token:
        offsets = token(text, add_special_tokens=False, return_offsets_mapping=True)["offset_mapping"]
    else:
        offsets = [m.span() for m in re.finditer(r"\S+", text)]
    if not offsets:
        return
    limit = 4096 if kind in ("table", "figure") else 512
    overlap = 0 if kind in ("table", "figure") else 64
    start = 0
    while start < len(offsets):
        end = min(start + limit, len(offsets))
        if end < len(offsets) and kind not in ("table", "figure"):
            cut = text.rfind("\n\n", offsets[start][0], offsets[end - 1][1])
            if cut > offsets[min(start + 383, end - 1)][0]:
                end = next((j for j in range(start + 1, end) if offsets[j][0] >= cut + 2), end)
        a, b = offsets[start][0], offsets[end - 1][1]
        yield a, b, text[a:b]
        if end == len(offsets):
            break
        start = max(start + 1, end - overlap)


def _database(path):
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    return db


def build(root, mode="hybrid", download=False):
    root = Path(root).resolve()
    if download and mode != "lexical":
        rag_models.download_models()
    fp = fingerprint(root)
    final = index_path(root)
    final.parent.mkdir(parents=True, exist_ok=True)
    old_vectors = {}
    if final.exists():
        with _database(final) as old:
            old_version = old.execute("SELECT value FROM info WHERE key='version'").fetchone()
            if old_version and old_version[0] == INDEX_VERSION and old.execute(
                    "SELECT value FROM info WHERE key='fingerprint'").fetchone()[0] == fp:
                if mode == "lexical" or old.execute("SELECT count(*) FROM evidence WHERE vector IS NULL").fetchone()[0] == 0:
                    return {"snapshot": fp, "unchanged": True}
            try:
                old_vectors = {r["retrieval"]: r["vector"] for r in old.execute(
                    "SELECT retrieval, vector FROM evidence WHERE vector IS NOT NULL")}
            except sqlite3.OperationalError:
                pass
    token = rag_models.tokenizer(download=download) if mode != "lexical" else None
    temp = final.with_name(f".{final.name}.{os.getpid()}.tmp")
    if temp.exists():
        temp.unlink()
    db = _database(temp)
    try:
        db.executescript("""
            CREATE TABLE info(key TEXT PRIMARY KEY, value TEXT NOT NULL);
            CREATE TABLE evidence(
                id TEXT PRIMARY KEY, paper_id TEXT, kind TEXT, source_path TEXT,
                source_hash TEXT, locator TEXT, start INTEGER, end INTEGER,
                page INTEGER, title TEXT, year INTEGER, section TEXT,
                text TEXT, retrieval TEXT, metadata TEXT, vector BLOB
            );
            CREATE VIRTUAL TABLE evidence_fts USING fts5(
                id UNINDEXED, body, tokenize='unicode61 remove_diacritics 2');
            CREATE TABLE benchmarks(row_number INTEGER PRIMARY KEY, evidence_id TEXT, data TEXT);
        """)
        db.execute("INSERT INTO info VALUES ('fingerprint', ?)", (fp,))
        db.execute("INSERT INTO info VALUES ('version', ?)", (INDEX_VERSION,))
        db.execute("INSERT INTO info VALUES ('model', ?)",
                   ("lexical" if mode == "lexical" else rag_models.EMBED_REV,))
        pending = []

        def add(paper, kind, path, source_hash, locator, text, section="", page=None):
            rel = str(path.relative_to(root))
            title = paper.get("title") or paper["id"]
            for start, end, chunk in _chunks(text, token, kind):
                evidence_id = digest(f"{paper['id']}|{source_hash}|{locator}|{start}|{end}".encode())[:24]
                retrieval = f"{title} ({paper.get('year') or 'n/r'}). {section}\n{chunk}"
                vector = old_vectors.get(retrieval) if mode != "lexical" else None
                metadata = {k: paper.get(k) for k in
                            ("authors", "doi", "arxiv_id", "venue", "url", "type", "extraction")}
                db.execute("INSERT INTO evidence VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                           (evidence_id, paper["id"], kind, rel, source_hash, locator,
                            start, end, page, title, paper.get("year"), section,
                            chunk, retrieval, json.dumps(metadata, ensure_ascii=False), vector))
                db.execute("INSERT INTO evidence_fts(id,body) VALUES (?,?)",
                           (evidence_id, retrieval))
                if mode != "lexical" and vector is None:
                    pending.append((evidence_id, retrieval))
                yield evidence_id

        papers = {}
        for p in sorted((root / "papers").glob("*/metadata.json")):
            meta = json.loads(p.read_text())
            if schema.validate_metadata(meta):
                raise ValueError(f"invalid metadata: {p}")
            papers[meta["id"]] = meta
            sections = p.parent / "sections.jsonl"
            section_hash = file_hash(sections)
            for n, line in enumerate(sections.read_text().splitlines()):
                row = json.loads(line)
                errs = schema.validate_section_row(row, meta["id"], n)
                if errs:
                    raise ValueError(f"{sections}:{n+1}: {'; '.join(errs)}")
                list(add(meta, row["kind"], sections, section_hash, row["id"], row["text"],
                         row["subsection"] or row["section"], row["page"]))
            if meta["status"]["fiche"] == "done":
                note = p.parent / "fiche.md"
                list(add(meta, "fiche", note, file_hash(note), "fiche", note.read_text(),
                         "curated reading note"))
        bench_path = root / "benchmarks.csv"
        bench_hash = file_hash(bench_path)
        with bench_path.open(newline="") as f:
            reader = csv.DictReader(f)
            if schema.check_header(reader.fieldnames):
                raise ValueError("benchmark columns differ from the corpus schema")
            for line_no, row in enumerate(reader, start=2):
                errs = schema.validate_benchmark_row(row)
                for key in schema.NUMERIC_COLUMNS:
                    val = row[key]
                    if val != schema.NR:
                        try:
                            if not math.isfinite(float(val)):
                                errs.append(f"nonfinite {key}")
                        except (TypeError, ValueError):
                            errs.append(f"invalid {key}")
                if errs:
                    raise ValueError(f"{bench_path}:{line_no}: {'; '.join(errs)}")
                if row["paper_id"] not in papers:
                    raise ValueError(f"unknown benchmark paper: {row['paper_id']}")
                text = "; ".join(f"{k}: {v}" for k, v in row.items())
                ids = list(add(papers[row["paper_id"]], "benchmark", bench_path, bench_hash,
                               f"row-{line_no}", text, row["source_section"]))
                db.execute("INSERT INTO benchmarks VALUES (?,?,?)",
                           (line_no, ids[0], json.dumps(row, ensure_ascii=False)))
        if pending:
            vectors = rag_models.embed_texts([t for _, t in pending], download=download)
            db.executemany("UPDATE evidence SET vector=? WHERE id=?",
                           [(v.tobytes(), evidence_id) for (evidence_id, _), v in zip(pending, vectors)])
        count = db.execute("SELECT count(*) FROM evidence").fetchone()[0]
        db.commit()
        db.close()
        os.replace(temp, final)
    except Exception:
        db.close()
        temp.unlink(missing_ok=True)
        raise
    return {"snapshot": fp, "unchanged": False, "records": count}


def open_index(root, stale=False):
    if not index_path(root).exists():
        raise RuntimeError("RAG index missing; run bin/pdb rag index")
    db = _database(index_path(root))
    try:
        version = db.execute("SELECT value FROM info WHERE key='version'").fetchone()
        if not version or version[0] != INDEX_VERSION:
            raise RuntimeError("RAG index format changed; run bin/pdb rag index")
        fp = db.execute("SELECT value FROM info WHERE key='fingerprint'").fetchone()[0]
        if not stale and fp != fingerprint(root):
            raise RuntimeError("RAG index is stale; run bin/pdb rag index")
        return db, fp
    except Exception:
        db.close()
        raise


def _result(row):
    out = {k: row[k] for k in row.keys() if k not in ("vector", "retrieval")}
    out["metadata"] = json.loads(out["metadata"])
    return out


def search(root, query, mode="hybrid", limit=12, paper=None, kind=None, reranking=None):
    if not query.strip():
        raise ValueError("empty query")
    if mode not in ("lexical", "dense", "hybrid"):
        raise ValueError("mode must be lexical, dense, or hybrid")
    db, fp = open_index(root)
    try:
        where, args = [], []
        if paper:
            where.append("paper_id=?")
            args.append(paper)
        if kind:
            where.append("kind=?")
            args.append(kind)
        condition = (" AND " + " AND ".join(where)) if where else ""
        channels = []
        if mode in ("lexical", "hybrid"):
            terms = re.findall(r"\w+", query, re.UNICODE)[:20]
            if terms:
                expression = " OR ".join('"' + t.replace('"', '""') + '"' for t in terms)
                sql = ("SELECT evidence.id AS id FROM evidence_fts JOIN evidence "
                       "ON evidence.id=evidence_fts.id WHERE evidence_fts MATCH ?" + condition +
                       " ORDER BY bm25(evidence_fts) LIMIT 40")
                channels.append([r["id"] for r in db.execute(sql, [expression, *args])])
        if mode in ("dense", "hybrid"):
            rows = list(db.execute("SELECT id,vector FROM evidence WHERE vector IS NOT NULL" +
                                   (" AND " + " AND ".join(where) if where else ""), args))
            if not rows:
                raise RuntimeError("dense index unavailable; run bin/pdb rag index")
            import numpy as np
            q = rag_models.embed_texts([query], query=True)[0]
            mat = np.stack([np.frombuffer(r["vector"], dtype=np.float32) for r in rows])
            sims = mat @ q
            channels.append([rows[int(i)]["id"] for i in np.argsort(-sims)[:40]])
        scores = {}
        for ids in channels:
            for rank, evidence_id in enumerate(ids, start=1):
                scores[evidence_id] = scores.get(evidence_id, 0.0) + 1 / (60 + rank)
        ranked = sorted(scores, key=scores.get, reverse=True)[:80]
        results = [_result(db.execute("SELECT * FROM evidence WHERE id=?", (x,)).fetchone())
                   for x in ranked]
        if reranking is None:
            reranking = mode == "hybrid"
        if reranking and results:
            relevance = rag_models.rerank(query, [r["text"] for r in results])
            for result, score in zip(results, relevance):
                result["rerank_score"] = score
            results.sort(key=lambda r: r["rerank_score"], reverse=True)
        else:
            for result in results:
                result["fusion_score"] = scores[result["id"]]
        selected, counts = [], {}
        for result in results:
            pid = result["paper_id"]
            if not paper and counts.get(pid, 0) >= 3:
                continue
            selected.append(result)
            counts[pid] = counts.get(pid, 0) + 1
            if len(selected) >= limit:
                break
        return {"query": query, "mode": mode, "snapshot": fp,
                "total_candidates": len(scores), "truncated": len(scores) > len(selected),
                "results": selected}
    finally:
        db.close()


def evidence(root, evidence_id, parent=False):
    db, fp = open_index(root)
    try:
        row = db.execute("SELECT * FROM evidence WHERE id=?", (evidence_id,)).fetchone()
        if row is None:
            raise KeyError(evidence_id)
        result = _result(row)
        result["snapshot"] = fp
        if parent:
            siblings = db.execute("SELECT text FROM evidence WHERE paper_id=? AND source_hash=? "
                                  "AND locator=? ORDER BY start", (row["paper_id"],
                                  row["source_hash"], row["locator"])).fetchall()
            result["parent_text"] = "\n".join(r["text"] for r in siblings)[:12000]
        return result
    finally:
        db.close()


def benchmarks(root, filters=None):
    filters = filters or []
    if not isinstance(filters, list) or any(not isinstance(f, dict) for f in filters):
        raise ValueError("benchmark filters must be a JSON list of objects")
    for f in filters:
        if f.get("field") not in schema.ALL_COLUMNS or f.get("op") not in ("eq", "gte", "lte"):
            raise ValueError("unsupported benchmark filter")
        if f["op"] != "eq":
            if f["field"] not in schema.NUMERIC_COLUMNS:
                raise ValueError("range filter requires a numeric field")
            try:
                if not math.isfinite(float(f.get("value"))):
                    raise ValueError("nonfinite filter")
            except (TypeError, ValueError) as e:
                raise ValueError("numeric benchmark filter requires a finite value") from e
    db, fp = open_index(root)
    try:
        out = []
        for r in db.execute("SELECT * FROM benchmarks ORDER BY row_number"):
            row = json.loads(r["data"])
            def match(f):
                value = row.get(f["field"], schema.NR)
                target = f.get("value")
                if f["op"] == "eq":
                    return str(value).casefold() == str(target).casefold()
                if f["field"] not in schema.NUMERIC_COLUMNS or value == schema.NR:
                    return False
                number = float(value)
                threshold = float(target)
                if not math.isfinite(threshold):
                    raise ValueError("nonfinite filter")
                return number >= threshold if f["op"] == "gte" else number <= threshold
            if all(match(f) for f in filters):
                item = {**row, "evidence_id": r["evidence_id"], "row_number": r["row_number"]}
                if row["fps"] != schema.NR and row["power_w"] != schema.NR and float(row["power_w"]) > 0:
                    item["computed_fps_per_w"] = float(row["fps"]) / float(row["power_w"])
                    item["computed_power_scope"] = row["power_scope"]
                out.append(item)
        return {"snapshot": fp, "total_matches": len(out), "results": out}
    finally:
        db.close()


def check_answer(root, data):
    errors = []
    if not isinstance(data, dict) or not isinstance(data.get("claims"), list) or not data["claims"]:
        raise ValueError("answer record requires a nonempty claims list")
    db, fp = open_index(root)
    try:
        if data.get("snapshot") != fp:
            errors.append("answer snapshot differs from current index")
        for i, claim in enumerate(data["claims"]):
            if not isinstance(claim, dict) or not isinstance(claim.get("text"), str) or not claim["text"].strip():
                errors.append(f"claim {i}: missing claim text")
                continue
            citations = claim.get("citations")
            if citations is None:
                evidence_ids = claim.get("evidence_ids")
                citations = [{"id": eid, "excerpt": claim.get("excerpt")}
                             for eid in evidence_ids] if isinstance(evidence_ids, list) else []
            if not isinstance(citations, list) or not citations:
                errors.append(f"claim {i}: no evidence")
                continue
            for citation in citations:
                if not isinstance(citation, dict) or not isinstance(citation.get("id"), str):
                    errors.append(f"claim {i}: malformed citation")
                    continue
                evidence_id = citation["id"]
                excerpt = citation.get("excerpt")
                if not isinstance(excerpt, str) or not excerpt.strip():
                    errors.append(f"claim {i}: missing excerpt for {evidence_id}")
                    continue
                row = db.execute("SELECT text FROM evidence WHERE id=?", (evidence_id,)).fetchone()
                if row is None:
                    errors.append(f"claim {i}: unknown evidence {evidence_id}")
                elif excerpt not in row["text"]:
                    errors.append(f"claim {i}: excerpt absent from {evidence_id}")
        return {"valid": not errors, "errors": errors, "snapshot": fp,
                "semantic_support_checked": False}
    finally:
        db.close()
