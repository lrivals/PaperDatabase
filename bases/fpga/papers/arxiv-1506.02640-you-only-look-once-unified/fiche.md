---
id: arxiv-1506.02640-you-only-look-once-unified
fiche: done
date: 2026-10-04
benchmarks: none
---

# You Only Look Once: Unified, Real-Time Object Detection

Joseph Redmon, Santosh Divvala, Ross Girshick, Ali Farhadi, 2016 (arXiv 2015), CVPR 2016. DOI 10.1109/CVPR.2016.91, https://arxiv.org/abs/1506.02640
Type : conférence (CVPR 2016, relue par les pairs) ; la version lue ici est le preprint arXiv.

## Problème

Les détecteurs d'objets de l'époque réutilisent des classifieurs (DPM, R-CNN : propositions de régions, extraction de caractéristiques, SVM, régression de boîtes, NMS) : pipelines complexes, lents et difficiles à optimiser, car chaque composant est entraîné séparément (§1). Les auteurs veulent un détecteur unique, entraîné de bout en bout et temps réel.

## Méthode

- Détection posée comme une régression : l'image est découpée en grille S × S ; chaque cellule prédit B boîtes (x, y, w, h, confiance) et C probabilités de classe conditionnelles (§2). Sur PASCAL VOC : S = 7, B = 2, C = 20, soit un tenseur 7 × 7 × 30, 98 boîtes par image (§2, §2.3).
- Réseau : 24 couches convolutives puis 2 couches entièrement connectées, inspiré de GoogLeNet, avec des réductions 1 × 1 suivies de 3 × 3 (§2.1, Fig. 3). Fast YOLO : 9 couches convolutives au lieu de 24, filtres moins nombreux (§2.1).
- Entraînement : pré-entraînement des 20 premières couches sur ImageNet (environ une semaine, top-5 88 % sur la validation 2012), puis ajout de 4 couches convolutives et 2 couches FC, entrée portée de 224 × 224 à 448 × 448 (§2.2). Framework Darknet (§2.2). Perte somme des erreurs quadratiques à plusieurs termes, pondérée (§2.2).
- Post-traitement : NMS, qui ajoute 2-3 % de mAP (§2.3).
- Pas de quantification ni de mapping FPGA : le papier ne traite pas l'embarqué.

## Plateforme et implémentation

GPU Titan X, sans traitement par lots (§1 ; la même phrase donne les 45 fps de YOLO et « plus de 150 fps » de Fast YOLO). Plateforme des autres mesures du Tableau 1 : n/r. Puissance, fréquence, ressources, mémoire : n/r. Précision numérique (FP32 ou autre) : n/r. Code : démo et code source annoncés sur le site du projet http://pjreddie.com/yolo/ (§5) ; pas de bitstream (sans objet).

## Résultats

PASCAL VOC 2007 (Table 1) :

| Modèle | Entraînement | mAP (%) | FPS |
|---|---|---|---|
| Fast YOLO | 2007+2012 | 52,7 | 155 |
| YOLO | 2007+2012 | 63,4 | 45 |
| YOLO VGG-16 | 2007+2012 | 66,4 | 21 |
| 100 Hz DPM (Sadeghi) | 2007 | 16,0 | 100 |
| 30 Hz DPM (Sadeghi) | 2007 | 26,1 | 30 |
| Fast R-CNN | 2007+2012 | 70,0 | 0,5 |
| Faster R-CNN VGG-16 | 2007+2012 | 73,2 | 7 |
| Faster R-CNN ZF | 2007+2012 | 62,1 | 18 |

- Analyse d'erreurs VOC 2007 (§4.2, Fig. 4) : les erreurs de localisation dominent chez YOLO ; Fast R-CNN produit 13,6 % de faux positifs sur le fond, presque 3 fois plus que YOLO. Le corps du Tableau 2 est mal extrait ; chiffres du tableau d'erreurs recoupés avec le texte seulement pour 13,6 %.
- Combinaison Fast R-CNN + YOLO : Fast R-CNN seul 71,8 % mAP sur VOC 2007, 75,0 % combiné (+3,2) (légende Table 2) ; sur VOC 2012, YOLO seul 57,9 % mAP (§4.4), combinaison +2,3 % (§4.4, Table 3).
- Généralisation aux œuvres d'art (Fig. 5, Picasso et People-Art) : YOLO AP personne 59,2 sur VOC 2007, 53,3 AP Picasso, best F1 0,590 ; People-Art 45 ; R-CNN 54,2 / 10,4 / 0,226 / 26 ; DPM 43,2 / 37,8 / 0,458 / 32 (le tableau de la figure est reconstruit : alignement des colonnes à vérifier).
- Démo webcam en temps réel, sans chiffre (§5).

→ reportés dans `benchmarks.csv` : 3 lignes proposées (Fast YOLO, YOLO, YOLO VGG-16, VOC 2007, Table 1), à ajouter par l'agent principal.

## Limites et critique

- Contraintes spatiales fortes : une classe et deux boîtes par cellule, difficultés sur les petits objets en groupe et sur les ratios inhabituels ; caractéristiques grossières ; perte identique pour petites et grandes boîtes, d'où des erreurs de localisation (§2.4).
- Précision inférieure aux meilleurs détecteurs : 63,4 % contre 73,2 % pour Faster R-CNN VGG-16 (Table 1), 57,9 % sur VOC 2012 (§4.4). Moins bon sur bouteille, mouton, téléviseur (§4.4).
- Comparaison des vitesses : matériel de mesure précisé seulement pour YOLO / Fast YOLO (Titan X) ; pour les autres détecteurs, n/r dans le texte lu. Les FPS ne sont donc pas strictement comparables. Les DPM temps réel de Sadeghi sont mesurés par ces auteurs ou repris : n/r.
- Aucune mesure d'énergie, de mémoire ni de latence ; aucun résultat sur matériel embarqué. Baseline Jetson / FPGA : aucune (déduit : la Titan X est un GPU de bureau, sans rapport avec un budget embarqué).
- Évaluation sur 20 classes VOC seulement ; pas de sécurité ni de robustesse étudiées.

## Pertinence pour la thèse

Papier fondateur de la famille YOLO, point de départ de l'axe yolo-fpga : il fixe l'architecture en détecteur monolithique à une passe, plus simple à déployer sur FPGA qu'un pipeline à propositions de régions (déduit). Il ne dit rien de la quantification, du mapping matériel ni de la certification : tout cela reste à instruire dans les travaux ultérieurs (YOLOv2, v3, déploiements FPGA). Utile comme référence de précision et de FPS pour la vidéosurveillance de personnes, avec la réserve que la classe « person » n'est évaluée qu'en généralisation sur l'art (Fig. 5).

## Gaps identifiés

- Aucune mesure de puissance ni sur plateforme embarquée dans l'article d'origine ; à compléter par les papiers de déploiement.
- Faiblesse sur les petits objets et en localisation : critique pour la détection de personnes à distance en vidéosurveillance.
- Aucun élément de sûreté ou de certification (distribution des erreurs fond / localisation non traitée du point de vue du risque).

## Statut de lecture

Papier complet (corps lu par sections via `fulltext.md` ; extraction GROBID correcte). Les corps des Tableaux 2 et 3 manquent ou sont dégradés (« sans corps extrait » dans `extraction.warnings`) : leurs chiffres ne sont repris que lorsque le texte ou la légende les redonne. Le tableau de la Fig. 5 est reconstruit, à vérifier.
Ce qui suit est déduit et non affirmé par les auteurs : l'intérêt d'un détecteur monolithique pour un déploiement FPGA ; l'écart avec un contexte embarqué (Titan X) ; la pertinence pour la vidéosurveillance.
