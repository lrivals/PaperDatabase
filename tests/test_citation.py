"""Tests de lib/citation.py et de son branchement dans bin/ingest.py (sans GROBID ni PDF).

.venv/bin/python -m unittest discover tests
"""
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from lib import citation, schema  # noqa: E402

_spec = importlib.util.spec_from_file_location("ingest", ROOT / "bin" / "ingest.py")
ingest = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ingest)

# Exports réels (24/09/2026), abstracts retirés.
IEEE_BIB = """@ARTICLE{10897979,
  author={Hozhabr, Seyed Hani and Giorgi, Roberto},
  journal={IEEE Access},
  title={A Survey on Real-Time Object Detection on FPGAs},
  year={2025},
  volume={13},
  number={},
  pages={38195-38238},
  doi={10.1109/ACCESS.2025.3544515}}
"""
MDPI_BIB = """
@Article{s23042208,
AUTHOR = {Zhai, Jiaqi and Li, Bin and Lv, Shunsen and Zhou, Qinglei},
TITLE = {FPGA-Based Vehicle Detection and Tracking Accelerator},
JOURNAL = {Sensors},
VOLUME = {23},
YEAR = {2023},
NUMBER = {4},
ARTICLE-NUMBER = {2208},
DOI = {10.3390/s23042208}
}
"""
ACM_BIB = """@article{10.1145/3744339,
author = {El Zeinaty, Christophe and Hamidouche, Wassim and Herrou, Glenn and Menard, Daniel},
title = {Designing Object Detection Models for TinyML: Foundations, Comparative Analysis, Challenges, and Emerging Solutions},
year = {2025},
volume = {58},
number = {2},
doi = {10.1145/3744339},
journal = {ACM Comput. Surv.},
articleno = {50},
}
"""
SPRINGER_RIS = """TY  - JOUR
AU  - Mittal, Payal
PY  - 2024
DA  - 2024/08/10
TI  - A comprehensive survey of deep learning-based lightweight object detection models for edge devices
JO  - Artificial Intelligence Review
SP  - 242
VL  - 57
IS  - 9
DO  - 10.1007/s10462-024-10877-1
ER  -
"""


class TestParse(unittest.TestCase):
    def test_ieee(self):
        (e,) = citation.parse_bibtex(IEEE_BIB)
        self.assertEqual(e["authors"][0], {"given": "Seyed Hani", "family": "Hozhabr"})
        self.assertEqual((e["year"], e["type"]), (2025, "journal"))
        self.assertEqual(e["venue"], "IEEE Access 13, 38195-38238")  # number vide ignoré
        self.assertEqual(e["doi"], "10.1109/ACCESS.2025.3544515")

    def test_mdpi_article_number(self):
        (e,) = citation.parse_bibtex(MDPI_BIB)
        self.assertEqual(e["venue"], "Sensors 23(4), 2208")
        self.assertEqual([a["family"] for a in e["authors"]], ["Zhai", "Li", "Lv", "Zhou"])

    def test_acm_compound_family_name(self):
        # cas El Zeinaty (24/09/2026) : GROBID avait pris « Rennes » pour premier auteur
        (e,) = citation.parse_bibtex(ACM_BIB)
        self.assertEqual(e["authors"][0], {"given": "Christophe", "family": "El Zeinaty"})
        self.assertEqual(e["venue"], "ACM Comput. Surv. 58(2), 50")

    def test_ris(self):
        (e,) = citation.parse_ris(SPRINGER_RIS)
        self.assertEqual(e["authors"], [{"given": "Payal", "family": "Mittal"}])
        self.assertEqual((e["year"], e["type"], e["doi"]), (2024, "journal", "10.1007/s10462-024-10877-1"))
        self.assertEqual(e["venue"], "Artificial Intelligence Review 57(9), 242")

    def test_latex_quotes_and_given_first(self):
        (e,) = citation.parse_bibtex('@inproceedings{k, author = "M{\\\'e}nard, Daniel and Jean {D}upont",'
                                     ' title = "Caf{\\\'e} {FPGA}", booktitle = {Proc. DATE}, year = 2024}')
        self.assertEqual(e["title"], "Café FPGA")
        self.assertEqual(e["authors"], [{"given": "Daniel", "family": "Ménard"},
                                        {"given": "Jean", "family": "Dupont"}])
        self.assertEqual((e["venue"], e["type"], e["year"]), ("Proc. DATE", "conference", 2024))


class TestFind(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.d = Path(self.tmp.name)
        (self.d / "articles_export_20260924.bib").write_text(MDPI_BIB + ACM_BIB)
        (self.d / "citation.ris").write_text(SPRINGER_RIS)
        (self.d / "notes.txt").write_text("@article{x, title={FPGA-Based Vehicle Detection}}")

    def tearDown(self):
        self.tmp.cleanup()

    def test_doi_case_insensitive(self):
        p, e = citation.find(self.d, doi="10.3390/S23042208")
        self.assertEqual((p.name, e["authors"][0]["family"]), ("articles_export_20260924.bib", "Zhai"))

    def test_title_when_no_doi(self):
        p, e = citation.find(self.d, title="A Comprehensive Survey of Deep Learning Based Lightweight "
                                           "Object Detection Models for Edge Devices")
        self.assertEqual(p.name, "citation.ris")

    def test_no_match(self):
        self.assertIsNone(citation.find(self.d, doi="10.1/none", title="FPGA-Based Vehicle"))


class TestIngest(unittest.TestCase):
    def test_citation_beats_grobid_header(self):
        warnings = []
        header = {"title": "Designing Object Detection Models for TinyML", "authors": [
            {"given": "Insa", "family": "Rennes"}], "year": None, "doi": None}
        meta = ingest.merge_metadata(None, header, "grobid", warnings)
        self.assertIn("type de publication à préciser", warnings)
        (cit,) = citation.parse_bibtex(ACM_BIB)
        ingest.apply_citation(meta, cit, warnings)
        self.assertEqual((meta["year"], meta["type"]), (2025, "journal"))
        self.assertEqual(meta["authors"][0]["family"], "El Zeinaty")
        self.assertEqual(meta["url"], "https://doi.org/10.1145/3744339")
        self.assertNotIn("type de publication à préciser", warnings)

    def test_pymupdf_warning_dropped(self):
        warnings = []
        meta = ingest.merge_metadata(None, {}, "pymupdf", warnings)
        self.assertIn(schema.WARN_MANUAL_METADATA, warnings)
        ingest.apply_citation(meta, citation.parse_ris(SPRINGER_RIS)[0], warnings)
        self.assertNotIn(schema.WARN_MANUAL_METADATA, warnings)

    def test_store_moves_single_copies_grouped(self):
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            out = t / "paper"; out.mkdir()
            single, grouped = t / "a.ris", t / "b.bib"
            single.write_text(SPRINGER_RIS)
            grouped.write_text(MDPI_BIB + ACM_BIB)
            ingest.store_citation(single, out)
            self.assertFalse(single.exists())
            self.assertTrue((out / "citation.ris").exists())
            ingest.store_citation(grouped, out)
            self.assertTrue(grouped.exists())  # sert encore à l'autre PDF
            self.assertTrue((out / "citation.bib").exists())


if __name__ == "__main__":
    unittest.main()
