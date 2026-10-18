"""Tests de lib/answerlog.py et lib/snapshot.py (provenance des réponses, lot H).

.venv/bin/python -m unittest discover tests
"""
import datetime
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from lib import answerlog, rag, snapshot  # noqa: E402

PID = "arxiv-1612.07119-finn"
RECORD = {"id": "q1", "q": "FPS de FINN ?", "verdict": "suffisant",
          "requirements": [{"text": "FPS", "status": "couvert"}],
          "claims": [{"text": "21 900 FPS", "kind": "lu",
                      "citations": [{"id": "1612.07119#001.0", "excerpt": "21,900 FPS"},
                                    {"id": "1612.07119#009.0", "excerpt": "?"}]}]}


class TestAnswerLog(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        d = self.root / "papers" / PID
        d.mkdir(parents=True)
        (d / "metadata.json").write_text(json.dumps({"id": PID, "arxiv_id": "1612.07119", "title": "FINN",
                                                     "year": 2016, "authors": []}))
        (d / "sections.jsonl").write_text(json.dumps({
            "id": f"{PID}#001", "paper_id": PID, "kind": "section", "section": "5", "subsection": None,
            "order": 1, "page": 1, "text": "CNV reaches 21,900 FPS on the ZC706."}) + "\n")
        (self.root / "benchmarks.csv").write_text("paper_id\n")

    def tearDown(self):
        self.tmp.cleanup()

    def test_snapshot_changes_with_corpus(self):
        a = snapshot.fingerprint(self.root)
        self.assertEqual(a, snapshot.fingerprint(self.root))
        (self.root / "papers" / PID / "fiche.md").write_text("---\nfiche: done\n---\n")
        self.assertNotEqual(a, snapshot.fingerprint(self.root))

    def test_entry_and_append(self):
        now = datetime.datetime(2026, 10, 18, 12, 0)
        line = answerlog.entry(self.root, ROOT, RECORD, "test", now=now)
        sha = rag.sha1(rag.load_chunks(self.root)[0]["text"])[:8]
        self.assertEqual(line["passages"], {"1612.07119#001.0": sha, "1612.07119#009.0": None})
        self.assertEqual(line["snapshot"], snapshot.fingerprint(self.root))
        self.assertEqual((line["base"], line["date"]), ("test", "2026-10-18T12:00:00"))
        path = answerlog.append(self.root, line, now=now)
        self.assertEqual(path, self.root / ".cache" / "answers" / "2026-10.jsonl")
        answerlog.append(self.root, line, now=now)
        self.assertEqual(len(path.read_text().splitlines()), 2)

    def test_invalid_record(self):
        with self.assertRaises(ValueError):
            answerlog.entry(self.root, ROOT, {"id": "x", "verdict": "peut-être", "claims": []}, "test")

    def test_enabled(self):
        self.assertFalse(answerlog.enabled({}))
        self.assertTrue(answerlog.enabled({"log_answers": True}))


if __name__ == "__main__":
    unittest.main()
