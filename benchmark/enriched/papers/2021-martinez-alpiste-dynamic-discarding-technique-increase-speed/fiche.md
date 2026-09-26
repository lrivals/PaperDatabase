---
id: 2021-martinez-alpiste-dynamic-discarding-technique-increase-speed
fiche: done
date:
---

# A dynamic discarding technique to increase speed and preserve accuracy for YOLOv3

Ignacio Martinez‐Alpiste, Gelayol Golcarenarenji, Qi Wang, José M. Alcaraz Calero, 2021, Neural Computing and Applications. https://doi.org/10.1007/s00521-021-05764-7
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

Critical reading: The paper proposes a "dynamic discarding" technique for YOLOv3 and Tiny-YOLOv3 (3l). It skips YOLO output heads that are not needed at run time. A proximity sensor gives the object's distance, and only the matching scale head runs: layer 0 for near, 1 for medium, 2 for far. Accuracy is claimed to be preserved because only unused operations are removed.

Hardware: this is NOT an FPGA paper, despite the auto-inferred 'yolo-fpga' axis. Everything runs on an NVIDIA Jetson Xavier GPU through PyTorch. TensorRT, OpenCV (CPU-only here), TF Lite and Snapdragon could not run the technique. This means TensorRT optimisation was not used, so the absolute speed is likely far from what this device can reach. FPGAs appear only in Related Work (Moussawi et al., SSD on Arria 10; Hemmati et al., HOG+SVM on Zynq).

Measured results in the supplied passages are only relative: at least 5.5% speed-up with two output heads and 22% with one, against standard YOLOv3 in MAXN (30 W) mode. The actual FPS, latency and BFLOPS values are in Tables 7 and 8, which are not in the supplied text. For Tiny-YOLOv3 (3l), the passages only say FPS improved for every single-head output across input sizes 416, 608, 832 and 1056.

Accuracy: the 55.3 mAP on COCO is the original YOLOv3 author's figure, not re-measured. It is probably AP50 at 608. The per-distance accuracy (Tables 9 and 10) comes from the authors' own driving tests. They say far-range accuracy drops when only head 2 runs, so heads 1 and 2 need to run together.

Caveats: 30 W is the power-mode cap, not measured power, so power is recorded as n/r. Precision is not stated (probably FP32 PyTorch). No LUT, DSP or BRAM figures apply. Metadata extraction was flagged 'ok: false'.
