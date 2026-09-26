---
id: 2021-ponnusamy-deep-learning-x-ray-baggage
fiche: done
date:
---

# Deep Learning-Based X-Ray Baggage Hazardous Object Detection – An FPGA Implementation

Vijayakumar Ponnusamy, Diwakar R. Marur, Deepa Dhanaskodi, Thangavel Palaniappan, 2021, Revue d intelligence artificielle. https://doi.org/10.18280/ria.350510
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

Critical reading: The paper runs YOLOv3 on a PYNQ-Z1 (Zynq) board to find hazardous objects (gun, blade, knife) in X-ray baggage images. Only one step is fully described: pre-processing, 3x3 kernel operations and YOLOv3 classification are split between the PS and PL. The reported results are per-class mAP from Table 1: gun 98.5, blade 98.0, knife 98.9. The abstract's claim of '98.9% accuracy' is the single best class (knife), not an overall figure. There are several serious weaknesses. (1) Training used Darknet in Google Colab with only 500 samples. The dataset is not named, and no train/test split or IoU threshold is given. The confidence threshold was picked to give '98% accuracy', which suggests it was tuned on the evaluation data. (2) The text does not say whether the mAP was measured on the FPGA or in software. (3) No throughput, latency, power, clock frequency or quantization/data format is reported, even though the paper names data representation as a key issue. (4) Table 2 (resources) did not survive extraction. The only value left is '130 k', near the classification row, and its column is unknown. A PYNQ-Z1 (XC7Z020) has about 53.2k LUTs and 106.4k FFs, so 130k cannot be a LUT count; it may be FFs, a different unit, or a mistake. I left LUT/FF/BRAM/DSP as n/r; check them against the original PDF. (5) There is no baseline comparison to other FPGA YOLO designs or to CPU/GPU. The sections on CNN vs handcrafted features and transfer learning are claimed but not backed by numbers. Overall, treat this as weak evidence that YOLOv3 can run on an FPGA for this task; it gives no usable performance figures.
