---
id: arxiv-2101.05108-fast-convolutional-neural-networks-fpgas
fiche: done
date:
---

# Fast convolutional neural networks on FPGAs with hls4ml

Thea Aarrestad, Vladimir Loncar, Nicolò Ghielmetti, Maurizio Pierini, Sioni Summers, Jennifer Ngadiuba, Christoffer Petersson, Hampus Linander, Yutaro Iiyama, Giuseppe Di Guglielmo, Javier Duarte, Philip Harris, Dylan Rankin, Sergo Jindariani, Kevin Pedro, Nhan Tran, Mia Liu, Edward Kreinar, Zhenbin Wu, Duc Hoang, 2021, arXiv preprint. https://doi.org/10.1088/2632-2153/ac0ea1
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

Critical reading (from the supplied passages only): The paper extends hls4ml (v0.5.0, Vivado HLS 2020.1 backend) to support streaming Conv2D and pooling layers. Its line-buffer design is similar to im2col and uses precomputed binary-mask instructions. The benchmark is a small SVHN CNN with 3 conv blocks (16/16/24 filters) and dense layers of 42 and 64 neurons. The paper tests pruning to 50% sparsity, post-training quantization (PTQ), QKeras quantization-aware training (QAT), and AutoQKeras heterogeneous quantization. The design targets a Xilinx VU9P at 200 MHz with reuse factor 1, so it is fully parallel. A secondary target is a Zynq XC7Z020 at 100 MHz, but only the caption of its table (Table 4) is supplied.

Headline claims from the Abstract:
- About 5 µs inference latency.
- Critical FPGA resources (DSPs) cut by 97% with no accuracy loss, and by 99% with 6% accuracy loss.

Accuracy values (10-fold mean ± std, Keras): BF 94.1 ± 0.1, BP 93.8 ± 0.2, AQ 90.1 ± 0.1, AQP 89.5 ± 0.2. The passages report that PTQ fails below 14 bits, while QAT keeps accuracy down to 3–4 bits.

Caveats:
1. The supplied passages do not include the Table 3 and Table 4 values (latency, LUTs, DSPs, BRAM), so these fields are n/r.
2. The Fig. 13 resources are only given qualitatively, as a percentage of the device.
3. The latency figure is from post-synthesis/HLS results, not an on-board measurement.
4. The 5 µs latency is in microseconds. The column is in ms and the values must not be unit-converted, so latency_ms is set to n/r and the value is recorded here.
5. The energy figures (QTOOLS, 45 nm estimate) are not FPGA power, so power is n/r.
6. The paper metadata flags that no sections were detected, so most text sits under '(préambule)'.
