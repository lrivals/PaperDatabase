---
id: arxiv-2211.11647-benchmarking-edge-computing-devices-grape
fiche: done
date:
---

# Benchmarking Edge Computing Devices for Grape Bunches and Trunks Detection using Accelerated Object Detection Single Shot MultiBox Deep Learning Models

Sandro Costa Magalhães, Filipe Neves Santos, Pedro Machado, António Paulo Moreira, Jorge Dias, 2022, Engineering Applications of Artificial Intelligence 117, 105604 (2022). https://doi.org/10.1016/j.engappai.2022.105604
Type : article de journal

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

Critical reading: The paper benchmarks one detector, RetinaNet ResNet-50 fine-tuned on VineSet (1125 non-augmented test images, 3 classes). It runs on a Jetson TX2 (TF-TRT, FP32/FP16), a Coral Dev Board TPU (Edge TPU Compiler, INT8 PTQ) and on ZCU104 and KV260 DPUs (Vitis-AI 1.4, INT8 PTQ). An RTX3090 serves as a reference only.

The supplied passages give measured hardware results only as ranges in the Abstract:
- FPGAs: 14 to 25 FPS.
- GPUs: 3 to 5 FPS.
- TPU and GPU power: about 5 W.
- Accuracy across devices: F1 about 70 and mAP about 60.
The Results figures (Figs 4 to 7) were not supplied as numbers, so per-device values cannot be assigned. For example, the passages do not say whether 25 FPS belongs to the ZCU104, which has 2 DPU cores, or whether both cores were used.

Caveats:
- Timing covers only the model core, averaged after 50 warm-up images. Pre- and post-processing in OpenCV on the CPU are excluded, so end-to-end FPS will be lower.
- Power was measured at the board input with a Fluke 175 multimeter, with voltage and current read in two separate steps. That is not simultaneous or continuous sampling.
- The FPGA boards ran a stock PetaLinux image with all resources active, which likely inflates FPGA power.
- The Jetson Nanos failed to compile the model, and the TX2 could not produce INT8, so there is no INT8 comparison on the GPU.
- The TPU had the worst precision and recall after quantisation.
- No LUT, DSP or BRAM figures or DPU configuration are given, and no GOPS are reported.
- There are internal inconsistencies. The Nano and TX2 are called 1000 and 2000 "TFLOPS", which is probably meant to be GFLOPS. The title says SSD while the model is RetinaNet.
