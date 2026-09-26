---
id: arxiv-1807.00962-neuromemristive-circuits-edge-computing-review
fiche: done
date:
---

# Neuromemristive Circuits for Edge Computing: A Review

Olga Krestinskaya, Alex Pappachen James, Leon Ong Chua, 2019, arXiv preprint. https://doi.org/10.1109/tnnls.2019.2899262
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

This is a survey of CMOS-memristive neuromorphic architectures for edge computing: synapse types (1M, 2M, 2M1R, 1T1M, 2T1M, 4M bridge), neuron circuits, and network types (ANN, DNN, CeNN, CNN, SNN, HTM). The paper reports no new experiments. Every number is taken from cited works. Many of those works are circuit simulations rather than fabricated or measured hardware, and the passages often don't say which. Examples: 92% for 8x8 MNIST with a partly fabricated 128x64 crossbar [93]; 97.84% and 6.4x lower energy for a 5-layer stochastic spiking CNN [94]; 644.2 GOPS/W for an accelerator [105]; 1.64 TOPS, 13.7 mW and 119.7 TOPS/W for a fabricated 128x64 crossbar [109]; 15.6 µW for an SNN position detector [115]. Metrics also aren't comparable across entries: some report efficiency, some peak read throughput, and accuracy comes from different datasets and input sizes. The claims about edge security and robustness to variability are argued in words only, with no numbers. Because of the no-conversion rule, the 6.3 mW figure for [106]/[107] is left out of power_w (the field is in watts). The 1.64 TOPS figure for [109] is also not entered, since gops is in GOPS. None of the cited works use FPGAs, so LUT, DSP and BRAM are n/r. Both rows below are secondary citations and are marked medium confidence. The Table I and Table II captions came with no table contents.
