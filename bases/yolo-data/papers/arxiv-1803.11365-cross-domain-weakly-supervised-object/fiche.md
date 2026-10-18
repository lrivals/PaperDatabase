---
id: arxiv-1803.11365-cross-domain-weakly-supervised-object
fiche: done
date: 2026-10-18
---

# Cross-Domain Weakly-Supervised Object Detection through Progressive Domain Adaptation

Naoto Inoue, Ryosuke Furuta, Toshihiko Yamasaki, Kiyoharu Aizawa, 2018, arXiv preprint. https://arxiv.org/abs/1803.11365 (pas de DOI)
Type : preprint non relu par les pairs

## Problème

Détecter des objets communs dans des domaines d'image très différents des photos (clipart, aquarelle, bande dessinée) alors que construire un jeu annoté en boîtes pour chaque domaine est irréaliste (manque de sources, droits d'auteur, coût d'annotation) (§1). Tâche posée : « cross-domain weakly supervised object detection » : (i) boîtes + classes dans un domaine source ; (ii) seulement des labels d'image (liste des classes présentes) dans le domaine cible ; (iii) les classes cibles sont tout ou partie des classes sources (§1). Les auteurs rappellent que l'annotation d'une boîte coûte 35 s (citation [32]) ou 7 s par extreme clicking (citation [26]) (§2.1) ; ces chiffres ne sont pas mesurés ici.

## Méthode

Détecteur pleinement supervisé (FSD) pré-entraîné sur la source (VOC2007+2012 trainval), puis deux fine-tunings successifs (Fig. 3, §4) :

1. **Domain transfer (DT)** : CycleGAN non apparié entre source et cible convertit les images sources (avec leurs boîtes) en images au style cible ; les boîtes restent exactes, mais l'image est de qualité imparfaite (§4, §4.1). Le FSD est fine-tuné 1 époque dessus (§5.1).
2. **Pseudo-labeling (PL)** : sur chaque image cible avec ses labels d'image z, le FSD (déjà adapté par DT) prédit ; pour chaque classe c de z, on garde la détection la plus confiante (top-1) comme pseudo-boîte (§4.2). Image de vraie qualité, boîtes approximatives. Fine-tuning 10 000 itérations (§5.1). Aucune couche du FSD n'est modifiée ; méthode applicable à tout détecteur (§4.2).

L'ordre est jugé critique : la qualité du PL dépend du FSD utilisé (§4). Baseline : SSD300 (ChainerCV), aussi testé avec YOLOv2 et Faster R-CNN (Table 3). Comparés : WSDDN, ContextLocNet (détection faiblement supervisée), ADDA (adaptation par alignement de distributions), ensemble (§5.1).

## Plateforme et implémentation

Pas de matériel dédié : implémentation Chainer, GPU, puissance et débit `n/r`. Hyperparamètres : CycleGAN lr 1e-5 pendant 10 époques puis décroissance linéaire sur 10 ; fine-tuning lr 1e-5, mais 1e-6 sur Watercolor2k car sur-apprentissage même pour l'Ideal case ; NMS 0,45, seuil de confiance 0,01 ; entrée SSD 300×300 (§5.1, §5.3). Pour les variantes « +extra », 30 000 itérations (§5.3). Jeux et code publiés : https://naoto0804.github.io/cross_domain_detection (note de bas de page, §1) ; non vérifié ici.

## Résultats

**Jeux créés** (Table 1, §3) : annotés en boîtes via Amazon Mechanical Turk (§3). Protocole de consignes, nombre d'annotateurs, accord inter-annotateurs : `n/r` dans le texte principal (renvoi au matériel supplémentaire, absent de `fulltext.md`).

| Jeu | Classes | Images | Instances | Origine (§3.1-3.2) |
|---|---|---|---|---|
| Clipart1k | 20 (= VOC) | 1 000 | 3 165 | CMPlaces + Openclipart + Pixabay, requêtes sur 205 classes de scènes |
| Watercolor2k | 6 | 2 000 | 3 315 | BAM! (labels d'image bruités, 80-90 % de précision) |
| Comic2k | 6 | 2 000 | 6 389 | BAM! |

Total 5 000 images, 12 869 instances (§3). Les 6 classes de Watercolor/Comic : bicycle, bird, cat, car, dog, person (intersection VOC et BAM!). Watercolor/Comic : images contenant au moins une des 6 classes d'après les labels BAM! sans autre filtrage : 17 814 (aquarelle) et 52 790 (BD) ; 2 000 tirées au hasard et annotées en boîtes ; le reste (15 814 et 50 790, « extra ») garde ses labels d'image bruités et incomplets (§3.2). Découpage train/test 1:1, boîtes du train ignorées sauf pour l'Ideal case (§5.1).

**mAP (%), SSD300** (Tables 2-5 ; Table 2 : corps reconstruit par Grobid, seules les valeurs recoupées par le texte sont reprises) :

| Méthode | Clipart1k | Watercolor2k | Comic2k |
|---|---|---|---|
| Baseline (source seule) | 26,8 | 49,6 | 24,9 |
| ADDA | 27,4 | 49,8 | 23,8 |
| WSDDN / CLNet | 4,4 / 7,8 | 12,7 / 17,4 | 5,6 / 3,8 |
| DT | 38,0 | 50,4 | 29,8 |
| PL | 36,4 | 54,0 | 32,9 |
| DT+PL | 46,0 | 54,3 | 37,2 |
| PL +extra / DT+PL +extra | n/r | 59,1 / 59,1 | 36,9 / 42,2 |
| Ideal case (boîtes cibles du train) | 55,4 | 58,4 | 46,4 |

- Clipart1k : DT +11,2 pts, PL +9,6 pts, DT+PL +19,2 pts sur la baseline, à 9,4 pts de l'Ideal case (§5.2). Sans labels d'image, PL (top-1 global) tombe à 25,3 et DT+PL à 32,7 (< DT seul, 38,0) : les labels d'image sont indispensables à PL (§5.2 Ablation, Table 2). DT seul n'exige aucun label cible (§5.2).
- Autres détecteurs sur Clipart1k (Table 3) : YOLOv2 25,5 → 39,9 (Ideal 51,2) ; Faster R-CNN 26,2 → 34,9 (Ideal 50,0). Gain moindre que pour SSD300, que les auteurs attribuent (hypothèse) à l'augmentation de données de SSD (zoom in/out) utile avec des pseudo-labels bruités (§5.2).
- Avec les images extra (aucune annotation manuelle, labels BAM! bruités), DT+PL atteint ou dépasse l'Ideal case entraîné sur 1 000 images annotées sur Watercolor2k (59,1 vs 58,4) ; sur Comic2k il reste 4,2 pts sous (42,2 vs 46,4, différence calculée) (§5.3).
- Gain annoncé : environ 5 à 20 pts de mAP sur les meilleures baselines (résumé).
- Erreurs (Fig. 4, §5.2) : le détecteur source échoue surtout par confusion de classes et de fond, pas par localisation ; PL réduit surtout ces confusions.

→ reportés dans `benchmarks.csv` : 12 lignes proposées (Clipart1k SSD300 baseline, DT, PL, DT+PL, Ideal, DT+PL sans label ; YOLOv2 et Faster R-CNN DT+PL ; Watercolor2k DT+PL et DT+PL +extra ; Comic2k DT+PL et DT+PL +extra), ajoutées par l'agent principal.

## Limites et critique

- Source et cible sont toutes deux relativement faciles : VOC (20 classes) vers 6 à 20 classes, détecteurs de 2016-2018 (SSD300, YOLOv2). Aucun YOLO récent, pas de COCO ; transfert à d'autres écarts de domaine (infrarouge, aérien, médical) non testé.
- PL ne garde qu'une boîte par classe présente (top-1) : les instances multiples sont perdues, ou comptées comme négatifs. Reconnu par les auteurs comme travail futur (§6). Le bruit de PL est donc fort sur des images à plusieurs objets de même classe.
- Test sur 500 images en moyenne par jeu (moitié des jeux) : variations de quelques points peu fiables (aucun écart-type ni répétition rapportés, `n/r`). Pas de seuil IoU de mAP explicite dans le texte (§5.1 dit seulement AP/mAP) : probablement 0,5 VOC, déduit.
- L'hyperparamètre lr a été changé pour Watercolor2k à cause de l'Ideal case : réglage sur le test non exclu, non discuté.
- « Ideal case » est une borne « faible » (pré-entraînée source puis fine-tunée sur 500 à 1 000 images annotées), non un entraînement complet : ses chiffres (Clipart 55,4, Watercolor 58,4, Comic 46,4) sont dépassés par DT+PL +extra sur Watercolor2k.
- Les labels « extra » sont des labels de moteur de recherche/BAM! (80-90 % de précision) : le gain dépend d'un tri de qualité de cette source ; il faudrait vérifier ce taux sur d'autres sources.
- DT : de l'aveu des auteurs, la traduction CycleGAN est imparfaite (transfère couleur et texture, garde bords et sémantique) (§5.4). Pas d'ablation du style transfert sur la précision des boîtes.
- Coûts d'annotation (35 s, 7 s) : cités, non mesurés ; aucune mesure du temps pour obtenir les labels d'image ni comparaison coût/gain.
- Préprint ; protocole d'annotation détaillé dans un matériel supplémentaire non lu.

## Pertinence

- **CONSTRUIRE** : trois jeux de domaine hors photo (Clipart1k, Watercolor2k, Comic2k), 6 à 20 classes, avec une méthode de collecte reproductible (requêtes sur des classes de scènes, tri par attributs d'une base annotée par image), et une réserve « extra » de grandes quantités d'images à labels d'image bruités. À utiliser pour évaluer la robustesse à un changement de style, pas pour un usage direct dans un projet de photos.
- **ANNOTER** : quand l'annotation en boîtes du domaine cible est trop chère, on peut se contenter de labels d'image (classes présentes) et d'un détecteur déjà entraîné sur un domaine proche annoté en boîtes. Sur 3 jeux, DT+PL récupère de 9,4 pts d'écart à l'Ideal case (Clipart) à un niveau égal ou supérieur (Watercolor avec extra) ; il reste 4,2 pts sous l'Ideal case sur Comic2k avec extra et 9,2 pts sans (calculé). Règle pratique : labels d'image suffisants si l'écart de domaine est surtout de style (couleur, texture) et si les classes cibles sont dans celles de la source ; les labels d'image sont indispensables (sans eux PL est nuisible, §5.2). Ne tient pas si les images contiennent beaucoup d'instances d'une même classe (top-1).
- **PRÉTRAITER** : n/a, hormis la remarque que le détecteur redimensionne à 300×300.
- **AUGMENTER** : le transfert de style CycleGAN des images sources annotées est une augmentation de domaine qui conserve les boîtes (+11,2 pts sur Clipart sans aucun label cible, +0,8 sur Watercolor, +4,9 sur Comic par rapport à la baseline, calculé sur Tables 4-5) ; le gain est donc inégal selon le domaine. Applicable à un dataset à peu de données cibles : stylisation des images annotées, puis pseudo-labels ; le choix du détecteur compte, avec un plus petit gain pour YOLOv2 que SSD (Table 3).
- Dans quel cas appliquer : peu ou pas de boîtes dans le domaine cible, labels d'image faciles à obtenir (moteur de recherche, métadonnées), source annotée proche par ses classes. Pour une chaîne YOLO moderne, c'est une recette à reproduire, pas une valeur à reprendre.

## Gaps identifiés

- Aucune version de la méthode avec un détecteur de type YOLO récent (v5-v11) ni avec des pseudo-labels multi-instances (au-delà du top-1) ni avec un modèle fondation.
- Pas de mesure du coût réel (temps humain) des labels d'image vs boîtes, donc pas de courbe coût-qualité.
- Pas de comparaison à une annotation partielle par boîtes (quelques centaines de boîtes cibles) ou à l'active learning.

## Statut de lecture

papier complet (`fulltext.md` lu en entier, extraction grobid ok). Table 2 : corps reconstruit par Grobid avec colonnes mélangées (lignes Ideal case et DT fusionnées) ; seules les valeurs mAP confirmées par le texte ou par la Table 3 sont retenues (baseline 26,8, DT 38,0, PL 36,4, DT+PL 46,0, Ideal 55,4, PL sans label 25,3, DT+PL sans label 32,7), les AP par classe sont ignorés. Table 1 : valeurs lisibles malgré l'avertissement d'extraction. Matériel supplémentaire (consignes d'annotation, hyperparamètres YOLOv2/Faster R-CNN) absent. Déduit et non affirmé par les auteurs : taille des ensembles train/test (1:1 de 1 000 ou 2 000 images), seuil IoU de la mAP, tous les écarts « à l'Ideal case » hors Clipart (calculés), l'hypothèse sur l'augmentation de SSD (formulée comme une suggestion par les auteurs).
