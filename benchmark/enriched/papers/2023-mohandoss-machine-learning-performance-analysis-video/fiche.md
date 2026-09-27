---
id: 2023-mohandoss-machine-learning-performance-analysis-video
fiche: done
date:
---

# Machine Learning Based Performance Analysis of Video Object Detection and Classification Using Modified Yolov3 and Mobilenet Algorithm

T. Mohandoss, J Rangaraj, 2023, Journal of Machine and Computing. https://doi.org/10.53759/7669/jmc202303025
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

Critical reading (from the supplied passages only): The paper swaps YOLOv3's Darknet-53 backbone for MobileNet (depthwise plus pointwise convolutions, 416x416 input per Table 1). It adds a Kalman-filter denoising step and binary cross-entropy for class prediction. Evaluation uses frame sequences described as MOT20. The paper calls MOT20 a "real-time video dataset acquired on this work", but it is a public benchmark. Reported headline numbers: accuracy 99 (Abstract and Fig 5), precision 98, recall 95, TP 95, FP "94" and detection rate 93. It gives baseline precision of 95/93/91/82/81 for SSD/RCNN/F-RCNN/YOLOv2/YOLOv3. There are serious methodological red flags. (1) Metric definitions are confused: FP is described as both false alarms and frames per second, a high FP rate is called "most excellent", MAP is defined as "mean absolute position" rather than mean average precision, and precision is defined as measurement repeatability. (2) Reporting per-frame-sequence maxima suggests best-case reporting. (3) There is an internal inconsistency in Table 1 (a 7x7 average pool applied to a 13x13 map). (4) No hardware platform, FPGA device, quantization, toolflow, resource usage or throughput is given. Table 11 (power and latency) appears only as a caption, with no values in the passages. The automatic 'yolo-fpga' axis is not supported by this text, so no measured hardware result is present. The rows below record only the algorithmic accuracy and precision claims, with low confidence.
