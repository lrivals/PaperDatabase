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

L'arborescence reste la source de vérité, lisible et réparable à la main. Un index de
recherche dérivé et reconstruisible dans `.cache/rag/` combine recherche lexicale,
embeddings locaux et reclassement pour trouver les passages à vérifier.

---

## 1. Traitement des PDF

```
arXiv id / URL ──► bin/add.py ──► inbox/ ──► bin/ingest.py ──► papers/<paper_id>/
PDF local ────────────────────────► inbox/        │
                                                  ├─ GROBID (Docker) : structure, métadonnées, références
                                                  └─ repli PyMuPDF si GROBID est indisponible
```

- **`add.py`** récupère un article arXiv (métadonnées via l'API, puis le PDF) ou copie un
  PDF local dans `inbox/`, puis lance l'ingestion.
- **`ingest.py`** passe chaque PDF de `inbox/` dans GROBID :
  - il fusionne les métadonnées (export de citation `.bib` / `.ris` déposé à côté, puis
    arXiv, puis GROBID ; un champ inconnu reste `null`) ;
  - il nettoie le corps (en-têtes, numéros de page, bibliographie) ;
  - il garde les légendes de figures et de tableaux, qui portent souvent les chiffres ;
  - il écrit les fichiers ci-dessous.

  Il est idempotent, et `--force` réextrait sans jamais écraser une fiche déjà rédigée.
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

---

## 2. Base de connaissance et navigation par un LLM

L'agent lit **du résumé vers le détail** et s'arrête dès qu'il a la réponse :

| Couche | Fichier | Sert à |
|---|---|---|
| 1 | `INDEX.md` | savoir quels articles existent, par axe, fichés ou non (généré par `reindex.py`) |
| 2 | `benchmarks.csv` | trouver tous les chiffres, une ligne par configuration rapportée, avec section source et niveau de confiance |
| 3 | `papers/<id>/fiche.md` | lire l'analyse critique d'un article |
| 4 | `fulltext.md`, `sections.jsonl` | lire le texte intégral ; `grep` sur `papers/*/sections.jsonl` pour chercher dans tout le corpus |
| 5 | `gaps.md` | consulter les zones non couvertes par le corpus, chacune appuyée par des `paper_id` |
| — | `external_refs.csv` | repérer les travaux absents de la base les plus cités par le corpus (généré par `reindex.py`) : les prochaines lectures |

**Liens entre articles :**

- des axes de veille (valeurs fermées) et des tags (modèles, plateformes, toolflows) ;
- les références extraites, qui permettent de repérer les citations internes au corpus ;
- les clés `paper_id` partagées entre `benchmarks.csv`, les fiches, `INDEX.md` et `gaps.md`.

**Mode d'emploi de l'agent :** [CLAUDE.md](CLAUDE.md) donne l'ordre de lecture et les règles
de travail : ne jamais inventer de référence, écrire `n/r` pour une valeur non rapportée,
distinguer le lu du déduit, relever les comparaisons biaisées. Trois commandes Claude Code
(`.claude/commands/`) automatisent le travail :

| Commande | Effet |
|---|---|
| `/paper-add <arxiv-id \| url \| chemin.pdf>` | acquisition, ingestion et réindexation |
| `/paper-fiche <paper_id>` | remplit la fiche et ajoute les lignes de `benchmarks.csv`, chaque chiffre avec sa section source |
| `/paper-gaps` | met à jour `gaps.md` depuis les fiches terminées et les benchmarks |
| `/paper-ask <question>` | recherche des passages sourcés, vérifie les chiffres et complète éventuellement le corpus avec des PDF en libre accès |

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

Pour la recherche RAG locale sur GPU, installer les dépendances séparées puis construire
l'index dérivé :

```bash
.venv/bin/pip install -r requirements-rag.txt
bin/pdb rag index --download       # télécharge une fois les modèles Qwen épinglés
bin/pdb rag search "KV260 power consumption"
```

`/paper-ask` utilise cet index et peut chercher de nouveaux PDF via OpenAlex/arXiv quand
la base ne suffit pas. Les papiers importés gardent un PDF et une trace d'acquisition ;
leurs fiches restent à faire. Voir [le plan RAG](docs/RAG_IMPLEMENTATION_PLAN.md).

Le [benchmark synthétique](docs/BENCHMARK.md) utilise un corpus isolé de 200 articles,
des questions générées localement sur GPU et une validation automatique indépendante.
`bin/pdb bench --help` expose les étapes de construction et d'évaluation.

---

## Adapter à un autre sujet de recherche

Le pipeline ne dépend pas du domaine. Pour changer de sujet :

1. Définir les axes de veille dans `lib/schema.py` (`AXES`) et leurs titres dans
   `bin/reindex.py` (`AXIS_TITLES`).
2. Adapter la pré-classification automatique (`AXIS_RULES`, `TAG_RULES`) et la découverte
   (`TOPIC_RE`, `HARDWARE_AXES`, `AXIS_QUERIES`) dans `bin/ingest.py`.
3. Redéfinir les colonnes de `benchmarks.csv` (`BENCHMARK_COLUMNS`, `NUMERIC_COLUMNS` dans
   `lib/schema.py`) et le template de fiche.
4. Réécrire les règles de travail de [CLAUDE.md](CLAUDE.md) pour le domaine.

---

## Visualisation (outil secondaire)

Cet outil est une vue d'ensemble destinée à l'utilisateur. **Le LLM ne s'en sert pas.**

`bin/viz.py` est une application Dash locale à deux onglets.

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
├── docs/GUIDE.md           # guide d'utilisation
├── bin/                    # pdb (point d'entrée), setup.sh, grobid.sh, add.py, ingest.py,
│                           # reindex.py, discover.py, viz.py
├── lib/                    # ids, tei, doc, pdftext, schema, refs, openalex, status, graph…
├── tests/
├── .claude/commands/       # /paper-add, /paper-fiche, /paper-gaps, /paper-discover
├── inbox/                  # PDF en attente d'ingestion
└── papers/<paper_id>/      # un dossier par article
```

---

## État et documentation

Au 24/09/2026, le corpus couvre la vision embarquée sur FPGA, Jetson, VPU, Edge TPU, Hailo
et MCU :
- 28 articles ingérés, tous via GROBID : 21 par arXiv, 7 déposés à la main avec leur export
  de citation ;
- 24 fiches rédigées ;
- 109 lignes dans `benchmarks.csv` ;
- 16 gaps dans `gaps.md`, dont 12 étayés.

S'y ajoutent une liste de labos ([labs.md](labs.md)) et un protocole d'expérience
([docs/experiences/](docs/experiences/)). L'avancement et les tâches à faire sont dans
[SETUP.md §9](SETUP.md#9-état-actuel-et-tâches-à-faire).

| Document | Contenu |
|---|---|
| [docs/GUIDE.md](docs/GUIDE.md) | guide d'utilisation : prise en main, routine, extension du corpus, dépannage |
| [SETUP.md](SETUP.md) | installation, rôle de chaque script, flux de travail, vérification, tâches |
| [DATA_MODEL.md](DATA_MODEL.md) | schémas : `paper_id`, `metadata.json`, `sections.jsonl`, `refs.jsonl`, `benchmarks.csv`, fiche |
| [CLAUDE.md](CLAUDE.md) | mode d'emploi et règles de travail de l'agent |
| [INDEX.md](INDEX.md) | index des articles |
| [gaps.md](gaps.md) | carte des gaps |
