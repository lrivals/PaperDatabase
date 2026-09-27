---
id: arxiv-2508.21493-sira-scaled-integer-range-analysis
fiche: done
date:
---

# SIRA: Scaled-Integer Range Analysis for Optimizing FPGA Dataflow Neural Network Accelerators

Yaman Umuroglu, Christoph Berganski, Felix Jentzsch, Michal Danilowicz, Tomasz Kryjak, Charalampos Bezaitis, Magnus Sjalander, Ian Colbert, Thomas Preusser, Jakoba Petri-Koenig, Michaela Blott, 2025, arXiv preprint. https://arxiv.org/abs/2508.21493
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

SIRA (Umuroglu et al., arXiv 2508.21493, preprint) is a static analysis pass. It uses interval arithmetic to find the range, scale and bias of every tensor in a QONNX graph. It works one node at a time, with separate propagation rules for Quant, Add, Mul and MatMul/Conv. Scales and biases only pass through affine regions. MatMul needs weight/activation scaling that is at most per-channel, and the weights must have zero bias. The authors use this information in FINN in three ways: (i) collapsing scales and biases into one aggregated Mul/Add, so MatMul runs on pure integers; (ii) shrinking accumulators without losing accuracy; and (iii) a generic version of streamlining that turns layer tails into multi-thresholding. It fixes four stated gaps in the original streamlining work by Umuroglu & Jahre: no concrete algorithm, only one conversion example, a dependence on a later thresholding step, and no analysis of trade-offs.

Motivation (Table 1): a 3-bit ResNet-8 on CIFAR-100 loses more than 2 percentage points with the least expressive scale factors compared with the most expressive. The float32 reference is 70.52.

Headline result (abstract): on average across the QONNX model-zoo workloads, SIRA cuts LUTs by 17%, DSPs by 66% and accumulator bitwidth by 22%.

Critical points:
- The supplied passages give only the captions of Tables 5–8, not their values. So there are no per-model LUT/DSP/BRAM/FPS figures, no FPGA part, and no power figure here.
- The results come from out-of-context synthesis, not board measurements.
- Interval bounds can be loose because of the dependency problem.
- Thresholding cost grows exponentially with activation bitwidth. Table 7 shows cases where thresholds use more LUTs than float operations. So SIRA does not always help.
- Whether fixed-point aggregated scales cost any accuracy is not quantified in these passages.

Before trusting this row, check it against Table 6.
