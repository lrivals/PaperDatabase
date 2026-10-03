import csv
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib import base, bases, registry, schema, xbase  # noqa: E402


def make_base(root, cfg):
    root = Path(root)
    (root / "papers").mkdir(parents=True)
    (root / "base.json").write_text(json.dumps(cfg))
    with open(root / "benchmarks.csv", "w", newline="") as f:
        csv.writer(f, lineterminator="\n").writerow(schema.BENCHMARK_COLUMNS)
    return root


def add_paper(root, pid, title, abstract="", refs=(), doi=None, arxiv_id=None, axes=(), fiche="done",
              year=2024):
    d = Path(root, "papers", pid)
    d.mkdir()
    meta = {**schema.new_metadata(pid), "title": title, "year": year, "doi": doi, "arxiv_id": arxiv_id,
            "axes": list(axes), "status": {"extracted": True, "fiche": fiche},
            "extraction": {"backend": "grobid", "ok": True, "warnings": []}}
    (d / "metadata.json").write_text(json.dumps(meta))
    (d / "sections.jsonl").write_text(json.dumps({"id": f"{pid}#000", "paper_id": pid, "kind": "abstract",
                                                  "text": abstract}) + "\n")
    (d / "refs.jsonl").write_text("".join(json.dumps({"paper_id": pid, "raw": r["title"], "authors": [],
                                                      "year": r.get("year"), "doi": r.get("doi"),
                                                      "arxiv_id": r.get("arxiv_id"), "title": r["title"]})
                                          + "\n" for r in refs))
    (d / "paper.pdf").write_bytes(b"%PDF-1.4 test")
    (d / "fiche.md").write_text(f"---\nid: {pid}\nfiche: {fiche}\ndate: 2026-01-01\n---\n\n# {title}\n\n"
                                "## Statut de lecture\n\nlu\n")
    return d


FPGA = {"name": "fpga", "axes": {"surveys": "S", "yolo-fpga": "Y", "ae": "AE"},
        "axis_rules": {"yolo-fpga": r"\byolo", "ae": "autoencoder"}}
DRONE = {"name": "drone", "axes": {"surveys": "S", "drone": "D", "det-fpga": "F"},
         "axis_rules": {"drone": r"\b(?:uav|drone)", "det-fpga": r"\bFPGA"},
         "topic_re": r"\b(?:uav|drone|FPGA)", "topic_min_hits": 1}

ZHANG = "Optimizing FPGA-based Accelerator Design for Deep Convolutional Neural Networks"
HLS = "A codesign workflow for low-power FPGA inference in drones"
AE = "Convolutional autoencoder accelerator for anomaly detection in particle physics"
RESNET = "Deep residual learning for image recognition in large scale settings"


class TwoBases(unittest.TestCase):
    """Fixture : une base « fpga » (source) et une base « drone » (cible)."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        t = Path(self.tmp.name)
        self.env = {"PDB_REGISTRY": str(t / "reg.json")}
        self.fpga = make_base(t / "fpga", FPGA)
        self.drone = make_base(t / "drone", DRONE)
        add_paper(self.fpga, "2015-zhang-optimizing-fpga", ZHANG, "CNN accelerator on FPGA.",
                  doi="10.1145/2684746.2689060", refs=[{"title": RESNET, "year": 2016}])
        add_paper(self.fpga, "2021-x-codesign-workflow-low", HLS, "FPGA inference for UAV and drone.",
                  arxiv_id="2103.05579", refs=[{"title": RESNET, "year": 2016}])
        add_paper(self.fpga, "2021-y-convolutional-autoencoder", AE, "An autoencoder on custom hardware.", axes=["ae"])
        add_paper(self.fpga, "2020-shared-yolo-drone-paper", "YOLO for drone detection on embedded FPGA",
                  "yolo drone", doi="10.1/shared", axes=["yolo-fpga"])
        # la cible cite Zhang (par DOI) et ResNet ; elle possède déjà le papier « shared » (DOI identique)
        add_paper(self.drone, "2024-a-uav-detector-fpga", "Tiny UAV detector on FPGA", "uav fpga",
                  refs=[{"title": ZHANG, "doi": "10.1145/2684746.2689060", "year": 2015},
                        {"title": RESNET, "year": 2016}, {"title": RESNET, "year": 2016}])
        add_paper(self.drone, "2024-b-shared-copy", "YOLO for drone detection on embedded FPGAs",
                  doi="10.1/SHARED")
        with open(self.fpga / "benchmarks.csv", "a", newline="") as f:
            w = csv.DictWriter(f, fieldnames=schema.BENCHMARK_COLUMNS, lineterminator="\n")
            w.writerow({c: "n/r" for c in schema.BENCHMARK_COLUMNS} | {
                "paper_id": "2015-zhang-optimizing-fpga", "model": "AlexNet", "confidence": "high"})

    def tearDown(self):
        self.tmp.cleanup()


class XBaseTest(TwoBases):
    def test_matcher_doi_arxiv_title(self):
        m = xbase.Matcher([("p", {"doi": "10.1/ABC", "arxiv_id": "2101.00001v2", "title": ZHANG, "year": 2015})])
        self.assertEqual(m.find({"doi": "10.1/abc"}), "p")
        self.assertEqual(m.find({"arxiv_id": "2101.00001"}), "p")
        self.assertEqual(m.find({"title": ZHANG.lower() + ".", "year": 2016}), "p")
        # titre voisin (non identique) : l'année départage, comme dans lib/refs.py
        self.assertEqual(m.find({"title": ZHANG + " on chips", "year": 2016}), "p")
        self.assertIsNone(m.find({"title": ZHANG + " on chips", "year": 2020}))

    def test_scan_kinds(self):
        rows = xbase.scan(self.drone, [("fpga", self.fpga)])
        by_id = {r["paper_id"]: r for r in rows if r["paper_id"]}
        self.assertEqual(by_id["2015-zhang-optimizing-fpga"]["kind"], "cited_here")
        self.assertEqual(by_id["2015-zhang-optimizing-fpga"]["n_citers_target"], 1)
        self.assertEqual(by_id["2021-x-codesign-workflow-low"]["kind"], "in_base")
        self.assertNotIn("2021-y-convolutional-autoencoder", by_id)   # hors des règles de la cible
        self.assertNotIn("2020-shared-yolo-drone-paper", by_id)       # déjà dans la cible
        ext = [r for r in rows if r["kind"] == "ref_elsewhere"]
        self.assertEqual([r["title"] for r in ext], [RESNET])        # cité ici (1) et là-bas (2)
        self.assertEqual(rows[0]["kind"], "cited_here")

    def test_scan_without_rules_lists_everything(self):
        t = make_base(Path(self.tmp.name) / "empty", {"name": "vide", "axes": {"surveys": "S"}})
        rows = xbase.scan(t, [("fpga", self.fpga)], kinds=("in_base",))
        self.assertEqual(len(rows), 4)

    def test_import(self):
        r = xbase.import_paper(self.fpga, "2015-zhang-optimizing-fpga", self.drone, "fpga")
        self.assertEqual(r["benchmarks"], 1)
        d = self.drone / "papers" / "2015-zhang-optimizing-fpga"
        meta = json.loads((d / "metadata.json").read_text())
        self.assertEqual(meta["axes"], ["det-fpga"])                 # reclassé selon la cible
        self.assertEqual(meta["status"]["fiche"], "todo")
        self.assertEqual(meta["imported_from"]["base"], "fpga")
        self.assertEqual(meta["imported_from"]["fiche"], "done")
        fiche = (d / "fiche.md").read_text()
        self.assertEqual(schema.read_front_matter(fiche)["fiche"], "todo")
        self.assertIn("Importée de la base `fpga`", fiche)
        self.assertTrue((d / "paper.pdf").exists())
        # schema.AXES est celui de la base active, pas de la cible : seuls ces écarts-là sont admis
        self.assertEqual([e for e in schema.validate_metadata(meta) if not e.startswith("axe inconnu")], [])
        with self.assertRaises(xbase.ImportError_):
            xbase.import_paper(self.fpga, "2015-zhang-optimizing-fpga", self.drone, "fpga")
        with self.assertRaises(xbase.ImportError_):   # même article sous un autre id (DOI)
            xbase.import_paper(self.fpga, "2020-shared-yolo-drone-paper", self.drone, "fpga")
        xbase.import_paper(self.fpga, "2021-y-convolutional-autoencoder", self.drone, "fpga", with_pdf=False)
        self.assertFalse((self.drone / "papers" / "2021-y-convolutional-autoencoder" / "paper.pdf").exists())
        # une ligne de benchmark n'est copiée qu'une fois
        with open(self.drone / "benchmarks.csv", newline="") as f:
            self.assertEqual(sum(1 for _ in csv.DictReader(f)), 1)

    def test_import_into_wider_header(self):
        # la cible a des colonnes optionnelles : la ligne copiée garde l'alignement, n/r ailleurs
        with open(self.drone / "benchmarks.csv", "w", newline="") as f:
            csv.writer(f, lineterminator="\n").writerow([*schema.BENCHMARK_COLUMNS, "chunk_id", "batch"])
        xbase.import_paper(self.fpga, "2015-zhang-optimizing-fpga", self.drone, "fpga")
        with open(self.drone / "benchmarks.csv", newline="") as f:
            reader = csv.DictReader(f)
            self.assertEqual(schema.check_header(reader.fieldnames), [])
            rows = list(reader)
        self.assertEqual(len(rows), 1)
        self.assertEqual((rows[0]["model"], rows[0]["chunk_id"], rows[0]["batch"]), ("AlexNet", "n/r", "n/r"))
        self.assertEqual(schema.validate_benchmark_row(rows[0]), [])

    def test_find_elsewhere(self):
        registry.register("fpga", self.fpga, self.env)
        registry.register("drone", self.drone, self.env)
        self.assertEqual(xbase.find_elsewhere({"arxiv_id": "2103.05579v1"}, self.drone, self.env),
                         [("fpga", "2021-x-codesign-workflow-low")])
        self.assertEqual(xbase.find_elsewhere({"arxiv_id": "2103.05579"}, self.fpga, self.env), [])


class BasesTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.env = {"PDB_REGISTRY": str(self.dir / "reg.json")}

    def tearDown(self):
        self.tmp.cleanup()

    def test_create(self):
        root = bases.create("anomalies", "Anomalies sur images industrielles.", self.dir / "A",
                            title="Anomalies", env=self.env, reindex_after=False)
        self.assertEqual(registry.resolve("anomalies", self.env), root)
        cfg = base.load_config(root)
        self.assertEqual(cfg["name"], "Anomalies")
        for f in ("CLAUDE.md", "profile.md", "gaps.md", "labs.md", ".gitignore", "benchmarks.csv"):
            self.assertTrue((root / f).is_file(), f)
        for link in ("bin", ".venv", ".claude/commands"):
            self.assertTrue((root / link).is_symlink(), link)
        self.assertEqual((root / "bin").resolve(), base.CODE / "bin")
        self.assertNotIn("{", (root / "CLAUDE.md").read_text().split("\n")[0])
        self.assertEqual(bases.theme(root), "Anomalies sur images industrielles.")
        self.assertEqual(bases.pending_suggestions(root), [])
        with self.assertRaises(bases.BaseError):          # nom déjà pris
            bases.create("anomalies", "x", self.dir / "B", env=self.env, reindex_after=False)
        with self.assertRaises(bases.BaseError):          # dossier non vide
            bases.create("autre", "x", root, env=self.env, reindex_after=False)
        with self.assertRaises(bases.BaseError):          # thème vide
            bases.create("autre", "  ", self.dir / "C", env=self.env, reindex_after=False)

    def test_suggestions_and_check(self):
        root = make_base(self.dir / "D", DRONE)
        (root / "profile.md").write_text("# P\n\n## Thème (utilisateur)\n\nDrones.\n\n"
                                         "## Suggestions en attente\n\n<!-- aide -->\n"
                                         "- 2026-09-28 (x) — axe tracking — 3 papiers\n\n## Historique\n\n- a\n")
        self.assertEqual(bases.pending_suggestions(root), ["- 2026-09-28 (x) — axe tracking — 3 papiers"])
        add_paper(root, "2024-a-uav-detector-fpga", "Tiny UAV detector on FPGA", "uav fpga", axes=["drone"])
        add_paper(root, "2024-c-cooking-recipes-for", "Cooking recipes for students", "pasta")
        r = bases.check(root)
        self.assertEqual(r["errors"], [])
        self.assertEqual([c[0] for c in r["changes"]], ["2024-a-uav-detector-fpga"])
        self.assertEqual(r["out_of_topic"], ["2024-c-cooking-recipes-for"])
        s = bases.stats("d", root)
        self.assertEqual((s["papers"], s["done"], s["suggestions"]), (2, 2, 1))


try:
    from lib import vizbases
except ImportError:  # requirements-viz.txt absent
    vizbases = None


@unittest.skipIf(vizbases is None, "requirements-viz.txt non installé")
class VizBasesTest(TwoBases):
    def test_scan_rows_and_import(self):
        registry.register("fpga", self.fpga, self.env)
        rows = xbase.scan(self.drone, [("fpga", self.fpga)])
        data = vizbases.scan_rows(rows)
        self.assertEqual(data[0]["ident"], "fpga:2015-zhang-optimizing-fpga")
        ext = next(i for i, r in enumerate(rows) if r["kind"] == "ref_elsewhere")
        with mock.patch.dict(os.environ, self.env):
            done, msgs = vizbases.run_import(rows, [0, ext], self.drone)
        self.assertEqual([d["paper_id"] for d in done], ["2015-zhang-optimizing-fpga"])
        self.assertEqual(len(msgs), 1)
        self.assertIn("absent de toutes les bases", msgs[0])

    def test_profile_panel_hides_comments(self):
        (self.drone / "profile.md").write_text("# P\n\n## Thème (utilisateur)\n\nx\n\n"
                                               "## Suggestions en attente\n\n<!-- aide -->\n")
        text = json.dumps(vizbases.profile_panel(self.drone), default=lambda c: c.to_plotly_json())
        self.assertNotIn("aide", text)


if __name__ == "__main__":
    unittest.main()
