---
id: arxiv-2501.01511-treelut-efficient-alternative-deep-neural
fiche: done
date:
---

# TreeLUT: An Efficient Alternative to Deep Neural Networks for Inference Acceleration Using Gradient Boosted Decision Trees

Alireza Khataei, Kia Bazargan, 2025, arXiv preprint. https://arxiv.org/abs/2501.01511
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

TreeLUT (Khataei & Bazargan, FPGA '25; the metadata says arXiv preprint, but the passages cite the FPGA '25 proceedings) is an open-source Python tool. It trains XGBoost gradient-boosted decision trees on inputs quantized before training (min-max normalization to w_feature bits), quantizes the leaves to w_tree bits using per-tree min shifts and a global scale, and writes Verilog directly without HLS. The design is a fully unrolled 3-layer architecture (key-generator comparators, then MUX-based trees, then adder trees). Pipelining is controlled by [p0,p1,p2] to reach II=1. It is evaluated on MNIST, JSC and NID using post-place&route Vivado results, with accuracy from post-implementation functional simulation. Claimed results: on MNIST, about 97% accuracy with 4.2x to 101x lower area-delay product than LUT-based neural networks (18.4x vs PolyLUT-Add for TreeLUT (II); 881.5x vs POLYBiNN (I)); on JSC, 471.9x lower area-delay product than hls4ml (Fahim et al.), which uses 38 DSPs; on NID, 2.7x vs Alsharari et al. (II).

Caveats:
(1) The baseline numbers are quoted from the original papers, not re-run. They mix post-synthesis and post-place&route results and probably different FPGA parts. The baseline for each dataset was chosen as the one closest in accuracy, which is a selection that favors TreeLUT.
(2) The target FPGA device is not named in the supplied passages.
(3) Table 5 rounds accuracies to whole percentages. Precise values come from Tables 2 and 3.
(4) There is an inconsistency: the DWN comparison (Table 6) gives TreeLUT MNIST at 96.6% with 2,278 LUTs, while Table 5 gives TreeLUT (I) at about 97% with 4,478 LUTs. This suggests a different device or setup that the passages do not explain.
(5) The table extraction is garbled. Fmax, latency, FF and some LUT values are missing, and area x delay (LUT x ns) is reported instead of latency. Latency was not derived.
(6) Only area-delay product is compared. There is no power or energy data.
(7) The DSP and BRAM values of 0 come from the abstract's statement that the design uses no BRAMs or DSPs. The table cells for those columns were not recovered.
(8) On NID, accuracy after quantization (92.7) is higher than before (92.0), which may be test-set noise.
