---
id: 2022-feng-benchmark-analysis-yolo-performance-edge
fiche: done
date:
---

# Benchmark Analysis of YOLO Performance on Edge Intelligence Devices

Haogang Feng, Gaoze Mu, Shida Zhong, Peichang Zhang, Tao Yuan, 2022, Cryptography 6(2), 16. https://doi.org/10.3390/cryptography6020016
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

What the paper does: it benchmarks Darknet YOLO models on three edge boards: Jetson Nano, Jetson Xavier NX (6-core 15 W mode) and Raspberry Pi 4B with an Intel NCS2 (OpenVINO FP16 IR). The models are YOLOv3/v3-tiny at S=416 on all boards, YOLOv3/v3-tiny at S=320/608 on the Nano, and YOLOv4/v4-tiny at S=416 on the Nano. The test data is two videos from gitee: Video1 (1596 frames, 768×436) and Video2 (960 frames, 1920×1080). Weights are COCO-pretrained. Results are averaged over 10 runs. It is not an FPGA paper, so there are no LUT, DSP or BRAM figures and no GOPS.

Critical issues:
(1) Accuracy is reported only as 'mean confidence' (average score of correctly detected objects). There is no mAP and no ground truth is described, so these numbers are not comparable to standard detection accuracy.
(2) The text and tables disagree. The text and conclusion say YOLOv3-tiny scores 57.9 on Jetson, but Table 3 shows 59.7. The text also says Video1 has 960 frames, while the table note says 1596. The abstract claims NCS2 YOLOv3-tiny FPS is 7.6× YOLOv3; Table 3 gives 18.8/2.5 = 7.5.
(3) NCS2 YOLOv3-tiny runs at 18.8 FPS on Video1 but scores 0 mean confidence because the OpenVINO Model Optimizer broke the Region layer conversion. That FPS therefore does not represent a working detector.
(4) The toolflow on Jetson is unclear: Darknet is compiled on the device, but the paper also says 'GPU to compile TensorFlow'. TensorRT was deliberately not used, so the Jetson results understate what the hardware can do.
(5) The FP16 claim rests on a questionable rationale ('Nano only supports FP16'). How precision was enforced in Darknet is not described.
(6) Power scope is mixed. Table 3 'Power' comes from JTOP on the Jetsons and a USB meter on the RPi, so it is probably board-level but this is not stated. Tables 5–6 report GPU-rail power only. Idle power is not subtracted.
(7) Latency is not reported; only FPS and total time are given.
(8) The Table 3 extraction merges rows; the values below were separated by position, so they carry some risk of misreading.
