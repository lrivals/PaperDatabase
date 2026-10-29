---
id: arxiv-2403.02886-revisiting-confidence-estimation-reliable-failure
fiche: done
date: 2026-10-26
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

Aucune plateforme matérielle : entraînement SGD, 200 epochs, batch 128 sur CIFAR-10/100 (§3.1), 90 epochs sur Tiny-ImageNet (App. C). GPU, FPS, latence, coût de calcul de l'inférence : n/r. Code publié : https://github.com/Impression2805/FMFP (Abstract). Pas de quantification ni de FPGA. Coût d'inférence de FMFP identique au modèle de base (déduit : seuls les poids changent, un seul passage avant), à comparer à MCDropout (≈100 passages, §4.2) et aux ensembles.

## Résultats

- Les méthodes de calibration/OOD dégradent la failure prediction : ResNet110 CIFAR-10, AURC (×10³) baseline 9.52, mixup 16.27, LS 25.89, energy 15.13, ODIN 20.82 (Table 1) ; temperature scaling n'apporte rien, AUROC CIFAR-10 ResNet 90.76 baseline, 89.15 TS-valid (Table 2) ; même constat sur ImageNet (Fig. 4).
- FMFP meilleur que baseline MSP, CRL et OpenMix : sur ResNet110, +3.94 et +2.47 points d'AUROC sur CIFAR-10 et CIFAR-100 (§4.2, Table 3). Comparaison VGG-16 CIFAR-10 : AUROC 93.56 contre 91.18 (baseline) et 92.05 (ConfidNet) ; AURC 6.31 contre 12.66 (Table 5).
- Long-tailed (CIFAR-LT, ρ=100, ResNet-32, §4.3) : CRL dégrade la failure prediction, FMFP la maintient. Covariate shift (CIFAR-10/100-C, 75 corruptions) : FMFP > baseline et CRL, ex. +13.05 points d'AUROC sur « defocus » niveau 5 (§4.4, Fig. 16). Détection OOD aussi améliorée (Table 9, §4.5).
- Benchmarks : aucune ligne justifiable, article ML sans mesure sur plateforme matérielle → `benchmarks: none`.

## Limites et critique

- Tâche de classification sur petites images (CIFAR, Tiny-ImageNet, ImageNet), pas de détection d'objets : la notion d'« échec » (erreur de classe) n'a pas d'équivalent direct pour un faux négatif de détecteur (boîte manquante), cible de la thèse.
- Score = confiance de sortie du réseau principal, donc suppose un passage complet : pas de sortie anticipée, pas d'évaluation de coût ni de latence, pas de WCET.
- Pas de garantie formelle sur le taux d'erreurs manquées à un seuil donné : on optimise l'AUROC/AURC, pas un rappel conservateur des erreurs. PAC-Bayes borne l'erreur de généralisation, pas la séparation des confiances (le lien est une conjecture, §4.1.1).
- Résultats moyennés sur 3 runs, écarts-types parfois importants ; Tables 3-4 en partie illisibles dans l'extraction (corps du tableau reconstruit, avertissement `extraction.warnings`) : seuls les chiffres du texte, de Table 1, 2 et 5 sont cités ici. Reproductibilité : code publié.
- SAM double le coût d'entraînement (déduit, deux gradients par pas) ; non discuté.

## Pertinence pour la thèse

Rattachement ARCYS : fondement de la partie « prédiction d'échec » du moniteur (profile.md, questions ARCYS). Apporte (1) un avertissement méthodologique : calibrer ou utiliser un score OOD ne suffit pas à prédire les erreurs, il faut évaluer le moniteur directement en AURC/AUROC ; (2) une règle de rejet de Chow et un cadre risque-couverture adaptés à des sorties anticipées conservatrices (rejeter vers le réseau complet ce qui est incertain) ; (3) FMFP, entraînement par minima plats sans surcoût d'inférence, compatible avec un moniteur léger sur FPGA et probablement avec la quantification (flatness, hypothèse déduite non testée). Reste ouvert : détection de personnes (faux négatifs), quantification INT8/INT4, matériel, WCET, garanties.

## Gaps identifiés

- Failure prediction pour des détecteurs (faux négatifs de personnes) : non traitée ici.
- Effet de la quantification sur la séparation de confiance et sur les minima plats : non étudié.
- Coût matériel d'un moniteur de confiance (FPGA) et son WCET : absent.
- Couplage entre seuil de rejet et sorties anticipées conservatrices : absent.

## Statut de lecture

Papier complet (fulltext.md lu en entier, backend grobid). Tables 3 et 4 : corps partiellement extrait, chiffres non utilisés. Déduit et non affirmé par les auteurs : coût d'inférence de FMFP, coût d'entraînement de SAM, transfert à la détection d'objets et à la quantification, lien avec la thèse. Version publiée TPAMI non vérifiable dans le texte.
