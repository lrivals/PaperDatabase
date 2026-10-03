"""Économie de la délégation : sous-agent contre travail fait par l'agent principal (lot I).

L'économie d'un sous-agent est un contrefactuel : la même tâche faite en direct n'est jamais
observée. On l'estime à partir du transcript principal de la session (même stdlib, mêmes
formats que lib/agentlog.py).

Ce qui coûte, au tarif de l'agent principal : tout ce qui entre dans son contexte (travail fait
en direct, ou résultat rendu par un agent) est écrit une fois en cache, puis **relu à chaque
tour suivant** jusqu'à la compaction ou la fin de session.

Pour un agent (T tours, sortie O, contexte accumulé G, résultat R, prompt P), lancé quand le
contexte principal vaut C0, et suivi de A tours principaux :
  délégué = coût réel du sous-agent + P × sortie + R × (écriture + A × lecture)
  direct  = O × sortie + G × écriture + (T × C0' + relectures internes) × lecture + G × A' × lecture
            (tarifs de l'agent principal ; mêmes tours qu'en délégué, sans coût de démarrage)
En direct, le travail des agents précédents reste aussi dans le contexte (C0' = C0 + leur G) ;
A' s'arrête à la compaction simulée, quand contexte réel + travail accumulé dépasse
CONTEXT_LIMIT (le travail accumulé repart alors de zéro).
  économie = direct − délégué − vérification
Vérification : relectures par l'agent principal des fichiers que l'agent a écrits. Un agent
noté « refait » est une perte sèche. Les lectures dupliquées entre agents d'un même lot sont
déjà dans le coût des agents : elles sont signalées, pas ajoutées.

Calage : les transcripts sous-estiment la sortie (réponses sans stop_reason, réflexion
invisible) ; la ligne `cost-state` du transcript principal (cumul de Claude Code par modèle)
fixe le total, et le manque est réparti sur les réponses incomplètes.
"""
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path

from lib import agentlog as al

CPT = al.CHARS_PER_TOKEN
BATCH_S = 120          # agents lancés à moins de 2 min d'écart : un même lot
COMPACT_DROP = 0.5     # le contexte principal chute de plus de moitié : compaction
FEW_TURNS = 10         # « fin de session » : moins de tours principaux après le retour,
END_SHARE = 0.15       # ou moins de 15 % des tours de la session
CONTEXT_LIMIT = 850_000  # en direct, contexte principal + travail des agents au-delà : compaction
                         # simulée (fenêtre de 1M ; 962k est le plus grand contexte observé)
TASK_ID_RE = re.compile(r"<task-id>([\w-]+)</task-id>")


def _dt(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00")) if s else None


def _ctx(u):
    return ((u.get("input_tokens") or 0) + (u.get("cache_read_input_tokens") or 0)
            + (u.get("cache_creation_input_tokens") or 0))


def _result_chars(c):
    body = c.get("content")
    if isinstance(body, str):
        return len(body)
    return sum(len(b.get("text") or "") for b in body or [] if isinstance(b, dict))


def _tool_results(lines):
    out = {}
    for d in lines:
        if d.get("type") != "user":
            continue
        content = (d.get("message") or {}).get("content")
        for c in content if isinstance(content, list) else []:
            if isinstance(c, dict) and c.get("type") == "tool_result":
                out[c.get("tool_use_id")] = _result_chars(c)
    return out


def _usage_counter(u):
    return Counter({"input_tokens": u.get("input_tokens") or 0, "output_tokens": u.get("output_tokens") or 0,
                    "cache_read": u.get("cache_read_input_tokens") or 0,
                    "cache_creation": u.get("cache_creation_input_tokens") or 0,
                    "cache_creation_1h": (u.get("cache_creation") or {}).get("ephemeral_1h_input_tokens") or 0})


# ---------------------------------------------------------------- lecture des transcripts

class Session:
    """Transcript principal : tours, appels Agent, retours, outils, compactions, cost-state."""

    def __init__(self, path):
        self.path = Path(path)
        self.sid = self.path.stem
        lines = al._read_jsonl(self.path)
        msgs = al._assistant_messages(lines, sidechain=False)
        self.turns = [{"ts": _dt(m["_ts"]), "ctx": _ctx(m["usage"]), "model": m.get("model"),
                       "usage": m["usage"], "incomplete": not m["stop_reason"]} for m in msgs]
        self.calls, self.tools = {}, []
        for i, m in enumerate(msgs):
            for c in m["content"]:
                if c.get("type") == "tool_use":
                    self.calls[c.get("id")] = i
                    self.tools.append((self.turns[i]["ts"], c))
        self.results = _tool_results(lines)
        self.returns, self.cost_state = {}, None
        for d in lines:
            if d.get("type") == "cost-state":
                self.cost_state = d
            elif d.get("type") in ("user", "attachment") and d.get("timestamp"):
                raw = json.dumps(d.get("message") or d.get("attachment") or {}, ensure_ascii=False)
                for aid in TASK_ID_RE.findall(raw):
                    self.returns.setdefault(aid, _dt(d["timestamp"]))
        self.compactions = [i for i in range(1, len(self.turns))
                            if self.turns[i - 1]["ctx"] and
                            self.turns[i]["ctx"] < COMPACT_DROP * self.turns[i - 1]["ctx"]]
        models = Counter(t["model"] for t in self.turns if t["model"])
        self.model = models.most_common(1)[0][0] if models else None
        self.usage = {}  # modèle → Counter, sortie calée par calibrate()
        self.incomplete = Counter()
        for t in self.turns:
            self.usage.setdefault(t["model"], Counter()).update(_usage_counter(t["usage"]))
            self.incomplete[t["model"]] += t["incomplete"]

    def turns_after(self, ts):
        """Tours principaux après `ts`, jusqu'à la compaction suivante (exclue)."""
        idx = [i for i, t in enumerate(self.turns) if t["ts"] and t["ts"] > ts]
        if not idx:
            return 0
        stop = next((c for c in self.compactions if c > idx[0]), len(self.turns))
        return sum(1 for i in idx if i < stop)

    def context_at(self, tool_use_id, ts):
        i = self.calls.get(tool_use_id)
        if i is None:
            before = [t for t in self.turns if t["ts"] and ts and t["ts"] <= ts]
            return before[-1]["ctx"] if before else 0
        return self.turns[i]["ctx"]


def subagent_detail(path):
    """Ce que le contrefactuel demande au transcript d'un sous-agent."""
    lines = al._read_jsonl(path)
    msgs = al._assistant_messages(lines)
    ctxs = [_ctx(m["usage"]) for m in msgs]
    results = _tool_results(lines)
    written, reads = set(), []
    for t in al._tool_uses(lines):
        inp = t.get("input") or {}
        if t.get("name") in ("Write", "Edit", "MultiEdit", "NotebookEdit") and inp.get("file_path"):
            written.add(inp["file_path"])
        elif t.get("name") == "Read" and inp.get("file_path"):
            reads.append((inp["file_path"], results.get(t.get("id"), 0)))
    stamps = [_dt(d["timestamp"]) for d in lines if d.get("timestamp")]
    return {"grown": max(0, ctxs[-1] - ctxs[0]) if ctxs else 0,
            "internal": sum(c - ctxs[0] for c in ctxs[1:]) if ctxs else 0,
            "written": written, "reads": reads,
            "start": min(stamps) if stamps else None, "end": max(stamps) if stamps else None}


def load_sessions(records):
    out = {}
    for r in records:
        sid, t = r.get("session_id"), r.get("transcript")
        if sid and t and sid not in out:
            p = al.session_transcript_of(t)
            out[sid] = Session(p) if p.is_file() else None
    return {k: v for k, v in out.items() if v}


# ---------------------------------------------------------------- calage sur le cost-state

def calibrate(records, sessions):
    """Copie des enregistrements, sortie calée sur le cost-state de chaque session.

    Calage seulement si les lectures de cache du cost-state et des transcripts concordent
    (±2 %) : sinon le cost-state ou le journal est incomplet pour cette session.
    Met aussi à jour la sortie de l'agent principal (Session.usage).
    """
    recs = [dict(r) for r in records]
    for sid, s in sessions.items():
        mu = (s.cost_state or {}).get("modelUsage") or {}
        mine = [r for r in recs if r.get("session_id") == sid]
        for model, u in mu.items():
            subs = [r for r in mine if r.get("model_served") == model]
            main_u = s.usage.get(model, Counter())
            reads = main_u["cache_read"] + sum(r.get("cache_read") or 0 for r in subs)
            target_reads = u.get("cacheReadInputTokens") or 0
            if not target_reads or abs(reads - target_reads) > 0.02 * target_reads:
                continue
            have = main_u["output_tokens"] + sum(r.get("output_tokens") or 0 for r in subs)
            missing = (u.get("outputTokens") or 0) - have
            w_main = s.incomplete[model]
            weights = [r.get("incomplete_turns", r.get("turns") or 0) for r in subs]
            total_w = w_main + sum(weights)
            if missing <= 0 or not total_w:
                continue
            for r, w in zip(subs, weights):
                add = int(missing * w / total_w)
                r["output_tokens"] = (r.get("output_tokens") or 0) + add
                r["total_tokens"] = (r.get("total_tokens") or 0) + add
                r["output_source"] = "calé"
            if model in s.usage:
                s.usage[model]["output_tokens"] += int(missing * w_main / total_w)
    return recs


def main_cost(session, prices):
    return sum(al.cost({**u, "model_served": m}, prices) or 0 for m, u in session.usage.items())


# ---------------------------------------------------------------- contrefactuel

def _prices(model, prices):
    p = al._price_for(model, prices)
    if p is None:
        return None
    return {"out": p["output"] / 1e6, "read": p["cache_read"] / 1e6,
            "write": p["input"] * prices.get("cache_write_5m", 1.25) / 1e6}


def _write_price(session, prices):
    """Prix d'écriture en cache de l'agent principal, au mélange 5 min / 1 h qu'il pratique."""
    p = al._price_for(session.model, prices)
    u = session.usage.get(session.model, Counter())
    c1h, c = u["cache_creation_1h"], u["cache_creation"]
    w = ((c - c1h) * prices.get("cache_write_5m", 1.25) + c1h * prices.get("cache_write_1h", 2.0)) / c if c \
        else prices.get("cache_write_5m", 1.25)
    return p["input"] * w / 1e6


def _touches(tool, written):
    inp = tool.get("input") or {}
    name = tool.get("name")
    if name == "Read":
        return inp.get("file_path") in written
    if name == "Grep":
        return inp.get("path") in written
    if name == "Bash":
        cmd = str(inp.get("command", ""))
        return any(w in cmd or (len(Path(w).name) >= 8 and Path(w).name in cmd) for w in written)
    return False


def _direct_timeline(session, items):
    """Mode direct simulé : {agent_id: (A', travail accumulé au lancement)}.

    `items` : (agent_id, lancement, retour, G). Le G d'un agent entre dans le contexte virtuel
    à son retour et y est relu à chaque tour principal, jusqu'à la compaction réelle suivante
    ou jusqu'à ce que contexte réel + travail accumulé dépasse CONTEXT_LIMIT (compaction
    simulée) : le travail accumulé repart alors de zéro, et ces agents n'y reviennent pas.
    """
    after, at_launch, active, done = {a: 0 for a, *_ in items}, {}, {}, set()
    real = set(session.compactions)
    for i, t in enumerate(session.turns):
        ts = t["ts"]
        if ts is None:
            continue
        for a, start, ret, g in items:
            if a not in at_launch and start and start <= ts:
                at_launch[a] = sum(active.values())
            if a not in active and a not in done and ret and ret < ts:
                active[a] = g
        if i in real or t["ctx"] + sum(active.values()) > CONTEXT_LIMIT:
            done |= set(active)
            active = {}
            continue
        for a in active:
            after[a] += 1
    return {a: (after[a], at_launch.get(a, 0)) for a, *_ in items}


def savings(records, sessions, prices=None):
    """Une ligne par agent : coût délégué, direct estimé, vérification, économie, causes."""
    prices = al.load_prices() if prices is None else prices
    details = {r["agent_id"]: subagent_detail(r["transcript"]) for r in records
               if r.get("session_id") in sessions and r.get("transcript") and Path(r["transcript"]).is_file()}
    dup = _duplicate_reads(records, details)
    timelines = {}
    for sid, s in sessions.items():
        items = [(r["agent_id"], details[r["agent_id"]]["start"],
                  s.returns.get(r["agent_id"]) or details[r["agent_id"]]["end"], details[r["agent_id"]]["grown"])
                 for r in records if r.get("session_id") == sid and r["agent_id"] in details]
        timelines[sid] = _direct_timeline(s, items)
    rows = []
    for r in records:
        s, d = sessions.get(r.get("session_id")), details.get(r["agent_id"])
        pm = _prices(s.model, prices) if s else None
        sub_cost = al.cost(r, prices)
        if not (s and d and pm and sub_cost is not None):
            continue
        pm["write"] = _write_price(s, prices)
        ret = s.returns.get(r["agent_id"]) or d["end"]
        after = s.turns_after(ret) if ret else 0
        c0 = s.context_at(r.get("tool_use_id"), d["start"])
        res, prompt = (r.get("result_chars") or 0) / CPT, (r.get("prompt_chars") or 0) / CPT
        turns, out = r.get("turns") or 0, r.get("output_tokens") or 0
        delegated = sub_cost + prompt * pm["out"] + res * (pm["write"] + after * pm["read"])
        after_d, acc = timelines[r["session_id"]].get(r["agent_id"], (after, 0))
        direct = (out * pm["out"] + d["grown"] * pm["write"]
                  + (turns * (c0 + acc) + d["internal"]) * pm["read"] + d["grown"] * after_d * pm["read"])
        vtok = sum(s.results.get(t.get("id"), 0) for ts, t in s.tools
                   if ret and ts and ts > ret and _touches(t, d["written"])) / CPT
        verify = vtok * (pm["write"] + after * pm["read"])
        saved = -(delegated + verify) if r.get("verified") == "refait" else direct - delegated - verify
        ps = _prices(r.get("model_served"), prices)
        dup_tok = dup.get(r["agent_id"], 0)
        row = {"agent_id": r["agent_id"], "session_id": r["session_id"], "task_class": r.get("task_class"),
               "model_served": r.get("model_served"), "base": r.get("base"),
               "description": r.get("description"), "main_model": s.model,
               "delegated": delegated, "direct": direct, "verify": verify, "saved": saved,
               "after": after, "after_direct": after_d, "c0": c0, "acc": acc,
               "session_turns": len(s.turns), "result_tokens": res, "dup_tokens": dup_tok,
               "dup_cost": dup_tok * (ps["write"] + turns / 2 * ps["read"]) if ps else 0,
               "startup": (r.get("first_turn_tokens") or 0) / r["total_tokens"] if r.get("total_tokens") else 0,
               "verified": r.get("verified"), "grown": d["grown"]}
        row["causes"] = causes(row, pm)
        rows.append(row)
    return rows


def _duplicate_reads(records, details):
    """Tokens relus par un agent alors qu'un autre agent du même lot avait déjà lu le fichier."""
    out = Counter()
    by_session = {}
    for r in records:
        if r["agent_id"] in details and details[r["agent_id"]]["start"]:
            by_session.setdefault(r["session_id"], []).append(r["agent_id"])
    for aids in by_session.values():
        aids.sort(key=lambda a: details[a]["start"])
        for i, a in enumerate(aids):
            earlier = [b for b in aids[:i]
                       if (details[a]["start"] - details[b]["start"]).total_seconds() < BATCH_S]
            seen = {f for b in earlier for f, _ in details[b]["reads"]}
            out[a] = sum(chars for f, chars in details[a]["reads"] if f in seen) / CPT
    return out


def causes(row, pm):
    """Pourquoi la délégation coûte plus que prévu (étiquettes du rapport)."""
    tags = []
    if row["verified"] == "refait":
        tags.append("refait")
    if row["model_served"] == row["main_model"]:
        tags.append("même modèle")
    if row["after"] < max(FEW_TURNS, END_SHARE * row["session_turns"]):
        tags.append("fin de session")
    if row["result_tokens"] * row["after"] * pm["read"] > 0.25 * row["delegated"]:
        tags.append("résultat long")
    if row["startup"] > al.STARTUP_WARN:
        tags.append("démarrage")
    if row["direct"] and row["verify"] > 0.3 * row["direct"]:
        tags.append("vérification lourde")
    if row["grown"] and row["dup_tokens"] > 0.2 * row["grown"]:
        tags.append("lectures dupliquées")
    return tags


# ---------------------------------------------------------------- rapports

def _group_rows(rows, by):
    keys = al.GROUPS[by]
    groups = {}
    for r in rows:
        groups.setdefault(" · ".join(al._short_model(r.get(k)) if k == "model_served" else str(r.get(k) or "?")
                                     for k in keys), []).append(r)
    return sorted(groups.items(), key=lambda kv: -sum(x["delegated"] for x in kv[1]))


def report_savings(rows, by="task-model", worst=10):
    if not rows:
        return "Économie : aucun agent dont la session soit lisible."
    out = [f"## Économie de la délégation (estimée, {len(rows)} appels)", "",
           "| groupe | appels | délégué | direct estimé | vérification | économie | % du direct | perdants |",
           "|---|--:|--:|--:|--:|--:|--:|--:|"]
    for g, rs in _group_rows(rows, by):
        d, x, v, s = (sum(r[k] for r in rs) for k in ("delegated", "direct", "verify", "saved"))
        lost = sum(1 for r in rs if r["saved"] < 0)
        out.append(f"| {g} | {len(rs)} | {al._usd(d)} | {al._usd(x)} | {al._usd(v)} | {al._usd(s)} | "
                   f"{al._pct(s / x if x else None)} | {lost or ''} |")
    d, x, s = (sum(r[k] for r in rows) for k in ("delegated", "direct", "saved"))
    dup = sum(r["dup_cost"] for r in rows)
    out += ["", f"Total : délégué {al._usd(d)}, direct estimé {al._usd(x)}, économie {al._usd(s)} "
                f"({al._pct(s / x if x else None)}). Lectures dupliquées entre agents d'un même lot : "
                f"{al._usd(dup)} (déjà dans le délégué).",
            "Direct estimé : mêmes tours au tarif de l'agent principal, sans démarrage, avec la relecture "
            "du travail à chaque tour suivant jusqu'à la compaction. C'est une estimation : la valider "
            "par une expérience appariée (docs/AMELIORATIONS.md, I-6)."]
    bad = sorted(rows, key=lambda r: r["saved"] / r["direct"] if r["direct"] else 0)[:worst]
    if bad:
        out += ["", f"## Cas défavorables ({len(bad)} plus faibles économies relatives)", "",
                "| agent | classe · modèle | description | délégué | direct | économie | tours après (délégué / direct) | causes |",
                "|---|---|---|--:|--:|--:|--:|---|"]
        for r in bad:
            out.append(f"| {r['agent_id'][:10]} | {r['task_class']} · {al._short_model(r['model_served'])} | "
                       f"{(r['description'] or '')[:40]} | {al._usd(r['delegated'])} | {al._usd(r['direct'])} | "
                       f"{al._usd(r['saved'])} | {r['after']} / {r['after_direct']} | {', '.join(r['causes'])} |")
    return "\n".join(out)


def report_calibration(records, sessions, prices=None):
    """Σ calculé (principal + sous-agents, calés) contre le coût que Claude Code a compté."""
    prices = al.load_prices() if prices is None else prices
    out = ["## Calage sur le coût compté par Claude Code (cost-state)", "",
           "| session | cost-state | calculé | écart | agent principal | sous-agents |", "|---|--:|--:|--:|--:|--:|"]
    for sid, s in sorted(sessions.items()):
        cs = (s.cost_state or {}).get("totalCostUSD")
        main = main_cost(s, prices)
        sub = sum(al.cost(r, prices) or 0 for r in records if r.get("session_id") == sid)
        gap = None if not cs else (main + sub - cs) / cs
        out.append(f"| {sid[:8]} | {al._usd(cs)} | {al._usd(main + sub)} | {al._pct(gap)} | "
                   f"{al._usd(main)} | {al._usd(sub)} |")
    return "\n".join(out)


def report_session(sid_prefix, records, prices=None):
    prices = al.load_prices() if prices is None else prices
    mine = [r for r in records if (r.get("session_id") or "").startswith(sid_prefix)]
    if not mine:
        return f"aucun sous-agent journalisé pour la session {sid_prefix!r}"
    sids = {r["session_id"] for r in mine}
    if len(sids) > 1:
        return f"{sid_prefix!r} désigne {len(sids)} sessions : préciser"
    sessions = load_sessions(mine)
    recs = calibrate(mine, sessions)
    rows = savings(recs, sessions, prices)
    (sid, s), = sessions.items()
    main, sub = main_cost(s, prices), sum(al.cost(r, prices) or 0 for r in recs)
    cs = (s.cost_state or {}).get("totalCostUSD")
    out = [f"# Session {sid}", "",
           f"Coût compté par Claude Code : {al._usd(cs)} ; calculé : {al._usd(main + sub)} "
           f"(agent principal {al._usd(main)}, {al._short_model(s.model)}, {len(s.turns)} tours ; "
           f"{len(recs)} sous-agents {al._usd(sub)}).",
           f"Économie estimée de la délégation : {al._usd(sum(r['saved'] for r in rows))} "
           f"(direct estimé {al._usd(sum(r['direct'] for r in rows))}).", "",
           "| agent | classe · modèle | description | coût | délégué | direct | économie | tours après (délégué / direct) | causes |",
           "|---|---|---|--:|--:|--:|--:|--:|---|"]
    by_id = {r["agent_id"]: r for r in recs}
    for r in sorted(rows, key=lambda r: by_id[r["agent_id"]].get("ts") or ""):
        out.append(f"| {r['agent_id'][:10]} | {r['task_class']} · {al._short_model(r['model_served'])} | "
                   f"{(r['description'] or '')[:40]} | {al._usd(al.cost(by_id[r['agent_id']], prices))} | "
                   f"{al._usd(r['delegated'])} | {al._usd(r['direct'])} | {al._usd(r['saved'])} | "
                   f"{r['after']} / {r['after_direct']} | {', '.join(r['causes'])} |")
    return "\n".join(out)
