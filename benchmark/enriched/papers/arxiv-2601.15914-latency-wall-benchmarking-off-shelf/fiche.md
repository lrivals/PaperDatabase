---
id: arxiv-2601.15914-latency-wall-benchmarking-off-shelf
fiche: done
date:
---

# The Latency Wall: Benchmarking Off-the-Shelf Emotion Recognition for Real-Time Virtual Avatars

Yarin Benyamin, 2026, arXiv preprint. https://arxiv.org/abs/2601.15914
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

Critical reading: single-author technical report benchmarking off-the-shelf models for a two-stage pipeline (face detection, then 7-class zero-shot/pre-trained emotion classification) against a 140 ms motion-to-photon budget. The author calls this budget a heuristic, not a clinically validated threshold. All measurements are CPU-only on an unspecified 'standard i7 Laptop CPU'. The passages give no FPGA, power, LUT/DSP/BRAM, quantization or toolflow information, so the automatically inferred 'yolo-fpga' axis looks wrong and should be removed. The extracted tables lost their latency columns. Only YOLOv11n detection (53.96 ms) and ViT-FER classification (193.58 ms, from Eq. 2; ~247.54 ms combined, 1.9x the 130 ms AI budget) have exact latencies. The equation does not say which dataset the 193.58 ms was measured on. Accuracy: every detector reaches 100 on UIBVFED avatars, but on FER-2013 YOLOv11n drops to 21.59 and YOLOv12n to 35.18 (YOLOv8n 80.79, MTCNN 83.64). The paper does not define the detection 'accuracy' metric (no IoU threshold or mAP). Classification on avatars is near chance: ViT-FER 27.42, CLIP-L 22.88, SigLIP2 So400m 4.24, with a random-guess baseline of about 14.2. On human faces ViT-FER reaches 63.64. Limitations: no fine-tuning, no GPU or edge-accelerator comparison, no batch or thread settings, and latency variance is not reported.
