---
id: arxiv-1909.00169-imbalance-problems-object-detection-review
fiche: done
date: 2026-10-18
benchmarks: none
---

# Imbalance Problems in Object Detection: A Review

Kemal Oksuz, Baris Can Cam, Sinan Kalkan, Emre Akbas, 2019, arXiv preprint. https://arxiv.org/abs/1909.00169
Type : preprint non relu par les pairs (survey ; dépôt de suivi annoncé : github.com/kemaloksuz/ObjectDetectionImbalance)

## Problème

Un déséquilibre apparaît « lorsque la distribution d'une propriété d'entrée affecte la performance » (§1). Le papier recense huit problèmes de déséquilibre dans les détecteurs profonds, les range dans une taxonomie à quatre familles (Table 1, §3), et critique pour chacun les remèdes publiés et les questions ouvertes. Les auteurs notent que certains déséquilibres viennent des données (classes, localisation des objets) et d'autres de la méthode, donc évitables par un autre choix de méthode : perte de régression, déséquilibre d'objectifs, déséquilibre de features, distribution des IoU (§3).

## Méthode

Revue de littérature, sans expérience nouvelle sur un benchmark. Quelques figures sont calculées par les auteurs : anchors RetinaNet par classe sur MS-COCO (Fig. 4), statistiques de classes, de tailles et de positions des jeux de données (Fig. 5, 7, 13), effet du régresseur sur l'IoU (Fig. 12).

Taxonomie (Table 1, §3 ; ce qui est « donnée » ou « méthode » est la lecture des auteurs en §3) :

| Famille | Problème | Remèdes côté DONNÉES | Remèdes côté PERTE / ARCHITECTURE |
|---|---|---|---|
| Classe (§4) | avant-plan / arrière-plan | échantillonnage dur : aléatoire, SSD (négatifs à plus forte perte), OHEM, IoU-based sampling, filtrage des négatifs faciles (§4.1.1) ; génératifs (§4.1.4) : Adversarial Fast-RCNN (features), Task Aware Data Synthesis (GAN), PSIS (échange d'instances de même classe entre deux images selon la performance de la classe), pRoI Generator (RoIs positifs à IoU voulu) | pondération douce : YOLO (fond × 0,5), Focal Loss (γ = 2), GHM, PISA (§4.1.2) ; sans échantillonnage : Residual Objectness, réglages d'initialisation et de poids, AP Loss, DR Loss (§4.1.3) |
| Classe (§4) | avant-plan / avant-plan, jeu de données (longue traîne) | méthodes génératives (copier-coller d'objets, GAN) citées comme applicables (§4.2.1) | regroupement hiérarchique de classes par similarité (Ouyang et al.) |
| Classe (§4) | avant-plan / avant-plan, lot | OFB sampling : probabilité d'échantillonnage par boîte pour un lot uniforme en classes ; gain « non significatif » (§4.2.2) | n/a |
| Échelle (§5) | objets / boîtes | entraînement sur pyramide d'images : SNIP (n'active que les boîtes de taille adaptée), SNIPER (rognage) (§5.1.3) | prédiction multi-niveaux (SSD, MSCNN, SDP), FPN, combinaisons image + feature (§5.1.1-5.1.4) |
| Échelle (§5) | niveau des features | n/a | PANet, Libra FPN, STDN, Parallel-FPN, NAS-FPN, Auto-FPN… (§5.2) |
| Spatial (§6) | perte de régression | n/a | Smooth L1, Balanced L1, KL Loss, IoU / GIoU / DIoU / CIoU Loss (§6.1, Table 5) |
| Spatial (§6) | distribution des IoU | boîtes générées à IoU uniforme : IoU-uniform R-CNN (jitters), pRoI Generator (§6.2) | Cascade R-CNN (seuils 0,5 / 0,6 / 0,7), HSD |
| Spatial (§6) | position des objets | n/a | Guided Anchoring (ancres apprises), FreeAnchor (appariement par sac de candidates) (§6.3) |
| Objectif (§7) | classification contre régression | n/a | pondération de tâches (hyperparamètre validé), CARL, Guided Loss ; plages de pertes à harmoniser |

À retenir pour des données de détection :
- Sur le déséquilibre entre classes, le papier ne fournit aucun protocole « combien d'instances par classe ». Il note qu'une classe très rare peut figurer parmi les mieux détectées : le nombre d'exemples n'explique pas seul l'écart, d'après l'étude PSIS [65] qu'il cite (§4.4.2).
- Il écrit que les petits objets sont « surprenamment abondants » dans les jeux de données (biais vers les petites tailles, Fig. 7) mais que les méthodes d'échelle échouent encore sur eux (§3, §5).
- Il observe que les ré-échantillonnages de la classification (sur- et sous-échantillonnage, SMOTE / ADASYN, fine-tuning sur sous-ensemble équilibré, class-balanced loss, redondance de données, active learning, GAN) n'ont presque pas été portés à la détection (§8.1). C'est la liste de pistes la plus utile pour une base « données ».

## Plateforme et implémentation

Sans objet (survey, pas d'implémentation). Pas de puce ni de puissance. Pas de code propre, hors la page web de suivi (lien du §1.1, non vérifiée ici).

## Résultats

Aucun résultat original. Les chiffres du survey sont ceux des travaux cités, rapportés en « amélioration relative » sur des protocoles différents (backbone, jeu, résolution) :
- Focal Loss : 31,1 à 34,0 mAP, +9,3 % relatif (§4.3) ; OHEM : +14,7 % relatif sur Fast R-CNN VGG-16 (§4.3) ; PISA : 36,4 à 38,0 mAP sur les positifs (§4.3).
- SSD, nombre de couches de prédiction : 62,4 (1 couche), 70,7 (3), 74,6 (5) mAP@0,5 sur VOC07 (§5.3). FPN : 34,9 à 36,2 (§5.3). NAS-FPN : 40,1 à 44,2, avec environ 2 fois plus de paramètres et +26 % de temps (§5.3).
- Cascade R-CNN : 36,2 à 42,8 (§6.4). Guided Anchoring : +9,1 % de rappel moyen avec 90 % d'ancres en moins (§6.4).

Aucune ligne n'est ajoutée à `benchmarks.csv` : c'est un survey, les chiffres appartiennent aux travaux cités et ne sont pas comparables entre eux (règle de `/paper-fiche`, `benchmarks: none`).

## Limites et critique

- Date de 2019 : rien sur Mosaic / MixUp / CutMix / Copy-Paste modernes, YOLOv4 et suivants, ATSS / SimOTA / TAL, DETR, ni sur les modèles fondation. Les remèdes « données » y sont réduits aux méthodes génératives (§4.1.4).
- Les gains cités sont des relatifs pris à des protocoles hétérogènes ; les auteurs le disent pour HSD contre Cascade R-CNN (résolutions différentes, §6.4). Aucun classement n'est justifiable.
- Presque tout porte sur les détecteurs à ancres (Faster R-CNN, RetinaNet, SSD) ; les détecteurs bottom-up sont renvoyés aux questions ouvertes (§9.4). Le déséquilibre d'étiquetage par assignation (seuils IoU 0,5 / 0,4 / 0,3 selon Fast R-CNN / RetinaNet / RPN, §9.3) est signalé sans trancher.
- Le survey ne traite ni le bruit de labels comme cause de déséquilibre, ni les stratégies de découpage de dataset.
- Le texte d'origine est partiellement mutilé : Table 4 (méthodes génératives) sans corps, liste des méthodes de la Fig. 2 en vrac ; les valeurs de Table 4 sont `n/r` ici.

## Pertinence pour la thèse

Pertinence pour le thème de la base (axe `imbalance-small`), à appliquer ainsi :
- CONSTRUIRE un dataset : repérer d'abord le type de déséquilibre. Le déséquilibre avant / arrière-plan est géré par le détecteur (perte, échantillonnage) et non par la collecte. Le déséquilibre inter-classes et la distribution des tailles sont des propriétés du dataset (§3) : on les mesure avec des histogrammes de classes, de tailles et de positions comme en Fig. 5, 7 et 13. Pas de seuil chiffré fourni pour décider quand corriger.
- AUGMENTER : pour une classe rare ou des petits objets, la famille « génération » du survey correspond à copier-coller, échange d'instances de même classe selon la performance (PSIS) et synthèse GAN (§4.1.4). Elle est présentée comme applicable aux deux formes de déséquilibre de classes (§4.2.1). Les remèdes multi-échelle côté données sont les pyramides d'images et le rognage (SNIP, SNIPER, §5.1.3).
- PRÉTRAITER : SNIP établit que l'écart d'échelle entre entraînement et test compte (sur-échantillonner l'image d'un facteur 2 bat réduire le stride de 2, §5.1.3) ; c'est la justification du tiling / de la résolution d'entrée pour les petits objets.
- ANNOTER : §9.3 relie les labels bruités aux exemples difficiles faussement positifs ; un label de qualité aide au sampling difficile.
- Quand l'appliquer : surtout si le détecteur n'a pas déjà de perte focale ou d'assignation adaptative ; sur un YOLO moderne, le fond est déjà géré par la perte et l'assignation, donc la marge est surtout sur les classes rares, les petits objets et le bruit de labels.

Couverture de la base (d'après INDEX.md, fiches parfois encore `todo`) :

| Remède du survey | Dans la base |
|---|---|
| Focal Loss | oui (`arxiv-1708.02002`, fiche todo) |
| Longue traîne : perte et dataset | Equalization Loss (todo), LVIS (fiche) |
| Assignation de labels | ATSS (todo) ; ancres et appariement du YOLOv4 |
| Copier-coller, échange d'instances | Copy-Paste (Ghiasi), Select-Mosaic, Kisantal (petits objets) |
| Augmentation apprise, tiling | Zoph (AutoAugment détection), SAHI, Dynamic Tiling, Clustered Detection |
| Biais du pseudo-label | Unbiased Teacher |
| Bag of freebies | oui |

Manquants dans la base : OHEM et hard-example mining ; GHM, PISA, Libra R-CNN (sampling doux et équilibré) ; SNIP / SNIPER (pyramide d'images, entraînement échelle-conscient) ; FPN, PANet, NAS-FPN (non « données » mais citables pour l'échelle) ; pertes IoU (GIoU, CIoU, Balanced L1) ; Cascade R-CNN ; Guided Anchoring / FreeAnchor ; class-balanced loss / repeat-factor sampling (via LVIS ?) ; sur-échantillonnage de classes rares et SMOTE adaptés à la détection ; synthèse GAN de données dures (Task Aware Data Synthesis) et PSIS ; DETR / assignation Hongrois.

## Gaps identifiés

Questions ouvertes énoncées par les auteurs (§4.4, §5.4, §6.5, §9) :
- Utilité d'un exemple : sampling dur (OHEM) contre PISA (positifs faciles) ; poids optimal des négatifs ; effet sur le déséquilibre inter-classes jamais étudié (§4.4.1).
- Cause de la faible performance d'une classe, non corrélée au nombre d'exemples ; littérature de classification (transfert, redondance, supervision faible, perte dédiée) non transposée (§4.4.2). Effet du déséquilibre au niveau du lot (§4.4.3). Perte de rang AP Loss non spécifique par classe (§4.4.4).
- Caractéristiques des couches (abstraction, grossièreté, cardinalité) à quantifier ; pyramides d'images limitées par la mémoire (§5.4).
- Régression : perte unifiant plusieurs aspects, analyse des pertes complexes, meilleures ancres, déséquilibre de position relative, des boîtes qui se recouvrent, et de l'orientation (§6.5). Objectif : interdépendance classification / régression, rythmes d'apprentissage (§7.2).
- Transverse : approche unifiée, mesure d'un déséquilibre (quelle distribution cible, comment quantifier, §9.2), consensus sur le seuil IoU positif / négatif (§9.3), détecteurs bottom-up (§9.4).

Pour `gaps.md` : (1) aucun papier de la base ne mesure l'effet des remèdes de classification (sur-échantillonnage, class-balanced) sur un détecteur type YOLO ; (2) orientation et position des objets comme déséquilibre de données (OBB, drones) : ouvert dans le survey et absent de la base ; (3) mesure quantitative du déséquilibre d'un dataset de détection (classes, tailles, positions) : ouvert (§9.2).

## Statut de lecture

papier complet (`fulltext.md` lu en entier, extraction grobid ok). Table 4 sans corps extrait ; la liste de la Fig. 2 est en vrac ; Fig. 1-19 lues par légende seulement.
Ce qui suit est déduit et non affirmé par les auteurs : la lecture « données » des remèdes (qui est donnée et qui est perte), les applications au guide de la base (construire, annoter, prétraiter, augmenter), la couverture de la base et la liste des manquants, la marge réduite sur un YOLO moderne.
