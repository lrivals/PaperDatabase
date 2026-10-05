---
id: arxiv-1902.04103-bag-freebies-training-object-detection
fiche: done
date: 2026-10-05
---

# Bag of Freebies for Training Object Detection Neural Networks

Zhi Zhang, Tong He, Hang Zhang, Zhongyue Zhang, Junyuan Xie, Mu Li, 2019, arXiv preprint. https://arxiv.org/abs/1902.04103
Type : preprint non relu par les pairs

## Problème

Les détecteurs (one-stage comme YOLO/SSD, two-stage comme Faster R-CNN) ont chacun un pipeline de données et d'entraînement différent, ce qui empêche de transférer les astuces d'une famille à l'autre (§1). Les auteurs cherchent des « freebies » : modifications d'entraînement seul, sans changer l'architecture ni le coût d'inférence, qui améliorent la mAP (Abstract, §1).

## Méthode

Six astuces, empilées incrémentalement sur YOLOv3 (Darknet-53) et Faster R-CNN (ResNet) :

- **Mixup visuellement cohérent pour la détection (§3.1)** : mélange de pixels de deux images avec alignement préservant la géométrie (pas de déformation initiale) ; les labels des deux images sont conservés tous deux (pas de mélange de one-hot comme en classification). Le ratio suit une loi Beta(α, β) avec α, β ≥ 1 (au lieu de B(0.2, 0.2) du mixup de classification, où la plupart des mélanges sont presque du bruit) : les objets deviennent « cohérents », comme des images de transition de vidéo à faible FPS. Beta(1.5, 1.5) est « marginalement meilleur » que Beta(1.0, 1.0) (uniforme) et meilleur qu'un mélange fixe 50/50 (§3.1, Table 1 : corps non extrait, valeurs n/r). Variante « loss pondérée » : la perte de chaque objet est pondérée par le ratio de son image d'origine (Légende Table 1). Motivation : l'occlusion mutuelle est courante en détection ; le réseau doit voir des patchs encombrés inhabituels (§3.1).
- **Label smoothing sur la tête de classification (§3.2)** : q_i = 1−ε si i = classe vraie, ε/(K−1) sinon (Eq. 3) ; pour les sorties sigmoïde de YOLOv3, on corrige simplement les bornes des cibles. Valeur de ε : n/r.
- **Prétraitement / augmentation (§3.3)** : géométrique (crop contraint, expansion, flip horizontal, resize aléatoire à interpolation aléatoire) et colorimétrique (luminosité, teinte, saturation, contraste). Pour Faster R-CNN, **pas de crop aléatoire** : l'échantillonnage de RoI joue déjà ce rôle (§3.3) ; seul le flip horizontal (p = 0,5) est gardé (§4.1).
- **Planning d'entraînement (§3.4)** : cosinus au lieu du pas (YOLOv3 d'origine : ×0,1 à 40k et 45k itérations), avec warmup, jugé critique pour YOLOv3 (gradient dominé par les négatifs au départ).
- **BatchNorm synchronisée (§3.5)**, **entraînement à formes aléatoires (§3.6)** : H = W ∈ {320, …, 608} par pas de 32 pour YOLOv3.

## Plateforme et implémentation

Entraînement multi-GPU (nombre et type : n/r) ; mesure d'inférence non faite : aucune latence, FPS ni puissance rapportée (n/r). Code et poids pré-entraînés publiés dans GluonCV (§1, §5). Évaluation à échelle unique, un seul modèle, NMS standard, sans données externes (§4).

## Résultats

Ablation incrémentale sur YOLOv3 (Table 3, VOC07 test, 416×416, entraîné sur VOC07+12 trainval) :

| Étape | mAP | Δ | Δ cumulé |
|---|---|---|---|
| sans augmentation de données | 64,26 | −15,99 | −15,99 |
| baseline | 80,25 | 0 | 0 |
| + BN synchronisée | 80,81 | +0,56 | +0,56 |
| + formes aléatoires | 81,23 | +0,42 | +0,98 |
| + cosinus | 81,69 | +0,46 | +1,44 |
| + label smoothing | 82,14 | +0,45 | +1,89 |
| + mixup | 83,68 | +1,54 | +3,43 |

Le mixup est la plus grosse contribution (+1,54), devant tout autre freebie. Mais l'augmentation de base pèse bien plus : sa suppression coûte 15,99 points (§4.1 : « nearly 16% »), donc le détecteur one-stage en dépend fortement.

Faster R-CNN (Table 4, VOC07 test, 600×1000) : sans augmentation 77,61 (−0,16) ; baseline 77,77 ; + cosinus 79,59 (+1,82) ; + label smoothing 80,23 (+0,64) ; + mixup 81,32 (+0,89), cumul +3,55 (Table 4). Contraste one-stage / two-stage : l'augmentation géométrique ne vaut que 0,16 point pour Faster R-CNN, car l'échantillonnage de RoI remplace le crop aléatoire (§4.1).

COCO 2017 val, mAP 0.5:0.95 (Table 5 ; corps non extrait, valeurs lues dans le texte de §4.2 : à vérifier) :

| Modèle | d'origine | avec BoF | Δ |
|---|---|---|---|
| Faster R-CNN R50 | 36,5 | 37,6 | +1,1 |
| Faster R-CNN R101 | 39,4 | 41,1 | +1,7 |
| YOLOv3 @320 | 28,2 | 33,6 | +5,4 |
| YOLOv3 @416 | 31,0 | 36,0 | +5,0 |
| YOLOv3 @608 | 33,0 | 37,0 | +4,0 |

Le gain est plus grand à basse résolution (§4.2). YOLOv3 avec BoF atteint 37,0 contre 36,5 pour Faster R-CNN R50 d'origine (§4.2).

Robustesse (Fig. 5, Table 2, §3.1) : test « éléphant dans la pièce » (patch d'éléphant glissé sur une image d'intérieur), YOLOv3 entraîné sur COCO 2017 : 94,12 avec le mixup cohérent contre 42,95 sans (métrique exacte : n/r, corps de Table 2 non extrait ; les chiffres viennent du texte). Test qualitatif et sur un cas unique.

Mixup en deux phases (Tables 6 et 7, §4.3 ; corps non extrait, valeurs de COCO val telles que lues dans la source, à vérifier). YOLOv3/Darknet-53 : −/− 35,0 ; mixup détection seul 35,3 ; mixup pré-entraînement seul 36,4 ; les deux 37,0. Faster R-CNN R101 : 39,9 ; 40,1 ; 40,1 ; 41,1. Le texte annonce « ≈0,2 » pour une phase et « 1,2 » pour les deux, ce qui colle à Faster R-CNN ; pour YOLOv3 les écarts lus (+0,3, +1,4, +2,0) ne correspondent pas : doute sur l'attribution des cellules. Retenu : les deux phases se cumulent (§4.3).

→ reportés dans `benchmarks.csv` : 17 lignes proposées (Table 3 : 7 ; Table 4 : 5 ; Table 5 : 5). Tables 1, 2, 6, 7 non reprises (corps absent ou ambigu).

## Limites et critique

- Ablation **incrémentale et ordonnée** : chaque Δ dépend de l'ordre d'empilement (le mixup est ajouté en dernier) ; pas d'ablation « une astuce seule » ni d'interaction mesurée (sauf mixup en §4.3).
- Pas de répétitions ni d'écart-type : des écarts de 0,4 à 0,6 point sont du même ordre qu'un bruit de graine habituel sur VOC (déduit, non mesuré par les auteurs).
- Table 1 (choix de la loi Beta) sans corps extrait : l'avantage de Beta(1,5, 1,5) sur 1,0 est qualifié de « marginal » ; rien ne prouve la supériorité d'une valeur précise. Le ratio de mélange et le fait que les deux jeux de labels sont conservés sont à confirmer dans GluonCV.
- Baseline de l'ablation VOC (80,25 à 416) bien plus haute que le YOLOv3 d'origine : la baseline GluonCV inclut déjà une augmentation « standard » non détaillée (liste du §3.3 sans paramètres).
- Les « 5 % » de l'abstract sont le gain sur COCO à 320 (+5,4), qui compare au YOLOv3 d'origine (Darknet), pas à la même implémentation sans astuces.
- Détails de l'entraînement (durées, epochs, ε, batch, GPU) : n/r ; pas de petits objets analysés (seulement la mAP globale, Fig. 7-8 par classe) ; effet du mixup sur objets occultés évalué sur un seul cas.
- Preprint, 2019, YOLOv3 uniquement : ne couvre pas Mosaic de YOLOv4/v5 ni les pipelines Ultralytics.

## Pertinence pour la thèse

Pour **AUGMENTER** un dataset de détection : mesure directe, sur YOLOv3, de la valeur de l'augmentation. Sans augmentation, −16 points sur VOC ; les augmentations géométriques et colorimétriques sont donc obligatoires pour un détecteur one-stage, alors qu'elles comptent à peine pour un two-stage (−0,16). À appliquer : tout entraînement YOLO de petit dataset, où l'on part de l'augmentation standard puis on ajoute le mixup (le plus rentable des freebies, +1,54) avec un ratio Beta(1,5, 1,5) plutôt que le Beta(0,2, 0,2) de la classification ; il est surtout utile quand les scènes sont encombrées ou occultées et pour la robustesse à des objets hors contexte (Table 2). À **PRÉTRAITER** : l'entraînement à résolution aléatoire (320–608, pas de 32) apporte +0,42 et le gain des BoF est plus fort à basse résolution d'inférence (+5,4 à 320) : utile pour la cible embarquée. Label smoothing (+0,45 YOLOv3, +0,64 Faster R-CNN) : gratuit, utile quand les labels sont bruités (déduit, non testé ici). Pour **CONSTRUIRE/ANNOTER** : rien de direct. Laisse ouvert : combinaison avec Mosaic / Copy-Paste, effet sur les petits objets, comparaison avec des augmentations apprises (voir [Simple Copy-Paste](../arxiv-2012.07177-simple-copy-paste-strong-data/fiche.md), [YOLOv4](../arxiv-2004.10934-yolov4-optimal-speed-accuracy-object/fiche.md) qui reprennent ces astuces).

## Gaps identifiés

- Ablation par astuce isolée et par ordre aléatoire sur un YOLO moderne ; effet du mixup détection vs Mosaic.
- Effet de ces freebies selon la taille du dataset (VOC 16k vs COCO 118k seulement ; pas de régime peu de données).
- Effet sur petits objets / mAP_small, non rapporté.

## Statut de lecture

Papier complet (fulltext.md lu en entier, extraction grobid). Tables 1, 5, 6, 7 : corps non extrait ; leurs chiffres viennent du texte courant et sont à vérifier sur le PDF ; Table 2 : seules deux valeurs lisibles.
Ce qui suit est déduit et non affirmé par les auteurs : bruit de graine ; utilité du label smoothing sous bruit de labels ; adéquation au cas embarqué ; attribution des cellules des Tables 6 et 7 ; lecture « les deux jeux de labels sont conservés » (le texte parle d'un alignement préservant la géométrie et d'une loss pondérée, sans détailler les labels).
