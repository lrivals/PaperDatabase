---
id: arxiv-1804.02767-yolov3-incremental-improvement
fiche: done
date: 2026-10-18
---

# YOLOv3: An Incremental Improvement

Joseph Redmon, Ali Farhadi, 2018, arXiv preprint. https://arxiv.org/abs/1804.02767
Type : preprint non relu par les pairs (rapport technique, ton volontairement informel)

## Problème

Les auteurs ne posent pas de verrou : ils rassemblent « une série de petits changements » apportés à YOLO depuis YOLO9000, pour avoir une source citable (§1). L'objectif implicite est un détecteur one-stage plus précis que YOLOv2 tout en restant rapide. Pour cette base, le papier vaut surtout par sa recette de données : ancres, assignation des labels, étiquetage multi-label (§2.1-2.3).

## Méthode

- Architecture : backbone Darknet-53 (53 couches convolutives 3x3 et 1x1 avec connexions résiduelles, §2.4) ; trois échelles de sortie à la manière des FPN, par suréchantillonnage x2 et concaténation avec une carte antérieure (§2.3) ; tenseur N x N x [3 x (4+1+80)] sur COCO (§2.3). Entraînement sur images entières, sans hard negative mining, multi-échelle, « lots d'augmentation de données », batch norm, framework Darknet (§2.5) ; les augmentations exactes ne sont pas détaillées (n/r).
- Ancres (§2.3) : k-means pour obtenir les priors de boîtes ; 9 clusters et 3 échelles « choisis arbitrairement », clusters répartis également entre échelles (3 par échelle). Sur COCO : (10x13), (16x30), (33x23), (30x61), (62x45), (59x119), (116x90), (156x198), (373x326). La distance utilisée par le k-means, la taille d'entrée de référence de ces valeurs et l'attribution exacte des ancres aux échelles ne sont pas dites (n/r) ; l'attribution des petites ancres à l'échelle la plus fine est une déduction.
- Prédiction de boîte (§2.1) : tx, ty, tw, th avec b = sigmoïde(t) + offset de cellule pour le centre et p·e^t pour la taille ; perte en somme des carrés.
- Assignation des labels (§2.1) : l'objectness vaut 1 pour l'ancre qui recouvre une vérité terrain plus que toute autre ancre ; une ancre non meilleure mais qui recouvre une vérité terrain au-delà de 0,5 est ignorée (pas de perte) ; « contrairement à [17], un seul prior est assigné par objet » ; une ancre non assignée ne subit aucune perte de coordonnées ni de classe, seulement d'objectness.
- Classes (§2.2) : classification multi-label par classifieurs logistiques indépendants et entropie croisée binaire, sans softmax, jugé inutile pour la performance. Justification des auteurs : sur Open Images, de nombreux labels se recouvrent (Woman et Person), et le softmax suppose exactement une classe par boîte, ce qui est souvent faux.
- Pas de quantification, pas de mapping FPGA ; le NMS n'est pas décrit.

## Résultats

- YOLOv3 320x320 : 22 ms, 28,2 mAP (Abstract) ; « aussi précis que SSD mais 3 fois plus rapide ». 57,9 AP50 en 51 ms sur Titan X contre 57,5 AP50 en 198 ms pour RetinaNet, soit 3,8 fois plus rapide (Abstract).
- Table 3 (COCO, YOLOv3 608x608, Darknet-53) : AP 33,0 / AP50 57,9 / AP75 34,4 / APS 18,3 / APM 35,4 / APL 41,9. Comparaisons (AP / AP50 / AP75 / APS / APM / APL) : YOLOv2 21,6 / 44,0 / 19,2 / 5,0 / 22,4 / 35,5 ; SSD513 31,2 / 50,4 / 33,3 / 10,2 / 34,5 / 49,8 ; DSSD513 33,2 / 53,3 / 35,2 / 13,0 / 35,4 / 51,1 ; RetinaNet ResNet-101-FPN 39,1 / 59,1 / 42,3 / 21,8 / 42,7 / 50,2.
- Écart AP50 - AP75 (calcul à partir de la Table 3, déduit) : YOLOv3 23,5 points (57,9 - 34,4) ; YOLOv2 24,8 ; SSD513 17,1 ; DSSD513 18,1 ; RetinaNet-101-FPN 16,8. Les auteurs disent que « la performance chute fortement quand le seuil d'IoU augmente », ce qui indique que YOLOv3 a du mal à aligner parfaitement les boîtes (§3).
- Objets par taille (§3) : YOLOv3 renverse la faiblesse historique de YOLO sur les petits objets (APS 18,3 contre 5,0 pour YOLOv2 ; Table 3) grâce aux prédictions multi-échelles, mais est moins bon sur objets moyens et grands (APL 41,9 contre 50,2 pour RetinaNet-101-FPN et 49,8 pour SSD513) ; « plus d'investigation nécessaire » (§3).
- Backbones, ImageNet 256x256 (Table 2) : Darknet-19 74,1/91,8 top-1/top-5, 7,29 Bn ops, 171 FPS ; ResNet-101 77,1/93,7, 19,7, 53 FPS ; ResNet-152 77,6/93,8, 29,4, 37 FPS ; Darknet-53 77,2/93,8, 18,7 Bn ops, 1457 BFLOP/s, 78 FPS.
- Ce qui n'a pas marché (§4) : (1) prédiction de l'offset x,y comme multiple de la largeur/hauteur de l'ancre avec activation linéaire : instabilité, mauvais résultats ; (2) activation linéaire au lieu de logistique pour x,y : perte de quelques points de mAP ; (3) focal loss : environ -2 points de mAP, hypothèse (non vérifiée, « on n'est pas totalement sûrs ») : l'objectness séparée et les probabilités de classe conditionnelles rendent déjà YOLOv3 robuste au déséquilibre ciblé ; (4) double seuil d'IoU façon Faster R-CNN (positif >= 0,7, ignoré entre 0,3 et 0,7, négatif < 0,3) : « pas de bons résultats ». Les auteurs précisent que ces pistes pourraient fonctionner avec plus de réglage (§4). Aucun chiffre détaillé, aucune ablation tabulée.

Lignes ajoutées à `benchmarks.csv` (proposées à l'agent principal, 8 lignes, GPU Titan X) : YOLOv3 320 (28,2 mAP, 22 ms, Abstract) ; YOLOv3 608 AP50 57,9 / 51 ms (Abstract, Table 3) ; YOLOv3 608 AP 33,0, AP75 34,4, APS 18,3, APM 35,4, APL 41,9 (Table 3) ; Darknet-53 ImageNet top-1 77,2 à 78 FPS (Table 2).

## Limites et critique

- Les temps d'exécution des concurrents sont repris d'un autre papier (tableaux « volés » de RetinaNet [9], §3) et mélangent M40 et Titan X (§2) ; le papier n'indique ni batch, ni précision numérique, ni inclusion du NMS dans les temps.
- Le papier met en avant AP50 et conteste la métrique COCO ; sur AP (0,5:0,95) YOLOv3 reste derrière RetinaNet (33,0 contre 39,1, Table 3). Les graphes ont des origines non nulles (aveu des auteurs, Rebuttal).
- Aucune ablation sur les choix de données : le choix de 9 clusters et 3 échelles est dit arbitraire (§2.3), l'effet de l'assignation à une seule ancre, du seuil 0,5, de la perte logistique contre softmax n'est pas mesuré. Le seul bénéfice du multi-label cité l'est pour Open Images, sur lequel aucun résultat n'est donné ici.
- Les échecs de §4 sont rapportés de mémoire (« ce dont on se souvient ») sans protocole, sans dataset ni taille d'entrée : ils sont des indices, pas des résultats.
- Table 3 : seule la ligne YOLOv3 608 est extraite ; les lignes 320 et 416 manquent dans le texte extrait (le 320 n'est connu que par l'Abstract). Le nombre de paramètres et les FLOPs du détecteur complet ne sont pas rapportés.
- Argument des auteurs sur la précision de localisation (Rebuttal) : VOC a fixé son seuil d'IoU à 0,5 « pour tenir compte des inexactitudes des boîtes de vérité terrain » ; ils demandent si COCO, dont les labels sont meilleurs (masques de segmentation), justifie un seuil plus strict, et relèvent qu'il est difficile pour des humains de distinguer un IoU de 0,3 d'un IoU de 0,5. Opinion, pas résultat.
- Aucun résultat sur matériel embarqué, quantification, ni sécurité.

## Pertinence pour cette base

Ce que le papier apprend pour CONSTRUIRE, ANNOTER, PRÉTRAITER et AUGMENTER un dataset de détection de type YOLO (lu, sauf mention « déduit ») :

- ANNOTER / qualité des labels : l'écart AP50 - AP75 (23,5 points pour YOLOv3) mesure la précision de localisation, pas la classification ; il croise la tolérance des boîtes de vérité terrain. Les auteurs rappellent que VOC fixait son seuil à 0,5 pour absorber les imprécisions d'annotation (Rebuttal). Déduit : si le détecteur est évalué ou exploité à IoU élevé, des boîtes serrées sont requises ; à AP50, des annotations plus tolérantes suffisent. À appliquer pour fixer la consigne de serrage des boîtes selon l'usage (comptage ou détection grossière contre localisation fine).
- CONSTRUIRE / étiquetage : une classification logistique indépendante (multi-label) convient à des taxonomies dont les classes se recouvrent (Woman et Person dans Open Images, §2.2) ; avec un softmax, chaque boîte n'a qu'une classe. À appliquer quand le jeu de classes est hiérarchique ou non exclusif, ou quand on fusionne des datasets aux taxonomies différentes. Pour un jeu à classes exclusives, aucun gain affirmé.
- PRÉTRAITER / ancres : les 9 ancres sont calculées par k-means sur les boîtes du dataset (§2.3) ; les valeurs COCO (de 10x13 à 373x326) donnent un ordre de grandeur de la plage de tailles à couvrir, réparties en 3 par échelle. Pour un nouveau dataset (objets très petits, ratios inhabituels), il faut recalculer les ancres sur ses propres boîtes (déduit du principe ; le papier ne le teste pas), et leur nombre est un choix non ablaté.
- CONSTRUIRE / assignation : une seule ancre par vérité terrain, ignorance au-dessus de 0,5 d'IoU pour les autres, aucune perte de coordonnée ou de classe sur les ancres non assignées (§2.1). Conséquence pour les labels (déduit) : une vérité terrain manquante ou une boîte dupliquée fait traiter un vrai objet comme fond, ou une cible instable.
- Petits objets : APS 18,3 contre 5,0 pour YOLOv2 grâce aux trois échelles (Table 3, §3). Pour un dataset de petits objets, une tête à haute résolution compte autant que le tiling (voir SAHI dans la base). L'APL plus faible (41,9) alerte sur le compromis.
- Déséquilibre : la focal loss a coûté environ 2 points de mAP (§4) ; elle n'est donc pas un correctif automatique du déséquilibre de classes avec la structure objectness + classes de YOLOv3 (un seul essai non détaillé).
- AUGMENTER : le papier ne détaille aucune augmentation (n/r, §2.5) ; il n'apporte rien sur Mosaic, MixUp ou Copy-Paste.

## Gaps identifiés

- Effet mesuré du nombre d'ancres, de leur recalcul par dataset et de l'assignation une-ancre-par-objet : jamais ablaté ici ; à chercher dans les papiers sur l'assignation (ATSS, SimOTA, TAL).
- Lien entre bruit des boîtes de vérité terrain et AP75 : non étudié (seule une remarque dans le Rebuttal).
- Recette d'augmentation d'YOLOv3 non documentée.

## Statut de lecture

papier complet (fulltext.md, 18 sections) ; extraction grobid ok. Déduit et non affirmé par les auteurs : tous les écarts AP50 - AP75 (calculs à partir de la Table 3), les conséquences pour la qualité d'annotation, l'attribution des petites ancres à l'échelle la plus fine, la pertinence pour cette base, et la mention « batch/précision/NMS non précisés » (absence constatée dans le texte extrait). Table 1 (Darknet-53) est illisible (n/r) ; Table 3 est extraite sans avertissement de reconstruction mais sans les lignes YOLOv3 320/416 ; à comparer au PDF avant de citer d'autres lignes. Les valeurs de mémoire n'ont pas été utilisées.
