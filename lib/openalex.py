"""Client OpenAlex minimal : résolution DOI → arXiv, citations entrantes et sortantes,
travaux liés, recherche par mots-clés. Utilisé par bin/add.py (DOI) et bin/discover.py.

Réponses mises en cache dans .cache/openalex/ (une requête identique ne repart pas sur le
réseau). Variables d'environnement facultatives :
  OPENALEX_MAILTO   adresse de contact (« polite pool » d'OpenAlex, quotas plus larges) ;
  OPENALEX_API_KEY  clé gratuite, utile quand la recherche anonyme est suspendue.

Dans OpenAlex, la version arXiv et la version éditeur d'un article sont souvent deux
travaux distincts : resolve_corpus cherche les deux.
"""
import hashlib
import json
import os
import re
import time
from pathlib import Path

import requests

from lib import ids

API = "https://api.openalex.org"
ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / ".cache" / "openalex"
HEADERS = {"User-Agent": "PaperDatabase/1.0 (usage personnel, recherche bibliographique)"}
ARXIV_DOI_PREFIX = "10.48550/arxiv."
FIELDS = ("id", "doi", "title", "publication_year", "cited_by_count", "primary_location",
          "locations", "best_oa_location", "abstract_inverted_index", "referenced_works",
          "related_works", "type")
MAX_OR = 50  # identifiants par filtre « a|b|c » (limite de l'API : 100)


class OpenAlexError(Exception):
    pass


class Client:
    def __init__(self, cache_dir=CACHE, delay=0.15, session=None):
        self.cache_dir = Path(cache_dir) if cache_dir else None
        self.delay = delay
        self.session = session or requests
        self._last = 0.0

    def get(self, path, params=None):
        params = dict(params or {})
        if os.environ.get("OPENALEX_MAILTO"):
            params["mailto"] = os.environ["OPENALEX_MAILTO"]
        if os.environ.get("OPENALEX_API_KEY"):
            params["api_key"] = os.environ["OPENALEX_API_KEY"]
        public = {k: v for k, v in params.items() if k not in ("mailto", "api_key")}
        key = hashlib.sha1(json.dumps([path, public], sort_keys=True).encode()).hexdigest()
        cached = self.cache_dir / f"{key}.json" if self.cache_dir else None
        if cached and cached.exists():
            return json.loads(cached.read_text())

        wait = self.delay - (time.monotonic() - self._last)
        if wait > 0:
            time.sleep(wait)
        try:
            r = self.session.get(API + path, params=params, headers=HEADERS, timeout=30)
        except (requests.ConnectionError, requests.Timeout) as e:
            raise OpenAlexError(f"réseau indisponible ({type(e).__name__}) : api.openalex.org injoignable")
        self._last = time.monotonic()
        if r.status_code == 404:
            data = None
        elif r.status_code != 200:
            try:
                msg = r.json().get("message") or r.json().get("error")
            except ValueError:
                msg = r.text[:200]
            hint = ("" if os.environ.get("OPENALEX_API_KEY") else
                    " — une clé gratuite (variable OPENALEX_API_KEY, https://openalex.org) lève la plupart des limites")
            raise OpenAlexError(f"OpenAlex HTTP {r.status_code} : {msg}{hint}")
        else:
            data = r.json()
        if cached:
            cached.parent.mkdir(parents=True, exist_ok=True)
            cached.write_text(json.dumps(data))
        return data

    def work(self, key):
        """Un travail par clé OpenAlex (`doi:10.…`, `W123…`), ou None s'il est inconnu."""
        return self.get(f"/works/{key}", {"select": ",".join(FIELDS)})

    def works(self, filter=None, search=None, sort=None, limit=200):
        """Liste de travaux (pagination par curseur), au plus `limit`."""
        out, cursor = [], "*"
        while cursor and len(out) < limit:
            params = {"select": ",".join(FIELDS), "per-page": min(200, limit), "cursor": cursor}
            if filter:
                params["filter"] = filter
            if search:
                params["search"] = search
            if sort:
                params["sort"] = sort
            data = self.get("/works", params) or {}
            out += data.get("results") or []
            cursor = (data.get("meta") or {}).get("next_cursor")
            if not data.get("results"):
                break
        return out[:limit]

    def works_by_ids(self, openalex_ids):
        """Travaux d'une liste d'identifiants OpenAlex, par lots."""
        out, ids_ = [], sorted(set(openalex_ids))
        for i in range(0, len(ids_), MAX_OR):
            chunk = ids_[i:i + MAX_OR]
            out += self.works(filter="openalex_id:" + "|".join(chunk), limit=len(chunk))
        return out


# ---------------------------------------------------------------- lecture d'un travail

def short_id(oa_id):
    return (oa_id or "").rsplit("/", 1)[-1]


def _bare_doi(doi):
    return re.sub(r"^https?://(dx\.)?doi\.org/", "", doi or "", flags=re.IGNORECASE).lower() or None


def arxiv_id_of(work):
    """Identifiant arXiv d'un travail : DOI arXiv, ou l'une de ses localisations."""
    doi = _bare_doi(work.get("doi"))
    if doi and doi.startswith(ARXIV_DOI_PREFIX):
        return doi[len(ARXIV_DOI_PREFIX):]
    for loc in work.get("locations") or []:
        for url in (loc.get("landing_page_url"), loc.get("pdf_url")):
            if url and ids.is_arxiv_url(url):
                a = ids.find_arxiv_id(url)
                if a:
                    return a
    return None


def doi_of(work):
    """DOI éditeur (le DOI arXiv 10.48550 n'en est pas un)."""
    doi = _bare_doi(work.get("doi"))
    return None if not doi or doi.startswith(ARXIV_DOI_PREFIX) else doi


def venue_of(work):
    src = (work.get("primary_location") or {}).get("source") or {}
    return src.get("display_name")


def oa_url_of(work):
    """Lien open access légal fourni par OpenAlex (PDF, sinon page d'accueil)."""
    loc = work.get("best_oa_location") or {}
    return loc.get("pdf_url") or loc.get("landing_page_url")


def abstract_of(work):
    inv = work.get("abstract_inverted_index") or {}
    pos = sorted((i, w) for w, idx in inv.items() for i in idx)
    return " ".join(w for _, w in pos) or None


def summary(work):
    """Vue plate d'un travail, pour candidates.csv."""
    return {
        "openalex_id": short_id(work.get("id")),
        "title": " ".join((work.get("title") or "").split()) or None,
        "year": work.get("publication_year"),
        "venue": venue_of(work),
        "doi": doi_of(work),
        "arxiv_id": arxiv_id_of(work),
        "oa_url": oa_url_of(work),
        "cited_by_count": work.get("cited_by_count") or 0,
        "abstract": abstract_of(work),
    }


# ---------------------------------------------------------------- corpus

def lookup_keys(meta):
    """Clés OpenAlex sous lesquelles chercher un papier du corpus (éditeur, puis arXiv)."""
    keys = []
    if meta.get("doi") and not meta["doi"].lower().startswith(ARXIV_DOI_PREFIX):
        keys.append("doi:" + meta["doi"].lower())
    if meta.get("arxiv_id"):
        keys.append("doi:" + ARXIV_DOI_PREFIX + meta["arxiv_id"].lower())
    return keys


def resolve_corpus(client, papers):
    """{paper_id: [travaux OpenAlex]} ; un papier absent d'OpenAlex a une liste vide."""
    found = {}
    for p in papers:
        works = []
        for k in lookup_keys(p):
            w = client.work(k)
            if w and all(w["id"] != x["id"] for x in works):
                works.append(w)
        found[p["id"]] = works
    return found


def resolve_doi(client, doi):
    """(travail, arxiv_id) pour un DOI ; (None, None) si OpenAlex ne le connaît pas."""
    doi = _bare_doi(doi)
    if doi.startswith(ARXIV_DOI_PREFIX):
        return None, doi[len(ARXIV_DOI_PREFIX):]
    w = client.work("doi:" + doi)
    return (w, arxiv_id_of(w)) if w else (None, None)
