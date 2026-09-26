---
id: arxiv-2509.04153-real-time-fpga-cnns-detection
fiche: done
date:
---

# Real Time FPGA Based CNNs for Detection, Classification, and Tracking in Autonomous Systems: State of the Art Designs and Optimizations

Safa Mohammed Sali, Mahmoud Meribout, Ashiyana Abdul Majeed, 2025, arXiv preprint. https://arxiv.org/abs/2509.04153
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

Survey (Sali, Meribout, Majeed, arXiv 2509.04153, 2025) of FPGA CNN deployment for detection, classification and tracking. It covers LUT-DSP, SoC and ACAP (Versal) platforms, parallelism and pipelining, quantization, DSP packing, pruning and toolflows (Vitis AI, FINN, Intel FPGA AI Suite). The paper runs no experiments of its own. Every hardware number here comes from a cited work. That includes Tables VII–IX, H2PIPE [73] (>1000 FPS ResNet-50 on Stratix 10 NX), Peccia et al. [74] (two INT8 MACs per DSP48E2, 60% mean speed-up over Gemmini) and HAPM [76]. The rows below are secondary data and should be checked against the primary papers.

Problems with the source:
- The comparison tables leave out quantization, dataset and power measurement scope. Power values mix boards and conditions, e.g. 1.11 W versus 77 W.
- Table VIII puts U-Net (segmentation) and RBPnet4's F1 score under a "Top 1" accuracy column.
- The GROBID extraction garbles some columns. One example is Table VII [100], where LUTs and DSPs are merged ("484209 1153").
- Some entries look suspect: 19 BRAM for LCAM-YOLOX, and 1609 FPS at 77 W for the custom SSD.
- The GOPS/W comparison in Section II (Zynq 7z100 at 16.7 versus RTX 3090 at 6.32 [132]) is taken from one cited source and does not compare like with like.
- The peak-TOPS figures in Table IV are vendor ranges, not measurements.

The survey does raise useful open problems: RTOS-level management of PS-PL interaction, the cost of balancing a pipeline, and the fact that sparsity alone does not guarantee a speed-up (YOLOv7 pruning [77]).
