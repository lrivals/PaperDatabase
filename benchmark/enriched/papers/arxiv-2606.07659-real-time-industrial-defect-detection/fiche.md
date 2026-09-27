---
id: arxiv-2606.07659-real-time-industrial-defect-detection
fiche: done
date:
---

# Real-Time Industrial Defect Detection on Edge Hardware Using Fine-Tuned YOLOv8: A Systematic Benchmark on the NEU Surface Defect Database and MVTec AD with Automotive & Battery Manufacturing Extensions

Emmanuel Ezeji Somtochukwu, Nitesh Rijal, 2026, arXiv preprint. https://arxiv.org/abs/2606.07659
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

Critical reading: the paper benchmarks the four YOLOv8 variants (n/s/m/l) with supervised bounding-box detection on NEU-DET (6 classes, 1,440 train / 360 val) and MVTec AD (58 classes from 13 categories; masks converted to boxes; Cable and Capsule held out). The only measured hardware result is GPU latency on an NVIDIA Tesla T4 (Google Colab). NEU-DET: YOLOv8l 74.1 mAP@0.5 at 15.8 ms; YOLOv8n 73.6 at 2.1 ms. MVTec AD: YOLOv8m 72.4 at 11.8 ms; YOLOv8s 72.2 at 5.7 ms.

Caveats:
(1) There is no FPGA or edge-device measurement, even though the paper is tagged yolo-fpga. The 'Jetson est.' values carry a '~' and are estimates. The limitations section says Jetson Orin NX TensorRT INT8 results are pending hardware access. The T4 is a datacenter GPU, so the 'edge' framing is not backed by measurement.
(2) The latency protocol is not given: batch size, precision (FP32/FP16), and whether pre- and post-processing are included are all unstated. No FPS, power or throughput figures are reported.
(3) The headline 'ranking inversion' on MVTec AD rests on a 2.7pp spread across only 236 validation images, with 2–6 instances per class. Results come from a single run with no seeds or variance, so the inversion may be noise.
(4) Internal inconsistencies: the NEU-DET gap is given as both 0.5pp (abstract) and a 0.9pp range. The epoch count for NEU-DET is missing in Methodology (Table II caption says 50).
(5) The MVTec AD box protocol (contour extraction, <100px filtered) is custom. By the authors' own statement it is not comparable to AUROC-based anomaly detection results.
(6) The per-class finding is well argued: periodic-texture defects fail (crazing 50.6, grid_bent 4.9).
(7) Metadata needs checking: the author name is split inconsistently (Ezeji Emmanuel vs Somtochukwu), and the preamble title differs (no 'Battery').

The table text was garbled during extraction, so the rows use only the values stated in prose.
