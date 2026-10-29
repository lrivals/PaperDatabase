---
id: arxiv-1911.10317-plantdoc-dataset-visual-plant-disease
fiche: done
date: 2026-10-29
---

# PlantDoc: A Dataset for Visual Plant Disease Detection

Davinder Singh, Naman Jain, Pranjali Jain, Pratik Kayal, Sudhakar Kumawat, Nipun Batra, 2019, arXiv preprint (la version ACM CoDS-COMAD 2020 porte le DOI). https://doi.org/10.1145/3371158.3371196
Type : preprint non relu par les pairs

## Problème

Les jeux publics de maladies de plantes (PlantVillage, PVD) sont pris en laboratoire, fond uni ; les auteurs posent que leur efficacité « dans le monde réel » est probablement faible (1911.10317#004.0). Il n'existe pas de jeu public en conditions non contrôlées (fond, lumière, plusieurs feuilles par image).

## Méthode

- Collecte : ~20 900 images Google Images / Ecosia, requêtes sur les 38 classes de PlantVillage ; filtrage par 4 personnes d'après les consignes d'APSNet, chaque image contrôlée par deux personnes ; retrait des images non-feuille, de labo, hors périmètre et des doublons inter-classes ; classes de moins de 50 images supprimées. Résultat : 2 598 images, 13 espèces, 27 classes (17 maladies + 10 saines) (1911.10317#006.0, 1911.10317#001.2).
- Annotation : boîtes englobantes LabelImg sur toutes les feuilles, avec classe, boîte >= ~1/8 de l'image (1911.10317#006.2). Variante Cropped-PlantDoc (C-PD) : 9 216 feuilles recadrées (1911.10317#006.2).
- Protocole : classification sur images brutes (VGG16) et sur C-PD (VGG16, InceptionV3, InceptionResNetV2) ; SGD momentum 0,9, lr 0,001, images redimensionnées à 100x100, poids ImageNet Keras, augmentation usuelle ; GPU V100 (1911.10317#010.0). Détection : Faster R-CNN InceptionResNetV2 et MobileNet(-SSD), mAP@0,5 (1911.10317#012.0).
- Split : 80/20 (probablement aléatoire au niveau image ou feuille ; non précisé, voir Limites) ; test « PVD -> PlantDoc » = entraînement sur tout PVD, test sur 100 % de PlantDoc (Tables 1-2).

## Plateforme et implémentation

Entraînement sur NVIDIA V100, Keras/TensorFlow (1911.10317#010.0). Application mobile à base de MobileNet SSD sur CPU mobile « en temps réel » (§6, 1911.10317#014.0), sans latence ni FPS chiffrés (n/r). Puissance : n/r. Code et jeu de données : annoncés « à venir » sur GitHub (formulation au futur) ; lien non vérifié ici.

## Résultats

Classification, images brutes, VGG16, 27 classes (Table 1, 1911.10317#023.0) :
- ImageNet, entraîné PlantDoc 80 % / test PlantDoc 20 % : acc. 13,74 %, F1 0,12.
- ImageNet, entraîné PVD / test PlantDoc 100 % : acc. 15,08 %, F1 0,15.
- ImageNet+PVD (pré-entraînement), puis PlantDoc 80 % / test 20 % : acc. 29,73 %, F1 0,28.

Classification, feuilles recadrées C-PD (Table 2, 1911.10317#024.0), acc. / F1 :
- VGG16 : 44,52 / 0,44 (ImageNet, C-PD 80/20) ; 19,73 / 0,18 (PVD -> C-PD 100 %) ; 60,41 / 0,60 (ImageNet+PVD, C-PD 80/20).
- InceptionV3 : 46,67 / 0,46 ; 30,78 / 0,28 ; 62,06 / 0,61.
- InceptionResNetV2 : 49,04 / 0,49 ; 39,87 / 0,38 ; 70,53 / 0,70.
Les auteurs concluent que passer de « PVD seul » à « affiner sur PlantDoc » réduit l'erreur jusqu'à 31 points (1911.10317#001.1, résumé). Cet écart (39,87 -> 70,53, InceptionResNetV2) est calculé sur Table 2.

Détection de feuilles, mAP@0,5 (Table 3, 1911.10317#024.0) : MobileNet COCO 32,8 ; MobileNet COCO+PVD 22,4 ; Faster R-CNN InceptionResNetV2 iNaturalist 36,1 ; COCO 38,9. Les auteurs notent que PVD ne contribue pas (le pré-entraînement PVD fait perdre ~10 points à MobileNet) (1911.10317#013.0).
Remarque : le papier ne dit pas si la détection est mono-classe ; les boîtes portent la classe de maladie, donc la mAP est vraisemblablement multi-classes (déduit, non affirmé).

Table 3 reconstruite par PyMuPDF : à vérifier ; chiffres recoupés avec le texte (38,9 ; 22) et le doublon de tableau (1911.10317#025.0).
→ reportés dans `benchmarks.csv` : aucune ligne ajoutée par cet agent (l'agent principal colle les lignes renvoyées).

## Limites et critique

- Étiquetage : images web classées par 4 personnes sans expertise phytopathologique ; les auteurs reconnaissent des images potentiellement mal étiquetées (ex. tache bactérienne vs Septoria de la tomate) (1911.10317#015.0, Fig. 6). Le bruit d'étiquettes plafonne toute métrique sur PlantDoc, y compris celle de SerreIA.
- Petit jeu (2 598 images, classes à partir de 50 images) ; plusieurs feuilles de classes différentes par image ; basse résolution (§5, 1911.10317#013.0).
- Split : seul « 80/20 » est donné. Le papier ne dit pas si la découpe est faite avant le recadrage C-PD (risque de fuite entre feuilles d'une même photo) ni si elle est stratifiée. Déduit : les 70,53 % sont donc probablement optimistes.
- Les images brutes à 100x100 détruisent le détail ; modèles anciens (VGG16, InceptionV3) ; pas de seeds ni d'écarts-types.
- Le test « PVD -> PlantDoc » utilise les 27 classes de PlantDoc, sous-ensemble des 38 de PVD (déduit de la collecte par noms de classes PVD) ; pas de rappel/précision binaire sain/malade.
- Le papier n'étudie ni le remplacement de fond, ni l'adaptation de domaine, ni la calibration.
- Le résultat sur le pré-entraînement PVD est contradictoire entre tâches : +15 points en classification (Table 1 : 13,74 -> 29,73), -10 points en détection MobileNet (Table 3). Pas de test de significativité.

## Pour SerreIA

Ce que le projet reprend :
1. **Protocole de référence hors domaine** : le test PlantDoc de SerreIA (`vision/eval/cross_domain_eval.py`, `vision/datasets/prepare.py`) correspond à la ligne « PVD -> PlantDoc » (Tables 1-2). Reprendre ce protocole comme plancher de comparaison, mais passer de 27 classes à la tête binaire sain/malade.
2. **Expérience « effet du pré-entraînement » à refaire** : le papier trouve que PVD aide la classification (+15 points, VGG16, 1911.10317#023.0) mais dégrade la détection MobileNet (32,8 -> 22,4 mAP, 1911.10317#024.0). SerreIA entraîne YOLOv8n (`vision/train/train_yolo.py`) sur feuilles flattées par PV : tester YOLOv8n pré-entraîné COCO seul contre COCO+PV/PV+CCMT, et mesurer sur PlantDoc le taux de faux positifs sur images saines (42 % actuellement).
3. **Fine-tuning sur du terrain** : l'ajout d'images non-labo est le gain le plus grand du papier (39,87 -> 70,53, Table 2). Pour SerreIA : un split PlantDoc (train/val par photo, pas par feuille) pour affiner la tête et recalibrer (`vision/eval/temperature.py`) ; garder une partie hors apprentissage comme test final (`vision/labeling/build_yolo_dataset.py` pour les boîtes).
4. **Format d'annotation** : boîtes de feuilles + classe, PlantDoc ayant ce format ; réutilisable pour `vision/labeling/yolo_format.py` et `pseudo_labels.py`. La règle « boîte >= 1/8 de l'image » est une règle de filtrage candidate pour rejeter les crops inexploitables.
5. **Bruit d'étiquettes** : les confusions que les auteurs avouent (Fig. 6) sont une cause plausible du plafond à F1 classe 0,264 ; à vérifier sur un échantillon de faux positifs/négatifs de SerreIA (inférence, non démontrée par le papier).

**Comparabilité avec les chiffres de SerreIA : non.**
- Métrique : exactitude/F1 multi-classes à 27 classes, contre rappel 0,986 / précision 0,679 / spécificité 0,50 / F1 classe 0,264 (binaire sain/malade, tête multi-têtes) : pas la même tâche.
- Jeu d'entraînement : PVD seul (ImageNet) ; SerreIA entraîne PV+CCMT avec EfficientNet-B0 : source plus variée, architecture moderne.
- Test : PlantDoc dans les deux cas, hors domaine pour les modèles PVD ; mais les lignes « PlantDoc 80/20 » du papier sont in-domain (test issu du même jeu que l'apprentissage) et ne se comparent pas à SerreIA. Résolution 100x100 contre celle de SerreIA (non lue ici).
- Détection : mAP@0,5 du papier (38,9 ; 32,8) est sur PlantDoc entier avec le même jeu en train/test (split non précisé) ; le mAP@0,5 de SerreIA (0,956) est mesuré sur un test flatté par PV. Ni l'un ni l'autre n'est mesure de faux positifs sur images saines.
- Ni calibration ni ECE dans le papier ; aucune comparaison possible sur ce point.

## Gaps identifiés

- Pas de mesure PlantVillage -> PlantDoc avec backbone moderne (EfficientNet, YOLOv8) dans le corpus ; à croiser avec les papiers sur l'écart de domaine.
- Aucun test de remplacement de fond ni d'adaptation de domaine sur PlantDoc dans ce papier.
- Qualité des étiquettes PlantDoc non auditée (à chercher : travaux de re-étiquetage).

## Statut de lecture

papier complet (fulltext.md de 147 lignes, extraction grobid ; Table 3 reconstruite par PyMuPDF, chiffres recoupés avec le texte).
Déduit et non affirmé par les auteurs : fuite possible du split 80/20, multi-classes de la mAP, 27 classes sous-ensemble de PVD, plausibilité du bruit d'étiquettes comme cause du plafond de SerreIA, comparabilité avec SerreIA. Les fichiers `vision/…` ont été listés mais pas lus en détail ; le rôle de chacun est supposé d'après son nom.
