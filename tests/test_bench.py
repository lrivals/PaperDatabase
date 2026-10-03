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
            source = next((ROOT / "bases" / "fpga" / "papers").glob("*/metadata.json")).parent
            shutil.copytree(source, root / "papers" / source.name,
                            ignore=shutil.ignore_patterns("paper.pdf", "grobid.tei.xml"))
            with (root / "benchmarks.csv").open("w", newline="") as f:
                csv.writer(f).writerow(schema.BENCHMARK_COLUMNS)
            self.assertEqual(reindex.run(root), 0)
            self.assertIn(source.name, (root / "INDEX.md").read_text())

    def test_reindex_accepts_optional_columns(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            source = next((ROOT / "bases" / "fpga" / "papers").glob("*/metadata.json")).parent
            shutil.copytree(source, root / "papers" / source.name,
                            ignore=shutil.ignore_patterns("paper.pdf", "grobid.tei.xml"))
            fields = [*schema.BENCHMARK_COLUMNS, "chunk_id", "input_res"]
            with (root / "benchmarks.csv").open("w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=fields)
                w.writeheader()
                w.writerow({c: "n/r" for c in fields} | {
                    "paper_id": source.name, "model": "m", "confidence": "high",
                    "chunk_id": f"{source.name}#000.0", "input_res": "416x416"})
            self.assertEqual(reindex.run(root), 0)
            (root / "benchmarks.csv").write_text(
                (root / "benchmarks.csv").read_text().replace("input_res", "notes", 1))
            self.assertEqual(reindex.run(root), 1)

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

    def test_claude_wrapper_reads_structured_output_and_errors(self):
        stream = "\n".join(json.dumps(e) for e in (
            {"type": "assistant", "message": {"content": [
                {"type": "tool_use", "name": "Bash", "input": {"command": "ls"}}]}},
            {"type": "result", "is_error": False, "structured_output": {"valid": True},
             "usage": {"input_tokens": 3}}))
        data, usage, events = bench_cli.claude_result(stream)
        self.assertEqual((data, usage["input_tokens"], len(events)), ({"valid": True}, 3, 2))
        text = json.dumps({"type": "result", "is_error": False, "result": '{"valid": false}'})
        self.assertEqual(bench_cli.claude_result(text)[0], {"valid": False})
        with self.assertRaisesRegex(RuntimeError, "Not logged in"):
            bench_cli.claude_result(json.dumps({"type": "result", "is_error": True,
                                                "result": "Not logged in"}))
        with patch.dict(bench_cli.os.environ, {"PDB_BENCH_CLAUDE": "/opt/claude"}):
            self.assertEqual(bench_cli.claude_binary(), "/opt/claude")
        done = type("Done", (), {"stdout": text, "stderr": ""})
        with patch.object(bench_cli.subprocess, "run", return_value=done):
            self.assertEqual(bench_cli.claude("q", {"valid": "boolean"}), {"valid": False})
            with self.assertRaisesRegex(ValueError, "schema mismatch"):
                bench_cli.claude("q", {"other": "string"})

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
