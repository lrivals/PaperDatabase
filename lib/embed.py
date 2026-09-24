"""Embeddings de papiers (sentence-transformers), avec cache disque.

Optionnel : `.venv/bin/pip install -r requirements-embed.txt`. Sans la dépendance,
available() renvoie False et lib/graph.py reste au TF-IDF.

Un papier = moyenne des embeddings normalisés de ses morceaux de texte (abstract + sections,
découpés en ~200 mots pour rester sous la fenêtre du modèle), renormalisée. Le cache
(<cache_dir>/<modèle>.npz) est indexé par id + sha1 du texte : un papier ré-extrait est
recalculé, les autres sont relus. Il vit hors de papers/ : la base n'est pas modifiée.
"""
import hashlib
import importlib.util
from pathlib import Path

import numpy as np

DEFAULT_MODEL = "all-MiniLM-L6-v2"
CHUNK_WORDS = 200

_models = {}


def available():
    return importlib.util.find_spec("sentence_transformers") is not None


def chunks(text, n=CHUNK_WORDS):
    words = text.split()
    return [" ".join(words[i:i + n]) for i in range(0, len(words), n)] or [""]


def _digest(text):
    return hashlib.sha1(text.encode()).hexdigest()


def _model(name):
    if name not in _models:
        from sentence_transformers import SentenceTransformer
        _models[name] = SentenceTransformer(name)
    return _models[name]


def _encode(texts, model):
    """Encode une liste de textes ; séparé pour être remplacé dans les tests."""
    return _model(model).encode(texts, normalize_embeddings=True, show_progress_bar=False)


def embed_papers(papers, model=DEFAULT_MODEL, cache_dir=None):
    """Matrice (n_papiers × dim) à lignes normalisées, dans l'ordre de `papers`.

    papers : dicts avec "id" et "text" (lib/graph.load_corpus).
    """
    texts = [p["text"] or p.get("title") or "" for p in papers]
    keys = [f"{p['id']}:{_digest(t)}" for p, t in zip(papers, texts)]

    cache = {}
    path = Path(cache_dir) / f"{model.replace('/', '_')}.npz" if cache_dir else None
    if path and path.exists():
        with np.load(path) as f:
            cache = {k: f[k] for k in f.files}

    missing = [i for i, k in enumerate(keys) if k not in cache]
    if missing:
        spans, flat = [], []
        for i in missing:
            cs = chunks(texts[i])
            spans.append((len(flat), len(flat) + len(cs)))
            flat += cs
        vecs = np.asarray(_encode(flat, model), dtype=np.float32)
        for i, (a, b) in zip(missing, spans):
            v = vecs[a:b].mean(axis=0)
            cache[keys[i]] = v / (np.linalg.norm(v) or 1.0)
        if path:
            path.parent.mkdir(parents=True, exist_ok=True)
            np.savez(path, **{k: cache[k] for k in keys})

    return np.vstack([cache[k] for k in keys]).astype(float)
