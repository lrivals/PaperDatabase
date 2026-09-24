"""Tests de la généalogie (lib/lineage.py) sur un mini-corpus synthétique daté.

.venv/bin/python -m unittest discover tests      # requiert requirements-viz.txt

Chaîne de citations : p1 (2016) ← p2 (2018) ← p3 (2020) ← p4 (2024) ; p5 (année n/r) cite p1.
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

try:
    from lib import graph, lineage
except ImportError:  # dépendances de visualisation absentes
    graph = None

YOLO1 = {"title": "You Only Look Once: Unified, Real-Time Object Detection", "year": 2016,
         "arxiv_id": "1506.02640"}
YOLO3 = {"title": "YOLOv3: An Incremental Improvement", "year": 2018, "arxiv_id": "1804.02767"}
SINGLE = {"title": "A Reference Cited Only By The First Paper", "year": 2015}


def _meta(pid, title, year, arxiv_id, tags=(), fiche="todo"):
    return {"id": pid, "title": title, "authors": [{"given": "A", "family": pid.upper()}],
            "year": year, "venue": None, "doi": None, "arxiv_id": arxiv_id, "url": None,
            "type": "preprint", "axes": ["toolflows"], "tags": list(tags),
            "added": "2026-09-24", "extraction": {"backend": "grobid", "ok": True, "warnings": []},
            "status": {"extracted": True, "fiche": fiche}}


def ref(meta):
    return {"title": meta["title"], "year": meta["year"], "arxiv_id": meta["arxiv_id"]}


CORPUS = {
    "p1": (_meta("p1", "FINN: Fast Scalable Binarized Neural Network Inference", 2016, "1612.00001",
                 tags=["bnn"], fiche="done"),
           "binarized neural network fpga inference dataflow streaming",
           [YOLO1, SINGLE]),
    "p2": (_meta("p2", "FINN-R: An End-to-End Deep-Learning Framework", 2018, "1809.00002"),
           "quantized dataflow framework fpga exploration",
           ["p1", YOLO1]),
    "p3": (_meta("p3", "Mixed Precision Quantization for Edge Accelerators", 2020, "2001.00003"),
           "mixed precision quantization accelerator edge",
           ["p2"]),
    "p4": (_meta("p4", "Binarized YOLO Detection on Edge FPGAs", 2024, "2401.00004", tags=["bnn"]),
           "binarized neural network fpga inference yolo detection streaming",
           ["p3", YOLO1, YOLO3]),
    "p5": (_meta("p5", "Binarized Inference Without a Known Year", None, "2501.00005"),
           "binarized network",
           ["p1"]),
}


def write_corpus(root, fiche_text="---\nid: p1\nfiche: done\n---\n\n# FINN\n\n## Problème\n\nTexte."):
    metas = {pid: m for pid, (m, _, _) in CORPUS.items()}
    for pid, (meta, text, refs) in CORPUS.items():
        d = Path(root) / "papers" / pid
        d.mkdir(parents=True)
        (d / "metadata.json").write_text(json.dumps(meta))
        (d / "sections.jsonl").write_text(json.dumps({"kind": "section", "text": text}) + "\n")
        lines = [ref(metas[r]) if isinstance(r, str) else r for r in refs]
        (d / "refs.jsonl").write_text("".join(json.dumps(l) + "\n" for l in lines))
    (Path(root) / "papers" / "p1" / "fiche.md").write_text(fiche_text)
    (Path(root) / "benchmarks.csv").write_text(
        "paper_id,model,platform,quantization,fps,latency_ms,power_w,source_section,confidence\n"
        "p1,BNN,ZC706,1-bit,12000,n/r,n/r,Table 2,high\n"
        "p1,BNN-large,ZC706,1-bit,n/r,n/r,n/r,Table 3,low\n")


def ext_id(G, meta):
    return next(gid for gid, g in G.groups.items() if g["title"] == meta["title"])


@unittest.skipIf(graph is None, "requirements-viz.txt non installé")
class TestLineage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        write_corpus(cls.tmp.name)
        cls.G = graph.build(cls.tmp.name)
        cls.y1, cls.y3, cls.single = (ext_id(cls.G, m) for m in (YOLO1, YOLO3, SINGLE))

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_groups_cover_single_citations(self):
        self.assertIn(self.single, self.G.groups)
        self.assertNotIn(self.single, self.G.nodes)          # pas un nœud du graphe 3D
        self.assertEqual(self.G.node(self.single)["citers"], ["p1"])

    def test_from_paper_depth(self):
        role = lineage.from_paper(self.G, "p2", depth=1)
        self.assertEqual(role["p2"], "root")
        self.assertEqual(role["p1"], "ancestor")
        self.assertEqual(role[self.y1], "ancestor")
        self.assertEqual(role["p3"], "descendant")
        self.assertNotIn("p4", role)
        self.assertEqual(lineage.from_paper(self.G, "p2", depth=2)["p4"], "descendant")

    def test_from_paper_externals(self):
        # références directes : toutes, même citées une fois
        self.assertIn(self.single, lineage.from_paper(self.G, "p1", depth=1))
        # plus loin : seulement les externes co-citées
        role = lineage.from_paper(self.G, "p3", depth=2)
        self.assertIn(self.y1, role)
        self.assertNotIn(self.single, role)

    def test_subject_regex_and_intermediates(self):
        role = lineage.from_subject(self.G, "binar", intermediates=True)
        self.assertEqual({k for k, v in role.items() if v == "match"}, {"p1", "p4", "p5"})
        self.assertEqual({k for k, v in role.items() if v == "intermediate"}, {"p2", "p3"})
        self.assertNotIn("p2", lineage.from_subject(self.G, "binar", intermediates=False))

    def test_subject_matches_externals_and_tags(self):
        m = lineage.matches_subject(self.G, "yolo|you only look once")
        self.assertEqual(m, {"p4", self.y1, self.y3})
        self.assertEqual(lineage.matches_subject(self.G, "tag:bnn"), {"p1", "p4"})
        self.assertEqual(lineage.matches_subject(self.G, "("), set())    # regex invalide

    def test_edges_citation_only_and_no_external_pairs(self):
        L = lineage.build(self.G, subject="yolo|you only look once", intermediates=False)
        pairs = {(e["source"], e["target"]) for e in L["edges"]}
        self.assertEqual(pairs, {(self.y1, "p4"), (self.y3, "p4")})
        self.assertTrue(all(e["kind"] == "citation" for e in L["edges"]))
        # avec intermédiaires : la chaîne p1 ← p2 ← p3 relie YOLOv1 à p4
        L = lineage.build(self.G, subject="yolo|you only look once")
        self.assertEqual({k for k, n in L["nodes"].items() if n["role"] == "intermediate"},
                         {"p1", "p2", "p3"})

    def test_inferred_edges(self):
        L = lineage.build(self.G, subject="binar", intermediates=False, infer_threshold=0.2)
        inferred = [e for e in L["edges"] if e["kind"] == "inferred"]
        self.assertTrue(inferred)
        for e in inferred:
            a, b = L["nodes"][e["source"]], L["nodes"][e["target"]]
            self.assertEqual((a["kind"], b["kind"]), ("paper", "paper"))
            self.assertLess(a["year"], b["year"])
            self.assertNotIn(frozenset((e["source"], e["target"])),
                             {frozenset((c["source"], c["target"]))
                              for c in L["edges"] if c["kind"] == "citation"})
        self.assertEqual(len({e["target"] for e in inferred}), len(inferred))   # ≤ 1 par papier
        self.assertFalse([e for e in lineage.build(self.G, subject="binar")["edges"]
                          if e["kind"] == "inferred"])                          # seuil 0 = off

    def test_layout(self):
        L = lineage.build(self.G, subject="binar")
        self.assertEqual(L["ticks"][0], (0, "n/r"))
        self.assertEqual([t for _, t in L["ticks"]], ["n/r", "2016", "2018", "2020", "2024"])
        self.assertAlmostEqual(L["pos"]["p5"][0], 0)
        self.assertLess(L["pos"]["p1"][0], L["pos"]["p4"][0])
        self.assertEqual(L["pos"], lineage.build(self.G, subject="binar")["pos"])  # déterministe

    def test_empty(self):
        L = lineage.build(self.G)
        self.assertEqual((L["nodes"], L["edges"], L["pos"], L["ticks"]), ({}, [], {}, []))


if __name__ == "__main__":
    unittest.main()
