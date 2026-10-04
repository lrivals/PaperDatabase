---
id: arxiv-1804.02767-yolov3-incremental-improvement
fiche: done
date: 2026-10-04
benchmarks: none
---

# YOLOv3: An Incremental Improvement

Joseph Redmon, Ali Farhadi, 2018, arXiv preprint. https://arxiv.org/abs/1804.02767
Type : preprint non relu par les pairs (rapport technique, ton volontairement informel)

## Problème

Les auteurs ne posent pas de verrou : ils rassemblent « une série de petits changements » apportés à YOLO depuis YOLO9000, pour avoir une source citable (§1). L'objectif implicite est un détecteur one-stage plus précis que YOLOv2 tout en restant rapide.

## Méthode

- Boîtes : ancres par clustering k-means (9 clusters, 3 par échelle), prédiction tx, ty, tw, th comme dans YOLO9000, perte en somme des carrés (§2.1). Objectness par régression logistique ; un seul prior assigné par objet ; prédictions chevauchantes à plus de 0,5 sans être les meilleures ignorées (§2.1).
- Classes : classifieurs logistiques indépendants, entropie croisée binaire, pas de softmax (multi-étiquettes, §2.2).
- Trois échelles, à la manière des FPN : suréchantillonnage x2 et concaténation avec une carte de caractéristiques antérieure ; tenseur N x N x [3 x (4+1+80)] sur COCO (§2.3).
- Backbone Darknet-53 : 53 couches convolutives 3x3 et 1x1 avec connexions résiduelles (§2.4, Table 1). Entraînement sur images entières, multi-échelle, augmentation de données, batch norm, framework Darknet (§2.5).
- Pas de quantification, pas de mapping FPGA ; le NMS n'est pas décrit.
- Essais abandonnés (§4) : prédiction d'offsets x,y en multiples de la taille de l'ancre, activation linéaire pour x,y (perte de quelques points de mAP), focal loss (environ -2 points de mAP), double seuil d'IoU façon Faster R-CNN.

## Plateforme et implémentation

GPU uniquement : « M40 ou Titan X, basiquement le même GPU » (§2) ; temps de la Table 2 mesurés sur Titan X à 256 x 256. Pas de FPGA, pas de puissance (n/r), pas de ressources LUT/DSP/BRAM. Code publié : https://pjreddie.com/yolo/ (Abstract). Aucun bitstream.

## Résultats

- YOLOv3 320 x 320 : 22 ms, 28,2 mAP (Abstract) ; « aussi précis que SSD mais 3 fois plus rapide ».
- YOLOv3 608 x 608, Darknet-53 : AP 33,0 / AP50 57,9 / AP75 34,4 / APS 18,3 / APM 35,4 / APL 41,9 (Table 3) ; 51 ms sur Titan X (Abstract) ; RetinaNet 57,5 AP50 en 198 ms, soit 3,8 fois plus lent (Abstract).
- Table 3 : YOLOv2 21,6 AP / 44,0 AP50 ; SSD513 31,2 / 50,4 ; DSSD513 33,2 / 53,3 ; RetinaNet ResNet-101-FPN 39,1 / 59,1 ; RetinaNet ResNeXt-101-FPN 40,8 / 61,1. Fort sur AP50 et APS, mais l'AP chute quand le seuil d'IoU augmente, et APM/APL sont inférieures (§3).
- Backbones, ImageNet 256 x 256 (Table 2) : Darknet-19 74,1/91,8 top-1/top-5, 7,29 Bn ops, 171 FPS ; ResNet-101 77,1/93,7, 19,7, 53 FPS ; ResNet-152 77,6/93,8, 29,4, 37 FPS ; Darknet-53 77,2/93,8, 18,7 Bn ops, 1457 BFLOP/s, 78 FPS.
→ reportés dans `benchmarks.csv` : aucune ligne (voir ci-dessous).

Aucune ligne ajoutée : le travail est mesuré sur GPU Titan X seulement, hors plateforme embarquée, ce que `benchmarks.csv` exclut aujourd'hui (suggestion du profil reportée le 2026-10-01). Les lignes éventuelles sont laissées à l'agent principal.

## Limites et critique

- Les temps d'exécution des concurrents sont repris d'un autre papier (tableaux « volés » de RetinaNet [9], §3) et mélangent M40 et Titan X ; le papier n'indique ni batch, ni précision numérique, ni inclusion du NMS dans les temps.
- Le papier met en avant AP50 et conteste la métrique COCO ; sur AP (0,5:0,95) YOLOv3 reste derrière RetinaNet (33,0 contre 39,1 pour 608 x 608 contre ResNet-101-FPN, Table 3). Les graphes de la figure ont des origines non nulles (aveu des auteurs, Rebuttal).
- Table 3 : seule la ligne YOLOv3 608 est extraite ; les lignes 320 et 416 manquent dans le texte extrait (le 320 n'est connu que par l'Abstract). Le nombre de paramètres et les FLOPs du détecteur complet ne sont pas rapportés (seule la Table 2 donne les Bn ops du backbone).
- Aucun résultat sur matériel embarqué, quantification, ni sécurité.

## Pertinence pour la thèse

Référence de base de la famille YOLO (v3), sur laquelle reposent de nombreux accélérateurs FPGA : architecture (Darknet-53, 3 échelles, 9 ancres) à connaître pour juger les implémentations FPGA (YOLOv3-tiny, quantifications). Fournit la baseline GPU de précision/latence (Titan X). Ne traite ni FPGA, ni certification, ni détection de personnes spécifiquement. Laisse ouvert le coût matériel d'un Darknet-53 (18,7 Bn ops, Table 2).

## Gaps identifiés

- Baseline précision/latence GPU de YOLOv3 à confronter aux implémentations FPGA (pas de comparaison à puissance égale dans le papier).
- Sensibilité de YOLOv3 à l'alignement des boîtes (AP75 faible) : impact sur la détection de personnes en vidéosurveillance non étudié.

## Statut de lecture

papier complet (fulltext.md, 18 sections) ; extraction grobid ok.
Ce qui suit est déduit et non affirmé par les auteurs : la pertinence pour FPGA et la mention « batch/précision/NMS non précisés » (absence constatée dans le texte extrait). Table 3 et Table 1 sont partiellement extraites (lignes YOLOv3 320/416 absentes), à comparer au PDF avant de citer d'autres lignes.
