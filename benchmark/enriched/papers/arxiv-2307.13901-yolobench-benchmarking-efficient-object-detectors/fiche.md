---
id: arxiv-2307.13901-yolobench-benchmarking-efficient-object-detectors
fiche: done
date:
---

# YOLOBench: Benchmarking Efficient Object Detectors on Embedded Systems

Ivan Lazarevich, Matteo Grimaldi, Ravish Kumar, Saptarshi Mitra, Shahrukh Khan, Sudhakar Sah, 2023, arXiv preprint. https://arxiv.org/abs/2307.13901
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

YOLOBench (Deeplite, arXiv 2307.13901) benchmarks 550+ YOLO-based detectors. The models combine YOLOv3–v8 backbones and necks with depth factors {0.33, 0.67, 1.0}, width factors {0.25–1.0} and input resolutions from 160 to 480 in steps of 32. They are tested on 4 datasets (VOC, SKU-110k, WIDERFACE, COCO) and 4 embedded devices: Jetson Nano GPU (ONNX Runtime FP32), Khadas VIM3 NPU (INT16), Raspberry Pi 4 CPU (TFLite/XNNPACK) and an Intel CPU. All models share a fixed YOLOv8 anchor-free head, the same losses and the same Ultralytics training pipeline, so differences come only from the backbone and neck.

Main findings:
- Which models are Pareto-optimal depends on the device. VIM3 favours YOLOv6. The CPUs mix YOLOv5 and YOLOv7. The Jetson Nano is the most heterogeneous.
- With modern heads and training, older YOLOv3 and YOLOv4 backbones can still reach competitive trade-offs.
- In optimal models, depth and width are reduced before input resolution.
- Most zero-cost NAS proxies do worse than MAC count, but pre-activation NWOT helps predict Pareto-optimal models. Using it, the authors found YOLO-FBNetV3-D-PAN-C3, which they report is faster and more accurate than YOLOv8s and YOLOv8s-HSwish on Raspberry Pi 4 (TFLite FP32, 640x640, COCO).

Caveats:
- This is not an FPGA paper. There are no LUT, DSP or BRAM figures, no power measurements and no GOPS.
- The Table 4 text was garbled during extraction. Only the standard deviations survived (latency ±1.49, ±7.34, ±9.93 ms; mAP ±0.00–0.23%), so the mean latency and mAP values are recorded as n/r.
- Table 1 latencies (0.1, 0.05 and 0.5 s) are selection thresholds, not measurements.
- The authors say their YOLOv8s baseline scores slightly below Ultralytics' published numbers.
- The Intel CPU runtime is cut off in the supplied text.
- The metadata is flagged for manual verification.
