"""Tests de lib/compare.py (pdb compare, docs/AMELIORATIONS.md lot J).

.venv/bin/python -m unittest discover tests
"""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from lib import compare, schema  # noqa: E402

HEADER = list(schema.BENCHMARK_COLUMNS) + ["metric_def", "dataset_split", "input_res"]


def row(pid, fps="10", power="2", scope="board", acc="n/r", metric="mAP@0.5", dataset="COCO",
        split="val2017", res="416", task="detection", **kw):
    r = {c: "n/r" for c in HEADER}
    r.update(paper_id=pid, model=f"m-{pid}", platform="ZCU104", task=task, fps=fps, power_w=power,
             power_scope=scope, accuracy_value=acc, accuracy_metric=metric, metric_def=metric,
             dataset=dataset, dataset_split=split, input_res=res, source_section="Table 2",
             confidence="high", quantization="INT8", **kw)
    return r


class TestKey(unittest.TestCase):
    def test_key_columns(self):
        self.assertEqual(compare.key_columns("fps", "luts"), ["task", "dataset", "dataset_split"])
        self.assertIn("metric", compare.key_columns("accuracy_value", "fps"))
        self.assertIn("power_scope", compare.key_columns("fps", "power_w"))
        self.assertIn("metric", compare.key_columns("fps", "luts", metric="mAP"))

    def test_non_numeric_axis(self):
        with self.assertRaises(ValueError):
            compare.compare(HEADER, [], "model", "fps")


class TestCompare(unittest.TestCase):
    def test_chip_and_board_never_grouped(self):
        rows = [row("a", scope="board"), row("b", scope="board"), row("c", scope="chip"),
                row("d", scope="chip")]
        res = compare.compare(HEADER, rows, "fps", "power_w")
        self.assertEqual(len(res["groups"]), 2)
        for g in res["groups"]:
            self.assertEqual(len({r["power_scope"] for r in g["rows"]}), 1)

    def test_every_row_kept_or_excluded(self):
        rows = [row("a"), row("b"), row("c", power="n/r"), row("d", scope="chip"),
                row("e", dataset="VOC")]
        res = compare.compare(HEADER, rows, "fps", "power_w")
        c = res["counts"]
        self.assertEqual(c["kept"] + c["excluded"], c["filtered"])
        reasons = {r["paper_id"]: why for r, why in res["excluded"]}
        self.assertEqual(reasons["c"], "y (power_w) en n/r")
        self.assertEqual(reasons["d"], "power_scope incompatible")
        self.assertEqual(reasons["e"], "seul papier du groupe")

    def test_metric_difference_reason(self):
        rows = [row("a", acc="40"), row("b", acc="41"), row("c", acc="60", metric="mAP@0.5:0.95")]
        res = compare.compare(HEADER, rows, "accuracy_value", "fps")
        self.assertEqual(res["excluded"][0][1], "métrique différente")

    def test_confidence_levels(self):
        strong = compare.compare(HEADER, [row("a"), row("b")], "fps", "power_w")
        self.assertEqual(strong["groups"][0]["confidence"], "forte")
        varies = compare.compare(HEADER, [row("a"), row("b", res="640")], "fps", "power_w")
        self.assertEqual(varies["groups"][0]["confidence"], "réservée")
        self.assertEqual(varies["groups"][0]["conditions"][0]["values"], ["416", "640"])
        unknown = compare.compare(HEADER, [row("a"), row("b", res="n/r")], "fps", "power_w")
        self.assertEqual(unknown["groups"][0]["confidence"], "faible")
        split = compare.compare(HEADER, [row("a", split="n/r"), row("b", split="n/r")], "fps", "power_w")
        self.assertEqual(split["groups"][0]["confidence"], "faible")
        unverified = [row("a", acc="40"), row("b", acc="41")]
        for r in unverified:
            r["metric_def"] = "n/r"
        res = compare.compare(HEADER, unverified, "accuracy_value", "fps")
        self.assertEqual(res["groups"][0]["key"]["metric"], "~mAP@0.5")
        self.assertEqual(res["groups"][0]["confidence"], "faible")

    def test_platform_class_separates(self):
        header = HEADER + ["platform_class"]
        rows = [row("a", platform_class="embedded"), row("b", platform_class="embedded"),
                row("c", platform_class="server")]
        res = compare.compare(header, rows, "fps", "power_w")
        self.assertEqual(len(res["groups"]), 1)
        self.assertEqual(res["excluded"][0][1], "platform_class différente")

    def test_absent_optional_column_ignored(self):
        header = list(schema.BENCHMARK_COLUMNS)
        rows = [{k: v for k, v in row(p).items() if k in header} for p in "ab"]
        res = compare.compare(header, rows, "fps", "power_w")
        self.assertEqual(res["groups"][0]["conditions"], [])

    def test_select(self):
        rows = [row("a"), row("b", metric="top-1", task="classification"), row("c", dataset="VOC")]
        self.assertEqual([r["paper_id"] for r in compare.select(rows, task="detect")], ["a", "c"])
        self.assertEqual([r["paper_id"] for r in compare.select(rows, metric="top")], ["b"])
        self.assertEqual([r["paper_id"] for r in compare.select(rows, papers={"a", "c"})], ["a", "c"])


class TestRender(unittest.TestCase):
    def setUp(self):
        rows = [row("a"), row("b", chunk_id="b#003"), row("c", power="n/r")]
        self.res = compare.compare(HEADER, rows, "fps", "power_w")

    def test_json_schema(self):
        d = json.loads(compare.render(self.res, {"a": "A"}, "json"))
        self.assertEqual(set(d), {"x", "y", "key", "counts", "groups", "excluded"})
        g = d["groups"][0]
        self.assertEqual(g["papers"], ["A", "b"])
        r = g["rows"][1]
        self.assertEqual((r["source_section"], r["confidence"], r["chunk_id"]), ("Table 2", "high", "b#003"))
        self.assertEqual(d["excluded"][0]["reason"], "y (power_w) en n/r")

    def test_text_blocks(self):
        for fmt in ("tsv", "md"):
            out = compare.render(self.res, {}, fmt)
            for block in ("## 1. Configurations retenues", "## 2. Conditions", "## 3. Lignes exclues"):
                self.assertIn(block, out)
        self.assertIn("# tronqué", compare.render(self.res, {}, "tsv", max_chars=120))


if __name__ == "__main__":
    unittest.main()
