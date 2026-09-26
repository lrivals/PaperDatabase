---
id: arxiv-1805.03033-efficient-design-hardware-enabled-reservoir
fiche: done
date:
---

# Efficient Design of Hardware-Enabled Reservoir Computing in FPGAs

Bogdan Penkovsky, Laurent Larger, Daniel Brunner, 2018, arXiv preprint. https://arxiv.org/abs/1805.03033
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

Penkovsky, Larger & Brunner (2018) build a single-node (time-delay) reservoir computer on an Artix-7 XC7A100T FPGA. The hardware was designed in Clash (Haskell), compiled to VHDL, then built in Vivado. The paper adds two ideas: (1) a PCA 'linear autoencoder' merged into the input mask (W_I2 = W_I·Wc^T·Wc), and (2) a genetic algorithm (GA) search over the reservoir dynamics parameters (τ, β, Φ0, ρ). The task is isolated-digit speech recognition on the clean Aurora-II subset (2412 samples, 64-dimensional Lyon cochleagrams).

**Reported results**
- Without PCA, the GA reaches a word error rate (WER) of 3.8. With PCA (7 components, 94.9 variance kept, about 9x input compression), it reaches 2.1. This is the '1.8-fold' improvement.
- These WER values come from offline simulation with two-fold cross-validation on 500+500 digits, not from the FPGA.
- The claim that the GA is 5,106 times faster than grid search is an extrapolated estimate for a four-dimensional grid, not a measurement.

**Limitations of the supplied passages**
- The only measured hardware figure is that the design takes 'about 23% of FPGA area' with N = 600 nodes. The passages give no LUT, DSP or BRAM counts, no clock rate, throughput, latency or power.
- The FPGA test-set WER (on a separate set of 1000 digits) is cut off in the passages, so no hardware accuracy can be recorded.
- Inputs are compressed on the PC and sent over serial UART. Readout weights are trained offline. Hardware quantization is only modelled as injected noise of about 2^-13 (the buses are 16+2 bits wide).

**Inconsistencies**
- The text limits Φ0 to [0, π], yet the reported optimal values are −1.33 and −3.3125.
- The PCA analysis finds the best result with 13 components, but later experiments use 7.
- The dataset is small, and the only baseline is the authors' own configuration without PCA.
