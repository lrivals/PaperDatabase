"""Tests de lib/tablegold.py (vérité terrain des tableaux, lot E-e).

.venv/bin/python -m unittest discover tests
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from lib import tablegold as tg  # noqa: E402

GOLD = {"paper_id": "p", "section_id": "p#003", "label": "TABLE III", "page": 8,
        "header": ["DPU", "Power (W)", "LUTs"],
        "rows": [["B512", "4.792", "28.2k (12.4%)"], ["B800", "5.206", "31.2k (13.71%)"]],
        "units": {"Power (W)": "W"}, "defects": [], "reviewed": False}


def section(text, kind="table"):
    return {"id": "p#003", "paper_id": "p", "kind": kind, "text": text}


class TestNumbers(unittest.TestCase):
    def test_norm(self):
        self.assertEqual(tg.norm_number("18, 820"), "18820")
        self.assertEqual(tg.norm_number("3,5"), "3.5")
        self.assertEqual(tg.norm_number("−1.2"), "-1.2")
        self.assertEqual(tg.numbers("28.2k (12.4%)"), ["28.2k", "12.4"])


class TestScore(unittest.TestCase):
    def test_perfect(self):
        text = ("TABLE III FPGA resources\n\nDPU | Power (W) | LUTs\n\n"
                "B512 | 4.792 | 28.2k (12.4%)\n\nB800 | 5.206 | 31.2k (13.71%)")
        s = tg.score_table(GOLD, section(text))
        self.assertEqual((s["detected"], s["attached"], s["cells"], s["numbers"], s["units"]),
                         (True, True, 1.0, 1.0, 1.0))

    def test_shifted_and_wrong_caption(self):
        text = ("TABLE II other\n\nDPU | Power (W) | LUTs\n\n"
                "B512 | 28.2k (12.4%) | 4.792\n\nB800 | 5.206 | 31.2k (13.71%)")
        s = tg.score_table(GOLD, section(text))
        self.assertFalse(s["attached"])
        self.assertAlmostEqual(s["cells"], 4 / 6)  # B512 : 2 cellules sur 3 décalées
        self.assertEqual(s["numbers"], 1.0)    # tous les nombres sont là

    def test_missing_body(self):
        s = tg.score_table(GOLD, section("TABLE III FPGA resources"))
        self.assertFalse(s["detected"])
        self.assertEqual(s["cells"], 0.0)
        self.assertFalse(tg.score_table(GOLD, None)["detected"])

    def test_evaluate(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "papers" / "p").mkdir(parents=True)
            (Path(d) / "papers" / "p" / "sections.jsonl").write_text(json.dumps(section(
                "TABLE III x\n\nDPU | Power (W) | LUTs\n\nB512 | 4.792 | 28.2k (12.4%)")) + "\n")
            out = tg.evaluate(d, [GOLD])
            self.assertEqual(out["n"], 1)
            self.assertEqual(out["detected"], 1.0)
            self.assertEqual(out["cells"], 0.5)


if __name__ == "__main__":
    unittest.main()
