"""Réparation des ligatures perdues à l'extraction (« classi cation », « e cient », « the rst »).

Certains PDF encodent fi, ff, fl, ffi, ffl par un glyphe sans équivalent Unicode : le texte
extrait perd ces lettres et coupe le mot. Deux réparations, dans cet ordre :
  - jonction : « A B » → A + lig + B (« e cient » → « efficient ») ;
  - début de mot : « B » → lig + B (« the rst » → « the first »).
Une réparation n'a lieu que si le mot obtenu est connu et que le fragment (A ou B) ne l'est
pas : deux vrais mots voisins ne sont jamais collés.

« Connu » = présent dans au moins MIN_PAPERS papiers du corpus, ou dans la liste intégrée
KNOWN. Un fragment n'apparaît que dans les papiers abîmés : s'ils sont rares, il n'est pas
connu. Bibliothèque standard seulement.
"""
import json
import re
from pathlib import Path

LIGATURES = ("ffi", "ffl", "ff", "fi", "fl")
MIN_PAPERS = 2

# Mots fréquents du domaine qui contiennent une ligature (le corpus complète la liste).
KNOWN = frozenset("""
efficient efficiency efficiently inefficient inefficiency classification classifications
classifier classifiers classify classified misclassification configuration configurations
configurable reconfigurable reconfiguration configure configured significant significantly
different difference differences differs differ offer offers offered buffer buffers
buffered buffering effect effects effective effectively affine field fields first find
finds fine finer final finally fixed flow flows dataflow overflow float floating filter
filters filtering filtered flexible flexibility define defined definition benefit benefits
specific specifically specification quantification identify identified identification
figure figures offload offloading off offset traffic suffer sufficient difficult
""".split())

# Fragments typiques d'un mot abîmé : leur présence après réparation mérite un avertissement.
FRAGMENTS = frozenset("cient ciency cation cations guration gurations cant cantly rst".split())

_WORD = re.compile(r"[A-Za-z]+")


def words(text):
    return {w.lower() for w in _WORD.findall(text or "")}


def corpus_vocabulary(root, min_papers=MIN_PAPERS):
    """Mots présents dans au moins min_papers papiers (sections.jsonl), plus KNOWN."""
    counts = {}
    for path in Path(root, "papers").glob("*/sections.jsonl"):
        seen = set()
        for line in path.read_text().splitlines():
            if line.strip():
                seen |= words(json.loads(line).get("text"))
        for w in seen:
            counts[w] = counts.get(w, 0) + 1
    return {w for w, n in counts.items() if n >= min_papers} | KNOWN


def _case(word, like):
    return word[0].upper() + word[1:] if like[:1].isupper() else word


def _alone(b, vocab):
    """lig + b s'il est connu (« rst » → « first ») ; sinon None."""
    return next((lig + b for lig in LIGATURES if lig + b in vocab), None)


def repair(text, vocab):
    """(texte réparé, nombre de réparations). vocab : mots connus, en minuscules."""
    if not text:
        return text, 0
    tokens = list(_WORD.finditer(text))
    out, pos, n, i = [], 0, 0, 0
    while i < len(tokens):
        m = tokens[i]
        a = m.group()
        nxt = tokens[i + 1] if i + 1 < len(tokens) else None
        # jonction « A B » (un seul espace entre les deux, B en minuscules). Si A est un vrai
        # mot et que B se répare seul, la réparation seule l'emporte : « a ne-tuning » →
        # « a fine-tuning », pas « affine-tuning » ; « Roo ine » → « Roofline ».
        if nxt and text[m.end():nxt.start()] == " " and nxt.group().islower():
            b = nxt.group()
            if a.lower() not in vocab or (b not in vocab and not _alone(b, vocab)):
                joined = next((a.lower() + lig + b for lig in LIGATURES
                               if a.lower() + lig + b in vocab), None)
                if joined:
                    out += [text[pos:m.start()], _case(joined, a)]
                    pos, n, i = nxt.end(), n + 1, i + 2
                    continue
        # début de mot perdu : « rst » → « first » (minuscules seulement, hors URL)
        before, after = text[m.start() - 1:m.start()], text[m.end():m.end() + 1]
        if a.islower() and a not in vocab and before not in ("/", ".") and after != "/":
            fixed = _alone(a, vocab)
            if fixed:
                out += [text[pos:m.start()], fixed]
                pos, n = m.end(), n + 1
        i += 1
    out.append(text[pos:])
    return "".join(out), n


def leftover(text):
    """Nombre de fragments typiques restés dans le texte (hors césure « signifi-\ncantly »)."""
    text = text or ""
    return sum(1 for m in _WORD.finditer(text) if m.group().lower() in FRAGMENTS
               and not text[:m.start()].rstrip().endswith("-"))


def repair_blocks(blocks, vocab):
    """Répare les paragraphes des blocs (lib/doc.Block) en place.
    Retourne (réparations, fragments restants)."""
    fixed = left = 0
    for b in blocks:
        paras = []
        for t, page in b.paras:
            t, k = repair(t, vocab)
            fixed += k
            paras.append((t, page))
        b.paras = paras
        left += leftover("\n\n".join(t for t, _ in paras))  # césure d'un paragraphe à l'autre
        for attr in ("section", "subsection", "heading"):
            v = getattr(b, attr)
            if v:
                setattr(b, attr, repair(v, vocab)[0])
    return fixed, left
