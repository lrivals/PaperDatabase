# PaperDatabase — dépôt du code

Outil générique qui transforme des PDF d'articles scientifiques en base de connaissance
interrogeable par un LLM (fiches, benchmarks, passages sourcés). La racine du dépôt contient
le code seul : `bin/`, `lib/`, `tests/`, `templates/`, `.claude/commands/` (skills) et la
documentation du logiciel. Les données vivent dans des bases, une par dossier :

| Base | Dossier | Thème |
|---|---|---|
| `fpga` (défaut du registre) | [bases/fpga/](bases/fpga/) | vision embarquée sur FPGA (YOLO, autoencodeurs, apprentissage continu) |
| `drone` | [bases/drone/](bases/drone/) | vision embarquée sur drone (détection, accélérateurs, co-design système) |

**Travailler sur une base.** Chaque base a son propre `CLAUDE.md` (mode d'emploi, règles de
travail, format des réponses) : le lire avant toute question sur le corpus, et de préférence
ouvrir la session dans `bases/<nom>/`. Les commandes (`bin/pdb …`) et les skills
(`/paper-ask`, `/paper-fiche`…) agissent sur la base du dossier courant (fichier `base.json`
trouvé en remontant) ; depuis la racine, sur la base par défaut du registre
(`~/.config/pdb/bases.json`), ou sur celle désignée par `bin/pdb --base <nom> …`.
Ne jamais écrire dans une base depuis une autre : `bin/pdb base import <base>:<paper_id>`,
lancé dans la base qui reçoit. Détails : [README.md](README.md#plusieurs-bases-de-connaissance),
[DATA_MODEL.md §11](DATA_MODEL.md#11-plusieurs-bases--registre-basejson-profilemd).

**Travailler sur le code.** Structure, scripts et installation : [SETUP.md](SETUP.md) ; état
d'avancement : [SETUP.md §9](SETUP.md#9-état-actuel-et-tâches-à-faire) ; schémas et
conventions : [DATA_MODEL.md](DATA_MODEL.md) ; guide d'utilisation : [docs/GUIDE.md](docs/GUIDE.md).
Tests : `bin/pdb test`. Avant/après tout changement du pipeline : `bin/pdb eval --compare`
([docs/EVAL.md](docs/EVAL.md)). Une base neuve : `bin/pdb base new <nom> --theme "…"`
(créée sous `bases/<nom>/`).

**Langue.** Français par défaut. Termes techniques et titres d'articles en anglais.
