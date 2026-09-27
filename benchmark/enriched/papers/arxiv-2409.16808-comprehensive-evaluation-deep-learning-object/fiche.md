---
id: arxiv-2409.16808-comprehensive-evaluation-deep-learning-object
fiche: done
date:
---

# A Comprehensive Evaluation of Deep Learning Object Detection Models on Heterogeneous Edge Devices

Daghash K Alqahtani, Muhammad Aamir Cheema, Maria A Rodriguez, Adel N Toosi, 2024, arXiv preprint. https://arxiv.org/abs/2409.16808
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

Empirical benchmark of 8 detectors (YOLOv8 n/s/m, EfficientDet Lite0-2, SSD MobileNet V1, SSDLite MobileDet) on 9 edge platforms (Pi 3/4/5 CPU-only, each Pi with Coral Edge TPU, Pi 5 with AI HAT+ (Hailo-8), Jetson Nano, Jetson Orin Nano). Accuracy is COCO val mAP (5,000 images, scored with FiftyOne). Latency is server-side service time in ms and excludes network delay. Energy is reported only as mWh per request above idle, from a UM25C USB meter, so there are no watt figures and power_w is n/r.

Points to check before reusing these numbers:
(1) The platforms don't use the same inputs. YOLOv8 runs at 320x320 on the TPU but 640x640 on CPU, Hailo and TensorRT, so TPU speedups mix hardware gains with the smaller input. The authors say this themselves, and TPU YOLOv8 mAP drops to 16/25/32.
(2) Quantization and precision are never stated for TFLite, Edge TPU, HailoRT or TensorRT. They matter because EfficientDet/SSD mAP drops on Hailo (Lite 17-24, SSD v1 17).
(3) Jetson Nano and Orin Nano report identical mAP, and the Jetson latency passage is cut off, so no Jetson latency figures are available here.
(4) Per-model values are often given only as ranges (e.g., YOLOv8 76-240 ms on Hailo), so I only took values explicitly tied to a single model.
(5) No FPS, GOPS or FPGA resource figures are reported (this is not an FPGA paper). Batch and concurrency settings from Locust are not given.

Row 1, Pi 5 + AI HAT+ running YOLOv8n: energy per request above idle is 0.2 mWh (Fig. 2(h)).
Row 2, Pi 4 + TPU running SSD v1: energy is 0.10 mWh per request, and the same model takes 209 ms on the CPU-only Pi 4.
