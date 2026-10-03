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

    def test_fallback_to_reference_base(self):
        with tempfile.TemporaryDirectory() as d:
            env = {"PDB_REGISTRY": str(Path(d) / "absent.json")}
            self.assertEqual(base.data_root(env, cwd=d), base.REFERENCE)


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
        cfg = base.load_config(base.REFERENCE)
        axes, _ = base.classify(cfg, "YOLO on a Zynq FPGA")
        self.assertIn("yolo-fpga", axes)
        self.assertTrue(base.in_topic(cfg, "YOLO on a Zynq FPGA", "YOLO on a Zynq FPGA", axes))

    def test_reference_base(self):
        cfg = base.load_config(base.REFERENCE)
        self.assertIn("surveys", cfg["axes"])
        self.assertLessEqual(set(cfg["axis_rules"]), set(cfg["axes"]))

    def test_folder_without_marker_uses_reference_config(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(base.load_config(d), base.load_config(base.REFERENCE))

    def test_undeclared_axis_rejected(self):
        cfg = base.load_config(base.REFERENCE)
        cfg["axis_queries"] = {"inconnu": "x"}
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "base.json").write_text(json.dumps(cfg))
            with self.assertRaises(ValueError):
                base.load_config(d)



class PlotConfigTest(unittest.TestCase):
    def _load(self, extra):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "base.json").write_text(json.dumps({"name": "x", "axes": {"a": "A"}, **extra}))
            return base.load_config(d)

    def test_plot_tasks_is_read_as_plot_tasks(self):
        cfg = self._load({"plot_tasks": [["RUL", "\\bRUL\\b"]]})
        self.assertEqual(cfg["plot"]["tasks"], [["RUL", "\\bRUL\\b"]])
        cfg = self._load({"plot_tasks": [["old", "x"]], "plot": {"tasks": [["new", "y"]]}})
        self.assertEqual(cfg["plot"]["tasks"], [["new", "y"]])

    def test_plot_block_validated(self):
        bad = ({"plot": {"colours": {}}},                               # clé inconnue
               {"plot": {"tasks": [["t", "(unclosed"]]}},               # regex
               {"plot": {"families": [["f"]]}},                         # pas une paire
               {"plot": {"skip": ["bench_inexistante"]}},               # figure inconnue
               {"plot": {"min_rows": {"nope": 3}}},
               {"plot": {"split_task": "tracking"}},                    # pas une classe
               {"plot": {"max_other": 2}},
               {"plot": []})
        for extra in bad:
            with self.subTest(extra=extra), self.assertRaises(ValueError):
                self._load(extra)
        cfg = self._load({"plot": {"tasks": [["tracking", "track"]], "split_task": "tracking",
                                   "skip": ["bench_fpga_resources"], "max_other": 0.2}})
        self.assertEqual(cfg["plot"]["split_task"], "tracking")

    def test_reference_base_has_no_plot_settings(self):
        self.assertEqual(base.load_config(base.REFERENCE)["plot"], {})


if __name__ == "__main__":
    unittest.main()
