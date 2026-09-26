---
id: arxiv-2204.10619-real-time-hog-svm-object
fiche: done
date:
---

# Real-time HOG+SVM based object detection using SoC FPGA for a UHD video stream

Mateusz Wasala, Tomasz Kryjak, 2022, arXiv preprint. https://arxiv.org/abs/2204.10619
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

Wasala & Kryjak (2022) implement a single-scale HOG+SVM pedestrian detector on an AMD Xilinx ZCU104 (Zynq UltraScale+ MPSoC EV). It is written in SystemVerilog with Vivado 2020.2 and processes 3840x2160 video at 60 fps. The pipeline handles 4 pixels per clock, so the pixel clock needed for 4K at 60 fps drops from about 600 MHz to about 150 MHz (a frequency derived from the design, not a measured one). The design saves hardware in several ways. It approximates the gradient magnitude with max/min operations instead of a square root. It assigns orientation bins with a tangent look-up table instead of CORDIC. It builds histograms in registers with sum trees instead of BRAM. It normalises with a fast inverse square root (magic number 0x5F3759DF). It computes cell-based (rather than window-based) SVM partial sums and uses fixed-point arithmetic throughout. The ARM processor runs non-maximum suppression.

Critical points:
(1) The reported accuracy (98, versus 98.5 without the approximations) is the SVM's accuracy from the learning process on INRIA plus Oxford Town Centre (2600 positive and 24300 negative samples). It is not a hardware detection metric such as miss rate or AP, and no separate test split is described.
(2) Power of 9.579 W is an estimate, not a board measurement.
(3) The fixed-point bit widths in Table I and the resource counts in Table II are lost in the supplied text. The design is only described as using 'about half' of the ZCU104's resources. The Table II row for 'Ours' is garbled; its only number is 38.5, which cannot be mapped to a column, so LUTs, DSPs and BRAM are recorded as n/r.
(4) The detector works at a single scale only, so its 60 fps figure cannot be compared directly with multi-scale detectors. The paper gives no latency or GOPS figures.
(5) The claim that deep networks (YOLO) cannot run in real time at 4K is argued, not tested against a DNN baseline.
