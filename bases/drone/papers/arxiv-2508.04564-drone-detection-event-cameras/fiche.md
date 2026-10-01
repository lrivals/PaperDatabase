---
id: arxiv-2508.04564-drone-detection-event-cameras
fiche: done
date: 2026-10-01
benchmarks: none
---

# Drone Detection with Event Cameras

Gabriele Magrini, Lorenzo Berlincioni, Luca Cultrera, Federico Becattini, Pietro Pala, 2025, arXiv preprint. https://arxiv.org/abs/2508.04564
Type : preprint non relu par les pairs. Survey court (revue de littérature), sans expérience propre.
Point de vue contre-drone : `ground-to-air` / `viewpoint-unspecified` (capteurs fixes pour l'essentiel ; voir Pertinence).

## Problème

Les caméras à images (frame-based) détectent mal les drones : petite taille, forte agilité, flou de bougé, plage dynamique limitée (drone en contre-jour ou en faible lumière) (§1). Les auteurs passent en revue la vision événementielle comme solution : résolution temporelle de l'ordre de la microseconde, plage dynamique > 120 dB, faible consommation, données parcimonieuses qui suppriment le fond statique (§1, affirmés sans mesure propre).

## Méthode

Pas de méthode propre : revue de littérature organisée en taxonomie (Fig. 2). Représentations des événements (§4) : event frames (accumulation sur ∆t), nuages de points (x, y, t, p), grilles de voxels, frames à mémoire temporelle (Time Surface, TBR / SpikeTBR), représentations spike. Détecteurs cités : EV-SpSegNet (point cloud, GDSCA, STC loss), PointNet / PointNet++ pour classer drone / oiseau / insecte, DETR multimodal (ER-DETR), YOLO + DBSCAN, SNN entraîné par STDP (Kirkland), Spiking Swin Transformer (Zhang, sans puce neuromorphique). Au-delà de la détection (§5) : suivi (DCF+CNN, SiamEvent, HDETrack, YOLOv5 + KD-tree, baselines YOLO / RT-DETR / Faster-RCNN + ByteTrack sur FRED), prévision de trajectoire (Mamba auto-supervisé avec pseudo-labels LiDAR ; baselines LSTM / transformer sur FRED), analyse de la signature des hélices (fréquentiel, Poisson, EVPropNet, tachymétrie EV-Tach et EB-ASM, clôture virtuelle de Stewart sans réseau de neurones). Jeux de données (§6, Table 1) : Anti-UAV, EED, VisEvent, EventVOT, F-UAV-D, Ev-UAV, Ev-Flying, NeRDD, CRSOT, FRED, SFERA, jeu d'Iaboni ; simulation et événements synthétiques (Blender, Shah et al.).

## Plateforme et implémentation

Aucune plateforme propre. Matériel neuromorphe cité : Intel Loihi, SynSense Speck (clôture virtuelle de drone, Eldeborg et al., tâche « drone fencing » binaire) ; capteurs Prophesee EVK4 (1280×720, F-UAV-D), deux Prophesee fisheye (SFERA). Aucun chiffre de puissance, de latence ou de débit dans le texte. Code / jeux de données : aucun lien donné dans le survey (n/r).

## Résultats

Pas de résultat chiffré du survey. Seuls chiffres du texte, rapportés tels quels d'autres travaux : erreur relative de tachymétrie jusqu'à 0,03 % pour EV-Tach, comparable à un tachymètre laser (§5) ; Ev-UAV : 147 séquences, > 2,3 M d'annotations événementielles (§6) ; FRED : 7 h 07 min, 5 modèles de drones (Table 1, §6) ; NeRDD : 3 h 30 min, caméras fixes au sol (Table 1, §6) ; Fig. 1 : tendance du nombre de publications 2012-2024 (requête Google Scholar).
→ reportés dans `benchmarks.csv` : aucune ligne. Survey, les chiffres appartiennent aux travaux cités ; `benchmarks: none`.

## Limites et critique

- Survey court, sans méthodologie de recherche bibliographique ni tableau comparatif de performances (mAP, latence, énergie) entre détecteurs événementiels : impossible de classer les approches sur ce seul papier.
- Les avantages de l'événementiel (énergie, latence, > 120 dB) sont affirmés, jamais mesurés ni comparés à un baseline GPU / Jetson / MCU dans le texte. Aucune gamme de puissance (nano / FPGA / Jetson) n'est donnée.
- Le caractère « embarqué » est peu traité : la quasi-totalité des systèmes cités sont des capteurs fixes (NeRDD : caméras au sol stationnaires ; Iaboni : caméra au plafond ; clôture virtuelle). Seul EVPropNet (suivi / atterrissage sur drone non marqué) est mentionné comme application on-drone. Les distinctions sol → air / air → air ne sont pas faites par les auteurs (déduit).
- Limites reconnues par les auteurs : un objet immobile disparaît du flux événementiel (d'où le multimodal RGB + événements) ; météo (pluie, neige) difficile aussi pour les caméras événementielles ; domain shift des événements synthétiques.
- Pas de traitement des FPGA pour les événements, ni de la quantification.

## Pertinence pour la thèse

Axes : `counter-uav`, `tracking-navigation`, `datasets-benchmarks`, `nano-drone` (neuromorphique) et `surveys`. Utile comme carte du domaine et source de jeux de données événementiels (FRED, NeRDD, Ev-UAV, SFERA), de protocoles (MOTA, IDF1 pour FRED) et de pistes neuromorphiques (Speck, Loihi) pour la gamme mW. Ne constitue pas une contribution « IA embarquée » en soi : les systèmes décrits sont majoritairement sol → air. Laisse ouvert l'embarqué air → air avec capteur événementiel (puissance, latence, masse) et l'accélération FPGA du traitement événementiel.

## Gaps identifiés

- Aucune mesure puissance / latence de bout en bout d'un détecteur événementiel de drone sur plateforme embarquée (Jetson, FPGA, MCU) comparée au pipeline RGB.
- Détection événementielle de drone air → air (capteur sur un drone intercepteur) quasi absente.
- Pas de FPGA pour la détection événementielle de drones dans ce survey (à vérifier dans le corpus).
- Pas de métrique unifiée entre jeux événementiels (détection, suivi, prévision).

## Statut de lecture

Papier complet (fulltext.md intégral, 7 sections). Extraction `pymupdf` (`extraction.ok: false`) : texte lisible mais tableaux reconstruits à plat ; la Table 1 est une ligne de texte, ses colonnes (RGB/Event, durée) peuvent être décalées, durées reprises avec prudence. Déduit et non affirmé par les auteurs : le classement sol → air des systèmes cités, l'absence de comparaison à un baseline embarqué, l'absence de FPGA dans le survey. Les métadonnées (auteurs, titre) correspondent au texte lu.
