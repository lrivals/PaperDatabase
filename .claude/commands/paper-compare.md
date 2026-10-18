---
description: Compare des articles sur une question ou un axe (matrice, accords, désaccords, comparaisons impossibles), à partir de pdb compare et des passages sources
argument-hint: <question ou axe>
allowed-tools: Read, Grep, Write, Bash(bin/pdb compare:*), Bash(bin/pdb bench:*), Bash(bin/pdb claims:*), Bash(bin/pdb search:*), Bash(bin/pdb show:*), Bash(bin/pdb verify:*), Bash(bin/pdb paper:*)
---

Comparaison demandée : $ARGUMENTS

Compare les articles de la base sur cette question, sans classer des mesures qui ne se
comparent pas. Respecte les règles de `CLAUDE.md` ; le format des sorties de `pdb compare`
est dans `DATA_MODEL.md` §7.2.

1. **Exigences.** Écris pour toi 2 à 5 exigences (comme `/paper-ask`, étape 0) : les axes à
   comparer (précision, FPS, puissance, ressources…), la tâche, le jeu de données, les
   papiers visés.
2. **Chiffres.** Lance `bin/pdb compare --x <col> --y <col> [--task …] [--dataset …]
   [--metric …] [--paper A --paper B] --format json`. Axes : `accuracy_value`, `fps`, `gops`,
   `latency_ms`, `power_w`, `luts`, `dsps`, `bram`.
   - Ne compare qu'**à l'intérieur d'un groupe** (`groups`). Sa `confidence` (`forte`,
     `réservée`, `faible`) dit si la comparaison tient ; recopie-la.
   - `excluded` : chaque ligne écartée a son motif (`power_scope incompatible`, `métrique
     différente`, `x en n/r`, `seul papier du groupe`). Elles vont dans « Comparaisons
     impossibles », avec ce motif.
   - Aucun groupe : élargis un filtre une fois (sans `--dataset`, ou un autre axe), puis
     replie-toi sur `bin/pdb bench --comparable` et dis-le.
   - `confidence` d'une ligne (`high`/`medium`/`low`) mesure la transcription, pas la
     validité de la comparaison.
3. **Sources.** Pour chaque configuration retenue, remonte au passage original : son
   `chunk_id` s'il est rempli (`bin/pdb show`), sinon `bin/pdb search "<modèle> <plateforme>"
   --paper <id> -k 3`. Lis les `claims.jsonl` des papiers (`bin/pdb claims <id>`) quand ils
   existent : ils donnent les conditions de mesure déjà vérifiées. Les fiches servent à
   repérer les limites, jamais de source de chiffre.
4. **Vérification.** `bin/pdb verify <chunk_id> "<citation>"` sur chaque citation textuelle,
   avec les règles de `/paper-ask` (étape 5).
5. **Réponse.**
   - Verdict de suffisance (lot B) et exigences, comme `/paper-ask`.
   - **Matrice** : une ligne par configuration retenue (papier, méthode, plateforme, tâche,
     métrique, valeurs des deux axes, conditions de mesure, source), groupée par groupe
     `pdb compare`, avec la confiance du groupe.
   - **Accords** et **désaccords** entre papiers d'un même groupe, avec citations.
   - **Comparaisons impossibles** : lignes exclues et groupes séparés, avec la raison
     (portée, split, batch, métrique, valeur `n/r`).
   - **Limites** : preprints, `confidence: low`, métrique `~` non vérifiée.
6. Si l'utilisateur demande un fichier, écris `docs/comparaisons/<slug>.md` dans la base (seul
   fichier autorisé). N'écris jamais dans `benchmarks.csv`.
