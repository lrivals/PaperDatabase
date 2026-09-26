"""Tests de lib/openalex.py, bin/discover.py et de l'ajout par DOI / liste (bin/add.py),
sans réseau : les réponses OpenAlex sont simulées.

.venv/bin/python -m unittest discover tests
"""
import csv
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "bin"))

from lib import ids, openalex  # noqa: E402


def _load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "bin" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


discover = _load("discover")
add = _load("add")


def _work(wid, title, year=2022, doi=None, arxiv=None, venue="FPL", cited=10, refs_=(),
          abstract=None, related=()):
    locs = [{"landing_page_url": f"https://doi.org/{doi}" if doi else None, "pdf_url": None,
             "source": {"display_name": venue}}]
    if arxiv:
        locs.append({"landing_page_url": f"http://arxiv.org/abs/{arxiv}",
                     "pdf_url": f"https://arxiv.org/pdf/{arxiv}", "source": {"display_name": "arXiv"}})
    inv = {}
    for i, w in enumerate((abstract or "").split()):
        inv.setdefault(w, []).append(i)
    return {"id": f"https://openalex.org/{wid}", "doi": f"https://doi.org/{doi}" if doi else None,
            "title": title, "publication_year": year, "cited_by_count": cited,
            "primary_location": locs[0], "locations": locs,
            "best_oa_location": locs[-1] if arxiv else None,
            "abstract_inverted_index": inv or None,
            "referenced_works": [f"https://openalex.org/{r}" for r in refs_],
            "related_works": [f"https://openalex.org/{r}" for r in related]}


class TestWorkFields(unittest.TestCase):
    def test_arxiv_from_location_and_doi(self):
        w = _work("W1", "T", doi="10.1088/1748-0221/13/07/p07027", arxiv="1804.06913")
        self.assertEqual(openalex.arxiv_id_of(w), "1804.06913")
        self.assertEqual(openalex.doi_of(w), "10.1088/1748-0221/13/07/p07027")
        arx = {"id": "W2", "doi": "https://doi.org/10.48550/arxiv.2507.18174", "locations": []}
        self.assertEqual(openalex.arxiv_id_of(arx), "2507.18174")
        self.assertIsNone(openalex.doi_of(arx))  # le DOI arXiv n'est pas un DOI éditeur

    def test_abstract_rebuilt_in_order(self):
        w = _work("W1", "T", abstract="an FPGA autoencoder for an image")
        self.assertEqual(openalex.abstract_of(w), "an FPGA autoencoder for an image")

    def test_lookup_keys_publisher_then_arxiv(self):
        meta = {"doi": "10.1145/3242897", "arxiv_id": "1809.04570"}
        self.assertEqual(openalex.lookup_keys(meta),
                         ["doi:10.1145/3242897", "doi:10.48550/arxiv.1809.04570"])


class TestClientCache(unittest.TestCase):
    def test_second_call_served_from_cache(self):
        resp = mock.Mock(status_code=200, json=lambda: {"id": "W1"})
        session = mock.Mock(get=mock.Mock(return_value=resp))
        with tempfile.TemporaryDirectory() as d:
            c = openalex.Client(cache_dir=d, delay=0, session=session)
            self.assertEqual(c.work("doi:10.1/x"), {"id": "W1"})
            self.assertEqual(c.work("doi:10.1/x"), {"id": "W1"})
        self.assertEqual(session.get.call_count, 1)

    def test_http_error_raises(self):
        resp = mock.Mock(status_code=503, json=lambda: {"message": "search paused"})
        c = openalex.Client(cache_dir=None, delay=0, session=mock.Mock(get=mock.Mock(return_value=resp)))
        with self.assertRaisesRegex(openalex.OpenAlexError, "search paused"):
            c.work("doi:10.1/x")


class FakeClient:
    """Corpus : C1 (DOI 10.1/c1). Candidats : D1 (cite C1, versions éditeur + arXiv),
    R1 (cité par C1), X1 (hors sujet)."""

    def __init__(self):
        self.works_ = {
            "C1": _work("C1", "Corpus paper on FPGA toolflows", doi="10.1/c1", refs_=("R1", "X1")),
            "D1": _work("D1", "Convolutional autoencoder for images on FPGA", doi="10.2/d1",
                        refs_=("C1",), cited=40),
            "D1a": _work("D1a", "Convolutional Autoencoder for Images on FPGA.", arxiv="2301.00001",
                         venue="arXiv", refs_=("C1",)),
            "R1": _work("R1", "hls4ml quantized inference on Zynq devices", doi="10.3/r1"),
            "X1": _work("X1", "Protein folding with deep networks", doi="10.4/x1"),
        }

    def work(self, key):
        return self.works_["C1"] if key == "doi:10.1/c1" else None

    def works(self, filter=None, search=None, sort=None, limit=200):
        if filter and filter.startswith("cites:C1"):
            return [self.works_["D1"], self.works_["D1a"]]
        return []

    def works_by_ids(self, ids_):
        return [self.works_[i] for i in sorted(ids_) if i in self.works_]


class TestInTopic(unittest.TestCase):
    def check(self, title, abstract, axes=()):
        return discover.in_topic_of(title, f"{title} {abstract}", list(axes))

    def test_single_passing_mention_not_enough(self):
        # SqueezeNet : une seule mention de FPGA dans le résumé, rien dans le titre
        self.assertFalse(self.check(
            "SqueezeNet: AlexNet-level accuracy with 50x fewer parameters and <0.5MB model size",
            "Smaller CNNs are more feasible to deploy on FPGAs and other hardware with limited memory."))
        self.assertFalse(self.check("An Efficient Edge Detection Approach for Image Analysis", "Canny."))

    def test_title_repeated_mentions_or_hardware_axis(self):
        self.assertTrue(self.check("A TinyML Platform for On-Device Continual Learning", "latent replays"))
        self.assertTrue(self.check("UNPU: An Energy-Efficient Deep Neural Network Accelerator", "bit precision"))
        self.assertTrue(self.check("Object detection at 40 MHz",
                                   "We implement it on an FPGA; the FPGA design uses HLS."))
        self.assertTrue(self.check("A detector", "one mention of Kria", axes=["platforms"]))


class TestDiscover(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        (root / "papers" / "p1").mkdir(parents=True)
        (root / "papers" / "p1" / "metadata.json").write_text(json.dumps(
            {"id": "p1", "title": "Corpus paper on FPGA toolflows", "year": 2020,
             "doi": "10.1/c1", "arxiv_id": None}))
        self.patches = [mock.patch.object(discover, "ROOT", root),
                        mock.patch.object(discover, "CANDIDATES", root / "candidates.csv"),
                        mock.patch.object(discover, "ARXIV_LIST", root / "candidates_arxiv.txt")]
        for p in self.patches:
            p.start()
        self.root = root

    def tearDown(self):
        for p in self.patches:
            p.stop()
        self.tmp.cleanup()

    def test_forward_backward(self):
        with mock.patch("sys.stdout"):
            code = discover.run(["--min-links", "1"], client=FakeClient())
        self.assertEqual(code, 0)
        with open(self.root / "candidates.csv", newline="") as f:
            rows = list(csv.DictReader(f))
        titles = [r["title"] for r in rows]
        self.assertNotIn("Corpus paper on FPGA toolflows", titles)       # déjà en base
        self.assertEqual(sum("autoencoder" in t.lower() for t in titles), 1)  # 2 versions fusionnées
        d1 = next(r for r in rows if "autoencoder" in r["title"].lower())
        self.assertEqual((d1["doi"], d1["arxiv_id"]), ("10.2/d1", "2301.00001"))
        self.assertIn("autoencoder-fpga", d1["axes_guess"])
        self.assertEqual(d1["in_topic"], "oui")
        x1 = next(r for r in rows if r["title"].startswith("Protein"))
        self.assertEqual(x1["in_topic"], "non")
        self.assertEqual(rows[-1]["title"], x1["title"])                 # hors sujet en dernier
        listing = (self.root / "candidates_arxiv.txt").read_text()
        self.assertIn("2301.00001", listing)
        self.assertEqual(add.read_id_list(self.root / "candidates_arxiv.txt"), ["2301.00001"])


class TestAddHelpers(unittest.TestCase):
    def test_find_doi(self):
        self.assertEqual(ids.find_doi("10.1145/3242897"), "10.1145/3242897")
        self.assertEqual(ids.find_doi("https://doi.org/10.1109/FCCM.2016.22"), "10.1109/FCCM.2016.22")
        self.assertEqual(ids.find_doi("doi:10.1088/1748-0221/13/07/P07027"), "10.1088/1748-0221/13/07/P07027")
        self.assertIsNone(ids.find_doi("2507.18174"))
        self.assertIsNone(ids.find_doi("article.pdf"))

    def test_expand_args_from_file(self):
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
            f.write("# commentaire\n2507.18174   # titre\n\n10.1145/3242897\n")
        try:
            self.assertEqual(add.expand_args(["1612.07119", "--from", f.name]),
                             ["1612.07119", "2507.18174", "10.1145/3242897"])
        finally:
            Path(f.name).unlink()

    def test_doi_without_arxiv_refused_with_procedure(self):
        client = mock.Mock()
        client.work.return_value = _work("W9", "Paywalled paper", doi="10.9/p")
        with mock.patch.object(add, "PAPERS", Path(tempfile.gettempdir()) / "nonexistent-papers"):
            with self.assertRaisesRegex(add.AddError, r"(?s)pas de version arXiv.*inbox/"):
                add.add_doi("10.9/p", client=client)

    def test_doi_with_arxiv_version(self):
        client = mock.Mock()
        client.work.return_value = _work("W8", "Open paper", doi="10.8/o", arxiv="1804.06913", venue="JINST")
        with mock.patch.object(add, "PAPERS", Path(tempfile.gettempdir()) / "nonexistent-papers"), \
                mock.patch.object(add, "add_arxiv", return_value="pdf") as aa, mock.patch("sys.stdout"):
            self.assertEqual(add.add_doi("10.8/o", client=client), "pdf")
        aa.assert_called_once_with("1804.06913", doi="10.8/o", venue="JINST")


if __name__ == "__main__":
    unittest.main()
