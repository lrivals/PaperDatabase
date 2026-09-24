"""Graphe du corpus pour la visualisation 3D (bin/viz.py) : nœuds, liens, positions.

Couche données pure, sans Dash. Dépendances : requirements-viz.txt (numpy, scikit-learn,
networkx). Ne modifie aucun fichier de la base.

Types de liens :
  citation  — un papier cite un autre papier du corpus (dirigé)
  coupling  — références partagées (couplage bibliographique), poids = cosinus de Salton
              |A∩B| / √(|A|·|B|), moins écrasé que Jaccard par les surveys à 600 réfs
  text      — similarité cosinus TF-IDF sur le texte intégral
  themes    — axes et tags communs, poids = Jaccard
"""
import csv
import json
import random
import re
from collections import defaultdict
from itertools import combinations
from pathlib import Path

import networkx as nx
import numpy as np
from slugify import slugify
from sklearn.feature_extraction.text import TfidfVectorizer

from lib import schema

LINK_TYPES = ("citation", "coupling", "text", "themes")
TEXT_KINDS = ("abstract", "section")
MIN_TITLE_WORDS = 4   # un titre plus court est trop ambigu pour servir de clé


# ---------------------------------------------------------------- chargement

def _read_jsonl(path):
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def load_corpus(root):
    """Papiers de root/papers, avec texte, références et lignes de benchmarks.csv."""
    root = Path(root)
    bench = defaultdict(list)
    bench_path = root / "benchmarks.csv"
    if bench_path.exists():
        with open(bench_path, newline="") as f:
            for row in csv.DictReader(f):
                bench[row["paper_id"]].append(row)

    papers = []
    for path in sorted((root / "papers").glob("*/metadata.json")):
        meta = json.loads(path.read_text())
        d = path.parent
        sections = _read_jsonl(d / "sections.jsonl")
        papers.append({
            **meta,
            "text": "\n".join(s["text"] for s in sections if s.get("kind") in TEXT_KINDS),
            "refs": _read_jsonl(d / "refs.jsonl"),
            "benchmarks": bench.get(meta["id"], []),
        })
    return papers


# ---------------------------------------------------------- clés de références

def title_key(title):
    words = slugify(title or "", separator=" ").split()
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


# ---------------------------------------------------------------------- graphe

class CorpusGraph:
    """nodes : dict id → nœud ; links : liste de {source, target, type, weight, label}.

    Les liens `text` sont calculés pour toutes les paires ; le seuil s'applique à
    l'affichage (links_for).
    """

    def __init__(self, papers, min_citers=2):
        self.papers = papers
        self.nodes = {}
        self.links = []
        self.tfidf = None
        self._build_nodes()
        self._resolve_refs(min_citers)
        self._build_links()

    # -- nœuds

    def _build_nodes(self):
        for p in self.papers:
            self.nodes[p["id"]] = {
                "id": p["id"],
                "kind": "paper",
                "title": p.get("title") or schema.NR,
                "authors": schema.format_authors(p.get("authors") or [], max_n=3),
                "year": p.get("year"),
                "venue": p.get("venue"),
                "type": p.get("type"),
                "axes": p.get("axes") or [],
                "tags": p.get("tags") or [],
                "fiche": (p.get("status") or {}).get("fiche", "todo"),
                "url": (f"https://doi.org/{p['doi']}" if p.get("doi") else p.get("url")),
                "n_refs": len(p["refs"]),
                "n_bench": len(p["benchmarks"]),
            }

    def _resolve_refs(self, min_citers):
        """Rattache chaque référence à un papier du corpus ou à un groupe externe."""
        corpus_key = {}
        for p in self.papers:
            for k in ref_keys(p):
                corpus_key[k] = p["id"]

        group_of, group_info = {}, {}
        self.cites = defaultdict(set)      # paper_id → cibles (paper_id ou ext:<clé>)
        for p in self.papers:
            for r in p["refs"]:
                keys = ref_keys(r)
                if not keys:
                    continue
                target = next((corpus_key[k] for k in keys if k in corpus_key), None)
                if target is None:
                    target = next((group_of[k] for k in keys if k in group_of), None)
                    if target is None:
                        target = "ext:" + keys[0]
                        group_info[target] = {"title": r.get("title"), "year": r.get("year"),
                                              "keys": keys, "raw": r.get("raw")}
                    for k in keys:
                        group_of.setdefault(k, target)
                if target != p["id"]:
                    self.cites[p["id"]].add(target)

        citers = defaultdict(set)
        for pid, targets in self.cites.items():
            for t in targets:
                citers[t].add(pid)
        for gid, info in group_info.items():
            if len(citers[gid]) >= min_citers:
                self.nodes[gid] = {
                    "id": gid,
                    "kind": "external",
                    "title": info["title"] or info["raw"] or gid,
                    "year": info["year"],
                    "keys": info["keys"],
                    "citers": sorted(citers[gid]),
                }

    # -- liens

    def _build_links(self):
        ids_ = [p["id"] for p in self.papers]

        for src in ids_:
            for t in sorted(self.cites[src]):
                if t in self.nodes:
                    ext = self.nodes[t]["kind"] == "external"
                    self.links.append({"source": src, "target": t, "type": "citation",
                                       "weight": 1.0, "external": ext, "label": "cite"})

        for a, b in combinations(ids_, 2):
            ra, rb = self.cites[a], self.cites[b]
            shared = ra & rb
            if shared:
                self.links.append({"source": a, "target": b, "type": "coupling",
                                   "weight": len(shared) / (len(ra) * len(rb)) ** 0.5, "external": False,
                                   "label": f"{len(shared)} réf. partagée(s)"})
            ta = set(self.nodes[a]["axes"]) | set(self.nodes[a]["tags"])
            tb = set(self.nodes[b]["axes"]) | set(self.nodes[b]["tags"])
            if ta & tb:
                self.links.append({"source": a, "target": b, "type": "themes",
                                   "weight": len(ta & tb) / len(ta | tb), "external": False,
                                   "label": ", ".join(sorted(ta & tb))})

        texts = [p["text"] or (p.get("title") or "") for p in self.papers]
        if len(texts) >= 2 and any(t.strip() for t in texts):
            vec = TfidfVectorizer(stop_words="english", sublinear_tf=True,
                                  token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z0-9\-]+\b")
            try:
                self.tfidf = vec.fit_transform(texts)
            except ValueError:          # aucun terme exploitable
                self.tfidf = None
        if self.tfidf is not None:
            sim = (self.tfidf @ self.tfidf.T).toarray()
            for i, j in combinations(range(len(ids_)), 2):
                if sim[i, j] > 0:
                    self.links.append({"source": ids_[i], "target": ids_[j], "type": "text",
                                       "weight": float(sim[i, j]), "external": False,
                                       "label": f"cosinus {sim[i, j]:.2f}"})

    def links_for(self, types, text_threshold=0.0, show_external=False):
        return [l for l in self.links
                if l["type"] in types
                and (show_external or not l["external"])
                and (l["type"] != "text" or l["weight"] >= text_threshold)]

    def visible_nodes(self, show_external=False):
        return [n for n in self.nodes.values() if show_external or n["kind"] == "paper"]

    # -- positions

    def semantic_positions(self, show_external=False):
        """PCA 3D du TF-IDF ; externes au barycentre de leurs citants (+ jitter fixe)."""
        paper_ids = [p["id"] for p in self.papers]
        coords = np.zeros((len(paper_ids), 3))
        if self.tfidf is not None and len(paper_ids) >= 2:
            X = self.tfidf.toarray()
            X = X - X.mean(axis=0)
            U, S, _ = np.linalg.svd(X, full_matrices=False)
            k = min(3, len(S))
            coords[:, :k] = U[:, :k] * S[:k]
        pos = {pid: coords[i] for i, pid in enumerate(paper_ids)}
        pos = _normalize(pos)
        if show_external:
            for n in self.nodes.values():
                if n["kind"] == "external":
                    rng = random.Random(n["id"])
                    base = np.mean([pos[c] for c in n["citers"]], axis=0)
                    pos[n["id"]] = base + np.array([rng.uniform(-.08, .08) for _ in range(3)])
        return pos

    def force_positions(self, types, text_threshold=0.0, show_external=False):
        """Placement force-directed 3D sur les liens actifs (poids sommés par paire)."""
        g = nx.Graph()
        g.add_nodes_from(n["id"] for n in self.visible_nodes(show_external))
        for l in self.links_for(types, text_threshold, show_external):
            w = g.get_edge_data(l["source"], l["target"], {"weight": 0})["weight"]
            g.add_edge(l["source"], l["target"], weight=w + l["weight"])
        if not g.number_of_nodes():
            return {}
        # k élargi (défaut 1/√n) : sinon les papiers fortement couplés s'agglutinent
        k = 2.5 / g.number_of_nodes() ** 0.5
        pos = nx.spring_layout(g, dim=3, weight="weight", k=k, iterations=100, seed=42)
        return _normalize({k: np.asarray(v, dtype=float) for k, v in pos.items()})


def _normalize(pos):
    """Recentre et met à l'échelle dans [-1, 1]."""
    if not pos:
        return pos
    M = np.array(list(pos.values()))
    M = M - M.mean(axis=0)
    scale = np.abs(M).max() or 1.0
    return {k: M[i] / scale for i, k in enumerate(pos)}


def build(root, min_citers=2):
    return CorpusGraph(load_corpus(root), min_citers=min_citers)
