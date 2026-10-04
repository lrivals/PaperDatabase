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


class TestPaths(unittest.TestCase):
    def test_base_fixtures_else_code(self):
        with tempfile.TemporaryDirectory() as d:
            code, base = Path(d) / "code", Path(d) / "base"
            (code / "tests" / "fixtures").mkdir(parents=True)
            (code / "eval").mkdir()
            (code / "eval" / "thresholds.json").write_text("{}")
            base.mkdir()
            fx, res, th = ev.paths(base, code)
            self.assertEqual((fx, th), (code / "tests" / "fixtures", code / "eval" / "thresholds.json"))
            self.assertEqual(res, base / "eval" / "results")
            (base / "eval" / "fixtures").mkdir(parents=True)
            (base / "eval" / "thresholds.json").write_text("{}")
            fx, _, th = ev.paths(base, code)
            self.assertEqual((fx, th), (base / "eval" / "fixtures", base / "eval" / "thresholds.json"))
            # base de référence : root == code, jeux de tests/fixtures
            self.assertEqual(ev.paths(code, code)[0], code / "tests" / "fixtures")


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

    def test_rag_quality_subcorpus(self):
        fx = self.root / "fixtures"
        fx.mkdir()
        qs = [{"q": "wall power meter", "expect": ["arxiv-1612.07119-finn#001"]},
              {"q": "tiny memory", "expect": ["2021-lin-mcunet#000"]}]
        (fx / "rag_eval.jsonl").write_text("\n".join(json.dumps(q) for q in qs) + "\n")
        modes = ("lexical",)
        full = ev.rag_quality(self.root, fx, modes=modes, verify_n=2)
        self.assertEqual(full["corpus"], {"n_papers": 2, "subset": False,
                                          "papers": ["2021-lin-mcunet", "arxiv-1612.07119-finn"]})
        self.assertNotIn("skipped", full["sets"]["rag_eval"])
        sub = ev.rag_quality(self.root, fx, modes=modes, verify_n=2,
                             paper_ids=["arxiv-1612.07119-finn"])
        self.assertTrue(sub["corpus"]["subset"])
        self.assertEqual(sub["corpus"]["papers"], ["arxiv-1612.07119-finn"])
        self.assertLess(sub["passages"], full["passages"])
        self.assertEqual((sub["sets"]["rag_eval"]["n"], sub["sets"]["rag_eval"]["skipped"]), (1, 1))
        # la liste des papiers n'entre pas dans les métriques comparées
        self.assertNotIn("rag.corpus.papers", ev.flatten({"rag": sub}))
        with self.assertRaises(ValueError):
            ev.rag_quality(self.root, fx, modes=modes, paper_ids=["absent-paper"])

    def test_read_paper_ids(self):
        txt = self.root / "ids.txt"
        txt.write_text("a-1  # commentaire\n\n# ligne vide\nb-2\n")
        self.assertEqual(ev.read_paper_ids(txt), ["a-1", "b-2"])
        run = self.root / "run.json"
        run.write_text(json.dumps({"results": {"rag": {"corpus": {"papers": ["x"]}}}}))
        self.assertEqual(ev.read_paper_ids(run), ["x"])
        run.write_text(json.dumps({"results": {"rag": {}}}))
        with self.assertRaises(ValueError):
            ev.read_paper_ids(run)

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


FINN = "arxiv-1612.07119-finn"
POWER = "P wall using a wall power meter for the total board power consumption."


def case(qid, category, verdict, **kw):
    return {"id": qid, "q": f"question {qid}", "category": category, "required": ["x"],
            "gold_sources": [], "expected_verdict": verdict, **kw}


def record(qid, verdict, claims):
    return {"id": qid, "q": f"question {qid}", "verdict": verdict, "claims": claims}


@unittest.skipIf(rag is None, "numpy absent")
class TestAnswers(unittest.TestCase):
    """Volet « réponses finales » (docs/EVAL.md §10) sur le petit corpus de test_rag."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        write_corpus(self.root)
        self.patches = [mock.patch.object(embed, "available", return_value=False)]
        for p in self.patches:
            p.start()
        self.ix = rag.Index(self.root)
        self.bench = [{"paper_id": FINN, "source_section": "Table 2, §5"}]

    def tearDown(self):
        for p in self.patches:
            p.stop()
        self.tmp.cleanup()

    def test_validate_case_and_record(self):
        self.assertEqual(ev.validate_answer_case(case("a", "simple", "suffisant", gold_sources=[f"{FINN}#001"])), [])
        self.assertEqual(ev.validate_answer_case(case("b", "absent", "absent")), [])
        bad = ev.validate_answer_case(case("c", "numeric", "oui", gold_values=[{"value": "n/r"}]))
        self.assertTrue(any("expected_verdict" in p for p in bad))
        self.assertTrue(any("gold_sources vide" in p for p in bad))
        self.assertTrue(any("gold_values" in p for p in bad))
        self.assertEqual(ev.validate_answer_record(record("a", "partiel", [])), [])
        bad = ev.validate_answer_record({"id": "a", "verdict": "absent",
                                         "claims": [{"text": "t", "kind": "vu", "citations": [{}]}]})
        self.assertEqual(len(bad), 2)

    def test_check_citation(self):
        ok = ev.check_citation(self.ix, {"id": "1612.07119#001.0", "excerpt": POWER}, self.bench)
        self.assertEqual((ok["status"], ok["accepted"], ok["section"]), ("OK", True, f"{FINN}#001"))
        changed = ev.check_citation(self.ix, {"id": f"{FINN}#001", "excerpt": POWER.replace("total", "peak")},
                                    self.bench)
        self.assertEqual(changed["status"], "APPROX")
        self.assertEqual(ev.check_citation(self.ix, {"id": f"{FINN}#000.0", "excerpt": POWER}, self.bench)["status"],
                         "AILLEURS")  # citation trouvée dans un autre passage du papier : refusée
        self.assertEqual(ev.check_citation(self.ix, {"id": f"{FINN}#001.0"}, self.bench)["status"], "SANS_EXTRAIT")
        self.assertEqual(ev.check_citation(self.ix, {"id": "nowhere#000"}, self.bench)["status"], "INCONNU")
        self.assertTrue(ev.check_citation(self.ix, {"paper": "1612.07119", "source_section": "table 2"},
                                          self.bench)["accepted"])
        self.assertFalse(ev.check_citation(self.ix, {"paper": FINN, "source_section": "Table 9"},
                                           self.bench)["accepted"])
        two = self.bench + [{"paper_id": FINN, "source_section": "Table 4"}]
        self.assertTrue(ev.check_citation(self.ix, {"paper": FINN, "source_section": "Table 2 ; Table 4"},
                                          two)["accepted"])  # citation regroupant deux lignes
        self.assertFalse(ev.check_citation(self.ix, {"paper": FINN, "source_section": "Table 4, Table 9"},
                                           two)["accepted"])
        self.assertFalse(ev.check_citation(self.ix, {"paper": FINN, "source_section": "power_scope=board"},
                                           two)["accepted"])

    def test_score_answer(self):
        c = case("n1", "numeric", "suffisant", gold_sources=[f"{FINN}#001", "2021-lin-mcunet"],
                 gold_values=[{"value": "12.5", "unit": "W"}, {"value": "30", "unit": "FPS"}])
        r = record("n1", "suffisant", [
            {"text": "La puissance est mesurée au mur : 12.5 W.", "kind": "lu",
             "citations": [{"id": "1612.07119#001.0", "excerpt": POWER}]},
            {"text": "Atteint 30 images/s.", "kind": "lu", "citations": [{"id": "1612.07119#001.0"}]},
            {"text": "Donc la mesure inclut la carte entière.", "kind": "déduit"},
        ])
        s = ev.score_answer(self.ix, c, r, self.bench)
        self.assertTrue(s["verdict_ok"])
        self.assertEqual((s["claims_read"], s["citations"], s["citations_accepted"]), (2, 2, 1))
        self.assertEqual(s["unsupported_claims"], 1)  # citation sans extrait
        self.assertEqual(s["gold_source_recall"], 0.5)  # section FINN citée, MCUNet non
        self.assertEqual(s["gold_value_recall"], 0.5)  # 30 sans l'unité FPS
        self.assertIsNone(s["requirements_declared_covered"])

    def test_value_hit_french_decimals(self):
        claims = [{"text": "MCUNetV2 atteint 64,6 % sous 256 kB et traite 12,361 k images/s."}]
        self.assertTrue(ev._value_hit({"value": "64.6", "unit": "%"}, claims))
        self.assertTrue(ev._value_hit({"value": "12361"}, claims))
        self.assertFalse(ev._value_hit({"value": "12.361"}, claims))
        self.assertFalse(ev._value_hit({"value": "64.6", "unit": "mAP"}, claims))

    def test_answer_quality_and_cli_loader(self):
        cases = [case("s1", "simple", "suffisant", gold_sources=[FINN]),
                 case("o1", "absent", "absent"), case("o2", "absent", "absent"),
                 case("m1", "simple", "suffisant", gold_sources=[FINN])]
        records = {"s1": record("s1", "absent", []), "o1": record("o1", "partiel", []),
                   "o2": record("o2", "suffisant", [{"text": "Faux.", "citations": []}])}
        q = ev.answer_quality(self.ix, cases, records, self.bench, grades={"s1": {"exigences": 1}})
        self.assertEqual((q["cases"], q["answered"], q["n"], q["missing"]), (4, 3, 3, ["m1"]))
        self.assertEqual(q["verdict_accuracy"], 0.0)
        self.assertEqual(q["absent_recognized"], 0.5)
        self.assertEqual(q["false_absent"], 1.0)
        self.assertEqual(q["verdict_confusion"]["absent"], {"suffisant": 1, "partiel": 1, "absent": 0})
        self.assertEqual(q["by_category"]["absent"]["unsupported_claim_rate"], 1.0)
        self.assertEqual(q["human"], {"n": 1, "exigences": 0.5, "soutien": None, "conditions": None,
                                      "limites": None})
        flat = ev.flatten({"answers": {"sets": {"answers": q}}})
        self.assertFalse(ev.compare(flat, flat))
        self.assertIn("answers.sets.answers.per_question.s1.claims", flat)

        fx, run = self.root / "fx", self.root / "run"
        fx.mkdir()
        run.mkdir()
        (fx / "answers.jsonl").write_text("\n".join(json.dumps(c) for c in cases) + "\n")
        for qid, r in records.items():
            (run / f"{qid}.json").write_text(json.dumps(r))
        (run / "bad.json").write_text("{")
        (run / "extra.json").write_text(json.dumps(record("zz", "absent", [])))
        with (run / "grades.csv").open("w", newline="") as f:
            w = csv.writer(f)
            w.writerow(("id",) + ev.GRADE_CRITERIA)
            w.writerow(("o1", "2", "2", "", "x"))
        out = ev.answers_quality(self.root, fx, run)
        self.assertEqual(out["records"], 4)
        self.assertIn("run/bad.json", out["invalid"])
        self.assertEqual(out["unknown_ids"], ["zz"])
        self.assertEqual(list(out["sets"]), ["answers"])  # pas de answers_holdout.jsonl
        self.assertEqual(out["sets"]["answers"]["human"]["soutien"], 1.0)
        self.assertEqual(ev.answer_questions(fx, "answers")[0], ("s1", "question s1"))
        run2 = self.root / "run2"
        run2.mkdir()
        (run2 / "m1.json").write_text(json.dumps(record("m1", "suffisant", [])))
        (run2 / "o1.json").write_text(json.dumps(record("o1", "absent", [])))  # déjà dans run
        both = ev.answers_quality(self.root, fx, [run, run2])
        self.assertEqual(both["sets"]["answers"]["answered"], 4)
        self.assertIn("run2/o1", both["invalid"])
        self.assertEqual(ev.answer_questions(fx, "answers_holdout"), [])


if __name__ == "__main__":
    unittest.main()
