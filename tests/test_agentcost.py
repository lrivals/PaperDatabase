"""Tests de lib/agentcost.py (économie de la délégation, calage sur le cost-state, lot I).

.venv/bin/python -m unittest discover tests
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from lib import agentcost, agentlog  # noqa: E402

SID = "sess-2"
MAIN, SUB = "claude-big", "claude-small"
PRICES = {"cache_write_5m": 1.25, "cache_write_1h": 2.0,
          "models": {MAIN: {"input": 10.0, "output": 50.0, "cache_read": 1.0},
                     SUB: {"input": 2.0, "output": 10.0, "cache_read": 0.2}}}
WRITTEN, SHARED = "/w/out.md", "/r/shared.md"


def _usage(inp, out, read=0, write=0):
    return {"input_tokens": inp, "output_tokens": out, "cache_read_input_tokens": read,
            "cache_creation_input_tokens": write,
            "cache_creation": {"ephemeral_5m_input_tokens": write, "ephemeral_1h_input_tokens": 0}}


def _ts(s):
    return f"2026-10-03T10:{s // 60:02d}:{s % 60:02d}Z"


def _msg(mid, sec, content, usage, model, stop="tool_use", aid=None):
    d = {"type": "assistant", "sessionId": SID, "cwd": "/nowhere", "timestamp": _ts(sec),
         "message": {"id": mid, "model": model, "role": "assistant", "content": content,
                     "stop_reason": stop, "usage": usage}}
    if aid:
        d.update(isSidechain=True, agentId=aid)
    return d


def _user(sec, content, aid=None):
    d = {"type": "user", "sessionId": SID, "cwd": "/nowhere", "timestamp": _ts(sec),
         "message": {"role": "user", "content": content}}
    if aid:
        d.update(isSidechain=True, agentId=aid)
    return d


def _result(tid, text):
    return [{"type": "tool_result", "tool_use_id": tid, "content": text}]


def _subagent(sub_dir, aid, tool_id, t0, reads, writes=(), result="fini", incomplete=False):
    """Sous-agent de 3 tours : contexte 1000 → 3000 → 5000, sortie 100 par tour."""
    lines, tid = [_user(t0, "go", aid)], 0
    ctx = 1000
    for i, path in enumerate(reads):
        tid += 1
        lines += [_msg(f"{aid}-r{i}", t0 + 1 + i, [{"type": "tool_use", "id": f"{aid}-t{tid}", "name": "Read",
                                                    "input": {"file_path": path}}],
                       _usage(1, 100, read=ctx - 1), SUB, stop=None if incomplete else "tool_use", aid=aid),
                  _user(t0 + 1 + i, _result(f"{aid}-t{tid}", "x" * 7000), aid)]
        ctx += 2000
    for i, path in enumerate(writes):
        tid += 1
        lines += [_msg(f"{aid}-w{i}", t0 + 5 + i, [{"type": "tool_use", "id": f"{aid}-t{tid}", "name": "Write",
                                                    "input": {"file_path": path, "content": "z"}}],
                       _usage(1, 100, read=ctx - 1), SUB, aid=aid),
                  _user(t0 + 5 + i, _result(f"{aid}-t{tid}", "ok"), aid)]
    lines.append(_msg(f"{aid}-end", t0 + 20, [{"type": "text", "text": result}],
                      _usage(1, 100, read=ctx - 1), SUB, stop="end_turn", aid=aid))
    p = sub_dir / f"agent-{aid}.jsonl"
    p.write_text("".join(json.dumps(x) + "\n" for x in lines))
    p.with_name(f"agent-{aid}.meta.json").write_text(json.dumps({"description": f"[paper-fiche] {aid}",
                                                                 "toolUseId": tool_id}))
    return p


def write_project(projects, after=20, compact_at=None, main_ctx=10_000, cost_state=None, incomplete=False):
    """Session : deux agents lancés ensemble (lisent le même fichier), retour, `after` tours
    principaux dont une relecture du fichier écrit par l'agent A."""
    proj = projects / "-repo"
    sub_dir = proj / SID / "subagents"
    sub_dir.mkdir(parents=True)
    paths = [_subagent(sub_dir, "aaa", "TA", 1, [SHARED], [WRITTEN], result="r" * 350, incomplete=incomplete),
             _subagent(sub_dir, "bbb", "TB", 30, [SHARED, "/r/other.md"])]
    main = [_msg("p0", 0, [{"type": "tool_use", "id": "TA", "name": "Agent",
                            "input": {"description": "a", "prompt": "p" * 70, "model": "sonnet"}},
                           {"type": "tool_use", "id": "TB", "name": "Agent",
                            "input": {"description": "b", "prompt": "p" * 70, "model": "sonnet"}}],
                    _usage(1, 50, read=main_ctx - 1), MAIN),
            _user(0, _result("TA", "Async agent launched")),
            _user(100, "<task-notification><task-id>aaa</task-id>fini</task-notification>"),
            _user(101, "<task-notification><task-id>bbb</task-id>fini</task-notification>")]
    for i in range(after):
        ctx = main_ctx if compact_at is None or i < compact_at else main_ctx // 4
        content = [{"type": "text", "text": "ok"}]
        if i == 0:
            content = [{"type": "tool_use", "id": "TV", "name": "Read", "input": {"file_path": WRITTEN}}]
        main.append(_msg(f"p{i + 1}", 110 + i, content, _usage(1, 50, read=ctx - 1), MAIN))
        if i == 0:
            main.append(_user(110, _result("TV", "v" * 3500)))
    if cost_state:
        main.append({"type": "cost-state", **cost_state})
    (proj / f"{SID}.jsonl").write_text("".join(json.dumps(x) + "\n" for x in main))
    return [agentlog.record_for(p) for p in paths]


class TestSavings(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def _rows(self, **kw):
        recs = write_project(self.dir / "projects", **kw)
        sessions = agentcost.load_sessions(recs)
        return {r["agent_id"]: r for r in agentcost.savings(recs, sessions, PRICES)}, sessions

    def test_session_parsing(self):
        _, sessions = self._rows()
        s = sessions[SID]
        self.assertEqual(s.model, MAIN)
        self.assertEqual(set(s.returns), {"aaa", "bbb"})
        self.assertEqual(len(s.turns), 21)
        self.assertEqual(s.compactions, [])
        self.assertEqual(s.context_at("TA", None), 10_000)

    def test_delegation_pays_with_cheaper_model(self):
        rows, _ = self._rows()
        a = rows["aaa"]
        self.assertEqual((a["after"], a["after_direct"], a["c0"]), (20, 20, 10_000))
        self.assertGreater(a["direct"], a["delegated"])
        self.assertGreater(a["saved"], 0)
        self.assertNotIn("même modèle", a["causes"])

    def test_verification_cost(self):
        rows, _ = self._rows()
        self.assertGreater(rows["aaa"]["verify"], 0)  # relecture de /w/out.md après le retour
        self.assertEqual(rows["bbb"]["verify"], 0)    # bbb n'a rien écrit

    def test_duplicate_reads(self):
        rows, _ = self._rows()
        self.assertEqual(rows["aaa"]["dup_tokens"], 0)
        self.assertEqual(rows["bbb"]["dup_tokens"], 2000)  # /r/shared.md, déjà lu par aaa

    def test_real_compaction_cuts_after(self):
        rows, _ = self._rows(compact_at=5)
        self.assertEqual(rows["aaa"]["after"], 5)
        self.assertEqual(rows["aaa"]["after_direct"], 5)

    def test_simulated_compaction_cuts_direct_only(self):
        with mock.patch.object(agentcost, "CONTEXT_LIMIT", 10_000 + 2000 + 4000 - 1):
            rows, _ = self._rows()
        self.assertEqual(rows["aaa"]["after"], 20)       # délégué : le résultat reste en contexte
        self.assertEqual(rows["aaa"]["after_direct"], 0)  # direct : G(aaa) + G(bbb) déborde

    def test_end_of_session_and_redo(self):
        recs = write_project(self.dir / "projects", after=3)
        recs[0]["verified"] = "refait"
        sessions = agentcost.load_sessions(recs)
        a = {r["agent_id"]: r for r in agentcost.savings(recs, sessions, PRICES)}["aaa"]
        self.assertIn("fin de session", a["causes"])
        self.assertIn("refait", a["causes"])
        self.assertAlmostEqual(a["saved"], -(a["delegated"] + a["verify"]))

    def test_reports_render(self):
        recs = write_project(self.dir / "projects")
        sessions = agentcost.load_sessions(recs)
        out = agentcost.report_savings(agentcost.savings(recs, sessions, PRICES), worst=1)
        self.assertIn("Économie de la délégation", out)
        self.assertIn("Cas défavorables (1", out)
        self.assertIn("sess-2", agentcost.report_session("sess", recs, PRICES))


class TestCalibrate(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def _state(self, sub_reads, sub_out):
        main_reads = 10_000 - 1 + 20 * (10_000 - 1)
        return {"modelUsage": {MAIN: {"outputTokens": 50 * 21, "cacheReadInputTokens": main_reads},
                               SUB: {"outputTokens": sub_out, "cacheReadInputTokens": sub_reads}},
                "totalCostUSD": 1.0}

    def _calibrated(self, sub_reads, sub_out, incomplete=True):
        recs = write_project(self.dir / "projects", cost_state=self._state(sub_reads, sub_out),
                             incomplete=incomplete)
        sessions = agentcost.load_sessions(recs)
        return recs, {r["agent_id"]: r for r in agentcost.calibrate(recs, sessions)}

    def test_missing_output_spread(self):
        recs, cal = self._calibrated(sub_reads=15_994, sub_out=10_000)
        reads = sum(r["cache_read"] for r in recs)
        self.assertEqual(reads, 15_994)  # garde-fou du test : lectures de cache concordantes
        self.assertEqual(sum(r["output_tokens"] for r in cal.values()), 10_000)
        self.assertEqual(cal["aaa"]["output_source"], "calé")
        self.assertEqual(cal["bbb"]["output_source"], "calé")
        self.assertEqual(recs[0]["output_source"], "transcript")  # l'original n'est pas modifié

    def test_no_calibration_when_reads_disagree(self):
        recs, cal = self._calibrated(sub_reads=50_000, sub_out=10_000)
        self.assertEqual([r["output_tokens"] for r in recs], [cal[r["agent_id"]]["output_tokens"] for r in recs])
        self.assertEqual(cal["aaa"]["output_source"], "transcript")


if __name__ == "__main__":
    unittest.main()
