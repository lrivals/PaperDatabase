"""Représentation intermédiaire d'un article, commune aux backends GROBID et PyMuPDF,
et sérialisation vers fulltext.md / sections.jsonl.
"""
import re
from dataclasses import dataclass, field

MAX_SECTION_CHARS = 6000

_TOP_LEVEL_WORDS = re.compile(
    r"(?i)^(abstract|introduction|related work|background|conclusions?|discussion|"
    r"acknowledg|appendix|references|bibliography|future work|summary)"
)


@dataclass
class Block:
    kind: str                 # abstract | section | figure | table
    section: str              # section de rattachement, numérotation comprise
    subsection: str | None
    level: int | None         # 1 = section, 2+ = sous-section
    paras: list = field(default_factory=list)   # [(texte, page)]
    heading: str | None = None                  # titre introduit par ce bloc, s'il y en a un
    page: int | None = None


def heading_level(title, n=None, current_numbered=False):
    """Niveau d'un titre d'après sa numérotation : 'III.' → 1, 'A.' → 2, '3.2' → 2.

    Un titre non numéroté vaut 1, sauf au sein d'un papier numéroté où il est traité comme
    sous-section (sauf mots de premier niveau : Conclusion, Acknowledgment…).
    """
    if n:
        return len([p for p in n.strip(".").split(".") if p])
    if re.match(r"^[IVX]+\.\s", title):
        return 1
    if re.match(r"^[A-Z]\.\s", title):
        return 2
    m = re.match(r"^(\d+(?:\.\d+)*)\.?\s+\S", title)
    if m:
        return len(m.group(1).split("."))
    if re.match(r"^\d+\)\s", title):
        return 2
    if current_numbered and not _TOP_LEVEL_WORDS.match(title):
        return 2
    return 1


def is_numbered(title):
    return bool(title and re.match(r"^([IVX]+\.|\d+(\.\d+)*\.?)\s", title))


def split_paragraphs(paras, limit=MAX_SECTION_CHARS):
    """Découpe une suite de paragraphes en morceaux ≤ limit, sur frontières de paragraphes."""
    chunks, cur, size = [], [], 0
    for p in paras:
        if cur and size + len(p[0]) > limit:
            chunks.append(cur)
            cur, size = [], 0
        cur.append(p)
        size += len(p[0]) + 2
    if cur:
        chunks.append(cur)
    return chunks


def to_sections(paper_id, blocks):
    """Lignes de sections.jsonl, dans l'ordre du papier."""
    rows = []
    for b in blocks:
        if not b.paras:
            continue
        # une légende et ses lignes de tableau restent ensemble
        pieces = [b.paras] if b.kind in ("figure", "table") else split_paragraphs(b.paras)
        for chunk in pieces:
            order = len(rows)
            rows.append({
                "id": f"{paper_id}#{order:03d}",
                "paper_id": paper_id,
                "kind": b.kind,
                "section": b.section,
                "subsection": b.subsection,
                "order": order,
                "page": chunk[0][1] if chunk[0][1] is not None else b.page,
                "text": "\n\n".join(t for t, _ in chunk),
            })
    return rows


def _yaml_str(s):
    if s is None:
        return "null"
    return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"') + '"'


def render_fulltext(meta, blocks):
    out = [
        "---",
        f"id: {meta['id']}",
        f"title: {_yaml_str(meta.get('title'))}",
        f"year: {meta.get('year') if meta.get('year') is not None else 'null'}",
        f"backend: {meta['extraction']['backend']}",
        "---",
        "",
    ]
    current_section = None
    for b in blocks:
        if b.kind == "abstract":
            out += ["## Abstract", ""]
            current_section = "Abstract"
        elif b.kind in ("figure", "table"):
            if current_section != b.section:
                out += [f"## {b.section}", ""]
                current_section = b.section
            caption, *rows = [t for t, _ in b.paras]
            m = re.match(r"^((?:Fig\.|Figure|Table|TABLE)\s*[\dIVX]+[.:]?)\s*(.*)$", caption, re.S)
            out += [f"**{m.group(1)}** {m.group(2)}" if m else caption, ""]
            if rows:
                out += [f"    {r}" for r in rows] + [""]
            continue
        elif b.heading:
            if b.level == 1:
                out += [f"## {b.heading}", ""]
                current_section = b.section
            else:
                if current_section != b.section:
                    out += [f"## {b.section}", ""]
                    current_section = b.section
                out += [f"### {b.heading}", ""]
        for t, _ in b.paras:
            out += [t, ""]
    return "\n".join(out).rstrip() + "\n"
