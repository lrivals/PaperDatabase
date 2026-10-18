"""pdb table : tableaux d'un papier, leurs signaux de qualité et l'image de leur zone
(skill /table-review, docs/AMELIORATIONS.md §9 et lot E-e).

L'image est rendue depuis paper.pdf par PyMuPDF (`get_pixmap` sur la `bbox` de
sections.jsonl, lot E-a), pour comparer à l'œil les cellules extraites à la page.
"""
import json
from pathlib import Path

from lib import docling_tables, ligatures, tables

MARGIN = 10   # points autour de la zone du tableau
ZOOM = 2.5    # ~180 dpi : chiffres lisibles par un modèle multimodal


def _label(row):
    m = tables._LABEL.match(row["text"])
    return m.group(1) if m else row["text"][:30].split("\n")[0].strip()


def tables_of(folder, vocab=None):
    """Tableaux de sections.jsonl d'un papier : id, libellé, page, bbox, source, signaux."""
    folder = Path(folder)
    path = folder / "sections.jsonl"
    if not path.exists():
        return []
    cache, out = None, []
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if row["kind"] != "table":
            continue
        caption = None
        if (row.get("table_source") or "").startswith("docling"):
            cache = cache or docling_tables.load(folder) or {}
            caption = docling_tables.matched_caption(cache, row["text"])
        out.append({"id": row["id"], "label": _label(row), "page": row.get("page"),
                    "bbox": row.get("bbox"), "source": row.get("table_source"),
                    "signals": tables.quality(row["text"], vocab, caption), "text": row["text"]})
    return out


def find(items, query):
    """Tableau désigné par son libellé (« Table 3 », « III », « 3 »), ou par son id de section
    (complet ou suffixe « #025 »)."""
    q = query.strip()
    for t in items:
        if t["id"] == q or t["id"].endswith("#" + q.lstrip("#")):
            return t
    n = tables.label_number(q) if q.lower().startswith("table") else tables.number(q)
    for t in items:
        if t["label"].casefold() == q.casefold() or (n is not None and tables.label_number(t["label"]) == n):
            return t
    return None


def render_png(pdf, page, bbox, out, zoom=ZOOM, margin=MARGIN):
    """Image PNG de la zone bbox (points, origine en haut à gauche) de la page `page` (1 = première) ;
    page entière sans bbox. Renvoie le chemin écrit."""
    import pymupdf as fitz
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with fitz.open(pdf) as doc:
        p = doc[int(page) - 1]
        clip = None
        if bbox:
            x0, y0, x1, y1 = bbox
            clip = fitz.Rect(x0 - margin, y0 - margin, x1 + margin, y1 + margin) & p.rect
        p.get_pixmap(matrix=fitz.Matrix(zoom, zoom), clip=clip).save(str(out))
    return out


def corpus_vocabulary(root):
    return ligatures.corpus_vocabulary(Path(root))
