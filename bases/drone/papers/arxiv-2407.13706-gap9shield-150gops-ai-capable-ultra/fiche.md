---
id: arxiv-2407.13706-gap9shield-150gops-ai-capable-ultra
fiche: done
date: 2026-10-01
benchmarks: none
---

# GAP9Shield: A 150GOPS AI-capable Ultra-low Power Module for Vision and Ranging Applications on Nano-drones

Hanna Müller, Victor Kartsch, Luca Benini, 2024, arXiv preprint. https://arxiv.org/abs/2407.13706
Type : preprint non relu par les pairs (papier court de présentation de matériel)

## Problème

Le deck AI (GAP8 + caméra Himax HM01B0 QVGA monochrome) du Crazyflie est insuffisant hors environnement contrôlé : caméra basse résolution en niveaux de gris, GAP8 limité en calcul flottant, mémoire et fréquence (Intro). Il faut aussi combiner télémétrie (obstacle avoidance) et vision haute résolution dans un seul module, plus léger (Intro).

## Méthode

Pas d'algorithme nouveau : conception d'un shield enfichable sur Crazyflie (PCB 6 couches 50x27 mm, Fig. 1) autour du SoC GAP9 (GreenWaves), avec une caméra OV5647 5 MP (interface CSI-2), un module WiFi/BLE NINA-W102 (ESP32 ; WiFi et SPI répartis sur les deux coeurs) et un réseau de 5 capteurs ToF VL53L1 (droite, gauche, avant, arrière, haut). La section 3.2 ne fait que rappeler des résultats d'autres travaux ([5], [6], [7]) exécutés sur GAP9 (YOLO, MCL, NanoSLAM).

## Plateforme et implémentation

- SoC GAP9 : cluster RISC-V 9 coeurs avec accélérateur IA NE16, virgule flottante transprécision (FP32, FP16, bfloat16), contrôleur RISC-V mono-coeur, 330 µW/GOP, 15,6 GOPS (DSP) et 32,2 GMACs (ML), fréquence jusqu'à 370 MHz, veille 45 µW, 1,6 MB de L2 et 2 MB de mémoire non volatile en boîtier (§2.1). Ajouts sur la carte : PSRAM APS256XXN-OBR 256 Mbit, flash MX25UM51245GXDI00 512 Mbit (§2.1). Le chiffre « 150 GOPS » du titre n'est pas détaillé dans le texte extrait.
- Poids ~6 g, volume ~4050 mm3 (§3.1).
- Gamme de puissance : nano-drone, quelques dizaines à centaines de mW.
- Code / matériel : les auteurs « prévoient » de publier schémas et PCB (Intro) ; non publiés à la lecture, aucun lien.

## Résultats

Mesures propres du shield (§3.1), toutes sans méthode de mesure de puissance décrite :
- Masse et taille : ~15 % plus léger et 30 % plus petit en volume que AI-deck + Multi-ranger (7 g, 6480 mm3, note 3) (§3.1). L'abstract et l'introduction annoncent 20 % de réduction de poids : incohérent avec 6 g vs 7 g (~14 %).
- Ranging VL53L1 : ~40 SPS atteints, puissance max 150 mW (§3.1).
- OV5647 : 15 fps en QVGA (limité par un problème de driver), 45 fps en VGA ; 80 mW (QVGA 15 fps) et 120 mW (VGA 45 fps) (§3.1).
- WiFi : 8 Mbit/s en TCP (~250 mW), 12 Mbit/s en UDP (~260 mW) (§3.1). Streaming JPEG RGB QVGA via TCP ~7 FPS (~20 % de plus que l'AI-deck) et 4 FPS en VGA (§3.1).

Résultats rapportés d'autres travaux sur GAP9 (§3.2, non mesurés ici) :
- YOLOv5 modifié [5] : 38 ms, 2,5 mJ (prototype antérieur du shield).
- Plus petit YOLO « de précision acceptable » [6] : 17 ms, 1,59 mJ.
- MCL [5] : 23 mW en moyenne, à 15 Hz (ToF/odométrie) et 5 Hz (caméra).
- NanoSLAM [7] : 87,9 mW, moins de 250 ms.

→ reportés dans `benchmarks.csv` : aucune ligne. Les chiffres de détection, MCL et SLAM viennent de travaux cités ([5], [6], [7]), pas de ce papier ; les mesures propres (caméra, WiFi, ToF) ne sont pas des performances de modèle (fps de capteur, pas d'exactitude, ni de jeu de données). D'où `benchmarks: none`.

## Limites et critique

- Papier de présentation matériel court : aucun chiffre de détection, de précision ni de jeu de données ; les 17 ms / 1,59 mJ proviennent de [6] sans précision de modèle, de résolution ni de mAP.
- Les chiffres « sous 100 mW » ne sont ni mesurés sur le système complet en vol, ni accompagnés d'une méthode (puce vs carte). Le consommation du shield complet (WiFi 250 mW, caméra, ToF 150 mW) dépasse largement 100 mW : le « sous 100 mW » ne vaut que pour le SoC pendant l'exécution de l'algorithme (déduit).
- Incohérences internes : latence « 17 ms » (abstract) vs « 18-250 ms » (Intro) ; réduction de poids 20 % vs 15 % ; QVGA à 15 fps seulement (driver), donc 20 % de FPS en plus que l'AI-deck concerne le streaming WiFi, pas l'acquisition.
- Aucune comparaison avec le coût énergétique du shield en vol (autonomie, effet de 6 g sur la batterie) : l'amélioration « vol / batterie » est affirmée, pas mesurée.
- Pas de baseline Jetson ou GPU (hors gamme, nano-drone), ce qui est cohérent avec la gamme visée.
- Preprint, matériel non encore ouvert.

## Pertinence pour la thèse

Axe `nano-drone` : plateforme de référence GAP9 (successeur de GAP8) pour la vision embarquée en gamme mW, avec capteurs de distance intégrés. Utile pour situer la gamme nano (< 100 mW SoC) face aux gammes FPGA (W) et Jetson (~10 W). Elle ne fournit pas de résultat de détection propre ; ce sont les papiers [5], [6], [7] qu'il faut lire pour les chiffres.

## Gaps identifiés

- Aucun résultat YOLO/mAP_small mesuré sur nano-drone dans ce papier ; l'effet de la quantification (NE16) sur les petits objets n'est pas évalué.
- Aucune métrique système (autonomie, masse vs temps de vol) mesurée avec le shield.
- Mesures de puissance sans portée ni méthode, difficiles à comparer à celles des autres plateformes.

## Statut de lecture

Papier complet (fulltext.md lu en entier, ~12 ko). Extraction `pymupdf`, `ok: false` : texte probablement correct mais métadonnées à vérifier, la Fig. 1 (schéma) n'est pas lisible et le tableau éventuel n'existe pas. Le « 150 GOPS » du titre n'est pas justifié dans le texte (le texte donne 15,6 GOPS DSP et 32,2 GMACs ML).
Ce qui suit est déduit et non affirmé par les auteurs : que le « sous 100 mW » concerne le SoC seul ; l'incohérence poids 14 % vs 15 % vs 20 % ; la comparaison de gamme avec FPGA et Jetson.
