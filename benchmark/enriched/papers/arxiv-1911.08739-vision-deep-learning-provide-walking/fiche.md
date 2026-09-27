---
id: arxiv-1911.08739-vision-deep-learning-provide-walking
fiche: done
date:
---

# Vision: A Deep Learning Approach to provide walking assistance to the visually impaired

Nikhil Thakurdesai, Anupam Tripathi, Dheeraj Butani, Smita Sankhe, 2019, arXiv preprint. https://arxiv.org/abs/1911.08739
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

Assistive walking system for visually impaired users: YOLO object detection (YOLOv3 per Sec. 4, trained on COCO, with indoor/outdoor class-filtering modes) plus monocular depth estimation (a CNN synthesizes the right stereo view from the left image, then a stereo-matcher CNN with 1D correlation produces a disparity map, trained on KITTI), with pre-recorded text-to-speech audio output. Critical points: (1) The auto-assigned 'yolo-fpga' axis is wrong. None of the supplied passages mention an FPGA, hardware platform, quantization, throughput, latency, power or resource use. No measured hardware result is reported, so all hardware fields are n/r. (2) The only quantitative evaluation is Table I, which gives per-object detector confidence scores on a single unspecified image (YOLO 100/99, Faster RCNN 99/97, SSD 92/93). Confidence scores are not an accuracy metric like mAP and are not calibrated across models, so the claim that 'YOLO gives the best accuracy no matter the object' is unsupported. (3) The depth module has no quantitative evaluation in the supplied passages. It was trained on only 586 images (Sec. 6), and the authors describe the results only as 'decent' for nearby objects. (4) Minor inconsistency: the introduction says YOLO uses 'a single convolutional layer' to predict boxes, which is inaccurate. (5) No end-to-end system timing or runtime platform is given, so real-time feasibility is not shown. The single row records the Table I YOLO confidence value with low confidence, and Faster RCNN and SSD appear as baselines.
