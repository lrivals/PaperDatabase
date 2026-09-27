"""Onglet « Bases » de bin/viz.py : liste des bases, profil, création, recherche inter-bases.

Composants et rendus sans état ; les callbacks sont dans bin/viz.py. Les écritures (création
d'une base, import d'articles) passent par lib/bases.py et lib/xbase.py, comme `pdb base`.
Le profil n'est jamais modifié ici : ses changements se proposent et se valident avec
/base-profile.
"""
import re
from pathlib import Path

from dash import dash_table, dcc, html

from lib import bases, registry, xbase

KIND_LABEL = {"cited_here": "déjà cité ici", "in_base": "correspond aux règles",
              "ref_elsewhere": "cité ailleurs, absent partout"}
SCAN_COLUMNS = [("kind_label", "sorte"), ("score", "score"), ("source_base", "base"),
                ("title", "titre"), ("year", "année"), ("ident", "identifiant"), ("reasons", "raisons")]


def base_options(active_root):
    """Options du sélecteur : bases du registre, plus la base active si elle n'y est pas."""
    opts = [{"label": f"{n} — {bases.stats(n, d)['title']}" if (d / "base.json").is_file() else f"{n} (introuvable)",
             "value": str(d.resolve()), "disabled": not (d / "base.json").is_file()}
            for n, d in registry.all_bases()]
    active = str(Path(active_root).resolve())
    if active not in {o["value"] for o in opts}:
        opts.insert(0, {"label": f"{Path(active).name} (non enregistrée)", "value": active})
    return opts


def bases_table(active_root):
    rows = bases.all_stats()
    if not rows:
        return html.P("Aucune base enregistrée : créer la première ci-dessous, ou "
                      "`bin/pdb base register <dossier>`.", className="muted")
    active = Path(active_root).resolve()
    head = ["", "nom", "titre", "papiers", "fiches faites", "importés", "benchmarks", "axes",
            "suggestions", "modifiée"]
    body = []
    for r in rows:
        mark = ("▶ " if Path(r["path"]).resolve() == active else "") + ("★" if r["default"] else "")
        cells = [mark, r["name"], r["title"], r["papers"], r["done"], r["imported"], r["benchmarks"],
                 r["axes"], r["suggestions"] or "", r["modified"]] if r["exists"] else \
                [mark, r["name"], f"dossier introuvable : {r['path']}", *[""] * 7]
        body.append(html.Tr([html.Td(c) for c in cells], title=r["path"]))
    return html.Div(className="bench-wrap", children=[
        html.Table(className="bench", children=[html.Tr([html.Th(h) for h in head]), *body]),
        html.P("▶ base affichée   ★ base par défaut (hors de tout dossier de base)", className="muted"),
    ])


def profile_panel(root):
    root = Path(root)
    path = root / bases.PROFILE
    if not path.exists():
        return html.Div([html.P("Pas encore de profile.md pour cette base.", className="muted"),
                         html.P("Dans Claude Code, depuis le dossier de la base : /base-profile "
                                "(rédige le profil depuis base.json et CLAUDE.md, à valider).")])
    info = bases.info(root)
    sugg = info["suggestions"]
    axes = html.Table(className="bench", children=[
        html.Tr([html.Th(h) for h in ("axe", "titre", "papiers", "règle")]),
        *[html.Tr([html.Td(a), html.Td(t), html.Td(n), html.Td("oui" if r or a == "surveys" else "—")])
          for a, t, n, r in info["axes"]]])
    return html.Div([
        html.Div(className="notice", children=[
            html.B(f"{len(sugg)} suggestion(s) de profil en attente. "),
            "Les examiner avec /base-profile dans Claude Code (rien n'est appliqué sans accord).",
        ]) if sugg else None,
        html.Details(open=False, children=[html.Summary(f"Axes ({len(info['axes'])}) · "
                                                        f"{len(info['unclassified'])} papier(s) sans axe"),
                                           html.Div(axes, className="bench-wrap")]),
        dcc.Markdown(re.sub(r"<!--.*?-->", "", path.read_text(), flags=re.DOTALL), className="fiche"),
    ])


def create_form():
    return html.Div(children=[
        html.Div(className="form-row", children=[
            html.Label(["Nom court", dcc.Input(id="new-name", type="text", placeholder="anomalies")]),
            html.Label(["Intitulé", dcc.Input(id="new-title", type="text",
                                              placeholder="Détection d'anomalies industrielles")]),
            html.Label(["Dossier (facultatif)", dcc.Input(id="new-path", type="text",
                                                          placeholder=str(bases.default_path("<nom>")))]),
        ]),
        html.Label(["Thème, en quelques phrases (le LLM le précisera avec /base-profile)",
                    dcc.Textarea(id="new-theme", style={"width": "100%", "height": "80px"})]),
        html.Button("Créer la base", id="new-create"),
        html.Div(id="new-msg", className="muted"),
    ])


def scan_controls():
    return html.Div(children=[
        html.Div(className="form-row", children=[
            html.Label(["Chercher dans", dcc.Checklist(id="scan-sources", inline=True)]),
            html.Label(["Sortes", dcc.Checklist(
                id="scan-kinds", value=list(xbase.KINDS), inline=True,
                options=[{"label": f" {KIND_LABEL[k]} ", "value": k} for k in xbase.KINDS])]),
        ]),
        html.Button("Chercher", id="scan-run"),
        html.Button("Importer la sélection", id="scan-import", disabled=True),
        html.Div(id="scan-msg", className="muted"),
        dcc.Loading(dash_table.DataTable(
            id="scan-table", data=[], row_selectable="multi", selected_rows=[], page_size=25,
            sort_action="native", filter_action="native",
            columns=[{"name": n, "id": i} for i, n in SCAN_COLUMNS],
            style_table={"overflowX": "auto"},
            style_cell={"fontFamily": "system-ui, sans-serif", "fontSize": 12, "textAlign": "left",
                        "whiteSpace": "normal", "height": "auto", "maxWidth": "420px"},
            style_data_conditional=[{"if": {"filter_query": '{kind} = "ref_elsewhere"'},
                                     "color": "#6b6a64"}],
        )),
    ])


def layout():
    return html.Div(className="bases-tab", children=[
        html.H3("Mes bases"),
        html.Div(id="bases-table"),
        html.H3("Profil de la base affichée"),
        html.Div(id="bases-profile"),
        html.H3("Compléter depuis mes autres bases"),
        html.P("Articles déjà présents dans une autre base (copiés avec leur extraction ; la fiche "
               "repasse à « todo », pertinence à réévaluer) ou cités ailleurs (à ajouter avec "
               "/paper-add). Le score ordonne, il ne juge pas : comparer au profil.",
               className="muted"),
        scan_controls(),
        html.H3("Nouvelle base"),
        create_form(),
    ])


def scan_rows(rows):
    """Lignes de xbase.scan → données du tableau (colonnes d'affichage en plus)."""
    out = []
    for r in rows:
        ident = f"{r['source_base']}:{r['paper_id']}" if r["paper_id"] else (
            f"arXiv {r['arxiv_id']}" if r["arxiv_id"] else (r["doi"] or ""))
        out.append({**r, "kind_label": KIND_LABEL[r["kind"]], "ident": ident,
                    "year": r["year"] or ""})
    return out


def run_import(rows, selected, root):
    """Importe les lignes sélectionnées qui désignent un papier d'une autre base.
    Retourne (importés, messages)."""
    done, msgs = [], []
    for i in selected or []:
        r = rows[i]
        if not r.get("paper_id"):
            ident = r.get("arxiv_id") or r.get("doi")
            msgs.append(f"{(r['title'] or '')[:60]} : absent de toutes les bases → "
                        + (f"/paper-add {ident}" if ident else "pas d'identifiant, à chercher à la main"))
            continue
        src = registry.resolve(r["source_base"])
        try:
            done.append(xbase.import_paper(src, r["paper_id"], root, r["source_base"]))
        except (xbase.ImportError_, TypeError) as e:
            msgs.append(f"{r['paper_id']} : {e}")
    return done, msgs
