---
id: arxiv-2401.15453-bayesian-inference-accelerator-spiking-neural
fiche: done
date:
---

# Bayesian Inference Accelerator for Spiking Neural Networks

Prabodh Katti, Anagha Nimbekar, Chen Li, Amit Acharyya, Bashir M. Al-Hashimi, Bipin Rajendran, 2024, arXiv preprint. https://arxiv.org/abs/2401.15453
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

Critical reading (from the supplied passages only): The authors train a Bayesian binary ResNet-18 on CIFAR-10 with BayesBiNN, which gives Bernoulli weights in {-1,+1}. They convert it to an 8-bit SNN through a quantized ReLU with L=8, then map it to a Zynq-7000 (PYNQ) PS–PL accelerator. The accelerator has 64 multiplier-less mux-based PEs and a 16-LFSR PRNG bank that takes 4 random numbers from each 32-bit LFSR.

Software accuracy: 92.4 for the ANN, 91.9 after quantized-ReLU retraining, and about 91.5 for the SNN with nMC=10 within 4 timesteps. Accuracy falls to about 89.4 with the hardware-friendly 8-bit PRNG. Reusing LFSR bits has little effect, but random-number precision matters. The Bayesian SNN has lower ECE than the STE frequentist baseline, even when its accuracy is lower.

Measured hardware results:
- Table I gives 1.06e-5 ms to generate 64 random numbers with the LFSR at 94 MHz, for both the no-reuse and max-reuse versions.
- Table II reports utilization only as percentages: LUTs 5.3, FFs 2.78, DSPs 2.73, BRAMs 33.57. The luts, dsps and bram fields therefore hold percentages of the device, not absolute counts.

Caveats:
- The extracted text of Table III has no numbers for power, GOPS, frequency or GOPS/DSP. The abstract's '6.5x GOPS/DSP' and 'up to 30x less power' are relative claims that cannot be checked here, so power and GOPS are n/r.
- Power is said to include both PS and PL, i.e. system/board-level.
- There is no end-to-end inference latency or FPS figure. The 1.06e-5 ms is PRNG time only, so row 1 leaves latency as n/r.
- Table I's accuracy values at T=16 are missing from the extracted text.
- The toolflow (e.g. Vivado/HLS) and the exact Zynq part are not stated.
- The conclusion admits that the PS–PL data transfer (von Neumann bottleneck) limits system throughput.
- Metadata extraction was flagged as unverified.
