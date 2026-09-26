"""Bounded open-access discovery and ingestion for evidence searches."""

import hashlib
import ipaddress
import json
import os
import re
import socket
import time
import fcntl
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from lxml import etree

from lib import ids, openalex, rag_models, rag_qwen as rag

MAX_SEARCHES = 8
MAX_PAPERS = 8
MAX_PDF = 50 * 1024 * 1024
MAX_BYTES = 200 * 1024 * 1024
MAX_SECONDS = 900


def _run_dir(root, run_id):
    if not re.fullmatch(r"[a-zA-Z0-9_-]{1,64}", run_id):
        raise ValueError("run ID must contain only letters, digits, _ or -")
    return Path(root) / ".cache" / "rag" / "runs" / run_id


def _save(path, data):
    temp = path.with_suffix(".tmp")
    temp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    os.replace(temp, path)


def _public_https(url):
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("external PDF URL must be public HTTPS")
    for result in socket.getaddrinfo(parsed.hostname, 443, type=socket.SOCK_STREAM):
        if not ipaddress.ip_address(result[4][0]).is_global:
            raise ValueError("external PDF URL resolves to a private address")


def _download(url, target, budget):
    """Validate every redirect, stream into staging, and enforce shared byte limits."""
    for _ in range(5):
        _public_https(url)
        with requests.get(url, timeout=(15, 120), stream=True, allow_redirects=False) as res:
            if res.is_redirect:
                url = urljoin(url, res.headers["Location"])
                continue
            res.raise_for_status()
            if int(res.headers.get("Content-Length", "0")) > MAX_PDF:
                raise ValueError("PDF exceeds 50 MB")
            count = 0
            first = b""
            with target.open("wb") as f:
                for part in res.iter_content(1 << 18):
                    if not part:
                        continue
                    if len(first) < 4:
                        first += part[:4 - len(first)]
                        if len(first) == 4 and first != b"%PDF":
                            raise ValueError("download is not a PDF")
                    count += len(part)
                    if count > MAX_PDF or budget + count > MAX_BYTES:
                        raise ValueError("PDF byte budget exceeded")
                    f.write(part)
            if first != b"%PDF":
                raise ValueError("download is not a PDF")
            return count, url
    raise ValueError("too many PDF redirects")


def _arxiv_candidates(query, limit=8):
    params = {"search_query": " AND ".join(f"all:{word}" for word in query.split()[:2]),
              "start": 0, "max_results": limit, "sortBy": "relevance"}
    res = requests.get("https://export.arxiv.org/api/query", params=params, timeout=30)
    res.raise_for_status()
    ns = {"a": "http://www.w3.org/2005/Atom"}
    feed = etree.fromstring(res.content)
    result = []
    for e in feed.xpath("a:entry", namespaces=ns):
        arxiv_id = ids.find_arxiv_id(e.xpath("string(a:id)", namespaces=ns))
        if not arxiv_id:
            continue
        title = " ".join(e.xpath("string(a:title)", namespaces=ns).split())
        abstract = " ".join(e.xpath("string(a:summary)", namespaces=ns).split())
        authors = []
        for a in e.xpath("a:author/a:name/text()", namespaces=ns):
            parts = a.split()
            authors.append({"given": " ".join(parts[:-1]) or None, "family": parts[-1]})
        published = e.xpath("string(a:published)", namespaces=ns)
        result.append({"title": title, "abstract": abstract,
                       "year": int(published[:4]) if published else None,
                       "authors": authors, "arxiv_id": arxiv_id, "doi": None,
                       "venue": "arXiv preprint", "type": "preprint",
                       "url": f"https://arxiv.org/abs/{arxiv_id}",
                       "pdf_url": f"https://arxiv.org/pdf/{arxiv_id}",
                       "version": re.search(r"v\d+$", e.xpath("string(a:id)", namespaces=ns) or "").group(0)
                                  if re.search(r"v\d+$", e.xpath("string(a:id)", namespaces=ns) or "") else None})
    return result


def _openalex_candidates(query, cache, limit=12):
    client = openalex.Client(cache_dir=cache)
    candidates = []
    for work in client.works(search=query, limit=limit):
        arxiv_id = openalex.arxiv_id_of(work)
        urls = ([f"https://arxiv.org/pdf/{arxiv_id}"] if arxiv_id else [])
        urls += [loc["pdf_url"] for loc in
                 [work.get("best_oa_location") or {}, *(work.get("locations") or [])]
                 if loc.get("pdf_url")]
        if not urls:
            continue
        authors = []
        for a in work.get("authorships") or []:
            name = (a.get("author") or {}).get("display_name") or ""
            parts = name.split()
            if parts:
                authors.append({"given": " ".join(parts[:-1]) or None,
                                "family": parts[-1]})
        candidates.append({"title": work.get("title"),
                           "abstract": openalex.abstract_of(work),
                           "year": work.get("publication_year"),
                           "authors": authors, "arxiv_id": arxiv_id,
                           "doi": openalex.doi_of(work),
                           "venue": openalex.venue_of(work),
                           "url": f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id else
                                  (work.get("doi") or work.get("id")),
                           "openalex_id": openalex.short_id(work.get("id")),
                           "pdf_urls": list(dict.fromkeys(urls))})
    return candidates


def _score(query, candidate):
    words = set(re.findall(r"\w+", query.casefold())) - {
        "what", "which", "where", "does", "with", "from", "have", "that", "this",
        "how", "the", "and", "are", "for", "its", "was", "can", "did", "who", "why",
        "pour", "quel", "quelle", "quels", "quelles", "avec", "dans", "est", "les",
        "une", "des", "sur", "par", "qui", "que", "comment"}
    title = set(re.findall(r"\w+", (candidate.get("title") or "").casefold()))
    abstract = set(re.findall(r"\w+", (candidate.get("abstract") or "").casefold()))
    return 3 * len(words & title) + len(words & abstract)


def _source_match(stage, query):
    """Choose a passage from parsed original text before adding a paper to the library."""
    rows = [json.loads(line) for line in (stage / "sections.jsonl").read_text().splitlines()]
    rows = [r for r in rows if r["kind"] in ("abstract", "section", "table", "figure")
            and len(r["text"].strip()) >= 80]
    if not rows or sum(len(r["text"]) for r in rows) < 1000:
        raise ValueError("PDF extraction has too little original text")
    token = rag_models.tokenizer()
    passages = [{"locator": r["id"], "start": start, "end": end, "text": chunk}
                for r in rows for start, end, chunk in rag._chunks(r["text"], token, r["kind"])
                if len(chunk.strip()) >= 80]
    words = set(re.findall(r"\w+", query.casefold()))
    passages.sort(key=lambda r: len(words & set(re.findall(r"\w+", r["text"].casefold()))),
                  reverse=True)
    passages = passages[:8]
    scores = rag_models.rerank(query, [r["text"] for r in passages])
    best = max(range(len(scores)), key=scores.__getitem__)
    if scores[best] < 0.5:
        raise ValueError("no extracted source passage meets the relevance threshold")
    return passages[best], scores[best]


def _acquire_unlocked(root, query, run_id, limit=3):
    """Import relevant, validated full texts; return explicit acquisition outcomes."""
    if not query.strip():
        raise ValueError("empty discovery question")
    root = Path(root).resolve()
    run = _run_dir(root, run_id)
    run.mkdir(parents=True, exist_ok=True)
    manifest_path = run / "manifest.json"
    state = json.loads(manifest_path.read_text()) if manifest_path.exists() else {
        "started": time.time(), "searches": 0, "attempts": 0,
        "downloads": 0, "bytes": 0,
        "queries": [], "imported": [], "errors": []}
    state.setdefault("attempts", state["downloads"])
    if state["searches"] >= MAX_SEARCHES or time.time() - state["started"] > MAX_SECONDS:
        raise RuntimeError("external search budget exhausted")
    state["searches"] += 1
    state["queries"].append(query)
    _save(manifest_path, state)
    candidates = []
    try:
        candidates.extend(_openalex_candidates(query, run / "openalex-cache"))
    except (openalex.OpenAlexError, requests.RequestException) as e:
        state["errors"].append(f"OpenAlex: {e}")
    try:
        candidates.extend(_arxiv_candidates(query))
    except (requests.RequestException, etree.XMLSyntaxError) as e:
        state["errors"].append(f"arXiv: {e}")
    candidates.sort(key=lambda c: _score(query, c), reverse=True)
    from bin import ingest, reindex
    known = [json.loads(p.read_text()) for p in (root / "papers").glob("*/metadata.json")]
    known_hashes = {hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in (root / "papers").glob("*/paper.pdf")}
    imported = []
    selected = []
    seen = set()
    for c in candidates:
        if (len(imported) >= limit or state["attempts"] >= MAX_PAPERS or
                state["bytes"] >= MAX_BYTES or time.time() - state["started"] > MAX_SECONDS):
            break
        if _score(query, c) == 0:
            continue
        identity = c.get("arxiv_id") or c.get("doi") or c.get("openalex_id") or c.get("title")
        if identity in seen:
            continue
        seen.add(identity)
        if any((c.get("arxiv_id") and c["arxiv_id"] == p.get("arxiv_id")) or
               (c.get("doi") and c["doi"].casefold() == (p.get("doi") or "").casefold())
               for p in known):
            continue
        folder = run / "external" / hashlib.sha256(str(identity).encode()).hexdigest()[:16]
        folder.mkdir(parents=True, exist_ok=True)
        pdf = folder / "source.pdf"
        urls = c.get("pdf_urls") or [c["pdf_url"]]
        retrieved = None
        for url in urls:
            if state["attempts"] >= MAX_PAPERS or state["bytes"] >= MAX_BYTES:
                break
            state["attempts"] += 1
            _save(manifest_path, state)
            try:
                size, resolved = _download(url, pdf, state["bytes"])
                retrieved = resolved
                state["bytes"] += size
                state["downloads"] += 1
                _save(manifest_path, state)
                break
            except (ValueError, requests.RequestException, OSError) as e:
                state["bytes"] += pdf.stat().st_size if pdf.exists() else 0
                pdf.unlink(missing_ok=True)
                state["errors"].append(f"{identity}: {type(e).__name__}: {e}")
                _save(manifest_path, state)
        if not retrieved:
            continue
        try:
            pdf_hash = hashlib.sha256(pdf.read_bytes()).hexdigest()
            if pdf_hash in known_hashes:
                raise ValueError("PDF already exists in the library")
            stage = folder / "papers"
            stage.mkdir(exist_ok=True)
            status, detail = ingest.process(pdf, papers_dir=stage, source_meta=c,
                                             citation_dirs=(folder,),
                                             use_grobid=ingest.grobid_alive())
            if status != "ingéré":
                raise ValueError(detail)
            staged = next(stage.iterdir())
            meta = json.loads((staged / "metadata.json").read_text())
            problems, notes = [], []
            reindex.check_paper_files(staged, meta, problems, notes)
            if problems:
                raise ValueError("; ".join(problems))
            passage, relevance = _source_match(staged, query)
            if (root / "papers" / staged.name).exists():
                raise ValueError("paper ID collision; staged file kept for review")
            provenance = {"query": query, "provider": c.get("openalex_id") or "arxiv",
                          "source_url": retrieved, "retrieved_at": time.time(),
                          "version": c.get("version"),
                          "sha256": pdf_hash,
                          "selected_locator": passage["locator"],
                          "selected_start": passage["start"],
                          "selected_end": passage["end"],
                          "selected_relevance": relevance,
                          "extraction_warnings": meta["extraction"]["warnings"]}
            (staged / "acquisition.json").write_text(
                json.dumps(provenance, ensure_ascii=False, indent=2) + "\n")
            os.replace(staged, root / "papers" / staged.name)
            known.append(meta)
            known_hashes.add(pdf_hash)
            imported.append(staged.name)
            selected.append((staged.name, passage["locator"], passage["start"], passage["end"]))
            state["imported"].append(staged.name)
            _save(manifest_path, state)
        except Exception as e:
            state["errors"].append(f"{identity}: parse/import: {e}")
            _save(manifest_path, state)
    if imported:
        if reindex.run(root):
            raise RuntimeError("imported papers need index validation; check bin/pdb reindex")
        rag.build(root, mode="hybrid", download=False)
    evidence = []
    if selected:
        db, _ = rag.open_index(root)
        try:
            for paper_id, locator, start, end in selected:
                row = db.execute("SELECT id, text FROM evidence WHERE paper_id=? AND locator=? "
                                 "AND start=? AND end=?", (paper_id, locator, start, end)).fetchone()
                if row:
                    evidence.append({"paper_id": paper_id, "evidence_id": row["id"],
                                     "excerpt": row["text"][:400]})
        finally:
            db.close()
    return {"run": run_id, "query": query, "imported": imported,
            "selected_evidence": evidence,
            "errors": state["errors"], "searches": state["searches"],
            "attempts": state["attempts"], "downloads": state["downloads"],
            "bytes": state["bytes"]}


def acquire(root, query, run_id, limit=3):
    """Serialize corpus mutations and the following index rebuild."""
    lock = Path(root) / ".cache" / "rag" / "import.lock"
    lock.parent.mkdir(parents=True, exist_ok=True)
    with lock.open("w") as file:
        fcntl.flock(file, fcntl.LOCK_EX)
        return _acquire_unlocked(root, query, run_id, limit)
