---
id: arxiv-2310.08401-performance-power-assessment-cnn-packages
fiche: done
date:
---

# Performance/power assessment of CNN packages on embedded automotive platforms

Paolo Burgio, Gianluca Brilli, 2023, arXiv preprint. https://arxiv.org/abs/2310.08401
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

Burgio & Brilli (arXiv 2310.08401) compare how YOLO v2/v3 (full and tiny) and AlexNet perform on NVIDIA Jetson boards (Xavier AGX, TX2, Nano) and on Xilinx Zynq UltraScale+ boards (ZCU102/XCZU9EG and Ultra96, which the abstract suggests is the XCZU3EG). The FPGA networks use INT8, sometimes with pruning, via the Xilinx SDK flow. The GPUs use TensorRT without pruning.

Critical reading:
(1) The text extraction lost almost every table number. Only mAP percentages survive. E2E latency, board and SoC power, power efficiency and FPS values for Tables I–XII are missing. The paper says the FPGA boards are at least twice as power-efficient as the GPUs and that TX2 beats Xavier, but none of those numbers can be checked from these passages.
(2) Rows below are limited to the recoverable FPGA mAP for YOLO v2 on VOC with INT8 (Table IX/X baseline row). The values are Ultra96 63.78 and ZCU102 64.56. The column-to-board order is confirmed by the consolidated passage "Ultra96 63.78% ZCU102 64.56%". Oddly, the INT8 FPGA mAP is higher than the GPU floating-point mAP (about 58.8). The paper does not explain this beyond "low-level optimizations", which suggests the models or preprocessing differ rather than it being a pure effect of quantization.
(3) Pruned variants on the same pair of boards (Ultra96 first, then ZCU102): 22g 62.94/63.10, 24g 61.41/61.96, 26g 61.59/61.25. The claim that pruning gives efficiency "for free" can't be checked without the missing power and throughput numbers.
(4) Tiny YOLO v3 on the FPGAs reaches only 4.6 mAP (COCO), which makes it close to useless in practice. YOLO v3 on Berkeley has two FPGA variants, (A) 19.44 and (B) 55.20, and the text does not define them clearly.
(5) Batching tests used YOLO v3 on COCO. The ZCU102 scales up to 4–8 threads, while the Ultra96 is already saturated. The 500 and 2500 FPS at 13 and 25 W figures are for AlexNet classification on TX2 and Xavier, not the FPGAs.
(6) The metadata is flagged as unverified, table references are garbled ("Table VI-A" and similar), and there is no DOI or venue. Treat all extracted values as medium confidence and check them against the PDF.
