---
id: arxiv-2406.05412-select-mosaic-data-augmentation-method
fiche: done
date: 2026-10-18
---

# Select-Mosaic: Data Augmentation Method for Dense Small Object Scenes

Hao Zhang, Shuaijie Zhang, Renbin Zou, 2024, arXiv preprint. https://arxiv.org/abs/2406.05412 (pas de DOI)
Type : preprint non relu par les pairs

## Problème

Mosaic assemble quatre images tirées au hasard autour d'un point central aléatoire (§1, §2). Les auteurs estiment qu'il a « certain limitations » pour des tâches précises, dont les images aériennes à nombreux petits objets très denses (Résumé). Ils ne chiffrent pas la limite : pas de statistique de densité par mosaïque, pas d'analyse d'échec de Mosaic. L'argument est implicite : le tirage aléatoire ne favorise pas les mosaïques denses (§3, « increase the probability of scenes with dense small objects »).

## Méthode

Règle de sélection (§3, Fig. 1b, Fig. 2b), en plus de Mosaic :
1. calcul de la densité d'objets de chacune des 4 images tirées (« target density ») ;
2. calcul de l'aire des 4 régions (masks) définies par le point central ;
3. l'image la plus dense est placée dans la région la plus grande ; les 3 autres sont assemblées au hasard.

Paramètre S : probabilité d'appliquer la sélection ; sinon Mosaic standard (§3). Select-Mosaic s'emploie « en conjonction » avec Mosaic. Définition de la densité (objets/pixel ? objets/image ?) : n/r. Détecteur : YOLOv5 (variante, taille d'entrée, epochs, optimiseur : n/r) (§4). Jeux : AI-TOD (ablation) et VisDrone2019 (généralisation) (§4). Code : https://github.com/malagoutou/Select-Mosaic (Résumé).

## Plateforme et implémentation

Entraînement uniquement ; matériel d'entraînement n/r. Aucune mesure de vitesse ni de puissance (l'augmentation n'agit qu'à l'entraînement). Code publié (lien ci-dessus, non vérifié ici).

## Résultats

Ablation sur S, YOLOv5, AI-TOD (Table 1) :

| Config | P | R | AP50 | mAP |
|---|---|---|---|---|
| Mosaic | 66.65 | 40.30 | 42.70 | 18.06 |
| S=0.1 | 67.46 | 41.27 | 43.38 | 18.32 |
| S=0.2 | 69.55 | 40.14 | 43.39 | 18.35 |
| S=0.3 | 66.54 | 41.57 | 43.09 | 18.39 |
| S=0.4 | 67.08 | 41.78 | 44.21 | 18.73 |
| S=0.5 | 69.14 | 41.37 | 43.31 | 18.62 |
| S=0.6 | 68.33 | 41.14 | 43.70 | 18.66 |
| S=0.7 | 67.56 | 41.18 | 43.43 | 18.59 |

Meilleur AP50 : S=0.4, +1.51 point AP50 et +0.67 point mAP sur Mosaic (différences calculées sur la Table 1). Les valeurs S>0.7 ne sont pas testées.

VisDrone2019, YOLOv5 (Table 2) : Mosaic P 50.22 / R 42.93 / AP50 42.73 / mAP 24.86 ; Select-Mosaic P 52.15 / R 42.47 / AP50 43.11 / mAP 25.08 (S utilisé : n/r). Gain : +0.38 AP50, +0.22 mAP (calculé).

La Conclusion annonce +2.17 % AP50 sur AI-TOD et +0.37 % sur VisDrone. Le +2.17 ne correspond à aucune différence de la Table 1 (+1.51 au mieux) ; +0.37 est proche de +0.38 (arrondi probable). Non expliqué.

→ reportés dans `benchmarks.csv` : 10 lignes proposées (8 Table 1, 2 Table 2), AP50 uniquement, confidence high (corps de tableau lisible, recoupé avec la Conclusion pour VisDrone).

## Limites et critique

- Évaluation faible : un seul détecteur (YOLOv5, ancien), deux jeux, une graine, aucune variance ni intervalle de confiance. Le résumé parle d'« stability » sans aucune mesure de stabilité.
- Gains petits devant le bruit probable d'un entraînement unique : +0.38 AP50 / +0.22 mAP sur VisDrone ; sur AI-TOD la courbe en S est non monotone (S=0.3 : 43.09 ; S=0.4 : 44.21 ; S=0.5 : 43.31), donc le pic à 0.4 peut être du bruit (déduit). Toute valeur de S bat pourtant Mosaic en AP50 (+0.39 à +1.51), ce qui est un signal modeste mais cohérent.
- S choisi sur les mêmes mesures que celles rapportées : split (val ou test) n/r, risque de sélection sur le jeu d'évaluation.
- Baselines : seulement Mosaic standard. Pas de comparaison avec MixUp, CutMix, Copy-Paste, SAHI/tiling, ni avec une simple hausse de la probabilité de Mosaic ou une résolution plus haute, qui ciblent aussi les petits objets.
- Pas d'analyse par taille d'objet ni par densité (AP_small, AP_tiny), alors que c'est la revendication ; pas de contrôle de l'effet « image dense en grande région » vs « plus d'objets par mosaïque ».
- Pas de détail de protocole (hyperparamètres, résolution, epochs, définition de la densité) : reproductibilité limitée au code publié.
- Papier court (~2 pages de contenu), peu cité (déduit), non relu par les pairs. Incohérence +2.17 vs +1.51 ci-dessus.
- Pas d'évaluation sur les jeux à objets moins denses : le risque de dégrader les scènes éparses n'est pas mesuré (S sert à le contrôler, §3).

## Pertinence pour la thèse

Pour AUGMENTER un dataset de détection de petits objets aériens (AI-TOD, VisDrone), l'idée applicable est : biaiser Mosaic pour que la plus grande tuile reçoive l'image la plus dense, avec une probabilité S (0.1 à 0.7 testé, 0.4 le meilleur sur AI-TOD). À essayer en dernier recours léger (pas de coût d'annotation, calcul de densité à partir des labels existants), mais le gain est faible et non démontré statistiquement : à traiter comme une hypothèse à reproduire avec plusieurs graines sur son propre jeu, pas comme une recette. Ne concerne ni CONSTRUIRE, ni ANNOTER, ni PRÉTRAITER. Complète SAHI/tiling (autre levier sur les petits objets) sans être comparé à lui.

## Gaps identifiés

- Pas de comparaison Mosaic biaisé vs tiling/SAHI vs Copy-Paste sur petits objets denses.
- Aucun résultat multi-graines pour les variantes de Mosaic ; effet sur les détecteurs YOLO récents (v8+) non testé.
- Effet par taille d'objet (AP_tiny) non mesuré.

## Statut de lecture

Papier complet (fulltext.md lu en entier ; extraction grobid ok). Table 2 signalée « sans corps extrait » dans les warnings, mais le corps figure bien dans fulltext.md et a été lu ; cohérent avec la Conclusion pour l'AP50.
Ce qui suit est déduit et non affirmé par les auteurs : les différences absolues calculées, le caractère bruité du pic S=0.4, l'absence de citations, la raison implicite du problème de Mosaic (probabilité de scènes denses), le split d'évaluation inconnu.
