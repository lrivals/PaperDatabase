---
id: arxiv-2405.03715-iterative-filter-pruning-concatenation-cnn
fiche: done
date:
---

# Iterative Filter Pruning for Concatenation-based CNN Architectures

Svetlana Pavlitska, Oliver Bagge, Federico Peccia, Toghrul Mammadov, J. Marius Zöllner, 2024, arXiv preprint. https://arxiv.org/abs/2405.03715
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

Critical reading: the paper proposes a connectivity-graph method for structured filter pruning that handles concatenation layers. Layers and pruning rates are chosen iteratively by sensitivity analysis (V = x·y^a over FLOPs or params and mAP), then the model is fine-tuned. It is applied to YOLOv7 and YOLOv7-tiny on COCO, with 14 pruning iterations. The smallest-L2 criterion works best, and pruning before BN fusion is much better than after.

Hardware: RocketChip + 32x32 Gemmini at 150 MHz with 2048 kB L2 on a ZCU102, via TFLite int8 → TVM/microTVM. The same models also run through TVM on a Jetson AGX Xavier.

Caveats:
(1) The measured FPS pair is for YOLOv7-tiny_RELU6, not the original model: SiLU is replaced by ReLU6 and the input drops to 480x480. Unpruned mAP falls from 0.360 to 0.331. The pruned model's mAP is only shown in figures, so accuracy is n/r.
(2) The reported speedup percentages don't match the FPS numbers. FPGA 7.78→14.06 FPS is a 45% latency cut (or +81% throughput), but the text says 37% for tiny and 45% for YOLOv7. Jetson 4.02→6.92 FPS is a 42% latency cut, but the text says 64%. The definition of "speedup" is unclear.
(3) The abstract's "2x speedup for convolutional layers" conflicts with the 54%/40% FPGA conv-layer figures.
(4) Calling 14 FPS "real-time" is generous.
(5) The Jetson is slower than a 150 MHz soft-SoC, which suggests the TVM target on the Jetson was not tuned or not GPU-optimized. It's unclear whether int8 applies to the Jetson.
(6) No power, resource use (LUT/DSP/BRAM) or YOLOv7 FPS numbers are given in the text. The up-to-80% sparsity claim is only shown in figures.
(7) The extraction is flagged ok=false and the metadata needs checking by hand.
