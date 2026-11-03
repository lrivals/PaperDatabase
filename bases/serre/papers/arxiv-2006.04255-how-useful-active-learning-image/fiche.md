---
id: arxiv-2006.04255-how-useful-active-learning-image
fiche: done
date: 2026-11-03
benchmarks: none
---

# How useful is Active Learning for Image-based Plant Phenotyping?

Koushik Nagasubramanian, Talukder Z. Jubery, Fateme Fotouhi Ardakani, Seyed Vahid Mirnezami, Asheesh K. Singh, Arti Singh, Soumik Sarkar, Baskar Ganapathysubramanian, 2020, arXiv preprint. https://arxiv.org/abs/2006.04255
Type : preprint non relu par les pairs

## Problème

L'annotation d'images pour le phénotypage (maladies, stress) est coûteuse et exige un expert (pathologiste) ; les modèles supervisés ont besoin de beaucoup d'étiquettes (Introduction). Les auteurs veulent une première comparaison de stratégies d'apprentissage actif (AL) sur deux problèmes canoniques de phénotypage, à budget d'annotation fixé.

## Méthode

AL pool-based : lot initial aléatoire de 1000 images, entraînement 100 epochs, requête de 1000 images par la fonction d'acquisition, réentraînement depuis zéro à chaque tour, jusqu'à épuisement du budget (§2.2, Fig. 3). Quatre stratégies plus un tirage aléatoire (§2.3) : Least Confidence, Entropy, Core-set (diversité, couche pénultième, approximation gloutonne), DBAL (MC-dropout + BALD). Deux jeux : soybean stress (16 573 images RGB, 8 stress + sain, labo à éclairage constant, MobileNetV2, budget 10 000) et weed species (17 509 images, 8 espèces + « sans adventice », champ, ResNet-50, budget 9000) (§2.1, §2.2, Fig. 1-2). 10 répétitions ; 5 % des données tirées au hasard pour la validation ; Adam, lr 0,001 ; meilleur modèle sur la validation conservé.

## Plateforme et implémentation

Keras / TensorFlow (§2.2). Matériel d'entraînement n/r, pas de déploiement embarqué, pas de latence. Code publié : non mentionné (n/r).

## Résultats

Résultats uniquement sous forme de courbes (Fig. 4, 5) ; aucune valeur numérique d'exactitude dans le texte extrait ni de tableau.
- Soybean : les méthodes par incertitude (LC, Entropy, DBAL) dépassent le tirage aléatoire ; Core-set fait moins bien (§3, Fig. 4).
- Weed : toutes les méthodes AL dépassent l'aléatoire ; gains plus grands que sur soybean, attribués (hypothèse des auteurs) à des conditions de champ plus difficiles (§3, Fig. 5).
- Gain surtout aux faibles effectifs étiquetés ; Entropy « marginalement meilleur » (§4).
- Les méthodes par incertitude échantillonnent plus les classes difficiles (classes 0 et 7, deux bactérioses aux symptômes confondants) (§3, Fig. 6-7).
- Creux de précision à 2000 échantillons sur soybean, attribué au déséquilibre de classes de l'ensemble étiqueté (§3).
→ reportés dans `benchmarks.csv` : aucune ligne (chiffres lisibles seulement sur courbes, non extraits ; `benchmarks: none`).

## Limites et critique

- Aucun chiffre ni intervalle de confiance : « mieux » n'est pas quantifié ni testé statistiquement (10 répétitions moyennées, dispersion non donnée dans le texte).
- Précision mesurée « sur le jeu complet » (§2.2) alors que 5 % sont réservés à la validation et que le pool étiqueté fait partie du jeu : évaluation possiblement contaminée par les données d'entraînement ; pas de jeu de test séparé décrit.
- Deux architectures différentes sur deux jeux différents : effets architecture et jeu confondus. Pas de comparaison à d'autres leviers (transfert, augmentation).
- Pas de test hors domaine ; les deux jeux sont évalués in-domain. La légende de Fig. 2 et de Fig. 7 est copiée de l'autre jeu (erreur d'édition).
- Pas de coût d'annotation réel, pas d'annotateur dans la boucle (étiquettes déjà disponibles, déduit). Pas de lot de requête autre que 1000 ni d'étude des hyperparamètres de DBAL (T non donné).
- Preprint, code non publié.

## Pertinence pour la thèse

Axe `active-labelling` de la base SerreIA : montre qu'une sélection par incertitude (entropie en tête) réduit le besoin d'étiquettes sur un jeu de maladies de feuilles de soja, utile pour étiqueter les captures de la serre (PlantDoc / CCMT) avec un expert. Les incertitudes de type entropie rejoignent aussi la calibration (axe `calibration-decision`), mais sans calibration ici. Laisse ouvert : AL sous décalage de domaine, interaction avec la calibration, gain chiffré.

## Gaps identifiés

- AL en conditions de domain shift (PlantVillage vers terrain) : non couvert.
- Effet de la calibration (temperature scaling) sur les fonctions d'acquisition par incertitude : non traité.
- Gain en nombre d'étiquettes à performance égale : non quantifié dans le texte.

## Statut de lecture

papier complet (fulltext.md lu en entier ; extraction grobid ok). Les figures 4-7 ne sont pas lues (courbes, pas de valeurs extraites).
Ce qui suit est déduit et non affirmé par les auteurs : contamination possible de l'évaluation (§2.2 ambigu), absence d'annotateur humain réel, code non publié (seulement non mentionné).
