---
id: arxiv-2110.06948-challenges-unsupervised-anomaly-detection-particle
fiche: done
date:
---

# Challenges for unsupervised anomaly detection in particle physics

Katherine M. Fraser, Samuel Homiller, Rashmish K. Mishra, Bryan Ostdiek, Matthew D. Schwartz, 2022, arXiv preprint. https://doi.org/10.1007/jhep03(2022)066
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

Critical reading note (Fraser et al., JHEP 2022, arXiv:2110.06948). This is a physics and ML methodology paper, not a hardware paper. None of the supplied passages mention an FPGA, a hardware platform, quantization, latency, throughput, power or resource usage. The 'autoencoder-fpga' axis was assigned automatically, so it is doubtful and should be checked manually.

What the paper does: it trains a convolutional VAE on QCD jet images only. The encoder has 1, 2 or 3 downsampling blocks, each with two 3x3 convolutional layers of 5 filters, ELU activations and 2x2 average pooling. These feed a 100-node dense layer and a 64-dimensional latent space; the decoder mirrors the encoder. The VAE is used to separate boosted top-jet and W-jet signals from background, scored by AUC.

Main findings:
1. Hyperparameters matter a lot. The best β values are 1e-7, 1e-7 and 1e-8 for MSE training with 1, 2 and 3 downsampling blocks, and 1e-5, 1e-8 and 1e-7 for Wass(1) training. The configuration with the lowest validation loss is not the best anomaly detector: the 1-block network has the lowest loss but is consistently the worst detector. The optimal settings also differ between the top and W signals.
2. Networks trained with MSE, using the full loss as the anomaly score, generally do best. Training with a Wasserstein loss does slightly worse, even though its latent space is more strongly correlated with Wasserstein distances.
3. Euclidean distances in the latent space correlate with 1-Wasserstein distances between images. Reported Pearson r values: about 0.77–0.78 in the latent space (Fig. 4); 0.75 after the first downsampling block and 0.87 after the second (Fig. 5); 0.44 between raw-image MSE and Wass(1) (Fig. 1).
4. A training-free alternative, the optimal-transport distance to QCD medoids, performs about as well as the VAE. 5–6 medoids work better than the 2–4 that the elbow method selects, and smaller p in the p-Wasserstein metric works better.

Limitations for the database:
- The AUC numbers in Tables 1 and 2 were lost in extraction; only headers and captions survive. No accuracy value can be copied.
- There are no hardware, FPS, GOPS, latency, power or resource figures.
- The dataset is described only as QCD background with top and W jet signals; the dataset section itself was not supplied.

Because no supplied passage reports a measured hardware result and no AUC value can be copied, no benchmark rows are included. If rows are wanted later, the numeric AUCs should be pulled from Table 1 (VAE) and Table 2 (medoid distances) in the original PDF.
