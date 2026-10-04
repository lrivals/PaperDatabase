# PaperDatabase — guide technique

Base de connaissance d'articles scientifiques (vision embarquée sur FPGA), conçue pour être
interrogée par Claude Code.

Ce document décrit **ce qui est en place, comment le réinstaller et le faire tourner, et ce
qui reste à faire** (§9). Les schémas de données exacts sont dans
[DATA_MODEL.md](DATA_MODEL.md). Le mode d'emploi destiné à l'agent est dans
[CLAUDE.md](CLAUDE.md).

---

## 1. Principe

Le consommateur final de cette base n'est pas un moteur de recherche vectoriel : c'est
**Claude Code**, qui dispose déjà de `grep`, `glob` et `read`. Sur un corpus de quelques
dizaines à quelques centaines d'articles, une arborescence bien nommée avec un index et un
CSV greppable fait mieux qu'un index d'embeddings — et reste lisible, diffable et réparable
à la main.

D'où trois règles de conception :

1. **Tout est du texte.** Pas de base de données, pas de vector store, pas de format binaire
   à part le PDF d'origine conservé comme preuve.
2. **Chaque chiffre est traçable.** Toute valeur du tableau comparatif porte la section de
   l'article d'où elle vient. Une valeur non rapportée par les auteurs s'écrit `n/r`, jamais
   une estimation.
3. **L'agent lit du résumé vers le détail.** `INDEX.md` → `benchmarks.csv` → `fiche.md` →
   `fulltext.md`. Le PDF n'est jamais rouvert par l'agent.

Ce que le pipeline produit, pour chaque article : des métadonnées vérifiées, un texte
nettoyé et découpé en sections, une fiche de lecture et une ou plusieurs lignes de benchmark.

Le code sert plusieurs bases séparées : chaque base est un dossier avec son `base.json` (axes
du domaine), enregistrées dans un registre (`bin/pdb base list`) ; la base active est celle du répertoire courant, ou celle de `bin/pdb --base NOM` ([DATA_MODEL.md §11](DATA_MODEL.md#11-plusieurs-bases--registre-basejson-profilemd)).
La racine du dépôt ne contient que le code ; les bases vivent dans `bases/<nom>/`. La base de
référence est `bases/fpga/` (vision embarquée sur FPGA), la seconde `bases/drone/`.

---

## 2. Arborescence

```
PaperDatabase/
├── README.md               # présentation du projet
├── CLAUDE.md               # pour l'agent : dépôt du code, renvoi vers les bases
├── SETUP.md                # ce fichier
├── DATA_MODEL.md           # schémas et conventions
├── bases/                  # une base par dossier (détail plus bas)
│   ├── fpga/               # base de référence : vision embarquée sur FPGA
│   └── drone/              # vision embarquée sur drone
├── templates/              # CLAUDE.base.md et profile.md, copiés par pdb base new
├── requirements.txt
├── requirements-viz.txt    # optionnel : dépendances de la visualisation
├── requirements-embed.txt  # optionnel : embeddings (sentence-transformers) pour la visualisation
├── requirements-docling.txt # optionnel : Docling pour les tableaux sans corps
├── requirements-plot.txt   # optionnel : matplotlib pour bin/pdb plot
├── eval/                   # banc d'évaluation : thresholds.json (seuils par défaut)
├── benchmark/              # export versionné du banc synthétique (pdb synth)
├── .venv/                  # non versionné
├── .cache/bench/           # non versionné : répertoire de travail de pdb synth
├── docs/GUIDE.md           # guide d'utilisation (prise en main, extension du corpus)
├── docs/RAG.md             # requêtes sans LLM et recherche de passages
├── docs/EVAL.md            # banc d'évaluation du logiciel (pdb eval) et résultats
├── bin/                    # scripts du pipeline
│   ├── pdb, pdb.py         # point d'entrée unique (status, add, ingest, discover…)
│   ├── setup.sh
│   ├── grobid.sh
│   ├── add.py
│   ├── ingest.py
│   ├── reindex.py
│   ├── discover.py         # candidats à l'ajout via OpenAlex
│   ├── bases.py            # pdb base : list, new, register, use, info, check, scan, import
│   └── viz.py              # app Dash : graphe 3D, généalogie, onglet Bases
├── lib/                    # code partagé
│   ├── ids.py
│   ├── tei.py
│   ├── doc.py              # représentation commune GROBID / PyMuPDF
│   ├── pdftext.py          # extraction de repli PyMuPDF
│   ├── ligatures.py        # réparation des ligatures perdues (« classi cation »)
│   ├── tables.py           # tableaux réduits à leur légende : reconstruction PyMuPDF
│   ├── docling_tables.py   # optionnel : second repli Docling (OCR en option)
│   ├── citation.py         # exports .bib / .ris éditeur
│   ├── schema.py
│   ├── refs.py             # rapprochement des références, classement des externes, citations
│   ├── query.py            # requêtes N0 sans LLM (pdb bench, paper, cites)
│   ├── claims.py           # claims.jsonl : contrôle des excerpts (reindex, pdb claims)
│   ├── rag.py              # recherche de passages (pdb search, show, verify) ; moteur CPU
│   │                       # par défaut, moteur Qwen si la route GPU est active (§10)
│   ├── rag_models.py       # route GPU : modèles Qwen3 épinglés, détection CUDA, réglage pdb gpu
│   ├── rag_qwen.py         # route GPU : index de preuves SQLite de pdb rag
│   ├── rag_external.py     # route GPU : acquisition open access (pdb rag acquire / approve)
│   ├── evaluation.py       # banc d'évaluation (pdb eval)
│   ├── openalex.py         # client OpenAlex (DOI → arXiv, citations, recherche), cache
│   ├── status.py           # état de la base et prochaines actions (pdb status)
│   ├── graph.py            # nœuds, liens et positions du graphe 3D
│   ├── lineage.py          # généalogie : sous-graphe de citations sur une frise
│   ├── vizfig.py           # figures Plotly et panneau de détail de viz.py
│   ├── plotdata.py         # données des figures statiques (pdb plot), stdlib seulement
│   ├── plotfig.py          # figures matplotlib de pdb plot : benchmarks, éval, corpus
│   ├── embed.py            # optionnel : embeddings avec cache (.cache/)
│   ├── base.py             # base active, lecture de base.json, classement selon ses règles
│   ├── registry.py         # registre des bases (~/.config/pdb/bases.json)
│   ├── bases.py            # création, statistiques, profil, contrôle des règles
│   ├── xbase.py            # entre bases : scan des candidats, import par copie
│   └── vizbases.py         # onglet Bases de viz.py
├── tests/
│   ├── fixtures/sample.tei.xml
│   ├── fixtures/rag_eval*.jsonl  # questions d'évaluation : dev, holdout, FR, hors corpus
│   ├── test_tei.py
│   ├── test_schema.py
│   ├── test_ingest.py
│   ├── test_ligatures.py
│   ├── test_tables.py      # tableaux réduits à leur légende : PDF synthétique, rapprochement Docling
│   ├── test_evaluation.py  # métriques du banc sur de petits cas construits
│   ├── test_refs.py
│   ├── test_reindex.py     # notes benchmarks, mesures propres own-…
│   ├── test_claims.py      # claims.jsonl : excerpts, nombres, passage modifié, reindex
│   ├── test_query.py
│   ├── test_rag.py         # encodeur factice
│   ├── test_graph.py
│   ├── test_lineage.py
│   ├── test_viz.py
│   ├── test_plot.py        # familles, quantification, n/r, runs d'éval ; rendu des figures
│   ├── test_embed.py
│   ├── test_openalex.py    # OpenAlex simulé : découverte, ajout par DOI / liste
│   ├── test_citation.py    # exports .bib / .ris éditeur : lecture, appariement, priorité
│   ├── test_status.py
│   ├── test_base.py        # base active, base.json minimal, classement
│   ├── test_registry.py    # registre, ordre de résolution de la base active
│   └── test_xbase.py       # scan entre bases, import, création, onglet Bases
├── .claude/commands/       # /paper-add, /paper-fiche, /paper-extract, /paper-gaps, /paper-discover,
│                           # /paper-ask, /paper-research, /base-profile, /eval-answers
├── .claude/settings.json   # hook SubagentStop → bin/agent_log.py (journal des sous-agents)
└── tests/ …
```

Une base (`bases/fpga/`, `bases/drone/`, ou toute base créée par `pdb base new`) :

```
bases/<nom>/
├── CLAUDE.md               # mode d'emploi de la base pour l'agent
├── base.json               # axes, règles de classement (DATA_MODEL §11)
├── profile.md              # thème et périmètre, affinés par /base-profile
├── INDEX.md                # GÉNÉRÉ — table de tous les papiers
├── external_refs.csv       # GÉNÉRÉ — travaux hors base les plus cités par le corpus
├── candidates.csv          # GÉNÉRÉ par discover, non versionné — candidats OpenAlex
├── candidates_arxiv.txt    # GÉNÉRÉ par discover, non versionné — liste pour add --from
├── benchmarks.csv          # une ligne par configuration rapportée
├── gaps.md                 # carte des verrous et zones non couvertes
├── labs.md                 # laboratoires et équipes
├── figures/                # sortie de bin/pdb plot (PNG par défaut) et manifest.json
├── eval/                   # runs du banc (results/), et ses propres fixtures/, thresholds.json s'il y a lieu
├── docs/                   # documents propres à la base (fpga : experiences/, etat-de-l-art/)
├── .cache/                 # non versionné : index de passages, embeddings, réponses OpenAlex
├── bin, .venv, .claude/commands, .claude/settings.json   # liens vers le code (racine du dépôt)
├── inbox/                  # dépôt des PDF à ingérer
└── papers/
    └── <paper_id>/
        ├── paper.pdf       # PDF d'origine, conservé comme preuve
        ├── grobid.tei.xml  # sortie brute de GROBID, trace d'extraction
        ├── docling_tables.json # tableaux lus par Docling, s'il a été lancé (trace)
        ├── citation.bib    # export de citation éditeur (.bib ou .ris), s'il a été déposé
        ├── metadata.json   # titre, auteurs, année, venue, DOI, axes, statut
        ├── fulltext.md     # texte nettoyé, sections en ## / ###
        ├── sections.jsonl  # une ligne par section, avec page
        ├── refs.jsonl      # références citées
        ├── fiche.md        # fiche de lecture
        └── claims.jsonl    # preuves atomiques, s'il y a lieu (/paper-extract, DATA_MODEL §12)
```

Les commandes Claude Code (`/paper-add`, `/paper-fiche`, `/paper-gaps`, `/paper-discover`) vivent dans
`.claude/commands/` à la racine ; chaque base y accède par un lien, et une session Claude Code
ouverte dans `bases/<nom>/` lit le `CLAUDE.md` de la base (plus celui, générique, de la racine).

Tests : `.venv/bin/python -m unittest discover tests` — parsing TEI sur une sortie GROBID
réelle (`test_tei.py`), conformité DATA_MODEL (`test_schema.py`), conservation des axes et
tags à la ré-extraction (`test_ingest.py`), rapprochement des références et
`external_refs.csv` (`test_refs.py`), découverte OpenAlex, ajout par DOI et par liste
sur des réponses simulées (`test_openalex.py`), état et prochaines actions
(`test_status.py`), recherche de passages et `verify` (`test_rag.py`), tableaux et
rapprochement Docling sans Docling installé (`test_tables.py`), métriques du banc
(`test_evaluation.py`), et graphe sur un mini-corpus synthétique (`test_graph.py`, ignoré
si `requirements-viz.txt` n'est pas installé). La qualité sur le vrai corpus se mesure à
part : `bin/pdb eval` ([docs/EVAL.md](docs/EVAL.md)).

---

## 3. Prérequis

Vérifiés sur cette machine au 21/09/2026 :

| Outil | Version constatée | Rôle |
|---|---|---|
| Python | 3.12.4 (miniconda) | pipeline |
| Docker | 29.2.1, démon actif | héberge GROBID |
| jq | présent | inspection des JSON en ligne de commande |

Dépendances Python (`requirements.txt`) :

```
pymupdf          # extraction PDF de repli
lxml             # parsing du TEI GROBID
requests         # API arXiv + appels GROBID
python-slugify   # construction des identifiants
```

Un venv **local au dossier** (`PaperDatabase/.venv`) est préférable à la base conda : le
pipeline reste autonome et n'entre pas en conflit avec les environnements de tes autres
projets.

---

## 4. Installation (ou réinstallation) pas à pas

Tout est déjà en place sur cette machine. Cette section sert à reconstruire l'environnement
(nouvelle machine, venv supprimé) et à vérifier qu'il fonctionne.

### Étape 1 — environnement Python

```bash
cd ~/Documents/Perso/PaperDatabase
bash bin/setup.sh          # crée .venv s'il n'existe pas, installe requirements.txt
```

**Critère de réussite :** `.venv/bin/python -c "import pymupdf, lxml, requests; print('ok')"`
affiche `ok`.

Optionnel, pour la visualisation 3D (`bin/viz.py`) — dépendances séparées pour garder le
pipeline d'ingestion léger :

```bash
.venv/bin/pip install -r requirements-viz.txt   # dash, plotly, numpy, scikit-learn, networkx
.venv/bin/pip install -r requirements-embed.txt # encore plus optionnel : sentence-transformers (torch)
```

Optionnel, pour les figures statiques (`bin/pdb plot`) :

```bash
.venv/bin/pip install -r requirements-plot.txt  # matplotlib
```

### Étape 2 — GROBID

GROBID transforme un PDF scientifique en TEI XML structuré : titre, auteurs, année, DOI,
abstract, sections du corps, références. C'est ce qui évite de saisir les métadonnées à la
main et de se battre avec les PDF à deux colonnes.

```bash
bash bin/grobid.sh start   # = docker run --rm -d --name grobid -p 8070:8070 lfoppiano/grobid:0.8.1
```

L'image `lfoppiano/grobid` est la variante CRF seule (~400 Mo, CPU) : suffisante ici, et
bien plus légère que l'image complète avec modèles deep learning (plusieurs Go).

**Critère de réussite :**

```bash
curl -s localhost:8070/api/isalive    # -> true
```

Compte quelques dizaines de secondes au premier démarrage, le temps que le service charge
ses modèles.

### Étape 3 — contrôle sur un article

Le corpus contient déjà `papers/arxiv-2507.18174-.../`. Sur une installation neuve, un
`add.py` sur un id déjà ingéré est ignoré ; pour tester l'extraction de bout en bout,
réingérer sans toucher à la fiche :

```bash
.venv/bin/python bin/ingest.py --force papers/arxiv-2507.18174-*/paper.pdf
```

**Critère de réussite :** le dossier contient `metadata.json`, `fulltext.md`,
`sections.jsonl`, `refs.jsonl` et `fiche.md`, et `metadata.json` indique
`extraction.backend = "grobid"`. Voir §8 pour la relecture à faire.

### Étape 4 — versionnage

Le dossier est un dépôt git (remote : `https://github.com/lrivals/PaperDatabase.git`,
premier commit : mise en place du pipeline et amorçage arXiv). Le versionnage rend l'état de
l'art diffable : on voit la bibliographie se construire et les fiches évoluer.

`.gitignore` :

```
**/paper.pdf
**/grobid.tei.xml
inbox/*.pdf
inbox/*.meta.json
inbox/*.bib
inbox/*.ris
.venv/
__pycache__/
```

Les PDF et les TEI bruts sont régénérables ou re-téléchargeables ; tout le corpus textuel,
les fiches et le CSV sont versionnés.

---

## 5. Les scripts

Référence de ce que fait chaque script (tous implémentés). Chaque script a un rôle unique ;
en cas de modification, garder cette section à jour. Au quotidien, on passe par `bin/pdb`
(ci-dessous) ; le guide d'utilisation est [docs/GUIDE.md](docs/GUIDE.md).

### `bin/pdb <commande>`

Point d'entrée unique. Wrapper bash qui lance `bin/pdb.py` avec le Python de `.venv` (et
dit de lancer `setup.sh` s'il manque) ; utilisable via un lien symbolique dans le `PATH`.
Chaque sous-commande délègue aux scripts ci-dessous, sans logique propre :

| Commande | Délègue à | En plus |
|---|---|---|
| `status` | `lib/status.py` | état de l'environnement (venv, Docker, GROBID, dépendances optionnelles) et du corpus (papiers par axe, fiches à faire, extractions `ok: false`, benchmarks, gaps, `inbox/`, git), puis au plus 3 actions suggérées par ordre de priorité |
| `add …` | `add.run` | propose de démarrer GROBID s'il est arrêté (`--start-grobid` : sans question), puis `reindex.run` |
| `ingest [--force] [pdf…]` | `ingest.run` | idem |
| `ingest --reparse [--tables docling [--ocr]] [id…]` | `ingest.reparse` | ré-extraction depuis `grobid.tei.xml`, sans GROBID (Docling pour les tableaux sans corps si demandé), puis `reindex.run` |
| `reindex [--no-plot]` | `reindex.run`, `lib/plotrun.py` | régénère aussi les figures périmées (§ `bin/pdb plot`) ; `add` et `ingest` acceptent `--no-plot` |
| `discover …` | `discover.run` | |
| `grobid start\|stop\|status`, `viz`, `test` | `grobid.sh`, `viz.py`, `unittest` | |
| `search`, `show`, `verify` | `lib/rag.py` | recherche de passages (BM25 + embeddings bge-small, fusion RRF, `--rerank` en option ; Qwen3 sur GPU si la route GPU est active, `--gpu`/`--cpu` pour forcer), texte exact, contrôle de citation (statut `NOMBRES` si un nombre diffère) ; index dans `.cache/rag/`, reconstruit par `reindex` : [docs/RAG.md](docs/RAG.md) §4-5, §13 |
| `gpu [status\|on\|off\|download]` | `lib/rag_models.py` | route GPU optionnelle : état (torch, CUDA, modèles, vecteurs de la base), activation (réglage de la machine dans `~/.config/pdb/config.json`, ou `PDB_GPU=1`), téléchargement des modèles : §10, [docs/RAG.md](docs/RAG.md) §13 |
| `eval [--extract\|--rag\|--speed] [--gpu] [--papers FICHIER] [--answers DIR…] [--save] [--compare [JSON]]`, `eval --questions [JEU]`, `test --rag` | `lib/evaluation.py` | banc d'évaluation : extraction, recherche (jeux `tests/fixtures/rag_eval*.jsonl`), pertinence, `verify`, temps ; réponses finales enregistrées (`--answers`, jeux `answers*.jsonl`, `--questions` les liste sans les attentes : [docs/EVAL.md](docs/EVAL.md) §10) ; `--papers` rejoue la recherche sur un sous-corpus (liste de `paper_id` ou run enregistré, runs `-sub` : EVAL.md §9, lot K-0) ; runs dans `eval/results/` de la base, seuils dans `eval/thresholds.json` : [docs/EVAL.md](docs/EVAL.md) |
| `bench [filtres]`, `paper <requête>…` | `lib/query.py` | requêtes N0 sans LLM sur `benchmarks.csv` et `metadata.json`, bibliothèque standard seulement ; `bench --own` pour les mesures propres ; options et format de sortie : [docs/RAG.md](docs/RAG.md) §5.1 et §5.4 |
| `claims <id>`, `claims [<id>] --check` | `lib/claims.py` | preuves atomiques d'un papier ; `--check` : schéma et excerpts contrôlés par `rag.verify` contre leur passage, comme `reindex` ([DATA_MODEL.md](DATA_MODEL.md) §12) |
| `cites <id> [--external]`, `cited-by <id>` | `lib/refs.py`, `lib/query.py` | graphe de citations internes, références hors base avec leur nombre de citants : [docs/RAG.md](docs/RAG.md) §5.5 |
| `plot [bench\|eval\|corpus\|all] [--only a,b] [--out DIR] [--format png\|pdf\|svg] [--list] [--stale] [--check [--brief]]` | `lib/plotdata.py`, `lib/plotfig.py` | figures statiques, voir ci-dessous |
| `agents [--scan [--force]] [--report [--by task\|model\|base\|task-model] [--since D] [--worst N]] [--session ID] [--mark ID VERDICT]` | `lib/agentlog.py`, `lib/agentcost.py` | journal et coût des sous-agents Claude Code (`.cache/agents.jsonl` du dépôt), économie estimée de la délégation, calage sur le coût compté par Claude Code ; voir `bin/agent_log.py` ci-dessous |

### `bin/pdb plot`

Figures matplotlib, écrites dans `figures/` de la base active (PNG à 200 dpi par défaut ; `--format pdf` pour
une version vectorielle, pour LaTeX). Lecture seule sur la base. Trois groupes, `--list` pour les noms :

| Groupe | Source | Figures |
|---|---|---|
| `bench` | `benchmarks.csv` | débit vs puissance (détection / autres tâches, iso-FPS/W), GOPS/W par précision, LUT vs DSP par toolflow, précision vs débit et précision vs latence (un panneau par métrique), précision de calcul par famille |
| `eval` | `eval/results/*.json` (dernier run qui contient chaque volet) | recall@5/@10 et MRR par mode et jeu, verdicts de `verify`, couverture d'extraction et tableaux par papier, temps d'exécution, évolution entre runs |
| `corpus` | `metadata.json`, `benchmarks.csv`, `refs.jsonl`, `external_refs.csv` | papiers par année et type, par axe (fiches done/todo), part de n/r par colonne, papiers les plus cités (dans et hors base), carte famille × axe / tâche (cases à 0 = gaps candidats) |

Règles : une valeur `n/r` n'est jamais tracée ; chaque figure porte en pied sa source et le
nombre de lignes tracées sur le total ; les métriques de précision différentes ne partagent
jamais un axe ; puissance mesurée (puce, carte) en marqueur plein, estimée ou de portée non
dite en marqueur creux. `figures/manifest.json` garde, par figure, les sources, les
effectifs et le run d'évaluation utilisé. Les plateformes (texte libre) sont regroupées en
familles et les quantifications en classes de précision par des heuristiques
(`lib/plotdata.platform_family`, `quant_bucket`) ; une plateforme `n/r` forme sa propre famille
(« plateforme non rapportée », papiers algorithmiques), distincte de « autre » (nommée mais non
classée) ; `tests/test_plot.py` vérifie que chaque plateforme des bases livrées a une
famille et que la part de tâches « autre » reste sous le seuil de la base. Les axes sont ceux
de la base. Une figure sans données (aucune ligne chiffrée, aucun run d'évaluation) est
ignorée, avec sa raison, au lieu d'être tracée à vide. Palette : celle de `viz.py`.

**Personnalisation par base** : bloc `plot` de `base.json` (DATA_MODEL §11.2.1) — classes de
tâches (`tasks`), familles de plateformes propres à la base (`families`, essayées après celles
du code), tâche isolée dans `bench_fps_power` (`split_task`), figures écartées (`skip`, dites
« écartée par base.json »), seuils des panneaux de précision (`min_rows`), part « autre »
tolérée (`max_other`). Sans bloc, les réglages par défaut (ceux de la base fpga).

- `pdb plot --check` (sans matplotlib) : parts de lignes en « autre » (plateforme, tâche) et
  en `n/r`, libellés les plus fréquents restés non classés, figures qui seraient ignorées ou
  écartées, puis un bloc `plot` **proposé** (règles déduites des libellés « autre » :
  mot-clé dominant de chaque tâche, famille du code reconnue par un mot-clé de plateforme),
  à relire avant de le coller dans `.cache/base.proposed.json`. `--brief` : une ligne par
  alerte (pour `/paper-fiche`). Code de retour 1 seulement si `base.json` est invalide.
- `pdb base check [--config F]` montre la même mesure, avant → après, pour une proposition :
  `/base-profile` éprouve un bloc `plot` comme il éprouve des `axis_rules`.
- `pdb plot --stale` ne régénère que les figures périmées : source plus récente que la figure
  (`benchmarks.csv`, `base.json`, `eval/results/`, `papers/`) ou réglages changés
  (`config_hash` du manifest : empreinte du bloc `plot` et des axes).
- **Les figures suivent la base.** `reindex` — donc la fin de `pdb add`, `pdb ingest` et de
  `/paper-fiche` — régénère les figures `bench_*` et `corpus_*` périmées
  (`lib/plotrun.auto_refresh`) ; à la fin d'un banc, `pdb eval --save` (dont
  `--answers … --save`, `/eval-answers`) refait celles du groupe `eval`, et
  `pdb bench --add-columns` les `bench_*` / `corpus_*`. Une ligne
  `Figures : N régénérée(s) …` le dit ; une figure à jour n'est pas retracée (quelques
  secondes par figure). Conditions : la base a déjà un `figures/manifest.json` (premier tracé
  par `bin/pdb plot` : une base neuve ne trace rien d'elle-même), `plot.auto` n'est pas
  `false`, ni `--no-plot` (`reindex`, `add`, `ingest`) ni `PDB_NO_PLOT=1`, et matplotlib est
  installé. Sinon une `note` donne les figures périmées et `bin/pdb plot --stale`. Une
  figure en échec n'est qu'une `note` : la réindexation réussit quand même.

### `bin/setup.sh`

Crée le venv et installe `requirements.txt`. Idempotent : ne recrée pas un venv existant.

### `bin/grobid.sh {start|stop|status}`

- `start` : lance le conteneur s'il n'est pas déjà actif, puis boucle sur
  `/api/isalive` jusqu'à réponse `true` (timeout 120 s, message clair si dépassement).
- `stop` : arrête le conteneur.
- `status` : code de sortie 0 si GROBID répond, 1 sinon. Les autres scripts s'en servent
  pour décider du repli.

### `bin/add.py <arxiv-id|url|doi|chemin.pdf>… [--from liste.txt]`

Acquisition. Quatre formes d'entrée :

| Entrée | Comportement |
|---|---|
| `2507.18174` ou une URL `arxiv.org/abs/...` / `/pdf/...` | interroge l'API `export.arxiv.org/api/query` (titre, auteurs, date de v1, abstract, DOI si présent), télécharge le PDF dans `inbox/`, écrit un `<nom>.meta.json` compagnon |
| DOI (`10.…`, `doi:10.…`, `https://doi.org/10.…`) | résolu par OpenAlex (`lib/openalex.py`) : s'il a une version arXiv, traité comme un id arXiv, avec le DOI éditeur et la venue d'OpenAlex (`venue_openalex` dans le `.meta.json`, avertissement « type à préciser ») ; sinon refus avec le titre, l'éventuel lien open access légal et la procédure `inbox/`. Aucun téléchargement hors arXiv. DOI déjà présent dans un `metadata.json` : refusé |
| chemin vers un PDF local | copie dans `inbox/`, sans métadonnées compagnon |
| URL non-arXiv | refuse avec un message expliquant de télécharger le PDF à la main et de le déposer dans `inbox/` |

`--from liste.txt` lit un identifiant par ligne (texte après `#` ignoré) : c'est le format
de `candidates_arxiv.txt`. Enchaîne ensuite sur `ingest.py` pour les fichiers acquis.

Cas d'erreur à traiter explicitement : id arXiv inexistant, réseau indisponible, PDF déjà
présent dans `inbox/` ou déjà ingéré.

### `bin/ingest.py [--force] [chemin.pdf]` / `bin/ingest.py --reparse [paper_id…]`

Le cœur du pipeline. Sans argument, traite tous les PDF de `inbox/` non encore ingérés.

Pour chaque PDF :

1. **Extraction.** POST multipart vers `http://localhost:8070/api/processFulltextDocument`
   avec `consolidateHeader=0` (la consolidation interroge un service externe — on l'évite
   pour ne pas dépendre du réseau ni ralentir l'ingestion). La réponse TEI est écrite telle
   quelle dans `grobid.tei.xml`.
2. **Repli.** Si `grobid.sh status` échoue ou si GROBID renvoie une erreur, extraction via
   PyMuPDF : texte page par page, découpage en sections par heuristique sur les titres
   numérotés (`^\d+\.?\s+[A-Z]`). `extraction.backend` vaut alors `pymupdf` et
   `extraction.warnings` contient `"métadonnées à vérifier à la main"`.
3. **Fusion des métadonnées**, par ordre de confiance décroissant : export de citation
   éditeur (`.bib` / `.ris`) > `.meta.json` arXiv > `teiHeader` GROBID > vide. Les champs
   restés vides sont laissés à `null` — jamais devinés. L'export de citation
   (`lib/citation.py`, sans dépendance) est cherché à côté du PDF et dans `inbox/`, et
   apparié par DOI, sinon par titre (≥ 0,9) : son nom de fichier est libre. Il fixe titre,
   auteurs, année, venue, DOI et type, prime aussi sur un `metadata.json` existant lors
   d'un `--force`, puis est rangé dans `papers/<paper_id>/citation.bib|.ris` (copié et non
   déplacé s'il décrit plusieurs papiers).
4. **Nettoyage** du corps, dans cet ordre :
   - suppression des lignes identiques réapparaissant sur ≥ 3 pages (en-têtes/pieds de page) ;
   - suppression des numéros de page isolés et des mentions de copyright / DOI de bas de page ;
   - la bibliographie sort du corps et part dans `refs.jsonl` ;
   - les légendes de figures et de tableaux sont **conservées** (elles portent souvent les
     chiffres de performance), taguées `figure` / `table` dans `sections.jsonl` ;
   - les équations mal extraites sont conservées telles quelles, sans tentative de
     reconstruction ;
   - les ligatures perdues (« classi cation », « e cient », « the rst ») sont réparées
     par `lib/ligatures.py` : un mot n'est recollé que si le résultat est connu (présent
     dans ≥ 2 papiers du corpus ou dans une liste intégrée) et que le fragment ne l'est
     pas ; le nombre de réparations et les fragments restants vont dans
     `extraction.warnings` ;
   - un tableau dont GROBID n'a gardé que la légende (corps < 150 caractères) est cherché
     sur sa page par `page.find_tables()` de PyMuPDF (tableaux à filets seulement), collé à
     la légende et dans la même colonne (`lib/tables.py`) ; un tableau reconstruit porte la
     mention « [corps du tableau reconstruit par PyMuPDF : à vérifier] », et les tableaux
     reconstruits ou restés sans corps sont listés dans `extraction.warnings` puis par
     `pdb status` (« tableaux à vérifier ») ;
   - un paragraphe que GROBID a classé en figure sans légende est rendu au corps quand il
     ressemble à de la prose (`tei.looks_like_prose`) : il est réinséré après le paragraphe
     coupé en pleine phrase de la même page (ou du bas de la précédente), sinon après le
     dernier paragraphe de sa page.
5. **Écriture** de `fulltext.md`, `sections.jsonl`, `refs.jsonl`, `metadata.json`, et
   création de `fiche.md` depuis le template de [DATA_MODEL.md](DATA_MODEL.md) avec
   `status.fiche = "todo"`.
6. **Déplacement** du PDF vers `papers/<paper_id>/paper.pdf` (et non copie : `inbox/` doit
   se vider, c'est le signal qu'il ne reste rien à traiter).

Idempotent : un PDF dont le `paper_id` existe déjà est ignoré, sauf `--force` qui réécrit
tout sauf `fiche.md` (le travail de lecture ne doit jamais être écrasé par une
ré-extraction). Les métadonnées déjà présentes priment ; les axes et tags d'une fiche `done`
sont conservés tels quels, ceux d'une fiche `todo` sont l'union des anciens et des nouveaux
(`keep_classification`, testé par `test_ingest.py`) : une correction manuelle survit à la
ré-extraction. De même pour `extraction.warnings` : seuls les avertissements d'extraction
(sections, ligatures, corps court, repli) sont recalculés ; ceux sur les métadonnées,
ajoutés ou retirés à la main, sont conservés (`reextraction_warnings`).

`--reparse` ré-extrait les papiers déjà ingérés (tous, ou ceux dont le `paper_id` contient
un des motifs donnés) depuis leur `grobid.tei.xml`, sans appeler GROBID ; un papier sans TEI
est relu depuis `paper.pdf` par PyMuPDF. À lancer après une amélioration du parsing :
`bin/pdb ingest --reparse` réindexe ensuite. Les `chunk_id` des papiers modifiés peuvent
changer.

`--tables docling [--ocr]` (avec `--reparse`, dépendance optionnelle
`requirements-docling.txt`) : après le repli PyMuPDF, les tableaux restés sans corps sont
cherchés dans la sortie de Docling (`lib/docling_tables.py`). Le rapprochement se fait par
numéro de légende (Table 3 = TABLE III, à une page près), sinon par tableau sans légende
unique sur la page. La légende est marquée « reconstruit par Docling : à vérifier ». Docling
prend 25 à 100 s par papier sur CPU ; sa sortie est gardée dans
`papers/<id>/docling_tables.json`, et tout `--reparse` ultérieur la relit sans l'option.
`--ocr` relance Docling avec OCR (tableaux en image).

### `bin/reindex.py`

Relit tous les `papers/*/metadata.json` et régénère `INDEX.md` : un tableau par axe de
veille, trié par année décroissante, colonnes `id | titre | auteurs | année | venue | type |
fiche`. Ajoute en tête un compteur (`N papiers, M fiches à faire`).

Vérifie aussi la cohérence : tout `paper_id` apparaissant dans `benchmarks.csv` doit exister
dans `papers/` (sauf une mesure propre `own-…`, qui doit avoir son protocole dans
`docs/experiences/`, DATA_MODEL §1), et signale les fiches `done` qui n'ont aucune ligne de
benchmark (souvent le signe d'un oubli, sauf pour les surveys et les fiches marquées
`benchmarks: none`, DATA_MODEL §8).

Régénère aussi `external_refs.csv` ([DATA_MODEL.md](DATA_MODEL.md) §9) : les travaux absents
de la base cités par au moins deux papiers, du plus cité au moins cité. Les variantes d'une
même référence (ligature perdue, coquille, titre tronqué par GROBID) y sont fusionnées par
`lib/refs.py`.

Enfin, sur la base active (pas sur un corpus isolé), régénère les figures `pdb plot`
périmées par le changement, ou les signale (§ `bin/pdb plot`, « Les figures suivent la
base »).

Ne modifie jamais `benchmarks.csv` ni les fiches — il ne fait que lire et régénérer l'index.

### `bin/discover.py [--forward] [--backward] [--related] [--query "…"] [--axis A] [--since AAAA]`

Découverte de candidats via OpenAlex. Chaque papier du corpus est d'abord retrouvé dans
OpenAlex par son DOI éditeur **et** son DOI arXiv (`10.48550/arxiv.<id>`), car les deux
versions y sont souvent deux travaux distincts. Puis, selon les modes (défaut :
`--forward --backward`) :

- `--forward` : pour chaque version, les `--limit` (50) travaux citants les plus cités,
  depuis `--since` ;
- `--backward` : travaux référencés par au moins `--min-links` (2) papiers du corpus ;
- `--related` : `related_works` d'OpenAlex ;
- `--query` / `--axis` : recherche plein texte (`AXIS_QUERIES` de `ingest.py` pour un axe).

Les papiers déjà en base sont exclus (clés de `lib/refs.py`), les versions d'un même travail
fusionnées par titre normalisé. Chaque candidat reçoit ses axes probables
(`ingest.classify`), un drapeau `in_topic` (axe de `HARDWARE_AXES`, titre selon
`TITLE_TOPIC_RE`, ou au moins deux mentions de `TOPIC_RE`) et un score
(3 × liens de citation avec le corpus + liens « related » + 2 si trouvé par requête
+ 2 × axes + log10 des citations). Sorties : `candidates.csv` (DATA_MODEL §10) et
`candidates_arxiv.txt` (les `--top` premiers candidats dans le sujet disponibles sur arXiv,
pour `add --from`). Un mode en échec (HTTP 503 de la recherche anonyme, par exemple)
n'empêche pas les autres ; sans aucun candidat, les fichiers ne sont pas réécrits.

Réseau : `lib/openalex.py` met les réponses en cache dans `.cache/openalex/` et lit
`OPENALEX_API_KEY` et `OPENALEX_MAILTO` dans l'environnement (facultatifs).

### `bin/viz.py [--port 8050] [--debug]`

Application Dash locale (http://127.0.0.1:8050), deux onglets : **Graphe 3D** (un nuage où
chaque point est un papier de `papers/`) et **Généalogie** (frise des citations d'un papier
ou d'un sujet). Lecture seule : ne touche à aucun fichier de la base (seul le cache des
embeddings est écrit, dans `.cache/`, non versionné). Le calcul (`lib/graph.py`) est fait au
démarrage ; le bouton « Recharger le corpus » relit `papers/` après une ingestion sans
relancer l'app.

**Liens** (cochables, un trait coloré par type, épaisseur = poids relatif au lien le plus
fort du même type) :

| Type | Source | Poids |
|---|---|---|
| Citations | `refs.jsonl` rapproché des papiers du corpus (arXiv id → DOI → titre normalisé) | 1 |
| Références partagées | couplage bibliographique : références communes à deux papiers | cosinus de Salton \|A∩B\| / √(\|A\|·\|B\|) |
| Similarité textuelle | TF-IDF (ou embeddings, voir plus bas) sur le texte de `sections.jsonl` (abstract + sections) | cosinus, filtré par un seuil réglable |
| Thèmes communs | axes ∪ tags de `metadata.json` | Jaccard |

**Placement** : *force* (force-directed 3D sur les liens cochés : les papiers liés se
rapprochent, la vue change quand on coche/décoche) ou *sémantique* (PCA 3D de la similarité
textuelle, positions fixes : la proximité = vocabulaire ou sens commun).

**Couleur** : axe principal (premier axe de `metadata.json` ; l'infobulle liste tous les
axes), tag principal, année, type de publication ou statut de fiche. Palette à 8 couleurs
fixes doublées d'un symbole ; au-delà de 8 catégories, le reste est en gris. **Surligner**
un axe ou un tag estompe les autres papiers et les liens qui ne les touchent pas.

**Recherche** : liste déroulante filtrable (« auteur année — titre ») sur les papiers et,
si elles sont affichées, les références externes. Choisir un papier (ou cliquer un point)
le sélectionne : anneau sombre, voisins directs mis en avant, reste estompé. La sélection
survit au rechargement.

**Filtres** (graphe 3D) : plage d'années, statut de fiche, type de publication. Les papiers
filtrés sont retirés avant le placement ; un papier sans année n'est jamais exclu par le
filtre d'années. En placement sémantique, filtrer ne déplace pas les autres papiers.

**Références externes** (option) : travaux cités par ≥ 2 papiers du corpus mais absents de
la base, en petits points gris. Ce sont des candidats naturels à `/paper-add`.

**Panneau de détail** (clic ou recherche) : métadonnées, lien arXiv/DOI, fiche de lecture
rendue en Markdown (repliable), lignes de `benchmarks.csv` du papier (les lignes
`confidence: low` sont surlignées), liste des liens avec leur poids. Pour une référence
externe : liens arXiv/DOI (sinon recherche Google Scholar), commande `/paper-add` prête à
copier, rang dans `external_refs.csv`. Le bouton « Voir sa généalogie » ouvre l'onglet
Généalogie avec ce papier comme racine.

**Généalogie** (`lib/lineage.py`) : frise où x = année de parution (une colonne par année
présente, échelle **non proportionnelle** ; colonne « n/r » en premier pour les années
inconnues), flèches du travail cité vers le travail qui le cite. Deux points de départ :
- *papier* : ses ancêtres (ce qu'il cite, récursivement via les papiers du corpus) et ses
  descendants (ce qui le cite), profondeur 1 à 3. Toutes ses références directes sont
  montrées, même citées une seule fois ; plus loin, seules les externes co-citées ;
- *sujet* : mot-clé ou regex (insensible à la casse) sur les titres des papiers et des
  références externes et sur les axes/tags des papiers, ou `axis:x` / `tag:x`. Option
  « intermédiaires » : ajoute les papiers du corpus hors sujet situés sur une chaîne de
  citations entre deux nœuds du sujet. Exemple : `yolo|you only look once` (le titre de
  YOLOv1 ne contient pas « yolo »).

Option **suite probable** (seuil > 0) : arête en tirets entre deux papiers du corpus sans
citation entre eux, d'années croissantes, de similarité textuelle ≥ seuil (au plus une par
papier, vers le prédécesseur le plus proche). C'est une **inférence**, pas une donnée lue ;
la légende le dit.

**Similarité : TF-IDF ou embeddings.** Avec `requirements-embed.txt` installé
(sentence-transformers, modèle `all-MiniLM-L6-v2`), le bouton « embeddings » remplace le
TF-IDF pour les liens *similarité textuelle*, le placement sémantique et la suite probable.
Chaque papier = moyenne des embeddings de morceaux de ~200 mots ; cache
`.cache/embeddings/<modèle>.npz` indexé par id + sha1 du texte (un papier ré-extrait est
recalculé). Sans la dépendance, le bouton est grisé et tout reste au TF-IDF.

**Exporter** : télécharge la vue courante (3D ou généalogie) en HTML autonome (plotly.js
chargé depuis le CDN), dans le dossier de téléchargement du navigateur.

Limites à garder en tête avant d'interpréter la vue :
- la similarité TF-IDF est **lexicale**, pas sémantique : deux papiers qui disent la même
  chose avec un vocabulaire différent paraîtront éloignés (les embeddings atténuent ce
  défaut, sans le supprimer : `all-MiniLM-L6-v2` n'est pas entraîné sur des articles
  scientifiques) ;
- le couplage et les citations dépendent de la qualité d'extraction des références par
  GROBID : une référence mal parsée (titre tronqué, sans identifiant, année erronée) ne se
  rapproche de rien ou tombe dans la mauvaise colonne de la frise ;
- les titres de moins de 4 mots ne servent pas de clé de rapprochement (trop ambigus) ;
- **généalogie** : une référence externe n'a pas de bibliographie connue, donc aucune
  flèche n'en part vers une autre externe. L'histoire d'un modèle hors corpus (YOLOv1 →
  v3 → v5) n'est visible qu'à travers les papiers du corpus qui citent ces versions ;
- avec une dizaine de papiers, les positions sont surtout illustratives.

### `lib/graph.py`

Couche données de la visualisation, sans Dash : chargement du corpus, construction des
liens (rapprochement des références délégué à `lib/refs.py`), filtres (`filter_ids`,
paramètre `keep`), similarité TF-IDF ou embeddings (`set_similarity`), positions
sémantiques (PCA) et force-directed (`networkx.spring_layout`). Garde toutes les références
(`groups`, `citers`), y compris celles citées une seule fois, pour la généalogie. Testé par
`tests/test_graph.py`.

### `lib/lineage.py`, `lib/vizfig.py`, `lib/embed.py`

`lineage.py` : sous-graphe généalogique (papier racine ou sujet) et placement par couches
(Sugiyama simplifié, déterministe), sans Dash ; testé par `tests/test_lineage.py`.
`vizfig.py` : figures Plotly (3D, frise) et panneau de détail, appelables sans serveur ;
testé par `tests/test_viz.py`. `embed.py` : embeddings sentence-transformers avec cache,
optionnel ; testé par `tests/test_embed.py` (encodeur simulé, sans la dépendance). La
recherche de passages (`lib/rag.py`) a son propre index : [docs/RAG.md](docs/RAG.md).

### `lib/refs.py`

Rapprochement des références, sans dépendance de visualisation : clés exactes
(`ref_keys` : arXiv → DOI → titre normalisé), puis fusion des titres quasi identiques à un an
près (`same_title`), choix du titre d'affichage le moins abîmé (`best_title`) et classement
des travaux hors base (`external_ranking`), qui cite qui (`citations`, pour `pdb cites` /
`cited-by`). Utilisé par `lib/graph.py`, `reindex.py` et `bin/pdb.py`.
Testé par `tests/test_refs.py`.

### `lib/docling_tables.py`

Second repli pour les tableaux restés sans corps après `lib/tables.py`, optionnel
(`requirements-docling.txt`). `extract(pdf, ocr)` lance Docling (TableFormer ACCURATE) ;
`recover(blocks, found)` rapproche ses tableaux des blocs vides par numéro de légende (arabe
ou romain, à une page près), sinon par rang vertical parmi les tableaux sans légende de la
même page. Il n'accepte que des grilles ≥ 2 × 2 à moitié remplies (`usable`) et marque la
légende « reconstruit par Docling : à vérifier ». Sortie mise en cache dans
`papers/<id>/docling_tables.json`. Testé par `tests/test_tables.py`, sans Docling. Apport
mesuré : [docs/EVAL.md](docs/EVAL.md) §6.

### `bin/agent_log.py` et `lib/agentlog.py`

Journal des sous-agents ([docs/AMELIORATIONS.md, lot I](docs/AMELIORATIONS.md#lot-i--journal-et-coût-des-sous-agents)).
`agent_log.py` est le hook `SubagentStop` de `.claude/settings.json` (lié dans chaque base) :
il lit le JSON du hook sur stdin, relit le transcript du sous-agent
(`~/.claude/projects/<projet>/<session>/subagents/agent-<id>.jsonl` et son `.meta.json`) et
ajoute une ligne à `.cache/agents.jsonl` à la racine du dépôt (`$PDB_AGENTLOG_DIR` pour un
autre dossier). Python du système, bibliothèque standard seulement ; ne bloque jamais la
session (erreurs dans `.cache/agents.errors.log`, sortie 0 ; `PDB_AGENTLOG_RAW=1` garde
l'entrée brute). Le dernier tour de l'agent n'est souvent pas encore écrit quand le hook
passe : une ligne incomplète est réécrite par un processus détaché (`agent_log.py
--refresh`, attente `PDB_AGENTLOG_WAIT`, 60 s par défaut), et `pdb agents --scan` relit les
agents journalisés incomplets. `lib/agentlog.py` : parseur (tokens dédupliqués par `message.id`, premier
tour, outils, lectures intégrales de `fulltext.md`), rattrapage des sessions passées,
coût (tarifs dans `lib/agent_prices.json`) et rapport de `pdb agents`. `lib/agentcost.py` :
lecture du transcript principal (tours, appels `Agent`, retours, compactions, ligne
`cost-state`), calage de la sortie des sous-agents sur le cost-state (les transcripts la
sous-estiment), coût contrefactuel « fait en direct », vérification et lectures dupliquées,
étiquettes des cas défavorables, bilan d'une session (`--session`). Formules et hypothèses :
[AMELIORATIONS.md, I-3](docs/AMELIORATIONS.md#i-3-indicateurs). Testé par
`tests/test_agentlog.py` et `tests/test_agentcost.py`.

### `lib/evaluation.py`

Banc `bin/pdb eval` : métriques d'extraction (couverture du texte, tableaux, en-tête GROBID,
valeurs de `benchmarks.csv`), de recherche (recall, MRR, nDCG, jeux dev / holdout / FR),
de pertinence (seuil calibré puis validé), de `verify` (citations modifiées) et de temps ;
`flatten`, `compare`, `check_thresholds` pour `--compare`. Protocole : [docs/EVAL.md](docs/EVAL.md).

### `lib/ligatures.py`

Réparation des ligatures fi/ff/fl/ffi/ffl perdues à l'extraction, appelée par `ingest.py`
sur les blocs des deux backends. Jonction « e cient » → « efficient », début de mot
« the rst » → « the first » ; un mot n'est réparé que si le résultat est connu (mot présent
dans ≥ 2 papiers du corpus, ou liste intégrée `KNOWN`) et le fragment inconnu. Les URL ne
sont pas touchées. Testé par `tests/test_ligatures.py`.

### `lib/ids.py`

Construction du `paper_id` (voir [DATA_MODEL.md](DATA_MODEL.md)), slugification, détection
d'un identifiant arXiv dans une chaîne ou une URL.

### `lib/tei.py`

Parsing du TEI GROBID — la brique la plus délicate, testée par `tests/test_tei.py` sur un
TEI réel (arXiv 2507.18174, GROBID 0.8.1) :

- `teiHeader` → titre, auteurs (nom + prénom séparés), date de publication, DOI, venue,
  abstract ;
- `text/body` → `div[@type]` avec `head` puis `<p>` → sections et sous-sections ordonnées ;
- `text/back/div[@type="references"]/listBibl/biblStruct` → références.

### `lib/schema.py`

Définit le schéma de `metadata.json` et les colonnes de `benchmarks.csv`, avec une fonction
de validation appelée par `ingest.py` et `reindex.py`. Un seul endroit à modifier quand le
schéma bouge.

---

## 6. Flux de travail quotidien

Version pas à pas, avec la stratégie d'extension du corpus : [docs/GUIDE.md](docs/GUIDE.md).

```bash
bin/pdb status                          # où en est la base, quoi faire ensuite
bin/pdb add 2509.04153                  # arXiv ; aussi un DOI, un PDF local, --from liste.txt
cp ~/Téléchargements/article.pdf inbox/ && bin/pdb ingest   # article sous paywall
bin/pdb discover --forward --backward   # candidats → candidates.csv, candidates_arxiv.txt
bin/pdb viz                             # visualisation, http://127.0.0.1:8050
bin/pdb plot                            # figures statiques → figures/ (benchmarks, éval, corpus)
```

`add` et `ingest` réindexent d'eux-mêmes ; après une fiche remplie ou une ligne de benchmark
ajoutée à la main : `bin/pdb reindex`.

Dans Claude Code :

```
/paper-fiche arxiv-2507.18174-real-time-object-detection-classification
/paper-discover autoencoder-fpga        # propose des papiers, ajoute après accord
/paper-gaps                             # toutes les 3 à 5 fiches
```

`/paper-fiche` lit `fulltext.md`, remplit `fiche.md` et ajoute les lignes de
`benchmarks.csv`, avec la section source de chaque chiffre.

---

## 7. Amorçage depuis la bibliographie de départ

[basicStart.txt](bases/fpga/basicStart.txt) contient une vingtaine d'articles. Les neuf qui portent un
identifiant arXiv **sont ingérés** (tous par GROBID), avec cette boucle :

```bash
for id in 2509.04153 2507.18174 1806.01683 2512.01463 2103.05579 \
          2411.01431 2602.15751 2403.07851 2604.21280; do
  .venv/bin/python bin/add.py $id
done
```

Les autres — Kim & Kim 2025 (*Sensors*, DOI 10.3390/s25206359), l'accélérateur YOLO
end-to-end (*Neural Computing & Applications* 2023), YOLOv4-tiny de Valadanzoj et al., le
YOLOv3-Tiny sur Kria KV260 (IEEE), l'accélérateur YOLOv5 (ScienceDirect 2025), le YOLOv5 sur
ZCU102 (PMC11434529), le CAE sur PYNQ-Z2 (IEEE), le comparatif hls4ml/FINN (Springer),
Chameleon (TCAD 2024) et l'accélérateur SLDA (IEEE) — sont derrière des paywalls ou des
plateformes sans API : PDF à récupérer à la main, puis dépôt dans `inbox/`. **Pas encore
fait** — voir §9.

⚠️ `basicStart.txt` prévient que ces références ont été collectées à partir de résumés
seulement. **Chaque référence est à vérifier** (titre exact, auteurs, année, venue) au moment
de l'ingestion : GROBID lit le PDF réel, donc un écart entre le TEI et la note de départ est
le signal qu'une référence était approximative.

---

## 8. Vérification

À faire une fois, sérieusement, avant d'ingérer tout le corpus — une erreur d'extraction non
détectée se propage à toutes les fiches. Les points 1 à 5 concernent l'ingestion (déjà
utilisable) ; 6 et 7 supposent au moins une fiche remplie. L'avancement se coche au §9.

1. **Métadonnées.** Ouvre `papers/arxiv-2507.18174-*/metadata.json` : titre exact, liste
   d'auteurs complète et dans l'ordre, année cohérente avec l'identifiant arXiv.
2. **Texte.** Ouvre `fulltext.md` et contrôle : les sections apparaissent dans l'ordre du
   papier ; aucune phrase n'est coupée par un saut de colonne ; aucun en-tête ou numéro de
   page ne subsiste ; la bibliographie n'est plus dans le corps ; les légendes de figures
   sont présentes.
3. **Repli PyMuPDF.** `bash bin/grobid.sh stop`, puis ingère un quatrième papier :
   l'extraction doit réussir malgré tout, avec `extraction.backend = "pymupdf"` et un
   warning explicite dans `metadata.json`. Relance ensuite GROBID.
4. **PDF sans métadonnées.** Dépose dans `inbox/` un PDF récupéré chez un éditeur et lance
   `ingest.py` : GROBID doit retrouver seul titre, auteurs et année.
5. **Index.** `reindex.py` puis lecture d'`INDEX.md` : le compte de papiers et de fiches
   `todo` est juste, chaque papier est rangé sous le bon axe.
6. **Fiche.** Lance `/paper-fiche` sur un papier dont tu as lu le PDF, et recoupe : chaque
   chiffre de `benchmarks.csv` doit être exact et porter la bonne section source, et les
   valeurs absentes du papier doivent bien être `n/r`.
7. **Bout en bout.** Dans une session Claude Code neuve, pose une question du type
   *« quels papiers dépassent 25 FPS sous 5 W, et avec quel toolflow ? »*. La réponse doit
   se construire depuis `benchmarks.csv` et les fiches, sans qu'aucun PDF ne soit rouvert.

---

## 9. État actuel et tâches à faire

Point au 03/10/2026. À mettre à jour à chaque étape franchie (cocher, dater, déplacer dans
« En place »).

**Bilan du 03/10/2026 (figures par base).** Bloc `plot` de `base.json` (DATA_MODEL
§11.2.1 ; `plot_tasks` reste lu), `pdb plot --check` (diagnostic et proposition de règles),
`--stale`, `config_hash` dans le manifest, mesure « Figures » de `pdb base check`, avis de
régénération automatique des figures périmées par `reindex` et `pdb eval --save`
(`lib/plotrun.py`, `plot.auto`, `--no-plot` / `PDB_NO_PLOT`) ; branché dans `/base-profile`
et `/paper-fiche`. Base drone :
tâches et famille neuromorphique propres ; base stage : figures matérielles écartées.

**Bilan du 03/10/2026 (lot D, état de l'art fpga).**
- Lot D en place (D-5 : `pdb bench --comparable`) : colonnes optionnelles de `benchmarks.csv` (DATA_MODEL §7),
  `pdb bench --add-columns` et `--check`, mesure `in_cited_chunk`, `/paper-fiche`. Les trois
  bases réindexent sans changer leur CSV. 230 tests.
- `pdb eval --compare` (fpga) : recall@5 du holdout en hybride + rerank à 0,72, sous le
  plancher de 0,8 ; même valeur sur `main` sans le lot, donc baisse antérieure (EVAL.md §11).
- État de l'art LaTeX fpga : trois glossaires (plateformes, modèles, métriques et unités,
  `gloss-*.tex`), liés depuis le texte, compilés par `makeglossaries` dans le Makefile ;
  figures `pdb plot` régénérées sur les 299 lignes (nouvelle `bench_accuracy_latency`).

- [x] **Recherche : recall@5 du holdout fpga 0,80 → 0,72** entre le 28/09 et le 02/10
  (corpus 45 → 101 papiers, lot G) : cause isolée le 04/10/2026 (lot K-0, EVAL.md §9). Le
  code actuel sur les 45 papiers du 28/09 refait 0,80. La baisse vient du corpus. Quatre
  attentes ont été élargies après lecture des passages, et le holdout est revenu à 0,80 sur
  les 101 papiers. Option `pdb eval --papers` (sous-corpus) ; chaque run garde `corpus.papers`.

**Bilan du 02/10/2026 (fiabilité des réponses, route de recherche).**
- Feuille de route [docs/AMELIORATIONS.md](docs/AMELIORATIONS.md) : 8 lots (A à H) et 5
  skills, spécifiés.
- Lot A en place : `pdb eval --answers DIR…` / `--questions`, mode `--record` de
  `/paper-ask`, skill `/eval-answers`, jeux fpga 12 + 12 (EVAL.md §10). Premier run, en
  lexical seul (modèles non téléchargeables dans le conteneur) : verdict juste 0,83 (dev) et
  0,92 (holdout), hors corpus reconnu 6/6, citations acceptées 0,96 et 1,00. Faiblesses :
  questions de synthèse (3 verdicts sur 6 justes), sources attendues trop étroites,
  2409.07114 manqué deux fois.
- Lot G en grande partie fait : une route de recherche, CPU par défaut, Qwen en moteur
  optionnel de `pdb search` (`pdb gpu`, RAG.md §13).
- 218 tests.

**Bilan du 01/10/2026 (base fpga : profil, 8ᵉ passage des gaps, état de l'art).**
- Profil (`/base-profile`) : règle `safety-certification` élargie (EASA, assurance, ODD,
  TQL, moniteurs, conformal, incertitude) et `radiation` restreint aux effets radiatifs ;
  `person-detection` dans `hardware_axes` ; papiers hors sujet 13 → 4. 19 des 22 suggestions
  retenues, 1 écartée (élargir `yolo-fpga`), 2 reportées (ci-dessous).
- `gaps.md`, 8ᵉ passage (101 fiches, 299 lignes) : 36 gaps dont 29 étayés ; sections
  nouvelles « Sûreté, fiabilité et certification » (9) et « Détection de personnes en milieu
  industriel » (4) ; gap « AE complet sur petite FPGA » supprimé (contredit par 2407.17647 et
  2503.04832).
- État de l'art LaTeX (`bases/fpga/docs/etat-de-l-art/`) : section
  `sec-surete-certification.tex` (34 papiers cités), gaps et cadre de `fpga.tex` repris,
  `refs.bib` complété depuis les `metadata.json`.

- [ ] **Schéma : type « report »** pour les rapports d'autorité (EASA CoDANN 2020 / II,
  Concept Paper 2024 ont `type: null`) — suggestion de profil reportée le 01/10/2026.
- [ ] **Schéma : mesures sans plateforme embarquée** (Re-ID, détection de personnes sur GPU)
  dans `benchmarks.csv` ou à part — utiles comme référence pour le cas d'application ;
  suggestion reportée le 01/10/2026.
- [ ] Base fpga : `arxiv-2607.13106` annonce 29 lignes de benchmarks dans sa fiche, 23 dans
  `benchmarks.csv` (lignes IP DPU de la Table III manquantes), relevé au 8ᵉ passage.

**Bilan du 29/09/2026 (figures multi-bases).** `pdb plot` adapté aux bases sans mesures
matérielles (base stage : fps, gops, puissance, LUT/DSP presque tous n/r) : une figure sans
données est ignorée avec sa raison au lieu d'un PNG vide ; nouvelle figure
`bench_accuracy_latency` ; familles « SoC mobile » et « plateforme non rapportée » (séparée de
« autre ») ; classes de tâches par base (`plot_tasks` de `base.json`, DATA_MODEL §11.2) ; axes
et tâches lus dans le `Context` de la base tracée. Figures de stage dans `bases/stage/figures/`
(7 figures, bench et eval sans données ignorées). `tests/test_plot.py` : 15 tests, sur fpga et stage.

**Bilan du 29/09/2026 (base stage).** 3ᵉ base, `bases/stage/` : références du stage ISAE
(apprentissage continu embarqué sur MCU pour la maintenance prédictive ; dépôt
`cl-embedded`). `base.json` : 8 axes calqués sur les sections de la bibliographie
(`cl-methods`, `tinyml-odl`, `quantization`, `pdm-rul`, `anomaly-detection`,
`drift-detection`, `datasets`, `surveys`) ; `profile.md` (inclus / exclus). 50 articles :
- 33 par arXiv (`bin/pdb add --from`, identifiants vérifiés sur l'API arXiv) ;
- 16 PDF locaux (Zotero du stage, `Articles_ES_FS/`, `data/raw/`) ou en accès libre (JMLR
  pour Gretton 2012, PHM Society pour Lessmeier 2016), déposés dans `inbox/` avec un `.bib`
  fusionné des quatre bibliographies du stage (46 entrées) et deux exports Crossref ;
- 1 importé de `fpga` (Ravaglia 2021, `base import`).
Périmètre : 38 des 46 articles des `.bib` (48 références moins 2 sources web), 2 des 6
articles de `docs/context/` (Nagel, BinaryConnect), 10 articles lus mais non cités.
Exclus : sources web (CWRU Data Center, Blue Docker), jeux UCI, deux ebooks commerciaux.

Défaut constaté : `lib/citation.py` apparie par titre avec un seuil de 0,9, et
« Overcoming Catastrophic Forgetting in *Graph* Neural Networks » (2012.06002) a reçu l'entrée
de Kirkpatrick 2017. Corrigé à la main (article réajouté sans `.bib`) ; le seuil seul ne
suffit pas pour des titres qui ne diffèrent que d'un mot.

- [ ] **Base stage : 12 articles à déposer à la main** (sans PDF local ni version arXiv ; DOI
  vérifiés sur Crossref), PDF + export `.bib` dans `bases/stage/inbox/`, puis `bin/pdb ingest` :
  - Mahalanobis 1936, *On the Generalised Distance in Statistics* : original sans DOI, réimpression
    Sankhyā A 2019, doi:10.1007/s13171-019-00164-5
  - Page 1954, *Continuous Inspection Schemes*, Biometrika : doi:10.1093/biomet/41.1-2.100
  - Massey 1951, *The Kolmogorov-Smirnov Test for Goodness of Fit*, JASA : doi:10.1080/01621459.1951.10500769
  - Hinkley 1971, *Inference about the change-point from cumulative sum tests* : doi:10.1093/biomet/58.3.509
  - Gama et al. 2004, *Learning with Drift Detection* (DDM) : doi:10.1007/978-3-540-28645-5_29
  - Baena-García et al. 2006, *Early Drift Detection Method* : atelier IWKDDS (ECML PKDD 2006), sans DOI
  - Bifet & Gavaldà 2007, *ADWIN*, SIAM SDM : doi:10.1137/1.9781611972771.42
  - Liu et al. 2008, *Isolation Forest*, ICDM : doi:10.1109/ICDM.2008.17
  - Smith & Randall 2015, *Bearing Diagnostics Using the CWRU Data*, MSSP : doi:10.1016/j.ymssp.2015.04.021
  - Tiwari et al. 1994, *Power Analysis of Embedded Software*, IEEE TVLSI : doi:10.1109/92.335012
  - Vergara et al. 2012, *Chemical gas sensor drift compensation…* : doi:10.1016/j.snb.2012.01.074
  - Helwig et al. 2015, *Condition Monitoring of a Complex Hydraulic System*, I2MTC : doi:10.1109/I2MTC.2015.7151267
- [ ] Base stage : 50 fiches à rédiger (`/paper-fiche`), puis `/paper-gaps`.

**Bilan du 28/09/2026 (base fpga dans `bases/`).** La base `fpga` quitte la racine pour
`bases/fpga/` (papers/, benchmarks.csv, INDEX.md, gaps.md, labs.md, figures/, eval/results/,
docs/experiences/, .cache/, basicStart.txt, CLAUDE.md) ; la racine ne contient plus que le
code, avec un `CLAUDE.md` générique. `lib/base.REFERENCE` (= `bases/fpga`) remplace le dépôt
du code comme dernier recours de la base active et comme configuration des dossiers sans
`base.json`. Registre local à refaire dans un clone existant :
`bin/pdb base forget fpga && bin/pdb base register bases/fpga --name fpga && bin/pdb base use fpga`. Banc
relancé sur les deux bases (`pdb eval --save --compare`) : runs `2026-09-28T1039-76dc85e`
(fpga) et `2026-09-28T1043-76dc85e` (drone), 0 écart avec les précédents, tous seuils
atteints (docs/EVAL.md §9) ; figures `pdb plot all` régénérées pour les deux bases.

**Bilan du 28/09/2026 (base drone).** Base `drone` déplacée dans le dépôt (`bases/drone/`) ;
24 articles ajoutés ; 73 fiches sur 73 (230 lignes de benchmark ajoutées, 324 en tout) ;
profil précisé par `/base-profile` (règle sol → air / air → air, vol agile, « AAV ») ;
`gaps.md` 2ᵉ passe (19 gaps, dont 17 étayés) ; figures `pdb plot`. Captures de l'interface
dans `docs/images/`.

**Bilan du 28/09/2026 (plusieurs bases).** Registre des bases (`lib/registry.py`,
`~/.config/pdb/bases.json`), `bin/pdb --base NOM`, `bin/pdb base list|new|register|forget|use|
info|check|scan|import` (`bin/bases.py`, `lib/bases.py`, `lib/xbase.py`) ; `base.json` minimal
accepté (seuls `name` et `axes` requis) ; `profile.md` et skill `/base-profile` (le LLM propose,
l'utilisateur valide ; `/paper-fiche` ajoute des suggestions en attente) ; recherche
inter-bases (`cited_here`, `in_base`, `ref_elsewhere`) et import par copie ; `bin/pdb add`
signale un article présent dans une autre base ; onglet Bases dans `bin/viz.py`
(`lib/vizbases.py`). `lib/refs.py` : index des titres par longueur et préfixe (regroupement
identique, `reindex` bien plus rapide). DATA_MODEL §11, GUIDE §8.

**Bilan du 26/09/2026 (figures).** `bin/pdb plot` (`lib/plotdata.py`, `lib/plotfig.py`,
`requirements-plot.txt`) : 15 figures statiques en trois groupes (benchmarks, évaluation du
logiciel, statistiques du corpus), sources et effectifs dans `figures/manifest.json` ;
`tests/test_plot.py` (10 tests).

**Bilan du 24/09/2026.** Outillage : conservation des axes/tags à la ré-extraction,
`lib/refs.py` (rapprochement et fusion des variantes de références), `external_refs.csv`,
nettoyage des en-têtes GROBID (DOI gabarit, identifiant arXiv du tampon, auteurs
dédoublonnés) ; 42 tests. Corpus : ajout de FINN, FINN-R et fpgaConvNet (toolflow),
vérification §8.1-8.5, 9 fiches rédigées, 15 lignes de benchmark, venues et DOI vérifiés
(arXiv + Crossref).

**Bilan du 24/09/2026 (prise en main).** Point d'entrée unique `bin/pdb` (`status` avec
prochaines actions, `add`/`ingest` qui réindexent), ajout par DOI (résolu vers arXiv via
OpenAlex) et par lot (`--from`), découverte de candidats `bin/pdb discover` +
`/paper-discover`, guide d'utilisation [docs/GUIDE.md](docs/GUIDE.md) ; 77 tests.

**Bilan du 24/09/2026 (fiches et gaps).** Fiches FINN (8 lignes de benchmark) et FINN-R
(12 lignes) : 11 fiches `done` sur 12, 35 lignes. `gaps.md` réécrit par `/paper-gaps` :
14 gaps, dont 10 étayés. `/paper-discover autoencoder-fpga` : le gap autoencodeurs est
reformulé en « anomalie visuelle » (la compression d'image apprise sur FPGA existe) ; liste
courte en attente de validation (ci-dessous). `discover` : `in_topic` exige désormais un
contexte matériel (`HARDWARE_AXES`, `TOPIC_RE`).

**Bilan du 24/09/2026 (fpgaConvNet, puissance).** Ajout de arxiv-2108.03986 (autoencodeurs
sur FPGA au LHC, Nature Machine Intelligence 2022) ; fiche fpgaConvNet (aucune ligne de
benchmark : ratios seulement) ; colonne `power_scope` dans `benchmarks.csv` (`chip` |
`board` | `board-dynamic` | `estimated` | `unspecified`, validée par `lib/schema.py`) ;
`/paper-gaps` relancé : gaps « réseaux hors on-chip » et « puissance » réécrits ; 78 tests.

**Bilan du 24/09/2026 (vision embarquée hors FPGA).**
- Élargissement du corpus au-delà du FPGA : Jetson, VPU, Edge TPU, Hailo-8, MCU / TinyML.
  Passage de 13 à 28 papiers : 15 ajouts (8 par arXiv, 7 par dépôt manuel dans `inbox/`).
- 13 fiches rédigées : 24 `done` sur 28, dont Feng 2022, 2211.11647, Zhai 2023,
  El Zeinaty 2025, MCUNetV2, TinyissimoYOLO, 2108.03986 (LHC), Shuvo 2023, Mittal 2024,
  Hozhabr 2025, Rey 2025 (Orin, TensorRT INT8) et Alqahtani (mAP COCO sur Orin et Hailo).
- `benchmarks.csv` passe de 35 à 109 lignes. Premières lignes `chip` (14) et premières mAP
  COCO (15, sur Jetson et Hailo, aucune sur FPGA).
- `gaps.md`, 5e passage : 16 gaps, dont 12 étayés. Nouveaux :
  - « précision non vérifiée sur la cible après compilation » ;
  - « passerelle MCU ↔ FPGA ».
  Reformulé : « surveys *embarqué* sans FPGA, ou *FPGA* sans comparaison chiffrée ». Le
  gap « baseline Jetson » est partiellement comblé.
- Outillage : `lib/citation.py`. Un export `.bib` ou `.ris` déposé dans `inbox/` est
  apparié au PDF par DOI, sinon par titre ; ses champs priment sur l'en-tête GROBID, puis
  il est rangé dans `papers/<id>/citation.*`.
- Nouveaux fichiers : [labs.md](bases/fpga/labs.md) (labos et encadrants, INSA Rennes / IETR à
  vérifier) et le protocole [docs/experiences/kv260-map-sur-cible.md](bases/fpga/docs/experiences/kv260-map-sur-cible.md).
- Clé `OPENALEX_API_KEY` configurée dans `~/.bashrc`.
- 89 tests.

**Bilan du 25/09/2026 (requêtes et recherche de passages).** Spécification et détail :
[docs/RAG.md](docs/RAG.md).
- Requêtes N0 sans LLM : `pdb bench` (filtres, tri, `--count`, colonnes de source toujours
  affichées) et `pdb paper` (fiche d'identité, id court), `lib/query.py`.
- Recherche de passages `lib/rag.py` : découpage de `sections.jsonl`, BM25 + embeddings
  bge-small, fusion RRF, index incrémental dans `.cache/rag/` reconstruit par `reindex`.
  Commandes `pdb search` (option `--rerank`, cross-encoder), `pdb show`, `pdb verify`,
  `pdb test --rag`.
- Skill `/paper-ask`, essayée en réel sur la mesure de puissance (RAG.md §12) : ~2 500 tokens
  lus, 7 citations vérifiées `OK`.
- Évaluation : recall@5 0,90 en anglais (1,00 avec `--rerank`), 0,50 en français.
- 113 tests.

**Bilan du 25/09/2026 (outillage restant).**
- `pdb cites` / `cited-by` (`--external`), `pdb paper` sur plusieurs ids.
- Réparation des ligatures perdues (`lib/ligatures.py`) et des paragraphes que GROBID
  classait en figure (`tei.looks_like_prose`). Corpus ré-extrait par le nouveau
  `ingest --reparse`, sans GROBID ; les avertissements manuels sont désormais conservés.
- `benchmarks: none` pour une fiche sans ligne justifiée ; mesures propres `own-…`
  (DATA_MODEL §1, `bench --own`).
- `discover` : `in_topic` plus strict (titre, axe matériel, ou deux mentions).
- 133 tests.

**Bilan du 26/09/2026 (tableaux perdus).**
- Constat : 52 tableaux sur 148 n'ont que leur légende dans le TEI. GROBID localise la
  légende (6 à 9 pt de haut) sans le corps : découper la page aux coordonnées TEI ne suffit
  donc pas.
- `lib/tables.py` : repli `find_tables()` de PyMuPDF sur la page entière, tableau à filets
  collé à la légende. La stratégie « text » est écartée : elle découpait la prose en
  colonnes, 0 tableau exploitable sur 44. Résultat : 3 tableaux reconstruits (2108.03986
  Tables I et IV, 2411.01431 Table 2), 49 signalés « sans corps » dans `pdb status`.
- Recherche de passages inchangée après `ingest --reparse` : recall@5 EN 0,90, 1,00 avec
  rerank. 143 tests.
- **Essai de Docling** (2.130, installé dans `.venv`, pas encore dans les requirements),
  sur 6 papiers, entre 25 et 100 s par papier sur CPU :
  - sans OCR, bons tableaux pour zhai (9), 2512.01463 (10, dont les Tables 3 à 9 absentes
    du TEI) et FINN (4). Erreurs restantes : décalage de colonnes de FINN Table 3 (BRAM
    SFC-max 4.5, non corrigé) ; DSP et LUT apparemment inversés sur 2 lignes de
    2512.01463 Table 3 ; cellules manquantes dans zhai Table 9 ;
  - shuvo, cui et hozhabr (IEEE Access) : tableaux en image ou en tracés vectoriels, sans
    texte extractible (grilles 0×0 sans OCR) ;
  - avec OCR (RapidOCR, pleine page) : tableaux propres pour shuvo Table 8 et cui
    Tables 5 à 9 ; échec sur hozhabr Tables 9-10 (paysage pivoté : transposé et illisible).
  - Conclusion : utile en second backend pour les tableaux seulement, jamais sans la
    mention « à vérifier ». À brancher si l'on accepte la dépendance (voir tâches).

**Bilan du 26/09/2026 (banc d'évaluation).** `bin/pdb eval` ([docs/EVAL.md](docs/EVAL.md),
`lib/evaluation.py`, `tests/test_evaluation.py`) : extraction (couverture du texte 0,91,
tableaux avec corps 0,66, en-tête GROBID, valeurs de `benchmarks.csv` retrouvées dans le
tableau cité 0,74 contre 0,86 dans le texte), recherche (nouveau jeu holdout de 25 questions :
recall@5 hybride 0,84, contre 0,90 sur le jeu dev), questions hors corpus, `verify`, temps.
Rapport de référence dans `bases/fpga/eval/results/`, seuils dans `eval/thresholds.json`. 153 tests.
Défauts mis au jour, à corriger (tâche 12) :
- l'alerte « pertinence faible » ne se déclenche sur aucune des 10 questions hors corpus ;
- `verify` accepte (APPROX) une citation avec un chiffre ou un mot modifié ;
- `tei.clean_doi` laisse passer le DOI gabarit MDPI `10.3390/electronics1010000`.

**Bilan du 26/09/2026 (corrections mesurées par le banc).** Détail : [docs/EVAL.md](docs/EVAL.md) §6.
- `verify` refuse (`NOMBRES`, code 1) une citation dont les nombres diffèrent du passage :
  0/38 chiffres modifiés acceptés, contre 38/38 avant ; 40/40 citations exactes restent
  `OK`. `/paper-ask` mis à jour.
- Pertinence faible : ni le cosinus ni le cross-encoder ne remplissent la règle fixée
  d'avance (validation : cross-encoder 90 % hors corpus signalés, mais 40 % du corpus à
  tort). L'alerte `# pertinence faible` est retirée de `pdb search`.
- Docling branché (`ingest --reparse --tables docling [--ocr]`, `lib/docling_tables.py`,
  cache `docling_tables.json`) : tableaux avec corps 0,66 → 0,90 (41 reconstruits, OCR sur
  shuvo, cui, hozhabr), à vérifier. Sans effet sur les valeurs de `benchmarks.csv` ni sur la
  recherche.
- 162 tests.

### Prochaines étapes prioritaires

1. [ ] **Liste courte autoencodeurs** : 2108.03986 ajouté (fiche à faire :
   `/paper-fiche arxiv-2108.03986-autoencoders-fpgas-real-time-unsupervised`). Reste (`/paper-discover autoencoder-fpga`,
   24/09/2026, métadonnées OpenAlex à vérifier) :
   à déposer dans `inbox/` (aucun n'a de version arXiv) :
   - **prioritaire**, sous paywall IEEE (accès université) : F-LIC (A-SSCC 2022, DOI
     10.1109/a-sscc56115.2022.9980666) ; FPGA Codec System of Learned Image Compression
     (JETCAS 2024, DOI 10.1109/jetcas.2024.3386328) ; Low Latency Variational Autoencoder
     on FPGAs (JETCAS 2024, DOI 10.1109/jetcas.2024.3389660) ; Edge-Compatible CAE on FPGA
     (IEEE Sensors Letters 2022, DOI 10.1109/lsens.2022.3159972) ; An Efficient
     FPGA-based Architecture for Contractive Autoencoders (FCCM 2020, DOI
     10.1109/fccm48280.2020.00062, entraînement en ligne sur Zynq : lien avec l'axe CL) ;
   - en open access (OJCAS) : An Energy Efficient EdgeAI Autoencoder Accelerator for
     Reinforcement Learning (DOI 10.1109/ojcas.2020.3043737) — FPGA ou ASIC : à vérifier.
2. [x] **Ficher fpgaConvNet** et relancer `/paper-gaps` (24/09/2026). Suite logique :
   ajouter l'article FCCM 2016 (DOI 10.1109/FCCM.2016.22, paywall, 6 citants) pour les
   chiffres absolus absents du papier de workshop.
3. [ ] **Expérience à reproduire** : YOLOv5 INT8 via Vitis AI sur Kria KV260, avec mAP sur
   le split officiel (COCO val), résolution et variante déclarées, puissance mesurée au
   wattmètre (carte) et via la télémétrie de la puce (modèle : P_chip / P_wall de FINN,
   arxiv-1612.07119 §5.1), latence et FPS à batch 1 — pour combler le gap « protocole de
   mesure YOLO » de `gaps.md`, et servir de baseline aux travaux de thèse. Ajouter une
   comparaison Jetson (Orin Nano) dans les mêmes conditions. Protocole détaillé (24/09/2026,
   non exécuté) : [docs/experiences/kv260-map-sur-cible.md](bases/fpga/docs/experiences/kv260-map-sur-cible.md).
   Il mesure la mAP COCO val sur la carte, NMS compris, et la compare au modèle flottant et
   au modèle quantifié simulé (gap « précision non vérifiée sur la cible »).
4. [x] **Convention puissance** (24/09/2026) : colonne `power_scope`, DATA_MODEL §7,
   `/paper-fiche` ; 35 lignes renseignées (16 `board`, 4 `unspecified`, 3 `estimated`,
   0 `chip`).
5. [ ] **Fiches restantes (4)** : `2023-cui-…` (survey d'anomalie visuelle industrielle,
   prioritaire pour l'axe `autoencoder-fpga`), arxiv-2010.15277, arxiv-2206.15472,
   arxiv-2409.07114 (apprentissage continu et entraînement sur MCU).
6. [ ] **Baseline Jetson complète** : aucune source ne réunit Orin + TensorRT INT8
   déclaré + mAP COCO + puissance de carte en W.
   - Rey et al. (arxiv-2502.15737) donnent INT8 et une puissance par télémétrie, sur un
     jeu privé.
   - Alqahtani et al. (arxiv-2409.16808) donnent la mAP COCO et une énergie hors repos,
     précision non déclarée.
   Il faut soit la mesurer (volet Orin du protocole KV260), soit déposer dans `inbox/`
   *Benchmarking YOLOv8 Variants… on Jetson Orin NX* (Computers 2026, DOI
   10.3390/computers15020074) avec son `.bib`.
7. [ ] **PDF à récupérer à la main (accès université, avec export `.bib`)** :
   - *Embedded AI performances of Nvidia's Jetson Orin SoC series* (HAL 2023) ;
   - *Review of large YOLOv8 and RT-DETR energy efficiency on edge devices* (Sci. Rep.
     2026, DOI 10.1038/s41598-026-46453-6) ;
   - *Accelerating Deep Learning Inference: A Comparative Analysis…* (Electronics 2025,
     DOI 10.3390/electronics14152977) ;
   - Anupreetham et al. [67] (NMS pipeliné sur FPGA) et D. Zhang et al. [86] (détecteur
     entièrement sur FPGA), cités par 2025-hozhabr : références dans son `refs.jsonl`.
8. [ ] **Tableaux** (liste dans `bin/pdb status`, « tableaux à vérifier ») : Docling branché le
   26/09/2026, puis passé (avec OCR) sur les deux bases le 29/09/2026 (EVAL.md §9). Restent
   sans corps 31 tableaux dans fpga et 24 dans drone, dont de faux tableaux (prose,
   algorithme ou note classés en tableau par GROBID). Restent notamment les 14 tableaux de
   2026-fata, 2409.07114 Tables II et IV, et 2211.11647. Les tableaux reconstruits (fpga 118,
   drone 106) sont à relire avant tout usage chiffré. Défauts déjà repérés : cui Table 9
   (colonnes perdues), hozhabr Table 5 (fragments OCR), Tables 9-10 (paysage pivoté), FINN
   Table 3 (colonnes décalées, BRAM SFC-max), 2512.01463 Table 3 (DSP/LUT inversés ?).
9. [ ] **Vérifications contre le PDF** des chiffres lus en figures seulement : 2211.11647
   (Fig. 6, 7 et 12) ; tableaux perdus à l'extraction dans 2025-hozhabr (Tables 9-10) et
   2023-shuvo (Tables 6-10).
10. [ ] **labs.md** : vérifier le rattachement IETR de l'équipe INSA Rennes (Menard, Herrou)
   et récupérer le dépôt public annoncé par 2025-el-zeinaty.
11. [ ] **Recherche de passages et requêtes sans génération** (spécification du 25/09/2026 :
    [docs/RAG.md](docs/RAG.md)). Ordre proposé :
    - [x] `pdb bench` et `pdb paper` (N0, indépendants de l'index), `lib/query.py`,
      `tests/test_query.py` (25/09/2026, 101 tests) ;
    - [x] `lib/rag.py` (passages, BM25 + embeddings bge-small, fusion RRF, cache
      `.cache/rag/`), `tests/test_rag.py` ; `pdb search`, `show`, `verify`, `test --rag` ;
      branchement dans `reindex.py` ; skill `/paper-ask` ; jeux d'évaluation
      `tests/fixtures/rag_eval.jsonl` (20 q.) et `rag_eval_fr.jsonl` (8 q.) (25/09/2026,
      110 tests). Évaluation : recall@5 0,90 en anglais, 0,50 en français (RAG.md §10) ;
    - [x] `pdb cites` / `cited-by`, `--external` (RAG.md §5.5), et `pdb paper` sur
      plusieurs ids (25/09/2026) ;
    - [x] essai réel de `/paper-ask` sur la mesure de puissance (RAG.md §12) ; corrigés
      ensuite : id court des noms composés, `bench --count` (112 tests) ;
    - [x] reranking par cross-encoder, option `search --rerank` : recall@5 0,90 → 1,00 en
      anglais (question NMS récupérée), MRR 0,33 → 0,26 en français. Option non activée par
      défaut, utilisée par `/paper-ask` (RAG.md §10, 113 tests) ;
    - [ ] relever les puissances de 2211.11647 dans ses figures (portée `board`), et
      vérifier la portée de tegrastats pour les 14 lignes `chip` de 2502.15737 (constats
      de l'essai de `/paper-ask`).
12. [ ] **Défauts révélés par `bin/pdb eval`** ([docs/EVAL.md](docs/EVAL.md) §5-6) :
    - [x] `verify` refuse une citation aux nombres différents (26/09/2026, 0/38 acceptées) ;
    - [x] « pertinence faible » : aucun signal fiable (cosinus, cross-encoder), alerte retirée
      (26/09/2026) ; piste restante : combiner les deux signaux, à valider sur un nouveau
      jeu hors corpus ;
    - [ ] `tei.clean_doi` : rejeter les DOI gabarits MDPI (`…1010000`) ;
    - [ ] recherche sur tableaux : 2 questions holdout sur 2 manquées, même après Docling ;
    - [ ] `verify` : un mot remplacé loin d'un nombre donne toujours `APPROX` (38/40).

### En place

| Brique | État |
|---|---|
| Pipeline d'ingestion (`add.py`, `ingest.py`, `grobid.sh`, repli PyMuPDF) | fonctionnel, testé (`test_tei.py`, `test_ingest.py`) ; repli PyMuPDF et PDF sans métadonnées vérifiés en réel (§8.3-8.4) le 24/09/2026 |
| Nettoyage de l'en-tête GROBID (`lib/tei.py`) | depuis le 24/09/2026 : DOI gabarit rejeté (`10.1145/nnnnnnn.nnnnnnn`), identifiant arXiv lu dans le tampon du PDF (`arXiv:1809.04570v1[cs.AR]`), auteurs dédoublonnés (Preusser = Preußer), césures réparées (« Gam- Bardella »), affiliations prises pour des auteurs retirées |
| Axes et tags à la ré-extraction | conservés depuis le 24/09/2026 : fiche `done` → inchangés ; fiche `todo` → union anciens + nouveaux (`keep_classification`) |
| Index et contrôle de cohérence (`reindex.py`) | fonctionnel, 0 erreur ; contrôle de conformité DATA_MODEL complet (`test_schema.py`) ; génère aussi `external_refs.csv` |
| Références (`lib/refs.py`) | rapprochement par clés exactes + fusion des titres quasi identiques (ligatures perdues, coquilles, titres tronqués ; ±1 an), titre d'affichage le moins abîmé ; testé (`test_refs.py`) ; utilisé par la vue 3D et `reindex.py` |
| Classement des références externes | `external_refs.csv` : travaux hors base cités par ≥ 2 papiers (DATA_MODEL §9) ; 576 pour fpga, 466 pour drone au 29/09/2026 |
| Tableaux réduits à leur légende (`lib/tables.py`, `lib/docling_tables.py`) | depuis le 26/09/2026 : repli `find_tables()` PyMuPDF (tableaux à filets), puis Docling, avec OCR pour les tableaux en image ; passé sur les deux bases le 29/09/2026 : tableaux avec corps 0,87 (fpga, 401 tableaux, 110 Docling) et 0,71 → 0,90 (drone, 96 Docling) (EVAL.md §6 et §9) ; testé (`test_tables.py`) ; restent sans corps 31 (fpga) et 24 (drone), dont de faux tableaux. **Manque** : relecture des tableaux reconstruits (erreurs de colonnes, fragments d'OCR) |
| Hiérarchie des titres de `fulltext.md` | titres parasites filtrés, niveau 3 géré, sections non détectées par GROBID signalées dans `extraction.warnings` |
| Commandes Claude Code `/paper-add`, `/paper-fiche`, `/paper-gaps`, `/paper-discover` | écrites (`.claude/commands/`) ; `/paper-fiche` rodé sur 24 papiers (surveys, benchmarks multi-plateformes, MCU) ; `/paper-discover` rodée le 24/09/2026 (vision embarquée, baseline Orin), avec la clé OpenAlex |
| Fichiers de citation éditeur (`lib/citation.py`) | depuis le 24/09/2026 : lecture `.bib` / `.ris` sans dépendance, appariement au PDF par DOI puis par titre, priorité sur l'en-tête GROBID, conservation dans `papers/<id>/citation.*` ; testé (`test_citation.py`) et vérifié en réel sur 6 exports (IEEE, ACM, MDPI, Springer) |
| Point d'entrée `bin/pdb` et `status` (`lib/status.py`) | depuis le 24/09/2026 ; testé (`test_status.py`) ; vérifié sur le vrai corpus (12 papiers, 3 fiches à faire, axe `autoencoder-fpga` signalé) |
| Découverte (`bin/discover.py`, `lib/openalex.py`) et ajout par DOI / `--from` | depuis le 24/09/2026 ; testé sur réponses simulées (`test_openalex.py`) ; vérifié en réel : 12/12 papiers retrouvés dans OpenAlex, ~290 candidats (`--forward --backward`), DOI 10.1088/1748-0221/13/07/P07027 → arXiv 1804.06913. La recherche plein texte anonyme (`--query`, `--axis`) était suspendue par OpenAlex (HTTP 503) le jour du test |
| Corpus | 28 papiers (le 24/09/2026) : 21 par arXiv, 7 déposés à la main avec leur export de citation (Feng 2022, Zhai 2023, El Zeinaty 2025, Shuvo 2023, Mittal 2024, Hozhabr 2025, Cui 2023) ; tous extraits par GROBID ; périmètre élargi à Jetson, VPU, Edge TPU, Hailo et MCU |
| Fiches de lecture | 24 / 28 `done` (le 24/09/2026) ; restent 2023-cui, arxiv-2010.15277, arxiv-2206.15472 et arxiv-2409.07114 |
| `benchmarks.csv` | 109 lignes (le 24/09/2026) : 16 `board`, 14 `chip` (Rey et al., Jetson et RPi), 24 `unspecified`, 3 `estimated`, 52 sans puissance ; 71 lignes de détection, dont 15 avec mAP COCO (Alqahtani et al., Jetson et Hailo), aucune ligne FPGA avec mAP COCO ; aucune ligne pour les surveys, hls4ml 2021 ni fpgaConvNet (justifié dans les fiches) |
| `gaps.md` | 16 gaps, dont 12 étayés (5e passage, le 24/09/2026, 24 fiches `done`) |
| Visualisation (`viz.py`, `lib/graph.py`, `lib/lineage.py`, `lib/vizfig.py`, `lib/embed.py`) | terminée le 24/09/2026 : graphe 3D (recherche, filtres, surlignage des liens, détail avec fiche et benchmarks, export HTML) et onglet Généalogie (papier ou sujet, suite probable déduite) ; embeddings optionnels ; testée (`test_graph.py`, `test_lineage.py`, `test_viz.py`, `test_embed.py` ; 77 tests au total avec ceux du 24/09/2026) ; 10 citations internes, 89 références externes co-citées |
| Requêtes et recherche de passages (`lib/query.py`, `lib/rag.py`, `pdb bench`/`paper`/`search`/`show`/`verify`) | depuis le 25/09/2026 : BM25 + embeddings bge-small, fusion RRF, reranking optionnel, index incrémental ; `verify` contrôle les nombres et l'alerte « pertinence faible » est retirée (26/09/2026) ; testé (`test_query.py`, `test_rag.py`) et évalué (RAG.md §10, EVAL.md) ; skill `/paper-ask` essayée en réel (RAG.md §12) |
| Banc d'évaluation (`bin/pdb eval`, `lib/evaluation.py`) | depuis le 26/09/2026 : extraction, recherche (dev, holdout, FR, hors corpus), `verify`, temps ; réponses finales (`--answers`, 02/10/2026, EVAL.md §10) ; `--save` / `--compare` et seuils ; testé (`test_evaluation.py`) ; rapport de référence dans [docs/EVAL.md](docs/EVAL.md) §5, corrections mesurées (§6) |
| Versionnage | dépôt git + remote GitHub ; travaux du 24/09/2026 commités et poussés |

### Tâches — corpus

- [x] **Ficher les 9 papiers initiaux** (`/paper-fiche`). Fait le 24/09/2026, en commençant
  par 2507.18174 (test de bout en bout). Axes confirmés, warnings retirés.
- [x] Ficher FINN et FINN-R (24/09/2026). Reste fpgaConvNet : « Prochaines étapes » (2).
- [x] `/paper-gaps` (24/09/2026) : 14 gaps. À relancer après fpgaConvNet.
- [ ] FINN, Table 3 : colonne BRAM mal extraite (SFC-max 4,5 contre 130,5 en §5.2.3) ; FINN-R :
  Table 4 (précision des réseaux) absente — vérifier sur le PDF.
- [ ] **Vérifications contre le PDF, à faire à la main** (le PDF est exclu du travail de
  l'agent par CLAUDE.md) :
  - 2512.01463 : sections 1, 5, 6, 8, 10, 11 non détectées ; Tables 3, 6, 7 absentes ;
  - 2103.05579 : Table 1 (ressources FPGA PTQ vs QAT) absente — seuls chiffres propres du
    papier, donc aucune ligne de benchmark ;
  - 2602.15751 : corps de la Table 1 absent (chiffres pris dans le texte, `medium`) ;
  - 2604.21280 : Tables III (résolutions d'entrée) et V absentes ;
  - 2509.04153 (I), 1806.01683 (3) : titres non détectés, sans impact sur les fiches.
- [x] `arxiv-2602.15751-…` : `type: journal`, `venue` : *Machine Learning: Science and
  Technology* (DOI 10.1088/2632-2153/ae8218). Fait le 24/09/2026.
- [x] Venues et DOI des autres papiers (24/09/2026) : ELMAR 2025 (2507.18174), DATE 2024
  (2403.07851), FCCM 2026 (2604.21280), ACM TECS 2024 (2411.01431), TinyML Research
  Symposium 2021 (2103.05579, sans DOI), rapport technique HAL (1806.01683). Acceptation
  lue dans les commentaires arXiv, DOI confirmés par Crossref ; les fiches précisent que le
  texte lu est la version arXiv.
- [ ] Récupérer à la main les ~10 articles sous paywall de `basicStart.txt` (§7), les
  déposer dans `inbox/`, `ingest.py`, et vérifier chaque référence contre le PDF réel.
- [x] Ajouter les références externes les plus co-citées (24/09/2026) : FINN (1612.07119,
  FPGA '17, DOI 10.1145/3020078.3021744), FINN-R (1809.04570, ACM TRETS 11(3), DOI
  10.1145/3242897), fpgaConvNet **toolflow** (1711.08740, workshop NIPS 2017 — ce n'est
  pas l'article FCCM 2016, qui reste en tête d'`external_refs.csv`, cité par 6 papiers,
  paywall IEEE).
- [ ] Prochains candidats d'`external_refs.csv` (à vérifier avant ajout) : *Fast inference
  of deep neural networks in FPGAs for particle physics* (arXiv 1804.06913, 4 citants),
  *Latency-Driven Design for FPGA-based Convolutional Neural Networks* (FPL 2017).
- [ ] Trier les candidats de `bin/pdb discover` (premier passage le 24/09/2026, métadonnées
  OpenAlex non vérifiées) via `/paper-discover`. Les trois cités en tête à l'époque
  (2101.05108, 2108.03986, 2110.10486) sont dans la base et fichés (constaté le 01/10/2026) ;
  `candidates.csv` reste à trier.
- [x] Clé OpenAlex gratuite (`OPENALEX_API_KEY`) configurée dans `~/.bashrc` le
  24/09/2026 : `--query` et `--axis` ne dépendent plus de la recherche anonyme (HTTP 429 et
  503 constatés sans clé).
- [x] Vérification du §8, points 1 à 5 (24/09/2026) :
  1. métadonnées de 2507.18174 correctes ;
  2. texte : ordre des sections, en-têtes, bibliographie et légendes corrects, mais la
     fin de §III-B est classée en « figure sans légende » et le titre « V. CONCLUSION » est
     absorbé par la Table I ; césures perdues (« FPGAbased ») ;
  3. repli PyMuPDF (GROBID arrêté, FINN) : `backend = "pymupdf"`, `ok: false`, warnings
     explicites, aucune section détectée ; ré-extraction GROBID ensuite par `--force` ;
  4. PDF sans métadonnées : le PDF éditeur ACM est bloqué (403 anti-bot), test fait avec le
     PDF arXiv de FINN-R sans `.meta.json` ; a révélé les défauts d'en-tête corrigés dans
     `lib/tei.py` (voir « En place ») ;
  5. `INDEX.md` : comptes justes, papiers rangés sous leurs axes.
- [ ] §8.6-8.7, à faire par l'utilisateur : recouper une fiche avec un PDF lu soi-même ;
  poser une question quantitative dans une session neuve et vérifier qu'aucun PDF n'est
  rouvert.
- [x] Commiter la visualisation : déjà fait (commit 6f04a6b).

### Tâches — analyse

- [ ] Expérience de référence YOLOv5 INT8 sur KV260 avec protocole de mesure complet :
  voir « Prochaines étapes prioritaires » (3). Consigner les résultats dans
  `benchmarks.csv` sous le `paper_id` `own-2026-kv260-map-sur-cible` (convention des mesures
  propres définie le 25/09/2026, DATA_MODEL §1 ; `bin/pdb bench --own`).

- [ ] Généalogies à relever dès maintenant (onglet Généalogie) : `hls4ml`, `finn|binar`,
  `yolo|you only look once` — lignées de toolflows et points où le corpus ne couvre pas un
  maillon (candidats à `/paper-add`).
- [ ] Une fois 15-20 fiches `done` : repasser sur la vue 3D (placement *force*, liens
  *thèmes communs* + *références partagées*) et relever les axes isolés ou peu reliés entre
  eux — candidats à reporter dans `gaps.md` via `/paper-gaps`.
- [ ] Au même stade, `/graphify PaperDatabase/papers` pour une détection de communautés,
  à confronter à la vue 3D.

### Tâches — outillage

- [x] **Point d'entrée unique et état de la base** (24/09/2026) : `bin/pdb`, `pdb status`
  (prochaines actions), réindexation automatique après `add`/`ingest`.
- [x] **Ajout par DOI et par lot** (24/09/2026) : `add.py` résout un DOI vers sa version
  arXiv (OpenAlex) et lit `--from liste.txt`.
- [x] **Découverte de candidats** (24/09/2026) : `bin/discover.py`, `lib/openalex.py`,
  `/paper-discover`, `candidates.csv` ; guide `docs/GUIDE.md`.
- [ ] **Roder `/paper-discover`** sur un axe et un gap. Fait le 25/09/2026 : `in_topic` exige
  un titre explicite (`TITLE_TOPIC_RE` : FPGA, accélérateur, TinyML, MCU, edge computing…),
  un axe matériel, ou au moins deux mentions de `TOPIC_RE`. Évalué sur les 857 travaux du
  cache OpenAlex : 34 hors-sujet sortent (SqueezeNet, DoReFa-Net, chants d'oiseaux…), 46
  papiers TinyML / accélérateurs / apprentissage on-device entrent (472 → 484 « oui »).
  Reste : relancer `bin/pdb discover` en réel (écrase `candidates.csv`), puis juger le tri
  et le score sur un axe et un gap.

- [x] **Axes et tags stables à la ré-extraction** (24/09/2026) : `keep_classification`
  dans `ingest.py`, testé par `test_ingest.py`.
- [x] **Classement des références externes** (24/09/2026) : `external_refs.csv`, généré par
  `reindex.py`.
- [x] **Fusion des variantes d'une même référence** (24/09/2026) : `lib/refs.py` fusionne
  les titres quasi identiques (ratio ≥ 0,92, ou préfixe ≥ 6 mots, années à ±1 an) ; les
  publications distinctes (fpgaConvNet FCCM 2016 / TNNLS 2019) restent séparées.
- [x] **Ligatures perdues à l'extraction** (25/09/2026) : `lib/ligatures.py` recolle les
  mots (« classi cation », « e cient », « the rst ») d'après le vocabulaire du corpus (mots
  présents dans ≥ 2 papiers) et une liste intégrée ; warning dans `extraction.warnings`.
  1806.01683 : 162 mots réparés, aucun fragment restant, aucune modification ailleurs.
- [x] **Texte classé en figure par GROBID** (25/09/2026) : `tei.looks_like_prose`, puis
  réinsertion après le paragraphe coupé (même page ou bas de la précédente). 40 → 21
  « [figure sans légende identifiée] » dans le corpus ; les restantes sont de vraies
  légendes, des tableaux, ou des cas ambigus (« The anticipated output… », 2024-mittal).
- [x] **Note `reindex.py` pour une fiche `done` sans benchmark** (25/09/2026) :
  `benchmarks: none` dans le front-matter de la fiche (DATA_MODEL §8) ; posé sur hls4ml 2021
  (2103.05579) et fpgaConvNet (1711.08740).
- [x] **Ré-extraction sans GROBID** (25/09/2026) : `bin/pdb ingest --reparse [id…]` relit
  `grobid.tei.xml` ; les avertissements manuels survivent à la ré-extraction. Corpus
  ré-extrait le 25/09/2026 ; `pdb test --rag` : rappel inchangé (RAG.md §10).
- [x] **Embeddings dans la vue 3D** (24/09/2026) : `lib/embed.py` (sentence-transformers,
  cache `.cache/embeddings/`), bouton TF-IDF / embeddings dans `viz.py`. Pas encore testé
  avec le vrai modèle (dépendance non installée) : à faire après
  `pip install -r requirements-embed.txt`. Réutilisable pour la recherche sémantique
  ci-dessous.
- [ ] **Améliorations du 02/10/2026, spécifiées** (lots A et B faits) : fiabilité des réponses,
  tableaux et nouveaux skills ([docs/AMELIORATIONS.md](docs/AMELIORATIONS.md), §10 pour
  l'ordre) :
  - [x] lot A, évaluation des réponses finales (02/10/2026) : `pdb eval --answers DIR` et
    `--questions`, mode `--record` de `/paper-ask`, skill `/eval-answers`, jeux de départ
    fpga `tests/fixtures/answers{,_holdout}.jsonl` (12 + 12, 4 catégories dont hors corpus),
    protocole [docs/EVAL.md](docs/EVAL.md) §10. Premier run le 02/10/2026, en lexical seul
    (verdict juste 0,83 dev / 0,92 holdout, hors corpus 6/6, EVAL.md §10). Second run le
    même jour (lot B), 22 verdicts sur 24 stables. Restent : run hybride + rerank, sources alternatives dans les jeux, jeux
    40 / 60 relus par un tiers, jeux drone et stage, notes humaines, seuils ;
  - [x] lot B, verdict suffisant / partiel / absent par exigence dans `/paper-ask`
    (02/10/2026) : exigences avant la recherche, verdict en tête de chaque réponse, même règle
    dans `/paper-research` et les `CLAUDE.md` de base. Second run du banc (lexical seul) :
    hors corpus 6/6, 0 faux `absent`, citations 1,00, 22 verdicts sur 24 stables
    (EVAL.md §10) ;
  - [x] lot C, preuves atomiques `claims.jsonl` et skill `/paper-extract` (03/10/2026) :
    `schema.validate_claim_row`, `lib/claims.py`, contrôle des excerpts dans `reindex`,
    `pdb claims <id> [--check]`, DATA_MODEL §12. Essai sur FINN (fpga) : 32 claims, 100 %
    des excerpts vérifiés. Restent : claims indexées par `lib/rag.py` et lues par
    `/paper-ask`, extraction des autres papiers ;
  - [x] lot D-1 à D-4 (03/10/2026) : colonnes optionnelles de `benchmarks.csv` (`chunk_id`,
    `metric_def`, `dataset_split`, `input_res`, `batch`, `measure_protocol`,
    `original_value` ; `schema.check_header`), `pdb bench --add-columns` et `--check`
    (valeur dans le passage cité), mesure `in_cited_chunk` du banc `table_values`,
    `/paper-fiche` qui les remplit. Les trois bases réindexent sans changer leur CSV ;
  - [x] lot D-5 (03/10/2026), `pdb bench --comparable [accuracy|power]` : groupes par tâche,
    jeu, split, métrique (ou portée de puissance), comparaisons impossibles signalées ;
    consigne dans `/paper-ask` ;
  - [x] lot E-a, E-c, E-d (03/10/2026) : `bbox` et `table_source` dans `sections.jsonl`
    (trois bases complétées sans changer le texte), index des grands tableaux par rangées
    avec légende et en-tête répétés (`rag.split_table`), signaux de qualité par tableau
    (`tables.quality`, `pdb status --tables`), `tables.label_number` corrigé pour les
    légendes sans espace (« TABLE1. ») ;
  - [ ] lot E-b et E-e : OCR par zone, vérité terrain annotée (`tables_gold.jsonl`) ;
  - [ ] lot F, recherche en français (requêtes multiples, modèle multilingue évalué, jeu
    ≥ 30 questions) ;
  - [ ] lot G, `pdb search` route de référence : en grande partie fait le 02/10/2026 (route CPU par défaut,
    Qwen comme moteur optionnel de `pdb search`, `pdb gpu`, `pdb eval --rag --gpu`
    comparable, `pdb rag` réservé au GPU ; RAG.md §13) ; reste `check-answer` qui contrôle
    les nombres et `/paper-research` sur les `chunk_id` ;
  - [ ] lot H, snapshot dans `pdb search --format json`, journal de réponses optionnel ;
  - [x] lot I, journal et coût des sous-agents (03/10/2026) : hook `SubagentStop` →
    `bin/agent_log.py` → `.cache/agents.jsonl`, `lib/agentlog.py`, `pdb agents [--scan]
    [--report] [--mark]`, convention `[classe]` dans le `CLAUDE.md` racine ; rattrapage :
    67 sous-agents ; puis calage de la sortie sur le cost-state (les 4 sessions à 0 %,
    sous-agents 78,9 $ au lieu de 55,6 $) et économie estimée de la délégation
    (`lib/agentcost.py`, `--session`, `--worst` : 119 $, 59 % du direct estimé) ;
  - [x] lot I-6, expérience appariée (03/10/2026) : 3 `/paper-fiche` en direct (2,30 $, 324 s)
    et déléguées à `sonnet` (1,35 $, 133 s) ; le contrefactuel prédit 2,21 $ pour le direct
    (−4 %). Elle a révélé que le hook passait avant le dernier tour : relecture détachée
    (`agent_log.py --refresh`) et `--scan` qui relit les agents incomplets ;
  - [ ] lot I-5e : après une vingtaine d'appels étiquetés et notés, révision chiffrée de la
    table de délégation du `CLAUDE.md` (`pdb agents --report`) ;
  - [ ] lot J, `pdb compare` (`lib/compare.py`) : deux axes avec clé de précision et
    `power_scope` ensemble, trois blocs (retenues traçables, conditions qui varient ou
    manquent, exclusions motivées), confiance de la comparaison, JSON ; puis figures et
    colonnes `clock_mhz` / `latency_scope` ;
  - [ ] skills `/paper-compare`, `/state-of-art`, `/table-review`, `/research-question`.
- [ ] **Pistes d'amélioration du 26/09/2026, non commencées** (analyse de la doc et du
  corpus ; ordre proposé) :
  1. ~~traçabilité : colonne `chunk_id` dans `benchmarks.csv` et `pdb bench --check`~~ :
     fait le 03/10/2026 (lot D) ;
  2. économie de tokens : `pdb outline <id>`, `pdb digest <id>` (abstract, contributions,
     résultats, conclusion, tableaux) et `pdb numbers <id>` (nombres + unités avec
     `chunk_id`). Réécrire ensuite `/paper-fiche` pour partir de ces sorties au lieu de lire
     `fulltext.md` en entier (15 à 275 Ko par papier), et rendre `/paper-gaps` incrémental
     (liste `gaps:` dans le front-matter des fiches) ;
  3. découverte : score sémantique des candidats (bge-small sur titre + résumé OpenAlex,
     comparé au corpus, aux axes et à `gaps.md`), couplage bibliographique,
     `candidates_decisions.csv` pour ne plus reproposer les rejets, et `discover --short N` ;
  4. généricité : profil de corpus `corpus.toml` (axes, regex, requêtes, colonnes de
     benchmark propres au domaine, template de fiche), aujourd'hui codé en dur dans
     `bin/ingest.py` et `lib/schema.py`, et `pdb init --profile` ;
  5. références consolidées via `referenced_works` d'OpenAlex (10 citations internes
     seulement) ; jeu d'évaluation RAG généré par corpus.
- [x] **Docling en second backend pour les tableaux** (branché le 26/09/2026, EVAL.md §6 ;
  prévu ainsi) : `bin/pdb ingest --tables docling [id…]` pour les tableaux « sans corps »,
  OCR réservé aux pages sans texte, rapprochement par page et libellé de légende, mention
  « reconstruit par Docling : à vérifier » ; `requirements-docling.txt` optionnel.
- [x] **Recherche sémantique** (25/09/2026) : `lib/rag.py`, index local **par-dessus**
  `sections.jsonl` (BM25 + sentence-transformers bge-small, fusion RRF), sans rien changer
  à l'arborescence. Pas de ChromaDB : une recherche exhaustive en numpy suffit jusqu'à
  ~10⁵ passages ([docs/RAG.md](docs/RAG.md) §11).

## 10. Route GPU optionnelle (Qwen3), acquisition et benchmark synthétique

Route GPU optionnelle, apportée par Maksym Lytvynenko : modèles `lib/rag_models.py`,
index de preuves `lib/rag_qwen.py`, acquisition `lib/rag_external.py`, commande
`bin/pdb rag`, skill `/paper-research`. **Elle ne sert que si l'utilisateur veut utiliser
sa carte graphique et qu'elle est CUDA** ; la route par défaut est `pdb search` (CPU, §5).
Les deux routes travaillent ensemble ([docs/RAG.md §13](docs/RAG.md#13-route-gpu-optionnelle-qwen3)) :

- `bin/pdb gpu on` active la route (réglage de la machine ; `PDB_GPU=1|0` pour une session).
  `pdb search`, et donc `/paper-ask`, encodent alors les mêmes passages avec Qwen : mêmes
  `chunk_id`, mêmes `show` / `verify`. Sans torch, sans CUDA ou sans vecteurs Qwen pour la
  base, `pdb search` reste sur le CPU et le dit ;
- `pdb reindex` met à jour les vecteurs Qwen et l'index de `pdb rag` quand la route est
  active ;
- `pdb eval --rag --gpu --compare <run CPU>` compare les deux moteurs sur les mêmes jeux ;
- `pdb rag` (dense, hybride, `acquire`, `approve`) s'arrête d'emblée sans GPU et renvoie
  vers `pdb search`.

Le benchmark synthétique qui évalue la route est `bin/pdb synth` ([docs/BENCHMARK.md](docs/BENCHMARK.md)).

Installer `.venv/bin/pip install -r requirements-rag.txt`, puis lancer `bin/pdb gpu on`
(modèles et vecteurs de `pdb search`) et, pour `/paper-research`,
`bin/pdb rag index --download`. Cette première exécution télécharge les versions épinglées
de Qwen3-Embedding-4B et Qwen3-Reranker-4B ; les suivantes se font depuis le cache local.
La commande nécessite un GPU CUDA compatible pour les modes `dense` et `hybrid`. Sur une
machine sans GPU, `bin/pdb rag index --mode lexical` et
`bin/pdb rag search "question" --mode lexical` restent disponibles. Les dépendances de
`requirements-embed.txt` concernent uniquement la visualisation et sont indépendantes.

L'index `.cache/rag/index.sqlite3` est un instantané des fichiers sources. Après une
modification manuelle de `sections.jsonl`, `fiche.md`, `metadata.json` ou `benchmarks.csv`,
relancer `bin/pdb rag index`. Une recherche sur un index périmé échoue explicitement.
`bin/pdb rag search "question"` renvoie des identifiants de passage, leurs pages, sections,
types, empreintes de source et scores ; `bin/pdb rag evidence ID --parent` affiche aussi la
section parente. Les faits rapportés doivent venir de `abstract`, `section`, `table` ou
`figure` ; les fiches guident la navigation et les lignes de benchmark sont des
transcriptions à vérifier contre l'original.

`bin/pdb rag benchmarks --filter-json '[{"field":"fps","op":"gte","value":25}]'`
parcourt toutes les configurations sans limite de résultats. Une valeur `n/r` n'entre pas
dans un filtre numérique. `computed_fps_per_w` apparaît uniquement quand FPS et puissance
sont tous deux rapportés ; le `power_scope` est conservé. Pour vérifier les identifiants et
les extraits d'une réponse, enregistrer un JSON contenant `snapshot` et
`claims: [{"text": "...", "citations": [{"id": "...", "excerpt": "..."}]}]`, puis lancer
`bin/pdb rag check-answer réponse.json`. Ce contrôle est structurel : l'agent doit encore
vérifier que le passage soutient réellement la phrase.

Dans Claude Code, `/paper-research <question>` (route GPU seulement) effectue une rédaction suivie d'une liste de
trois lacunes au maximum, de recherches complémentaires, puis d'un contrôle des sources.
Quand le corpus ne suffit pas, `bin/pdb rag acquire "requête" --run identifiant` interroge
OpenAlex et arXiv, met les PDF en staging, vérifie qu'un passage extrait répond à la requête,
et laisse les articles retenus en staging. Seuls ceux que l'utilisateur accepte entrent dans
`papers/`, via `bin/pdb rag approve identifiant PAPER_ID…`, qui reconstruit ensuite les
index. Chaque ajout conserve
`acquisition.json` ; la fiche reste `todo`. Le budget partagé d'un run est huit recherches,
huit PDF, 50 Mo par PDF, 200 Mo au total et quinze minutes. Les échecs de téléchargement ou
d'extraction sont rapportés, jamais interprétés comme absence de travaux.

La base d'évaluation pilote et les commandes d'ablation sont dans
`docs/RAG_IMPLEMENTATION_PLAN.md`. L'étude bibliographique qui motive ces choix est dans
`docs/research/rag-improvement-study-2026-09-25.md`.
