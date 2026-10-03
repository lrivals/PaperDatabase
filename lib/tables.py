"""Tableaux dont GROBID n'a gardé que la légende : reconstruction par PyMuPDF.

GROBID localise souvent la légende d'un tableau sans en extraire le corps (coords de 6 à
9 pt de haut). On cherche alors, sur la même page, un tableau à filets détecté par
`page.find_tables()` (stratégie par défaut, sur les traits), collé à la légende (au-dessus
ou au-dessous) et dans la même colonne. La stratégie « text » est exclue : sur ce corpus
elle découpe la prose voisine en colonnes (essai du 26/09/2026, 0 tableau exploitable sur 44).

Un tableau reconstruit est marqué dans sa légende (RECOVERED_MARK) : ses chiffres sont à
vérifier avant d'entrer dans benchmarks.csv. Les tableaux restés sans corps sont renvoyés
pour être signalés dans extraction.warnings.
"""
import re
from collections import Counter

MIN_BODY_CHARS = 150    # sous ce seuil, le corps TEI d'un tableau est considéré comme perdu
MAX_GAP = 40            # écart vertical maximal légende ↔ tableau, en points
MIN_OVERLAP = 0.5       # recouvrement horizontal minimal, rapporté à la plus étroite des deux
RECOVERED_MARK = "[corps du tableau reconstruit par PyMuPDF : à vérifier]"

_LABEL = re.compile(r"(?i)^\s*(table\s*[A-Z]?[\dIVXL]+)")


def label(block):
    """« Table 3 », « TABLE IV » ; sinon le début de la légende."""
    caption = block.paras[0][0] if block.paras else ""
    m = _LABEL.match(caption)
    return m.group(1) if m else (caption[:30].strip() or f"tableau p. {block.page}")


_ROMAN = {"I": 1, "V": 5, "X": 10, "L": 50}


def number(s):
    """Numéro d'un tableau : « 3 » → 3, « IV » → 4, « A2 » → 2 ; None sinon."""
    m = re.fullmatch(r"[A-Z]?(\d+)|([IVXL]+)", (s or "").strip().upper())
    if not m:
        return None
    if m.group(1):
        return int(m.group(1))
    vals = [_ROMAN[c] for c in m.group(2)]
    return sum(-v if i + 1 < len(vals) and v < vals[i + 1] else v for i, v in enumerate(vals))


def label_number(text):
    """Numéro du tableau d'après le début d'une légende (« TABLE III. … » → 3)."""
    m = _LABEL.match(text or "")
    return number(re.sub(r"(?i)^\s*table\s*", "", m.group(1))) if m else None


def body_chars(block):
    return sum(len(t) for t, _ in block.paras[1:])


def _rows(table):
    rows = []
    for row in table.extract():
        cells = [re.sub(r"\s+", " ", c or "").strip() for c in row]
        if any(cells):
            rows.append(cells)
    return rows


def plausible(rows):
    """Grille de données plutôt que prose : ≥ 2 lignes et 2 colonnes, cellules surtout
    remplies, courtes, pas réduites à une lettre, ≥ 20 % de cellules chiffrées et ≤ 30 %
    de cellules de 4 mots ou plus (la prose découpée en colonnes en a presque partout)."""
    if len(rows) < 2 or max(len(r) for r in rows) < 2:
        return False
    cells = [c for r in rows for c in r]
    filled = [c for c in cells if c]
    if len(filled) < 0.5 * len(cells):
        return False
    mean = sum(len(c) for c in filled) / len(filled)
    digits = sum(1 for c in filled if any(ch.isdigit() for ch in c))
    wordy = sum(1 for c in filled if len(c.split()) >= 4)
    return 2 <= mean <= 40 and digits >= 0.2 * len(filled) and wordy <= 0.3 * len(filled)


def _near(bbox, tb):
    """Écart vertical entre la légende et le tableau, None s'ils ne sont pas alignés."""
    _, x0, y0, x1, y1 = bbox
    overlap = min(x1, tb[2]) - max(x0, tb[0])
    narrow = min(x1 - x0, tb[2] - tb[0])
    if narrow <= 0 or overlap < MIN_OVERLAP * narrow:
        return None
    if tb[1] >= y1 - 2:        # tableau sous la légende
        gap = tb[1] - y1
    elif tb[3] <= y0 + 2:      # tableau au-dessus
        gap = y0 - tb[3]
    else:                      # zones qui se chevauchent
        gap = 0
    return gap if gap <= MAX_GAP else None


def recover(pdf_path, blocks):
    """Complète en place les tableaux sans corps. Retourne (reconstruits, perdus) : listes
    de libellés. Sans PDF lisible, rien n'est modifié et tout tableau vide est « perdu »."""
    empty = [b for b in blocks if b.kind == "table" and body_chars(b) < MIN_BODY_CHARS]
    if not empty:
        return [], []
    try:
        import pymupdf
        pdf = pymupdf.open(pdf_path)
    except Exception:
        return [], [label(b) for b in empty]

    found, used, recovered, lost = {}, set(), [], []
    for b in empty:
        best = None
        if b.bbox and 1 <= b.bbox[0] <= len(pdf):
            page = b.bbox[0]
            if page not in found:
                try:
                    found[page] = pdf[page - 1].find_tables().tables
                except Exception:
                    found[page] = []
            for i, t in enumerate(found[page]):
                gap = _near(b.bbox, t.bbox)
                if gap is None or (page, i) in used:
                    continue
                rows = _rows(t)
                if plausible(rows) and (best is None or gap < best[0]):
                    best = (gap, (page, i), rows)
        if best is None:
            lost.append(label(b))
            continue
        _, key, rows = best
        used.add(key)
        page = b.paras[0][1]
        b.paras = [(f"{b.paras[0][0]} {RECOVERED_MARK}", page)] + \
                  [(" | ".join(r), page) for r in rows]
        b.zone, b.table_source = (key[0], *found[key[0]][key[1]].bbox), "pymupdf"
        recovered.append(label(b))
    return recovered, lost


# ------------------------------------------------- qualité d'un tableau (lot E-d)

QUALITY_SIGNALS = {
    "empty_cells": "plus de 30 % de cellules vides",
    "ragged": "nombre de cellules variable d'une rangée à l'autre",
    "no_header": "1re rangée surtout numérique",
    "ocr_suspect": "mots illisibles (OCR, lettres perdues) ou O / l pris pour 0 / 1",
    "merged_numbers": "plusieurs nombres dans une même cellule (colonnes fusionnées)",
    "lost_columns": "une seule colonne de valeurs, de moyenne ou de total (colonnes perdues ?)",
    "caption_mismatch": "corps Docling rattaché par la page, pas par le numéro de légende",
}
EMPTY_SHARE = 0.3     # empty_cells : part de cellules vides au-delà de laquelle on signale
RAGGED_SHARE = 0.2    # ragged : part des rangées de corps hors du nombre de cellules le plus courant
GIBBERISH_MIN = 3     # ocr_suspect : mots illisibles distincts à partir desquels on signale

_NUM = re.compile(r"[-+±~∼≈<>]?\d[\d,]*(\.\d+)?[kKMGT%x×]?")
_AGGREGATE = re.compile(r"(?i)(average|avg\.?|mean|total|overall)")
_OCR_DIGIT = re.compile(r"(?<![A-Za-z])(\d+[OolI]\d*|[OolI]\d+)(?![A-Za-z])")
_VOWELS = set("aeiouy")


def _is_num(cell):
    return bool(_NUM.fullmatch(cell.replace(" ", "")))


def _gibberish(word):
    """Mot illisible : presque sans voyelles ou presque que des voyelles, ou 5 consonnes de
    suite (« arcths », « aoees ») ; aussi les mots amputés de leur 1re lettre (« bject »)."""
    share = sum(c in _VOWELS for c in word) / len(word)
    return share <= 0.2 or share >= 0.7 or re.search(r"[^aeiouy]{5}", word) is not None


def quality(text, vocab=None, docling_caption=None):
    """Signaux de QUALITY_SIGNALS levés par un tableau de sections.jsonl (légende, puis une
    rangée par paragraphe, cellules séparées par « | »). Liste vide : rien à signaler.

    vocab : mots connus du corpus (ligatures.corpus_vocabulary), pour ocr_suspect ; sans
    lui, seule la confusion O / l avec 0 / 1 est cherchée. docling_caption : légende du
    tableau Docling qui a fourni le corps (docling_tables.matched_caption), None sinon."""
    paras = [p for p in text.split("\n\n") if p.strip()]
    rows = [[c.strip() for c in p.split("|")] for p in paras[1:]]
    out = []
    if docling_caption is not None:
        mine, theirs = label_number(paras[0] if paras else ""), label_number(docling_caption)
        if (mine != theirs or mine is None) and docling_caption[:30] != (paras[0] if paras else "")[:30]:
            out.append("caption_mismatch")
    if len(rows) < 2:
        return out
    cells = [c for r in rows for c in r]
    if sum(1 for c in cells if not c) > EMPTY_SHARE * len(cells):
        out.append("empty_cells")
    n_head = 2 if len(rows) > 2 and units_row(rows[1]) else 1
    body = rows[n_head:]
    if body:
        counts = Counter(len(r) for r in body)
        usual = counts.most_common(1)[0][0]
        if sum(n for k, n in counts.items() if k != usual) > RAGGED_SHARE * len(body):
            out.append("ragged")
    head = [c for c in rows[0] if c]
    if head and sum(_is_num(c) for c in head) > 0.5 * len(head):
        out.append("no_header")
    words = re.findall(r"[a-z]+", " ".join(cells))
    unreadable = {w for w in words if len(w) >= 4 and w not in vocab and _gibberish(w)} if vocab else set()
    if len(unreadable) >= GIBBERISH_MIN or _OCR_DIGIT.search(" ".join(cells)):
        out.append("ocr_suspect")
    if any(sum(_is_num(t) for t in c.split()) >= 2 and all(_is_num(t) or t in "kKMG" for t in c.split())
           for c in cells):
        out.append("merged_numbers")
    values = [c for c in rows[0][1:] if c]
    if len(values) == 1 and _AGGREGATE.fullmatch(values[0]):
        out.append("lost_columns")
    return out


def units_row(cells):
    """Rangée d'unités sous l'en-tête : cellules non vides toutes entre parenthèses ou crochets."""
    cells = [c for c in cells if c]
    return bool(cells) and all(c[0] in "([" and c[-1] in ")]" for c in cells)
