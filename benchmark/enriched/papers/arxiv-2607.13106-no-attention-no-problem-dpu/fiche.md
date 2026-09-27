---
id: arxiv-2607.13106-no-attention-no-problem-dpu
fiche: done
date:
---

# No Attention, No Problem: DPU-Aware Attention Approximation in Modern YOLO on FPGA

Suraj Karki, Qazi Arbab Ahmed, Thorsten Jungeblut, 2026, arXiv preprint. https://arxiv.org/abs/2607.13106
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

Karki et al. (HSBI, arXiv 2607.13106, 2026) make YOLOv8n, YOLOv11n and YOLOv26n run on the Vitis AI DPU (DPUCZDX8G, ZCU104), in both standard and OBB versions. They swap unsupported activations for ReLU and replace split operations with 1x1 convolutions. They also approximate C2PSA spatial attention: parallel 1x1 Q/K/V convolutions, a scaled element-wise q⊙k product, and hard-sigmoid in place of softmax. The models are quantized to INT8 with post-training quantization and tested on six datasets and all eight DPU sizes (B512–B4096).

Main results (IV. RESULTS): YOLOv26n and YOLOv26n-OBB have the best end-to-end performance on B4096: 34.05 and 29.55 FPS, with 29.37 and 33.85 ms latency. These were measured on one DPU core using the PETS2009-S2L1 video (768×576), not on the accuracy datasets.

Critical points:
(1) Power is Vivado-reported on-chip power for each DPU configuration (4.792–8.760 W), not measured board power, and it does not depend on the model. So the claim of about 3× lower power than the state of the art [27] compares estimated power with another paper's figure of unknown scope.
(2) The accuracy loss figures disagree. The abstract and conclusion say about 5% absolute loss from quantization, but the results section says about 7% on average across datasets for the attention-based variants. Some cases are much worse, for example YOLOv8n on KITTI: 0.64 to 0.34.
(3) Tables I and II disagree slightly (YOLOv8n KITTI modified: 0.63 vs 0.64 on CPU).
(4) The DPU-only FPS and latency are shown only in Figs. 6–8, which were not supplied. The large gap between DPU and end-to-end speed is blamed on Python post-processing and NMS on the ARM, so end-to-end FPS mostly reflects software, not the accelerator.
(5) The B1152 resource row looks odd: 38 BRAM, compared with 76 for B1024.
(6) GOPS is not reported, and accuracy is given only as mAP@0.5:0.95.

The rows below pair each model's FPGA mAP (COCO for the standard model, DOTA for the OBB model) with the throughput measured on PETS2009. They also use the design-level B4096 resources and power. These mixed pairings are why confidence is medium.
