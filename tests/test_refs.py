"""Tests du rapprochement des références (lib/refs.py) et de external_refs.csv.

.venv/bin/python -m unittest discover tests
"""
import csv
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from lib import refs  # noqa: E402


def _paper(pid, title, year=2024, arxiv_id=None, refs_=()):
    return {"id": pid, "title": title, "year": year, "arxiv_id": arxiv_id, "doi": None,
            "refs": list(refs_)}


def _ref(title, year=2016, **kw):
    return {"title": title, "year": year, "raw": title, **kw}


class TestSameTitle(unittest.TestCase):
    def w(self, t):
        return refs.title_words(t)

    def test_lost_ligature(self):
        self.assertTrue(refs.same_title(self.w("Efficient processing of deep neural networks: a tutorial"),
                                        self.w("E cient Processing of Deep Neural Networks: A Tutorial")))

    def test_truncated_title(self):
        self.assertTrue(refs.same_title(self.w("Framework TDR for the LHCb Upgrade II"),
                                        self.w("Framework TDR for the LHCb Upgrade II: Opportunities in flavour physics")))

    def test_distinct_titles(self):
        self.assertFalse(refs.same_title(
            self.w("fpgaConvNet: A Framework for Mapping Convolutional Neural Networks on FPGAs"),
            self.w("fpgaConvNet: Mapping Regular and Irregular Convolutional Neural Networks on FPGAs")))
        self.assertFalse(refs.same_title(
            self.w("FINN: A Framework for Fast, Scalable Binarized Neural Network Inference"),
            self.w("FINN-R: An End-to-End Deep-Learning Framework for Fast Exploration of Quantized Neural Networks")))

    def test_short_titles_never_fuzzy(self):
        self.assertFalse(refs.same_title(self.w("Deep learning"), self.w("Deep learnin")))

    def test_best_title(self):
        self.assertEqual(refs.best_title(["Ca e: Convolutional architecture", "Caffe: Convolutional architecture"]),
                         "Caffe: Convolutional architecture")


class TestGroupRefs(unittest.TestCase):
    CAFFE = "Caffe: Convolutional Architecture for Fast Feature Embedding"

    def setUp(self):
        self.papers = [
            _paper("pa", "Alpha: Quantized YOLO Detection on Edge FPGAs", arxiv_id="2401.00001", refs_=[
                _ref(self.CAFFE, 2014),
                _ref("fpgaConvNet: A Framework for Mapping Convolutional Neural Networks on FPGAs", 2016),
                _ref("Batch normalization: accelerating deep network training", 2015),
            ]),
            _paper("pb", "Beta: Convolutional Autoencoders for Anomaly Detection", refs_=[
                _ref("Ca e: Convolutional Architecture for Fast Feature Embedding", 2014),
                _ref("fpgaConvNet: Mapping Regular and Irregular Convolutional Neural Networks on FPGAs", 2019),
                _ref("Batch normalisation: accelerating deep network training", 2021),   # autre année
                _ref("Alpha: Quantized YOLO Detecton on Edge FPGA", 2024),                # coquille → corpus
            ]),
            _paper("pc", "Gamma: Continual Learning with Hyperdimensional Computing", refs_=[
                _ref("Caffe: convolutional architecture for fast feature embedding.", None),
            ]),
        ]
        self.cites, self.groups = refs.group_refs(self.papers)

    def test_fuzzy_merge_and_display_title(self):
        caffe = [g for g in self.groups.values() if g["title"] == self.CAFFE]
        self.assertEqual(len(caffe), 1)
        citers = refs.citers_of(self.cites)
        gid = next(k for k, g in self.groups.items() if g["title"] == self.CAFFE)
        self.assertEqual(citers[gid], {"pa", "pb", "pc"})

    def test_distinct_publications_stay_apart(self):
        titles = [g["title"] for g in self.groups.values()]
        self.assertEqual(sum(t.startswith("fpgaConvNet") for t in titles), 2)
        self.assertEqual(sum(t.lower().startswith("batch normali") for t in titles), 2)

    def test_fuzzy_corpus_citation(self):
        self.assertIn("pa", self.cites["pb"])

    def test_ranking(self):
        rows = refs.external_ranking(self.papers)
        self.assertEqual([r["title"] for r in rows], [self.CAFFE])
        self.assertEqual(rows[0]["citers"], "pa;pb;pc")
        self.assertEqual(rows[0]["rank"], 1)


class TestCitations(unittest.TestCase):
    def test_cites_and_cited_by(self):
        b = _paper("b", "Binarized networks on reconfigurable hardware made fast", 2016,
                   arxiv_id="1612.07119")
        a = _paper("a", "Paper A about things", refs_=[
            _ref("whatever", arxiv_id="1612.07119v2"),
            _ref("An external work cited by two papers")])
        c = _paper("c", "Paper C about other things", refs_=[
            _ref("Binarized networks on reconfigurable hardware made"),   # titre tronqué, 6 mots
            _ref("An external work cited by two papers")])
        cites, citers, groups = refs.citations([a, b, c])
        self.assertIn("b", cites["a"])
        self.assertIn("b", cites["c"])
        self.assertEqual(citers["b"], {"a", "c"})
        (ext,) = groups
        self.assertEqual(citers[ext], {"a", "c"})
        self.assertNotIn("b", cites)


class TestExternalCsv(unittest.TestCase):
    def test_write_external(self):
        spec = importlib.util.spec_from_file_location("reindex", ROOT / "bin" / "reindex.py")
        reindex = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(reindex)
        rows = [{"rank": 1, "n_citers": 2, "title": "A, B: comma title", "year": None,
                 "arxiv_id": None, "doi": "10.1/x", "citers": "pa;pb"}]
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "external_refs.csv"
            reindex.write_external(path, rows)
            with open(path, newline="") as f:
                out = list(csv.DictReader(f))
        self.assertEqual(out[0]["title"], "A, B: comma title")
        self.assertEqual(out[0]["year"], "n/r")
        self.assertEqual(tuple(out[0]), refs.EXTERNAL_FIELDS)


if __name__ == "__main__":
    unittest.main()
