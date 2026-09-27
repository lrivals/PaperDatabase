---
id: 2023-tapiador-implementing-cnn-fpga-programmable-logic
fiche: done
date:
---

# Implementing a CNN in FPGA Programmable Logic for NILM Application

Miguel Tapiador, Laura de Diego-Otón, Álvaro Hernández, Rubén Nieto, 2023, n/r. https://doi.org/10.1109/dcis58620.2023.10335989
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

Tapiador et al. (DCIS 2023) take a small NILM load-classification CNN (from their earlier ref. [7]: 64x64 current-window images, 17 classes, BLUED data at 4 kHz). They quantize it with Brevitas quantization-aware training and build a streaming IP with FINN for a Zybo Z7-20 (XC7Z020). The weights are 3-bit, except the first fully-connected layer (8192-256), which is 2-bit. The passages give no activation bit width. To fit FINN, padding was added to the convolutions, which grows the first FC layer from 6272 to 8192 inputs. The FC1 weights are stored in BRAM and the other layers in LUTRAM. The IP sits in a Zynq SoC with ARM and DMA, and an extra FINN transform was needed to add TLAST.

Measured results: post-implementation resources, CNN IP / whole system: LUT 16911/20937, FF 32920/38518, RAMB36E1 118 (84.29%)/120, DSP 75/75. On-board accuracy on the test set was 96.96, against 98.19 for the float CNN and 96.94 for the software QCNN. Precision, recall and F1 were 97.26, 96.72 and 96.95.

Caveats:
- Throughput is only FINN's estimate (21 FPS at 100 MHz), not a measurement. The design deliberately trades latency for fewer resources.
- No power, energy or measured latency is reported.
- No comparison with other FPGA or CPU implementations.
- BRAM use (about 85%) is the binding constraint.
- Test-set size and class balance are not given in the passages. The drop is also uneven across classes (class 00 is hit harder).
- Metadata was flagged for manual check.
