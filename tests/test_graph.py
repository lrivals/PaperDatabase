"""Tests du graphe de corpus (lib/graph.py) sur un mini-corpus synthétique.

.venv/bin/python -m unittest discover tests      # requiert requirements-viz.txt
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

try:
    import numpy as np
    from lib import graph
except ImportError:  # dépendances de visualisation absentes
    graph = None


def _paper(pid, title, arxiv_id=None, doi=None, axes=(), tags=(), text=""):
    return {"id": pid, "title": title, "authors": [{"given": "A", "family": pid}], "year": 2024,
            "venue": None, "doi": doi, "arxiv_id": arxiv_id, "url": None, "type": "preprint",
            "axes": list(axes), "tags": list(tags), "added": "2026-09-24",
            "extraction": {"backend": "grobid", "ok": True, "warnings": []},
            "status": {"extracted": True, "fiche": "todo"}}, text


SHARED_1 = {"title": "FINN: A Framework for Fast Scalable Binarized Inference", "arxiv_id": "1612.07119"}
SHARED_2 = {"title": "Deep Residual Learning for Image Recognition", "doi": "10.1109/CVPR.2016.90"}
ONLY_C = {"title": "A Reference Cited By Only One Paper Here", "arxiv_id": "2001.00001"}


@unittest.skipIf(graph is None, "requirements-viz.txt non installé")
class TestGraph(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        root = Path(cls.tmp.name)
        corpus = {
            "pa": (_paper("pa", "Alpha: Quantized YOLO Detection on Edge FPGAs", arxiv_id="2401.00001",
                          axes=["yolo-fpga"], tags=["yolov5", "kv260"],
                          text="yolo detection fpga quantization int8 accelerator"),
                   [SHARED_1, SHARED_2]),
            "pb": (_paper("pb", "Beta: Convolutional Autoencoders for Anomaly Detection", doi="10.1/beta",
                          axes=["autoencoder-fpga"], tags=["hls4ml"],
                          text="autoencoder anomaly detection hls4ml latency"),
                   [SHARED_1, SHARED_2, {"title": "Alpha - Quantized YOLO detection on edge FPGAs!"}]),
            "pc": (_paper("pc", "Gamma: Continual Learning with Hyperdimensional Computing",
                          axes=["continual-learning"], tags=["hdc", "kv260"],
                          text="continual learning hyperdimensional replay"),
                   [{"title": "x", "arxiv_id": "2401.00001v2"}, {"doi": "10.1/BETA"}, SHARED_1, ONLY_C]),
        }
        for pid, ((meta, text), refs) in corpus.items():
            d = root / "papers" / pid
            d.mkdir(parents=True)
            (d / "metadata.json").write_text(json.dumps(meta))
            (d / "sections.jsonl").write_text(json.dumps({"kind": "section", "text": text}) + "\n")
            (d / "refs.jsonl").write_text("".join(json.dumps(r) + "\n" for r in refs))
        cls.g = graph.build(root)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def links(self, type_):
        return {(l["source"], l["target"]): l for l in self.g.links
                if l["type"] == type_ and not l["external"]}

    def test_citations_by_arxiv_doi_and_title(self):
        cit = self.links("citation")
        self.assertIn(("pc", "pa"), cit)   # arXiv id, suffixe de version ignoré
        self.assertIn(("pc", "pb"), cit)   # DOI, casse ignorée
        self.assertIn(("pb", "pa"), cit)   # titre normalisé (ponctuation, casse)
        self.assertEqual(len(cit), 3)

    def test_coupling_weight(self):
        # pa cite {S1, S2} ; pb cite {S1, S2, pa} → 2 / √(2·3)
        w = self.links("coupling")[("pa", "pb")]["weight"]
        self.assertAlmostEqual(w, 2 / 6 ** 0.5)

    def test_themes(self):
        th = self.links("themes")
        self.assertIn(("pa", "pc"), th)          # tag kv260 commun
        self.assertNotIn(("pa", "pb"), th)

    def test_external_nodes(self):
        ext = {n["title"]: n for n in self.g.nodes.values() if n["kind"] == "external"}
        self.assertEqual(ext[SHARED_1["title"]]["citers"], ["pa", "pb", "pc"])
        self.assertIn(SHARED_2["title"], ext)
        self.assertNotIn(ONLY_C["title"], ext)   # cité une seule fois
        self.assertEqual(len(ext), 2)

    def test_text_threshold(self):
        all_text = self.g.links_for(["text"], 0.0)
        self.assertTrue(all(0 < l["weight"] <= 1 for l in all_text))
        self.assertEqual(self.g.links_for(["text"], 1.01), [])

    def test_positions_finite(self):
        for pos, n in ((self.g.semantic_positions(True), 5),
                       (self.g.force_positions(graph.LINK_TYPES, 0.0, True), 5),
                       (self.g.force_positions([], 0.0, False), 3)):
            self.assertEqual(len(pos), n)
            for v in pos.values():
                self.assertEqual(len(v), 3)
                self.assertTrue(np.isfinite(v).all())


if __name__ == "__main__":
    unittest.main()
