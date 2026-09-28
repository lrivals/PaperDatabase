# PaperDatabase — mode d'emploi

Base de connaissance d'articles scientifiques sur la vision embarquée sur FPGA (YOLO,
autoencodeurs, apprentissage continu), destinée à préparer une thèse. Nom court : `fpga`
(base par défaut du registre) ; thème et périmètre : [profile.md](profile.md).

**Plusieurs bases.** Le dépôt contient une seconde base, `drone` (vision embarquée sur drone :
détection, accélérateurs, co-design système), dans [bases/drone/](bases/drone/), avec son
propre `CLAUDE.md`. Depuis ce dossier, les commandes et les skills agissent sur la base `fpga`
seulement. Ne jamais écrire dans `bases/drone/` depuis ici : pour reprendre un article d'une
base à l'autre, `bin/pdb base import <base>:<paper_id>` lancé dans la base qui le reçoit.
Mode d'emploi multi-bases : [README.md](README.md#plusieurs-bases-de-connaissance),
[DATA_MODEL.md §11](DATA_MODEL.md#11-plusieurs-bases--registre-basejson-profilemd).

Structure, scripts et procédure d'installation : [SETUP.md](SETUP.md).
État d'avancement et tâches à faire : [SETUP.md §9](SETUP.md#9-état-actuel-et-tâches-à-faire).
Schémas et conventions : [DATA_MODEL.md](DATA_MODEL.md).
Guide d'utilisation (pour l'humain) : [docs/GUIDE.md](docs/GUIDE.md).

---

## Comment chercher ici

Lis du résumé vers le détail, et arrête-toi dès que tu as la réponse.

1. **[INDEX.md](INDEX.md)** — quels papiers existent, sur quel axe, fichés ou non. Thème et
   périmètre de la base : [profile.md](profile.md).
2. **[benchmarks.csv](benchmarks.csv)** — tous les chiffres (FPS, GOPS, W, LUT/DSP/BRAM,
   quantification, toolflow). Pour toute question quantitative, interroge-le avec
   `bin/pdb bench` plutôt que de le lire en entier ou de faire un `grep`. Exemple :
   `bin/pdb bench --platform kv260 --has power_w --cols model,fps,power_w`, et `-h` pour
   les filtres. La sortie garde `source_section`, `confidence` et `power_scope`. Une ligne
   par configuration rapportée, avec sa section source.
   Pour l'identité d'un papier (auteurs, venue, preprint ou non, statut de la fiche) :
   `bin/pdb paper <id court | mot du titre>`, sans ouvrir `metadata.json`.
3. **`papers/<id>/fiche.md`** — la lecture critique : problème, méthode, limites, pertinence.
4. **Passages** — `bin/pdb search "<question en anglais>"`, qui renvoie des passages avec
   `chunk_id`, section, page et extrait, puis `bin/pdb show <chunk_id>` sur 2 ou 3 d'entre
   eux. Vérifie chaque citation textuelle avec `bin/pdb verify <chunk_id> "<citation>"`.
   `search` renvoie toujours des passages, même hors sujet : si aucun extrait ne répond,
   dis que la base ne traite probablement pas le sujet (aucun seuil fiable, docs/EVAL.md §5).
   La skill `/paper-ask` enchaîne tout cela ; détails dans [docs/RAG.md](docs/RAG.md).
   `grep` sur `papers/*/sections.jsonl` reste utile pour une chaîne exacte.
   `papers/<id>/fulltext.md`, le texte intégral, en dernier recours seulement.
5. **`papers/<id>/paper.pdf`** — ne l'ouvre pas. Il est conservé comme preuve, pas comme
   source de travail ; tout ce qu'il contient est déjà dans `fulltext.md`.

**Quoi lire ensuite ?** [external_refs.csv](external_refs.csv) (généré) classe les travaux
absents de la base par nombre de papiers du corpus qui les citent. Données issues du parsing
des bibliographies : à vérifier avant de les citer. Au-delà des références, `/paper-discover`
(ou `bin/pdb discover`) produit `candidates.csv` depuis OpenAlex : citations entrantes,
recherche par axe ou par gap (DATA_MODEL §10). Métadonnées OpenAlex, non vérifiées.

`refs.jsonl`, `grobid.tei.xml` et `docling_tables.json` ne servent pas à répondre aux
questions : le premier alimente la visualisation 3D (`bin/viz.py`) et `external_refs.csv`,
les deux autres sont des traces brutes d'extraction. Un tableau dont la légende porte
« reconstruit par PyMuPDF » ou « reconstruit par Docling : à vérifier » n'est pas fiable
chiffre à chiffre ([docs/EVAL.md](docs/EVAL.md) §6).

---

## Commandes

| Commande | Effet |
|---|---|
| `bin/pdb status` | état de la base et prochaines actions suggérées |
| `bin/pdb base list` / `info` / `check` / `new <nom> --theme "…"` | bases enregistrées ; profil et axes de celle-ci ; effet des règles de `base.json` ; création ([DATA_MODEL.md](DATA_MODEL.md) §11) |
| `bin/pdb base scan [--from NOM]` / `base import NOM:<paper_id>` | articles utiles présents ou cités dans mes autres bases → `xbase_candidates.csv` ; copie d'un article (fiche repassée à `todo`) |
| `bin/pdb --base NOM <commande>` | agir sur une autre base que celle du dossier courant |
| `/base-profile [consigne]` | le LLM propose d'affiner le profil (`profile.md`, axes et règles de `base.json`) ; rien n'est écrit sans accord |
| `bin/pdb eval [--extract\|--rag\|--speed] [--save] [--compare]` | banc d'évaluation du logiciel : qualité d'extraction, recherche de passages, `verify`, temps ; à lancer avant/après tout changement du pipeline ([docs/EVAL.md](docs/EVAL.md)) |
| `bin/pdb bench [filtres]` | filtre `benchmarks.csv` sans LLM ; les colonnes de source restent affichées ([docs/RAG.md](docs/RAG.md) §5.1) |
| `bin/pdb search "<q>"`, `show <chunk_id>`, `verify <chunk_id> "<citation>"` | passages sourcés sans LLM, texte exact, contrôle d'une citation ([docs/RAG.md](docs/RAG.md) §5) |
| `/paper-ask <question>` | réponse sourcée et vérifiée : `bench`, puis `search`, `show`, `verify` |
| `bin/pdb paper <id \| mot>…` | fiche d'identité d'un papier : métadonnées, preprint, statut de la fiche, nombre de benchmarks (`--bench` pour les lignes) ; plusieurs ids → une ligne par papier (`--fields short,type`) |
| `bin/pdb cites <id>` / `bin/pdb cited-by <id>` | graphe de citations internes (`--external` : références hors base, avec leur nombre de citants) |
| `/paper-add <arxiv-id \| url \| doi \| chemin.pdf>` | acquisition + ingestion + réindexation (un DOI est résolu vers sa version arXiv via OpenAlex) |
| `/paper-fiche <paper_id>` | remplit `fiche.md` et les lignes de `benchmarks.csv` |
| `/paper-gaps` | met à jour `gaps.md` depuis les fiches `done` et `benchmarks.csv` |
| `/paper-discover [axe \| gap \| mots-clés]` | cherche des candidats (OpenAlex), propose une liste courte, n'ajoute qu'après accord de l'utilisateur |
| `/paper-ask <question>` | recherche hybride et réponse documentée ; peut ajouter automatiquement les articles open access utilisés comme preuve |
| `bin/pdb plot [bench\|eval\|corpus\|all] [--only a,b] [--format png\|pdf]` | figures statiques (PNG par défaut) dans `figures/` : benchmarks (FPS/W, GOPS/W, ressources, précision), évaluation du logiciel, statistiques du corpus et carte des gaps ; sources et effectifs dans `figures/manifest.json` (`requirements-plot.txt`, SETUP.md §5) |
| `.venv/bin/python bin/viz.py` | visualisation du corpus (app Dash, http://127.0.0.1:8050) : graphe 3D (couleur par thème, liens citations / références partagées / similarité textuelle / thèmes communs, recherche, filtres, détail avec fiche et benchmarks) et onglet Généalogie (frise des citations d'un papier ou d'un sujet). Dépendances : `requirements-viz.txt` (+ `requirements-embed.txt`, optionnel). Détails : [SETUP.md](SETUP.md) §5 |

Après toute modification du corpus (fiche remplie, ligne de benchmark ajoutée) :
`.venv/bin/python bin/reindex.py` (régénère `INDEX.md` et `external_refs.csv`) ;
`bin/pdb add` et `bin/pdb ingest` le font d'eux-mêmes.
Si `/paper-ask` utilise l'index de passages, relancer ensuite `bin/pdb rag index` ;
une recherche sur un instantané périmé échoue explicitement.

Pour ajouter un article sous paywall, il faut déposer le PDF dans `inbox/` à la main, puis
`bin/pdb ingest`. Aucun contournement de paywall.

---

## Règles de travail

Reprises de `basicStart.txt`, elles s'appliquent à toute réponse portant sur ce dossier.

**Langue.** Français par défaut. Termes techniques et titres d'articles en anglais.

**Sources.** Ne jamais inventer de référence. Pour chaque article cité : titre, auteurs,
année, venue, lien ou DOI. En cas de doute, le dire et vérifier — la bibliographie de départ
a été constituée à partir de résumés seuls, donc certaines références peuvent être
approximatives.

**Chiffres.** Une valeur non rapportée par les auteurs s'écrit `n/r`, jamais une estimation.
Tout chiffre avancé porte sa section source. Quand `confidence` vaut `low` dans
`benchmarks.csv`, le signaler dans la réponse.

**Lu vs déduit.** Distinguer explicitement ce qui vient du papier de ce qui est une
inférence. Signaler les preprints non relus par les pairs (`type: preprint`).

**Esprit critique.** Relever les comparaisons biaisées, les métriques non comparables d'un
papier à l'autre (conditions de mesure, batch size, mesure de puissance puce vs carte — colonne
`power_scope` de `benchmarks.csv`),
l'absence de code ou de bitstream publiés. Comparer à un baseline GPU / Jetson / MCU quand
c'est pertinent.

**Gaps.** Les zones non couvertes sont la matière première d'une problématique de thèse :
les signaler plutôt que de les combler par des suppositions. Un exemple déjà identifié : les
autoencodeurs sur FPGA sont surtout étudiés sur séries temporelles et physique des
particules, peu sur images.

---

## Format des réponses

- Structurées et concises, tableaux pour toute comparaison.
- Une synthèse d'article suit : problème, méthode, résultats, limites, pertinence pour la
  thèse.
- Terminer par 2-3 pistes concrètes : papier à lire, expérience à reproduire, gap à creuser.

Livrables récurrents attendus : fiche de lecture par article, tableau comparatif, carte des
gaps, brouillon de pré-projet de thèse, liste de labos et d'encadrants (France : LIRMM,
IETR, LAAS, CEA-List…) — tenue dans [labs.md](labs.md).
