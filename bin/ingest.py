#!/usr/bin/env python3
"""Ingestion des PDF de inbox/ : extraction, nettoyage, écriture de papers/<paper_id>/.

usage : ingest.py [--force] [chemin.pdf ...]
        ingest.py --reparse [--tables docling [--ocr]] [paper_id ...]
Sans chemin, traite tous les PDF de inbox/. --reparse ré-extrait les papiers déjà ingérés
(tous, ou ceux dont le paper_id contient un des motifs) depuis leur grobid.tei.xml, sans
GROBID (repli PyMuPDF sur paper.pdf pour ceux qui n'en ont pas) ; fiche.md n'est jamais
écrasée. --tables docling relance Docling sur les tableaux restés sans corps (25-100 s par
papier ; résultat gardé dans papers/<id>/docling_tables.json, relu ensuite). Voir SETUP.md §5.
"""
import argparse
import difflib
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

CODE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(CODE))

import requests  # noqa: E402

from lib import base, citation, doc, docling_tables, ids, ligatures, pdftext, schema, tables, tei  # noqa: E402

ROOT = base.ROOT
INBOX = ROOT / "inbox"
PAPERS = ROOT / "papers"
GROBID_URL = "http://localhost:8070/api/processFulltextDocument"
# Champs qu'un fichier de citation éditeur (.bib / .ris, lib/citation.py) fixe dans metadata.json
CITATION_KEYS = ("title", "authors", "year", "venue", "doi", "type")

# Règles propres au domaine de la base, lues dans base.json (lib/base.py, DATA_MODEL §11).
# Découverte (bin/discover.py) : un candidat est « dans le sujet » s'il relève d'un des
# hardware_axes, si son titre correspond à title_topic_re, ou si titre + résumé mentionnent
# au moins topic_min_hits fois topic_re (contexte matériel). Une mention isolée dans le
# résumé ne suffit pas (SqueezeNet, DoReFa-Net : « feasible FPGA deployment » en passant),
# ni un axe thématique seul (autoencodeur, YOLO sans matériel). AXIS_QUERIES sert de requête
# par défaut pour `discover --axis`.
_CFG = base.CONFIG
AXIS_QUERIES = dict(_CFG["axis_queries"])


# --- utilitaires ----------------------------------------------------------------------

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def grobid_alive():
    r = subprocess.run(["bash", str(CODE / "bin" / "grobid.sh"), "status"], capture_output=True)
    return r.returncode == 0


def grobid_extract(pdf):
    with open(pdf, "rb") as f:
        r = requests.post(
            GROBID_URL,
            files={"input": (pdf.name, f, "application/pdf")},
            data={
                "consolidateHeader": "0",
                "consolidateCitations": "0",
                "includeRawCitations": "1",
                "teiCoordinates": ["p", "head", "figure", "biblStruct"],
            },
            timeout=300,
        )
    if r.status_code != 200:
        raise RuntimeError(f"GROBID HTTP {r.status_code} : {r.text[:200]}")
    return r.content


def find_existing(arxiv_id, digest, papers_dir=None):
    """Dossier papers/ déjà occupé par cet article (même id arXiv ou même PDF)."""
    papers_dir = Path(papers_dir) if papers_dir is not None else PAPERS
    if arxiv_id:
        hits = sorted(papers_dir.glob(ids.arxiv_dir_prefix(arxiv_id) + "*"))
        if hits:
            return hits[0]
    for p in papers_dir.glob("*/paper.pdf"):
        if sha256(p) == digest:
            return p.parent
    return None


def classify(text, title_kw=""):
    return base.classify(_CFG, text, title_kw)


def keep_classification(old, axes, tags):
    """Axes et tags d'une ré-extraction : ceux d'une fiche `done` priment (confirmés à la
    lecture) ; sinon union ordonnée des anciens puis des nouveaux, pour ne pas perdre une
    correction manuelle quand l'abstract ré-extrait diffère."""
    if not old:
        return axes, tags
    old_axes, old_tags = old.get("axes") or [], old.get("tags") or []
    if old.get("status", {}).get("fiche") == "done":
        return old_axes, old_tags
    return (list(dict.fromkeys(old_axes + axes)), list(dict.fromkeys(old_tags + tags)))


def _full(a):
    return re.sub(r"[^a-z]", "", " ".join(x for x in (a.get("given"), a.get("family")) if x).lower())


def _best_split(arx_author, tei_authors):
    """arXiv ne donne que le nom complet (« Rashed Al Amin ») : on reprend la séparation
    prénom/nom de GROBID quand le nom complet est identique."""
    for t in tei_authors:
        if _full(t) == _full(arx_author):
            return {"given": t["given"], "family": t["family"]}
    return arx_author


def merge_metadata(arx, header, backend, warnings):
    """.meta.json arXiv > teiHeader GROBID > null. Rien n'est deviné."""
    meta = schema.new_metadata()
    for k in ("title", "authors", "year", "venue", "doi", "arxiv_id"):
        v = (arx or {}).get(k) or header.get(k)
        meta[k] = v if v not in ("", []) else ([] if k == "authors" else None)
    if arx and header.get("authors"):
        meta["authors"] = [_best_split(a, header["authors"]) for a in meta["authors"]]

    if arx:
        meta["url"] = (f"https://arxiv.org/abs/{arx['arxiv_id']}" if arx.get("arxiv_id")
                       else arx.get("url") or (f"https://doi.org/{meta['doi']}" if meta["doi"] else None))
        if arx.get("type") in schema.TYPES:
            meta["type"] = arx["type"]
        if arx.get("journal_ref"):
            meta["venue"] = arx["journal_ref"]
            warnings.append(f"publié ailleurs selon arXiv (journal_ref : {arx['journal_ref']}) : "
                            "type journal/conference à préciser")
        elif arx.get("venue_openalex"):  # ajout par DOI (bin/add.py) : version éditeur connue
            meta["venue"] = arx["venue_openalex"]
            warnings.append(f"publié ailleurs selon OpenAlex ({arx['venue_openalex']}, DOI {meta['doi']}) : "
                            "type journal/conference à préciser")
        elif arx.get("arxiv_id"):
            meta["venue"] = "arXiv preprint"
            meta["type"] = "preprint"
        if header.get("title") and arx.get("title"):
            ratio = difflib.SequenceMatcher(None, header["title"].lower(), arx["title"].lower()).ratio()
            if ratio < 0.8:
                warnings.append(f"titre du PDF ≠ titre arXiv : « {header['title']} »")
    else:
        if meta["arxiv_id"]:  # tampon arXiv du PDF, lu par GROBID
            meta["url"] = f"https://arxiv.org/abs/{meta['arxiv_id']}"
        elif meta["doi"]:
            meta["url"] = f"https://doi.org/{meta['doi']}"
        warnings.append("type de publication à préciser")
    if backend == "pymupdf" and schema.WARN_MANUAL_METADATA not in warnings:
        warnings.insert(0, schema.WARN_MANUAL_METADATA)
    return meta


def apply_citation(meta, cit, warnings):
    """Fichier de citation éditeur (lib/citation.py) : ses champs non vides priment."""
    for k in CITATION_KEYS:
        if cit.get(k) not in (None, []):
            meta[k] = cit[k]
    if cit.get("doi") and not meta.get("arxiv_id"):
        meta["url"] = f"https://doi.org/{cit['doi']}"
    warnings[:] = resolved_by_citation(warnings, cit)
    return meta


def resolved_by_citation(warnings, cit):
    """Avertissements restants une fois un fichier de citation appliqué."""
    resolved = ("type de publication", "publié ailleurs") if cit.get("type") else ()
    return [w for w in warnings if not w.startswith(resolved) and w != schema.WARN_MANUAL_METADATA]


# Avertissements recalculés à chaque extraction ; les autres (métadonnées, notes manuelles)
# appartiennent à l'utilisateur une fois le papier ingéré : une ré-extraction les conserve.
EXTRACTION_WARNINGS = ("GROBID a échoué", "ligatures perdues", "aucune section détectée",
                       "sections numérotées non détectées", "corps très court",
                       schema.WARN_TABLES_RECOVERED, schema.WARN_TABLES_DOCLING, schema.WARN_TABLES_LOST)
AXES_WARNINGS = (schema.WARN_AXES_GUESSED, "aucun axe détecté")


def reextraction_warnings(old, new, cit=None):
    """Avertissements d'une ré-extraction : ceux de l'ancien metadata.json, hors extraction
    (moins ceux qu'un fichier de citation résout), puis les avertissements d'extraction
    recalculés. Fiche done : plus aucun avertissement sur les axes (confirmés)."""
    kept = [w for w in (old.get("extraction") or {}).get("warnings") or []
            if not w.startswith(EXTRACTION_WARNINGS)]
    if cit:
        kept = resolved_by_citation(kept, cit)
    out = kept + [w for w in new if w.startswith(EXTRACTION_WARNINGS) and w not in kept]
    if (old.get("status") or {}).get("fiche") == "done":
        out = [w for w in out if not w.startswith(AXES_WARNINGS)]
    return out


def find_citation(pdf, doi, title, dirs=None):
    """Fichier de citation qui correspond au PDF, à côté de lui ou dans inbox/."""
    for d in dict.fromkeys(dirs if dirs is not None else (pdf.parent, INBOX)):
        if d.is_dir():
            found = citation.find(d, doi=doi, title=title)
            if found:
                return found
    return None


def store_citation(path, out):
    """Conserve le fichier de citation dans papers/<id>/ comme preuve des métadonnées.

    Déplacé s'il ne décrit que ce papier, copié s'il en décrit plusieurs (export groupé).
    """
    target = out / f"citation{path.suffix.lower()}"
    if path.resolve() == target.resolve():
        return
    if len(citation.parse(path)) > 1:
        shutil.copyfile(path, target)
    else:
        shutil.move(str(path), target)


def check_missing(meta, warnings):
    for k in ("title", "year"):
        if meta[k] is None:
            warnings.append(f"{k} introuvable")
    if not meta["authors"]:
        warnings.append("auteurs introuvables")
    return meta


# --- traitement d'un PDF --------------------------------------------------------------

def process(pdf, force=False, use_grobid=True, tei_bytes=None, vocab=None, docling=False, ocr=False,
            papers_dir=None, source_meta=None, citation_dirs=None):
    """Retourne ('ingéré' | 'ignoré', message).

    tei_bytes : TEI déjà obtenu (--reparse), GROBID n'est alors pas appelé.
    vocab : vocabulaire de lib/ligatures (calculé sur le corpus si absent).
    docling : lance Docling sur les tableaux restés sans corps (lib/docling_tables.py) ; sans
    cette option, un docling_tables.json déjà présent est relu. ocr : Docling avec OCR.
    """
    pdf = Path(pdf).resolve()
    meta_json = pdf.with_suffix(".meta.json")
    arx = source_meta if source_meta is not None else (json.loads(meta_json.read_text()) if meta_json.exists() else None)
    digest = sha256(pdf)
    papers_dir = Path(papers_dir) if papers_dir is not None else PAPERS

    existing = find_existing((arx or {}).get("arxiv_id"), digest, papers_dir)
    if existing and not force:
        return "ignoré", f"déjà ingéré dans papers/{existing.name} (--force pour ré-extraire ; sinon supprimer le PDF de inbox/)"

    warnings = []
    if tei_bytes is not None:
        header, blocks, refs = tei.parse(tei_bytes)
        backend = "grobid"
    elif use_grobid:
        try:
            tei_bytes = grobid_extract(pdf)
            header, blocks, refs = tei.parse(tei_bytes)
            backend = "grobid"
        except Exception as e:  # repli sur PyMuPDF
            warnings.append(f"GROBID a échoué ({e}) : repli PyMuPDF")
            tei_bytes = None
    if tei_bytes is None:
        header, blocks, refs = pdftext.extract(pdf)
        backend = "pymupdf"

    if source_meta and source_meta.get("title") and header.get("title"):
        claimed = source_meta["title"].casefold()
        extracted = header["title"].casefold()
        if len(extracted) >= 15 and difflib.SequenceMatcher(
                None, claimed, extracted).ratio() < 0.4:
            raise ValueError("external PDF title does not match its discovery record")

    old = json.loads((existing / "metadata.json").read_text()) if existing else None
    meta = merge_metadata(arx, header, backend, warnings)
    if old:  # ré-extraction : les métadonnées déjà validées (ou corrigées à la main) priment
        for k in ("title", "authors", "year", "venue", "doi", "arxiv_id", "url", "type", "added"):
            if old.get(k) not in (None, []):
                meta[k] = old[k]
        meta["status"]["fiche"] = old.get("status", {}).get("fiche", "todo")
        warnings[:] = [w for w in warnings if not w.startswith(("type de publication", "publié ailleurs"))]
    cit = find_citation(pdf, (arx or {}).get("doi") or header.get("doi"),
                        (arx or {}).get("title") or header.get("title"), dirs=citation_dirs)
    if cit:  # déposé exprès pour corriger l'en-tête : prime aussi sur l'ancien metadata.json
        apply_citation(meta, cit[1], warnings)
    check_missing(meta, warnings)
    abstract = (arx or {}).get("abstract") or header.get("abstract") or ""
    title_kw = " ".join([meta["title"] or "", " ".join(header.get("keywords", []))])
    axes, tags = classify(f"{title_kw} {abstract}", title_kw)
    meta["axes"], meta["tags"] = keep_classification(old, axes, tags)
    warnings.append(schema.WARN_AXES_GUESSED if axes else "aucun axe détecté : à classer dans /paper-fiche")

    if existing:
        paper_id = existing.name  # un paper_id ne change jamais
    else:
        paper_id, w = ids.make_paper_id(meta)
        warnings += w
        if (papers_dir / paper_id).exists():
            return "ignoré", f"papers/{paper_id} existe déjà pour un autre PDF : conflit à résoudre à la main"
    meta["id"] = paper_id

    fixed, left = ligatures.repair_blocks(blocks, vocab if vocab is not None
                                          else ligatures.corpus_vocabulary(ROOT))
    if fixed:
        warnings.append(f"ligatures perdues à l'extraction : {fixed} mot(s) réparé(s) (lib/ligatures.py)")
    if left:
        warnings.append(f"ligatures perdues : {left} fragment(s) non réparé(s) (« classi cation »…)")

    docling_found = None  # tableaux Docling à mettre en cache dans papers/<id>/
    if backend == "grobid":
        recovered, lost = tables.recover(pdf, blocks)
        if recovered:
            warnings.append(f"{schema.WARN_TABLES_RECOVERED} : {', '.join(recovered)}")
        if lost:
            cache = docling_tables.load(existing) if existing else None
            if docling and (cache is None or (ocr and not cache.get("ocr"))):
                cache = {"ocr": ocr, "tables": docling_tables.extract(pdf, ocr=ocr)}
                docling_found = cache
            if cache:
                by_docling, lost = docling_tables.recover(blocks, cache["tables"])
                if by_docling:
                    warnings.append(f"{schema.WARN_TABLES_DOCLING} : {', '.join(by_docling)}")
        if lost:
            warnings.append(f"{schema.WARN_TABLES_LOST} : {', '.join(lost)}")

    body_chars = sum(len(t) for b in blocks if b.kind == "section" for t, _ in b.paras)
    if not any(b.kind == "section" and b.heading for b in blocks):
        warnings.append("aucune section détectée")
    gaps = doc.numbering_gaps(blocks)
    if gaps:
        warnings.append(f"sections numérotées non détectées : {', '.join(gaps)} — "
                        "leur texte est rattaché à la section précédente")
    if body_chars < 2000:
        warnings.append(f"corps très court ({body_chars} caractères) : extraction douteuse")
    if old:
        warnings = reextraction_warnings(old, warnings, cit[1] if cit else None)
    meta["extraction"] = {
        "backend": backend,
        "ok": backend == "grobid" and body_chars >= 2000,
        "warnings": warnings,
    }
    meta["status"]["extracted"] = True

    out = papers_dir / paper_id

    errs = schema.validate_metadata(meta)
    if errs:
        raise ValueError("metadata.json non conforme : " + "; ".join(errs))

    out.mkdir(parents=True, exist_ok=True)
    tei_path = out / "grobid.tei.xml"
    if tei_bytes is not None:
        tei_path.write_bytes(tei_bytes)
    elif tei_path.exists():
        tei_path.unlink()  # trace d'une extraction précédente, plus d'actualité
    (out / "fulltext.md").write_text(doc.render_fulltext(meta, blocks))
    with open(out / "sections.jsonl", "w") as f:
        for row in doc.to_sections(paper_id, blocks):
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    with open(out / "refs.jsonl", "w") as f:
        for r in refs:
            f.write(json.dumps({"paper_id": paper_id, **r}, ensure_ascii=False) + "\n")
    (out / "metadata.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n")
    if not (out / "fiche.md").exists():
        (out / "fiche.md").write_text(schema.render_fiche(meta))

    target = out / "paper.pdf"
    if pdf != target:
        shutil.move(str(pdf), target)
    if meta_json.exists():
        meta_json.unlink()
    if cit:
        store_citation(cit[0], out)
    if docling_found:
        docling_tables.save(out, docling_found["tables"], docling_found["ocr"])
    note = f" [{backend}]" + (f" — {len(warnings)} avertissement(s)" if warnings else "")
    return "ingéré", f"papers/{paper_id}{note}"


def run(pdfs=None, force=False):
    """Ingère les PDF donnés (ou tout inbox/). Retourne le nombre d'erreurs."""
    if pdfs:
        pdfs = [Path(p) for p in pdfs]
    else:
        pdfs = sorted(INBOX.glob("*.pdf"))
    if not pdfs:
        print("inbox/ est vide : rien à ingérer.")
        return 0

    use_grobid = grobid_alive()
    if not use_grobid:
        print("GROBID ne répond pas (bash bin/grobid.sh start) : repli PyMuPDF, métadonnées à vérifier.")

    counts = {"ingéré": 0, "ignoré": 0, "erreur": 0}
    vocab = ligatures.corpus_vocabulary(ROOT)
    for pdf in pdfs:
        try:
            status, msg = process(pdf, force=force, use_grobid=use_grobid, vocab=vocab)
        except Exception as e:
            status, msg = "erreur", f"{type(e).__name__}: {e}"
        counts[status] += 1
        print(f"{status:7} {pdf.name} → {msg}")
    print(f"\n{counts['ingéré']} ingéré(s), {counts['ignoré']} ignoré(s), {counts['erreur']} erreur(s).")
    if counts["ingéré"]:
        print("Penser à lancer : bin/pdb reindex (fait automatiquement par bin/pdb add et bin/pdb ingest)")
    return counts["erreur"]


def reparse(patterns=(), docling=False, ocr=False):
    """Ré-extrait les papiers déjà ingérés depuis papers/<id>/grobid.tei.xml (sans GROBID),
    ou depuis paper.pdf par PyMuPDF s'ils n'ont pas de TEI. Retourne le nombre d'erreurs.
    docling, ocr : voir process."""
    folders = sorted(p for p in PAPERS.iterdir() if (p / "metadata.json").exists())
    if patterns:
        folders = [f for f in folders if any(q in f.name for q in patterns)]
    if not folders:
        print("aucun papier ne correspond.")
        return 1
    vocab = ligatures.corpus_vocabulary(ROOT)
    errors = 0
    for folder in folders:
        pdf, tei_path = folder / "paper.pdf", folder / "grobid.tei.xml"
        try:
            if not pdf.exists():
                raise FileNotFoundError("paper.pdf absent (gitignoré : le redéposer)")
            tei_bytes = tei_path.read_bytes() if tei_path.exists() else None
            status, msg = process(pdf, force=True, use_grobid=False, tei_bytes=tei_bytes, vocab=vocab,
                                  docling=docling, ocr=ocr)
        except Exception as e:
            status, msg = "erreur", f"{type(e).__name__}: {e}"
            errors += 1
        print(f"{status:7} {folder.name} → {msg}")
    return errors


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--force", action="store_true",
                    help="ré-extrait un article déjà ingéré (fiche.md n'est jamais écrasée)")
    ap.add_argument("--reparse", action="store_true",
                    help="ré-extrait les papiers déjà ingérés depuis leur TEI, sans GROBID")
    ap.add_argument("--tables", choices=("docling",),
                    help="avec --reparse : relance Docling sur les tableaux restés sans corps (lent)")
    ap.add_argument("--ocr", action="store_true", help="avec --tables docling : OCR des tableaux en image")
    ap.add_argument("pdfs", nargs="*", help="PDF à ingérer (défaut : tout inbox/) ; avec --reparse : motifs de paper_id")
    args = ap.parse_args()
    if args.reparse:
        sys.exit(1 if reparse(args.pdfs, docling=args.tables == "docling", ocr=args.ocr) else 0)
    sys.exit(1 if run(args.pdfs, force=args.force) else 0)


if __name__ == "__main__":
    main()
