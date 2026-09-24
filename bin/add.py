#!/usr/bin/env python3
"""Acquisition d'un article, puis ingestion.

usage : add.py <arxiv-id | url arXiv | chemin.pdf> [...]

- id ou URL arXiv : métadonnées via l'API arXiv, PDF téléchargé dans inbox/ ;
- PDF local       : copié dans inbox/ ;
- autre URL       : refusée — télécharger le PDF à la main et le déposer dans inbox/.
"""
import json
import shutil
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "bin"))

import requests  # noqa: E402
from lxml import etree  # noqa: E402

import ingest  # noqa: E402
from lib import ids  # noqa: E402

INBOX = ROOT / "inbox"
PAPERS = ROOT / "papers"
API = "http://export.arxiv.org/api/query"
HEADERS = {"User-Agent": "PaperDatabase/1.0 (usage personnel, recherche bibliographique)"}
ATOM = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
API_DELAY = 3  # secondes entre deux appels, politique d'usage de l'API arXiv


class AddError(Exception):
    pass


def _t(node, path):
    r = node.xpath(path, namespaces=ATOM)
    if not r:
        return None
    s = " ".join((r[0].text or "").split())
    return s or None


def _split_name(name):
    parts = name.split()
    if len(parts) == 1:
        return {"given": None, "family": parts[0]}
    return {"given": " ".join(parts[:-1]), "family": parts[-1]}


def arxiv_metadata(arxiv_id):
    try:
        r = requests.get(API, params={"id_list": arxiv_id, "max_results": 1}, headers=HEADERS, timeout=30)
    except (requests.ConnectionError, requests.Timeout) as e:
        raise AddError(f"réseau indisponible ({type(e).__name__}) : impossible de joindre export.arxiv.org")
    if r.status_code != 200:
        raise AddError(f"API arXiv : HTTP {r.status_code} pour {arxiv_id}")
    feed = etree.fromstring(r.content)
    entries = feed.xpath("a:entry", namespaces=ATOM)
    entry = entries[0] if entries else None
    if entry is None or "api/errors" in (_t(entry, "a:id") or "") or not _t(entry, "a:title"):
        raise AddError(f"identifiant arXiv inexistant : {arxiv_id}")
    published = _t(entry, "a:published")  # date de la v1
    return {
        "arxiv_id": arxiv_id,
        "title": _t(entry, "a:title"),
        "authors": [_split_name(_t(a, "a:name")) for a in entry.xpath("a:author", namespaces=ATOM)],
        "year": int(published[:4]) if published else None,
        "published": published,
        "abstract": _t(entry, "a:summary"),
        "doi": _t(entry, "arxiv:doi"),
        "journal_ref": _t(entry, "arxiv:journal_ref"),
        "venue": None,
    }


def download_pdf(arxiv_id, dest):
    url = f"https://arxiv.org/pdf/{arxiv_id}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=120)
    except (requests.ConnectionError, requests.Timeout) as e:
        raise AddError(f"réseau indisponible ({type(e).__name__}) : téléchargement de {url} impossible")
    if r.status_code != 200 or not r.content.startswith(b"%PDF"):
        raise AddError(f"PDF introuvable à {url} (HTTP {r.status_code})")
    dest.write_bytes(r.content)


def add_arxiv(arxiv_id):
    stem = f"arxiv-{arxiv_id.replace('/', '_')}"
    pdf, meta_path = INBOX / f"{stem}.pdf", INBOX / f"{stem}.meta.json"
    done = sorted(PAPERS.glob(ids.arxiv_dir_prefix(arxiv_id) + "*"))
    if done:
        raise AddError(f"{arxiv_id} déjà ingéré : papers/{done[0].name}")
    if pdf.exists():
        raise AddError(f"{pdf.name} déjà présent dans inbox/ : lancer .venv/bin/python bin/ingest.py")
    meta = arxiv_metadata(arxiv_id)
    print(f"arXiv {arxiv_id} : {meta['title']} ({meta['year']})")
    download_pdf(arxiv_id, pdf)
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n")
    return pdf


def add_local(path):
    src = Path(path).expanduser().resolve()
    if not src.is_file():
        raise AddError(f"fichier introuvable : {src}")
    with open(src, "rb") as f:
        if f.read(4) != b"%PDF":
            raise AddError(f"{src.name} n'est pas un PDF")
    dest = INBOX / src.name
    if dest.exists():
        raise AddError(f"{dest.name} déjà présent dans inbox/ : lancer .venv/bin/python bin/ingest.py")
    digest = ingest.sha256(src)
    for p in PAPERS.glob("*/paper.pdf"):
        if ingest.sha256(p) == digest:
            raise AddError(f"{src.name} déjà ingéré : papers/{p.parent.name}")
    shutil.copy2(src, dest)
    return dest


def acquire(arg):
    arxiv_id = ids.find_arxiv_id(arg)
    if arxiv_id:
        return add_arxiv(arxiv_id)
    if arg.startswith(("http://", "https://")) or arg.startswith("www."):
        if ids.is_arxiv_url(arg):
            raise AddError(f"URL arXiv sans identifiant reconnaissable : {arg}")
        raise AddError(
            "URL non-arXiv : pas de téléchargement automatique (ni contournement de paywall).\n"
            "  Télécharge le PDF à la main (accès université), puis :\n"
            "    cp ~/Téléchargements/article.pdf inbox/ && .venv/bin/python bin/ingest.py"
        )
    return add_local(arg)


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0 if args else 2)
    INBOX.mkdir(exist_ok=True)
    pdfs, failed = [], 0
    for i, arg in enumerate(args):
        if i and ids.find_arxiv_id(arg):
            time.sleep(API_DELAY)
        try:
            pdfs.append(acquire(arg))
        except AddError as e:
            failed += 1
            print(f"erreur  {arg} : {e}", file=sys.stderr)
    if pdfs:
        failed += ingest.run(pdfs)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
