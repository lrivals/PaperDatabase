---
id: arxiv-2502.15737-performance-analysis-you-only-look
fiche: done
date:
---

# A Performance Analysis of You Only Look Once Models for Deployment on Constrained Computational Edge Devices in Drone Applications

Lucas Rey, Ana M Bernardos, Andrzej D Dobrzycki, David Carramiñana, Luca Bergesio, Juan A Besada, José Ramón Casar, 2025, Electronics 2025, 14(3), 638. https://doi.org/10.3390/electronics14030638
Type : article de journal

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

GPU/CPU edge benchmark, not FPGA: YOLOv8n/s with post-training quantization (FP32/FP16/INT8 via TensorRT; the RPi5 runs FP32 only via NCNN) on Jetson Orin Nano, Orin NX and Raspberry Pi 5. Detection is single-target (TurtleBot robots) on an in-house indoor drone dataset of 6000 images at 640x640. Because the task is this easy, the mAP50-95 values (about 0.72–0.86) do not transfer to real UAV scenes. INT8 costs a lot of accuracy: YOLOv8n mAP50-95 drops from 0.8422 to 0.7190 on the Orin Nano. In return, the Orin NX reaches 65.83 FPS and 0.179 J/inference.

Problems found:
(1) The power column in Table 4 is labelled 'Energy Consumption (W•s)' but the text treats it as mean power in W. The measurement scope (board vs. module, and which sensor) is not described.
(2) The text says the Orin Nano's power rises from 7.4 W (FP32) to 8.7 W (INT8). Table 4 shows the opposite direction: 8.790 for YOLOv8s FP32 and 7.483 for YOLOv8n INT8.
(3) Inferences per minute do not match FPS. For example, 3443 inferences/min is about 57.4/s, while the reported speed is 65.83 FPS. So the energy-per-inference figure (EPI = power×60/IPM) and FPS come from different measurements.
(4) The 35.09 ms edge round-trip time in Table 6 is attributed to the Orin Nano with YOLOv8s FP16. In Table 5, however, 35.09 ms is the Orin NX value; the Orin Nano with YOLOv8s FP16 is 49.44 ms.
(5) Table 7 gives mAP50 as 0.7190 for NX YOLOv8n INT8. In Table 4, 0.7190 is the mAP50-95 value; mAP50 is 0.8276.
(6) The '52 FPS' in the abstract is the FP32 result on the Orin NX (52.19).
(7) Mean iteration times in the text are 15.16 ms (NX) and 23.16 ms (Nano) for YOLOv8n INT8. They are not directly comparable to Table 4 FPS or the testbed processing times (14.29 ms and 20.54 ms).
(8) The Raspberry Pi 5 could not complete the realistic testbed runs.

The rows below take the clean, unmerged Table 4 lines. Confidence is medium because the extracted table is partly garbled and the power units are unclear.
