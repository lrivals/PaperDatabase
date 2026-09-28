---
id: arxiv-1905.06388-mavbench-micro-aerial-vehicle-benchmarking
fiche: done
date: 2026-09-28
benchmarks: none
---

# MAVBench: Micro Aerial Vehicle Benchmarking

Behzad Boroujerdian, Hasan Genc, Srivatsan Krishnan, Wenzhi Cui, Aleksandra Faust, Vijay Janapa Reddi, 2019, 2018 51st Annual IEEE/ACM International Symposium on Microarchitecture (MICRO). https://arxiv.org/abs/1905.06388
Type : conférence (MICRO 2018, selon le `journal_ref` arXiv ; version arXiv déposée en 2019). DOI n/r dans les métadonnées.

## Problème

Les architectes matériels manquent d'outils pour comprendre comment performance, puissance
et goulots de calcul affectent les applications de MAV (drones < 2 kg, §II-A), dont
l'autonomie est limitée (< 20 min typiquement, §I). Il faut évaluer le calcul **en boucle
fermée** avec le véhicule et l'environnement, pas des noyaux isolés (§I, §IV). Question
centrale : « what is the role of computing in autonomous MAVs? » (§I).

## Méthode

- **Simulateur en boucle fermée** (§III) : Unreal + AirSim sur un hôte i7 + GTX 1080 Ti pour
  l'environnement, les capteurs et la dynamique ; contrôleur de vol simulé par AirSim
  (Pixhawk/PX4 possible) ; **ordinateur compagnon réel en hardware-in-the-loop, Jetson TX2**,
  relié en Ethernet ; applications sous ROS.
- **Modèle d'énergie** ajouté à AirSim : puissance paramétrique fonction de vitesse,
  accélération, masse et vent (Éq. 1, d'après [30]) ; batterie par comptage de coulombs
  (§III-C).
- **Suite de 5 applications de bout en bout** (§IV-B) : Scanning, Package Delivery, Aerial
  Photography, 3D Mapping, Search and Rescue. Noyaux interchangeables : YOLO, HOG, Haar
  (détection), KCF (suivi), ORB-SLAM2, VINS-Mono (localisation), OctoMap, OMPL (RRT, PRM +
  A*), next-best-view planner, lissage de trajectoire (§IV-C).
- **Métriques Quality-of-Flight** : temps de mission et énergie surtout (§IV-D).
- **Études** : balayage fréquence (0,8 / 1,5 / 2,2 GHz) et nombre de cœurs A57 (2 à 4) du
  TX2, cœurs Denver coupés (§V-C, Fig. 15) ; trois études de cas : délestage vers le cloud,
  résolution d'OctoMap dynamique, bruit capteur (§VI).
- Mesure réelle de puissance en vol d'un 3DR Solo avec un wattmètre Eagle Tree eLogger V4
  sur la batterie, 50 Hz (§V-B).

## Plateforme et implémentation

- Ordinateur compagnon : **NVIDIA Jetson TX2** (Pascal 256 cœurs + ARM), ~10 W en moyenne
  selon les auteurs (§I) → gamme Jetson (~10 W). Aucun FPGA, aucun MCU.
- Puissance du TX2 : mesurée ? Non décrit ; le chiffre de 10 W est donné comme ordre de
  grandeur (§I). La puissance des rotors du drone simulé vient du modèle (Éq. 1).
- Drone simulé pour les cartes de chaleur : DJI Matrice 100 (§V-C).
- **Code** : présenté comme « open source » (résumé, §VI), lien n/r dans le texte extrait.

## Résultats

- **Puissance d'un MAV** : 300 à 400 W pour les rotors d'un DJI Matrice ou 3DR Solo ; le
  calcul consomme en moyenne < 5 % de la puissance totale (§I). Rotors ≈ 20 fois la
  puissance du reste sur le 3DR Solo mesuré (légende Fig. 9).
- **Vitesse max bornée par le calcul** : 8,83 à 1,57 m/s pour un temps pixel → réponse de
  0 à 4 s (Fig. 8a, Éq. 2).
- **Micro-benchmark SLAM** : accélérer le traitement 5× réduit l'énergie du drone d'environ
  4× (§V-B, Fig. 8b).
- **Mise à l'échelle du TX2** (§V-C, Fig. 10-15) :

| Application | Temps de mission | Énergie | Autres |
|---|---|---|---|
| Scanning | effet négligeable | effet négligeable | planning amorti (< 0,001 %) |
| Package Delivery | −84 % | −82 % | vitesse moyenne ×4,8 ; OctoMap ×2,9 |
| 3D Mapping | −86 % | −83 % | vitesse moyenne ×5,3 ; OctoMap ×6 |
| Search and Rescue | −67 % | −57 % | détection ×1,8 ; vitesse moyenne ×2,2 |
| Aerial Photography | +267 % (souhaitable ici) | pas de tendance | erreur de cadrage −53 % |

- **Cloud** : planification 3× plus rapide, mission jusqu'à −50 % (3D Mapping, §VI-A,
  Fig. 16) sur LAN 1 Gb/s « qui imite la 5G ».
- **OctoMap** : de < 0,2 m à 1,0 m de résolution, temps de traitement de > 0,4 s à < 0,1 s
  (Fig. 18) ; la résolution dynamique (0,15 / 0,80 m) améliore la consommation batterie
  jusqu'à **1,8×**, et 0,80 m statique fait échouer la mission (§VI-B, Fig. 19).
- **Bruit de profondeur** (Table II, reconstruite par PyMuPDF) : écart-type 0 → 1,5 m, temps
  de mission 72 → 137 s, re-planifications 2 → 8, échec 10 % à 1,5 m (§VI-C).

→ reportés dans `benchmarks.csv` : aucune ligne. Le papier ne donne ni FPS, ni latence, ni
précision d'un détecteur sous forme exploitable : la Table I (profil temporel des noyaux en
ms) n'a pas de corps extrait, et les résultats sont des ratios lus sur des cartes de chaleur
(Fig. 10-15) ou des temps de mission, qui ne rentrent pas dans le schéma de `benchmarks.csv`.

## Limites et critique

- **Tout est en simulation**, sauf le TX2 et la mesure de puissance du 3DR Solo : le
  modèle d'énergie (Éq. 1) et le « reality gap » (§III-E) conditionnent tous les chiffres
  de mission. Les coefficients β du modèle ne sont pas donnés.
- **Non-déterminisme reconnu** : anomalies du balayage de cœurs attribuées au caractère non
  temps réel de ROS, AirSim et TCP/IP (§V-C). Pas de nombre de répétitions ni d'écart-type.
- **Une seule plateforme de calcul (TX2)**, balayée en DVFS : l'effet d'un accélérateur
  (FPGA, GPU embarqué différent, MCU) n'est pas mesuré. La conclusion « plus de calcul =
  moins d'énergie » repose sur un calcul à ~10 W sur un drone de 300-400 W ; elle ne se
  transpose pas telle quelle à un nano-drone où le calcul pèse une fraction bien plus grande
  du budget (déduit).
- **Masse du calcul ignorée** : le modèle Éq. 1 contient la masse m, mais l'étude ne fait
  pas varier la masse du calculateur avec sa puissance (déduit du texte, pas discuté).
- **Détection** : YOLO et HOG sont fournis, mais aucune précision de détection n'est
  rapportée ; l'étude de cas « fiabilité » porte sur le bruit capteur, pas sur des fautes
  matérielles (l'injection de bit flips est seulement évoquée, §VI-C).
- Le délestage cloud sur LAN 1 Gb/s est optimiste pour un drone en extérieur.

## Pertinence pour la thèse

- **Référence fondatrice de l'axe `system-codesign`** : établit par des chiffres que le
  calcul agit sur l'énergie totale **via le temps de mission et la vitesse max sûre**, pas
  via sa propre puissance (§V). C'est exactement la métrique système absente des papiers
  YOLO/FPGA (hypothèse de `gaps.md`).
- Fournit le modèle de vitesse max en fonction du temps pixel → réponse (Éq. 2, Fig. 8a),
  réutilisable pour traduire la latence d'un accélérateur FPGA en vitesse de vol sûre.
- Base d'expérimentation possible : remplacer le TX2 par un SoC FPGA en hardware-in-the-loop
  (§III-D l'autorise explicitement).
- Laisse ouvert : effet de la **masse** et de la **puissance** du calculateur (FPGA 2-5 W
  contre TX2 ~10 W), détection de petits objets, fautes matérielles.

## Gaps identifiés

- **Métriques système pour les accélérateurs FPGA** : MAVBench fournit le cadre (temps de
  mission, énergie, vitesse sûre), mais aucun papier FPGA de la base ne semble l'utiliser
  (à vérifier dans le corpus).
- **Compromis masse / puissance / latence du calculateur** non exploré : seule la fréquence
  du TX2 varie.
- **Fiabilité du calcul** (soft errors) évoquée comme extension, non réalisée (§VI-C).
- Précision de détection absente des QoF : aucune boucle entre mAP et succès de mission.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). La Table I (profil
temporel des noyaux sur TX2, en ms) est réduite à ses en-têtes dans l'extraction ; la
Table II est reconstruite par PyMuPDF (à vérifier). Les Fig. 10-15 (cartes de chaleur)
ne sont connues que par le texte.

Ce qui suit est déduit et non affirmé par les auteurs :
- la non-transposabilité de la conclusion aux nano-drones ;
- l'absence de variation de la masse du calculateur dans l'étude ;
- l'usage possible d'un SoC FPGA en hardware-in-the-loop dans MAVBench ;
- l'absence d'utilisation de ces métriques par les papiers FPGA du corpus (non vérifiée).
