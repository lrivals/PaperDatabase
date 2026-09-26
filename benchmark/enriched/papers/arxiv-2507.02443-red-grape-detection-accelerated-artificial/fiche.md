---
id: arxiv-2507.02443-red-grape-detection-accelerated-artificial
fiche: done
date:
---

# Red grape detection with accelerated artificial neural networks in the FPGA's programmable logic

Sandro Costa Magalhães, Marco Almeida, Filipe Neves dos Santos, António Paulo Moreira, Jorge Dias, 2025, arXiv preprint. https://arxiv.org/abs/2507.02443
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

Critical reading: The authors use FINN and Brevitas to deploy three small quantised classifiers in the programmable logic (PL) of an AMD ZCU104: MobileNet v1 w4a4, CNV w2a2 and CNV w1a1 (a binary neural network). The task is binary grape/no-grape classification of 32x32 px tiles from their open RG2C dataset (test set of 2156 tiles). Headline results: MobileNet v1 reaches a 98 % success rate (Abstract) and 6610.94 FPS (Fig. 8; the Abstract rounds this to 6611). Both CNV variants reach 819.33 FPS.

Caveats:
(1) Per-model precision, recall and F1 appear only as a bar chart (Fig. 4) with no values in the text. Only the Abstract's '98 %' for MobileNet is usable, and its metric ('success rate') is not defined.
(2) The FPS definition is unclear. Eq. 4 gives FPS_image = FPS_chunk × Nc, which multiplies rather than divides by the number of chunks. The stated speed-ups ('263×' and '32×' over 25 FPS) match 6611/25 and 819/25, so the plotted values look like tile or throughput rates, not full-frame rates for 1920x1080 images.
(3) The dataset counts do not add up. 1198 images at 1920x1080 cut into non-overlapping 32x32 tiles would give far more than the 10782 tiles reported, so tiles were apparently filtered without explanation.
(4) No LUT, DSP, BRAM, power, latency, clock or folding (PE/SIMD) values are reported. The comparison against Vitis-AI/DPU ([10]) is asserted, not measured on the same setup.
(5) The CNV w1a1 and w2a2 results are identical (819.33 FPS), which suggests a throughput bottleneck outside the compute (not investigated). The authors also note that CNV was not optimised.

Rows: I included MobileNet v1 w4a4 and CNV w2a2. CNV w1a1 has the same FPS and no accuracy figure in the text, so it is not a separate row.
