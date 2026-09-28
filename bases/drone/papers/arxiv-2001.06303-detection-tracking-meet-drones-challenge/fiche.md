---
id: arxiv-2001.06303-detection-tracking-meet-drones-challenge
fiche: done
date: 2026-09-28
benchmarks: none
---

# Detection and Tracking Meet Drones Challenge

Pengfei Zhu, Longyin Wen, Dawei Du, Xiao Bian, Heng Fan, Qinghua Hu, Haibin Ling, 2020, arXiv preprint. https://arxiv.org/abs/2001.06303
Type : preprint non relu par les pairs (version arXiv v3 du 4 oct. 2021 ; une version publiée
en revue existe probablement, IEEE TPAMI, mais elle n'est pas mentionnée dans le texte : à vérifier)

## Problème

Les détecteurs et trackers génériques sont sous-optimaux sur les images de drone, à cause des
variations de point de vue, d'échelle et du flou de bougé (§1). Les auteurs attribuent le
retard du domaine au manque de jeux de données drone publics, volumineux et annotés à la main
(§1, §2.3). Ils résument les trois éditions du challenge VisDrone (ECCV 2018, ICCV 2019,
ECCV 2020, plus de 100 équipes) et analysent les méthodes soumises (Abstract, §1).

## Méthode

Papier dataset + synthèse de challenge, sans méthode propre.
- **Jeu VisDrone** : 263 clips vidéo (179 264 images) et 10 209 images fixes, plus de
  2,5 millions de boîtes annotées sur 10 catégories (piéton, personne, voiture, van, bus,
  camion, moto, vélo, tricycle à auvent, tricycle), prises dans 14 villes chinoises (§1,
  Fig. 1). Caméras : DJI Mavic et Phantom (3 à 4P). Résolution max 3840 × 2160 en vidéo,
  2000 × 1500 en image (texte sous Fig. 1). Attributs d'occlusion et de troncature (§4.1).
  Plus de 6 000 heures d'annotation (§8).
- **Quatre tâches** : DET (image), VID (vidéo), SOT (suivi mono-objet), MOT (multi-objets)
  (§1).
  - DET : 6 471 / 548 / 1 580 / 1 610 images (train / val / test-challenge / test-dev)
    (§4.1).
  - VID et MOT : 96 clips, 5 catégories (§5.1, §7).
  - SOT : 167 séquences (139 276 images), plus 25 séquences longues ajoutées en 2019
    (§6.1).
- **Protocoles** : AP COCO (AP@[.5:.95], AP50, AP75, AR1 à AR500) pour DET et VID (§4.2) ;
  succès et précision à 20 px (OTB) pour SOT (§6.2) ; mAP de tracklets sur trois seuils
  d'IoU et CLEAR-MOT (MOTA, IDF1…) pour MOT (§7.1). Vérité terrain du test cachée,
  évaluation par serveur (§3).
- **Revue** des familles de méthodes soumises : anchor-based / anchor-free, cascade,
  ensembles, agrégation temporelle, trackers Siamese / DiMP, tracking-by-detection (§4.3,
  §5.2, §6.3, §7.2).

## Plateforme et implémentation

Aucune plateforme embarquée. Les seules indications matérielles concernent la VID :
« most of the aforementioned methods are computationally expensive for practical
applications, i.e., the running speeds are less than 10 fps on a workstation with one GTX
1080Ti GPU » (§5.3). Pour les autres tâches, vitesse, puissance et plateforme : n/r.
Données et résultats publiés : https://github.com/VisDrone/VisDrone-Dataset (Abstract) et
http://www.aiskyeye.com/ (§3).

## Résultats

Meilleurs résultats du test-challenge par tâche (chiffres des équipes participantes) :

| Tâche | Édition | Meilleure méthode | Score | Source |
|---|---|---|---|---|
| DET | 2018 | HAL-Retina-Net | AP 31,88 | Table 2 |
| DET | 2019 | DPNet-ensemble | AP 29,62 | Table 2 |
| DET | 2020 | DroneEye2020 (Cascade R-CNN + DetectoRS) | AP 34,57 ; AP50 58,21 | Table 2 |
| VID | 2018 | CFE-SSDv2 | AP 21,57 | Table 3 |
| VID | 2019 | DBAI-Det (Cascade R-CNN) | AP 29,22 | Table 3 |
| SOT | 2020 | LTNMI | succès 76,5 / précision 92,3 (test-challenge 2018) | §6.4 |
| SOT | 2020 | SMILEv2 | succès 55,5 / précision 91,9 (test-challenge 2019, long terme) | §6.4 |
| MOT | 2020 | COFE | AP 61,88 | Table 4 |
| MOT (avec détections) | 2018 | TrackCG | MOTA 42,6 ; IDF1 58,0 | Table 5 |

Baselines évalués par les auteurs sur le test-dev DET (Table 2) : CornerNet 23,43 AP,
Light-RCNN 22,08, FPN 22,06, Cascade R-CNN 21,80, DetNet 20,07, RefineDet 19,89, RetinaNet
18,94. En VID test-dev, FGFA 14,44 AP et D&T 14,21 AP, devant les détecteurs image (Table 3).
Les petites catégories restent faibles : le meilleur détecteur 2020 reste sous 25 % de mAP
sur person et bicycle (§4.5), et toutes les méthodes VID restent sous 15 % sur ces deux
classes (§5.4).

→ reportés dans `benchmarks.csv` : aucune ligne. Les résultats du test-challenge sont ceux
d'équipes tierces. Les baselines test-dev évalués par les auteurs n'ont ni plateforme, ni
vitesse, ni puissance : on n'aurait que des lignes de précision seule sur GPU non précisé.
Les chiffres de référence sont gardés dans le tableau ci-dessus.

## Limites et critique

- **Aucune métrique d'efficacité.** Les auteurs le reconnaissent : « all submissions focus
  more on accuracy than efficiency » (§8). Les méthodes gagnantes sont des ensembles, des
  Cascade R-CNN et du test multi-échelle, inutilisables à bord. Les seules vitesses citées
  sont inférieures à 10 FPS sur une GTX 1080Ti de bureau (§5.3).
- **Protocole AP COCO** (moyenne sur IoU 0,5:0,95). Il n'est pas comparable aux mAP@0.5
  souvent rapportés par les papiers YOLO sur VisDrone, ni à l'IoU mono-objet de DAC-SDC.
  Pas d'AP_small séparé dans les tableaux, malgré l'accent mis sur les petits objets.
- **Tables extraites imparfaitement** : les colonnes AR des Tables 2 et 3 sont décalées
  dans l'extraction (en-têtes et valeurs mélangés). Seules les colonnes AP et AP50 ont été
  reprises ici.
- **Évolution des splits** : le test-challenge SOT change entre 2018 et 2019 (25 séquences
  longues ajoutées, §6.1), donc les scores ne sont pas comparables d'une édition à l'autre
  sur ce set.
- **Biais de domaine** (déduit) : images prises par des drones grand public DJI, en Chine
  seulement, sur des scènes urbaines et routières. Pas de contre-drone ni d'air → air.

## Pertinence pour la thèse

- **Référence obligatoire pour VisDrone**, le benchmark de base de l'axe `drone-detection`.
  Le papier fixe les splits, les 10 classes, les attributs d'occlusion et le protocole AP
  COCO. À citer pour toute évaluation, en précisant test-dev contre test-challenge.
- **Justifie le problème des petits objets** : plafond de 35 % d'AP en 2020, et échec sur
  person et bicycle (§4.5). Les directions suggérées vont dans le même sens : ancres
  anchor-free, contexte, fusion détection et suivi (§8).
- **Le §8 formule explicitement le gap de la thèse** : « the computation resources are
  limited on drone platform, making it impossible to deploy a large model on such edge
  devices », avec une recommandation de NAS sous contrainte matérielle. Rien n'est mesuré.
- Les axes SOT et MOT fournissent des métriques (succès/précision, MOTA, IDF1) pour l'axe
  `tracking-navigation`, là encore sans contrainte embarquée.

## Gaps identifiés

- **VisDrone sans métrique d'efficacité** : aucun FPS, aucune puissance, aucune plateforme
  embarquée dans le challenge de 2018 à 2020. Les auteurs l'annoncent pour les éditions
  suivantes (§8). À vérifier dans les éditions 2021 et après.
- **Pas d'AP_small dans les résultats publiés** : l'effet des optimisations embarquées
  (quantification, réduction de résolution) sur les petites classes reste à mesurer. Cela
  rejoint l'hypothèse « quantification contre mAP_small » de `gaps.md`.
- **Fusion détection et suivi pour petits objets** : proposée comme direction (§8), jamais
  évaluée sous contrainte de calcul embarqué.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). Tables 1 à 5 présentes
dans l'extraction, mais les Tables 2 et 3 ont des colonnes AR décalées. La Fig. 6 (nuages
succès/précision SOT) n'est connue que par le texte du §6.4.

Ce qui suit est déduit et non affirmé par les auteurs :
- la publication probable dans IEEE TPAMI (non mentionnée dans le texte) ;
- l'incompatibilité des méthodes gagnantes avec un déploiement à bord ;
- le biais de domaine (Chine, drones DJI, scènes urbaines) ;
- la non-comparabilité avec les mAP@0.5 des papiers YOLO.
