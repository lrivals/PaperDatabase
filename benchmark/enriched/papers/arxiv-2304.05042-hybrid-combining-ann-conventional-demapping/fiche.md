---
id: arxiv-2304.05042-hybrid-combining-ann-conventional-demapping
fiche: done
date:
---

# A Hybrid Approach combining ANN-based and Conventional Demapping in Communication for Efficient FPGA-Implementation

Jonas Ney, Bilal Hammoud, Norbert Wehn, 2023, arXiv preprint. https://arxiv.org/abs/2304.05042
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

What the paper does: it trains a 16-QAM mapper and demapper ANN end-to-end over an AWGN channel in PyTorch. The demapper is 2 inputs, 3 fully connected layers of 16 neurons, ReLU and sigmoid. The demapper ANN can then be retrained on an Avnet Ultra96-V2 board (ZU3EG) using Vivado HLS 2019.2 and layers from the FINN library. After retraining, the paper samples the decision regions, computes one Voronoi centroid per region, and passes the centroids to a suboptimal max-log soft demapper for inference.

Communication results (Table 1, on-board retraining after a pi/4 phase offset):
- At 8 dB SNR, the baseline BER is 0.0103. Before retraining, BER is 0.316 for AE inference and 0.323 with centroids. After retraining, it is 0.0127 for AE inference and 0.0143 with centroids.
- At -2 dB SNR, the baseline BER is 0.19. Before retraining it is 0.318 and 0.319. After retraining it is 0.199 and 0.2005.
- The authors say BER matches a conventional demapper up to 10 dB and drops slightly at 12 dB.

Hardware results (Table 2):
- Soft demapper: latency 5.33e-8 s, throughput 7.50e7 symbols/s, power 5.5e-2 W, energy 7.33e-10 J/symbol.
- AE inference: latency 8.10e-8 s, throughput 1.23e7 symbols/s, power 4.53e-1 W, energy 3.67e-8 J/symbol.
- AE training: latency 2.67e-7 s, throughput 3.75e6 symbols/s, power 5.47e-1 W.
- The text claims 10x fewer LUTs, 352x fewer DSPs, 10x lower power and 50x better energy efficiency for the soft demapper.

Caveats:
1. The Table 2 extraction is garbled. The soft demapper's BRAM, DSP, FF and LUT cells are missing. The AE inference row has only three resource numbers (18.5, 10895, 11343) for four columns. I read them as BRAM, FF and LUT with the DSP cell lost, because a ZU3EG has only 360 DSPs. That mapping is uncertain.
2. Latency is reported in seconds, so latency_ms is left n/r to avoid a unit conversion. Throughput is in symbols/s, not frames/s, so fps is n/r. Power scope is not stated.
3. The comparison is not equal in scope. The ANN design was sized to use all available DSPs, while the soft demapper was only sized to match its latency and throughput range. Retraining still needs the costly training module (about 19.8k LUTs). No bit-widths or quantization are given. Only one channel impairment (a fixed phase offset) and one modulation were tested.
4. The Gbps throughput claimed for parallel soft-demapper instances is a projection, not a measurement.
