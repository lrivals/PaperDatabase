"""Tests de lib/claims.py (lot C, DATA_MODEL §12) et de son appel dans bin/reindex.py.

.venv/bin/python -m unittest discover tests
"""
import contextlib
import csv
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from lib import claims, rag, schema  # noqa: E402

_spec = importlib.util.spec_from_file_location("reindex", ROOT / "bin" / "reindex.py")
reindex = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(reindex)

PID = "arxiv-1612.07119-finn"
META = {"id": PID, "arxiv_id": "1612.07119", "title": "FINN", "year": 2016,
        "authors": [{"given": "Y", "family": "Umuroglu"}]}
LONG = " ".join(["filler"] * 400)
SECTIONS = [
    ("001", f"Table 1: CNV reaches 21,900 FPS at 11.7 W on the ZC706. {LONG} 283 GOPS"),
    ("002", "The board idles at 7 W, which is included in all power figures."),
]


def _claim(n, chunk, excerpt, **kw):
    return {"claim_id": f"{PID}!c{n:02d}", "kind": "résultat", "text": "…", "voice": "auteurs",
            "source_chunk": chunk, "excerpt": excerpt, **kw}


class TestClaims(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.dir = self.root / "papers" / PID
        self.dir.mkdir(parents=True)
        (self.dir / "metadata.json").write_text(json.dumps(META))
        (self.dir / "sections.jsonl").write_text("".join(json.dumps({
            "id": f"{PID}#{sid}", "paper_id": PID, "kind": "table", "section": "5",
            "subsection": None, "order": int(sid), "page": 1, "text": text}) + "\n"
            for sid, text in SECTIONS))
        with open(self.root / "benchmarks.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=schema.BENCHMARK_COLUMNS, lineterminator="\n")
            w.writeheader()
            w.writerow({c: PID if c == "paper_id" else "n/r" for c in schema.BENCHMARK_COLUMNS})

    def tearDown(self):
        self.tmp.cleanup()

    def _write(self, rows, extra=""):
        (self.dir / claims.FILENAME).write_text(
            "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows) + extra)

    def _levels(self):
        results, summary = claims.check(self.root)
        return {(r["line"], r["level"]): r["msg"] for r in results}, summary

    def test_no_claims(self):
        self.assertEqual(claims.check(self.root), ([], {"claims": 0, "papers": 0, "verified": 0}))

    def test_verified(self):
        sha = rag.sha1(rag.load_chunks(self.root)[-1]["text"])[:8]
        self._write([
            _claim(1, f"{PID}#001.0", "CNV reaches 21,900 FPS at 11.7 W", benchmark_row=1),
            _claim(2, "1612.07119#002", "the board idles at 7 W", chunk_sha1=sha),  # id court, sans .k
            _claim(3, f"{PID}#002.0", "The board idles at 7 W which includes all power figures",
                   voice="déduit"),                                                 # APPROX
        ])
        got, summary = self._levels()
        self.assertEqual(got, {})
        self.assertEqual(summary, {"claims": 3, "papers": 1, "verified": 3})

    def test_errors(self):
        self._write([
            _claim(1, f"{PID}#002.0", "the board consumes 40 W at peak"),            # ABSENT
            _claim(2, f"{PID}#002.0", "The board idles at 9 W, which is included"),  # NOMBRES
            _claim(3, f"{PID}#002.0", "CNV reaches 21,900 FPS at 11.7 W"),           # autre passage
            _claim(4, f"{PID}#009.0", "anything"),                                   # introuvable
            _claim(5, f"{PID}#002.0", "the board idles at 7 W", chunk_sha1="deadbeef"),  # MODIFIÉ
            _claim(5, f"{PID}#002.0", "the board idles at 7 W"),                     # doublon
            _claim(6, f"{PID}#002.0", "the board idles at 7 W", benchmark_row=2),    # 1 seule ligne
            _claim(7, f"{PID}#002.0", "CNV reaches 21,900 FPS", chunk_sha1="deadbeef"),  # erreur > MODIFIÉ
        ], extra="{pas du json\n")
        got, summary = self._levels()
        self.assertIn("ABSENT", got[(1, "erreur")])
        self.assertIn("NOMBRES", got[(2, "erreur")])
        self.assertIn(f"trouvé dans 1612.07119#001.0", got[(3, "erreur")])
        self.assertIn("introuvable", got[(4, "erreur")])
        self.assertIn("modifié", got[(5, "note")])
        self.assertIn("en double", got[(6, "erreur")])
        self.assertIn("que 1 ligne", got[(7, "erreur")])
        self.assertIn("corriger source_chunk (et chunk_sha1)", got[(8, "erreur")])
        self.assertNotIn((8, "note"), got)
        self.assertIn("illisible", got[(9, "erreur")])
        self.assertEqual(summary["verified"], 2)   # lignes 5 (MODIFIÉ, note) et 6 (doublon d'id)
        self.assertIn("# 8 claim(s) dans 1 papier(s), 2 excerpt(s) vérifié(s)",
                      claims.render(*claims.check(self.root)))

    def test_text_numbers(self):
        self._write([
            _claim(1, f"{PID}#001.0", "CNV reaches 21,900 FPS", text="CNV : 21 900 FPS à 11,7 W sur ZC706, 283 GOPS"),
            _claim(2, f"{PID}#002.0", "the board idles at 7 W", text="La carte consomme 7 W au repos, 12 W en charge"),
        ])
        got, summary = self._levels()
        self.assertEqual(summary["verified"], 2)
        self.assertEqual(list(got), [(2, "note")])          # 283 : même section, autre passage
        self.assertTrue(got[(2, "note")].endswith(": 12 (conversion ? autre passage ?)"))

    def test_other_paper_chunk(self):
        other = self.root / "papers" / "2022-feng-yolo-edge"
        other.mkdir()
        (other / "metadata.json").write_text(json.dumps({"id": other.name, "title": "Y"}))
        (other / "sections.jsonl").write_text(json.dumps({
            "id": f"{other.name}#000", "paper_id": other.name, "kind": "section", "section": "1",
            "subsection": None, "order": 0, "page": 1, "text": "YOLO at 9 FPS."}) + "\n")
        self._write([_claim(1, f"{other.name}#000.0", "YOLO at 9 FPS")])
        got, _ = self._levels()
        self.assertIn("introuvable dans ce papier", got[(1, "erreur")])
        self.assertEqual(claims.check(self.root, {other.name})[1]["papers"], 0)

    def test_reindex(self):
        self._write([_claim(1, f"{PID}#002.0", "the board consumes 40 W"),
                     _claim(2, f"{PID}#002.0", "the board idles at 7 W", chunk_sha1="deadbeef")])
        before = (self.dir / claims.FILENAME).read_text()
        problems, notes = [], []
        with contextlib.redirect_stdout(io.StringIO()) as out:
            reindex.check_claims(self.root, problems, notes)
        self.assertIn("2 claims dans 1 papier(s), 1 excerpts vérifiés", out.getvalue())
        self.assertEqual(len(problems), 1)
        self.assertTrue(problems[0].startswith(f"{PID} : claims.jsonl ligne 1 : excerpt ABSENT"))
        self.assertEqual(len(notes), 1)
        self.assertEqual((self.dir / claims.FILENAME).read_text(), before)


if __name__ == "__main__":
    unittest.main()
