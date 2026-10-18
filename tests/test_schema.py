"""Tests des validateurs de DATA_MODEL.md (§1, §5, §6, §8) et de la hiérarchie des titres (§4).

.venv/bin/python -m unittest discover tests
"""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from lib import doc, schema  # noqa: E402
from lib.doc import Block  # noqa: E402

PID = "arxiv-2507.18174-yolo-edge-fpga"


def section_row(order=0, **kw):
    row = {"id": f"{PID}#{order:03d}", "paper_id": PID, "kind": "section",
           "section": "3. Experimental Results", "subsection": None, "order": order,
           "page": 7, "text": "..."}
    row.update(kw)
    return row


def ref_row(**kw):
    row = {"paper_id": PID, "raw": "[12] J. Redmon and A. Farhadi, ...",
           "title": "YOLOv3: An Incremental Improvement", "authors": ["Redmon", "Farhadi"],
           "year": 2018, "doi": None, "arxiv_id": "1804.02767"}
    row.update(kw)
    return row


class TestPaperId(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(schema.validate_paper_id(PID, {"arxiv_id": "2507.18174"}), [])
        self.assertEqual(schema.validate_paper_id("2025-kim-yolov2-zynq7000", {"arxiv_id": None}), [])
        self.assertEqual(schema.validate_paper_id("unknown-unknown-some-title", {"arxiv_id": None}), [])
        self.assertEqual(schema.validate_paper_id("arxiv-cs_0101001-old-paper", {"arxiv_id": "cs/0101001"}), [])

    def test_invalid(self):
        self.assertTrue(schema.validate_paper_id(PID, {"arxiv_id": "2507.99999"}))
        self.assertTrue(schema.validate_paper_id(PID, {"arxiv_id": None}))
        self.assertTrue(schema.validate_paper_id("Kim_YOLOv2", {"arxiv_id": None}))
        self.assertTrue(schema.validate_paper_id("2025-kim-Yolo-Zynq", {"arxiv_id": None}))


def bench_row(**kw):
    row = {c: "n/r" for c in schema.BENCHMARK_COLUMNS}
    row.update(paper_id=PID, model="YOLOv8n", confidence="high", source_section="Table 2")
    row.update(kw)
    return row


class TestBenchmarkColumns(unittest.TestCase):
    def test_header(self):
        cols = list(schema.BENCHMARK_COLUMNS)
        self.assertEqual(schema.check_header(cols), [])
        self.assertEqual(schema.check_header(cols + ["batch", "chunk_id"]), [])  # sous-ensemble, tout ordre
        self.assertEqual(schema.check_header(list(schema.ALL_COLUMNS)), [])
        self.assertTrue(schema.check_header(cols[1:] + cols[:1]))                # ordre des obligatoires
        self.assertTrue(schema.check_header(cols[:-1]))                          # obligatoire manquante
        self.assertTrue(schema.check_header(cols + ["notes"]))                   # colonne inconnue
        self.assertTrue(schema.check_header(cols + ["batch", "batch"]))          # doublon
        self.assertTrue(schema.check_header(None))

    def test_optional_values(self):
        self.assertEqual(schema.validate_benchmark_row(bench_row()), [])
        ok = bench_row(chunk_id=f"{PID}#041.0", batch="1", input_res="416x416", metric_def="n/r")
        self.assertEqual(schema.validate_benchmark_row(ok), [])
        self.assertEqual(schema.validate_benchmark_row(bench_row(chunk_id="2507.18174#041")), [])
        self.assertTrue(schema.validate_benchmark_row(bench_row(input_res="")))  # présente : n/r, pas vide
        self.assertTrue(schema.validate_benchmark_row(bench_row(batch="1.5")))
        self.assertEqual(schema.validate_benchmark_row(bench_row(platform_class="server")), [])
        self.assertTrue(schema.validate_benchmark_row(bench_row(platform_class="cloud")))
        self.assertTrue(schema.validate_benchmark_row(bench_row(chunk_id="Table 2")))
        self.assertTrue(schema.validate_benchmark_row(bench_row(chunk_id=f"{PID}#a.0")))


class TestSectionRow(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(schema.validate_section_row(section_row(12), PID, 12), [])
        self.assertEqual(schema.validate_section_row(section_row(page=None), PID, 0), [])

    def test_invalid(self):
        row = section_row()
        del row["page"]
        self.assertTrue(schema.validate_section_row(row, PID, 0))
        self.assertTrue(schema.validate_section_row(section_row(1), PID, 0))  # order décalé
        self.assertTrue(schema.validate_section_row(section_row(id=f"{PID}#12"), PID, 0))
        self.assertTrue(schema.validate_section_row(section_row(kind="caption"), PID, 0))
        self.assertTrue(schema.validate_section_row(section_row(subsection=""), PID, 0))
        self.assertTrue(schema.validate_section_row(section_row(page=0), PID, 0))
        self.assertTrue(schema.validate_section_row(section_row(text="  "), PID, 0))

    def test_table_fields(self):
        ok = section_row(kind="table", bbox=[50.0, 110, 300, 200.5], table_source="docling-ocr")
        self.assertEqual(schema.validate_section_row(ok, PID, 0), [])
        self.assertEqual(schema.validate_section_row(section_row(kind="table", table_source="grobid"), PID, 0), [])
        self.assertTrue(schema.validate_section_row(section_row(bbox=[0, 0, 1, 1]), PID, 0))   # kind section
        self.assertTrue(schema.validate_section_row(section_row(kind="table", table_source="ocr"), PID, 0))
        for bad in ([50, 110, 300], [300, 110, 50, 200], [50, 110, 300, "200"], None):
            self.assertTrue(schema.validate_section_row(section_row(kind="table", bbox=bad), PID, 0))
        self.assertTrue(schema.validate_section_row(section_row(kind="table", quality={}), PID, 0))


class TestRefRow(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(schema.validate_ref_row(ref_row(), PID), [])

    def test_invalid(self):
        row = ref_row()
        del row["raw"]
        self.assertTrue(schema.validate_ref_row(row, PID))
        self.assertTrue(schema.validate_ref_row(ref_row(doi=""), PID))
        self.assertTrue(schema.validate_ref_row(ref_row(year="2018"), PID))
        self.assertTrue(schema.validate_ref_row(ref_row(paper_id="autre"), PID))


class TestFrontMatter(unittest.TestCase):
    def test_read(self):
        text = '---\nid: x\ntitle: "A \\"quoted\\" title: yes"\nyear: null\ndate:\n---\n\n# body\n'
        self.assertEqual(schema.read_front_matter(text),
                         {"id": "x", "title": 'A "quoted" title: yes', "year": None, "date": None})

    def test_absent_or_unclosed(self):
        self.assertEqual(schema.read_front_matter("# titre\n"), {})
        self.assertEqual(schema.read_front_matter("---\nid: x\n"), {})

    def test_fiche_template(self):
        meta = {"id": PID, "title": "T", "authors": [], "year": 2025, "venue": None,
                "doi": None, "url": None, "type": "preprint"}
        text = schema.render_fiche(meta)
        self.assertEqual(schema.read_front_matter(text)["fiche"], "todo")
        self.assertIn("\n## Statut de lecture", text)


class TestHeadings(unittest.TestCase):
    def test_levels(self):
        self.assertEqual(doc.heading_level("II. RELATED WORK"), 1)
        self.assertEqual(doc.heading_level("3.2 Training"), 2)
        self.assertEqual(doc.heading_level("3.2. Training", "3.2"), 2)
        # chiffres arabes dans un papier en chiffres romains : sous la sous-section courante
        self.assertEqual(doc.heading_level("1. Spatial Dataflow", "1.", section="IV. FPGA",
                                           subsection="B. Optimization"), 3)
        self.assertEqual(doc.heading_level("1. Spatial Dataflow", "1.", section="IV. FPGA"), 2)
        # I. après H. : la lettre I, pas la section I
        self.assertEqual(doc.heading_level("I. Comparison", section="VII. EVALUATION",
                                           subsection="H. End-to-End"), 2)
        self.assertEqual(doc.heading_level("II. RELATED WORK", section="I. INTRODUCTION",
                                           subsection="H. End-to-End"), 1)
        self.assertEqual(doc.heading_level("Layer fusion", section="IV. FPGA"), 2)
        self.assertEqual(doc.heading_level("Conclusion", section="IV. FPGA"), 1)

    def test_junk(self):
        for t in ("2021. | ViT Variants", "2017.6. | Transformer [90]", "𝑜", "4.",
                  "13.9x larger", "* Corresponding author"):
            self.assertTrue(doc.is_junk_heading(t), t)
        for t in ("Layer fusion", "3.2 Training", "IV. FPGA-BASED CNN IMPLEMENTATION",
                  "A. Deployment", "12. Related work"):
            self.assertFalse(doc.is_junk_heading(t), t)

    def test_numbering_gaps(self):
        def sec(h, level=1):
            return Block("section", h, None, level, [("x", 1)], heading=h)
        blocks = [Block("abstract", "Abstract", None, 1, [("x", 1)]),
                  sec("2. Background"), sec("2.1. Sub", 2), sec("4. Results"), sec("Conclusion")]
        self.assertEqual(doc.numbering_gaps(blocks), ["1", "3"])
        roman = [sec("II. RELATED WORK"), sec("III. METHOD"), sec("V. RESULTS")]
        self.assertEqual(doc.numbering_gaps(roman), ["I", "IV"])
        self.assertEqual(doc.numbering_gaps([sec("Introduction")]), [])

    def test_roman_to_int(self):
        self.assertEqual([doc.roman_to_int(r) for r in ("I", "IV", "IX", "XIV")], [1, 4, 9, 14])


def claim_row(**kw):
    row = {"claim_id": f"{PID}!c07", "kind": "résultat",
           "text": "Le détecteur atteint 45 FPS sur ZCU104.", "voice": "auteurs",
           "source_chunk": f"{PID}#017.0", "excerpt": "reaches 45 FPS on the ZCU104",
           "conditions": {"dataset": "COCO", "batch": "1", "power_scope": "board"},
           "benchmark_row": 2, "caveats": ["mAP mesurée en flottant"], "chunk_sha1": "0123abcd"}
    row.update(kw)
    return row


class TestClaimRow(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(schema.validate_claim_row(claim_row(), PID, n_bench_rows=3), [])
        minimal = {k: claim_row()[k] for k in schema.CLAIM_REQUIRED}
        self.assertEqual(schema.validate_claim_row(minimal, PID), [])
        self.assertEqual(schema.validate_claim_row(claim_row(benchmark_row=None, conditions=None,
                                                             source_chunk="2507.18174#017.0"), PID), [])
        self.assertEqual(schema.validate_claim_row(claim_row(conditions={"power_scope": "n/r"}), PID), [])

    def test_keys(self):
        row = claim_row()
        del row["excerpt"]
        self.assertIn("manquante", schema.validate_claim_row(row, PID)[0])
        self.assertIn("inconnue", schema.validate_claim_row(claim_row(note="x"), PID)[0])
        self.assertTrue(schema.validate_claim_row(claim_row(text="  "), PID))
        self.assertTrue(schema.validate_claim_row([], PID))

    def test_invalid_values(self):
        bad = [
            dict(claim_id="autre-papier!c07"), dict(claim_id=f"{PID}#c07"), dict(claim_id=f"{PID}!c7"),
            dict(kind="résultats"), dict(voice="lecteur"), dict(source_chunk="017.0"),
            dict(conditions=["COCO"]), dict(conditions={"batch": ""}), dict(conditions={"batch": 1}),
            dict(conditions={"power_scope": "wall"}),
            dict(benchmark_row=0), dict(benchmark_row=True), dict(benchmark_row="2"),
            dict(caveats="une réserve"), dict(caveats=[""]),
            dict(chunk_sha1="xyz"), dict(chunk_sha1="0123"),
        ]
        for kw in bad:
            self.assertTrue(schema.validate_claim_row(claim_row(**kw), PID), kw)
        self.assertIn("que 1 ligne", schema.validate_claim_row(claim_row(), PID, n_bench_rows=1)[0])


if __name__ == "__main__":
    unittest.main()
