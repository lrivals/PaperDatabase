"""Figures statiques de bin/pdb plot (matplotlib) : benchmarks, évaluation, corpus.

Une fonction par figure, `fig_<nom>(ctx) -> (Figure, info)` ; `info` décrit les sources et
les effectifs (manifest.json). Données préparées par lib/plotdata.py. Même palette que
bin/viz.py (lib/vizfig.PALETTE, validée : skill dataviz) ; au-delà de trois catégories sur
un nuage de points, la couleur est doublée d'un marqueur. Chaque figure porte en pied sa
source et le nombre de lignes tracées sur le total (valeurs n/r exclues, jamais estimées).
"""
import textwrap

import numpy as np
from collections import Counter

import matplotlib
import matplotlib.patches  # noqa: F401  (Rectangle des heatmaps)
import matplotlib.ticker  # noqa: F401
import matplotlib.colors  # noqa: F401

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402

from lib import plotdata as D  # noqa: E402
from lib import query, refs, schema  # noqa: E402

# Palette de lib/vizfig.py (non importée : vizfig tire Dash). Ordre fixe, jamais cyclé.
PALETTE = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948"]
MARKERS = ["o", "D", "s", "^", "v", "P", "X", "*"]
OTHER_COLOR = "#8a8a86"
SURFACE = "#fcfcfb"
INK = "#1f1f1e"
INK_MUTED = "#6b6a64"
GRID = "#e4e3de"
EMPTY = "#f0efec"
SEQ = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]

FAMILY_COLOR = {f: PALETTE[i] for i, f in enumerate(D.FAMILIES)}
FAMILY_COLOR[D.OTHER] = OTHER_COLOR
FAMILY_MARKER = {f: MARKERS[i] for i, f in enumerate(D.FAMILIES)}
FAMILY_MARKER[D.OTHER] = "."
MEASURED = ("chip", "board", "board-dynamic")   # puissance mesurée (marqueur plein)

plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "font.size": 9, "axes.titlesize": 10, "axes.titleweight": "bold", "axes.titlelocation": "left",
    "axes.labelcolor": INK, "text.color": INK, "xtick.color": INK_MUTED, "ytick.color": INK_MUTED,
    "axes.edgecolor": GRID, "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "axes.axisbelow": True,
    "legend.frameon": False, "legend.fontsize": 8, "lines.linewidth": 2,
})


# ------------------------------------------------------------------ utilitaires

def _footer(fig, text):
    fig.text(0.01, 0.06 / fig.get_figheight(), text, fontsize=7, color=INK_MUTED, ha="left",
             va="bottom", wrap=True)


def _title(fig, title, subtitle=None):
    h = fig.get_figheight()
    fig.text(0.01, 1 - 0.1 / h, title, fontsize=12, fontweight="bold", ha="left", va="top")
    if subtitle:
        fig.text(0.01, 1 - 0.38 / h, subtitle, fontsize=8.5, color=INK_MUTED, ha="left", va="top")


def _fig_legend(fig, handles=None, labels=None, ncol=6):
    """Légende sous les panneaux, au-dessus du pied : ne masque jamais de données."""
    kw = {"handles": handles} if labels is None else {"handles": handles, "labels": labels}
    fig.legend(**kw, loc="lower center", ncol=ncol, bbox_to_anchor=(0.5, 0.42 / fig.get_figheight()))
    fig._pdb_legend = True


def _layout(fig):
    """Marges fixes en pouces : titre et sous-titre en haut, pied (et légende) en bas."""
    h = fig.get_figheight()
    bottom = (0.45 + (0.35 if getattr(fig, "_pdb_legend", False) else 0)) / h
    fig.tight_layout(rect=(0, bottom, 1, 1 - 0.62 / h))


def _num(v, _pos=None):
    """10, 500, 2 k, 1 M : graduations lisibles sur un axe log."""
    if v >= 1e6:
        return f"{v / 1e6:g} M"
    if v >= 1e3:
        return f"{v / 1e3:g} k"
    return f"{v:g}"


def _log(ax, which="xy"):
    for axis, name in ((ax.xaxis, "x"), (ax.yaxis, "y")):
        if name in which:
            getattr(ax, f"set_{name}scale")("log")
            axis.set_major_locator(_ShortLogLocator())
            axis.set_major_formatter(matplotlib.ticker.FuncFormatter(_num))
            axis.set_minor_formatter(matplotlib.ticker.NullFormatter())


class _ShortLogLocator(matplotlib.ticker.LogLocator):
    """Graduations 1-2-5 quand l'axe couvre moins de deux décades, puissances de 10 sinon."""

    def tick_values(self, vmin, vmax):
        import math
        if vmin > 0 and vmax > 0 and math.log10(vmax / vmin) < 2:
            self._subs = np.array([1.0, 2.0, 5.0])
        else:
            self._subs = np.array([1.0])
        return super().tick_values(vmin, vmax)


def _on(color):
    """Encre lisible sur un aplat : blanc sur les teintes sombres, INK sur les claires."""
    r, g, b = matplotlib.colors.to_rgb(color)
    lum = 0.2126 * r ** 2.2 + 0.7152 * g ** 2.2 + 0.0722 * b ** 2.2
    return INK if lum > 0.3 else "white"


def _ms(v):
    return f"{v:.3g} ms" if v < 1000 else f"{v / 1000:.2f} s"


def _wrap(s, width):
    return "\n".join(textwrap.wrap(s, width, break_long_words=False)) or s


def _trunc(s, n):
    return s if len(s) <= n else s[: n - 1] + "…"


def _bar_labels(ax, bars, fmt="{:.0f}"):
    for b in bars:
        w = b.get_width()
        if w <= 0:
            continue
        ax.text(w, b.get_y() + b.get_height() / 2, " " + fmt.format(w), va="center",
                fontsize=7.5, color=INK_MUTED)


def _family_handles(families, measured_note=True):
    handles = [Line2D([], [], ls="", marker=FAMILY_MARKER[f], markersize=7,
                      markerfacecolor=FAMILY_COLOR[f], markeredgecolor=FAMILY_COLOR[f], label=f)
               for f in families]
    if measured_note:
        handles += [Line2D([], [], ls="", marker="o", markersize=7, markerfacecolor=INK_MUTED,
                           markeredgecolor=INK_MUTED, label="puissance mesurée (puce / carte)"),
                    Line2D([], [], ls="", marker="o", markersize=7, markerfacecolor="none",
                           markeredgecolor=INK_MUTED, label="estimée ou portée non dite")]
    return handles


def _scatter_family(ax, points, x, y, measured_fill=True):
    fams = []
    for f in list(D.FAMILIES) + [D.OTHER]:
        pts = [p for p in points if p["_family"] == f]
        if not pts:
            continue
        fams.append(f)
        for measured in (True, False):
            sub = [p for p in pts if (p.get("power_scope") in MEASURED) == measured] \
                if measured_fill else (pts if measured else [])
            if not sub:
                continue
            ax.scatter([p["_v"][x] for p in sub], [p["_v"][y] for p in sub], s=42,
                       marker=FAMILY_MARKER[f], linewidths=1.3, edgecolors=FAMILY_COLOR[f],
                       facecolors=FAMILY_COLOR[f] if measured else "none", zorder=3)
        low = [p for p in pts if p.get("confidence") == "low"]
        for p in low:
            ax.annotate("confidence low", (p["_v"][x], p["_v"][y]), fontsize=6.5,
                        color=INK_MUTED, xytext=(4, -8), textcoords="offset points")
    return fams


# ------------------------------------------------------------------ benchmarks.csv

def fig_bench_fps_power(ctx):
    rows = ctx.rows
    pts, n, total = D.numeric(rows, "fps", "power_w")
    groups = [("Détection", [p for p in pts if D.task_bucket(p["task"]) == "détection"]),
              ("Autres tâches (classification, AE, apprentissage continu…)",
               [p for p in pts if D.task_bucket(p["task"]) != "détection"])]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.8), sharey=False)
    _title(fig, "Débit et puissance rapportés",
           "Lignes iso-efficacité en FPS/W. Échelles log. Une ligne = une configuration "
           "rapportée par un papier.")
    fams = set()
    for ax, (label, sub) in zip(axes, groups):
        fams |= set(_scatter_family(ax, sub, "power_w", "fps"))
        _log(ax)
        ax.set_title(f"{label} — {len(sub)} lignes", fontsize=9)
        ax.set_xlabel("puissance (W)")
        ax.set_ylabel("débit (images/s)")
        if sub:
            xs = [p["_v"]["power_w"] for p in sub]
            lo, hi = min(xs) / 1.5, max(xs) * 1.5
            ax.set_xlim(lo, hi)
            ylo, yhi = ax.get_ylim()
            for eff in (0.1, 1, 10, 100, 1000, 10000, 100000):
                ys = (eff * lo, eff * hi)
                if ys[1] < ylo or ys[0] > yhi:
                    continue
                ax.plot([lo, hi], ys, color=GRID, lw=1, ls="--", zorder=1)
                xt = min(hi / 1.3, yhi / eff / 1.3)
                if xt > lo:
                    ax.text(xt, eff * xt, f"{eff:g} FPS/W", fontsize=6.5, color=INK_MUTED,
                            ha="right", va="bottom", rotation=0)
            ax.set_ylim(ylo, yhi)
    _fig_legend(fig, _family_handles([f for f in list(D.FAMILIES) + [D.OTHER] if f in fams]))
    _footer(fig, f"Source : benchmarks.csv, colonnes fps et power_w ; {n} lignes sur {total} "
                 "(n/r exclus). Portées de puissance hétérogènes (power_scope) : puce, carte et "
                 "estimation ne sont pas comparables. Tâches, modèles et tailles d'entrée différents "
                 "d'un point à l'autre.")
    _layout(fig)
    return fig, {"sources": ["benchmarks.csv"], "n": n, "total": total}


def fig_bench_gops_per_watt(ctx):
    pts, n, total = D.numeric(ctx.rows, "gops", "power_w")
    order = [b for b in D.QUANT_BUCKETS if any(D.quant_bucket(p["quantization"]) == b for p in pts)]
    fig, ax = plt.subplots(figsize=(9, 4.6))
    _title(fig, "Efficacité énergétique par précision de calcul",
           "GOPS/W = gops / power_w de la même ligne. Points individuels ; trait = médiane.")
    fams = set()
    for i, b in enumerate(order):
        sub = [p for p in pts if D.quant_bucket(p["quantization"]) == b]
        vals = sorted(p["_v"]["gops"] / p["_v"]["power_w"] for p in sub)
        for j, p in enumerate(sub):
            f = p["_family"]
            fams.add(f)
            jitter = ((j % 7) - 3) * 0.05
            measured = p.get("power_scope") in MEASURED
            ax.scatter(i + jitter, p["_v"]["gops"] / p["_v"]["power_w"], s=40,
                       marker=FAMILY_MARKER[f], edgecolors=FAMILY_COLOR[f], linewidths=1.3,
                       facecolors=FAMILY_COLOR[f] if measured else "none", zorder=3)
        med = vals[len(vals) // 2] if len(vals) % 2 else (vals[len(vals) // 2 - 1] + vals[len(vals) // 2]) / 2
        ax.plot([i - 0.3, i + 0.3], [med, med], color=INK, lw=2, zorder=4)
        ax.text(i + 0.32, med, f"{med:.3g}", fontsize=7.5, color=INK_MUTED, va="center")
    ax.set_xticks(range(len(order)), [f"{b}\n(n={sum(1 for p in pts if D.quant_bucket(p['quantization']) == b)})"
                                      for b in order])
    _log(ax, "y")
    ax.set_ylabel("GOPS/W")
    ax.grid(axis="x", visible=False)
    ax.legend(handles=_family_handles([f for f in D.FAMILIES if f in fams]), loc="upper left")
    _footer(fig, f"Source : benchmarks.csv ; {n} lignes sur {total} ont gops et power_w (n/r exclus). "
                 "Précision regroupée depuis la colonne quantization (heuristique, lib/plotdata.quant_bucket). "
                 "GOPS comptés différemment selon les papiers (MAC = 1 ou 2 op).")
    _layout(fig)
    return fig, {"sources": ["benchmarks.csv"], "n": n, "total": total}


def fig_bench_fpga_resources(ctx):
    pts, _, total = D.numeric(ctx.rows, "luts", "dsps")
    pts = [p for p in pts if p["_family"] == "FPGA"]
    n = len(pts)
    counts = Counter(p["toolflow"] for p in pts)
    top = [t for t, _ in counts.most_common() if t != schema.NR][:7]
    fig, ax = plt.subplots(figsize=(8.5, 5))
    _title(fig, "Ressources FPGA consommées, par toolflow",
           "LUT et DSP rapportés pour une même configuration. Échelles log.")
    for i, t in enumerate(top + ["autre / n/r"]):
        sub = [p for p in pts if (p["toolflow"] if p["toolflow"] in top else "autre / n/r") == t]
        if not sub:
            continue
        color = PALETTE[i] if t in top else OTHER_COLOR
        ax.scatter([p["_v"]["luts"] for p in sub], [max(p["_v"]["dsps"], 0.8) for p in sub],
                   s=42, marker=MARKERS[i] if t in top else ".", color=color,
                   edgecolors=SURFACE, linewidths=0.6, label=f"{t} ({len(sub)})", zorder=3)
    _log(ax)
    ax.set_xlabel("LUT")
    ax.set_ylabel("DSP (0 tracé à 0,8)")
    ax.legend(loc="upper left")
    _footer(fig, f"Source : benchmarks.csv, lignes FPGA avec luts et dsps chiffrés ; {n} lignes "
                 f"sur {total}. Les FPGA ciblés diffèrent (Zynq-7000 à Virtex UltraScale+) : "
                 "un point ne dit rien du taux d'occupation.")
    _layout(fig)
    return fig, {"sources": ["benchmarks.csv"], "n": n, "total": total}


def fig_bench_accuracy_fps(ctx):
    panels = D.accuracy_panels(ctx.rows)
    total = len(ctx.rows)
    n = sum(len(p) for _, p in panels)
    k = max(len(panels), 1)
    fig, axes = plt.subplots(1, k, figsize=(3.6 * k + 1, 4.4), squeeze=False)
    _title(fig, "Précision et débit, une métrique par panneau",
           "Métriques de précision différentes : jamais sur le même axe. Débit en échelle log.")
    fams = set()
    for ax, (metric, pts) in zip(axes[0], panels):
        fams |= set(_scatter_family(ax, pts, "fps", "accuracy_value", measured_fill=False))
        _log(ax, "x")
        ax.set_title(_wrap(metric, 34) + f"\n{len(pts)} lignes", fontsize=8.5)
        ax.set_xlabel("débit (images/s)")
    axes[0][0].set_ylabel("valeur de la métrique")
    if fams:
        _fig_legend(fig, _family_handles([f for f in D.FAMILIES if f in fams], measured_note=False))
    _footer(fig, f"Source : benchmarks.csv, colonnes accuracy_metric, accuracy_value, fps ; "
                 f"{n} lignes sur {total}, métriques rapportées par au moins 4 lignes avec débit. "
                 "Métriques non comparables entre panneaux (jeu, IoU, nombre de classes).")
    _layout(fig)
    return fig, {"sources": ["benchmarks.csv"], "n": n, "total": total,
                 "metrics": [m for m, _ in panels]}


def fig_bench_quantization(ctx):
    rows = ctx.rows
    fams = [f for f in list(D.FAMILIES) + [D.OTHER]
            if any(D.platform_family(r["platform"]) == f for r in rows)]
    table = {f: Counter(D.quant_bucket(r["quantization"]) for r in rows
                        if D.platform_family(r["platform"]) == f) for f in fams}
    fig, ax = plt.subplots(figsize=(9.5, 4.2))
    _title(fig, "Précision de calcul par famille de plateforme",
           "Nombre de configurations rapportées (lignes de benchmarks.csv).")
    left = [0] * len(fams)
    for i, b in enumerate(D.QUANT_BUCKETS):
        vals = [table[f][b] for f in fams]
        if not any(vals):
            continue
        color = OTHER_COLOR if b == schema.NR else PALETTE[i]
        ax.barh(fams, vals, left=left, color=color, edgecolor=SURFACE, linewidth=2,
                label=b, height=0.62)
        for y, (v, l0) in enumerate(zip(vals, left)):
            if v >= 3:
                ax.text(l0 + v / 2, y, str(v), ha="center", va="center", fontsize=7, color=_on(color))
        left = [a + v for a, v in zip(left, vals)]
    for y, tot in enumerate(left):
        ax.text(tot, y, f"  {tot}", va="center", fontsize=8, color=INK_MUTED)
    ax.invert_yaxis()
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("lignes")
    _fig_legend(fig, ncol=8)
    _footer(fig, "Source : benchmarks.csv, colonnes platform et quantization regroupées "
                 "(heuristiques de lib/plotdata : platform_family, quant_bucket).")
    _layout(fig)
    return fig, {"sources": ["benchmarks.csv"], "n": len(rows), "total": len(rows)}


# ------------------------------------------------------------------ eval/results

MODES = ("hybrid", "dense", "lexical", "hybrid+rerank")
SETS = {"rag_eval": "rag_eval (EN)", "rag_eval_holdout": "holdout (EN)", "rag_eval_fr": "FR"}


def _eval(ctx, volet):
    got = ctx.latest.get(volet)
    if not got:
        raise LookupError(f"aucun run de pdb eval ne contient le volet {volet} "
                          "(lancer bin/pdb eval --save)")
    return got


def fig_eval_retrieval(ctx):
    rag, run = _eval(ctx, "rag")
    sets = [s for s in SETS if s in rag.get("sets", {})]
    metrics = ("recall@5", "recall@10", "mrr")
    thr = ctx.thresholds.get("rag.sets.rag_eval.hybrid.recall@5", {}).get("min")
    fig, axes = plt.subplots(1, 3, figsize=(11, 4), sharey=True)
    _title(fig, "Recherche de passages : qualité par mode et par jeu de questions",
           "Part des questions dont le passage attendu est dans les k premiers ; MRR = rang "
           "réciproque moyen.")
    width = 0.8 / len(MODES)
    for ax, m in zip(axes, metrics):
        for i, mode in enumerate(MODES):
            vals = [rag["sets"][s].get(mode, {}).get(m) for s in sets]
            xs = [j + (i - (len(MODES) - 1) / 2) * width for j in range(len(sets))]
            ok = [(x, v) for x, v in zip(xs, vals) if v is not None]
            ax.bar([x for x, _ in ok], [v for _, v in ok], width=width * 0.92, color=PALETTE[i],
                   label=mode if m == metrics[0] else None, zorder=3)
        ax.set_xticks(range(len(sets)), [f"{SETS[s]}\nn={rag['sets'][s].get('n', '?')}" for s in sets])
        ax.set_title(m, fontsize=9)
        ax.set_ylim(0, 1.05)
        ax.grid(axis="x", visible=False)
        if m == "recall@5" and thr is not None:
            ax.axhline(thr, color=INK_MUTED, lw=1, ls="--", zorder=4)
            ax.text(len(sets) - 0.5, thr, f"seuil {thr:g}", fontsize=7, color=INK_MUTED,
                    ha="right", va="bottom")
    _fig_legend(fig, ncol=4)
    _footer(fig, f"Source : eval/results/{run['_file']} ({D.run_label(run)}), volet rag ; "
                 f"{rag.get('passages', '?')} passages indexés, modèle {rag.get('model', '?')}. "
                 "Seuil : eval/thresholds.json.")
    _layout(fig)
    return fig, {"sources": [f"eval/results/{run['_file']}"], "run": D.run_label(run)}


VERIFY_EXPECTED = {"exact": "accepter", "mot remplacé": "accepter (APPROX)",
                   "chiffre modifié": "rejeter", "autre papier": "rejeter"}
VERIFY_STATUS = ("OK", "APPROX", "NOMBRES", "ABSENT")


def fig_eval_verify(ctx):
    rag, run = _eval(ctx, "rag")
    ver = rag.get("verify", {})
    cats = list(ver)
    fig, ax = plt.subplots(figsize=(9, 3.6))
    _title(fig, "pdb verify : verdict selon la perturbation de la citation",
           "Accepté = OK ou APPROX ; NOMBRES = texte proche mais chiffres différents ; "
           "ABSENT = introuvable dans le passage.")
    left = [0.0] * len(cats)
    for i, st in enumerate(VERIFY_STATUS):
        vals = [ver[c].get("status", {}).get(st, 0) / max(ver[c].get("n", 1), 1) for c in cats]
        ax.barh(range(len(cats)), vals, left=left, color=PALETTE[i], edgecolor=SURFACE,
                linewidth=2, label=st, height=0.6)
        for y, (v, l0) in enumerate(zip(vals, left)):
            if v >= 0.08:
                ax.text(l0 + v / 2, y, f"{v:.0%}", ha="center", va="center", fontsize=7.5,
                        color=_on(PALETTE[i]))
        left = [a + v for a, v in zip(left, vals)]
    ax.set_yticks(range(len(cats)), [f"{c} (n={ver[c].get('n')})\nattendu : {VERIFY_EXPECTED.get(c, '?')}"
                                     for c in cats])
    ax.invert_yaxis()
    ax.set_xlim(0, 1)
    ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1))
    ax.grid(axis="y", visible=False)
    _fig_legend(fig, ncol=4)
    _footer(fig, f"Source : eval/results/{run['_file']} ({D.run_label(run)}), rag.verify. "
                 "Citations perturbées générées par pdb eval (docs/EVAL.md).")
    _layout(fig)
    return fig, {"sources": [f"eval/results/{run['_file']}"], "run": D.run_label(run)}


def fig_eval_extraction(ctx):
    ext, run = _eval(ctx, "extraction")
    q = ext.get("quality", {})
    per = q.get("per_paper", {})
    ids = sorted(per, key=lambda p: per[p].get("coverage", 0))
    short = ctx.short
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, max(4, 0.2 * len(ids) + 1.8)), sharey=True,
                                 gridspec_kw={"width_ratios": (3, 2)})
    _title(fig, "Qualité de l'extraction du texte, par papier",
           f"Couverture moyenne {q.get('coverage_mean', 0):.3f} ; tableaux avec corps "
           f"{q.get('tables_with_body_rate', 0):.0%} ({q.get('tables', '?')} tableaux).")
    y = range(len(ids))
    a1.barh(y, [per[p].get("coverage", 0) for p in ids], color=PALETTE[0], height=0.7, zorder=3)
    thr = ctx.thresholds.get("extraction.quality.coverage_mean", {}).get("min")
    if thr is not None:
        a1.axvline(thr, color=INK_MUTED, lw=1, ls="--", zorder=4)
        a1.text(thr, -0.9, f"seuil moyenne {thr:g} ", fontsize=7, color=INK_MUTED, ha="right")
    a1.axvline(q.get("coverage_mean", 0), color=INK, lw=1.2, zorder=4)
    a1.set_xlim(min(0.7, min((per[p].get("coverage", 1) for p in ids), default=0.7) - 0.02), 1)
    a1.set_xlabel("couverture (texte extrait / texte du PDF)")
    a1.set_yticks(list(y), [short.get(p, p) for p in ids], fontsize=7)
    a1.set_title("Couverture", fontsize=9)
    with_body = [per[p].get("tables_with_body", 0) for p in ids]
    without = [per[p].get("tables", 0) - w for p, w in zip(ids, with_body)]
    a2.barh(y, with_body, color=PALETTE[2], height=0.7, label="avec corps", zorder=3,
            edgecolor=SURFACE, linewidth=1)
    a2.barh(y, without, left=with_body, color=OTHER_COLOR, height=0.7, label="légende seule",
            zorder=3, edgecolor=SURFACE, linewidth=1)
    a2.set_xlabel("tableaux")
    a2.set_title("Tableaux extraits", fontsize=9)
    a2.legend(loc="lower right")
    for a in (a1, a2):
        a.grid(axis="y", visible=False)
    _footer(fig, f"Source : eval/results/{run['_file']} ({D.run_label(run)}), extraction.quality ; "
                 f"{q.get('papers', len(ids))} papiers. Trait plein = moyenne. Seuil : eval/thresholds.json.")
    _layout(fig)
    return fig, {"sources": [f"eval/results/{run['_file']}"], "run": D.run_label(run), "n": len(ids)}


def fig_eval_latency(ctx):
    sp, run = _eval(ctx, "speed")
    items = []
    for key, label in (("search_lexical_ms", "search lexical"), ("search_dense_ms", "search dense"),
                       ("search_hybrid_ms", "search hybrid"),
                       ("search_hybrid+rerank_ms", "search hybrid+rerank")):
        if isinstance(sp.get(key), dict):
            items.append((label, sp[key].get("p50"), sp[key].get("p95")))
    if isinstance(sp.get("verify_ms"), (int, float)):
        items.append(("verify", sp["verify_ms"], None))
    if isinstance(sp.get("index_load_s"), (int, float)):
        items.append(("chargement de l'index", sp["index_load_s"] * 1000, None))
    for cmd, s in (sp.get("cli_s") or {}).items():
        items.append((f"CLI pdb {cmd}", s * 1000, None))
    fig, ax = plt.subplots(figsize=(9, 0.38 * len(items) + 1.8))
    _title(fig, "Temps d'exécution", "Médiane (p50) ; trait = p95 quand il est mesuré. Échelle log.")
    y = range(len(items))
    ax.barh(y, [i[1] for i in items], color=PALETTE[0], height=0.6, zorder=3)
    for yi, (_, p50, p95) in zip(y, items):
        if p95:
            ax.plot([p50, p95], [yi, yi], color=INK, lw=1.2, zorder=4)
            ax.plot([p95], [yi], marker="|", color=INK, markersize=8, zorder=4)
        label = _ms(p50) + (f"  (p95 {_ms(p95)})" if p95 else "")
        ax.text((p95 or p50) * 1.12, yi, label, va="center", fontsize=7.5, color=INK_MUTED)
    ax.set_yticks(list(y), [i[0] for i in items])
    ax.invert_yaxis()
    _log(ax, "x")
    ax.set_xlim(right=max(i[2] or i[1] for i in items) * 8)
    ax.set_xlabel("ms")
    ax.grid(axis="y", visible=False)
    _footer(fig, f"Source : eval/results/{run['_file']} ({D.run_label(run)}), volet speed ; "
                 f"{sp.get('passages', '?')} passages. CLI = processus complet, démarrage de Python compris.")
    _layout(fig)
    return fig, {"sources": [f"eval/results/{run['_file']}"], "run": D.run_label(run)}


HISTORY = {"recall@5 hybrid (rag_eval)": "rag.sets.rag_eval.hybrid.recall@5",
           "recall@5 hybrid (holdout)": "rag.sets.rag_eval_holdout.hybrid.recall@5",
           "couverture moyenne (extraction)": "extraction.quality.coverage_mean",
           "tableaux avec corps (extraction)": "extraction.quality.tables_with_body_rate"}


def fig_eval_history(ctx):
    hist = D.eval_history(ctx.runs, HISTORY)
    dates = sorted({d for s in hist.values() for d, _ in s})
    if len(dates) < 2:
        raise LookupError("moins de deux runs de pdb eval : pas d'historique à tracer")
    fig, ax = plt.subplots(figsize=(9, 4))
    _title(fig, "Évolution des métriques d'évaluation au fil des runs",
           "Un point par run de pdb eval --save qui mesure la métrique.")
    for i, (name, series) in enumerate(hist.items()):
        if not series:
            continue
        xs = [dates.index(d) for d, _ in series]
        ax.plot(xs, [v for _, v in series], color=PALETTE[i], marker=MARKERS[i], markersize=6,
                label=name, zorder=3)
    ax.set_xticks(range(len(dates)), [d.replace("T", "\n") for d in dates], fontsize=7)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("valeur (0–1)")
    ax.legend(loc="lower left")
    _footer(fig, f"Source : eval/results/*.json ({len(ctx.runs)} runs). Runs partiels : une "
                 "métrique n'apparaît que pour les runs qui mesurent son volet.")
    _layout(fig)
    return fig, {"sources": [f"eval/results/{r['_file']}" for r in ctx.runs]}


# ------------------------------------------------------------------ corpus

def fig_corpus_years(ctx):
    by_year = D.corpus_by_year(ctx.papers)
    years = sorted(y for y in by_year if y is not None)
    years_all = list(range(years[0], years[-1] + 1)) if years else []
    types = [t for t in schema.TYPES if any(by_year[y][t] for y in by_year)]
    fig, ax = plt.subplots(figsize=(9, 3.8))
    _title(fig, "Papiers de la base par année et par type",
           f"{len(ctx.papers)} papiers ; les preprints ne sont pas relus par les pairs.")
    bottom = [0] * len(years_all)
    for i, t in enumerate(types):
        vals = [by_year.get(y, Counter())[t] for y in years_all]
        ax.bar(years_all, vals, bottom=bottom, color=PALETTE[i], edgecolor=SURFACE, linewidth=1.5,
               label=t, width=0.75, zorder=3)
        bottom = [a + v for a, v in zip(bottom, vals)]
    for x, tot in zip(years_all, bottom):
        if tot:
            ax.text(x, tot, str(tot), ha="center", va="bottom", fontsize=7.5, color=INK_MUTED)
    ax.grid(axis="x", visible=False)
    ax.set_ylabel("papiers")
    ax.legend(loc="upper left")
    unknown = sum(by_year.get(None, Counter()).values())
    _footer(fig, "Source : papers/*/metadata.json (year, type)."
                 + (f" {unknown} papier(s) sans année non tracés." if unknown else ""))
    _layout(fig)
    return fig, {"sources": ["papers/*/metadata.json"], "n": len(ctx.papers)}


def fig_corpus_axes(ctx):
    by_axis = D.corpus_by_axis(ctx.papers)
    axes_ = list(by_axis)
    fig, ax = plt.subplots(figsize=(8.5, 3.6))
    _title(fig, "Papiers par axe de veille et état de la fiche de lecture",
           "Un papier compte dans chacun de ses axes (total supérieur au nombre de papiers).")
    done = [by_axis[a]["done"] for a in axes_]
    todo = [by_axis[a]["todo"] for a in axes_]
    ax.barh(axes_, done, color=PALETTE[0], label="fiche done", height=0.6, edgecolor=SURFACE,
            linewidth=2, zorder=3)
    ax.barh(axes_, todo, left=done, color=OTHER_COLOR, label="fiche todo", height=0.6,
            edgecolor=SURFACE, linewidth=2, zorder=3)
    for y, (d, t) in enumerate(zip(done, todo)):
        ax.text(d + t, y, f"  {d + t}" + (f" ({t} todo)" if t else ""), va="center", fontsize=8,
                color=INK_MUTED)
    ax.invert_yaxis()
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("papiers")
    _fig_legend(fig, ncol=2)
    _footer(fig, "Source : papers/*/metadata.json (axes, status.fiche). Axes : DATA_MODEL.md §3.")
    _layout(fig)
    return fig, {"sources": ["papers/*/metadata.json"], "n": len(ctx.papers)}


def fig_corpus_bench_coverage(ctx):
    rows = ctx.rows
    cols = [c for c in schema.BENCHMARK_COLUMNS if c not in ("paper_id", "source_section",
                                                             "confidence", "power_scope")]
    rates = D.nr_rates(rows, cols)
    cols = sorted(cols, key=lambda c: rates[c])
    fig, (a1, a2, a3) = plt.subplots(1, 3, figsize=(11.5, 4.6),
                                     gridspec_kw={"width_ratios": (2.2, 1, 1)})
    _title(fig, "Complétude de benchmarks.csv",
           f"{len(rows)} lignes, {len({r['paper_id'] for r in rows})} papiers. n/r = non rapporté "
           "par les auteurs.")
    bars = a1.barh(cols, [rates[c] for c in cols], color=PALETTE[1], height=0.65, zorder=3)
    for b, c in zip(bars, cols):
        a1.text(b.get_width(), b.get_y() + b.get_height() / 2, f" {rates[c]:.0%}", va="center",
                fontsize=7.5, color=INK_MUTED)
    a1.set_xlim(0, 1.1)
    a1.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1))
    a1.set_title("Part de n/r par colonne", fontsize=9)
    for ax, col, order, title in ((a2, "power_scope", list(schema.POWER_SCOPES) + [schema.NR],
                                   "power_scope"),
                                  (a3, "confidence", list(schema.CONFIDENCE), "confidence")):
        c = Counter(r[col] for r in rows)
        keys = [k for k in order if c[k]]
        bars = ax.barh(keys, [c[k] for k in keys], height=0.6, zorder=3,
                       color=[OTHER_COLOR if k == schema.NR else PALETTE[0] for k in keys])
        _bar_labels(ax, bars)
        ax.set_title(title, fontsize=9)
        ax.invert_yaxis()
        ax.set_xlim(0, max(c.values()) * 1.25)
        ax.set_xlabel("lignes")
    for ax in (a1, a2, a3):
        ax.grid(axis="y", visible=False)
    _footer(fig, "Source : benchmarks.csv. power_scope : chip, board, board-dynamic, estimated, "
                 "unspecified (DATA_MODEL.md) ; n/r quand power_w est n/r.")
    _layout(fig)
    return fig, {"sources": ["benchmarks.csv"], "n": len(rows)}


def fig_corpus_citations(ctx, top=15):
    internal = D.cited_by_counts(ctx.papers, refs.citations(ctx.ref_papers))[:top]
    external = D.load_external_refs(ctx.root, top)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 5.2))
    _title(fig, "Papiers les plus cités par le corpus",
           "Nombre de papiers de la base qui les citent (bibliographies extraites, "
           "rapprochées par lib/refs.py).")
    by_id = {m["id"]: m for m in ctx.papers}
    labels = [f"{ctx.short.get(p, p)} — {_trunc(by_id[p].get('title') or '', 40)}" for p, _ in internal]
    bars = a1.barh(range(len(internal)), [c for _, c in internal], color=PALETTE[0], height=0.65, zorder=3)
    a1.set_yticks(range(len(internal)), labels, fontsize=7)
    a1.set_title("Dans la base (cited-by)", fontsize=9)
    _bar_labels(a1, bars)
    labels = [f"{_trunc(e['title'], 48)} ({e['year']})" for e in external]
    bars = a2.barh(range(len(external)), [e["n"] for e in external], color=OTHER_COLOR,
                   height=0.65, zorder=3)
    a2.set_yticks(range(len(external)), labels, fontsize=7)
    a2.set_title("Hors base (external_refs.csv) : candidats à lire", fontsize=9)
    _bar_labels(a2, bars)
    for ax in (a1, a2):
        ax.invert_yaxis()
        ax.grid(axis="y", visible=False)
        ax.set_xlabel("papiers citants")
        ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))
    _footer(fig, "Sources : papers/*/refs.jsonl (lib/refs.citations) et external_refs.csv. "
                 "Références issues du parsing des bibliographies : à vérifier avant de les citer.")
    _layout(fig)
    return fig, {"sources": ["papers/*/refs.jsonl", "external_refs.csv"],
                 "n_internal": len(internal), "n_external": len(external)}


def _heatmap(ax, rows_, cols, matrix, title):
    cmap = LinearSegmentedColormap.from_list("seq", SEQ)
    vmax = max((v for r in matrix for v in r), default=1) or 1
    for i, row in enumerate(matrix):
        for j, v in enumerate(row):
            color = EMPTY if v == 0 else cmap(0.15 + 0.85 * v / vmax)
            ax.add_patch(matplotlib.patches.Rectangle((j - 0.5, i - 0.5), 1, 1, facecolor=color,
                                                      edgecolor=SURFACE, linewidth=2))
            ax.text(j, i, "0" if v == 0 else str(v), ha="center", va="center", fontsize=8,
                    color=INK_MUTED if v == 0 else _on(color))
    ax.set_xlim(-0.5, len(cols) - 0.5)
    ax.set_ylim(len(rows_) - 0.5, -0.5)
    ax.set_xticks(range(len(cols)), [_wrap(c, 12) for c in cols], fontsize=7.5)
    ax.set_yticks(range(len(rows_)), rows_)
    ax.grid(False)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(length=0)
    ax.set_title(title, fontsize=9)


def fig_corpus_gaps(ctx):
    r1, c1, m1 = D.coverage_matrix(ctx.rows, ctx.papers, "axis")
    r2, c2, m2 = D.coverage_matrix(ctx.rows, ctx.papers, "task")
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 0.45 * max(len(r1), len(r2)) + 2.6))
    _title(fig, "Carte de couverture des benchmarks : où sont les gaps ?",
           "Nombre de papiers distincts ayant au moins une ligne chiffrée par case. "
           "Case à 0 = gap candidat (à confirmer dans gaps.md).")
    _heatmap(a1, r1, c1, m1, "famille × axe du papier")
    _heatmap(a2, r2, c2, m2, "famille × tâche de la ligne")
    _footer(fig, "Sources : benchmarks.csv (platform, task) et papers/*/metadata.json (axes). "
                 "Familles et tâches regroupées par lib/plotdata ; axe surveys exclu. Un 0 signifie « absent de la base », "
                 "pas « absent de la littérature ».")
    _layout(fig)
    return fig, {"sources": ["benchmarks.csv", "papers/*/metadata.json"],
                 "zeros_axis": [(r, c) for i, r in enumerate(r1) for j, c in enumerate(c1) if m1[i][j] == 0],
                 "zeros_task": [(r, c) for i, r in enumerate(r2) for j, c in enumerate(c2) if m2[i][j] == 0]}


# ------------------------------------------------------------------ registre

FIGURES = {
    # nom : (groupe, fonction, description)
    "bench_fps_power": ("bench", fig_bench_fps_power, "débit vs puissance, détection / autres tâches"),
    "bench_gops_per_watt": ("bench", fig_bench_gops_per_watt, "GOPS/W par précision de calcul"),
    "bench_fpga_resources": ("bench", fig_bench_fpga_resources, "LUT vs DSP des FPGA, par toolflow"),
    "bench_accuracy_fps": ("bench", fig_bench_accuracy_fps, "précision vs débit, un panneau par métrique"),
    "bench_quantization": ("bench", fig_bench_quantization, "précision de calcul par famille de plateforme"),
    "eval_retrieval": ("eval", fig_eval_retrieval, "recall@5/@10 et MRR par mode et jeu de questions"),
    "eval_verify": ("eval", fig_eval_verify, "verdicts de pdb verify par perturbation"),
    "eval_extraction": ("eval", fig_eval_extraction, "couverture du texte et tableaux, par papier"),
    "eval_latency": ("eval", fig_eval_latency, "temps d'exécution (recherche, verify, CLI)"),
    "eval_history": ("eval", fig_eval_history, "évolution des métriques au fil des runs"),
    "corpus_years": ("corpus", fig_corpus_years, "papiers par année et type"),
    "corpus_axes": ("corpus", fig_corpus_axes, "papiers par axe, fiches done / todo"),
    "corpus_bench_coverage": ("corpus", fig_corpus_bench_coverage, "part de n/r, power_scope, confidence"),
    "corpus_citations": ("corpus", fig_corpus_citations, "papiers les plus cités, dans et hors base"),
    "corpus_gaps": ("corpus", fig_corpus_gaps, "heatmaps famille × axe / tâche (cases vides = gaps)"),
}


class Context:
    """Données chargées à la demande, partagées entre les figures d'un même appel."""

    def __init__(self, root):
        self.root = root
        self._cache = {}

    def _get(self, key, load):
        if key not in self._cache:
            self._cache[key] = load()
        return self._cache[key]

    rows = property(lambda s: s._get("rows", lambda: query.load_benchmarks(s.root)[1]))
    papers = property(lambda s: s._get("papers", lambda: query.load_papers(s.root)))
    ref_papers = property(lambda s: s._get("ref_papers", lambda: refs.load_papers(s.root)))
    short = property(lambda s: s._get("short", lambda: query.short_ids(s.papers)))
    runs = property(lambda s: s._get("runs", lambda: D.load_eval_runs(s.root / "eval" / "results")))
    latest = property(lambda s: s._get("latest", lambda: D.latest_eval(s.runs)))
    thresholds = property(lambda s: s._get("thr", lambda: D.load_thresholds(
        s.root / "eval" / "thresholds.json")))
