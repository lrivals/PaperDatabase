---
id: arxiv-1909.13396-req-yolo-resource-aware-efficient
fiche: done
date:
---

# REQ-YOLO: A Resource-Aware, Efficient Quantization Framework for Object Detection on FPGAs

Caiwen Ding, Shuo Wang, Ning Liu, Kaidi Xu, Yanzhi Wang, Yun Liang, 2019, arXiv preprint. https://arxiv.org/abs/1909.13396
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

REQ-YOLO (FPGA '19; arXiv 1909.13396) targets tiny YOLO (the YOLOv2-tiny variant with 9 CONV layers and 416x416 input). It combines three techniques: (1) block-circulant compression of CONV weights (model YOLO-3 uses block/FFT size 16); (2) ADMM-based quantization applied directly to the FFT-domain weights; (3) a per-layer heterogeneous scheme. In that scheme, DSP-based equal-distance quantization is used for accuracy-sensitive layers, and LUT shift-based mixed powers-of-two quantization for the rest. The platform is an Alpha Data ADM-PCIE-7V3 (Virtex-7 690t) at 200 MHz, built with Xilinx SDx 2017.4 HLS plus a template-based C/C++ code generator. All weights sit in on-chip BRAM, so off-chip DDR is never used for weights.

Measured result recovered: Table 1 gives total layer-wise latency for YOLO-3. Equal-distance is 4,801.0 µs with a 5.93 Mb model; heterogeneous is 3,183.6 µs with a 4.95 Mb model. The ratio is about 1.51x, which matches the claimed 1.5x speedup. These latencies are in µs. The schema column is in ms and unit conversion is not allowed, so latency_ms is n/r in the rows.

Critical points:
- Table 2's FPS, power and FPS/W values are missing from the supplied text. Only relative claims survive: 1.5x performance and 1.6x efficiency for YOLO1 over YOLO0; at least 10x FPS over [15,33]; about 6x less power than GTX 1070; 5.7x and 9.4x better efficiency. So fps, power, gops and absolute resources are all n/r.
- Table 1 does not state which dataset it uses. Accuracy is given only as extra degradation from 32-bit to 6-bit: 0.73 (mAP, PASCAL VOC) and 0.2 (IOU, DataDJI). No absolute mAP is given, and the bit-width used on hardware is not stated clearly.
- The resource model contains an apparent typo: #CONVD appears in both DSP terms.
- The text says 'RNN designs' where it means YOLO.
- The FPGA baselines use different devices (Virtex-7 485t, Zynq 7020) and do not report power, so the efficiency comparison is GPU-only.
- In Table 1, per-layer latencies appear only for Conv7 (1,832.7 µs, equal-distance); the other layer values were lost in extraction.
