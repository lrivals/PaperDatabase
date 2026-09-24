"""Tests des embeddings (lib/embed.py) et de leur branchement dans lib/graph.py.

L'encodeur est remplacé par une fonction déterministe : ces tests ne demandent pas
sentence-transformers (seulement numpy, et requirements-viz.txt pour la partie graphe).
"""
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    import numpy as np
    from lib import embed
except ImportError:
    embed = None
try:
    from lib import graph
    from test_lineage import write_corpus
except ImportError:
    graph = None


def fake_encode(texts, model):
    """Vecteur = présence de quelques mots-clés (+1 pour éviter le vecteur nul)."""
    words = ("binarized", "quantization", "yolo", "dataflow")
    return np.array([[float(w in t) for w in words] + [1.0] for t in texts])


@unittest.skipIf(embed is None, "numpy non installé")
class TestEmbed(unittest.TestCase):
    def test_chunks(self):
        self.assertEqual(embed.chunks("a b c d e", n=2), ["a b", "c d", "e"])
        self.assertEqual(embed.chunks(""), [""])

    def test_cache_reused(self):
        papers = [{"id": "a", "text": "binarized yolo"}, {"id": "b", "text": "quantization"}]
        with tempfile.TemporaryDirectory() as d, \
                mock.patch.object(embed, "_encode", side_effect=fake_encode) as enc:
            X = embed.embed_papers(papers, cache_dir=d)
            self.assertEqual(X.shape, (2, 5))
            np.testing.assert_allclose(np.linalg.norm(X, axis=1), 1.0)
            self.assertEqual(enc.call_count, 1)
            np.testing.assert_allclose(embed.embed_papers(papers, cache_dir=d), X)
            self.assertEqual(enc.call_count, 1)                # relu depuis le cache
            papers[1]["text"] = "dataflow"                     # texte modifié → recalcul
            embed.embed_papers(papers, cache_dir=d)
            self.assertEqual(enc.call_count, 2)
            self.assertEqual(len(enc.call_args[0][0]), 1)      # seul b est ré-encodé


@unittest.skipIf(graph is None, "requirements-viz.txt non installé")
class TestGraphSimilarity(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        write_corpus(self.tmp.name)
        self.G = graph.build(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_fallback_without_dependency(self):
        with mock.patch.object(embed, "available", return_value=False):
            self.assertEqual(self.G.set_similarity("embed"), "tfidf")

    def test_switch_to_embeddings(self):
        before = {(l["source"], l["target"]): l["weight"] for l in self.G.links_for(["text"])}
        with mock.patch.object(embed, "available", return_value=True), \
                mock.patch.object(embed, "_encode", side_effect=fake_encode):
            self.assertEqual(self.G.set_similarity("embed"), "embed")
        after = {(l["source"], l["target"]): l["weight"] for l in self.G.links_for(["text"])}
        self.assertNotEqual(before, after)
        self.assertTrue((Path(self.tmp.name) / ".cache" / "embeddings").is_dir())
        self.assertEqual(len(self.G.semantic_positions()), 5)
        self.G.set_similarity("tfidf")
        self.assertEqual(before, {(l["source"], l["target"]): l["weight"]
                                  for l in self.G.links_for(["text"])})


if __name__ == "__main__":
    unittest.main()
