---
id: arxiv-2406.14239-leyolo-embedded-architecture-object-detection
fiche: done
date:
---

# LeYOLO, New Embedded Architecture for Object Detection

Lilian Hollard, Lucas Mohimont, Nathalie Gaveau, Luiz Angelo Steffenel, 2024, arXiv preprint. https://arxiv.org/abs/2406.14239
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

LeYOLO (arXiv 2406.14239) proposes LeNeck, a detection neck that works with any lightweight classifier, and LeYOLO (Nano to Large), a YOLO-style detector built for parameter and FLOP efficiency. Both are trained and evaluated on MSCOCO (mAP) with 4×P100 GPUs.

Critical points:
1. There is no FPGA work in these passages. The 'yolo-fpga' axis was assigned automatically and looks wrong: hardware results are on STM32 MPUs/MCUs (STM32MP257FAI3, STM32N6570-DK, STM32H7/F7/F4 DISCO boards).
2. PDF extraction failed for the tables. Tables IV–XI show only captions and headers, so no latency, mAP, FLOP or parameter values can be copied. Every numeric field is therefore n/r.
3. The text gives only qualitative or relative claims:
   - Real-time at 320×320.
   - Under 1 s per inference at 640×640 on STM32. This is an upper bound, not a measured value.
   - The optional-pointwise inverted bottleneck saves 8.5% inference time versus the classic inverted bottleneck.
   - An expansion ratio of 2 instead of 3 gives 17% faster inference (Table IX).
   - LeNeck is 'nearly as fast' as SSDLite with better mAP.
   - LeYOLO-Small 'matches' YOLOv8–v10 accuracy.
4. No power, energy or memory-footprint measurements are reported, even though the paper is framed around low power.
5. Quantization and deployment toolchain are not stated beyond 'ONNX' in the Table IV–VI captions. It is unclear whether the MCU runs used int8 (e.g., via STM32Cube.AI).
6. The title-page author list omits Gaveau, while the metadata includes them. This should be checked by hand.

Before these rows are used, the table values must be pulled from the original PDF.
