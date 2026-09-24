"""Graphe du corpus pour la visualisation 3D (bin/viz.py) : nœuds, liens, positions.

Couche données pure, sans Dash. Dépendances : requirements-viz.txt (numpy, scikit-learn,
networkx). Ne modifie aucun fichier de la base.

Types de liens :
  citation  — un papier cite un autre papier du corpus (dirigé)
  coupling  — références partagées (couplage bibliographique), poids = cosinus de Salton
              |A∩B| / √(|A|·|B|), moins écrasé que Jaccard par les surveys à 600 réfs
  text      — similarité cosinus TF-IDF sur le texte intégral
  themes    — axes et tags communs, poids = Jaccard

La similarité textuelle (liens `text`, placement sémantique) vient du TF-IDF, ou des
embeddings de lib/embed.py si sentence-transformers est installé (set_similarity).
"""
import csv
import json
import random
from collections import defaultdict
from itertools import combinations
from pathlib import Path

import networkx as nx
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from lib import refs, schema

LINK_TYPES = ("citation", "coupling", "text", "themes")
TEXT_KINDS = ("abstract", "section")


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


# ---------------------------------------------------------------------- graphe

class CorpusGraph:
    """nodes : dict id → nœud ; links : liste de {source, target, type, weight, label}.

    Les liens `text` sont calculés pour toutes les paires ; le seuil s'applique à
    l'affichage (links_for).
    """

    def __init__(self, papers, min_citers=2, root=None):
        self.papers = papers
        self.root = Path(root) if root else None
        self.nodes = {}
        self.links = []
        self.tfidf = None
        self.similarity = "tfidf"
        self._matrices = {}         # "tfidf" | "embed" → matrice lignes normalisées
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
                "arxiv_id": p.get("arxiv_id"),
                "doi": p.get("doi"),
                "n_refs": len(p["refs"]),
                "n_bench": len(p["benchmarks"]),
                "benchmarks": p["benchmarks"],
            }

    def _resolve_refs(self, min_citers):
        """Rattache chaque référence à un papier du corpus ou à un groupe externe (lib/refs.py).

        self.groups et self.citers couvrent toutes les références (vue généalogie) ; seules
        celles citées par ≥ min_citers papiers deviennent des nœuds du graphe 3D.
        """
        self.cites, self.groups = refs.group_refs(self.papers)   # paper_id → cibles
        self.citers = refs.citers_of(self.cites)
        ranked = sorted((gid for gid in self.groups if len(self.citers[gid]) >= min_citers),
                        key=lambda gid: (-len(self.citers[gid]), -(self.groups[gid]["year"] or 0),
                                         (self.groups[gid]["title"] or "").lower()))
        for rank, gid in enumerate(ranked, 1):
            self.nodes[gid] = self.external_node(gid)
            self.nodes[gid]["rank"] = rank     # même ordre que external_refs.csv

    def external_node(self, gid):
        info = self.groups[gid]
        return {
            "id": gid,
            "kind": "external",
            "title": info["title"] or info["raw"] or gid,
            "year": info["year"],
            "arxiv_id": info["arxiv_id"],
            "doi": info["doi"],
            "keys": info["keys"],
            "citers": sorted(self.citers[gid]),
            "rank": None,
        }

    def node(self, nid):
        """Nœud du graphe, ou nœud externe construit à la volée (référence citée une fois)."""
        if nid in self.nodes:
            return self.nodes[nid]
        if nid in self.groups:
            return self.external_node(nid)
        return None

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
            self._matrices["tfidf"] = self.tfidf.toarray()
        self._build_text_links()

    def _build_text_links(self):
        # nouvelle liste assignée d'un coup : les callbacks Dash lisent self.links en parallèle
        links = [l for l in self.links if l["type"] != "text"]
        X = self.text_matrix()
        if X is not None:
            ids_ = [p["id"] for p in self.papers]
            sim = X @ X.T
            for i, j in combinations(range(len(ids_)), 2):
                if sim[i, j] > 0:
                    links.append({"source": ids_[i], "target": ids_[j], "type": "text",
                                  "weight": float(min(sim[i, j], 1.0)), "external": False,
                                  "label": f"cosinus {sim[i, j]:.2f}"})
        self.links = links

    def text_matrix(self):
        """Matrice papiers × dimensions (lignes normalisées) de la similarité courante."""
        return self._matrices.get(self.similarity)

    def set_similarity(self, kind):
        """'tfidf' ou 'embed'. Retourne le mode effectif ('tfidf' si les embeddings sont
        indisponibles)."""
        if kind == "embed" and "embed" not in self._matrices:
            from lib import embed
            if not embed.available():
                kind = "tfidf"
            else:
                cache = self.root / ".cache" / "embeddings" if self.root else None
                self._matrices["embed"] = embed.embed_papers(self.papers, cache_dir=cache)
        if kind != self.similarity:
            self.similarity = kind
            self._build_text_links()
        return self.similarity

    # -- filtres

    def filter_ids(self, years=None, fiche=None, types=None):
        """Ids des papiers retenus par les filtres (None = pas de filtre). Un papier sans
        année passe le filtre d'années : l'absence de donnée n'est pas une exclusion."""
        keep = set()
        for n in self.nodes.values():
            if n["kind"] != "paper":
                continue
            if years and n["year"] is not None and not years[0] <= n["year"] <= years[1]:
                continue
            if fiche is not None and n["fiche"] not in fiche:
                continue
            if types is not None and (n["type"] or schema.NR) not in types:
                continue
            keep.add(n["id"])
        return keep

    def _visible(self, nid, show_external, keep):
        n = self.nodes[nid]
        if n["kind"] == "external":
            return show_external and (keep is None or any(c in keep for c in n["citers"]))
        return keep is None or nid in keep

    def links_for(self, types, text_threshold=0.0, show_external=False, keep=None):
        return [l for l in self.links
                if l["type"] in types
                and (show_external or not l["external"])
                and (l["type"] != "text" or l["weight"] >= text_threshold)
                and (keep is None or (self._visible(l["source"], show_external, keep)
                                      and self._visible(l["target"], show_external, keep)))]

    def visible_nodes(self, show_external=False, keep=None):
        return [n for n in self.nodes.values() if self._visible(n["id"], show_external, keep)]

    # -- positions

    def semantic_positions(self, show_external=False, keep=None):
        """PCA 3D de la similarité courante ; externes au barycentre de leurs citants
        (+ jitter fixe). Calculée sur tout le corpus : filtrer ne déplace pas les papiers."""
        paper_ids = [p["id"] for p in self.papers]
        coords = np.zeros((len(paper_ids), 3))
        X = self.text_matrix()
        if X is not None and len(paper_ids) >= 2:
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
        return {k: v for k, v in pos.items() if self._visible(k, show_external, keep)}

    def force_positions(self, types, text_threshold=0.0, show_external=False, keep=None):
        """Placement force-directed 3D sur les liens actifs (poids sommés par paire)."""
        g = nx.Graph()
        g.add_nodes_from(n["id"] for n in self.visible_nodes(show_external, keep))
        for l in self.links_for(types, text_threshold, show_external, keep):
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
    return CorpusGraph(load_corpus(root), min_citers=min_citers, root=root)
