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

---

## 2. Arborescence

```
PaperDatabase/
├── README.md               # présentation du projet
├── CLAUDE.md               # mode d'emploi de la base pour l'agent
├── SETUP.md                # ce fichier
├── DATA_MODEL.md           # schémas et conventions
├── INDEX.md                # GÉNÉRÉ — table de tous les papiers
├── external_refs.csv       # GÉNÉRÉ — travaux hors base les plus cités par le corpus
├── candidates.csv          # GÉNÉRÉ par discover, non versionné — candidats OpenAlex
├── candidates_arxiv.txt    # GÉNÉRÉ par discover, non versionné — liste pour add --from
├── benchmarks.csv          # une ligne par configuration rapportée
├── gaps.md                 # carte des verrous et zones non couvertes
├── basicStart.txt          # bibliographie de départ (source d'amorçage)
├── requirements.txt
├── requirements-viz.txt    # optionnel : dépendances de la visualisation
├── requirements-embed.txt  # optionnel : embeddings (sentence-transformers) pour la visualisation
├── requirements-docling.txt # optionnel : Docling pour les tableaux sans corps
├── eval/                   # banc d'évaluation : thresholds.json, results/<date>-<commit>.json
├── .venv/                  # non versionné
├── .cache/                 # non versionné : embeddings, réponses OpenAlex
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
│   └── viz.py              # app Dash : graphe 3D et généalogie du corpus
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
│   ├── rag.py              # recherche de passages (pdb search, show, verify)
│   ├── evaluation.py       # banc d'évaluation (pdb eval)
│   ├── openalex.py         # client OpenAlex (DOI → arXiv, citations, recherche), cache
│   ├── status.py           # état de la base et prochaines actions (pdb status)
│   ├── graph.py            # nœuds, liens et positions du graphe 3D
│   ├── lineage.py          # généalogie : sous-graphe de citations sur une frise
│   ├── vizfig.py           # figures Plotly et panneau de détail de viz.py
│   └── embed.py            # optionnel : embeddings avec cache (.cache/)
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
│   ├── test_query.py
│   ├── test_rag.py         # encodeur factice
│   ├── test_graph.py
│   ├── test_lineage.py
│   ├── test_viz.py
│   ├── test_embed.py
│   ├── test_openalex.py    # OpenAlex simulé : découverte, ajout par DOI / liste
│   ├── test_citation.py    # exports .bib / .ris éditeur : lecture, appariement, priorité
│   └── test_status.py
├── .claude/commands/       # /paper-add, /paper-fiche, /paper-gaps, /paper-discover, /paper-ask
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
        └── fiche.md        # fiche de lecture
```

Les commandes Claude Code (`/paper-add`, `/paper-fiche`, `/paper-gaps`, `/paper-discover`) vivent dans
`.claude/commands/` : ce dossier est lui-même la racine du projet Claude Code (il porte
`CLAUDE.md`).

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
| `reindex` | `reindex.run` | |
| `discover …` | `discover.run` | |
| `grobid start\|stop\|status`, `viz`, `test` | `grobid.sh`, `viz.py`, `unittest` | |
| `search`, `show`, `verify` | `lib/rag.py` | recherche de passages (BM25 + embeddings bge-small, fusion RRF, `--rerank` en option), texte exact, contrôle de citation (statut `NOMBRES` si un nombre diffère) ; index dans `.cache/rag/`, reconstruit par `reindex` : [docs/RAG.md](docs/RAG.md) §4-5 |
| `eval [--extract\|--rag\|--speed] [--save] [--compare [JSON]]`, `test --rag` | `lib/evaluation.py` | banc d'évaluation : extraction, recherche (jeux `tests/fixtures/rag_eval*.jsonl`), pertinence, `verify`, temps ; runs dans `eval/results/`, seuils dans `eval/thresholds.json` : [docs/EVAL.md](docs/EVAL.md) |
| `bench [filtres]`, `paper <requête>…` | `lib/query.py` | requêtes N0 sans LLM sur `benchmarks.csv` et `metadata.json`, bibliothèque standard seulement ; `bench --own` pour les mesures propres ; options et format de sortie : [docs/RAG.md](docs/RAG.md) §5.1 et §5.4 |
| `cites <id> [--external]`, `cited-by <id>` | `lib/refs.py`, `lib/query.py` | graphe de citations internes, références hors base avec leur nombre de citants : [docs/RAG.md](docs/RAG.md) §5.5 |

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

[basicStart.txt](basicStart.txt) contient une vingtaine d'articles. Les neuf qui portent un
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

Point au 26/09/2026. À mettre à jour à chaque étape franchie (cocher, dater, déplacer dans
« En place »).

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
- Nouveaux fichiers : [labs.md](labs.md) (labos et encadrants, INSA Rennes / IETR à
  vérifier) et le protocole [docs/experiences/kv260-map-sur-cible.md](docs/experiences/kv260-map-sur-cible.md).
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
Rapport de référence dans `eval/results/`, seuils dans `eval/thresholds.json`. 153 tests.
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
   non exécuté) : [docs/experiences/kv260-map-sur-cible.md](docs/experiences/kv260-map-sur-cible.md).
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
   26/09/2026. 12 tableaux restent sans corps, dont au moins 7 blocs qui ne sont pas des
   tableaux (prose, algorithme ou note classés en tableau par GROBID) ; restent notamment
   2409.07114 Tables II et IV, et 2211.11647. Les 44 tableaux reconstruits (41 Docling, 3
   PyMuPDF) sont à relire avant tout usage chiffré. Défauts déjà repérés : cui Table 9
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
| Classement des références externes | `external_refs.csv` : 319 travaux hors base cités par ≥ 2 papiers (DATA_MODEL §9) |
| Tableaux réduits à leur légende (`lib/tables.py`, `lib/docling_tables.py`) | depuis le 26/09/2026 : repli `find_tables()` PyMuPDF (tableaux à filets, 3 reconstruits), puis Docling (41 reconstruits, OCR pour shuvo, cui, hozhabr) ; tableaux avec corps 0,66 → 0,90 (EVAL.md §6) ; testé (`test_tables.py`) ; 12 restent sans corps, dont au moins 7 faux tableaux. **Manque** : relecture des tableaux reconstruits (erreurs de colonnes, fragments d'OCR) |
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
| Banc d'évaluation (`bin/pdb eval`, `lib/evaluation.py`) | depuis le 26/09/2026 : extraction, recherche (dev, holdout, FR, hors corpus), `verify`, temps ; `--save` / `--compare` et seuils ; testé (`test_evaluation.py`) ; rapport de référence dans [docs/EVAL.md](docs/EVAL.md) §5, corrections mesurées (§6) |
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
  OpenAlex non vérifiées) via `/paper-discover`. En tête : *Fast convolutional neural
  networks on FPGAs with hls4ml* (arXiv 2101.05108, cite 4 papiers du corpus) ;
  *Autoencoders on field-programmable gate arrays for real-time, unsupervised new physics
  detection at 40 MHz at the LHC* (arXiv 2108.03986) pour l'axe `autoencoder-fpga`, qui
  n'a qu'un papier ; *A TinyML Platform for On-Device Continual Learning With Quantized
  Latent Replays* (arXiv 2110.10486) pour la comparaison MCU / FPGA en apprentissage continu.
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
- [ ] **Pistes d'amélioration du 26/09/2026, non commencées** (analyse de la doc et du
  corpus ; ordre proposé) :
  1. traçabilité : colonne `chunk_id` dans `benchmarks.csv` et `pdb bench --check`, qui
     vérifie que chaque valeur numérique apparaît dans son passage source ;
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

## 10. Recherche GPU (Qwen3), acquisition et benchmark synthétique

Second moteur de recherche, indépendant de `pdb search` (bge-small, CPU, §5) : module `lib/rag_qwen.py`, commande `bin/pdb rag`, skill `/paper-research`. Le benchmark synthétique qui l'évalue est `bin/pdb synth` ([docs/BENCHMARK.md](docs/BENCHMARK.md)).

Installer `.venv/bin/pip install -r requirements-rag.txt`, puis lancer
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

Dans Claude Code, `/paper-research <question>` effectue une rédaction suivie d'une liste de
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
