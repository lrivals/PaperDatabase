# Article : PaperDatabase

Article LaTeX qui présente le logiciel : principes, pipeline, couche de recherche (RAG),
apports, tests et évaluation.

- Prérequis : `pdflatex` et `bibtex` (TeX Live avec `babel-french`, `natbib`, `tikz`, `listings`).
- Compiler : `make -C docs/article` → `docs/article/paperdatabase.pdf` (français) et
  `paperdatabase-en.pdf` (anglais). Figures : `figures/` (`bin/pdb plot all`). Nettoyer : `make -C docs/article clean`.
- Les chiffres sont ceux du 26/09/2026 (run complet de `bin/pdb eval` sur 45 articles, 3 479 passages :
  `eval/results/2026-09-26T2044-65074b7.json` ; comparaison Qwen : docs/EVAL.md §8, 28 articles). Pour
  les mettre à jour : `bin/pdb status` (corpus), `bin/pdb test` (nombre de tests),
  `bin/pdb eval` (section 6 : extraction, recherche, hors corpus, `verify`, temps), puis
  reporter les valeurs dans `paperdatabase.tex` et `paperdatabase-en.tex`. Liens vers le lexique
  et le glossaire : macro `\gl{clé}{texte}`, cibles `\hypertarget{gl:clé}` dans les annexes. Détail des mesures : [docs/EVAL.md](../EVAL.md).
- `refs.bib` : références vérifiées sur OpenAlex ; n'y ajouter que des références vérifiées.
