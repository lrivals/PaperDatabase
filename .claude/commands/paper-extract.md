---
description: Extrait les preuves atomiques d'un article (claims.jsonl), chacune liée à un passage vérifié
argument-hint: <paper_id>
allowed-tools: Read, Write, Bash(bin/pdb paper:*), Bash(bin/pdb bench:*), Bash(bin/pdb search:*), Bash(bin/pdb show:*), Bash(bin/pdb verify:*), Bash(bin/pdb claims:*), Bash(.venv/bin/python bin/reindex.py --no-plot)
---

Écris `papers/$ARGUMENTS/claims.jsonl` : les preuves atomiques du papier, chacune reliée au
passage qui l'établit. Respecte les règles de `CLAUDE.md` et le contrat de `DATA_MODEL.md`
§12. Le thème de la base, qui dit quelles affirmations comptent, est dans `profile.md`.

## Sources

- `bin/pdb paper $ARGUMENTS` : la fiche doit être `done`. Sinon arrête-toi et propose
  `/paper-fiche $ARGUMENTS`.
- Lis `papers/<id>/fiche.md` : elle dit quoi extraire et où le chercher (`(Table 2)`, `(§IV-A)`).
- `bin/pdb bench --paper <id> --format json` : les lignes du papier, dans l'ordre du fichier.
  Leur rang (1, 2, …) est le `benchmark_row` d'une claim qui transcrit cette ligne.
- Passages : `bin/pdb search "<requête en anglais>" --paper <id> -k 5`, puis `bin/pdb show
  <chunk_id>`. N'ouvre `fulltext.md` que si la fiche et la recherche ne localisent pas une
  affirmation ; jamais `paper.pdf`.

## Claims

10 à 40 claims, sans doublon, en français (termes techniques en anglais). Une claim = une
affirmation vérifiable : un résultat avec ses conditions, un choix de méthode, une limite
reconnue, une hypothèse, un élément de contexte utile au thème.

Une ligne JSON par claim, numérotées `c01`, `c02`… :

```json
{"claim_id": "<paper_id>!c07", "kind": "résultat",
 "text": "Le détecteur atteint 45 FPS sur ZCU104 à 8 W (carte).",
 "voice": "auteurs",
 "source_chunk": "<chunk_id tel que pdb show l'affiche>", "chunk_sha1": "3f9a01bc",
 "excerpt": "<texte copié du passage>",
 "conditions": {"dataset": "COCO", "split": "val2017", "resolution": "416x416", "batch": "1",
                "precision": "INT8", "power_scope": "board", "protocol": "n/r"},
 "benchmark_row": 3, "caveats": ["mAP mesurée en flottant, pas sur la cible"]}
```

- `kind` : `résultat | méthode | limite | hypothèse | contexte`.
- `voice` : `auteurs` si le passage l'affirme ; `déduit` pour toute interprétation de ta part
  (comparaison non faite par les auteurs, limite qu'ils ne reconnaissent pas). Une claim
  `déduit` a quand même un passage : celui sur lequel repose l'inférence.
- `excerpt` : **copié** du passage affiché par `pdb show`, court (une phrase ou une ligne de
  tableau), avec ses nombres exacts. Coupe avec « … » plutôt que de reformuler.
- `chunk_sha1` : les 8 caractères hexadécimaux qui suivent `sha1:` dans l'en-tête de
  `pdb show`, sans le préfixe.
- `conditions` (surtout pour `résultat`) : clés utiles parmi `dataset`, `split`,
  `resolution`, `batch`, `precision`, `platform`, `power_scope`, `protocol` ; `n/r` si le
  papier ne le dit pas, jamais d'estimation. `power_scope` : `chip | board | board-dynamic |
  estimated | unspecified | n/r`, selon les règles de `benchmarks.csv` (DATA_MODEL §7). Une
  seule valeur : si le papier donne deux portées (P_chip et P_wall), `power_scope` suit la
  puissance citée en premier dans `text`, et `protocol` décrit les deux mesures.
- `benchmark_row` : seulement si la claim transcrit une ligne de `benchmarks.csv` (une
  seule : si elle en couvre plusieurs, une claim par ligne, ou le rang principal et les
  autres en `caveats`). C'est la même preuve, pas une confirmation.
- Chaque nombre de `text` doit se lire dans la section du passage, à la même valeur
  (« 12,3 » pour « 12.3 ») : `--check` note les autres (conversion, valeur d'un autre
  passage). Une valeur tirée d'un autre passage → une autre claim.
- `caveats` : réserves sur la mesure ou sa comparabilité (liste, facultative).
- Pas de claim sans passage : si tu ne retrouves pas le passage, n'écris pas la claim.

## Vérification

1. Pour chaque claim : `bin/pdb verify <source_chunk> "<excerpt>"`. `ABSENT` → recopie
   l'extrait depuis `pdb show` ou retire la claim ; `NOMBRES` → reprends les nombres exacts ;
   « trouvée dans … » → corrige `source_chunk` (et `chunk_sha1`).
2. Écris le fichier en entier (il remplace un `claims.jsonl` existant).
3. `bin/pdb claims <id> --check` doit finir sans ligne `erreur`.

Ne modifie ni `fiche.md`, ni `benchmarks.csv`, ni `metadata.json`. Si une claim contredit la
fiche ou une ligne du CSV, signale-le dans ton résumé sans corriger.

## Fin

En session directe : `.venv/bin/python bin/reindex.py --no-plot` (0 erreur). En sous-agent,
la réindexation reste à l'agent principal. Puis résume : nombre de claims par `kind`, part
de `déduit`, claims liées à `benchmarks.csv`, contradictions relevées avec la fiche ou le CSV.
