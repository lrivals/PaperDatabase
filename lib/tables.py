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
    return number(m.group(1).split()[-1]) if m else None


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
        recovered.append(label(b))
    return recovered, lost
