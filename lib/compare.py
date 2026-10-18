"""pdb compare : comparaison de configurations sur deux axes numériques de benchmarks.csv
(docs/AMELIORATIONS.md, lot J-1 à J-3). Déterministe, sans modèle de langage.

L'outil ne classe pas les meilleurs chiffres : il montre quelles lignes sont comparées,
pourquoi elles le sont, et quelles différences empêchent une comparaison fiable. Chaque
ligne filtrée est soit retenue dans un groupe, soit exclue avec un motif.
"""
import json

from lib import query, schema

NR = schema.NR
ACCURACY = "accuracy_value"
POWER = "power_w"
# conditions qui ne séparent pas les groupes mais rendent la comparaison réservée
VARYING = query.VARYING
LEVELS = ("forte", "réservée", "faible")
ROW_FIELDS = ("model", "platform", "source_section", "confidence", "chunk_id")


def key_columns(x, y, metric=None):
    """Colonnes de la clé de groupe : task, dataset, dataset_split ; la métrique dès qu'un axe
    ou un filtre porte sur la précision ; power_scope dès qu'un axe est une puissance."""
    cols = ["task", "dataset", "dataset_split"]
    if ACCURACY in (x, y) or metric:
        cols.append("metric")
    if POWER in (x, y):
        cols.append("power_scope")
    return cols


def _value(r, c):
    return query._metric(r) if c == "metric" else (r.get(c) or NR).strip() or NR


def _is_nr(v):
    return (v or NR).strip() in (NR, "")


def select(rows, task=None, dataset=None, metric=None, platform=None, papers=None):
    """Filtres de la commande : sous-chaînes insensibles à la casse ; metric porte sur
    metric_def ou accuracy_metric ; papers : ensemble de paper_id."""
    contains = {c: v for c, v in (("task", task), ("dataset", dataset), ("platform", platform)) if v}
    out = query.filter_rows(rows, contains)
    if metric:
        m = metric.lower()
        out = [r for r in out if m in (r.get("metric_def") or "").lower()
               or m in (r.get("accuracy_metric") or "").lower()]
    if papers:
        out = [r for r in out if r["paper_id"] in papers]
    return out


def _confidence(display, conditions):
    """forte : clé complète, aucune condition ne varie ; réservée : une condition varie ;
    faible : une condition de la clé ou d'une ligne est inconnue, ou la métrique n'est pas
    vérifiée (~)."""
    if any(_is_nr(v) for c, v in display.items() if c != "metric") \
            or display.get("metric", "").startswith("~") \
            or any(c["missing"] for c in conditions):
        return "faible"
    if any(len(c["values"]) > 1 for c in conditions):
        return "réservée"
    return "forte"


def _conditions(rs, header):
    """Conditions de VARYING présentes dans l'en-tête : valeurs distinctes et lignes en n/r."""
    out = []
    for c in VARYING:
        if c not in header:
            continue
        values = []
        for r in rs:
            v = (r.get(c) or NR).strip()
            if not _is_nr(v) and query._norm(v) not in {query._norm(x) for x in values}:
                values.append(v)
        missing = sum(1 for r in rs if _is_nr(r.get(c)))
        if len(values) > 1 or missing:
            out.append({"column": c, "values": values, "missing": missing})
    return out


def _exclusion_reason(display, multi, cols):
    """Motif d'exclusion d'une ligne d'un groupe d'un seul papier : la colonne de la clé qui
    la sépare d'un groupe de plusieurs papiers de même tâche et même jeu, sinon « seul papier
    du groupe »."""
    same = [g for g in multi if query._norm(g["key"]["task"]) == query._norm(display["task"])
            and query._norm(g["key"]["dataset"]) == query._norm(display["dataset"])]
    labels = {"metric": "métrique différente", "power_scope": "power_scope incompatible",
              "dataset_split": "dataset_split différent", "platform_class": "platform_class différente"}
    for g in same:
        for c in cols:
            if c in labels and query._norm(g["key"][c]) != query._norm(display[c]):
                return labels[c]
    return "seul papier du groupe"


def compare(header, rows, x, y, metric=None, min_papers=2):
    """Groupes comparables sur les axes x et y, et lignes exclues avec leur motif.

    Aucune valeur n'est devinée : un n/r sur un axe exclut la ligne ; un n/r dans la clé la
    laisse dans son groupe, dont la confiance devient « faible »."""
    for c in (x, y):
        if c not in schema.NUMERIC_COLUMNS:
            raise ValueError(f"axe {c!r} non numérique ; axes possibles : {', '.join(schema.NUMERIC_COLUMNS)}")
    cols = key_columns(x, y, metric)
    if "platform_class" in header:  # une mesure serveur ne se compare pas à une mesure embarquée
        cols.append("platform_class")
    excluded, groups = [], {}
    for r in rows:
        bad = [f"{ax} ({c}) en n/r" for ax, c in (("x", x), ("y", y)) if query.to_float(r.get(c)) is None]
        if bad:
            excluded.append((r, " ; ".join(bad)))
            continue
        display = {c: _value(r, c) for c in cols}
        g = groups.setdefault(tuple(query._norm(display[c]) for c in cols), {"key": display, "rows": []})
        g["rows"].append(r)
    kept, multi = [], []
    for g in groups.values():
        g["papers"] = sorted({r["paper_id"] for r in g["rows"]})
        (multi if len(g["papers"]) >= min_papers else kept).append(g)
    for g in kept:  # groupes d'un seul papier : exclus, avec le motif le plus précis
        reason = _exclusion_reason(g["key"], multi, cols)
        excluded.extend((r, reason) for r in g["rows"])
    for g in multi:
        g["conditions"] = _conditions(g["rows"], header)
        g["confidence"] = _confidence(g["key"], g["conditions"])
    multi.sort(key=lambda g: (-len(g["papers"]), -len(g["rows"]),
                              tuple(query._norm(v) for v in g["key"].values())))
    return {"x": x, "y": y, "key": cols, "groups": multi, "excluded": excluded,
            "counts": {"filtered": len(rows), "kept": sum(len(g["rows"]) for g in multi),
                       "excluded": len(excluded)}}


# -------------------------------------------------------------------- rendu

def _row(r, x, y, short):
    return {"paper": short.get(r["paper_id"], r["paper_id"]), x: r.get(x), y: r.get(y),
            **{f: (r.get(f) or NR) for f in ROW_FIELDS}}


def to_json(res, short):
    """Schéma stable (DATA_MODEL §7.2) : groups (configurations retenues), conditions,
    excluded (motif par ligne), counts."""
    x, y = res["x"], res["y"]
    return {
        "x": x, "y": y, "key": res["key"], "counts": res["counts"],
        "groups": [{"key": g["key"], "confidence": g["confidence"],
                    "papers": [short.get(p, p) for p in g["papers"]],
                    "conditions": g["conditions"],
                    "rows": [_row(r, x, y, short) for r in g["rows"]]} for g in res["groups"]],
        "excluded": [{**_row(r, x, y, short), "reason": why} for r, why in res["excluded"]],
    }


def render(res, short, fmt="tsv", max_chars=None):
    if fmt == "json":
        return json.dumps(to_json(res, short), ensure_ascii=False, indent=1)
    x, y = res["x"], res["y"]
    sep = " | " if fmt == "md" else "\t"

    def line(vals):
        vals = [str(v).replace("\t", " ").replace("|", "/") for v in vals]
        return ("| " + sep.join(vals) + " |") if fmt == "md" else sep.join(vals)

    def head(vals):
        out = [line(vals)]
        if fmt == "md":
            out.append("|" + "---|" * len(vals))
        return out

    c = res["counts"]
    lines = [f"# {c['filtered']} lignes filtrées : {c['kept']} retenues dans {len(res['groups'])} "
             f"groupe(s), {c['excluded']} exclues ; clé : {', '.join(res['key'])}", "",
             "## 1. Configurations retenues"]
    if not res["groups"]:
        lines.append("# aucun groupe ne réunit deux papiers : pas de comparaison valable")
    for i, g in enumerate(res["groups"], start=1):
        key = " ; ".join(f"{k}={v}" for k, v in g["key"].items())
        lines += ["", f"### g{i} [{g['confidence']}] {key}"]
        lines += head(["paper", "model", "platform", x, y, "source_section", "confidence", "chunk_id"])
        for r in g["rows"]:
            d = _row(r, x, y, short)
            lines.append(line([d["paper"], d["model"], d["platform"], d[x], d[y],
                               d["source_section"], d["confidence"], d["chunk_id"]]))
    lines += ["", "## 2. Conditions qui varient ou manquent"]
    any_cond = False
    for i, g in enumerate(res["groups"], start=1):
        for cd in g["conditions"]:
            any_cond = True
            parts = []
            if len(cd["values"]) > 1:
                parts.append(" | ".join(cd["values"]))
            if cd["missing"]:
                parts.append(f"non renseignée pour {cd['missing']} ligne(s)")
            lines.append(f"g{i}\t{cd['column']} : " + " ; ".join(parts))
        if g["key"].get("metric", "").startswith("~"):
            any_cond = True
            lines.append(f"g{i}\tmetric_def non renseignée (définition de la métrique non vérifiée)")
        for k, v in g["key"].items():
            if k != "metric" and _is_nr(v):
                any_cond = True
                lines.append(f"g{i}\t{k} en n/r : comparabilité non établie")
    if not any_cond:
        lines.append("aucune")
    lines += ["", "## 3. Lignes exclues"]
    if res["excluded"]:
        lines += head(["paper", "model", "platform", "motif"])
        for r, why in res["excluded"]:
            lines.append(line([short.get(r["paper_id"], r["paper_id"]), r.get("model") or NR,
                               r.get("platform") or NR, why]))
    else:
        lines.append("aucune")
    lines += ["", "# confidence (high/medium/low) : qualité de la transcription, pas validité de la comparaison"]
    out = "\n".join(lines)
    if max_chars and len(out) > max_chars:
        out = out[:max_chars].rsplit("\n", 1)[0] + "\n# tronqué (--format json pour tout voir)"
    return out
