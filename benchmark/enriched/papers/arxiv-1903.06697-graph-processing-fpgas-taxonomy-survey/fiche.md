---
id: arxiv-1903.06697-graph-processing-fpgas-taxonomy-survey
fiche: done
date:
---

# Graph Processing on FPGAs: Taxonomy, Survey, Challenges

Maciej Besta, Dimitri Stanojevic, Johannes De Fine Licht, Tal Ben-Nun, Torsten Hoefler, 2019, arXiv preprint. https://arxiv.org/abs/1903.06697
Type : preprint non relu par les pairs

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

## Lecture automatique

Besta et al. (arXiv 1903.06697, 2019) is a survey and taxonomy of graph processing on FPGAs. It runs no experiments of its own. It sorts prior work by: generic framework vs. single-algorithm design; graph problem (BFS, SSSP, CC/WCC, PR, TC/GC, BC, MM, MST, SpMV); programming model (vertex-centric, edge-centric, GAS, BSP, MapReduce, substream-centric, graph virtualization, direct hardware mapping); language (HDL vs. HLS); multi-FPGA scaling; and where the input graph is stored (BRAM, DRAM, SRAM, HMC, or hardwired). It identifies two main bottlenecks: limited DRAM–FPGA bandwidth, which leaves graph workloads memory-bound with many random accesses, and limited on-chip BRAM. Techniques for these include HMC, update combining and edge sorting (FPGP/ForeGraph), graph compression (Lee et al. ExtraV, ratios 1.9–9.36), and partitioning into intervals and shards.

Critical remarks:
(1) All quantitative claims are taken from the cited papers. Examples: Umuroglu et al. use 82% of BRAM for the result vector and cannot go beyond about 2M vertices / 65M edges; GraVF's largest graph is 128k vertices / 512k edges on a Virtex 7; Zhang et al.'s HMC module holds 4GB; Convey HC-1 has 80 GB/s peak bandwidth. None of these are the authors' own measurements. The survey also does not compare throughput (e.g., MTEPS/GTEPS), power, or resource use across designs, so its tables cannot be used to rank performance.
(2) Table 3 compares works mainly by the largest graph each one handled (n, m). This measures scalability, not efficiency.
(3) Coverage ends in early 2019. HBM-based designs and later HLS frameworks are missing.
(4) Extraction problems: no section headings were detected (everything is under '(préambule)'); Table 3 check/cross symbols are garbled (\u0007); and the metadata header's running title ('Towards Understanding of Modern Graph Processing, Storage, and Analytics') differs from the paper title, so it should be checked by hand.

No benchmark rows were added. The passages report no hardware measurements by the survey's own authors. The cited figures from other works (Umuroglu, Zhang, GraVF, Lee) would be misattributed if entered under this paper_id; they should be taken from those original papers instead.
