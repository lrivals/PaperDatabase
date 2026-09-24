"""Parsing du TEI produit par GROBID.

Produit la représentation intermédiaire commune aux deux backends (voir lib/doc.py) :
un en-tête (métadonnées), une liste de blocs ordonnés, une liste de références.
"""
import re

from lxml import etree

from lib.doc import Block, heading_level, is_numbered
from lib.ids import find_arxiv_id

NS = {"tei": "http://www.tei-c.org/ns/1.0"}
FIGURES_SECTION = "Figures et tableaux"


def _x(node, path):
    return node.xpath(path, namespaces=NS)


def _first(node, path):
    r = _x(node, path)
    return r[0] if r else None


def _text(node):
    """Texte d'un nœud, espaces normalisés ; None si vide."""
    if node is None:
        return None
    if isinstance(node, str):
        t = node
    else:
        t = "".join(node.itertext())
    t = re.sub(r"\s+", " ", t).strip()
    return t or None


def _page(node):
    """Page du PDF d'après l'attribut coords (« page,x,y,w,h;… »)."""
    c = node.get("coords")
    if not c:
        return None
    try:
        return int(c.split(",", 1)[0])
    except ValueError:
        return None


def _year(s):
    m = re.search(r"(1[89]|20)\d{2}", s or "")
    return int(m.group(0)) if m else None


def load(path_or_bytes):
    if isinstance(path_or_bytes, (bytes, bytearray)):
        return etree.fromstring(path_or_bytes)
    return etree.parse(str(path_or_bytes)).getroot()


# --- teiHeader ------------------------------------------------------------------------

def _person(pers):
    given = " ".join(t for t in (_text(f) for f in _x(pers, "tei:forename")) if t) or None
    family = _text(_first(pers, "tei:surname"))
    return {"given": given, "family": family}


def parse_header(root):
    h = _first(root, "tei:teiHeader")
    bibl = _first(h, "tei:fileDesc/tei:sourceDesc/tei:biblStruct")

    title = _text(_first(h, "tei:fileDesc/tei:titleStmt/tei:title[@type='main']"))
    authors = []
    if bibl is not None:
        for pers in _x(bibl, "tei:analytic/tei:author/tei:persName"):
            a = _person(pers)
            if a["family"]:
                authors.append(a)

    year = None
    for path in (
        "tei:fileDesc/tei:publicationStmt/tei:date[@type='published']/@when",
        "tei:fileDesc/tei:sourceDesc/tei:biblStruct/tei:monogr/tei:imprint/tei:date/@when",
        "tei:fileDesc/tei:publicationStmt/tei:date/@when",
    ):
        v = _first(h, path)
        if v and _year(v):
            year = _year(v)
            break

    doi = arxiv_id = venue = None
    if bibl is not None:
        doi = _text(_first(bibl, ".//tei:idno[@type='DOI']"))
        arx = _text(_first(bibl, ".//tei:idno[@type='arXiv']"))
        arxiv_id = find_arxiv_id(arx.replace("arXiv:", "")) if arx else None
        venue = _text(_first(bibl, "tei:monogr/tei:title[@level='j' or @level='m']"))

    abstract = _text(_first(h, "tei:profileDesc/tei:abstract"))
    keywords = [t for t in (_text(k) for k in _x(h, "tei:profileDesc/tei:textClass/tei:keywords/tei:term")) if t]
    return {
        "title": title,
        "authors": authors,
        "year": year,
        "venue": venue,
        "doi": doi,
        "arxiv_id": arxiv_id,
        "abstract": abstract,
        "keywords": keywords,
    }


# --- text/body ------------------------------------------------------------------------

def _paragraph_nodes(div):
    """Paragraphes d'une div dans l'ordre : p, formules, éléments de liste."""
    return _x(div, "tei:p | tei:formula | tei:list/tei:item | tei:note[@type!='raw_reference']")


def _table_text(fig):
    rows = []
    for row in _x(fig, ".//tei:table/tei:row"):
        cells = [_text(c) or "" for c in _x(row, "tei:cell")]
        if any(cells):
            rows.append(" | ".join(cells))
    return rows


def parse_body(root):
    """Blocs ordonnés : abstract, sections (avec hiérarchie), puis figures et tableaux."""
    blocks = []
    last_page = 1

    abstract = _first(root, "tei:teiHeader/tei:profileDesc/tei:abstract")
    if abstract is not None:
        paras = []
        for p in _x(abstract, ".//tei:p") or [abstract]:
            t = _text(p)
            if t:
                last_page = _page(p) or last_page
                paras.append((t, last_page))
        if paras:
            blocks.append(Block("abstract", "Abstract", None, 1, paras))

    body = _first(root, "tei:text/tei:body")
    if body is None:
        return blocks

    section = None
    for div in _x(body, "tei:div"):
        head = _first(div, "tei:head")
        head_text = _text(head)
        n = head.get("n") if head is not None else None
        if head_text:
            title = f"{n.rstrip('.')}. {head_text}" if n else head_text
            level = heading_level(title, n, current_numbered=is_numbered(section))
        else:
            title, level = None, None

        if level == 1 or (title and section is None):
            section, subsection = title, None
            level = 1
        elif level:
            subsection = title
        else:
            # div sans titre : suite de la section courante
            subsection = blocks[-1].subsection if blocks and blocks[-1].kind == "section" else None

        paras = []
        for p in _paragraph_nodes(div):
            t = _text(p)
            if not t:
                continue
            last_page = _page(p) or last_page
            paras.append((t, last_page))
        page = (_page(head) if head is not None else None) or (paras[0][1] if paras else last_page)
        blocks.append(Block("section", section or "(sans titre)", subsection, level,
                            paras, heading=title, page=page))

    for fig in _x(body, ".//tei:figure"):
        kind = "table" if fig.get("type") == "table" else "figure"
        label = _text(_first(fig, "tei:head"))
        if label:
            label = re.sub(r"\s+([.:])", r"\1", label)  # « TABLE I . » → « TABLE I. »
        desc = _text(_first(fig, "tei:figDesc"))
        if desc and label and desc.startswith(label.rstrip(" .")):
            label = None  # la légende répète déjà « Fig. 1. »
        caption = " ".join(t for t in (label, desc) if t)
        lines = _table_text(fig) if kind == "table" else []
        if not caption and not lines:
            continue
        page = _page(fig) or last_page
        if not label and not (desc and re.match(r"(?i)(fig|table)", desc)):
            caption = f"[figure sans légende identifiée] {caption}"
        paras = [(caption, page)] + [(line, page) for line in lines]
        blocks.append(Block(kind, FIGURES_SECTION, None, 1, paras, page=page))
    return blocks


# --- text/back ------------------------------------------------------------------------

def parse_refs(root):
    refs = []
    for b in _x(root, "tei:text/tei:back//tei:div[@type='references']//tei:biblStruct"):
        title = _text(_first(b, "tei:analytic/tei:title[@type='main']")) or \
            _text(_first(b, "tei:monogr/tei:title"))
        authors = [s for s in (_text(x) for x in _x(b, "tei:analytic/tei:author/tei:persName/tei:surname")) if s]
        if not authors:
            authors = [s for s in (_text(x) for x in _x(b, "tei:monogr/tei:author/tei:persName/tei:surname")) if s]
        arx = _text(_first(b, ".//tei:idno[@type='arXiv']"))
        refs.append({
            "raw": _text(_first(b, "tei:note[@type='raw_reference']")),
            "title": title,
            "authors": authors,
            "year": _year(_first(b, ".//tei:imprint/tei:date/@when")),
            "doi": _text(_first(b, ".//tei:idno[@type='DOI']")),
            "arxiv_id": find_arxiv_id(arx.replace("arXiv:", "")) if arx else None,
        })
    return refs


def parse(path_or_bytes):
    root = load(path_or_bytes)
    return parse_header(root), parse_body(root), parse_refs(root)
