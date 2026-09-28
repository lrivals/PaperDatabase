"""Tests de lib/plotdata.py (données des figures) et smoke test de lib/plotfig.py (pdb plot).

.venv/bin/python -m unittest discover tests
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
FPGA = ROOT / "bases" / "fpga"   # base réelle de référence

from lib import plotdata as D  # noqa: E402
from lib import schema  # noqa: E402

try:
    import matplotlib  # noqa: F401
    HAS_MPL = True
except ImportError:
    HAS_MPL = False


def _row(pid, platform="ZCU104", task="detection", fps="n/r", power="n/r", scope="n/r",
         quant="INT8", gops="n/r", metric="n/r", acc="n/r"):
    r = {c: "n/r" for c in schema.BENCHMARK_COLUMNS}
    r.update(paper_id=pid, model="m", platform=platform, task=task, fps=fps, power_w=power,
             power_scope=scope, quantization=quant, gops=gops, accuracy_metric=metric,
             accuracy_value=acc, confidence="high", source_section="Table 1")
    return r


class TestFamilies(unittest.TestCase):
    def test_real_platform_strings(self):
        cases = {
            "Zynq-7000 XC7Z020 (PYNQ-Z1)": "FPGA",
            "Kria KV260 (DPU)": "FPGA",
            "AWS F1 XCVU9P (237 MHz)": "FPGA",
            "xcu250-figd2104-2L-e (dit « Kintex UltraScale »)": "FPGA",
            "Jetson Orin Nano 8 GB (GPU Ampere 1024 cœurs)": "GPU embarqué",
            "Raspberry Pi 5 + AI HAT+ (Hailo-8)": "NPU / VPU",   # avant « Raspberry Pi »
            "Raspberry Pi 4B + Intel NCS2 (Myriad X VPU)": "NPU / VPU",
            "Raspberry Pi 5 (Cortex-A76, CPU seul)": "CPU",
            "STM32H743 (Cortex-M7, 512 kB SRAM)": "MCU",
            "GAP9 MCU (240 MHz, 650 mV)": "MCU",
            "NVIDIA GeForce GTX 1650 (4 GB)": "GPU bureau",
            "ASIC 14 nm FinFET": "ASIC",
            "n/r": D.OTHER,
            "": D.OTHER,
        }
        for platform, family in cases.items():
            self.assertEqual(D.platform_family(platform), family, platform)

    def test_every_csv_platform_is_classified(self):
        _, rows = __import__("lib.query", fromlist=["x"]).load_benchmarks(FPGA)
        unknown = {r["platform"] for r in rows if D.platform_family(r["platform"]) == D.OTHER}
        self.assertEqual(unknown, set(), "plateformes sans famille : compléter _FAMILY_RULES")


class TestQuantization(unittest.TestCase):
    def test_buckets(self):
        cases = {
            "FP16": "FP16", "INT8 (PTQ TensorRT)": "8 bits", "W1A1": "1–2 bits",
            "ternary W / ternary A (2 bits)": "1–2 bits", "ap_fixed<16,6>": "≥ 9 bits (fixe)",
            "32-bit fixed-point": "≥ 9 bits (fixe)", "QAT 7 bits (QKeras)": "3–7 bits",
            "W8A16": "8 bits", "HGQ (per-parameter fixed point)": "mixte",
            "INT8 étage figé / FP32 étage adaptatif": "mixte",
            "INT8 (CNN) / binary HV": "8 bits",
            "PTQ 8 bits selon les tables (4 bits selon §VI)": "8 bits",   # premier cité
            "n/r": schema.NR, "n/r (OpenVINO)": schema.NR,
        }
        for q, bucket in cases.items():
            self.assertEqual(D.quant_bucket(q), bucket, q)
            self.assertIn(D.quant_bucket(q), D.QUANT_BUCKETS)


class TestBenchmarks(unittest.TestCase):
    def test_numeric_excludes_nr(self):
        rows = [_row("a", fps="10", power="2"), _row("b", fps="n/r", power="3"),
                _row("c", fps="5", power="n/r")]
        pts, n, total = D.numeric(rows, "fps", "power_w")
        self.assertEqual((n, total), (1, 3))
        self.assertEqual(pts[0]["_v"], {"fps": 10.0, "power_w": 2.0})
        self.assertEqual(pts[0]["_family"], "FPGA")

    def test_nr_rates(self):
        rows = [_row("a", fps="10"), _row("b"), _row("c"), _row("d", fps="1")]
        self.assertEqual(D.nr_rates(rows, ["fps"]), {"fps": 0.5})

    def test_accuracy_panels_one_metric_each(self):
        rows = ([_row(str(i), fps="10", metric="mAP50 COCO", acc="40") for i in range(4)]
                + [_row(str(i), fps="10", metric="top-1", acc="70") for i in range(3)]
                + [_row(str(i), fps="10", metric="mean confidence (pas une précision)", acc="80")
                   for i in range(5)])
        panels = D.accuracy_panels(rows, min_rows=4)
        self.assertEqual([m for m, _ in panels], ["mAP50 COCO"])

    def test_coverage_matrix_counts_distinct_papers(self):
        papers = [{"id": "p1", "axes": ["yolo-fpga"]}, {"id": "p2", "axes": ["yolo-fpga", "surveys"]}]
        rows = [_row("p1"), _row("p1"), _row("p2"), _row("p2", platform="Jetson Nano")]
        fams, cols, m = D.coverage_matrix(rows, papers, "axis")
        self.assertNotIn("surveys", cols)
        self.assertEqual(m[fams.index("FPGA")][cols.index("yolo-fpga")], 2)
        self.assertEqual(m[fams.index("GPU embarqué")][cols.index("yolo-fpga")], 1)
        self.assertEqual(m[fams.index("FPGA")][cols.index("toolflows")], 0)
        fams, cols, m = D.coverage_matrix(rows, papers, "task")
        self.assertEqual(m[fams.index("FPGA")][cols.index("détection")], 2)


class TestEval(unittest.TestCase):
    def _runs(self, tmp):
        runs = [
            {"date": "2026-01-01T0000", "commit": "a", "dirty": False, "volets": ["extraction", "rag"],
             "results": {"extraction": {"quality": {"coverage_mean": 0.8}},
                         "rag": {"sets": {"rag_eval": {"hybrid": {"recall@5": 0.7}}}}}},
            {"date": "2026-01-02T0000", "commit": "b", "dirty": True, "volets": ["rag"],
             "results": {"rag": {"sets": {"rag_eval": {"hybrid": {"recall@5": 0.9}}}}}},
        ]
        for i, r in enumerate(runs):
            (Path(tmp) / f"{i}.json").write_text(json.dumps(r))
        (Path(tmp) / "broken.json").write_text("{")
        return D.load_eval_runs(tmp)

    def test_latest_per_volet(self):
        with tempfile.TemporaryDirectory() as tmp:
            runs = self._runs(tmp)
        self.assertEqual(len(runs), 2)
        latest = D.latest_eval(runs)
        self.assertEqual(latest["rag"][1]["commit"], "b")          # dernier run qui a rag
        self.assertEqual(latest["extraction"][1]["commit"], "a")   # le run b n'a pas extraction
        self.assertEqual(D.run_label(latest["rag"][1]), "2026-01-02T0000 · b (dirty)")

    def test_history(self):
        with tempfile.TemporaryDirectory() as tmp:
            runs = self._runs(tmp)
        h = D.eval_history(runs, {"r5": "rag.sets.rag_eval.hybrid.recall@5",
                                  "cov": "extraction.quality.coverage_mean"})
        self.assertEqual([v for _, v in h["r5"]], [0.7, 0.9])
        self.assertEqual(len(h["cov"]), 1)


@unittest.skipUnless(HAS_MPL, "matplotlib absent (requirements-plot.txt)")
class TestFigures(unittest.TestCase):
    def test_all_figures_render_on_the_real_base(self):
        from lib import plotfig
        import matplotlib.pyplot as plt
        ctx = plotfig.Context(FPGA)
        for name, (_, fn, _) in plotfig.FIGURES.items():
            with self.subTest(name):
                try:
                    fig, info = fn(ctx)
                except LookupError:
                    continue            # pas de run d'éval pour ce volet : figure ignorée
                self.assertIn("sources", info)
                plt.close(fig)


if __name__ == "__main__":
    unittest.main()
