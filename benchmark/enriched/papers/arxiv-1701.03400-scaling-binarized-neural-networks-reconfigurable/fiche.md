---
id: arxiv-1701.03400-scaling-binarized-neural-networks-reconfigurable
fiche: done
date:
---

# Scaling Binarized Neural Networks on Reconfigurable Logic

Nicholas J. Fraser, Yaman Umuroglu, Giulio Gambardella, Michaela Blott, Philip Leong, Magnus Jahre, Kees Vissers, 2017, arXiv preprint. https://arxiv.org/abs/1701.03400
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

Fraser et al. (2017) extend FINN to larger BNNs on an Alpha Data ADM-PCIE-8K5 board with a Kintex UltraScale KU115 FPGA running at 125 MHz. The main contribution is streaming padding with -1 values. This keeps the datapath binary: 0-padding would need ternary {-1,0,+1} values and a 2-bit datapath. In Table 1, -1-padding matches 0-padding (sigma=1: 88.3 vs 88.6; sigma=1/2: 85.2 vs 85.2). Both beat no-padding by about 4-5 points, but padding costs 2-3 times more operations per frame (Table 2).

Headline result: cnn(1), at 1.2 GOP/frame, runs at 12 kFPS with 671 µs latency, draws under 41 W of board power, and delivers 14.8 TOPS (Table 3: 14,814 GOps/s). The stated CIFAR-10 accuracy is 88.7.

Issues for critical reading:
(1) Accuracy doesn't match across the paper. The abstract gives 88.7, but Table 1 gives cnn(1) 88.3 with -1-padding and 88.6 with 0-padding.
(2) Power is only an upper bound for the whole board ("less than 41 W"). No power is reported per design. The resource counts include the PCIe infrastructure.
(3) The extracted Table 3 is garbled. LUT, BRAM and kFPS values are missing, and only GOps/s survives for the padded designs. All designs were built for the same target of about 12 kFPS.
(4) The GPU comparison (Titan X at 3.2 kFPS and 227 W on AlexNet) sets binary operations against 32-bit float and uses a different network and dataset. It is not a like-for-like comparison.
(5) The comparison with FINN mixes devices (Z7045 vs KU115). FINN's MLPs come closer to the theoretical peak. BRAM use is poor because weights are split across many PEs and SIMD lanes, which limits scaling to cnn(2).

Units: I copied values without conversion. In row 1, the fps value is in kFPS (12) and latency_ms holds 671 in µs (0.671 ms).
