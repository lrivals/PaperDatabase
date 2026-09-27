---
id: arxiv-2609.24757-npu-accelerator-quantized-real-time
fiche: done
date:
---

# NPU Accelerator: Quantized Real-Time Vehicle Detection on PYNQ-Z1 Using FINN

Daniel Gutierrez, Antonio Cuesta, Jorge Fe, Bruno Gutierrez, Rashed Al Koutayni, 2026, arXiv preprint. https://arxiv.org/abs/2609.24757
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

Critical reading: the paper deploys FINN streaming YOLO-style detectors (LP-YOLO w4a4 320×320, LP-YOLO Slim w2a4 256×256, and a custom YOLOv3-tiny w4a4 reference) on a PYNQ-Z1 (Zynq XC7Z020). The flow is Brevitas QAT → QONNX → FINN → Vivado. Four requirements must all pass at once: more than 30 FPS, more than 7 FPS/W, PL latency under 50 ms, and VOC mAP@0.5 above 0.55. Only LP-YOLO Slim at 142.86 MHz meets all four: 35.66 FPS, 2.91 W, 12.25 FPS/W, 45.11 ms PL latency, 49.77 ms end-to-end latency, and 0.594 VOC mAP.

Strengths: the numbers are measured on the board (batch 100, power at the 12 V input rail, so it is board-level). The paper keeps FINN estimates separate from measurements; for example, FINN estimated 38 FPS but the board measured about 22 FPS. It also reports PL and end-to-end latency separately, and the end-to-end overhead is about 4.65 ms.

Caveats:
(1) The 0.594 mAP for the 142.86 MHz design was not re-measured. It is carried over from the 125 MHz run because 'the model is unchanged'.
(2) Accuracy is the tightest requirement, only 0.044 above the 0.55 threshold.
(3) The Table I text is garbled. The CLK/Batch column and the 125 MHz Slim row are missing, and the YOLOv3-tiny clock is not given.
(4) No LUT/DSP/BRAM use or GOPS figures are reported, even though the paper discusses resource limits.
(5) The two best hardware results (200 MHz and manual-FIFO LP-YOLO) have no mAP.
(6) The QAT claim (within 0.006 mAP of floating point) was shown on YOLOv3-tiny, not on the deployed w2a4 Slim model.
(7) The COCO numbers use a 'filtered' board-test protocol re-measured in Aug. 2026, so their provenance differs.
(8) The paper cites Section VII-D, and the extraction flags Section VI as undetected, so some content may be missing.
(9) Wording such as 'supplied table' suggests the text was derived from a project report.

For the rows: latency_ms is the HW-PL latency (end-to-end latency is 49.77 ms at 142.86 MHz and 56.13 ms at 125 MHz). FPS is sustained throughput at batch 100.
