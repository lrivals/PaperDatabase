---
id: arxiv-2607.18936-ngps-gps-denied-aerial-geo
fiche: done
date: 2026-10-01
---

# NGPS: GPS-Denied Aerial Geo-Localization and 2.5D Reconstruction via Deep Satellite Image Matching and Multi-Rate Sensor Fusion

Sanket Sharma (chercheur indépendant), 2026, arXiv preprint. https://arxiv.org/abs/2607.18936
Type : preprint non relu par les pairs (le bandeau du PDF indique « accepté à IROS 2026, Pittsburgh, 27 sept.–1er oct. 2026, publication à venir » ; non vérifié ailleurs).

## Problème

Positionnement absolu d'un UAV volant haut (60–150 m AGL, caméra orientée vers le bas) sans GNSS (brouillage, canyons urbains). Le VIO seul dérive sans fermeture de boucle (§I). Les auteurs veulent un positionnement absolu par appariement de l'image drone avec une image satellite géoréférencée, exécutable en temps réel sur calculateur embarqué (§I).

## Méthode

- Module NGPS : SuperPoint (descripteurs 256-D) + LightGlue, RANSAC (homographie, seuil 5 px), au moins 20 correspondances (seuil de matchabilité 0,5) (§III-C1). Extraction d'un « kernel » k×k = 300 px de la référence satellite, recentré par prédiction avec la vitesse VIO (kernel prédictif, Éq. 1), redimensionné à 900×900 (§III-C2). Rotation estimée par médiane de trois méthodes (homographie, points clés, contour) avec validation temporelle (§III-D).
- VIO : VINS-Fusion monoculaire + IMU, fenêtre glissante de 10 images clés, 150 points KLT (§III-B).
- Fusion : UKF à 15 états, trois mesures asynchrones (NGPS 2D à 1–2 Hz, VIO 6D à 10–20 Hz, IMU 9D à 100–200 Hz) traitées dans une file à priorité temporelle (Algorithme 1). Bruit de mesure NGPS adaptatif : score de confiance γ = 0,4·ratio d'inliers + 0,4·confiance LightGlue − 0,2·tanh(erreur de reprojection/5), borné à [0,1 ; 0,8], R = σ²_base/γ² (Éq. 7-8, §III-E5).
- Reconstruction 2.5D : optimisation de graphe de poses VINS (Ceres, perte de Huber) ancrée par NGPS, orthomosaïque et DSM temps réel (§III-F). Seuls x, y et vitesse horizontale vont à l'EKF3 d'ArduPilot (100–400 Hz) via uXRCE-DDS ; l'altitude reste côté contrôleur de vol (§III-G).

## Plateforme et implémentation

Hexacoptère sur mesure, Cube Orange Plus, calculateur NVIDIA Jetson Orin NX (Ubuntu 22.04, CUDA 11.4, PyTorch 2.0, ROS2 Humble), caméra Topotek à nacelle orientée vers le bas (§IV-A). Référence : Google Earth, GSD ~0,3 m/pixel. Vérité terrain : RTK-GPS (±2 cm). Quantification, fréquence, consommation et mémoire : n/r. Code : « en partie » open source, https://github.com/snktshrma/ngps flight (Abstract) ; le reste n'est pas publié.

## Résultats

- Cinq séquences réelles (Table II : Urban-100, Suburb-80, Agri-60, Mixed-100, High-150 ; 2–4 m/s ; 6,1–12,3 min). RMSE de position du système fusionné adaptatif : 2,94 m (Abstract, §IV-B), contre 10,37 m pour le VIO seul (§IV-E4), soit 3,5× ; NGPS + IMU sans VIO : 4,46 m (§IV-E4). Taux de réussite de l'appariement NGPS : 87,0 % (§IV-B) ; échec sur 21,7 % des images à 150 m contre 10,4 % en moyenne à 60–100 m.
- Par altitude : 2,73 m à 60 m, 1,82–2,06 m à 80–100 m, 6,04 m (ATE pire cas) à 150 m et 2 m/s (§IV-E2, §V). Gain maximal en Agri-60 (5,6×), minimal en High-150 (1,9×) (§IV-B).
- Bruit adaptatif vs bruit fixe : -11 % de RMSE, -12 % d'erreur maximale (§IV-E3). Kernel prédictif à 4 m/s : 84,7 % de réussite contre 64,3 % pour le centrage statique (§IV-E4). File à priorité : +20 % vs ordre d'arrivée, +35 % vs décimation (§IV-E4).
- Comparaison à un VIO monoculaire de George et al. [13] : ATE de NGPS 1,7–6,0 m entre 40 et 150 m, contre 6,74–55,81 m pour le VIO mono, divergent à 40 m / 2 m/s (§IV-C ; corps de la Table VI absent).
- Calcul sur Jetson Orin NX (§IV-D) : NGPS ~2,6 Hz avec CUDA, ~0,5 Hz sur CPU ; LightGlue = 82 % du temps GPU ; UKF < 1 ms par cycle, sortie fusionnée 10–20 Hz. Les temps en ms de la Table VII sont absents du texte extrait.
→ reportés dans `benchmarks.csv` : 2 lignes (NGPS sur Orin NX en GPU puis en CPU, cadence du module NGPS et RMSE global), écrites dans le fichier tampon de l'agent, non dans benchmarks.csv.

## Limites et critique

- Un seul auteur indépendant, preprint, code partiel : résultats non reproductibles en l'état. Cinq séquences seulement, un seul site (apparemment ; non précisé), une seule plateforme.
- La référence satellite est Google Earth (conditions de licence et fraîcheur non discutées) ; sensibilité au décalage temporel de l'imagerie reconnue en §IV-F mais non mesurée.
- Le baseline VIO de la Table VI vient d'un autre papier (George et al.), avec un jeu de données différent : comparaison non appariée, l'auteur le reconnaît pour 150 m (†). Pas de comparaison à d'autres méthodes de géolocalisation absolue (cross-view, SuperGlue seul, etc.) dans le texte extrait.
- Altitude minimale ~40 m ; chute à 150 m (6,04 m) ; échec en texture pauvre (champs). Dépendance au GPU : 0,5 Hz sur CPU.
- Aucune consommation, aucune empreinte mémoire, aucune latence de bout en bout mesurée ; la puissance de la gamme Jetson (~10 W selon la carte, déduit et non rapporté) n'est pas donnée. Pas de quantification ni d'optimisation TensorRT.
- Pas de métrique système (autonomie, vitesse de vol sûre) ; pas de fiabilité (soft errors, mode dégradé garanti), alors que le repli sur VIO seul est le mode de défaillance.

## Pertinence pour la thèse

Axe `tracking-navigation`, gamme Jetson. Référence de navigation sans GNSS embarquée sur drone : budget de calcul concret (SuperPoint + LightGlue sur Orin NX, 2,6 Hz) et compromis fréquence/précision. Pas de détection ni de FPGA. Laisse ouvert : portage FPGA/ASIC de l'appariement transformer (LightGlue dominant à 82 %), mesure de puissance, et lien entre cadence de correction absolue et vitesse de vol sûre.

## Gaps identifiés

- Aucune implémentation FPGA / NPU de SuperPoint + LightGlue pour la géolocalisation aérienne ; le calcul de référence est un Jetson avec GPU obligatoire.
- Puissance et énergie de la géolocalisation visuelle embarquée non rapportées : pas de lien précision ↔ autonomie.
- Pas de fiabilité du mode dégradé (échecs d'appariement 10–22 %) ni de garantie de sûreté pour la fusion VIO / satellite.
- Cadence absolue de 1–2 Hz et vitesse de vol (2–4 m/s) : relation à la vitesse de vol agile non étudiée.

## Statut de lecture

Papier complet (fulltext.md lu en entier), extraction `pymupdf` (`extraction.ok: false`) : le corps des tableaux III, IV, V, VI, VII, VIII, IX est absent du texte extrait. Seuls les chiffres cités dans le texte courant sont utilisés ; les temps en ms (Table VII), les RMSE par séquence (Table IV) et les erreurs de rotation (Table V) ne sont pas lus.
Ce qui suit est déduit et non affirmé par les auteurs : l'absence de comparaison à d'autres méthodes de géolocalisation absolue (d'après le texte extrait seulement) ; l'ordre de grandeur de puissance du Jetson ; que le RMSE de 2,94 m est obtenu avec le kernel prédictif et le traitement GPU (non précisé pour le CPU).
