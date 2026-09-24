#!/usr/bin/env python3
"""Visualisation 3D du corpus : nuage de papiers, coloré par thème, relié par citations,
références partagées, similarité textuelle ou thèmes communs.

    .venv/bin/pip install -r requirements-viz.txt     # une fois
    .venv/bin/python bin/viz.py [--port 8050] [--debug]

puis ouvrir http://127.0.0.1:8050. Lecture seule : ne modifie aucun fichier de la base.
"""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import plotly.graph_objects as go  # noqa: E402
from dash import Dash, Input, Output, ctx, dcc, html, no_update  # noqa: E402

from lib import graph, schema  # noqa: E402

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

LINK_STYLE = {
    # traits pleins seulement : les tirets de Scatter3d se fragmentent en 3D
    "citation": {"label": "Citations", "color": "#e34948", "dash": "solid"},
    "coupling": {"label": "Références partagées", "color": "#4a3aa7", "dash": "solid"},
    "text": {"label": "Similarité textuelle (TF-IDF)", "color": "#2a78d6", "dash": "solid"},
    "themes": {"label": "Thèmes communs (axes + tags)", "color": "#1baf7a", "dash": "solid"},
}
WIDTHS = (1.5, 3.5, 6)       # faible / moyen / fort, relatif au poids max du type

COLOR_BY = {
    "axis": "Axe principal",
    "tag": "Tag principal",
    "year": "Année",
    "type": "Type de publication",
    "fiche": "Statut de la fiche",
}

G = graph.build(ROOT)


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


# ------------------------------------------------------------------- figure

def hover(n):
    if n["kind"] == "external":
        return (f"<b>{_wrap(n['title'])}</b><br>{n['year'] or schema.NR} · absent de la base"
                f"<br>cité par {len(n['citers'])} papiers du corpus")
    pre = " · <i>preprint</i>" if n["type"] == "preprint" else ""
    return (f"<b>{_wrap(n['title'])}</b><br>{n['authors']}, {n['year'] or schema.NR}{pre}"
            f"<br>axes : {', '.join(n['axes']) or '—'}<br>tags : {', '.join(n['tags']) or '—'}"
            f"<br>fiche : {n['fiche']}")


def _wrap(s, width=70):
    words, lines, cur = s.split(), [], ""
    for w in words:
        if cur and len(cur) + len(w) > width:
            lines.append(cur)
            cur = ""
        cur = f"{cur} {w}".strip()
    return "<br>".join(lines + [cur])


def link_traces(links, pos):
    traces = []
    for t in graph.LINK_TYPES:
        ls = [l for l in links if l["type"] == t and l["source"] in pos and l["target"] in pos]
        if not ls:
            continue
        wmax = max(l["weight"] for l in ls) or 1.0
        bins = [[], [], []]
        for l in ls:
            bins[min(2, int(3 * l["weight"] / wmax - 1e-9))].append(l)
        st = LINK_STYLE[t]
        for i, group in enumerate(bins):
            if not group:
                continue
            xs, ys, zs = [], [], []
            for l in group:
                a, b = pos[l["source"]], pos[l["target"]]
                xs += [a[0], b[0], None]
                ys += [a[1], b[1], None]
                zs += [a[2], b[2], None]
            traces.append(go.Scatter3d(
                x=xs, y=ys, z=zs, mode="lines", hoverinfo="skip",
                line={"color": st["color"], "width": WIDTHS[i], "dash": st["dash"]},
                opacity=0.35 + 0.2 * i,
                name=st["label"], legendgroup=f"link-{t}", showlegend=(i == max(
                    k for k, g in enumerate(bins) if g)),
                legendrank=900,
            ))
    return traces


def node_traces(nodes, pos, color_by, highlight):
    papers = [n for n in nodes if n["kind"] == "paper" and n["id"] in pos]
    externals = [n for n in nodes if n["kind"] == "external" and n["id"] in pos]
    traces = []

    def scatter(group, name, opacity, showlegend, **marker):
        return go.Scatter3d(
            x=[pos[n["id"]][0] for n in group], y=[pos[n["id"]][1] for n in group],
            z=[pos[n["id"]][2] for n in group],
            mode="markers+text" if opacity == 1 else "markers",
            text=[_short(n) for n in group] if opacity == 1 else None,
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
            group = [n for n in papers if highlighted(n, highlight) is hl]
            if group:
                traces.append(scatter(
                    group, "papiers", 1 if hl else 0.15, False,
                    color=[n["year"] or lo for n in group], colorscale=YEAR_SCALE,
                    cmin=lo, cmax=hi if hi > lo else lo + 1, symbol="circle",
                    colorbar={"title": "année", "thickness": 12, "len": 0.5} if hl else None,
                    showscale=hl))
    else:
        order = category_order(papers, color_by)
        styles = style_map(order)
        for cat in order:
            color, symbol = styles[cat]
            for hl in (True, False):
                group = [n for n in papers
                         if category(n, color_by) == cat and highlighted(n, highlight) is hl]
                if group:
                    traces.append(scatter(group, cat, 1 if hl else 0.15, hl,
                                          color=color, symbol=symbol))

    if externals:
        traces.append(go.Scatter3d(
            x=[pos[n["id"]][0] for n in externals], y=[pos[n["id"]][1] for n in externals],
            z=[pos[n["id"]][2] for n in externals], mode="markers",
            customdata=[n["id"] for n in externals],
            hovertext=[hover(n) for n in externals], hoverinfo="text",
            marker={"size": 4, "color": EXTERNAL_COLOR, "symbol": "circle"},
            opacity=0.7, name="référence externe co-citée",
        ))
    return traces


def _short(n):
    """Étiquette courte : 1er auteur + année."""
    first = n["authors"].split(",")[0].replace(" et al.", "").split()[-1] if n["authors"] != schema.NR else "?"
    return f"{first} {n['year'] or ''}".strip()


def make_figure(color_by, highlight, types, threshold, layout, show_ext):
    links = G.links_for(types, threshold, show_ext)
    if layout == "force":
        pos = G.force_positions(types, threshold, show_ext)
    else:
        pos = G.semantic_positions(show_ext)
    nodes = G.visible_nodes(show_ext)
    fig = go.Figure(link_traces(links, pos) + node_traces(nodes, pos, color_by, highlight))
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


# ------------------------------------------------------------------ détails

def details(node_id):
    n = G.nodes.get(node_id)
    if n is None:
        return html.P("Cliquer sur un point pour afficher le détail.", className="muted")
    if n["kind"] == "external":
        citers = [html.Li(G.nodes[c]["title"]) for c in n["citers"]]
        return [
            html.H3(n["title"]),
            html.P(f"{n['year'] or schema.NR} · clés : {', '.join(n['keys'])}", className="muted"),
            html.P(html.B("Absent de la base — candidat à /paper-add.")),
            html.P(f"Cité par {len(n['citers'])} papiers du corpus :"),
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
    return [
        html.H3(n["title"]),
        html.P(f"{n['authors']} · {n['year'] or schema.NR} · {n['venue'] or schema.NR}"),
        html.P(html.B("Preprint non relu par les pairs.")) if n["type"] == "preprint" else None,
        html.P([html.A(n["url"], href=n["url"], target="_blank")]) if n["url"] else None,
        html.P(f"Axes : {', '.join(n['axes']) or '—'}  ·  Tags : {', '.join(n['tags']) or '—'}"),
        html.P([f"Fiche : {n['fiche']}  ·  ", html.Code(f"papers/{n['id']}/fiche.md")]),
        html.P(f"{n['n_refs']} références extraites · {n['n_bench']} ligne(s) dans benchmarks.csv",
               className="muted"),
        html.H4(f"Liens ({len(rows)})"),
        html.Ul(link_items),
    ]


# ------------------------------------------------------------------------ app

def highlight_options():
    axes = sorted({a for n in G.visible_nodes() for a in n["axes"]})
    tags = sorted({t for n in G.visible_nodes() for t in n["tags"]})
    return ([{"label": f"axe : {a}", "value": f"axis:{a}"} for a in axes]
            + [{"label": f"tag : {t}", "value": f"tag:{t}"} for t in tags])


def control(label, component):
    return html.Div([html.Label(label, className="ctl-label"), component], className="ctl")


app = Dash(__name__, title="PaperDatabase — graphe 3D")
app.index_string = app.index_string.replace("</head>", """<style>
body { margin: 0; background: #fcfcfb; color: #1f1f1e; font-family: system-ui, sans-serif; font-size: 14px; }
.wrap { display: grid; grid-template-columns: 280px 1fr 360px; height: 100vh; }
.side { padding: 16px; overflow-y: auto; border-right: 1px solid #e4e3dd; }
.detail { padding: 16px; overflow-y: auto; border-left: 1px solid #e4e3dd; }
.ctl { margin-bottom: 18px; } .ctl-label { display: block; font-weight: 600; margin-bottom: 6px; }
.muted { color: #6b6a64; } h1 { font-size: 18px; margin: 0 0 4px; } h3 { font-size: 15px; }
.detail ul { padding-left: 18px; } .detail li { margin-bottom: 4px; }
button { padding: 6px 12px; border: 1px solid #c3c2b7; background: white; border-radius: 6px; cursor: pointer; }
@media (max-width: 1000px) { .wrap { grid-template-columns: 1fr; height: auto; } #graph { height: 70vh !important; } }
</style></head>""")

app.layout = html.Div(className="wrap", children=[
    html.Div(className="side", children=[
        html.H1("Corpus en 3D"),
        html.P(id="summary", className="muted"),
        control("Couleur par", dcc.Dropdown(
            id="color-by", value="axis", clearable=False,
            options=[{"label": v, "value": k} for k, v in COLOR_BY.items()])),
        control("Surligner", dcc.Dropdown(id="highlight", options=highlight_options(),
                                          placeholder="un axe ou un tag…")),
        control("Liens affichés", dcc.Checklist(
            id="link-types", value=["citation", "coupling"],
            options=[{"label": " " + LINK_STYLE[t]["label"], "value": t} for t in graph.LINK_TYPES],
            labelStyle={"display": "block"})),
        control("Seuil de similarité textuelle", dcc.Slider(
            id="threshold", min=0, max=1, step=0.05, value=0.25,
            marks={0: "0", 0.25: "0.25", 0.5: "0.5", 0.75: "0.75", 1: "1"})),
        control("Placement", dcc.RadioItems(
            id="layout", value="force",
            options=[{"label": " force (suit les liens cochés)", "value": "force"},
                     {"label": " sémantique (PCA du TF-IDF)", "value": "semantic"}],
            labelStyle={"display": "block"})),
        control("Références externes", dcc.Checklist(
            id="show-ext", value=[],
            options=[{"label": " afficher les travaux cités par ≥ 2 papiers", "value": "on"}])),
        html.Button("Recharger le corpus", id="reload"),
        html.P("Épaisseur d'un lien : poids relatif au lien le plus fort du même type.",
               className="muted", style={"marginTop": "18px"}),
    ]),
    dcc.Graph(id="graph", style={"height": "100vh"}, config={"displaylogo": False}),
    html.Div(id="detail", className="detail", children=details(None)),
])


def summary():
    papers = [n for n in G.nodes.values() if n["kind"] == "paper"]
    ext = len(G.nodes) - len(papers)
    cit = sum(1 for l in G.links if l["type"] == "citation" and not l["external"])
    return f"{len(papers)} papiers · {cit} citations internes · {ext} références externes co-citées"


@app.callback(Output("graph", "figure"), Output("summary", "children"),
              Output("highlight", "options"),
              Input("color-by", "value"), Input("highlight", "value"),
              Input("link-types", "value"), Input("threshold", "value"),
              Input("layout", "value"), Input("show-ext", "value"), Input("reload", "n_clicks"))
def update(color_by, hl, types, threshold, layout, show_ext, reload_clicks):
    global G
    if ctx.triggered_id == "reload":
        G = graph.build(ROOT)
    fig = make_figure(color_by, hl, types or [], threshold, layout, bool(show_ext))
    return fig, summary(), highlight_options()


@app.callback(Output("detail", "children"), Input("graph", "clickData"))
def show_detail(click):
    if not click:
        return no_update
    return details(click["points"][0].get("customdata"))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--port", type=int, default=8050)
    ap.add_argument("--debug", action="store_true")
    args = ap.parse_args()
    print(f"{summary()}\n→ http://127.0.0.1:{args.port}")
    app.run(host="127.0.0.1", port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()
