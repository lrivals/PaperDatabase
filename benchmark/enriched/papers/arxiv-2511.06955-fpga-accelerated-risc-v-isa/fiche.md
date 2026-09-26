---
id: arxiv-2511.06955-fpga-accelerated-risc-v-isa
fiche: done
date:
---

# FPGA-Accelerated RISC-V ISA Extensions for Efficient Neural Network Inference on Edge Devices

Arya Parameshwara, Santosh Hanamappa Mokashi, 2025, arXiv preprint. https://arxiv.org/abs/2511.06955
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

Critical reading note (arXiv 2511.06955, Parameshwara & Mokashi, 2025). Claim: custom "RISC-V ISA extensions" (FPGA.VCONV, FPGA.GEMM, FPGA.RELU, FPGA.CUSTOM) backed by FPGA accelerators on a PYNQ-Z2 (Zynq-7020) give an average 2.14× speedup and a 49.1% energy reduction over an ARM Cortex-A9 baseline on MobileNet V2, ResNet-18, EfficientNet Lite and YOLO Tiny. The baseline is GCC 11.2 -O3 with NEON and ARM Compute Library v23.02 at a fixed 666 MHz. The accelerators use INT16 fixed point (Q8.8 activations, Q12.4 weights) with per-tensor calibration on 1,000 ImageNet/COCO samples. Per-extension speedups: VCONV 7.2×, GEMM 4.2×, RELU 3.0×. VCONV accounts for 60–75% of saved time.

Problems to check before using any numbers:
(1) Architecture is unclear. The title says RISC-V, but the system diagram shows an ARM Cortex-A9 @ 650 MHz driving FPGA accelerators, and VCONV is said to replace about 800 ARM instructions. It is not clear what actually runs the custom instructions.
(2) Resource figures don't agree. The base core is listed as 229 LUTs (0.43%), 0 DSPs and 16×36 Kb BRAM. That BRAM is reported as "256 KB, 5.2%", but 16×36 Kb is about 72 KB, and 16 of 140 blocks is about 11%. The text also mentions a separate 64 KB BRAM. "4.9 MB total" should be 4.9 Mb. The integrated bitstream uses 9.6% LUTs, 8.2% FFs, 40.7% BRAM and 43.6% DSPs (96 of 220, which is consistent). This makes the "0.43% LUTs, minimal resources" claim misleading.
(3) The core and accelerator both run at only 50 MHz, while the CPU runs at 666 MHz.
(4) The accuracy loss is exactly −0.1% for every model, including YOLO Tiny mAP. The FP32 and INT16 absolute values were not in the supplied text.
(5) The statistics don't add up. "15 runs × 2 configurations = 60 inferences" doesn't match 4 models, which would be 120. A single t(14) is reported for all models combined.
(6) Tables III–XI were not in the supplied passages (captions only). So there are no per-model latency, energy, FPS or GOPS values; the table cells are n/r.

Power: 1.85–2.14 W measured with onboard sensors (INA226, 1 kHz). The 1.85 W idle power is subtracted when computing energy.

Toolflow: not stated.
