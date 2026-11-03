---
id: arxiv-2110.14051-unified-survey-anomaly-novelty-open
fiche: done
date: 2026-11-03
benchmarks: none
---

# A Unified Survey on Anomaly, Novelty, Open-Set, and Out-of-Distribution Detection: Solutions and Future Challenges

Mohammadreza Salehi, Hossein Mirzaei, Dan Hendrycks, Yixuan Li, Mohammad Hossein Rohban, Mohammad Sabokrou, 2021, arXiv preprint. https://arxiv.org/abs/2110.14051 (arXiv 2110.14051 ; pas de DOI). Code des implémentations et benchmarks : https://github.com/taslimisina/osr-ood-ad-methods (Abstract).
Type : preprint non relu par les pairs (survey)

## Problème

Les auteurs posent que l'anomaly detection (AD), la novelty detection (ND, one-class), l'open-set recognition (OSR) et l'OOD detection répondent au même besoin (repérer les échantillons hors de la distribution d'entraînement, donc ne pas les ranger dans une classe connue) mais ont été étudiées séparément, sans « cross-pollination » (Abstract, §1). Il n'existait selon eux pas de survey complet et récent sur l'OOD detection (Abstract). Ils proposent une vue unifiée des quatre domaines, leurs protocoles d'évaluation respectifs et des pistes futures.

## Méthode

Revue de la littérature, pas de méthode nouvelle. Contenu :
- Taxonomie commune : modélisation générative (AE, GAN, auto-régressif/flow) vs discriminative, niveaux de supervision (§2, Fig. 2, Table 1).
- AD/ND (§3) : Isolation Forest, DBSCAN, LOF, OC-SVM/SVDD ; puis Deep SVDD, GT, GOAD, CSI, CutPaste, Mem-AE, ALOCC, student-teacher, Multi-KD, etc.
- OSR (§4) : OpenMax, G-OpenMax, OSRCI, C2AE, CROSR, RPL, CAC, PROSER, etc. ; définition de l'« openness » (Eq. 38).
- OOD detection (§5) : MSP, ODIN (temperature scaling + perturbation), Mahalanobis, Outlier Exposure, energy score, likelihood ratio / complexité d'entrée, MOS, GradNorm, ReAct, VOS (détection d'objets), KNN.
- Idées partagées entre domaines (§6) : compression des normaux, outlier exposure, génération d'outliers, prototypes, pré-entraînement, auto-supervision. Datasets (§7), métriques AUROC / FPR@TPR / AUPR / accuracy / F-mesure (§8), protocoles comparés (§8.6), défis (§9) et pistes (§10).

## Plateforme et implémentation

Sans objet : aucune plateforme matérielle, aucune puissance, aucun FPS, aucune ressource FPGA (n/r). Seule indication de coût : MC-Dropout « 40 fois plus lent » que MSP (§10.1, rapporté sans mesure détaillée) ; ODIN ajoute une passe avant et une passe arrière au test (§10.1). Code : dépôt GitHub annoncé dans l'Abstract (non vérifié ici).

## Résultats

Survey : les chiffres des travaux cités ne sont pas reportés dans `benchmarks.csv` (règle de la skill). Les Tables 7 et 8 reprennent les AUROC des papiers originaux (« reported from the main papers »). Les auteurs ont toutefois leurs propres évaluations (« based on our evaluations », moyenne de 10 exécutions) en classification d'images 32x32, sans plateforme matérielle ni coût mesuré, donc sans ligne justifiable pour ce schéma orienté matériel. → reportés dans `benchmarks.csv` : aucune ligne (`benchmarks: none`).

Constats principaux, tels qu'écrits par les auteurs :
- Aucune méthode n'est bonne à la fois en OOD proche (near, CIFAR-10 vs CIFAR-100) et lointain (far), sauf les approches Outlier Exposure qui utilisent un jeu auxiliaire (§10.1, Tables 3, 4, 6). Ex. CIFAR-10 vs CIFAR-100 : MSP AUROC 87.77, MSP-OE 93.29 (Table 3, valeurs à confirmer, voir Limites).
- Mahalanobis améliore souvent le OOD lointain mais dégrade le proche et varie fortement selon que le jeu OOD est recadré ou redimensionné (§10.1).
- MOS : le FPR@95%TPR de MSP passe de 17.34 % à 76.94 % quand les classes ImageNet passent de 50 à 1000 (§5.20, résultat du papier MOS cité).
- Baseline MSP sur MVTec AD, défauts fréquents comme classes normales et défauts rares comme outliers : AUC 50.2 à 56.4 pour Cable, Capsule, Wood, Carpet, « pas mieux que le hasard » (§10.3, Table 5).
- ViT-B16 pré-entraîné ImageNet-22K moins bon que Softmax/OpenMax/CROSR entraînés from scratch en OSR proche sur SVHN (82.18 contre 88.60 pour Softmax) et MNIST (94.89 contre 97.80) (§10.11, Table 9, moyenne de 5 exécutions, 6 classes connues).
- ODIN ne se confond pas avec la calibration : la température d'ODIN (T élevé, ex. 1000) maximise l'écart ID/OOD et n'a plus de sens comme confiance prédictive ; la calibration utilise un T bien plus doux (§5.2).
- Les protocoles diffèrent : en AD/ND on suppose implicitement 10 % de normaux (une classe CIFAR-10 contre neuf), en OOD les anomalies sont rares, en OSR elles peuvent être majoritaires (§8.6).

## Limites et critique

- Survey de 2021, préprint : ne couvre ni les travaux plus récents ni la détection OOD sur images agronomiques. Aucun résultat sur PlantVillage / PlantDoc ou des données de plantes (déduit de la lecture : aucun de ces mots-clés n'apparaît).
- Les tableaux 3, 4, 6 sont des évaluations internes sur images 32x32 (CIFAR, TinyImageNet) et jeux OOD synthétiques (Gaussian, Rademacher, Blob) : leur transfert à des feuilles en conditions de serre n'est pas démontré (déduit).
- Tableaux 7, 8, 9 : chiffres rapportés des papiers d'origine, protocoles et architectures non harmonisés ; les auteurs ne donnent pas les écarts-types.
- Extraction : les tableaux 2, 7, 9 sont listés « sans corps extrait » dans `metadata.json` ; les corps visibles dans `fulltext.md` sont reconstitués et partiellement décalés (ex. Table 3, ligne MSP : les valeurs 94.78 et 70.50 figurent à la fois en FPR95 et en AUROC/AUPR, ce qui ressemble à un décalage de colonnes ; ligne ODIN : AUPR identique à MC-Dropout). Ne pas citer ces cellules sans vérifier sur le PDF. Table 7 est illisible (lignes concaténées).
- Incohérences de rédaction relevées : Table 3 annoncée « inlier CIFAR-10 » avec une colonne CIFAR-100 ; numérotation des sections de §10 incomplète (10.2, 10.8 absentes en texte propre).
- Aucune mesure d'énergie, de latence ou de mémoire sur cible embarquée : l'information « coût de calcul » se limite à des ordres de grandeur (MC-Dropout x40, ODIN passe avant + arrière).

## Pertinence pour la thèse

Pour SerreIA (axes `domain-shift`, `calibration-decision`, `anomaly`, `surveys`) : référence de cadrage pour la question « réduire les fausses alertes `anormal` à rappel donné » et pour le test hors domaine PlantVillage vers PlantDoc, vu comme un problème d'OOD / de décalage de domaine. Apports exploitables, à valider sur les données du projet :
- MSP est un baseline difficile à battre (§5.1) et sert de point de départ au seuil de rejet sur les têtes du classifieur ; le score d'énergie est sans hyperparamètre (§5.15) ; ReAct se combine avec MSP / ODIN / énergie (§5.23), tous post hoc, donc compatibles avec un modèle EfficientNet-B0 déjà entraîné.
- Distinction ODIN / calibration (§5.2) : le temperature scaling de calibration (ECE) et celui d'ODIN poursuivent des objectifs opposés ; ne pas les mélanger dans le pipeline.
- Protocole : évaluer sur OOD proche et lointain (§10.1) et rapporter FPR@95TPR en plus de l'AUROC (§8.2).
- Outlier Exposure : des images hors-serre (fonds, autres plantes) peuvent servir d'outliers auxiliaires (§5.6) ; l'avantage d'OE est le seul constaté comme robuste à la fois en proche et en lointain (§10.1).
- Mise en garde ViT pré-entraîné (§10.11) et défis OSR sur différences fines (§10.3), proches du cas maladies visuellement voisines.
Reste ouvert : aucun chiffre sur le surcoût en edge (RPi 5 / Hailo), pas de cas agronomique, pas de traitement de l'agrégation multi-feuilles.

## Gaps identifiés

- Détection OOD / rejet de classes inconnues sur images de plantes en conditions réelles (PlantDoc), absente de ce survey.
- Coût de calcul et énergie des détecteurs OOD post hoc (MSP, énergie, Mahalanobis, KNN, ODIN) sur edge : non mesurés ici.
- Calibration et détection OOD jointes (le papier les oppose, §5.2) : pas de protocole commun pour fixer un seuil à rappel donné.
- Open-world recognition avec apprentissage incrémental (nouvelles maladies) : cité comme défi (§10.10), pas de solution.

## Statut de lecture

papier complet (fulltext.md lu en entier, lignes 1 à 1454 ; extraction `grobid`, `extraction.ok` vrai). Les tableaux 2, 7, 9 n'ont pas de corps fiable extrait (légende seule, corps reconstitué) ; Tables 3, 4, 5, 6, 8, 9 lus mais à vérifier sur le PDF avant citation chiffrée.
Ce qui suit est déduit et non affirmé par les auteurs : l'absence d'images agronomiques dans le survey ; le décalage de colonnes de la Table 3 ; la pertinence pour SerreIA (utilisation de MSP, énergie, OE avec des images hors-serre) ; le fait que les évaluations internes ne se transfèrent pas aux feuilles.
