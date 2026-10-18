"""Vérité terrain des tableaux (lot E-e) : notation de l'extraction contre des tableaux
transcrits depuis l'image de leur zone (eval/fixtures/tables_gold.jsonl, DATA_MODEL §7.3).

Quatre mesures, séparées (docs/AMELIORATIONS.md, lot E-e) :
- détection : la section attendue est un tableau qui a un corps (au moins deux rangées) ;
- rattachement : sa légende porte le numéro du tableau attendu ;
- cellules : part des cellules numériques de la vérité retrouvées à la même colonne de la
  rangée extraite la plus proche, après normalisation des nombres ; `numbers` : part des
  nombres retrouvés n'importe où dans le tableau (sans contrainte de position) ;
- unités : part des unités attendues présentes dans le texte extrait.
"""
import json
import re
from pathlib import Path

from lib import tables

_NUM = re.compile(r"[-+]?\d+(?:[.,]\d+)*(?:\s?[kKMG](?![a-zA-Z]))?")


def norm_number(s):
    """« 18, 820 » → 18820 ; « 28.2k » → 28.2k ; « −3,5 » → -3.5 (virgule décimale seule)."""
    s = (s or "").replace("−", "-").replace(" ", "").replace("\xa0", "")
    s = re.sub(r"(\d),\s?(\d{3})(?!\d)", r"\1\2", s)   # séparateur de milliers
    s = re.sub(r"(\d),(\d)", r"\1.\2", s)               # virgule décimale
    s = re.sub(r"\s+", "", s).lower()
    return s


def numbers(text):
    return [norm_number(m.group(0)) for m in _NUM.finditer(text or "")]


def cell_key(cell):
    """Contenu numérique comparable d'une cellule, ou None si elle n'a pas de nombre."""
    ns = numbers(cell)
    return tuple(ns) if ns else None


def _extracted(row_text):
    paras = [p for p in row_text.split("\n\n") if p.strip()]
    return paras[0] if paras else "", [[c.strip() for c in p.split("|")] for p in paras[1:]]


def _best_row(gold_row, rows):
    want = set(n for c in gold_row for n in numbers(c))
    best, score = None, -1
    for r in rows:
        s = len(want & set(n for c in r for n in numbers(c)))
        if s > score:
            best, score = r, s
    return best


def score_table(gold, section):
    """Mesures d'un tableau ; section : ligne de sections.jsonl (None si absente)."""
    out = {"section_id": gold["section_id"], "label": gold["label"], "detected": False,
           "attached": False, "cells": None, "numbers": None, "units": None}
    if section is None or section.get("kind") != "table":
        return out
    caption, rows = _extracted(section["text"])
    out["detected"] = len(rows) >= 2
    want = tables.label_number(gold["label"])
    out["attached"] = want is not None and tables.label_number(caption) == want
    num_cells = hit = 0
    for grow in gold.get("rows") or []:
        match = _best_row(grow, rows) if rows else None
        for j, cell in enumerate(grow):
            key = cell_key(cell)
            if key is None:
                continue
            num_cells += 1
            if match is not None and j < len(match) and cell_key(match[j]) == key:
                hit += 1
    if num_cells:
        out["cells"] = hit / num_cells
        gold_nums = [n for r in gold["rows"] for c in r for n in numbers(c)]
        got = numbers(section["text"])
        pool = list(got)
        found = 0
        for n in gold_nums:
            if n in pool:
                pool.remove(n)
                found += 1
        out["numbers"] = found / len(gold_nums)
    units = [u for u in (gold.get("units") or {}).values() if u]
    if units:
        low = section["text"].lower()
        out["units"] = sum(u.lower() in low for u in units) / len(units)
    return out


def load_sections(root, paper_ids):
    out = {}
    for pid in paper_ids:
        path = Path(root) / "papers" / pid / "sections.jsonl"
        if path.exists():
            for line in path.read_text().splitlines():
                if line.strip():
                    row = json.loads(line)
                    out[row["id"]] = row
    return out


def evaluate(root, gold_rows):
    """Moyennes sur les tableaux de la vérité terrain, et le détail par tableau."""
    sections = load_sections(root, {g["paper_id"] for g in gold_rows})
    per = [score_table(g, sections.get(g["section_id"])) for g in gold_rows]

    def mean(key):
        xs = [p[key] for p in per if p[key] is not None]
        return sum(xs) / len(xs) if xs else None

    return {"n": len(per), "reviewed": sum(1 for g in gold_rows if g.get("reviewed")),
            "detected": mean("detected"), "attached": mean("attached"), "cells": mean("cells"),
            "numbers": mean("numbers"), "units": mean("units"), "per_table": per}
