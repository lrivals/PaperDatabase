"""Tests de bin/ingest.py qui ne demandent ni GROBID ni PDF.

.venv/bin/python -m unittest discover tests
"""
import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

_spec = importlib.util.spec_from_file_location("ingest", ROOT / "bin" / "ingest.py")
ingest = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ingest)


def _old(fiche, axes, tags):
    return {"axes": axes, "tags": tags, "status": {"extracted": True, "fiche": fiche}}


class TestKeepClassification(unittest.TestCase):
    def test_first_ingestion(self):
        self.assertEqual(ingest.keep_classification(None, ["toolflows"], ["hls4ml"]),
                         (["toolflows"], ["hls4ml"]))

    def test_todo_union_keeps_manual_tags(self):
        # cas 2103.05579 (24/09/2026) : l'abstract GROBID ne mentionne plus quantization/pruning
        old = _old("todo", ["toolflows"], ["hls4ml", "quantization", "pruning"])
        axes, tags = ingest.keep_classification(old, ["toolflows", "platforms"], ["hls4ml", "zynq"])
        self.assertEqual(axes, ["toolflows", "platforms"])
        self.assertEqual(tags, ["hls4ml", "quantization", "pruning", "zynq"])

    def test_done_keeps_confirmed(self):
        old = _old("done", ["yolo-fpga"], ["yolov5"])
        self.assertEqual(ingest.keep_classification(old, ["platforms"], ["kv260"]),
                         (["yolo-fpga"], ["yolov5"]))

    def test_classify(self):
        axes, tags = ingest.classify("A survey of YOLOv5-tiny with hls4ml on KV260", "A survey")
        self.assertEqual(axes[0], "surveys")
        self.assertIn("yolo-fpga", axes)
        self.assertEqual(tags[:3], ["yolov5-tiny", "hls4ml", "kv260"])


if __name__ == "__main__":
    unittest.main()
