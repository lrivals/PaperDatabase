# Feuille de route : fiabilité des réponses, tableaux et nouveaux skills

Spécification du 02/10/2026. État : lots A et B en place (même date) ; lot D en place
(03/10/2026) ; lot G en grande partie fait (route unique, RAG.md §13) ; autres lots non commencés (lot I, journal des
sous-agents, spécifié le 02/10/2026). Elle décrit comment mettre en place les
améliorations issues de l'analyse du système : réponses qui reconnaissent des preuves
incomplètes, comparaisons numériques qui gardent leurs conditions, tableaux contrôlables, et
cinq nouveaux skills. Chaque chantier part d'un constat mesuré dans le dépôt, puis donne la
conception, les fichiers touchés, les formats et le critère d'acceptation.

Suivi : [SETUP.md §9](../SETUP.md#9-état-actuel-et-tâches-à-faire), « Tâches — outillage ».
Banc d'évaluation : [EVAL.md](EVAL.md). Schémas : [DATA_MODEL.md](../DATA_MODEL.md).

## Sommaire

0. [Principes](#0-principes)
1. [Lot A — Évaluation des réponses finales](#lot-a--évaluation-des-réponses-finales)
2. [Lot B — Suffisance des preuves](#lot-b--suffisance-des-preuves)
3. [Lot C — Preuves atomiques (`claims.jsonl`)](#lot-c--preuves-atomiques-claimsjsonl)
4. [Lot D — Conditions de comparaison dans `benchmarks.csv`](#lot-d--conditions-de-comparaison-dans-benchmarkscsv)
5. [Lot E — Tableaux](#lot-e--tableaux)
6. [Lot F — Recherche en français](#lot-f--recherche-en-français)
7. [Lot G — Une route de recherche de référence](#lot-g--une-route-de-recherche-de-référence)
8. [Lot H — Provenance des réponses](#lot-h--provenance-des-réponses)
9. [Lot I — Journal et coût des sous-agents](#lot-i--journal-et-coût-des-sous-agents)
10. [Lot J — Outil de comparaison `pdb compare`](#lot-j--outil-de-comparaison-pdb-compare)
11. [Nouveaux skills](#9-nouveaux-skills)
12. [Ordre de mise en œuvre](#10-ordre-de-mise-en-œuvre)
13. [Hors périmètre](#11-hors-périmètre)

---

## 0. Principes

- **Les fichiers texte restent la source de vérité.** Tout nouvel artefact (`claims.jsonl`,
  qualité de tableau, journal de réponses) est soit versionné et lisible, soit dérivé et
  reconstructible dans `.cache/`.
- **Rien n'entre dans `benchmarks.csv` sans relecture humaine.** Un tableau reconstruit par
  PyMuPDF ou Docling, une cellule OCR, une valeur proposée par un skill restent des
  propositions.
- **Une fiche, une ligne CSV et le papier ne sont pas trois sources.** Ils remontent au même
  passage ; seul le passage original compte comme preuve.
- **Tout gain se prouve sur le banc.** `bin/pdb eval --save` avant, changement,
  `bin/pdb eval --compare` après, sur dev **et** holdout. On ne règle jamais un paramètre
  sur un holdout.
- **Compatibilité.** Les champs ajoutés sont optionnels ; une base existante reste valide
  sans migration (`bin/reindex.py` à 0 erreur).

---

## Lot A — Évaluation des réponses finales

> **En place le 02/10/2026** : `pdb eval --answers` / `--questions`, `lib/evaluation.py`
> (`answer_quality`), mode `--record` de `/paper-ask`, skill `/eval-answers`, jeux de départ
> fpga (12 + 12 questions). Protocole et formats : [EVAL.md §10](EVAL.md#10-réponses-finales-pdb-eval---answers-02102026).
> Premier run le 02/10/2026, en lexical seul : verdict juste 0,83 (dev) et 0,92 (holdout),
> hors corpus reconnu 6/6 (EVAL.md §10). Reste : run hybride + rerank et second run
> (variance), sources alternatives dans les jeux, frontière suffisant / partiel des
> questions de synthèse, jeux complets (40 / 60) relus par un tiers, jeux des bases drone et
> stage, notes humaines, seuils.

**Constat.** Le banc mesure l'extraction, le classement des passages et `verify`, mais pas la
réponse rédigée : « pas d'évaluation de bout en bout de `/paper-ask` » (EVAL.md §7). Or le
classement ne prédit pas la qualité de la réponse : recall@5 hybride 0,90 sur dev, 0,84 sur
holdout, 0,50 en français (EVAL.md §5), et aucun seuil de score ne sépare les questions hors
corpus (0/10 signalées, EVAL.md §5-6). Ce lot est le prérequis des autres : sans lui, aucun
changement de modèle ou de format ne peut être jugé sur ce qui compte.

**Conception.**

1. Jeux de questions par base, `bases/<nom>/eval/fixtures/answers.jsonl` (dev) et
   `answers_holdout.jsonl`, en quatre catégories équilibrées :

   | Catégorie | Exemple de forme | Ce qu'on vérifie |
   |---|---|---|
   | `simple` | « Quelle méthode de quantification utilise X ? » | fait sourcé |
   | `numeric` | « FPS et puissance de Y sur ZCU104 à batch 1 ? » | valeur, unité, conditions |
   | `synthesis` | « Quelles approches de CL tiennent sur MCU ? » | couverture multi-papiers |
   | `absent` | question proche du thème mais non couverte | refus ou réponse partielle |

   Schéma d'une ligne (compatible avec `paths()` de `lib/evaluation.py:40`, qui cherche déjà
   `eval/fixtures/*.jsonl` dans la base) :

   ```json
   {"q": "…", "category": "numeric",
    "required": ["fps de Y sur ZCU104", "puissance et sa portée", "batch"],
    "gold_sources": ["<paper_id>#017"],
    "gold_values": [{"field": "fps", "value": "45.2", "unit": "FPS"}],
    "expected_verdict": "suffisant"}
   ```

   `expected_verdict` ∈ `suffisant | partiel | absent` (lot B). Taille visée : 40 questions
   dev, 60 holdout par base, écrites ou relues par quelqu'un d'autre que l'auteur du code
   (recommandation déjà faite dans RAG_IMPLEMENTATION_PLAN.md).

2. Enregistrement de réponse : le skill écrit un JSON aligné sur celui de
   `pdb rag check-answer` (SETUP.md §10) pour ne pas créer un troisième format :

   ```json
   {"q": "…", "snapshot": "<empreinte>", "verdict": "partiel",
    "requirements": [{"text": "fps de Y sur ZCU104", "status": "couvert"}],
    "claims": [{"text": "…", "kind": "lu|déduit",
                "citations": [{"id": "<chunk_id>", "excerpt": "…"}]}]}
   ```

3. Notation, `bin/pdb eval --answers <dossier de réponses>` dans `lib/evaluation.py` :
   - **automatique** : citations valides (`rag.verify` sur chaque `excerpt`, statut `OK` ou
     `APPROX` sans écart de nombres), sources attendues citées, valeurs de `gold_values`
     présentes avec leur unité, justesse du verdict (matrice 3 × 3) ;
   - **humaine**, grille courte à 0/1/2 par réponse : exigences couvertes, affirmations
     soutenues par leur passage, conditions de mesure explicites, limites signalées. Les
     notes vont dans `eval/answers/<run>/grades.csv`.

**Fichiers.** `lib/evaluation.py` (nouvelle fonction `answer_quality`), `bin/pdb.py`
(option `--answers`), `eval/thresholds.json` (seuils `answers.*`), fixtures par base,
`tests/test_evaluation.py`. Pas de LLM dans le banc : les réponses sont produites à part,
par le skill, puis notées.

**Acceptation.** Run de référence enregistré par base ; aucun seuil fixé avant d'avoir deux
runs pour mesurer la variance.

---

## Lot B — Suffisance des preuves

> **En place le 02/10/2026** : exigences, statut par exigence et verdict dans chaque réponse
> de `/paper-ask` (plus seulement en mode `--record`), même règle dans `/paper-research`,
> format des réponses des `CLAUDE.md` de base. Acceptation atteinte sur fpga (second run du
> banc, lexical seul) : 6/6 hors corpus `absent`, 0 faux `absent` ; 22 verdicts sur 24
> stables d'un run à l'autre. Reste : frontière suffisant / partiel des questions de
> synthèse dans le jeu ([EVAL.md §10](EVAL.md#second-run-lot-b-02102026)).

**Constat.** `pdb search` renvoie toujours des passages, même hors sujet ; l'alerte
« pertinence faible » a été retirée faute de signal fiable (EVAL.md §6, commentaire en tête
de `lib/rag.py`). La décision doit donc porter sur le **contenu** des passages, pas sur un
score.

**Conception.** Dans `/paper-ask` :

1. Avant la recherche, décomposer la question en 2 à 5 **exigences** (ce qu'une réponse
   complète doit établir : valeur, plateforme, condition, comparaison…).
2. Après `search` / `show` / `verify`, marquer chaque exigence `couvert` (passage vérifié),
   `partiel` (passage voisin : autre plateforme, autre batch, portée de puissance
   différente) ou `absent`.
3. Verdict global : `suffisant` si toutes sont couvertes, `absent` si aucune, `partiel`
   sinon. Il ouvre la réponse, avant les sections **Lu / Déduit / Non trouvé dans la base**,
   et la section « Non trouvé » liste les exigences `absent`.
4. Un verdict `absent` ne dit pas que la littérature ne traite pas le sujet ; la réponse le
   rappelle et propose `/paper-discover` (même prudence que `gaps.md`).

**Fichiers.** `.claude/commands/paper-ask.md`, `.claude/commands/paper-research.md` (même
règle), `templates/CLAUDE.base.md` et les `CLAUDE.md` de base (format de réponse).

**Acceptation.** Sur les questions `absent` du lot A : ≥ 80 % de verdicts `absent` ou
`partiel` ; sur les autres : ≤ 10 % de `absent` à tort. Mêmes seuils d'adoption que ceux
utilisés pour `low_relevance` (`lib/evaluation.py:397`).

---

## Lot C — Preuves atomiques (`claims.jsonl`)

**Constat.** La fiche (`fiche.md`) est un résumé de lecture ; les chiffres y portent leur
source (`(Table 2)`), mais pas les affirmations qualitatives (méthode, limite, hypothèse), ni
leurs conditions. Une réponse ou une section d'état de l'art doit retrouver le passage
original, ce qui coûte une recherche par affirmation.

**Conception.** Un fichier par papier, `papers/<id>/claims.jsonl`, produit par
`/paper-extract` (§9) :

```json
{"claim_id": "<paper_id>!c07", "kind": "résultat",
 "text": "Le détecteur atteint 45 FPS sur ZCU104 à 8 W (carte).",
 "voice": "auteurs",
 "source_chunk": "<paper_id>#017.0", "excerpt": "…texte exact…",
 "conditions": {"dataset": "COCO", "split": "val2017", "resolution": "416x416",
                "batch": "1", "precision": "INT8", "power_scope": "board",
                "protocol": "n/r"},
 "benchmark_row": 3, "caveats": ["mAP mesurée en flottant, pas sur la cible"]}
```

- `kind` ∈ `résultat | méthode | limite | hypothèse | contexte` ; `voice` ∈ `auteurs | déduit`
  (une interprétation du lecteur reste marquée comme telle).
- `conditions` reprend la convention `n/r` (en tête de DATA_MODEL.md) ; jamais d'estimation.
- `benchmark_row` relie la preuve à la ligne de `benchmarks.csv` qui la transcrit (rang de la
  ligne parmi celles du papier) : c'est la même preuve, pas une confirmation.
- `bin/reindex.py` valide le schéma (`lib/schema.py`, nouvelle `validate_claim_row`) et
  contrôle chaque `excerpt` par `rag.verify` contre `source_chunk` ; un `excerpt` `ABSENT` ou
  `NOMBRES` est une erreur, `MODIFIÉ` (passage ré-extrait) un avertissement.
- `lib/rag.py` peut indexer les claims comme type de passage `claim` **renvoyant** à leur
  `source_chunk` ; la citation finale reste le passage, jamais le claim.

**Fichiers.** `lib/schema.py`, `bin/reindex.py`, `lib/rag.py` (optionnel), `DATA_MODEL.md`
(nouvelle section), `tests/test_schema.py`, `tests/test_reindex.py`,
`.claude/commands/paper-extract.md`.

**Acceptation.** 100 % des `excerpt` vérifiés à la réindexation ; sur le lot A, catégorie
`synthesis`, la couverture des exigences progresse sans baisse de la validité des citations.

---

## Lot D — Conditions de comparaison dans `benchmarks.csv`

> **D-1 à D-4 en place le 03/10/2026** : `schema.OPTIONAL_COLUMNS` et `schema.check_header`,
> utilisés par `reindex`, `rag_qwen` et l'import entre bases (`lib/xbase.py`, qui écrit
> désormais avec l'en-tête de la base cible) ; `pdb bench --add-columns` pour étendre
> l'en-tête à la demande (`reindex` ne touche jamais le CSV) ; `pdb bench --check`, avec les
> statuts `passage` / `section` / `converti` (lu via `original_value`) / `absent` /
> `introuvable` ; mesure `in_cited_chunk` du banc `table_values` ; `/paper-fiche`. Les trois
> bases réindexent sans erreur avec leur CSV inchangé. `pdb synth` écrit ses propres CSV à
> 20 colonnes, toujours valides.
>
> **D-5 en place le 03/10/2026** : `pdb bench --comparable [accuracy|power]`
> (`query.comparable_groups`, `impossible_comparisons`) ; consigne dans `/paper-ask` avant
> toute comparaison entre papiers. Écarts à la conception : la métrique est `metric_def` à
> défaut `accuracy_metric` (marquée `~`), et `power_scope` n'entre dans la clé qu'en mode
> `power`, où la métrique en sort ; normalisation limitée à la casse et aux espaces.

**Constat.** `benchmarks.csv` a 20 colonnes fixes (`lib/schema.py:22`). Le jeu de données y
figure, mais pas le split, la résolution, le batch, la définition exacte de la métrique ni
le protocole de mesure, qui restent dans la fiche ou dans `source_section`. Deux lignes
peuvent alors sembler comparables sans l'être. `gaps.md` (fpga) note aussi que le schéma
représente mal les métriques de sûreté. Enfin, la traçabilité s'arrête à la section :
la piste « colonne `chunk_id` » de SETUP §9 (26/09/2026) n'est pas faite.

**Conception.**

1. Colonnes **optionnelles**, après les 20 actuelles, dans `schema.OPTIONAL_COLUMNS` :

   | Colonne | Contenu | Exemple |
   |---|---|---|
   | `chunk_id` | passage qui contient la valeur | `2108.03986#041.0` |
   | `metric_def` | définition exacte de `accuracy_metric` | `mAP@0.5:0.95, COCO protocol` |
   | `dataset_split` | split évalué | `val2017` |
   | `input_res` | résolution d'entrée | `416x416` |
   | `batch` | taille de batch | `1` |
   | `measure_protocol` | comment FPS/puissance sont mesurés | `wattmètre carte, moyenne 60 s` |
   | `original_value` | valeur telle qu'écrite, si une colonne est normalisée | `12.3 mJ/frame` |

   Une colonne optionnelle absente vaut `n/r` ; présente, elle suit les mêmes règles
   (`n/r` plutôt que vide).

2. Contrôle d'en-tête assoupli : les 20 colonnes obligatoires en tête et dans l'ordre, puis
   un sous-ensemble des optionnelles. Trois endroits comparent aujourd'hui l'en-tête au
   tuple exact et sont à modifier ensemble : `bin/reindex.py:111`, `lib/rag_qwen.py:165`,
   `bin/bench_cli.py` (en-tête écrit l. 137 et 830, schéma JSON l. 356-359, invite l. 789).
   `lib/query.py` lit déjà l'en-tête du fichier et n'a pas à changer.

3. `pdb bench --check` : pour chaque ligne qui a un `chunk_id`, vérifier que chaque valeur
   numérique apparaît dans le passage (`rag.number_tokens`, `lib/rag.py:358`). Le banc
   `table_values` (`lib/evaluation.py:251`) gagne une mesure « valeur dans le passage cité ».

4. `/paper-fiche` renseigne les nouvelles colonnes pour les nouvelles lignes ; les anciennes
   restent à `n/r` et sont complétées au fil des relectures (pas de migration de masse).

5. `pdb bench` : option `--comparable` qui regroupe les lignes par (`task`, `dataset`,
   `dataset_split`, `metric_def`, `power_scope`) et signale les comparaisons impossibles.

**Fichiers.** `lib/schema.py`, `bin/reindex.py`, `lib/rag_qwen.py`, `bin/bench_cli.py`,
`lib/query.py` (`--check`, `--comparable`), `DATA_MODEL.md` §7, `paper-fiche.md`,
`tests/test_schema.py`, `tests/test_query.py`, `tests/test_bench.py`.

**Acceptation.** Les trois bases réindexent sans erreur sans toucher à leur CSV ; un CSV avec
colonnes optionnelles passe `reindex`, `pdb bench`, `pdb rag benchmarks` et `pdb synth`.

---

## Lot E — Tableaux

**Constat.**

- Extraction en deux temps : PyMuPDF `find_tables()` sur la page de la légende
  (`lib/tables.py:95`), puis Docling sur **tout le PDF** si des tableaux restent sans corps,
  OCR activé par papier (`lib/docling_tables.py:27-34`). Les tableaux reconstruits portent
  la mention « à vérifier ».
- Le taux de tableaux avec corps atteint 0,87 (fpga) et 0,90 (drone) (EVAL.md §9), mais il
  mesure la **présence** d'un corps, pas l'exactitude des cellules. Défauts connus : cui
  Table 9 (colonnes perdues), hozhabr Table 5 (fragments OCR) et Tables 9-10 (paysage),
  FINN Table 3 (colonnes décalées), 2512.01463 Table 3 (DSP/LUT inversés ?). Restent 31 + 24
  tableaux sans corps (SETUP §9, point 8).
- La page et la bbox Docling restent dans `docling_tables.json` ; `sections.jsonl` ne garde
  que la page de la légende. Aucun rendu d'image de page n'existe dans le code.
- Dans l'index CPU, un tableau de plus de 250 mots est découpé en fenêtres de 200 mots
  (`lib/rag.py:28`, `split_text` l. 78) : les fenêtres suivantes perdent légende et en-tête,
  et les sauts de ligne. Les 2 questions holdout sur tableaux restent manquées, même après
  Docling (EVAL.md §6).
- Seuls signaux de qualité : les avertissements `WARN_TABLES_*` de `metadata.json`
  (`lib/schema.py:55-57`), par papier.

**Conception**, en cinq volets indépendants :

**E-a. Localisation conservée.** `sections.jsonl`, lignes `kind: "table"` : champs
optionnels `bbox` (`[x0, y0, x1, y1]`, points, origine en haut à gauche) et `table_source`
(`grobid | pymupdf | docling | docling-ocr`). Ils viennent de la bbox TEI (déjà lue,
`lib/doc.py:24`), du tableau PyMuPDF retenu ou de l'entrée Docling appariée. Validation dans
`schema.validate_section_row`.

**E-b. OCR ciblé par zone.** `pdb ingest --reparse --tables docling --ocr` ne traite plus le
PDF entier : pour chaque tableau sans corps, on recadre la zone (page de la légende, bbox
élargie vers le bas jusqu'au bloc suivant), on la rend en image (`page.get_pixmap(clip=…,
dpi=200)` de PyMuPDF) et on lance Docling sur cette image seule. Gains attendus : temps
(1 h 15 pour 40 papiers aujourd'hui, EVAL.md §9) et moins d'appariements erronés, puisque
légende et zone sont liées dès le départ. Le cache garde `{page, bbox, dpi, ocr}` pour
chaque recadrage. L'appariement actuel par numéro et par rang (`recover`, l. 85) reste le
repli.

**E-c. Tableaux lisibles dans l'index.** Dans `rag.load_chunks`, découper les tableaux par
**lignes** et non par mots, et répéter « légende + ligne d'en-tête » en tête de chaque
fenêtre. Le texte encodé (`encoded_text`, l. 109) préfixe aussi l'unité quand l'en-tête la
donne. `lib/rag_qwen.py` garde ses tableaux entiers ; seul le préfixe change.

**E-d. Indicateurs de qualité par tableau.** Calculés à l'extraction, rangés dans
`docling_tables.json` (`quality`) et repris par `pdb status` :

| Signal | Règle | Effet |
|---|---|---|
| `empty_cells` | part de cellules vides > 30 % | relecture |
| `ragged` | nombre de cellules variable d'une ligne à l'autre | relecture |
| `no_header` | 1re ligne majoritairement numérique | relecture |
| `ocr_suspect` | caractères hors alphabet, `O`/`0`, `l`/`1` dans un nombre | relecture |
| `merged_numbers` | nombre collé à un autre (« 12361k0.31 ») | relecture |
| `caption_mismatch` | appariement par rang plutôt que par numéro | relecture |

Un tableau signalé apparaît en tête de « tableaux à vérifier » dans `pdb status`.

**E-e. Vérité terrain des tableaux.** Une vingtaine de tableaux annotés à la main, défauts
connus compris, dans `bases/<nom>/eval/fixtures/tables_gold.jsonl` :
`{"paper_id", "label": "Table 3", "page", "header": [...], "rows": [[...]], "units": {...}}`.
`pdb eval --extract` mesure séparément : détection (le tableau a un corps), rattachement à
la bonne légende, exactitude des cellules (égalité après normalisation des nombres), unités
conservées. Le taux « tableaux avec corps » reste affiché mais n'est plus le seul indicateur.

**Fichiers.** `lib/tables.py`, `lib/docling_tables.py`, `lib/doc.py`, `bin/ingest.py`,
`lib/rag.py`, `lib/schema.py`, `lib/status.py`, `lib/evaluation.py`, `DATA_MODEL.md`
(`sections.jsonl`, `docling_tables.json`), `tests/test_tables.py`, `tests/test_rag.py`.

**Acceptation.** E-c : les 2 questions holdout sur tableaux retrouvées, sans baisse ailleurs.
E-b : exactitude des cellules (E-e) au moins égale à celle du passage pleine page, pour un
temps moindre. E-d : chaque défaut connu listé plus haut est signalé.

---

## Lot F — Recherche en français

**Constat.** Le modèle d'embeddings est anglais (`BAAI/bge-small-en-v1.5`, `lib/rag.py:25`) ;
le jeu français ne compte que 8 questions (recall@5 hybride 0,50, dense 0,62 ; EVAL.md §5),
trop peu pour conclure.

**Conception.**

1. `/paper-ask` traduit systématiquement la question en une ou deux requêtes anglaises (ce
   que le skill demande déjà pour `search`) et garde la requête française comme troisième
   variante ; les résultats sont fusionnés par RRF.
2. Un modèle multilingue (par exemple `BAAI/bge-m3`) est évalué **à côté** du modèle actuel,
   sans le remplacer, via le paramètre `model` de `rag.build_index` (l. 146).
3. Jeu français porté à au moins 30 questions par base, en dev et holdout séparés
   (`rag_eval_fr.jsonl`, `rag_eval_fr_holdout.jsonl`), écrites indépendamment des questions
   anglaises.

**Fichiers.** `.claude/commands/paper-ask.md`, `lib/rag.py` (fusion multi-requêtes,
optionnelle), fixtures, `lib/evaluation.py` (jeu `fr_holdout`).

**Acceptation.** recall@5 français ≥ 0,75 sur le holdout, sans perte sur les jeux anglais.
Changer de modèle par défaut seulement si le gain tient aussi sur le jeu de réponses du lot A.

---

## Lot G — Une route de recherche de référence

**Constat.** Deux routes coexistent (SETUP §5 et §10) :

| | `pdb search / show / verify` | `pdb rag …` |
|---|---|---|
| Code | `lib/rag.py` | `lib/rag_qwen.py`, `bin/rag_cli.py` |
| Modèles | BM25 + bge-small, rerank MiniLM, CPU | FTS5 + Qwen3-Embedding/Reranker-4B, GPU |
| Identifiants | `chunk_id` lisible | `evidence_id` haché |
| Contrôle | `verify` (OK / APPROX / NOMBRES / ABSENT / MODIFIÉ) | `check-answer` (structurel) |
| Skill | `/paper-ask` | `/paper-research` |
| Évaluation | `pdb eval --rag --save`, comparable | `pdb rag evaluate`, affichage seul |

Sur le pilote, le dense et le rerank Qwen n'améliorent pas la route lexicale
(RAG_IMPLEMENTATION_PLAN.md).

**Conception.**

1. **Route de référence : `pdb search`** (CPU, identifiants lisibles, `verify` complet).
   `pdb rag` reste une option pour le désaccord de vocabulaire et l'acquisition en libre
   accès. Le GUIDE et les `CLAUDE.md` de base le disent dans un tableau « quand utiliser
   quoi ».
2. `pdb rag evaluate --save` écrit un JSON au format de `pdb eval` (même clés
   `rag.<jeu>.<mode>.*`) pour que `pdb eval --compare` compare les deux routes sur les mêmes
   jeux. `eval/qwen_on_eval.py` devient inutile.
3. `check-answer` réutilise `rag.numbers_match` pour refuser une citation aux nombres
   différents, comme `verify`.
4. Toute décision de fusion ou de retrait d'une route attend le lot A : on compare les
   **réponses**, pas seulement les rangs.

**Fichiers.** `bin/rag_cli.py`, `lib/rag_qwen.py`, `docs/GUIDE.md`, `docs/RAG.md`,
`templates/CLAUDE.base.md`.

**État (02/10/2026).** Points 1 et 2 faits autrement que prévu : au lieu d'un
`pdb rag evaluate --save`, les modèles Qwen sont devenus un moteur optionnel de
`pdb search` (mêmes passages, mêmes `chunk_id`), activé par `bin/pdb gpu on` seulement si
l'utilisateur veut utiliser sa carte graphique et qu'elle est CUDA. `pdb eval --rag --gpu`
écrit les mêmes clés que `pdb eval --rag`, donc `--compare` met les deux moteurs côte à côte.
`pdb rag` et `/paper-research` restent la route GPU (index de preuves, acquisition). Tableau
« quand utiliser quoi » : [RAG.md §13](RAG.md#13-route-gpu-optionnelle-qwen3). Reste : point 3
(`check-answer` et `numbers_match`), et le point 4 attend toujours le lot A sur GPU.

---

## Lot H — Provenance des réponses

**Constat.** Seule la route Qwen renvoie une empreinte du corpus (`snapshot`, calculée par
`fingerprint`, `lib/rag_qwen.py:38`) ; `pdb search` n'en a pas. Aucune requête ni réponse
n'est journalisée : après une réindexation ou une ré-extraction, on ne peut pas savoir sur
quoi une réponse reposait.

**Conception.**

1. `pdb search --format json` et `pdb show --format json` ajoutent `snapshot` (même
   fonction, déplacée dans un module commun) et `index` (`{model, rerank, mode}`).
2. `/paper-ask` et `/paper-research` écrivent, quand l'option est active dans `base.json`
   (`"log_answers": true`), une ligne par réponse dans `.cache/answers/<AAAA-MM>.jsonl` :
   question, requêtes lancées, filtres `bench`, passages retenus avec `sha1`, verdict
   (lot B), snapshot, commit du code. Le format est celui de l'enregistrement du lot A :
   une réponse journalisée peut devenir un cas de test.
3. `pdb verify --sha1` (déjà en place) permet de rejouer une réponse et de détecter les
   passages modifiés depuis.

**Fichiers.** `lib/rag.py`, `bin/pdb.py`, `lib/rag_qwen.py`, `lib/base.py` (clé de
`base.json`), skills de réponse, `DATA_MODEL.md` §11.

---

## Lot I — Journal et coût des sous-agents

**Constat.** Le `CLAUDE.md` racine demande de déléguer aux sous-agents et de choisir le modèle
selon la tâche (`haiku` pour la mécanique, `sonnet` pour l'extraction, `opus` pour la
synthèse), mais rien n'est mesuré. On ne sait pas ce que coûte un appel, si la délégation
économise des tokens par rapport à un travail fait en direct, ni si la table tâche → modèle
est bien réglée. Or un agent démarre sans contexte : il paie à chaque appel son prompt
système, la définition de ses outils, le prompt de la tâche et la relecture du `CLAUDE.md` de
la base. Pour une petite tâche, ce coût fixe peut dépasser le gain.

**Objectif.** Une ligne par appel de sous-agent (tâche, agent, modèle, tokens, durée, issue),
puis un rapport qui permet de réviser la table de délégation avec des chiffres.

### I-1. Sources de données

Quatre pistes, de la plus simple à la plus complète. Elles se combinent : I-a pour le journal
courant, I-b pour le détail, I-c pour rattraper le passé et mesurer l'agent principal.

| Piste | Mécanisme | Donne | Limite |
|---|---|---|---|
| **I-a. Hook `PostToolUse` sur `Agent`** | `.claude/settings.json` (versionné), `matcher: "Agent"` (et `"Task"`, ancien nom de l'outil), commande `bin/agent_log.py`. Le hook reçoit en JSON sur stdin `session_id`, `cwd`, `tool_input` (`description`, `subagent_type`, `model`, `prompt`) et `tool_response` (`totalTokens`, `totalDurationMs`, `totalToolUseCount`, `usage` : `input_tokens`, `output_tokens`, `cache_read_input_tokens`, `cache_creation_input_tokens`). | Une ligne par appel, automatiquement, sans dépendre de la discipline du modèle. | Champs à confirmer sur la version de Claude Code installée : au premier essai, écrire le JSON brut dans `.cache/agents.raw.jsonl` et ajuster le parseur. Rien sur le détail tour par tour. |
| **I-b. Hook `SubagentStop`** | Reçoit `agent_id`, `agent_type` et `agent_transcript_path` ; le script relit le transcript du sous-agent et somme `message.usage` de chaque message assistant. | Coût par tour, modèle réellement servi, liste des outils appelés et des fichiers lus : repère un agent qui lit `fulltext.md` en entier ou relance dix fois `pdb search`. | Transcript local à la machine ; format interne susceptible de changer. |
| **I-c. Analyse a posteriori des transcripts** | Commande `bin/pdb agents` qui lit `~/.claude/projects/<projet>/<session>.jsonl` et `<session>/subagents/*.jsonl`. | Reconstruit le journal sans hook, rattrape les sessions passées, et mesure aussi le **coût de l'agent principal** : seule façon de comparer « délégué » et « fait en direct ». | À lancer à la main ; dépend du même format interne que I-b. |
| **I-d. Rapport demandé dans le prompt** | L'agent termine par une ligne `TASK: <classe> \| MODEL: <modèle> \| VERIFIED: …`. | L'étiquette de tâche et un statut. | Un agent ne connaît pas sa propre consommation : jamais une source de tokens. Repli seulement. |

**Étiquette de tâche.** Pour regrouper les appels, chaque `description` d'agent commence par
la classe de la table de délégation entre crochets : `[paper-add]`, `[paper-fiche]`,
`[bench-rows]`, `[paper-ask]`, `[explore]`, `[paper-gaps]`, `[base-profile]`, `[compare]`,
`[plan]`, `[doi-lookup]`, `[candidates]`. Le hook la sépare de la description ; sans
crochets, `task_class = "autre"`. Cette convention s'ajoute au `CLAUDE.md` racine, à côté de
la table.

### I-2. Format du journal

`.cache/agents.jsonl` à la racine du dépôt : dérivé, non versionné (`.cache/` est déjà
ignoré, principe §0), une ligne JSON par appel.

```json
{"ts": "2026-10-02T14:05:12Z", "session_id": "…", "base": "fpga",
 "task_class": "paper-fiche", "description": "fiche de lin2024yolo",
 "subagent_type": "general-purpose", "model_requested": "sonnet", "model_served": "claude-sonnet-…",
 "input_tokens": 41200, "output_tokens": 3900, "cache_read": 28000, "cache_creation": 9100,
 "total_tokens": 82200, "first_turn_tokens": 18500,
 "duration_ms": 94000, "tool_calls": 17, "tools": {"Read": 6, "Bash": 9, "Edit": 2},
 "status": "ok", "prompt_chars": 1450, "result_chars": 2100, "verified": null}
```

- `base` : nom de la base résolue depuis `cwd` par `data_root` (`lib/base.py`, même
  règle que les commandes : `base.json` en remontant, sinon la base par défaut du registre).
- `first_turn_tokens` (I-b) : tokens du premier tour, soit le coût fixe de démarrage.
- `status` : `ok`, `erreur` ou `interrompu`.
- `verified` : ce que l'agent principal a fait du résultat, `repris` (tel quel), `corrigé`
  ou `refait`. Rempli après coup par `bin/pdb agents --mark <ts> corrigé`, ou par le skill
  appelant quand il vérifie le rapport (règle « vérifier ce qu'ils rapportent » du
  `CLAUDE.md`).

Le hook n'échoue jamais bloquant : toute erreur de parsing est écrite dans
`.cache/agents.errors.log` et le script sort avec le code 0.

### I-3. Indicateurs

`bin/pdb agents --report [--since AAAA-MM-JJ] [--by task|model|base]` produit un tableau
Markdown :

| Indicateur | Calcul | Ce qu'il dit |
|---|---|---|
| Coût par tâche × modèle | médiane et p90 de `total_tokens` | base de la révision de la table |
| Coût en prix | tokens × tarif par modèle (input, output, cache read, cache write), tarifs dans un fichier de config et non en dur | les tokens d'`opus` et de `haiku` ne valent pas le même prix |
| Surcoût de démarrage | `first_turn_tokens / total_tokens` | au-delà de ~50 %, la tâche est trop petite pour être déléguée |
| Taux de reprise | part de `corrigé` + `refait` par tâche × modèle | un modèle moins cher mais souvent refait coûte plus cher au total |
| Coût effectif | coût de l'agent + coût de la reprise par l'agent principal | le vrai coût d'une délégation |
| Part de cache | `cache_read / (input_tokens + cache_read)` | faible sur des appels répétés (une fiche par agent) : préambule à rendre identique |
| Outils | nombre d'appels et lectures volumineuses | lectures inutiles à interdire dans le prompt |
| Témoin | même classe de tâche faite en direct (I-c) | la délégation est-elle rentable pour cette classe ? |

### I-4. Pistes d'optimisation à tester

Chaque piste se juge sur le rapport, avant/après, comme un changement de pipeline sur le
banc d'EVAL.md :

1. **Regrouper les tâches mécaniques.** Plusieurs `/paper-add` ou recherches de DOI dans un
   seul agent `haiku` : le coût fixe se paie une fois.
2. **Gabarit de prompt d'agent** (`templates/agent-prompt.md`) : base visée, chemin du
   `CLAUDE.md` à lire, périmètre de fichiers, format de retour court. Un préambule identique
   d'un appel à l'autre profite mieux du cache qu'un contexte recopié à chaque fois.
3. **Ajuster les modèles d'après le taux de reprise.** Essayer `haiku` sur les fiches de
   papiers courts, ou `sonnet` à la place d'`opus` pour `/paper-gaps` ; garder la
   descente seulement si la reprise reste basse.
4. **Restreindre les lectures.** Interdire dans le prompt la lecture intégrale de
   `fulltext.md` (passer par `pdb search` / `pdb show`), limiter les outils au strict
   nécessaire.
5. **Seuil de délégation chiffré.** Remplacer « garder en direct ce qui est court » par un
   seuil tiré du surcoût de démarrage mesuré (par exemple : ne pas déléguer une tâche dont
   le coût direct estimé est inférieur au coût fixe d'un agent).
6. **Résultats courts.** Demander un retour compact (chemins écrits, décisions, doutes)
   plutôt qu'un compte rendu : tout ce que l'agent renvoie entre dans le contexte de
   l'agent principal et se paie à chaque tour suivant.
7. **Parallélisme utile seulement.** Des agents en parallèle ne coûtent pas moins de tokens ;
   ils font gagner du temps. Les mesurer à part (`duration_ms`) pour ne pas confondre les
   deux gains.

### I-5. Mise en œuvre

| Étape | Contenu |
|---|---|
| I-5a | `bin/agent_log.py` en mode brut (I-a) et hook dans `.claude/settings.json` ; quelques délégations pour fixer le format réel. |
| I-5b | Parseur définitif, `.cache/agents.jsonl`, convention `[task_class]` dans le `CLAUDE.md` racine. |
| I-5c | Hook `SubagentStop` (I-b) : `first_turn_tokens`, `tools`, `model_served`. |
| I-5d | `bin/pdb agents` : `--report`, `--mark`, lecture des transcripts passés (I-c). |
| I-5e | Après ~20 délégations : rapport consigné, révision chiffrée de la table du `CLAUDE.md`. |

**Fichiers.** `.claude/settings.json`, `bin/agent_log.py`, `bin/pdb.py` (sous-commande
`agents`), `lib/agentlog.py` (parsing commun hook / transcripts), `CLAUDE.md` racine,
`templates/agent-prompt.md`, `tests/test_agentlog.py` (transcript et entrée de hook
d'exemple dans `tests/fixtures/`).

**Critère d'acceptation.** Chaque appel `Agent` d'une session produit une ligne valide dans
`.cache/agents.jsonl` sans jamais bloquer la session ; `pdb agents --report` donne coût,
surcoût de démarrage et taux de reprise par tâche × modèle ; la table de délégation du
`CLAUDE.md` est révisée au moins une fois à partir de ce rapport.

---

## Lot J — Outil de comparaison `pdb compare`

**Constat.** `benchmarks.csv` est le bon point de départ : une ligne par configuration, la
source de chaque mesure. `pdb bench --comparable` (D-5) regroupe déjà les lignes par tâche,
jeu, split et métrique (plus `power_scope` en mode `power`). Il signale aussi les conditions
qui varient (`query.VARYING`), celles en `n/r` et les comparaisons impossibles
(`lib/query.py:252-365`). Il reste sept manques :

1. **Pas de comparaison sur deux axes.** On choisit soit le mode `accuracy`, soit le mode
   `power`. On ne peut donc pas demander « FPS contre puissance, à métrique et jeu égaux »,
   qui demande d'appliquer à la fois la clé de précision et `power_scope`.
2. **Les lignes du JSON ne sont pas traçables.** Elles ne gardent que paper, model,
   platform et la valeur. `source_section`, `confidence`, `chunk_id` et les conditions de
   la ligne en sont absents.
3. **Les lignes exclues ne sont pas expliquées.** Une valeur en `n/r` disparaît sans
   message. Un groupe d'un seul papier n'apparaît que dans un compte.
4. **La comparaison n'a pas de niveau de confiance.** `varies` et `unknown` sont listés,
   mais n'en tirent aucun degré. Rien ne distingue non plus `confidence`, qui mesure la
   qualité de transcription, de la validité de la comparaison.
5. **La sélection est limitée.** `--paper` n'est pas répétable : on ne peut pas comparer
   les papiers A et B. Il n'y a pas de filtre par famille de plateformes.
6. **Les figures mélangent les portées.** `bench_fps_power` (`lib/plotfig.py:204`)
   sépare les puissances mesurées des puissances estimées, mais met `chip` et `board` dans
   le même nuage. Elle ne s'appuie pas sur les groupes comparables.
7. **Des conditions ne sont pas dans le schéma.** La fréquence d'horloge et la portée
   de la latence (bout en bout, ou inférence seule) n'ont pas de colonne.

**Conception.**

1. **J-1. Commande.** `lib/compare.py` contient une fonction déterministe, sans modèle de
   langage. Elle charge et filtre avec `query.load_benchmarks` et `query.filter_rows`, et
   groupe avec `query.comparable_groups`, à étendre plutôt qu'à dupliquer.
   `bin/pdb.py` reçoit la sous-commande `compare` :

   ```bash
   bin/pdb compare --task detection --metric mAP@0.5 --dataset COCO --x fps --y power_w
   bin/pdb compare --paper A --paper B --platform zynq --x accuracy_value --y luts
   ```

   Options : `--task`, `--metric`, `--dataset`, `--x`, `--y` (colonnes numériques de
   `schema.NUMERIC_COLUMNS`), `--paper` répétable, `--platform`, `--format tsv|md|json`
   et `--max-chars`.

2. **J-2. Règles.**
   - Clé de groupe : `task`, `dataset`, `dataset_split` et la métrique (`metric_def`, à
     défaut `~accuracy_metric`), dès qu'un axe ou un filtre porte sur la précision.
     `power_scope` entre dans la clé dès qu'un axe est `power_w` ou une valeur qui en
     dépend : une puissance `chip` ne se mélange jamais à une puissance `board`.
   - Aucune valeur n'est devinée. Un `n/r` sur un axe exclut la ligne. Un `n/r` dans la
     clé laisse la ligne dans son groupe, marquée « comparabilité non établie ».
   - Confiance de la comparaison, par groupe :
     - `forte` quand la clé est complète et qu'aucune condition de `VARYING` ne varie ;
     - `réservée` quand une condition varie (résolution, quantification, batch,
       protocole) ;
     - `faible` quand une condition est inconnue (`n/r`) ou que la métrique n'est pas
       vérifiée (`~`).
   - `confidence` (`high` / `medium` / `low`) est affichée ligne par ligne comme un
     **indicateur de qualité de transcription**. Elle ne garantit pas la validité
     scientifique et n'entre pas dans la confiance de la comparaison.

3. **J-3. Sortie en trois blocs.**
   1. *Configurations retenues*, par groupe : valeurs des axes, `paper_id`, `model`,
      `platform`, `source_section`, `confidence` et `chunk_id`.
   2. *Conditions qui varient ou manquent*, avec leur nombre, par exemple « input_res
      non renseignée pour 2 lignes » ou « quantization : INT8 | FP16 ».
   3. *Lignes exclues* : une ligne par exclusion, avec son motif (`métrique différente`,
      `power_scope incompatible`, `x en n/r`, `seul papier du groupe`…).

   Le format `--format json` reprend ces trois blocs avec un schéma stable, documenté dans
   `DATA_MODEL.md`. `/paper-compare` le lit, et les skills de synthèse ou de rédaction
   peuvent le réutiliser.

4. **J-4. Figures.** `pdb compare … --plot [png|svg]`, ou une figure `pdb plot`, construite
   à partir des groupes de J-1 : FPS contre puissance, précision contre ressources. Chaque
   `power_scope` forme une série. Une légende signale les groupes `réservée` ou `faible`.
   On corrige au passage `bench_fps_power`, qui mélange les portées.

5. **J-5. Schéma enrichi à la demande.** Les colonnes optionnelles `clock_mhz` et
   `latency_scope` s'ajoutent à `schema.OPTIONAL_COLUMNS`, puis `pdb bench --add-columns`
   les ajoute aux bases qui en ont besoin. Elles ne deviennent pas obligatoires. Une
   colonne optionnelle présente rejoint `VARYING`.

Principe : l'outil ne classe pas les meilleurs chiffres. Il montre **quelles lignes sont
comparées, pourquoi elles le sont, et quelles différences empêchent une comparaison
fiable**.

**Ordre.** D'abord un MVP tabulaire (J-1 à J-3), puis les figures (J-4), puis
l'enrichissement du schéma au fil des besoins (J-5).

**Fichiers.** `lib/compare.py`, `bin/pdb.py`, `lib/query.py` (`comparable_groups`
réutilisé et étendu), `lib/plotdata.py` et `lib/plotfig.py` (J-4), `lib/schema.py` (J-5),
`DATA_MODEL.md` §7, `docs/GUIDE.md`, `.claude/commands/paper-ask.md` (consigne de
comparaison), `tests/test_compare.py`.

**Acceptation.** Sur la base fpga, `pdb compare --task detection --dataset COCO --x fps
--y power_w` ne place jamais `chip` et `board` dans le même groupe. Chaque ligne filtrée
est soit retenue, soit exclue avec un motif, sans perte silencieuse. Le JSON donne
`source_section` et `confidence` pour chaque ligne retenue. `pdb bench --comparable` garde
sa sortie actuelle.

---

## 9. Nouveaux skills

Format commun : `.claude/commands/<nom>.md`, front-matter `description`, `argument-hint`,
`allowed-tools` (comme les skills actuels), argument dans `$ARGUMENTS`. Chaque skill agit
sur la base du dossier courant et respecte son `CLAUDE.md`. Modèle conseillé : table de
délégation du `CLAUDE.md` racine.

Workflow cible :

```
/paper-fiche ──► /paper-extract ──► /paper-compare ──► /state-of-art
                                         ▲
/paper-gaps ──► /research-question ──────┘ (axes à comparer)
/table-review ──► corrections relues ──► benchmarks.csv
```

### `/paper-extract <paper_id>` — preuves atomiques

| | |
|---|---|
| Rôle | Produire `papers/<id>/claims.jsonl` (lot C) à partir d'une fiche `done`. |
| Entrées | `fiche.md`, lignes du papier dans `benchmarks.csv`, puis passages via `pdb search` / `pdb show` (pas de lecture intégrale de `fulltext.md` si la fiche suffit à localiser). |
| Sortie | 10 à 40 claims, chacune avec `source_chunk` et `excerpt` vérifiés par `pdb verify`. |
| Outils | `Read`, `Write` (le seul `claims.jsonl`), `Bash(bin/pdb search:*)`, `Bash(bin/pdb show:*)`, `Bash(bin/pdb verify:*)`, `Bash(bin/pdb bench:*)`, réindexation. |
| Garde-fous | Ne modifie ni `fiche.md` ni `benchmarks.csv`. Aucune claim sans passage. `voice: déduit` pour toute interprétation. Valeurs selon les règles de `benchmarks.csv` (`n/r`, portée de puissance). |
| Modèle | `sonnet`, un agent par papier. |
| Dépend de | lot C (schéma, validation). |

### `/paper-compare <question ou axe>` — comparaison d'articles

| | |
|---|---|
| Rôle | Matrice comparant méthodes, plateformes, tâches, métriques, conditions de mesure et limites, puis accords, désaccords et **comparaisons impossibles** (conditions incompatibles ou `n/r`). |
| Entrées | `pdb compare --format json` (lot J), à défaut `pdb bench --comparable` (lot D) ; `claims.jsonl`, fiches, passages originaux des configurations retenues. |
| Sortie | Réponse dans la conversation ; si demandé, `docs/comparaisons/<slug>.md` dans la base. |
| Outils | `Read`, `Grep`, `Bash(bin/pdb bench:*)`, `search`, `show`, `verify`, `paper`. |
| Garde-fous | Remonte au passage original derrière chaque fiche ou ligne CSV. Pas de classement entre mesures de portées, splits ou batchs différents : elles vont dans « comparaisons impossibles » avec la raison. Verdict de suffisance (lot B). |
| Modèle | `opus`. |

### `/state-of-art <section ou axe>` — rédaction de l'état de l'art

| | |
|---|---|
| Rôle | Rédiger ou réviser une section LaTeX de `docs/etat-de-l-art/` (fpga : `sec-*.tex`, `refs.bib`, `Makefile`). |
| Entrées | `profile.md`, fiches, `claims.jsonl`, sorties de `/paper-compare`, `gaps.md`, section existante. |
| Sortie | Le fichier `sec-<axe>.tex` et un registre `claims-<axe>.csv` (phrase, `\cite` utilisé, `claim_id` ou `chunk_id`, statut `rapporté | interprété | lacune`). |
| Outils | `Read`, `Edit`/`Write` limités à `docs/etat-de-l-art/`, `Bash(bin/pdb …)` en lecture, `Bash(make -C docs/etat-de-l-art)`. |
| Garde-fous | Aucune clé `\cite` absente de `refs.bib` ; aucune référence ni citation inventée. Sépare résultats rapportés, interprétations et lacunes. Rappelle les limites de couverture du corpus (même prudence que `gaps.md`). Compile sans erreur. |
| Modèle | `opus`. |

### `/table-review <paper_id>` — relecture des tableaux extraits

| | |
|---|---|
| Rôle | Présenter chaque tableau reconstruit ou signalé (lot E-d) avec sa page, sa légende, l'image recadrée de la zone et les cellules extraites ; lister les cellules suspectes. |
| Entrées | `docling_tables.json`, `sections.jsonl` (`bbox`, lot E-a), image rendue par une commande `pdb table <id> <label> --png` (à créer, PyMuPDF `get_pixmap`). |
| Sortie | Propositions de corrections dans `papers/<id>/tables_review.md` ; l'utilisateur valide. Une correction acceptée peut alimenter la vérité terrain (E-e). |
| Outils | `Read` (images comprises), `Write` (le seul `tables_review.md`), `Bash(bin/pdb table:*)`, `Bash(bin/pdb status)`. |
| Garde-fous | N'écrit jamais dans `benchmarks.csv` ; les valeurs incertaines y entrent après accord, via `/paper-fiche`. |
| Modèle | `sonnet`. |

### `/research-question <axe ou gap>` — question de recherche

| | |
|---|---|
| Rôle | Transformer un gap de `gaps.md` en problème, hypothèse, questions de recherche, protocole expérimental possible et critères de validation. |
| Entrées | `gaps.md`, `profile.md`, fiches et claims qui étayent le gap, `benchmarks.csv`, protocoles existants (`docs/experiences/`). |
| Sortie | Dans la conversation ; si demandé, `docs/questions/<slug>.md` dans la base. |
| Outils | `Read`, `Grep`, `Bash(bin/pdb …)` en lecture. |
| Garde-fous | Marque ce qui est étayé par le corpus et ce qui reste à vérifier dans la littérature (`/paper-discover`). Un gap `hypothèse` ne devient pas un fait. |
| Modèle | `opus`. |

Priorité : `/paper-extract` puis `/state-of-art` (la rédaction est le livrable où les règles
de preuve et de citation comptent le plus), ensuite `/paper-compare`, `/table-review` et
`/research-question`.

---

## 10. Ordre de mise en œuvre

| Étape | Contenu | Pourquoi à ce rang |
|---|---|---|
| 1 | **Lot A** (jeux et notation des réponses) | mesure commune de tout le reste |
| 2 | **Lot B** (suffisance dans `/paper-ask`) | gain direct de fiabilité, sans code lourd |
| 3 | **Lot D-1 à D-3** (`chunk_id`, colonnes optionnelles, `bench --check`) | traçabilité des nombres |
| 4 | **Lot C** + `/paper-extract` | prépare comparaison et rédaction |
| 5 | **Lot E-a, E-c, E-d** (localisation, index, qualité) | rend les tableaux trouvables et contrôlables |
| 6 | `/table-review`, puis **E-e** (vérité terrain) et **E-b** (OCR par zone) | E-b se juge sur E-e |
| 7 | **Lot J-1 à J-3** (`pdb compare` tabulaire), puis `/paper-compare`, `/state-of-art` | J donne au skill une entrée déterministe ; le tout s'appuie sur C et D |
| 7 bis | **Lot J-4, J-5** (figures, colonnes `clock_mhz`, `latency_scope`) | au fil des besoins |
| 8 | **Lots G et H** (route de référence, provenance) | décisions éclairées par le lot A |
| 9 | **Lot F** (français), `/research-question` | gains moins prioritaires |
| à part | **Lot I** (journal et coût des sous-agents) | indépendant du pipeline : peut commencer à tout moment, utile dès qu'on délègue |

Pour chaque étape : tests dans `tests/` (`bin/pdb test`), `bin/pdb eval --save` avant et
`--compare` après, mise à jour de `DATA_MODEL.md` si un format change, case cochée dans
SETUP §9 et résultat consigné dans EVAL.md.

---

## 11. Hors périmètre

Modèles d'embeddings ou de reranking plus lourds, graphe de connaissances enrichi, résumés
automatiques de papiers : à garder comme expériences tant qu'ils ne montrent pas un gain sur
le jeu de réponses du lot A.
