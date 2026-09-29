---
id: arxiv-1610.02136-baseline-detecting-misclassified-out-distribution
fiche: done
date: 2026-09-29
benchmarks: none
---

# A Baseline for Detecting Misclassified and Out-of-Distribution Examples in Neural Networks

Dan Hendrycks, Kevin Gimpel, 2017, International Conference on Learning Representations (ICLR) 2017. https://arxiv.org/abs/1610.02136 (DOI n/r)
Type : conférence (ICLR 2017) ; version arXiv lue.

## Problème

Un classifieur échoue silencieusement quand la distribution de test diffère de celle d'entraînement, avec des prédictions à haute confiance (§1). Deux tâches : prédire si un exemple est mal classé (erreur/succès) et s'il est hors distribution (OOD) (§2). Les auteurs veulent un baseline simple et une évaluation standardisée.

## Méthode

- Baseline : probabilité softmax maximale (MSP) comme score ; évaluation par AUROC (base 50 %) et AUPR, avec « Succ/Err » et « In/Out » comme classe positive (§2, §3). Ils insistent que la MSP n'est pas une confiance calibrée (bruit gaussien sur MNIST : 91 % de « confiance », §1) mais discrimine quand même.
- Tâches : vision (MNIST, CIFAR-10, CIFAR-100 ; OOD = SUN, Omniglot, notMNIST, bruit), NLP (IMDB, 20 Newsgroups, Reuters, POS tagging WSJ/tweets) et parole (TIMIT, CTC, softmax sans le symbole blank) (§3).
- Module d'anormalité (§4) : décodeur auxiliaire reconstruisant l'entrée + un scoreur sigmoïde entraîné sur exemples propres contre bruités ; surpasse la MSP sur TIMIT et MNIST.

## Plateforme et implémentation

Sans objet (aucune cible matérielle, réseaux de laboratoire : MLP 3x256 pour MNIST, WRN 40-4 pour CIFAR, LSTM/MLP pour le reste, §3.1). Code : n/r (non mentionné dans le texte lu).

## Résultats

- Erreur/succès : AUROC 97 (MNIST), 93 (CIFAR-10), 87 (CIFAR-100), qui baisse avec l'erreur du modèle (Table 1).
- OOD : CIFAR-10/SUN AUROC 95, CIFAR-100/SUN 91, MNIST/notMNIST 85 (Table 2, corps extrait du texte : chiffres lus dans le dump, tableaux « sans corps extrait » selon les avertissements, à vérifier). NLP : IMDB/All 94 (Table 4), 15/5 Newsgroups 75 (Table 6). POS : WSJ/Weblog 61 (Table 8), cas presque OOD.
- Module d'anormalité : moyenne AUROC 97 contre 80 pour le softmax sur TIMIT, 100 contre 93 sur MNIST (Table 11).
- Aucun chiffre matériel : pas de ligne dans `benchmarks.csv` (`benchmarks: none`).

## Limites et critique

- Tâches et OOD jouets pour la vision (MNIST, CIFAR, SUN, bruit gaussien) ; pas de détection d'objets ni de vidéo. Les OOD faciles (bruit) donnent des AUROC élevés trompeurs.
- La MSP échoue sur les OOD proches (WSJ/Weblog AUROC 61, Table 8) et sur les entrées proches du domaine (« near-OOD »), comme le reconnaissent les auteurs.
- Le module d'anormalité est entraîné avec des bruits synthétiques et évalué sur des types voisins ; comparaison au baseline seulement sur deux tâches.
- Pas de garantie formelle ni de seuil de fonctionnement : les scores AUROC/AUPR ne donnent pas un taux de fausses alarmes ou de détections manquées à un point de fonctionnement, pourtant nécessaire pour la sûreté.
- Le baseline est ancien (2016) ; supplanté par ODIN, Mahalanobis, energy, etc. (connaissance externe, non affirmée par le papier).
- Tableaux 2, 4, 7, 11 listés sans corps extrait : leurs chiffres sont pris dans le texte reconstitué en fin de fichier, dont l'ordre est mélangé (plusieurs légendes mal appariées).

## Pertinence pour la thèse

Référence fondatrice pour la surveillance à l'exécution (axe `safety-certification`) : MSP comme moniteur OOD/erreur, très peu coûteux, donc implémentable sur FPGA en post-traitement du réseau (un softmax et un seuil), et le module d'anormalité rappelle le principe de l'autoencodeur comme détecteur (lien avec l'axe autoencodeurs). Ne traite ni le détecteur d'objets YOLO (sorties de type objectness, pas softmax global), ni le matériel, ni la certification.

## Gaps identifiés

- Moniteur OOD/erreur sur détecteur d'objets (YOLO) et sur FPGA : coût matériel, latence, comportement en quantification INT8 (la MSP dépend de la calibration des logits).
- Choix et validation d'un seuil de rejet avec taux de fausse alarme garanti (zone industrielle : les personnes manquées coûtent plus que les fausses alarmes).
- Évaluation des moniteurs sur near-OOD réalistes (changement d'éclairage, EPI, occultation) plutôt que bruit ou datasets étrangers.

## Statut de lecture

Papier complet (fulltext.md lu en entier). Tables 2, 4, 7 et 11 sans corps propre : leurs valeurs sont reprises du texte de flux mélangé ; les légendes sont décalées d'un numéro, à vérifier sur le PDF. Déduit et non affirmé par les auteurs : implémentabilité sur FPGA, limites de la MSP sur détecteurs d'objets et en INT8, état de l'art postérieur.
