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
STAGE = ROOT / "bases" / "stage"  # base sans mesures matérielles (papiers algorithmiques, MCU)
DRONE = ROOT / "bases" / "drone"  # base avec bloc plot : tâches et famille propres
BASES = (FPGA, STAGE, DRONE)

from lib import plotdata as D  # noqa: E402
from lib import base, query, schema  # noqa: E402

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
            "Pixel 2 single large core (Snapdragon 835)": "SoC mobile",
            "Qualcomm Hexagon DSP HVX via NN-API (Pixel 2)": "SoC mobile",
            "VEGA (PULP, 9 cœurs RISC-V, ASIC 22 nm GF) @ 375 MHz": "MCU",   # avant ASIC
            "n/r": D.PLATFORM_NR,
            "n/r (PC)": D.PLATFORM_NR,
            "": D.PLATFORM_NR,
            "Loihi": D.OTHER,
        }
        for platform, family in cases.items():
            self.assertEqual(D.platform_family(platform), family, platform)

    def test_every_csv_platform_is_classified(self):
        for root in BASES:
            rules = D.family_rules(base.load_config(root))
            _, rows = query.load_benchmarks(root)
            unknown = {r["platform"] for r in rows if D.platform_family(r["platform"], rules) == D.OTHER}
            self.assertEqual(unknown, set(), f"{root.name} : plateformes sans famille, compléter "
                                             "_FAMILY_RULES ou plot.families (pdb plot --check)")

    def test_base_families_come_after_code_rules(self):
        cfg = {"plot": {"families": [["neuromorphique", "loihi"], ["GPU bureau", r"\bgpu\b"]]}}
        rules = D.family_rules(cfg)
        self.assertEqual(D.platform_family("Intel Loihi (Kapoho Bay)", rules), "neuromorphique")
        self.assertEqual(D.platform_family("PC (GPU n/r)", rules), "GPU bureau")
        # une règle de base ne vole pas une plateforme que le code reconnaît
        self.assertEqual(D.platform_family("Jetson Nano (GPU Maxwell)", rules), "GPU embarqué")
        self.assertEqual(D.platform_family("Intel Loihi"), D.OTHER)      # sans la base
        self.assertEqual(D.families(rules), (*D.FAMILIES, "neuromorphique"))

    def test_family_colours_stable_across_bases(self):
        if not HAS_MPL:
            self.skipTest("matplotlib absent")
        from lib import plotfig
        _, c0, _ = plotfig.family_style(D.FAMILIES)
        order, c1, m1 = plotfig.family_style(D.families(D.family_rules(base.load_config(DRONE))))
        for f in D.FAMILIES:
            self.assertEqual(c0[f], c1[f], f)
        self.assertNotIn(c1["neuromorphique"], plotfig.PALETTE)
        self.assertEqual(order[-2:], (D.OTHER, D.PLATFORM_NR))


class TestTasks(unittest.TestCase):
    def test_default_rules_unchanged(self):
        cases = {"continual learning (class-incremental)": "apprentissage continu",
                 "anomaly detection": "anomalie", "object detection": "détection",
                 "image classification": "classification", "autoencoder compression": "compression / AE",
                 "RUL prediction (turbofan)": D.OTHER}
        for task, bucket in cases.items():
            self.assertEqual(D.task_bucket(task), bucket, task)
        self.assertEqual(D.task_labels(D.task_rules({})), D.TASKS)

    def test_base_rules(self):
        tasks = D.task_rules(base.load_config(STAGE))
        cases = {"RUL prediction (turbofan)": "RUL / pronostic",
                 "concept drift detection": "anomalie / dérive",
                 "keyword spotting (inference)": "classification",
                 "on-device transfer learning (fine-tuning)": "apprentissage continu"}
        for task, bucket in cases.items():
            self.assertEqual(D.task_bucket(task, tasks), bucket, task)
        self.assertIn("RUL / pronostic", D.task_labels(tasks))

    def test_task_other_share_under_threshold(self):
        for root in BASES:
            cfg = base.load_config(root)
            _, rows = query.load_benchmarks(root)
            r = D.plot_check(rows, cfg)
            with self.subTest(base=root.name):
                self.assertLessEqual(r["rates"]["task_other"], r["max_other"],
                                     f"{root.name} : trop de tâches « autre » (pdb plot --check)")
                self.assertLessEqual(r["rates"]["platform_other"], r["max_other"])


class TestPlotCheck(unittest.TestCase):
    def test_suggested_task_rule_groups_variants(self):
        sugg = D.suggest_task_rules({"tracking (SOT)": 2, "single-object tracking": 2,
                                     "pose estimation": 1})
        self.assertEqual(len(sugg), 1)
        label, rx = sugg[0]
        self.assertEqual(label, "tracking")
        for t in ("tracking (SOT)", "single-object tracking", "multi-target tracker"):
            self.assertRegex(t, rx)

    def test_family_hints(self):
        fams, rest = D.suggest_family_rules({"Intel Loihi 2": 1, "PC (GPU n/r)": 1, "Zork-9": 2})
        self.assertEqual([f for f, _ in fams], ["neuromorphique", "GPU bureau"])
        self.assertEqual(rest, {"Zork-9": 2})

    def test_check_proposes_only_over_threshold(self):
        rows = ([_row(str(i), task="object tracking") for i in range(4)]
                + [_row(str(i), task="object detection") for i in range(6)])
        r = D.plot_check(rows, {"plot": {}})
        self.assertTrue(r["alerts"])
        self.assertIn(["tracking", r"\btrack"], r["proposed"]["tasks"])
        self.assertEqual(r["proposed"]["tasks"][-2:], [["détection", "detection"],
                                                       ["classification", "classification"]])
        r = D.plot_check(rows, {"plot": {"max_other": 0.5}})
        self.assertEqual(r["alerts"], [])
        self.assertNotIn("tasks", r["proposed"])

    def test_check_per_paper(self):
        rows = [_row("a", platform="Loihi", task="optical flow"), _row("b")]
        r = D.plot_check(rows, {"plot": {}}, paper="a")
        self.assertEqual(r["rows"], 1)
        self.assertEqual(len(r["alerts"]), 2)
        self.assertEqual(D.plot_check(rows, {"plot": {}}, paper="b")["alerts"], [])

    def test_no_fpga_suggests_skipping_resources(self):
        rows = [_row("a", platform="STM32H7")]
        self.assertIn("bench_fpga_resources", D.plot_check(rows, {"plot": {}})["proposed"]["skip"])
        self.assertNotIn("skip", D.plot_check([_row("a")], {"plot": {}})["proposed"])


class TestStale(unittest.TestCase):
    def test_stale_figures(self):
        import os
        import time
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "benchmarks.csv").write_text("x\n")
            (root / "base.json").write_text("{}")
            out = root / "figures"
            out.mkdir()
            cfg = {"axes": {"a": "A"}, "plot": {}}
            h = D.config_hash(cfg)
            (out / "bench_quantization.png").write_text("")
            manifest = {"bench_quantization": {"file": "bench_quantization.png", "config_hash": h},
                        "bench_fps_power": {"skipped": "aucune ligne", "checked": time.time() + 10,
                                            "config_hash": h}}
            figs = {"bench_quantization": "bench", "bench_fps_power": "bench",
                    "bench_gops_per_watt": "bench"}
            past = time.time() - 100
            for f in ("benchmarks.csv", "base.json"):
                os.utime(root / f, (past, past))
            self.assertEqual(D.stale_figures(root, out, manifest, figs, cfg),
                             {"bench_gops_per_watt": "jamais générée"})
            os.utime(root / "benchmarks.csv", (time.time() + 5, time.time() + 5))
            self.assertEqual(set(D.stale_figures(root, out, manifest, figs, cfg)),
                             {"bench_quantization", "bench_gops_per_watt"})
            cfg2 = {"axes": {"a": "A"}, "plot": {"skip": ["bench_fpga_resources"]}}
            self.assertEqual(D.stale_figures(root, out, manifest, figs, cfg2)["bench_fps_power"],
                             "réglages de base.json changés")


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

    def test_coverage_matrix_base_axes_and_nr_platform(self):
        papers = [{"id": "p1", "axes": ["pdm-rul"]}]
        rows = [_row("p1", platform="n/r", task="RUL prediction")]
        tasks = (("RUL / pronostic", r"\bRUL\b"),)
        fams, cols, m = D.coverage_matrix(rows, papers, "axis", axes=("surveys", "pdm-rul", "datasets"))
        self.assertEqual((fams, cols, m), ([D.PLATFORM_NR], ["pdm-rul", "datasets"], [[1, 0]]))
        fams, cols, m = D.coverage_matrix(rows, papers, "task", tasks=tasks)
        self.assertEqual((fams, cols, m), ([D.PLATFORM_NR], ["RUL / pronostic"], [[1]]))

    def test_accuracy_panels_other_column(self):
        rows = [_row(str(i), metric="top-1", acc="70") for i in range(3)]
        for r in rows:
            r["latency_ms"] = "12"
        self.assertEqual(D.accuracy_panels(rows, x="fps", min_rows=3), [])
        self.assertEqual([m for m, _ in D.accuracy_panels(rows, x="latency_ms", min_rows=3)], ["top-1"])


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
    def test_figure_names_match_base(self):
        from lib import plotfig
        self.assertEqual(tuple(plotfig.FIGURES), base.PLOT_FIGURES)

    def test_split_task_and_new_family_in_figures(self):
        from lib import plotfig
        import matplotlib.pyplot as plt
        ctx = plotfig.Context(DRONE)
        fig, _ = plotfig.fig_corpus_gaps(ctx)
        labels = {t.get_text() for ax in fig.axes for t in ax.get_yticklabels()}
        self.assertIn("neuromorphique", labels)
        plt.close(fig)
        ctx._cache["cfg"] = {**ctx.cfg, "plot": {**ctx.plot, "split_task": "suivi (tracking)"}}
        fig, _ = plotfig.fig_bench_fps_power(ctx)
        self.assertTrue(fig.axes[0].get_title(loc="left").startswith("Suivi (tracking)"))
        plt.close(fig)

    def test_all_figures_render_on_the_real_bases(self):
        from lib import plotfig
        import matplotlib.pyplot as plt
        for root in BASES:
            ctx = plotfig.Context(root)
            for name, (_, fn, _) in plotfig.FIGURES.items():
                with self.subTest(base=root.name, figure=name):
                    try:
                        fig, info = fn(ctx)
                    except LookupError:
                        continue        # pas de run d'éval, ou pas de données : figure ignorée
                    self.assertIn("sources", info)
                    plt.close(fig)

    def test_empty_figures_are_skipped(self):
        from lib import plotfig
        ctx = plotfig.Context(STAGE)     # aucune ligne fps + power_w, aucun FPGA
        for fn in (plotfig.fig_bench_fps_power, plotfig.fig_bench_fpga_resources):
            with self.assertRaises(LookupError):
                fn(ctx)



class TestAutoRefresh(unittest.TestCase):
    """lib/plotrun : régénération des figures périmées après un changement de la base."""

    def _base(self, d, plot=None):
        import shutil
        root = Path(d)
        cfg = json.loads((STAGE / "base.json").read_text())
        if plot is not None:
            cfg["plot"] = plot
        (root / "base.json").write_text(json.dumps(cfg))
        shutil.copy(STAGE / "benchmarks.csv", root / "benchmarks.csv")
        (root / "papers").mkdir()
        return root

    def test_auto_enabled(self):
        from lib import plotrun
        with tempfile.TemporaryDirectory() as d:
            root = self._base(d)
            self.assertFalse(plotrun.auto_enabled(root, env={})[0])        # pas de manifest
            self.assertEqual(plotrun.auto_refresh(root, env={}), ([], []))  # et pas de bruit
            (root / "figures").mkdir()
            (root / "figures" / "manifest.json").write_text("{}")
            self.assertTrue(plotrun.auto_enabled(root, env={})[0])
            self.assertFalse(plotrun.auto_enabled(root, env={"PDB_NO_PLOT": "1"})[0])
        with tempfile.TemporaryDirectory() as d:
            root = self._base(d, plot={"auto": False})
            (root / "figures").mkdir()
            (root / "figures" / "manifest.json").write_text("{}")
            ok, why = plotrun.auto_enabled(root, env={})
            self.assertFalse(ok)
            self.assertIn("plot.auto", why)
            lines, notes = plotrun.auto_refresh(root, groups=("bench",), env={})
            self.assertEqual(lines, [])
            self.assertIn("plot --stale", notes[0])

    @unittest.skipUnless(HAS_MPL, "matplotlib absent (requirements-plot.txt)")
    def test_refresh_only_stale_groups(self):
        import os
        import time
        from lib import plotrun
        with tempfile.TemporaryDirectory() as d:
            root = self._base(d)
            (root / "figures").mkdir()
            (root / "figures" / "manifest.json").write_text("{}")
            lines, notes = plotrun.auto_refresh(root, groups=("bench",), env={})
            self.assertTrue(lines[0].startswith("Figures :"), lines)
            self.assertTrue((root / "figures" / "bench_quantization.png").exists())
            self.assertEqual(plotrun.stale(root, ("bench",)), {})          # rien à refaire
            self.assertNotIn("bench_fpga_resources", plotrun.load_manifest(root / "figures"))
            later = time.time() + 30                                      # nouvel article
            os.utime(root / "benchmarks.csv", (later, later))
            self.assertIn("bench_quantization", plotrun.stale(root, ("bench",)))
            self.assertTrue(all(n.startswith("bench_") for n in plotrun.stale(root, ("bench",))))

    def test_plot_auto_validated(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "base.json").write_text(json.dumps({"name": "x", "axes": {"a": "A"},
                                                           "plot": {"auto": "oui"}}))
            with self.assertRaises(ValueError):
                base.load_config(d)


if __name__ == "__main__":
    unittest.main()
