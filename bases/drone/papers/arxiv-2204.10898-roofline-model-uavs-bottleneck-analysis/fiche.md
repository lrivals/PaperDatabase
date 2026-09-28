---
id: arxiv-2204.10898-roofline-model-uavs-bottleneck-analysis
fiche: done
date: 2026-09-28
benchmarks: none
---

# Roofline Model for UAVs: A Bottleneck Analysis Tool for Onboard Compute Characterization of Autonomous Unmanned Aerial Vehicles

Srivatsan Krishnan, Zishen Wan, Kshitij Bhardwaj, Ninad Jadhav, Aleksandra Faust, Vijay Janapa Reddi, 2022, arXiv preprint. https://arxiv.org/abs/2204.10898
Type : preprint non relu par les pairs (d'après `metadata.json` ; une version publiée en conférence est possible mais n'est pas mentionnée dans le texte)

## Problème

Le calcul embarqué des UAV est choisi ou conçu de façon « ad hoc », sur des métriques isolées
(débit crête, faible puissance), sans mesurer son effet sur la performance de la mission.
Les auteurs affirment qu'un tel choix peut dégrader la vitesse sûre d'un facteur 2,3, et
qu'un accélérateur optimisé pour la seule basse consommation peut la dégrader d'un facteur
4,3 sur un nano-UAV (§I).

## Méthode

- **Modèle F-1** (« roofline pour UAV ») : vitesse sûre V_safe en fonction du débit de
  décision f_action = min(1/T_sensor, 1/T_compute, 1/T_control) (Éq. 3), à partir de la
  relation V_safe = a_max (√(T²_action + 2d/a_max) − T_action) reprise de travaux
  antérieurs [22] (Éq. 4). Le coude (« knee-point ») sépare les régimes **sensor-bound**,
  **compute-bound** et **physics-bound** (§III-B, Fig. 4a).
- **Effet de la masse** : un TDP plus élevé implique un dissipateur plus lourd (calculateur
  de dissipateur [54]), donc une a_max plus faible et un plafond plus bas (§III-E, Fig. 4c,
  Fig. 12). La traînée n'est pas modélisée (§IV).
- **Validation en vol** : 4 quadricoptères S500 construits par les auteurs (Ras-Pi4 ou
  UpBoard, lests de 50 g et 150 g), contrôleur MAVROS maison, Vicon pour la vérité terrain ;
  arrêt avant un obstacle à 3 m, 5 essais par vitesse (§IV, Table I, Fig. 6-7).
- **Skyline** : outil web interactif (boutons capteur, TDP, latence, masse, poussée),
  https://bit.ly/skyline-tool (§V, Table II).
- **Études de cas** (§VI-VII) : choix du calculateur (Intel NCS contre NVIDIA AGX sur
  DJI Spark), choix de l'algorithme (SPA/MAVBench contre E2E TrailNet/DroNet sur AscTec
  Pelican + TX2), redondance modulaire double (2 × TX2), système complet, et accélérateurs
  dédiés (Navion, PULP-DroNet) sur un nano-UAV.

## Plateforme et implémentation

Pas d'accélérateur propre. Validation sur Raspberry Pi 4 et Intel UpBoard (Up Squared),
contrôleur de vol NXP FMUK66, batterie 3S 5 000 mAh (Table I). Les débits des calculateurs
des études de cas (TX2, AGX, NCS, Ras-Pi, Navion, PULP) proviennent de l'outil ou de la
littérature ; la méthode de mesure n'est pas décrite (n/r). Puissance : seuls des TDP
(30 W et 15 W pour l'AGX) et des valeurs publiées (Navion 2 mW, PULP 64 mW) sont cités ;
aucune mesure propre. Outil Skyline publié en ligne ; code source n/r.

## Résultats

- **Validation** : erreur du modèle sur la vitesse sûre de 9,5 %, 7,2 %, 5,1 % et 6,45 %
  pour UAV-A à UAV-D (§IV, Fig. 7b). UAV-A : 2,13 m/s prédit (§IV ; 2,2 m/s dans la
  légende de la Fig. 7) contre 1,9 m/s mesuré. Le modèle surestime toujours (§IV).
- **NCS contre AGX (DJI Spark, DroNet)** : AGX à 230 FPS contre NCS à 150 FPS, mais plafond
  plus bas pour l'AGX à cause de sa masse (280 g + 162 g de dissipateur à 30 W, contre 47 g
  pour le NCS) ; passer l'AGX de 30 W à 15 W de TDP (hypothèse à débit constant) divise le
  dissipateur par deux (81 g) et augmente la vitesse sûre de 75 % (§VI-A, Fig. 11b, 12).
- **Algorithmes (Pelican + TX2)** : SPA à 1,1 Hz, soit 2,3 m/s ; TrailNet 55 Hz et DroNet
  178 Hz, sur-dimensionnés de 1,27× et 4,13× par rapport au coude à 43 Hz ; SPA à améliorer
  de 39× (§VI-B).
- **Redondance double (2 × TX2)** : −33 % de vitesse sûre (§VI-C, Fig. 14b).
- **Système complet** : sur Pelican, un Ras-Pi4 devrait gagner 3,3× (DroNet), 110×
  (TrailNet) ou 660× (CAD2RL) ; sur DJI Spark, TX2 + DroNet est 6× au-delà du coude à 30 Hz
  (§VI-D).
- **Accélérateurs nano** : PULP-DroNet (6 FPS à 64 mW) est compute-bound et doit gagner
  4,33× ; Navion (172 FPS à 2 mW pour la VIO seule) donne un pipeline SPA complet à 810 ms,
  soit 1,23 Hz, contre un coude à 26 Hz, donc 21,1× à gagner (§VII, Fig. 16c).

→ reportés dans `benchmarks.csv` : aucune ligne. Le papier est un modèle analytique ; ses
seules mesures propres sont des vitesses sûres en vol, qui ne rentrent pas dans le schéma de
`benchmarks.csv`. Les débits de TX2, AGX, NCS, PULP et Navion sont repris d'ailleurs ou de
l'outil, sans méthode de mesure décrite.

## Limites et critique

- **Validation étroite** : 4 drones du même châssis S500, un seul scénario (arrêt avant un
  obstacle à 3 m), à f_action fixé à 10 Hz par la boucle ROS (§IV). Le régime compute-bound
  et les nano-UAV ne sont **pas validés en vol** ; les conclusions sur PULP et Navion
  (§VII) sont purement modélisées.
- **Physique simplifiée** : pas de traînée, linéarisation à gauche du coude, a_max « typique »
  de 50 m/s² dans l'exemple (§III-D, §IV). Le modèle ne dit rien de la latence de bout en
  bout ni de la gigue, seulement du débit.
- **Masse du calcul réduite au dissipateur** : le calculateur de dissipateur [54] est une
  approximation ; la consommation électrique du calcul sur la batterie (autonomie) n'entre
  pas dans le modèle, alors que c'est l'autre moitié du co-design calcul ↔ énergie ↔ vol.
- **Débits non sourcés** : 230 FPS (AGX), 150 FPS (NCS), 178 Hz (TX2) sans précision, batch,
  ni résolution ; l'hypothèse « TDP divisé par 2 à débit constant » (§VI-A) est admise sans
  justification.
- **Perception absente** : le seul critère de performance est la vitesse sûre ; la qualité
  de détection (précision, taux de fausses alarmes) ne réduit jamais la « sensing distance »
  d dans le modèle (déduit).
- Coquilles : le cadre d'un nano-UAV est donné à « 7mm or less » (§II-B) ; 2,13 contre
  2,2 m/s (§IV contre Fig. 7).

## Pertinence pour la thèse

- **Référence centrale de l'axe `system-codesign`** : c'est la formulation la plus directe
  de l'hypothèse de départ de la base (« aucune métrique système, autonomie ou vitesse de
  vol sûre, dans les papiers YOLO/FPGA »). F-1 donne une métrique système simple à calculer
  pour un détecteur embarqué : placer un design FPGA par rapport au coude de son drone.
- Argument réutilisable dans la problématique : plus de FPS au-delà du coude est inutile,
  et un FPGA à 2-5 W peut battre une Jetson plus rapide par la masse (dissipateur) — à
  démontrer, le papier ne traite **aucun FPGA** (déduit).
- Couvre les trois gammes de puissance (PULP à 64 mW, TX2/AGX à ~10-30 W de TDP), mais
  seulement par modèle.
- Le cas de la redondance double (§VI-C) quantifie le coût en vitesse d'une tolérance aux
  fautes par duplication : point d'entrée pour l'axe `reliability`.

## Gaps identifiés

- **FPGA absents du modèle F-1** : aucune étude de cas FPGA ; placer un YOLO/FPGA mesuré
  (FPS, W à la carte, masse) sur une roofline UAV est à faire.
- **Qualité de perception ignorée** : f_action et d sont indépendants de la précision du
  détecteur ; un modèle qui relie mAP (petits objets, distance de détection) et vitesse
  sûre manque.
- **Énergie du calcul et autonomie** non modélisées ici (seulement la masse) ; à recouper
  avec les travaux antérieurs des mêmes auteurs (réf. [62], cf. 2020-krishnan dans la base).
- **Validation compute-bound et nano-UAV en vol** : absente.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`, aucun avertissement
autre que les axes). Les figures (rooflines, Fig. 11, 13-16) ne sont lisibles qu'à travers
le texte. Table III (liste des études de cas) : légende seule, corps absent.

Ce qui suit est déduit et non affirmé par les auteurs : l'avantage potentiel d'un FPGA par
la masse ; l'absence de lien entre précision du détecteur et distance de détection dans le
modèle ; le statut « non validé en vol » des conclusions sur PULP et Navion (conséquence de
§IV, non formulée par les auteurs) ; le lien entre la réf. [62] et le papier 2020-krishnan
de la base.
