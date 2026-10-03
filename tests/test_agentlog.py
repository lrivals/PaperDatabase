"""Tests de lib/agentlog.py et du hook bin/agent_log.py (journal des sous-agents, lot I).

.venv/bin/python -m unittest discover tests
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from lib import agentlog  # noqa: E402

SID = "sess-1"
AID = "abc123"
TOOL_ID = "toolu_parent"


def _assistant(mid, ts, content, usage, model="claude-sonnet-5-5", stop="tool_use"):
    return {"type": "assistant", "isSidechain": True, "agentId": AID, "sessionId": SID,
            "cwd": "/nowhere", "timestamp": ts,
            "message": {"id": mid, "model": model, "role": "assistant", "content": content,
                        "stop_reason": stop, "usage": usage}}


def _usage(inp, out, read=0, write=0, write_1h=0):
    return {"input_tokens": inp, "output_tokens": out, "cache_read_input_tokens": read,
            "cache_creation_input_tokens": write,
            "cache_creation": {"ephemeral_5m_input_tokens": write - write_1h,
                               "ephemeral_1h_input_tokens": write_1h}}


def write_session(projects, description="[paper-fiche] fiche de x"):
    """Projet factice : transcript principal + un sous-agent (message m1 sur deux lignes)."""
    proj = projects / "-repo"
    sub = proj / SID / "subagents"
    sub.mkdir(parents=True)
    u1 = _usage(10, 50, read=0, write=1000)
    lines = [
        {"type": "user", "isSidechain": True, "agentId": AID, "sessionId": SID, "cwd": "/nowhere",
         "timestamp": "2026-10-03T10:00:00Z", "message": {"role": "user", "content": "go"}},
        _assistant("m1", "2026-10-03T10:00:05Z", [{"type": "text", "text": "je lis"}], u1),
        _assistant("m1", "2026-10-03T10:00:05Z",
                   [{"type": "tool_use", "id": "t1", "name": "Read",
                     "input": {"file_path": "/b/papers/p/fulltext.md"}}], u1),
        _assistant("m2", "2026-10-03T10:00:20Z",
                   [{"type": "tool_use", "id": "t2", "name": "Bash", "input": {"command": "bin/pdb search x"}}],
                   _usage(5, 100, read=1000, write=200)),
        _assistant("syn", "2026-10-03T10:00:21Z", [{"type": "text", "text": "x"}], _usage(999, 999),
                   model="<synthetic>"),
        _assistant("m3", "2026-10-03T10:01:05Z", [{"type": "text", "text": "fini : 3 fichiers"}],
                   _usage(5, 200, read=1200, write=0), stop="end_turn"),
    ]
    t = sub / f"agent-{AID}.jsonl"
    t.write_text("".join(json.dumps(x) + "\n" for x in lines))
    (sub / f"agent-{AID}.meta.json").write_text(json.dumps(
        {"agentType": "general-purpose", "description": description, "toolUseId": TOOL_ID,
         "requestShape": "background"}))
    parent = [
        {"type": "assistant", "sessionId": SID, "timestamp": "2026-10-03T09:59:59Z",
         "message": {"id": "p1", "model": "claude-opus-5-5", "role": "assistant",
                     "content": [{"type": "tool_use", "id": TOOL_ID, "name": "Agent",
                                  "input": {"description": description, "model": "sonnet",
                                            "subagent_type": "general-purpose", "prompt": "x" * 42}}],
                     "usage": _usage(3, 30, read=5000, write=100)}},
    ]
    (proj / f"{SID}.jsonl").write_text("".join(json.dumps(x) + "\n" for x in parent))
    return t


class TestParse(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.t = write_session(self.dir / "projects")

    def tearDown(self):
        self.tmp.cleanup()

    def test_task_class(self):
        self.assertEqual(agentlog.task_class("[paper-add] lot 3"), ("paper-add", "lot 3"))
        self.assertEqual(agentlog.task_class("Fiches drone lot 0"), ("autre", "Fiches drone lot 0"))
        self.assertEqual(agentlog.task_class(None), ("autre", ""))

    def test_dedup_and_totals(self):
        r = agentlog.parse_subagent(self.t)
        self.assertEqual(r["turns"], 3)  # m1 sur deux lignes, <synthetic> ignoré
        self.assertEqual(r["input_tokens"], 20)
        self.assertEqual(r["output_tokens"], 350)
        self.assertEqual(r["cache_read"], 2200)
        self.assertEqual(r["cache_creation"], 1200)
        self.assertEqual(r["total_tokens"], 20 + 350 + 2200 + 1200)
        self.assertEqual(r["first_turn_tokens"], 1060)
        self.assertEqual(r["model_served"], "claude-sonnet-5-5")
        self.assertEqual(r["duration_ms"], 65000)
        self.assertEqual(r["tools"], {"Read": 1, "Bash": 1})
        self.assertEqual(r["big_reads"], 1)
        self.assertEqual((r["status"], r["result_chars"]), ("ok", len("fini : 3 fichiers")))
        self.assertEqual((r["task_class"], r["description"]), ("paper-fiche", "fiche de x"))

    def test_enrich_from_parent(self):
        r = agentlog.record_for(self.t)
        self.assertEqual(r["model_requested"], "sonnet")
        self.assertEqual(r["prompt_chars"], 42)
        self.assertNotIn("_tool_use_id", r)

    def test_scan_is_idempotent_and_mark(self):
        env = {"PDB_AGENTLOG_DIR": str(self.dir / "cache")}
        roots = ["/repo"]  # encodé en « -repo »
        self.assertEqual(agentlog.scan(roots, env, projects=self.dir / "projects"), (1, []))
        self.assertEqual(agentlog.scan(roots, env, projects=self.dir / "projects"), (0, []))
        self.assertEqual(agentlog.mark("abc", "corrigé", env), AID)
        agentlog.scan(roots, env, projects=self.dir / "projects", force=True)  # reprise de l'agent
        recs = agentlog.load(env)
        self.assertEqual(len(recs), 1)
        self.assertEqual(recs[0]["verified"], "corrigé")  # la relecture n'efface pas la note
        with self.assertRaises(ValueError):
            agentlog.mark("abc", "bof", env)
        with self.assertRaises(ValueError):
            agentlog.mark("zzz", "repris", env)

    def test_incomplete_response(self):
        """Sans stop_reason, l'usage journalisé est celui du début du flux : sortie estimée."""
        big = {"type": "tool_use", "id": "t9", "name": "Write",
               "input": {"file_path": "/x", "content": "y" * 3500}}
        lines = [_assistant("m9", "2026-10-03T10:00:00Z", [{"type": "text", "text": "a"}], _usage(1, 8), stop=None),
                 _assistant("m9", "2026-10-03T10:00:01Z", [big], _usage(1, 5, read=40), stop=None),
                 _assistant("m10", "2026-10-03T10:00:02Z", [{"type": "text", "text": "ok"}], _usage(1, 7),
                            stop="end_turn")]
        m9, m10 = agentlog._assistant_messages(lines)
        self.assertEqual(m9["usage"]["cache_read_input_tokens"], 40)  # usage max sur les lignes
        self.assertGreater(m9["usage"]["output_tokens"], 1000)        # ≈ 3 560 car. / 3,5
        self.assertTrue(m9.get("_estimated"))
        self.assertEqual(len(m9["content"]), 2)
        self.assertEqual(m10["usage"]["output_tokens"], 7)            # réponse complète : intacte
        self.assertFalse(m10.get("_estimated"))


class TestCostReport(unittest.TestCase):
    PRICES = {"cache_write_5m": 1.25, "cache_write_1h": 2.0,
              "models": {"claude-x": {"input": 2.0, "output": 10.0, "cache_read": 0.2}}}

    def _rec(self, **kw):
        r = {"agent_id": "a", "task_class": "paper-add", "model_served": "claude-x",
             "input_tokens": 1_000_000, "output_tokens": 0, "cache_read": 0, "cache_creation": 0,
             "cache_creation_1h": 0, "total_tokens": 1_000_000, "first_turn_tokens": 600_000,
             "duration_ms": 1000, "verified": None}
        r.update(kw)
        return r

    def test_cost(self):
        self.assertAlmostEqual(agentlog.cost(self._rec(), self.PRICES), 2.0)
        r = self._rec(input_tokens=0, output_tokens=1_000_000, cache_read=1_000_000,
                      cache_creation=2_000_000, cache_creation_1h=1_000_000)
        self.assertAlmostEqual(agentlog.cost(r, self.PRICES), 10 + 0.2 + 2 * 1.25 + 2 * 2.0)
        self.assertAlmostEqual(agentlog.cost(self._rec(model_served="claude-x-20260101"), self.PRICES), 2.0)
        self.assertIsNone(agentlog.cost(self._rec(model_served="inconnu"), self.PRICES))

    def test_summary_and_report(self):
        recs = [self._rec(agent_id="a", verified="repris"), self._rec(agent_id="b", verified="refait"),
                self._rec(agent_id="c", total_tokens=3_000_000)]
        row, = agentlog.summarize(recs, "task-model", self.PRICES)
        self.assertEqual((row["n"], row["tokens_med"], row["rework"]), (3, 1_000_000, (1, 2)))
        self.assertAlmostEqual(row["cost"], 6.0)
        self.assertEqual(row["group"], "paper-add · x")
        text = agentlog.report(recs, prices=self.PRICES)
        self.assertIn("| paper-add · x | 3 |", text)
        self.assertIn("⚠", text)  # 60 % des tokens au premier tour
        self.assertIn("Journal vide", agentlog.report([], prices=self.PRICES))


class TestHook(unittest.TestCase):
    def _run(self, stdin, cache):
        env = {**os.environ, "PDB_AGENTLOG_DIR": str(cache)}
        return subprocess.run([sys.executable, str(ROOT / "bin" / "agent_log.py")], input=stdin,
                              text=True, env=env, capture_output=True)

    def test_hook_appends(self):
        with tempfile.TemporaryDirectory() as d:
            t = write_session(Path(d) / "projects")
            sess = agentlog.session_transcript_of(t)
            ev = {"session_id": SID, "transcript_path": str(sess), "agent_id": AID}
            p = self._run(json.dumps(ev), Path(d) / "cache")
            self.assertEqual(p.returncode, 0)
            recs = agentlog.load({"PDB_AGENTLOG_DIR": str(Path(d) / "cache")})
            self.assertEqual([(r["agent_id"], r["model_requested"]) for r in recs], [(AID, "sonnet")])

    def test_hook_too_early_is_refreshed(self):
        """Hook passé avant l'écriture du dernier tour : ligne incomplète, puis corrigée."""
        with tempfile.TemporaryDirectory() as d:
            t = write_session(Path(d) / "projects")
            full = t.read_text()
            t.write_text("".join(full.splitlines(keepends=True)[:-1]))  # sans le tour final
            env = {"PDB_AGENTLOG_DIR": str(Path(d) / "cache")}
            ev = {"session_id": SID, "transcript_path": str(agentlog.session_transcript_of(t)), "agent_id": AID}
            self._run(json.dumps(ev), Path(d) / "cache")
            self.assertEqual(agentlog.load(env)[0]["status"], "interrompu")
            t.write_text(full)  # le tour final arrive
            rec = agentlog.wait_complete(t, timeout=5, poll=0.05)
            self.assertEqual((rec["status"], rec["turns"]), ("ok", 3))
            # --scan relit un agent journalisé incomplet, même sans --force
            self.assertEqual(agentlog.scan(["/repo"], env, projects=Path(d) / "projects"), (1, []))
            self.assertEqual(agentlog.load(env)[0]["status"], "ok")
            self.assertEqual(agentlog.scan(["/repo"], env, projects=Path(d) / "projects"), (0, []))

    def test_hook_never_fails(self):
        with tempfile.TemporaryDirectory() as d:
            for bad in ("", "{not json", json.dumps({"agent_id": "x"})):
                p = self._run(bad, Path(d))
                self.assertEqual(p.returncode, 0)
            self.assertTrue((Path(d) / "agents.errors.log").is_file())
            self.assertFalse((Path(d) / "agents.jsonl").exists())


if __name__ == "__main__":
    unittest.main()
