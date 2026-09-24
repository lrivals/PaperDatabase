"""Fichiers de citation éditeur (.bib, .ris) déposés dans inbox/ à côté d'un PDF.

L'export de citation d'un éditeur (IEEE Xplore, ACM DL, MDPI, Springer) est plus fiable que
l'en-tête lu par GROBID sur un PDF sans arXiv : premier auteur, année et venue y sont
exacts. ingest.py apparie chaque PDF à un fichier de citation d'inbox/ par DOI, sinon par
titre (le nom du fichier n'a en général aucun rapport avec celui du PDF), et ses champs
priment alors sur le teiHeader. Aucune dépendance externe.
"""
import difflib
import re
import unicodedata
from pathlib import Path

EXTENSIONS = (".bib", ".ris")
TITLE_RATIO = 0.9  # seuil d'appariement par titre (SequenceMatcher, titres normalisés)

BIB_TYPES = {"article": "journal", "inproceedings": "conference", "conference": "conference",
             "phdthesis": "thesis", "mastersthesis": "thesis"}
RIS_TYPES = {"JOUR": "journal", "JFULL": "journal", "EJOUR": "journal", "MGZN": "journal",
             "CONF": "conference", "CPAPER": "conference", "THES": "thesis"}
# Accents LaTeX les plus courants : {\'e}, \'{e}, \'e…
_ACCENTS = {"'": "\u0301", "`": "\u0300", "^": "\u0302", '"': "\u0308", "~": "\u0303", "c": "\u0327"}


def _delatex(s):
    s = re.sub(r"\\([`'^\"~c])\s*\{?\s*([A-Za-z])\}?",
               lambda m: unicodedata.normalize("NFC", m.group(2) + _ACCENTS[m.group(1)]), s)
    s = re.sub(r"\\&", "&", s)
    s = s.replace("{", "").replace("}", "").replace("--", "-")
    return re.sub(r"\s+", " ", s).strip()


def _person(name):
    """« Nom, Prénom » ou « Prénom Nom » → {given, family}."""
    name = _delatex(name)
    if "," in name:
        family, given = (p.strip() for p in name.split(",", 1))
    else:
        parts = name.split()
        family, given = (parts[-1], " ".join(parts[:-1])) if len(parts) > 1 else (name, "")
    return {"given": given or None, "family": family}


def _venue(journal, volume=None, number=None, pages=None):
    """« Sensors 23(4), 2208 » : venue lisible, sans rien deviner."""
    if not journal:
        return None
    v = journal
    if volume:
        v += f" {volume}" + (f"({number})" if number else "")
    if pages:
        v += ("," if volume else "") + f" {pages}"
    return v


def _bib_fields(body):
    """Champs d'une entrée BibTeX (valeurs entre accolades imbriquées ou guillemets)."""
    fields, i = {}, 0
    while True:
        m = re.compile(r"\s*,?\s*([A-Za-z][\w-]*)\s*=\s*").match(body, i)
        if not m:
            break
        key, i = m.group(1).lower(), m.end()
        if i < len(body) and body[i] in "{\"":
            quoted, depth, j = body[i] == "\"", 0, i + 1
            while j < len(body):  # fin : accolade fermante de niveau 0, ou guillemet hors accolades
                c = body[j]
                if c == "{":
                    depth += 1
                elif c == "}":
                    if depth == 0 and not quoted:
                        break
                    depth -= 1
                elif c == "\"" and quoted and depth == 0:
                    break
                j += 1
            fields[key], i = body[i + 1:j], j + 1
        else:
            m2 = re.compile(r"[^,}\s]+").match(body, i)
            if not m2:
                break
            fields[key], i = m2.group(0), m2.end()
    return fields


def parse_bibtex(text):
    """Liste des entrées d'un .bib, au format de metadata.json (champs connus seulement)."""
    out = []
    for m in re.finditer(r"@(\w+)\s*\{\s*[^,]*,", text):
        etype = m.group(1).lower()
        if etype in ("comment", "string", "preamble"):
            continue
        start, depth, j = m.end(), 1, m.end()
        while j < len(text) and depth:
            depth += {"{": 1, "}": -1}.get(text[j], 0)
            j += 1
        f = {k: _delatex(v) for k, v in _bib_fields(text[start:j - 1]).items()}
        year = re.search(r"\d{4}", f.get("year", ""))
        out.append({
            "title": f.get("title") or None,
            "authors": [_person(a) for a in re.split(r"\s+and\s+", f["author"])] if f.get("author") else [],
            "year": int(year.group(0)) if year else None,
            "venue": _venue(f.get("journal") or f.get("booktitle"), f.get("volume"), f.get("number"),
                            f.get("pages") or f.get("article-number") or f.get("articleno")),
            "doi": _doi(f.get("doi")),
            "type": BIB_TYPES.get(etype),
        })
    return out


def parse_ris(text):
    out, cur = [], None
    for line in text.splitlines():
        m = re.match(r"^([A-Z][A-Z0-9])  -\s?(.*)$", line)
        if not m:
            continue
        tag, val = m.group(1), m.group(2).strip()
        if tag == "TY":
            cur = {"TY": val}
        elif cur is None:
            continue
        elif tag == "ER":
            out.append(_ris_entry(cur))
            cur = None
        else:
            cur.setdefault(tag, []).append(val)
    return out


def _ris_entry(r):
    first = lambda *tags: next((r[t][0] for t in tags if r.get(t)), None)  # noqa: E731
    year = re.search(r"\d{4}", first("PY", "Y1", "DA") or "")
    sp, ep = first("SP"), first("EP")
    return {
        "title": first("TI", "T1"),
        "authors": [_person(a) for a in r.get("AU", []) + r.get("A1", [])],
        "year": int(year.group(0)) if year else None,
        "venue": _venue(first("JO", "T2", "JF", "BT"), first("VL"), first("IS"),
                        f"{sp}-{ep}" if sp and ep else sp),
        "doi": _doi(first("DO")),
        "type": RIS_TYPES.get(r["TY"]),
    }


def _doi(s):
    if not s:
        return None
    s = re.sub(r"^(https?://(dx\.)?doi\.org/|doi:)", "", s.strip(), flags=re.IGNORECASE)
    return s or None


def parse(path):
    path = Path(path)
    text = path.read_text(encoding="utf-8", errors="replace")
    return parse_ris(text) if path.suffix.lower() == ".ris" else parse_bibtex(text)


def _norm_title(t):
    return re.sub(r"[^a-z0-9]+", " ", (t or "").lower()).strip()


def find(directory, doi=None, title=None):
    """(chemin, entrée) du fichier de citation de `directory` qui correspond au PDF, ou None.

    DOI identique d'abord, sinon titre quasi identique (≥ TITLE_RATIO). Un fichier à
    plusieurs entrées n'est retenu que pour l'entrée qui correspond.
    """
    best = None
    for p in sorted(Path(directory).iterdir()):
        if p.suffix.lower() not in EXTENSIONS or not p.is_file():
            continue
        for e in parse(p):
            if doi and e["doi"] and e["doi"].lower() == doi.lower():
                return p, e
            if title and e["title"]:
                ratio = difflib.SequenceMatcher(None, _norm_title(title), _norm_title(e["title"])).ratio()
                if ratio >= TITLE_RATIO and (best is None or ratio > best[0]):
                    best = (ratio, p, e)
    return best[1:] if best else None
