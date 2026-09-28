# Article : PaperDatabase

Article LaTeX qui présente le logiciel : principes, pipeline, couche de recherche (RAG),
apports, tests et évaluation.

- Prérequis : `pdflatex` et `bibtex` (TeX Live avec `babel-french`, `natbib`, `tikz`, `listings`).
- Compiler : `make -C docs/article` → `docs/article/paperdatabase.pdf` (français) et
  `paperdatabase-en.pdf` (anglais). Figures : celles de la base fpga, `bases/fpga/figures/`
  (`bin/pdb plot all` lancé dans `bases/fpga/`). Nettoyer : `make -C docs/article clean`.
- Les chiffres de la base fpga sont ceux du run `bin/pdb eval` du 26/09/2026 (45 articles,
  3 479 passages : `bases/fpga/eval/results/2026-09-26T2044-65074b7.json`), reproduits à
  l'identique le 28/09 (`2026-09-28T1039-76dc85e`, d'où viennent les temps). Base drone
  (section « Un second corpus ») : `bases/drone/eval/results/2026-09-28T1043-76dc85e.json`.
  Comparaison Qwen : docs/EVAL.md §8, 28 articles. Pour les mettre à jour :
  `bin/pdb base list` (corpus des deux bases), `bin/pdb test` (nombre de tests),
  `bin/pdb eval` dans chaque base (section 6 : extraction, recherche, hors corpus, `verify`,
  temps ; comparaison des bases : docs/EVAL.md §9), puis reporter les valeurs dans
  `paperdatabase.tex` et `paperdatabase-en.tex`. Liens vers le lexique
  et le glossaire : macro `\gl{clé}{texte}`, cibles `\hypertarget{gl:clé}` dans les annexes. Détail des mesures : [docs/EVAL.md](../EVAL.md).
- `refs.bib` : références vérifiées sur OpenAlex ; n'y ajouter que des références vérifiées.
