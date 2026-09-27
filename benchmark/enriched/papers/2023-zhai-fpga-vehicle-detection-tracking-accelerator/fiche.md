---
id: 2023-zhai-fpga-vehicle-detection-tracking-accelerator
fiche: done
date:
---

# FPGA-Based Vehicle Detection and Tracking Accelerator

Jiaqi Zhai, Bin Li, Shunsen Lv, Qinglei Zhou, 2023, Sensors 23(4), 2208. https://doi.org/10.3390/s23042208
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

Zhai et al. (Sensors 2023) build a Zynq-7000 accelerator that runs pruned YOLOv3 and YOLOv3-tiny for vehicle detection, with DeepSORT tracking on the host CPU. The models are compressed with binary-search dynamic-threshold structured pruning plus knowledge distillation. They are then quantised to dynamic 16-bit fixed point, choosing Q per layer for weights, activations and intermediate results. Memory is reused between layers, weights are reordered in advance, and transfers use ping-pong double buffering. Software can switch between the two models depending on traffic.

Headline result (Table 8, Fixed-16 at 230 MHz): YOLOv3-tiny reaches 91.65 fps and 67.91 GOP/s at 12.51 W full power (1.31 W dynamic), with mAP 0.599 on UA-DETRAC. YOLOv3 reaches 3.23 fps and 63.51 GOP/s at 0.711 mAP.

Caveats:
(1) Table 8 gives only two resource columns for 'This Work'. I matched them to the Float-32 and Fixed-16 designs because they line up with the dual-core figures in Table 9 (DSPs 602 ≈ 2×301; BRAM 263 ≈ 2×132.5). Each design appears to be shared by both models, so both rows use the same resource values. This alignment is my inference, not stated in the paper.
(2) mAP is identical for Float-32 and Fixed-16 (0.711 / 0.599). Either quantisation caused no loss, or accuracy was not measured separately for each precision.
(3) YOLOv3-tiny is listed at 0.735 GOP, which suggests a pruned model. The CPU and GPU baselines in Table 7 use the same 0.735 GOP, but the pruned vs. unpruned status of each comparison is unclear.
(4) The exact Zynq part is not named. Full-power measurement is not described, so its scope may be board or SoC. The fps figures probably leave out host-side preprocessing, NMS and DeepSORT.
(5) Table 7 gives no power for Baseline3 (ZCU9EG) yet reports an efficiency of 3.71 GOPS/W.
(6) Table 9 reports a dual-core Fixed-16 setup with higher numbers (YOLOv3-tiny at 168.72 fps, 124.01 GOP/s, 15.18 W). These are not included as rows.
(7) Re-ID training (Table 6) improves tracking, e.g. IDF1 on MVI_40771 rises from 69.3 to 80.6.
