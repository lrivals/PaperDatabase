---
id: arxiv-2504.06996-neural-signal-compression-raman-tinyml
fiche: done
date:
---

# Neural Signal Compression using RAMAN tinyML Accelerator for BCI Applications

Adithya Krishna, Sohan Debnath, Madhuvanthi Srivatsav, André van Schaik, Mahesh Mehendale, Chetan Singh Thakur, 2025, arXiv preprint. https://arxiv.org/abs/2504.06996
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

RAMAN is a sparse tinyML accelerator (12 PEs × 4 MACs, 8-bit weights and activations, 24-bit partial sums). It runs the encoder of a convolutional autoencoder (CAE) that compresses 96-channel × 100-sample LFP windows from two macaques (K and L, from dataset [53]). The compression ratio is 150 for DS-CAE1 and 37.5 for MobileNetV1-CAE(0.25x). On the Efinix Ti60 FPGA, Table I lists one set of resources for both models: 37.3k LUTs, 8.6k FFs, 52.3k XLR cells (86%) and 61 DSPs. Memory blocks, clock, latency and power differ by model. The balanced stochastic pruning uses an LFSR (32 LUTs + 20 FFs), and the passages give its parameter-memory saving as 15.7–32.4% versus magnitude pruning, with nearly the same SNDR and R2.

Caveats:
(1) Power is estimated, not measured. The FPGA figures (47.91 mW at 2 MHz, 53.97 mW at 7 MHz) are about 94% static. The 65-nm ASIC figure (1.45 mW, 15.1 µW per channel) comes only from post-layout simulation, not silicon. That makes the per-channel comparison against fabricated chips in Table V uneven.
(2) Latency is about 45–48 ms per 50 ms window at 2–7 MHz. Throughput is only just real-time, and the paper reports no FPS or GOPS.
(3) The passages don't say whether the SNDR and R2 values in Table V come from RAMAN's on-FPGA output or from the QAT model in PyTorch. I assume the 8-bit, 75%-pruned configuration shown in Fig. 9.
(4) The per-cell values in Table III and Table IV were lost in extraction, so the stochastic-vs-magnitude pruning numbers can't be checked.
(5) The prior works in Table V use different signal types (EEG, spike, ECoG, LFP) and bit precisions, and lossless and lossy methods sit side by side. Only Valencia et al. [54] uses the same dataset, so it is the only like-for-like baseline.

Row choices: the LUT count is copied exactly as '37.3k'. BRAM is the count of 10 kB memory blocks. Accuracy is the Monkey K SNDR; Monkey L is 27.43 dB for DS-CAE1 and 28.49 dB for MobileNetV1-CAE(0.25x).
