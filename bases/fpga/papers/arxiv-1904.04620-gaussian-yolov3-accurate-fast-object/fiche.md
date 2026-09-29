---
id: arxiv-1904.04620-gaussian-yolov3-accurate-fast-object
fiche: done
date: 2026-09-29
benchmarks: none
---

# Gaussian YOLOv3: An Accurate and Fast Object Detector Using Localization Uncertainty for Autonomous Driving

Jiwoong Choi, Dayoung Chun, Hyun Kim, Hyuk-Jae Lee, 2019, arXiv preprint. https://arxiv.org/abs/1904.04620
Type : preprint non relu par les pairs

## Problème

Les détecteurs one-stage (YOLOv3) sortent des coordonnées de boîte déterministes, sans indication de leur fiabilité ; les faux positifs par mauvaise localisation sont jugés dangereux en conduite autonome (freinages intempestifs, accidents), et les détecteurs plus précis ne tiennent pas le temps réel (> 30 fps) à 512x512 ou plus (§1). L'article ne traite pas de FPGA : la cible est un GPU de bureau.

## Méthode

- Chaque coordonnée de boîte (tx, ty, tw, th) est modélisée par une gaussienne unique (moyenne et variance, Eq. 1-4) : la couche de détection de YOLOv3 sort 8 valeurs au lieu de 4 (§3.1).
- Perte de boîte remplacée par une log-vraisemblance négative (NLL, Eq. 5-9) avec pondération par taille d'objet, qui donne une atténuation de perte sur les données bruitées (§3.2).
- Critère de détection : objectness x score de classe x (1 - incertitude de localisation moyenne) (Eq. 10) : les boîtes très incertaines sont filtrées (§3.3).
- Surcoût : 99 GFLOPs contre 99,04 GFLOPs (+0,04 %) à 512x512, 10 classes (§3.1).

## Plateforme et implémentation

Aucune plateforme embarquée : NVIDIA GTX 1080 Ti, CUDA 8.0, cuDNN v7 (§4). Fréquence, puissance, ressources : sans objet / n/r. Code : non mentionné dans le texte.

## Résultats

- KITTI (validation, IoU 0,7 voiture, 0,5 piéton et cycliste) : mAP 83,61 pour Gaussian YOLOv3 (512x512, 43,13 fps) contre 80,52 pour YOLOv3 (43,57 fps), soit +3,09 ; à 704x704 : 86,79 mAP à 24,91 fps, contre 85,42 mAP / 23,98 fps pour SINet (Table 2).
- BDD (test, IoU 0,75) : mAP 18,4 à 42,5 fps contre 14,9 à 42,9 fps pour YOLOv3, soit +3,5 ; 736x736 : 20,8 mAP à 22,5 fps contre 19,1 mAP / 21,0 fps pour CFENet (Table 3, en-têtes de colonnes perdus à l'extraction).
- COCO : AP 36,1, soit +3,1 sur YOLOv3, AP75 39,0 (+4,6) ; chiffres dans le texte seulement (§4.2).
- KITTI : faux positifs 1 681 à 985 (-41,40 %), vrais positifs 13 575 à 14 560 (+7,26 %) ; BDD : FP 86 380 à 51 296 (-40,62 %), TP 57 261 à 59 724 (+4,30 %) (Table 4, seuil de détection 0,5).
- Corrélation entre IoU et incertitude de localisation : l'IoU croît quand l'incertitude baisse (Fig. 3, voitures).
→ reportés dans `benchmarks.csv` : aucune ligne. Mesures uniquement sur GPU de bureau, sans plateforme FPGA ni embarquée (exclu du périmètre des benchmarks de la base).

## Limites et critique

- Uniquement GPU de bureau (fps sur GTX 1080 Ti) ; aucun transfert à un FPGA ou quantification étudiés. Le gain de +0,04 % de FLOPs est en outre mesuré sur le seul réseau, pas de mesure de latence embarquée.
- Baselines réentraînées avec les réglages par défaut de chaque code officiel, sans garantie d'équité de réglage ; CFENet provient du classement KITTI (sans fps, cellule illisible dans Table 2).
- L'incertitude modélisée est de l'incertitude aléatoire (bruit de données, Kendall) sur la localisation, seule : pas d'incertitude épistémique, ni de calibration mesurée (pas d'ECE), ni évaluation hors distribution. La relation IoU-incertitude est un graphe moyen sur la classe voiture (Fig. 3).
- Les gains de FP/TP sont mesurés à un seul seuil (0,5) ; les revendications de sécurité (« prévenir des accidents mortels ») ne sont pas démontrées.
- Domaine conduite autonome (KITTI, BDD) ; pas de personnes en secteur industriel.
- Preprint non relu par les pairs ; aucune publication de code dans le texte.

## Pertinence pour la thèse

Pertinence indirecte mais réelle pour l'axe sûreté : c'est un exemple léger et bon marché (+0,04 % de FLOPs) de détecteur YOLO fournissant un score de fiabilité de boîte, exploitable comme signal de surveillance à l'exécution (moniteur, rejet de détections incertaines) pour le cas d'application YOLO en vidéosurveillance de personnes. La classe pedestrian de KITTI et BDD offre un point de comparaison, mais hors contexte industriel. Reste ouvert : portage FPGA de la tête à 8 sorties (calcul de sigmoïde et de critère), calibration de l'incertitude et lien avec une argumentation d'assurance (IEC 61508, ISO/IEC TR 5469).

## Gaps identifiés

- Estimation d'incertitude (localisation, classification) dans un détecteur YOLO déployé sur FPGA : coût matériel, quantification de la tête gaussienne.
- Calibration et validation de l'incertitude comme moniteur d'exécution en contexte certifiable.

## Statut de lecture

Papier complet (texte extrait lu en entier). Table 3 : en-têtes de colonnes manquants à l'extraction (la légende est mélangée avec celle de la Table 4) ; les valeurs mAP / fps ont été lues dans le texte du §4.2 et recoupées. Déduit et non affirmé par les auteurs : l'usage comme moniteur d'exécution, l'absence de calibration, la limite du seuil unique, la pertinence pour la thèse.
