"""Tests du parsing TEI sur une sortie GROBID réelle (arXiv 2507.18174, GROBID 0.8.1).

.venv/bin/python -m unittest discover tests
"""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from lib import doc, ids, schema, tei  # noqa: E402

FIXTURE = ROOT / "tests" / "fixtures" / "sample.tei.xml"


class TestTei(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.header, cls.blocks, cls.refs = tei.parse(FIXTURE)

    def test_header(self):
        h = self.header
        self.assertEqual(h["title"], "Real-Time Object Detection and Classification using YOLO for Edge FPGAs")
        self.assertEqual([a["family"] for a in h["authors"]], ["Al Amin", "Obermaisser"])
        self.assertEqual(h["authors"][0]["given"], "Rashed")
        self.assertIsNone(h["year"])  # absente du PDF : jamais devinée
        self.assertTrue(h["abstract"].startswith("Object detection and classification"))

    def test_sections_order_and_hierarchy(self):
        secs = [b for b in self.blocks if b.kind == "section"]
        self.assertEqual(self.blocks[0].kind, "abstract")
        self.assertEqual(secs[0].section, "I. INTRODUCTION")
        sub = next(b for b in secs if b.subsection == "A. Dataset Preparation")
        self.assertEqual(sub.section, "III. IMPLEMENTATION")
        self.assertEqual(sub.level, 2)
        self.assertEqual(sub.page, 2)

    def test_figures_and_tables_kept(self):
        tables = [b for b in self.blocks if b.kind == "table"]
        self.assertEqual(len(tables), 1)
        self.assertTrue(tables[0].paras[0][0].startswith("TABLE I."))
        self.assertIn("Power (W) | 13.6", "\n".join(t for t, _ in tables[0].paras))
        self.assertTrue(any(b.kind == "figure" and "Fig. 2." in b.paras[0][0] for b in self.blocks))

    def test_refs(self):
        self.assertEqual(len(self.refs), 19)
        satay = self.refs[13]
        self.assertTrue(satay["title"].startswith("SATAY"))
        self.assertEqual(satay["year"], 2023)
        self.assertIn("Montgomerie-Corcoran", satay["raw"])

    def test_render(self):
        meta = schema.new_metadata("t")
        meta.update(title=self.header["title"])
        meta["extraction"]["backend"] = "grobid"
        md = doc.render_fulltext(meta, self.blocks)
        self.assertIn("\n## II. RELATED WORK\n", md)
        self.assertIn("\n### B. Model Training\n", md)
        self.assertIn("**TABLE I.**", md)
        self.assertNotIn("Microsoft COCO: Common objects", md)  # bibliographie hors du corps
        rows = doc.to_sections("t", self.blocks)
        self.assertEqual([r["order"] for r in rows], list(range(len(rows))))
        self.assertEqual(rows[0]["id"], "t#000")


class TestIds(unittest.TestCase):
    def test_header_cleaning(self):
        # en-tête FINN-R (arXiv 1809.04570, gabarit ACM) tel que GROBID 0.8.1 le produit
        authors = tei.clean_authors([
            {"given": "Thomas B", "family": "Preusser"},
            {"given": "Giulio", "family": tei._dehyphen("Gam- Bardella")},
            {"given": "Xilinx", "family": "Research"},
            {"given": "Thomas B", "family": "Preußer"},
            {"given": "Giulio", "family": "Gambardella"},
            {"given": "Miriam", "family": "Leeser"},
        ])
        self.assertEqual([a["family"] for a in authors], ["Preusser", "Gambardella", "Leeser"])
        self.assertIsNone(tei.clean_doi("10.1145/nnnnnnn.nnnnnnn"))
        self.assertIsNone(tei.clean_doi("not a doi"))
        self.assertEqual(tei.clean_doi("10.1145/3242897"), "10.1145/3242897")
        self.assertEqual(tei.clean_doi("10.1561/1000000005"), "10.1561/1000000005")
        self.assertEqual(tei.clean_arxiv("arXiv:1809.04570v1[cs.AR]"), "1809.04570")
        self.assertEqual(tei.clean_arxiv("arXiv:2507.18174"), "2507.18174")

    def test_find_arxiv_id(self):
        self.assertEqual(ids.find_arxiv_id("2507.18174"), "2507.18174")
        self.assertEqual(ids.find_arxiv_id("https://arxiv.org/abs/2507.18174v2"), "2507.18174")
        self.assertEqual(ids.find_arxiv_id("https://arxiv.org/pdf/2507.18174.pdf"), "2507.18174")
        self.assertEqual(ids.find_arxiv_id("arXiv:hep-th/9901001v1"), "hep-th/9901001")
        self.assertIsNone(ids.find_arxiv_id("https://ieeexplore.ieee.org/document/123"))

    def test_paper_id(self):
        pid, w = ids.make_paper_id({"arxiv_id": "2507.18174",
                                    "title": "Real-Time Object Detection and Classification using YOLO for Edge FPGAs"})
        self.assertEqual(pid, "arxiv-2507.18174-real-time-object-detection-classification")
        pid, w = ids.make_paper_id({"title": "Design of a YOLOv2 Accelerator on a Zynq-7000 FPGA",
                                    "year": 2025, "authors": [{"given": "J.", "family": "Kim"}]})
        self.assertEqual(pid, "2025-kim-design-yolov2-accelerator-zynq-7000")
        self.assertEqual(w, [])


class TestSchema(unittest.TestCase):
    def test_benchmark_row(self):
        row = {c: "n/r" for c in schema.BENCHMARK_COLUMNS}
        row["confidence"] = "high"
        self.assertEqual(schema.validate_benchmark_row(row), [])
        row["fps"] = "~30"
        self.assertTrue(schema.validate_benchmark_row(row))


if __name__ == "__main__":
    unittest.main()
