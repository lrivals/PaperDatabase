---
id: arxiv-2403.02886-revisiting-confidence-estimation-reliable-failure
fiche: done
date: 2026-11-03
benchmarks: none
---

# Revisiting Confidence Estimation: Towards Reliable Failure Prediction

Fei Zhu, Xu-Yao Zhang, Zhen Cheng, Cheng-Lin Liu, 2024, arXiv preprint. https://arxiv.org/abs/2403.02886
Type : preprint non relu par les pairs (le texte dit étendre une publication de conférence [48] ; il ne mentionne ni TPAMI ni aucune venue de revue, donc la version publiée IEEE TPAMI 46(5) n'est pas confirmée par le texte)

## Problème

Les DNN sont sur-confiants sur leurs erreurs (échantillons mal classés de classes connues, et OOD). Les auteurs se demandent si une confiance calibrée, ou issue d'une méthode de détection OOD, permet de filtrer les prédictions erronées (failure prediction = misclassification detection = selective classification, §2.3). Ils constatent que la plupart de ces méthodes nuisent à cette tâche (§1, Fig. 1).

## Méthode

Étude empirique (§3) de méthodes de calibration (mixup, label smoothing, focal, Lp norm, temperature scaling) et de détection OOD (LogitNorm, OE, ODIN, energy, ReAct, MLogit) évaluées en failure prediction (AURC, E-AURC, AUROC, FPR95, AUPR-S/E). Analyse théorique : décomposition calibration / grouping / aléatoire des scoring rules propres (§3.3.1) et désalignement des règles de rejet de Bayes entre failure prediction (règle de Chow, max P(y|x) ≥ 1-c) et détection OOD (rapport de densités) (§3.3.2, Prop. 2-3). Méthode proposée FMFP (§4.1) : recherche de minima plats par combinaison de SWA (moyenne de poids) et SAM (perturbation de poids), plug-and-play, sans réseau auxiliaire ni exemples d'erreur à l'entraînement. Justification par borne PAC-Bayes (§4.1.3) et phénomène de « reliable overfitting » (AUROC décroît en fin d'entraînement alors que l'accuracy croît, Fig. 9). Classification d'images seulement : pas de détection d'objets.

## Plateforme et implémentation

Aucune plateforme d'inférence ni mesure de puissance (n/r) : entraînement SGD, 200 epochs, batch 128 sur CIFAR-10/100 (§3.1), 90 epochs sur Tiny-ImageNet (App. C). GPU, FPS, latence, coût de calcul de l'inférence : n/r. Code publié : https://github.com/Impression2805/FMFP (Abstract). Pas de quantification ni de matériel embarqué. Coût d'inférence de FMFP identique au modèle de base (déduit : seuls les poids changent, un seul passage avant), à comparer à MCDropout (≈100 passages, §4.2) et aux ensembles.

## Résultats

- Les méthodes de calibration/OOD dégradent la failure prediction : ResNet110 CIFAR-10, AURC (×10³) baseline 9.52, mixup 16.27, LS 25.89, energy 15.13, ODIN 20.82 (Table 1) ; temperature scaling n'apporte rien, AUROC CIFAR-10 ResNet 90.76 baseline, 89.15 TS-valid (Table 2) ; même constat sur ImageNet (Fig. 4).
- FMFP meilleur que baseline MSP, CRL et OpenMix : sur ResNet110, +3.94 et +2.47 points d'AUROC sur CIFAR-10 et CIFAR-100 (§4.2, Table 3). Comparaison VGG-16 CIFAR-10 : AUROC 93.56 contre 91.18 (baseline) et 92.05 (ConfidNet) ; AURC 6.31 contre 12.66 (Table 5).
- Long-tailed (CIFAR-LT, ρ=100, ResNet-32, §4.3) : CRL dégrade la failure prediction, FMFP la maintient. Covariate shift (CIFAR-10/100-C, 75 corruptions) : FMFP > baseline et CRL, ex. +13.05 points d'AUROC sur « defocus » niveau 5 (§4.4, Fig. 16). Détection OOD aussi améliorée (Table 9, §4.5).
- Benchmarks : aucune ligne justifiable pour `benchmarks.csv` (colonnes plateforme / FPS / puissance sans objet : article d'apprentissage automatique sans mesure d'inférence sur plateforme, jeux CIFAR sans rapport avec les plantes) → `benchmarks: none`. Les métriques d'échec de prédiction ci-dessus restent dans cette fiche.
- VGG-16 : les valeurs baseline, MCDropout, Trust-Score, ConfidNet viennent de [40] (†), pas des auteurs (Table 5).

## Limites et critique

- Tâche de classification sur petites images (CIFAR, Tiny-ImageNet, ImageNet), aucune image de plante, pas de détection d'objets : transfert à un classifieur de maladies en décalage de domaine non démontré (déduit).
- Score = confiance de sortie du réseau principal : pas d'évaluation de coût ni de latence d'inférence.
- Pas de garantie formelle sur le taux d'erreurs manquées à un seuil donné : on optimise l'AUROC/AURC, pas un rappel conservateur des erreurs. PAC-Bayes borne l'erreur de généralisation, pas la séparation des confiances (le lien est une conjecture, §4.1.1).
- Résultats moyennés sur 3 runs, écarts-types parfois importants ; Tables 3-4 en partie illisibles dans l'extraction (corps du tableau reconstruit, avertissement `extraction.warnings`) : seuls les chiffres du texte, de Table 1, 2 et 5 sont cités ici. Reproductibilité : code publié.
- SAM double le coût d'entraînement (déduit, deux gradients par pas) ; non discuté.

## Pertinence pour la base serre

Axe `calibration-decision` (profile.md : calibrer un classifieur, choisir les seuils pour réduire les fausses alertes « anormal » à rappel donné, rejeter les crops inexploitables ou hors distribution). Apports, en lien avec le classifieur EfficientNet-B0 (PlantVillage + CCMT, test PlantDoc) :

- Avertissement méthodologique (lu, Tables 1-2, §3.2) : temperature scaling, label smoothing, mixup et scores OOD (energy, ODIN, MLogit) abaissent l'ECE ou améliorent la détection OOD mais dégradent la séparation entre prédictions justes et fausses. Pour SerreIA, évaluer le rejet directement en AURC / AUROC (courbe risque-couverture) et pas seulement en ECE après temperature scaling.
- Règle de Chow (Prop. 2, §3.3.2) : seuil sur max P(y|x) ≥ 1-c, avec un coût de rejet c : cadre pour fixer le seuil « anormal » à partir d'un coût de fausse alerte. Distinction entre rejet d'erreurs in-domain (zone de confusion entre classes) et rejet OOD (rapport de densités) : un crop de fond ou une feuille hors classes (PlantDoc) relève du second, une confusion entre maladies du premier ; un seul score ne sert pas forcément les deux (lu, Fig. 6-7).
- FMFP (SWA + SAM, §4.1) : entraînement seul, sans surcoût d'inférence (déduit) ; covariate shift CIFAR-10/100-C (§4.4, Fig. 16) proche, par analogie seulement, du décalage PlantVillage vers terrain. Transfert aux feuilles, à EfficientNet-B0 et à PlantDoc : non testé par les auteurs (déduit).
- Pas de chiffre exploitable pour l'edge (Raspberry Pi, Hailo) : la quantification INT8 pourrait modifier la séparation de confiance, non étudié.

Reste ouvert pour la base : validité sur images de plantes, agrégation de plusieurs feuilles par capture, effet de la quantification Hailo sur les scores.

## Gaps identifiés

- Failure prediction pour un pipeline détecteur de feuilles + classifieur (faux négatifs de détection, crops inexploitables) : non traitée ici.
- Effet de la quantification (INT8) sur la séparation de confiance et sur les minima plats : non étudié.
- Coût d'un moniteur de confiance sur edge (Raspberry Pi, Hailo) : absent.
- Agrégation de plusieurs prédictions (feuilles d'une capture) et rejet au niveau de la capture : absent ; évaluation sur images de plantes ou en décalage laboratoire vers terrain : absente.

## Statut de lecture

Papier complet (fulltext.md lu en entier, backend grobid). Tables 3 et 4 : corps partiellement extrait, chiffres non utilisés. Fiche importée de la base `fpga`, faits revérifiés contre fulltext.md (Tables 1, 2, 5, §4.2, §4.4) ; section Pertinence réécrite pour serre. Déduit et non affirmé par les auteurs : coût d'inférence de FMFP, coût d'entraînement de SAM, transfert aux images de plantes, à EfficientNet-B0 et à la quantification, lien avec SerreIA. Version publiée TPAMI non vérifiable dans le texte.
