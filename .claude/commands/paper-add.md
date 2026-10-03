---
description: Ajoute un article à la base (arXiv id/URL, DOI ou PDF local), puis réindexe
argument-hint: <arxiv-id | url arXiv | doi | chemin.pdf>
allowed-tools: Bash(.venv/bin/python bin/add.py:*), Bash(.venv/bin/python bin/reindex.py), Bash(bash bin/grobid.sh:*), Bash(bin/pdb base import:*), Read, Grep
---

Ajoute l'article `$ARGUMENTS` à la base courante (le dossier qui contient `base.json` ; son
thème est dans `profile.md`).

1. `bash bin/grobid.sh status` ; s'il est inactif, `bash bin/grobid.sh start` (sinon
   l'ingestion passe en repli PyMuPDF avec des métadonnées à vérifier).
2. `.venv/bin/python bin/add.py $ARGUMENTS` (un DOI est résolu vers sa version arXiv via
   OpenAlex). Si la commande refuse une URL non-arXiv ou un DOI sans version arXiv, ne
   cherche **aucun** moyen de contourner un paywall : rappelle la procédure de dépôt manuel
   dans `inbox/` (le PDF, plus l'export de citation `.bib` / `.ris` de l'éditeur, qui fixe
   auteurs, année et venue ; docs/GUIDE.md §4.5) et arrête-toi.
   Si elle répond « déjà dans la base X », l'article existe dans une autre de mes bases :
   lance la commande `bin/pdb base import X:<paper_id>` qu'elle indique (copie sans
   réextraction, fiche repassée à `todo`, pertinence à réévaluer), puis continue.
3. Lis `papers/<paper_id>/metadata.json` du papier ingéré et rapporte :
   - titre, auteurs, année, venue, type, axes ;
   - chaque entrée de `extraction.warnings` ;
   - s'il est importé (`imported_from`) : la base d'origine et le statut de sa fiche là-bas ;
   - si `basicStart.txt` existe et que l'article y figure, les écarts entre la note de départ (titre,
     auteurs, année, venue, chiffres annoncés) et ce que dit le PDF. Un écart signale une
     référence approximative : le dire explicitement.
4. `.venv/bin/python bin/reindex.py` et rapporte le compteur. Il refait aussi les figures
   périmées (ligne `Figures : …`) : ne lance pas `pdb plot` en plus.

Réponds en français, brièvement. Termine en proposant `/paper-fiche <paper_id>`.
