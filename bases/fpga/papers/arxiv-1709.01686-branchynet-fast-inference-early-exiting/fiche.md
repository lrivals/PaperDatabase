---
id: arxiv-1709.01686-branchynet-fast-inference-early-exiting
fiche: done
date: 2026-10-26
benchmarks: none
---

# BranchyNet: Fast Inference via Early Exiting from Deep Neural Networks

Surat Teerapittayanon, Bradley McDanel, H. T. Kung, 2017, arXiv preprint. https://arxiv.org/abs/1709.01686 (pas de DOI)
Type : preprint non relu par les pairs (travail fondateur des sorties anticipées ; la version ICPR 2016 n'est pas celle de la base)

## Problème

Les réseaux profonds coûtent en latence et en énergie à l'inférence, ce qui gêne les applications temps réel et à énergie limitée (Abstract, §I). Les auteurs partent de l'observation que les caractéristiques des couches précoces suffisent souvent à classer correctement une grande partie des échantillons (§I) ; les passer par toutes les couches est donc du calcul gaspillé.

## Méthode

- Architecture : réseau de base (« main branch ») augmenté de branches latérales, chacune terminée par un point de sortie (§III-A, Fig. 1). Branches à un seul niveau, sans imbrication (§III).
- Entraînement : optimisation conjointe d'une somme pondérée des pertes softmax de tous les points de sortie, Adam (§III-B). Poids plus forts sur les sorties précoces : +1 % de précision sur une version simplifiée de B-AlexNet (poids 1,0 / 0,3 contre poids égaux) (§V-A). Initialisation avec les poids du réseau de base : gain de « plusieurs pour cent » sur l'initialisation aléatoire (§IV, non chiffré).
- Inférence : à chaque sortie, entropie du softmax comparée à un seuil T_n ; si entropie < T_n, la prédiction sort, sinon l'échantillon continue ; la dernière sortie classe toujours (§III-C, Fig. 2).
- Seuils : choisis par balayage et recherche du « coude » de la courbe précision/temps (§IV, §V-B) ; pistes non réalisées : méta-reconnaissance (petit MLP par sortie prédisant si l'échantillon sera bien classé), OpenMax (§V-B).
- Position et structure des branches : placement empirique, pas d'algorithme automatique (§V-A) ; branches précoces plus profondes, tardives plus petites (§V-C).

## Plateforme et implémentation

CPU 3,0 GHz avec 20 Mo de L3 et GPU NVIDIA GeForce GTX TITAN X (Maxwell) 12 Go ; pas de FPGA ni de cible embarquée (§IV). Puissance et énergie : n/r (aucune mesure, malgré l'argument énergétique). Batch 1 (Fig. 3). Code : les auteurs indiquent avoir fourni le code, incluant le criblage de T (§V-B, réf. [24]) ; lien non relevé dans le texte extrait.

## Résultats

Classification sur MNIST (B-LeNet) et CIFAR10 (B-AlexNet, B-ResNet-110), temps moyen par échantillon, batch 1, au point « coude » (Table I) :

| Réseau | Précision base → Branchy | Temps CPU (ms) | Temps GPU (ms) | Accélération CPU / GPU | % sorti à chaque sortie |
|---|---|---|---|---|---|
| LeNet | 99,20 → 99,25 | 3,37 → 0,62 | 1,58 → 0,34 | 5,4x / 4,7x | 94,3 / 5,63 |
| AlexNet | 79,19 → 78,38 | 9,56 → 6,32 | 3,15 → 1,30 | 1,5x / 2,4x | 65,6 / 25,2 / 9,2 |
| ResNet-110 | 80,70 → 79,17 | 137,20 → 73,5 | 70,9 → 37,2 | 1,9x / 1,9x | 41,5 / 13,8 / 44,7 |

Seuils T retenus : 0,025 (B-LeNet), 0,0001 et 0,05 (B-AlexNet), 0,3 et 0,2 (B-ResNet) (Table I). Les auteurs concluent à 2x-6x d'accélération sur CPU et GPU (§VI). Sur CIFAR10 la précision baisse de 0,8 à 1,5 point au coude choisi ; ils précisent qu'un autre seuil donnerait une précision supérieure à ResNet pour un gain de temps bien moindre (§IV). Le tableau a été extrait par parsing : colonnes mal alignées dans `fulltext.md`, valeurs recoupées avec le texte (§IV : 94 %, 65 %, 41 %, 5,4/4,7x, 1,5/2,4x, 1,9/1,9x). Effet du cache : les seuils agressifs réduisent le temps CPU et le taux de défauts de cache (Fig. 6, §V-D). Taille de lot : un lot plus grand réduit le bénéfice, car tous les échantillons du lot doivent sortir avant le suivant (Fig. 3).
→ `benchmarks.csv` : aucune ligne (`benchmarks: none`). Les mesures portent seulement sur CPU de bureau et GPU de bureau (Titan X), hors du périmètre « plateforme matérielle embarquée » de la base ; aucune puissance mesurée.

## Limites et critique

- Aucune plateforme embarquée, aucune mesure d'énergie ni de puissance, alors que l'énergie est le motif annoncé. Le gain en temps moyen est donc un gain moyen, non un pire cas.
- Datasets petits (MNIST, CIFAR10), réseaux de classification ; la détection et la segmentation sont citées comme extensions possibles, sans expérience (§III, §VI).
- Le seuil est choisi au coude sur les données d'évaluation (§IV, Fig. 3) : pas de jeu de validation séparé décrit, donc risque d'optimisme (déduit).
- Le critère d'exit est l'entropie du softmax, mesure de confiance non calibrée ; les auteurs l'admettent implicitement en proposant OpenMax et la méta-reconnaissance (§V-B). Aucune garantie sur la fiabilité de l'exit : pas de métrique d'erreur parmi les échantillons sortis tôt, ni de taux de faux accepts (déduit : non rapportés).
- Gain mesuré sur la moyenne avec batch 1 : le temps de l'échantillon le plus lent reste celui du réseau complet plus les branches traversées, ce qui est défavorable à une borne de temps d'exécution (déduit).
- Le temps CPU/GPU dépend de l'implémentation logicielle ; rien sur la variabilité (écart-type) ni sur le nombre d'exécutions.

## Pertinence pour la thèse

Travail fondateur nommé dans `profile.md` (exclusion levée pour BranchyNet) pour l'axe `failure-prediction`. Pour le sujet ARCYS (prédiction d'échec ciblée sur les faux négatifs d'un détecteur de personnes, moniteur sur FPGA) :
- Apporte le mécanisme de base : une sortie auxiliaire entraînée conjointement, avec un score de confiance (entropie) et un seuil par sortie. Le moniteur de faux négatifs peut se lire comme un point de sortie dont le signal est l'échec du détecteur plutôt que la classification (inférence).
- Le papier utilise l'exit comme raccourci de calcul (vitesse). Le sujet ARCYS le veut comme signalement conservateur : il faudrait inverser le rôle du seuil (privilégier le rappel des échecs, pas le gain de temps), ce que le papier ne traite pas.
- Calibration et seuil appris/balayé sans garantie : renvoie à l'axe `failure-prediction` (calibration, abstention) et au besoin d'un seuil justifiable en certification.
- Aucun lien direct avec la quantification, le FPGA, le WCET ; la variabilité du temps selon l'exit pose la question de la borne temporelle (axe `timing-analysis`, déduit).

## Gaps identifiés

- Sorties anticipées dont le signal cible le faux négatif d'un détecteur (et non l'erreur de classification), avec seuil conservateur : absent ici.
- Sorties anticipées mesurées sur FPGA avec latence et énergie : absentes ; aucune borne de pire cas.
- Choix et réglage des seuils avec garantie (jeu de calibration séparé, taux d'échec toléré) : seulement esquissés (§V-B).

## Statut de lecture

Papier complet (fulltext.md lu en entier ; extraction GROBID `ok`). Table I extraite avec colonnes mal alignées, valeurs recoupées avec le texte. Fig. 2 (algorithme) mal extraite, algorithme lu dans §III-C. Ce qui suit est déduit et non affirmé par les auteurs : lecture du moniteur de faux négatifs comme point de sortie ; absence de jeu de validation pour T ; contraste moyenne contre pire cas ; absence de lien code relevée dans le texte extrait.
