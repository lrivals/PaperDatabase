---
id: 2022-velasco-gallego-radis-real-time-anomaly-detection
fiche: done
date:
---

# RADIS: A real-time anomaly detection intelligent system for fault diagnosis of marine machinery

Christian Velasco-Gallego, Iraklis Lazakis, 2022, Expert Systems with Applications. https://doi.org/10.1016/j.eswa.2022.117634
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

RADIS is an offline-trained LSTM-based VAE that reconstructs 14 sensor parameters from a tanker ship's diesel generator. The data has more than 66,000 one-minute instances per parameter. Pre-processing finds steady states using a first-order Markov transition-matrix image and connected component analysis, then normalises values to [-1, 1] and applies sliding windows. Per-parameter NRMSE between observed and reconstructed subsequences forms an image. Multi-level Otsu thresholding labels anomalies, with the number of classes chosen by GMM/EM and BIC. In practice this was reduced to two-level thresholding because the multi-level version was too slow for real-time use. Hyperparameters were chosen by grid search with k-fold cross-validation. The reported result is an average accuracy of 92.5 on anomalies simulated by injecting Gaussian/random noise, not on real faults.

Critical points:
(1) The passages contain no FPGA or other hardware implementation and no measured hardware result: no latency, throughput, power or resource figures. FPGA appears only in the literature review (Cheng et al. 2019 denoising filter), so the 'autoencoder-fpga' axis tag looks wrong.
(2) The real-time claim is only simulated. The authors say a real-world deployment and inference acceleration remain future work.
(3) The evaluation uses synthetic noise anomalies, reports only accuracy (no precision, recall or F1), and has no baseline comparison.
(4) The authors acknowledge that the Markov states and VAE hyperparameters were chosen heuristically and that the model may miss long dependencies.
(5) The paper's metadata still needs manual checking.
