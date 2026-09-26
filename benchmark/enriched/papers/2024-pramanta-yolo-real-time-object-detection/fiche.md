---
id: 2024-pramanta-yolo-real-time-object-detection
fiche: done
date:
---

# YOLO real-time object detection on EV3-Robot using FPGA hardware Accelerator

Dinda Pramanta, Ninnart Fuengfusin, Arie Rachmad Syulistyo, Hakaru Tamukoh, 2024, Proceedings of International Conference on Artificial Life and Robotics. https://doi.org/10.5954/icarob.2024.os15-1
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

Critical reading (Pramanta et al., ICAROB 2024): A short system-integration paper. An EV3 educational robot acts as a Bluetooth socket server, and a local PC client runs YOLOv3 (COCO pre-trained weights, filtered to the 'person' class, class_id = 0) on frames from a wireless camera. The authors say they run the YOLO model on the deep-learning processor unit (DPU) of a Kria KV260 as the accelerator. Measured results: (1) command round-trip latency, defined as RTT/2, is reported only as 'below 1,000 ms' (the Table 1 values were not extracted). (2) Table 2 compares an i7-13700F with no accelerator (2.63 FPS, 270.3 ms inference) against the KV260 (3.78 FPS, 264.4 ms). Detection is marked 'Success' in both cases.

Weaknesses:
- Inference time improves only about 2%, yet FPS rises about 44%.
- 1000/264.4 ≈ 3.78, so the KV260 FPS matches its inference time. 1000/270.3 ≈ 3.70, not 2.63, so the CPU FPS probably includes pipeline or communication overhead that is not explained.
- The paper does not report quantization (the DPU implies INT8, but this is never stated), input resolution, accuracy/mAP, power, FPGA resources, DPU configuration or toolflow version.
- The evaluation is a single qualitative 'person' detection with no dataset-level metrics.
- It is unclear whether the camera stream travels over the network to the KV260, and whether the reported timing includes that transfer.

Metadata extraction was flagged for manual verification. Treat the benchmark rows as weak evidence.
