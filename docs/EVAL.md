# Banc d'évaluation du logiciel

`bin/pdb eval` mesure la qualité et la vitesse du pipeline, pas le contenu des papiers. Il
couvre l'extraction (PDF → `fulltext.md` / `sections.jsonl`), la recherche de passages
(`pdb search`), la vérification de citations (`pdb verify`) et les temps d'exécution.
Il tourne sans LLM ni réseau, sur le corpus réel, et n'écrit rien dans `papers/` ni dans
`.cache/rag/`. Code : [lib/evaluation.py](../lib/evaluation.py).

```
bin/pdb eval                      # tout (~3,5 min sur CPU)
bin/pdb eval --extract            # extraction seule (~10 s)
bin/pdb eval --rag                # recherche, pertinence faible, verify (~2 min)
bin/pdb eval --speed [--no-cli]   # temps (~1 min)
bin/pdb eval --save               # enregistre eval/results/<date>-<commit>.json
bin/pdb eval --compare [JSON]     # écarts avec le dernier run enregistré ; code 1 si un seuil manque
bin/pdb eval --answers DIR        # réponses finales enregistrées d'un run (§10)
bin/pdb eval --questions [JEU]    # questions d'un jeu de réponses, sans les attentes (§10)
bin/pdb test --rag                # alias de pdb eval --rag
```

**Quand le lancer.** Avant et après tout changement d'extraction (GROBID, Docling, `tei.py`,
`tables.py`), de découpage, de modèle d'embeddings, de fusion ou de reranking, et quand le
corpus grossit. La démarche est la suivante : `eval --save` avant, modification, puis
`eval --compare`. Les temps sont affichés mais pas comparés, car ils varient d'un run à
l'autre. Les seuils sont dans [eval/thresholds.json](../eval/thresholds.json).

**Quelle base.** Le banc porte sur la base active : `bin/pdb --base drone eval` ou
`bin/pdb eval` lancé dans `bases/drone/` évalue la base drone, avec ses propres questions et
ses propres runs (§9). Les §1-8 décrivent la base fpga (`bases/fpga/`), base de référence
du logiciel ; ses runs sont dans `bases/fpga/eval/results/`.

---

## 1. Extraction : métriques intrinsèques

Aucune annotation n'est nécessaire, tout est calculé par papier puis agrégé
(`per_paper` dans le JSON).

| Métrique | Définition |
|---|---|
| couverture du texte | part des occurrences de mots (≥ 4 lettres, sans accents ni ligatures) de la couche texte PyMuPDF du PDF, bibliographie retirée, retrouvées dans `fulltext.md` |
| tableaux avec corps | tableaux dont le corps (hors légende) dépasse `tables.MIN_BODY_CHARS` |
| ligatures restantes | fragments typiques (`ligatures.leftover`) pour 10 000 mots |
| sections non détectées | papiers avec l'avertissement « sections numérotées non détectées » |
| titres espacés | papiers dont un titre est lu lettre par lettre (« I N T R O D U C T I O N ») |

La couverture ne peut pas atteindre 1, car une partie du texte est exclue volontairement :
en-têtes et pieds de page courants (« Manuscript submitted to ACM », numéros de page),
affiliations, texte des figures vectorielles, mots coupés par une césure (« detec- tion »).
Elle se lit donc en relatif, d'un run à l'autre ou d'un papier à l'autre. La bibliographie
est coupée au dernier titre « References », lettres espacées comprises. À défaut de titre,
la coupe se fait à une ligne `[1]` située dans la seconde moitié du texte (cas de
2108.03986).

## 2. Extraction : vérité terrain

**En-tête GROBID.** L'en-tête brut (`tei.parse_header` sur `grobid.tei.xml`, nettoyage
compris) est comparé à `metadata.json`. Ce dernier sert de référence : il a été vérifié à la
main, par arXiv, par Crossref ou par l'export éditeur. On mesure donc ce que GROBID seul
aurait donné, et non l'état final de la base. Métriques : titre normalisé exact, année, DOI,
identifiant arXiv, F1 sur les noms de famille des auteurs.

**Valeurs de benchmarks.csv.** Chaque valeur numérique (FPS, GOPS, latence, W, LUT, DSP, BRAM,
précision) a été relevée à la main par `/paper-fiche`. On la cherche telle quelle (égalité de
nombres, séparateurs de milliers tolérés) :
- dans le tableau cité par `source_section` (« Table 3 », « Table II ») ;
- n'importe où dans le texte.

Une valeur convertie par l'auteur de la fiche manque dans les deux cas. Beaucoup de lignes
citent aussi de la prose ou une figure (« Table 3, §5.2 », « Abstract, §III (Fig. 2),
Table II ») et tiennent leur valeur de là. La variante **« tableaux seuls »** se limite donc
aux lignes dont `source_section` ne cite que des tableaux : c'est elle qui mesure
l'extraction des tableaux. Cette vérité terrain existait déjà : aucune annotation nouvelle
n'a été nécessaire.

## 3. Recherche de passages

**Jeux** (`tests/fixtures/`) :

| Jeu | Questions | Rôle |
|---|---|---|
| `rag_eval.jsonl` | 20, EN | jeu **dev**, qui a servi aux choix de RAG.md §10 (modèle, fusion, rerank) |
| `rag_eval_holdout.jsonl` | 25, EN | jeu **holdout**, écrit le 26/09/2026 et jamais utilisé pour régler ; couvre les 12 papiers absents du jeu dev, 2 questions sur tableaux (`kinds: ["table"]`), 3 questions multi-papiers |
| `rag_eval_fr.jsonl` | 8, FR | traductions de questions dev |
| `rag_eval_neg.jsonl` | 10, EN | questions **hors corpus** (repliement des protéines, blockchain…), calibration du seuil de pertinence ; une question marquée `ambiguous` (à moitié couverte) est exclue |
| `rag_eval_neg_holdout.jsonl` | 10, EN | questions hors corpus de **validation**, écrites avant toute mesure du cross-encoder |

Les attentes sont construites comme pour le jeu dev (RAG.md §10) : ce sont les sections des
papiers cibles qui contiennent le motif (`evaluation.expect_from_pattern`). Elles sont ensuite
figées dans le fichier. Trois attentes du holdout ont été élargies après lecture des passages
renvoyés (champ `revised`), parce que ces passages répondaient bien à la question :
- « KD » n'était pas couvert par le motif « knowledge distillation » ;
- les systolic arrays sont aussi définis dans hozhabr ;
- la comparaison des Jetson figure aussi dans 2211.11647.

Avant cette correction, le holdout donnait recall@5 0,68 avec rerank. Aucun réglage du
système n'a été fait sur ce jeu. Pour qu'il reste un holdout, il ne faut en régler aucun
paramètre : si l'on règle dessus, écrire un nouveau jeu.

**Métriques** : recall@5, recall@10, MRR, paper@5, comme dans RAG.md §10, plus nDCG@10.
Le nDCG@10 utilise un gain binaire par section attendue, et chaque section attendue ne compte
qu'une fois. Il récompense donc le fait de trouver *plusieurs* sections pertinentes, et reste
bas quand une question en attend beaucoup (jusqu'à 49). Il sert à comparer deux runs, pas à
être lu seul.

**Pertinence faible.** Peut-on dire, sans LLM, que la base ne traite pas une question ? Deux
signaux sont mesurés pour chaque question (`evaluation.relevance_scores`) :
- `cos` : meilleur cosinus de la recherche dense ;
- `rerank` : meilleur score du cross-encoder sur les 3 premiers passages hybrides
  (`rag.relevance_score`).

Pour chaque signal, le seuil est choisi sur la calibration (jeu dev + `rag_eval_neg`), en
maximisant l'exactitude équilibrée (`evaluation.best_threshold`). Il est ensuite appliqué à
la validation (holdout + `rag_eval_neg_holdout`), qui ne sert jamais à le choisir. La règle
d'adoption a été fixée avant la mesure : en validation, au moins 80 % des questions hors
corpus signalées, et au plus 5 % des questions du corpus.

**`verify`.** Les citations de test sont tirées de 40 passages au hasard (graine fixe) :
- une phrase exacte, qui doit être acceptée ;
- la même phrase avec un mot remplacé, qui doit être refusée ;
- une phrase avec un chiffre modifié, qui doit être refusée ;
- une phrase d'un autre papier, qui doit être refusée.

« Accepté » veut dire ce que `pdb verify` traduit par le code 0 : OK ou APPROX, dans le
passage indiqué.

## 4. Temps

- Extraction hors GROBID, rejouée en mémoire sur 3 papiers (le plus petit, le médian et le
  plus gros PDF) : TEI → blocs, ligatures, tableaux, rendu. Le repli PyMuPDF est mesuré sur les
  mêmes papiers. GROBID n'est pas chronométré, car c'est un serveur externe.
- Chargement de l'index, débit d'encodage (sur 200 passages, extrapolé à l'index complet),
  latence de `search` à chaud par mode (p50, p95, sur les 20 questions dev), `verify`.
- Commandes à froid (`status`, `bench`, `paper`, `search`, `show`), lancées en sous-processus,
  démarrage de Python compris : c'est le coût réel d'un appel par un LLM.

Toutes les valeurs sont des médianes de 3 répétitions, sur la machine de développement (CPU,
sans GPU).

---

## 5. Rapport de référence (26/09/2026)

`bases/fpga/eval/results/2026-09-26T0051-80aa05e-dirty.json`. Le suffixe `-dirty` vient de ce que le banc
lui-même n'était pas encore commité ; le code mesuré est celui du commit 80aa05e. Corpus :
28 papiers, tous extraits par GROBID, 2 398 passages.

### Extraction

| Métrique | Valeur |
|---|---|
| couverture du texte | moyenne 0,91 ; minimum 0,80 (2512.01463), puis 0,82 (2024-mittal) et 0,84 (2103.05579) |
| tableaux avec corps | 0,66 (148 tableaux, dont 3 reconstruits par PyMuPDF) |
| ligatures restantes | 0,00 pour 10 000 mots |
| papiers avec sections non détectées | 7 / 28 |
| papiers avec titres espacés | 1 (2023-shuvo) |
| en-tête GROBID : titre / année / DOI / arXiv / auteurs F1 | 0,93 / 0,50 / 0,42 / 0,67 / 0,86 |
| valeurs de benchmarks.csv dans le tableau cité / dans le texte | 0,74 / 0,86 (339 valeurs) |

Lecture :
- **L'année et le DOI** sont bas surtout par construction. Le PDF arXiv ne porte ni le DOI de
  la version publiée ni, souvent, de date : sur les 14 écarts d'année, GROBID ne rend rien
  dans 10 cas. Dans les 4 autres, il lit l'année de la version publiée ou révisée, alors que
  la base retient celle du preprint (2010.15277 : 2022 contre 2020 ; 2411.01431 : 2025 contre
  2024). C'est pour cela que `ingest.py` complète ces champs depuis arXiv et depuis les
  exports `.bib`.
- **Défaut réel repéré** : 2502.15737 reçoit le DOI gabarit MDPI `10.3390/electronics1010000`,
  que `tei.clean_doi` ne rejette pas (seuls les gabarits `nnnn` et `xxxx` le sont). Il est
  corrigé dans `metadata.json`, mais un nouveau papier MDPI hériterait du même DOI.
- **Tableaux** : 12 % des valeurs relevées à la main (0,86 − 0,74) figurent dans le texte mais
  pas dans le tableau cité. *Correction du 26/09/2026 (§6)* : ce ne sont pas des tableaux
  vides. Ces valeurs viennent surtout de la prose ou des figures citées dans la même
  `source_section`, ou sont écrites autrement dans le tableau (« 0 » contre « – »). Sur les
  lignes qui ne citent que des tableaux (226 valeurs), le taux est de 0,80.

### Recherche de passages

| Jeu | Mode | recall@5 | recall@10 | MRR | nDCG@10 | paper@5 |
|---|---|---|---|---|---|---|
| dev (20) | lexical | 0,95 | 0,95 | 0,75 | 0,38 | 1,00 |
| dev (20) | dense | 0,90 | 0,90 | 0,76 | 0,40 | 0,95 |
| dev (20) | hybride (défaut) | 0,90 | 0,95 | 0,75 | 0,40 | 0,95 |
| dev (20) | hybride + rerank | **1,00** | 1,00 | **0,85** | 0,46 | 1,00 |
| holdout (25) | lexical | 0,68 | 0,80 | 0,59 | 0,29 | 0,80 |
| holdout (25) | dense | 0,76 | 0,80 | 0,64 | 0,37 | 0,88 |
| holdout (25) | hybride (défaut) | **0,84** | 0,84 | 0,65 | 0,35 | 0,92 |
| holdout (25) | hybride + rerank | 0,80 | 0,80 | **0,78** | **0,41** | 0,88 |
| FR (8) | hybride | 0,50 | 0,62 | 0,36 | 0,14 | 0,62 |
| FR (8) | dense | 0,62 | 0,75 | 0,46 | 0,20 | 0,75 |

Lecture :
- Le banc retrouve exactement les chiffres de RAG.md §10 sur le jeu dev. C'est le contrôle de
  non-régression de l'outil de mesure lui-même.
- **Le jeu dev était optimiste.** Sur le holdout, le rappel perd 6 à 27 points selon le mode.
  Le lexical passe de premier à dernier (0,95 → 0,68), ce qui confirme la réserve de RAG.md :
  les attentes choisies par mots-clés favorisaient BM25. L'hybride reste le mode le plus
  robuste.
- **Le rerank n'améliore plus le rappel** sur le holdout (0,84 → 0,80). Il améliore en
  revanche nettement le rang (MRR 0,65 → 0,78). Le gain de rappel « 0,90 → 1,00 » de RAG.md
  ne se généralise donc pas. Le gain de classement, lui, se confirme.
- **Échecs réels du holdout** (hybride + rerank) : les 2 questions sur tableaux (ressources
  des autoencodeurs de 2108.03986, prototypes FINN), la tolérance aux radiations (2602.15751),
  le QAT de 2108.03986 et la distillation de dataset (2409.07114). Les tableaux sont peu
  retrouvés : leur texte est court, et souvent réduit à la légende.

### Pertinence faible et `verify`

| Contrôle | Résultat |
|---|---|
| questions hors corpus signalées « pertinence faible » (cos < 0,60) | **0 / 10** |
| questions du corpus signalées à tort | 0 / 45 |
| cosinus : max hors corpus / min corpus | 0,83 / 0,69 |
| verify, phrase exacte acceptée | 40 / 40 |
| verify, phrase d'un autre papier refusée | 40 / 40 |
| verify, **mot remplacé accepté** (APPROX) | **39 / 40** |
| verify, **chiffre modifié accepté** (APPROX) | **38 / 38** |

Deux défauts du logiciel sont mis en évidence :
- **L'alerte « pertinence faible » ne se déclenche jamais.** Avec bge-small, une question
  hors sujet obtient un cosinus de 0,66 à 0,83, autant que les questions pertinentes (à
  partir de 0,69). Une question comme « Training large transformer language models on TPU
  pods » est d'ailleurs à moitié couverte par la section LLM de 2411.01431. Le calibrage « hors sujet 0,45-0,55 » de `rag.py` ne tient pas. Aucun
  seuil sur le cosinus seul ne sépare les deux listes. Il faut un autre signal : score du
  cross-encoder, écart entre le 1er et le 10e cosinus, ou recouvrement lexical.
- **`verify` accepte une citation dont un chiffre ou un mot a été changé.** Le ratio reste
  au-dessus de `VERIFY_MIN` = 0,85, donc le statut est APPROX, avec le code 0. Or la règle
  « Chiffres » de CLAUDE.md compte justement sur `verify` pour garantir les nombres cités.
  Correction possible : refuser APPROX dès que les nombres de la citation diffèrent de ceux
  du passage, et signaler les mots qui diffèrent.

### Temps

| Mesure | Valeur |
|---|---|
| extraction hors GROBID, par papier | 0,01 à 0,21 s |
| repli PyMuPDF, par papier | 0,02 à 0,14 s |
| chargement de l'index | 0,15 s |
| encodage bge-small | ~18 passages/s, index complet ≈ 134 s |
| `search` à chaud, p50 / p95 | lexical 7 / 14 ms ; hybride 114 / 179 ms ; hybride + rerank 1 405 / 1 689 ms |
| `verify` | 1 ms |
| commandes à froid | `status` 0,13 s ; `bench` 0,05 s ; `paper` 0,05 s ; `show` 0,31 s ; `search` 5,8 s |

Le coût d'une recherche vient presque entièrement du démarrage (import de torch, chargement
des modèles : 5,8 s à froid contre 0,1 s à chaud). Un processus résident, comme le serveur
MCP de RAG.md §11, le supprimerait. Le rerank multiplie par 12 la latence à chaud.

---

## 6. Corrections du 26/09/2026

Mesurées avec `pdb eval --compare`. Rapports dans `bases/fpga/eval/results/` : `…T0051…` (référence),
`…T0100…` (première version du contrôle des nombres), `…T0108…` (version finale et
pertinence faible), `…T0109…` (extraction avant Docling).

### `verify` : contrôle des nombres

`rag.numbers_match` (RAG.md §5.6) : les nombres de la citation doivent former une suite
contiguë des nombres du passage, et chacun doit y figurer avec ses mots voisins.

| Cas (citations) | Acceptés avant | Première version | Après |
|---|---|---|---|
| exact (40) | 1,00 | 1,00 | 1,00 |
| chiffre modifié (38) | **1,00** | 0,16 | **0,00** (38 `NOMBRES`) |
| mot remplacé (40) | 0,97 | 0,97 | 0,95 (1 `NOMBRES`, mot voisin d'un nombre) |
| autre papier (40) | 0,00 | 0,00 | 0,00 |

La première version acceptait encore 6 citations. Dans 5 cas, un nombre isolé était reconnu
comme sous-chaîne d'un autre (« 4 » dans « 6.4 »). Dans le dernier, « Section 2 » était
accepté parce qu'un 2 figurait ailleurs dans le passage. Le contrôle des mots voisins règle
les deux. La recherche de passages n'a pas bougé. Reste non traité : un **mot** remplacé loin
de tout nombre donne toujours `APPROX` (38 cas sur 40). `/paper-ask` ne garde une citation
`APPROX` que présentée comme paraphrase.

### Pertinence faible : aucun signal fiable, alerte retirée

| Signal | Seuil (calibration) | Hors corpus signalés (validation) | Corpus signalés à tort (validation) | Adopté |
|---|---|---|---|---|
| cos (seuil en place, 0,60) | — | 0,00 | 0,00 | — |
| cos | 0,79 | 0,80 | 0,24 | non |
| cross-encoder | 2,37 | 0,90 | **0,40** | non |

Aucun signal ne remplit la règle d'adoption (au plus 5 % de questions du corpus signalées).
Le cross-encoder sépare mieux les médianes (corpus 4,1 ; hors corpus −6,0), mais certaines
questions du corpus tombent très bas (jusqu'à −11). Beaucoup de ces questions sont celles
où la recherche échoue déjà : radiations, QAT, distillation de dataset, tableaux FINN. D'autres
sont bien retrouvées (panneaux routiers, vignes) et seraient signalées à tort.

Conformément à la règle, l'avertissement `# pertinence faible` a été **retiré** de
`pdb search`, car il rassurait à tort. `/paper-ask` et CLAUDE.md demandent désormais de
juger à la lecture des extraits. Le banc continue de mesurer les deux signaux :
`rag.relevance_score` reste disponible pour un essai futur (combinaison des deux signaux,
autre cross-encoder), à valider sur un nouveau jeu hors corpus.

### Docling pour les tableaux sans corps

`lib/docling_tables.py`, `bin/pdb ingest --reparse --tables docling [--ocr]` (SETUP §5).
Docling tourne sur les 18 papiers qui avaient des tableaux sans corps (environ 20 min sans
OCR), puis avec OCR sur les 3 papiers IEEE Access dont les tableaux sont des images (shuvo,
cui, hozhabr : 10 min).

| Étape | Tableaux avec corps | Reconstruits Docling | Valeurs dans le tableau cité (toutes / tableaux seuls) |
|---|---|---|---|
| avant (`…T0109…`) | 0,66 | 0 | 0,74 / 0,80 |
| Docling, filtre `tables.plausible` | 0,68 | 8 | 0,74 |
| Docling, filtre propre (`usable`) et appariement par rang (`…T0124…`) | 0,73 | 15 | 0,74 |
| + OCR sur 3 papiers (`…T0136…`) | **0,90** | 41 | 0,74 / 0,80 |

Lecture :
- **Couverture des tableaux.** Elle passe de 0,66 à 0,90 ; il reste 12 tableaux sans corps
  (`pdb status`). Parmi eux, 7 blocs n'en sont pas : de la prose ou un algorithme que GROBID a
  classés en tableau.
- **Filtre de plausibilité.** Le premier essai en perdait 27 à cause de `tables.plausible`,
  conçu contre la prose que PyMuPDF découpe en colonnes. Ce filtre exige 20 % de cellules
  chiffrées, ce qui rejette les tableaux de synthèse des surveys et les grilles à coches.
  Pour Docling, qui a déjà reconnu la structure et dont la légende correspond, on demande
  seulement une grille ≥ 2 × 2 remplie à moitié.
- **Sans effet sur les valeurs de `benchmarks.csv`.** Les tableaux cités par les fiches
  avaient déjà un corps : les valeurs manquantes viennent de corps GROBID abîmés (cellules
  fusionnées comme « 12361k0.31 » dans FINN Table 3, que Docling reproduit), de la prose
  citée dans la même `source_section`, ou d'écritures différentes. Docling, appliqué aussi à
  ces tableaux, n'en retrouve aucune de plus (essai hors corpus).
- **Sans effet sur la recherche** : les 2 questions holdout sur tableaux restent manquées.
  En hybride, une question change de rang (holdout 0,84 → 0,80, QAT de 2108.03986) ; avec
  rerank, rien ne change.
- **Qualité, contrôlée à l'œil sur 3 tableaux OCR** : shuvo Table 8 est propre ; cui
  Table 9 ne garde que la colonne « Average » ; hozhabr Table 5 contient des fragments
  d'OCR illisibles. La mention « reconstruit par Docling : à vérifier » est indispensable.
  Ces tableaux ne doivent pas alimenter `benchmarks.csv` sans relecture contre le PDF.
- **Suite (29/09/2026)** : passage étendu aux deux bases, avec OCR ; voir §9, « Docling sur
  les deux bases ».

## 7. Limites du banc

- 25 questions holdout : un écart de 0,04 correspond à une seule question. Le jeu gagnerait à
  être complété par des questions écrites par quelqu'un d'autre que l'auteur du code.
- Les attentes par motif sont une approximation des sections pertinentes. Elles pénalisent
  une bonne réponse formulée autrement (voir les 3 révisions du §3).
- La vérité terrain des tableaux ne couvre que les valeurs reprises dans `benchmarks.csv`.
- Pas d'évaluation de bout en bout de `/paper-ask` (réponse rédigée par un LLM) : elle
  demande un jugement humain et consomme des tokens. *Depuis le 02/10/2026* : volet
  `--answers` (§10), sans run de référence pour l'instant.
- Pas de comparaison GROBID / Docling : le banc est prêt à la chiffrer une fois Docling
  branché (couverture, tableaux avec corps, valeurs dans le tableau cité).
- Les extensions prévues pour ces limites sont spécifiées dans
  [AMELIORATIONS.md](AMELIORATIONS.md) : évaluation des réponses finales (lot A, en place,
  §10) et vérité terrain des cellules de tableaux (lot E-e).

## 8. Recherche GPU (Qwen3, `pdb rag`) sur les mêmes jeux (26/09/2026)

Les jeux du §3 (mêmes fichiers, mêmes attentes, `evaluation.ranking_metrics`, même protocole
de pertinence faible) appliqués au second moteur, `lib/rag_qwen.py` : SQLite FTS5,
Qwen3-Embedding-4B, fusion RRF, Qwen3-Reranker-4B, RTX 5090. Corpus identique pour les deux
moteurs : 28 papiers après fusion de `main` et `dev` ; `pdb eval --rag` y retrouve exactement
les chiffres du §5. Script : [eval/qwen_on_eval.py](../eval/qwen_on_eval.py).

| Jeu | Moteur | recall@5 | recall@10 | MRR | nDCG@10 | s / question |
|---|---|---|---|---|---|---|
| dev (20) | bge-small hybride + rerank | **1,00** | **1,00** | **0,85** | **0,46** | ~1,4 |
| dev (20) | Qwen hybride (sans rerank) | 0,90 | 0,90 | 0,78 | 0,37 | 0,7 |
| dev (20) | Qwen hybride + rerank | 0,80 | 0,80 | 0,76 | 0,35 | 3,7 |
| holdout (25) | bge-small hybride | 0,80 | 0,84 | 0,67 | 0,36 | 0,1 |
| holdout (25) | bge-small hybride + rerank | 0,80 | 0,80 | **0,78** | **0,41** | ~1,4 |
| holdout (25) | Qwen hybride + rerank | **0,88** | **0,92** | 0,75 | 0,35 | 3,3 |
| FR (8) | bge-small dense (meilleur mode) | 0,62 | 0,75 | 0,46 | 0,19 | 0,1 |
| FR (8) | Qwen dense | **1,00** | **1,00** | 0,63 | 0,22 | 0,7 |
| FR (8) | Qwen hybride + rerank | **1,00** | **1,00** | **0,88** | **0,31** | 3,8 |

| Pertinence faible (score du reranker, top 3 hybride) | Seuil | Hors corpus signalés (validation) | Corpus signalés à tort (validation) | Adopté |
|---|---|---|---|---|
| cross-encoder MiniLM (bge-small) | 2,37 | 0,90 | 0,40 | non |
| Qwen3-Reranker-4B (probabilité « yes ») | 0,96 | **1,00** | **0,16** | non |

Lecture :
- **Français** : c'est le seul écart net. Qwen retrouve les 8 questions (0,62 au mieux avec
  bge-small), sans reformulation en anglais.
- **Holdout** : +0,08 de rappel@5 (2 questions sur 25), MRR comparable. **Dev** : Qwen est
  en dessous (0,80 contre 1,00) ; le jeu dev a servi à régler bge-small (§3), l'écart y est
  donc attendu, mais il n'est pas nul.
- **Lexical** : FTS5 de `rag_qwen` fait moins bien que le BM25 de `rag.py` (dev 0,80 contre
  0,95 ; FR 0,00). En hybride français, il noie le canal dense (0,12) : le reranker rattrape.
- **Pertinence faible** : le reranker Qwen sépare la calibration parfaitement et signale les
  10 questions hors corpus de validation, mais aussi 4 des 25 questions du holdout
  (vote majoritaire / soft errors, famille FPGA spatiale, « systolic » paraphrasé, cas
  d'usage physique). La règle (≤ 5 %) n'est pas remplie ; c'est toutefois le premier signal
  proche. À revalider sur un nouveau jeu avant tout usage.
- **Coût** : GPU de 32 Go, modèles rechargés à chaque requête (3 à 4 s avec rerank, contre
  ~1,4 s pour bge-small + MiniLM sur CPU). Les deux jeux restent petits : 0,04 = 1 question.
- Différences de protocole : Qwen plafonne à 3 passages par papier et indexe aussi fiches et
  lignes de benchmark ; les limiter au texte original ne change pas le rappel (ligne
  « original text only » du JSON).
- **Depuis le 02/10/2026**, les modèles Qwen sont aussi un moteur optionnel de `pdb search`
  (route GPU, [RAG.md §13](RAG.md#13-route-gpu-optionnelle-qwen3)). Ils se mesurent alors
  directement avec le banc : `pdb eval --rag --gpu --save` (fichier suffixé `-gpu`), puis
  `pdb eval --rag --gpu --compare <run CPU>` ; plus besoin de `eval/qwen_on_eval.py` pour ce
  moteur. Mesure à faire sur une machine avec GPU.

## 9. Banc par base

**Emplacements** (`evaluation.paths`) :

| Élément | Chemin dans la base | Repli |
|---|---|---|
| questions (5 jeux du §3) | `eval/fixtures/` | `tests/fixtures/` du code, écrits pour la base fpga |
| seuils | `eval/thresholds.json` | celui du code |
| runs enregistrés, `--compare` | `eval/results/` | aucun : chaque base a ses runs |

La base fpga (`bases/fpga/`) n'a pas de `eval/fixtures/` : elle utilise les jeux de
`tests/fixtures/` du code et les seuils de `eval/thresholds.json` du code ; ses runs sont dans
`bases/fpga/eval/results/`. Le commit noté dans un run est celui du code. Le
volet temps chronomètre `bench --cols model,fps,power_w -n 5` et `paper <premier id court>`,
qui ne dépendent plus du corpus fpga. `bin/pdb test` porte toujours sur le code.

Pour une nouvelle base, écrire ses 5 jeux dans `eval/fixtures/`. Si elle n'en a pas, le banc
tourne avec les questions fpga et le rappel ne veut alors rien dire. Il faut aussi copier les
seuils avant le premier run.

### Jeu de la base drone (28/09/2026)

Questions dans [bases/drone/eval/fixtures/](../bases/drone/eval/fixtures/), même format et même
protocole que le §3, sur 73 papiers :

| Jeu | Questions | Contenu |
|---|---|---|
| `rag_eval.jsonl` | 20, EN | dev : un fait distinctif par papier, 20 papiers répartis sur les 9 axes |
| `rag_eval_holdout.jsonl` | 20, EN | 20 autres papiers : 3 questions multi-papiers (modèle F-1 de 2204.10898 et Krishnan 2020 ; Loihi dans 2303.08778 et 2108.03694 ; score DAC-SDC de Xu 2021 et Zhang 2024), 2 questions sur tableaux (puissance au repos de Feng 2022, FPS et puissance selon le nombre de threads de Nguyen 2024) |
| `rag_eval_fr.jsonl` | 8, FR | traductions de questions dev |
| `rag_eval_neg.jsonl` | 10, EN | hors corpus ; 3 `ambiguous` (drones d'épandage, empreinte RF des télécommandes, réglementation UE), sujets cités en passant dans le corpus |
| `rag_eval_neg_holdout.jsonl` | 10, EN | hors corpus de validation ; 2 `ambiguous` (livraison par drones, RL sur Atari) |

Chaque question paraphrase un fait lu dans la fiche, sans reprendre les mots-clés du passage
(« Cutting a large image into overlapping tiles at test time » pour SAHI, et non
« slicing »). Les attentes sont données par `expect_from_pattern`, entre 1 et 40 sections par
motif. Les champs `papers` et `pattern` restent dans chaque ligne.

**Révisions du holdout.** Au premier run
(`bases/drone/eval/results/2026-09-28T1011-78b56a9-dirty.json`), hybride + rerank donnait
recall@5 0,85 et hybride 0,90, avec 3 questions manquées. Après lecture des 5 passages
renvoyés pour chacune :
- *concours DAC-SDC* : élargie. `2021-xu#002` répond mot pour mot (« a combination of
  throughput, power, and detection accuracy ») et la description du concours dans SkyNet aussi ;
  le motif d'origine ne couvrait pas ces passages ;
- *drone qui repère d'autres drones avec sa caméra* : élargie. Dogfight (2103.17242, papier du
  jeu dev) traite exactement ce cas ; la question admettait deux papiers ;
- *puissance au repos* (tableau) : **non élargie**. `2022-feng#015` ne donne que la valeur du
  NCS2 (0,64 W) ; les valeurs des Jetson ne sont que dans le Table 4. C'est un échec réel.

Aucun paramètre du système n'a été réglé sur ces jeux.

### Rapport de référence drone et comparaison avec fpga

Run de référence drone : `bases/drone/eval/results/2026-09-28T1016-78b56a9-dirty.json`, avec
les seuils de la base fpga fixés avant le premier run. Pour fpga, le run de référence est
`bases/fpga/eval/results/2026-09-26T2044-65074b7.json` (45 papiers). Le suffixe `-dirty` indique que
`lib/evaluation.py` n'était pas commité.

| Métrique | fpga (45 papiers) | drone (73 papiers) |
|---|---|---|
| passages indexés | 3 479 | 4 525 |
| couverture du texte : moyenne / minimum | 0,91 / 0,81 | 0,90 / 0,70 (2504.11967) |
| tableaux avec corps | 0,88 | 0,71 (378 tableaux) |
| en-tête : titre / année / DOI / arXiv / auteurs F1 | 0,91 / 0,42 / 0,62 / 0,72 / 0,86 | 0,92 / 0,64 / 0,70 / 0,80 / 0,94 |
| valeurs de benchmarks.csv : dans le tableau cité / dans le texte | 0,65 / 0,76 (588) | 0,60 / 0,74 (716) |
| dev, hybride / hybride + rerank (recall@5) | 0,90 / 1,00 | 0,95 / 1,00 |
| holdout, hybride / hybride + rerank (recall@5) | 0,72 / 0,80 (25 q.) | 0,95 / 0,95 (20 q.) |
| holdout, MRR hybride + rerank | 0,71 | 0,92 |
| FR, hybride + rerank (recall@5) | 0,50 | 0,62 |
| pertinence faible, `cos` : hors corpus / corpus signalés (validation) | 0,80 / 0,20 | 1,00 / 0,10 |
| `verify` : exact accepté / mot remplacé accepté / chiffre modifié / autre papier | 1,00 / 0,88 / 0,00 / 0,00 | 1,00 / 0,85 / 0,00 / 0,00 |

**Seuils** : tous atteints. Le recall@5 du holdout en hybride + rerank vaut 0,95 (plancher
0,8), la couverture moyenne 0,90 (plancher 0,85) et le titre 0,92 (plancher 0,8). `verify`
accepte toutes les citations exactes et refuse tous les chiffres modifiés et toutes les
citations d'un autre papier.

Lecture :
- **Le holdout drone est plus facile que celui de fpga, on ne peut pas conclure que la
  recherche marche mieux.** Le corpus drone est plus hétérogène (détection, suivi,
  neuromorphique, course…) : un fait distinctif y a moins de voisins proches que dans un
  corpus fpga centré sur les accélérateurs. Deux attentes ont en outre été élargies (sans
  elles : 0,85). Avec 20 questions, 0,05 = 1 question.
- **Échecs restants.** Le tableau de puissance au repos est manqué par tous les modes, comme
  les tableaux du holdout fpga : un tableau est un passage court, souvent réduit à sa
  légende. En français, 3 questions sur 8 restent manquées (bit flips, conception de bas en
  haut, course de drones) ; le lexical y est nul.
- **Pertinence faible** : le signal `cos` signale les 8 questions hors corpus non ambiguës de
  validation, mais aussi 2 des 20 questions du holdout. La règle d'adoption (≤ 5 %) n'est pas
  remplie, comme pour fpga : aucune alerte n'est réintroduite.
- **Extraction** : la couverture minimale (0,70, survey anti-UAV 2504.11967) et le taux de
  tableaux avec corps (0,71) sont plus bas que pour fpga ; 18 papiers ont des sections non
  détectées. Ces valeurs ne sont pas sous un seuil, mais la base drone est la première à
  relire si l'on améliore l'extraction des tableaux.

### Nouveaux runs de référence, après le déplacement de fpga (28/09/2026)

Les deux bases ont été réévaluées (tous les volets, `pdb eval --save --compare`) après le
déplacement de la base fpga dans `bases/fpga/` (commit 76dc85e). Ces runs sont propres
(sans `-dirty`) et remplacent les précédents comme références :

| Base | Run | Comparé à | Écarts |
|---|---|---|---|
| fpga | `bases/fpga/eval/results/2026-09-28T1039-76dc85e.json` | `2026-09-26T2044-65074b7.json` | 0 |
| drone | `bases/drone/eval/results/2026-09-28T1043-76dc85e.json` | `2026-09-28T1016-78b56a9-dirty.json` | 0 |

Toutes les métriques du tableau ci-dessus sont reproduites à l'identique et tous les seuils
sont atteints : le déplacement n'a changé ni l'extraction, ni l'index de passages, ni
`verify`. Temps (médianes, non comparés) : hybride p50 126 ms (fpga) et 112 ms (drone),
hybride + rerank p50 1,39 s et 1,14 s, `search` à froid 6,9 s et 6,7 s.
Figures régénérées dans `bases/<nom>/figures/` (`pdb plot all`) ; la base drone a désormais
ses figures `eval_*`.

### Docling sur les deux bases (29/09/2026)

Passage Docling sur tous les papiers dont des tableaux étaient restés sans corps et qui
n'avaient pas encore de `docling_tables.json` : 20 papiers fpga, 40 papiers drone
(`pdb ingest --reparse --tables docling <ids>`). Un second passage avec OCR
(`--ocr`) a suivi sur les papiers qui en avaient encore : 18 papiers fpga, 22 papiers drone
(1 h 15). Avant cela, 17 papiers fpga ajoutés le 28/09 alors que GROBID était arrêté
(backend `pymupdf`, sans `grobid.tei.xml`) ont été réextraits par
`pdb ingest --force papers/<id>/paper.pdf`. Sans TEI, leurs tableaux n'étaient pas repérés
et n'apparaissaient donc pas dans « tableaux à vérifier ».

Tableaux signalés par `pdb status` (sans corps / reconstruits) :

| Base | Avant | Après GROBID (fpga) | Docling | + OCR |
|---|---|---|---|---|
| fpga (69 papiers) | 31 / 79 | 63 / 83 | 41 / 108 | **31 / 118** |
| drone (73 papiers) | 108 / 20 | — | 59 / 71 | **24 / 106** |

`pdb eval --extract --compare` contre les runs de référence du 28/09 (non remplacés, ces
runs ne couvrant que l'extraction) :

| Métrique | fpga | drone |
|---|---|---|
| tableaux avec corps | 0,88 → 0,87 (233 → 401 tableaux ; 110 Docling, 8 PyMuPDF) | **0,71 → 0,90** (378 ; 96 Docling, 10 PyMuPDF) |
| valeurs dans le tableau cité / tableaux seuls | 0,65 → 0,63 / 0,71 → 0,67 | 0,60 → 0,63 / 0,66 → 0,67 |
| couverture moyenne / minimum | 0,91 → 0,90 / 0,81 → 0,57 | 0,90 → 0,91 / 0,70 → 0,77 |

Lecture :
- **drone** : l'effet de Docling se lit directement, car le corpus n'a pas changé. Le taux
  de tableaux avec corps rejoint celui de fpga. Les valeurs de `benchmarks.csv` retrouvées
  dans leur tableau montent de 3 points : c'est le premier gain de Docling sur ces valeurs
  (§6 n'en trouvait aucun sur fpga).
- **fpga** : les écarts mêlent Docling et les 24 papiers ajoutés le 28/09. La baisse des
  valeurs retrouvées vient des 23 lignes de benchmark importées avec
  arxiv-2607.13106, dont 14 valeurs sont hors du tableau cité. Le minimum de couverture
  (0,57) est la thèse NTU `2021-piyasena-fpga-acceleration-continual-learning` (103 pages).
- **Restes** : 31 + 24 tableaux sans corps, dont de faux tableaux (prose ou algorithme
  classés en tableau par GROBID). Les 14 tableaux sans corps de `2026-fata-low-cost-fpga-enhanced-cnn`
  sont à regarder en premier. Les tableaux reconstruits (224 en tout) portent la mention
  « à vérifier » et ne doivent pas alimenter `benchmarks.csv` sans relecture.
- `pdb test` : 204 tests sur 205 réussissent. `test_rag_qwen.test_external_import_is_isolated`
  échoue parce qu'il ne peut pas charger un modèle depuis huggingface.co ; aucun code n'a
  changé.

## 10. Réponses finales (`pdb eval --answers`, 02/10/2026)

Lot A de [AMELIORATIONS.md](AMELIORATIONS.md). Les §3-8 mesurent le classement des passages ;
ce volet mesure la **réponse rédigée** : sait-elle reconnaître une question hors corpus,
ses citations tiennent-elles, retrouve-t-elle les sources et les valeurs attendues ? Le banc
reste sans LLM : les réponses sont produites à part, puis notées.

```
/eval-answers [answers|answers_holdout] [run]     # dans Claude Code : produit et note un run
bin/pdb eval --questions [answers|answers_holdout] # id et question, sans les attentes
bin/pdb eval --answers eval/answers/<run>… [--save] [--compare]  # plusieurs runs : notés ensemble
```

**Jeux.** `answers.jsonl` (dev) et `answers_holdout.jsonl`, dans `eval/fixtures/` de la base
ou, pour fpga, dans `tests/fixtures/` (même règle que les autres jeux, `evaluation.paths`).
Quatre catégories :

| Catégorie | Ce qu'on vérifie | Verdict attendu |
|---|---|---|
| `simple` | un fait sourcé dans un papier | `suffisant` |
| `numeric` | valeurs, unités, conditions | `suffisant` |
| `synthesis` | couverture de plusieurs papiers | `suffisant` (ou `partiel`) |
| `absent` | question proche du thème, non couverte par le corpus | `absent` |

Une ligne du jeu :

```json
{"id": "dev-n1", "q": "Quel débit et quelle latence TinyissimoYOLO atteint-il sur le MAX78000 ?",
 "category": "numeric", "required": ["le débit en FPS", "la latence par inférence"],
 "gold_sources": ["2306.00001#000", "2306.00001#006"],
 "gold_values": [{"field": "fps", "value": "180", "unit": "fps"}, {"field": "latency_ms", "value": "5.5", "unit": "ms"}],
 "expected_verdict": "suffisant"}
```

- `gold_sources` : sections (`paper#NNN`, id court accepté) ou papiers entiers (`paper_id`),
  vide pour `absent`.
- `gold_values` (facultatif) : nombres attendus dans une affirmation de la réponse, avec leur
  unité si `unit` est donnée ; virgule décimale française acceptée (« 64,6 % »).
- Les questions `absent` sont choisies proches du thème (polypes en endoscopie, langue des
  signes, sonar, EEG…) et vérifiées absentes par recherche plein texte dans `sections.jsonl` :
  les jeux `rag_eval_neg*` (biologie, finance…) sont trop éloignés pour tester la réponse.

**Enregistrement d'une réponse.** `/paper-ask … --record eval/answers/<run>/<id>.json` écrit
la réponse sous forme d'affirmations citées, avec ses exigences et son verdict de suffisance
(format dans [paper-ask.md](../.claude/commands/paper-ask.md)) :

```json
{"id": "dev-n1", "q": "…", "verdict": "suffisant",
 "requirements": [{"text": "le débit en FPS", "status": "couvert"}],
 "claims": [{"text": "TinyissimoYOLO atteint jusqu'à 180 fps sur le MAX78000.", "kind": "lu",
             "citations": [{"id": "2306.00001#000.0", "excerpt": "achieving high frame-rate of up to 180 fps"}]},
            {"text": "L'accélérateur CNN explique l'écart.", "kind": "déduit"}]}
```

Une citation de `pdb bench` s'écrit `{"paper": "1612.07119", "source_section": "Table 3"}`.
`/eval-answers` ne donne aux agents que la question (`pdb eval --questions`) : ni catégorie,
ni sources, ni verdict attendu.

**Métriques**, par jeu et par catégorie (`lib/evaluation.py`, `answer_quality`) :

| Métrique | Définition |
|---|---|
| `verdict_accuracy` | verdict = verdict attendu |
| `absent_recognized` | questions `absent` : verdict `absent` ou `partiel` |
| `false_absent` | autres questions : verdict `absent` à tort |
| `citation_accept_rate` | citations acceptées / citations. Passage : `rag.verify` sur l'extrait, `OK` ou `APPROX` **dans le passage indiqué** (comme le code 0 de `pdb verify`) ; sans extrait, inconnu, `NOMBRES` ou trouvé ailleurs : refusé. Benchmark : chaque partie de la section citée (séparée par `;` ou `,`) figure dans la `source_section` d'une ligne du papier |
| `unsupported_claim_rate` | affirmations `lu` sans aucune citation acceptée / affirmations `lu` |
| `gold_source_recall` | sources attendues citées (par une citation acceptée) |
| `gold_value_recall` | valeurs attendues présentes dans une affirmation, avec leur unité |
| `verdict_confusion` | matrice attendu × obtenu |
| `human.*` | notes de `grades.csv`, ramenées à [0, 1] |

**Notes humaines.** `eval/answers/<run>/grades.csv`, colonnes
`id,exigences,soutien,conditions,limites`, de 0 à 2 :

| Critère | 0 | 1 | 2 |
|---|---|---|---|
| `exigences` | la question n'est pas traitée | traitée en partie | toutes les exigences traitées ou déclarées absentes |
| `soutien` | une affirmation est contredite par son passage | des affirmations débordent leur passage | chaque affirmation `lu` est soutenue |
| `conditions` | chiffres sans conditions | conditions partielles | plateforme, précision, batch, portée de puissance… explicites |
| `limites` | aucune réserve | réserves génériques | limites du corpus et des mesures signalées |

Les contrôles automatiques vérifient que les extraits existent, pas qu'ils soutiennent la
phrase : seule la note `soutien` le dit.

**Jeux de départ (fpga).** 12 questions dev et 12 holdout, 3 par catégorie, écrites par
l'auteur du code : c'est une graine. Objectif : 40 dev / 60 holdout par base, écrits ou relus
par quelqu'un d'autre. Aucun seuil n'est fixé dans `thresholds.json` avant deux runs
complets, pour mesurer la variance d'un run à l'autre (même question, réponses différentes).
Ne rien régler sur `answers_holdout`.

**Lecture d'un run.** `pdb eval --answers` liste aussi les enregistrements non conformes,
les ids absents des jeux, les questions sans réponse et, par question, les verdicts faux et
les affirmations non soutenues. `--save` enregistre le run dans `eval/results/` avec les
autres volets ; `--compare` ignore le détail par question (`per_question`).

### Premier run (02/10/2026)

`bases/fpga/eval/results/2026-10-02T1111-353e788-dirty.json` ; réponses dans
`bases/fpga/eval/answers/2026-10-02-answers{,_holdout}/`. Une réponse par question, par un
agent Sonnet qui ne recevait que la question. **Configuration dégradée** : la recherche
dense et le reranking étaient indisponibles (téléchargement des modèles refusé par le
réseau du conteneur), donc `pdb search` en lexical seul, sans `--rerank`. Le run de
référence de `/paper-ask` reste à faire avec le mode hybride + rerank.

| Jeu | n | verdict juste | citations acceptées | affirmations non soutenues | sources attendues | valeurs attendues |
|---|---|---|---|---|---|---|
| dev | 12 | 0,83 | 0,96 | 0,02 | 0,91 | 1,00 |
| holdout | 12 | 0,92 | 1,00 | 0,00 | 0,67 | 1,00 |

Par catégorie, sur les deux jeux : `simple`, `numeric` et `absent` ont tous un verdict juste
(18/18) ; `synthesis` en a 3 sur 6. Hors corpus : 6/6 questions reconnues `absent`, aucune
question du corpus déclarée `absent` à tort.

Lecture :
- **Hors corpus.** Sur des questions proches du thème, les réponses disent que la base ne
  traite pas le sujet, sans combler par des connaissances générales. C'est le comportement
  que le score de recherche ne permettait pas d'obtenir (§5-6). Avec 6 questions, c'est un
  signal, pas une mesure.
- **Synthèse.** Les 3 verdicts faux sont `partiel` là où le jeu attend `suffisant` (dev-y1,
  dev-y2, ho-y3). L'agent pose des exigences plus fines que celles du jeu (budget mémoire de
  chaque méthode, protocole commun) et les trouve incomplètes : c'est défendable, et la
  frontière suffisant / partiel des questions de synthèse est à préciser dans le jeu.
- **Une source manquée deux fois** : 2409.07114 (apprentissage incrémental sur MCU), absente
  de dev-y1 et de ho-y3 ; c'était déjà un échec de recherche du holdout passages (§5).
- **Sources attendues trop étroites.** La plupart des écarts de `gold_source_recall` (0,67 en
  holdout) viennent d'une source équivalente : le chiffre est cité par sa ligne `bench`
  ou par le passage tableau plutôt que par la section de texte attendue (dev-n1, ho-n2,
  ho-n3). Le jeu doit accepter des sources alternatives ; le chiffre sous-estime la réponse.
- **Défauts réels relevés** : dev-s2 porte `suffisant` alors qu'une de ses exigences est
  `partiel` (règle du verdict non appliquée) ; dev-y2 cite deux fois une ligne de
  benchmark par `power_scope=board` au lieu de sa section source.
- **Correcteur corrigé pendant le run** : une citation `bench` regroupant plusieurs lignes
  (« Table 3 ; Table 4 ») était refusée ; chaque partie est maintenant contrôlée.

Notes humaines : `grades.csv` créés, vides. Aucun seuil fixé : il faut un second run complet
(variance d'un run à l'autre) et la configuration hybride + rerank.
