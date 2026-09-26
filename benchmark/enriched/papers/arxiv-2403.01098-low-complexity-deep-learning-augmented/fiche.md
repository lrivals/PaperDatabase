---
id: arxiv-2403.01098-low-complexity-deep-learning-augmented
fiche: done
date:
---

# Low Complexity Deep Learning Augmented Wireless Channel Estimation for Pilot-Based OFDM on Zynq System on Chip

Animesh Sharma, Syed Asrar Ul Haq, Sumit J. Darak, 2024, arXiv preprint. https://arxiv.org/abs/2403.01098
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

Sharma, Haq & Darak (2024) build channel estimation (CE) for pilot-based OFDM on a Xilinx ZC706 Zynq SoC, with a dual-core ARM A9 and a 7-series FPGA. They compare four estimators: LS (least squares), LMMSE (linear minimum mean square error), iResNet (the prior state-of-the-art deep-learning CE, put on hardware here for the first time) and their proposed LSiDNN, an LS-augmented interpolated two-layer DNN. They use hardware-software co-design (splitting work between the ARM processor and the FPGA fabric) and choose fixed-point word lengths by comparing MSE against single-precision float. The chosen formats are (12,4) for LS, (16,4) for iResNet and (26,8) for LSiDNN.

Table X gives two LSiDNN variants. The low-latency one (LSiDNN LL) runs in 0.08632 on the FPGA, which the text calls 86% faster than on the ARM, and is close to LS at 0.070558. The low-complexity one (LSiDNN CE) runs in 0.714885. The paper says LSiDNN CE uses 97%, 85%, 80% and 67% fewer BRAM, DSP, LUT and FF resources than LSiDNN LL.

Critical points:
1. **Time units are unclear.** Table X's header says execution time is in seconds, but the text says the ARM-only iResNet takes 40 µs, which matches the table's 40.25315. The values are probably microseconds, so I left latency_ms as n/r rather than guess.
2. **Resource counts are missing.** The absolute BRAM, DSP and LUT numbers were lost in text extraction; only relative percentages survive. Those columns are n/r.
3. **Power source is not stated.** The table gives "Total" and "Dynamic" power, but the passages don't say whether these are Vivado estimates or board measurements, so power_scope is unspecified.
4. **No accuracy numbers in the hardware table.** The paper claims fixed-point versions match float MSE/BER, but only shows this in figures; no number is given in the text.
5. **Generalization is weak.** The authors admit DL-based CE degrades badly when test channel conditions differ from training.
6. **Abstract claims can't be fully checked.** The abstract's "88-90% lower execution time" and "38-85% lower resources" figures can only be partly verified, because the text breaks off mid-sentence at the iResNet comparison.
