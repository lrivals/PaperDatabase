---
description: Relit les tableaux extraits d'un article contre l'image de leur zone et propose des corrections (tables_review.md), sans toucher benchmarks.csv
argument-hint: <paper_id> [tableau]
allowed-tools: Read, Write, Bash(bin/pdb table:*), Bash(bin/pdb paper:*), Bash(bin/pdb bench:*), Bash(bin/pdb status:*)
---

Relecture des tableaux : $ARGUMENTS

Compare chaque tableau extrait (texte de `sections.jsonl`) à l'image de sa zone dans le PDF,
et propose des corrections. Respecte les règles de `CLAUDE.md`.

1. `bin/pdb table <paper_id>` : liste des tableaux, page, source du corps (`grobid`,
   `pymupdf`, `docling`, `docling-ocr`), zone connue ou non, signaux de qualité (lot E-d :
   `empty_cells`, `ragged`, `no_header`, `ocr_suspect`, `merged_numbers`,
   `caption_mismatch`). Si un tableau est donné en argument, ne traite que lui ; sinon,
   d'abord les tableaux signalés, puis ceux qui portent des lignes de `benchmarks.csv`
   (`bin/pdb bench --paper <id> --cols model,source_section`).
2. Pour chaque tableau : `bin/pdb table <paper_id> "<Table N>" --png`, puis `Read` de
   l'image écrite. Sans zone (`zone non`), l'image est la page entière : repère le tableau
   par sa légende.
3. Compare cellule par cellule : en-tête, unités, nombres (chiffres, séparateurs, signes),
   cellules fusionnées ou décalées, rangées manquantes, légende rattachée au bon tableau.
   L'image fait foi ; si elle est illisible, dis-le et ne propose rien pour ces cellules.
4. Écris `papers/<paper_id>/tables_review.md` (seul fichier autorisé), un bloc par tableau :

   ```markdown
   ## Table 3 (section #027, page 8, source grobid, signaux : ragged)
   Verdict : fidèle | corrections | inexploitable
   | rangée | colonne | extrait | image | remarque |
   |---|---|---|---|---|
   | B1024 | LUTs | 36.5k (16%) | 36.5k (16%) | — |
   Lignes de benchmarks.csv concernées : <rang, modèle, colonne, valeur actuelle → valeur image>
   Vérité terrain proposée (E-e) : {"paper_id": …, "label": "Table 3", "page": 8, "header": […], "rows": [[…]], "units": {…}}
   ```

   La ligne « Vérité terrain proposée » reprend le tableau entier, transcrit de l'image, au
   format de `eval/fixtures/tables_gold.jsonl` (DATA_MODEL §7.3). Elle n'entre dans ce
   fichier qu'après accord de l'utilisateur.
5. Garde-fous : n'écris jamais dans `benchmarks.csv` ni dans `sections.jsonl`. Une valeur
   de `benchmarks.csv` contredite par l'image est signalée ; elle se corrige ensuite, après
   accord, par `/paper-fiche`. Termine par un résumé de 3 lignes : tableaux relus, verdicts,
   corrections proposées.
