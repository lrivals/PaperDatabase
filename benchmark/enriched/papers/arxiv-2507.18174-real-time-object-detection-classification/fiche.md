---
id: arxiv-2507.18174-real-time-object-detection-classification
fiche: done
date:
---

# Real-Time Object Detection and Classification using YOLO for Edge FPGAs

Rashed Al Amin, Roman Obermaisser, 2025, 2025 International Symposium ELMAR. https://doi.org/10.1109/ELMAR66948.2025.11193980
Type : conférence

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

YOLOv5 was trained in PyTorch with SGD (lr 0.01, batch 32, 100 epochs) on COCO and GTSRB. It was quantized from FP32 to INT8 after training and compiled with Vitis AI for the DPU on a Xilinx Kria KV260. The only hardware result reported is 98.6 'classification accuracy', 9 FPS, 3.5 W and 2.6 FPS/W. This comes from 72 curated test images drawn from both datasets.

Points to read critically:
(1) Accuracy is not stated consistently. The abstract says 99 while the results section and Table I say 98.6. The metric is not defined either: it is not mAP, and COCO and GTSRB are not reported separately.
(2) 72 images is too small a test set to support comparisons with other work. Most rows in Table I report mAP on different datasets, so the accuracy comparison is not like-for-like.
(3) The paper does not say how the 3.5 W was measured (board or chip, idle or under load). Latency is claimed to be 'real-time' and 'low', but no latency number is given. 9 FPS is weak for real-time ADAS use.
(4) The paper claims to be 'resource-efficient' but reports no LUT, DSP or BRAM use and no DPU configuration. No input resolution, YOLOv5 variant (n/s/m) or FP32-vs-INT8 accuracy comparison is given.
(5) The method is contradictory: it is described as post-training quantization but also credits 'quantization-aware techniques'. The abstract says 'GTSRD' instead of GTSRB. Future work promises 'multiclass detection', yet the system already uses 80-class COCO.
(6) Some Table I baseline figures don't match elsewhere. The Ngo et al. entry lists 25 FPS, but the related-work text says up to 29 FPS. Amin et al.'s 15 FPS / 3.5 W works out to 4.29 FPS/W, but the table lists 4.2. The paper's own efficiency checks out: 9 / 3.5 = 2.57, rounded to 2.6.
The claim that it 'improves energy efficiency' over prior work is not supported by its own table: 2.6 FPS/W is lower than 4, 4.7, 4.2 and 3.1.
