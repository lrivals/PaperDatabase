---
id: arxiv-2309.01587-satay-streaming-architecture-toolflow-accelerating
fiche: done
date:
---

# SATAY: A Streaming Architecture Toolflow for Accelerating YOLO Models on FPGA Devices

Alexander Montgomerie-Corcoran, Petros Toupas, Zhewen Yu, Christos-Savvas Bouganis, 2023, arXiv preprint. https://arxiv.org/abs/2309.01587
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

SATAY (Imperial College London, arXiv 2309.01587, 2023) is a toolflow that turns YOLO ONNX models into streaming FPGA accelerators. It uses SAMO as its base and Vivado 2020.1 for synthesis. The design is a deeply pipelined dataflow architecture: every layer gets its own hardware block, and all weights stay on-chip in URAM/BRAM. New blocks handle YOLO-specific operations (Resize, HardSwish, Leaky ReLU, Split/Concat/Add). Long skip connections are buffered in off-chip memory through a software FIFO, and fine-grained quantization (W8A16 in Table III) reduces on-chip memory use. The paper evaluates YOLOv3, YOLOv5 and YOLOv8 on U250, ZCU104, VCU110 and VCU118, and says this is the first FPGA implementation of YOLOv8.

Claims in the text:
- The YOLOv8s VCU110 design has 8% higher GOP/s/DSP than the next-best fixed-point accelerator.
- GOP/s/DSP is 1.1–3.4× higher on YOLOv3-tiny than [10], [34], [35], and 7.3× higher on YOLOv5s than [26].
- Speed-up averages 79× over an ARM Cortex-A72 and 3.6× over a Jetson TX2, using FPGA designs picked for similar energy.
- ZCU104 performs much better than the Jetson TX2 at similar power (Table IV).

Critical points:
1. The extracted Tables III and IV are garbled. Their numbers (LUT, DSP, BRAM, latency, power, GOP/s, mAP) cannot be matched reliably to model/device columns, so every absolute metric below is n/r.
2. The 1.1–3.4× and 3.6× figures are ranges or averages over hand-picked comparison points. Choosing FPGA designs by matching energy is a comparison method the authors picked themselves.
3. GOP/s/DSP rewards designs that use LUT-based arithmetic, and the binarized design [8] still has higher efficiency.
4. Accuracy is reported as mAP50 on COCO 2017 val in Table III but mAP50-95 in Fig. 10, and prior works use different datasets (for example, PASCAL VOC for [8]). This limits how comparable the numbers are.
5. It is unclear whether the power numbers are board-level or chip-level.
6. The metadata extraction is flagged for manual checking.
7. Recover the Table III/IV values from the original PDF before filling in any absolute numbers.
