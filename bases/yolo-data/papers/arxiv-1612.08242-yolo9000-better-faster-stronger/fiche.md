---
id: arxiv-1612.08242-yolo9000-better-faster-stronger
fiche: done
date: 2026-10-18
---

# YOLO9000: Better, Faster, Stronger

Joseph Redmon, Ali Farhadi, 2017, CVPR 2017 (arXiv 1612.08242, déposé en 2016). https://arxiv.org/abs/1612.08242 (DOI : n/r).
Type : conférence relue par les pairs (CVPR 2017) ; la version lue est la version arXiv.

## Problème

Détecteur généraliste rapide, précis et étendu à beaucoup de classes. YOLO fait beaucoup d'erreurs de localisation et a un rappel faible face aux méthodes à propositions de régions (§2). Côté données : les jeux de détection (milliers à centaines de milliers d'images, dizaines à centaines de classes) sont très inférieurs aux jeux de classification (millions d'images), et annoter pour la détection coûte bien plus cher que pour la classification (§1).

## Méthode

Architecture (§2-3) : YOLOv2 = YOLO + batch norm partout (>2 % de mAP), sans couches entièrement connectées, avec ancres, entrée 416×416 (carte 13×13, un seul centre), position contrainte par sigmoïde (~+5 % avec les clusters), passthrough 26×26×512 → 13×13×2048 (~+1 %). Backbone Darknet-19 : 19 conv., 5 max-pooling, 5,58 Gflops (VGG-16 : 30,69 ; réseau YOLO : 8,52). Tête : 3 conv. 3×3 à 1024 filtres puis conv. 1×1 ; VOC : 5 boîtes × (5 + 20) = 125 filtres (§3).

Aspects données (le cœur de cette fiche) :

- **Ancres par k-means (« dimension clusters », §2).** k-means sur les boîtes d'entraînement, distance d(boîte, centroïde) = 1 − IOU(boîte, centroïde) (et non euclidienne : les grandes boîtes feraient plus d'erreur). k varié, courbe de l'IOU moyen au plus proche centroïde (Fig. 2, non extraite) ; k = 5 retenu comme compromis complexité du modèle / rappel. Les centroïdes diffèrent des ancres manuelles : moins de boîtes courtes et larges, plus de boîtes hautes et fines. Les dimensions sont prédites comme décalage par rapport aux centroïdes (b_w = p_w·e^{t_w}).
- **Entraînement multi-échelle (§2).** Le réseau étant tout-convolutif, toutes les 10 batches une nouvelle taille d'entrée est tirée au hasard parmi les multiples de 32 {320, 352, …, 608} et le réseau est redimensionné à la volée. Un même jeu de poids sert à toutes les tailles (compromis vitesse/précision à l'inférence).
- **Classifieur haute résolution (§2-3).** Préentraînement ImageNet 160 époques à 224×224 (SGD, lr 0,1, décroissance polynomiale de puissance 4, wd 0,0005, momentum 0,9), puis fine-tuning de 10 époques à 448×448 (lr 10⁻³) avant le fine-tuning en détection : ~+4 % de mAP. Le réseau n'a plus à s'adapter à la fois à la tâche et à la résolution.
- **Augmentation (§3).** Classification : recadrages aléatoires, rotations, décalages de teinte, saturation et exposition. Détection : « similaire à YOLO et SSD » avec recadrages aléatoires, décalage de couleur, etc. (liste détaillée n/r) ; même stratégie sur COCO et VOC ; 160 époques, lr 10⁻³ divisé par 10 aux époques 60 et 90.
- **Entraînement conjoint détection + classification (§4).** Images mélangées des deux jeux. Image de détection : perte YOLOv2 complète ; la perte de classification ne se propage qu'au niveau de l'étiquette ou au-dessus dans l'arbre (étiquette « dog » : aucune erreur imputée à « German Shepherd »). Image de classification (sans boîte) : seule la perte de classification est rétropropagée, sur la boîte qui prédit la plus forte probabilité pour la classe ; on suppose qu'elle recouvre le « vrai » objet d'au moins 0,3 IOU et on rétropropage une perte d'objectness sur cette hypothèse.
- **WordTree et fusion de jeux (§4).** Arbre hiérarchique construit à partir de WordNet (graphe orienté) : on ajoute les synsets à chemin unique, puis, itérativement, le chemin qui agrandit le moins l'arbre. Probabilités conditionnelles à chaque nœud, softmax sur les co-hyponymes ; probabilité absolue = produit le long du chemin, Pr(physical object) donné par l'objectness. Les étiquettes se propagent vers le haut (une « Norfolk terrier » est aussi « dog », « mammal »). Fusion = projeter les classes de chaque jeu sur des synsets (Fig. 6, ImageNet + COCO). WordTree1k : 1000 → 1369 nœuds. Jeu combiné : COCO + top 9000 classes ImageNet + classes ImageNet-détection manquantes = 9418 classes ; COCO sur-échantillonné pour que ImageNet ne soit que 4:1 plus grand. YOLO9000 : 3 ancres au lieu de 5 pour limiter la taille de sortie.

Pas de toolflow FPGA, pas de quantification (flottants, framework Darknet ; déduit, non écrit explicitement).

## Plateforme et implémentation

GPU GeForce GTX Titan X (modèle original, pas Pascal) pour tous les temps (légende Table 3). Pas de FPGA ni de puissance (`n/r`). Code et modèles pré-entraînés publiés : http://pjreddie.com/yolo9000/ (§1).

## Résultats

- VOC 2007 : 76,8 mAP à 67 FPS ; 78,6 mAP à 40 FPS (Abstract, §2). À 288×288 : plus de 90 FPS, mAP « presque aussi bon » que Fast R-CNN (§2). Chaque entrée est le même modèle évalué à une taille différente (légende Table 3).
- Ancres (Table 1, VOC 2007, IOU moyen aux priors non modifiés) : k-means SSE k=5 : 58,7 ; k-means 1−IOU k=5 : 61,0 ; ancres manuelles (Faster R-CNN, 9) : 60,9 ; k-means 1−IOU k=9 : 67,2. Soit 5 clusters ≈ 9 ancres manuelles, et k=9 nettement mieux (§2). L'IOU moyen est calculé sur les boîtes de VOC 2007 ; choix de k par plateau de la courbe Fig. 2 (valeurs n/r).
- Ancres vs sans ancres : 69,5 mAP, rappel 81 % (sans) contre 69,2 mAP, rappel 88 % (avec), 98 boîtes → plus d'un millier (§2).
- Trajectoire Table 2 (mAP VOC 2007) : 63,4 (YOLO) → … → 69,5 → 69,2 → 74,4 → 75,4 → 76,8 → 78,6. La ligne extraite est lisible mais l'association colonne-ligne aux étapes (batch norm, hi-res classifier, multi-échelle…) n'est pas fiable ; seuls les gains cités dans le texte sont utilisés (batch norm >2 %, classifieur 448 ~4 %, clusters+position ~5 %, passthrough ~1 %). Le gain du multi-échelle seul n'est pas isolé dans le texte : n/r.
- VOC 2012 : 73,4 mAP pour YOLOv2 544 (§2, ligne YOLOv2 544 recopiée dans le fulltext, Table 4 sans corps).
- COCO : 44,0 mAP à IOU 0,5 (§2, Table 5 non extraite) ; comparable à SSD et Faster R-CNN.
- Darknet-19 ImageNet : 72,9 / 91,2 % top-1/top-5 à 224 ; 76,5 / 93,3 % à 448 (§3). WordTree1k : 71,9 / 90,4 % (§4).
- YOLO9000 : 19,7 mAP sur ImageNet détection (val), 16,0 mAP sur les 156 classes sans boîte (seules 44 classes sur 200 communes avec COCO) (§4). Bon sur les animaux (renard 52,1, tigre 61,0, armadillo 61,7 ; Table 7), nul sur vêtements et équipement (lunettes de soleil, maillot de bain : 0,0), car COCO n'a de boîtes que pour « person » (§4).
- Lignes ajoutées dans `benchmarks.csv` (proposées à l'agent principal, 9 lignes, `.cache/bench/`) : VOC 2007 76,8 ; VOC 2007 78,6 ; VOC 2012 73,4 ; COCO 44,0 ; Darknet-19 224 (72,9) ; Darknet-19 448 (76,5) ; WordTree1k (71,9) ; YOLO9000 19,7 ; YOLO9000 16,0.

## Limites et critique

- Ancres : IOU moyen mesuré sur les boîtes d'entraînement/VOC 2007 (le texte ne précise pas si train ou test) ; l'IOU moyen n'est pas la mAP, et le gain de k=9 n'est pas chiffré en mAP. Choix de k fait « à l'œil » sur une courbe (Fig. 2 non extraite), sans critère formel. Pas d'étude sur des jeux à objets très petits ou très déséquilibrés.
- Multi-échelle et haute résolution : gains donnés sans barre d'erreur ni répétition ; l'ablation en cascade (Table 2) mélange l'ordre des ajouts, donc les gains dépendent de l'ordre.
- Traitement des images sans boîtes : l'hypothèse « recouvrement ≥ 0,3 IOU avec le vrai objet » est heuristique, non validée ; les auteurs le reconnaissent en annonçant de « meilleures stratégies d'appariement » (§5). Les classes sans analogue visuel dans COCO échouent (vêtements, équipement ; Table 7) : l'objectness ne généralise pas hors des catégories vues avec boîtes. Les 16,0 mAP sont mesurés sur ImageNet-détection, pas sur COCO.
- Les augmentations de détection ne sont pas détaillées (paramètres n/r) ; pas de Mosaic, MixUp, etc. (postérieurs).
- Tous les FPS sont sur un GPU de bureau ; aucune puissance. Corps de Table 1 (extrait), 3, 4, 6 absents sauf Table 1 : FPS des baselines non vérifiables. Comparaisons avec des baselines de 2015-2016 et des jeux d'entraînement différents (07+12, 07++12).

## Pertinence pour ce thème

- **Ancres (CONSTRUIRE / PRÉTRAITER).** Pour un nouveau jeu, recalculer les ancres par k-means avec la distance 1−IOU sur les boîtes du jeu d'entraînement (dimensions dans l'espace de l'entrée), plutôt que reprendre les ancres COCO. 5 clusters donnent un IOU moyen (61,0) proche de 9 ancres manuelles (60,9) ; 9 clusters, 67,2 (Table 1). Cas d'usage : domaine aux formes de boîtes différentes de COCO (objets longs, vue aérienne). Corollaire : les boîtes dépendent de la résolution d'entrée choisie, donc recalculer après tout changement de taille.
- **Multi-échelle (AUGMENTER).** Tirer une taille d'entrée parmi {320…608} tous les 10 batches fait office d'augmentation d'échelle et rend le modèle utilisable à plusieurs résolutions ; utile si la résolution de déploiement ou la taille des objets varie, ou pour un compromis vitesse/précision en embarqué. À ne pas confondre avec le tiling.
- **Résolution du préentraînement (PRÉTRAITER).** Faire le fine-tuning du classifieur à la résolution d'inférence avant la détection (~+4 % mAP) : choisir la résolution d'entraînement du backbone comme celle des images du jeu.
- **Peu de boîtes, beaucoup d'étiquettes de classe (ANNOTER / CONSTRUIRE).** Mélanger des images avec boîtes et des images avec seulement une étiquette de classe permet d'élargir le vocabulaire sans payer l'annotation de boîtes ; la hiérarchie WordTree fusionne des taxonomies de granularité différente (« dog » vs races). À appliquer quand on fusionne des jeux aux taxonomies différentes ou quand des classes n'ont que des étiquettes d'image. Limite : la localisation vient du seul jeu avec boîtes, donc les classes sans analogue visuel restent mal détectées (0,0 AP sur vêtements). Équilibrer les jeux par sur-échantillonnage (4:1) est une règle de composition de lots réutilisable.
- Lien avec les autres papiers de la base : référence historique de l'ancrage, à confronter aux méthodes d'assignation et sans ancres.

## Gaps identifiés

- Aucune comparaison chiffrée de la mAP selon k ni de l'effet de recalculer les ancres sur un jeu non COCO (seulement l'IOU moyen, sur VOC 2007).
- Gain isolé du multi-échelle n/r ; pas d'étude de sensibilité de l'ensemble de tailles.
- Traitement des images sans boîtes validé seulement par l'hypothèse 0,3 IOU, sans comparaison à une alternative.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier ; backend `grobid`, `ok`). Corps de Table 3, 4, 6 absents ; Table 5 et Figure 2 (courbe de l'IOU selon k) non extraites ; colonnes de Table 2 mal reconstruites. Déduit et non affirmé par les auteurs : absence de quantification (poids flottants) ; lecture des gains d'ablation seulement via le texte ; association des deux points VOC 2007 à des tailles d'entrée précises (n/r). Fiche réévaluée pour la base yolo-data (bandeau d'import retiré ; `imported_from` conservé dans `metadata.json`).
