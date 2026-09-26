"""Small checks for isolated benchmark routing and evidence matching."""

import csv
import json
import shutil
import tempfile
import unittest
from io import BytesIO
from pathlib import Path
from unittest.mock import patch

from bin import bench_cli, reindex
from lib import schema


ROOT = Path(__file__).resolve().parent.parent


class BenchTest(unittest.TestCase):
    def test_reindex_accepts_an_isolated_root(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            source = next((ROOT / "papers").glob("*/metadata.json")).parent
            shutil.copytree(source, root / "papers" / source.name,
                            ignore=shutil.ignore_patterns("paper.pdf", "grobid.tei.xml"))
            with (root / "benchmarks.csv").open("w", newline="") as f:
                csv.writer(f).writerow(schema.BENCHMARK_COLUMNS)
            self.assertEqual(reindex.run(root), 0)
            self.assertIn(source.name, (root / "INDEX.md").read_text())

    def test_evidence_matches_original_locator_and_quote(self):
        evidence = {"paper_id": "p1", "id": "p1#001", "quote": "verified result"}
        hit = {"paper_id": "p1", "locator": "p1#001", "kind": "section",
               "text": "A verified result was reported."}
        self.assertTrue(bench_cli.retrieved_match(hit, evidence))
        self.assertFalse(bench_cli.retrieved_match({**hit, "locator": "p1#002"}, evidence))
        self.assertFalse(bench_cli.retrieved_match({**hit, "kind": "fiche"}, evidence))

    def test_cpu_search_hits_match_through_their_parent_section(self):
        class Index:
            def search(self, q, k, mode, rerank):
                return [{"paper_id": "p1", "kind": "section", "section_id": "p1#001",
                         "chunk_id": "p1#001.1", "text": "second window only"}]
        evidence = {"paper_id": "p1", "id": "p1#001", "quote": "first window quote"}
        hits = bench_cli.cpu_search(Index(), "q", False,
                                    {"p1#001": "first window quote. second window only"})
        self.assertTrue(bench_cli.retrieved_match(hits[0], evidence))

    def test_local_generator_rejects_a_different_loaded_model(self):
        response = BytesIO(json.dumps({"model": "other.gguf", "choices": [
            {"message": {"content": '{"cases": []}'}}]}).encode())
        with patch.object(bench_cli.urllib.request, "urlopen", return_value=response):
            with self.assertRaisesRegex(RuntimeError, "frozen generation model"):
                bench_cli.local_generate("question", 1, 1)

    def test_generation_refills_a_rejected_development_case_after_test_is_full(self):
        cases = [{"category": "single", "split": split, "language": language}
                 for split, count in (("development", 8), ("test", 12))
                 for language in ("en", "fr") for _ in range(count)]
        cases.pop(0)
        self.assertEqual(bench_cli.generation_group(cases, "single"),
                         ("development", "en", 1))

    def test_missing_candidates_exclude_aliases_and_abbreviated_titles(self):
        with tempfile.TemporaryDirectory() as d:
            meta = Path(d) / "metadata.json"
            meta.write_text(json.dumps({"title": "FINN-R: A Framework for Neural Networks",
                                        "arxiv_id": "1809.04570", "doi": "10.1/finn"}))
            rejected = [
                {"identity": "10.1/other", "title": "FINN-R"},
                {"identity": "10.1/finn", "title": "An alternative long title for the same work"},
                {"identity": "10.1/absent", "title": "A distinct absent paper about FPGA memory systems"}]
            with patch.object(bench_cli, "sources", return_value=[meta]), \
                    patch.object(bench_cli, "read", return_value={"rejected": rejected}):
                self.assertEqual(bench_cli.absent_candidates(), [rejected[2]])


if __name__ == "__main__":
    unittest.main()
