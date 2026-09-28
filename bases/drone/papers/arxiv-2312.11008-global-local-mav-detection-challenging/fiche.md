---
id: arxiv-2312.11008-global-local-mav-detection-challenging
fiche: done
date: 2026-09-28
---

# Global-Local MAV Detection under Challenging Conditions based on Appearance and Motion

Hanqing Guo, Ye Zheng, Yin Zhang, Zhi Gao, Shiyu Zhao, 2023, arXiv preprint. https://arxiv.org/abs/2312.11008
Type : preprint non relu par les pairs

## Problème

Détection **air → air** d'un MAV cible par la caméra d'un MAV en vol (§I). Plus dur que le
sol → air : caméra mobile, fond complexe vu d'en haut (bâtiments, arbres), cibles minuscules
(8×8 pixels à ~100 m dans une image 1920×1080, Fig. 1), et calcul embarqué limité. Les
méthodes par apparence échouent sur petits objets ; les méthodes par mouvement supposent un
fond plan, sont coûteuses, et ne voient pas un multirotor en vol stationnaire (§I).

## Méthode

GLAD (Global-Local MAV Detector, Fig. 2) :
- **détecteur global** sur l'image entière : YOLOv5s (entrée 640×640, seuil de confiance
  haut T0 = 0,5) ; en cas d'échec, module **mouvement** (GMD) : compensation du mouvement
  propre par homographie (grille 30×20 de points suivis par Lucas-Kanade pyramidal + RANSAC),
  différence d'images à seuil adaptatif (lumière, mouvement de fond), morphologie, puis
  classifieur par mouvement (variances d'angle et de vitesse des vecteurs) et petit CNN
  32×32 MAV / fouillis (§III, §IV, Fig. 3-4, Table II) ;
- **détecteur local** dans une région de recherche 300×300 autour de la cible, élargie
  (L = 300 + 4·T_lost) et positionnée par un **filtre de Kalman** sur la vitesse relative ;
  YOLOv5s entraîné sur crops 320×320, seuil bas T1 = 0,1 (§III) ;
- **commutateur** global ↔ local (retour au global après ~30 images d'échec local).

Nouveau jeu **ARD-MAV** : 60 vidéos, 106 665 images 1920×1080, filmées depuis DJI Mavic 2
Pro et M300, objets de 6×3 à 136×75 pixels, taille moyenne 0,02 % de l'image (plus petite
que NPS-Drones, FL-Drones, DUT Anti-UAV, Drone-vs-Bird ; Table I). 45 vidéos en
entraînement / validation, 15 en test (§V-A).

## Plateforme et implémentation

- PC avec **NVIDIA GeForce RTX 3070** (§V-B).
- **NVIDIA Jetson Xavier NX** (« 6-core CPU and 8G of GPU memory »), YOLOv5s accéléré par
  **TensorRT** + pycuda (§V-B). Précision (FP16 / INT8) : n/r. Mode de puissance du Jetson :
  n/r. Puissance mesurée : n/r. Gamme de puissance : Jetson (~10-20 W, déduit ; non mesurée).
- Jeu de données publié : https://github.com/WestlakeIntelligentRobotics/GLAD (résumé).
  Publication du code du détecteur : non affirmée dans le texte.

## Résultats

- ARD-MAV (15 vidéos de test), GLAD : P 0,92, R 0,82, F 0,87, AP50 0,80 ; 146,5 FPS sur PC
  (Table IV). Détail par condition : AP 0,91 (ordinaire), 0,81 (fond complexe), 0,58
  (petits MAV < 100 pixels) (Table III).
- Comparaison ARD-MAV (Table IV) : YOLOv5s à 640 : R 0,20, AP 0,56 (149,3 FPS) ; YOLOv5s à
  1536 : AP 0,61 (88,5 FPS) ; TPH-YOLOv5l à 1536 : AP 0,73, **12,8 FPS** ; Dogfight 0,22
  (1,0 FPS) ; MEGA 0,31 (3,5 FPS).
- NPS-Drones : AP 0,89, F 0,93, à égalité d'AP avec Dogfight (Table V ; chiffres des
  concurrents repris de [21]).
- Drone-vs-Bird : AP 0,701 contre 0,667 (DETR) (Table VI ; concurrents repris de [12]).
- Ablation (§V-E, Table VII non extraite) : la région locale fait passer le rappel du
  module apparence de 0,17 à 0,51.
- **Jetson Xavier NX** (Table VIII) : YOLOv5s TensorRT 28,5 FPS ; GMD 5,1 FPS ; LMD 10,6 FPS ;
  **moyenne 23,6 FPS** sur les vidéos de test (PC : 146,5).

→ reportés dans `benchmarks.csv` : 4 lignes (GLAD ARD-MAV sur RTX 3070, Table IV ; GLAD
ARD-MAV sur Jetson Xavier NX, Table VIII, précision n/r ; GLAD NPS-Drones, Table V ; GLAD
Drone-vs-Bird, Table VI).

## Limites et critique

- **« Near real-time » = moyenne** : 23,6 FPS en moyenne sur Jetson, mais 5,1 FPS dès que le
  module mouvement global est appelé, c'est-à-dire précisément dans les cas difficiles
  (Table VIII). La latence pire cas, critique pour un intercepteur, n'est pas donnée.
- **Incohérence texte / tableau** : §V-F donne GMD 10,6 FPS et LMD 5,1 FPS sur Jetson, la
  Table VIII l'inverse.
- **Précision sur Jetson non mesurée** : l'AP est donnée sur PC ; l'effet de TensorRT
  (précision numérique non dite) n'est pas évalué.
- **Aucune puissance, aucun vol en boucle fermée** : l'expérience Jetson est un rejeu des
  vidéos, pas un déploiement à bord.
- **Comparaisons** : sur ARD-MAV, les concurrents sont ré-entraînés par les auteurs ; sur
  NPS-Drones et Drone-vs-Bird, leurs chiffres sont repris de [21] et [12] (protocoles
  potentiellement différents). Un seul MAV par vidéo : pas de multi-cible.
- Nombreux seuils empiriques (T0-T5, D1, Table II) réglés sur ARD-MAV : risque de
  sur-ajustement au jeu des auteurs.

## Pertinence pour la thèse

Forte. C'est un des rares travaux **air → air** avec un **chiffre embarqué** (Jetson Xavier
NX) et un jeu de données public de très petites cibles :
- ARD-MAV est un banc pertinent pour un détecteur embarqué d'intercepteur (taille moyenne
  0,02 % de l'image) ;
- l'idée global → local (crop à pleine résolution autour de la cible suivie) contourne la
  perte de résolution du sous-échantillonnage à 640, sans tête P2 coûteuse : piste de
  co-design directement transposable sur FPGA (petit YOLO sur crop 320×320) (déduit) ;
- montre que la partie non-DNN (homographie, Lucas-Kanade, morphologie) devient le goulot
  sur Jetson (5,1 FPS), ce qui plaide pour son accélération matérielle (déduit).
Même équipe (Westlake, S. Zhao) que 2021-zheng-air-air-visual-detection-micro et
2023-zheng-detection-localization-tracking-multiple-mavs.

## Gaps identifiés

- Latence pire cas et puissance d'un pipeline air → air hybride (DNN + mouvement) sur cible
  embarquée : non mesurées.
- Accélération matérielle (FPGA) de la compensation de mouvement / différence d'images pour
  la détection de MAV : absente.
- Évaluation de la précision après déploiement (TensorRT, quantification) sur petits MAV :
  absente.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). Manquent : la
**Table VII** (ablation, non extraite ; seuls les chiffres cités dans le texte sont lus) et
une partie de la description des jeux NPS-Drones et Drone-vs-Bird (§V-A tronquée). Les
Tables VI et VIII, signalées « sans corps », sont en fait lisibles dans « Figures et
tableaux ». La colonne FPS de GLAD dans la Table IV est fusionnée avec l'AP (« 0.80 146.5 »),
lue comme AP 0,80 et 146,5 FPS, recoupé par la Table VIII.

Ce qui suit est déduit et non affirmé par les auteurs :
- la gamme de puissance du Jetson Xavier NX ;
- la transposabilité de l'approche global → local sur FPGA ;
- le goulot des modules non-DNN et l'intérêt de leur accélération.
