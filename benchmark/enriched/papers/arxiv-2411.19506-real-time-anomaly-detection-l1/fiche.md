---
id: arxiv-2411.19506-real-time-anomaly-detection-l1
fiche: done
date:
---

# Real-time Anomaly Detection at the L1 Trigger of CMS Experiment

Abhijith Gandrakota, 2024, arXiv preprint. https://arxiv.org/abs/2411.19506
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

ICHEP 2024 proceedings (CMS collaboration): two L1 anomaly-detection triggers. AXOL1TL is a VAE on L1 objects (10 jets, 4 e/γ, 4 μ, MET; pT/η/φ as raw integers; latent size 8). Only the encoder runs online, and the anomaly score is Σμ². CICADA is a convolutional AE on an 18x14 calorimeter image, compressed by knowledge distillation. Both use QKeras QAT, go through hls4ml to HLS, and run on Xilinx Virtex-7 in the CMS Global Trigger test crate. The text says the FPGA outputs are bit-exact (Fig. 2). Critical reading: (1) The text reports no measured hardware numbers: no LUT/DSP/BRAM counts, no measured latency, no power, no bit widths. '50 ns' and '40 MHz' are GT system limits the network is said to meet, not reported measurements. 50 ns is not converted to ms, so latency_ms is n/r. (2) The 46% efficiency gain over the rest of the L1 menu at 1 kHz for H→4b is described as estimated, not measured on hardware, and the text does not say how the comparison was matched. (3) Live-run evidence is qualitative: stable rates at five thresholds, orthogonality to the standard menu, no sculpting of the invariant mass. (4) Only AXOL1TL was commissioned, and CICADA has no deployment results in these passages. (5) Training and validation used a 50/50 split of 2023 ZeroBias data at √s=13.6 TeV, PU 62. One row covers the deployed AXOL1TL. Confidence is medium because resource and latency figures are missing.
