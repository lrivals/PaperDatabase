---
id: arxiv-2305.01823-out-distribution-detection-algorithms-robust
fiche: done
date: 2026-11-03
---

# Out-of-distribution detection algorithms for robust insect classification

Mojdeh Saadati, Aditya Balu, Shivani Chiranjeevi, Talukder Zaki Jubery, Asheesh K Singh, Soumik Sarkar, Arti Singh, Baskar Ganapathysubramanian, 2023, arXiv preprint. https://arxiv.org/abs/2305.01823
Type : preprint non relu par les pairs

## Problème

Un classifieur d'insectes (142 espèces) produit une prédiction fausse sur des images hors distribution (véhicules, visages, insectes non appris, images floues) ; les auteurs veulent qu'il s'abstienne et passe la main à un humain (§1). Ils étudient des méthodes OOD « extrusives » (enveloppant un classifieur déjà entraîné, sans réentraînement), jugées adaptées aux modèles agricoles coûteux à réentraîner (§1).

## Méthode

Trois détecteurs OOD comparés (§2.1) : MSP (probabilité softmax maximale, seuil), Mahalanobis (MAH, gaussiennes par classe sur les features de l'avant-dernière couche, covariance partagée, entraîné sur une moitié du split de validation) et énergie (EBM, E(x) = -T log Σ exp(f_i(x)/T), T = 1). Trois classifieurs (§2.2) : ResNet50 (23 M de paramètres), RegNetY32 (145 M), VGG11 (133 M). 15 classifieurs de précision croissante par architecture, soit 45 modèles, de 80 % à 97,5 % de précision de validation (§3.1) ; entraînement : entropie croisée, AdamW, lr 1e-3, batch 256 (§3.1).
Données (§2.3) : ID = sous-ensemble iNaturalist de 142 espèces, 2 M d'images, split 7/3 train/validation ; la validation est coupée en deux (entraînement de MAH / test). Quatre jeux OOD : ImageNet sans insectes (9730 images, far OOD), Human Face (3059, far OOD), Non-Insecta iNaturalist (74 740, near OOD), OODInsect (56 487 insectes hors des 142 classes, near OOD). Métriques : AUROC et FPR95 (§2.4). Trois axes d'analyse : précision/architecture (§3.1), degré de dissimilarité du jeu OOD (§3.2), déséquilibre des classes (§3.3).

## Plateforme et implémentation

Calcul sur cluster HPC, une carte NVIDIA A100 80 Go (§2). Aucune mesure de latence, de puissance ni de déploiement edge : `n/r`. Code et poids : non mentionnés dans le texte lu (donc « non publiés » à notre connaissance de ce texte).

## Résultats

- Conclusion qualitative : EBM est presque toujours meilleur que MAH et MSP sur les trois architectures (§3.1, Fig. 6) et sur les quatre jeux OOD (§3.2, Fig. 7) ; MSP a un FPR95 élevé quel que soit le jeu OOD (§3.2). RegNetY32 + EBM est présenté comme la meilleure combinaison (§3).
- Chiffres rapportés pour RegNetY32 + EBM : AUROC = 0,72 ; au seuil d'énergie 31,0, FPR = 0,31, TPR = 0,69, « accuracy » OOD = 68,97 (§3, avant 3.1 ; Fig. 5). Le jeu OOD de ce chiffre n'est pas précisé. Quantiles d'énergie ID (médiane 36,68) et OOD (médiane 23,69), chevauchement partiel (§3, Fig. 5b).
- Précision du classifieur vs OOD (§3.1) : pas d'amélioration de l'AUROC de EBM avec la précision pour les grands modèles (VGG11, RegNetY32) ; corrélation observée seulement pour ResNet50. Évalué sur Non-Insecta, ID rééchantillonné à 74 740.
- Dissimilarité (§3.2) : meilleurs résultats sur ImageNet et OODInsect ; les auteurs avancent une hypothèse (pré-entraînement sur Instagram) non testée.
- Déséquilibre (§3.3, Fig. 8) : EBM robuste, MAH sensible. Le texte de la conclusion est incohérent : il dit EBM et MSP insensibles, la légende de la Fig. 8 dit que seul MAH varie.
- Valeurs par figure uniquement (Fig. 6, 7, 8) : aucune valeur numérique extractible du texte.
→ reportés dans `benchmarks.csv` : 2 lignes proposées (RegNetY32 + EBM : AUROC 0,72 ; exactitude OOD 68,97 au seuil 31,0), `confidence: medium` (valeurs du texte), `chunk_id` 2305.01823#009.0.

## Limites et critique

- AUROC de 0,72 : faible. Le message « EBM excellent » repose sur des comparaisons relatives lues sur des figures, sans chiffres ni intervalles de confiance ni répétitions.
- Le jeu OOD du chiffre principal n'est pas dit ; l'« accuracy » 68,97 n'est pas définie (équilibre ID/OOD non précisé) ; le seuil 31,0 est choisi sur les données d'évaluation (risque de sur-ajustement, déduit).
- Contradiction interne sur la sensibilité de MSP au déséquilibre (§3.3 / conclusion / Fig. 8). Texte de conclusion tronqué par l'extraction.
- Qualifier EBM de « discriminatif » et MAH de « génératif » est inversé dans l'intro (§1) par rapport à l'usage ; sans conséquence sur les résultats.
- Pas de comparaison avec des méthodes intrusives ni plus récentes (ODIN, KNN, ViM) ; pas de temps de calcul ; pas de code publié.
- Domaine : insectes iNaturalist, pas des feuilles malades de serre ; le transfert aux maladies est affirmé, non testé.

## Pertinence pour la thèse

Pertinence pour SerreIA : axe `calibration-decision` / OOD et rejet (questions de recherche sur le rejet des crops inexploitables et hors distribution). Apporte une méthode d'enveloppe (énergie, sans réentraînement) applicable à l'EfficientNet-B0 du projet, avec un coût d'inférence quasi nul (déduit : calcul sur les logits). Montre aussi que MSP seul donne beaucoup de fausses acceptations et que la précision ne garantit pas la qualité OOD. Les chiffres ne se transposent pas : autre domaine, autre jeu OOD, détecteur modeste (AUROC 0,72). Laisse ouvert : test sur PlantVillage vs PlantDoc, seuil par rappel donné, combinaison avec la calibration (temperature scaling) et l'agrégation multi-feuilles.

## Gaps identifiés

- OOD/rejet sur feuilles de plantes (PlantDoc comme OOD de PlantVillage) : non couvert ici.
- Choix du seuil à rappel donné et coût des fausses alertes : non traité (seuil optimisé sur le test).
- Pas de coût edge (RPi/Hailo) des scores OOD.

## Statut de lecture

papier complet (`fulltext.md` lu en entier ; extraction GROBID, `extraction.ok: true`, conclusion partiellement tronquée ; figures non lues, donc Fig. 5 à 8 non chiffrées).
Ce qui suit est déduit et non affirmé par les auteurs : seuil choisi sur les données d'évaluation ; coût d'inférence quasi nul de l'énergie ; non-publication du code (absent du texte) ; pertinence pour EfficientNet-B0 / SerreIA.
