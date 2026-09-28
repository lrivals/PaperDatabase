"""Rapprochement des références (refs.jsonl) entre elles et avec les papiers du corpus.

Sans dépendance de visualisation : utilisé par lib/graph.py (vue 3D) et par
bin/reindex.py (classement external_refs.csv).

Deux références désignent le même travail si elles partagent une clé exacte
(arXiv → DOI → titre normalisé), ou, à défaut, si leurs titres sont quasi identiques
(coquille, troncature ou ponctuation d'un parsing GROBID) avec des années compatibles.
Deux publications aux titres réellement différents (ex. fpgaConvNet FCCM 2016 et
TNNLS 2019) restent distinctes.
"""
import difflib
import json
import re
from collections import defaultdict
from pathlib import Path

from slugify import slugify

MIN_TITLE_WORDS = 4     # un titre plus court est trop ambigu pour servir de clé
FUZZY_RATIO = 0.92      # SequenceMatcher sur les titres normalisés
PREFIX_MIN_WORDS = 6    # titre tronqué : préfixe d'au moins 6 mots de l'autre
MAX_YEAR_GAP = 1        # au-delà, deux titres voisins sont deux publications

EXTERNAL_FIELDS = ("rank", "n_citers", "title", "year", "arxiv_id", "doi", "citers")


# ---------------------------------------------------------------- clés

def title_words(title):
    return slugify(title or "", separator=" ").split()


def title_key(title):
    words = title_words(title)
    return "title:" + "-".join(words) if len(words) >= MIN_TITLE_WORDS else None


def ref_keys(d):
    """Clés de rapprochement d'une référence ou d'un metadata : arxiv → doi → titre."""
    keys = []
    if d.get("arxiv_id"):
        keys.append("arxiv:" + re.sub(r"v\d+$", "", d["arxiv_id"].lower()))
    if d.get("doi"):
        keys.append("doi:" + d["doi"].lower())
    tk = title_key(d.get("title"))
    if tk:
        keys.append(tk)
    return keys


# ---------------------------------------------------------------- titres voisins

def _years_compatible(a, b):
    return a is None or b is None or abs(a - b) <= MAX_YEAR_GAP


def same_title(wa, wb):
    """Titres normalisés (listes de mots) quasi identiques."""
    if len(wa) < MIN_TITLE_WORDS or len(wb) < MIN_TITLE_WORDS:
        return False
    short, long_ = sorted((wa, wb), key=len)
    if len(short) >= PREFIX_MIN_WORDS and long_[:len(short)] == short:
        return True
    sa, sb = " ".join(wa), " ".join(wb)
    # borne de real_quick_ratio, calculée sans construire le SequenceMatcher (coûteux)
    if 2 * min(len(sa), len(sb)) < FUZZY_RATIO * (len(sa) + len(sb)):
        return False
    m = difflib.SequenceMatcher(None, sa, sb, autojunk=False)
    return (m.real_quick_ratio() >= FUZZY_RATIO and m.quick_ratio() >= FUZZY_RATIO
            and m.ratio() >= FUZZY_RATIO)


_SHORT_OK = {"a", "an", "as", "at", "by", "in", "is", "of", "on", "or", "to", "vs", "ai", "ml",
             "3d", "2d", "io", "ip", "fp", "we", "be", "do"}


def best_title(titles):
    """Titre d'affichage d'un groupe : le moins abîmé par l'extraction (ligatures perdues,
    ex. « E cient » pour « Efficient »), puis le plus complet, ponctuation finale exclue."""
    def broken(t):
        return sum(1 for w in re.findall(r"[^\W_]+", t)
                   if len(w) <= 2 and w.lower() not in _SHORT_OK and not w.isdigit())
    return min(titles, key=lambda t: (broken(t), -len(t.rstrip(" .")))) if titles else None


_ALPHABET = {c: i for i, c in enumerate("abcdefghijklmnopqrstuvwxyz0123456789 ")}


def _char_counts(s):
    """Comptes par caractère ; tout autre caractère dans une case commune (la borne reste
    supérieure ou égale au vrai quick_ratio : le filtre ne rejette jamais à tort)."""
    v = [0] * (len(_ALPHABET) + 1)
    for c in s:
        v[_ALPHABET.get(c, len(_ALPHABET))] += 1
    return v


class _TitleIndex:
    """Titres déjà vus → cible ; recherche d'un titre voisin, filtrée par l'année."""

    # Seuls deux cas peuvent rendre same_title vrai : longueurs voisines (borne du ratio), ou
    # préfixe d'au moins PREFIX_MIN_WORDS mots, donc mêmes premiers mots. On n'examine que ces
    # entrées-là, dans l'ordre d'insertion (la première qui correspond gagne, comme avant).

    def __init__(self):
        self.entries = []               # (mots, année, cible)
        self.vecs = []                  # comptes de caractères (borne de quick_ratio)
        self.by_len = defaultdict(list)     # longueur du titre joint → indices
        self.by_prefix = defaultdict(list)  # PREFIX_MIN_WORDS premiers mots → indices

    def add(self, title, year, target):
        words = title_words(title)
        if len(words) >= MIN_TITLE_WORDS:
            i = len(self.entries)
            self.entries.append((words, year, target))
            self.vecs.append(_char_counts(" ".join(words)))
            self.by_len[len(" ".join(words))].append(i)
            if len(words) >= PREFIX_MIN_WORDS:
                self.by_prefix[tuple(words[:PREFIX_MIN_WORDS])].append(i)

    def find(self, title, year):
        words = title_words(title)
        if len(words) < MIN_TITLE_WORDS:
            return None
        n = len(" ".join(words))
        lo, hi = n * FUZZY_RATIO / (2 - FUZZY_RATIO), n * (2 - FUZZY_RATIO) / FUZZY_RATIO
        cand = {i for length in range(int(lo), int(hi) + 2) for i in self.by_len.get(length, ())}
        prefix = set(self.by_prefix.get(tuple(words[:PREFIX_MIN_WORDS]), ())) \
            if len(words) >= PREFIX_MIN_WORDS else set()
        vec = _char_counts(" ".join(words))
        for i in sorted(cand | prefix):
            w, y, target = self.entries[i]
            if not _years_compatible(year, y):
                continue
            # quick_ratio ≥ FUZZY_RATIO est nécessaire hors préfixe : testé ici sans difflib
            if i not in prefix:
                m = sum(map(min, vec, self.vecs[i]))
                if 2 * m < FUZZY_RATIO * (n + len(" ".join(w))):
                    continue
            if same_title(words, w):
                return target
        return None


# ---------------------------------------------------------------- regroupement

def group_refs(papers):
    """Rattache chaque référence à un papier du corpus ou à un groupe externe.

    papers : dicts metadata + clé "refs" (lignes de refs.jsonl).
    Retourne (cites, groups) :
      cites  — paper_id → set de cibles (paper_id du corpus ou "ext:<clé>")
      groups — "ext:<clé>" → {title, year, arxiv_id, doi, keys, raw, variants}
               (variants : tous les titres rencontrés ; title : le meilleur d'entre eux)
    """
    corpus_key, corpus_titles = {}, _TitleIndex()
    for p in papers:
        for k in ref_keys(p):
            corpus_key[k] = p["id"]
        corpus_titles.add(p.get("title"), p.get("year"), p["id"])

    group_of, groups, group_titles = {}, {}, _TitleIndex()
    cites = defaultdict(set)
    for p in papers:
        for r in p["refs"]:
            keys = ref_keys(r)
            if not keys:
                continue
            target = next((corpus_key[k] for k in keys if k in corpus_key), None)
            if target is None:
                target = corpus_titles.find(r.get("title"), r.get("year"))
            if target is None:
                target = next((group_of[k] for k in keys if k in group_of), None)
                if target is None:
                    target = group_titles.find(r.get("title"), r.get("year"))
                if target is None:
                    target = "ext:" + keys[0]
                    groups[target] = {"title": r.get("title"), "year": r.get("year"),
                                      "arxiv_id": r.get("arxiv_id"), "doi": r.get("doi"),
                                      "keys": [], "raw": r.get("raw"), "variants": []}
                g = groups[target]
                for f in ("title", "year", "arxiv_id", "doi"):
                    if g[f] is None and r.get(f) is not None:
                        g[f] = r[f]
                if r.get("title") and r["title"] not in g["variants"]:
                    g["variants"].append(r["title"])
                for k in keys:
                    if k not in g["keys"]:
                        g["keys"].append(k)
                    group_of.setdefault(k, target)
                group_titles.add(r.get("title"), r.get("year"), target)
            if target != p["id"]:
                cites[p["id"]].add(target)
    for g in groups.values():
        g["title"] = best_title(g["variants"]) or g["title"]
    return cites, groups


def citers_of(cites):
    citers = defaultdict(set)
    for pid, targets in cites.items():
        for t in targets:
            citers[t].add(pid)
    return citers


def citations(papers):
    """(cites, citers, groups) : qui cite quoi, qui est cité par qui (cibles internes et
    groupes « ext: »), et les groupes externes. Utilisé par bin/pdb cites / cited-by."""
    cites, groups = group_refs(papers)
    return cites, citers_of(cites), groups


def external_ranking(papers, min_citers=2):
    """Travaux absents de la base cités par au moins min_citers papiers, du plus cité au
    moins cité (puis du plus récent au plus ancien)."""
    cites, groups = group_refs(papers)
    citers = citers_of(cites)
    rows = [(gid, g, sorted(citers[gid])) for gid, g in groups.items()
            if len(citers[gid]) >= min_citers]
    rows.sort(key=lambda x: (-len(x[2]), -(x[1]["year"] or 0), (x[1]["title"] or "").lower()))
    return [{"rank": i, "n_citers": len(c), "title": g["title"] or g["raw"] or gid,
             "year": g["year"], "arxiv_id": g["arxiv_id"], "doi": g["doi"], "citers": ";".join(c)}
            for i, (gid, g, c) in enumerate(rows, 1)]


def load_papers(root):
    """metadata.json + refs.jsonl de chaque papier de root/papers."""
    papers = []
    for path in sorted(Path(root, "papers").glob("*/metadata.json")):
        meta = json.loads(path.read_text())
        refs_path = path.parent / "refs.jsonl"
        refs = ([json.loads(l) for l in refs_path.read_text().splitlines() if l.strip()]
                if refs_path.exists() else [])
        papers.append({**meta, "refs": refs})
    return papers
