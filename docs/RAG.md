# Recherche de passages (RAG) et requêtes sans génération

Spécification de la couche de recherche de PaperDatabase : ce qu'elle doit faire, comment la
construire, comment s'en servir. **Statut : partiellement en place** (voir [SETUP.md §9](../SETUP.md#9-état-actuel-et-tâches-à-faire)).
En place depuis le 25/09/2026 : `pdb bench` (§5.1) et `pdb paper` (§5.4), dans
[lib/query.py](../lib/query.py). Le reste (index de passages, `search`, `show`, `verify`,
`cites`, `/paper-ask`) est à implémenter.

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

## 2. Ce qui existe déjà et ce qui manque

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
  recouvrement. `all-MiniLM-L6-v2` tronque au-delà de 256 tokens, soit environ 200 mots, et
  une entrée non découpée perdrait donc sa fin.
- Identifiant de passage : `chunk_id = <id de la section>.<k>`, par exemple
  `arxiv-1612.07119-finn-framework-fast-scalable-binarized#014.2`. `k` commence à 0 ; une
  section non découpée a le seul passage `.0`.
- Chaque passage garde : `chunk_id`, `paper_id`, `kind`, `section`, `subsection`, `page`,
  `text`, et `sha1` du texte.
- Le texte encodé est préfixé du titre de section (`"3. Experimental Results — …"`). Cela
  donne du contexte au vecteur sans modifier le texte renvoyé.

Volume attendu : ~2 000 passages pour le corpus actuel.

### 4.2 Deux index, une fusion

| Index | Rôle | Implémentation |
|---|---|---|
| Dense | proximité de sens, synonymes, reformulations | `all-MiniLM-L6-v2` via `lib/embed._encode` (vecteurs normalisés, produit scalaire = cosinus). Variante plus précise : `BAAI/bge-small-en-v1.5` (même taille de vecteur, 384) |
| Lexical (BM25) | termes exacts : noms de cartes (`ZCU104`), de modèles (`YOLOv5n`), sigles, nombres | BM25 écrit à la main (~40 lignes, `k1=1.5`, `b=0.75`), avec une tokenisation qui conserve les jetons alphanumériques (`int8`, `kv260`, `yolov5`) |

**Fusion par *Reciprocal Rank Fusion* :** `score(d) = Σ 1 / (60 + rang_i(d))` sur les deux
classements. Cette méthode ne dépend pas de l'échelle des scores, ne demande aucun réglage,
et elle est déterministe. En cas d'égalité, le `chunk_id` le plus petit passe en premier.

Filtres appliqués **avant** le classement : `--paper`, `--axis` (lu dans `metadata.json`),
`--kind`, `--section` (sous-chaîne, insensible à la casse), `--since`.

### 4.3 Stockage et mise à jour

- Emplacement : `.cache/rag/`, déjà ignoré par git. L'index est dérivé de la base et
  reconstructible ; il ne va jamais dans `papers/`.
  - `chunks.jsonl` : les passages (§4.1) ;
  - `<modèle>.npz` : matrice des vecteurs, clés `chunk_id:sha1` (même principe que le cache de `lib/embed.py`) ;
  - `bm25.json` : fréquences documentaires et longueurs ;
  - `manifest.json` : modèle, date, nombre de passages, sha1 de chaque `sections.jsonl`.
- Mise à jour incrémentale : seuls les papiers dont le sha1 de `sections.jsonl` a changé sont
  redécoupés et réencodés. Le BM25 est recalculé en entier, ce qui prend moins d'une seconde.
- Déclenchement : `bin/reindex.py` appelle `rag.build_index()` quand `sentence_transformers`
  est présent (`embed.available()`). Sinon, seul le BM25 est construit et `search` le signale
  en tête de sortie (`# mode: lexical seul`). `add` et `ingest` passent déjà par `reindex`.

### 4.4 Module `lib/rag.py` — API proposée

```python
build_index(root, model=DEFAULT_MODEL, force=False) -> dict      # manifest
search(query, k=8, filters=None, mode="hybrid") -> list[Hit]      # Hit: chunk_id, paper_id, section, page, score, snippet, sha1
get(chunk_id, context=0) -> list[Chunk]                            # passage exact, ± voisins
verify(chunk_id, quote) -> tuple[str, float]                       # ("OK"|"APPROX"|"ABSENT", ratio)
```

Réutiliser : `embed._encode`, `embed.available`, `embed._digest` ([lib/embed.py](../lib/embed.py)) ;
le chargement du corpus de `lib/graph.load_corpus` pour les métadonnées (axes, titres).

---

## 5. Commandes sans génération

Les sorties montrées ci-dessous sont **illustratives** (format visé) ; les `chunk_id` et
scores y sont fictifs, sauf la ligne de `bench`, tirée de `benchmarks.csv`.

Toutes les commandes s'ajoutent au dictionnaire `COMMANDS` de [bin/pdb.py](../bin/pdb.py) et à
sa docstring. Conventions communes à toutes les sorties :

- sortie en TSV par défaut, `--format md|json` à la demande ;
- première ligne = en-tête de colonnes, et rien d'autre : pas de bannière ni de texte d'aide ;
- `--max-chars N` tronque la sortie totale et termine par `# tronqué : N lignes omises` ;
- papiers désignés par un **identifiant court** (`finn`, `2507.18174`, `hozhabr25`…) quand une
  colonne le répète. Une légende `# ids: court=paper_id` en fin de sortie donne la
  correspondance, une fois par identifiant ;
- code de sortie 0 si des résultats existent, 1 sinon. Claude peut ainsi enchaîner sans lire
  une sortie vide.

### 5.1 `pdb bench` — N0 sur `benchmarks.csv`

```
bin/pdb bench [--platform S] [--model S] [--task S] [--quant S] [--toolflow S] [--dataset S]
              [--paper ID] [--where COL=S]… [--min COL=X]… [--max COL=X]… [--has COL]…
              [--cols a,b,c] [--sort COL [--desc]] [-n N] [--format tsv|md|json] [--max-chars N]
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

```
$ bin/pdb bench --platform kv260 --cols model,quantization,fps,power_w
paper	model	quantization	fps	power_w	power_scope	source_section	confidence
2507.18174	YOLOv5 (variante n/r)	INT8	9	3.5	unspecified	Table I	high
…
# ids: 2507.18174=arxiv-2507.18174-real-time-object-detection-classification
```

Coût : ~40 tokens par ligne, contre ~10 000 pour lire `benchmarks.csv` en entier (38 Ko).

### 5.2 `pdb search` — N1, recherche de passages

```
bin/pdb search "<question>" [-k 8] [--paper ID] [--axis A] [--section S] [--kind K]
               [--mode hybrid|dense|lexical] [--ids-only]
```

Une ligne par passage : `chunk_id  section  p.  score  extrait`. L'extrait fait ~160 caractères
et il est centré sur le terme de la requête le mieux représenté, mis entre `«»`.

```
$ bin/pdb search "power measured at the wall vs chip" -k 3
chunk	section	page	score	snippet
finn#021.0	5.1 Experimental Setup	7	0.032	…we report «power» both at the «wall» (P_wall) and on-«chip» (P_chip) using…
…
```

Coût : ~70 tokens par résultat, soit ~600 pour `-k 8`. `--ids-only` descend à ~15 tokens par
résultat, utile pour enchaîner avec `show`.

### 5.3 `pdb show` — texte exact d'un passage

```
bin/pdb show <chunk_id>… [--context N]
```

Affiche pour chaque passage un en-tête `## <chunk_id> — <section> — p. <page> — sha1:<8 car.>`,
suivi du texte exact. `--context 1` ajoute le passage précédent et le suivant. Coût : ~270
tokens par passage de 200 mots.

### 5.4 `pdb paper` — fiche d'identité d'un papier

```
bin/pdb paper <id|court|sous-chaîne> [--fields a,b,…] [--bench] [--format tsv|md|json]
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

### 5.5 `pdb cites` / `pdb cited-by` — graphe de citations

```
bin/pdb cites <id>        # références du papier présentes dans la base
bin/pdb cited-by <id>     # papiers de la base qui le citent
```

Réutilise `lib/refs.ref_keys` et le rapprochement de DATA_MODEL §6. L'option `--external`
inclut les références hors base (titre, année, nombre de citants, comme `external_refs.csv`).

### 5.6 `pdb verify` — contrôle d'une citation

```
bin/pdb verify <chunk_id> "<citation textuelle>"
```

- Normalise les deux textes avant de comparer : casse, espaces, ligatures (`ﬁ`→`fi`, et
  ligatures perdues comme « E cient »), tirets et césures, guillemets.
- Recherche exacte, puis, à défaut, meilleure fenêtre `difflib.SequenceMatcher`.
- Sortie sur une ligne :
  - `OK` : présente telle quelle ;
  - `APPROX 0.93` : ratio ≥ 0,85, avec la fenêtre trouvée ;
  - `ABSENT` : ratio < 0,85.
- `--sha1 <8 car.>` signale `MODIFIÉ` si le passage a changé depuis que la citation a été prise.

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
4. **Budget explicite** : `--max-chars 4000` par défaut dans la skill.
5. Le cache HTTP ou de réponses n'est **pas** nécessaire : les commandes sont locales et
   s'exécutent en moins d'une seconde une fois l'index chargé.

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

Format de citation dans les réponses rédigées : `[finn#021.0]`, et la légende des
identifiants courts en fin de réponse.

---

## 8. Skill `/paper-ask`

Fichier `.claude/commands/paper-ask.md`, sur le modèle de `paper-gaps.md` :

```markdown
---
description: Répond à une question sur le corpus par recherche de passages sourcés (sans lire fulltext.md)
allowed-tools: Read, Bash(bin/pdb bench:*), Bash(bin/pdb search:*), Bash(bin/pdb show:*), Bash(bin/pdb paper:*), Bash(bin/pdb cites:*), Bash(bin/pdb cited-by:*), Bash(bin/pdb verify:*)
---
```

Déroulé demandé à Claude :

1. Question chiffrée : `pdb bench` d'abord (N0).
2. Sinon, ou en complément : `pdb search` avec 1 ou 2 formulations en anglais (le corpus est
   en anglais), `-k 8`.
3. `pdb show` sur les 2 ou 3 passages les plus prometteurs seulement.
4. Réponse avec citations `[chunk_id]` ; `pdb verify` sur chaque citation textuelle ; toute
   citation `ABSENT` est retirée.
5. Structure : **Lu** (sourcé), puis **Déduit**, puis **Non trouvé dans la base**.
   Signalements obligatoires : `confidence: low`, `preprint`, `power_scope` hétérogènes.
6. 2 ou 3 pistes (règle de `CLAUDE.md`).

---

## 9. Mise en place, pas à pas

1. **Dépendances** : `.venv/bin/pip install -r requirements-embed.txt`, déjà fait sur la
   machine actuelle. Le premier appel télécharge le modèle (~90 Mo).
2. **Écrire `lib/rag.py`** (§4) et `tests/test_rag.py`, avec un encodeur factice comme
   `fake_encode` dans [tests/test_embed.py](../tests/test_embed.py) : les tests ne doivent pas
   dépendre de sentence-transformers.
3. **Ajouter les commandes** `bench`, `search`, `show`, `paper`, `cites`, `cited-by` et
   `verify` à `bin/pdb.py` (§5). `bench` et `paper` sont indépendantes de l'index et peuvent
   être écrites en premier : ce sont celles qui économisent le plus.
4. **Brancher `build_index()` dans `bin/reindex.py`** (§4.3).
5. **Construire et tester** :
   ```bash
   bin/pdb reindex
   bin/pdb search "binarized neural network streaming architecture" -k 5
   bin/pdb show <chunk_id renvoyé>
   bin/pdb verify <chunk_id> "<phrase copiée>"      # → OK
   bin/pdb test
   ```
6. **Écrire `.claude/commands/paper-ask.md`** (§8).
7. **Mettre à jour la documentation** :
   - `CLAUDE.md` (« Comment chercher ici » ; déjà fait) ;
   - SETUP.md §5 : nouvelles commandes ; SETUP.md §9 : cocher les tâches ;
   - docs/GUIDE.md : exemples d'usage.
   Passer le statut en tête de ce fichier à « en place ».

---

## 10. Évaluation

- `tests/fixtures/rag_eval.jsonl` contient ~20 questions écrites à la main. Chacune donne les
  `chunk_id` qui y répondent et le niveau attendu (N0/N1) :
  `{"q": "…", "expect": ["finn#021.0"], "level": "N1"}`.
- Métriques : **recall@5** (au moins un passage attendu dans les 5 premiers) et **MRR**.
  Seuil d'acceptation proposé : recall@5 ≥ 0,8.
- Comparaison `--mode dense | lexical | hybrid` pour justifier la fusion et le choix du modèle.
- Le script d'évaluation est lancé à la main (`bin/pdb test --rag`) : il a besoin du vrai
  modèle, contrairement aux tests unitaires.

---

## 11. Limites et évolutions

- **Taille du corpus** : ~2 000 passages ; une recherche exhaustive en numpy prend quelques
  millisecondes. Une base vectorielle serveur (Chroma, Qdrant, pgvector) n'apporterait rien
  avant ~10⁵ passages.
- **Tableaux et figures** : ils sont mal extraits (SETUP §9, tâche 8). Un chiffre absent de
  `benchmarks.csv` et pris dans une table cassée ne sera pas retrouvé de façon fiable, et
  `bench` reste la source de référence pour les chiffres.
- **Langue** : le corpus et le modèle sont en anglais. Une question en français est reformulée
  en anglais par Claude avant `search`. Sinon, on peut passer à
  `paraphrase-multilingual-MiniLM-L12-v2`, ce qui demande de reconstruire l'index.
- **Reclassement** (*reranking*) par un cross-encoder (`cross-encoder/ms-marco-MiniLM-L-6-v2`)
  sur les 30 premiers résultats : à envisager seulement si l'évaluation (§10) le justifie.
- **Serveur MCP** : exposer `search`, `show`, `bench` et `verify` comme outils MCP, pour les
  utiliser hors de ce dossier ou depuis une autre application. Même `lib/rag.py`, autre interface.
- **Généricité** : rien ici ne dépend du domaine FPGA. Seuls `bench` (colonnes de
  `benchmarks.csv`) et les axes sont propres au corpus, et `bench` devrait lire les colonnes
  depuis l'en-tête du CSV plutôt que les coder en dur.
