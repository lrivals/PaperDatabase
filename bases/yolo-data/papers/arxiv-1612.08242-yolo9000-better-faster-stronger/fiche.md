---
id: arxiv-1612.08242-yolo9000-better-faster-stronger
fiche: todo
date: 2026-10-04
benchmarks: none
---

> **Importée de la base `fpga` le 2026-10-05.** Cette fiche a été écrite pour une autre base (autre thème) : pertinence à réévaluer ici, puis `fiche: done` via `/paper-fiche`. Statut d'origine : done.

# YOLO9000: Better, Faster, Stronger

Joseph Redmon, Ali Farhadi, 2017, CVPR 2017 (arXiv 1612.08242, déposé en 2016). https://arxiv.org/abs/1612.08242
Type : conférence relue par les pairs (CVPR 2017, venue réelle corrigée dans `metadata.json` ; la version lue est la version arXiv).

## Problème

Détecteur généraliste à la fois rapide, précis et étendu à beaucoup de classes. YOLO souffre
de nombreuses erreurs de localisation et d'un rappel faible face aux méthodes à propositions
de régions (§2). Les jeux de détection restent bien plus petits que les jeux de classification
(§1).

## Méthode

YOLOv2 : empilement d'améliorations sur YOLO (§2, Table 2) : batch norm sur toutes les
couches (>2 % de mAP), classifieur fin-tuné à 448×448 (~+4 %), suppression des couches
entièrement connectées au profit d'ancres, entrée 416×416 (carte 13×13), 5 ancres issues d'un
k-means avec distance 1-IOU (k=5), prédiction de position contrainte par sigmoïde (~+5 %),
couche passthrough 26×26×512 vers 13×13×2048 (~+1 %), entraînement multi-échelle toutes les
10 batches parmi {320…608}. Backbone Darknet-19 : 19 couches conv., 5 max-pooling, 5,58 Gflops
contre 30,69 (VGG-16) et 8,52 (réseau YOLO) (§3). YOLO9000 : entraînement conjoint COCO + top
9000 classes d'ImageNet via WordTree (arbre WordNet, 9418 classes), 3 ancres au lieu de 5 (§4).
Pas de toolflow FPGA, pas de quantification : poids flottants, framework Darknet.

## Plateforme et implémentation

GPU GeForce GTX Titan X (modèle original, pas Pascal) pour tous les temps (légende Table 3).
Pas de FPGA, pas de puissance (`n/r`). Code et modèles pré-entraînés publiés : http://pjreddie.com/yolo9000/ (§1).

## Résultats

- VOC 2007 : 76,8 mAP à 67 FPS ; 78,6 mAP à 40 FPS (Abstract, §2). À 288×288 : >90 FPS, mAP « presque aussi bon » que Fast R-CNN (§2). Chaque entrée est le même modèle évalué à une taille différente (légende Table 3).
- Trajectoire Table 2 (mAP VOC 2007) : 63,4 (YOLO) → … → 69,5 (convolutionnel) → 69,2 (ancres, rappel 81 % → 88 %, §2) → 74,4 → 75,4 → 76,8 → 78,6. Les colonnes intermédiaires de Table 2 sont mal reconstruites, à ne pas utiliser ligne à ligne.
- VOC 2012 : 73,4 mAP pour YOLOv2 544 (§2, Table 4 sans corps extrait ; 73,4 retrouvé dans une ligne « YOLOv2 544 » accolée à Table 2, chunk 1612.08242#016.1).
- COCO : 44,0 mAP à IOU 0,5 (§2, Table 5 non extraite) ; comparable à SSD et Faster R-CNN.
- Darknet-19 ImageNet : 72,9 / 91,2 % top-1/top-5 à 224 ; 76,5 / 93,3 % à 448 (§3).
- YOLO9000 : 19,7 mAP sur ImageNet détection (val), 16,0 mAP sur les 156 classes sans annotation de boîte (§4).
→ reportés dans `benchmarks.csv` : voir lignes proposées à l'agent principal (5 lignes, aucune écrite ici).

## Limites et critique

- Tous les FPS sont sur un GPU de bureau de 2015 ; aucune valeur de puissance, de latence, de mémoire, de quantification : non transposable tel quel à l'embarqué.
- Les corps de Table 1, 3, 4, 6 n'ont pas été extraits : les FPS des baselines (Faster R-CNN, SSD) et les FPS par résolution ne sont pas vérifiables ici. La résolution associée à 76,8 / 67 FPS et 78,6 / 40 FPS n'est pas explicite dans le texte (déduit : 416 et 544 ; Table 2 liste « hi-res detector » pour 78,6).
- Les comparaisons mélangent des jeux d'entraînement différents (07+12, 07++12) et des baselines de 2015-2016.
- Le mAP de COCO est donné à IOU 0,5 seulement dans le texte ; pas de mAP 0,5:0,95 dans le fulltext.
- Contrainte d'une seule bounding box par ancre, sans évaluation de robustesse ni de sûreté.

## Pertinence pour la thèse

Architecture de référence de la lignée YOLO : Darknet-19, ancres k-means, passthrough, sortie 13×13 ; base de nombreux portages FPGA (YOLOv2 tiny, quantifié). Fournit un baseline GPU Titan X (précision/FPS) pour comparer les accélérateurs FPGA, à signaler comme baseline déduit. Rien sur la certification, la sûreté, ni la détection de personnes en particulier (classe `person` de VOC).

## Gaps identifiés

- Aucune étude de la sensibilité du multi-échelle à la quantification INT8 (non traité).
- Pas de baseline puissance/énergie : à compléter par des papiers de portage.

## Statut de lecture

Papier complet (lecture de `fulltext.md` par plages ; backend `grobid`, `ok`). Tables 1, 3, 4, 6 sans corps extrait ; Table 5 absente.
Ce qui suit est déduit et non affirmé par les auteurs : résolutions 416/544 associées aux deux points VOC 2007 ; utilité comme baseline pour la thèse.
