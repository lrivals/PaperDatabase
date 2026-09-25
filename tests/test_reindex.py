"""Tests de bin/reindex.py : notes sur les benchmarks, mesures propres (own-…) dans INDEX.md.

.venv/bin/python -m unittest discover tests
"""
import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from lib import schema  # noqa: E402

_spec = importlib.util.spec_from_file_location("reindex", ROOT / "bin" / "reindex.py")
reindex = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(reindex)


def _p(pid, fiche="done", axes=("yolo-fpga",)):
    return {"id": pid, "axes": list(axes), "status": {"fiche": fiche}}


class TestBenchNotes(unittest.TestCase):
    def test_done_without_rows(self):
        papers = [_p("a"), _p("b"), _p("c", axes=("surveys",)), _p("d", fiche="todo"), _p("e")]
        rows = [{"paper_id": "e"}]
        notes = reindex.bench_notes(papers, rows, {"b": {"benchmarks": "none"}})
        self.assertEqual(len(notes), 1)
        self.assertTrue(notes[0].startswith("a : fiche done sans ligne"))

    def test_none_but_rows(self):
        notes = reindex.bench_notes([_p("a")], [{"paper_id": "a"}], {"a": {"benchmarks": "none"}})
        self.assertEqual(len(notes), 1)
        self.assertIn("benchmarks: none, mais", notes[0])


class TestOwnMeasurements(unittest.TestCase):
    def test_own_ids(self):
        self.assertTrue(schema.is_own_id("own-2026-kv260-map-sur-cible"))
        self.assertEqual(schema.own_source("own-2026-kv260-map-sur-cible"),
                         "docs/experiences/kv260-map-sur-cible.md")
        for bad in ("own-kv260", "own-26-x", "2026-own-x", "arxiv-1612.07119-finn", None):
            self.assertFalse(schema.is_own_id(bad), bad)
            self.assertIsNone(schema.own_source(bad))
        # jamais un nom de dossier papers/ valide
        self.assertTrue(schema.validate_paper_id("own-2026-kv260", {}))

    def test_index_section(self):
        rows = [{"paper_id": "own-2026-kv260-map"}, {"paper_id": "own-2026-kv260-map"},
                {"paper_id": "a"}]
        out = reindex.render([_p("a")], rows)
        self.assertIn("## Mesures propres", out)
        self.assertIn("| own-2026-kv260-map | [docs/experiences/kv260-map.md]"
                      "(docs/experiences/kv260-map.md) | 2 |", out)
        self.assertNotIn("Mesures propres", reindex.render([_p("a")], rows[2:]))


if __name__ == "__main__":
    unittest.main()
