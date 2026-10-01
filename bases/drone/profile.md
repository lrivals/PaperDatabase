# Profil — Vision embarquée sur drone

Thème et périmètre de la base. La partie machine (axes, règles de classement, requêtes de
découverte) est dans `base.json` ; ce fichier en donne la justification. Le LLM propose des
changements (`/base-profile`, suggestions de `/paper-fiche`) ; rien n'est appliqué sans accord.

## Thème (utilisateur)

Base de connaissance d'articles scientifiques sur la vision embarquée sur drone : détection
(YOLO, petits objets), accélérateurs embarqués (FPGA, MCU/nano-drone, ASIC, neuromorphique),
co-design calcul ↔ énergie ↔ vol et fiabilité. Destinée à préparer une thèse.

## Précisions

- Finalité : préparer une thèse, en complément de la base « vision embarquée sur FPGA »
  (`fpga`), dont des papiers peuvent être importés (`bin/pdb base import fpga:<id>`).
- Hypothèses de départ, à étayer (`gaps.md`) : les YOLO drone SOTA (tête P2, Transformer) ne
  sont presque jamais portés sur FPGA ; l'effet de la quantification sur le mAP_small n'est
  pas mesuré ; aucune métrique système (autonomie, vitesse de vol sûre) dans les papiers
  YOLO/FPGA.
- Toujours situer un résultat dans sa gamme de puissance : nano (GAP8, mW), FPGA (W),
  Jetson (~10 W).
- **Règle sol → air / air → air.** Tout papier contre-drone porte un tag de point de vue :
  `air-to-air` (détecteur embarqué sur un drone), `ground-to-air` (capteur au sol) ou
  `viewpoint-unspecified` (non déclaré, jeux mêlant les points de vue). Les papiers
  `ground-to-air` restent dans la base comme jeux de données, métriques (mSA) et références
  de contraste, jamais comme contribution « IA embarquée » ; à la découverte, on n'en ajoute
  plus que s'ils apportent un jeu de données ou un protocole.
- **Vol agile** (course de drones, vol à haute vitesse) : sous-thème de `tracking-navigation`,
  retenu comme référence de latence perception → contrôle en gamme Jetson (tag `drone-racing`).
- **YOLO « petits objets » génériques** : inclus en `drone-detection` seulement s'ils sont
  évalués sur un jeu drone (VisDrone, UAVDT, DAC-SDC…), même en évaluation secondaire ;
  sinon hors périmètre.
- L'axe `drone-fpga` couvre toute accélération FPGA / SoC embarquée utile au drone,
  détection et navigation (SLAM, planification, ROS sur FPGA, hardware-in-the-loop).

## Inclus

- Détection sur images aériennes et de drone, petits objets (VisDrone, UAVDT, DAC-SDC).
- Détection applicative embarquée sur drone (feux de forêt, fumée, inspection).
- Accélération FPGA / SoC embarquée à bord : détection et noyaux de navigation.
- Contre-drone **air → air** (détecteur embarqué sur un drone intercepteur).
- Jeux de données et benchmarks de contre-drone, y compris filmés du sol (Anti-UAV,
  Anti-UAV410, MAV-VID, Drone-vs-Bird), comme données et métriques.
- Nano-drones, MCU, ASIC, neuromorphique.
- Co-design calcul ↔ énergie ↔ vol ; fiabilité du calcul embarqué ; suivi et navigation, y
  compris vol agile.

## Exclus

- Contre-drone **sol → air** (capteur fixe au sol) comme contribution méthode : ne relève pas
  de l'IA embarquée. Les papiers déjà présents gardent le tag `ground-to-air`.
- Détecteurs « légers pour l'embarqué » déployés sur un capteur au sol (Raspberry Pi de
  surveillance) : même statut que le sol → air.
- Résultats sur GPU de bureau présentés comme « embarqués ».
- YOLO « petits objets » sans aucune évaluation sur un jeu drone.
- Localisation non visuelle (UWB, radio) : hors périmètre ; LAND reste comme contexte
  « budget énergie nano-drone » (tag `hors-perimetre`).

## Vocabulaire

UAV, AAV (terme IEEE récent), MAV, nano-drone, VisDrone, UAVDT, DAC-SDC, Det-Fly, Anti-UAV,
Drone-vs-Bird, mAP_small, mSA, IoU mono-objet vs mAP multi-classe, tête P2, GAP8/GAP9,
Crazyflie, roofline, autonomie, soft errors, sol → air / air → air, rejet des oiseaux et
avions, drone racing, vol agile, VIO, MPC, sim-to-real.

## Suggestions en attente

<!-- Une ligne par suggestion : - AAAA-MM-JJ (source : paper_id ou /base-profile) — proposition — raison -->
- 2026-10-01 (arxiv-2509.18610-singer-onboard-generalist-vision-language, arxiv-2605.00884-litevla-h-dual-rate-vision, arxiv-2609.25415-cloud-edge-split-profiling-onboard) — sous-thème « VLM / VLA embarqués et split bord-cloud » sous system-codesign / tracking-navigation, tags vlm et vla, inclus seulement avec mesure sur calculateur embarqué — trois papiers hors YOLO/FPGA, aucun terme VLM/VLA dans le vocabulaire
- 2026-10-01 (arxiv-2508.04564-drone-detection-event-cameras) — vocabulaire « caméra événementielle / neuromorphique (DVS, SNN, Loihi, Speck) », tag event-camera ; préciser son statut sol → air — survey de capteurs surtout fixes, tag de point de vue non posé
- 2026-10-01 (arxiv-2603.01850-tiny-dronerf-tiny-neural-radiance) — sous-thème « apprentissage embarqué / fédéré sur nano-drone », tag on-device-training — non couvert par le profil
- 2026-10-01 (arxiv-2607.18936-ngps-gps-denied-aerial-geo) — « navigation sans GNSS par géolocalisation visuelle » comme sous-thème de tracking-navigation, tag gnss-denied — le profil n'exclut que la localisation non visuelle
- 2026-10-01 (arxiv-2609.21005-project-scout-interceptor-drone-perimeter) — termes « interception », « C-UAS » au vocabulaire de counter-uav — absents
- 2026-10-01 (arxiv-2603.02936-self-supervised-domain-adaptation-visual) — « adaptation de domaine sim-to-real embarquée » au vocabulaire — seul sim-to-real y figure

## Historique

- 2026-09-28 — base créée à la main (liens vers `../PaperDatabase`), 9 axes dans `base.json`.
- 2026-09-28 — déplacée dans le dépôt PaperDatabase (`bases/drone/`), versionnée avec lui.
- 2026-09-28 — profil rédigé par Claude à partir de `CLAUDE.md` et `base.json`, à relire (`/base-profile`).
- 2026-09-28 — règle sol → air / air → air : tag de point de vue obligatoire en contre-drone ; sol → air gardé comme données et références, exclu comme méthode — suggestions de Seidaliyeva, F-YOLOv7, YOLO-GCOF, Zheng 2023, Gao 2024, Anti-UAV, MAV-VID (13 suggestions de /paper-fiche traitées).
- 2026-09-28 — vol agile ajouté comme sous-thème de tracking-navigation (tag drone-racing) — Kaufmann 2023, survey UZH.
- 2026-09-28 — YOLO petits objets génériques : inclus seulement avec évaluation sur un jeu drone — SF-YOLOv5.
- 2026-09-28 — axe drone-fpga élargi à « Accélération FPGA / SoC embarquée (détection, navigation) » — Robotic computing on FPGAs.
- 2026-09-28 — « AAV » ajouté à topic_re / title_topic_re ; détection applicative (feux) incluse, tag wildfire — YOLOX FPGA feux de forêt.
- 2026-09-28 — localisation non visuelle exclue ; LAND gardé comme contexte (tag hors-perimetre).
- 2026-09-28 — règles de tags resserrées (ground-to-air, air-to-air, bird-rejection, drone-racing) ; pénalité regex « fixed camera » écartée (faux positifs, ex. UAVDT).
