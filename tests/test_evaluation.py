"""Tests de lib/evaluation.py (banc d'évaluation) : métriques sur de petits cas construits.

L'encodeur factice de test_rag.py remplace le modèle. Le banc sur le vrai corpus :
bin/pdb eval (docs/EVAL.md).
"""
import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))

from lib import evaluation as ev  # noqa: E402

try:
    from lib import embed, rag
    from test_rag import fake_encode, write_corpus
except ImportError:
    rag = None


class TestHelpers(unittest.TestCase):
    def test_coverage_counts_occurrences(self):
        self.assertEqual(ev.coverage("alpha alpha beta", "alpha beta"), 2 / 3)
        self.assertEqual(ev.coverage("Efﬁcient design", "efficient design"), 1.0)  # ligature
        self.assertIsNone(ev.coverage("a b c", "x"))  # aucun mot de 4 lettres

    def test_strip_bibliography(self):
        body = "Intro text.\n" * 10
        self.assertEqual(ev.strip_bibliography(body + "References\n[1] A. B."), body)
        self.assertEqual(ev.strip_bibliography(body + "R E F E R E N C E S\n[1] A."), body)
        self.assertEqual(ev.strip_bibliography(body + "[1] LHC Machine. JINST."), body)
        early = "[1] cited early\n" + body
        self.assertEqual(ev.strip_bibliography(early), early)  # « [1] » en début de texte

    def test_cited_tables(self):
        self.assertEqual(ev.cited_tables("Table 3, Table 4, §5.2.3 (BRAM)"), {3, 4})
        self.assertEqual(ev.cited_tables("Table VII, Table VI, Table II"), {7, 6, 2})
        self.assertEqual(ev.cited_tables("§IV-C (Fig. 4d)"), set())

    def test_numbers_and_values(self):
        found = ev.numbers("LUT | 143,927 | 62% ; 3.5 W ; 12 345 ops ; 0.31 µs")
        for v in ("143927", "62", "3.5", "12345", "0.31"):
            self.assertTrue(ev.value_in(v, found), v)
        self.assertFalse(ev.value_in("3.6", found))
        self.assertIsNone(ev.value_in("n/r", found))

    def test_ranking_metrics(self):
        res = [{"section_id": s, "paper_id": s.split("#")[0]} for s in ("p#1", "p#2", "q#1", "p#2")]
        m = ev.ranking_metrics(res, ["q#1", "q#9"])
        self.assertEqual((m["first"], m["recall@5"], m["mrr"]), (3, 1.0, 1 / 3))
        self.assertAlmostEqual(m["ndcg@10"], 0.5 / (1 + 1 / 1.5849625), places=4)
        self.assertEqual(ev.ranking_metrics(res, ["z#1"])["recall@10"], 0.0)

    def test_flatten_compare_thresholds(self):
        flat = ev.flatten({"rag": {"a": {"recall@5": 0.7, "misses": ["q"]}, "ok": True},
                           "speed": {"x": 1.0}})
        self.assertEqual(flat, {"rag.a.recall@5": 0.7, "rag.ok": 1.0, "speed.x": 1.0})
        self.assertEqual(ev.compare(flat, {**flat, "speed.x": 2.0}), [])  # temps ignorés
        self.assertEqual(ev.compare(flat, {**flat, "rag.a.recall@5": 0.9}),
                         [("rag.a.recall@5", 0.7, 0.9)])
        fails = ev.check_thresholds(flat, {"_doc": "", "rag.a.recall@5": {"min": 0.8},
                                           "rag.ok": {"max": 1.0}, "absent": {"min": 0}})
        self.assertEqual([f[0] for f in fails], ["rag.a.recall@5", "absent"])


class TestCorpusMetrics(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        d = self.root / "papers" / "arxiv-1111.00001-demo"
        d.mkdir(parents=True)
        (d / "metadata.json").write_text(json.dumps(
            {"id": d.name, "title": "Demo", "arxiv_id": "1111.00001", "extraction": {"backend": "grobid"}}))
        rows = [{"id": f"{d.name}#000", "paper_id": d.name, "kind": "section", "section": "1. Intro",
                 "text": "We reach 120 FPS at 3.5 W."},
                {"id": f"{d.name}#001", "paper_id": d.name, "kind": "table", "section": "Figures",
                 "text": "TABLE II Results\n\nLUT | 14,200 | DSP | 360"}]
        (d / "sections.jsonl").write_text("\n".join(json.dumps(r) for r in rows) + "\n")
        with open(self.root / "benchmarks.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["paper_id", "source_section", *ev.BENCH_VALUES])
            w.writeheader()
            base = dict.fromkeys(ev.BENCH_VALUES, "n/r")
            w.writerow({**base, "paper_id": d.name, "source_section": "Table II",
                        "luts": "14200", "dsps": "360", "fps": "120", "power_w": "4"})

    def tearDown(self):
        self.tmp.cleanup()

    def test_table_values(self):
        t = ev.table_values(self.root)
        # 4 valeurs : LUT et DSP dans la Table II, FPS seulement dans le texte, 4 W nulle part
        self.assertEqual(t["values"], 4)
        self.assertEqual(t["in_cited_table"], 0.5)
        self.assertEqual(t["in_text"], 0.75)
        self.assertEqual(t["rows_cited_table_absent"], 0)

    def test_expect_from_pattern(self):
        self.assertEqual(ev.expect_from_pattern(self.root, ["1111.00001"], r"LUT"),
                         ["arxiv-1111.00001-demo#001"])
        self.assertEqual(ev.expect_from_pattern(self.root, ["1111.00001"], r"LUT", ["section"]), [])


@unittest.skipIf(rag is None, "numpy absent")
class TestRagMetrics(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        write_corpus(self.root)
        self.patches = [mock.patch.object(embed, "available", return_value=True),
                        mock.patch.object(embed, "_encode", side_effect=fake_encode)]
        for p in self.patches:
            p.start()
        rag.build_index(self.root)
        self.ix = rag.Index(self.root)

    def tearDown(self):
        for p in self.patches:
            p.stop()
        self.tmp.cleanup()

    def test_evaluate_set(self):
        qs = [{"q": "wall power meter", "expect": ["arxiv-1612.07119-finn#001"]},
              {"q": "unrelated zzz", "expect": ["nowhere#000"]}]
        out = ev.evaluate_set(self.ix, qs, modes=("lexical",))
        self.assertEqual(out["lexical"]["recall@5"], 0.5)
        self.assertEqual(out["lexical"]["misses"], ["unrelated zzz"])

    def test_best_threshold(self):
        self.assertEqual(ev.best_threshold([0.8, 0.9], [0.1, 0.3]), 0.55)
        self.assertIn(ev.best_threshold([0.5], [0.5]), (0.5 - 1e-6, 0.5 + 1e-6))  # inséparables

    def test_low_relevance(self):
        cos = {"in a": 0.8, "in b": 0.75, "off a": 0.7, "off b": 0.72, "off c": 0.9}
        ce = {"in a": 5.0, "in b": 3.0, "off a": -8.0, "off b": -6.0, "off c": -7.0}
        search = lambda q, k, mode: [{"cos": cos[q]}]  # noqa: E731
        with mock.patch.object(self.ix, "search", search), \
                mock.patch.object(rag, "relevance_score", lambda ix, q: ce[q]):
            lr = ev.low_relevance(self.ix, [{"q": "in a"}], [{"q": "off a"}, {"q": "x", "ambiguous": "?"}],
                                  [{"q": "in b"}], [{"q": "off b"}, {"q": "off c"}])
        self.assertEqual(lr["n"], {"cal_pos": 1, "cal_neg": 1, "val_pos": 1, "val_neg": 2})
        self.assertEqual(lr["rerank"]["threshold"], -1.5)
        self.assertEqual(lr["rerank"]["validation"], {"flagged_negatives": 1.0, "flagged_positives": 0.0})
        self.assertTrue(lr["rerank"]["adopted"])
        # le cosinus sépare la calibration mais pas la validation (off c à 0,9)
        self.assertEqual(lr["cos"]["validation"]["flagged_negatives"], 0.5)
        self.assertEqual(lr["cos"]["val_negatives_missed"], ["off c"])
        self.assertFalse(lr["cos"]["adopted"])

    def test_verify_cases(self):
        sentence = "The accelerator reaches {} frames per second on the evaluation board with batch one."
        chunks = [{"chunk_id": f"{pid}#000.0", "section_id": f"{pid}#000", "paper_id": pid,
                   "kind": "section", "section": "S", "subsection": None, "page": 1,
                   "text": " ".join(sentence.format(n) for n in (12, 34)), "sha1": pid}
                  for pid in ("a-paper", "b-paper")]
        ix = rag.Index(self.root, chunks=chunks)
        cases = ev.verify_cases(ix, n=2, seed=1)
        self.assertEqual(cases, ev.verify_cases(ix, n=2, seed=1))  # déterministe
        self.assertEqual({c[0] for c in cases}, {"exact", "mot remplacé", "chiffre modifié", "autre papier"})
        self.assertTrue(all(expected == (case == "exact") for case, _, _, expected in cases))
        acc = ev.verify_accuracy(ix, n=2, seed=1)
        self.assertEqual(acc["exact"]["accepted_rate"], 1.0)


if __name__ == "__main__":
    unittest.main()
