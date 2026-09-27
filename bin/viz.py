#!/usr/bin/env python3
"""Visualisation du corpus : graphe 3D (papiers colorés par thème, reliés par citations,
références partagées, similarité textuelle ou thèmes communs), généalogie (frise des
citations d'un papier ou d'un sujet) et gestion des bases (onglet Bases : sélecteur, profil,
recherche d'articles dans les autres bases, import, création).

    .venv/bin/pip install -r requirements-viz.txt     # une fois
    .venv/bin/pip install -r requirements-embed.txt   # optionnel : similarité par embeddings
    .venv/bin/python bin/viz.py [--port 8050] [--debug]

puis ouvrir http://127.0.0.1:8050. Les vues 3D et Généalogie sont en lecture seule (seul le
cache des embeddings est écrit, dans .cache/). L'onglet Bases écrit seulement sur action
explicite : « Créer la base » et « Importer la sélection » (comme `pdb base new` / `import`).
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import plotly.graph_objects as go  # noqa: E402
from dash import Dash, Input, Output, State, ctx, dcc, html, no_update  # noqa: E402

from lib import base, bases, embed, graph, lineage, registry, schema, vizbases, vizfig, xbase  # noqa: E402
from lib.vizfig import COLOR_BY, LINK_STYLE  # noqa: E402

ROOT = base.ROOT
G = graph.build(ROOT)
vizfig.AXES_ORDER = list(base.load_config(ROOT)["axes"])
EMBED_OK = embed.available()


def set_base(root):
    """Change la base affichée (application locale, mono-utilisateur : état global)."""
    global ROOT, G
    ROOT = Path(root).resolve()
    vizfig.AXES_ORDER = list(base.load_config(ROOT)["axes"])
    G = graph.build(ROOT)


def base_title():
    name = registry.name_of(ROOT)
    return f"{base.load_config(ROOT)['name']}" + (f" ({name})" if name else "")


def year_bounds():
    years = [n["year"] for n in G.nodes.values() if n["kind"] == "paper" and n["year"]]
    return (min(years), max(years)) if years else (2000, 2030)


def year_marks(lo, hi):
    step = max(1, (hi - lo) // 4)
    return {y: str(y) for y in range(lo, hi + 1, step)} | {hi: str(hi)}


def highlight_options():
    axes = sorted({a for n in G.visible_nodes() for a in n["axes"]})
    tags = sorted({t for n in G.visible_nodes() for t in n["tags"]})
    return ([{"label": f"axe : {a}", "value": f"axis:{a}"} for a in axes]
            + [{"label": f"tag : {t}", "value": f"tag:{t}"} for t in tags])


def paper_options():
    papers = sorted((n for n in G.nodes.values() if n["kind"] == "paper"),
                    key=lambda n: (n["year"] or 0, n["title"]))
    return [{"label": vizfig.option_label(n), "value": n["id"]} for n in papers]


def search_options(show_ext):
    ext = sorted((n for n in G.nodes.values() if n["kind"] == "external"),
                 key=lambda n: n["title"].lower())
    return paper_options() + ([{"label": vizfig.option_label(n), "value": n["id"]} for n in ext]
                              if show_ext else [])


def summary():
    papers = [n for n in G.nodes.values() if n["kind"] == "paper"]
    ext = len(G.nodes) - len(papers)
    cit = sum(1 for l in G.links if l["type"] == "citation" and not l["external"])
    return f"{len(papers)} papiers · {cit} citations internes · {ext} références externes co-citées"


def control(label, component):
    return html.Div([html.Label(label, className="ctl-label"), component], className="ctl")


def radio(id_, value, options):
    return dcc.RadioItems(id=id_, value=value, options=options, labelStyle={"display": "block"})


LO, HI = year_bounds()
TYPES_PRESENT = [t for t in (*schema.TYPES, schema.NR)
                 if any((n["type"] or schema.NR) == t for n in G.nodes.values() if n["kind"] == "paper")]

app = Dash(__name__, title="PaperDatabase — bases et corpus")
app.index_string = app.index_string.replace("</head>", """<style>
body { margin: 0; background: #fcfcfb; color: #1f1f1e; font-family: system-ui, sans-serif; font-size: 14px; }
.wrap { display: grid; grid-template-columns: 290px 1fr 380px; height: 100vh; }
.side { padding: 16px; overflow-y: auto; border-right: 1px solid #e4e3dd; }
.center { display: flex; flex-direction: column; min-width: 0; overflow: auto; }
.detail { padding: 16px; overflow-y: auto; border-left: 1px solid #e4e3dd; }
.ctl { margin-bottom: 16px; } .ctl-label { display: block; font-weight: 600; margin-bottom: 6px; }
.group { font-size: 12px; text-transform: uppercase; letter-spacing: .05em; color: #6b6a64; margin: 22px 0 10px; }
.muted { color: #6b6a64; } h1 { font-size: 18px; margin: 0 0 4px; } h3 { font-size: 15px; } h4 { margin: 16px 0 6px; }
.detail ul { padding-left: 18px; } .detail li { margin-bottom: 4px; }
.fiche { font-size: 13px; border-left: 3px solid #e4e3dd; padding-left: 10px; }
.fiche h1 { font-size: 15px; } .fiche h2 { font-size: 14px; }
details summary { cursor: pointer; font-weight: 600; margin: 8px 0; }
.bench-wrap { overflow-x: auto; } table.bench { border-collapse: collapse; font-size: 12px; }
.bench th, .bench td { border-bottom: 1px solid #e4e3dd; padding: 3px 6px; text-align: left; vertical-align: top; }
.bench tr.low td { background: #fdf0d5; }
.lin-bar { display: flex; flex-wrap: wrap; gap: 16px; padding: 12px 16px; border-bottom: 1px solid #e4e3dd; align-items: flex-end; }
.lin-bar .ctl { margin: 0; min-width: 160px; }
button { padding: 6px 12px; border: 1px solid #c3c2b7; background: white; border-radius: 6px; cursor: pointer; margin: 0 6px 6px 0; }
button:disabled { opacity: .45; cursor: default; }
input[type=text] { padding: 6px 8px; border: 1px solid #c3c2b7; border-radius: 4px; width: 220px; }
.bases-tab { padding: 8px 20px 40px; } .bases-tab h3 { margin: 22px 0 8px; }
.form-row { display: flex; flex-wrap: wrap; gap: 16px; margin-bottom: 10px; }
.form-row label, .bases-tab > div > label { display: flex; flex-direction: column; gap: 4px; font-weight: 600; }
.notice { background: #fdf0d5; border-left: 3px solid #d9a441; padding: 8px 10px; margin: 8px 0; }
.ok { color: #2f6b3a; } .err { color: #a3312a; white-space: pre-line; }
@media (max-width: 1100px) { .wrap { grid-template-columns: 1fr; height: auto; } #graph { height: 70vh !important; } }
</style></head>""")

embed_label = ("embeddings (sentence-transformers)" if EMBED_OK
               else "embeddings — pip install -r requirements-embed.txt")

sidebar = html.Div(className="side", children=[
    control("Base", dcc.Dropdown(id="base-select", options=vizbases.base_options(ROOT),
                                 value=str(ROOT), clearable=False, optionHeight=50)),
    html.H1(base_title(), id="corpus-title"),
    html.P(id="summary", className="muted"),
    control("Rechercher", dcc.Dropdown(id="search", options=search_options(False),
                                       placeholder="titre ou auteur…", optionHeight=50)),

    html.Div("Graphe 3D", className="group"),
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
    control("Placement", radio("layout", "force", [
        {"label": " force (suit les liens cochés)", "value": "force"},
        {"label": " sémantique (PCA de la similarité)", "value": "semantic"}])),
    control("Affichage", dcc.Checklist(
        id="show-ext", value=[],
        options=[{"label": " références externes citées par ≥ 2 papiers", "value": "on"}])),

    html.Div("Filtres (graphe 3D)", className="group"),
    control("Années", dcc.RangeSlider(id="years", min=LO, max=HI, step=1, value=[LO, HI],
                                      marks=year_marks(LO, HI),
                                      tooltip={"placement": "bottom"})),
    control("Fiche", dcc.Checklist(id="fiche-filter", value=list(schema.FICHE_STATUS), inline=True,
                                   options=[{"label": f" {s} ", "value": s}
                                            for s in schema.FICHE_STATUS])),
    control("Type", dcc.Checklist(id="type-filter", value=TYPES_PRESENT,
                                  options=[{"label": f" {t}", "value": t} for t in TYPES_PRESENT],
                                  labelStyle={"display": "block"})),

    html.Div("Commun aux deux vues", className="group"),
    control("Similarité textuelle", radio("similarity", "tfidf", [
        {"label": " TF-IDF (lexicale)", "value": "tfidf"},
        {"label": " " + embed_label, "value": "embed", "disabled": not EMBED_OK}])),
    control("Étiquettes", dcc.Checklist(id="labels", value=["on"],
                                        options=[{"label": " afficher", "value": "on"}])),
    html.Button("Recharger le corpus", id="reload"),
    html.Button("Exporter la vue (HTML)", id="export"),
    dcc.Download(id="download"),
    html.P("Épaisseur d'un lien : poids relatif au lien le plus fort du même type.",
           className="muted", style={"marginTop": "12px"}),
])

lineage_bar = html.Div(className="lin-bar", children=[
    control("Point de départ", dcc.RadioItems(
        id="lin-mode", value="subject", inline=True,
        options=[{"label": " sujet ", "value": "subject"}, {"label": " papier", "value": "paper"}])),
    control("Sujet (mot-clé, regex, axis:x, tag:x)",
            dcc.Input(id="lin-subject", type="text", value="hls4ml", debounce=True,
                      placeholder="yolo|you only look once")),
    control("Papier racine", dcc.Dropdown(id="lin-root", options=paper_options(),
                                          placeholder="choisir…", style={"width": "320px"})),
    control("Profondeur (papier)", dcc.Slider(id="lin-depth", min=1, max=3, step=1, value=2,
                                              marks={1: "1", 2: "2", 3: "3"})),
    control("Options", dcc.Checklist(
        id="lin-inter", value=["on"],
        options=[{"label": " intermédiaires (sujet)", "value": "on"}])),
    control("Suite probable (déduite) : seuil", dcc.Slider(
        id="lin-infer", min=0, max=0.8, step=0.05, value=0,
        marks={0: "off", 0.2: "0.2", 0.4: "0.4", 0.6: "0.6", 0.8: "0.8"})),
    html.P(id="lin-summary", className="muted", style={"margin": 0, "flexBasis": "100%"}),
])

app.layout = html.Div(className="wrap", children=[
    sidebar,
    html.Div(className="center", children=[
        dcc.Tabs(id="tabs", value="3d", children=[
            dcc.Tab(label="Graphe 3D", value="3d", children=[
                dcc.Loading(dcc.Graph(id="graph", style={"height": "calc(100vh - 50px)"},
                                      config={"displaylogo": False}))]),
            dcc.Tab(label="Généalogie", value="lineage", children=[
                lineage_bar,
                dcc.Loading(dcc.Graph(id="lineage-graph", config={"displaylogo": False}))]),
            dcc.Tab(label="Bases", value="bases", children=[vizbases.layout()]),
        ]),
    ]),
    html.Div(className="detail", children=[
        html.Button("Voir sa généalogie", id="to-lineage", disabled=True),
        html.Div(id="detail", children=vizfig.details(G, None, ROOT)),
    ]),
    dcc.Store(id="selected"),
    dcc.Store(id="version", data=0),
    dcc.Store(id="imported", data=0),      # incrémenté après un import : recharge le corpus
    dcc.Store(id="registry-rev", data=0),  # incrémenté après une création : recharge la liste
    dcc.Store(id="scan-data", data=[]),
])


# ----------------------------------------------------------------- callbacks
# Seul le callback `corpus` modifie G (rechargement, mode de similarité) ; les autres
# dépendent de `version` et ne font que lire.

@app.callback(Output("version", "data"), Output("similarity", "value"),
              Output("corpus-title", "children"), Output("selected", "data", allow_duplicate=True),
              Input("reload", "n_clicks"), Input("similarity", "value"), Input("base-select", "value"),
              Input("imported", "data"), State("version", "data"), prevent_initial_call="initial_duplicate")
def corpus(_, similarity, root, _imported, version):
    global G
    selected = no_update
    if ctx.triggered_id == "base-select" and root and Path(root).resolve() != ROOT:
        set_base(root)
        selected = None
    elif ctx.triggered_id in ("reload", "imported"):
        G = graph.build(ROOT)
    effective = G.set_similarity(similarity)
    return (version or 0) + 1, effective, base_title(), selected


@app.callback(Output("selected", "data"), Output("search", "value"),
              Input("graph", "clickData"), Input("lineage-graph", "clickData"),
              Input("search", "value"), prevent_initial_call=True)
def select(click3d, click_lin, search):
    if ctx.triggered_id == "search":
        return search, no_update
    click = click3d if ctx.triggered_id == "graph" else click_lin
    nid = (click or {}).get("points", [{}])[0].get("customdata")
    if not nid:
        return no_update, no_update
    return nid, nid


def _filters(years, bounds, fiche, types):
    """keep (ids retenus) ou None si aucun filtre n'est actif."""
    full_years = list(years or []) == list(bounds)
    all_fiche = set(fiche or []) >= set(schema.FICHE_STATUS)
    all_types = set(types or []) >= set(TYPES_PRESENT)
    if full_years and all_fiche and all_types:
        return None
    return G.filter_ids(None if full_years else years, None if all_fiche else set(fiche or []),
                        None if all_types else set(types or []))


@app.callback(Output("graph", "figure"), Output("summary", "children"),
              Output("highlight", "options"), Output("highlight", "value"),
              Output("search", "options"), Output("lin-root", "options"),
              Output("years", "min"), Output("years", "max"), Output("years", "marks"),
              Output("years", "value"),
              Input("color-by", "value"), Input("highlight", "value"),
              Input("link-types", "value"), Input("threshold", "value"),
              Input("layout", "value"), Input("show-ext", "value"), Input("labels", "value"),
              Input("years", "value"), Input("fiche-filter", "value"), Input("type-filter", "value"),
              Input("selected", "data"), Input("version", "data"),
              State("years", "min"), State("years", "max"))
def update(color_by, hl, types, threshold, layout, show_ext, labels, years, fiche, ptypes,
           selected, _, ymin, ymax):
    lo, hi = year_bounds()
    if list(years or []) == [ymin, ymax]:      # plage complète : suit les nouvelles années
        years = [lo, hi]
    options = highlight_options()
    if hl not in {o["value"] for o in options}:
        hl = None
    keep = _filters(years, (lo, hi), fiche, ptypes)
    fig = vizfig.make_figure(G, color_by, hl, types or [], threshold, layout, bool(show_ext),
                             keep, selected, bool(labels))
    return (fig, summary(), options, hl, search_options(bool(show_ext)), paper_options(),
            lo, hi, year_marks(lo, hi), years)


@app.callback(Output("detail", "children"), Output("to-lineage", "disabled"),
              Input("selected", "data"), Input("version", "data"))
def show_detail(selected, _):
    n = G.node(selected) if selected else None
    return vizfig.details(G, selected, ROOT), not (n and n["kind"] == "paper")


@app.callback(Output("tabs", "value"), Output("lin-mode", "value"), Output("lin-root", "value"),
              Input("to-lineage", "n_clicks"), State("selected", "data"), prevent_initial_call=True)
def to_lineage(_, selected):
    return "lineage", "paper", selected


@app.callback(Output("lineage-graph", "figure"), Output("lin-summary", "children"),
              Input("lin-mode", "value"), Input("lin-root", "value"), Input("lin-subject", "value"),
              Input("lin-depth", "value"), Input("lin-inter", "value"), Input("lin-infer", "value"),
              Input("labels", "value"), Input("selected", "data"), Input("version", "data"))
def update_lineage(mode, root, subject, depth, inter, infer, labels, selected, _):
    if mode == "paper":
        L = lineage.build(G, root=root if root in G.nodes else None, depth=depth,
                          infer_threshold=infer or 0)
    else:
        L = lineage.build(G, subject=(subject or "").strip() or None,
                          intermediates=bool(inter), infer_threshold=infer or 0)
    nodes = L["nodes"].values()
    n_pap = sum(1 for n in nodes if n["kind"] == "paper")
    n_cit = sum(1 for e in L["edges"] if e["kind"] == "citation")
    n_inf = len(L["edges"]) - n_cit
    text = (f"{n_pap} papier(s) du corpus · {len(L['nodes']) - n_pap} référence(s) externe(s) · "
            f"{n_cit} citation(s) lue(s)"
            + (f" · {n_inf} suite(s) probable(s), déduite(s)" if n_inf else "")
            + " · les références externes n'ont pas de bibliographie connue.") if nodes else ""
    return vizfig.lineage_figure(L, selected, bool(labels)), text


@app.callback(Output("download", "data"), Input("export", "n_clicks"),
              State("tabs", "value"), State("graph", "figure"), State("lineage-graph", "figure"),
              prevent_initial_call=True)
def export(_, tab, fig3d, fig_lin):
    fig = go.Figure(fig_lin if tab == "lineage" else fig3d)
    name = "genealogie.html" if tab == "lineage" else "graphe-3d.html"
    return {"content": fig.to_html(include_plotlyjs="cdn"), "filename": name}


# ----------------------------------------------------------------- onglet Bases

@app.callback(Output("bases-table", "children"), Output("bases-profile", "children"),
              Output("scan-sources", "options"), Output("scan-sources", "value"),
              Output("base-select", "options"),
              Input("version", "data"), Input("registry-rev", "data"))
def bases_panel(_, _rev):
    others = [(n, d) for n, d in registry.all_bases()
              if d.resolve() != ROOT and (d / "base.json").is_file()]
    opts = [{"label": f" {n} ", "value": n} for n, _ in others]
    return (vizbases.bases_table(ROOT), vizbases.profile_panel(ROOT), opts, [n for n, _ in others],
            vizbases.base_options(ROOT))


@app.callback(Output("scan-data", "data"), Output("scan-table", "data"),
              Output("scan-table", "selected_rows"), Output("scan-msg", "children"),
              Input("scan-run", "n_clicks"), Input("base-select", "value"),
              State("scan-sources", "value"), State("scan-kinds", "value"), prevent_initial_call=True)
def scan(n, _, names, kinds):
    if ctx.triggered_id != "scan-run":        # autre base affichée : résultat périmé
        return [], [], [], ""
    sources = [(nm, registry.resolve(nm)) for nm in names or [] if registry.resolve(nm)]
    if not sources:
        return [], [], [], "Aucune autre base à parcourir."
    rows = xbase.scan(ROOT, sources, tuple(kinds or xbase.KINDS))
    xbase.write(rows, ROOT / xbase.OUT)
    counts = " · ".join(f"{sum(r['kind'] == k for r in rows)} {vizbases.KIND_LABEL[k]}" for k in xbase.KINDS)
    return rows, vizbases.scan_rows(rows), [], f"{len(rows)} candidats ({counts}) — aussi dans {xbase.OUT}"


@app.callback(Output("scan-import", "disabled"), Input("scan-table", "selected_rows"))
def can_import(selected):
    return not selected


@app.callback(Output("imported", "data"), Output("scan-msg", "children", allow_duplicate=True),
              Output("scan-data", "data", allow_duplicate=True),
              Output("scan-table", "data", allow_duplicate=True),
              Output("scan-table", "selected_rows", allow_duplicate=True),
              Input("scan-import", "n_clicks"), State("scan-data", "data"),
              State("scan-table", "selected_rows"), State("imported", "data"), prevent_initial_call=True)
def import_selected(_, rows, selected, imported):
    done, msgs = vizbases.run_import(rows, selected, ROOT)
    gone = {d["paper_id"] for d in done}
    rows = [r for r in rows if not (r["paper_id"] and r["paper_id"] in gone)]
    if done:
        rc = bases.reindex(ROOT, quiet=True)
        if rc:
            msgs.append("reindex a signalé une erreur : lancer bin/pdb reindex pour le détail")
    head = (f"{len(done)} article(s) importé(s) : " + ", ".join(d["paper_id"] for d in done)
            + ". Fiches repassées à « todo » : /paper-fiche pour les réévaluer.") if done else ""
    return ((imported or 0) + 1 if done else no_update,
            html.Div([html.P(head, className="ok") if head else None,
                      html.P("\n".join(msgs), className="err") if msgs else None]),
            rows, vizbases.scan_rows(rows), [])


@app.callback(Output("new-msg", "children"), Output("registry-rev", "data"),
              Input("new-create", "n_clicks"),
              State("new-name", "value"), State("new-title", "value"), State("new-path", "value"),
              State("new-theme", "value"), State("registry-rev", "data"), prevent_initial_call=True)
def create_base(_, name, title, path, theme, rev):
    try:
        root = bases.create((name or "").strip(), theme, (path or "").strip() or None, title)
    except (bases.BaseError, ValueError, OSError) as e:
        return html.P(str(e), className="err"), no_update
    return (html.Div([html.P(f"Base « {name} » créée : {root}", className="ok"),
                      html.P(f"Suite : cd {root}, puis /base-profile dans Claude Code pour en tirer "
                             "axes et règles. Elle est déjà dans le sélecteur Base.")]),
            (rev or 0) + 1)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--port", type=int, default=8050)
    ap.add_argument("--debug", action="store_true")
    args = ap.parse_args()
    print(f"{base_title()} — {summary()}\n→ http://127.0.0.1:{args.port}")
    app.run(host="127.0.0.1", port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()
