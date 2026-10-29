---
id: arxiv-1910.04851-addressing-failure-prediction-learning-model
fiche: todo
date: 2026-10-26
benchmarks: none
---

> **Importée de la base `fpga` le 2026-10-29.** Cette fiche a été écrite pour une autre base (autre thème) : pertinence à réévaluer ici, puis `fiche: done` via `/paper-fiche`. Statut d'origine : done.

# Addressing Failure Prediction by Learning Model Confidence

Charles Corbière, Nicolas Thome, Avner Bar-Hen, Matthieu Cord, Patrick Pérez, 2019, arXiv preprint. https://arxiv.org/abs/1910.04851
Type : preprint non relu par les pairs

## Problème

Prédire les échecs d'un réseau profond : disposer d'une mesure de confiance dont le classement
sépare prédictions correctes et erronées, pour décider de garder la prédiction ou de passer la
main à un humain / système de secours / alarme (§1). Les auteurs reprochent à la Maximum Class
Probability (MCP, softmax) de donner des confiances élevées y compris aux erreurs, d'où un
fort recouvrement des deux distributions (Fig. 1, §1).

## Méthode

- Critère True Class Probability (TCP) : P(Y=y*|w,x) ; garanties : TCP > 1/2 implique prédiction correcte, TCP < 1/K implique erreur ; zone [1/K, 1/2] sans garantie (§2.1). Variante normalisée TCP_r = TCP/MCP (éq. 3).
- Classe y* inconnue au test : ConfidNet apprend TCP par régression (perte L2, éq. 4) sur les features de l'avant-dernière couche du classifieur M (gelé) ; 5 couches denses à sortie sigmoïde, convolutions 1x1 en segmentation (§2.2, §3.1).
- Apprentissage en deux temps : ConfidNet seul, puis fine-tuning d'un encodeur dupliqué (dropout désactivé, learning rate réduit) pour ne pas modifier M (§2.2).
- Comparés : MCP, MCDropout, Trust Score ; métriques FPR-95%-TPR, AUPR-Error, AUPR-Success, AUROC (§3.1-3.2). Code : https://github.com/valeoai/ConfidNet (§3).

## Plateforme et implémentation

Aucune plateforme matérielle : n/r (pas de FPGA, ni de GPU/CPU précisé dans le texte principal ; détails d'entraînement renvoyés au supplementary, non fourni dans fulltext). Code publié (lien ci-dessus). Mesure de puissance, latence, FPS : n/r. Seule remarque de coût : ConfidNet est « aussi rapide que le réseau de segmentation d'origine » (§3.2, affirmation qualitative sans chiffre).

## Résultats

- ConfidNet meilleur que MCP, MCDropout et Trust Score dans tous les réglages en AUPR-Error (Table 1) : MNIST MLP 57,37 contre 37,70 (MCP) ; MNIST SmallConvNet 45,89 contre 35,05 ; SVHN 50,72 contre 48,18 ; CIFAR-10 VGG16 49,94 contre 45,36 ; CIFAR-100 73,68 contre 71,99 ; CamVid SegNet 50,51 contre 48,53. Gain net sur petits modèles, faible sur gros jeux (CIFAR-100 : +1,7 points).
- Trust Score se dégrade sur CIFAR-10/100 et CamVid (Table 1, §3.2) ; sur CamVid il a été calculé sur un échantillon de pixels pour cause de coût (§3.2).
- Fine-tuning de l'encodeur : environ +1 à +2 points (Table 2 : MNIST 43,94 vers 45,89 ; CIFAR-100 72,68 vers 73,68).
- Entraîner sur un jeu de validation (10 %) dégrade les résultats, sauf CIFAR-100 (+0,17) (Table 3, §3.3). Perte BCE inférieure à la perte L2 sur CIFAR-10 (47,95 contre 49,94) et CamVid (48,96 contre 50,51) (Table 4, corps de tableau reconstruit, valeurs aussi données dans le texte).
- Courbes risque-couverture : gain surtout à forte couverture (0,8-0,95 CIFAR-10) (Fig. 3, §3.2).
→ reportés dans `benchmarks.csv` : aucune ligne. Papier de ML purement logiciel (classification, segmentation), sans mesure sur plateforme matérielle ; les métriques sont de qualité de détection d'erreur (AUPR), pas de performance embarquée.

## Limites et critique

- Aucune évaluation matérielle : coût mémoire/calcul de ConfidNet (5 couches denses + encodeur dupliqué après fine-tuning, donc un second encodeur à embarquer) non chiffré. Déduit, non affirmé.
- Jeux petits et réseaux simples (MNIST, SVHN, CIFAR, VGG-16, SegNet) ; pas de détection d'objets ni de personnes, donc pas de notion de faux négatif critique ; l'erreur visée est symétrique (toute mauvaise classe).
- Confiance apprise sur le jeu d'entraînement, où les erreurs sont rares (sur-apprentissage) ; l'entraînement sur validation dégrade (§3.3). Un moniteur appris sur un modèle quantifié ou sous décalage de domaine n'est pas étudié.
- Pas de garantie formelle sur [1/K, 1/2] ; pas d'analyse de robustesse ni de calibration. Gains faibles sur CIFAR-100 ; pas de barres d'erreur visibles dans le texte extrait.
- Table 4 : corps de tableau mal extrait (« sans corps extrait » dans les warnings), valeurs recoupées avec le texte §3.3.
- Preprint 2019, non relu par les pairs.

## Pertinence pour la thèse

Référence directe pour la prédiction d'échec du sujet ARCYS : le moniteur est un petit réseau appris avec (au-dessus des features de) le modèle principal, ce qui correspond à l'idée d'un moniteur appris conjointement au détecteur de personnes. Son critère TCP cible l'erreur par rapport à la vérité terrain, ce qu'on pourrait réorienter vers le faux négatif critique (personne non détectée). Utile aussi comme point de départ pour des sorties anticipées conservatrices (signal de confiance fiable pour déclencher une alarme ou une redondance). Laissé ouvert : détection d'objets, impact de la quantification sur le moniteur, implémentation FPGA du moniteur, coût et WCET du moniteur, absence de garantie certifiable.

## Gaps identifiés

- Moniteur de confiance appris pour détecteurs d'objets (faux négatifs) : non traité.
- Coût matériel (FPGA) et temporel (WCET) d'un moniteur de type ConfidNet : non mesuré.
- Robustesse du moniteur sous quantification et décalage de domaine : non étudiée.

## Statut de lecture

papier complet (fulltext.md lu en entier ; supplementary non disponible). Extraction grobid ok ; Table 4 sans corps extrait.
Ce qui suit est déduit et non affirmé par les auteurs : coût d'un second encodeur embarqué, transposition au faux négatif d'un détecteur de personnes, usage pour sorties anticipées conservatrices.
