"""Schéma de la base : metadata.json, benchmarks.csv, fiche.md.

Seul endroit où le contrat de DATA_MODEL.md est codé. Toute évolution du schéma se fait ici.
"""
import datetime as _dt
import re

from lib import base, ids

NR = "n/r"

AXES = tuple(base.CONFIG["axes"])  # propres à chaque base : base.json (DATA_MODEL §11)
TYPES = ("preprint", "journal", "conference", "thesis", "repo", "report")
BACKENDS = ("grobid", "pymupdf")
FICHE_STATUS = ("todo", "done")
SECTION_KINDS = ("abstract", "section", "figure", "table")
CONFIDENCE = ("high", "medium", "low")
# Portée de power_w (DATA_MODEL §7) : puce, carte, carte moins le repos, estimation par outil,
# ou mesure dont la portée n'est pas dite. n/r quand power_w vaut n/r.
POWER_SCOPES = ("chip", "board", "board-dynamic", "estimated", "unspecified")

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
    "power_scope",
    "luts",
    "dsps",
    "bram",
    "dataset",
    "toolflow",
    "baseline",
    "source_section",
    "confidence",
)

# Colonnes optionnelles (DATA_MODEL §7) : après les obligatoires, un sous-ensemble dans
# n'importe quel ordre. Absente, une colonne vaut n/r ; présente, elle suit les mêmes règles.
OPTIONAL_COLUMNS = (
    "chunk_id",          # passage qui contient la valeur (pdb show / pdb bench --check)
    "metric_def",        # définition exacte de accuracy_metric
    "dataset_split",
    "input_res",
    "batch",
    "measure_protocol",  # comment FPS et puissance sont mesurés
    "original_value",    # valeur telle qu'écrite, si une colonne est normalisée
    "platform_class",    # embedded | server : mesure de référence hors cible embarquée
)
PLATFORM_CLASSES = ("embedded", "server")
ALL_COLUMNS = BENCHMARK_COLUMNS + OPTIONAL_COLUMNS

# Colonnes numériques : un nombre ou n/r, rien d'autre.
NUMERIC_COLUMNS = (
    "accuracy_value", "fps", "gops", "latency_ms", "power_w", "luts", "dsps", "bram",
)

NO_BENCHMARKS = "none"  # front-matter de fiche.md : `benchmarks: none`, absence de ligne justifiée

WARN_MANUAL_METADATA ="métadonnées à vérifier à la main"
WARN_AXES_GUESSED = "axes déduits automatiquement, à confirmer dans /paper-fiche"
# Tableaux dont GROBID n'a gardé que la légende (lib/tables.py), recalculés à chaque extraction
WARN_TABLES_RECOVERED = "tableaux reconstruits par PyMuPDF, chiffres à vérifier"
WARN_TABLES_DOCLING = "tableaux reconstruits par Docling, chiffres à vérifier"
WARN_TABLES_LOST = "tableaux sans corps extrait (légende seule)"

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


# chunk_id : <paper_id ou id court>#<section>[.<k>] (lib/rag.load_chunks, resolve_chunk_id)
CHUNK_ID_RE = re.compile(r"^[^#\s]+#\d+(?:\.\d+)?$")


def check_header(fieldnames):
    """En-tête de benchmarks.csv : les colonnes obligatoires en tête et dans l'ordre, puis un
    sous-ensemble des optionnelles. Liste des problèmes ; vide si conforme."""
    names = list(fieldnames or ())
    n = len(BENCHMARK_COLUMNS)
    if tuple(names[:n]) != BENCHMARK_COLUMNS:
        return ["en-tête : les colonnes de schema.BENCHMARK_COLUMNS doivent venir en tête, dans l'ordre"]
    errs = []
    extra = names[n:]
    unknown = [c for c in extra if c not in OPTIONAL_COLUMNS]
    if unknown:
        errs.append(f"en-tête : colonne(s) inconnue(s) : {', '.join(unknown)} "
                    f"(optionnelles : {', '.join(OPTIONAL_COLUMNS)})")
    dup = sorted({c for c in extra if extra.count(c) > 1})
    if dup:
        errs.append(f"en-tête : colonne(s) en double : {', '.join(dup)}")
    return errs


def validate_benchmark_row(row):
    """row : dict issu de csv.DictReader. Liste des problèmes ; vide si conforme."""
    errs = []
    missing = [c for c in BENCHMARK_COLUMNS if c not in row]
    if missing:
        return [f"colonnes manquantes : {', '.join(missing)}"]
    present = [c for c in OPTIONAL_COLUMNS if c in row]
    for c in (*BENCHMARK_COLUMNS, *present):
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
    scope, power = (row["power_scope"] or "").strip(), (row["power_w"] or "").strip()
    if power == NR and scope != NR:
        errs.append(f"power_scope = {scope!r} alors que power_w = n/r : n/r attendu")
    elif power not in (NR, "") and scope not in POWER_SCOPES:
        errs.append(f"power_scope = {scope!r} : {' | '.join(POWER_SCOPES)}")
    batch = (row.get("batch") or "").strip()
    if batch not in ("", NR) and not batch.isdigit():
        errs.append(f"batch = {batch!r} : entier ou n/r attendu")
    pclass = (row.get("platform_class") or "").strip()
    if pclass not in ("", NR) and pclass not in PLATFORM_CLASSES:
        errs.append(f"platform_class = {pclass!r} : {' | '.join(PLATFORM_CLASSES)} | n/r")
    chunk = (row.get("chunk_id") or "").strip()
    if chunk not in ("", NR) and not CHUNK_ID_RE.match(chunk):
        errs.append(f"chunk_id = {chunk!r} : forme <paper_id>#<section>.<k> attendue")
    return errs


# --- claims.jsonl (DATA_MODEL §12) : preuves atomiques, chacune liée à un passage ----------

CLAIM_KINDS = ("résultat", "méthode", "limite", "hypothèse", "contexte")
CLAIM_VOICES = ("auteurs", "déduit")
CLAIM_REQUIRED = ("claim_id", "kind", "text", "voice", "source_chunk", "excerpt")
CLAIM_OPTIONAL = ("conditions", "benchmark_row", "caveats", "chunk_sha1")
CLAIM_ID_RE = re.compile(r"^(?P<pid>[^!\s]+)!c\d{2,}$")
SHA_PREFIX_RE = re.compile(r"^[0-9a-f]{8,40}$")


def validate_claim_row(row, paper_id, n_bench_rows=None):
    """Une ligne de claims.jsonl (schéma seul : l'excerpt est contrôlé par lib/claims.check).
    n_bench_rows : nombre de lignes du papier dans benchmarks.csv, borne de benchmark_row."""
    if not isinstance(row, dict):
        return ["objet JSON attendu"]
    missing = [k for k in CLAIM_REQUIRED if k not in row]
    if missing:
        return [f"clé(s) manquante(s) : {', '.join(missing)}"]
    errs = []
    unknown = sorted(k for k in row if k not in CLAIM_REQUIRED + CLAIM_OPTIONAL)
    if unknown:
        errs.append(f"clé(s) inconnue(s) : {', '.join(unknown)}")
    for k in CLAIM_REQUIRED:
        if not isinstance(row[k], str) or not row[k].strip():
            errs.append(f"{k} vide ou non textuel")
    if errs:
        return errs
    m = CLAIM_ID_RE.match(row["claim_id"])
    if not m or m.group("pid") != paper_id:
        errs.append(f"claim_id = {row['claim_id']!r} : {paper_id}!c<NN> attendu")
    if row["kind"] not in CLAIM_KINDS:
        errs.append(f"kind = {row['kind']!r} : {' | '.join(CLAIM_KINDS)}")
    if row["voice"] not in CLAIM_VOICES:
        errs.append(f"voice = {row['voice']!r} : {' | '.join(CLAIM_VOICES)}")
    if not CHUNK_ID_RE.match(row["source_chunk"]):
        errs.append(f"source_chunk = {row['source_chunk']!r} : forme <paper_id>#<section>.<k> attendue")
    cond = row.get("conditions")
    if cond is not None:
        if not isinstance(cond, dict):
            errs.append("conditions doit être un objet")
        else:
            for k, v in cond.items():
                if not isinstance(v, str) or not v.strip():
                    errs.append(f"conditions.{k} vide ou non textuel : écrire n/r")
            scope = cond.get("power_scope")
            if isinstance(scope, str) and scope not in (NR, *POWER_SCOPES):
                errs.append(f"conditions.power_scope = {scope!r} : {' | '.join(POWER_SCOPES)} | n/r")
    br = row.get("benchmark_row")
    if br is not None:
        if not isinstance(br, int) or isinstance(br, bool) or br < 1:
            errs.append(f"benchmark_row = {br!r} : entier ≥ 1 ou null")
        elif n_bench_rows is not None and br > n_bench_rows:
            errs.append(f"benchmark_row = {br} : le papier n'a que {n_bench_rows} ligne(s) dans benchmarks.csv")
    cav = row.get("caveats")
    if cav is not None and (not isinstance(cav, list)
                            or not all(isinstance(c, str) and c.strip() for c in cav)):
        errs.append("caveats doit être une liste de textes non vides")
    sha = row.get("chunk_sha1")
    if sha is not None and not (isinstance(sha, str) and SHA_PREFIX_RE.match(sha)):
        errs.append(f"chunk_sha1 = {sha!r} : 8 à 40 caractères hexadécimaux")
    return errs


# --- paper_id, sections.jsonl, refs.jsonl, front-matter -------------------------------

_SLUG = r"[a-z0-9]+(?:-[a-z0-9]+)*"
PAPER_ID_RE = re.compile(
    rf"^(?:arxiv-(?:\d{{4}}\.\d{{4,5}}|[a-z\-]+(?:\.[A-Za-z]{{2}})?_\d{{7}})-{_SLUG}"
    rf"|(?:\d{{4}}|unknown)-{_SLUG})$"
)

# Mesures propres (DATA_MODEL §1) : lignes de benchmarks.csv sans dossier papers/, dont la
# source est le protocole docs/experiences/<slug>.md.
OWN_ID_RE = re.compile(rf"^own-\d{{4}}-({_SLUG})$")
EXPERIENCES_DIR = "docs/experiences"


def is_own_id(pid):
    return bool(OWN_ID_RE.match(pid or ""))


def own_source(pid):
    """Chemin (relatif au dossier de la base) du protocole d'une mesure propre ; None si pid n'en est pas une."""
    m = OWN_ID_RE.match(pid or "")
    return f"{EXPERIENCES_DIR}/{m.group(1)}.md" if m else None


SECTION_KEYS = ("id", "paper_id", "kind", "section", "subsection", "order", "page", "text")
# lignes kind "table" seulement (lot E-a) : zone du tableau sur la page de la ligne, origine du corps
SECTION_TABLE_KEYS = ("bbox", "table_source")
TABLE_SOURCES = ("grobid", "pymupdf", "docling", "docling-ocr")
REF_KEYS = ("paper_id", "raw", "title", "authors", "year", "doi", "arxiv_id")


def validate_paper_id(pid, meta):
    """DATA_MODEL §1. Liste des problèmes ; vide si conforme."""
    if not PAPER_ID_RE.match(pid or ""):
        return [f"paper_id {pid!r} : forme arxiv-<id>-<slug> ou <annee>-<auteur>-<slug> attendue"]
    arxiv_id = meta.get("arxiv_id")
    if arxiv_id and not pid.startswith(ids.arxiv_dir_prefix(arxiv_id)):
        return [f"paper_id {pid!r} ne commence pas par {ids.arxiv_dir_prefix(arxiv_id)!r}"]
    if not arxiv_id and pid.startswith("arxiv-"):
        return [f"paper_id {pid!r} de forme arXiv, mais arxiv_id vaut null"]
    return []


def _no_empty_strings(row, keys):
    return [f"{k} vaut \"\" : utiliser null" for k in keys if row.get(k) == ""]


def validate_section_row(row, paper_id, order):
    """Une ligne de sections.jsonl (DATA_MODEL §5), attendue à la position order."""
    extra = set(row) - set(SECTION_KEYS)
    if not set(SECTION_KEYS) <= set(row) or not extra <= set(SECTION_TABLE_KEYS):
        return [f"clés {sorted(row)} ≠ {sorted(SECTION_KEYS)} (+ {', '.join(SECTION_TABLE_KEYS)})"]
    errs = _no_empty_strings(row, ("subsection",))
    if extra and row["kind"] != "table":
        errs.append(f"{', '.join(sorted(extra))} : réservé(s) aux lignes kind table")
    if "table_source" in row and row["table_source"] not in TABLE_SOURCES:
        errs.append(f"table_source inconnu : {row['table_source']!r} ({' | '.join(TABLE_SOURCES)})")
    if "bbox" in row:
        b = row["bbox"]
        if not (isinstance(b, list) and len(b) == 4
                and all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in b)
                and b[0] < b[2] and b[1] < b[3]):
            errs.append(f"bbox = {b!r} : [x0, y0, x1, y1] attendu, x0 < x1 et y0 < y1")
    if row["paper_id"] != paper_id:
        errs.append(f"paper_id = {row['paper_id']!r}")
    if row["order"] != order:
        errs.append(f"order = {row['order']!r}, {order} attendu")
    if row["id"] != f"{paper_id}#{order:03d}":
        errs.append(f"id = {row['id']!r}, {paper_id}#{order:03d} attendu")
    if row["kind"] not in SECTION_KINDS:
        errs.append(f"kind inconnu : {row['kind']!r}")
    if not isinstance(row["section"], str) or not row["section"].strip():
        errs.append("section vide")
    page = row["page"]
    if page is not None and (not isinstance(page, int) or isinstance(page, bool) or page < 1):
        errs.append(f"page = {page!r} : entier ≥ 1 ou null")
    if not isinstance(row["text"], str) or not row["text"].strip():
        errs.append("text vide")
    return errs


def validate_ref_row(row, paper_id):
    """Une ligne de refs.jsonl (DATA_MODEL §6)."""
    if tuple(sorted(row)) != tuple(sorted(REF_KEYS)):
        return [f"clés {sorted(row)} ≠ {sorted(REF_KEYS)}"]
    errs = _no_empty_strings(row, ("raw", "title", "doi", "arxiv_id"))
    if row["paper_id"] != paper_id:
        errs.append(f"paper_id = {row['paper_id']!r}")
    if not isinstance(row["authors"], list):
        errs.append("authors doit être une liste")
    year = row["year"]
    if year is not None and (not isinstance(year, int) or isinstance(year, bool)):
        errs.append(f"year = {year!r} : entier ou null")
    return errs


def read_front_matter(text):
    """Front-matter `clé: valeur` d'un fichier Markdown ; {} s'il n'y en a pas.

    Les valeurs restent des chaînes, guillemets retirés ; `null` et une valeur vide donnent None.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    out = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return out
        key, sep, value = line.partition(":")
        if not sep:
            continue
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] == '"':
            value = value[1:-1].replace('\\"', '"').replace("\\\\", "\\")
        out[key.strip()] = None if value in ("", "null") else value
    return {}  # front-matter non refermé


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
    "report": "rapport (autorité, institution)",
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
