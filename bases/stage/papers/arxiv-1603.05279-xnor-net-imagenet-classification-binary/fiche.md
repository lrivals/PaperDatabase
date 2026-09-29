---
id: arxiv-1603.05279-xnor-net-imagenet-classification-binary
fiche: done
date: 2026-09-29
---

# XNOR-Net: ImageNet Classification Using Binary Convolutional Neural Networks

Mohammad Rastegari, Vicente Ordonez, Joseph Redmon, Ali Farhadi, 2016, European Conference on Computer Vision (ECCV). https://arxiv.org/abs/1603.05279
Type : conférence

## Problème

Les CNN (AlexNet : 61 M de paramètres, 249 Mo, 1,5 G opérations par image) sont trop lourds
pour les téléphones et l'électronique embarquée (§1). Les réseaux binaires existants
(BinaryConnect, BinaryNet) n'avaient pas été évalués ni rendus précis sur ImageNet (§1-2).

## Méthode

- **Binary-Weight-Networks (BWN)** : W ≈ α·B avec B = sign(W) et α = moyenne des |W| par
  filtre (solution optimale de ‖W − αB‖², éq. 2-6) → 32× moins de mémoire, convolution par
  additions/soustractions (≈ 2×) (§3.1).
- Entraînement : binarisation en passes avant et arrière, gradient du signe par STE
  (1_{|r|≤1}), **mise à jour des poids réels** (les petites variations seraient perdues après
  binarisation) (§3.1, Alg. 1).
- **XNOR-Net** : entrées aussi binarisées, échelle β par sous-tenseur d'entrée (calculée par une
  convolution de la moyenne des |I| sur les canaux) ; convolution par **XNOR + bitcount**
  (éq. 11) (§3.2).
- Bloc réordonné : BatchNorm → activation binaire → convolution binaire → pooling (au lieu de
  conv → BN → activation → pooling) ; première et dernière couche non binarisées (§3.2, §4.1).
- Extension possible à k bits et aux gradients binaires (−1,4 point top-1) (§3.2, §4.2).

## Plateforme et implémentation

Accélération évaluée en **nombre d'opérations haute précision** : 62,27× théorique, 58× mesuré
dans leur implémentation CPU pour une convolution (c = 256, 3×3, 14×14), hors allocation et
accès mémoire (§4.1). Modèle de CPU : n/r. Code : http://allenai.org/plato/xnornet (Abstract).

## Résultats

- ImageNet AlexNet (top-1 / top-5) : **BWN 56,8 / 79,4** ; BinaryConnect 35,4 / 61,0 ;
  **XNOR-Net 44,2 / 69,2** ; BinaryNet 27,9 / 50,42 ; AlexNet flottant 56,6 / 80,2 (Table 1).
- ResNet-18 : BWN 60,8 / 83,0 ; XNOR-Net 51,2 / 73,2 ; flottant 69,3 / 89,2. Variante GoogLeNet :
  BWN 65,5 / 86,1 contre 71,3 / 90,0 (Table 2).
- CIFAR-10 : erreur 9,88 % (BWN) et 10,17 % (XNOR-Net) (§4.2).
- Ablations : α calculé analytiquement (56,8 top-1) plutôt qu'appris comme paramètre (46,2)
  (Table 3a) ; supprimer β coûte moins de 1 point (§4.2).

→ reportés dans `benchmarks.csv` : 3 lignes (AlexNet BWN et XNOR-Net, Table 1 reconstruite,
`medium` ; ResNet-18 XNOR-Net, Table 2, `high`).

## Limites et critique

- L'accélération de 58× est un **compte d'opérations** dans une convolution isolée, sans accès
  mémoire ni réseau complet : pas une latence mesurée de bout en bout.
- Le BWN AlexNet « aussi précis » que le flottant compare à un AlexNet sans BN ni LRN dans leur
  implémentation (§4.2) : baseline discutable.
- XNOR-Net perd 12-18 points top-1 face au flottant ; première et dernière couches restent en
  précision pleine.
- Aucune mesure d'énergie ni de plateforme embarquée.

## Pertinence pour la thèse

Référence de la quantification binaire dans la bibliographie du stage, à l'extrême opposé de
l'INT8. Comme TWN et BinaryConnect, elle garde des **poids réels pour la mise à jour** : sur
MCU, cela signifie qu'un apprentissage en ligne binaire exigerait une copie haute précision
en RAM, ce qui annule une partie du gain mémoire (déduit).

## Gaps identifiés

- Mise à jour de réseaux binaires sans copie flottante : non traitée.
- Gain réel (latence, énergie) sur Cortex-M : non mesuré.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Tables 1 et 3 reconstruites par PyMuPDF ; fin de
§3.2 (k bits) et de §4.2 (ResNet) partiellement désordonnées.
Déduit et non affirmé par les auteurs : conséquence mémoire pour l'apprentissage en ligne.
