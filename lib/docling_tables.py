"""Second repli pour les tableaux sans corps : Docling (TableFormer), après lib/tables.py.

GROBID ne garde souvent que la légende d'un tableau ; le repli PyMuPDF (lib/tables.py) ne
lit que les tableaux à filets. Docling reconnaît la structure des tableaux sans filets, et,
avec l'OCR, ceux qui sont en image. Il est lent (25 à 100 s par papier sur CPU) et optionnel :
`.venv/bin/pip install -r requirements-docling.txt`.

Ses tableaux sont gardés dans papers/<id>/docling_tables.json (trace brute, comme
grobid.tei.xml) : une ré-extraction les relit sans relancer Docling. Un tableau reconstruit
est marqué dans sa légende (MARK) : erreurs connues de décalage de colonnes (essai du
26/09/2026, SETUP §9), chiffres à vérifier avant d'entrer dans benchmarks.csv.
"""
import importlib.util
import json
from pathlib import Path

from lib import tables

CACHE = "docling_tables.json"
MARK = "[corps du tableau reconstruit par Docling : à vérifier]"


def available():
    return importlib.util.find_spec("docling") is not None


def extract(pdf, ocr=False):
    """Tableaux du PDF : [{page, bbox (x0, y0, x1, y1, origine en haut à gauche), caption,
    rows}]. rows[0] est la ligne d'en-tête lue par Docling."""
    from docling.datamodel.base_models import InputFormat
    from docling.datamodel.pipeline_options import PdfPipelineOptions, TableFormerMode
    from docling.document_converter import DocumentConverter, PdfFormatOption

    opts = PdfPipelineOptions(do_ocr=ocr, do_table_structure=True)
    opts.table_structure_options.mode = TableFormerMode.ACCURATE
    conv = DocumentConverter(format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=opts)})
    doc = conv.convert(str(pdf)).document
    out = []
    for t in doc.tables:
        prov = t.prov[0] if t.prov else None
        bbox = None
        if prov:
            height = doc.pages[prov.page_no].size.height
            box = prov.bbox.to_top_left_origin(page_height=height)
            bbox = [round(box.l, 1), round(box.t, 1), round(box.r, 1), round(box.b, 1)]
        df = t.export_to_dataframe(doc=doc)
        rows = [[str(c) for c in df.columns]] + [[str(c) for c in r] for r in df.itertuples(index=False)]
        out.append({"page": prov.page_no if prov else None, "bbox": bbox,
                    "caption": t.caption_text(doc), "rows": rows})
    return out


def load(folder):
    """Cache d'un papier : {"ocr": bool, "tables": [...]} ou None."""
    path = Path(folder) / CACHE
    return json.loads(path.read_text()) if path.exists() else None


def save(folder, found, ocr):
    from importlib.metadata import version
    (Path(folder) / CACHE).write_text(json.dumps(
        {"docling": version("docling"), "ocr": ocr, "tables": found}, ensure_ascii=False, indent=1) + "\n")


def _clean(rows):
    """Lignes sans cellules vides en fin, en-têtes numériques générés (« 0, 1, 2 ») retirés."""
    rows = [[" ".join(c.split()) for c in r] for r in rows]
    if rows and all(c.isdigit() and int(c) == i for i, c in enumerate(rows[0])):
        rows = rows[1:]
    return [r for r in rows if any(r)]


def usable(rows):
    """Grille exploitable : ≥ 2 lignes, ≥ 2 colonnes, au moins la moitié des cellules remplies.
    Moins exigeant que tables.plausible, qui écarte la prose découpée en colonnes par
    PyMuPDF : Docling a déjà reconnu un tableau, et sa légende correspond. Les tableaux de
    synthèse textuels (surveys) et les grilles à coches passent donc. Une grille vide
    (0 × 0 : tableau en image, lu sans OCR) ne passe pas."""
    if len(rows) < 2 or max(len(r) for r in rows) < 2:
        return False
    cells = [c for r in rows for c in r]
    return sum(1 for c in cells if c) >= 0.5 * len(cells)


def recover(blocks, found):
    """Complète en place les tableaux encore sans corps avec ceux de Docling.

    Rapprochement : même numéro de légende (Table 3 = TABLE III), à une page près ; sinon,
    parmi les tableaux sans numéro de la même page, le seul, ou celui de même rang vertical
    quand la page compte autant de tableaux Docling sans numéro que de blocs vides sans
    correspondant. Les grilles inexploitables (usable) sont écartées. Retourne
    (reconstruits, perdus) : listes de libellés."""
    empty = [b for b in blocks if b.kind == "table" and tables.body_chars(b) < tables.MIN_BODY_CHARS]
    found = [{**t, "n": tables.label_number(t.get("caption")), "rows": _clean(t["rows"])} for t in found or []]
    used, recovered, lost = set(), [], []

    def page_of(b):
        return b.bbox[0] if b.bbox else b.page

    # blocs sans correspondant numéroté, par page : pour l'appariement par rang vertical
    def numbered(b):
        n = tables.label_number(b.paras[0][0] if b.paras else "")
        return n is not None and any(t["n"] == n for t in found)

    unmatched = {}
    for b in empty:
        if not numbered(b):
            unmatched.setdefault(page_of(b), []).append(b)
    for b in empty:
        n = tables.label_number(b.paras[0][0] if b.paras else "")
        page = page_of(b)
        pick = None
        if n is not None:
            same = [i for i, t in enumerate(found) if i not in used and t["n"] == n
                    and (page is None or t["page"] is None or abs(t["page"] - page) <= 1)]
            same.sort(key=lambda i: abs((found[i]["page"] or 0) - (page or 0)))
            pick = same[0] if same else None
        if pick is None and page is not None:
            alone = [i for i, t in enumerate(found) if t["n"] is None and t["page"] == page]
            peers = unmatched.get(page, [])
            if len(alone) == 1 and len(peers) == 1:
                pick = alone[0]
            elif len(alone) == len(peers) > 1 and b in peers:
                alone.sort(key=lambda i: found[i]["bbox"][1] if found[i]["bbox"] else 0)
                ranked = sorted(peers, key=lambda x: (x.bbox or (0, 0, 0))[2])
                pick = alone[ranked.index(b)]
            if pick in used:
                pick = None
        if pick is None or not usable(found[pick]["rows"]):
            lost.append(tables.label(b))
            continue
        used.add(pick)
        pg = b.paras[0][1]
        b.paras = [(f"{b.paras[0][0]} {MARK}", pg)] + [(" | ".join(r), pg) for r in found[pick]["rows"]]
        recovered.append(tables.label(b))
    return recovered, lost
