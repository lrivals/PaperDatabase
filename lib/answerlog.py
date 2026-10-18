"""Journal des réponses (lot H, provenance) : quand `"log_answers": true` dans base.json,
/paper-ask et /paper-research ajoutent chaque réponse à .cache/answers/<AAAA-MM>.jsonl.

Une ligne reprend l'enregistrement du lot A (id, q, verdict, requirements, claims : une
réponse journalisée peut devenir un cas de test, docs/EVAL.md §10) et y ajoute ce qui permet
de la rejouer : date, commit du code, empreinte du corpus (lib/snapshot.py), et l'empreinte
sha1 de chaque passage cité (pdb verify --sha1 signale ensuite un passage modifié).
"""
import datetime
import json
import subprocess
from pathlib import Path

from lib import evaluation, rag, snapshot


def enabled(cfg):
    return bool((cfg or {}).get("log_answers"))


def _commit(code):
    out = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=code, capture_output=True, text=True)
    return out.stdout.strip() or None


def passages(root, record):
    """{chunk_id cité: sha1 du passage (8 car.)}, ou None si le passage est introuvable."""
    from lib import query
    chunks = rag.load_chunks(root)
    by_id = {c["chunk_id"]: c for c in chunks}
    short = query.short_ids(query.load_papers(root))
    out = {}
    for c in record.get("claims") or ():
        for cit in c.get("citations") or ():
            cid = cit.get("id")
            if cid and cid not in out:
                full = rag.resolve_chunk_id(cid, by_id, short)
                out[cid] = rag.sha1(by_id[full]["text"])[:8] if full else None
    return out


def entry(root, code, record, base_name, now=None):
    problems = evaluation.validate_answer_record(record)
    if problems:
        raise ValueError("; ".join(problems))
    now = now or datetime.datetime.now()
    return {**record, "date": now.isoformat(timespec="seconds"), "base": base_name,
            "commit": _commit(code), "snapshot": snapshot.fingerprint(root),
            "passages": passages(root, record)}


def append(root, line, now=None):
    now = now or datetime.datetime.now()
    path = Path(root) / ".cache" / "answers" / f"{now:%Y-%m}.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a") as f:
        f.write(json.dumps(line, ensure_ascii=False) + "\n")
    return path
