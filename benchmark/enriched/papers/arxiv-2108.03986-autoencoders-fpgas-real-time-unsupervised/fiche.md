---
id: arxiv-2108.03986-autoencoders-fpgas-real-time-unsupervised
fiche: done
date:
---

# Autoencoders on FPGAs for real-time, unsupervised new physics detection at 40 MHz at the Large Hadron Collider

Ekaterina Govorkova, Ema Puljak, Thea Aarrestad, Thomas James, Vladimir Loncar, Maurizio Pierini, Adrian Alan Pol, Nicolò Ghielmetti, Maksymilian Graczyk, Sioni Summers, Jennifer Ngadiuba, Thong Q Nguyen, Javier Duarte, Zhenbin Wu, 2021, Nature Machine Intelligence 4, 154 (2022). https://doi.org/10.1038/s42256-022-00441-3
Type : article de journal

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

Govorkova et al. (Nature MI 2022) put DNN and CNN autoencoders (AE) and variational autoencoders (VAE) on a Xilinx VU9P using QKeras and hls4ml, for unsupervised anomaly detection in the LHC Level-1 trigger. All models are 50% pruned. For the VAEs, the anomaly score is the KL divergence (D_KL) computed from the encoder's μ and σ. This drops the decoder, the Gaussian sampling and the input buffering, which roughly halves latency. Detection performance stays similar: AUC 84–95% across the four signals, and TPR at an FPR of 1e-5 is only about 0.05–6%. It is highest for A→4ℓ.

Hardware numbers (Table III) are Vivado HLS 2020.1 estimates at a 5 ns clock, not post-place-and-route or on-board measurements. Resources are given as percentages of the VU9P, not absolute counts. Latency and II are in ns: DNN VAE 80/5, DNN AE 130/5, CNN VAE 365/115, CNN AE 1480/895. The CNN AE fails the resource and II constraints. The only on-hardware check is the DNN VAE inside emp-fwk on a VCU118 at 240 MHz. There, the outputs matched the HLS C simulation, but no timing, resource or power values are given. A Virtex-7 690 estimate for the DNN VAE is also given: 205 ns latency, 9% LUT.

Limitations:
- No power, throughput or GOPS figures are reported.
- The floating-point Table I values are not in the supplied passages, so the compression cost cannot be quantified here.
- VAE QAT was unstable, so the VAEs use PTQ.
- The abstract's 'less than 3% of logic' matches the DNN VAE's LUT estimate.

Row conventions: latency_ms is n/r because the source reports ns and units are not converted; see the latencies above. luts, dsps and bram are percentages of the VU9P. Accuracy is the AUC for A→4ℓ from Table II.
