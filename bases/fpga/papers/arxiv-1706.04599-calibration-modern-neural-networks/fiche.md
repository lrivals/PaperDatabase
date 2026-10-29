---
id: arxiv-1706.04599-calibration-modern-neural-networks
fiche: done
date: 2026-10-26
benchmarks: none
---

# On Calibration of Modern Neural Networks

Chuan Guo, Geoff Pleiss, Yu Sun, Kilian Q. Weinberger, 2017, arXiv preprint (la version texte indique ICML 2017, PMLR 70, mais `metadata.json` la range en preprint). https://arxiv.org/abs/1706.04599
Type : preprint non relu par les pairs selon les métadonnées de la base (venue ICML 2017 non vérifiée ici).

## Problème

Un classifieur doit indiquer quand il risque de se tromper : la probabilité associée à la classe prédite doit refléter sa vraisemblance réelle de justesse (calibration, éq. 1, §2). Les auteurs constatent que les réseaux modernes, profonds et peu régularisés, sont mal calibrés (surconfiance), contrairement à ceux d'il y a dix ans (§1, Fig. 1).

## Méthode

- Métriques : diagrammes de fiabilité, ECE (15 bins, éq. 3), MCE (éq. 5), NLL (§2).
- Étude des facteurs de miscalibration : profondeur, largeur, Batch Normalization, weight decay (§3, Fig. 2) ; surapprentissage de la NLL sans surapprentissage de l'erreur 0/1 (Fig. 3).
- Méthodes de post-traitement sur jeu de validation, poids du réseau figés (§4) : histogram binning, isotonic regression, BBQ, Platt scaling, matrix / vector scaling, et temperature scaling (un seul scalaire T, logits divisés par T, T optimisé en NLL sur la validation, §4.2 éq. 9). T ne change pas l'argmax : la précision est inchangée.
- Expériences : 6 jeux d'images (Birds, Cars, ImageNet, CIFAR-10/100, SVHN) avec ResNet, ResNet SD, Wide ResNet, DenseNet, LeNet ; 4 jeux de texte (20 News, Reuters, SST) avec DAN et TreeLSTM (§5).

## Plateforme et implémentation

Aucune plateforme matérielle : entraînement et évaluation logiciels (Torch7 cité pour l'implémentation de T via `nn.MulConstant`, §5). Matériel, puissance, latence : n/r. Code publié : non précisé dans le texte lu.

## Résultats

- Les modèles non calibrés ont typiquement un ECE de 4 à 10 % (Table 1, texte §5) ; exemples : ResNet 110 sur CIFAR-100, 16,53 % avant, 1,26 % après temperature scaling (Table 1) ; DenseNet 161 sur ImageNet, 6,28 % puis 1,99 % (Table 1).
- Temperature scaling surpasse les autres méthodes sur les tâches de vision et reste comparable sur le texte ; il fait mieux que vector et matrix scaling, plus généraux (§5). Matrix scaling échoue sur beaucoup de classes (21,13 % sur Birds, non convergé sur ImageNet, Table 1).
- Les méthodes à bins modifient souvent les prédictions de classe et dégradent la précision (§5, renvoi Table S1-S3 absente du texte extrait).
- Coût : T se trouve en environ 10 itérations de gradient conjugué, une fraction de seconde (§5 « Computation time »).
- Calibration et précision ne sont pas optimisées par les mêmes réglages : plus de weight decay améliore la calibration au-delà de l'optimum de précision (§3).
→ aucune ligne dans `benchmarks.csv` : article de ML purement logiciel, sans mesure sur plateforme matérielle (FPGA, Jetson, MCU) ; `benchmarks: none`.

## Limites et critique

- Calibration mesurée sur la classe prédite d'une classification multiclasse ; pas de détection d'objets, pas de calibration par boîte ni de faux négatifs de détection.
- Hypothèse que validation et test suivent la même distribution (§4) ; aucune étude du décalage de domaine.
- ECE dépendant du binning (les auteurs le notent, §5) ; la Table 1 est reconstruite à l'extraction, chiffres à vérifier avant citation fine.
- Causalité non établie entre capacité, BN, weight decay et miscalibration (§3 : « we cannot claim causality »).
- Aucune considération de coût matériel, de quantification ou de virgule fixe : l'effet de la quantification sur la calibration n'est pas étudié (déduit de l'absence dans le texte).
- Calibration globale : une bonne ECE ne garantit pas que les erreurs critiques (faux négatifs) soient détectées, point non traité par les auteurs (déduit).

## Pertinence pour la thèse

Référence de base de l'axe `failure-prediction` du sujet ARCYS. Elle donne le vocabulaire et les métriques de la confiance fiable (ECE, MCE, NLL, diagrammes de fiabilité) et une brique très peu coûteuse : le temperature scaling, un scalaire appliqué aux logits, implémentable sur FPGA en un produit à virgule fixe, sans changer la décision ni la précision. Utile comme référence de comparaison pour un moniteur de prédiction d'échec ciblé sur les faux négatifs d'un détecteur de personnes, et pour les seuils des sorties anticipées conservatrices (un seuil de confiance n'a de sens que si la confiance est calibrée ; MSDNet et BranchyNet utilisent de tels seuils). Reste ouvert : calibration de détecteurs type YOLO, calibration après quantification INT8 / virgule fixe, calibration sous décalage de domaine, lien avec le WCET du moniteur. Raisonnement de pertinence déduit, non affirmé par les auteurs, dont l'exemple est le piéton pour véhicule autonome (§1).

## Gaps identifiés

- Calibration d'un détecteur d'objets (score d'objectness et de classe) plutôt que d'un classifieur, avec attention aux faux négatifs.
- Effet de la quantification (INT8, virgule fixe) sur la calibration et sur T.
- Coût matériel d'un moniteur de confiance sur FPGA (n/r ici).

## Statut de lecture

Papier complet : `fulltext.md` lu en entier (extraction grobid, `extraction.ok` vrai). Les Tables S1 à S3 (MCE, erreur, NLL) et la Table 1 sont reconstruites ou absentes du texte extrait ; les valeurs de la Table 1 citées ci-dessus sont à recouper avec le PDF avant usage chiffré.
Ce qui suit est déduit et non affirmé par les auteurs : l'implémentation en virgule fixe sur FPGA, le lien avec les faux négatifs d'un détecteur, l'absence d'étude de la quantification.
