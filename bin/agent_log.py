#!/usr/bin/env python3
"""Hook SubagentStop de Claude Code : une ligne par sous-agent dans .cache/agents.jsonl.

Branché dans .claude/settings.json (lié dans chaque base). Lit sur stdin le JSON du hook
(session_id, transcript_path, agent_id, agent_transcript_path), relit le transcript du
sous-agent et ajoute la ligne au journal (lib/agentlog.py, docs/AMELIORATIONS.md lot I).
Ne bloque jamais la session : toute erreur va dans .cache/agents.errors.log, sortie 0.
PDB_AGENTLOG_RAW=1 : copie aussi l'entrée brute dans .cache/agents.raw.jsonl.

Au moment du hook, le dernier tour du sous-agent n'est souvent pas encore écrit dans son
transcript (réponse finale et son usage manquants). Si la ligne écrite est incomplète, un
processus détaché (`--refresh`) relit le transcript jusqu'à ce qu'il soit complet
(PDB_AGENTLOG_WAIT secondes au plus, 60 par défaut) et ajoute la ligne corrigée ; le journal
fusionne les deux par agent_id.
"""
import datetime
import json
import os
import subprocess
import sys
import traceback
from pathlib import Path

CODE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(CODE))


def subagent_transcript(event):
    p = event.get("agent_transcript_path")
    if p:
        return Path(p)
    tp, aid, sid = event.get("transcript_path"), event.get("agent_id"), event.get("session_id")
    if not (tp and aid):
        raise ValueError("entrée sans agent_transcript_path ni (transcript_path, agent_id)")
    return Path(tp).parent / (sid or Path(tp).stem) / "subagents" / f"agent-{aid}.jsonl"


def refresh(path, session_transcript):
    """Processus détaché : attend le transcript complet, puis réécrit la ligne."""
    from lib import agentlog
    try:
        wait = float(os.environ.get("PDB_AGENTLOG_WAIT", "60"))
        agentlog.append(agentlog.wait_complete(path, session_transcript or None, timeout=wait))
    except Exception:
        _log_error(f"--refresh {path}")


def _log_error(raw):
    from lib import agentlog
    try:
        d = agentlog.journal_dir()
        d.mkdir(parents=True, exist_ok=True)
        with open(d / "agents.errors.log", "a", encoding="utf-8") as f:
            f.write(f"--- {datetime.datetime.now().isoformat(timespec='seconds')}\n"
                    f"{raw[:2000]}\n{traceback.format_exc()}")
    except Exception:
        pass


def main():
    from lib import agentlog
    if sys.argv[1:2] == ["--refresh"]:
        return refresh(*sys.argv[2:4])
    raw = sys.stdin.read()
    try:
        if os.environ.get("PDB_AGENTLOG_RAW") == "1":
            d = agentlog.journal_dir()
            d.mkdir(parents=True, exist_ok=True)
            with open(d / "agents.raw.jsonl", "a", encoding="utf-8") as f:
                f.write(raw.strip() + "\n")
        event = json.loads(raw)
        rec = agentlog.parse_subagent(subagent_transcript(event))
        tp = event.get("transcript_path")
        agentlog.enrich_from_parent(rec, tp or agentlog.session_transcript_of(subagent_transcript(event)))
        agentlog.append(rec)
        if rec["status"] != "ok":
            subprocess.Popen([sys.executable, str(Path(__file__).resolve()), "--refresh",
                              str(subagent_transcript(event)), tp or ""],
                             stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL, start_new_session=True)
    except Exception:
        _log_error(raw)
    return 0


if __name__ == "__main__":
    try:
        main()
    finally:
        sys.exit(0)
