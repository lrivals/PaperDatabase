"""Empreinte du corpus (lot H, provenance des réponses) : sha256 des fichiers qui font foi
(benchmarks.csv, et pour chaque papier metadata.json, sections.jsonl, fiche.md). Deux
réponses de même empreinte reposent sur le même corpus. Partagée par la route CPU
(pdb search) et la route GPU (lib/rag_qwen.py).
"""
import hashlib
from pathlib import Path

FILES = ("metadata.json", "sections.jsonl", "fiche.md")


def paths(root):
    root = Path(root)
    out = [root / "benchmarks.csv"]
    for d in sorted((root / "papers").iterdir()):
        if d.is_dir():
            out += [d / name for name in FILES]
    return out


def fingerprint(root):
    root = Path(root)
    h = hashlib.sha256()
    for p in paths(root):
        if not p.exists():  # papier sans fiche : absent de l'empreinte
            continue
        h.update(str(p.relative_to(root)).encode())
        h.update(p.read_bytes())
    return h.hexdigest()
