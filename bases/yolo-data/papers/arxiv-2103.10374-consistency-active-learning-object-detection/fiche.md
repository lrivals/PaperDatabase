---
id: arxiv-2103.10374-consistency-active-learning-object-detection
fiche: done
date: 2026-10-18
---

# Consistency-based Active Learning for Object Detection

Weiping Yu, Sijie Zhu, Taojiannan Yang, Chen Chen, 2021, arXiv preprint. https://arxiv.org/abs/2103.10374 (DOI : n/r)
Type : preprint non relu par les pairs

## Problème

Les méthodes d'active learning (AL) sont surtout conçues pour la classification ; transférées à la détection, le gain sur la sélection aléatoire s'effondre (Table 1 : LL4AL +6,5 % / +10,1 % en classification contre +2,6 % / +2,7 % en détection aux cycles 1 / 2 ; VAAL +6,2 % / +6,0 % contre +2,3 % / +0,0 %). Les auteurs attribuent cet écart à trois inconsistances (§3.2) : (1) un détecteur fait régression de boîte et classification, qu'une perte unique ne résume pas ; (2) l'information est locale (un petit objet informatif est noyé dans une image « globalement facile ») ; (3) une image contient plusieurs objets, ce qui déséquilibre plus facilement la distribution de classes du pool annoté.

## Méthode

CALD (Consistency-based Active Learning for Detection), AL par pool avec C cycles, chacun consommant 1/C du budget (§3.1). Deux étapes (Fig. 2).

**Étape 1, information individuelle (§3.3.1).** Chaque image non annotée subit des augmentations A (ablation : F = flip horizontal, C = cutout, D = downsize, R = rotation, G = bruit gaussien, S = sel et poivre ; CALD retient « FCDR », §4.2). Les prédictions du détecteur sur l'image originale sont transportées sur l'image augmentée (par ex. flip de la boîte, score de classe inchangé) : ce sont les « prédictions de référence » (b_k, s_k). Chacune est appariée à la prédiction directe de l'image augmentée de plus fort IoU (Éq. 3). Cohérence : m_k = C_b + C_s (Éq. 4-5), avec C_b = IoU des deux boîtes et C_s = moyenne des confidences max des deux scores, multipliée par (1 − JS entre les distributions de classes) ; m_k est dans [0, 2]. Le critère n'est pas « m_k le plus petit » (appariement mauvais et faible confiance = instabilité sans intérêt, Fig. 3b) mais la distance à un point de base β : M(x) = E_A[min_k |m_k − β|] (Éq. 6). Le minimum sur les prédictions (et non la moyenne) cible la région locale la plus informative. β = 1,3, trouvé par recherche en grille (5 pas), utilisé pour tous les jeux et détecteurs (§3.3.1, §4.2). Boîtes et classes sont donc unifiées en une seule valeur. On garde un pool initial X_I légèrement supérieur au budget.

**Étape 2, information mutuelle, équilibrage des classes (§3.3.2).** La distribution de classes du pool annoté (Softmax des comptes de vérité terrain, Éq. 7) est comparée à celle de chaque image de X_I (Softmax des confidences max par classe, sur prédictions de référence et de l'image augmentée, Éq. 8) par divergence JS. L'algorithme 1 choisit gloutonnement les images de plus grande distance, c'est-à-dire de distribution la plus différente du pool annoté, jusqu'au budget du cycle. Effet constaté (Fig. 4, lecture visuelle) : la part des classes majoritaires (person) baisse, celle des minoritaires (bus, bike) monte.

## Plateforme et implémentation

Pas de matériel embarqué. Détecteurs : Faster R-CNN (FRCNN, deux étages) et RetinaNet (un étage), ResNet50 + FPN, implémentation Torchvision par défaut, 20 époques par cycle, moyenne de 3 essais (§4). GPU, durée et coût de la sélection : n/r. Code publié : non mentionné dans le texte lu (n/r).

## Résultats

**Protocole (§4).** VOC 2007 (trainval pour l'entraînement, test pour l'évaluation) et VOC 2012 (train / val) : 500 images initiales tirées au hasard, 500 par cycle ; pour RetinaNet 1000 images initiales (500 jugées trop peu pour un modèle robuste). COCO : 5000 images initiales, 1000 par cycle (suivant LS+C/LT/C). Métrique : mAP à IoU 0,5 sur VOC, mAP moyenne IoU 0,5:0,95 sur COCO. Nombre total de cycles : n/r dans le texte (les courbes de la Fig. 5 ne sont pas lisibles). Concurrents : Random, SSM, LS+C, LT/C (propres à la détection ; LT/C réservé aux détecteurs à deux étages), LL4AL et VAAL (indépendants de la tâche).

**Gains vs aléatoire et vs autres méthodes (§4.1).** CALD domine toutes les méthodes sur les trois jeux et les deux détecteurs (Fig. 5).
- FRCNN, 1er cycle : +8,4 % (VOC 2012) et +7,0 % (VOC 2007) en mAP sur Random ; +5,7 % et +3,8 % sur la seconde meilleure, LT/C. Les gains sur la seconde meilleure décroissent aux cycles suivants (« 3,1 à 1,2 » et « 2,3 à 1,4 » : lecture du texte, jeu associé non précisé). Raison avancée : le pool non annoté se vide et toutes les méthodes sélectionnent les mêmes images. Table 1 donne +8,4 % (cycle 1) et +5,8 % (cycle 2) sur Random pour CALD (VOC 2012 implicite, non dit).
- LL4AL et VAAL sont à 5,4 % et 5,7 % sous CALD au cycle 1 de VOC 2012 avec FRCNN ; LT/C est à 2,5 % sous CALD en moyenne sur VOC 2012.
- RetinaNet : +11,8 % sur Random en moyenne sur VOC 2012 ; LL4AL est à 2,5 % sous CALD en moyenne.
- COCO : les chiffres de la Fig. 5 (par ex. 17,3, 18,2 pour RetinaNet) sont des fragments illisibles ; aucun gain COCO chiffré de façon fiable (n/r). Le résumé est tronqué (« by 2.9/2.8/0. ») : n/r.
- Les classes difficiles (AP < 40 % en sélection aléatoire) gagnent plus que les autres (Fig. 6, lecture visuelle).

**Ablations (§4.2, VOC 2012, FRCNN).** Moyenne au lieu du minimum, β = 0 ou suppression du facteur de confiance : performances en baisse (moyenne : forte baisse ; facteur de confiance : légère). Optimum de β autour de 1,3 ; β = 2,0 sélectionne les images les moins informatives (pire que le hasard). Le choix des augmentations influe peu (Fig. 7b). Taux d'expansion de X_I (Table 2) : 0 % (étape 1 seule) 56,9 / 62,8 ; 10 % 57,4 / 63,3 ; 20 % 57,8 / 63,7 ; 30 % 57,3 / 63,5 ; 40 % 57,1 / 63,7 (mAP aux cycles 1 / 2). L'étape 2 apporte donc +0,9 mAP aux deux cycles à 20 %.

→ reportés dans `benchmarks.csv` : 4 lignes proposées (Table 2, VOC 2012, FRCNN, cycles 1 et 2, expansion 0 % et 20 %), confidence `medium` (corps de Table 2 signalé comme non extrait par l'extracteur, recoupé par le texte pour 0 % et 20 %). Les courbes de la Fig. 5 ne donnent aucune ligne fiable.

## Limites et critique

- Preprint, pas de relecture. Évaluation sur VOC et COCO uniquement (jeux équilibrés, images à peu d'objets), avec des détecteurs à ancres de type Torchvision ; aucun YOLO. Que les gains tiennent pour un détecteur de la famille YOLO est une hypothèse (déduit).
- Les gains sont donnés en pourcentage sans que le texte dise toujours s'il s'agit de points de mAP ou de gain relatif (Table 1 : « improvement compared with random selection », en %). Les valeurs absolues de mAP par cycle sont dans des courbes que l'extraction ne restitue pas.
- Gains modestes en absolu après le premier cycle, qui s'amenuisent (§4.1) ; sur COCO les écarts apparents sont de l'ordre de 0,1 à 0,6 mAP (fragments de Fig. 5, à vérifier sur le PDF).
- β = 1,3 est optimisé sur VOC 2012 avec FRCNN (§4.2) puis déclaré valable partout : non testé sur un détecteur ou un domaine éloigné. Le coût de calcul (plusieurs passes d'inférence par image non annotée, avec 4 augmentations) n'est pas mesuré.
- Le critère suppose un détecteur déjà correct (initialisation 500 à 1000 images, 5000 sur COCO) : démarrage à froid avec peu d'images non traité. L'annotation est supposée sans bruit (oracle parfait).
- L'équilibrage (étape 2) s'appuie sur les prédictions du modèle courant pour estimer les classes des images non annotées : les classes que le modèle ne détecte pas encore ne sont pas rééquilibrées (déduit).
- Pas de comparaison à un coût d'annotation en temps ni à des méthodes à pseudo-labels (hors périmètre du papier).

## Pertinence pour la thèse

Pour CONSTRUIRE un dataset de détection avec un budget d'annotation limité : CALD indique quelles images annoter en premier. Recette applicable à un détecteur quelconque, sans accès aux propositions de région : (1) un détecteur entraîné sur un petit lot aléatoire (500 à 1000 images ici) ; (2) inférence sur l'image originale et sur 4 augmentations (flip, cutout, downsize, rotation) ; (3) score = distance minimale de la cohérence boîte + classe à β = 1,3 ; (4) surdimensionner le lot de 20 % puis resélectionner par divergence de distribution de classes vers les classes sous-représentées. À appliquer quand le pool non annoté est grand, l'annotation coûteuse, et que la distribution de classes est déséquilibrée (l'étape 2 y apporte +0,9 mAP, Table 2). Pour ANNOTER : réduit le nombre de boîtes à dessiner, au prix de calcul d'inférence. Pour AUGMENTER : les augmentations servent ici de sonde d'instabilité du modèle, pas de données d'entraînement ; elles ne recoupent pas Mosaic ou Copy-Paste. Pour PRÉTRAITER : n/a. Reste ouvert : validation sur YOLO, petits objets, domaines spécialisés (drone, embarqué), démarrage à froid.

## Gaps identifiés

- Active learning pour détecteurs de la famille YOLO (Ultralytics) : aucune évaluation ici.
- Mesure du gain en coût d'annotation réel (temps, nombre de boîtes) plutôt qu'en nombre d'images.
- Sélection par AL pour petits objets / images tuilées, et interaction avec l'augmentation d'entraînement.
- Effet d'un oracle bruyant (bruit de labels) sur la sélection.

## Statut de lecture

Papier complet (fulltext.md lu en entier, extraction grobid ok). Réserves : le résumé est tronqué à « 2.9/2.8/0. » ; la Figure 5 (courbes et valeurs par cycle, y compris COCO) et la Figure 6 sont illisibles ou à peine lisibles en texte ; Table 2 signalée « sans corps extrait » par les avertissements, mais son corps figure dans fulltext.md et ses valeurs 0 % / 20 % sont recoupées avec le texte (§4.2).
Ce qui suit est déduit et non affirmé par les auteurs : transposabilité à YOLO ; limite de l'étape 2 pour les classes non encore détectées ; absence de code (non mentionné) ; 1er cycle = 1000 images annotées sur VOC.
