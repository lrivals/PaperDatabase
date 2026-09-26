---
id: arxiv-2503.08700-real-time-semantic-segmentation-aerial
fiche: done
date:
---

# Real-Time Semantic Segmentation of Aerial Images Using an Embedded U-Net: A Comparison of CPU, GPU, and FPGA Workflows

Julien Posso, Hugo Kieffer, Nicolas Menga, Omar Hlimi, Sébastien Tarris, Hubert Guerard, Guy Bois, Matthieu Couderc, Eric Jenn, 2025, arXiv preprint. https://arxiv.org/abs/2503.08700
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

Critical reading (from the supplied passages only): The paper compares five deployment workflows for a lightweight U-Net on the Inria aerial building-segmentation task. The workflows are TensorFlow-GPU and cuDNN on Jetson AGX Xavier, TVM on the CPUs of Ultra96/ZCU104, FINN on ZCU104, and Vitis-AI on ZCU102. The authors say the U-Net has 16x fewer parameters and MACs than the original while keeping accuracy, and that it beats the Inria FCN+MLP baseline on building IoU and pixel accuracy. However, the Inria baseline's architecture is not fully specified, so this comparison is weak.

Main caveats:
(1) The passages include only table captions (Tables I–XIV). None of the table values are present, so every accuracy, throughput, latency, power and resource figure is n/r here.
(2) The cuDNN and FINN results were never run on the board. The cuDNN figures are scaled from a partial network (31.6% of the MACs and 60.7% of the parameters/feature maps). The FINN figures are estimates, and the authors call FINN's resource estimator unreliable. Only the post-implementation Vivado LUT report (Table IX) is concrete.
(3) The only measured number in the text, the 238 for the first inference of a batch of 8 on the Jetson, is cut off before its unit. It is therefore not recorded.
(4) The Vitis-AI setup is 3 DPU cores at 4096 ops/cycle and 100 MHz. That is a peak configuration, not a measured GOPS value, so it is not converted.
(5) The paper says all workflows are compared at iso-accuracy. It reports that FINN (binary weights, 4-bit activations, no DSPs, LUT-limited) loses a little accuracy. It reports that Vitis-AI 8-bit post-training quantization slightly improves accuracy (DSP/BRAM-limited) and gives the best energy efficiency.
The conclusion that Vitis-AI is the best choice combines measured metrics with qualitative engineering scores (Table XIV: high/medium/low). The FINN comparison relies on estimates, not measurements.
