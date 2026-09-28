---
id: arxiv-2301.12175-bio-inspired-autonomous-exploration-policies
fiche: done
date: 2026-09-28
---

# Bio-inspired Autonomous Exploration Policies with CNN-based Object Detection on Nano-drones

Lorenzo Lamberti, Luca Bompani, Victor Javier Kartsch, Manuele Rusci, Daniele Palossi, Luca Benini, 2023, arXiv preprint. https://arxiv.org/abs/2301.12175
Type : preprint non relu par les pairs selon `metadata.json`. Une version DATE 2023 est
probable mais non confirmée par le texte extrait : à vérifier.

## Problème

Mener une mission **multi-objectifs** (exploration, évitement d'obstacles, détection
d'objets) entièrement à bord d'un nano-drone de moins de 10 g de charge utile, dont
l'électronique ne dispose que de 5 à 10 % du budget de puissance total (Abstract, §I).
Selon les auteurs, c'est le premier nano-drone totalement autonome sur ce type de mission
(§I, §V).

## Méthode

- **Partage des tâches entre deux MCU** (host-accelerator, §III-B) :
  - STM32F405 (Cortex-M4, moins de 100 MMAC/s) : contrôle de vol et politique
    d'exploration, une machine d'états sur les capteurs ToF ;
  - GAP8 (environ 1 GMAC/s) : acquisition caméra et CNN de détection. Aucune interaction
    entre les deux tâches.
- **Quatre politiques bio-inspirées** sur 3 ToF VL53L1x (§III-C) : pseudo-aléatoire
  (virage aléatoire de plus de 90° à 1 m d'un obstacle), wall-following (à 0,5 m du mur),
  spirale, rotate-and-measure.
- **Détecteur** : SSD + MobileNetV2 à trois largeurs (1,0×, 0,75×, 0,5×), pré-entraîné
  sur OpenImages ; 2 classes (bouteille, canette), images 320 × 240 en niveaux de gris
  (§III-D, §IV-A). Fine-tuning sur un « Himax Dataset » propre (321 images
  d'entraînement, 279 de test) pour combler l'écart de domaine avec la caméra embarquée.
- **Quantification INT8** par QAT (TensorFlow Object Detection API, plages symétriques),
  puis génération de code C par **GAPflow** (GreenWaves), avec un buffer L2 limité à
  250 kB (§III-D).

## Plateforme et implémentation

- Crazyflie 2.1 (27 g, 10 cm) + Flow deck + Multi-ranger deck (5 ToF, 0-4 m, 20 Hz) +
  AI-deck (§III-A).
- **GAP8** : 8 cœurs RISC-V, jusqu'à 175 MHz, 64 kB de L1 et 512 kB de L2. AI-deck avec
  caméra Himax HM01B0 QVGA en niveaux de gris, 8 MB de HyperRAM et 64 MB de HyperFlash.
  Réglage des mesures : cluster à 160 MHz sous 1,2 V, périphériques à 250 MHz (§IV-A).
- **Puissance** : mesurée composant par composant avec un Nordic Power Profiler Kit 2
  (§IV-C, Table IV). L'AI-deck consomme 134,5 mW avec SSD 1,0× et culmine à 143,5 mW
  avec SSD 0,75× (Table II, texte). L'Abstract précise que les 134 mW incluent capteur
  d'image et mémoires externes : c'est une puissance **à la carte AI-deck**
  (`power_scope: board`).
- Code : non mentionné dans le texte extrait.

## Résultats

- **Détecteurs sur GAP8** (Table II) :

| SSD | Param. | MMAC | MAC/cycle | FPS | mAP Himax INT8 | P AI-deck |
|---|---|---|---|---|---|---|
| 1,0× | 4,7 M | 534 | 5,3 | 1,6 | 50 % | 134,5 mW |
| 0,75× | 2,7 M | 358 | 5,9 | 2,3 | 48 % | 143,5 mW |
| 0,5× | 1,2 M | 193 | 5,3 | 4,3 | n/r | n/r |

  mAP au sens COCO. Le modèle 1,0× atteint 59 % sur OpenImages, perd 9 points sur les
  images Himax, remonte à 55 % après fine-tuning, puis 50 % en INT8 (§IV-A). La Table I
  n'est pas extraite.
- **Exploration** (§IV-B, Fig. 5) : 60 vols de 3 min dans une pièce de 6,5 × 5,5 m
  (143 cellules). Couverture du pseudo-aléatoire : 35 % → 74 % → 80 % à 0,1, 0,5 et
  1 m/s ; de la spirale : 35 % → 82 % → 83 %. L'Abstract attribue les 83 % au
  pseudo-aléatoire, le §IV-B à la spirale : incohérence interne.
- **Boucle fermée** (Table III) : taux de détection moyen de **90 %** (6 objets, 5 vols)
  avec pseudo-aléatoire, SSD 1,0× et 0,5 m/s. À 1 m/s, il tombe à 83 %. Le SSD 1,0× est
  toujours meilleur ou égal au 0,75×, pourtant plus rapide : la précision prime sur le
  débit dans ce cadre (§IV-C).
- **Bilan de puissance** (Table IV) : moteurs 7,32 W (91,31 %), électronique du
  Crazyflie 0,277 W, AI-deck 0,134 W (1,67 %), Multi-ranger 0,286 W ; total 8,02 W.

→ reportés dans `benchmarks.csv` (fichier du lot) : 3 lignes, une par largeur de SSD sur
GAP8 (Table II). Le mAP INT8 vient du texte (§IV-A), d'où `medium` pour les deux
premières lignes ; mAP n/r pour le 0,5×.

## Limites et critique

- **Détection simple** : 2 classes d'objets posés au sol, dans une pièce de 36 m², avec
  6 objets. Le mAP de 50 % est mesuré sur 279 images propres. Rien de comparable à
  VisDrone ou à des petits objets en extérieur.
- **1,6 FPS** : le débit limite directement la vitesse de vol utile. Le taux de détection
  baisse à 1 m/s (§IV-C). Les auteurs le constatent, sans modèle explicite de ce lien.
- **Latence** non rapportée (seulement un débit) ; le détail de l'énergie par inférence
  n'est pas donné.
- **Baseline externe faible** : RPi 3B+ à 0,71 FPS et jusqu'à 3 W [20], sur un autre jeu
  et un autre drone. Aucune comparaison avec un GAP9 ou un MCU à NPU.
- La Table IV est essentielle mais agrège : on ne sait pas si la puissance des moteurs
  dépend de la politique ou de la vitesse. Mesure de puissance faite par composant, hors
  vol probablement (déduit : l'instrument PPK2 suggère une mesure au banc).
- Détection par vol seul (5 runs) avec une forte variance de couverture (21 %, Fig. 6).

## Pertinence pour la thèse

- **Référence de la gamme nano (mW)** pour l'axe `nano-drone` : 134 mW pour la vision,
  soit 1,67 % du budget total de 8 W dominé par les moteurs (Table IV). C'est un chiffre
  clé pour l'axe `system-codesign` : sur un nano-drone, **le calcul de vision pèse peu
  en puissance**, mais son débit limite la vitesse de vol et donc l'efficacité de mission.
- Le résultat « précision > débit » (Table III) et la dépendance à la vitesse de vol sont
  une première ébauche de métrique système (taux de détection de mission), justement ce
  qui manque aux papiers YOLO/FPGA (hypothèse de `gaps.md`).
- Chaîne complète QAT → GAPflow → GAP8 reproductible sur Crazyflie + AI-deck, matériel
  commercial.

## Gaps identifiés

- **Modèle explicite débit de détection ↔ vitesse de vol ↔ couverture** : observé ici
  (Table III), pas formalisé.
- **Part du calcul dans le budget énergétique** : 1,67 % sur nano-drone (Table IV) ; à
  comparer avec un FPGA (W) sur un drone de taille moyenne, où la part n'est pas mesurée
  dans les papiers FPGA (à étayer).
- **Petits objets / scènes réelles sur nano-drone** : non traités (2 classes en intérieur).

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). La Table I (mAP des
trois modèles sur OpenImages et Himax, avant et après quantification) n'a pas de corps
extrait : seuls les chiffres cités au §IV-A sont connus, d'où mAP n/r pour SSD 0,5×. La
Table IV est bien extraite malgré l'avertissement de `extraction.warnings`. La phrase
sur la vitesse relative des petits modèles est coupée au §IV-A et reprise sous la Table II.
Le §III-D est tronqué au milieu d'une phrase (« detection heads, which … predicts »).

Ce qui suit est déduit et non affirmé par les auteurs :
- la portée `board` de la puissance (AI-deck entier : l'Abstract inclut capteur et
  mémoires externes) ;
- la mesure au banc plutôt qu'en vol ;
- la venue DATE 2023.
