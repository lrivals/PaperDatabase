# PaperDatabase — mode d'emploi

Base de connaissance d'articles scientifiques sur la vision embarquée sur FPGA (YOLO,
autoencodeurs, apprentissage continu), destinée à préparer une thèse.

Structure, scripts et procédure d'installation : [SETUP.md](SETUP.md).
État d'avancement et tâches à faire : [SETUP.md §9](SETUP.md#9-état-actuel-et-tâches-à-faire).
Schémas et conventions : [DATA_MODEL.md](DATA_MODEL.md).

---

## Comment chercher ici

Lis du résumé vers le détail, et arrête-toi dès que tu as la réponse.

1. **[INDEX.md](INDEX.md)** — quels papiers existent, sur quel axe, fichés ou non.
2. **[benchmarks.csv](benchmarks.csv)** — tous les chiffres (FPS, GOPS, W, LUT/DSP/BRAM,
   quantification, toolflow). `grep` dessus pour toute question quantitative. Une ligne par
   configuration rapportée, avec sa section source.
3. **`papers/<id>/fiche.md`** — la lecture critique : problème, méthode, limites, pertinence.
4. **`papers/<id>/fulltext.md`** — le texte intégral, en dernier recours seulement. Pour une
   recherche ciblée dans le corpus entier, `grep` sur `papers/*/sections.jsonl` (chaque ligne
   porte sa section et sa page).
5. **`papers/<id>/paper.pdf`** — ne l'ouvre pas. Il est conservé comme preuve, pas comme
   source de travail ; tout ce qu'il contient est déjà dans `fulltext.md`.

`refs.jsonl` et `grobid.tei.xml` ne servent pas à répondre aux questions : le premier
alimente la visualisation 3D (`bin/viz.py`), le second est la trace brute d'extraction.

---

## Commandes

| Commande | Effet |
|---|---|
| `/paper-add <arxiv-id \| url \| chemin.pdf>` | acquisition + ingestion + réindexation |
| `/paper-fiche <paper_id>` | remplit `fiche.md` et les lignes de `benchmarks.csv` |
| `/paper-gaps` | met à jour `gaps.md` depuis les fiches `done` et `benchmarks.csv` |
| `.venv/bin/python bin/viz.py` | graphe 3D du corpus (app Dash, http://127.0.0.1:8050) : couleur par thème, liens citations / références partagées / similarité TF-IDF / thèmes communs. Dépendances : `requirements-viz.txt`. Détails : [SETUP.md](SETUP.md) §5 |

Après toute modification du corpus (ingestion, fiche remplie, ligne de benchmark ajoutée) :
`.venv/bin/python bin/reindex.py`.

Pour ajouter un article sous paywall, il faut déposer le PDF dans `inbox/` à la main, puis
`.venv/bin/python bin/ingest.py`. Aucun contournement de paywall.

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
papier à l'autre (conditions de mesure, batch size, mesure de puissance puce vs carte),
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
IETR, LAAS, CEA-List…).
