# Article : PaperDatabase

Article LaTeX qui présente le logiciel : principes, pipeline, couche de recherche (RAG),
apports, tests et évaluation.

- Prérequis : `pdflatex` et `bibtex` (TeX Live avec `babel-french`, `natbib`, `tikz`, `listings`).
- Compiler : `make -C docs/article` → `docs/article/paperdatabase.pdf`. Nettoyer : `make -C docs/article clean`.
- Les chiffres sont ceux du 26/09/2026 (run complet de `bin/pdb eval`, 2 414 passages). Pour
  les mettre à jour : `bin/pdb status` (corpus), `bin/pdb test` (nombre de tests),
  `bin/pdb eval` (section 6 : extraction, recherche, hors corpus, `verify`, temps), puis
  reporter les valeurs dans `paperdatabase.tex`. Détail des mesures : [docs/EVAL.md](../EVAL.md).
- `refs.bib` : références vérifiées sur OpenAlex ; n'y ajouter que des références vérifiées.
