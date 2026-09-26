---
id: 2024-qureshi-semantic-segmentation-yolo-detector-aerial
fiche: done
date:
---

# Semantic Segmentation and YOLO Detector over Aerial Vehicle Images

Asifa Mehmood Qureshi, 2024, Computers, materials & continua/Computers, materials & continua (Print). https://doi.org/10.32604/cmc.2024.052582
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

Critical reading (based only on the supplied passages): this is a CPU/software paper, not an FPGA paper, so the automatic 'yolo-fpga' axis tag looks wrong. The pipeline has six steps: preprocessing, semantic segmentation (maximum-entropy scaling beat XGBoost and FCM, with 89.2 and 90.8 accuracy on the two datasets), YOLO detection, SURF features with ID assignment, Kalman-filter tracking, and centroid-based path estimation. The experiments ran in Python on a laptop (Intel Core i5-7200U, 2.50 GHz, 6 GB RAM). The paper reports no FPS, latency, power or FPGA resource figures, so it says nothing about hardware efficiency. It does claim segmentation lowers computational cost, but gives no timing to back this up. There are internal inconsistencies. The abstract and keywords say YOLOv5, but the Introduction says 'YOLOv4 is implemented', and the table compares against 'YOLOv4 [48]'. The text also mixes 'MOTP' and 'MTP'. The table bodies did not come through the extraction (only captions survive), so the SOTA comparison cannot be checked. The paper reports detection precision of 94.1 (Roundabout) and 96.1 (VAID). Tracking results are MOTA 87.2 and MOTP 92.3 on Roundabout, and MOTA 91.7 and MOTP 95.6 on VAID. The passages give no train/test split or IoU threshold, and do not say whether the detector was pretrained. The rows below record detection precision. Quantization is not reported and is assumed to be FP32 software inference.
