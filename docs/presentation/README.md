# Présentation : PaperDatabase

Diapositives Beamer (thème metropolis, 16:9, français, 19 pages) pour introduire le projet :
problème, idée, pipeline, navigation en couches, recherche de passages, principes de
fiabilité, skills, plusieurs bases, visualisation, évaluation, limites, démarrage rapide.

- Prérequis : `pdflatex` (TeX Live avec `beamer`, `beamertheme-metropolis`, `babel-french`,
  `tikz`, `listings`).
- Compiler : `make -C docs/presentation` → `docs/presentation/paperdatabase-slides.pdf`.
  Nettoyer : `make -C docs/presentation clean`.
- Images : `docs/images/viz-scan.png` (capture de l'interface) et
  `bases/fpga/figures/bench_fps_power.png` (`bin/pdb plot all` lancé dans `bases/fpga/`).
- Version du 18/10/2026. Chiffres repris du [README](../../README.md) : effectifs des bases au
  18/10/2026, résultats de `bin/pdb eval` ([docs/EVAL.md](../EVAL.md)), nombre de tests.
  La sortie de `pdb search` (diapositive « Exemple ») est réelle ; la réponse `/paper-ask`
  qui la suit est abrégée, à titre d'illustration.
- Pour mettre à jour : `bin/pdb base list` (effectifs), `bin/pdb test`, puis reporter les
  valeurs dans `paperdatabase-slides.tex`. Ne présenter comme livré que ce qui est dans le code.
