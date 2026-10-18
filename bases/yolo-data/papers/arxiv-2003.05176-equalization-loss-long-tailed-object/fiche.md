---
id: arxiv-2003.05176-equalization-loss-long-tailed-object
fiche: done
date: 2026-10-18
---

# Equalization Loss for Long-Tailed Object Recognition

Jingru Tan, Changbao Wang, Buyu Li, Quanquan Li, Wanli Ouyang, Changqing Yin, Junjie Yan, 2020, arXiv preprint. https://arxiv.org/abs/2003.05176
Type : preprint non relu par les pairs

## Problème

Sur un jeu à grand vocabulaire et à longue traîne (LVIS), les détecteurs échouent sur les classes rares (résumé, §1). Les auteurs expliquent cela par la compétition entre classes : tout exemple positif d'une classe est un négatif pour toutes les autres, donc le classifieur d'une classe rare reçoit surtout des gradients « décourageants » et peu de gradients positifs (§1, §3.1). Fig. 1 : la norme moyenne du gradient négatif dépasse celle du gradient positif pour les classes rares, l'inverse pour les classes fréquentes. Les travaux antérieurs traitent le déséquilibre par ré-échantillonnage ou par des pertes focalisées sur fond contre premier plan, pas sur le déséquilibre entre classes de premier plan (§1).

## Méthode

Equalization loss (EQL) : sigmoid cross-entropy avec un poids par classe et par proposition, w_j = 1 − E(r)·T_λ(f_j)·(1 − y_j) (Éq. 6-7, §3.2). E(r) vaut 1 pour une proposition de premier plan. f_j est la fréquence de la classe (nombre d'images de la classe sur nombre d'images du jeu). T_λ(f) vaut 1 si f < λ, sinon 0. Pour une classe en dessous du seuil λ, on ignore donc les gradients négatifs venant de propositions d'autres classes de premier plan ; ceux du fond sont conservés, sinon le modèle produit beaucoup de faux positifs (§3.2). Le seuil se règle par le Tail Ratio TR(λ), part des images des classes sous λ (Éq. 8). Sur LVIS, une classe n'est pas ignorée si elle figure dans les listes d'étiquettes positives ou négatives au niveau image (§4.2). Variante softmax (SEQL) pour la classification, avec un tirage aléatoire β de probabilité γ qui garde les négatifs (§3.3). Aucune modification d'architecture, de données ni d'échantillonnage.

## Plateforme et implémentation

Mask R-CNN + FPN (mapping masque agnostique de la classe), images 800/1333, flip horizontal seul, 16 GPU, batch 32, SGD, 25 époques, lr 0,04 (§4.2). Puissance : n/r (sans objet). Code publié : https://github.com/tztztztztz/eql.detectron2 (résumé). Aucun YOLO ni détecteur à une étape testé.

## Résultats

Toutes les valeurs sont en mask AP sur LVIS v0.5 val, ResNet-50 FPN, sauf mention. Les corps des tableaux 3, 4, 5, 6, 10, 12 ont été extraits en désordre ; les valeurs ci-dessous sont celles lisibles, recoupées avec le texte.

- **Gain principal (Table 1, Table 2)** : R-50-FPN, AP 20,1 → 22,8 ; AP_r 7,2 → 11,3 (+4,1) ; AP_c 19,9 → 24,7 (+4,8) ; AP_f 25,4 → 25,1 (−0,3). Le texte confirme +4,1 et +4,8 (résumé). Autres modèles (Table 1, ordre des colonnes du corps reconstruit, à vérifier) : R-101-FPN 22,2 → 24,8 ; R-50-C4 19,7 → 22,5 ; Cascade R-50-FPN 21,1 → 23,1. Le gain vient surtout des classes rares et communes (§4.3).
- **Ablation du seuil λ (Table 2, §4.4)** : λ_r = 1,76e-4 (TR 0,93 %, sépare exactement les classes rares) : AP 20,8, AP_r 11,7, AP_c 20,2, AP_f 25,2. λ_c = 1,76e-3 (TR 9,08 %, inclut rares et communes, valeur retenue) : AP 22,8, AP_r 11,3, AP_c 24,7, AP_f 25,1. λ = 5e-3 (TR 18,17 %) : AP 22,4, AP_r 10,0, AP_c 23,6, AP_f 25,7. Le meilleur TR est entre 2 % et 10 % (§4.4) ; l'AP global monte tant que λ couvre plus de queue puis se dégrade quand λ atteint des classes fréquentes. AP_f reste stable car EQL n'agit pas au-dessus de λ.
- **Forme de T_λ (Table 3)** : seuil dur 22,8 ; décroissance exponentielle 22,3 ; Gompertz 22,7. Résultats proches, le seuil dur a moins d'hyper-paramètres.
- **Rôle de E(r) (Table 4, Fig. 4)** : sans E(r), AP 22,2 (AP_r 12,5, AP_f 23,1) contre 22,8 avec. Sans E(r), le fond est aussi ignoré, d'où plus de faux positifs ; AP_r monte quand même car le protocole LVIS ignore les faux positifs des classes d'incertitude (§4.4).
- **Comparaison avec d'autres méthodes (Table 5, §4.5)** : sigmoid 20,1 (AP_r 7,2 / AP_c 19,9 / AP_f 25,4) ; softmax 20,2 (4,5 / 20,8 / 25,6) ; class-aware sampling 18,5 (7,3 / 19,3 / 21,9) ; repeat factor sampling 21,3 (12,2 / 21,5 / 24,7) ; EQL 22,8 (11,3 / 24,7 / 25,1). Selon les auteurs, le ré-échantillonnage améliore AP_r et AP_c au détriment d'AP_f, les pondérations par fréquence donnent un gain global négligeable, EQL gagne sur AP_r et AP_c sans toucher AP_f. Le corps du tableau 5 est partiellement désordonné : le texte ne chiffre pas les pondérations de classes, leurs lignes sont `n/r` ici. Attention : RFS fait mieux qu'EQL sur AP_r (12,2 contre 11,3) mais perd 0,7 d'AP_f ; les auteurs combinent les deux dans la solution du concours (Annexe A).
- **Open Images OID19 (Table 6, §5)** : AP 57,83 pour EQL contre 56,50 (class-aware sampling) et 48,13 (sigmoid) ; TR 3 %, λ 3e-4. Gain de 2,6 et 10,88 points sur le groupe des 100 classes les plus rares (texte). Corps du tableau désordonné : à vérifier.
- **Concours LVIS 2019 (Table 11, 12)** : 36,4 mask AP en val (base du concours 30,1) ; 28,85 sur test 20k, AP_r 17,71, 1er du concours ; baseline LVIS 20,49 (AP_r 9,80). Solution = grosse architecture + EQL + RFS + COCO/Open Images en données externes + tests multi-échelles + ré-ajustement des scores : EQL n'est pas isolé.
- **Classification (Table 8)** : CIFAR-100-LT, SEQL 43,38 top-1 contre 41,33 en softmax ; ImageNet-LT : chiffres de la Table 10 `n/r` (corps manquant).
→ reportés dans `benchmarks.csv` : lignes proposées par l'agent (15), à ajouter par l'agent principal.

## Limites et critique

- Évalué sur LVIS (segmentation d'instances, Mask R-CNN à deux étapes) et Open Images ; jamais sur un détecteur à une étape de type YOLO ni sur COCO. L'effet sur un YOLO est déduit, non mesuré. Une tête de classification sigmoid indépendante (cas de YOLO v5/v8) est compatible avec la formule, mais l'objectness et l'assignation de labels de YOLO modifient ce que « proposition de premier plan » veut dire (déduit).
- Les gains dépendent du protocole LVIS : annotations éparses, étiquettes image-niveau positives/négatives qui restaurent les gradients négatifs (§4.2), faux positifs de classes incertaines ignorés (§4.4, qui explique le résultat contre-intuitif de la Table 4). Sur un jeu exhaustivement annoté, le résultat peut différer (déduit).
- λ est un hyper-paramètre propre à chaque jeu, réglé sur la val (TR 2-10 %), pas de règle universelle ; fréquence en nombre d'images, pas d'instances.
- RFS donne un AP_r supérieur (12,2) et la Table 5 ne teste pas la combinaison EQL + RFS isolément ; le concours les combine mais sans ablation séparée.
- Une seule exécution rapportée, pas d'écart-type ; différences de 0,1 à 0,5 AP de la Table 2/3 non significatives.
- Preprint, code publié (Detectron2).

## Pertinence pour la thèse

Axe `imbalance-small`. Pour CONSTRUIRE un dataset déséquilibré : le papier montre que le manque d'exemples ne suffit pas, le gradient négatif des classes dominantes écrase les classes rares, donc collecter 10 à 100 images de plus par classe rare reste le levier de fond, et la perte seule récupère +4 AP_r sur LVIS (Table 2). Pour ANNOTER : sur un jeu partiellement annoté, il faut des étiquettes négatives au niveau image (classe absente de façon certaine) sans quoi on perd les gradients utiles (§4.2) ; déduit : annoter les classes rares exhaustivement vaut mieux que les classes fréquentes. Pour PRÉTRAITER : rien. Pour AUGMENTER : non traité ; RFS est cité comme complément (Table 5) et peut se combiner avec EQL (Annexe A). Quand l'appliquer (déduit) : jeu avec beaucoup de classes et une queue de moins de 10 % des images ; commencer par RFS ou un oversampling modéré (simple, sans toucher à la perte), ajouter EQL si AP_r reste bas, vérifier que AP des classes fréquentes ne baisse pas. Pour un jeu à peu de classes (typique YOLO personnalisé) le papier n'apporte pas de preuve directe.

## Gaps identifiés

- Aucune mesure de EQL (ou de RFS) sur un détecteur de la famille YOLO ni sur un jeu exhaustivement annoté.
- Interaction avec Mosaic/Copy-Paste (augmentations qui changent la fréquence effective des classes) non étudiée.
- Absence d'une règle pour fixer λ sans val ; seuil en images et non en instances.

## Statut de lecture

papier complet (`fulltext.md`, backend grobid). Tableaux 3, 4, 5, 6, 10, 12 : corps extrait en désordre ou absent (`extraction.warnings`) ; les chiffres retenus sont ceux que le texte recoupe, `confidence: medium`. Table 1 : colonnes réordonnées par l'extraction, reconstruites par recoupement avec la Table 2 (R-50-FPN) ; les autres lignes sont à vérifier. Déduit et non affirmé par les auteurs : application à YOLO, comparaison fréquent/rare pour le choix de λ en pratique, conseils d'annotation, ordre RFS puis EQL.
