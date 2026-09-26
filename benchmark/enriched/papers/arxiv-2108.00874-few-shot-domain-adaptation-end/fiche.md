---
id: arxiv-2108.00874-few-shot-domain-adaptation-end
fiche: done
date:
---

# Few-Shot Domain Adaptation For End-to-End Communication

Jayaram Raghuram, Yijing Zeng, Dolores García Martí, Rafael Ruiz Ortiz, Somesh Jha, Joerg Widmer, Suman Banerjee, 2021, arXiv preprint. https://arxiv.org/abs/2108.00874
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

What the paper does: few-shot, test-time domain adaptation for an autoencoder-based end-to-end communication system. The channel is modelled with a Gaussian mixture density network (MDN). When the channel changes, the MDN is adapted with one affine transformation per mixture component, trained with BFGS and a closed-form KL-divergence penalty that limits how far the adapted distribution can drift. The fitted transforms are then used to build a feature transformation at the decoder input, so the encoder and decoder networks are not retrained. It only needs a small labelled target set, and the labels come free because they are the transmitted messages.

Evidence: symbol error rate (SER) plotted against the number of target samples per class. Simulated shifts include AWGN, Ricean fading, uniform fading and random Gaussian mixtures with or without phase shifts. There is also a real over-the-air mmWave FPGA testbed (Lacruz et al. 2021: 2 GHz bandwidth per channel, 60 GHz SIVERS antennas) with 20%, 25% and 30% IQ imbalance. The only number stated in the text is a relative SER improvement of "around 69%" over the fine-tuning baselines at 30% IQ imbalance with 10 samples per class. All other results appear only in figures (Figs. 4–6), so no absolute SER values can be copied.

Critical points:
1. The FPGA is the testbed radio, not an accelerator. The passages give no throughput, latency, power or resource figures (LUT/DSP/BRAM), so those fields are n/r.
2. The method fails in the AWGN to Ricean fading case (Fig. 4c).
3. The fine-tuning baselines are weak: fixed epoch counts and no regularisation. The retrained oracle is shown only as a reference line.
4. The evaluation protocol, sample sizes and number of trials are in Appendix C.1, which was not supplied.
5. The claim of robustness when Assumptions A1/A2 are violated rests on appendix ablations that were not supplied.
6. Table 1 compares parameter counts only symbolically: k(d²+2d+2) for the proposed method against the full-MDN and last-layer counts. No numeric counts are given.
7. The extraction metadata says no sections were detected, so almost everything is labelled "(préambule)".
