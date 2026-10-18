"""Preuves atomiques (lot C, DATA_MODEL §12) : papers/<id>/claims.jsonl.

Chaque claim renvoie à un passage (`source_chunk`) et en cite un extrait exact (`excerpt`),
contrôlé par rag.verify contre ce passage. La claim aide à retrouver la preuve ; la citation
finale reste le passage. Ce module ne modifie jamais claims.jsonl (produit par /paper-extract).
"""
import json
import math
import re
from pathlib import Path
from types import SimpleNamespace

from lib import query, schema

FILENAME = "claims.jsonl"
ERROR, NOTE = "erreur", "note"
# Mots qui mêlent lettres et chiffres (ZC706, 3x512, INT8) : noms, pas des valeurs.
_ALNUM = re.compile(r"\b(?=\w*[^\W\d_])(?=\w*\d)\w+\b")


def missing_numbers(text, section_texts):
    """Nombres de `text` (claim en français : « 12,3 » → 12.3 ; noms comme ZC706 ou INT8
    ignorés) qu'aucun passage de la section ne contient, à la même valeur."""
    from lib import rag
    ref = [query.to_float(t) for x in section_texts for t in rag.number_tokens(x)]
    ref = [v for v in ref if v is not None]
    out = []
    for t in rag.number_tokens(re.sub(r"(\d),(\d)", r"\1.\2", _ALNUM.sub(" ", text))):
        v = query.to_float(t)
        if v is not None and not any(math.isclose(v, x, rel_tol=1e-9, abs_tol=1e-12) for x in ref):
            out.append(t)
    return out


def paths(root, paper_ids=None):
    """claims.jsonl présents dans la base, triés ; restreints à paper_ids si donné."""
    out = sorted((Path(root) / "papers").glob(f"*/{FILENAME}"))
    return [p for p in out if paper_ids is None or p.parent.name in paper_ids]


def load(path):
    """[(n° de ligne, dict ou None, erreur JSON ou None)] ; lignes vides ignorées."""
    out = []
    for i, line in enumerate(Path(path).read_text().splitlines(), start=1):
        if not line.strip():
            continue
        try:
            out.append((i, json.loads(line), None))
        except json.JSONDecodeError as e:
            out.append((i, None, str(e)))
    return out


def linked(root, chunk_ids, short_chunk_id=lambda c: c):
    """Claims dont le source_chunk est l'un des passages chunk_ids (lot C : /paper-ask lit
    les preuves déjà vérifiées des passages qu'il retient). Renvoie {chunk_id: [claim]} ;
    les ids sont comparés sous leur forme courte (short_chunk_id) comme sous leur forme brute."""
    want = {}
    for c in chunk_ids:
        want[c] = c
        want[short_chunk_id(c)] = c
    papers = {c.split("#")[0] for c in chunk_ids}
    out = {}
    for path in paths(root, papers):
        for _, row, err in load(path):
            if err or not row:
                continue
            src = row.get("source_chunk") or ""
            key = want.get(src) or want.get(short_chunk_id(src))
            if key:
                out.setdefault(key, []).append(row)
    return out


def check(root, paper_ids=None):
    """Contrôle les claims.jsonl de la base (ou de paper_ids). Renvoie (résultats, bilan).

    résultats : [{paper_id, line, claim_id, level: erreur|note, msg}] ; bilan : {claims,
    papers, verified}. Erreurs : schéma, claim_id en double, passage introuvable ou d'un
    autre papier, excerpt ABSENT ou NOMBRES, excerpt trouvé dans un autre passage que
    source_chunk. Notes : passage modifié depuis l'extraction (chunk_sha1, statut MODIFIÉ) ;
    nombres du text absents de la section du passage (conversion, ou valeur tirée d'ailleurs)."""
    files = paths(root, paper_ids)
    summary = {"claims": 0, "papers": len(files), "verified": 0}
    if not files:
        return [], summary
    from lib import rag  # import paresseux : sans claims.jsonl, rien à charger
    chunks = rag.load_chunks(root)
    index = SimpleNamespace(chunks=chunks, by_id={c["chunk_id"]: i for i, c in enumerate(chunks)})
    by_section = {}
    for c in chunks:
        by_section.setdefault(c["section_id"], []).append(c["text"])
    short = query.short_ids(query.load_papers(root))
    n_rows = {}
    for r in query.load_benchmarks(root)[1]:
        n_rows[r.get("paper_id")] = n_rows.get(r.get("paper_id"), 0) + 1

    def sid(cid):
        pid, _, rest = cid.partition("#")
        return f"{short.get(pid, pid)}#{rest}"

    out = []
    for path in files:
        pid = path.parent.name
        seen = {}
        for line, row, err in load(path):
            res = {"paper_id": pid, "line": line,
                   "claim_id": row.get("claim_id") if isinstance(row, dict) else None}

            def add(level, msg):
                out.append({**res, "level": level, "msg": msg})

            if err:
                add(ERROR, f"ligne illisible ({err})")
                continue
            summary["claims"] += 1
            errs = schema.validate_claim_row(row, pid, n_rows.get(pid, 0))
            for e in errs:
                add(ERROR, e)
            cid = res["claim_id"]
            if isinstance(cid, str):
                if cid in seen:
                    add(ERROR, f"claim_id en double (déjà ligne {seen[cid]})")
                seen.setdefault(cid, line)
            if errs:
                continue
            full = rag.resolve_chunk_id(row["source_chunk"], index.by_id, short)
            if full is None or chunks[index.by_id[full]]["paper_id"] != pid:
                add(ERROR, f"source_chunk {row['source_chunk']} introuvable dans ce papier")
                continue
            # l'excerpt d'abord : un passage modifié (chunk_sha1) n'est qu'une note s'il le
            # contient encore, et ne masque jamais une erreur
            status, ratio, where = rag.verify(index, full, row["excerpt"])
            sha = row.get("chunk_sha1")
            changed = (" ; passage modifié depuis l'extraction (chunk_sha1)"
                       if sha and not chunks[index.by_id[full]]["sha1"].startswith(sha) else "")
            if status in ("OK", "APPROX") and where != full:
                add(ERROR, f"excerpt trouvé dans {sid(where)}, pas dans {sid(full)} : "
                           "corriger source_chunk (et chunk_sha1)")
            elif status in ("OK", "APPROX"):
                summary["verified"] += 1
                if changed:
                    add(NOTE, f"passage {sid(full)} modifié depuis l'extraction (chunk_sha1), "
                              "excerpt toujours présent : relancer /paper-extract")
                miss = missing_numbers(row["text"], by_section[chunks[index.by_id[full]]["section_id"]])
                if miss:
                    add(NOTE, f"nombre(s) du text absent(s) de la section de {sid(full)} : "
                              f"{', '.join(miss)} (conversion ? autre passage ?)")
            else:
                add(ERROR, f"excerpt {status} ({ratio:.2f}) dans {sid(full)}{changed}")
    return out, summary


def render(results, summary):
    """Sortie de pdb claims --check et des lignes de reindex."""
    lines = [f"{r['level']}\t{r['paper_id']}\tligne {r['line']}\t"
             f"{(r['claim_id'] or '-').rpartition('!')[2]}\t{r['msg']}"
             for r in results]
    lines.append(f"# {summary['claims']} claim(s) dans {summary['papers']} papier(s), "
                 f"{summary['verified']} excerpt(s) vérifié(s)")
    return "\n".join(lines)
