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


_ROMAN_HEADING = re.compile(r"^([IVX]+)\.\s")
_LETTER_HEADING = re.compile(r"^([A-Z])\.\s")
_ARABIC_HEADING = re.compile(r"^(\d+(?:\.\d+)*)\.?\s+\S")
_ROMAN_VALUES = {"I": 1, "V": 5, "X": 10}


def roman_to_int(s):
    total = 0
    for c, nxt in zip(s, s[1:] + " "):
        v = _ROMAN_VALUES[c]
        total += -v if nxt in _ROMAN_VALUES and _ROMAN_VALUES[nxt] > v else v
    return total


def is_junk_heading(title):
    """Titre parasite détecté par l'extracteur : cellule de tableau, symbole isolé, mesure.

    Règles volontairement conservatrices : un titre de paragraphe non numéroté mais lisible
    (« Layer fusion ») n'est jamais considéré comme parasite.
    """
    t = title.strip()
    if sum(c.isalpha() for c in t) < 3:          # « 𝑜 », « 4. »
        return True
    if not t[0].isalnum():                       # « * Corresponding author »
        return True
    if "|" in t:                                 # cellules de tableau : « 2021. | ViT Variants »
        return True
    m = re.match(r"^(\d+)\.", t)
    if m and int(m.group(1)) >= 100:             # une année, pas un numéro de section
        return True
    return bool(re.match(r"^\d+(\.\d+)?[a-zA-Z%×]", t))  # une mesure : « 13.9x larger »


def heading_level(title, n=None, section=None, subsection=None):
    """Niveau d'un titre d'après sa numérotation : 'III.' → 1, 'A.' → 2, '3.2' → 2.

    section et subsection sont les titres courants (subsection : dernier titre de niveau 2).
    - Un titre non numéroté vaut 1, sauf au sein d'un papier numéroté où il est traité comme
      sous-section (sauf mots de premier niveau : Conclusion, Acknowledgment…).
    - Dans un papier numéroté en chiffres romains, un titre en chiffres arabes (« 1. ») est
      un niveau sous la sous-section courante.
    - « I. », « V. », « X. » sont des lettres de sous-section quand ils suivent H, U ou W.
    """
    roman_paper = bool(section and _ROMAN_HEADING.match(section))
    m = _ROMAN_HEADING.match(title)
    prev = _LETTER_HEADING.match(subsection or "")
    if m and len(m.group(1)) == 1 and prev and ord(m.group(1)) == ord(prev.group(1)) + 1:
        return 2
    if n:
        level = len([p for p in n.strip(".").split(".") if p])
    elif m:
        return 1
    elif _LETTER_HEADING.match(title):
        return 2
    elif _ARABIC_HEADING.match(title):
        level = len(_ARABIC_HEADING.match(title).group(1).split("."))
    elif re.match(r"^\d+\)\s", title):
        return 2
    elif is_numbered(section) and not _TOP_LEVEL_WORDS.match(title):
        return 2
    else:
        return 1
    if roman_paper:
        return level + (2 if subsection else 1)
    return level


def is_numbered(title):
    return bool(title and re.match(r"^([IVX]+\.|\d+(\.\d+)*\.?)\s", title))


def numbering_gaps(blocks):
    """Numéros de sections de premier niveau absents de la séquence 1…max.

    Le style (romain ou arabe) est celui de la majorité des titres de premier niveau.
    Retourne les numéros manquants tels qu'ils seraient imprimés : ['1', '5'] ou ['I'].
    """
    roman, arabic = set(), set()
    for b in blocks:
        if b.kind != "section" or b.level != 1 or not b.heading:
            continue
        m = _ROMAN_HEADING.match(b.heading)
        if m:
            roman.add(m.group(1))
            continue
        m = re.match(r"^(\d+)\.?\s", b.heading)
        if m:
            arabic.add(int(m.group(1)))
    if len(roman) > len(arabic):
        seen = {roman_to_int(r): r for r in roman}
        labels = {v: k for k, v in _ROMAN_LABELS.items()}
        return [labels.get(k, str(k)) for k in range(1, max(seen) + 1) if k not in seen]
    if arabic:
        return [str(k) for k in range(1, max(arabic) + 1) if k not in arabic]
    return []


_ROMAN_LABELS = {r: roman_to_int(r) for r in (
    "I II III IV V VI VII VIII IX X XI XII XIII XIV XV XVI XVII XVIII XIX XX".split())}


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
                out += [f"{'#' * (min(b.level or 2, 3) + 1)} {b.heading}", ""]
        for t, _ in b.paras:
            out += [t, ""]
    return "\n".join(out).rstrip() + "\n"
