"""Figures et panneau de détail de bin/viz.py (graphe 3D, généalogie).

Fonctions pures sur un CorpusGraph (lib/graph.py) : aucune dépendance au serveur Dash, ce
qui permet de les tester sans le lancer (tests/test_viz.py). Lecture seule.
"""
import re
from pathlib import Path

import plotly.graph_objects as go
from dash import dcc, html

from lib import graph, schema

# Palette catégorielle à ordre fixe (dataviz, thème clair). Au-delà de 8 catégories, le
# reste est regroupé dans « autre ». Le symbole double la couleur : sur un nuage de points
# toutes les paires de couleurs se côtoient, la couleur seule ne suffit pas à distinguer.
PALETTE = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948"]
SYMBOLS = ["circle", "diamond", "square", "circle-open", "diamond-open", "square-open", "cross", "x"]
OTHER_COLOR = "#8a8a86"
EXTERNAL_COLOR = "#b5b4ad"
SURFACE = "#fcfcfb"
INK = "#1f1f1e"
INK_MUTED = "#6b6a64"
YEAR_SCALE = [[0, "#cde2fb"], [0.5, "#3987e5"], [1, "#0d366b"]]
DIM = 0.15              # opacité des papiers hors surlignage / sélection
DIM_LINK = 0.08         # opacité des liens hors surlignage / sélection

LINK_STYLE = {
    # traits pleins seulement : les tirets de Scatter3d se fragmentent en 3D
    "citation": {"label": "Citations", "color": "#e34948"},
    "coupling": {"label": "Références partagées", "color": "#4a3aa7"},
    "text": {"label": "Similarité textuelle", "color": "#2a78d6"},
    "themes": {"label": "Thèmes communs (axes + tags)", "color": "#1baf7a"},
}
WIDTHS = (1.5, 3.5, 6)       # faible / moyen / fort, relatif au poids max du type

COLOR_BY = {
    "axis": "Axe principal",
    "tag": "Tag principal",
    "year": "Année",
    "type": "Type de publication",
    "fiche": "Statut de la fiche",
}

BENCH_COLUMNS = (("model", "modèle"), ("platform", "plateforme"), ("quantization", "quantif."),
                 ("fps", "FPS"), ("latency_ms", "latence (ms)"), ("power_w", "W"), ("power_scope", "portée W"),
                 ("source_section", "source"))


# ------------------------------------------------------------------ couleurs

def category(node, color_by):
    if color_by == "axis":
        return node["axes"][0] if node["axes"] else "non classé"
    if color_by == "tag":
        return node["tags"][0] if node["tags"] else "sans tag"
    if color_by == "type":
        return node["type"] or schema.NR
    if color_by == "fiche":
        return node["fiche"]
    return None


def category_order(nodes, color_by):
    """Ordre fixe : axes dans l'ordre de schema.AXES, sinon par fréquence puis nom."""
    if color_by == "axis":
        return list(schema.AXES) + ["non classé"]
    if color_by == "fiche":
        return list(schema.FICHE_STATUS)
    if color_by == "type":
        return list(schema.TYPES) + [schema.NR]
    counts = {}
    for n in nodes:
        c = category(n, color_by)
        counts[c] = counts.get(c, 0) + 1
    return sorted(counts, key=lambda c: (-counts[c], c))


def style_map(order):
    """catégorie → (couleur, symbole) ; tout ce qui dépasse 8 tombe dans « autre »."""
    return {c: (PALETTE[i], SYMBOLS[i]) if i < len(PALETTE) else (OTHER_COLOR, "circle")
            for i, c in enumerate(order)}


def highlighted(node, highlight):
    if not highlight:
        return True
    kind, _, value = highlight.partition(":")
    return value in node.get("axes" if kind == "axis" else "tags", [])


def focus_set(nodes, links, highlight, selected):
    """Ids mis en avant (None = tout) : papiers surlignés, plus le papier sélectionné et
    ses voisins directs par les liens affichés."""
    focus = None
    if highlight:
        focus = {n["id"] for n in nodes if n["kind"] == "paper" and highlighted(n, highlight)}
    if selected and any(n["id"] == selected for n in nodes):
        near = {selected}
        for l in links:
            if selected in (l["source"], l["target"]):
                near |= {l["source"], l["target"]}
        focus = near if focus is None else focus | near
    return focus


# ------------------------------------------------------------------- textes

def hover(n):
    if n["kind"] == "external":
        return (f"<b>{wrap(n['title'])}</b><br>{n['year'] or schema.NR} · absent de la base"
                f"<br>cité par {len(n['citers'])} papier(s) du corpus"
                "<br><i>bibliographie inconnue : ses propres citations ne sont pas tracées</i>")
    pre = " · <i>preprint</i>" if n["type"] == "preprint" else ""
    return (f"<b>{wrap(n['title'])}</b><br>{n['authors']}, {n['year'] or schema.NR}{pre}"
            f"<br>axes : {', '.join(n['axes']) or '—'}<br>tags : {', '.join(n['tags']) or '—'}"
            f"<br>fiche : {n['fiche']}")


def wrap(s, width=70):
    words, lines, cur = (s or "").split(), [], ""
    for w in words:
        if cur and len(cur) + len(w) > width:
            lines.append(cur)
            cur = ""
        cur = f"{cur} {w}".strip()
    return "<br>".join(lines + [cur])


def short(n):
    """Étiquette courte : nom du 1er auteur + année (titre tronqué pour une externe)."""
    if n["kind"] == "external":
        t = n["title"] or "?"
        return (t[:24] + "…") if len(t) > 25 else t
    authors = n.get("authors") or ""
    first = authors.split(",")[0].replace(" et al.", "").split()
    name = first[-1] if first and authors != schema.NR else "?"
    return f"{name} {n['year'] or ''}".strip()


def option_label(n):
    return f"{short(n)} — {n['title']}" if n["kind"] == "paper" else f"[externe] {n['title']}"


# --------------------------------------------------------------- graphe 3D

def link_traces(links, pos, focus=None):
    traces = []
    for t in graph.LINK_TYPES:
        ls = [l for l in links if l["type"] == t and l["source"] in pos and l["target"] in pos]
        if not ls:
            continue
        wmax = max(l["weight"] for l in ls) or 1.0
        st = LINK_STYLE[t]
        bins = [[], [], []]
        dimmed = []
        for l in ls:
            if focus is not None and l["source"] not in focus and l["target"] not in focus:
                dimmed.append(l)
            else:
                bins[min(2, int(3 * l["weight"] / wmax - 1e-9))].append(l)
        shown = [i for i, g in enumerate(bins) if g]
        for i in shown:
            traces.append(_segments3d(bins[i], pos, st["color"], WIDTHS[i], 0.35 + 0.2 * i,
                                      st["label"], f"link-{t}", i == shown[-1]))
        if dimmed:
            traces.append(_segments3d(dimmed, pos, st["color"], WIDTHS[0], DIM_LINK,
                                      st["label"], f"link-{t}", not shown))
    return traces


def _segments3d(group, pos, color, width, opacity, name, legendgroup, showlegend):
    xs, ys, zs = [], [], []
    for l in group:
        a, b = pos[l["source"]], pos[l["target"]]
        xs += [a[0], b[0], None]
        ys += [a[1], b[1], None]
        zs += [a[2], b[2], None]
    return go.Scatter3d(x=xs, y=ys, z=zs, mode="lines", hoverinfo="skip",
                        line={"color": color, "width": width}, opacity=opacity,
                        name=name, legendgroup=legendgroup, showlegend=showlegend,
                        legendrank=900)


def node_traces(nodes, pos, color_by, focus=None, labels=True):
    papers = [n for n in nodes if n["kind"] == "paper" and n["id"] in pos]
    externals = [n for n in nodes if n["kind"] == "external" and n["id"] in pos]
    traces = []

    def on(n):
        return focus is None or n["id"] in focus

    def scatter(group, name, opacity, showlegend, **marker):
        text = labels and opacity == 1
        return go.Scatter3d(
            x=[pos[n["id"]][0] for n in group], y=[pos[n["id"]][1] for n in group],
            z=[pos[n["id"]][2] for n in group],
            mode="markers+text" if text else "markers",
            text=[short(n) for n in group] if text else None,
            textposition="top center", textfont={"size": 10, "color": INK_MUTED},
            customdata=[n["id"] for n in group],
            hovertext=[hover(n) for n in group], hoverinfo="text",
            marker={"size": 9, "line": {"width": 2, "color": SURFACE}, **marker},
            opacity=opacity, name=name, legendgroup=name, showlegend=showlegend,
        )

    if color_by == "year":
        years = [n["year"] for n in papers if n["year"]]
        lo, hi = (min(years), max(years)) if years else (0, 1)
        for hl in (True, False):
            group = [n for n in papers if on(n) is hl]
            if group:
                traces.append(scatter(
                    group, "papiers", 1 if hl else DIM, False,
                    color=[n["year"] or lo for n in group], colorscale=YEAR_SCALE,
                    cmin=lo, cmax=hi if hi > lo else lo + 1, symbol="circle",
                    colorbar={"title": {"text": "année"}, "thickness": 12, "len": 0.5}
                    if hl else None,
                    showscale=hl))
    else:
        order = category_order(papers, color_by)
        styles = style_map(order)
        for cat in order:
            color, symbol = styles[cat]
            for hl in (True, False):
                group = [n for n in papers if category(n, color_by) == cat and on(n) is hl]
                if group:
                    traces.append(scatter(group, cat, 1 if hl else DIM, hl,
                                          color=color, symbol=symbol))

    for hl in (True, False):
        group = [n for n in externals if on(n) is hl]
        if group:
            traces.append(go.Scatter3d(
                x=[pos[n["id"]][0] for n in group], y=[pos[n["id"]][1] for n in group],
                z=[pos[n["id"]][2] for n in group], mode="markers",
                customdata=[n["id"] for n in group],
                hovertext=[hover(n) for n in group], hoverinfo="text",
                marker={"size": 4, "color": EXTERNAL_COLOR, "symbol": "circle"},
                opacity=0.7 if hl else DIM, name="référence externe co-citée",
                legendgroup="external", showlegend=hl,
            ))
    return traces


def selection_trace(node, p):
    """Anneau sombre autour du papier sélectionné."""
    return go.Scatter3d(x=[p[0]], y=[p[1]], z=[p[2]], mode="markers", hoverinfo="skip",
                        marker={"size": 16, "symbol": "circle-open", "color": INK,
                                "line": {"width": 3, "color": INK}},
                        name="sélection", showlegend=False)


def make_figure(G, color_by="axis", highlight=None, types=("citation", "coupling"),
                threshold=0.25, layout="force", show_ext=False, keep=None, selected=None,
                labels=True):
    links = G.links_for(types, threshold, show_ext, keep)
    if layout == "force":
        pos = G.force_positions(types, threshold, show_ext, keep)
    else:
        pos = G.semantic_positions(show_ext, keep)
    nodes = G.visible_nodes(show_ext, keep)
    focus = focus_set(nodes, links, highlight, selected)
    traces = link_traces(links, pos, focus) + node_traces(nodes, pos, color_by, focus, labels)
    if selected in pos:
        traces.append(selection_trace(G.nodes[selected], pos[selected]))
    fig = go.Figure(traces)
    axis = {"showgrid": False, "zeroline": False, "showticklabels": False,
            "showbackground": False, "title": ""}
    fig.update_layout(
        paper_bgcolor=SURFACE, font={"color": INK, "family": "system-ui, sans-serif"},
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        scene={"xaxis": axis, "yaxis": axis, "zaxis": axis, "bgcolor": SURFACE},
        legend={"title": {"text": COLOR_BY[color_by]}, "itemsizing": "constant",
                "bgcolor": "rgba(252,252,251,0.85)", "x": 0, "y": 1},
        hoverlabel={"bgcolor": "white", "font": {"color": INK}},
        uirevision=layout,      # garde l'angle de caméra tant que le placement ne change pas
    )
    return fig


# -------------------------------------------------------------- généalogie

LINEAGE_STYLE = {
    "root": {"label": "racine", "symbol": "star", "size": 20},
    "paper": {"label": "papier du corpus", "symbol": "circle", "size": 13},
    "intermediate": {"label": "papier intermédiaire (hors sujet)", "symbol": "diamond", "size": 12},
    "external": {"label": "référence externe (bibliographie inconnue)", "symbol": "circle-open",
                 "size": 10},
}
CITATION_COLOR = "#e34948"
INFERRED_COLOR = "#2a78d6"


def _lineage_kind(n):
    if n["role"] == "root":
        return "root"
    if n["kind"] == "external":
        return "external"
    return "intermediate" if n["role"] == "intermediate" else "paper"


def lineage_figure(L, selected=None, labels=True):
    """Frise : x = année, flèches du travail cité vers le travail qui le cite."""
    nodes, pos = L["nodes"], L["pos"]
    fig = go.Figure()
    if not nodes:
        fig.add_annotation(text="Choisir un papier racine ou un sujet.", showarrow=False,
                           font={"color": INK_MUTED, "size": 14}, x=0.5, y=0.5,
                           xref="paper", yref="paper")
        fig.update_layout(paper_bgcolor=SURFACE, plot_bgcolor=SURFACE,
                          xaxis={"visible": False}, yaxis={"visible": False})
        return fig

    inferred = [e for e in L["edges"] if e["kind"] == "inferred"]
    if inferred:
        xs, ys = [], []
        for e in inferred:
            (ax, ay), (bx, by) = pos[e["source"]], pos[e["target"]]
            xs += [ax, bx, None]
            ys += [ay, by, None]
        fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", hoverinfo="skip",
                                 line={"color": INFERRED_COLOR, "width": 1.5, "dash": "dash"},
                                 name="suite probable (déduite : similarité textuelle)"))
    citations = [e for e in L["edges"] if e["kind"] == "citation"]
    if citations:     # entrée de légende pour les flèches (annotations)
        fig.add_trace(go.Scatter(x=[None], y=[None], mode="lines",
                                 line={"color": CITATION_COLOR, "width": 1.5},
                                 name="citation lue (cité → citant)"))
    for e in L["edges"]:
        (ax, ay), (bx, by) = pos[e["source"]], pos[e["target"]]
        if e["kind"] == "inferred":        # pointe seule, le trait est en tirets
            ax, ay = bx - 0.25 * (bx - ax), by - 0.25 * (by - ay)
        fig.add_annotation(x=bx, y=by, ax=ax, ay=ay, xref="x", yref="y", axref="x", ayref="y",
                           text="", showarrow=True, arrowhead=2, arrowsize=1.1, arrowwidth=1.3,
                           arrowcolor=CITATION_COLOR if e["kind"] == "citation" else INFERRED_COLOR,
                           opacity=0.7, standoff=7, startstandoff=0 if e["kind"] == "inferred" else 6)

    order = graph_axis_order(nodes)
    styles = style_map(order)
    many = len(nodes) > 25       # au-delà, les externes ne sont nommées qu'au survol
    for kind, st in LINEAGE_STYLE.items():
        group = [n for n in nodes.values() if _lineage_kind(n) == kind]
        if not group:
            continue
        if kind == "external":
            color = [EXTERNAL_COLOR] * len(group)
        else:
            color = [styles[category(n, "axis")][0] for n in group]
        text = [("" if (many and n["kind"] == "external") else short(n)) for n in group]
        fig.add_trace(go.Scatter(
            x=[pos[n["id"]][0] for n in group], y=[pos[n["id"]][1] for n in group],
            mode="markers+text" if labels else "markers",
            text=text if labels else None, textposition="top center",
            textfont={"size": 10, "color": INK_MUTED},
            customdata=[n["id"] for n in group],
            hovertext=[hover(n) + f"<br>rôle : {n['role']}" for n in group], hoverinfo="text",
            marker={"size": st["size"], "symbol": st["symbol"], "color": color,
                    "line": {"width": 1.5 if kind == "external" else 1,
                             "color": EXTERNAL_COLOR if kind == "external" else SURFACE}},
            name=st["label"],
        ))
    if selected in pos:
        x, y = pos[selected]
        fig.add_trace(go.Scatter(x=[x], y=[y], mode="markers", hoverinfo="skip",
                                 showlegend=False,
                                 marker={"size": 26, "symbol": "circle-open", "color": INK,
                                         "line": {"width": 2.5, "color": INK}}))

    ticks = L["ticks"]
    tallest = max(sum(1 for p in pos.values() if round(p[0]) == x) for x, _ in ticks)
    fig.update_layout(
        paper_bgcolor=SURFACE, plot_bgcolor=SURFACE, height=max(520, 120 + 56 * tallest),
        font={"color": INK, "family": "system-ui, sans-serif"},
        margin={"l": 20, "r": 20, "t": 60, "b": 50},
        xaxis={"tickvals": [x for x, _ in ticks], "ticktext": [t for _, t in ticks],
               "range": [-0.5, len(ticks) - 0.2], "showgrid": True, "gridcolor": "#ecebe6",
               "zeroline": False,
               "title": {"text": "année de parution (une colonne par année présente, "
                                 "échelle non proportionnelle)"}},
        yaxis={"visible": False},
        legend={"orientation": "h", "y": 1.01, "yanchor": "bottom", "x": 0,
                "bgcolor": "rgba(252,252,251,0.85)"},
        hoverlabel={"bgcolor": "white", "font": {"color": INK}},
    )
    return fig


def graph_axis_order(nodes):
    return category_order([n for n in nodes.values() if n["kind"] == "paper"], "axis")


# ------------------------------------------------------------------ détails

def read_fiche(root, pid):
    """Contenu de fiche.md sans le front-matter YAML, ou None."""
    path = Path(root) / "papers" / pid / "fiche.md"
    if not path.exists():
        return None
    text = path.read_text()
    return re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S).strip()


def bench_table(rows):
    head = html.Tr([html.Th(label) for _, label in BENCH_COLUMNS])
    body = []
    for r in rows:
        low = r.get("confidence") == "low"
        cells = [html.Td(r.get(k) or schema.NR) for k, _ in BENCH_COLUMNS]
        body.append(html.Tr(cells, className="low" if low else None,
                            title="confidence = low : chiffre à vérifier" if low else None))
    return html.Table([html.Thead(head), html.Tbody(body)], className="bench")


def external_links(n):
    links = []
    if n.get("arxiv_id"):
        links.append(html.A(f"arXiv {n['arxiv_id']}", href=f"https://arxiv.org/abs/{n['arxiv_id']}",
                            target="_blank"))
    if n.get("doi"):
        links.append(html.A(f"DOI {n['doi']}", href=f"https://doi.org/{n['doi']}", target="_blank"))
    if not links:
        q = re.sub(r"\s+", "+", (n["title"] or "").strip())
        links.append(html.A("chercher sur Google Scholar",
                            href=f"https://scholar.google.com/scholar?q={q}", target="_blank"))
    out = []
    for a in links:
        out += [a, " · "]
    return out[:-1]


def details(G, node_id, root):
    n = G.node(node_id) if node_id else None
    if n is None:
        return html.P("Cliquer sur un point ou chercher un papier pour afficher le détail.",
                      className="muted")
    if n["kind"] == "external":
        ident = n.get("arxiv_id") or n.get("doi")
        citers = [html.Li(G.nodes[c]["title"]) for c in n["citers"]]
        rank = (f"rang {n['rank']} dans external_refs.csv" if n.get("rank")
                else "cité une seule fois : absent d'external_refs.csv")
        return [
            html.H3(n["title"]),
            html.P(f"{n['year'] or schema.NR} · {rank}", className="muted"),
            html.P(external_links(n)),
            html.P(html.B("Absent de la base — candidat à /paper-add.")),
            html.P(html.Code(f"/paper-add {ident}")) if ident else
            html.P("Pas d'identifiant extrait : retrouver l'arXiv ou le DOI avant /paper-add.",
                   className="muted"),
            html.P("Titre issu du parsing des bibliographies : à vérifier avant de le citer.",
                   className="muted"),
            html.P(f"Cité par {len(n['citers'])} papier(s) du corpus :"),
            html.Ul(citers),
        ]

    rows = []
    for l in G.links:
        if node_id not in (l["source"], l["target"]):
            continue
        other = l["target"] if l["source"] == node_id else l["source"]
        if l["type"] == "citation":
            verb = "cite" if l["source"] == node_id else "est cité par"
        else:
            verb = LINK_STYLE[l["type"]]["label"].lower()
        rows.append((l["type"], -l["weight"], verb, G.nodes[other]["title"], l["label"]))
    rows.sort()
    link_items = [html.Li([html.Span(f"{verb} ", className="muted"), title,
                           html.Span(f" — {label}", className="muted")])
                  for _, _, verb, title, label in rows[:40]]

    fiche = read_fiche(root, node_id) if n["fiche"] == "done" else None
    bench = n.get("benchmarks") or []
    low = sum(1 for r in bench if r.get("confidence") == "low")
    return [
        html.H3(n["title"]),
        html.P(f"{n['authors']} · {n['year'] or schema.NR} · {n['venue'] or schema.NR}"),
        html.P(html.B("Preprint non relu par les pairs.")) if n["type"] == "preprint" else None,
        html.P([html.A(n["url"], href=n["url"], target="_blank")]) if n["url"] else None,
        html.P(f"Axes : {', '.join(n['axes']) or '—'}  ·  Tags : {', '.join(n['tags']) or '—'}"),
        html.P([f"Fiche : {n['fiche']}  ·  ", html.Code(f"papers/{n['id']}/fiche.md")]),
        html.Details([html.Summary("Fiche de lecture"), dcc.Markdown(fiche, className="fiche")],
                     open=False) if fiche else
        html.P("Fiche non rédigée (/paper-fiche).", className="muted"),
        html.H4(f"Benchmarks ({len(bench)})"),
        (html.Div([bench_table(bench),
                   html.P(f"{low} ligne(s) en confidence low (surlignées) : à vérifier.",
                          className="muted") if low else None], className="bench-wrap")
         if bench else html.P("Aucune ligne dans benchmarks.csv.", className="muted")),
        html.P(f"{n['n_refs']} références extraites", className="muted"),
        html.H4(f"Liens ({len(rows)})"),
        html.Ul(link_items),
    ]
