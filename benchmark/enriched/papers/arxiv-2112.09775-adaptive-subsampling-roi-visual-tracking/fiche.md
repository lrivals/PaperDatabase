---
id: arxiv-2112.09775-adaptive-subsampling-roi-visual-tracking
fiche: done
date:
---

# Adaptive Subsampling for ROI-based Visual Tracking: Algorithms and FPGA Implementation

Odrika Iqbal, Victor Isaac Torres Muro, Sameeksha Katoch, Andreas Spanias, Suren Jayasuriya, 2021, arXiv preprint. https://arxiv.org/abs/2112.09775
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

What the paper claims: it uses an object detector together with a Kalman filter (KF) to predict where the region of interest (ROI) will be in the next frame. The image sensor then reads out only that ROI, which saves sensor power. The authors compared MS, KCF, DAT, YOLO, Tiny-YOLO, ECO, ATOM and DiMP, each with and without the KF, on OTB100 (100 videos) and the LaSOT test split (280 videos). They report AUC at IoU@[0:0.05:1] with a keyframe every 11 frames. DiMP+KF scored best (0.4817 on OTB100, 0.4702 on LaSOT). ECO+KF (0.4568 and 0.3471) was chosen for the FPGA because ATOM and DiMP use custom layers that Vitis AI does not support. ECO's VGG feature extractor was quantised to INT8 with the Vitis AI (VAI) quantiser and compiled for the DPU on a ZCU102 board. The Kalman filter, preprocessing and ROI masking run in Python on the ARM cores. YOLOv3+KF, a VAI model-zoo model (yolov3 tf voc), was also accelerated for comparison.

Caveats:
1. The only measured hardware number in the supplied passages is ECO+KF at 19.23 FPS. The passages give no clock, batch size, resolution or end-to-end/DPU breakdown. They only say YOLO+KF is "faster" and give no number. The contents of Table III (hardware performance) and Table IV (resources) are not in the passages, so LUT, DSP, BRAM, latency and GOPS are n/r.
2. The AUC values are software results using full-precision pre-trained networks. They were not re-measured after INT8 quantisation on the FPGA.
3. The ~4 W (ECO) and ~6 W (YOLO) figures come from an analytical CMOS image-sensor readout model, not from FPGA board measurements. They are therefore left out of power_w.
4. The ROI is simulated digitally, because no ROI-programmable camera was available. The actual sensor power savings are not measured.
5. The YOLO accuracy in Table I cites [53] without a version number. That it matches the deployed YOLOv3 is an assumption.
6. Only pre-trained networks were used. The authors themselves suggest that the gap between OTB100 and LaSOT results may come from not fine-tuning on LaSOT.
