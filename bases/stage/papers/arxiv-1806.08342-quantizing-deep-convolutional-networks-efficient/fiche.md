---
id: arxiv-1806.08342-quantizing-deep-convolutional-networks-efficient
fiche: done
date: 2026-09-29
---

# Quantizing Deep Convolutional Networks for Efficient Inference: A Whitepaper

Raghuraman Krishnamoorthi, 2018, arXiv preprint. https://arxiv.org/abs/1806.08342
Type : preprint non relu par les pairs

## Problème

Guide pratique : comment quantifier des CNN pour l'inférence en poids et activations
entiers, avec quelle perte de précision et quel gain de latence, et quelles règles suivre pour
l'entraînement et le matériel (Abstract, §1).

## Méthode

- Quantificateurs uniformes : **affine** (échelle Δ + zero-point z, 0 représentable
  exactement), **symétrique** (z = 0, plage restreinte à ±(N/2 − 1) pour le SIMD),
  **stochastique** (bruit uniforme + arrondi, pour l'entraînement) (§2.1-2.3).
- Rétropropagation à travers le quantificateur par **straight-through estimator** (gradient
  passé tel quel dans [x_min, x_max]) (§2.4, éq. 14-15).
- Paramètres : min/max réels pour les poids, moyenne glissante des min/max pour les
  activations (§2.5).
- Granularité : **par couche** ou **par canal** (une échelle par noyau de sortie) pour les
  poids ; activations par couche (§2.6).
- Post-training quantization (PTQ) poids seuls ou poids + activations (≈ 100 mini-batchs de
  calibration) ; quantization-aware training (QAT) avec poids flottants mis à jour et
  quantifiés à chaque passe (§3.1-3.2, éq. 16-17).
- Batch-norm : repliement avec facteur de correction σ_B/σ puis gel des statistiques après
  ≈ 200-400 k pas (§3.2.2).
- Outils TensorFlow / TFLite (tf.contrib.quantize, TOCO, NN-API) (§3.2).

## Plateforme et implémentation

Google Pixel 2 : un grand cœur CPU, et DSP Qualcomm Hexagon HVX via NN-API (§6, Table 7).
Consommation : n/r.

## Résultats

- **PTQ 8 bits** (poids par canal asymétriques, activations par couche) : MobileNet-v1 1 224
  0,703 contre 0,709 en flottant ; MobileNet-v2 0,697 contre 0,719 ; ResNet et Inception à
  moins de 0,01 (Table 3). En **par couche**, MobileNet-v1 et v2 s'effondrent à 0,001 (Table 3),
  à cause de la batch-norm qui étale les plages entre noyaux (§3.1.3).
- Presque toute la perte vient des poids ; les activations 8 bits sont quasi sans perte (§3.1.3).
- **4 bits de poids** : PTQ par canal symétrique 0,001 sur MobileNet-v1 ; QAT le remonte à 0,65
  (flottant 0,709) ; Inception-v3 0,76 contre 0,78 (Table 5).
- 4 bits d'activations (poids 8 bits) : QAT MobileNet-v1 0,64, v2 0,58 (Table 6).
- Latence Pixel 2 (ms, flottant / entier CPU / entier DSP) : MobileNet-v1 1 224 155 / 68 / 16 ;
  MobileNet-v2 105 / 63 / 15,5 ; Inception-v3 1391 / 536 ; ResNet-v1-50 874 / 440 (Table 7)
  → 2-3× sur CPU, ≈ 10× sur DSP (§6).
- Bonnes pratiques : quantification stochastique moins bonne que déterministe ; partir d'un
  modèle flottant ; se méfier des moyennes exponentielles des poids en QAT ; ReLU plutôt que
  ReLU6 (§4, §5).

→ reportés dans `benchmarks.csv` : 3 lignes (MobileNet-v1 PTQ INT8 sur CPU et sur DSP, QAT
4 bits de poids ; `medium`, tableaux reconstruits par PyMuPDF).

## Limites et critique

- Rapport technique Google non relu par les pairs (preprint), centré sur l'outillage
  TensorFlow.
- Tables 2 et 3 identiques à l'extraction (Table 2 = doublon) ; Table 4 (QAT 8 bits) non
  extraite.
- Aucune mesure d'énergie ; plateformes smartphone.
- Le gel des statistiques de batch-norm et le STE sont présentés comme recettes, sans analyse.

## Pertinence pour la thèse

Référence du stage pour les choix de quantification INT8 : **par canal pour les poids, par
couche pour les activations**, et QAT avec poids flottants maîtres. Pour un EWC en INT8, deux
points transposables : (1) les mises à jour de faible amplitude « sous-débordent » si l'on ne
garde pas de copie flottante des poids (argument explicite du papier pour la QAT, §3.2) ;
(2) les tenseurs à grande dynamique (comme un Fisher) se quantifient mal en granularité
grossière (déduit).

## Gaps identifiés

- Mise à jour des poids sans copie flottante (entraînement entièrement entier) : non traitée.
- Quantification pour la régression : les auteurs suggèrent qu'elle demande plus de bits
  (16 bits), sans expérience (§7).

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Tables 1, 3, 6, 7 reconstruites par PyMuPDF ;
Table 4 absente ; §3.2.4 tronquée ; figures non chiffrées.
Déduit et non affirmé par les auteurs : conséquences pour la quantification d'EWC.
