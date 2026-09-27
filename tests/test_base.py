import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib import base  # noqa: E402


class DataRootTest(unittest.TestCase):
    def test_env_wins(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(base.data_root({"PDB_ROOT": d}, cwd=base.CODE), Path(d).resolve())

    def test_marker_found_in_parent(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "base.json").write_text("{}")
            sub = Path(d) / "papers" / "x"
            sub.mkdir(parents=True)
            self.assertEqual(base.data_root({}, cwd=sub), Path(d).resolve())

    def test_fallback_to_code(self):
        with tempfile.TemporaryDirectory() as d:
            env = {"PDB_REGISTRY": str(Path(d) / "absent.json")}
            self.assertEqual(base.data_root(env, cwd=d), base.CODE)


class ConfigTest(unittest.TestCase):
    def test_minimal_base(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "base.json").write_text(json.dumps({"name": "x", "axes": {"surveys": "S"}}))
            cfg = base.load_config(d)
            self.assertEqual(cfg["axis_rules"], {})
            self.assertTrue(base.in_topic(cfg, "anything", "anything", []))
            self.assertEqual(base.classify(cfg, "A survey of YOLOv8", "A survey"), (["surveys"], ["yolov8"]))

    def test_bad_regex_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "base.json").write_text(json.dumps({"name": "x", "axes": {"a": "A"},
                                                           "axis_rules": {"a": "(unclosed"}}))
            with self.assertRaises(ValueError):
                base.load_config(d)

    def test_classify_uses_given_config(self):
        cfg = base.load_config(base.CODE)
        axes, _ = base.classify(cfg, "YOLO on a Zynq FPGA")
        self.assertIn("yolo-fpga", axes)
        self.assertTrue(base.in_topic(cfg, "YOLO on a Zynq FPGA", "YOLO on a Zynq FPGA", axes))

    def test_reference_base(self):
        cfg = base.load_config(base.CODE)
        self.assertIn("surveys", cfg["axes"])
        self.assertLessEqual(set(cfg["axis_rules"]), set(cfg["axes"]))

    def test_folder_without_marker_uses_code_config(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(base.load_config(d), base.load_config(base.CODE))

    def test_undeclared_axis_rejected(self):
        cfg = base.load_config(base.CODE)
        cfg["axis_queries"] = {"inconnu": "x"}
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "base.json").write_text(json.dumps(cfg))
            with self.assertRaises(ValueError):
                base.load_config(d)


if __name__ == "__main__":
    unittest.main()
