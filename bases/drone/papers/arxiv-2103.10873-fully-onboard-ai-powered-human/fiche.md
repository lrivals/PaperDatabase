---
id: arxiv-2103.10873-fully-onboard-ai-powered-human
fiche: done
date: 2026-09-28
---

# Fully Onboard AI-powered Human-Drone Pose Estimation on Ultra-low Power Autonomous Flying Nano-UAVs

Daniele Palossi, Nicky Zimmerman, Alessio Burrello, Francesco Conti, Hanna Müller, Luca Maria Gambardella, Luca Benini, Alessandro Giusti, Jérôme Guzzi, 2021, arXiv preprint. https://arxiv.org/abs/2103.10873
Type : preprint non relu par les pairs (d'après `metadata.json` ; une version journal existe probablement, voir « Statut de lecture »)

## Problème

Faire tourner **à bord d'un nano-drone** de 27 g (Crazyflie 2.1), avec un processeur de
classe MCU sous 100 mW, un CNN qui estime la pose relative d'une personne (x, y, z, θ) à
partir d'une caméra basse résolution, et fermer la boucle de contrôle pour rester face à
elle (interaction humain-drone). Aucun calcul déporté : le WiFi est coupé en vol (§III-B).
La baseline applicative, le Proximity NN [4] (ResNet), tournait sur le GPU d'un PC distant
avec un Parrot Bebop 2 (§II).

## Méthode

- **PULP-Frontnet** : CNN sans connexions résiduelles, avec une conv 5×5, un max-pool, 3
  blocs de 2 conv 3×3, un dropout et une couche FC à 4 sorties (§IV-A, Fig. 3). Trois
  variantes : **160×32** (14,1 MMAC, 499 kB), **160×16** (4,3 MMAC, 184 kB) et **80×32**
  (4,0 MMAC, 348 kB). Le Proximity NN compte 96,5 MMAC et 6116 kB (Table II).
- **Données** : jeu propre de 6657 images 160×160 en niveaux de gris, étiquetées par motion
  capture, 10 sujets (6 pour l'entraînement, 4 pour le test) (§IV-B). **Augmentation
  « pitch » synthétique** par recadrage vertical en 160×96 (±14°), puis augmentations
  photométriques et optiques (vignettage, flou) (§IV-B, Fig. 4).
- **Quantification** : QAT avec NEMO (variante de PACT), linéaire par couche, poids sur
  128 niveaux (INT8 signé) et activations sur 8 bits non signés ; BN en entier avec des
  paramètres 32 bits. Le réseau tourne entièrement en entier (§IV-C).
- **Déploiement** : PULP-NN (jusqu'à 15,6 MAC/cycle) et DORY pour le tiling
  L3→L2→L1 en double buffering ; pour 160×16, tous les poids sont préchargés en L2 (code
  DORY modifié à la main) (§IV-C).
- **Contrôle** : 4 boucles. Caméra et inférence sur le GAP8 ; filtre de Kalman, contrôle
  en vitesse et PID en cascade (100/500 Hz) sur le STM32F405. La pose passe par UART (§IV-D,
  Fig. 5).

## Plateforme et implémentation

- **Puce** : GreenWaves **GAP8** (1 fabric controller + cluster de 8 cœurs RISC-V RI5CY,
  L2 de 512 kB, L1 de 64 kB), sur l'AI-deck de Bitcraze (4,4 g, HyperRAM 64 Mbit,
  HyperFlash 512 Mbit, caméra Himax HM01B0 QVGA monochrome). Hôte : STM32F405 à 168 MHz
  (§III).
- **Gamme de puissance : nano (mW).** La puissance est mesurée **après le convertisseur
  DC/DC interne**, séparément pour les domaines FC et CL (Fig. 9) : puissance **puce**
  (SoC), sans caméra, sans STM32, sans moteurs → `power_scope = chip`.
- Balayage des fréquences FC/CL par pas de 25 MHz, avec la tension VDD associée (Fig. 7).
- Code, jeu de données : **non mentionnés** dans le texte extrait (des outils open source
  sont utilisés : NEMO, DORY, PULP-NN). Une vidéo supplémentaire est évoquée (§I).

## Résultats

- **Débit/puissance du SoC** (§V-B, Fig. 10) : 80×32 au pic, **134,7 fps pour 86,6 mW** ;
  160×16 à fréquence max (FC 250 MHz, CL 175 MHz), 110,7 fps pour 99 mW ; 80×32 à puissance
  minimale, 18,5 fps pour 8,6 mW. Aux points les plus efficaces, les trois réseaux
  consomment ~20 mW, et 80×32 est 2,5× plus rapide que 160×32 et 1,7× plus que 160×16.
- **Énergie par image** (§V-B, Fig. 7) : 1,28 mJ (160×32), 0,58 mJ (160×16), **0,43 mJ**
  (80×32).
- **Régression hors ligne** : MAE ~0,2 m sur x et y pour tous les modèles (§V-A). Les
  versions quantifiées sont équivalentes au FP32 « within noise margins » (Fig. 8).
  Le détail est dans la Table III, **absente de l'extraction**.
- **En vol** (Table IV, 2 sujets inconnus, 3 runs par réseau et par sujet, plus 1 run
  mocap ; 18 runs avec CNN au total) :

| Réseau | Taux contrôleur (Hz) | R² x / y / θ | e_xy médian (m) | e_θ médian (°) |
|---|---|---|---|---|
| 160×32 | 48 | 0,87 / 0,87 / 0,71 | 0,41 | 3,7 |
| 160×16 | 111 | 0,93 / 0,82 / 0,56 | 0,61 | 4,7 |
| 80×32 | 135 | 0,88 / 0,75 / 0,54 | 0,63 | 4,0 |
| mocap (vérité terrain) | 30 | 1,00 | 0,26 | 4,1 |

Taux de succès annoncé : 100 % (§I, contributions).

→ reportés dans `benchmarks.csv` : 3 lignes, `power_scope = chip`, confidence `medium`
(chiffres lus dans le texte de §V-B, qui commente la Fig. 10) : 80×32 au pic (134,7 fps,
0,0866 W), 160×16 à fréquence max (110,7 fps, 0,099 W), 80×32 à puissance minimale
(18,5 fps, 0,0086 W). Pas de ligne pour 160×32 : ni fps d'inférence ni puissance explicites
dans le texte, seulement le taux du contrôleur (48 Hz, Table IV). La précision est laissée
à `n/r` : la tâche est une régression (MAE, R²), sans métrique compatible avec la colonne.

## Limites et critique

- **Puissance puce seulement.** Les 86,6 mW excluent la caméra, le STM32, l'AI-deck
  entier et surtout les moteurs du Crazyflie (plusieurs W, déduit). Le papier ne donne pas
  l'impact sur l'autonomie de vol.
- **Tâche de régression, pas de détection.** Les chiffres ne se comparent pas à ceux d'un
  YOLO. Le CNN fait 4 MMAC, contre plusieurs GMAC pour un détecteur (déduit).
- **Baseline biaisée à l'avantage du papier :** le Proximity NN tourne sur GPU de bureau
  en FP32 ; la comparaison porte sur MAC et mémoire (24× moins d'opérations, 33× moins de
  mémoire), pas sur une implémentation optimisée concurrente.
- **Évaluation en vol limitée :** 2 sujets, une salle de 10×10 m, un parcours imposé au
  métronome (§V-C). La généralisation à d'autres environnements n'est pas testée.
- La Fig. 10 porte l'essentiel des chiffres de puissance ; seuls quelques points sont
  repris dans le texte.
- Le réseau le plus rapide n'est pas le meilleur en vol : 160×32 à 48 Hz donne l'erreur
  de position la plus faible (Table IV). Le débit maximal n'est donc pas la bonne cible,
  ce que le papier montre sans l'énoncer comme tel (déduit).

## Pertinence pour la thèse

- **Référence de l'axe `nano-drone`** : méthodologie complète perception → contrôle sur
  GAP8 (QAT NEMO, DORY, PULP-NN), avec une **analyse du compromis taille du réseau ↔
  énergie ↔ qualité de contrôle en boucle fermée**. C'est une rare métrique système
  (erreur de suivi en vol), celle qui manque aux papiers YOLO/FPGA.
- Donne l'ordre de grandeur de la **gamme nano** : ~0,4 mJ/image et 10 à 100 mW pour
  4 MMAC. C'est le point de comparaison bas face aux FPGA (W) et aux Jetson (~10 W).
- Montre que l'augmentation « pitch » est nécessaire quand la caméra n'est pas
  stabilisée : c'est un effet du vol sur la perception, transposable à la détection
  embarquée.
- Ne traite pas la détection d'objets, ni le contre-drone. Voir
  `arxiv-2407.02405-tiny-pulp-dronets-squeezing-neural` pour la suite de la lignée PULP.

## Gaps identifiés

- **Débit ≠ qualité de contrôle :** le réseau à 135 Hz suit moins bien que celui à 48 Hz
  (Table IV). Aucune étude ne relie fps, latence et précision de détection à la performance
  de vol pour un détecteur embarqué (à étayer).
- **Puissance du système entier non mesurée :** SoC seulement, jamais la part du calcul
  dans la consommation totale du drone.
- **Détection multi-objets sur GAP8** absente de ce papier (régression mono-cible).

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). Manques de
l'extraction : la **Table I** (taxonomie des drones par taille) et la **Table III**
(MAE/MSE par variable et par réseau) n'ont pas de corps extrait ; la section I (fin de
l'introduction) est fusionnée avec l'abstract ; la Fig. 10 n'est lue qu'à travers le texte.
La description de la variante 160×32 (§IV-A) est tronquée.

Métadonnées : `metadata.json` donne « arXiv preprint ». Le travail a vraisemblablement été
publié ensuite dans IEEE Internet of Things Journal (non vérifié ici, à confirmer avant
citation).

Ce qui suit est déduit et non affirmé par les auteurs :
- la consommation des moteurs (plusieurs W), l'absence d'effet mesuré sur l'autonomie ;
- l'écart de complexité avec un détecteur YOLO ;
- la lecture « débit maximal ≠ meilleure qualité de contrôle » de la Table IV ;
- la publication probable en journal.
