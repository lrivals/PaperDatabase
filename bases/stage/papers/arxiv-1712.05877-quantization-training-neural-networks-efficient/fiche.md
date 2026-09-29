---
id: arxiv-1712.05877-quantization-training-neural-networks-efficient
fiche: done
date: 2026-09-29
---

# Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference

Benoit Jacob, Skirmantas Kligys, Bo Chen, Menglong Zhu, Matthew Tang, Andrew Howard, Hartwig Adam, Dmitry Kalenichenko, 2018, IEEE Conference on Computer Vision and Pattern Recognition (CVPR). https://arxiv.org/abs/1712.05877
Type : conférence

## Problème

Les travaux de quantification sont évalués sur des architectures surdimensionnées (AlexNet,
VGG) et rarement mesurés sur du vrai matériel ; les réseaux binaires ou à décalages de bits
dégradent la précision ou n'apportent rien sur des CPU dotés de multiply-add (§1). Il faut un
schéma qui améliore le compromis latence ↔ précision de réseaux déjà efficaces (MobileNets)
sur CPU mobiles (§1).

## Méthode

- **Quantification affine** r = S(q − Z) : échelle S réelle, **zero-point** Z entier (le réel 0
  est exactement représentable), un couple (S, Z) par tableau de poids ou d'activations ;
  poids et activations sur 8 bits, **biais sur int32** avec S_bias = S₁S₂, Z_bias = 0 (§2.1, §2.4).
- **Arithmétique entière seule** : le seul facteur non entier M = S₁S₂/S₃ est ramené à
  M = 2⁻ⁿ M₀ avec M₀ ∈ [0,5 ; 1) en virgule fixe int32 + décalage arrondi (§2.2) ;
  zero-points factorisés pour garder un cœur GEMM uint8 × uint8 → int32 (§2.3).
- Couche fusionnée conv + biais + activation (clamp ReLU/ReLU6) + recalage + saturation
  uint8 (§2.4), bibliothèque gemmlowp ; astuces NEON (SQRDMULH, arrondi correct, poids int8
  jamais à −128 pour accumuler deux produits sur int16) (annexe B).
- **Entraînement avec quantification simulée** (« fake quantization ») : poids quantifiés avant
  convolution, activations aux points où elles le seront à l'inférence, rétropropagation et
  poids en flottant (§3, éq. 12) ; plages des poids = [min, max], plages des activations par
  moyenne exponentielle, quantification des activations retardée en début d'entraînement
  (§3.1) ; **repliement de la batch-norm** dans les poids avant quantification (§3.2).
- Motivation : la quantification post-entraînement échoue sur les petits modèles (plages de
  poids très différentes entre canaux, valeurs aberrantes) (§3).

## Plateforme et implémentation

Qualcomm Snapdragon 835 (cœurs big et LITTLE, Pixel 2) et Snapdragon 821 (Pixel 1), un à
quatre threads (§4.2, annexe D). Consommation : n/r. Code intégré à TensorFlow / TensorFlow
Lite (tf.contrib.quantize, gemmlowp) (§3.1, Algorithm 1).

## Résultats

- ResNets : précision entière à moins de 2 % du flottant (§4.1.1 ; Tables 4.1-4.2 non extraites).
- Inception v3 ImageNet (top-1) : ReLU6 78,4 → 75,4 % (8 bits) et 75,0 % (7 bits) ; ReLU
  78,3 → 74,2 et 73,7 % : ReLU6 se quantifie mieux (plage naturelle [0, 6]) (Table 4.3).
- MobileNets ImageNet : à 33 ms (30 fps) sur cœur LITTLE du Snapdragon 835, ≈ 10 points de
  mieux que le flottant à latence égale ; gain moindre sur le 821, optimisé pour le flottant
  (§4.2.1, Fig. 1.1c, 4.1, 4.2).
- MobileNet SSD COCO : jusqu'à 50 % de temps en moins pour −1,8 % relatif de précision
  (§4.2.2 ; Table 4.4 non extraite).
- Détection de visages (Snapdragon 835) : précision 68 → 66 % (DM 100 %), 65 → 62 % (50 %),
  56 → 54 % (25 %) (Table 4.5) ; latence 1 cœur big : 337 → 154 ms, 106 → 56 ms, 44 → 28 ms
  (≈ 36 fps) ; 4 cœurs : 69 / 30 / 18 ms (Table 4.6).
- Attributs de visage : poids plus sensibles que les activations à la réduction de bits ; 8 et
  7 bits ≈ flottant ; −10,6 % à 4 bits de poids (Table 4.7).

→ reportés dans `benchmarks.csv` : 2 lignes (Inception v3 INT8, Table 4.3, `high` ; détecteur
de visages DM 25 % sur 1 cœur big, Tables 4.5-4.6, `medium` car tableaux aplatis).

## Limites et critique

- Plateformes smartphone (Cortex-A), pas de MCU ; aucune mesure d'énergie.
- Tables 4.1, 4.2 et 4.4 absentes de l'extraction : chiffres ResNet et COCO seulement en texte.
- Granularité par tenseur (pas par canal) : les auteurs pointent eux-mêmes l'écart de plages
  entre canaux comme cause d'échec en post-entraînement (§3).
- L'entraînement reste en flottant : le schéma ne couvre pas la mise à jour des poids en entier.

## Pertinence pour la thèse

Définit le schéma de quantification **affine INT8 (échelle + zero-point, biais int32)** repris
par TensorFlow Lite et TFLM, donc le format natif des modèles déployés sur MCU dans le stage.
Point important pour un EWC en INT8 : les poids et leurs ancres doivent partager des échelles
compatibles, et la mise à jour en ligne doit respecter ce format ou passer par une copie
flottante, que ce papier conserve pour l'entraînement (déduit).

## Gaps identifiés

- Entraînement / mise à jour des poids directement en arithmétique entière : hors du papier.
- Quantification des tenseurs auxiliaires d'un algorithme de CL (Fisher, ancres) : non traitée.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, annexes A-D). Tables 4.1, 4.2, 4.4 non extraites ;
Tables 4.5-4.7 aplaties ; §4.2.4 réduite à son titre.
Déduit et non affirmé par les auteurs : conséquences pour l'EWC en INT8.
