---
description: Ajoute un article à la base (arXiv id/URL ou PDF local), puis réindexe
argument-hint: <arxiv-id | url arXiv | chemin.pdf>
allowed-tools: Bash(.venv/bin/python bin/add.py:*), Bash(.venv/bin/python bin/reindex.py), Bash(bash bin/grobid.sh:*), Read, Grep
---

Ajoute l'article `$ARGUMENTS` à PaperDatabase.

1. `bash bin/grobid.sh status` ; s'il est inactif, `bash bin/grobid.sh start` (sinon
   l'ingestion passe en repli PyMuPDF avec des métadonnées à vérifier).
2. `.venv/bin/python bin/add.py $ARGUMENTS`. Si la commande refuse une URL non-arXiv, ne
   cherche **aucun** moyen de contourner un paywall : rappelle la procédure de dépôt manuel
   dans `inbox/` et arrête-toi.
3. Lis `papers/<paper_id>/metadata.json` du papier ingéré et rapporte :
   - titre, auteurs, année, venue, type, axes ;
   - chaque entrée de `extraction.warnings` ;
   - si l'article figure dans `basicStart.txt`, les écarts entre la note de départ (titre,
     auteurs, année, venue, chiffres annoncés) et ce que dit le PDF. Un écart signale une
     référence approximative : le dire explicitement.
4. `.venv/bin/python bin/reindex.py` et rapporte le compteur.

Réponds en français, brièvement. Termine en proposant `/paper-fiche <paper_id>`.
