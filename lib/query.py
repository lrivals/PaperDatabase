"""Requêtes structurées sans LLM (niveau N0 de docs/RAG.md) : benchmarks.csv et metadata.json.

Bibliothèque standard seulement (plus lib/schema) : pas de numpy ni de sklearn, pour que
`bin/pdb bench` et `bin/pdb paper` restent instantanés. Sorties compactes (TSV par défaut),
chaque ligne de benchmark garde sa source (source_section, confidence, power_scope).
"""
import csv
import json
from pathlib import Path

from slugify import slugify

from lib import schema

NR = schema.NR
ALWAYS = ("paper_id", "source_section", "confidence")
CARD_FIELDS = ("id", "short", "title", "authors", "year", "venue", "type", "doi", "url",
               "axes", "tags", "fiche", "benchmarks", "warnings")


# ------------------------------------------------------------------ chargement

def load_benchmarks(root):
    """(en-tête, lignes) de benchmarks.csv ; en-tête lu dans le fichier, pas codé en dur."""
    path = Path(root) / "benchmarks.csv"
    if not path.exists():
        return [], []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        return list(reader.fieldnames or []), list(reader)


def load_papers(root):
    return [json.loads(p.read_text())
            for p in sorted((Path(root) / "papers").glob("*/metadata.json"))]


# ------------------------------------------------------------ identifiants courts

def _short_candidate(meta):
    """arxiv_id, sinon le préfixe « année-auteur » du paper_id (lib/ids.make_paper_id), qui
    garde les noms composés entiers (2025-el-zeinaty) ; à défaut, deux premiers segments."""
    if meta.get("arxiv_id"):
        return meta["arxiv_id"]
    authors = meta.get("authors") or []
    family = authors[0].get("family") if authors else None
    if family and meta.get("year"):
        prefix = f"{meta['year']}-{slugify(family)}"
        if meta["id"].startswith(prefix + "-") or meta["id"] == prefix:
            return prefix
    return "-".join(meta["id"].split("-")[:2])


def short_ids(metas):
    """paper_id → identifiant court : arxiv_id, sinon « année-auteur » ; complet si collision."""
    cand = {m["id"]: _short_candidate(m) for m in metas}
    counts = {}
    for c in cand.values():
        counts[c] = counts.get(c, 0) + 1
    return {pid: (c if counts[c] == 1 else pid) for pid, c in cand.items()}


def resolve(query, metas):
    """Papiers désignés par `query` : id complet, id court, sinon sous-chaîne d'id ou de titre."""
    q = query.strip().lower()
    short = short_ids(metas)
    exact = [m for m in metas if q in (m["id"].lower(), short[m["id"]].lower())]
    if exact:
        return exact
    return [m for m in metas if q in m["id"].lower() or q in (m.get("title") or "").lower()]


# ------------------------------------------------------------------- filtres

def to_float(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def filter_rows(rows, contains=None, minimum=None, maximum=None, has=()):
    """contains : {col: sous-chaîne} ; minimum / maximum : {col: nombre} (n/r exclu) ;
    has : colonnes qui ne doivent pas valoir n/r."""
    out = []
    for r in rows:
        if any(s.lower() not in (r.get(c) or "").lower() for c, s in (contains or {}).items()):
            continue
        if any(r.get(c, NR).strip() in (NR, "") for c in has):
            continue
        ok = True
        for bounds, better in ((minimum, lambda v, x: v >= x), (maximum, lambda v, x: v <= x)):
            for c, x in (bounds or {}).items():
                v = to_float(r.get(c))
                if v is None or not better(v, x):
                    ok = False
        if ok:
            out.append(r)
    return out


def sort_rows(rows, col, desc=False):
    """Tri numérique si toutes les valeurs renseignées sont des nombres ; n/r en dernier."""
    known = [r for r in rows if (r.get(col) or NR) != NR]
    unknown = [r for r in rows if (r.get(col) or NR) == NR]
    if all(to_float(r[col]) is not None for r in known):
        key = lambda r: to_float(r[col])  # noqa: E731
    else:
        key = lambda r: r[col].lower()  # noqa: E731
    return sorted(known, key=key, reverse=desc) + unknown


def select_columns(cols, header):
    """Colonnes demandées (toutes si vide) + celles qui portent la source, dans l'ordre du CSV."""
    if not cols:
        return list(header)
    unknown = [c for c in cols if c not in header]
    if unknown:
        raise ValueError(f"colonne(s) inconnue(s) : {', '.join(unknown)}. "
                         f"Valides : {', '.join(header)}")
    wanted = set(cols) | {c for c in ALWAYS if c in header}
    if "power_w" in wanted and "power_scope" in header:
        wanted.add("power_scope")
    return [c for c in header if c in wanted]


def count_rows(rows, cols, short):
    """Nombre de lignes par combinaison de valeurs de `cols` (paper_id en id court)."""
    counts = {}
    for r in rows:
        key = tuple(short.get(r[c], r[c]) if c == "paper_id" else (r.get(c) or "") for c in cols)
        counts[key] = counts.get(key, 0) + 1
    lines = ["n\t" + "\t".join("paper" if c == "paper_id" else c for c in cols)]
    lines += [f"{n}\t" + "\t".join(k) for k, n in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))]
    return "\n".join(lines)


# -------------------------------------------------------------------- rendu

def _hidden_differences(rows, cols):
    """Colonnes non affichées qui distinguent des lignes identiques à l'affichage."""
    groups = {}
    for r in rows:
        groups.setdefault(tuple(r.get(c) for c in cols), []).append(r)
    diff = set()
    for group in groups.values():
        for r in group[1:]:
            diff |= {c for c in r if c not in cols and r[c] != group[0].get(c)}
    return sorted(diff)


def render(rows, cols, short, fmt="tsv", max_chars=None):
    """rows filtrées → texte. short : paper_id → id court (légende en pied de sortie).

    max_chars : budget de la sortie entière, pied compris ; on coupe par lignes entières
    et la légende ne porte que sur les lignes gardées.
    """
    if fmt == "json":
        out = [{**{c: r.get(c) for c in cols}, "short": short.get(r["paper_id"], r["paper_id"])}
               for r in rows]
        return json.dumps(out, ensure_ascii=False, indent=1)

    def cell(r, c):
        v = r.get(c) or ""
        if c == "paper_id":
            v = short.get(v, v)
        v = v.replace("\t", " ").replace("\n", " ")
        return v.replace("|", "/") if fmt == "md" else v

    def line(vals):
        return "| " + " | ".join(vals) + " |" if fmt == "md" else "\t".join(vals)

    head = ["paper" if c == "paper_id" else c for c in cols]
    lines = [line(head)] + (["|" + "---|" * len(head)] if fmt == "md" else [])

    def footer(kept, omitted):
        out = [f"# tronqué : {omitted} lignes omises"] if omitted else []
        if any(r.get("confidence") == "low" for r in kept):
            out.append("# ! = confidence low")
        hidden = _hidden_differences(kept, cols)
        if hidden:
            out.append("# lignes identiques à l'affichage : elles diffèrent par "
                       + ", ".join(hidden))
        used = sorted({r["paper_id"] for r in kept} if "paper_id" in cols else ())
        used = [p for p in used if short.get(p, p) != p]
        if used:
            out.append("# ids: " + " ".join(f"{short[p]}={p}" for p in used))
        return out

    kept = []
    for i, r in enumerate(rows):
        vals = [cell(r, c) for c in cols]
        if r.get("confidence") == "low":
            vals[0] = "!" + vals[0]
        candidate = lines + [line(vals)]
        if max_chars and kept:
            size = len("\n".join(candidate + footer(kept + [r], len(rows) - i - 1)))
            if size > max_chars:
                return "\n".join(lines + footer(kept, len(rows) - i))
        lines, kept = candidate, kept + [r]
    return "\n".join(lines + footer(kept, 0))


def paper_card(meta, n_bench, short_id, fields=None):
    """Fiche d'identité d'un papier, une ligne `clé<TAB>valeur` par champ."""
    typ = meta.get("type")
    values = {
        "id": meta["id"],
        "short": short_id,
        "title": meta.get("title") or NR,
        "authors": schema.format_authors(meta.get("authors") or []),
        "year": meta.get("year") or NR,
        "venue": meta.get("venue") or NR,
        "type": f"{typ} (non relu par les pairs)" if typ == "preprint" else (typ or NR),
        "doi": meta.get("doi") or NR,
        "url": meta.get("url") or NR,
        "axes": ", ".join(meta.get("axes") or []) or NR,
        "tags": ", ".join(meta.get("tags") or []) or NR,
        "fiche": (meta.get("status") or {}).get("fiche") or NR,
        "benchmarks": n_bench,
        "warnings": len((meta.get("extraction") or {}).get("warnings") or []),
    }
    fields = fields or CARD_FIELDS
    unknown = [f for f in fields if f not in values]
    if unknown:
        raise ValueError(f"champ(s) inconnu(s) : {', '.join(unknown)}. "
                         f"Valides : {', '.join(CARD_FIELDS)}")
    return "\n".join(f"{f}\t{values[f]}" for f in fields)
