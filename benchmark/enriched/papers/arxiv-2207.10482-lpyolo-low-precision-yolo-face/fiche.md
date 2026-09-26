---
id: arxiv-2207.10482-lpyolo-low-precision-yolo-face
fiche: done
date:
---

# LPYOLO: Low Precision YOLO for Face Detection on FPGA

Bestami Gunay, Sefa Burak Okcu, Hasan Şakir Bılge, 2022, arXiv preprint. https://doi.org/10.11159/mvml22.108
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

LPYOLO redesigns TinyYolov3 for face detection. It removes the upsample and concat layers, cuts the kernels per layer by 5x, uses a 416x416x3 input and a 13x13x18 output, and replaces the final Sigmoid with a rescaled HardTanh at synthesis. The model is trained with QAT in Brevitas at several weight/activation bit widths, with 8-bit first and last layers. It is compiled with FINN (Vitis HLS, Vivado) onto a PYNQ-Z2 (Zynq 7020), and all parameters are kept in on-chip memory. The ARM PS handles pre/post-processing and TCP/IP streaming using multithreading. Headline result for 4W4A: 0.757 mAP on WiderFace Easy (0.590 Medium, 0.261 Hard), 18 FPS, 2.4 W total board power. Critical points: (1) The 52.3 ms latency is for the CNN only. Pre/post-processing times (18.5 / 7.5 ms) are reported only for the non-quantized PS run. The 18 FPS figure comes from pipelined, multithreaded streaming, not from 1/latency. (2) The claim of about 50x speedup does not match Table 3 directly. The CNN-only ratio is 5017.9/52.3 ≈ 96x. The paper does not explain how 50x was computed. (3) Accuracy is measured on the WiderFace validation split, and the abstract highlights only the Easy subset. The 'Hard' mAP (0.261) is much weaker. (4) Resource use is given only as percentages: 74% LUT, 11% LUTRAM, 65% BRAM, 51% FF, 92% DSP. These are copied as bare numbers in the luts/dsps/bram columns and are NOT absolute counts. (5) Power is total board power and the measurement method is not described. No GOPS figure is given, and there is no numerical comparison to prior FPGA face or YOLO designs. (6) '4-bit' is not uniform, because the first and last layers are 8-bit. (7) The extraction metadata flags that no sections were detected, so most passages are labelled '(préambule)'.
