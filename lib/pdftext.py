"""Extraction de repli via PyMuPDF, quand GROBID est indisponible ou échoue.

Moins fiable que GROBID : pas de métadonnées (hors champ titre du PDF), sections détectées
par heuristique sur les titres numérotés. Produit la même représentation que lib/tei.py.
"""
import re
from collections import Counter

import pymupdf

from lib.doc import Block, heading_level, is_numbered

HEADING_RE = re.compile(r"^(\d+(\.\d+)*\.?|[IVX]+\.)\s+[A-Z]")
SUBHEADING_RE = re.compile(r"^[A-H]\.\s+[A-Z][a-z]")  # « A. Deployment », une fois une section ouverte
CAPTION_RE = re.compile(r"^(Fig\.|Figure|Table|TABLE)\s*[\dIVX]+")
REFS_RE = re.compile(r"^(\d+\.?\s*)?(references|bibliography)$", re.IGNORECASE)
ABSTRACT_RE = re.compile(r"^abstract\b[\s.:—–-]*", re.IGNORECASE)
NOISE_RE = re.compile(
    r"^(\d{1,4}|page \d+( of \d+)?)$"                     # numéros de page isolés
    r"|©|copyright|all rights reserved"                    # mentions de copyright
    r"|^(https?://(dx\.)?doi\.org/|doi:\s*10\.)"           # DOI de bas de page
    r"|^arXiv:\d{4}\.\d{4,5}",                             # filigrane arXiv
    re.IGNORECASE,
)


def _norm(line):
    return re.sub(r"\d+", "#", line.strip().lower())


def _page_blocks(doc):
    """[(page, [lignes])] par bloc de texte, dans l'ordre de lecture de PyMuPDF."""
    out = []
    for pno, page in enumerate(doc, start=1):
        for b in page.get_text("blocks", sort=False):
            if b[6] != 0:  # bloc image
                continue
            lines = [l.strip() for l in b[4].splitlines() if l.strip()]
            if lines:
                out.append((pno, lines))
    return out


def _repeated_lines(blocks, min_pages=3):
    """Lignes identiques (chiffres neutralisés) présentes sur ≥ min_pages pages : en-têtes/pieds."""
    pages_by_line = {}
    for pno, lines in blocks:
        for l in lines:
            if len(l) < 120:
                pages_by_line.setdefault(_norm(l), set()).add(pno)
    return {k for k, v in pages_by_line.items() if len(v) >= min_pages}


def _join(lines):
    """Recolle les lignes d'un paragraphe, en réparant les césures en fin de ligne."""
    text = ""
    for l in lines:
        if text.endswith("-") and l[:1].islower():
            text = text[:-1] + l
        else:
            text = f"{text} {l}" if text else l
    return re.sub(r"\s+", " ", text).strip()


def _split_refs(paras):
    raw = " ".join(t for t, _ in paras)
    parts = re.split(r"\s(?=\[\d+\]\s)", raw)
    if len(parts) < 3:
        parts = [t for t, _ in paras]
    return [{"raw": p.strip(), "title": None, "authors": [], "year": None,
             "doi": None, "arxiv_id": None} for p in parts if p.strip()]


def extract(pdf_path):
    doc = pymupdf.open(pdf_path)
    title = (doc.metadata or {}).get("title") or None
    if title and (len(title) < 8 or re.search(r"(?i)\.(pdf|docx?|tex)$|^untitled|microsoft word", title)):
        title = None

    raw_blocks = _page_blocks(doc)
    repeated = _repeated_lines(raw_blocks)

    blocks, ref_paras = [], []
    section, subsection = None, None
    cur = None
    in_refs = False
    for pno, lines in raw_blocks:
        lines = [l for l in lines if _norm(l) not in repeated and not NOISE_RE.search(l)]
        if not lines:
            continue
        text = _join(lines)
        if in_refs:
            ref_paras.append((text, pno))
            continue
        if REFS_RE.match(text):
            in_refs = True
            continue
        if section is None and ABSTRACT_RE.match(text) and not any(b.kind == "abstract" for b in blocks):
            body = ABSTRACT_RE.sub("", text)
            cur = Block("abstract", "Abstract", None, 1, [(body, pno)] if body else [], page=pno)
            blocks.append(cur)
            continue
        if CAPTION_RE.match(text):
            kind = "table" if text.lower().startswith("tab") else "figure"
            blocks.append(Block(kind, section or "(préambule)", subsection, None, [(text, pno)], page=pno))
            continue
        is_heading = HEADING_RE.match(text) or (section and SUBHEADING_RE.match(text))
        if len(lines) <= 2 and len(text) < 100 and is_heading:
            level = heading_level(text, current_numbered=is_numbered(section))
            if level == 1 or section is None:
                section, subsection, level = text, None, 1
            else:
                subsection = text
            cur = Block("section", section, subsection, level, [], heading=text, page=pno)
            blocks.append(cur)
            continue
        # nouveau bloc après une légende, ou après un abstract déjà rempli
        if cur is None or blocks[-1] is not cur or (cur.kind == "abstract" and cur.paras):
            cur = Block("section", section or "(préambule)", subsection, None, [], page=pno)
            blocks.append(cur)
        cur.paras.append((text, pno))

    header = {"title": title, "authors": [], "year": None, "venue": None, "doi": None,
              "arxiv_id": None, "abstract": None, "keywords": []}
    abstract = next((b for b in blocks if b.kind == "abstract"), None)
    if abstract and abstract.paras:
        header["abstract"] = " ".join(t for t, _ in abstract.paras)
    return header, [b for b in blocks if b.paras or b.heading], _split_refs(ref_paras) if ref_paras else []
