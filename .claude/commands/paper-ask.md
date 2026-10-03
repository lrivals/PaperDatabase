---
description: Répond à une question sur le corpus à partir de passages sourcés et vérifiés, sans lire fulltext.md
allowed-tools: Read, Write, Bash(bin/pdb bench:*), Bash(bin/pdb search:*), Bash(bin/pdb show:*), Bash(bin/pdb paper:*), Bash(bin/pdb verify:*), Bash(bin/pdb cites:*), Bash(bin/pdb cited-by:*)
---

Question : $ARGUMENTS

Réponds à partir de la base uniquement, en dépensant le moins de tokens possible. La méthode
et les formats sont décrits dans `docs/RAG.md` ; ne le relis que si une commande te surprend.

0. **Exigences.** Avant toute recherche, écris pour toi 2 à 5 exigences : ce qu'une réponse
   complète doit établir (une valeur, sa plateforme, une condition de mesure, une
   comparaison, une méthode…). Elles reprennent ce que la question demande, sans plus : un
   détail qu'elle ne demande pas (protocole commun, budget mémoire de chaque méthode…) va
   dans les limites de la réponse, pas dans les exigences.
1. **Chiffres d'abord (N0).** Si la question porte sur des performances (FPS, W, latence,
   ressources, précision), commence par `bin/pdb bench` avec des filtres et `--cols` ciblés.
   Une sortie de `bench` qui répond déjà se transmet telle quelle, en tableau. Pour une vue
   d'ensemble (qui mesure quoi, avec quelle portée), `--count paper_id,power_scope` résume
   sans lister les lignes. Avant de **comparer des chiffres de plusieurs papiers**, lance les
   mêmes filtres avec `--comparable` (`--comparable power` pour des puissances) : ne compare
   qu'à l'intérieur d'un groupe ; des lignes de groupes différents (« comparaisons
   impossibles » : autre métrique, autre split, autre portée) se citent côte à côte en disant
   pourquoi elles ne se comparent pas, et une métrique marquée `~` a une définition non
   vérifiée (limite à signaler).
2. **Passages (N1).** Sinon, ou en complément, lance `bin/pdb search "<question>" -k 8 --rerank`.
   - Le moteur est choisi par `search` : CPU par défaut, Qwen sur GPU si l'utilisateur a
     activé la route GPU (`bin/pdb gpu on`). Ne force pas `--gpu` ; une ligne
     `# route GPU indisponible` sur stderr n'est pas une erreur (la recherche a répondu sur CPU).
   - Le corpus est en anglais : formule la requête en anglais, et essaie une deuxième
     formulation si la première ne donne rien d'utile.
   - Restreins la recherche avec `--paper`, `--section` ou `--kind` quand la question le permet.
   - `search` renvoie toujours des passages, même quand la base ne traite pas le sujet :
     aucun score ne le détecte de façon fiable (docs/EVAL.md §5). C'est le contenu des
     extraits qui décide (étape 6). Ne comble jamais un vide par tes connaissances générales.
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
6. **Suffisance.** Marque chaque exigence :
   - `couvert` : établie par un passage vérifié (étape 5) ou une ligne de `bench` ;
   - `partiel` : seul un passage voisin existe (autre plateforme, autre batch, autre
     précision, autre portée de puissance, autre jeu de données) ;
   - `absent` : rien trouvé.

   Verdict : `suffisant` si **toutes** les exigences sont `couvert` ; `absent` si **toutes**
   sont `absent` ; `partiel` dans tous les autres cas (une seule exigence `partiel` ou
   `absent` suffit à exclure `suffisant`).
7. **Structure.** La réponse s'ouvre par le verdict, puis les exigences :

   ```
   **Verdict : partiel** — 2 exigences couvertes sur 3
   - FPS de Y sur ZCU104 : couvert
   - puissance et sa portée : partiel (puissance puce seulement)
   - batch : absent
   ```

   - **Lu** : ce que les passages disent, avec leurs sources.
   - **Déduit** : tes rapprochements et inférences, sans citation.
   - **Non trouvé dans la base** : les exigences `absent`, et ce qui manque aux `partiel`.
     Relie-les à `gaps.md` si c'est pertinent.

   Verdict `absent` : dis que la base ne traite pas le sujet, et rappelle que cela ne dit pas
   que la littérature ne le traite pas (même prudence que `gaps.md`) ; propose
   `/paper-discover`. Pas de section **Lu** inventée pour remplir.

   Signale : `confidence: low` (lignes marquées `!`), les preprints (un seul appel pour
   tous les papiers cités : `bin/pdb paper id1 id2 … --fields short,type`), et les
   `power_scope` qui diffèrent entre les lignes que tu compares. Pour situer un papier dans
   sa lignée : `bin/pdb cites <id>` / `bin/pdb cited-by <id>`.
8. Termine par 2 ou 3 pistes : papier à lire, expérience, gap. Si la base ne suffit pas,
   propose `/paper-discover` ; `/paper-research` (acquisition open access) seulement si
   l'utilisateur utilise la route GPU.

Réponds en français et garde les termes techniques en anglais. Ajoute en fin de réponse la
légende des ids courts utilisés (reprise du pied des sorties `# ids:`).

**Mode enregistrement** (banc des réponses finales, `docs/EVAL.md` §10). Si la demande
contient `--record <fichier.json>`, retire-le de la question, réponds normalement, puis écris
ce fichier (et aucun autre) :

```json
{"id": "<nom du fichier sans .json>", "q": "<question>", "verdict": "suffisant|partiel|absent",
 "requirements": [{"text": "<ce qu'une réponse complète doit établir>", "status": "couvert|partiel|absent"}],
 "claims": [{"text": "<affirmation, telle que dans la réponse>", "kind": "lu|déduit",
             "citations": [{"id": "<chunk_id>", "excerpt": "<extrait exact, vérifié par pdb verify>"},
                           {"paper": "<id>", "source_section": "<Table 2>"}]}]}
```

- `requirements` et `verdict` : ceux de l'étape 6, tels qu'annoncés en tête de réponse.
- Une affirmation `lu` a au moins une citation : passage (`id` + `excerpt` copié du passage
  et accepté par `pdb verify`, avec le `chunk_id` corrigé si la sortie dit « trouvée dans
  … ») ou ligne de `bench` (`paper` + `source_section`). Une affirmation `déduit` n'en a pas.
- Les nombres s'écrivent dans `text` avec leur unité, comme dans la réponse.
