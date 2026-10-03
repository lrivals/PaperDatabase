"""Journal et coût des sous-agents Claude Code (docs/AMELIORATIONS.md, lot I).

Une ligne JSON par sous-agent dans CODE/.cache/agents.jsonl (ou $PDB_AGENTLOG_DIR/agents.jsonl),
tirée du transcript du sous-agent :
  ~/.claude/projects/<projet>/<session>/subagents/agent-<id>.jsonl  (+ agent-<id>.meta.json)
Le résultat de l'outil Agent ne porte pas de tokens (agents lancés en arrière-plan :
status « async_launched ») ; seul le transcript donne `message.usage` tour par tour. Une même
réponse s'étale sur plusieurs lignes (un bloc de contenu par ligne, même `message.id`) : on
déduplique par `message.id`.

Deux entrées : le hook SubagentStop (bin/agent_log.py) et `pdb agents --scan` (rattrapage des
sessions passées). Le journal est en ajout seul ; `load` fusionne les lignes d'un même agent
(la dernière valeur non nulle l'emporte), ce qui rend `--mark` et les reprises d'agent sûrs.

Stdlib seulement : le hook tourne avec le python3 du système, sans .venv.
"""
import json
import os
import re
import statistics
from collections import Counter
from pathlib import Path

CODE = Path(__file__).resolve().parent.parent
PRICES = Path(__file__).resolve().parent / "agent_prices.json"
PROJECTS = Path.home() / ".claude" / "projects"
VERDICTS = ("repris", "corrigé", "refait")
TASK_RE = re.compile(r"^\s*\[([\w-]+)\]\s*(.*)$", re.S)
STARTUP_WARN = 0.5  # surcoût de démarrage au-delà duquel la tâche est trop petite pour un agent


def journal_dir(env=None):
    env = os.environ if env is None else env
    return Path(env["PDB_AGENTLOG_DIR"]) if env.get("PDB_AGENTLOG_DIR") else CODE / ".cache"


def journal_path(env=None):
    return journal_dir(env) / "agents.jsonl"


def task_class(description):
    """« [paper-fiche] fiche de x » → ("paper-fiche", "fiche de x") ; sans crochets : « autre »."""
    m = TASK_RE.match(description or "")
    return (m.group(1), m.group(2).strip()) if m else ("autre", (description or "").strip())


def _read_jsonl(path):
    out = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out


def _assistant_messages(lines, sidechain=None):
    """Messages assistant uniques (par message.id), dans l'ordre, hors <synthetic>."""
    seen, msgs = set(), []
    for d in lines:
        if d.get("type") != "assistant":
            continue
        if sidechain is not None and bool(d.get("isSidechain")) != sidechain:
            continue
        m = d.get("message") or {}
        if m.get("model") == "<synthetic>":
            continue
        mid = m.get("id") or d.get("uuid")
        if mid in seen:
            continue
        seen.add(mid)
        msgs.append(m)
    return msgs


def _usage_sum(msgs):
    tot = Counter()
    for m in msgs:
        u = m.get("usage") or {}
        tot["input_tokens"] += u.get("input_tokens") or 0
        tot["output_tokens"] += u.get("output_tokens") or 0
        tot["cache_read"] += u.get("cache_read_input_tokens") or 0
        tot["cache_creation"] += u.get("cache_creation_input_tokens") or 0
        tot["cache_creation_1h"] += (u.get("cache_creation") or {}).get("ephemeral_1h_input_tokens") or 0
    return tot


def _turn_tokens(m):
    u = m.get("usage") or {}
    return sum(u.get(k) or 0 for k in ("input_tokens", "output_tokens", "cache_read_input_tokens",
                                       "cache_creation_input_tokens"))


def _tool_uses(lines):
    """tool_use du transcript, dédupliqués par id."""
    seen, out = set(), []
    for d in lines:
        if d.get("type") != "assistant":
            continue
        for c in (d.get("message") or {}).get("content") or []:
            if isinstance(c, dict) and c.get("type") == "tool_use" and c.get("id") not in seen:
                seen.add(c.get("id"))
                out.append(c)
    return out


def _big_read(tool):
    """Lecture intégrale de fulltext.md (Read sans limit, ou cat dans Bash)."""
    inp = tool.get("input") or {}
    if tool.get("name") == "Read":
        return str(inp.get("file_path", "")).endswith("fulltext.md") and not inp.get("limit")
    if tool.get("name") == "Bash":
        return bool(re.search(r"\bcat\b[^|;&]*fulltext\.md", str(inp.get("command", ""))))
    return False


def base_of(cwd):
    """Nom de la base active pour `cwd` (même règle que les commandes) ; None si indéterminé."""
    if not cwd:
        return None
    try:
        import sys
        if str(CODE) not in sys.path:
            sys.path.insert(0, str(CODE))
        from lib import base, registry
        env = {k: v for k, v in os.environ.items() if k not in ("PDB_ROOT", "PDB_BASE")}
        root = base.data_root(env=env, cwd=cwd)
        return registry.name_of(root, env) or root.name
    except Exception:
        return None


def parse_subagent(path):
    """Enregistrement du journal pour un transcript de sous-agent."""
    path = Path(path)
    lines = _read_jsonl(path)
    meta_p = path.with_name(path.name[:-len(".jsonl")] + ".meta.json")
    meta = json.loads(meta_p.read_text(encoding="utf-8")) if meta_p.is_file() else {}
    msgs = _assistant_messages(lines)
    tools = _tool_uses(lines)
    stamps = sorted(d["timestamp"] for d in lines if d.get("timestamp"))
    first = next((d for d in lines if d.get("sessionId")), {})
    models = Counter(m.get("model") for m in msgs if m.get("model"))
    last = msgs[-1] if msgs else {}
    result = "".join(c.get("text", "") for c in last.get("content") or []
                     if isinstance(c, dict) and c.get("type") == "text")
    agent_id = first.get("agentId") or path.stem.removeprefix("agent-")
    cls, desc = task_class(meta.get("description", ""))
    usage = _usage_sum(msgs)
    dur = None
    if len(stamps) >= 2:
        from datetime import datetime
        t0, t1 = (datetime.fromisoformat(s.replace("Z", "+00:00")) for s in (stamps[0], stamps[-1]))
        dur = int((t1 - t0).total_seconds() * 1000)
    return {
        "ts": stamps[0] if stamps else None, "session_id": first.get("sessionId"),
        "agent_id": agent_id, "cwd": first.get("cwd"), "base": base_of(first.get("cwd")),
        "task_class": cls, "description": desc,
        "subagent_type": meta.get("agentType"), "model_requested": None,
        "model_served": models.most_common(1)[0][0] if models else None,
        **usage, "total_tokens": sum(usage[k] for k in ("input_tokens", "output_tokens", "cache_read",
                                                        "cache_creation")),
        "first_turn_tokens": _turn_tokens(msgs[0]) if msgs else 0, "turns": len(msgs),
        "duration_ms": dur, "tool_calls": len(tools),
        "tools": dict(Counter(t.get("name") for t in tools)),
        "big_reads": sum(map(_big_read, tools)),
        "status": "ok" if last.get("stop_reason") == "end_turn" else "interrompu",
        "prompt_chars": None, "result_chars": len(result), "verified": None,
        "background": meta.get("requestShape") == "background" if meta else None,
        "_tool_use_id": meta.get("toolUseId"), "transcript": str(path),
    }


def enrich_from_parent(rec, session_transcript):
    """Complète avec l'appel Agent de l'agent principal : modèle demandé, taille du prompt."""
    tid = rec.pop("_tool_use_id", None)
    p = Path(session_transcript) if session_transcript else None
    if not tid or not p or not p.is_file():
        return rec
    with open(p, encoding="utf-8") as f:
        for line in f:
            if tid not in line:
                continue
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            for c in (d.get("message") or {}).get("content") or []:
                if isinstance(c, dict) and c.get("type") == "tool_use" and c.get("id") == tid:
                    inp = c.get("input") or {}
                    rec["model_requested"] = inp.get("model")
                    rec["prompt_chars"] = len(inp.get("prompt") or "")
                    rec["subagent_type"] = rec.get("subagent_type") or inp.get("subagent_type")
                    if not rec.get("description") and inp.get("description"):
                        rec["task_class"], rec["description"] = task_class(inp["description"])
                    return rec
    return rec


def session_transcript_of(subagent_path):
    """<projet>/<session>/subagents/agent-x.jsonl → <projet>/<session>.jsonl"""
    sess_dir = Path(subagent_path).parent.parent
    return sess_dir.with_name(sess_dir.name + ".jsonl")


def record_for(subagent_path):
    rec = parse_subagent(subagent_path)
    return enrich_from_parent(rec, session_transcript_of(subagent_path))


def append(rec, env=None):
    p = journal_path(env)
    p.parent.mkdir(parents=True, exist_ok=True)
    rec = {k: v for k, v in rec.items() if not k.startswith("_")}
    with open(p, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def load(env=None):
    """Journal fusionné par agent_id, dans l'ordre de première apparition."""
    p = journal_path(env)
    if not p.is_file():
        return []
    acc = {}
    for d in _read_jsonl(p):
        if d.get("agent_id"):
            acc.setdefault(d["agent_id"], {}).update({k: v for k, v in d.items() if v is not None})
    return [r for r in acc.values() if "total_tokens" in r]


def mark(prefix, verdict, env=None):
    """Note ce que l'agent principal a fait du résultat ; renvoie l'agent_id visé."""
    if verdict not in VERDICTS:
        raise ValueError(f"verdict inconnu : {verdict} ({', '.join(VERDICTS)})")
    hits = [r["agent_id"] for r in load(env)
            if r["agent_id"].startswith(prefix) or (r.get("ts") or "").startswith(prefix)]
    if len(hits) != 1:
        raise ValueError(f"{prefix!r} désigne {len(hits)} agents (il en faut un)")
    append({"agent_id": hits[0], "verified": verdict}, env)
    return hits[0]


# ---------------------------------------------------------------- rattrapage (I-c)

def project_dirs(roots, projects=None):
    """Dossiers ~/.claude/projects/ des sessions ouvertes dans `roots` ou en dessous."""
    projects = Path(projects or PROJECTS)
    if not projects.is_dir():
        return []
    keys = [re.sub(r"[^A-Za-z0-9]", "-", str(Path(r).resolve())) for r in roots]
    return sorted(d for d in projects.iterdir()
                  if d.is_dir() and any(d.name == k or d.name.startswith(k + "-") for k in keys))


def scan(roots, env=None, projects=None, force=False):
    """Ajoute au journal les sous-agents des transcripts passés ; renvoie (ajoutés, erreurs)."""
    known = {r["agent_id"] for r in load(env)}
    added, errors = 0, []
    for d in project_dirs(roots, projects):
        for t in sorted(d.glob("*/subagents/agent-*.jsonl")):
            aid = t.stem.removeprefix("agent-")
            if aid in known and not force:
                continue
            try:
                append(record_for(t), env)
                added += 1
            except Exception as e:  # un transcript abîmé ne bloque pas le rattrapage
                errors.append(f"{t}: {e}")
    return added, errors


def main_session_usage(session_transcript):
    """Tokens de l'agent principal d'une session (témoin I-c), hors sous-agents."""
    p = Path(session_transcript)
    if not p.is_file():
        return None
    msgs = _assistant_messages(_read_jsonl(p), sidechain=False)
    u = _usage_sum(msgs)
    models = Counter(m.get("model") for m in msgs if m.get("model"))
    return {**u, "total_tokens": sum(u[k] for k in ("input_tokens", "output_tokens", "cache_read",
                                                    "cache_creation")),
            "turns": len(msgs), "model_served": models.most_common(1)[0][0] if models else None}


# ---------------------------------------------------------------- coût et rapport (I-3)

def load_prices(path=None):
    p = Path(path or PRICES)
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}


def _price_for(model, prices):
    models = prices.get("models", {})
    if not model:
        return None
    if model in models:
        return models[model]
    for key in sorted(models, key=len, reverse=True):  # identifiant daté : claude-x-AAAAMMJJ
        if model.startswith(key):
            return models[key]
    return None


def cost(rec, prices):
    """Coût en dollars, ou None si le modèle n'a pas de tarif."""
    p = _price_for(rec.get("model_served"), prices)
    if p is None:
        return None
    w5, w1h = prices.get("cache_write_5m", 1.25), prices.get("cache_write_1h", 2.0)
    c1h = rec.get("cache_creation_1h") or 0
    c5 = (rec.get("cache_creation") or 0) - c1h
    return ((rec.get("input_tokens") or 0) * p["input"] + (rec.get("output_tokens") or 0) * p["output"]
            + (rec.get("cache_read") or 0) * p["cache_read"]
            + c5 * p["input"] * w5 + c1h * p["input"] * w1h) / 1e6


def _p90(xs):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(round(0.9 * (len(xs) - 1))))]


def _short_model(m):
    return (m or "?").removeprefix("claude-")


GROUPS = {"task": ("task_class",), "model": ("model_served",), "base": ("base",),
          "task-model": ("task_class", "model_served")}


def summarize(records, by="task-model", prices=None):
    """Lignes du rapport : une par groupe, indicateurs I-3."""
    keys = GROUPS[by]
    groups = {}
    for r in records:
        groups.setdefault(tuple(r.get(k) or "?" for k in keys), []).append(r)
    rows = []
    for g, rs in sorted(groups.items(), key=lambda kv: -sum(x.get("total_tokens", 0) for x in kv[1])):
        tot = [r.get("total_tokens") or 0 for r in rs]
        costs = [c for c in (cost(r, prices or {}) for r in rs) if c is not None]
        start = [r["first_turn_tokens"] / r["total_tokens"] for r in rs if r.get("total_tokens")]
        reads = sum(r.get("cache_read") or 0 for r in rs)
        fresh = sum((r.get("input_tokens") or 0) + (r.get("cache_creation") or 0) for r in rs)
        marked = [r["verified"] for r in rs if r.get("verified")]
        durs = [r["duration_ms"] for r in rs if r.get("duration_ms") is not None]
        rows.append({
            "group": " · ".join(_short_model(x) if k == "model_served" else str(x)
                                for k, x in zip(keys, g)),
            "n": len(rs), "tokens_med": statistics.median(tot), "tokens_p90": _p90(tot),
            "cost": sum(costs) if costs else None,
            "cost_med": statistics.median(costs) if costs else None,
            "startup_med": statistics.median(start) if start else None,
            "first_med": statistics.median(r.get("first_turn_tokens") or 0 for r in rs),
            "cache_share": reads / (reads + fresh) if reads + fresh else None,
            "rework": (sum(v != "repris" for v in marked), len(marked)),
            "dur_med_s": statistics.median(durs) / 1000 if durs else None,
            "big_reads": sum(r.get("big_reads") or 0 for r in rs),
        })
    return rows


def _k(x):
    return "—" if x is None else f"{x / 1000:.0f}k" if x >= 1000 else str(int(x))


def _pct(x):
    return "—" if x is None else f"{100 * x:.0f} %"


def _usd(x):
    return "—" if x is None else f"{x:.2f} $"


def report(records, by="task-model", prices=None, main=None):
    """Rapport Markdown ; `main` = {session_id: usage de l'agent principal} (témoin)."""
    prices = load_prices() if prices is None else prices
    if not records:
        return "Journal vide : aucun sous-agent enregistré (bin/pdb agents --scan pour rattraper)."
    out = [f"## Sous-agents ({len(records)} appels)", "",
           "| groupe | appels | tokens méd. | p90 | coût | coût méd. | 1er tour méd. | démarrage méd. | cache | "
           "reprise | durée méd. | lectures fulltext |",
           "|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|"]
    for r in summarize(records, by, prices):
        bad, n = r["rework"]
        start = _pct(r["startup_med"]) + (" ⚠" if (r["startup_med"] or 0) > STARTUP_WARN else "")
        rework = f"{bad}/{n}" if n else "—"
        dur = "—" if r["dur_med_s"] is None else f"{r['dur_med_s']:.0f} s"
        out.append(f"| {r['group']} | {r['n']} | {_k(r['tokens_med'])} | {_k(r['tokens_p90'])} | "
                   f"{_usd(r['cost'])} | {_usd(r['cost_med'])} | {_k(r['first_med'])} | {start} | {_pct(r['cache_share'])} | "
                   f"{rework} | {dur} | {r['big_reads'] or ''} |")
    total = [c for c in (cost(r, prices) for r in records) if c is not None]
    out += ["", f"Total sous-agents : {_k(sum(r.get('total_tokens') or 0 for r in records))} tokens, "
                f"{_usd(sum(total) if total else None)}."]
    unmarked = sum(1 for r in records if not r.get("verified"))
    if unmarked:
        out.append(f"Issue non notée pour {unmarked} appel(s) : bin/pdb agents --mark <id> "
                   f"{'|'.join(VERDICTS)}.")
    out.append(f"1er tour : contexte de départ (prompt système, outils, tâche), coût fixe de chaque agent. "
               f"Démarrage : 1er tour / tokens ; ⚠ au-delà de {int(STARTUP_WARN * 100)} %, tâche sans doute "
               "trop petite pour être déléguée. Tokens : lectures de cache comprises, recomptées à chaque tour.")
    if main:
        sub = Counter()
        for r in records:
            sub[r.get("session_id")] += cost(r, prices) or 0
        out += ["", f"## Agent principal (témoin, {len(main)} sessions)", "",
                "| session | modèle | tours | tokens | coût | coût sous-agents |", "|---|---|--:|--:|--:|--:|"]
        for sid, u in sorted(main.items(), key=lambda kv: -(kv[1] or {}).get("total_tokens", 0)):
            if not u:
                continue
            out.append(f"| {sid[:8]} | {_short_model(u['model_served'])} | {u['turns']} | "
                       f"{_k(u['total_tokens'])} | {_usd(cost(u, prices))} | {_usd(sub[sid])} |")
    return "\n".join(out)
