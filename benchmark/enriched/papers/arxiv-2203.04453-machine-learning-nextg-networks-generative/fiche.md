---
id: arxiv-2203.04453-machine-learning-nextg-networks-generative
fiche: done
date:
---

# Machine Learning in NextG Networks via Generative Adversarial Networks

Ender Ayanoğlu, Kemal Davaslıoğlu, Yalin E. Sagduyu, 2022, arXiv preprint. https://doi.org/10.1109/tccn.2022.3153004
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

This is a survey/tutorial of GANs for NextG networks (spectrum sharing, anomaly detection, security). It includes one small case study of its own: f-AnoGAN (a WGAN-GP generator/discriminator plus an encoder, with the anomaly score = reconstruction MSE + κ·discriminator-feature MSE) for outlier detection on RFMLS 2016a (11 modulations, SNR -20 to 18 dB). It trains on one modulation and tests on all 11, with a convolutional autoencoder (CAE) as the baseline.

Findings:
- Detection performance depends strongly on which modulation is used for training.
- AUROC is above 0.90 when training on AM-DSB, CPFSK, GFSK or WBFM with the S-RP, H-RP or JSD measures, and f-AnoGAN beats the CAE there.
- Training on AM-SSB or QAM16 fails. For these, the CAE is no better than random.
- The per-cell Table 8 AUROC values are not in the supplied passages, so accuracy_value is n/r.

Tuned settings: 3 critic updates per generator update, λ=10, κ=1.

Hardware result: the only measurement is average end-to-end inference time on an NVIDIA GeForce RTX 3060 GPU. This covers the encoder, generator and discriminator forward passes plus the score computation. It is 0.005784 s, or 172.9 samples/s, with no parallel processing (batch of one).
- The time is reported in seconds. Because the instructions say not to convert units, latency_ms is n/r and the value is kept here.
- 172.9 samples/s goes in the fps field.

Critical points:
- There is no FPGA, quantization, power or resource data. The automatically assigned 'autoencoder-fpga' axis looks wrong; the CAE is only a software baseline.
- The authors call their simulations 'very initial results'.
- No timing is given for the CAE baseline.
- The paper metadata is flagged for manual checking.
