---
id: arxiv-1901.09192-selectivenet-deep-neural-network-integrated
fiche: done
date: 2026-10-26
benchmarks: none
---

# SelectiveNet: A Deep Neural Network with an Integrated Reject Option

Yonatan Geifman, Ran El-Yaniv, 2019, arXiv preprint (la version ICML 2019 n'est pas vérifiée ici). https://arxiv.org/abs/1901.09192
Type : preprint non relu par les pairs

## Problème

Les mécanismes de rejet existants appliquent un seuil sur la confiance d'un réseau pré-entraîné sur tous les points (Softmax Response, SR ; MC-dropout), sans optimiser le réseau pour la zone de couverture visée (§1, §3). Les auteurs veulent un modèle qui apprend prédiction et rejet ensemble, pour une couverture cible c donnée (§2, Éq. 1 : minimiser le risque sélectif sous contrainte φ(g) ≥ c). MC-dropout coûte jusqu'à des centaines de passes avant par prédiction (§3).

## Méthode

Réseau à trois têtes sur un corps commun (§4.1) : prédiction f, sélection g (sigmoïde, prédit si g(x) ≥ 0,5) et tête auxiliaire h (entraînement seul, expose le corps à tous les exemples). Perte : risque sélectif empirique + pénalité quadratique λ·max(0, c − couverture)² (variante de point intérieur, Éq. 2), combinée à la perte auxiliaire : L = αL(f,g) + (1−α)L_h, α = 0,5, λ = 32 (§4.2, §6.3). Calibration post-entraînement de la couverture par un seuil τ (percentile 100(1−c) de g sur un jeu de validation non étiqueté), avec borne de Hoeffding (§5). Corps : VGG-16 adapté (CIFAR-10, SVHN, Cats vs Dogs) ; MLP pour la régression (§6.3). Pas de quantification ni de cible matérielle.

## Plateforme et implémentation

Aucune plateforme matérielle : entraînement et évaluation logiciels, plateforme n/r. Code publié : https://github.com/geifmany/SelectiveNet (§6).

## Résultats

- CIFAR-10, erreur 0/1 (risque sélectif) : à couverture 0,80, SelectiveNet 0,86±0,06 contre SR 1,05±0,07 et MC-dropout 1,08±0,05 ; à 1,00, 6,79 pour tous (Table 2).
- SVHN : 0,53±0,01 contre 0,61 (SR et MC-dropout) à 0,80 ; indistinguable à 0,95 (Table 3).
- Cats vs Dogs : 0,35±0,09 contre SR 0,68±0,05 à 0,80 (Table 4, corps de tableau non extrait proprement : valeurs à vérifier ; lues dans le texte extrait).
- Régression (Concrete, UCI) : gain de 26,8 à 30,5 % relatif sous 0,9 de couverture annoncé dans le texte (§7.2), tandis que la Table 5 montre 4,4 à 17,1 % : incohérence interne à signaler.
- Écart de couverture moyen par rapport à la cible : 3,63 % (SelectiveNet) contre 11,98 % (SR) (Table 1) ; la calibration τ le corrige (§5, §8.1).
Pas de métrique de faux négatifs par classe : le risque est l'erreur globale.
→ reportés dans `benchmarks.csv` : aucune ligne. Article ML sans mesure sur plateforme matérielle (FPS, puissance, ressources absents) ; la base ne garde que les mesures de plateforme.

## Limites et critique

- Petits jeux d'images 32×32 / 64×64 et un seul jeu tabulaire ; pas de détection d'objets, pas de faux négatifs d'une classe critique (§7).
- Risque symétrique (erreur 0/1) : aucune pondération du coût d'un rejet ou d'un faux négatif, contrairement à ce que voudrait une surveillance de sécurité.
- Un modèle par couverture cible (re-entraînement) ; la cible c est fixée à l'entraînement, la calibration τ ne compense que partiellement.
- Surcoût d'inférence : tête de sélection d'un FC 512 + sigmoïde (§6.3), non chiffré ; aucun coût mémoire, latence ni quantification mesurés.
- Hypothèse i.i.d. : aucune évaluation sous décalage de distribution ou OOD. Les résultats de l'écart relatif sont des moyennes sur 3 runs (§8.1) seulement.
- Preprint ; les baselines (SR, MC-dropout) sont celles de 2017.

## Pertinence pour la thèse

Axe `failure-prediction` du sujet ARCYS. Fondateur pour la prédiction sélective apprise conjointement avec le prédicteur : la tête de sélection g est un moniteur de défaillance intégré, de coût fixe (une seule passe, par opposition à MC-dropout), donc compatible avec un déterminisme temporel (WCET) et une implémentation FPGA (petit FC + sigmoïde, quantifiable en virgule fixe : déduit, non traité par les auteurs). Il alimente l'idée d'un moniteur appris avec le détecteur de personnes. Il laisse ouvert : la ciblage du faux négatif critique (perte asymétrique, notion de coût), l'extension à la détection d'objets (YOLO) et non à la classification, les sorties anticipées conservatrices (rejet comme signalement), l'effet de la quantification sur g et sur la couverture calibrée, et la robustesse sous décalage.

## Gaps identifiés

- Prédiction sélective pour la détection d'objets (boîtes, faux négatifs par objet) : absente ici.
- Perte sélective à coût asymétrique centrée sur le faux négatif d'une personne.
- Effet de la quantification (virgule fixe) sur la tête de sélection et la calibration de couverture.
- Garanties de couverture/risque sous décalage de distribution, pour une certification.

## Statut de lecture

Papier complet (fulltext.md lu en entier ; extraction grobid, ok ; Table 4 et Table 6 sans corps extrait, Table 5 mélangée avec la Table 6 : valeurs de ces tableaux à vérifier ou lues dans le texte).
Ce qui suit est déduit et non affirmé par les auteurs : la compatibilité avec le déterminisme temporel et une implémentation FPGA quantifiée ; l'adaptation à la détection de personnes ; la lecture de g comme moniteur de défaillance.
