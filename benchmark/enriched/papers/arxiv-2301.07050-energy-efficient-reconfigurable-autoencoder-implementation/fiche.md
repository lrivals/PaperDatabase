---
id: arxiv-2301.07050-energy-efficient-reconfigurable-autoencoder-implementation
fiche: done
date:
---

# An Energy-Efficient Reconfigurable Autoencoder Implementation on FPGA

Murat Isik, Matthew Oldland, Lifeng Zhou, 2023, arXiv preprint. https://arxiv.org/abs/2301.07050
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

Convolutional denoising autoencoder with 3 conv and 3 max-pool encoder layers, and 4 conv and 3 up-sample decoder layers. Inputs are 28x28x1 MNIST images with added Gaussian noise. The authors wrote the design in VHDL and ran it on a Xilinx XCZU7EV (504K LUTs) using Vivado 2021.1. They compared it with a Python/Colab implementation on an NVIDIA Tesla K80.

Headline FPGA result: 21.12 GOP/s at 100 MHz with 5.93 W on-chip power, 2.91 ms latency, and 3.56 GOP/s/W. The 3.56 figure matches 21.12 / 5.93.

Critical points:
(1) The paper does not say whether the 5.93 W is measured or a Vivado power-report estimate.
(2) No LUT, DSP or BRAM usage is given; only the device's total LUT count is stated. Arithmetic precision and quantization are also not given.
(3) Accuracy is poorly defined for a denoising task. The paper reports both 80% and a best value of 80.83%, and mentions a confusion matrix without explaining how accuracy was computed.
(4) Table II mixes different workloads. For example, Zhang et al. [5] and other prior FPGA CNN accelerators are not running the same autoencoder, so the claimed energy-efficiency advantage is not a like-for-like comparison.
(5) The K80 row in Table II looks internally inconsistent. The K80 is labelled 'ASIC (28nm)', with 1.48 GHz, 30 W, 1137.62 ms and 22000 GOP/s. That throughput and latency do not fit together, and the K80 shows 733 GOP/s/W, far more efficient than the FPGA, which contradicts the paper's claim of an efficiency advantage.
(6) The paper does not describe the GTX 1080 Ti row anywhere else.

FPS is not reported; it has not been derived from latency.
