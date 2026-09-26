---
description: Répond à une question sur le corpus à partir de passages sourcés et vérifiés, sans lire fulltext.md
allowed-tools: Read, Bash(bin/pdb bench:*), Bash(bin/pdb search:*), Bash(bin/pdb show:*), Bash(bin/pdb paper:*), Bash(bin/pdb verify:*), Bash(bin/pdb cites:*), Bash(bin/pdb cited-by:*)
---

Question : $ARGUMENTS

Réponds à partir de la base uniquement, en dépensant le moins de tokens possible. La méthode
et les formats sont décrits dans `docs/RAG.md` ; ne le relis que si une commande te surprend.

1. **Chiffres d'abord (N0).** Si la question porte sur des performances (FPS, W, latence,
   ressources, précision), commence par `bin/pdb bench` avec des filtres et `--cols` ciblés.
   Une sortie de `bench` qui répond déjà se transmet telle quelle, en tableau. Pour une vue
   d'ensemble (qui mesure quoi, avec quelle portée), `--count paper_id,power_scope` résume
   sans lister les lignes.
2. **Passages (N1).** Sinon, ou en complément, lance `bin/pdb search "<question>" -k 8 --rerank`.
   - Le corpus est en anglais : formule la requête en anglais, et essaie une deuxième
     formulation si la première ne donne rien d'utile.
   - Restreins la recherche avec `--paper`, `--section` ou `--kind` quand la question le permet.
   - `search` renvoie toujours des passages, même quand la base ne traite pas le sujet :
     aucun score ne le détecte de façon fiable (docs/EVAL.md §5). Si aucun extrait ne répond
     à la question, dis que la base ne la traite probablement pas. Ne comble pas le vide par
     tes connaissances générales.
3. **Lecture.** `bin/pdb show` sur 2 ou 3 passages au plus, ceux dont l'extrait répond.
   N'ouvre jamais `fulltext.md` ni `paper.pdf`.
4. **Réponse.** Cite chaque affirmation sous la forme `[chunk_id]` (id court, par exemple
   `[1612.07119#019.3]`). Pour un chiffre de `bench`, cite `[paper, source_section]`.
5. **Vérification.** Lance `bin/pdb verify <chunk_id> "<citation>"` sur chaque citation
   textuelle entre guillemets.
   - Retire toute citation `ABSENT`.
   - `NOMBRES` : un chiffre de la citation n'est pas celui du passage. Reprends le chiffre
     exact avec `bin/pdb show`, ou retire la citation. Ne la garde jamais en l'état.
   - Corrige le `chunk_id` si la sortie dit « trouvée dans … ».
   - Une citation `APPROX` peut rester si elle est présentée comme une paraphrase.
6. **Structure.**
   - **Lu** : ce que les passages disent, avec leurs sources.
   - **Déduit** : tes rapprochements et inférences, sans citation.
   - **Non trouvé dans la base** : ce qui manque. Relie-le à `gaps.md` si c'est pertinent.

   Signale : `confidence: low` (lignes marquées `!`), les preprints (un seul appel pour
   tous les papiers cités : `bin/pdb paper id1 id2 … --fields short,type`), et les
   `power_scope` qui diffèrent entre les lignes que tu compares. Pour situer un papier dans
   sa lignée : `bin/pdb cites <id>` / `bin/pdb cited-by <id>`.
7. Termine par 2 ou 3 pistes : papier à lire, expérience, gap.

Réponds en français et garde les termes techniques en anglais. Ajoute en fin de réponse la
légende des ids courts utilisés (reprise du pied des sorties `# ids:`).
