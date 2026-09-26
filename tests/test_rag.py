"""Tests de lib/rag.py (passages, BM25, fusion, vérification de citations).

L'encodeur est remplacé par une fonction déterministe : ces tests ne demandent pas
sentence-transformers (seulement numpy). L'évaluation sur le vrai modèle : bin/pdb test --rag.
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

try:
    import numpy as np
    from lib import embed, rag
except ImportError:
    rag = None

WORDS = ("binarized", "power", "memory", "forgetting")


def fake_encode(texts, model):
    """Vecteur = présence de quelques mots-clés (+1 pour éviter le vecteur nul), normalisé."""
    out = []
    for t in texts:
        v = np.array([1.0 if w in t.lower() else 0.0 for w in WORDS] + [0.1])
        out.append(v / np.linalg.norm(v))
    return np.array(out)


LONG = " ".join(f"w{i}" for i in range(300))
PAPERS = {
    "arxiv-1612.07119-finn": [
        ("abstract", "Abstract", "FINN builds binarized neural network accelerators on FPGA."),
        ("section", "5. Evaluation", "P wall using a wall power meter for the total board power "
                                     "consumption. Efﬁcient designs are energy- efficient."),
        ("section", "6. Long", LONG),
    ],
    "2021-lin-mcunet": [
        ("abstract", "Abstract", "Patch-based inference reduces peak memory on microcontrollers."),
        ("section", "4. Forgetting", "Catastrophic forgetting appears when learning new classes."),
    ],
}


def write_corpus(root):
    for pid, secs in PAPERS.items():
        d = root / "papers" / pid
        d.mkdir(parents=True)
        meta = {"id": pid, "title": pid, "axes": ["toolflows"] if "finn" in pid else ["platforms"],
                "arxiv_id": "1612.07119" if "finn" in pid else None}
        (d / "metadata.json").write_text(json.dumps(meta))
        rows = [{"id": f"{pid}#{i:03d}", "paper_id": pid, "kind": k, "section": s,
                 "subsection": None, "order": i, "page": i + 1, "text": t}
                for i, (k, s, t) in enumerate(secs)]
        (d / "sections.jsonl").write_text("\n".join(json.dumps(r) for r in rows) + "\n")


@unittest.skipIf(rag is None, "numpy absent")
class TestRag(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        write_corpus(self.root)
        self.patches = [mock.patch.object(embed, "available", return_value=True),
                        mock.patch.object(embed, "_encode", side_effect=fake_encode)]
        self.enc = [p.start() for p in self.patches][1]

    def tearDown(self):
        for p in self.patches:
            p.stop()
        self.tmp.cleanup()

    def index(self):
        rag.build_index(self.root)
        return rag.Index(self.root)

    def test_split_windows(self):
        parts = rag.split_text(LONG)
        self.assertEqual([len(p.split()) for p in parts], [200, 140])
        self.assertEqual(parts[0].split()[160], parts[1].split()[0])  # recouvrement de 40 mots
        self.assertEqual(rag.split_text("court"), ["court"])

    def test_chunk_ids(self):
        ids = [c["chunk_id"] for c in rag.load_chunks(self.root)]
        self.assertIn("arxiv-1612.07119-finn#002.1", ids)
        self.assertIn("2021-lin-mcunet#000.0", ids)

    def test_build_index_is_incremental(self):
        m = rag.build_index(self.root)
        self.assertEqual(m["encoded"], m["chunks"])
        self.assertEqual(rag.build_index(self.root)["encoded"], 0)
        sec = self.root / "papers" / "2021-lin-mcunet" / "sections.jsonl"
        sec.write_text(sec.read_text().replace("Catastrophic", "Severe"))
        self.assertEqual(rag.build_index(self.root)["encoded"], 1)

    def test_search_modes_and_filters(self):
        ix = self.index()
        top = ix.search("wall power measurement", k=3)
        self.assertEqual(top[0]["chunk_id"], "arxiv-1612.07119-finn#001.0")
        self.assertIsNotNone(top[0]["cos"])
        self.assertEqual(top, ix.search("wall power measurement", k=3))  # déterministe
        lex = ix.search("catastrophic forgetting", mode="lexical")
        self.assertEqual(lex[0]["section_id"], "2021-lin-mcunet#001")
        self.assertIsNone(lex[0]["cos"])
        only = ix.search("power", paper_ids={"2021-lin-mcunet"})
        self.assertEqual({h["paper_id"] for h in only}, {"2021-lin-mcunet"})
        self.assertEqual({h["kind"] for h in ix.search("memory", kind="abstract")}, {"abstract"})
        self.assertEqual({h["paper_id"] for h in ix.search("memory", axis="platforms")},
                         {"2021-lin-mcunet"})

    def test_rerank_reorders_pool(self):
        ix = self.index()
        # cross-encoder factice : préfère les passages qui parlent de mémoire
        fake = lambda q, texts, model=None: [1.0 if "memory" in t.lower() else 0.0 for t in texts]  # noqa: E731
        with mock.patch.object(rag, "_cross_scores", side_effect=fake):
            top = ix.search("wall power measurement", k=2, rerank=True)
        self.assertEqual(top[0]["chunk_id"], "2021-lin-mcunet#000.0")
        self.assertEqual(top[0]["rerank"], 1.0)
        self.assertEqual(len(top), 2)

    def test_lexical_fallback_without_vectors(self):
        with mock.patch.object(embed, "available", return_value=False):
            ix = rag.Index(self.root)
        self.assertFalse(ix.dense)
        self.assertEqual(ix.search("binarized")[0]["mode"], "lexical")

    def test_resolve_short_chunk_id(self):
        ix = self.index()
        full = "arxiv-1612.07119-finn#001.0"
        self.assertEqual(ix.resolve_chunk("1612.07119#001.0"), full)
        self.assertEqual(ix.resolve_chunk("1612.07119#001"), full)
        self.assertEqual(ix.short_chunk_id(full), "1612.07119#001.0")
        self.assertIsNone(ix.resolve_chunk("1612.07119#099.0"))
        self.assertEqual([c["chunk_id"] for c in ix.get(full, context=1)],
                         ["arxiv-1612.07119-finn#000.0", full, "arxiv-1612.07119-finn#002.0"])

    def test_verify(self):
        ix = self.index()
        cid = "arxiv-1612.07119-finn#001.0"
        self.assertEqual(rag.verify(ix, cid, "wall power meter for the TOTAL board")[0], "OK")
        # ligature et césure du texte source
        self.assertEqual(rag.verify(ix, cid, "Efficient designs are energy-efficient")[0], "OK")
        status, ratio, _ = rag.verify(ix, cid, "a wall power meter for the whole board power")
        self.assertEqual(status, "APPROX")
        self.assertGreaterEqual(ratio, rag.VERIFY_MIN)
        self.assertEqual(rag.verify(ix, cid, "measured with an oscilloscope")[0], "ABSENT")
        # trouvée ailleurs dans le papier
        self.assertEqual(rag.verify(ix, cid, "binarized neural network accelerators")[2],
                         "arxiv-1612.07119-finn#000.0")
        sha = ix.chunks[ix.by_id[cid]]["sha1"]
        self.assertEqual(rag.verify(ix, cid, "wall power", expect_sha=sha[:8])[0], "OK")
        self.assertEqual(rag.verify(ix, cid, "wall power", expect_sha="00000000")[0], "MODIFIÉ")

    def test_numbers_match(self):
        text = "On a ZC706 drawing 25 W, we reach 12.3 million images/s, 143,927 LUTs and 0.31 µs."
        ok = rag.numbers_match
        self.assertTrue(ok(text, "we reach 12.3 million images/s"))
        self.assertFalse(ok(text, "we reach 12.4 million images/s"))
        # 25 existe, mais pas à cette place : repéré par l'ordre des nombres…
        self.assertFalse(ok(text, "we reach 25 million images/s, 143,927 LUTs"))
        # … et, pour un nombre seul, par ses mots voisins
        self.assertFalse(ok(text, "we reach 25 million images/s"))
        self.assertFalse(ok("Section 2 reviews the background, Section 3 the method.",
                            "Section 3 reviews the background"))
        self.assertFalse(ok(text, "0.4 µs"))  # « 4 » ne vaut pas « 6.4 » : pas de sous-chaîne
        self.assertTrue(ok(text, "143 927 LUTs and 0.31 µs"))  # séparateur de milliers
        self.assertTrue(ok(text, "ZC706 drawing 25 W … 143,927 LUTs"))  # citation élidée
        self.assertFalse(ok(text, "ZC706 drawing 25 W … 143,928 LUTs"))
        self.assertTrue(ok(text, "3 million images/s"))  # coupée au milieu de « 12.3 »
        self.assertTrue(ok(text, "images per second"))  # sans nombre

    def test_verify_rejects_changed_number(self):
        chunks = [{"chunk_id": f"p#00{i}.0", "section_id": f"p#00{i}", "paper_id": "p", "kind": "section",
                   "section": "S", "subsection": None, "page": 1, "text": t, "sha1": str(i)}
                  for i, t in enumerate(("The prototype reaches 21906 images per second at 283 us latency on CIFAR-10.",
                                         "SVHN runs at 21906 images per second with 94.9% accuracy."))]
        ix = rag.Index(self.root, chunks=chunks)
        self.assertEqual(rag.verify(ix, "p#000.0", "reaches 21906 images per second at 283 us")[0], "OK")
        status, ratio, where = rag.verify(ix, "p#000.0", "reaches 21906 images per second at 288 us")
        self.assertEqual((status, where), ("NOMBRES", "p#000.0"))
        self.assertGreaterEqual(ratio, rag.VERIFY_MIN)
        # « 3.5 » et « 35 » ont la même forme normalisée : le contrôle des nombres les distingue
        self.assertEqual(rag.verify(ix, "p#001.0", "with 949% accuracy")[0], "NOMBRES")
        # bons nombres dans un autre passage du papier
        self.assertEqual(rag.verify(ix, "p#000.0", "runs at 21906 images per second with 94.9%")[2], "p#001.0")

    def test_snippet_marks_terms(self):
        text = "x " * 200 + "the wall power meter reads the board"
        snip = rag.snippet(text, "wall power", {"wall": 3.0, "power": 2.0})
        self.assertTrue(snip.startswith("…"))
        self.assertIn("«wall» «power»", snip)
        self.assertLessEqual(len(snip), rag.SNIPPET + 2)

    def test_evaluate(self):
        ix = self.index()
        qs = [{"q": "wall power", "expect": ["arxiv-1612.07119-finn#001"]},
              {"q": "catastrophic forgetting", "expect": ["2021-lin-mcunet#001"]}]
        res = rag.evaluate(ix, qs, k=1)
        self.assertEqual(set(res), {"hybrid", "dense", "lexical"})
        self.assertEqual(res["lexical"]["recall"], 1.0)
        self.assertEqual(res["lexical"]["misses"], [])


if __name__ == "__main__":
    unittest.main()
