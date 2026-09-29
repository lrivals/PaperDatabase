---
id: arxiv-2304.06052-confident-object-detection-conformal-prediction
fiche: done
date: 2026-09-29
benchmarks: none
---

# Confident Object Detection via Conformal Prediction and Conformal Risk Control: an Application to Railway Signaling

Léo Andéol, Thomas Fel, Florence De Grancey, Luca Mossina, 2023, arXiv preprint. https://arxiv.org/abs/2304.06052
Type : preprint non relu par les pairs

## Problème

Fournir une quantification d'incertitude (UQ) avec garanties formelles pour la sortie d'un détecteur d'objets utilisé dans un système critique et à terme certifié (§1). Cas d'usage : détection de feux de signalisation ferroviaires (Railway Traffic Light Detection / Localization) pour assister un conducteur de train sur lignes secondaires (§1.1). L'objectif est de garantir que la boîte englobante vraie est contenue dans l'ensemble prédit avec probabilité 1-alpha (Eq. 1).

## Méthode

Prédiction conforme (Split CP) et Conformal Risk Control (CRC), sans réentraînement, indépendants du modèle (§3.2-3.3) :
- Box-wise (§4.1) : appariement prédiction / vérité terrain par seuil d'IoU (garantie valable seulement pour les vrais positifs), marge additive (pixels) ou multiplicative (proportion de la largeur/hauteur), avec correction de Bonferroni (alpha/4 par coordonnée) ou nouveaux scores « max-additive » et « max-multiplicative » (quantile alpha du résidu maximal, Eq. 8-9), moins conservateurs.
- Image-wise (§4.2) : méthode « Hausdorff » de de Grancey et al. 2022 (couvrir 75 % des boîtes de l'image, beta = 0,25 fixé arbitrairement) contre CRC avec perte de recall par boîte (Eq. 16) ou par pixel (Eq. 17), lambda choisi par Eq. 4 ; marge ajoutée à chaque boîte prédite (Eq. 18-19).
Détecteurs : YOLOv5m, DETR-ResNet50, DiffusionDet, pré-entraînés puis fine-tunés (YOLOv5m 100 époques, DETR 3 époques ; DiffusionDet non fine-tuné faute de réussite, §5.1.1). Nouveau jeu de données de 3 414 images 1280x720 de 41 vidéos de lignes françaises, 3 508 boîtes, annotées à la main (Table 1, §2.2).

## Plateforme et implémentation

Aucune plateforme matérielle ni FPGA : n/r. Pas de mesure de temps, de puissance, de ressources. Code, jeu de données : non publiés dans le texte lu (note de bas de page non extraite ; à vérifier). Les vidéos sources viennent d'internet « avec l'accord de l'uploader » (§2.2), ce qui pose une question de diffusion du jeu de données.

## Résultats

- Réglages : alpha = 0,1, seuil d'objectness 0,3, IoU 0,3 ; pré-entraîné : 1 914 points de calibration / 1 500 de test (1 974 boîtes de test) ; fine-tuné : 1 414 / 1 000 / 1 000 (1 022 boîtes) (§5.1).
- Box-wise, couverture empirique (Table 4) : YOLOv5m pré-entraîné 0,93 / 0,94 / 0,95 / 0,96 (max-add. / max-mult. / add. / mult.), DETR 0,99 / 0,98 / 1,00 / 0,99, DiffusionDet 0,92 / 0,92 / 0,96 / 0,96, YOLOv5m fine-tuné 0,94 / 0,92 / 0,95 / 0,93. La cible 0,9 est dépassée : les scores avec Bonferroni sur-couvrent (§5.3.1). Les scores max donnent des marges plus petites que Bonferroni (Fig. 4, §5.3.1).
- Le stretch (rapport des aires boîte conformalisée / prédite) est plus faible pour YOLOv5m, mais parce que ce modèle produit peu de boîtes (§5.3.1). Valeurs des Tables 2, 3, 5, 6 : n/r (corps non extrait).
- Image-wise : mieux calibré que box-wise (§5.3.2) ; pour les deux premières lignes des Tables 5 et 6, aucun lambda ne satisfait Eq. 4 (pas assez de boîtes prédites) : la conformalisation ne compense pas un détecteur insuffisant. Instabilité de Hausdorff (effet de seuil : une boîte lointaine fait exploser la marge, Fig. 5).
- Aucune mesure matérielle : pas de ligne dans `benchmarks.csv` (`benchmarks: none`).

## Limites et critique

- Hypothèse d'échangeabilité (i.i.d.) : à long terme, les flux de données ne la satisfont pas, les auteurs l'écrivent (§6). Garantie marginale (moyenne sur calibration/test), pas conditionnelle à une image donnée : insuffisante pour une garantie par instance en sûreté (déduit).
- Garantie box-wise seulement sur les vrais positifs ; les faux négatifs (personne non détectée) ne sont pas couverts, et les faux positifs sont ignorés (§4.1, §4.2). Or en surveillance de personnes, l'oubli de détection est le risque principal.
- Niveaux atteints (alpha = 0,1) très loin des taux exigés en sûreté ; les auteurs jugent improbable que CP seule suffise (§6).
- Petit jeu de données (3 414 images, 1,03 boîte par image en moyenne), annoté par les auteurs, mono-classe ; tirage avec fuite possible entre images voisines d'une même vidéo (intervalle de 5 s entre frames, §2.2) qui viole l'échangeabilité (déduit). Pas d'intervalles de confiance sur les métriques ; une seule taille de split. Comparaison DiffusionDet / YOLOv5m / DETR non à iso-conditions d'entraînement (DiffusionDet non fine-tuné).
- Coût de calcul non mesuré : « légère » affirmée (§1) mais pas quantifiée, aucun test sur cible embarquée.

## Pertinence pour la thèse

Direct pour la surveillance à l'exécution et la certification d'un détecteur (axe sûreté) : donne une recette post-hoc, agnostique du modèle, pour attacher à un YOLO des boîtes avec garantie de couverture, ajoutable à un YOLO déployé sur FPGA (le calcul de marge à l'inférence est une simple addition sur les coordonnées, déduit de Eq. 12-19 ; la calibration est hors ligne). Le cas ferroviaire (chaîne fonctionnelle localisation / validation / reconnaissance, Fig. 1, référence à Alecu et al. 2022) est analogue à celui de la détection de personnes en site industriel dangereux, et de Grancey et al. 2022 traitait des piétons. Reste ouvert : garantie sur les faux négatifs, échangeabilité en dérive, coût et déterminisme d'implémentation sur FPGA, lien avec les normes (IEC 61508, ISO/PAS 8800).

## Gaps identifiés

- Prédiction conforme pour détecteurs YOLO déployés sur FPGA : aucune évaluation de coût matériel ni de compatibilité avec un pipeline quantifié INT8.
- Garanties conformes sur la détection de personnes (faux négatifs, recall par image) en environnement industriel : jeu de données inexistant dans la base.
- Conformal prediction hors échangeabilité (dérive, flux vidéo) pour l'assurance en service.

## Statut de lecture

Papier complet (fulltext.md lu en entier, 348 lignes). Corps des Tables 2, 3, 5 et 6 non extraits (avertissement d'extraction) : AP, stretch et valeurs image-wise n/r ; seules les Tables 1 et 4 sont exploitables (Table 4 non signalée comme reconstruite, valeurs recoupées avec le texte de §5.3.1).
Déduit et non affirmé par les auteurs : la portée limitée de la garantie marginale pour la sûreté, la fuite possible entre frames, la transposition au FPGA et à la détection de personnes.
