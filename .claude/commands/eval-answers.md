---
description: Banc des réponses finales — fait répondre /paper-ask à un jeu de questions, à l'aveugle, puis note le run
argument-hint: [answers|answers_holdout] [nom du run]
allowed-tools: Read, Write, Agent, Bash(bin/pdb eval:*), Bash(ls:*), Bash(mkdir:*)
---

Arguments : $ARGUMENTS (défaut : `answers`, run nommé `<AAAA-MM-JJ>-<jeu>`).

Banc des réponses finales (`docs/EVAL.md` §10, lot A de `docs/AMELIORATIONS.md`). Il mesure
la réponse rédigée, pas le classement des passages.

1. **Questions, sans les attentes.** Lance `bin/pdb eval --questions <jeu>` : une ligne
   `id<TAB>question` par cas. N'ouvre jamais le fichier du jeu (`answers*.jsonl`) : il
   contient les sources et valeurs attendues, et la réponse doit être produite à l'aveugle.
2. **Dossier du run.** `eval/answers/<run>/` dans la base courante (créé au besoin). Les
   questions qui y ont déjà un `<id>.json` sont sautées : un run interrompu se reprend.
3. **Une question par agent.** Pour chaque question restante, un sous-agent (`sonnet`,
   en parallèle par lots de 4 au plus) reçoit uniquement : la base (`bases/<nom>/`), la
   consigne de suivre `.claude/commands/paper-ask.md` en **mode enregistrement**, la
   question, et le chemin `eval/answers/<run>/<id>.json`. Rien d'autre : ni catégorie, ni
   verdict attendu, ni sources.
4. **Contrôle.** Chaque fichier attendu existe. Relance une seule fois l'agent d'une
   question dont le fichier manque ; sinon, signale-la sans l'écrire toi-même.
5. **Notation.** `bin/pdb eval --answers eval/answers/<run> --save`. Les enregistrements non
   conformes sont listés en tête : corrige l'appel, pas le fichier.
6. **Notes humaines.** Crée `eval/answers/<run>/grades.csv` s'il n'existe pas, avec l'en-tête
   `id,exigences,soutien,conditions,limites` et une ligne par question, notes vides.
   L'utilisateur note de 0 à 2 ; relancer l'étape 5 les intègre.

Réponds par le tableau de `pdb eval`, les questions au verdict faux ou aux affirmations non
soutenues, et le chemin du run. Jeu `answers_holdout` : rapporte les chiffres, ne propose
aucun réglage du pipeline à partir de ses échecs.
