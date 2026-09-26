---
id: 2024-mittal-comprehensive-survey-deep-learning-lightweight
fiche: done
date:
---

# A comprehensive survey of deep learning-based lightweight object detection models for edge devices

Payal Mittal, 2024, Artificial Intelligence Review 57(9), 242. https://doi.org/10.1007/s10462-024-10877-1
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

This is a survey (Mittal 2024, Artif. Intell. Rev.), not a primary hardware study. Every number in it is taken from other papers. It gives no FPGA resource figures (LUTs, DSPs, BRAM) and no power measurements. The FPGA text (Xilinx is the most-used family; REQ-YOLO uses block-circulant weights and mixed-precision weight quantization) has no numbers.

Problems with the passages:
- Tables 5 and 6 don't say which hardware, batch size or precision each FPS or latency figure came from, so the rows can't be compared with each other.
- FLOPs units are mixed and some look wrong. YOLOv3 is listed at "1453B". ThunderNet's "0.47" has no unit. PP-YOLOv2 with a ResNet101 backbone is listed at "0.115G", which is implausible.
- Several speed pairs don't match. YOLOv3-Tiny's 4.5 ms and 368 FPS imply different setups. GL-YOLO-Lite's 70.51 ms and 52.63 FPS can't both come from the same run.
- Text extraction has scrambled some Table 5/6 columns: PP-YOLOE-S, Slim YOLOv4 and YOLOv7-X.
- The survey says YOLOv7-X has the best COCO mAP but doesn't give the value in these passages.

Hardware results the survey reports from other papers:
- L4Net: 71.68 mAP (KITTI, per the Fig. 8 discussion), 13.7 M model size, 149 FPS on "NVIDIA TX" (TX1 or TX2 not stated) and 30.7 FPS on a Qualcomm-based device.
- ThunderNet: 24.1 FPS and 19.2 AP on COCO on an ARM-based smartphone.

The two rows below record these second-hand figures. Treat them as pointers to the original papers, not verified measurements.
