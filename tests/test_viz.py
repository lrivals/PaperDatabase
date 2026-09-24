"""Tests des figures et du panneau de détail (lib/vizfig.py), sans lancer le serveur Dash.

.venv/bin/python -m unittest discover tests      # requiert requirements-viz.txt
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    from lib import graph, lineage, vizfig
    from test_lineage import YOLO1, ext_id, write_corpus
except ImportError:  # dépendances de visualisation absentes
    vizfig = None


def _text(component):
    """Tout le texte d'un arbre de composants Dash."""
    return json.dumps(component, default=lambda c: c.to_plotly_json(), ensure_ascii=False)


@unittest.skipIf(vizfig is None, "requirements-viz.txt non installé")
class TestViz(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.tmp.name)
        write_corpus(cls.root)
        cls.G = graph.build(cls.root)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_make_figure_filters_and_selection(self):
        keep = self.G.filter_ids(years=[2018, 2024])
        self.assertEqual(keep, {"p2", "p3", "p4", "p5"})       # p5 : année n/r, conservé
        fig = vizfig.make_figure(self.G, "axis", None, list(graph.LINK_TYPES), 0.0, "force",
                                 True, keep, "p4", True)
        shown = {c for t in fig.data if t.customdata is not None for c in t.customdata}
        self.assertNotIn("p1", shown)
        self.assertIn("p4", shown)
        self.assertEqual(fig.data[-1].name, "sélection")

    def test_focus_dims_unrelated_links(self):
        links = self.G.links_for(["citation"])
        focus = vizfig.focus_set(self.G.visible_nodes(), links, None, "p1")
        self.assertEqual(focus, {"p1", "p2", "p5"})            # p1 et ses voisins directs
        traces = vizfig.link_traces(links, self.G.force_positions(["citation"]), focus)
        self.assertIn(vizfig.DIM_LINK, [t.opacity for t in traces])   # p3 → p4 estompé

    def test_lineage_figure(self):
        L = lineage.build(self.G, subject="binar", infer_threshold=0.2)
        fig = vizfig.lineage_figure(L, selected="p4")
        n_cit = sum(1 for e in L["edges"] if e["kind"] == "citation")
        self.assertEqual(len(fig.layout.annotations), len(L["edges"]))
        self.assertGreater(n_cit, 0)
        self.assertEqual(list(fig.layout.xaxis.ticktext), [t for _, t in L["ticks"]])
        names = [t.name for t in fig.data]
        self.assertTrue(any("déduite" in (n or "") for n in names))
        empty = vizfig.lineage_figure(lineage.build(self.G))
        self.assertEqual(len(empty.data), 0)

    def test_details_paper(self):
        s = _text(vizfig.details(self.G, "p1", self.root))
        self.assertIn("Fiche de lecture", s)
        self.assertIn("## Problème", s)
        self.assertNotIn("fiche: done", s)                    # front-matter retiré
        self.assertIn("12000", s)                              # tableau de benchmarks
        self.assertIn("confidence low", s)
        self.assertIn("Fiche non rédigée", _text(vizfig.details(self.G, "p2", self.root)))

    def test_details_external(self):
        s = _text(vizfig.details(self.G, ext_id(self.G, YOLO1), self.root))
        self.assertIn("/paper-add 1506.02640", s)
        self.assertIn("arxiv.org/abs/1506.02640", s)
        self.assertIn("rang 1", s)
        self.assertIn("Cliquer", _text(vizfig.details(self.G, None, self.root)))

    def test_short_labels(self):
        self.assertEqual(vizfig.short({"kind": "paper", "authors": "n/r", "year": None}), "?")
        self.assertEqual(vizfig.short({"kind": "paper", "authors": "", "year": 2020}), "? 2020")
        self.assertEqual(vizfig.short({"kind": "paper", "authors": "Umuroglu", "year": 2017}),
                         "Umuroglu 2017")
        self.assertTrue(vizfig.short({"kind": "external", "title": "x" * 40}).endswith("…"))


if __name__ == "__main__":
    unittest.main()
