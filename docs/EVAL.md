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
bin/pdb test --rag                # alias de pdb eval --rag
```

**Quand le lancer.** Avant et après tout changement d'extraction (GROBID, Docling, `tei.py`,
`tables.py`), de découpage, de modèle d'embeddings, de fusion ou de reranking, et quand le
corpus grossit. La démarche est la suivante : `eval --save` avant, modification, puis
`eval --compare`. Les temps sont affichés mais pas comparés, car ils varient d'un run à
l'autre. Les seuils sont dans [eval/thresholds.json](../eval/thresholds.json).

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

`eval/results/2026-09-26T0051-80aa05e-dirty.json`. Le suffixe `-dirty` vient de ce que le banc
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

Mesurées avec `pdb eval --compare`. Rapports dans `eval/results/` : `…T0051…` (référence),
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

## 7. Limites du banc

- 25 questions holdout : un écart de 0,04 correspond à une seule question. Le jeu gagnerait à
  être complété par des questions écrites par quelqu'un d'autre que l'auteur du code.
- Les attentes par motif sont une approximation des sections pertinentes. Elles pénalisent
  une bonne réponse formulée autrement (voir les 3 révisions du §3).
- La vérité terrain des tableaux ne couvre que les valeurs reprises dans `benchmarks.csv`.
- Pas d'évaluation de bout en bout de `/paper-ask` (réponse rédigée par un LLM) : elle
  demande un jugement humain et consomme des tokens.
- Pas de comparaison GROBID / Docling : le banc est prêt à la chiffrer une fois Docling
  branché (couverture, tableaux avec corps, valeurs dans le tableau cité).
