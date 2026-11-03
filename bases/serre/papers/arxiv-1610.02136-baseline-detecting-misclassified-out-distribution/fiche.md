---
id: arxiv-1610.02136-baseline-detecting-misclassified-out-distribution
fiche: done
date: 2026-11-03
---

# A Baseline for Detecting Misclassified and Out-of-Distribution Examples in Neural Networks

Dan Hendrycks, Kevin Gimpel, 2017, International Conference on Learning Representations (ICLR) 2017. https://arxiv.org/abs/1610.02136 (DOI n/r)
Type : conférence (ICLR 2017) ; version arXiv (1610.02136) lue.

## Problème

Un classifieur échoue silencieusement quand la distribution de test diffère de celle d'entraînement, avec des prédictions à haute confiance (§1). Deux tâches : prédire si un exemple est mal classé (erreur/succès) et s'il est hors distribution (OOD) (§2). Les auteurs veulent un baseline simple et une évaluation standardisée.

## Méthode

- Baseline : probabilité softmax maximale (MSP) comme score ; évaluation par AUROC (base 50 %) et AUPR, avec « Succ/Err » et « In/Out » comme classe positive (§2, §3). Ils insistent que la MSP n'est pas une confiance calibrée (bruit gaussien sur MNIST : 91 % de « confiance », §1) mais discrimine quand même.
- Tâches : vision (MNIST, CIFAR-10, CIFAR-100 ; OOD = SUN, Omniglot, notMNIST, bruit), NLP (IMDB, 20 Newsgroups, Reuters, POS tagging WSJ/tweets) et parole (TIMIT, CTC, softmax sans le symbole blank) (§3).
- Module d'anormalité (§4) : décodeur auxiliaire reconstruisant l'entrée + un scoreur sigmoïde entraîné sur exemples propres contre bruités ; surpasse la MSP sur TIMIT et MNIST.

## Plateforme et implémentation

Sans objet (aucune cible matérielle, réseaux de laboratoire : MLP 3x256 pour MNIST, WRN 40-4 pour CIFAR, LSTM/MLP pour le reste, §3.1). Code : n/r (non mentionné dans le texte lu).

## Résultats

- Erreur/succès par MSP : AUROC 97 (MNIST), 93 (CIFAR-10), 87 (CIFAR-100), qui baisse quand l'erreur du modèle monte (1,69 / 4,96 / 20,7 %) (Table 1). La probabilité moyenne des prédictions fausses reste élevée : 86 / 80 / 66 % (Table 1).
- OOD par MSP : CIFAR-10/SUN AUROC 95, CIFAR-100/SUN 91, MNIST/notMNIST 85 (Table 2) ; MNIST/Uniform 99, MNIST/Gaussian 90 ; probabilité moyenne des OOD 56-92 %. NLP : IMDB/All 94 (Table 4), 15/5 Newsgroups 75 (Table 6) ; POS : WSJ/Twitter 80, WSJ/Weblog 61 (Table 8, cas presque OOD) ; parole : TIMIT/All 97 (Table 9).
- Module d'anormalité : AUROC moyen 97 contre 80 pour le softmax sur TIMIT, 100 contre 93 sur MNIST (Table 11).
- Aucun chiffre matériel (ni latence ni puissance). Base : jeux jouets, aucun résultat sur plantes.
→ reportés dans `benchmarks.csv` (proposition de 6 lignes, vision seulement, plateforme `n/r`) : MNIST, CIFAR-10, CIFAR-100 en détection d'erreur (Table 1, high) ; CIFAR-10/SUN, CIFAR-100/SUN, MNIST/notMNIST en OOD (Table 2, medium : corps de tableau reconstruit à partir du flux de texte). NLP, parole et module d'anormalité non reportés (hors thème de la base).

## Limites et critique

- Tâches et OOD jouets pour la vision (MNIST, CIFAR, SUN, bruit gaussien) ; pas de détection d'objets ni de vidéo. Les OOD faciles (bruit) donnent des AUROC élevés trompeurs.
- La MSP échoue sur les OOD proches (WSJ/Weblog AUROC 61, Table 8) et sur les entrées proches du domaine (« near-OOD »), comme le reconnaissent les auteurs.
- Le module d'anormalité est entraîné avec des bruits synthétiques et évalué sur des types voisins ; comparaison au baseline seulement sur deux tâches.
- Pas de garantie formelle ni de seuil de fonctionnement : les scores AUROC/AUPR ne donnent pas un taux de fausses alarmes ou de détections manquées à un point de fonctionnement, pourtant nécessaire pour la sûreté.
- Le baseline est ancien (2016) ; supplanté par ODIN, Mahalanobis, energy, etc. (connaissance externe, non affirmée par le papier).
- Tableaux 2, 4, 7, 11 listés sans corps extrait : leurs chiffres sont pris dans le texte reconstitué en fin de fichier, dont l'ordre est mélangé (plusieurs légendes mal appariées).

## Pertinence pour le thème (serre)

Axe `calibration-decision`. Référence fondatrice pour le rejet des crops inexploitables et des captures hors distribution du projet SerreIA : la MSP du classifieur de maladies (EfficientNet-B0) est un score de rejet gratuit, sans réentraînement, à comparer au temperature scaling/ECE. Le papier insiste que la MSP n'est pas une confiance calibrée (91 % sur bruit gaussien, §1), donc seuil à choisir sur validation. Laisse ouvert : seuil à rappel donné (AUROC/AUPR seulement, pas de point de fonctionnement, §2), OOD proches (WSJ/Weblog 61, Table 8) analogues à PlantVillage vs PlantDoc, comportement sur plantes et après quantification INT8 sur Hailo (déduit, non traité). Fiche réévaluée depuis la base `fpga` (thème précédent : moniteur FPGA).

## Gaps identifiés

- MSP versus temperature scaling pour rejeter les crops de feuilles hors distribution, avec seuil à rappel « anormal » donné.
- Détection d'écart de domaine PlantVillage vers PlantDoc par MSP : near-OOD réaliste plutôt que bruit ou SUN.
- Effet de la quantification INT8 (Hailo-8L) sur la MSP et le seuil de rejet.

## Statut de lecture

Papier complet (fulltext.md lu en entier ; extraction grobid, ok). Tables 2, 4, 7 et 11 listées sans corps extrait : leurs valeurs sont reprises du texte de flux mélangé, dont les légendes sont décalées d'un numéro (à vérifier sur le PDF) ; Table 1 a un corps lisible. Déduit et non affirmé par les auteurs : application au classifieur de feuilles, comportement en INT8, état de l'art postérieur (ODIN, Mahalanobis, energy).
