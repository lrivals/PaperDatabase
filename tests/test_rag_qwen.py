"""Small end-to-end checks of evidence identity, unknown values and staged imports."""

import csv
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from lib import rag_external, rag_models, schema, rag_qwen as rag  # noqa: E402


class RagTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        source = ROOT / "papers" / "arxiv-2507.18174-real-time-object-detection-classification"
        shutil.copytree(source, self.root / "papers" / source.name,
                        ignore=shutil.ignore_patterns("paper.pdf", "grobid.tei.xml"))
        with (self.root / "benchmarks.csv").open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=schema.BENCHMARK_COLUMNS)
            writer.writeheader()
            with (ROOT / "benchmarks.csv").open(newline="") as original:
                for row in csv.DictReader(original):
                    if row["paper_id"] == source.name:
                        writer.writerow(row)

    def tearDown(self):
        self.tmp.cleanup()

    def test_lexical_source_and_numeric_conditions(self):
        rag.build(self.root, mode="lexical")
        hit = rag.search(self.root, "KV260 3.5 W", mode="lexical", reranking=False)
        self.assertTrue(any(r["paper_id"].startswith("arxiv-2507") for r in hit["results"]))
        self.assertTrue(any(r["kind"] in ("section", "table", "figure") for r in hit["results"]))
        rows = rag.benchmarks(self.root, [{"field": "power_scope", "op": "eq", "value": "unspecified"}])
        self.assertEqual(rows["total_matches"], 1)
        self.assertAlmostEqual(rows["results"][0]["computed_fps_per_w"], 9 / 3.5)
        self.assertEqual(rows["results"][0]["computed_power_scope"], "unspecified")
        eid = rows["results"][0]["evidence_id"]
        self.assertEqual(rag.evidence(self.root, eid)["kind"], "benchmark")
        self.assertTrue(rag.check_answer(self.root, {"snapshot": hit["snapshot"],
                                          "claims": [{"text": "9 FPS", "evidence_ids": [eid],
                                                      "excerpt": "fps: 9"}]})["valid"])
        self.assertFalse(rag.check_answer(self.root, {"snapshot": hit["snapshot"],
                                           "claims": [{"text": "9 FPS", "evidence_ids": [eid],
                                                       "excerpt": "fps: 99"}]})["valid"])
        self.assertTrue(rag.check_answer(self.root, {"snapshot": hit["snapshot"],
                                          "claims": [{"text": "9 FPS",
                                                      "citations": [{"id": eid, "excerpt": "fps: 9"}]}]})["valid"])
        with self.assertRaisesRegex(ValueError, "nonempty claims"):
            rag.check_answer(self.root, {"snapshot": hit["snapshot"], "claims": []})

    def test_stale_snapshot_and_rebuild(self):
        first = rag.build(self.root, mode="lexical")["snapshot"]
        self.assertTrue(rag.build(self.root, mode="lexical")["unchanged"])
        path = next((self.root / "papers").glob("*/fiche.md"))
        path.write_text(path.read_text() + "\nCurator correction.\n")
        with self.assertRaisesRegex(RuntimeError, "stale"):
            rag.search(self.root, "KV260", mode="lexical")
        self.assertNotEqual(rag.build(self.root, mode="lexical")["snapshot"], first)

    def test_external_import_is_isolated(self):
        import pymupdf
        pdf = pymupdf.open()
        page = pdf.new_page()
        page.insert_text((70, 70), "Example New FPGA Paper", fontsize=16)
        page.insert_text((70, 110), "I. INTRODUCTION", fontsize=12)
        page.insert_text((70, 135), "\n".join(
            ["FPGA accelerators process images in an edge computing pipeline." for _ in range(32)]),
            fontsize=10)
        data = pdf.tobytes()
        candidate = {"title": "Example New FPGA Paper", "year": 2026,
                     "authors": [{"given": "Ada", "family": "Test"}],
                     "arxiv_id": "2609.99999", "doi": None, "venue": "arXiv preprint",
                     "type": "preprint", "abstract": "FPGA accelerators process images",
                     "url": "https://arxiv.org/abs/2609.99999",
                     "pdf_url": "https://arxiv.org/pdf/2609.99999"}

        def download(url, target, budget):
            target.write_bytes(data)
            return len(data), url

        build_index = rag.build

        with mock.patch.object(rag_external, "_openalex_candidates", return_value=[candidate]), \
             mock.patch.object(rag_external, "_arxiv_candidates", return_value=[]), \
             mock.patch.object(rag_external, "_download", side_effect=download), \
             mock.patch.object(rag_models, "rerank", side_effect=lambda q, texts: [0.9] * len(texts)), \
             mock.patch("bin.ingest.grobid_alive", return_value=False), \
             mock.patch("bin.reindex.run", return_value=0), \
             mock.patch.object(rag, "build", side_effect=lambda root, **kw: build_index(root, mode="lexical")):
            result = rag_external.acquire(self.root, "FPGA accelerators", "trial")
            candidate["arxiv_id"] = "2609.99998"
            duplicate = rag_external.acquire(self.root, "FPGA accelerators", "second")
        self.assertEqual(len(result["imported"]), 1, result["errors"])
        created = self.root / "papers" / result["imported"][0]
        self.assertEqual(json.loads((created / "metadata.json").read_text())["status"]["fiche"], "todo")
        self.assertTrue((created / "paper.pdf").read_bytes().startswith(b"%PDF"))
        self.assertTrue((created / "acquisition.json").exists())
        self.assertEqual(result["selected_evidence"][0]["paper_id"], result["imported"][0])
        self.assertFalse(duplicate["imported"])
        self.assertTrue(any("PDF already exists" in error for error in duplicate["errors"]))

    def test_external_rejects_html_payload(self):
        class HtmlResponse:
            is_redirect = False
            headers = {}

            def __enter__(self):
                return self

            def __exit__(self, *args):
                pass

            def raise_for_status(self):
                pass

            def iter_content(self, _):
                yield b"<html>not a PDF</html>"

        target = self.root / "bad.pdf"
        with mock.patch.object(rag_external, "_public_https"), \
             mock.patch.object(rag_external.requests, "get", return_value=HtmlResponse()):
            with self.assertRaisesRegex(ValueError, "not a PDF"):
                rag_external._download("https://example.org/paper.pdf", target, 0)


if __name__ == "__main__":
    unittest.main()
