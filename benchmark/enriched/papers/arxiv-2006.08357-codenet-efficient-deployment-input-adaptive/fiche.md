---
id: arxiv-2006.08357-codenet-efficient-deployment-input-adaptive
fiche: done
date:
---

# CoDeNet: Efficient Deployment of Input-Adaptive Object Detection on Embedded FPGAs

Zhen Dong, Dequan Wang, Qijing Huang, Yizhao Gao, Yaohui Cai, Tian Li, Bichen Wu, Kurt Keutzer, John Wawrzynek, 2020, arXiv preprint. https://arxiv.org/abs/2006.08357
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

CoDeNet (FPGA '21; the metadata says arXiv preprint, but the passage says it appeared at FPGA '21) co-designs a hardware-friendly deformable convolution with the network. The changes are depthwise, bounded range, square-shaped sampling and offsets rounded to integers. The network is a ShuffleNetV2 + CenterNet anchor-free detector, quantized to 4-bit weights and 8-bit activations. It runs on an Ultra96 board (Zynq XCZU3EG) at 250 MHz, built with Vivado HLS as a dataflow design. The first layer and the split/shuffle/concat operations run on the ARM processor.

Hardware results:
- Kernel-level speedups are 1.36× for full deformable convolution and 9.76× for depthwise, measured on one synthetic layer (h=w=64, k=c=256). They are not end-to-end speedups.
- End to end, config c (512×512) reaches 26.9 fps at 61.7 AP50 on VOC07. The contributions list rounds this to "26 fps".
- Config a (256×256) has 31 ms single-batch latency at 51.1 AP50.
- Power is measured on the board supply line: 4.3 W idle and 5.6 W while running. The FPGA workload therefore adds only about 1.3 W. The figure of 5.75 fps/W for config a implies about 32 fps, which matches the 31 ms latency. It is not clear which configuration the 5.6 W was measured on.
- Resource use is 34144 LUTs (48.4%), 216 BRAM (100%) and 360 DSPs (100%). Only one utilization table is given, even though the paper says the accelerator is "customized for each configuration".

Inconsistencies and caveats:
- In the text, config a gets "53 AP50" (Table 3, likely FP32), but Table 5 gives 51.1 (w4a8).
- Config e has 72.4 AP50 in the text (FP32) but 69.7 in Table 5.
- The COCO sentence says CoDeNet2× gets "26.1 and 21.0 AP, with and without quantization respectively". This order looks reversed.
- The prior-work comparison mixes different datasets (DJI-UAV IoU vs VOC AP50), platforms and resolutions.
- The Tiny-YOLO comparison ("20.9× smaller, 10% more accurate") is based on model size, not measured FPGA throughput.
- Most table numbers (Tables 1–4) were lost in PDF extraction.
- No section headings were detected, so every passage except the Abstract is labeled "(préambule)".
