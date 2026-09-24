---
description: Met à jour gaps.md à partir des fiches done et de benchmarks.csv
allowed-tools: Read, Edit, Grep, Glob, Bash(.venv/bin/python bin/reindex.py)
---

Mets à jour `gaps.md`, la carte des verrous et zones non couvertes du corpus.

1. Lis `INDEX.md`, puis toutes les fiches `papers/*/fiche.md` dont le front-matter porte
   `fiche: done` (sections « Limites et critique », « Gaps identifiés », « Pertinence »), et
   `benchmarks.csv`.
2. Cherche les gaps selon plusieurs angles, tableau à l'appui quand c'est utile :
   - couverture croisée : axe × plateforme × tâche × toolflow — quelles cases sont vides
     dans `benchmarks.csv` ;
   - métriques systématiquement absentes (`n/r` fréquents : puissance, latence, BRAM…) ;
   - conditions de mesure non comparables d'un papier à l'autre ;
   - absence de code ou de bitstream publiés ;
   - limites récurrentes relevées dans les fiches.
3. Réécris `gaps.md` en gardant le format d'entrée décrit en tête du fichier. Pour chaque
   gap : les `paper_id` qui l'étayent, avec la section source ; le statut `hypothèse` ou
   `étayé`. Conserve les gaps existants encore valides, mets à jour leur statut, ne supprime
   un gap que si une fiche le contredit (et dis laquelle).
4. N'invente rien : un gap qui ne repose que sur l'absence de papiers dans la base reste une
   `hypothèse` — le corpus est petit et biaisé par la bibliographie de départ. Dis-le.

Si moins de ~10 fiches sont `done`, préviens que la carte est prématurée, puis fais-la quand
même sur ce qui existe.

Réponds par un résumé des gaps ajoutés / modifiés, et termine par 2-3 pistes concrètes
(papier à chercher, expérience à reproduire, question de thèse candidate).
