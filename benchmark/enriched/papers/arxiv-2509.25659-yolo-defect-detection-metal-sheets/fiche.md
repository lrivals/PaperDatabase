---
id: arxiv-2509.25659-yolo-defect-detection-metal-sheets
fiche: done
date:
---

# YOLO-Based Defect Detection for Metal Sheets

Po-Heng Chou, Chun-Chi Wang, Wei-Lung Mao, 2025, arXiv preprint. https://arxiv.org/abs/2509.25659
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

Critical reading: The paper compares YOLOv3, v4, v7 and v9 for detecting metal-sheet defects (surface scratches and irregular holes), with and without ConSinGAN single-image augmentation. It reports that YOLOv9 with ConSinGAN is best: mAP0.5 91.3, PRE 98.8, REC 85.7, F1 91.0, detection time 146 ms.

Hardware and tagging: All timings come from a PC with an Intel i7-13700K and an NVIDIA RTX4080 (16 GB), Windows 10, Anaconda. There is no FPGA, quantization, power or resource data, so the auto-assigned 'yolo-fpga' axis looks wrong and should be checked.

Issues found in the passages:
(1) The test set is not independent. Only 10 original sheet images were used. From these, 35 defect crops of 512x512 were cut and augmented to 735 images, then split at random 80/10/10. Near-duplicate synthetic images from the same source crops very likely appear in both train and test, which would inflate the metrics.
(2) The abstract and contributions call the 91.3 value 'accuracy', but it is mAP0.5.
(3) Some F1 values do not match their PRE and REC. For YOLOv4 with ConSinGAN, F1 is 76.2 while PRE is 73.1 and REC is 73.9; F1 cannot be higher than both. For YOLOv3, PRE 70.1 and REC 78.5 imply F1 of about 74.1, but 65.4 is reported.
(4) The text says average detection time is about 210 ms. The mean of the 8 values in Table II is about 191 ms.
(5) Augmentation only changes training data, yet it changes detection time (for example YOLOv9 goes from 161 to 146 ms). The timing protocol is not described: batch size, whether pre/post-processing is included, and whether the time is per image.
(6) There are no model sizes, no inference resolution beyond the 416x416 training size, no variance or repeated runs, and no external baseline.
(7) Some descriptions are wrong: PGI is called 'personal growth initiative' (it is Programmable Gradient Information), and YOLOv4's SAM is called 'segment anything model' (it is a spatial attention module).

Rows: Values are copied from Table II. That table was extracted under the 'V. CONCLUSION' heading, so that heading is used as source_section. Detection time is entered as latency_ms, with medium confidence because the timing scope is unclear. The dataset is described in 'IV. EXPERIMENTAL RESULTS'.
