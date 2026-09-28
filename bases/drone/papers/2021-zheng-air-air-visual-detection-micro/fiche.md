---
id: 2021-zheng-air-air-visual-detection-micro
fiche: done
date: 2026-09-28
---

# Air-to-Air Visual Detection of Micro-UAVs: An Experimental Evaluation of Deep Learning

Ye Zheng, Zhang Chen, Dailin Lv, Zhixing Li, Zhenzhong Lan, Shiyu Zhao, 2021, IEEE Robotics and Automation Letters 6(2), 1020-1027. https://doi.org/10.1109/LRA.2021.3056059
Type : article de journal

## Problème

Détection visuelle **air → air** de micro-drones par caméra monoculaire embarquée, pour
l'essaimage par vision, la défense contre les drones malveillants et le see-and-avoid
(§I). Les auteurs opposent explicitement ce cas au **sol → air** (caméra fixe, fond de
ciel) : en air → air, le fond peut être urbain ou naturel, le point de vue varie et la
cible peut faire moins de 10×10 pixels (§I). Aucune évaluation systématique des détecteurs
profonds n'existait pour ce cas, faute de jeu de données complet (§I, §II-C).

## Méthode

Deux contributions :
1. **Det-Fly** : 13 271 images 3840×2160 d'un DJI Mavic filmé par un DJI M210 (caméra
   XT2), annotées à la main ; distance relative 10-100 m, altitude 20-110 m ; fonds ciel,
   urbain, champ, montagne (20-30 % chacun) ; vues de face 36,4 %, de dessus 32,5 %, de
   dessous 31,1 % ; lumière forte/faible 10,8 %, flou de bouge 11,2 %, occlusion 0,8 %
   (§III, Fig. 1-3). Une seule cible, un seul modèle de drone par image. Public :
   https://github.com/Jake-WU/Det-Fly.
2. **Évaluation de 8 détecteurs** : SSD512, RetinaNet, YOLOv3 (DarkNet-53), RefineDet,
   Faster R-CNN, FPN, Cascade R-CNN, Grid R-CNN, backbone ResNet-50 sauf YOLOv3 ; split
   70 % entraînement (dont 10 % validation) / 30 % test (§IV). Analyse par fond, échelle,
   angle de vue et conditions difficiles (§V-C), et comparaison sur MIDGARD (§V-D).

Pas de nouveau détecteur, pas de quantification.

## Plateforme et implémentation

- Entraînement **et** temps d'inférence sur PC : Intel i7, 32 GB, **NVIDIA RTX 2080Ti**,
  « rather than an embedded computer in order to reduce training time » (§IV). Aucune
  mesure embarquée ; puissance n/r ; batch et résolution d'inférence n/r (Table I non
  extraite).
- Données publiques (lien ci-dessus) ; code d'entraînement : non mentionné.

## Résultats

AP sur Det-Fly (Table II, valeurs lues dans le texte §V-A) et temps d'inférence RTX 2080Ti
(Fig. 4, valeurs lues dans le texte §V-B) :

| Détecteur | Type | AP (%) | Temps (ms) |
|---|---|---|---|
| Grid R-CNN | 2 étages | 82,4 | 157 |
| Cascade R-CNN | 2 étages | 79,4 | n/r |
| SSD512 (ResNet-50) | 1 étage | 78,7 | 84 |
| FPN | 2 étages | « same AP » que SSD512 | n/r |
| RetinaNet | 1 étage | 77,9 | n/r |
| YOLOv3 (DarkNet-53) | 1 étage | 72,3 | 32 |
| Faster R-CNN | 2 étages | 70,5 | n/r |
| RefineDet | 1 étage | 69,5 | n/r |
| SSD512 (MobileNetV2) | 1 étage | 68,8 | 53 |

- Det-Fly-Simple / Det-Fly-Complex : ~5 points de baisse moyenne sur le jeu complexe,
  « mean Precision » 74,4 %, seul Grid R-CNN dépasse 80 % (§V-A).
- Par fond (mAP des 8 détecteurs) : ciel 88,3 %, urbain 62,0 % (§V-C1, Table III). Par
  angle : ~0,78 (dessus), ~0,72 (face), ~0,85 (dessous) (Fig. 6). L'AP croît avec la
  taille de cible pour tous (Fig. 5, valeurs n/r). L'occlusion partielle fait chuter l'AP ;
  lumière et flou peu (§V-C4, Table IV).
- Sur MIDGARD, les résultats sont ~10 % meilleurs que sur Det-Fly (§V-D, Table V).

→ reportés dans `benchmarks.csv` : 8 lignes — les 8 configurations dont l'AP est donnée
dans le texte (Grid R-CNN, Cascade R-CNN, SSD512-ResNet-50, RetinaNet, YOLOv3,
Faster R-CNN, RefineDet, SSD512-MobileNetV2), RTX 2080Ti, `confidence: medium` (Tables et
Fig. 4 non extraites). FPN omis (AP seulement « same as » SSD512).

## Limites et critique

- **Pas d'embarqué** : tous les temps viennent d'une RTX 2080Ti ; YOLOv3 à 32 ms sur GPU
  de bureau n'est pas temps réel sur un calculateur de drone (déduit). Le choix de
  ResNet-50 est motivé par l'embarqué (§IV) sans aucune mesure pour l'étayer.
- **Seuil d'IoU « set to 0 »** (§IV) : vraisemblablement une valeur tronquée à
  l'extraction (0,5 ?) ; tel qu'extrait, le protocole AP est ambigu. À vérifier dans le PDF
  par l'utilisateur.
- **Un seul drone cible (DJI Mavic)** et un seul drone porteur : généralisation à d'autres
  cibles non testée, reconnue par les auteurs (§III, §VI).
- **Images fixes échantillonnées à 5 FPS** ou prises à des poses choisies : pas de
  séquence vidéo continue, donc pas d'évaluation du suivi ni de l'information de
  mouvement.
- **Définition « petit objet » large** (< 10 % de la hauteur et largeur de l'image, §III) :
  bien au-dessus des cibles de quelques pixels des autres travaux anti-UAV.
- Détecteurs de 2018-2019 uniquement ; hyperparamètres « finely tuned » par détecteur, sans
  détail extrait (Table I).

## Pertinence pour la thèse

- **Référence centrale de l'axe `counter-uav` air → air** : l'un des rares jeux publics
  acquis réellement drone → drone, avec la distinction sol → air / air → air posée
  explicitement (§I) — exactement le critère du profil de la base.
- Montre l'écart de difficulté selon le fond (ciel 88,3 % contre urbain 62,0 %) et l'angle
  de vue : utile pour définir un protocole d'évaluation d'un détecteur embarqué.
- Laisse ouvert l'essentiel pour la thèse : **aucun détecteur n'est porté à bord** ; pas
  de mesure de latence, puissance, ni de YOLO récent ou quantifié.

## Gaps identifiés

- **Détection air → air réellement embarquée** : ce benchmark de référence n'évalue que
  sur GPU de bureau ; le portage FPGA / Jetson / MCU sur Det-Fly (FPS, W, AP) est un gap
  direct.
- **Résolution 4K contre entrée réseau réduite** : les auteurs citent le traitement
  d'images haute résolution comme perspective (§VI) ; lien avec les stratégies de tuilage
  ou de ROI sur accélérateur.
- **Généralisation multi-drones** : un seul modèle de cible.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). **Tables I à V sans
corps extrait** : hyperparamètres, AP détaillées par fond, conditions difficiles et
MIDGARD non lues ; seules les valeurs reprises dans le texte sont connues. Fig. 4 et Fig. 5
(temps et AP par échelle) non chiffrées dans le texte, sauf Grid R-CNN, SSD512 et YOLOv3.
L'Abstract est intégré dans l'introduction par l'extraction.

Ce qui suit est déduit et non affirmé par les auteurs :
- l'hypothèse d'un seuil d'IoU tronqué à l'extraction ;
- l'absence de temps réel de YOLOv3 sur calculateur embarqué ;
- l'identité de la plateforme des temps d'inférence (la RTX 2080Ti est la seule décrite).
