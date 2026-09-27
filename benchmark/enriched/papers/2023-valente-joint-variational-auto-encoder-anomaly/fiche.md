---
id: 2023-valente-joint-variational-auto-encoder-anomaly
fiche: done
date:
---

# Joint Variational Auto-Encoder for Anomaly Detection in High Energy Physics

Lorenzo Conceição Lima Valente, Luca Anzalone, Marco Lorusso, D. Bonacorsi, 2023, n/r. https://doi.org/10.22323/1.434.0014
Type : n/r

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

Critical reading: Valente et al. (ISGC 2023) train a convolutional JointVAE (continuous Gaussian plus Gumbel-Softmax discrete latents). It does unsupervised anomaly detection on 40x40 jet images: 200K QCD jets are the background and top jets are the signal, with a 75/25 split. Only the encoder is meant to go on the FPGA. For that reason, only KL-based anomaly scores are used (KL continuous, discrete and total); reconstruction-based scores are not available. To fit the Vivado HLS 2020.1 limit of 2048 parameters per layer, the encoder was reduced (fewer and shorter filters, plus a linear conv_fin layer). It was then trained quantization-aware in QKeras at <16,6> fixed point and converted with hls4ml. The reduction lowered KL-total performance, while quantization raised KL-discrete. The quantized KL-total AUC is about 81.2. Other values from Tables 1–3 (TPR@FPR=0.1 and the energy in µJ) are not in the supplied passages. The only energy figure given is a relative drop of 39.2%, estimated with QTOOLS for a 45 nm process; it is not an FPGA power measurement.

The hardware evidence consists only of per-layer Vivado HLS resource estimates at a 5 ns target clock (200 MHz) on an Alveo U250. Nothing was synthesized, placed and routed, or run on the board. No throughput or power figures are reported. The table caption mentions latency, but the supplied table has no latency values. The first layer, conv2_b0_0, could not be simulated in HLS. Its resources were extrapolated linearly from computational complexity to 6189696 LUTs (358% of the device), so the authors conclude the design cannot fit on a single FPGA. Overall this is a negative feasibility result, not a working accelerator.

Caveats: resource percentages are per layer and are not a full-design total. Blocks are repeated in the real model, so the true totals would be higher. The metadata still needs manual checking.
