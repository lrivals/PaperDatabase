---
id: arxiv-2609.02219-hardware-accelerated-instance-segmentation-resource
fiche: done
date:
---

# Hardware-Accelerated Instance Segmentation for Resource-Constrained Space Robotics with Criticality Analysis

Siddhant Shete, Hilmi Dogu Kücüker, Udo Frese, Frank Kirchner, 2026, arXiv preprint. https://arxiv.org/abs/2609.02219
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

Critical reading (supplied passages only): The paper deploys a YOLOv8m instance-segmentation model for rocks and craters on a lunar micro-rover (LuNiS, compute budget under 10 W). The target is a Zynq UltraScale+ MPSoC with a DPUCZDX8G B4096 DPU, compiled with Vitis AI. To get the whole graph to compile, the authors swap SiLU for HardSwish, replace the attention element-wise multiply with an additive projection, and make tensor shapes static. Calibration uses AVIS, a label-free method that deterministically picks the top-K samples by activation variance, followed by INT8 PTQ with bias correction. Table II gives these mAP values: GPU FP32 0.802; INT8 with random calibration 0.749 (-6.6%); plus bias correction 0.768 (-4.2%); plus AVIS 0.786 (-2.0%, IoU 0.767). The 69.8% recovery figure is computed against the random-calibration loss. Hardware results: the CPU–DPU hybrid runs at 309 ms, 5.7 W and 1.76 J/frame. The CPU-only baseline is 537 ms, 4.46 J/frame (about 8.3 W implied). The GPU is 121 ms at 11.8 W. Caveats: (1) Table III was garbled in extraction and lost its latency column; latencies come from the prose, and the energy values match latency × power. (2) The paper does not say whether power is measured at board or chip level. The GPU model is not named. The mAP IoU threshold and test-set size are not given. (3) The criticality section assumes a 1.2 s inference cycle, which does not match the reported 309 ms. (4) The operational margin is described for an 'X Rover' profile, which looks like an anonymization leftover. (5) The claim that AVIS halves calibration data is not backed by a table here. (6) No FPGA resource use (LUT/DSP/BRAM) is reported, and FPS is not given directly. (7) Results sit under the IV. METHODOLOGY heading because section V was not detected during extraction. (8) The 31.7% criticality reduction comes from a relative ranking model (occurrence × severity), not from radiation testing. Metadata was auto-extracted and flagged for manual check.
