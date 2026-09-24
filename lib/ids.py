"""Identifiants : paper_id, slugs, détection d'identifiants arXiv."""
import re

from slugify import slugify

# Nouveau format (0704.0001 → 2604.21280) et ancien format (cs/0101001, hep-th/9901001v2).
_ARXIV_NEW = r"\d{4}\.\d{4,5}"
_ARXIV_OLD = r"[a-z\-]+(?:\.[A-Z]{2})?/\d{7}"
_ARXIV_ID = rf"(?P<id>{_ARXIV_NEW}|{_ARXIV_OLD})(?:v\d+)?"

_ARXIV_URL_RE = re.compile(
    rf"arxiv\.org/(?:abs|pdf|html)/{_ARXIV_ID}(?:\.pdf)?", re.IGNORECASE
)
_ARXIV_BARE_RE = re.compile(rf"^(?:arxiv:)?{_ARXIV_ID}$", re.IGNORECASE)

STOPWORDS = set("""
a an and are as at be by for from in into is its of on or over the to toward towards
under using via with without based new novel study approach
le la les un une des du de d et en pour par sur avec dans au aux l
""".split())


def find_arxiv_id(s):
    """Identifiant arXiv (sans suffixe de version) contenu dans s, ou None."""
    s = s.strip()
    m = _ARXIV_BARE_RE.match(s) or _ARXIV_URL_RE.search(s)
    return m.group("id") if m else None


def is_arxiv_url(s):
    return "arxiv.org" in s.lower()


def slug(title, n_min=3, n_max=5):
    """Slug de 3 à 5 mots, minuscules, sans accents ni mots vides."""
    if not title:
        return "untitled"
    words = slugify(title, separator=" ").split()
    kept = [w for w in words if w not in STOPWORDS]
    if len(kept) < n_min:
        kept = words
    return "-".join(kept[:n_max]) or "untitled"


def arxiv_dir_prefix(arxiv_id):
    """Préfixe commun des dossiers d'un article arXiv (ancien format : / → _)."""
    return f"arxiv-{arxiv_id.replace('/', '_')}-"


def make_paper_id(meta):
    """paper_id selon DATA_MODEL §1. Retourne (paper_id, warnings)."""
    warnings = []
    s = slug(meta.get("title"))
    if meta.get("arxiv_id"):
        return arxiv_dir_prefix(meta["arxiv_id"]) + s, warnings
    year = meta.get("year")
    authors = meta.get("authors") or []
    family = authors[0].get("family") if authors else None
    if not year:
        warnings.append("année inconnue : paper_id construit avec 'unknown'")
    if not family:
        warnings.append("premier auteur inconnu : paper_id construit avec 'unknown'")
    first = slugify(family) if family else "unknown"
    return f"{year or 'unknown'}-{first}-{s}", warnings
