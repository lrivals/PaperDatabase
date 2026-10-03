# Recherche de passages (RAG) et requêtes sans génération

Spécification de la couche de recherche de PaperDatabase : ce qu'elle doit faire, comment la
construire, comment s'en servir. Suivi des tâches : [SETUP.md §9](../SETUP.md#9-état-actuel-et-tâches-à-faire).

## État au 25/09/2026 : implémenté et testé

| Élément | Code | Tests unitaires | Vérifié sur la base réelle |
|---|---|---|---|
| `pdb bench` : filtres, tri, colonnes de source forcées, `!` low, lignes identiques signalées, `--max-chars`, `--count` | [lib/query.py](../lib/query.py), [bin/pdb.py](../bin/pdb.py) | [tests/test_query.py](../tests/test_query.py) (14) | oui : KV260, `--sort fps --desc`, `--min`/`--max`, colonne inconnue → code 2, `--count paper_id,power_scope` |
| `pdb paper` : fiche d'identité, candidats si ambigu, `--bench`, plusieurs ids (une ligne chacun) | idem | idem | oui : `finn` (ambigu), `1612.07119 --bench`, `2022-feng --fields`, `1612.07119 2022-feng 2502.15737 finn` |
| Identifiants courts (arXiv, sinon année-auteur, noms composés compris) | `lib/query.short_ids` | idem | oui : 28 papiers, aucune collision ; `2025-el-zeinaty` corrigé après l'essai (§12) |
| Passages, BM25, embeddings bge-small, fusion RRF, filtres | [lib/rag.py](../lib/rag.py) | [tests/test_rag.py](../tests/test_rag.py) (10, encodeur factice) | oui : 2 405 passages ; évaluation §10 |
| `pdb search` : colonne `cos` (alerte `# pertinence faible` retirée le 26/09/2026) | `lib/rag.py`, `bin/pdb.py` | idem | oui : aucun seuil fiable, ni cosinus ni cross-encoder (EVAL.md §5) |
| `pdb show` : texte exact, sha1, `--context` | idem | idem | oui |
| `pdb verify` : OK / APPROX / NOMBRES / ABSENT / MODIFIÉ, « trouvée dans » | idem | idem | oui : 5 cas manuels (§5.6), 7 citations de l'essai de `/paper-ask` (§12), 158 citations générées par `pdb eval` (EVAL.md §6) |
| Index incrémental, branché dans `reindex` | `lib/rag.build_index`, [bin/reindex.py](../bin/reindex.py) | idem (réencodage d'un seul passage modifié) | oui : 0,2 s sans changement, ~3 min pour une construction complète |
| Évaluation `bin/pdb eval --rag` (alias `test --rag`) | `lib/evaluation.py`, `bin/pdb.py` | `test_evaluation.py` | oui : 20 questions dev, 25 holdout, 8 FR, 20 hors corpus (§10, [EVAL.md](EVAL.md)) |
| Skill `/paper-ask` | [.claude/commands/paper-ask.md](../.claude/commands/paper-ask.md) | — | oui : un essai réel (§12) |
| `pdb cites` / `cited-by`, `--external` | `lib/refs.citations`, `lib/query.citation_lines`, `bin/pdb.py` | `test_refs.py`, `test_query.py` | oui : `cited-by 1612.07119` (4 papiers), `cites 2025-hozhabr --external` (2 dans la base, 286 hors base) |
| Reranking par cross-encoder (`search --rerank`) | `lib/rag.py` (`_cross_scores`, `Index.search(rerank=True)`) | idem (cross-encoder factice) | oui : évaluation §10, +1,2 s par recherche ; activé dans `/paper-ask` |

| Route GPU optionnelle : moteur Qwen3 pour `pdb search` (`--gpu`), `pdb gpu`, `pdb eval --rag --gpu`, `pdb rag` réservé au GPU | `lib/rag.py`, [lib/rag_models.py](../lib/rag_models.py), `bin/pdb.py`, `bin/reindex.py` | `test_rag.py` (Qwen simulé), `test_rag_qwen.py` | non sur cette machine (pas de GPU) ; Qwen évalué par ailleurs (EVAL.md §8). §13 |

Au total, `bin/pdb test` passe 133 tests (le 25/09/2026, après `cites`, `paper` multiple,
ligatures, figures rendues au corps et mesures propres).

Objectifs, par ordre de priorité :

1. **Vérifiabilité** — tout élément renvoyé porte une source rejouable (passage, section, page).
2. **Économie de tokens** — répondre sans que le LLM lise un `fulltext.md` entier, et sans
   qu'il rédige quand une sortie brute suffit.
3. **Accès par le sens** — retrouver « continual learning » en cherchant « apprentissage
   incrémental », ce que `grep` ne sait pas faire.

---

## 1. Qu'est-ce qu'un RAG

*Retrieval-Augmented Generation* : au lieu de s'appuyer sur sa mémoire, le LLM reçoit, avec
la question, les passages de la base qui y répondent, et rédige à partir d'eux en les citant.

| Étape | Quand | Ce qui se passe |
|---|---|---|
| Indexation | une fois, puis à chaque ajout | le texte est découpé en passages ; chacun reçoit un vecteur (*embedding*) et une entrée dans un index lexical |
| Recherche (*retrieval*) | à chaque question | la question est vectorisée ; on récupère les *k* passages les plus proches, par le sens et par les mots |
| Génération | à chaque question | le LLM répond à partir de ces passages seulement, en citant leurs identifiants |

**Choix pour cette base : la génération reste à Claude Code.** Les commandes `bin/pdb` font
la recherche, de façon déterministe et sans appel à un LLM. Claude Code les appelle, lit les
sorties, et rédige quand il le faut. Il n'y a ni clé API ni coût supplémentaire, et
l'outillage actuel reste le même (skills, `CLAUDE.md`).

---

## 2. Point de départ (avant implémentation)

| Brique | Existant | Manque |
|---|---|---|
| Extraction | GROBID → `fulltext.md`, `sections.jsonl` (DATA_MODEL §4-5) | — |
| Unités de texte | `sections.jsonl` : 1 340 entrées sur 28 papiers, chacune avec `id`, `paper_id`, `section`, `subsection`, `page`. Longueur médiane 145 mots, max 1 248 ; 454 entrées dépassent 250 mots | un découpage adapté à la fenêtre du modèle d'embeddings (§4.1) |
| Embeddings | [lib/embed.py](../lib/embed.py) : `chunks()` (fenêtres de 200 mots), `_encode()`, cache sha1 sous `.cache/` | les vecteurs sont **moyennés par papier** (pour la vue 3D) ; il faut un vecteur **par passage** |
| Index lexical | TF-IDF par papier dans `lib/graph.py` (similarité entre papiers) | un index BM25 par passage |
| Données structurées | `benchmarks.csv` (109 lignes, `source_section`, `confidence`, `power_scope`), `metadata.json`, `refs.jsonl`, `INDEX.md` | une interface en ligne de commande pour les filtrer sans les lire en entier |
| Dépendances | `sentence-transformers` et `scikit-learn` déjà dans `.venv` (`requirements-embed.txt`, `requirements-viz.txt`) | — |

---

## 3. Principe directeur : trois niveaux de requête

Du moins cher au plus cher. **On ne monte d'un niveau que si le précédent ne suffit pas.**

| Niveau | Source | LLM ? | Coût typique | Exemple de question |
|---|---|---|---|---|
| **N0 — requête structurée** | `benchmarks.csv`, `metadata.json`, `refs.jsonl` | non | 100-500 tokens | « Quels accélérateurs YOLO sur KV260 en INT8, avec leur puissance ? » |
| **N1 — recherche de passages** | index de passages (§4) | non | 400-800 tokens (extraits), +300 par passage ouvert | « Où est discutée la mesure de puissance carte vs puce ? » |
| **N2 — synthèse** | sorties N0/N1 uniquement | oui (Claude Code) | celui de la rédaction | « Compare les stratégies de quantification des toolflows et dis ce qui manque » |

Les sorties N0 et N1 sont **déjà des réponses** quand la question est factuelle : un tableau
filtré ou trois passages sourcés suffisent souvent, et Claude peut les transmettre avec une
phrase d'introduction au lieu de reformuler. Le niveau N2 n'invente rien : il ne relie que ce
que N0/N1 ont renvoyé, et il sépare ce qui est lu de ce qui est déduit (règle de `CLAUDE.md`).

Les fiches (`fiche.md`, ~1 500 tokens chacune) gardent leur rôle : la lecture critique déjà
rédigée. On les lit quand la question porte sur un papier précis et sur son évaluation, pas
pour retrouver un fait.

---

## 4. Index de passages

### 4.1 Découpage

- Unité de base : une entrée de `sections.jsonl` (elle respecte déjà les paragraphes, DATA_MODEL §5).
- Une entrée de plus de 250 mots est coupée en fenêtres de 200 mots avec 40 mots de
  recouvrement : les modèles d'embeddings tronquent au-delà de 256 à 512 tokens, et une
  entrée non découpée perdrait sa fin.
- Un tableau de plus de 250 mots est coupé par rangées entières, jusqu'à environ 200 mots,
  sans recouvrement. Chaque fenêtre suivante reprend la légende, abrégée à sa première
  phrase, et la ligne d'en-tête, avec la ligne d'unités si elle existe : une valeur reste
  lisible avec sa colonne (`rag.split_table`, lot E-c, 03/10/2026). Une légende plus longue
  qu'une fenêtre (de la prose captée avec le tableau) a ses propres fenêtres de mots.
- Identifiant de passage : `chunk_id = <id de la section>.<k>`, par exemple
  `arxiv-1612.07119-finn-framework-fast-scalable-binarized#019.3`, `1612.07119#019.3` en
  forme courte. `k` commence à 0 ; une section non découpée a le seul passage `.0`. Un id de
  section sans `.k` (`1612.07119#019`) désigne son premier passage.
- Chaque passage garde : `chunk_id`, `section_id`, `paper_id`, `kind`, `section`,
  `subsection`, `page`, `text`, et le `sha1` du texte.
- Le texte encodé (dense et BM25) est préfixé du titre de section et de sous-section. Cela
  donne du contexte sans modifier le texte renvoyé.

Volume : 2 405 passages pour les 28 papiers du 25/09/2026.

### 4.2 Deux index, une fusion

| Index | Rôle | Implémentation |
|---|---|---|
| Dense | proximité de sens, reformulations, requête dans une autre langue | `BAAI/bge-small-en-v1.5` (384 dimensions) via `lib/embed._encode`, vecteurs normalisés. La requête (pas les passages) reçoit le préfixe recommandé par le modèle (`rag.QUERY_PREFIX`) |
| Lexical (BM25) | termes exacts : noms de cartes (`ZCU104`), de modèles (`YOLOv5n`), sigles, nombres | BM25 écrit à la main (`k1=1.5`, `b=0.75`), jetons `[a-z0-9]+` en minuscules |

**Fusion par *Reciprocal Rank Fusion* :** `score(d) = Σ 1 / (60 + rang_i(d))` sur les deux
classements. Cette méthode ne dépend pas de l'échelle des scores, ne demande aucun réglage,
et elle est déterministe. En cas d'égalité, le `chunk_id` le plus petit passe en premier.

Le score RRF ne dit rien de la pertinence absolue : `search` renvoie toujours k passages.
La sortie affiche aussi le **cosinus** entre la requête et chaque passage, mais il ne dit
pas si la base traite le sujet. L'avertissement `# pertinence faible` (cosinus < 0,60), qui
avait été calibré à la main sur quelques requêtes, a été retiré le 26/09/2026. Sur 10
questions hors corpus, il ne s'était jamais déclenché : leurs cosinus vont de 0,66 à 0,83.
Le score du cross-encoder ne fait pas mieux : au seuil qui sépare la calibration, il
signale 90 % des questions hors corpus, mais aussi 40 % des questions du corpus
(EVAL.md §5). C'est donc à la lecture des extraits de juger si la base répond.

Choix du modèle et du mode par défaut : voir l'évaluation (§10). `all-MiniLM-L6-v2`, que
la vue 3D utilise, s'y montre nettement plus faible.

Filtres appliqués **avant** le classement : `--paper`, `--axis` (lu dans `metadata.json`),
`--kind` et `--section` (sous-chaîne du titre de section ou de sous-section, insensible à
la casse).

### 4.3 Stockage et mise à jour

- Emplacement : `.cache/rag/<modèle>.npz`, déjà ignoré par git. Il contient les clés
  `chunk_id:sha1` et la matrice des vecteurs. L'index est dérivé de la base et
  reconstructible ; il ne va jamais dans `papers/`.
- Les passages et le BM25 sont recalculés à chaque commande depuis `sections.jsonl`, en
  moins d'une seconde : rien d'autre à stocker.
- Mise à jour incrémentale : seuls les passages dont la clé `chunk_id:sha1` est absente du
  cache sont encodés. Construction complète : ~3 min pour bge-small sur 22 cœurs CPU ;
  sans changement : 0,2 s.
- Déclenchement : `bin/reindex.py` appelle `rag.build_index()`, donc `add` et `ingest`
  aussi. Un échec de l'index devient une note, sans bloquer la réindexation. Sans
  sentence-transformers, ou si l'index est périmé, `search` passe en lexical seul et le
  signale en tête de sortie (`# mode: lexical seul`).
- Les modèles sont chargés hors ligne s'ils sont tous déjà en cache
  (`rag.quiet_model_loading`) : aucune requête au Hub à chaque recherche. Le mode hors
  ligne vaut pour tout le processus. Un index qui fera du reranking doit donc le déclarer
  (`Index(..., rerank=True)`), faute de quoi le cross-encoder ne pourrait pas être
  téléchargé au premier appel (bug rencontré et corrigé le 25/09/2026).
- Temps d'une commande à froid (mesuré par `pdb eval --speed`, EVAL.md §5) : `search` 5,8 s,
  dont l'essentiel est l'import de torch et le chargement du modèle ; `show` et `verify`
  environ 0,3 s, sans modèle.

### 4.4 Module `lib/rag.py`

```python
load_chunks(root) -> list[dict]                   # passages (§4.1)
build_index(root, chunks=None, model=DEFAULT_MODEL, force=False) -> dict   # manifeste
Index(root, model=DEFAULT_MODEL)                  # passages + BM25 + vecteurs
Index(root, model=DEFAULT_MODEL, rerank=False)    # rerank : déclare le cross-encoder (§4.3)
Index.search(q, k=8, mode="hybrid", paper_ids=None, axis=None, kind=None, section=None,
             rerank=False)
Index.get(chunk_id, context=0)                    # passage exact ± voisins du même papier
Index.resolve_chunk(cid) / Index.short_chunk_id(chunk_id)
verify(index, chunk_id, quote, expect_sha=None) -> (statut, ratio, chunk_id où trouvée)
numbers_match(text, quote) -> bool               # contrôle des nombres de verify (§5.6)
relevance_score(index, q) -> float               # meilleur score du cross-encoder (EVAL.md §6)
evaluate(index, questions, k=5) -> {mode: {recall, mrr, paper, misses}}
                                                 # remplacé par lib/evaluation.evaluate_set
```

---

## 5. Commandes sans génération

Les exemples ci-dessous sont des sorties réelles du 25/09/2026, tronquées.

Toutes les commandes sont dans `COMMANDS` de [bin/pdb.py](../bin/pdb.py) ; `-h` donne les
options. Conventions communes :

- sortie en TSV par défaut ; `--format md|json` selon la commande ;
- première ligne = en-tête de colonnes, pas de bannière. Les lignes qui commencent par `#`
  sont des notes (troncature, avertissement, légende) ;
- papiers désignés par un **identifiant court** : l'`arxiv_id` (`1612.07119`), sinon
  `année-auteur` (`2022-feng`), sinon l'id complet en cas de collision. La légende
  `# ids: court=paper_id` en fin de sortie donne la correspondance ;
- code de sortie 0 si des résultats existent, 1 sinon, 2 pour une erreur d'argument.

### 5.1 `pdb bench` — N0 sur `benchmarks.csv`

```
bin/pdb bench [--platform S] [--model S] [--task S] [--quant S] [--toolflow S] [--dataset S]
              [--paper ID] [--where COL=S]… [--min COL=X]… [--max COL=X]… [--has COL]…
              [--cols a,b,c | --count a,b] [--sort COL [--desc]] [-n N]
              [--format tsv|md|json] [--max-chars N] [--check]
bin/pdb bench --add-columns COL,…|all
```

- Les filtres texte portent sur une sous-chaîne, insensible à la casse. Les raccourcis
  (`--platform`…) valent `--where` sur la colonne du même nom ; `--quant` porte sur
  `quantization`. Toute colonne de l'en-tête du CSV est acceptée par `--where`, `--min`,
  `--max`, `--has`, `--cols` et `--sort` ; une colonne inconnue renvoie le code 2 avec la
  liste des colonnes valides.
- `--min` et `--max` excluent les `n/r` ; `--has power_w` aussi.
- `--paper` accepte un id complet, un id court ou un mot du titre (comme `pdb paper`).
- Colonnes **toujours incluses**, même avec `--cols` : `paper_id` (court), `source_section`,
  `confidence`, `power_scope` (si une colonne de puissance est affichée).
- Les `n/r` restent `n/r`. Le tri numérique les place en dernier.
- Une ligne dont `confidence` vaut `low` est préfixée de `!`. Un pied de sortie rappelle :
  `# ! = confidence low`.
- Quand des lignes sont identiques sur les colonnes affichées, le pied dit par quelles
  colonnes masquées elles diffèrent. Par exemple, les deux lignes CNV-max de FINN diffèrent
  par `dataset` (CIFAR-10 et SVHN).
- `--max-chars` compte la sortie entière, pied compris. La coupe se fait par lignes
  entières, et la légende des ids ne porte que sur les lignes gardées.
- Codes de sortie : 0 s'il y a des lignes, 1 s'il n'y en a aucune, 2 pour une erreur
  d'argument.
- `--count col,col` remplace les lignes par une synthèse : nombre de lignes par combinaison
  de valeurs, triée par effectif. Exemple : `--has power_w --count paper_id,power_scope`
  dit en 9 lignes qui mesure la puissance, et avec quelle portée.

```
$ bin/pdb bench --platform kv260 --cols model,quantization,fps,power_w
paper	model	quantization	fps	power_w	power_scope	source_section	confidence
2507.18174	YOLOv5 (variante n/r)	INT8	9	3.5	unspecified	Table I	high
…
# ids: 2507.18174=arxiv-2507.18174-real-time-object-detection-classification
```

Coût : ~40 tokens par ligne, contre ~10 000 pour lire `benchmarks.csv` en entier (38 Ko).

**Colonnes optionnelles et `--check`** (DATA_MODEL §7). `--add-columns all` ajoute à l'en-tête
les colonnes optionnelles (`chunk_id`, `metric_def`, `dataset_split`, `input_res`, `batch`,
`measure_protocol`, `original_value`), à `n/r` dans les lignes existantes. Ensuite, filtres et
`--cols` les acceptent comme les autres. `--check` prend les lignes filtrées qui ont un
`chunk_id` et cherche chaque valeur numérique dans le passage cité (`rag.number_tokens`).
Seules les valeurs qui n'y sont pas sont listées, avec l'un de ces statuts :

| Statut | Signification |
|---|---|
| `section` | la valeur est dans un autre passage de la même section (tableau coupé en fenêtres) |
| `converti` | la valeur manque, mais les nombres de `original_value` sont lus dans la section |
| `absent` | la valeur n'est pas trouvée |
| `introuvable` | le `chunk_id` ne correspond à aucun passage de ce papier |

Code 1 si une valeur est `absent` ou un `chunk_id` `introuvable`.

**`--comparable [accuracy|power]`** regroupe les lignes filtrées dont la valeur comparée est
renseignée (`accuracy_value`, ou `power_w` en mode `power`) par conditions de comparaison :
`task`, `dataset`, `dataset_split`, puis la métrique (mode `accuracy`) ou `power_scope` (mode
`power`). La métrique est `metric_def`, à défaut `accuracy_metric` préfixée de `~`
(définition non vérifiée). Une colonne optionnelle absente vaut `n/r`. Les valeurs sont
comparées sans casse ni espaces multiples, sans autre normalisation : « top-1 » et « top-1
accuracy » restent deux groupes, signalés.

- Seuls les groupes d'au moins deux papiers sont listés ; `-n` et `--max-chars` portent sur
  eux, et `--format json` donne tous les groupes avec leurs lignes.
- `power_scope` (mode `accuracy`) liste les portées du groupe, pour information. `varie`
  liste les conditions qui changent dans le groupe (`quantization`, `input_res`, `batch`,
  `measure_protocol`) : des réserves, pas des interdictions.
- Le pied signale les définitions non vérifiées (`~`), les groupes dont la clé contient
  `n/r` (comparabilité non établie) et les **comparaisons impossibles** : même tâche et même
  jeu, répartis sur plusieurs groupes, avec la colonne qui les sépare.

```
$ bin/pdb bench --comparable power
g	n	papers	task	dataset	dataset_split	power_scope	varie
1	9	2	classification	ImageNet	n/r	board	quantization
2	9	2	detection	UA-DETRAC	n/r	unspecified	quantization
3	7	2	detection	COCO	n/r	unspecified	quantization
# n/r dans la clé (dataset_split…) : comparabilité non établie, 3 groupe(s)
# comparaisons impossibles (même tâche et même jeu, autres conditions) :
#   classification / ImageNet : 2 groupes, 3 papier(s) (power_scope : board | unspecified)
…
# 43 groupe(s) d'un seul papier omis (--format json pour tout voir)
```

Sur fpga (03/10/2026), `--task detection --dataset coco --comparable` donne 56 lignes de 7
papiers en 9 groupes, dont aucun ne réunit deux papiers : chaque papier nomme sa mAP à sa
façon (`mAP@0.5:0.95`, `mAP50 COCO`, `mAP*`…), ou son jeu (`COCO val (5000 images)`,
`COCO (split n/r)`).

```
$ bin/pdb bench --check --paper 2110.10486
line	paper	chunk_id	column	value	status
2	2110.10486	2110.10486#033.0	latency_ms	2070	absent
# 1 ligne(s) avec chunk_id, 3 valeur(s) vérifiée(s), 1 dans le passage cité (33 %)
```

### 5.2 `pdb search` — N1, recherche de passages

```
bin/pdb search "<question>" [-k 8] [--paper ID] [--axis A] [--section S] [--kind K]
               [--mode hybrid|dense|lexical] [--rerank] [--ids-only] [--format tsv|json]
```

`--rerank` reclasse les 30 premiers résultats de la fusion avec le cross-encoder
`cross-encoder/ms-marco-MiniLM-L-6-v2` (~90 Mo, téléchargé au premier appel). Il améliore
les requêtes en anglais et dégrade un peu le classement en français (§10). Coût : +1,2 s.
Il n'est pas activé par défaut, mais `/paper-ask`, qui formule en anglais, l'utilise.

Une ligne par passage : `chunk`, `section`, `page`, `cos` (cosinus avec la requête, `n/r` en
lexical), `snippet`. L'extrait fait ~160 caractères ; il est centré sur le terme de la
requête le plus rare présent, et les termes rares sont mis entre `«»`.

```
$ bin/pdb search "power measured at the wall versus the FPGA rails" -k 3
chunk	section	page	cos	snippet
1612.07119#022.0	5. EVALUATION / 5.2.2. Energy Efficiency	8	0.78	…FPS per Watt for the prototypes for both the «wall» «power» and «FPGA» «power» readings…
2025-hozhabr#051.1	V. RESULTS ANALYSIS AND OPTIMIZATION / B. COMPARATIVE ANALYSIS…	31	0.77	…
1612.07119#019.3	5. EVALUATION / 5.1. Experimental Setup	7	0.73	…the PMBus interface to monitor the «FPGA» «power» supply «rails», and P «wall» using a «wall» «power» meter…
# ids: 2025-hozhabr=2025-hozhabr-survey-real-time-object-detection 1612.07119=arxiv-1612.07119-finn-framework-fast-scalable-binarized
```

Coût : ~70 tokens par résultat, soit ~600 pour `-k 8`. `--ids-only` descend à ~15 tokens par
résultat, utile pour enchaîner avec `show`.

### 5.3 `pdb show` — texte exact d'un passage

```
bin/pdb show <chunk_id>… [--context N]
```

Affiche pour chaque passage un en-tête `## <chunk_id> — <section> — p. <page> — sha1:<8 car.>`,
suivi du texte exact. `--context 1` ajoute les passages voisins du même papier, marqués
`(contexte)`. Coût : ~270 tokens par passage de 200 mots.

### 5.4 `pdb paper` — fiche d'identité d'un papier

```
bin/pdb paper <id|court|sous-chaîne>… [--fields a,b,…] [--bench] [--format tsv|md|json]
```

- Sortie : une ligne `clé<TAB>valeur` par champ. Champs : `id`, `short`, `title`,
  `authors`, `year`, `venue`, `type`, `doi`, `url`, `axes`, `tags`, `fiche` (`done`/`todo`),
  `benchmarks` (nombre de lignes) et `warnings` (avertissements d'extraction).
- Le type `preprint` est suivi de « (non relu par les pairs) ».
- `--bench` ajoute les lignes du papier, dans le rendu de `bench`.
- Une sous-chaîne ambiguë renvoie la liste des candidats (id court, année, titre), sans
  autres données, avec le code 1. Par exemple, `pdb paper finn` renvoie FINN et FINN-R.
- Id court : l'`arxiv_id` s'il existe, sinon `année-auteur` (`2022-feng`) ; l'id complet en
  cas de collision.
- Plusieurs arguments : en-tête des champs, puis une ligne TSV par papier (champs par
  défaut `short,year,type,title`). Un argument ambigu ou inconnu est signalé sur stderr
  (`# finn : ambigu : 1612.07119, 1809.04570`) sans bloquer les autres, avec le code 1 ;
  `--bench` est refusé.

### 5.5 `pdb cites` / `pdb cited-by` — graphe de citations

```
bin/pdb cites <id> [--external]   # références du papier présentes dans la base
bin/pdb cited-by <id>             # papiers de la base qui le citent
```

Même rapprochement que la vue 3D et `external_refs.csv` (`lib/refs.group_refs`,
DATA_MODEL §6 : arXiv, DOI, titre normalisé, titres quasi identiques).

- Première ligne : `# <id> cite N papier(s) de la base et M travaux hors base`.
- Puis une ligne `id_court<TAB>année<TAB>titre` par papier de la base, par année.
- `--external` ajoute les travaux hors base, du plus cité au moins cité dans le corpus :
  `ext<TAB>n_citants<TAB>année<TAB>titre<TAB>arXiv:…|doi:…|n/r`.
- Pied `# ids:` pour les ids courts, comme `search`.

### 5.6 `pdb verify` — contrôle d'une citation

```
bin/pdb verify <chunk_id> "<citation textuelle>" [--sha1 X]
```

- Normalise les deux textes avant de comparer : ligatures (`ﬁ`→`fi`), casse, césures
  (`energy- efficient`), puis retrait de tout ce qui n'est ni lettre ni chiffre (espaces,
  ponctuation, tirets, guillemets).
- Recherche exacte, puis, à défaut, meilleure fenêtre `difflib.SequenceMatcher`.
- Sortie sur une ligne `statut<TAB>ratio<TAB>chunk_id` :
  - `OK` : présente telle quelle (après normalisation) ;
  - `APPROX` : ressemblance ≥ 0,85 (`rag.VERIFY_MIN`) ;
  - `NOMBRES` : ressemblance ≥ 0,85, mais les nombres de la citation ne sont pas ceux du
    passage (depuis le 26/09/2026, voir ci-dessous) ;
  - `ABSENT` : ressemblance < 0,85 ;
  - `MODIFIÉ` : le passage a changé depuis que `--sha1` a été relevé avec `pdb show`.
- Code de sortie 0 pour `OK` et `APPROX` seulement.
- **Contrôle des nombres** (`rag.numbers_match`). Un chiffre changé dans une phrase longue
  laisse la ressemblance au-dessus de 0,85 : avant ce contrôle, `verify` répondait `APPROX`
  à 38 citations sur 38 dont un chiffre avait été modifié (EVAL.md §5). Désormais :
  - les nombres de la citation (« 143,927 » = « 143 927 ») doivent former une suite contiguë
    des nombres du passage, morceau par morceau si la citation est élidée par « … » ;
  - chaque nombre doit y figurer avec ses mots voisins : « Section 3 reviews » est refusé
    même si le passage contient un 3 ailleurs ;
  - un nombre n'est tronqué (« 5 W » tiré de « 3.5 W ») qu'au bord de la citation.

  Si un autre passage du papier a les bons nombres, il est proposé (« trouvée dans »). La
  normalisation retirant la ponctuation, c'est aussi ce contrôle qui distingue « 94.9 % » de
  « 949 % ». Un mot remplacé juste à côté d'un nombre donne aussi `NOMBRES`.
- Une citation absente du passage indiqué, mais présente ailleurs dans le papier, est
  signalée avec `trouvée dans <chunk_id>`, et le code de sortie vaut 1 : la source citée
  était fausse.
- Une ligature perdue à l'extraction (« E cient » pour « Efficient ») n'est pas réparée : elle
  donne `APPROX`.

```
$ bin/pdb verify 1612.07119#019.3 "P-wall using a wall-power meter for the whole board power consumption"
APPROX	0.95	1612.07119#019.3
$ bin/pdb verify 1612.07119#019.0 "Figure 10 plots the achieved FPS per Watt"
OK	1.00	1612.07119#019.0	trouvée dans 1612.07119#022.0
```

---

## 6. Économie de tokens

| Tâche | Aujourd'hui | Avec la couche de recherche |
|---|---|---|
| Un chiffre sur une plateforme | lire `benchmarks.csv` (~10 000 tokens) ou `grep` puis interpréter | `bench` filtré : 100-400 |
| Trouver où un sujet est traité | `grep` sur `sections.jsonl` (lignes JSON entières, jusqu'à 1 500 tokens par ligne) ; échoue sur les synonymes | `search -k 8` : ~600 |
| Lire la preuve d'une affirmation | ouvrir `fulltext.md` (~18 000 tokens en moyenne) | `show` sur 1 à 3 passages : 300-900 |
| Vérifier une citation | relire le passage | `verify` : ~20 |

Règles d'usage, reprises dans la skill `/paper-ask` (§8) :

1. **Divulgation progressive** : `search`, puis `show` sur 2 ou 3 passages au plus, jamais
   `fulltext.md` d'emblée.
2. **Filtrer à la source** : `--paper`, `--section`, `--cols` plutôt que de filtrer après lecture.
3. **Ne pas reformuler une sortie suffisante** : une sortie N0/N1 qui répond déjà est
   transmise telle quelle, avec les sources.
4. **Budget explicite** : `bench --max-chars`, `search -k`.
5. Pas de cache de réponses : les commandes sont locales. `bench` et `paper` répondent
   instantanément, `show` et `verify` en ~0,3 s, `search` en ~6 s (import de torch).

---

## 7. Vérifiabilité

| Élément renvoyé | Comment le vérifier |
|---|---|
| Passage | `chunk_id` → `pdb show` ; `page` → le PDF (DATA_MODEL §5) ; `sha1` → détecte une ré-extraction depuis la citation |
| Citation textuelle | `pdb verify <chunk_id> "<citation>"` |
| Chiffre | ligne de `pdb bench`, qui porte `source_section` et `confidence` → `pdb search "<table>" --paper <id>` pour relire la table |
| Classement | déterministe : même index, même requête, même classement (§4.2) |
| Absence d'information | `search` sans résultat pertinent ou `bench` vide : c'est un constat sur la base, pas sur la littérature. On le dit, et on le relie à `gaps.md` si c'est pertinent |

Ce qui ne se vérifie pas automatiquement : les paraphrases, les rapprochements entre papiers
et les inférences. Elles sont étiquetées **déduit** dans la réponse, selon la règle « Lu vs
déduit » de `CLAUDE.md`.

Format de citation dans les réponses rédigées : `[1612.07119#019.3]`, et la légende des
identifiants courts en fin de réponse.

---

## 8. Skill `/paper-ask`

Fichier [.claude/commands/paper-ask.md](../.claude/commands/paper-ask.md). Outils autorisés :
`Read`, `bin/pdb bench|search|show|paper|verify`. Déroulé demandé à Claude :

0. Avant la recherche : 2 à 5 **exigences** tirées de la question (ce qu'une réponse
   complète doit établir).
1. Question chiffrée : `pdb bench` d'abord (N0).
2. Sinon, ou en complément : `pdb search --rerank` avec une ou deux formulations **en anglais**, `-k 8` ;
   aucun score ne détecte le hors-corpus, c'est le contenu des extraits qui décide → ne pas combler.
3. `pdb show` sur les 2 ou 3 passages les plus prometteurs seulement ; jamais `fulltext.md`.
4. Réponse avec citations `[chunk_id]` ; `pdb verify` sur chaque citation textuelle ; toute
   citation `ABSENT` est retirée, et un `chunk_id` faux est corrigé.
5. Suffisance (lot B, 02/10/2026) : chaque exigence `couvert` (passage vérifié), `partiel`
   (passage voisin : autre plateforme, batch, portée de puissance) ou `absent` ; verdict
   `suffisant` (toutes couvertes), `absent` (toutes absentes) ou `partiel`. La réponse
   s'ouvre par le verdict et les exigences, puis **Lu** (sourcé), **Déduit**, **Non trouvé
   dans la base** (exigences absentes). Un verdict `absent` renvoie à `/paper-discover`.
   Signalements obligatoires : `confidence: low`, `preprint`, `power_scope` hétérogènes.
6. 2 ou 3 pistes (règle de `CLAUDE.md`).

---

## 9. Installation et reconstruction

1. **Dépendances** : `.venv/bin/pip install -r requirements-embed.txt`. Le premier
   `bin/pdb reindex` télécharge `bge-small-en-v1.5` (~130 Mo) et encode tout le corpus
   (~3 min). Sans cette dépendance, tout fonctionne en lexical seul.
2. **Construire ou mettre à jour** : `bin/pdb reindex`. `add` et `ingest` le font d'eux-mêmes.
3. **Contrôler** :
   ```bash
   bin/pdb search "binarized neural network streaming architecture" -k 5
   bin/pdb show <chunk_id renvoyé>
   bin/pdb verify <chunk_id> "<phrase copiée>"      # → OK
   bin/pdb test          # tests unitaires (encodeur factice)
   bin/pdb eval --rag    # évaluation sur le vrai modèle (§10)
   ```
4. **Route GPU (optionnelle)** : seulement si l'on veut se servir de sa carte graphique
   et qu'elle est CUDA. `bin/pdb gpu on` ; détails au §13.
5. **Changer de modèle** : `rag.DEFAULT_MODEL` (et `QUERY_PREFIX` si le modèle en demande
   un), puis `bin/pdb reindex` et `bin/pdb eval --rag` pour comparer. L'ancien cache reste
   dans `.cache/rag/` ; il peut être supprimé.

---

## 10. Évaluation

**Jeu** : [tests/fixtures/rag_eval.jsonl](../tests/fixtures/rag_eval.jsonl), 20 questions en
anglais, chacune avec :
- `expect` : les sections pertinentes (`paper#order`, indépendant du découpage en fenêtres) ;
- `papers` et `pattern` : la manière dont elles ont été choisies. Ce sont les sections des
  papiers cibles dont le texte contient le motif, par exemple `r"reuse factor"` dans les
  deux papiers hls4ml.

Les questions reformulent le sujet sans reprendre le motif quand c'était possible (« removes
duplicate bounding boxes » pour NMS), afin de tester la recherche par le sens. Deux motifs ont
été élargis après lecture des passages renvoyés : DAGM et BTAD pour les jeux de défauts de
surface, « SIMD lanes » pour le folding de FINN. Les passages renvoyés y répondaient bien à la
question, et les motifs d'origine étaient trop étroits.

**Métriques** : `recall@5` (au moins une section attendue dans les 5 premiers passages),
`MRR` (inverse du rang de la première bonne section) et `paper@5` (un passage d'un papier
cible dans les 5 premiers).

**Résultats du 25/09/2026** (2 405 passages) :

| Modèle | Mode | recall@5 EN | MRR EN | recall@5 FR (8 q.) | MRR FR |
|---|---|---|---|---|---|
| — | lexical (BM25) | **0,95** | **0,82** | 0,25 | 0,11 |
| all-MiniLM-L6-v2 | dense | 0,75 | 0,65 | 0,38 | 0,25 |
| all-MiniLM-L6-v2 | hybride | 0,95 | 0,74 | 0,50 | 0,25 |
| bge-small-en-v1.5 | dense | 0,90 | 0,79 | **0,62** | **0,46** |
| bge-small-en-v1.5 | hybride (défaut) | 0,90 | 0,79 | 0,50 | 0,33 |
| bge-small-en-v1.5 | hybride + rerank (`--rerank`) | **1,00** | **0,87** | 0,50 | 0,26 |

Après la ré-extraction du 25/09/2026 (ligatures réparées, 19 paragraphes rendus au corps,
2 396 passages), le rappel est inchangé partout ; les MRR bougent un peu (bge-small
hybride : 0,79 → 0,75 en anglais ; rerank : 0,87 → 0,85 ; BM25 : 0,82 → 0,75) et le rappel
BM25 en français monte (0,25 → 0,38).

La colonne FR porte sur 8 des questions, traduites à la main en français
([tests/fixtures/rag_eval_fr.jsonl](../tests/fixtures/rag_eval_fr.jsonl), mêmes `expect`,
question anglaise d'origine dans `en`). `bin/pdb eval --rag` évalue les deux jeux.

Lecture :
- **En anglais, les modes se valent** : sur 20 questions, un écart de 0,05 est une seule
  question. Le lexical est légèrement devant, ce qu'on attend puisque les sections attendues
  ont été choisies par mots-clés : l'évaluation favorise BM25.
- **En français, le lexical s'effondre** (0,25), et la recherche dense multilingue par
  accident de bge-small tient mieux.
- **Choix retenu : hybride avec bge-small**, le mode le plus robuste quand on ne sait pas
  comment la question sera formulée. La skill `/paper-ask` fait reformuler en anglais.
- **Reranking** : le cross-encoder récupère les 2 questions manquées en anglais. La première
  est la question NMS : « removes duplicate bounding boxes » ne contient ni « NMS » ni
  « non-maximum suppression », et aucun mode sans reranking ne la trouvait. En français, le
  rappel est inchangé et le MRR baisse (0,33 → 0,26), car le modèle est entraîné en
  anglais (MS MARCO).
- **Décision** : `--rerank` reste une option (règle fixée avant la mesure : activation par
  défaut seulement sans dégradation en français). `/paper-ask` l'active, parce qu'il
  formule toujours en anglais.
- **Réserve** : ces 20 questions ont servi à décider ; aucun réglage n'a été fait dessus,
  mais un jeu plus grand et écrit par quelqu'un d'autre confirmerait le gain.

Seuil d'acceptation proposé : recall@5 ≥ 0,8 en anglais. À relancer (`bin/pdb eval --rag`)
après tout changement de modèle, de découpage ou de fusion, et quand le corpus grossit.

**Mise à jour du 26/09/2026** : ce jeu fait désormais partie du banc `bin/pdb eval`
([EVAL.md](EVAL.md)), qui ajoute un jeu holdout de 25 questions jamais utilisé pour régler.
Sur ce holdout, le rappel est plus bas (hybride 0,84 ; rerank 0,80, mais MRR 0,65 → 0,78) :
le gain de rappel du rerank observé ici ne se généralise pas, son gain de classement si. Le
banc montre aussi que l'alerte « pertinence faible » ne se déclenche jamais et que `verify`
accepte (APPROX) une citation dont un chiffre a été modifié (EVAL.md §5).

---

## 11. Limites et évolutions

- **Taille du corpus** : ~2 000 passages ; une recherche exhaustive en numpy prend quelques
  millisecondes. Une base vectorielle serveur (Chroma, Qdrant, pgvector) n'apporterait rien
  avant ~10⁵ passages.
- **Tableaux et figures** : ils sont mal extraits (SETUP §9, tâche 8). Un chiffre absent de
  `benchmarks.csv` et pris dans une table cassée ne sera pas retrouvé de façon fiable, et
  `bench` reste la source de référence pour les chiffres.
- **Langue** : corpus et modèle en anglais. En français, la recherche perd beaucoup (§10) :
  une question en français doit être reformulée en anglais avant `search`, ce que fait la
  skill `/paper-ask`. Autre voie : un modèle multilingue
  (`paraphrase-multilingual-MiniLM-L12-v2`, `bge-m3`), puis `bin/pdb reindex` et
  `bin/pdb eval --rag` pour comparer.
- **Reclassement** (*reranking*) : en place en option (§5.2, §10). Évolution possible : un
  cross-encoder multilingue (`BAAI/bge-reranker-base`, plus lourd) pour ne plus dégrader
  le français. À évaluer avec `bin/pdb eval --rag`.
- **Serveur MCP** : exposer `search`, `show`, `bench` et `verify` comme outils MCP, pour les
  utiliser hors de ce dossier ou depuis une autre application. Même `lib/rag.py`, autre interface.
- **Généricité** : rien ici ne dépend du domaine FPGA. `bench` lit ses colonnes dans
  l'en-tête du CSV. Seuls ses raccourcis de filtre (`--platform`, `--quant`…) et le jeu
  d'évaluation sont propres au corpus.
- **Coût de démarrage** : ~6 s par commande `search` (0,1 s à chaud), dû à l'import de torch
  et au chargement du modèle ; `show` et `verify` s'en passent déjà (~0,3 s). Si cela gêne,
  un processus résident (serveur MCP ci-dessus) le paierait une seule fois. Le rerank
  ajoute ~1,4 s à chaud (EVAL.md §5).

---

## 12. Essai réel de `/paper-ask` (25/09/2026)

Question : « comment les papiers mesurent-ils la puissance, et est-ce comparable ? ».

**Déroulé suivi :**

| Étape | Commandes | Lu |
|---|---|---|
| N0 | `bench --has power_w`, agrégé à la main par papier et portée | 57 lignes, 8 papiers |
| N1 | 1 `search -k 10` (requête en anglais) | 3,2 Ko |
| Lecture | 1 `show` sur 3 passages | 3,8 Ko |
| Vérification | 7 `verify`, 8 `paper` (type de publication) | < 1 Ko |

Total : ~9 Ko lus, environ 2 500 tokens, sans ouvrir de `fulltext.md`. À titre de
comparaison, un seul `fulltext.md` en fait ~18 000 en moyenne.

**Ce qui a fonctionné :**
- les 7 citations textuelles sont revenues `OK` au premier essai ;
- la recherche a trouvé en une requête les quatre protocoles de mesure du corpus : FINN
  (PMBus et prise murale), 2211.11647 (multimètre à l'entrée de la carte), 2502.15737
  (tegrastats) et 2022-feng (puissance au repos mesurée avant les tests) ;
- la structure Lu / Déduit / Non trouvé a fait ressortir des points utiles :
  - la classe `chip` de 2502.15737 (tegrastats) est à vérifier ;
  - 2211.11647 décrit une mesure soignée mais n'a aucune ligne de puissance dans
    `benchmarks.csv`.

**Défauts relevés et corrigés :**
- l'id court de El Zeinaty était tronqué en `2025-el` : il est désormais pris dans le préfixe
  `année-auteur` du `paper_id` (test ajouté) ;
- l'agrégation par papier et portée demandait un `awk` : `bench --count` fait maintenant
  cette synthèse (test ajouté).

**Limites constatées :**
- 1 seul essai, jugé par la même instance qui l'a exécuté : ce n'est pas une évaluation
  indépendante ;
- `search` a renvoyé aussi des passages génériques (définition de la puissance dans les
  surveys, capteurs en introduction de hls4ml). Filtrer avec `--section` aurait réduit le
  bruit ;
- les 8 appels `paper` pour connaître le type de publication pourraient se réduire à un
  seul avec une option `--fields type` sur plusieurs ids. Fait depuis :
  `pdb paper id1 id2 … --fields short,type`, utilisé par `/paper-ask`.

---

## 13. Route GPU optionnelle (Qwen3)

Deux ensembles de recherche ont été développés en parallèle : la route décrite dans ce
document (`lib/rag.py`, CPU) et une route GPU apportée par Maksym Lytvynenko (`lib/rag_qwen.py`,
`lib/rag_models.py`, `lib/rag_external.py`, `bin/pdb rag`, `/paper-research` ;
[RAG_IMPLEMENTATION_PLAN.md](RAG_IMPLEMENTATION_PLAN.md)). Elles travaillent ensemble selon
une règle simple : **la route CPU est celle par défaut ; la route GPU ne sert que si
l'utilisateur veut utiliser sa carte graphique, et s'il en a une (CUDA).**

### 13.1 Quand utiliser quoi

| Besoin | Sans GPU (défaut) | Avec la route GPU activée |
|---|---|---|
| Chercher des passages | `pdb search` (BM25 + bge-small, rerank MiniLM) | `pdb search` : même commande, moteur Qwen3-Embedding-4B + Qwen3-Reranker-4B |
| Lire, vérifier une citation | `pdb show`, `pdb verify` | identiques (mêmes `chunk_id`) |
| Répondre à une question | `/paper-ask` | `/paper-ask` (moteur Qwen automatiquement) |
| Compléter la base par des articles open access | `/paper-discover`, `/paper-add` | en plus : `/paper-research` (`pdb rag acquire`, puis `approve` après accord) |
| Filtres exhaustifs sur les benchmarks | `pdb bench` | en plus : `pdb rag benchmarks --filter-json` |
| Évaluer la recherche | `pdb eval --rag` | `pdb eval --rag --gpu --compare <run CPU>` |

La route GPU est utile surtout pour les questions en français et le vocabulaire éloigné du
texte : sur les jeux de `pdb eval`, les modèles Qwen (mesurés avec `pdb rag`, RTX 5090 de
32 Go) retrouvent dans les 5 premiers les 8 questions françaises, contre 5 avec bge-small, et
gagnent 2 questions sur 25 au holdout, pour 3 à 4 s par requête avec rerank (EVAL.md §8,
BENCHMARK.md). En anglais, la route CPU fait aussi bien sur le pilote. Chaque modèle 4B en
BF16 occupe ~8 Go de mémoire GPU ; ils sont chargés l'un après l'autre. Les mesures du
moteur Qwen intégré à `pdb search` restent à faire : `pdb eval --rag --gpu --compare`.

### 13.2 Activer la route GPU

```bash
.venv/bin/pip install -r requirements-rag.txt   # torch, transformers (CUDA)
bin/pdb gpu            # état : demandée ? GPU détecté ? modèles en cache ? vecteurs de la base ?
bin/pdb gpu on         # active (réglage de la machine), télécharge les modèles (~16 Go) si
                       # besoin, puis réindexe la base active (vecteurs Qwen)
bin/pdb gpu off        # retour au moteur CPU
PDB_GPU=1 bin/pdb …    # active pour une commande ou une session ; PDB_GPU=0 désactive
```

Le réglage est enregistré dans `~/.config/pdb/config.json` (à côté du registre des bases) :
il concerne la machine, pas une base. `pdb search --gpu` ou `--cpu` force le moteur pour
une seule recherche.

**Repli.** Sans torch, sans CUDA, ou si les vecteurs Qwen de la base n'existent pas encore
(base pas réindexée depuis l'activation), `pdb search` reste sur le moteur CPU et l'écrit
sur stderr (`# route GPU indisponible : … ; moteur CPU`). Une question n'échoue jamais
faute de GPU. `pdb rag` en mode `dense`/`hybrid`, `acquire` et `approve` s'arrêtent au
contraire tout de suite avec un renvoi vers `pdb search` ; `pdb rag … --mode lexical`,
`evidence`, `benchmarks` et `check-answer` tournent sans GPU.

### 13.3 Ce qui est partagé

- **Passages et identifiants.** Le moteur Qwen de `pdb search` encode exactement les
  passages de `lib/rag.load_chunks` : `chunk_id`, `pdb show`, `pdb verify`, le mode
  enregistrement de `/paper-ask` et `pdb eval --answers` ne changent pas.
- **Cache.** `.cache/rag/` contient côte à côte `BAAI_bge-small-en-v1.5.npz` (CPU),
  `Qwen_Qwen3-Embedding-4B.npz` (GPU, même format, même clé `chunk_id:sha1`, réencodage
  incrémental) et, si `pdb rag index` a été lancé, `index.sqlite3` et `runs/` (route
  `pdb rag`).
- **Réindexation.** `pdb reindex` (et donc `add`, `ingest`) met toujours à jour les vecteurs
  CPU. Route GPU active : aussi les vecteurs Qwen et, s'il existe, l'index SQLite de
  `pdb rag`. Route inactive : un index `pdb rag` périmé est seulement signalé.
- **Modèles.** Une seule définition des modèles épinglés (révisions comprises) :
  `lib/rag_models.py`, utilisée par `pdb search --gpu`, `pdb rag` et l'acquisition.

### 13.4 Ce qui reste propre à `pdb rag`

`pdb rag` garde son index SQLite (FTS5 + vecteurs Qwen sur des morceaux de 512 jetons, avec
fiches et lignes de `benchmarks.csv` indexées comme preuves), ses `evidence_id` hachés et
son contrôle `check-answer` (identité et présence de l'extrait, pas les nombres). C'est
l'outil de `/paper-research`, qui ajoute la boucle de lacunes et l'acquisition open access
(OpenAlex + arXiv, budget borné, staging, import seulement après accord). Les deux formats
d'identifiants ne se mélangent pas dans une même réponse. Unification restante (lot G de
[AMELIORATIONS.md](AMELIORATIONS.md)) : `check-answer` qui contrôle aussi les nombres, et
`/paper-research` sur les `chunk_id` de `pdb search`.

