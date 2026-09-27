---
id: arxiv-1901.04986-systimator-design-space-exploration-methodology
fiche: done
date:
---

# Systimator: A Design Space Exploration Methodology for Systolic Array based CNNs Acceleration on the FPGA-based Edge Nodes

Hazoor Ahmad, Muhammad Tanvir, Muhammad Abdullah Hanif, Muhammad Usama Javed, Rehan Hafiz, Muhammad Shafique, 2018, arXiv preprint. https://arxiv.org/abs/1901.04986
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

Systimator (Ahmad et al., arXiv 1901.04986) is an analytical design space exploration method for systolic-array CNN accelerators on low-cost, memory-limited FPGAs. It models a generic architecture: an IFM buffer, a weight buffer, scratchpad rows, the systolic array, an accumulation block and a pooling/activation block. It supports two data traversal orders, feature-map reuse and filter reuse. Step 1 estimates on-chip memory layer by layer for I = P×Q×R design points and keeps only the points that fit N_DSP and M_BRAM. Step 2 ranks the remaining points by estimated total cycles T(i), using Eqs. 11–16 for DRAM load, scratchpad load, systolic array compute and write-back.

Case study: Tiny YOLO convolutional layers on an Artix-7 (86K slices, 220 DSPs, 4.9 Mb BRAM). The search covers 96 design points (F=4, P=6, Q=4, R=4; rt={104,52,26,13,7,4}; csa and chsa each {2,4,8,16}). The best estimates are 12.468 M cycles for feature-map reuse and 12.361 M cycles for filter reuse. The recommended configuration is a 16-column systolic array.

Critical points:
(1) Every result is an analytical estimate. The paper reports no synthesis, place-and-route or on-board measurement; the conclusion defers comparison with synthesized results to future work. There is also no clock frequency, so the cycle counts cannot be turned into latency or FPS. There are no accuracy, power, LUT, DSP-utilization or throughput figures. For these reasons no benchmark rows are extracted.
(2) The paper contradicts itself. Table I defines feature-map traversal as ρ=1, but Section III calls feature-map reuse ρ=0. The text also credits feature-map reuse with better performance because of lower communication overhead, yet the numbers it quotes favour filter reuse (12.361 < 12.468 M cycles).
(3) The figure references look wrong. Panels 'd and g' and 'c and g' are both cited, and the feasibility wording ('above the memory cut-off line') is unclear.
(4) The cycle model is simple. It adds the terms serially with no overlap of data transfer and compute, and it assumes a bus width W. Parallel IFM/weight transfer is listed as future work.
(5) Only the convolutional layers are evaluated. The dataset, quantization bit-width and detection accuracy are never stated.

Metadata flags are still unresolved: the extraction reported ok=false, and the metadata and axes need manual checking. The year is listed as 2018, but the arXiv ID 1901 points to January 2019.
