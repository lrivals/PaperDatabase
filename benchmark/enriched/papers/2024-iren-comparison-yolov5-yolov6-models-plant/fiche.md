---
id: 2024-iren-comparison-yolov5-yolov6-models-plant
fiche: done
date:
---

# Comparison of YOLOv5 and YOLOv6 Models for Plant Leaf Disease Detection

Ecem Iren, 2024, Engineering Technology & Applied Science Research. https://doi.org/10.48084/etasr.7033
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

Critical reading: This is a GPU training comparison of YOLOv5 and YOLOv6 for leaf-disease detection on PlantDoc (2,569 images, 30 classes, 90:10 split giving 2328 training and 239 validation images). It has no FPGA or other hardware-deployment content, so the automatic 'yolo-fpga' axis looks wrong and should be checked in /paper-fiche. Training ran in Google Colab on an NVIDIA Tesla T4. Hyperparameters were: lr 0.01, SGD, momentum 0.937. The epoch count and batch size are missing from the extracted Table I. Model scale (s/m/l/x) is not stated for either model. Validation results are: YOLOv5 mAP50 63.5, mAP50-95 48.8, precision 64.8, recall 54.8. YOLOv6 gets mAP50 62, mAP50-95 49.6, precision 56.6, recall 62.4. The only timing measure is training duration: 0.772 h for YOLOv5 and 2.282 h for YOLOv6. The table gives these without units; the text says hours. No inference latency, FPS, power or resource figures are reported. The claim that YOLOv6 is faster at inference is only cited, not measured. The abstract loosely calls mAP50 'mAP'. The results come from one run on a small validation set of 239 images, with no variance reported, so the roughly 1-point differences are not conclusive. Rows below record accuracy only. Hardware fields are n/r, and training time is kept out of latency_ms.
