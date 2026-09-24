# PaperDatabase — guide de mise en place

Base de connaissance d'articles scientifiques (vision embarquée sur FPGA), conçue pour être
interrogée par Claude Code.

Ce document décrit **quoi construire et comment le mettre en route**. Les schémas de données
exacts sont dans [DATA_MODEL.md](DATA_MODEL.md). Le mode d'emploi destiné à l'agent est dans
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

## 2. Arborescence cible

```
PaperDatabase/
├── CLAUDE.md               # mode d'emploi de la base pour l'agent
├── SETUP.md                # ce fichier
├── DATA_MODEL.md           # schémas et conventions
├── INDEX.md                # GÉNÉRÉ — table de tous les papiers
├── benchmarks.csv          # une ligne par configuration rapportée
├── gaps.md                 # carte des verrous et zones non couvertes
├── basicStart.txt          # bibliographie de départ (source d'amorçage)
├── requirements.txt
├── .venv/                  # non versionné
├── bin/                    # scripts du pipeline
│   ├── setup.sh
│   ├── grobid.sh
│   ├── add.py
│   ├── ingest.py
│   └── reindex.py
├── lib/                    # code partagé
│   ├── ids.py
│   ├── tei.py
│   └── schema.py
├── inbox/                  # dépôt des PDF à ingérer
└── papers/
    └── <paper_id>/
        ├── paper.pdf       # PDF d'origine, conservé comme preuve
        ├── grobid.tei.xml  # sortie brute de GROBID, trace d'extraction
        ├── metadata.json   # titre, auteurs, année, venue, DOI, axes, statut
        ├── fulltext.md     # texte nettoyé, sections en ## / ###
        ├── sections.jsonl  # une ligne par section, avec page
        ├── refs.jsonl      # références citées
        └── fiche.md        # fiche de lecture
```

Les commandes Claude Code (`/paper-add`, `/paper-fiche`, `/paper-gaps`) vivent dans
`.claude/commands/` : ce dossier est lui-même la racine du projet Claude Code (il porte
`CLAUDE.md`).

S'y ajoutent `lib/doc.py` (représentation intermédiaire commune aux deux backends, écriture
de `fulltext.md` / `sections.jsonl`), `lib/pdftext.py` (extraction de repli PyMuPDF) et
`tests/` (tests du parsing TEI sur une sortie GROBID réelle :
`.venv/bin/python -m unittest discover tests`).

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

## 4. Mise en place pas à pas

### Étape 1 — environnement Python

```bash
cd ~/Documents/Perso/PaperDatabase
bash bin/setup.sh          # crée .venv s'il n'existe pas, installe requirements.txt
```

**Critère de réussite :** `.venv/bin/python -c "import pymupdf, lxml, requests; print('ok')"`
affiche `ok`.

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

### Étape 3 — premier article de test

```bash
.venv/bin/python bin/add.py 2507.18174
```

**Critère de réussite :** un dossier `papers/arxiv-2507.18174-.../` contient `metadata.json`,
`fulltext.md`, `sections.jsonl` et `fiche.md`. Voir §7 pour la relecture à faire.

### Étape 4 — versionnage (recommandé)

Le dossier est un dépôt git (remote : `https://github.com/lrivals/PaperDatabase.git`). Le
versionnage rend l'état de l'art diffable : on voit la bibliographie se construire et les
fiches évoluer.

`.gitignore` :

```
**/paper.pdf
**/grobid.tei.xml
inbox/*.pdf
inbox/*.meta.json
.venv/
__pycache__/
```

Les PDF et les TEI bruts sont régénérables ou re-téléchargeables ; tout le corpus textuel,
les fiches et le CSV sont versionnés.

---

## 5. Les scripts à écrire

Cette section est la spécification d'implémentation. Chaque script a un rôle unique.

### `bin/setup.sh`

Crée le venv et installe `requirements.txt`. Idempotent : ne recrée pas un venv existant.

### `bin/grobid.sh {start|stop|status}`

- `start` : lance le conteneur s'il n'est pas déjà actif, puis boucle sur
  `/api/isalive` jusqu'à réponse `true` (timeout 120 s, message clair si dépassement).
- `stop` : arrête le conteneur.
- `status` : code de sortie 0 si GROBID répond, 1 sinon. Les autres scripts s'en servent
  pour décider du repli.

### `bin/add.py <arxiv-id|url|chemin.pdf>`

Acquisition. Trois formes d'entrée :

| Entrée | Comportement |
|---|---|
| `2507.18174` ou une URL `arxiv.org/abs/...` / `/pdf/...` | interroge l'API `export.arxiv.org/api/query` (titre, auteurs, date de v1, abstract, DOI si présent), télécharge le PDF dans `inbox/`, écrit un `<nom>.meta.json` compagnon |
| chemin vers un PDF local | copie dans `inbox/`, sans métadonnées compagnon |
| URL non-arXiv | refuse avec un message expliquant de télécharger le PDF à la main et de le déposer dans `inbox/` |

Enchaîne ensuite sur `ingest.py` pour le fichier concerné.

Cas d'erreur à traiter explicitement : id arXiv inexistant, réseau indisponible, PDF déjà
présent dans `inbox/` ou déjà ingéré.

### `bin/ingest.py [--force] [chemin.pdf]`

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
3. **Fusion des métadonnées**, par ordre de confiance décroissant :
   `.meta.json` arXiv > `teiHeader` GROBID > vide. Les champs restés vides sont laissés à
   `null` — jamais devinés.
4. **Nettoyage** du corps, dans cet ordre :
   - suppression des lignes identiques réapparaissant sur ≥ 3 pages (en-têtes/pieds de page) ;
   - suppression des numéros de page isolés et des mentions de copyright / DOI de bas de page ;
   - la bibliographie sort du corps et part dans `refs.jsonl` ;
   - les légendes de figures et de tableaux sont **conservées** (elles portent souvent les
     chiffres de performance), taguées `figure` / `table` dans `sections.jsonl` ;
   - les équations mal extraites sont conservées telles quelles, sans tentative de
     reconstruction.
5. **Écriture** de `fulltext.md`, `sections.jsonl`, `refs.jsonl`, `metadata.json`, et
   création de `fiche.md` depuis le template de [DATA_MODEL.md](DATA_MODEL.md) avec
   `status.fiche = "todo"`.
6. **Déplacement** du PDF vers `papers/<paper_id>/paper.pdf` (et non copie : `inbox/` doit
   se vider, c'est le signal qu'il ne reste rien à traiter).

Idempotent : un PDF dont le `paper_id` existe déjà est ignoré, sauf `--force` qui réécrit
tout sauf `fiche.md` (le travail de lecture ne doit jamais être écrasé par une
ré-extraction).

### `bin/reindex.py`

Relit tous les `papers/*/metadata.json` et régénère `INDEX.md` : un tableau par axe de
veille, trié par année décroissante, colonnes `id | titre | auteurs | année | venue | type |
fiche`. Ajoute en tête un compteur (`N papiers, M fiches à faire`).

Vérifie aussi la cohérence : tout `paper_id` apparaissant dans `benchmarks.csv` doit exister
dans `papers/`, et signale les fiches `done` qui n'ont aucune ligne de benchmark (souvent le
signe d'un oubli, sauf pour les surveys).

Ne modifie jamais `benchmarks.csv` ni les fiches — il ne fait que lire et régénérer l'index.

### `lib/ids.py`

Construction du `paper_id` (voir [DATA_MODEL.md](DATA_MODEL.md)), slugification, détection
d'un identifiant arXiv dans une chaîne ou une URL.

### `lib/tei.py`

Parsing du TEI GROBID — la brique la plus délicate, à écrire et tester en premier sur un TEI
réel :

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

**Ajouter un article arXiv :**

```bash
.venv/bin/python bin/add.py 2509.04153
```

**Ajouter un article sous paywall** (IEEE, Elsevier, Springer, PMC) — télécharge le PDF via
l'accès de l'université, puis :

```bash
cp ~/Téléchargements/article.pdf inbox/
.venv/bin/python bin/ingest.py
```

**Ficher un article** — dans Claude Code :

```
/paper-fiche arxiv-2507.18174-yolo-edge-fpga
```

L'agent lit `fulltext.md`, remplit `fiche.md` et ajoute les lignes dans `benchmarks.csv`, en
citant la section source de chaque chiffre.

**Après toute modification du corpus :**

```bash
.venv/bin/python bin/reindex.py
```

**Faire le point sur les gaps**, une fois une dizaine de fiches faites :

```
/paper-gaps
```

---

## 7. Amorçage depuis la bibliographie de départ

[basicStart.txt](basicStart.txt) contient une vingtaine d'articles. Neuf portent un
identifiant arXiv et sont donc ingérables sans intervention :

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
plateformes sans API : PDF à récupérer à la main, puis dépôt dans `inbox/`.

⚠️ `basicStart.txt` prévient que ces références ont été collectées à partir de résumés
seulement. **Chaque référence est à vérifier** (titre exact, auteurs, année, venue) au moment
de l'ingestion : GROBID lit le PDF réel, donc un écart entre le TEI et la note de départ est
le signal qu'une référence était approximative.

---

## 8. Vérification

À faire une fois, sérieusement, avant d'ingérer tout le corpus — une erreur d'extraction non
détectée se propage à toutes les fiches.

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

## 9. Extensions, plus tard

- **Graphe de connaissance.** Une fois 15-20 papiers fichés, `/graphify PaperDatabase/papers`
  produit un graphe, des communautés et une vue des liens entre travaux — utile pour nourrir
  `gaps.md`. Inutile avant d'avoir de la matière.
- **Recherche sémantique.** Au-delà de ~200 papiers, si `grep` ne suffit plus, ajouter un
  index local (sentence-transformers + ChromaDB) **par-dessus** `sections.jsonl`, sans rien
  changer à l'arborescence. C'est un ajout, jamais un remplacement.
- **Graphe de citations.** `refs.jsonl` est déjà produit et inutilisé : de quoi repérer les
  articles les plus cités du corpus et les manques évidents dans la bibliographie.
