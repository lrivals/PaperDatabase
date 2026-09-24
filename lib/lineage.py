"""Généalogie d'un papier ou d'un sujet : sous-graphe de citations placé sur une frise.

Couche données pure, sans Dash (utilisée par bin/viz.py, onglet « Généalogie »).

Arêtes orientées du travail cité vers le travail qui le cite (de l'ancien vers le récent) :
  citation — lue dans refs.jsonl d'un papier du corpus ;
  inferred — « suite probable », DÉDUITE : deux papiers du corpus du sous-graphe, sans
             citation entre eux, années croissantes et similarité textuelle ≥ seuil ; au
             plus une par papier (le prédécesseur le plus proche).

Une référence externe n'a pas de bibliographie connue : ses citations sortantes sont
inconnues, deux externes ne sont jamais reliés.
"""
import re
from collections import defaultdict

from lib import schema

ROLES = ("root", "match", "ancestor", "descendant", "intermediate")


def _citation_edges(G, ids):
    """(cité, citant) pour chaque citation lue dont les deux bouts sont dans ids."""
    return sorted((t, src) for src in ids if src in G.cites
                  for t in G.cites[src] if t in ids)


def from_paper(G, root, depth=2):
    """Ancêtres (ce que root cite, récursivement via les papiers du corpus) et descendants
    (ce qui le cite), jusqu'à `depth` sauts. Toutes les références directes de root sont
    incluses ; plus loin, seules les externes co-citées (nœuds du graphe 3D) le sont."""
    role = {root: "root"}
    frontier = {root}
    for d in range(depth):
        nxt = set()
        for pid in frontier:
            for t in G.cites.get(pid, ()):
                if t in role:
                    continue
                if t in G.groups and d > 0 and t not in G.nodes:
                    continue
                role[t] = "ancestor"
                if t not in G.groups:
                    nxt.add(t)
        frontier = nxt
    frontier = {root}
    for _ in range(depth):
        nxt = set()
        for pid in frontier:
            for c in G.citers.get(pid, ()):
                if c not in role:
                    role[c] = "descendant"
                    nxt.add(c)
        frontier = nxt
    return role


def matches_subject(G, subject):
    """Ids qui correspondent au sujet : « axis:x » / « tag:x » (papiers seulement) ou
    mot-clé / regex insensible à la casse sur les titres (papiers et références externes)
    et sur les axes et tags des papiers."""
    kind, _, value = subject.partition(":")
    if kind in ("axis", "tag") and value:
        field = "axes" if kind == "axis" else "tags"
        return {n["id"] for n in G.nodes.values() if n["kind"] == "paper" and value in n[field]}
    try:
        rx = re.compile(subject, re.I)
    except re.error:
        rx = re.compile(re.escape(subject), re.I)
    found = {n["id"] for n in G.nodes.values()
             if n["kind"] == "paper"
             and any(rx.search(t) for t in [n["title"] or ""] + n["axes"] + n["tags"])}
    found |= {gid for gid, g in G.groups.items()
              if any(rx.search(t) for t in (g["variants"] or [g["title"] or g["raw"] or ""]))}
    return found


def from_subject(G, subject, intermediates=True):
    """Nœuds du sujet + (option) papiers du corpus situés sur une chaîne de citations entre
    deux nœuds du sujet."""
    role = {m: "match" for m in matches_subject(G, subject)}
    if intermediates and role:
        # descendants[x] : ce que x cite, récursivement (papiers du corpus seulement)
        papers = [n["id"] for n in G.nodes.values() if n["kind"] == "paper"]
        reach = {p: _closure(p, lambda x: G.cites.get(x, ())) for p in papers}
        back = {p: _closure(p, lambda x: G.citers.get(x, ())) for p in papers}
        for p in papers:
            if p not in role and reach[p] & role.keys() and back[p] & role.keys():
                role[p] = "intermediate"
    return role


def _closure(start, step):
    seen, stack = set(), [start]
    while stack:
        for y in step(stack.pop()):
            if y not in seen:
                seen.add(y)
                stack.append(y)
    return seen


def inferred_edges(G, ids, threshold, cited):
    """Arêtes « suite probable » (déduites) entre papiers du corpus : au plus une par papier,
    vers le prédécesseur le plus similaire, parmi les paires sans citation lue."""
    X = G.text_matrix()
    if X is None or threshold <= 0:
        return []
    index = {p["id"]: i for i, p in enumerate(G.papers)}
    papers = [i for i in ids if i in index and G.nodes[i]["year"] is not None]
    linked = {frozenset(e) for e in cited}
    out = []
    for b in papers:
        best = None
        for a in papers:
            if G.nodes[a]["year"] >= G.nodes[b]["year"] or frozenset((a, b)) in linked:
                continue
            s = float(X[index[a]] @ X[index[b]])
            if s >= threshold and (best is None or s > best[0]):
                best = (s, a)
        if best:
            out.append((best[1], b, best[0]))
    return sorted(out)


def build(G, root=None, subject=None, depth=2, intermediates=True, infer_threshold=0.0):
    """Sous-graphe généalogique : {"nodes": {id: nœud + "role"}, "edges": [...],
    "pos": {id: (x, y)}, "ticks": [(x, libellé de colonne)]}."""
    if root:
        role = from_paper(G, root, depth)
    elif subject:
        role = from_subject(G, subject, intermediates)
    else:
        role = {}
    nodes = {}
    for nid, r in role.items():
        n = G.node(nid)
        if n is not None:
            nodes[nid] = {**n, "role": r}
    cited = _citation_edges(G, nodes)
    edges = [{"source": a, "target": b, "kind": "citation", "weight": 1.0} for a, b in cited]
    edges += [{"source": a, "target": b, "kind": "inferred", "weight": s}
              for a, b, s in inferred_edges(G, nodes, infer_threshold, cited)]
    pos, ticks = layout(nodes, edges)
    return {"nodes": nodes, "edges": edges, "pos": pos, "ticks": ticks}


def layout(nodes, edges, passes=6):
    """x = colonne de l'année (une colonne par année présente, « n/r » en premier ;
    échelle ordinale, pas proportionnelle au temps : une année aberrante issue du parsing
    n'écrase pas la frise), petit décalage alterné dans une colonne ; y = ordre par
    couches : tri par barycentre des voisins des colonnes précédentes puis suivantes
    (Sugiyama simplifié). Déterministe. Retourne (pos, ticks)."""
    if not nodes:
        return {}, []
    keys = sorted({n["year"] for n in nodes.values()}, key=lambda y: (y is not None, y or 0))
    index = {y: i for i, y in enumerate(keys)}
    col = {nid: index[n["year"]] for nid, n in nodes.items()}
    ticks = [(i, schema.NR if y is None else str(y)) for i, y in enumerate(keys)]

    columns = defaultdict(list)
    for nid in nodes:
        columns[col[nid]].append(nid)
    for c in columns.values():
        # papiers du corpus d'abord, puis par titre
        c.sort(key=lambda i: (nodes[i]["kind"] != "paper", (nodes[i]["title"] or "").lower(), i))

    preds, succs = defaultdict(list), defaultdict(list)
    for e in edges:
        a, b = e["source"], e["target"]
        if col[a] < col[b]:
            preds[b].append(a)
            succs[a].append(b)
        elif col[b] < col[a]:
            preds[a].append(b)
            succs[b].append(a)

    def ys():
        return {nid: i - (len(c) - 1) / 2 for c in columns.values() for i, nid in enumerate(c)}

    order = sorted(columns)
    for p in range(passes):
        y = ys()
        neigh, seq = (preds, order) if p % 2 == 0 else (succs, order[::-1])
        for x in seq:
            c = columns[x]
            key = {i: (sum(y[j] for j in neigh[i]) / len(neigh[i]) if neigh[i] else y[i])
                   for i in c}
            rank = {i: k for k, i in enumerate(c)}
            c.sort(key=lambda i: (key[i], rank[i]))
            y.update({nid: k - (len(c) - 1) / 2 for k, nid in enumerate(c)})

    y = ys()
    pos = {}
    for x, c in columns.items():
        for k, nid in enumerate(c):
            offset = 0.0 if len(c) == 1 else (0.12 if k % 2 else -0.12)
            pos[nid] = (x + offset, y[nid])
    return pos, ticks
