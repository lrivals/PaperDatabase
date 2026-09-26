---
id: arxiv-1711.08740-fpgaconvnet-toolflow-mapping-diverse-convolutional
fiche: done
date:
---

# fpgaConvNet: A Toolflow for Mapping Diverse Convolutional Neural Networks on Embedded FPGAs

Stylianos I Venieris, Christos-Savvas Bouganis, 2017, NIPS 2017 Workshop on Machine Learning on the Phone and other Consumer Devices. https://arxiv.org/abs/1711.08740
Type : conférence

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

fpgaConvNet (NIPS 2017 MLPCD workshop; toolflow version, not the FCCM 2016 paper) maps Caffe ConvNets to streaming FPGA accelerators. It models each design as a Synchronous Dataflow graph, using a topology matrix and a workload matrix. Design space exploration is treated as an optimisation problem using four transformations: graph partitioning with full reconfiguration (for throughput, with batching to hide the reconfiguration cost), coarse-grained folding, fine-grained folding, and weights reloading (for latency, using one flexible architecture instead of reconfiguring). The paper also claims the first FPGA mapping of DenseNet-161.

Evaluation: Zynq 7045 (FXP16, 125 MHz) versus Tegra X1 (TensorRT, cuDNN v6, FP16) on AlexNet, VGG16, GoogLeNet and DenseNet-161. Power was measured with a power monitor, with idle power subtracted.

Results, with both platforms held to a 5 W budget (GPU clocked down to 76.8 MHz):
- Throughput-driven: up to 5.53x faster than the GPU, average 3.32x, geometric mean 3.07x.
- Latency-driven: up to 6.65x, average 3.95x, geometric mean 3.43x.
- Against the GPU at its full 998 MHz, GOp/s/W improves 1.17x for throughput-driven (geo. mean 1.12x) and 1.70x for latency-driven (geo. mean 1.36x).

Weaknesses:
- The text reports only speed-up ratios. Absolute throughput, latency and GOp/s for each network are only in Fig. 3, which was not supplied.
- The 270 GOp/s (FPGA) and 79 GFLOPS (GPU) figures are theoretical peaks, not measurements.
- No FPGA resource use (LUTs, DSPs, BRAM) and no accuracy impact of FXP16 are reported.
- The GPU is heavily throttled for the 5 W comparison, which favours the FPGA. Its memory bandwidth (12.8 GB/s) is also far higher than the FPGA's (4.2 GB/s).
- The latency-driven comparison is reported as 'throughput improvement', so the latency metric is unclear.
- The rows below are cross-benchmark aggregates. The 5 W value is the configured power budget, not a measured draw.
