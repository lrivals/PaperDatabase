---
id: arxiv-2004.10934-yolov4-optimal-speed-accuracy-object
fiche: done
date: 2026-10-05
---

# YOLOv4: Optimal Speed and Accuracy of Object Detection

Alexey Bochkovskiy, Chien-Yao Wang, Hong-Yuan Mark Liao, 2020, arXiv preprint. https://arxiv.org/abs/2004.10934
Type : preprint non relu par les pairs

## Problème

Les auteurs veulent un détecteur temps réel entraînable sur un seul GPU grand public (1080 Ti / 2080 Ti), et un inventaire expérimental des astuces d'entraînement qui améliorent la précision sans coût d'inférence, le « bag of freebies » (BoF), dont l'augmentation de données est le cœur (§1, §2.2). Pour cette base : quelles recettes de données (augmentation, labels, assignation des ancres) valent leur coût, et de combien.

## Méthode

Architecture, en bref : CSPDarknet53 + SPP + PAN + tête YOLOv3 à ancres (§3.1, §3.4). Le reste relève de l'architecture (hors périmètre du profil). Ce qui compte ici est le BoF côté données et entraînement :

- **Augmentations connues** passées en revue (§2.2) : photométriques (luminosité, contraste, teinte, saturation, bruit) et géométriques (échelle, recadrage, flip, rotation) ; occultation simulée (random erase, CutOut, hide-and-seek, grid mask) ; mélange d'images (MixUp, CutMix) ; style transfer GAN.
- **Mosaic** (nouveau) : 4 images d'entraînement mélangées, donc 4 contextes ; permet de détecter des objets hors de leur contexte habituel, et la batch norm calcule ses statistiques sur 4 images par couche, ce qui réduit le besoin de grand mini-batch (Fig. 3, §3.3). CutMix n'en mélange que 2.
- **Self-Adversarial Training (SAT)** : en 2 passes avant/arrière, le réseau modifie d'abord l'image (pas les poids) pour se faire croire qu'il n'y a pas d'objet, puis s'entraîne normalement à détecter l'objet sur cette image altérée (§3.3).
- **Class label smoothing** (LS), appliqué à la sortie sigmoïde (§4.3, Fig. 7). Le lissage convertit les labels durs en doux (§2.2).
- **Élimination de la sensibilité de grille** (S) : `b_x = σ(t_x) + c_x` oblige à des `t_x` extrêmes pour atteindre le bord de cellule ; on multiplie le sigmoïde par un facteur supérieur à 1,0 (§4.3).
- **Plusieurs ancres par vérité terrain** (IT) : toute ancre dont l'IoU avec la vérité terrain dépasse un seuil est positive (§4.3). Seuil retenu par algorithme génétique : 0,213 (§4.1).
- **Ancres optimisées** (OA) pour l'entrée 512x512 (§4.3, légende Fig. 7) : la méthode d'optimisation n'est pas décrite.
- **Algorithme génétique** (GA) : recherche d'hyperparamètres sur les 10 % premiers du temps d'entraînement ; 300 époques sur YOLOv3-SPP avec perte GIoU, ensemble min-val 5k : lr 0,00261, momentum 0,949, seuil IoU d'affectation 0,213, normaliseur de perte 0,07 (§4.1, §4.3).
- Autres éléments du BoF, non liés aux données : CmBN, cosine annealing, taille de mini-batch dynamique avec formes d'entraînement aléatoires (DM), DropBlock, pertes IoU (GIoU, DIoU, CIoU).

## Plateforme et implémentation

GPU : entraînement sur un seul GPU (1080 Ti ou 2080 Ti) ; mesure de FPS sur GPU Maxwell, Pascal et Volta (Titan Volta ou Tesla V100), batch 1, sans TensorRT (Tables 8-10). Pas de puissance (`n/r`). Code publié : https://github.com/AlexeyAB/darknet (résumé).
Entraînement COCO : 500 500 pas, lr 0,01 divisé par 10 à 400 000 et 450 000, momentum 0,9, weight decay 0,0005, batch 64 (mini-batch 8 ou 4), entraînement multi-échelle (§4.1). ImageNet : 8 000 000 pas, +50 % de pas pour les expériences BoF (§4.1).

## Résultats

Bilan des ablations (c'est ce que le papier chiffre sur les données ; l extraction ne permet pas d attribuer chaque ligne).

**Classifieur (ImageNet val, top-1 / top-5)** — Tables 2 et 3, Fig. 7.
- CSPResNeXt-50 : 77,9 / 94,0 pour la ligne de départ, jusqu'à 79,8 / 95,2 pour la dernière ligne (Table 2). Les cases cochées (MixUp, CutMix, Mosaic, Bluring, Label Smoothing, Swish, Mish) ont été perdues à l'extraction : je ne peux pas dire quelle ligne correspond à quelle combinaison. Une ligne tombe à 64,5 / 86,0 (Table 2), sans attribution possible.
- CSPDarknet53 : 77,2 / 93,6 → 77,8 / 94,4 → 78,7 / 94,8 (Table 3) ; selon la légende de Fig. 7, ces lignes sont la base, le BoF-backbone et BoF + Mish (lecture de la légende, ordre des lignes déduit).
- Conclusion des auteurs (Fig. 7) : CutMix, Mosaic, class label smoothing et Mish améliorent le classifieur ; le « BoF-backbone » retenu = CutMix + Mosaic + class label smoothing, Mish en option. MixUp et le flou bilatéral ne sont pas retenus.

**Détecteur (COCO, CSPResNeXt50-PANet-SPP, 512x512)** — Table 4 : 17 lignes, dont les cases (S, M, IT, GA, LS, CBN, CA, DM, OA) sont perdues à l'extraction (« corps reconstruit », Table 3 déclarée sans corps).
- Avec perte MSE, les 9 premières lignes donnent AP 38,0 / 37,7 / 39,1 / 36,9 / 38,9 / 33,0 / 38,4 / 38,7 / 35,3, dont certaines sous la référence : une astuce de BoF peut nuire (Table 4).
- Pertes : GIoU 39,4, DIoU 39,1, CIoU 39,6 AP (Table 4).
- Ligne de plus haut AP avec MSE : 40,3 AP / 64,0 AP50 ; avec GIoU ou CIoU : 42,4 AP / 64,4 AP50 / 45,9 AP75 (Table 4). Cette combinaison finale sert de référence aux ablations BoS (Table 5).
- Le texte (§4.3) définit S, M, IT, GA, LS, CBN, CA, DM, OA mais ne donne pas le gain individuel de chacun : seule la table le fait, et sans les cases je ne peux pas les attribuer.
- Écart global : de 38,0 AP (première ligne) à 42,4 AP (Table 4) ; l'écart de 4,4 AP n'est pas une ablation propre (plusieurs astuces changent à la fois ; la première ligne n'est pas confirmée comme le baseline nu).

**Pré-entraînement du classifieur sur le détecteur** — Table 6 : BoF-backbone seul ne change presque rien (CSPResNeXt50 42,4 → 42,3 AP ; CSPDarknet53 42,4 AP) ; avec Mish, CSPDarknet53 monte à 43,0 AP / 64,9 / 46,5. Un meilleur classifieur ne donne donc pas toujours un meilleur détecteur (§4.4).

**Taille de mini-batch** — Table 7 : avec BoF/BoS, mini-batch 4 vs 8 : 41,6 vs 41,7 AP (CSPDarknet53-PANet-SPP, 512) ; sans BoF/BoS, 37,1 vs 38,4 AP (CSPResNeXt50, 608). Les auteurs en concluent que BoF/BoS suppriment le besoin de GPU coûteux (§4.5). Les deux paires utilisent des backbones et résolutions différents : lecture à nuancer.

**Modèle final** — COCO test-dev 2017, V100 : AP 41,2 / 43,0 / 43,5 à 416 / 512 / 608 pour 96 / 83 / 62 FPS ; AP50 62,8 / 64,9 / 65,7 ; AP_S 20,4 / 24,3 / 26,7 (Table 10). Le résumé annonce « ~65 FPS » et la Table 10 donne 62 FPS.
→ reportés dans `benchmarks.csv` (proposition) : 3 lignes (YOLOv4 416 / 512 / 608, Table 10, `confidence: medium` car corps de table reconstruit par GROBID).

Lecture pour les petits objets : AP_S monte de 20,4 (416) à 26,7 (608), soit +6,3 points pour une hausse de résolution d'entrée (Table 10) ; la résolution seule agit donc autant que bien des astuces de données (déduit de deux lignes).

## Limites et critique

- Les ablations Table 4 sont lisibles seulement en valeurs : les cases cochées de Tables 2-4 sont perdues, donc le gain individuel de Mosaic, SAT, LS, S, IT, OA n'est pas extractible ici ; il faut retourner au PDF (non ouvert, règle de la base) pour l'attribuer. SAT n'a aucun chiffre isolé dans le texte.
- Les ablations sont faites sur CSPResNeXt50-PANet-SPP à 512, pas sur le modèle final CSPDarknet53 ; transfert supposé.
- Interactions non mesurées : plusieurs astuces sont ajoutées en même temps, pas de plan factoriel complet ; Mosaic est cité comme réduisant le besoin de gros mini-batch mais l'effet n'est pas isolé (Table 7 change aussi le backbone).
- COCO uniquement (et ImageNet pour le classifieur) : pas de test sur petit dataset, domaine spécifique, ni sur la sensibilité à la taille du dataset. Le papier ne dit pas à partir de combien d'images Mosaic aide, ni son effet sur de gros objets (AP_L baisse de 56,0 à 53,3 de 416 à 608, Table 10, sans explication).
- Comparaisons de vitesse : GPUs différents selon les papiers cités, batch 1 sans TensorRT (Tables 8-10) ; chiffres de concurrents repris de leurs articles (résultats d'autrui, non reproduits).
- Les paramètres de Mosaic (taille de la grille, tirage du point de collage, traitement des boîtes coupées) ne sont pas décrits dans le texte : il faut lire le code Darknet.
- Preprint ; code publié (Darknet).

## Pertinence pour la thèse

Pour **AUGMENTER** : réfère historique de Mosaic (4 images, contexte différent, moins de dépendance au gros batch) et de SAT ; la recette BoF validée sur COCO : CutMix + Mosaic + class label smoothing côté classifieur, augmentations photométriques et géométriques classiques côté détecteur. À appliquer : entraînement de type YOLO sur un dataset de taille COCO ou plus ; sur un petit dataset ou des petits objets, Mosaic ajoute du contexte mais ce papier n'en mesure pas l'effet (hors COCO).
Pour **ANNOTER / CONSTRUIRE** : le label smoothing de classe suppose des labels où l'ambiguïté inter-classes est réelle ; le papier n'aborde ni qualité ni coût d'annotation.
Pour **PRÉTRAITER** : résolution d'entrée = levier fort pour petits objets (AP_S 20,4 → 26,7 de 416 à 608, Table 10) ; entraînement multi-échelle et mini-batch dynamique.
Pour **les ancres / l'assignation** : ancres optimisées (OA) pour 512x512, plusieurs ancres par vérité terrain avec seuil IoU 0,213 trouvé par GA, correction de la sensibilité de grille ; à reprendre quand on change de dataset (refaire le clustering des ancres sur ses propres boîtes : déduit, pas affirmé).
Reste ouvert : effet individuel de chaque astuce, petits datasets, domaines spécifiques, interaction avec le bruit de labels.

## Gaps identifiés

- Gain isolé de Mosaic / SAT / label smoothing / OA / IT sur détecteur : à récupérer dans le PDF (Table 4) ou par ablation propre (Ultralytics).
- Effet de Mosaic selon la taille du dataset et selon la taille des objets (petits vs grands) : absent.
- Méthode de calcul des ancres optimisées et réglage sur un dataset de domaine : absent.

## Statut de lecture

papier complet (`fulltext.md` lu en entier ; `paper.pdf` non ouvert). Extraction GROBID : les cases à cocher de Tables 2, 3 et 4 sont perdues (lignes de chiffres sans colonnes de features) ; Table 3 est signalée « sans corps extrait » dans les warnings alors qu'un corps partiel existe dans le texte. Les chiffres de ces tableaux sont donnés sans attribution à une configuration.
Ce qui suit est déduit et non affirmé par les auteurs : l'ordre des lignes de Table 3 (base / BoF / BoF + Mish) ; l'idée que la première ligne de Table 4 est le baseline ; la plateforme V100 exacte pour la Table 10 (« Titan Volta ou Tesla V100 ») ; la remarque sur AP_S vs résolution ; l'usage des ancres sur un nouveau dataset.
