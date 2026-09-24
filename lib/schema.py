"""Schéma de la base : metadata.json, benchmarks.csv, fiche.md.

Seul endroit où le contrat de DATA_MODEL.md est codé. Toute évolution du schéma se fait ici.
"""
import datetime as _dt

NR = "n/r"

AXES = (
    "surveys",
    "yolo-fpga",
    "autoencoder-fpga",
    "continual-learning",
    "toolflows",
    "platforms",
)
TYPES = ("preprint", "journal", "conference", "thesis", "repo")
BACKENDS = ("grobid", "pymupdf")
FICHE_STATUS = ("todo", "done")
SECTION_KINDS = ("abstract", "section", "figure", "table")
CONFIDENCE = ("high", "medium", "low")

BENCHMARK_COLUMNS = (
    "paper_id",
    "model",
    "task",
    "platform",
    "quantization",
    "accuracy_metric",
    "accuracy_value",
    "fps",
    "gops",
    "latency_ms",
    "power_w",
    "luts",
    "dsps",
    "bram",
    "dataset",
    "toolflow",
    "baseline",
    "source_section",
    "confidence",
)

# Colonnes numériques : un nombre ou n/r, rien d'autre.
NUMERIC_COLUMNS = (
    "accuracy_value", "fps", "gops", "latency_ms", "power_w", "luts", "dsps", "bram",
)

WARN_MANUAL_METADATA = "métadonnées à vérifier à la main"
WARN_AXES_GUESSED = "axes déduits automatiquement, à confirmer dans /paper-fiche"

METADATA_KEYS = (
    "id", "title", "authors", "year", "venue", "doi", "arxiv_id", "url", "type",
    "axes", "tags", "added", "extraction", "status",
)


def new_metadata(paper_id=None):
    """metadata.json vierge : tout champ inconnu vaut None."""
    return {
        "id": paper_id,
        "title": None,
        "authors": [],
        "year": None,
        "venue": None,
        "doi": None,
        "arxiv_id": None,
        "url": None,
        "type": None,
        "axes": [],
        "tags": [],
        "added": _dt.date.today().isoformat(),
        "extraction": {"backend": None, "ok": True, "warnings": []},
        "status": {"extracted": False, "fiche": "todo"},
    }


def validate_metadata(d):
    """Liste des problèmes de conformité ; vide si le fichier est conforme."""
    errs = []
    for k in METADATA_KEYS:
        if k not in d:
            errs.append(f"champ manquant : {k}")
    if errs:
        return errs

    for k in ("title", "venue", "doi", "arxiv_id", "url"):
        v = d[k]
        if v is not None and not isinstance(v, str):
            errs.append(f"{k} doit être une chaîne ou null")
        if v == "":
            errs.append(f"{k} vaut \"\" : utiliser null")
    if not isinstance(d["authors"], list):
        errs.append("authors doit être une liste")
    else:
        for i, a in enumerate(d["authors"]):
            if not isinstance(a, dict) or set(a) != {"given", "family"}:
                errs.append(f"authors[{i}] doit être {{given, family}}")
    if d["year"] is not None and not isinstance(d["year"], int):
        errs.append("year doit être un entier ou null")
    if d["type"] is not None and d["type"] not in TYPES:
        errs.append(f"type inconnu : {d['type']}")
    for a in d["axes"]:
        if a not in AXES:
            errs.append(f"axe inconnu : {a}")
    if not isinstance(d["tags"], list):
        errs.append("tags doit être une liste")
    try:
        _dt.date.fromisoformat(d["added"])
    except (TypeError, ValueError):
        errs.append("added doit être une date ISO")

    ex = d["extraction"]
    if not isinstance(ex, dict) or ex.get("backend") not in BACKENDS:
        errs.append("extraction.backend doit valoir grobid ou pymupdf")
    elif not isinstance(ex.get("ok"), bool) or not isinstance(ex.get("warnings"), list):
        errs.append("extraction.ok (bool) et extraction.warnings (liste) requis")
    st = d["status"]
    if not isinstance(st, dict) or st.get("fiche") not in FICHE_STATUS:
        errs.append("status.fiche doit valoir todo ou done")
    elif not isinstance(st.get("extracted"), bool):
        errs.append("status.extracted doit être un booléen")
    return errs


def validate_benchmark_row(row):
    """row : dict issu de csv.DictReader. Liste des problèmes ; vide si conforme."""
    errs = []
    missing = [c for c in BENCHMARK_COLUMNS if c not in row]
    if missing:
        return [f"colonnes manquantes : {', '.join(missing)}"]
    for c in BENCHMARK_COLUMNS:
        if (row[c] or "").strip() == "":
            errs.append(f"{c} vide : écrire n/r")
    for c in NUMERIC_COLUMNS:
        v = (row[c] or "").strip()
        if v and v != NR:
            try:
                float(v)
            except ValueError:
                errs.append(f"{c} = {v!r} : nombre ou n/r attendu")
    if row["confidence"] not in CONFIDENCE:
        errs.append(f"confidence = {row['confidence']!r} : high | medium | low")
    return errs


FICHE_TEMPLATE = """\
---
id: {id}
fiche: todo
date:
---

# {title}

{authors}, {year}, {venue}. {link}
Type : {type_label}

## Problème

Quel verrou le papier attaque-t-il, tel que les auteurs le posent.

## Méthode

Architecture, quantification, stratégie de mapping sur le FPGA, post-traitement (NMS…).
Toolflow employé.

## Plateforme et implémentation

Puce exacte, fréquence, ressources consommées, mémoire. Code ou bitstream publiés ? Où ?

## Résultats

Les chiffres, avec la section ou le tableau source. Baseline de comparaison.
→ reportés dans `benchmarks.csv` : <lignes ajoutées>

## Limites et critique

Comparaisons biaisées, métriques non comparables d'un papier à l'autre, conditions de mesure
non précisées, absence de reproductibilité. Ce que le papier ne mesure pas.

## Pertinence pour la thèse

Ce que ce travail apporte à l'axe visé, et ce qu'il laisse ouvert.

## Gaps identifiés

Points à reporter dans `gaps.md`.

## Statut de lecture

Résumé seul | sections lues : <liste> | papier complet.
Ce qui suit est déduit et non affirmé par les auteurs : <…>
"""

TYPE_LABELS = {
    "preprint": "preprint non relu par les pairs",
    "journal": "article de journal",
    "conference": "conférence",
    "thesis": "thèse",
    "repo": "dépôt de code",
    None: NR,
}


def format_authors(authors, max_n=None):
    names = [" ".join(p for p in (a.get("given"), a.get("family")) if p) for a in authors]
    if not names:
        return NR
    if max_n and len(names) > max_n:
        return f"{authors[0].get('family') or names[0]} et al."
    return ", ".join(names)


def render_fiche(meta):
    link = (f"https://doi.org/{meta['doi']}" if meta.get("doi") else meta.get("url")) or NR
    return FICHE_TEMPLATE.format(
        id=meta["id"],
        title=meta.get("title") or NR,
        authors=format_authors(meta.get("authors") or []),
        year=meta.get("year") or NR,
        venue=meta.get("venue") or NR,
        link=link,
        type_label=TYPE_LABELS.get(meta.get("type"), meta.get("type")),
    )
