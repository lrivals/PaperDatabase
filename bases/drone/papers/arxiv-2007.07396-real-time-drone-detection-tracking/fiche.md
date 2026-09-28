---
id: arxiv-2007.07396-real-time-drone-detection-tracking
fiche: done
date: 2026-09-28
---

# Real-Time Drone Detection and Tracking With Visible, Thermal and Acoustic Sensors

Fredrik Svanstrom, Cristofer Englund, Fernando Alonso-Fernandez, 2020, Proc. Intl Conf on Pattern Recognition, ICPR, Milan, Italy, 10-15 January 2021. https://arxiv.org/abs/2007.07396
Type : conférence (ICPR 2020, tenue en janvier 2021 ; version arXiv lue)

## Problème

Concevoir un système **portable de détection de drones au sol**, multi-capteurs, et
combler trois manques relevés dans la littérature : peu d'études en infrarouge thermique,
peu de fusion de capteurs, et presque aucune étude qui précise capteur, type de drone,
portée et jeu de données ; pas non plus d'étude de la performance en fonction de la
distance capteur-cible (§I, §III). Absence de jeu public multi-capteurs (§I).

## Méthode

- **Matériel** (§III-B) : caméra thermique FLIR Breach PTQ-136 (Boson 320×256, 60 FPS,
  FoV 24°×19°), caméscope visible Sony HDR-CX405 (1280×720, 50 FPS, via capture HDMI),
  caméra fish-eye 180° (1024×768, 30 FPS), micro directionnel, récepteur ADS-B (SDR) et
  GPS ; caméras IR et visible sur **tourelle pan/tilt** à servos, le tout sur un **trépied
  de géomètre** ; calcul sur un **ordinateur portable** (Intel i7-9850H + Nvidia MX150).
- **Logiciel** (§III-C) : Matlab, un script principal à 10 Hz et cinq « workers »
  parallèles asynchrones. Fish-eye : détecteur de mouvement GMM + filtre de Kalman
  multi-cibles pour pointer la tourelle. IR et visible : **YOLOv2** à 4 classes (drone,
  oiseau, avion, hélicoptère), entrée 256×256 (IR) ou 416×416 (visible). Audio : MFCC +
  **LSTM** à 3 classes (drone, hélicoptère, fond), fenêtre de 1 s rafraîchie 20 fois par
  seconde. ADS-B pour les aéronefs coopératifs.
- **Fusion** (§V-D) : combinaison pondérée des classes et confiances des capteurs, lissée
  sur ~1 s, avec un nombre minimal de capteurs requis réglable dans la GUI.
- **Jeu de données** (§IV) : 650 vidéos de 10 s (365 IR, 285 visibles), 203 328 images
  annotées, 90 clips audio ; trois aéroports suédois ; trois drones (Hubsan H107D+,
  DJI Phantom 4 Pro, DJI Flame Wheel F450) plus oiseaux, avions, hélicoptères (dont 49 clips
  YouTube) ; distance max drone 200 m ; trois classes de distance (Close / Medium /
  Distant) fixées par les critères DRI / Johnson : 15 px et 5 px de largeur dans l'image IR.
  Publié : https://github.com/DroneDetectionThesis/Drone-detection-dataset (§I, note 1).

## Plateforme et implémentation

Inférence sur **portable Dell Latitude 5401 : Intel i7-9850H + Nvidia MX150** (§III-B) ;
entraînement sur Nvidia RTX 2070 8 Go (§V-A). Matlab + Parallel Computing Toolbox. FPS de
chaque worker : affiché dans la GUI mais **non rapporté** (n/r). Latence de la boucle
tourelle : seulement « sub-second » comme exigence (§III-A), n/r mesurée. Puissance :
n/r. Jeu de données publié (lien ci-dessus) ; code : non publié dans le texte (n/r).

## Résultats

- **IR (YOLOv2)** : F1 = **0,7601** en moyenne sur les trois classes de distance ;
  **visible (YOLOv2)** : F1 = **0,7849** ; écarts IR / visible ≤ 3 % (§V-B, §VI ; détail
  par distance en Tables III-IV, non extraites). Performance en baisse avec la distance
  (§V-A).
- **Audio (MFCC + LSTM)** : F1 = **0,9323** (§VI ; Table V non extraite), contre 0,6984
  pour [28] en binaire (§V-C).
- **Fusion** (poids 1,0, au moins deux capteurs) : le système sort une classification
  « drone » dans **78 %** des occasions de détection, contre **67 %** pour la meilleure
  caméra seule (visible) (§V-D, Fig. 6). Sur 10 min sans drone, l'exigence de deux
  capteurs supprime toutes les fausses alarmes relevées (insectes, nuages) (§V-D, Fig. 7).
- Sources d'erreur : nuages éclairés par le soleil (IR), autofocus (visible) (§V-A, §V-B).

→ reportés dans `benchmarks.csv` : 3 lignes (YOLOv2 IR F1 76,01 ; YOLOv2 visible F1
78,49 ; MFCC + LSTM audio F1 93,23), plateforme portable i7 + MX150, FPS et puissance
n/r, `confidence: medium` (valeurs lues dans le texte, Tables III-V non extraites).

## Limites et critique

- **Contre-drone sol → air** : capteurs sur trépied, calcul sur portable. Hors du périmètre
  « IA embarquée » de la base (profile.md, Exclus) ; pertinent seulement comme **jeu de
  données** IR + visible et comme référence de fusion.
- **« Real-time » non chiffré** : aucun FPS, aucune latence mesurée malgré le titre.
- **Évaluation fragile** : 120 clips IR et 120 visibles, 5 par classe et par bin ; fusion
  jugée sur quelques sessions (COVID-19, vols annulés, §V-D) ; le « 78 % des occasions »
  n'a pas de définition formelle ni d'intervalle.
- **Comparaisons faibles** : le F1 de YOLOv2 dans [18] (0,728) est sur un autre jeu, une
  classe, résolution inconnue — les auteurs le signalent eux-mêmes (§V-B). Même remarque
  pour l'audio [28] (binaire).
- **Détecteur daté** (YOLOv2, 2016) et F1 à un seul seuil de confiance ; pas de mAP ni de
  courbe PR.
- **Portées modestes** : drones à 200 m max ; les classes « Distant » ne sont définies
  qu'en pixels.

## Pertinence pour la thèse

- **Axe `counter-uav`** (sol → air) et **`datasets-benchmarks`** : le jeu IR + visible
  public, avec classes de distance DRI / Johnson (15 px et 5 px), fournit une métrique de
  « portée de détection » réutilisable pour un détecteur **air → air** embarqué (déduit).
- La conclusion **IR 320×256 ≈ visible 640×512** (§V-B) est un argument pour un capteur
  thermique basse résolution à bord d'un drone intercepteur, moins coûteux en calcul
  (déduit).
- Aucun apport pour `drone-fpga`, `nano-drone`, `system-codesign`.

## Gaps identifiés

- **Performance en fonction de la distance** : bonne idée de protocole (bins DRI), jamais
  reprise ici avec un détecteur embarqué ni avec une mesure de mAP_small.
- **Fusion multi-capteurs à bord** : la fusion IR + visible + audio est faite sur portable
  au sol ; pour un drone porteur, l'audio est inutilisable (bruit des propres hélices,
  déduit) et le coût de deux détecteurs en parallèle n'est pas mesuré.
- **« Temps réel » non quantifié** dans les systèmes contre-drone sol → air.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). Les **Tables I à V
sont absentes** de l'extraction (ni légende ni corps) : résultats par classe de distance
(Tables III-IV), audio (Table V), classes de sortie (Table I) et répartition des vidéos
(Table II) non lus ; seuls les F1 moyens repris dans le texte sont cités. Figures 6-7
(analyse image par image) connues par le texte seulement.

Ce qui suit est déduit et non affirmé par les auteurs :
- l'intérêt du jeu et des bins DRI pour un détecteur air → air ;
- l'argument « IR basse résolution moins coûteux à bord » ;
- l'inutilisabilité de l'audio sur un drone porteur.
