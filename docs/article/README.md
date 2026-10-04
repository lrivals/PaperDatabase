# Article : PaperDatabase

Article LaTeX qui présente le logiciel : principes, pipeline, couche de recherche (RAG),
apports, tests et évaluation.

- Prérequis : `pdflatex` et `bibtex` (TeX Live avec `babel-french`, `natbib`, `tikz`, `listings`).
- Compiler : `make -C docs/article` → `docs/article/paperdatabase.pdf` (français) et
  `paperdatabase-en.pdf` (anglais). Figures : celles de la base fpga, `bases/fpga/figures/`
  (`bin/pdb plot all` lancé dans `bases/fpga/`). Nettoyer : `make -C docs/article clean`.
- Version du 03/10/2026. Les chiffres viennent des runs `bin/pdb eval` du 03/10/2026 au commit
  3925690 (docs/EVAL.md §9, « Runs des trois bases ») :
  - fpga, 101 articles, 8 601 passages : `bases/fpga/eval/results/2026-10-03T2340-3925690.json`,
    comparé au run de référence du 28/09 sur 45 articles (`2026-09-28T1039-76dc85e.json`) ;
  - drone, 87 articles : `bases/drone/eval/results/2026-10-03T2343-3925690.json` ;
  - stage, 56 articles, extraction seule : `bases/stage/eval/results/2026-10-03T2344-3925690.json`.

  Réponses rédigées (lots A et B) : runs du 02/10, `bases/fpga/eval/results/2026-10-02T1111-353e788-dirty.json`
  et `2026-10-02T1358-c90d749.json` (docs/EVAL.md §10). Délégation : `bin/pdb agents --report`
  et l'expérience appariée de docs/AMELIORATIONS.md, I-6. Comparaison Qwen : docs/EVAL.md §8,
  28 articles, non refaite.
- Pour mettre à jour : `bin/pdb base list` et `bin/pdb status` (corpus), `bin/pdb test` (nombre
  de tests), `bin/pdb eval --save --compare` dans chaque base (section 6), `bin/pdb agents
  --report` (délégation), puis reporter les valeurs dans `paperdatabase.tex` et
  `paperdatabase-en.tex`. Liens vers le lexique et le glossaire : macro `\gl{clé}{texte}`,
  cibles `\hypertarget{gl:clé}` dans les annexes. Détail des mesures : [docs/EVAL.md](../EVAL.md).
- Ne présenter comme livré que ce qui est dans le code : les lots J, K, F et H de
  [docs/AMELIORATIONS.md](../AMELIORATIONS.md) sont spécifiés seulement (section « Limites et
  perspectives »).
- `refs.bib` : références vérifiées sur OpenAlex ; n'y ajouter que des références vérifiées.
