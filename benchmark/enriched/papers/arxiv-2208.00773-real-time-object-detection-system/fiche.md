---
id: arxiv-2208.00773-real-time-object-detection-system
fiche: done
date:
---

# Real Time Object Detection System with YOLO and CNN Models: A Review

V Viswanatha, R K Chandana, Ramachandra A C, 2022, arXiv preprint. https://arxiv.org/abs/2208.00773
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

This is a narrative review, not a primary study. It contains no hardware experiments of its own. Every number in it is quoted from cited work without platform, dataset or setup details, so all rows are secondary and low confidence.

Critical points:
1. The English is badly garbled, apparently from automated paraphrasing ("frames consistent with 2d", "curling gold detection", "sluggish Vicinity"). This makes technical claims hard to verify.
2. Section II has an internal contradiction for the YOLOv2 curling system [18]: it gives 13 fps once and 30 fps once, both with 94.3% precision. The row below uses 13 fps, the explicitly measured test figure. The 30 fps value is unreliable.
3. The FPGA-relevant citation [5] (improved YOLO on Xilinx ZYNQ with 16-bit fixed-point weights) gives no numbers for throughput, resources, power or accuracy. It only says cost was "significantly reduced while maintaining accuracy," so it cannot fill a row.
4. The improved YOLOv3 road-detection claim [6] (+3.17% accuracy, -5.62% miss rate, extra 104x104 detection layer) has no hardware platform.
5. It repeats the original YOLO figures of 45 fps and 125 fps for Fast YOLO from [2] without naming the GPU.
6. The conclusion calls YOLOv4 the "second major version," which is factually wrong.
7. It miscategorizes CNN/RNN as "classification-based" versus YOLO as "regression-based."

Use this only as a pointer to primary sources ([5], [18], [2]), not as a source of benchmarks.
