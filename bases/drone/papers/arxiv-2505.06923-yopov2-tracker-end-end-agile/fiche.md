---
id: arxiv-2505.06923-yopov2-tracker-end-end-agile
fiche: done
date: 2026-10-01
---

# YOPOv2-Tracker: An End-to-End Agile Tracking and Navigation Framework from Perception to Action

Junjie Lu, Yulin Hui, Xuewei Zhang, Wencan Feng, Hongming Shen, Zhiyu Li, Bailing Tian, 2025, arXiv preprint. https://arxiv.org/abs/2505.06923
Type : preprint non relu par les pairs

## Problème

Le suivi agile d'une cible non coopérative en environnement encombré (forêt, bâtiments) repose d'ordinaire sur un pipeline séquentiel détection → cartographie (ESDF) → recherche de chemin → optimisation de trajectoire → contrôle. Les auteurs posent que cette chaîne ajoute de la latence et accumule des erreurs, ce qui est fatal à haute vitesse sur un petit quadrotor à capteurs et calcul limités (Abstract, §I). Les politiques de bout en bout existantes visent la course ou la navigation, pas le suivi de cible (§I).

## Méthode

- Réseau unique, entièrement convolutionnel : entrée RGB-D 160×96 (FOV 90°) et 6 états (vitesse, accélération) ; backbone ResNet-18 modifié (sous-échantillonnage 32×) donnant une grille 5×3 ; couches 1×1 à poids partagés sortant 14 valeurs par primitive (décalages, dérivées finales, coût de trajectoire, score d'objectness, position de la cible) (§III-C-1).
- Les primitives de mouvement (états finaux sur un treillis dans le FOV) jouent le rôle des anchor boxes de la détection ; le réseau prédit des décalages et des coûts ; NMS avec filtre de Kalman étendu (EKF, vitesse constante) pour la cohérence spatio-temporelle de la cible, puis choix de la meilleure trajectoire par coût de sécurité et de régularité (§III-B, §III-C-2).
- Trajectoire polynomiale d'ordre 5 dans l'espace plat différentiel ; le yaw est planifié séparément vers la cible estimée (§III-B, Fig. 6).
- Contrôle : suppression du contrôleur de position ; l'attitude et la poussée sont calculées directement depuis l'accélération désirée compensée par un observateur de perturbation à fort gain (§III-D). Politique indépendante du modèle dynamique (modèle point-masse), sans domain randomization.
- Entraînement sans démonstrations d'expert ni interaction simulateur : les gradients des coûts de trajectoire (régularité, sécurité via ESDF privilégié, but) sont rétropropagés dans le réseau ; pertes SmoothL1 sur le coût et la position cible, BCE sur l'objectness (§III-E). Données collectées à l'avance (poses aléatoires, images, nuage de points) ; en réel, cibles annotées par un détecteur YOLO (version n/r) (§III-E-3).
- Normalisation des entrées/sorties permettant d'ajuster la vitesse sans réentraîner (§III-C-1). Le même cadre se dégrade en politique de navigation en ajoutant une direction de but (§IV-C).
- Toolflow : TensorRT cité pour le déploiement GPU (§IV-A, §IV-B-1) ; pas de FPGA, pas de quantification déclarée.

## Plateforme et implémentation

- Quadrotor maison de 155 mm d'empattement, 850 g, rapport poussée/poids théorique 4,7, cadre OddityRC XI35, moteurs OddityRC-2006 2150KV, hélices 3,5 pouces, contrôleur NxtPX4 sous PX4, VIO VINS-Fusion, MAVROS (§IV-A).
- Calcul embarqué : NVIDIA Orin NX (180 g ; CPU 8 coeurs Cortex-A78 à 2,0 GHz ; GPU « 100 TOPS » selon les auteurs) ; variante mémoire/puissance (mode) n/r. Capteur : RealSense D455 (RGB-D, 16:9, FOV 90°, portée utile < 10 m) (§IV-A). Gamme de puissance : classe Jetson (~10 à 25 W, à titre indicatif, déduit) ; **puissance non rapportée par l'article**.
- Banc de simulation : Intel i7-9700, RTX 3060, 32 Go RAM, Ubuntu 20.04 (§IV-B-1).
- Code et matériel : annoncés comme publiés sur https://github.com/TJU-Aerial-Robotics/YOPO-Tracker (Abstract, §IV-A) ; existence non vérifiée ici (« The code will be released » dans l'Abstract).

## Résultats

- Latence perception → commande : 3 ms en moyenne en simulation (2 ms d'inférence sous TensorRT + 1 ms de post-traitement) sur i7-9700 + RTX 3060 (§IV-B-1), contre 66,7 ms (série) pour Vis. Tracker, dont près de 50 ms de cartographie/ESDF (§IV-B-1, Fig. 10A) ; Elas. Tracker plus rapide que Vis. Tracker mais valeur n/r dans le texte (Fig. 10A). Les auteurs annoncent « plus d'un ordre de grandeur » d'avantage (§IV-B-1).
- Embarqué : latence moyenne de 8,2 ms perception → action sur Orin NX en forêt réelle (§IV-B-3).
- Taux de succès en simulation (forêt de Poisson, densité 1/16 arbre/m², cible fuyant à 3 à 7 m/s, 10 essais par vitesse) : le modèle reste « constamment élevé » de 3 à 7 m/s, les baselines Elas. Tracker et Vis. Tracker chutent avec la vitesse ; **valeurs numériques n/r dans le texte** (Fig. 10B uniquement) (§IV-B-1).
- Vitesse maximale en suivi réel : 6 m/s en forêt dense (arbres espacés de 3 à 4 m), 5,6 m/s en bâtiments (§IV-B-3, Fig. 13, 14) ; les auteurs la comparent à 2,5 m/s maximum rapporté pour [2] (Vis. Tracker).
- Erreur d'estimation de la cible à 7 m/s en simulation : latérale ±0,5 m, longitudinale ±0,75 m (§IV-B-2, Fig. 12). Une seule distance minimale aux obstacles < 0,2 m, à 7 m/s (§IV-B-1, Fig. 10F).
- Navigation (variante) : comparée à Agile [4] à 4–10 m/s, clearance 4 et 5 m, 10 essais par niveau ; supérieur en environnement dense (Fig. 16, valeurs n/r dans le texte) ; vols réels jusqu'à 8 m/s (but à 90 m puis 35 m), vitesse > 8 m/s en Fig. 18 (§IV-C).
- Cadre incrémental par rapport à [6] (YOPO, erreur de position > 0,5 m à 5,5 m/s) (§IV-C-2).

→ reportés dans `benchmarks.csv` : 2 lignes (latence Orin NX en vol réel ; latence RTX 3060 en simulation). Aucun chiffre de précision/succès exploitable dans le texte extrait (figures seulement).

## Limites et critique

- Latence : le 3 ms est mesuré sur un GPU de bureau (RTX 3060), pas sur l'embarqué ; la valeur embarquée (8,2 ms sur Orin NX, §IV-B-3) n'est donnée que comme moyenne en vol, sans décomposition ni précision numérique (FP16/INT8 n/r), ni mode de puissance de l'Orin NX. **Aucune puissance, consommation ni autonomie** rapportée : le co-design calcul ↔ énergie ↔ vol n'est pas mesuré.
- Comparaison aux baselines : Elas. Tracker et Vis. Tracker sont conçues pour 2 à 2,5 m/s et sont mises dans des conditions qu'elles n'ont pas été conçues pour traiter (cartographie en ligne sur profondeur bruitée, détecteur YOLOv5s fourni par les auteurs) ; l'évader, lui, utilise la carte privilégiée (§IV-B-1). Latence des baselines mesurée sur CPU/GPU de bureau avec leur propre découpage (mapping/front/back), non équivalente à celle d'un pipeline porté sur Orin NX (déduit).
- Statistiques minces : 10 essais par vitesse, sans intervalle de confiance ; résultats surtout en figures (Fig. 10, 16), non reportés en chiffres dans le texte.
- Pas de prédiction de mouvement de la cible : les échecs viennent surtout des occlusions (§IV-B-1, Fig. 10C). Hypothèse de visibilité de la cible au départ (§IV-B-3). Cible principale : un humain (cible « large »), pas un petit objet ni un autre drone.
- Détection simplifiée à une classification binaire cible/fond ; aucune métrique de détection (mAP, IoU) ; pas de comparaison aux métriques de la base (DAC-SDC, VisDrone). Annotations réelles produites par un YOLO dont la version n'est pas donnée.
- Fiabilité : aucune analyse de défaillance matérielle, de soft errors ni de certification ; pas de FPGA ni d'accélérateur dédié.
- Preprint non relu par les pairs ; code annoncé (« will be released ») : à vérifier.

## Pertinence pour la thèse

Axe `tracking-navigation`, sous-thème vol agile (tag `drone-racing` dans la règle de la base) : référence de latence perception → contrôle en gamme Jetson (Orin NX, 8,2 ms bout en bout en vol réel) pour un quadrotor de 850 g, à comparer à Kaufmann 2023 et à la généalogie YOPO (Loquercio « learning high-speed flight in the wild »). Ce n'est pas du contre-drone : la cible est un humain, tag `air-to-air` non applicable. Pour la thèse « calcul embarqué », il montre qu'un seul réseau ResNet-18 de petite résolution suffit à remplacer le pipeline mapping + planning (à ~2 ms de GPU), ce qui pose la question du portage sur FPGA/MCU de ce type de politique, jamais traitée ici.

## Gaps identifiés

- Aucune mesure de puissance / énergie / autonomie pour une politique end-to-end de suivi ou de navigation agile ; pas de métrique système liant latence, consommation et vitesse de vol sûre.
- Politique de type YOPO jamais portée sur FPGA / MCU / ASIC (ResNet-18 sur 160×96 : candidat naturel) ; effet de la quantification (INT8) sur la sécurité de la trajectoire non étudié.
- Pas de contre-drone air → air avec cette approche (cible drone, petit objet) ; la cible est un humain.
- Latences baselines et proposée non mesurées sur la même plate-forme embarquée.

## Statut de lecture

papier complet (fulltext.md lu en entier, y compris §I à §V ; la liste de références n'a pas été exploitée). **Extraction `pymupdf`, `extraction.ok: false`** : le texte est bien lisible, mais les figures (Fig. 10, 16 : taux de succès, latences par module, régularité, clearance) ne sont pas extraites en chiffres ; aucun tableau de résultats dans cet article. Les équations (2)-(16) sont partiellement dégradées (indices perdus) ; l'équation de la loi de commande n'a pas été vérifiée symbole par symbole.
Ce qui suit est déduit et non affirmé par les auteurs : la gamme de puissance de l'Orin NX (~10 à 25 W) ; le fait que les latences des baselines ne sont pas comparables à celle de l'Orin NX ; la remarque sur le portage FPGA/MCU et l'absence d'INT8 (la précision numérique de TensorRT n'est pas dite).
