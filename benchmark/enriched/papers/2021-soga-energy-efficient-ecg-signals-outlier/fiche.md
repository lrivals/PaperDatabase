---
id: 2021-soga-energy-efficient-ecg-signals-outlier
fiche: done
date:
---

# Energy-Efficient ECG Signals Outlier Detection Hardware Using a Sparse Robust Deep Autoencoder

Naoto Soga, Shimpei Sato, Hiroki Nakahara, 2021, IEICE Transactions on Information and Systems. https://doi.org/10.1587/transinf.2020lop0011
Type : n/r

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

Soga et al. (IEICE 2021) build an ECG outlier detector: an unsupervised Robust Deep Autoencoder (RDA) trained on MIT-BIH Arrhythmia data. Weights are pruned to 90% sparsity, converted to 10-bit fixed point, and weight-shared (K-means, k=16, no retraining). They are stored in CRS sparse format and run on a Xilinx ZedBoard (Zynq-7000) at 100 MHz, built with SDSoC 2018.2.

Reported results against an ARM Cortex-M3 (Arduino Due): 11.7x faster ('12x' in the abstract), 11% of the CPU power, and 0.94% of the energy (106x better). Energy is power times execution time over 1282 ECG waves. Power is for the FPGA or CPU only, not the whole board.

Table 5 resources for the weight-sharing design: BRAM 13.5 (9.64%), DSP 7 (3.18%), LUT 5381 (10.11%), FF 8476. For the fixed-point design without weight sharing: BRAM 14.5, DSP 7, LUT 6285. The fixed-point design is 2.9x faster than float, and weight sharing keeps roughly the same speed. Parameter volume falls to 4.13% of the dense float model.

Critical issues:
(1) The supplied passages do not give the absolute throughput (waves/s), power (W), execution time (ms) or energy (J); only ratios are given. So fps, latency and power are n/r.
(2) The F1 values contradict each other. Dense = 0.967 and 90% sparse = 0.968, but the text also says the 10/11-bit fixed-point F1 of 0.989 is 'identical to the 90% sparse model'. It also says 9-bit = 0.957 is '1% lower' than dense.
(3) The accuracy degradation is given as 0.83 points in some places and 0.84 in others.
(4) The F1 score of the final k=16 weight-sharing design is not stated in the passages.
(5) The baseline is a very low-end microcontroller, which inflates the speedup and energy gains. There is no comparison with other FPGA or ASIC ECG detectors.
(6) Power seems to be tool-estimated or chip-level (FPGA only), but the method is not stated.
(7) Metadata extraction failed, so every passage is labelled '(préambule)'.
