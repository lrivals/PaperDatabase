# PaperDatabase — modèle de données

Contrat de données de la base. Toute modification de schéma se répercute dans
`lib/schema.py`, qui est le seul endroit où il est codé. `bin/reindex.py` vérifie chaque
fichier décrit ici (forme du `paper_id`, `metadata.json`, front-matter de `fulltext.md` et
`fiche.md`, chaque ligne de `sections.jsonl`, `refs.jsonl` et `benchmarks.csv`) et sort en
erreur au premier écart.

Convention qui prime sur toutes les autres : **une valeur non rapportée par les auteurs
s'écrit `n/r`**. Jamais une estimation, jamais une valeur reprise d'un autre papier, jamais
un blanc ambigu. C'est la traduction opérationnelle de la règle « ne jamais inventer ».

---

## 1. `paper_id`

Identifiant stable, lisible et triable, utilisé comme nom de dossier et comme clé dans
`benchmarks.csv`.

| Cas | Forme | Exemple |
|---|---|---|
| Article arXiv | `arxiv-<id>-<slug-titre-court>` | `arxiv-2507.18174-yolo-edge-fpga` |
| Autre | `<annee>-<premier-auteur>-<slug-titre-court>` | `2025-kim-yolov2-zynq7000` |
| Mesure propre | `own-<annee>-<slug-du-protocole>` | `own-2026-kv260-map-sur-cible` |

Le slug fait 3 à 5 mots, en minuscules, sans accents, mots vides retirés. Il est là pour la
lisibilité humaine : c'est l'`id` arXiv ou le couple auteur-année qui porte l'unicité.

Un `paper_id` ne change jamais une fois créé — il est référencé depuis `benchmarks.csv`,
`INDEX.md` et les fiches.

**Mesures propres.** Un id `own-…` n'existe que dans `benchmarks.csv` : il n'a jamais de
dossier `papers/`. Sa source est le protocole `docs/experiences/<slug-du-protocole>.md`,
complété des résultats, et `reindex.py` refuse une ligne dont le protocole manque.
`source_section` désigne la section de ce protocole. `INDEX.md` les liste sous « Mesures
propres » ; `bin/pdb bench --own` (ou `--no-own`) les isole de la littérature.

---

## 2. `metadata.json`

Un fichier par article, à la racine de `papers/<paper_id>/`.

```json
{
  "id": "arxiv-2507.18174-yolo-edge-fpga",
  "title": "Real-Time Object Detection and Classification using YOLO for Edge FPGAs",
  "authors": [
    {"given": "Rashed Al", "family": "Amin"},
    {"given": "Roman", "family": "Obermaisser"}
  ],
  "year": 2025,
  "venue": "arXiv preprint",
  "doi": null,
  "arxiv_id": "2507.18174",
  "url": "https://arxiv.org/abs/2507.18174",
  "type": "preprint",
  "axes": ["yolo-fpga", "surveys"],
  "tags": ["yolov8", "satay", "quantization"],
  "added": "2026-09-21",
  "extraction": {
    "backend": "grobid",
    "ok": true,
    "warnings": []
  },
  "status": {
    "extracted": true,
    "fiche": "todo"
  }
}
```

| Champ | Type | Notes |
|---|---|---|
| `id` | string | = nom du dossier |
| `title` | string | tel qu'imprimé sur le PDF |
| `authors` | array | `{given, family}`, dans l'ordre du papier |
| `year` | int \| null | année de publication ; pour arXiv, année de la v1 |
| `venue` | string \| null | journal, conférence, ou `"arXiv preprint"` |
| `doi` | string \| null | sans préfixe URL |
| `arxiv_id` | string \| null | |
| `url` | string \| null | lien canonique |
| `type` | enum | `preprint` \| `journal` \| `conference` \| `thesis` \| `repo` |
| `axes` | array | voir §3 ; plusieurs valeurs possibles |
| `tags` | array | libre : modèles, plateformes, toolflows cités |
| `added` | date ISO | date d'ingestion |
| `extraction.backend` | enum | `grobid` \| `pymupdf` |
| `extraction.ok` | bool | false si l'extraction a produit un résultat douteux |
| `extraction.warnings` | array | messages destinés à la relecture humaine |
| `status.extracted` | bool | |
| `status.fiche` | enum | `todo` \| `done` |

Un champ inconnu vaut `null`, jamais une chaîne vide ni une valeur devinée.

Quand un export de citation éditeur a été déposé avec le PDF, il est conservé à côté, dans
`citation.bib` ou `citation.ris` : c'est la source de `title`, `authors`, `year`, `venue`,
`doi` et `type` (SETUP.md §5, `ingest.py`). En cas d'écart avec `metadata.json`, l'export
fait foi, sauf correction manuelle ultérieure.

---

## 3. Axes de veille

Repris de `basicStart.txt`. Valeurs fermées — en ajouter une demande de mettre à jour
`lib/schema.py` et `reindex.py`.

| Axe | Contenu |
|---|---|
| `surveys` | surveys et toolflows généraux |
| `yolo-fpga` | détection YOLO v3→v11 et variantes tiny sur FPGA |
| `autoencoder-fpga` | CAE/VAE : compression, détection d'anomalies |
| `continual-learning` | apprentissage incrémental / continu embarqué (SLDA, replay, HDC) |
| `toolflows` | hls4ml, FINN, Vitis AI, Intel FPGA AI Suite, SATAY |
| `platforms` | Zynq, Kria, ZCU102/104, PYNQ, Versal ; comparaisons MCU/NPU/GPU |

---

## 4. `fulltext.md`

Front-matter YAML minimal, puis le corps en sections.

```markdown
---
id: arxiv-2507.18174-yolo-edge-fpga
title: Real-Time Object Detection and Classification using YOLO for Edge FPGAs
year: 2025
backend: grobid
---

## Abstract

...

## 1. Introduction

...

### 1.1 Motivation

...

## 3. Experimental Results

...

**Table 2.** Comparison of FPGA-based YOLO accelerators ...
```

Règles : la numérotation d'origine des sections est conservée (elle sert de référence dans
les fiches) ; les légendes de figures et de tableaux sont gardées en gras ; la bibliographie
n'y figure pas.

Les niveaux de titre suivent la numérotation : `##` pour une section, `###` pour une
sous-section, `####` au-delà (par exemple `1.` sous `IV.B` dans un papier numéroté en
chiffres romains). Les titres parasites produits par l'extracteur (cellule de tableau,
symbole isolé, année, mesure comme `13.9x`) sont rendus comme de simples paragraphes. Quand
des numéros de section manquent dans la séquence, c'est que l'extracteur n'a pas détecté
leur titre : leur texte est rattaché à la section précédente, et `extraction.warnings` le
signale (« sections numérotées non détectées : … »).

---

## 5. `sections.jsonl`

Une ligne JSON par section ou sous-section, dans l'ordre du papier.

```json
{"id": "arxiv-2507.18174-yolo-edge-fpga#012", "paper_id": "arxiv-2507.18174-yolo-edge-fpga", "kind": "section", "section": "3. Experimental Results", "subsection": null, "order": 12, "page": 7, "text": "..."}
```

| Champ | Notes |
|---|---|
| `id` | `<paper_id>#<order sur 3 chiffres>` |
| `kind` | `abstract` \| `section` \| `figure` \| `table` |
| `section` | titre de la section de rattachement, numérotation comprise |
| `subsection` | titre de sous-section, ou `null` |
| `order` | position dans le papier, à partir de 0 |
| `page` | page du PDF, pour retrouver le passage à l'œil |
| `text` | texte nettoyé |

Une section dépassant ~6000 caractères est découpée en plusieurs lignes qui partagent le
même `section` — le découpage suit les paragraphes, jamais un compte de tokens aveugle.

---

## 6. `refs.jsonl`

Une ligne par référence citée. Non chargé par l'agent pour répondre aux questions ; lu par
`lib/refs.py`, qui alimente la visualisation 3D (`bin/viz.py`) et `external_refs.csv` (§9).

```json
{"paper_id": "arxiv-2507.18174-yolo-edge-fpga", "raw": "[12] J. Redmon and A. Farhadi, ...", "title": "YOLOv3: An Incremental Improvement", "authors": ["Redmon", "Farhadi"], "year": 2018, "doi": null, "arxiv_id": "1804.02767"}
```

Rapprochement d'une référence avec un papier (`lib/refs.ref_keys`) : une référence et un
`metadata.json` produisent chacun des clés normalisées, comparées dans cet ordre :

| Clé | Normalisation |
|---|---|
| `arxiv:<id>` | minuscules, suffixe de version (`v2`) retiré |
| `doi:<doi>` | minuscules |
| `title:<slug>` | titre slugifié (sans accents, ponctuation ni casse) ; ignoré sous 4 mots |

Deux références qui partagent une clé désignent le même travail. À défaut de clé commune,
deux titres quasi identiques (ligature perdue — « E cient » pour « Efficient » —, coquille,
titre tronqué d'au moins 6 mots) désignent aussi le même travail, si leurs années diffèrent
d'au plus un an (`lib/refs.same_title`, ratio `SequenceMatcher` ≥ 0,92). Deux publications
aux titres réellement différents (fpgaConvNet FCCM 2016 et TNNLS 2019) restent distinctes.
Une référence qui ne produit aucune clé (ni identifiant ni titre exploitable) est ignorée.

---

## 7. `benchmarks.csv`

Le tableau comparatif, à la racine de `PaperDatabase/`. **Une ligne par configuration
rapportée** : un papier qui présente trois variantes (INT8, INT4, pruned) produit trois
lignes.

Colonnes, dans cet ordre :

| Colonne | Exemple | Notes |
|---|---|---|
| `paper_id` | `2025-kim-yolov2-zynq7000` | ou `own-<annee>-<slug>` pour une mesure propre (§1) |
| `model` | `YOLOv2` | tel que nommé par les auteurs |
| `task` | `object detection` | `detection` \| `classification` \| `anomaly detection` \| ... |
| `platform` | `Zynq-7000 XC7Z020` | référence exacte de la puce, pas seulement la famille |
| `quantization` | `INT8 W / INT5 A` | poids et activations séparés si différents |
| `accuracy_metric` | `mAP@0.5` | |
| `accuracy_value` | `79.0` | en %, sans unité |
| `fps` | `55` | |
| `gops` | `808.6` | |
| `latency_ms` | `n/r` | |
| `power_w` | `2.13` | en W, telle que rapportée ; sa portée va dans `power_scope` |
| `power_scope` | `board` | portée de `power_w` : `chip` (rails de la puce : PMBus, télémétrie) \| `board` (carte entière, wattmètre) \| `board-dynamic` (carte, puissance de repos soustraite) \| `estimated` (outil ou modèle, pas une mesure) \| `unspecified` (mesure dont la portée n'est pas dite) ; `n/r` si et seulement si `power_w` vaut `n/r` |
| `luts` | `41200` | |
| `dsps` | `220` | |
| `bram` | `140` | en blocs, pas en Mo |
| `dataset` | `COCO` | |
| `toolflow` | `Vitis AI` | `hls4ml` \| `FINN` \| `Vitis AI` \| `SATAY` \| `custom HLS` \| `custom RTL` |
| `baseline` | `RTX 2080Ti, GTX 1650` | comparaisons données par le papier, `n/r` si aucune |
| `source_section` | `Table 4` | d'où vient la ligne : section, tableau ou figure |
| `confidence` | `high` | `high` = lu dans un tableau ; `medium` = dans le texte ; `low` = déduit, à revérifier |

Deux puissances de portées différentes ne se comparent pas : une carte ZC706 consomme ~7 W au
repos (arxiv-1612.07119, §5.2.2), qu'une mesure `board` inclut et qu'une mesure `chip` ou
`board-dynamic` exclut. Quand un papier donne plusieurs portées (P_chip et P_wall), `power_w`
prend la mesure `board` et la fiche donne les autres.

`source_section` et `confidence` ne sont pas décoratifs : ils permettent de rouvrir le bon
passage en cas de doute et de repérer d'un coup d'œil les chiffres fragiles.

---

## 8. Template de `fiche.md`

Généré par `ingest.py` avec les champs vides, rempli par `/paper-fiche`.

```markdown
---
id: <paper_id>
fiche: todo
date: <date de rédaction>
---

# <Titre>

<Auteurs>, <année>, <venue>. <DOI ou URL>
Type : <preprint non relu par les pairs | article de journal | conférence>

## Problème

Quel verrou le papier attaque-t-il, tel que les auteurs le posent.

## Méthode

Architecture, quantification, stratégie de mapping sur le FPGA, post-traitement (NMS…).
Toolflow employé.

## Plateforme et implémentation

Puce exacte, fréquence, ressources consommées, mémoire. Code ou bitstream publiés ? Où ?

## Résultats

Les chiffres, avec la section ou le tableau source. Baseline de comparaison.
→ reportés dans `benchmarks.csv` : <lignes ajoutées>

## Limites et critique

Comparaisons biaisées, métriques non comparables d'un papier à l'autre, conditions de mesure
non précisées, absence de reproductibilité. Ce que le papier ne mesure pas.

## Pertinence pour la thèse

Ce que ce travail apporte à l'axe visé, et ce qu'il laisse ouvert.

## Gaps identifiés

Points à reporter dans `gaps.md`.

## Statut de lecture

Résumé seul | sections lues : <liste> | papier complet.
Ce qui suit est déduit et non affirmé par les auteurs : <…>
```

La section **Statut de lecture** est obligatoire : elle matérialise la distinction entre ce
qui a été lu et ce qui a été déduit, et empêche une fiche partielle de passer pour une
lecture complète.

Clé de front-matter facultative `benchmarks: none` : la fiche est `done` et le papier n'a
volontairement aucune ligne dans `benchmarks.csv` (ratios seulement, chiffres absents du
texte extrait…) ; la justification reste dans la section « Résultats ». `reindex.py` ne
signale alors plus « fiche done sans ligne », mais signale une fiche marquée `none` qui a
des lignes. Les surveys (axe `surveys`) n'en ont pas besoin.

---

## 9. `external_refs.csv`

**Généré par `bin/reindex.py` — ne pas éditer à la main.** Travaux absents de la base
cités par au moins deux papiers du corpus, du plus cité au moins cité (puis du plus récent
au plus ancien) : c'est la liste des lectures candidates à ajouter via `/paper-add`.

| Colonne | Contenu |
|---|---|
| `rank` | rang (1 = le plus cité) |
| `n_citers` | nombre de papiers du corpus qui le citent |
| `title` | titre le moins abîmé parmi les variantes rencontrées dans les `refs.jsonl` |
| `year` | année de la première référence qui la donne, sinon `n/r` |
| `arxiv_id`, `doi` | identifiants trouvés dans les références, sinon `n/r` |
| `citers` | `paper_id` citants, séparés par `;` |

Les données viennent du parsing GROBID des bibliographies : titre, année et identifiants sont
à vérifier au moment de l'ajout, jamais cités tels quels.

---

## 10. `candidates.csv` et `candidates_arxiv.txt`

**Générés par `bin/discover.py` (`bin/pdb discover`) — ne pas éditer à la main, non
versionnés.** Candidats à l'ajout trouvés via OpenAlex, papiers déjà en base exclus, triés
« dans le sujet » d'abord puis par score décroissant.

| Colonne | Contenu |
|---|---|
| `rank` | rang |
| `score` | 3 × liens de citation avec le corpus + liens « related » + 2 si trouvé par requête + 2 × axes probables + log10(citations + 1) |
| `in_topic` | `oui` si le candidat relève d'un axe de `ingest.HARDWARE_AXES`, si son titre correspond à `ingest.TITLE_TOPIC_RE` (FPGA, accélérateur, TinyML, MCU, edge computing…), ou si titre + résumé mentionnent au moins deux fois `ingest.TOPIC_RE` ; une mention isolée dans le résumé (SqueezeNet) ou un axe thématique seul (autoencodeur, YOLO logiciel) ne suffit pas |
| `reasons` | lien avec le corpus : `cite N papier(s) du corpus`, `cité par N papiers du corpus`, `lié à N papier(s) du corpus (OpenAlex)`, requête ou axe, séparés par ` ; ` |
| `title`, `year`, `venue` | d'après OpenAlex (versions arXiv et éditeur fusionnées ; la venue éditeur prime) |
| `doi` | DOI éditeur (jamais le DOI arXiv 10.48550), sinon `n/r` |
| `arxiv_id` | identifiant arXiv d'une des versions, sinon `n/r` |
| `oa_url` | lien open access légal signalé par OpenAlex, sinon `n/r` |
| `cited_by_count` | citations selon OpenAlex |
| `axes_guess` | axes devinés par `ingest.classify`, séparés par `;` |
| `openalex_id` | identifiant OpenAlex (`W…`) |

`candidates_arxiv.txt` : les premiers candidats `in_topic = oui` disponibles sur arXiv, un
par ligne (`<arxiv_id>  # titre (année) — raisons`), lisible par `bin/pdb add --from`.

Métadonnées OpenAlex : à vérifier au moment de l'ajout, jamais citées telles quelles.

