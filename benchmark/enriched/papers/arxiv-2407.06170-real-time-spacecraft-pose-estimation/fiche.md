---
id: arxiv-2407.06170-real-time-spacecraft-pose-estimation
fiche: done
date:
---

# Real-Time Spacecraft Pose Estimation Using Mixed-Precision Quantized Neural Network on COTS Reconfigurable MPSoC

Julien Posso, Guy Bois, Yvon Savaria, 2024, arXiv preprint. https://arxiv.org/abs/2407.06170
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

Posso, Bois and Savaria (arXiv 2407.06170, 2024) run a mixed-precision Mobile-URSONet (MobileNetV2 backbone, 240x240 input) for spacecraft pose estimation on the SPEED dataset. They build it with FINN/Brevitas as a dataflow accelerator with one unit per layer and on-chip weights, clocked at 187.5 MHz on a ZCU104 (Zynq UltraScale+ MPSoC).

Measured on the board: 58.7 FPS at 0.865 W, or 67.9 FPS/W. The Vivado post-implementation estimate was 250 FPS at 3.83 W (65.3 FPS/W). The passages do not say how the board power was measured (rail, board or dynamic), so power_scope is marked unspecified.

Critical points:
1. The real board is more than 4x slower than the estimate. The authors blame too few BRAMs, which made the FIFOs too small. FPS per watt stays about the same only because power drops by 4.4x as well.
2. Only the backbone runs on the FPGA. The network head runs on the CPU. The passages don't say whether the reported FPS covers the whole pipeline or just the backbone.
3. Accuracy drops a lot. The ESA score (lower is better) goes from 0.296 in Float32 to 0.307 in Int8, then to 0.411 in mixed precision. Orientation error rises from 13.0 to 18.7 degrees and position error from 0.71 to 0.91 m. The paper calls this "manageable", but the claims of 7.7x speed and 19.5x efficiency are made without matching accuracy against the baselines.
4. The comparisons are across platforms and against other papers' numbers: Edge TPU [13] at 7.66 FPS and 2.2 W, and Intel Atom [6] at 6.58 FPS and 3.7 W. The ratios check out: 58.7/7.66 ≈ 7.7 and 67.9/3.48 ≈ 19.5. However, the power measurement methods are probably not the same across these works. The Ultra96 works [11] and [12] cannot be compared because they report no throughput.
5. Resources are given only as percentages: LUT 91, BRAM 90, DSP 32, FF 26. The table records these bare percentages, not absolute counts. The exact per-layer bit-widths are not in the passages. Activations below 4 bits caused errors.
6. Latency and GOPS are not reported.

The FPGA outputs match Brevitas bit for bit, so the pose metrics on the board and on the computer are identical.
