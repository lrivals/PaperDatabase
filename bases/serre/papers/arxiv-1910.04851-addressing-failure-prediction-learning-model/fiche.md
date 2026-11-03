---
id: arxiv-1910.04851-addressing-failure-prediction-learning-model
fiche: done
date: 2026-11-03
---

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

Aucune plateforme matérielle : n/r (ni GPU ni CPU précisé dans le texte principal ; détails d'entraînement renvoyés au supplementary, absent de fulltext). Code publié (lien ci-dessus). Mesure de puissance, latence, FPS : n/r. Seule remarque de coût : ConfidNet est « aussi rapide que le réseau de segmentation d'origine » (§3.2, affirmation qualitative sans chiffre).

## Résultats

- ConfidNet meilleur que MCP, MCDropout et Trust Score dans tous les réglages en AUPR-Error (Table 1) : MNIST MLP 57,37 contre 37,70 (MCP) ; MNIST SmallConvNet 45,89 contre 35,05 ; SVHN 50,72 contre 48,18 ; CIFAR-10 VGG16 49,94 contre 45,36 ; CIFAR-100 73,68 contre 71,99 ; CamVid SegNet 50,51 contre 48,53. Gain net sur petits modèles, faible sur gros jeux (CIFAR-100 : +1,7 points).
- Trust Score se dégrade sur CIFAR-10/100 et CamVid (Table 1, §3.2) ; sur CamVid il a été calculé sur un échantillon de pixels pour cause de coût (§3.2).
- Fine-tuning de l'encodeur : environ +1 à +2 points (Table 2 : MNIST 43,94 vers 45,89 ; CIFAR-100 72,68 vers 73,68).
- Entraîner sur un jeu de validation (10 %) dégrade les résultats, sauf CIFAR-100 (+0,17) (Table 3, §3.3). Perte BCE inférieure à la perte L2 sur CIFAR-10 (47,95 contre 49,94) et CamVid (48,96 contre 50,51) (Table 4, corps de tableau reconstruit, valeurs aussi données dans le texte).
- Courbes risque-couverture : gain surtout à forte couverture (0,8-0,95 CIFAR-10) (Fig. 3, §3.2).
- Incohérences internes : MNIST SmallConvNet sans fine-tuning 43,94 (Table 2) est repris comme « train set » en Table 3, alors que Table 1 donne 45,89 ; MNIST MLP 57,34 (Table 3) contre 57,37 (Table 1) ; CamVid 50,28 (Table 3) contre 50,51 (Table 1). Table 1 fait foi pour les lignes ci-dessous.
→ reportés dans `benchmarks.csv` (proposition, 6 lignes, ConfidNet de la Table 1, `confidence: high`, chunk `1910.04851#017.0`, plateforme/quantification `n/r`) : MNIST MLP 57,37 ; MNIST SmallConvNet 45,89 ; SVHN 50,72 ; CIFAR-10 VGG-16 49,94 ; CIFAR-100 VGG-16 73,68 ; CamVid SegNet 50,51 (AUPR-Error, %, test in-domain ; MCP, MCDropout, TrustScore en `baseline`). Pas de ligne pour les variantes des Tables 2-4 (ablations).

## Limites et critique

- Aucune évaluation matérielle ni sur plantes : coût mémoire/calcul de ConfidNet (5 couches denses + encodeur dupliqué après fine-tuning, donc un second encodeur à embarquer) non chiffré. Déduit, non affirmé.
- Jeux petits et réseaux simples (MNIST, SVHN, CIFAR, VGG-16, SegNet) ; pas de détection d'objets ni de plantes, pas de notion de coût asymétrique des erreurs ; l'erreur visée est symétrique (toute mauvaise classe).
- Confiance apprise sur le jeu d'entraînement, où les erreurs sont rares (sur-apprentissage) ; l'entraînement sur validation dégrade (§3.3). Un moniteur appris sur un modèle quantifié ou sous décalage de domaine n'est pas étudié.
- Pas de garantie formelle sur [1/K, 1/2] ; pas d'analyse de robustesse ni de calibration. Gains faibles sur CIFAR-100 ; pas de barres d'erreur visibles dans le texte extrait.
- Table 4 : corps de tableau mal extrait (« sans corps extrait » dans les warnings), valeurs recoupées avec le texte §3.3.
- Preprint 2019, non relu par les pairs.

## Pertinence pour le thème (base serre)

Axe `calibration-decision`. Donne un critère de confiance (TCP) et un moniteur appris (ConfidNet) qui classe mieux erreurs et réussites que MCP : utile pour décider quand un classifieur de maladies doit rejeter une capture ou passer la main à l'humain, avec des courbes risque-couverture pour fixer un seuil à risque donné (Fig. 3, §3.2). Le papier ne traite ni plantes ni écart de domaine (PlantVillage vers PlantDoc), ni la calibration (ECE) : il écarte même le temperature scaling comme inefficace sur le classement des confiances (§2.3). Coût d'un second encodeur sur RPi/Hailo non chiffré (déduit). Transposition à EfficientNet-B0 et aux tests hors domaine : non démontrée, à tester.

## Gaps identifiés

- Failure prediction (TCP/ConfidNet) sur images de plantes et sous décalage de domaine (labo vers terrain) : non traité.
- Comparaison à temperature scaling + seuil MCP en ECE et en fausses alertes « anormal » à rappel donné : non faite.
- Coût (mémoire, latence) du moniteur sur RPi 5 / Hailo-8L et après quantification INT8 : non mesuré.

## Statut de lecture

papier complet (fulltext.md lu en entier ; supplementary non disponible). Extraction grobid ok (pas de bandeau PyMuPDF/Docling) ; Table 4 sans corps extrait, valeurs recoupées avec le texte §3.3 (le texte de la Table 3 est aussi partiellement désordonné).
Ce qui suit est déduit et non affirmé par les auteurs : coût d'un second encodeur embarqué, transposition aux classifieurs de maladies de plantes, usage pour le rejet de captures et le choix de seuils.
