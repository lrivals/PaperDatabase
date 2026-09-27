---
id: arxiv-2003.03852-low-precision-floating-point-arithmetic
fiche: done
date:
---

# Low Precision Floating-point Arithmetic for High Performance FPGA-based CNN Acceleration

Chen Wu, Mingyu Wang, Xinyuan Chu, Kun Wang, Lei He, 2020, arXiv preprint. https://arxiv.org/abs/2003.03852
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

Wu et al. (UCLA, arXiv 2003.03852, 2020) propose an 8-bit low-precision floating-point (LPFP) quantization that needs no retraining. It uses an MaEb format with M4E3 on hardware (M5E2 was the most accurate in emulation) and a per-layer scaling factor chosen to minimise MSE. They also build a Kintex-7 KC705 processor that fits four 8-bit LPFP multiplications into one DSP: each multiplication is reduced to one 4-bit MAC plus one 3-bit adder. Products are M10E4 values converted losslessly to fixed point, so accumulation is done in fixed point.

Claims made in the supplied text:
- Average top-1 loss of 0.5 or less and top-5 loss of 0.3 or less against FP32 on ImageNet, across six CNNs (AlexNet, VGG16, ResNet50/101/152, DenseNet201). These figures come from software emulation in Darknet, not from runs on the FPGA.
- An average throughput of 1100.4 GOPS, or 1.43 GOPS/DSP.
- Speedups of 64.5× over an Intel i9 CPU and 1.5× over existing FPGA accelerators.
- For VGG16 and YOLO against six prior accelerators, average throughput gains of 3.5× and 27.5×, and per-DSP gains of 4.1× and 5×.

Limitations for critical reading:
1. The passages give Tables I and III–VII by caption only, so per-model FPS, latency, power, LUT/DSP/BRAM use (Table IV, XC7K325T) and the absolute YOLO numbers cannot be extracted.
2. The 1100.4 GOPS figure is an average across networks that have very different GOP counts. No per-model result is given.
3. The YOLO comparison gives only relative ratios. It is unclear which YOLO version, dataset or accuracy was used, and no detection accuracy is reported.
4. The accuracy figures come from emulated quantization run on the CPU and GPU, not from outputs measured on the FPGA.
5. Power and energy efficiency are not stated in the supplied text.
6. The accuracy loss is given as an upper bound ("within"), not as an exact average.

Metadata flags the extraction as incomplete: Section V was merged into the preceding section.
