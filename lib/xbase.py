"""Entre bases : articles d'une autre base utiles à la base cible, et import par copie.

Sans LLM ni réseau. Trois sortes de candidats (DATA_MODEL §11) :
- cited_here    : papier présent dans une autre base, que des papiers de la cible citent déjà
                  (signal le plus fort : la cible le référence sans l'avoir) ;
- in_base       : papier présent dans une autre base, dont titre + résumé correspondent aux
                  règles de la cible (axis_rules, topic_re, tag_rules de son base.json) ;
- ref_elsewhere : travail absent de toutes les bases, cité par une autre base et correspondant
                  aux règles de la cible, ou cité à la fois ici et là-bas ; à ajouter par
                  /paper-add.
Les correspondances d'articles reprennent les clés de lib/refs.py (arXiv, DOI, titre
normalisé, titre voisin), celles qui construisent external_refs.csv.

Le score ne juge pas la pertinence : il ordonne. Le jugement se fait contre profile.md
(/paper-discover), et un import est toujours décidé par l'utilisateur.
"""
import csv
import datetime as _dt
import json
import re
import shutil
from pathlib import Path

from lib import base, refs, registry, schema

KINDS = ("cited_here", "in_base", "ref_elsewhere")
FIELDS = ("rank", "kind", "score", "source_base", "paper_id", "title", "year", "doi", "arxiv_id",
          "n_citers_target", "n_citers_source", "axes_guess", "reasons")
OUT = "xbase_candidates.csv"
MIN_SHARED_CITERS = 3   # ref_elsewhere hors règles : citants cumulés (cible + source)


class ImportError_(Exception):
    pass


# ---------------------------------------------------------------- lecture d'une base

def abstract_of(folder):
    path = Path(folder) / "sections.jsonl"
    if not path.exists():
        return ""
    for line in path.read_text().splitlines():
        if line.strip():
            row = json.loads(line)
            if row.get("kind") == "abstract":
                return row.get("text") or ""
    return ""


def load(root):
    """metadata + refs + résumé de chaque papier de root/papers."""
    papers = refs.load_papers(root)
    for p in papers:
        p["abstract"] = abstract_of(Path(root, "papers", p["id"]))
    return papers


class Matcher:
    """Reconnaît un article parmi un ensemble : clé exacte, puis titre voisin."""

    def __init__(self, items=()):
        self.key, self.titles = {}, refs._TitleIndex()
        for target, d in items:
            self.add(target, d)

    def add(self, target, d):
        for k in refs.ref_keys(d):
            self.key.setdefault(k, target)
        self.titles.add(d.get("title"), d.get("year"), target)

    def find(self, d):
        hit = next((self.key[k] for k in refs.ref_keys(d) if k in self.key), None)
        return hit if hit is not None else self.titles.find(d.get("title"), d.get("year"))


def _external_groups(papers):
    """Groupes « ext: » (travaux hors base cités) et leurs citants."""
    cites, groups = refs.group_refs(papers)
    citers = refs.citers_of(cites)
    return {gid: {**g, "citers": sorted(citers[gid])} for gid, g in groups.items()}


def _judge(cfg, title, text):
    """Axes devinés, étiquettes et appartenance au sujet selon les règles de la cible."""
    axes, tags = base.classify(cfg, text, title or "")
    return axes, tags, base.in_topic(cfg, title, text, axes)


def _has_rules(cfg):
    return bool(cfg["axis_rules"] or cfg["topic_re"] or cfg["title_topic_re"])


# ---------------------------------------------------------------- scan

def scan(target_root, sources, kinds=KINDS):
    """Candidats pour target_root, pris dans sources = [(nom, dossier)]. Liste de dicts FIELDS."""
    target_root = Path(target_root).resolve()
    cfg = base.load_config(target_root)
    rules = _has_rules(cfg)
    tpapers = load(target_root)
    in_target = Matcher((p["id"], p) for p in tpapers)
    t_ext = _external_groups(tpapers)
    cited_by_target = Matcher((gid, g) for gid, g in t_ext.items())

    best = {}   # clé canonique → candidat (un même article vu dans deux sources n'apparaît qu'une fois)
    seen = Matcher()

    def offer(d, cand):
        key = seen.find(d)
        if key is None:
            key = len(best)
            seen.add(key, d)
        if key not in best or cand["score"] > best[key]["score"]:
            best[key] = cand

    for name, sroot in sources:
        sroot = Path(sroot).resolve()
        if sroot == target_root:
            continue
        spapers = load(sroot)
        for p in spapers:
            if in_target.find(p) is not None:
                continue
            text = " ".join(filter(None, (p.get("title"), p["abstract"])))
            axes, tags, topic = _judge(cfg, p.get("title"), text)
            gid = cited_by_target.find(p)
            n_t = len(t_ext[gid]["citers"]) if gid else 0
            reasons = []
            if gid:
                kind = "cited_here"
                reasons.append(f"cité par {n_t} papier(s) de la cible : "
                               + ", ".join(t_ext[gid]["citers"][:3]) + ("…" if n_t > 3 else ""))
                score = 10 + 3 * n_t + 2 * len(axes)
            elif not rules:
                kind, score = "in_base", 0.0
                reasons.append("base cible sans règles : juger avec profile.md")
            elif topic and (axes or not cfg["axis_rules"]):
                kind, score = "in_base", 2 * len([a for a in axes if a != "surveys"]) + 0.5 * len(tags) + 1
            else:
                continue
            if kind not in kinds:
                continue
            if axes:
                reasons.append("axes : " + ",".join(axes))
            if tags:
                reasons.append("tags : " + ",".join(tags[:6]))
            if (p.get("status") or {}).get("fiche") == "done":
                reasons.append(f"fiche faite dans {name}")
            offer(p, {"kind": kind, "score": round(score, 1), "source_base": name, "paper_id": p["id"],
                      "title": p.get("title"), "year": p.get("year"), "doi": p.get("doi"),
                      "arxiv_id": p.get("arxiv_id"), "n_citers_target": n_t, "n_citers_source": 0,
                      "axes_guess": ",".join(axes), "reasons": " ; ".join(reasons)})

        if "ref_elsewhere" not in kinds:
            continue
        for gid, g in _external_groups(spapers).items():
            if in_target.find(g) is not None:
                continue
            title = g.get("title") or ""
            axes, tags, topic = _judge(cfg, title, title)
            tgid = cited_by_target.find(g)
            n_t = len(t_ext[tgid]["citers"]) if tgid else 0
            n_s = len(g["citers"])
            match = rules and axes and topic
            if n_t and (n_t + n_s >= MIN_SHARED_CITERS or match):
                # cité ici et là-bas : vaut d'être regardé même si le titre ne dit rien
                reasons = [f"cité par {n_t} papier(s) de la cible et {n_s} de {name}"]
            elif match and n_s >= 2:
                reasons = [f"cité par {n_s} papiers de {name}"]
            else:
                continue
            if axes:
                reasons.append("axes : " + ",".join(axes))
            score = 3 * n_t + n_s + 2 * len(axes)
            offer(g, {"kind": "ref_elsewhere", "score": float(score), "source_base": name,
                      "paper_id": "", "title": title, "year": g.get("year"), "doi": g.get("doi"),
                      "arxiv_id": g.get("arxiv_id"), "n_citers_target": n_t, "n_citers_source": n_s,
                      "axes_guess": ",".join(axes), "reasons": " ; ".join(reasons)})

    order = {k: i for i, k in enumerate(KINDS)}
    rows = sorted(best.values(), key=lambda r: (order[r["kind"]], -r["score"], -(r["year"] or 0)))
    return [{"rank": i, **r} for i, r in enumerate(rows, 1)]


def write(rows, path):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: "" if r.get(k) is None else r[k] for k in FIELDS})


# ---------------------------------------------------------------- recherche d'un article ailleurs

def find_elsewhere(d, here, env=None):
    """[(nom, paper_id)] des bases enregistrées (sauf `here`) qui contiennent l'article d
    (clés arxiv_id / doi / title)."""
    here = Path(here).resolve()
    hits = []
    for name, root in registry.all_bases(env):
        if root.resolve() == here or not (root / "papers").is_dir():
            continue
        m = Matcher((p["id"], p) for p in refs.load_papers(root))
        pid = m.find(d)
        if pid:
            hits.append((name, pid))
    return hits


# ---------------------------------------------------------------- import

BANNER = ("> **Importée de la base `{base}` le {date}.** Cette fiche a été écrite pour une autre "
          "base (autre thème) : pertinence à réévaluer ici, puis `fiche: done` via "
          "`/paper-fiche`. Statut d'origine : {status}.\n")


def _mark_fiche(text, banner):
    """fiche: todo dans le front-matter, bandeau juste après."""
    m = re.match(r"---\n.*?\n---\n", text, re.DOTALL)
    if not m:
        return banner + "\n" + text
    front = re.sub(r"^fiche:.*$", "fiche: todo", m.group(0), count=1, flags=re.MULTILINE)
    return front + "\n" + banner + text[m.end():]


def import_paper(src_root, paper_id, dst_root, src_name, with_pdf=True):
    """Copie papers/<paper_id>/ de src_root vers dst_root, reclassé selon la cible.

    Ne réindexe pas : l'appelant lance bases.reindex(dst_root) une fois tous les imports faits.
    Retourne {"paper_id", "axes", "benchmarks"}."""
    src_root, dst_root = Path(src_root).resolve(), Path(dst_root).resolve()
    if src_root == dst_root:
        raise ImportError_("source et cible sont la même base")
    src = src_root / "papers" / paper_id
    if not (src / "metadata.json").is_file():
        raise ImportError_(f"{paper_id} absent de {src_name}")
    meta = json.loads((src / "metadata.json").read_text())
    dst_papers = dst_root / "papers"
    dup = Matcher((p["id"], p) for p in refs.load_papers(dst_root)).find(meta)
    if dup or (dst_papers / paper_id).exists():
        raise ImportError_(f"{paper_id} déjà présent dans la cible : papers/{dup or paper_id}")

    cfg = base.load_config(dst_root)
    dst = dst_papers / paper_id
    dst_papers.mkdir(exist_ok=True)
    shutil.copytree(src, dst, ignore=None if with_pdf else shutil.ignore_patterns("paper.pdf"))

    today = _dt.date.today().isoformat()
    old_status = (meta.get("status") or {}).get("fiche", "todo")
    text = " ".join(filter(None, (meta.get("title"), abstract_of(src))))
    axes, tags = base.classify(cfg, text, meta.get("title") or "")
    meta["imported_from"] = {"base": src_name, "paper_id": paper_id, "date": today,
                             "fiche": old_status, "axes": meta.get("axes") or []}
    meta["axes"] = [a for a in axes if a in cfg["axes"]]
    meta["tags"] = list(dict.fromkeys((meta.get("tags") or []) + tags))
    meta["status"] = {**(meta.get("status") or {}), "fiche": "todo"}
    warnings = meta.setdefault("extraction", {}).setdefault("warnings", [])
    if schema.WARN_AXES_GUESSED not in warnings:
        warnings.append(schema.WARN_AXES_GUESSED)
    (dst / "metadata.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n")

    fiche = dst / "fiche.md"
    if fiche.exists():
        banner = BANNER.format(base=src_name, date=today, status=old_status)
        fiche.write_text(_mark_fiche(fiche.read_text(), banner))

    n_bench = _copy_benchmarks(src_root / "benchmarks.csv", dst_root / "benchmarks.csv", paper_id)
    return {"paper_id": paper_id, "axes": meta["axes"], "benchmarks": n_bench}


def _copy_benchmarks(src_csv, dst_csv, paper_id):
    if not src_csv.exists():
        return 0
    with open(src_csv, newline="") as f:
        rows = [r for r in csv.DictReader(f) if r.get("paper_id") == paper_id]
    if not rows:
        return 0
    fresh = not dst_csv.exists() or not dst_csv.read_text().strip()
    if not fresh:
        with open(dst_csv, newline="") as f:
            if any(r.get("paper_id") == paper_id for r in csv.DictReader(f)):
                return 0
    with open(dst_csv, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=schema.BENCHMARK_COLUMNS, extrasaction="ignore",
                           lineterminator="\n")
        if fresh:
            w.writeheader()
        w.writerows(rows)
    return len(rows)
