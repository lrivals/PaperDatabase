"""Tests de lib/tables.py (tableaux dont GROBID n'a gardé que la légende).

PDF synthétique produit par PyMuPDF : une légende, puis un tableau à filets.

.venv/bin/python -m unittest discover tests
"""
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import pymupdf  # noqa: E402

from lib import tables  # noqa: E402
from lib.doc import Block  # noqa: E402

CAPTION = (50, 100, 300, 108)   # zone de la légende, comme GROBID la localise
ROWS = [["Model", "FPS", "Power (W)"], ["YOLOv3-tiny", "55", "2.13"], ["YOLOv5n", "31", "4.8"]]


def make_pdf(path, with_table=True):
    doc = pymupdf.open()
    page = doc.new_page(width=595, height=842)
    page.insert_text((50, 106), "Table 2. Results on the board.", fontsize=8)
    if with_table:
        x0, y0, w, h = 50, 115, 80, 18
        for i, row in enumerate(ROWS):
            for j, cell in enumerate(row):
                r = pymupdf.Rect(x0 + j * w, y0 + i * h, x0 + (j + 1) * w, y0 + (i + 1) * h)
                page.draw_rect(r, color=(0, 0, 0), width=0.8)
                page.insert_text((r.x0 + 3, r.y1 - 5), cell, fontsize=7)
    doc.save(path)


def table_block(bbox=(1, *CAPTION), rows=()):
    paras = [("Table 2. Results on the board.", 1)] + [(r, 1) for r in rows]
    return Block("table", "Figures et tableaux", None, 1, paras, page=1, bbox=bbox)


class RecoverTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.pdf = Path(self.tmp.name) / "p.pdf"

    def tearDown(self):
        self.tmp.cleanup()

    def test_empty_table_is_rebuilt_below_caption(self):
        make_pdf(self.pdf)
        b = table_block()
        recovered, lost = tables.recover(self.pdf, [b])
        self.assertEqual((recovered, lost), (["Table 2"], []))
        self.assertIn(tables.RECOVERED_MARK, b.paras[0][0])
        body = [t for t, _ in b.paras[1:]]
        self.assertEqual(body[0], "Model | FPS | Power (W)")
        self.assertEqual(body[1], "YOLOv3-tiny | 55 | 2.13")

    def test_no_table_on_page_is_reported_lost(self):
        make_pdf(self.pdf, with_table=False)
        b = table_block()
        self.assertEqual(tables.recover(self.pdf, [b]), ([], ["Table 2"]))
        self.assertEqual(len(b.paras), 1)

    def test_table_in_other_column_is_ignored(self):
        make_pdf(self.pdf)
        b = table_block(bbox=(1, 330, 100, 560, 108))   # légende dans la colonne de droite
        self.assertEqual(tables.recover(self.pdf, [b]), ([], ["Table 2"]))

    def test_tei_body_long_enough_is_untouched(self):
        make_pdf(self.pdf)
        rows = ["a | b | c " * 10] * 2
        b = table_block(rows=rows)
        self.assertEqual(tables.recover(self.pdf, [b]), ([], []))
        self.assertEqual([t for t, _ in b.paras[1:]], rows)

    def test_missing_pdf_leaves_blocks_unchanged(self):
        b = table_block()
        self.assertEqual(tables.recover(self.pdf, [b]), ([], ["Table 2"]))


class PlausibleTest(unittest.TestCase):
    def test_numeric_grid(self):
        self.assertTrue(tables.plausible(ROWS))

    def test_prose_cut_into_columns(self):
        prose = [["introducing 2- bit quan", "tization of the activations instead of", "the weights"],
                 ["which reduces the memo", "ry footprint of the model by", "a factor of four"]]
        self.assertFalse(tables.plausible(prose))

    def test_single_letters(self):
        self.assertFalse(tables.plausible([["L", "L"], ["N", "1"], ["V", "L"]]))


if __name__ == "__main__":
    unittest.main()
