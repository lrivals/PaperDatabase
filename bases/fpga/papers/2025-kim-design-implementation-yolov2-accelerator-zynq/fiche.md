---
id: 2025-kim-design-implementation-yolov2-accelerator-zynq
fiche: done
date: 2026-09-29
---

# Design and Implementation of a YOLOv2 Accelerator on a Zynq-7000 FPGA

Huimin Kim, Tae-Kyoung Kim, 2025, Sensors (MDPI) 25(20), 6359 (venue et type déduits de la forme du DOI, `metadata.json` ne les donnait pas). https://doi.org/10.3390/s25206359
Type : article de journal (déduit du DOI MDPI Sensors, à confirmer)

## Problème

Les accélérateurs YOLO sur FPGA visent surtout des SoC haut de gamme ; les auteurs veulent une architecture légère qui tienne sur un SoC bas de gamme, le Zynq-7000 XC7Z020 (53 200 LUT, 106 400 FF, 630 KB de BRAM, 220 DSP) (§1.1, §3.1). YOLOv2 est choisi parce que ses blocs (convolutions 3x3 et 1x1, max pooling) subsistent dans les versions suivantes (§1.1).

## Méthode

- Architecture à fenêtre glissante (pas GEMM), écrite en Verilog RTL : 6 contrôleurs, 9 unités de traitement, FSM du contrôleur principal Idle / Start / MP / Conv / Done (§2, §3.7).
- Quantification INT16 (PTQ), un MAC par DSP (§3.1, §4).
- Réutilisation des filtres en BRAM (25,6 KB) et de l'IFM par line buffer (153,6 KB de BRAM de réutilisation) (§1.1, §3.2-3.3).
- Paramètres de tiling choisis par analyse de ressources : convolution 3x3 Tr = 3, Tc = 15 ; 1x1 Tr = 1, Tc = 13 ; max pooling Tr = 2, Tc = 52 (§3.4-3.5, Tables 5-6).
- Contrôleur Acc_Lock à base de stall qui surveille l'occupation des BRAM d'OFM pour éviter des aléas structurels (§3.6).
- Couches de concaténation et de détection exécutées sur le PS (Cortex-A9) sous PetaLinux (§4.2). Vivado 2023.2. Pas de toolflow HLS : custom RTL.

## Plateforme et implémentation

Carte Zybo Z7-20 (XC7Z020, ARM Cortex-A9 double coeur), horloge PL 100 MHz, présentée comme fréquence maximale atteignable (§4.1). Ressources (Table 8) : 26 147 LUT (49,15 %), 17 605 FF (16,55 %), 98 BRAM 36 Kb (70,00 %), 126 DSP (57,27 %). Puissance : 2,035 W au total « après implémentation », PS7 1,408 W, BRAM 0,269 W (§4.1, Fig. 12) ; méthode de mesure non décrite (une estimation d'outil est plausible, déduit) : portée `unspecified`. Code ou bitstream : non publiés d'après le texte.

## Résultats

- Écart de précision INT16 contre FP32 hôte PC d'environ 0,2 % sur les scores de détection (COCO : kite 64,7 % contre 64,9 %, person 58,1 % contre 58,3 %, 57,7 % contre 57,9 %) (§4.2) ; UA-DETRAC : bus 93,4 contre 93,6, van 89,5 contre 89,7, car-max 90,8 contre 91,0, car-min 54,1 contre 54,3 (Fig. 14, texte). Ce sont des scores sur des images d'exemple, pas un mAP sur un jeu complet.
- Temps : 12,02 s jusqu'à la couche de détection, 12,64 s au total sur COCO 416x416 (§4.2) ; Table 9 : latence 12 639 ms, 2,33 GOPS, 0,018 GOPS/DSP, énergie 25 720,37 mJ (Table 9, reconstruit par Docling, à vérifier). UA-DETRAC : 12,42 s dont 11,80 s avant la couche de détection (Fig. 14, texte).
- Comparaison sur le même XC7Z020 (Table 9) : [41] YOLOv4-Tiny 0,4 GOPS ; [42] YOLOv3-Tiny 10,5 GOPS ; [43] YOLOv3 62,9 GOPS ; FF et DSP inférieurs de jusqu'à 26 % et 15 % (§4.3). Le texte reconnaît une latence bien supérieure et l'absence de parallélisme multi-filtres (§4.4).
→ reportés dans `benchmarks.csv` : 2 lignes (COCO ; UA-DETRAC), dans `bench_rows.csv`.

## Limites et critique

- Débit très faible : 12,64 s par image 416x416 (soit moins de 0,1 FPS, déduit), 2,33 GOPS pour 126 DSP ; inutilisable en vidéo temps réel. La « réduction de 26 % de FF et 15 % de DSP » est obtenue contre des designs beaucoup plus rapides (10,5 à 62,9 GOPS) et pour un autre modèle : la comparaison porte sur la surface, pas sur l'efficacité, et les modèles diffèrent (YOLOv2 à 29,5 GFLOPs contre 5,6 à 19,5) (Table 9).
- Précision mesurée sur quelques détections d'exemple, non sur un mAP complet ; la cellule mAP de la Table 9 pour ce travail est illisible (48,1 apparaît dans une cellule ambiguë) : `n/r` retenu.
- Puissance : mesure ou estimation non précisée ; pas de comparaison à un GPU ou Jetson (que le résumé évoque pourtant comme motivation).
- Les couches concat et détection tournent sur le PS : latence de bout en bout non isolée pour ces étapes.
- Résultats de UA-DETRAC : entraînement/jeu de données peu décrits.
- Table 9 reconstruite automatiquement : chiffres à vérifier ; code non publié.

## Pertinence pour la thèse

Pertinence moyenne, comme cas d'étude d'accélérateur YOLO RTL sur SoC très contraint, avec des données de ressources et d'énergie exploitables. Le jeu UA-DETRAC (véhicules) est éloigné du cas personnes en zone industrielle. Aucune considération de sûreté, de déterminisme mesuré ou de certification, alors qu'une FSM déterministe et un pipeline à stall sont des éléments plutôt favorables à l'analyse de comportement temporel (déduit, non affirmé par les auteurs). Reste ouvert : débit temps réel, YOLO récents, sûreté.

## Gaps identifiés

- Accélérateurs YOLO sur FPGA de faible coût atteignant un débit vidéo, avec compromis surface/latence.
- Absence de toute évaluation de fiabilité (SEU) ou de traçabilité sur cette architecture.
- Mesure de puissance de portée non précisée (comparabilité).

## Statut de lecture

Papier complet (texte extrait lu en entier). Tables 2, 3, 4, 6, 9 reconstruites par Docling : chiffres à vérifier ; la Table 9 a des cellules mal alignées (mAP de ce travail illisible). Déduit et non affirmé par les auteurs : FPS inférieur à 0,1, nature de la mesure de puissance, venue et type via le DOI, remarques sur la sûreté et la pertinence pour la thèse.
