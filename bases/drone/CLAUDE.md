# Vision embarquée sur drone (base `drone`) — mode d'emploi

Base de connaissance d'articles scientifiques sur la vision embarquée sur drone : détection
(YOLO, petits objets), accélérateurs embarqués (FPGA, MCU/nano-drone, ASIC, neuromorphique),
co-design calcul ↔ énergie ↔ vol et fiabilité. Destinée à préparer une thèse. Nom court
dans le registre : `drone` (anciennement `DroneVisionDB`). Thème, périmètre et règles
(sol → air / air → air, vol agile…) : [profile.md](profile.md), qui fait foi.

**Base distincte** de la base « vision embarquée sur FPGA » (`../fpga/`),
dont elle partage le code et le dépôt git : elle vit dans `bases/drone/`, et `bin/`, `.venv`,
`.claude/commands/` sont des liens vers la racine du dépôt (le code). La base active est détectée par le fichier
`base.json` de ce dossier (axes, règles de classement ; `../../DATA_MODEL.md` §11). Ne jamais
écrire dans la base fpga depuis ici : pour en reprendre un article, `bin/pdb base import fpga:<id>`.
Quelques papiers y ont été copiés (DAC-SDC, SATAY, FINN…) : les deux copies évoluent
séparément.

État de l'art de départ (résumés seuls, non vérifié) : [docs/etat-de-l-art.md](docs/etat-de-l-art.md).

Structure, scripts et procédure d'installation (code partagé) : [SETUP.md](../../SETUP.md).
Schémas et conventions : [DATA_MODEL.md](../../DATA_MODEL.md).
Guide d'utilisation (pour l'humain) : [docs/GUIDE.md](../../docs/GUIDE.md).

---

## Comment chercher ici

Lis du résumé vers le détail, et arrête-toi dès que tu as la réponse.

1. **[INDEX.md](INDEX.md)** — quels papiers existent, sur quel axe, fichés ou non. Le
   périmètre (ce qui est inclus, exclu, et le statut des papiers `ground-to-air`) est dans
   [profile.md](profile.md).
2. **[benchmarks.csv](benchmarks.csv)** — tous les chiffres (FPS, GOPS, W, LUT/DSP/BRAM,
   quantification, toolflow). Pour toute question quantitative, interroge-le avec
   `bin/pdb bench` plutôt que de le lire en entier ou de faire un `grep`. Exemple :
   `bin/pdb bench --platform ultra96 --has power_w --cols model,fps,power_w`, et `-h` pour
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
   La skill `/paper-ask` enchaîne tout cela ; détails dans [docs/RAG.md](../../docs/RAG.md).
   `grep` sur `papers/*/sections.jsonl` reste utile pour une chaîne exacte.
   `papers/<id>/fulltext.md`, le texte intégral, en dernier recours seulement.
5. **`papers/<id>/paper.pdf`** — ne l'ouvre pas. Il est conservé comme preuve, pas comme
   source de travail ; tout ce qu'il contient est déjà dans `fulltext.md`.

**Quoi lire ensuite ?** D'abord la base `fpga` : `bin/pdb base scan --from fpga` classe ses
articles déjà cités ici, ou correspondant aux règles d'ici ; `bin/pdb base import fpga:<id>`
les copie. Puis [external_refs.csv](external_refs.csv) (généré) classe les travaux
absents de la base par nombre de papiers du corpus qui les citent. Données issues du parsing
des bibliographies : à vérifier avant de les citer. Au-delà des références, `/paper-discover`
(ou `bin/pdb discover`) produit `candidates.csv` depuis OpenAlex : citations entrantes,
recherche par axe ou par gap (DATA_MODEL §10). Métadonnées OpenAlex, non vérifiées.

`refs.jsonl`, `grobid.tei.xml` et `docling_tables.json` ne servent pas à répondre aux
questions : le premier alimente la visualisation 3D (`bin/viz.py`) et `external_refs.csv`,
les deux autres sont des traces brutes d'extraction. Un tableau dont la légende porte
« reconstruit par PyMuPDF » ou « reconstruit par Docling : à vérifier » n'est pas fiable
chiffre à chiffre ([docs/EVAL.md](../../docs/EVAL.md) §6).

---

## Commandes

| Commande | Effet |
|---|---|
| `bin/pdb status` | état de la base et prochaines actions suggérées |
| `bin/pdb base list` / `info` / `check` | bases enregistrées ; profil, axes et suggestions en attente de celle-ci ; effet des règles de `base.json` |
| `bin/pdb base scan [--from fpga]` / `base import fpga:<paper_id>` | articles utiles présents ou cités dans la base fpga → `xbase_candidates.csv` ; copie d'un article (fiche repassée à `todo`) |
| `/base-profile [consigne]` | le LLM propose d'affiner `profile.md` et `base.json` ; rien n'est écrit sans accord |
| `bin/pdb bench [filtres]` | filtre `benchmarks.csv` sans LLM ; les colonnes de source restent affichées ([docs/RAG.md](../../docs/RAG.md) §5.1) |
| `bin/pdb search "<q>"`, `show <chunk_id>`, `verify <chunk_id> "<citation>"` | passages sourcés sans LLM, texte exact, contrôle d'une citation ([docs/RAG.md](../../docs/RAG.md) §5) |
| `/paper-ask <question>` | réponse sourcée et vérifiée : `bench`, puis `search`, `show`, `verify` |
| `bin/pdb paper <id \| mot>…` | fiche d'identité d'un papier : métadonnées, preprint, statut de la fiche, nombre de benchmarks (`--bench` pour les lignes) ; plusieurs ids → une ligne par papier (`--fields short,type`) |
| `bin/pdb cites <id>` / `bin/pdb cited-by <id>` | graphe de citations internes (`--external` : références hors base, avec leur nombre de citants) |
| `/paper-add <arxiv-id \| url \| doi \| chemin.pdf>` | acquisition + ingestion + réindexation (un DOI est résolu vers sa version arXiv via OpenAlex) |
| `/paper-fiche <paper_id>` | remplit `fiche.md` et les lignes de `benchmarks.csv` |
| `/paper-gaps` | met à jour `gaps.md` depuis les fiches `done` et `benchmarks.csv` |
| `/paper-discover [axe \| gap \| mots-clés]` | cherche des candidats (base fpga d'abord, puis OpenAlex), propose une liste courte, n'ajoute qu'après accord de l'utilisateur |
| `/paper-research <question>` | **route GPU, sur demande seulement** (Qwen3, GPU CUDA, `bin/pdb gpu`) : recherche `bin/pdb rag` et acquisition d'articles open access, importés seulement après accord ; sans GPU, utiliser `/paper-ask` |
| `bin/pdb eval [--extract\|--rag\|--speed] [--save] [--compare]` | banc d'évaluation sur cette base : extraction, recherche de passages avec les questions de `eval/fixtures/`, `verify`, temps ; runs dans `eval/results/` ([docs/EVAL.md §9](../../docs/EVAL.md#9-banc-par-base)) |
| `bin/pdb plot [bench\|eval\|corpus\|all] [--only a,b] [--format png\|pdf]` | figures statiques (PNG par défaut) dans `figures/` : benchmarks (FPS/W, GOPS/W, ressources, précision), évaluation du logiciel, statistiques du corpus et carte des gaps ; sources et effectifs dans `figures/manifest.json` (`requirements-plot.txt`, SETUP.md §5) |
| `bin/pdb viz` (depuis ce dossier) | interface Plotly / Dash (http://127.0.0.1:8050), ouverte sur cette base, avec un sélecteur de base : graphe 3D (couleur par thème, liens citations / références partagées / similarité textuelle / thèmes communs, recherche, filtres, détail avec fiche et benchmarks), onglet Généalogie (frise des citations d'un papier ou d'un sujet) et onglet Bases (tableau des bases, profil, recherche dans la base fpga avec import, création d'une base). Dépendances : `requirements-viz.txt` (+ `requirements-embed.txt`, optionnel). Détails : [SETUP.md](../../SETUP.md) §5 |

Après toute modification du corpus (fiche remplie, ligne de benchmark ajoutée) :
`.venv/bin/python bin/reindex.py` (régénère `INDEX.md` et `external_refs.csv`) ;
`bin/pdb add` et `bin/pdb ingest` le font d'eux-mêmes.
`reindex` met aussi à jour l'index de passages de `pdb search` (et, si la route GPU est
active, les vecteurs Qwen et l'index de `pdb rag` : [docs/RAG.md §13](../../docs/RAG.md#13-route-gpu-optionnelle-qwen3)).

Pour ajouter un article sous paywall, il faut déposer le PDF dans `inbox/` à la main, puis
`bin/pdb ingest`. Aucun contournement de paywall.

---

## Règles de travail

Reprises de la base fpga (`../fpga/CLAUDE.md`), elles s'appliquent à toute réponse portant sur ce dossier.

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
c'est pertinent. Propre au drone : IoU mono-objet (DAC-SDC) ≠ mAP multi-classe (VisDrone) ;
FPS sans puissance mesurée à la carte ; résultats sur GPU de bureau présentés comme
« embarqués ». Toujours préciser la **gamme de puissance** d'un résultat : nano (GAP8, mW),
FPGA (W), Jetson (~10 W, par exemple les travaux de Zurich, Loquercio et Kaufmann). En
contre-drone, distinguer **sol → air** (capteur fixe au sol) et **air → air** (détecteur
embarqué sur un drone intercepteur) : seul le second relève de l'IA embarquée.

**Gaps.** Les zones non couvertes sont la matière première d'une problématique de thèse :
les signaler plutôt que de les combler par des suppositions. Hypothèses de départ, à étayer
(gaps.md) : les YOLO drone SOTA (tête P2, Transformer) ne sont presque jamais portés sur FPGA ;
l'effet de la quantification sur le mAP_small n'est pas mesuré ; aucune métrique système
(autonomie, vitesse de vol sûre) dans les papiers YOLO/FPGA.

---

## Format des réponses

- Structurées et concises, tableaux pour toute comparaison.
- Une synthèse d'article suit : problème, méthode, résultats, limites, pertinence pour la
  thèse.
- Terminer par 2-3 pistes concrètes : papier à lire, expérience à reproduire, gap à creuser.

Livrables récurrents attendus : fiche de lecture par article, tableau comparatif, carte des
gaps, brouillon de pré-projet de thèse, liste de labos et d'encadrants (France : LIRMM,
IETR, LAAS, CEA-List, ONERA, ISAE-SUPAERO…) — tenue dans [labs.md](labs.md).
