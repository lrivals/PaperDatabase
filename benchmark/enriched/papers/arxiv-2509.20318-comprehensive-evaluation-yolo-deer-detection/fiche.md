---
id: arxiv-2509.20318-comprehensive-evaluation-yolo-deer-detection
fiche: done
date:
---

# A Comprehensive Evaluation of YOLO-based Deer Detection Performance on Edge Devices

Bishal Adhikari, Jiajia Li, Eric S. Michel, Jacob Dykes, Te-Ming Paul Tseng, Mary Love Tagert, Dong Chen, 2025, arXiv preprint. https://arxiv.org/abs/2509.20318
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

Critical reading: This paper benchmarks 12 YOLO variants (v8, v9, v10 and v11 in n/t, s and m sizes) for single-class deer detection. It introduces a curated Cameratraps dataset of 3,095 images from Idaho camera-trap footage, split 2,578 train / 517 val. Inference runs on a Raspberry Pi 5 (CPU only, Cortex-A76, 16 GB) and an NVIDIA Jetson AGX Xavier. The paper has no FPGA implementation, so the automatically assigned 'yolo-fpga' axis looks wrong and should be checked by hand. Strengths: the cross-dataset test shows a clear domain gap. YOLOv11n scores AP@0.5 0.9920 on Roboflow but only 0.7395 on Cameratraps, with AP@50_95 dropping from 0.8475 to 0.5341. The dataset is public. Weaknesses: (1) The Table 5 values did not survive extraction; only headers remain. The passages give only bounds for edge results: YOLOv9t on Pi 5 takes >250 ms (<4 FPS), YOLOv8m on Pi 5 takes >1.5 s per frame, YOLOv11n and YOLOv10n on Jetson reach >40 FPS, s-models on Jetson reach >20 FPS, Jetson inference stays <70 ms, and Jetson AP@0.5 stays >0.85. (2) The 'total' and 'inference' timings are defined inconsistently: FPS comes from total time, including pre- and post-processing, and the authors blame the gap on software inefficiency. (3) The passages mention no precision, TensorRT, INT8 or hardware-specific optimization, and the conclusion defers that work, so the edge results are probably unoptimized framework inference. (4) No power measurements are given, even though the discussion argues that energy efficiency is a key point. (5) The high-end GPU used as the reference is not specified in these passages. (6) The summaries do not fully agree: the abstract says >30 FPS on Jetson and the conclusion says >25 FPS. Because only bounds are available, the numeric fields in the Jetson row are n/r. Re-extract Table 5 to fill them.
