"""Tests de lib/status.py (état de la base, prochaines actions).

.venv/bin/python -m unittest discover tests
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from lib import schema, status  # noqa: E402


def _state(**kw):
    s = {"venv": True, "docker": True, "grobid": True, "inbox": [], "todo": [],
         "done_after_gaps": 0, "axes": {a: 5 for a in schema.AXES}, "git_dirty": 0}
    s.update(kw)
    return s


class TestNextActions(unittest.TestCase):
    def test_priorities(self):
        acts = status.next_actions(_state(grobid=False, inbox=["a.pdf"], todo=["p1", "p2"]))
        self.assertEqual([a[0] for a in acts],
                         ["bin/pdb grobid start", "bin/pdb ingest", "/paper-fiche p1"])

    def test_gaps_then_thin_axis(self):
        axes = {a: 5 for a in schema.AXES}
        axes["autoencoder-fpga"] = 1
        acts = status.next_actions(_state(done_after_gaps=4, axes=axes))
        self.assertEqual([a[0] for a in acts], ["/paper-gaps", "/paper-discover autoencoder-fpga"])

    def test_all_done_suggests_discover(self):
        self.assertEqual(status.next_actions(_state())[0][0], "/paper-discover")


class TestCollect(unittest.TestCase):
    def test_minimal_corpus(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for pid, fiche, axes in (("p1", "done", ["yolo-fpga"]), ("p2", "todo", ["yolo-fpga"])):
                (root / "papers" / pid).mkdir(parents=True)
                (root / "papers" / pid / "metadata.json").write_text(json.dumps(
                    {"id": pid, "axes": axes, "status": {"fiche": fiche},
                     "extraction": {"ok": pid == "p1", "warnings": ["w"]}}))
                (root / "papers" / pid / "fiche.md").write_text("x")
            (root / "inbox").mkdir()
            (root / "inbox" / "new.pdf").write_bytes(b"%PDF")
            (root / "gaps.md").write_text("intro\n---\n### G1\n- Statut : étayé\n### G2\n- Statut : hypothèse\n")
            s = status.collect(root, check_services=False)
        self.assertEqual((s["n_papers"], s["n_done"], s["todo"]), (2, 1, ["p2"]))
        self.assertEqual(s["axes"]["yolo-fpga"], 2)
        self.assertEqual(s["inbox"], ["new.pdf"])
        self.assertEqual((s["n_gaps"], s["n_gaps_backed"]), (2, 1))
        self.assertEqual(s["extraction_issues"], [("p2", 1)])
        self.assertIn("À faire ensuite", status.render(s))


if __name__ == "__main__":
    unittest.main()
