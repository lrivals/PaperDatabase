"""Tests de lib/query.py (requêtes N0 : bin/pdb bench, bin/pdb paper).

.venv/bin/python -m unittest discover tests
"""
import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from lib import query, schema  # noqa: E402

PAPERS = [
    {"id": "arxiv-1612.07119-finn", "arxiv_id": "1612.07119", "title": "FINN: binarized",
     "year": 2016, "type": "conference", "authors": [{"given": "Y", "family": "Umuroglu"}]},
    {"id": "2022-feng-yolo-edge", "arxiv_id": None, "title": "YOLO on edge", "year": 2022,
     "type": "preprint", "authors": [], "extraction": {"warnings": ["w1", "w2"]},
     "status": {"fiche": "todo"}},
    {"id": "2022-feng-other-work", "arxiv_id": None, "title": "Another FINN study", "year": 2022},
]


def _row(pid, model, fps, power="n/r", scope="n/r", conf="high", dataset="d"):
    r = {c: "n/r" for c in schema.BENCHMARK_COLUMNS}
    r.update(paper_id=pid, model=model, platform="KV260" if "yolo" in pid else "ZC706",
             fps=fps, power_w=power, power_scope=scope, confidence=conf, dataset=dataset,
             source_section="Table 1")
    return r


ROWS = [
    _row("arxiv-1612.07119-finn", "CNV", "21900", "11.7", "board", dataset="CIFAR-10"),
    _row("arxiv-1612.07119-finn", "CNV", "21900", "11.7", "board", dataset="SVHN"),
    _row("2022-feng-yolo-edge", "YOLOv5s", "9", "3.5", "unspecified", conf="low"),
    _row("2022-feng-yolo-edge", "YOLOv5n", "n/r"),
    _row("2022-feng-other-work", "X", "120"),
]


class TestShortIds(unittest.TestCase):
    def test_arxiv_then_year_author_then_full_on_collision(self):
        short = query.short_ids(PAPERS)
        self.assertEqual(short["arxiv-1612.07119-finn"], "1612.07119")
        # deux papiers « 2022-feng » : collision → identifiant complet
        self.assertEqual(short["2022-feng-yolo-edge"], "2022-feng-yolo-edge")
        self.assertEqual(query.short_ids(PAPERS[:2])["2022-feng-yolo-edge"], "2022-feng")

    def test_compound_family_name(self):
        meta = {"id": "2025-el-zeinaty-designing-models", "year": 2025,
                "authors": [{"given": "C", "family": "El Zeinaty"}]}
        self.assertEqual(query.short_ids([meta])[meta["id"]], "2025-el-zeinaty")

    def test_resolve(self):
        self.assertEqual([m["id"] for m in query.resolve("1612.07119", PAPERS)],
                         ["arxiv-1612.07119-finn"])
        self.assertEqual([m["id"] for m in query.resolve("2022-FENG-YOLO-EDGE", PAPERS)],
                         ["2022-feng-yolo-edge"])
        # sous-chaîne du titre, ambiguë
        self.assertEqual(len(query.resolve("finn", PAPERS)), 2)
        self.assertEqual(query.resolve("absent", PAPERS), [])


class TestFilterSort(unittest.TestCase):
    def test_contains_case_insensitive(self):
        self.assertEqual(len(query.filter_rows(ROWS, contains={"platform": "kv2"})), 2)

    def test_numeric_bounds_exclude_nr(self):
        got = query.filter_rows(ROWS, minimum={"fps": 10})
        self.assertEqual([r["model"] for r in got], ["CNV", "CNV", "X"])
        got = query.filter_rows(ROWS, maximum={"fps": 100})
        self.assertEqual([r["model"] for r in got], ["YOLOv5s"])

    def test_has(self):
        self.assertEqual(len(query.filter_rows(ROWS, has=["power_w"])), 3)

    def test_sort_numeric_nr_last(self):
        self.assertEqual([r["fps"] for r in query.sort_rows(ROWS, "fps")],
                         ["9", "120", "21900", "21900", "n/r"])
        self.assertEqual([r["fps"] for r in query.sort_rows(ROWS, "fps", desc=True)][-1], "n/r")


class TestRender(unittest.TestCase):
    header = list(schema.BENCHMARK_COLUMNS)

    def test_source_columns_always_kept(self):
        cols = query.select_columns(["model", "power_w"], self.header)
        self.assertEqual(cols, ["paper_id", "model", "power_w", "power_scope",
                                "source_section", "confidence"])
        with self.assertRaises(ValueError):
            query.select_columns(["nope"], self.header)

    def test_tsv_low_marker_legend_hidden_diff(self):
        short = query.short_ids(PAPERS[:2])
        cols = query.select_columns(["model", "fps"], self.header)
        out = query.render(ROWS[:3], cols, short)
        lines = out.splitlines()
        self.assertEqual(lines[0], "paper\tmodel\tfps\tsource_section\tconfidence")
        self.assertTrue(lines[3].startswith("!2022-feng\tYOLOv5s"))
        self.assertIn("# ! = confidence low", lines)
        self.assertIn("# lignes identiques à l'affichage : elles diffèrent par dataset", lines)
        self.assertIn("# ids: 2022-feng=2022-feng-yolo-edge 1612.07119=arxiv-1612.07119-finn",
                      lines)

    def test_max_chars_truncates_whole_lines_and_legend(self):
        short = query.short_ids(PAPERS[:2])
        cols = query.select_columns(["model"], self.header)
        full = query.render(ROWS[:4], cols, short)
        out = query.render(ROWS[:4], cols, short, max_chars=len(full) - 40)
        self.assertLessEqual(len(out), len(full) - 40)
        self.assertIn("# tronqué :", out)
        self.assertNotIn("2022-feng=", out)  # papier coupé → absent de la légende

    def test_md_and_json(self):
        cols = query.select_columns(["model"], self.header)
        md = query.render(ROWS[:1], cols, {}, fmt="md").splitlines()
        self.assertEqual(md[1], "|---|---|---|---|")
        data = json.loads(query.render(ROWS[:1], cols, {"arxiv-1612.07119-finn": "1612.07119"},
                                       fmt="json"))
        self.assertEqual((data[0]["paper_id"], data[0]["short"]),
                         ("arxiv-1612.07119-finn", "1612.07119"))


class TestCount(unittest.TestCase):
    def test_count_rows(self):
        out = query.count_rows(ROWS, ["paper_id", "power_scope"], {"arxiv-1612.07119-finn": "finn"})
        self.assertEqual(out.splitlines()[:2], ["n\tpaper\tpower_scope", "2\tfinn\tboard"])


class TestPaperCard(unittest.TestCase):
    def test_preprint_and_fields(self):
        card = query.paper_card(PAPERS[1], 2, "2022-feng")
        d = dict(line.split("\t", 1) for line in card.splitlines())
        self.assertEqual(d["type"], "preprint (non relu par les pairs)")
        self.assertEqual((d["authors"], d["fiche"], d["benchmarks"], d["warnings"]),
                         ("n/r", "todo", "2", "2"))
        self.assertEqual(query.paper_card(PAPERS[0], 0, "x", ["title", "year"]),
                         "title\tFINN: binarized\nyear\t2016")
        with self.assertRaises(ValueError):
            query.paper_card(PAPERS[0], 0, "x", ["nope"])

    def test_paper_table(self):
        cards = [query.card_values(m, 0, s, ["short", "type"])
                 for m, s in ((PAPERS[0], "1612.07119"), (PAPERS[1], "2022-feng"))]
        self.assertEqual(query.paper_table(cards),
                         "short\ttype\n1612.07119\tconference\n"
                         "2022-feng\tpreprint (non relu par les pairs)")
        self.assertEqual(query.paper_table([]), "")


class TestCitationLines(unittest.TestCase):
    def test_internal_then_external(self):
        by_id = {m["id"]: m for m in PAPERS}
        short = query.short_ids(PAPERS)
        groups = {"ext:a": {"title": "Rare", "year": 2015, "arxiv_id": None, "doi": "10.1/r"},
                  "ext:b": {"title": "Popular", "year": 2016, "arxiv_id": "1510.00149", "doi": None}}
        citers = {"ext:a": {"p1"}, "ext:b": {"p1", "p2"}}
        targets = {"2022-feng-yolo-edge", "arxiv-1612.07119-finn", "ext:a", "ext:b"}
        self.assertEqual(query.citation_lines(targets, by_id, short), [
            "1612.07119\t2016\tFINN: binarized",
            "2022-feng-yolo-edge\t2022\tYOLO on edge"])
        lines = query.citation_lines(targets, by_id, short, groups, citers)
        self.assertEqual(lines[2:], ["ext\t2\t2016\tPopular\tarXiv:1510.00149",
                                     "ext\t1\t2015\tRare\tdoi:10.1/r"])


class TestLoad(unittest.TestCase):
    def test_load_from_disk(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for m in PAPERS:
                (root / "papers" / m["id"]).mkdir(parents=True)
                (root / "papers" / m["id"] / "metadata.json").write_text(json.dumps(m))
            with open(root / "benchmarks.csv", "w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=schema.BENCHMARK_COLUMNS)
                w.writeheader()
                w.writerows(ROWS)
            header, rows = query.load_benchmarks(root)
            self.assertEqual(header, list(schema.BENCHMARK_COLUMNS))
            self.assertEqual(len(rows), 5)
            self.assertEqual(len(query.load_papers(root)), 3)
            self.assertEqual(query.load_benchmarks(root / "absent"), ([], []))


if __name__ == "__main__":
    unittest.main()
