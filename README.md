# PaperDatabase

Transforme des PDF d'articles scientifiques en une **base de connaissance textuelle,
structurée et reliée**, qu'un LLM (ici Claude Code) peut parcourir avec `grep` et `read`
sans jamais rouvrir un PDF.

L'outil n'est lié à aucun domaine : il traite n'importe quel corpus d'articles scientifiques.
Son **cas de test et d'usage** actuel est la préparation d'une thèse sur la vision embarquée
sur FPGA (YOLO, autoencodeurs, apprentissage continu). Les axes, les tags et les colonnes de
benchmark de ce dépôt sont ceux de ce cas d'usage ; ils se remplacent facilement (voir
[Adapter à un autre sujet](#adapter-à-un-autre-sujet-de-recherche)).

---

## Pourquoi

Dans un projet de recherche, un LLM travaille mal sur des PDF bruts. Il perd du contexte à
les relire, ne sait pas où chercher un chiffre et confond vite ce que dit un article avec ce
qu'il en déduit.

PaperDatabase convertit chaque article en fichiers texte : sections numérotées et paginées,
métadonnées vérifiées, références extraites, fiche de lecture et chiffres rangés dans un CSV.
Ces fichiers s'organisent en couches, du résumé au texte intégral. L'agent lit la couche la
plus haute qui répond à sa question et ne descend que si nécessaire.

Il n'y a pas de base de données. La source de vérité est une arborescence de fichiers texte
bien nommés et greppables, lisible, diffable et réparable à la main. Un index de passages
local (BM25 + embeddings, dans `.cache/`, régénérable) s'ajoute par-dessus pour la recherche
par le sens, sans rien changer aux fichiers.

---

## 1. Traitement des PDF

```
arXiv id / URL ──► bin/add.py ──► inbox/ ──► bin/ingest.py ──► papers/<paper_id>/
DOI ──► OpenAlex ──► version arXiv ─┘              │
PDF local (+ .bib/.ris) ──────────► inbox/        ├─ GROBID (Docker) : structure, métadonnées, références
                                                  ├─ PyMuPDF : tableaux réduits à leur légende
                                                  └─ repli PyMuPDF si GROBID est indisponible
```

- **`add.py`** récupère un article arXiv (métadonnées via l'API, puis le PDF), résout un DOI
  vers sa version arXiv via OpenAlex, ou copie un PDF local dans `inbox/`, puis lance
  l'ingestion. `--from liste.txt` traite un lot.
- **`ingest.py`** passe chaque PDF de `inbox/` dans GROBID :
  - il fusionne les métadonnées (export de citation `.bib` / `.ris` déposé à côté, puis
    arXiv, puis GROBID ; un champ inconnu reste `null`) ;
  - il nettoie le corps (en-têtes, numéros de page, bibliographie), répare les ligatures
    perdues (« classi cation ») et rend au corps les paragraphes que GROBID prenait pour
    des figures ;
  - il garde les légendes et le contenu des tableaux, qui portent souvent les chiffres ;
    quand GROBID n'a gardé que la légende, il tente de reconstruire le tableau depuis le
    PDF (PyMuPDF, puis Docling avec `--reparse --tables docling [--ocr]`), marqué « à
    vérifier », sinon il le signale ;
  - il écrit les fichiers ci-dessous.

  Il est idempotent, et `--force` réextrait sans jamais écraser une fiche déjà rédigée.
  `--reparse` ré-extrait tout le corpus depuis les TEI conservés, sans GROBID, après une
  amélioration du parsing.
- Les articles sous paywall se déposent **à la main** dans `inbox/`. L'outil ne contourne
  aucun paywall.

Chaque article devient un dossier `papers/<paper_id>/` :

| Fichier | Contenu |
|---|---|
| `metadata.json` | titre, auteurs, année, venue, DOI/arXiv, type (preprint signalé), axes, tags, statut |
| `fulltext.md` | texte intégral nettoyé, sections `##` / `###` avec leur numérotation d'origine |
| `sections.jsonl` | une ligne par section avec son type (abstract, section, figure, table) et sa **page** |
| `refs.jsonl` | références citées : titre, auteurs, année, DOI, arXiv id |
| `fiche.md` | fiche de lecture : problème, méthode, résultats, limites, pertinence, lu vs déduit |
| `paper.pdf`, `grobid.tei.xml` | preuve et trace d'extraction, non versionnés |
| `docling_tables.json` | tableaux lus par Docling, s'il a été lancé (trace, relue par `--reparse`) |

---

## 2. Base de connaissance et navigation par un LLM

L'agent lit **du résumé vers le détail** et s'arrête dès qu'il a la réponse :

| Couche | Fichier | Sert à |
|---|---|---|
| 1 | `INDEX.md` | savoir quels articles existent, par axe, fichés ou non (généré par `reindex.py`) |
| 2 | `benchmarks.csv` | trouver tous les chiffres, une ligne par configuration rapportée, avec section source et niveau de confiance |
| 3 | `papers/<id>/fiche.md` | lire l'analyse critique d'un article |
| 4 | passages (`bin/pdb search`, `show`, `verify`) | trouver les 2-3 passages qui répondent, les lire en texte exact, vérifier chaque citation |
| — | `fulltext.md` | texte intégral, en dernier recours seulement |
| 5 | `gaps.md` | consulter les zones non couvertes par le corpus, chacune appuyée par des `paper_id` |
| — | `external_refs.csv` | repérer les travaux absents de la base les plus cités par le corpus (généré par `reindex.py`) : les prochaines lectures |

**Requêtes sans LLM** (`bin/pdb`, bibliothèque standard ou index local ; sortie compacte,
colonnes de source toujours affichées) :

| Commande | Effet |
|---|---|
| `bin/pdb bench [filtres]` | filtre `benchmarks.csv` (plateforme, colonne renseignée, tri, `--count`) |
| `bin/pdb paper <id \| mot>` | fiche d'identité d'un papier : métadonnées, preprint, statut de fiche, benchmarks |
| `bin/pdb search "<question>"` | passages classés (BM25 + embeddings bge-small, fusion RRF, `--rerank` en option), avec `chunk_id`, section et page |
| `bin/pdb show <chunk_id>` / `verify <chunk_id> "<citation>"` | texte exact d'un passage / contrôle qu'une citation y figure, nombres compris (`NOMBRES` si un chiffre diffère) |
| `bin/pdb cites <id>` / `cited-by <id>` | graphe de citations internes, références hors base (`--external`) |

Sur un essai réel (répondre à une question sur la mesure de puissance), cette chaîne a lu
~2 500 tokens au lieu des textes intégraux.

**Performances mesurées** par le banc `bin/pdb eval` ([docs/EVAL.md](docs/EVAL.md)) :
- recherche : recall@5 de 0,90 en anglais sur le jeu qui a servi aux réglages, 0,84 sur un
  jeu de questions jamais utilisé pour régler, et 0,50 en français ;
- `verify` rejette les 38 citations dont un chiffre a été modifié et accepte les 40
  citations exactes ;
- extraction : 91 % du texte du PDF retrouvé et 90 % des tableaux avec leur corps.

Limite connue : `search` renvoie toujours des passages, et aucun score ne dit de façon fiable
que la base ne traite pas une question.

**Liens entre articles :**

- des axes de veille (valeurs fermées) et des tags (modèles, plateformes, toolflows) ;
- les références extraites, qui permettent de repérer les citations internes au corpus ;
- les clés `paper_id` partagées entre `benchmarks.csv`, les fiches, `INDEX.md` et `gaps.md`.

**Mode d'emploi de l'agent :** [CLAUDE.md](CLAUDE.md) donne l'ordre de lecture et les règles
de travail : ne jamais inventer de référence, écrire `n/r` pour une valeur non rapportée,
distinguer le lu du déduit, relever les comparaisons biaisées. Cinq commandes Claude Code
(`.claude/commands/`) automatisent le travail :

| Commande | Effet |
|---|---|
| `/paper-add <arxiv-id \| url \| doi \| chemin.pdf>` | acquisition, ingestion et réindexation |
| `/paper-fiche <paper_id>` | remplit la fiche et ajoute les lignes de `benchmarks.csv`, chaque chiffre avec sa section source |
| `/paper-ask <question>` | réponse sourcée : `bench`, puis `search`, `show`, `verify` ; chaque citation vérifiée |
| `/paper-discover [axe \| gap \| mots-clés]` | candidats via OpenAlex (citations du corpus, recherche), liste courte, ajout après accord |
| `/paper-gaps` | met à jour `gaps.md` depuis les fiches terminées et les benchmarks |

---

## Principes

- **Tout est du texte**, à part le PDF d'origine conservé comme preuve.
- **Chaque chiffre est traçable** : il porte sa section, son tableau ou sa figure source.
  Une valeur non rapportée s'écrit `n/r`, jamais une estimation.
- **Le lu et le déduit sont séparés** : chaque fiche a une section « Statut de lecture »
  obligatoire.
- **Un seul endroit code le schéma** : `lib/schema.py`, validé par `reindex.py`.

---

## Démarrage rapide

Prérequis : Python 3.12, Docker. **Guide d'utilisation pas à pas : [docs/GUIDE.md](docs/GUIDE.md).**
Présentation sous forme d'article (principes, RAG, tests, évaluation) :
[docs/article/](docs/article/), à compiler avec `make -C docs/article`.

```bash
bash bin/setup.sh              # crée .venv, installe requirements.txt
bin/pdb grobid start           # GROBID sur localhost:8070
bin/pdb status                 # état de la base et prochaines actions
bin/pdb add 2507.18174         # un article arXiv (ou un DOI, un PDF local, --from liste.txt)
bin/pdb discover               # papiers candidats à l'ajout (OpenAlex) → candidates.csv
```

`add` et `ingest` réindexent d'eux-mêmes (`INDEX.md`, `external_refs.csv`). Ensuite, dans
Claude Code : `/paper-fiche <paper_id>` produit la fiche de lecture, `/paper-discover`
propose des papiers à ajouter, `/paper-gaps` met à jour la carte des gaps. Le détail de
chaque script est dans [SETUP.md](SETUP.md).

---

## Recherche GPU et benchmark synthétique

En complément de `pdb search`, `bin/pdb rag` indexe le corpus avec Qwen3-Embedding-4B et Qwen3-Reranker-4B (GPU CUDA, `requirements-rag.txt`) et peut acquérir des PDF en libre accès ; `/paper-research` s'en sert. `bin/pdb synth` construit un benchmark synthétique sur un corpus isolé de 200 articles (questions générées localement, validées par deux sessions indépendantes ; validation, agents et juge passent par Claude Code en mode non interactif) : [docs/BENCHMARK.md](docs/BENCHMARK.md), [SETUP.md §10](SETUP.md).

---

## Adapter à un autre sujet de recherche

Le pipeline ne dépend pas du domaine, et un même code sert plusieurs bases séparées, une
par sujet ([DATA_MODEL.md §11](DATA_MODEL.md#11-plusieurs-bases--registre-basejson-profilemd)) :

1. `bin/pdb base new <nom> --theme "…"` crée la base (dossier, liens vers le code,
   `profile.md`, `CLAUDE.md` générique) et l'enregistre.
2. `/base-profile`, dans ce dossier, propose les axes de veille, les règles de
   pré-classification et de découverte (`base.json`) et le périmètre (`profile.md`) ; le
   profil se précise ensuite au fil des fiches, toujours sur validation de l'utilisateur.
3. `bin/pdb base scan` puis `bin/pdb base import` reprennent dans les autres bases les articles
   utiles au nouveau sujet.

Les colonnes de `benchmarks.csv` (`BENCHMARK_COLUMNS` dans `lib/schema.py`) et le template de
fiche restent communs à toutes les bases.

---

## Visualisation (outil secondaire)

Cet outil est une vue d'ensemble destinée à l'utilisateur. **Le LLM ne s'en sert pas.**

`bin/viz.py` est une application Dash locale à trois onglets (Graphe 3D, Généalogie, Bases),
avec un sélecteur de la base affichée.

**Graphe 3D** — le corpus en nuage de points :

- la couleur donne le thème (axe, tag, année, type ou statut de fiche) ;
- les liens montrent les citations, les références partagées, la similarité textuelle
  (TF-IDF, ou embeddings si `requirements-embed.txt` est installé) ou les thèmes communs ;
- le placement est soit force-directed, soit sémantique ;
- recherche par titre ou auteur, filtres par année, statut de fiche et type ;
- un clic affiche la fiche de lecture et les lignes de `benchmarks.csv` du papier ;
- en option, les travaux cités par plusieurs articles mais absents de la base apparaissent,
  comme candidats à l'ajout.

**Généalogie** — l'historique d'un sujet ou d'un papier sur une frise chronologique, le long
des citations : ce qu'il cite, ce qui le cite, et, en option, les « suites probables »
déduites de la similarité textuelle (signalées comme inférées).

```bash
.venv/bin/pip install -r requirements-viz.txt   # dépendances séparées, optionnelles
.venv/bin/python bin/viz.py                     # http://127.0.0.1:8050
```

Détails et limites : [SETUP.md §5](SETUP.md#binvizpy---port-8050---debug).

---

## Arborescence

```
PaperDatabase/
├── README.md  CLAUDE.md  SETUP.md  DATA_MODEL.md
├── INDEX.md  external_refs.csv   # générés
├── benchmarks.csv  gaps.md  basicStart.txt
├── docs/                   # GUIDE.md (utilisation), RAG.md (recherche), EVAL.md (banc), experiences/
├── eval/                   # seuils et résultats du banc (pdb eval)
├── bin/                    # pdb (point d'entrée), setup.sh, grobid.sh, add.py, ingest.py,
│                           # reindex.py, discover.py, viz.py
├── lib/                    # ids, tei, doc, pdftext, ligatures, tables, schema, refs, query, rag,
│                           # openalex, citation, status, evaluation, docling_tables…
├── tests/
├── .claude/commands/       # /paper-add, /paper-fiche, /paper-gaps, /paper-discover, /paper-ask
├── inbox/                  # PDF en attente d'ingestion
└── papers/<paper_id>/      # un dossier par article
```

---

## État et documentation

Au 26/09/2026, le corpus couvre la vision embarquée sur FPGA, Jetson, VPU, Edge TPU, Hailo
et MCU :
- 28 articles ingérés, tous via GROBID : 21 par arXiv, 7 déposés à la main avec leur export
  de citation ;
- 24 fiches rédigées ;
- 109 lignes dans `benchmarks.csv` ;
- 16 gaps dans `gaps.md`, dont 12 étayés.

### Ce qui marche (testé : 162 tests unitaires, banc `pdb eval`, essais sur le vrai corpus)

- acquisition arXiv, DOI (via OpenAlex), PDF local, par lot ; exports `.bib` / `.ris`
  éditeur prioritaires sur l'en-tête GROBID (vérifié sur 6 exports IEEE, ACM, MDPI,
  Springer) ;
- extraction GROBID avec repli PyMuPDF, nettoyage d'en-tête, ligatures, hiérarchie des
  titres, ré-extraction sans GROBID ; axes, tags et avertissements manuels conservés ;
- requêtes sans LLM (`bench`, `paper`, `search`, `show`, `verify`, `cites`) et skill
  `/paper-ask`, essayée en réel ;
- découverte de candidats OpenAlex, `external_refs.csv`, `pdb status` avec prochaines
  actions ;
- tableaux réduits à leur légende : reconstruction PyMuPDF des tableaux à filets, puis
  Docling en option, avec OCR pour les tableaux en image (44 reconstruits sur 56, marqués
  « à vérifier ») ;
- banc d'évaluation `bin/pdb eval` : qualité d'extraction, recherche, `verify`, temps ;
  comparaison entre deux runs et seuils ([docs/EVAL.md](docs/EVAL.md)).

### Ce qui manque encore

- **Tableaux** : les 44 tableaux reconstruits sont à relire contre le PDF (colonnes décalées
  ou perdues, fragments d'OCR), et 12 restent sans corps. Les valeurs de `benchmarks.csv`
  ne sont retrouvées telles quelles dans leur tableau que dans 80 % des cas.
- **Recherche** : les questions sur tableaux échouent encore, et l'absence de sujet n'est
  pas détectée ([docs/EVAL.md](docs/EVAL.md) §6).
- **Généricité** : axes, regex de classification et colonnes de benchmark sont encore codés
  en dur (voir ci-dessus) ; un profil de corpus (`corpus.toml`) est prévu.
- **Économie de tokens** : `/paper-fiche` lit encore `fulltext.md` en entier ; un digest
  déterministe et une pré-extraction des nombres sont prévus.
- **Traçabilité automatique** : lier chaque ligne de `benchmarks.csv` à un `chunk_id` et
  vérifier que la valeur y figure.
- **Découverte** : score sémantique des candidats et mémoire des rejets ; références
  consolidées via OpenAlex (10 citations internes seulement aujourd'hui).

Détail et ordre proposé : [SETUP.md §9](SETUP.md#9-état-actuel-et-tâches-à-faire).

S'y ajoutent une liste de labos ([labs.md](labs.md)) et un protocole d'expérience
([docs/experiences/](docs/experiences/)). L'avancement et les tâches à faire sont dans
[SETUP.md §9](SETUP.md#9-état-actuel-et-tâches-à-faire).

| Document | Contenu |
|---|---|
| [docs/GUIDE.md](docs/GUIDE.md) | guide d'utilisation : prise en main, routine, extension du corpus, dépannage |
| [SETUP.md](SETUP.md) | installation, rôle de chaque script, flux de travail, vérification, tâches |
| [docs/RAG.md](docs/RAG.md) | requêtes sans LLM et recherche de passages : spécification, évaluation, essai réel |
| [docs/EVAL.md](docs/EVAL.md) | banc d'évaluation du logiciel (`pdb eval`) : protocole, résultats de référence, corrections mesurées |
| [DATA_MODEL.md](DATA_MODEL.md) | schémas : `paper_id`, `metadata.json`, `sections.jsonl`, `refs.jsonl`, `benchmarks.csv`, fiche |
| [CLAUDE.md](CLAUDE.md) | mode d'emploi et règles de travail de l'agent |
| [INDEX.md](INDEX.md) | index des articles |
| [gaps.md](gaps.md) | carte des gaps |
