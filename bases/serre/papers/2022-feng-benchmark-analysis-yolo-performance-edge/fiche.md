---
id: 2022-feng-benchmark-analysis-yolo-performance-edge
fiche: done
date: 2026-10-29
---

# Benchmark Analysis of YOLO Performance on Edge Intelligence Devices

Haogang Feng, Gaoze Mu, Shida Zhong, Peichang Zhang, Tao Yuan, 2022, Cryptography 6(2), 16. https://doi.org/10.3390/cryptography6020016
Type : article de journal (MDPI *Cryptography*, venue inattendue pour ce sujet)

## Problème

Les auteurs veulent mesurer concrètement ce que des cartes mono-carte (SBC) équipées
d'accélérateurs peuvent faire tourner comme détecteur YOLO, au lieu d'en rester à des
modèles « edge » discutés à un niveau théorique (§1). Question posée : FPS, mémoire, CPU
et énergie de quatre YOLO sur trois SBC grand public.

## Méthode

- Modèles : YOLOv3, YOLOv3-tiny, YOLOv4, YOLOv4-tiny, poids pré-entraînés COCO du site
  Darknet, sans réentraînement (§3.3).
- Précision : FP16 partout, parce que le Jetson Nano ne supporte que le FP16 (§3.3.1).
- Chaîne logicielle :
  - Jetson : Darknet compilé sur la carte, GPU, **sans TensorRT**, choisi exprès pour rester
    comparable au RPi (§3.2) ;
  - RPi + NCS2 : Darknet → TensorFlow PB → IR OpenVINO FP16 (Model Optimizer) (§3.3).
- Données : deux vidéos téléchargées sur gitee (§4) : Video1 (1596 images, 768×436, une
  personne) et Video2 (960 images, 1920×1080, une salle de classe avec quatre personnes).
  Chaque mesure est la moyenne de 10 passes.
- Résolution d'entrée : S = 416 pour la comparaison entre cartes (Table 3), S = 320 / 608
  sur Nano seulement (Table 5).
- Mesures : FPS, CPU (%), mémoire (GB), puissance (W), temps (s). Outils : JTOP sur les
  Jetson, `top` et un « USB dynamometer » sur le RPi (§4).

## Plateforme et implémentation

| Carte | Accélérateur | Mémoire | Enveloppe nominale | Prix |
|---|---|---|---|---|
| Jetson Nano | GPU Maxwell 128 cœurs (0,5 TFLOPs) | 4 GB LPDDR4 | 5-10 W | 89 $ |
| Jetson Xavier NX (mode 15 W, 6 cœurs) | GPU Volta 384 cœurs + 48 Tensor Cores (1,3 TFLOPs) | 8 GB LPDDR4x | 10-15 W | 399 $ |
| Raspberry Pi 4B + Intel NCS2 | Myriad X VPU via USB 3.0 (1 TFLOPs) | 4 GB LPDDR4 | 3-6,25 W + 1 W | 55 + 69 $ |

(Table 2 ; ce sont des spécifications constructeur reprises par les auteurs, pas des mesures.)

Puissance à vide mesurée (Table 4) : RPi + NCS2 3,16 W (NCS2 seul : 0,64 W), Nano 2,60 W,
Xavier NX 3,15 W.

Portée de la puissance : la méthode n'est pas décrite au-delà des outils (JTOP, wattmètre
USB). On ne sait pas quels rails JTOP additionne, ni où le wattmètre USB est branché. →
`power_scope = unspecified`. Les Tables 5 et 6 ne donnent que la puissance du **GPU seul**
(3,3-4,0 W), une portée différente de celle de la Table 3 : je ne l'ai pas reportée dans
`power_w`.

Code et scripts : non publiés. Vidéos : sur gitee [44], sans lien direct dans le texte extrait.

## Résultats

Table 3 (S = 416, FP16) :

| Modèle | Vidéo | RPi + NCS2 : FPS / W | Nano : FPS / W | Xavier NX : FPS / W |
|---|---|---|---|---|
| YOLOv3 | Video1 | 2,5 / 6,0 | 1,7 / 7,9 | 6,1 / 15,2 |
| YOLOv3-tiny | Video1 | 18,8 / 6,5 | 6,8 / 7,2 | 41,1 / 13,5 |
| YOLOv3 | Video2 | 2,5 / 6,2 | 1,6 / 8,0 | 5,9 / 15,2 |
| YOLOv3-tiny | Video2 | 19,0 / 6,8 | 6,6 / 7,4 | 35,6 / 13,2 |

- Xavier NX est la plus rapide dans tous les cas ; Nano est la plus lente (§4.1).
- La taille de la vidéo change peu le FPS (§4.1).
- YOLOv3-tiny avec Video1 sur RPi + NCS2 : **confiance moyenne 0 %** contre 59,7 % sur les
  Jetson (Table 3). Les auteurs l'attribuent à la conversion OpenVINO, qui coupe puis recolle
  les couches Region de Darknet (§4.1, §5).
- Mémoire : sous YOLOv3-tiny avec Video1, Nano et NX occupent respectivement 9× et 12× plus
  de mémoire que RPi + NCS2 (§4.1.2, Fig. 5).
- Énergie : Xavier NX consomme le plus en puissance mais le moins en énergie par vidéo,
  parce qu'elle finit plus vite. Nano est la moins sobre (§4.1.3, Fig. 6).
- Sur Nano (Table 5), passer de S = 320 à S = 608 divise le FPS par environ 3 (YOLOv3-tiny,
  Video1 : 10,3 → 3,3 FPS).
- Sur Nano (Table 6), YOLOv4-tiny à S = 416 donne 15,0 FPS (Video1) et 14,2 FPS (Video2).
- Les auteurs avancent un gain d'environ ×2 avec TensorRT (§4.2), mais le reprennent d'une
  référence [45] **sans le mesurer**.

→ lignes de `benchmarks.csv` : 24, déjà présentes (reprises à l'import depuis `drone`), aucune ajoutée ici
- 12 lignes de la Table 3 (3 cartes × 2 modèles × 2 vidéos). Quatre sont en
  `confidence: medium` (NX YOLOv3 et RPi YOLOv3-tiny, pour les deux vidéos) : l'extraction
  avait fusionné leurs cellules et je les ai reconstituées dans l'ordre des colonnes, en
  recoupant avec le texte (§4.1).
- 8 lignes de la Table 5 (Nano, S = 320 / 608), FPS seulement.
- 4 lignes de la Table 6 (Nano, YOLOv4 / YOLOv4-tiny).

## Limites et critique

- **Aucune mesure de précision.** La « mean confidence » est la moyenne des scores de
  confiance des détections (§4.1), pas une mAP : il n'y a ni vérité terrain, ni jeu
  d'évaluation standard. Elle ne se compare pas aux mAP COCO des papiers FPGA. Dans
  `benchmarks.csv`, `accuracy_metric` le signale.
- **Jetson bridés.** Sans TensorRT et en FP16, alors que Xavier NX supporte l'INT8 (§3.3.1),
  le FPS des Jetson est très en dessous de ce qu'elles font en pratique. La comparaison est
  équitable entre cartes, mais ces chiffres ne servent pas de baseline « état de l'art
  Jetson » face à un FPGA.
- **FPS de bout en bout** sur des vidéos (décodage, redimensionnement et affichage
  compris). Pas de latence d'inférence isolée, pas de batch déclaré.
- **Puissance hétérogène :** JTOP côté Jetson, wattmètre USB côté RPi, portée non décrite.
  Les chiffres « Power » (Table 3) et « GPU Power » (Tables 5-6) ne se comparent pas.
- **Deux vidéos seulement**, dont une avec une seule personne, sans lien de téléchargement
  exploitable dans le texte extrait.
- **Incohérence possible** dans la colonne « Time » de la Table 3 : 960 images à 19,0 FPS
  devraient prendre environ 50 s, mais la table indique 162 s pour RPi + NCS2 avec
  YOLOv3-tiny et Video2. C'est peut-être une erreur de l'extraction ou du papier : à
  vérifier sur le PDF (déduit).
- Pas de FPGA, alors que le titre parle d'edge en général. Les auteurs l'annoncent en
  travaux futurs (§5).

## Pertinence pour SerreIA

Lecture secondaire : le papier ne contient ni Hailo, ni RPi 5, ni détection de feuilles. Il
sert de **repère d'ordre de grandeur** (SBC bas coût, YOLO COCO) et de **contre-exemple de
méthode**, pas de baseline chiffrée pour le Hailo-8L. Les modèles (YOLOv3/v4, FP16, Darknet)
sont d'une autre génération que le YOLOv8n INT8 visé.

- Point à retenir pour le HEF : la conversion vers un accélérateur dédié peut dégrader
  silencieusement la détection (confiance moyenne 0 % pour YOLOv3-tiny / Video1 sur RPi + NCS2,
  Table 3, 2022-feng#027.0 ; cause : coupure des couches Region par OpenVINO, 2022-feng#017.0).
  Cela justifie le critère de `05-edge-deploiement.md` (écart HEF vs ONNX < 2 points sur `test`
  et `test_xdomain`) : mesurer la précision sur la cible, pas seulement le FPS.

## Pour SerreIA

**Plateformes et chiffres de référence (hors Hailo).** Seul repère proche d'un RPi + NPU USB :
RPi 4B + Intel NCS2 (Myriad X, FP16), YOLOv3-tiny S = 416 : 18,8 à 19,0 FPS pour 6,5 à 6,8 W
(Table 3, 2022-feng#027.0) ; YOLOv3 : 2,5 FPS pour 6,0 à 6,2 W. Jetson Nano, même modèle :
6,6 à 6,8 FPS, 7,2 à 7,4 W ; Xavier NX : 35,6 à 41,1 FPS, 13,2 à 13,5 W. Puissance à vide :
RPi + NCS2 3,16 W, Nano 2,60 W, NX 3,15 W (Table 4, 2022-feng#028.0). À prendre comme plancher
« génération 2020 » : le Hailo-8L (13 TOPS INT8) n'est pas comparable en débit, et aucun de ces
chiffres ne remplace une mesure `hailortcli benchmark` sur le Pi 5.

**Conditions de mesure à reprendre (ou à ne pas reprendre).**
- Résolution : S = 416 pour la comparaison entre cartes, 320 / 608 sur Nano seulement : le FPS
  est divisé par environ 3 de 320 à 608 (YOLOv3-tiny, Table 5). SerreIA doit fixer sa
  résolution d'entrée (YOLOv8n de feuilles, puis crops 224 × 224 pour EfficientNet-B0) et la
  noter avec chaque chiffre.
- Données : deux vidéos de 768 × 436 et 1920 × 1080 (2022-feng#012.0) ; le FPS change peu
  entre les deux (§4.1) car le redimensionnement vers S est fixe. Batch non déclaré (batch 1
  supposé, non affirmé).
- FPS de bout en bout sur vidéo (lecture, redimensionnement, affichage compris), moyenne de
  10 passes ; pas de latence isolée. Pour SerreIA, séparer : latence du modèle seul
  (`hailortcli benchmark`), puis chaîne complète caméra + pré-traitement + NMS + classifieur.
- Puissance : JTOP (Jetson) et wattmètre USB (RPi), portée non décrite (`unspecified`). À
  refaire au wattmètre sur l'alimentation du Pi 5 + HAT, au repos et en charge.

**Pièges de comparaison.**
- Pas de TensorRT, FP16 sur Jetson (§3.2, 2022-feng#006.0) : Jetson sous-évalués ; le gain
  ×2 avec TensorRT est cité d'une référence, non mesuré (2022-feng#016.2). Comparaison
  équitable entre ces trois cartes, pas face à un Hailo en INT8.
- « Mean confidence » n'est pas une mAP : aucune précision n'est mesurée ; ne pas la comparer
  aux mAP ou aux accuracies de PlantVillage / PlantDoc.
- Les puissances de la Table 3 (carte entière ou presque) et celles des Tables 5-6 (GPU seul)
  ne se comparent pas ; les watts du NCS2 ne comptent pas la consommation de l'hôte
  de la même manière que JTOP (déduit, méthode non décrite).
- Spécifications constructeur (TFLOPs, W nominaux, Table 2) : ne pas les mélanger avec les
  mesures.

## Gaps identifiés

- **Protocole de mesure :** confirme le gap existant (pour SerreIA : aucune référence Hailo-8L / RPi 5 ici, à chercher). Même hors FPGA, un benchmark publié ne
  donne ni mAP, ni latence, ni portée de puissance.
- **Baseline Jetson à jour :** il manque une baseline Jetson optimisée (TensorRT INT8, mAP
  COCO val, puissance carte au wattmètre) pour comparer honnêtement un YOLO sur FPGA.
  À chercher (Jetson Orin, TensorRT).
- **Précision après compilation :** la perte de précision due au toolflow (conversion,
  quantification) est rarement mesurée sur la cible elle-même. C'est une hypothèse à étayer
  avec les papiers FPGA du corpus.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). La Table 3 est mal
découpée dans `fulltext.md` : les valeurs ont été réalignées à la main.

Ce qui suit est déduit et non affirmé par les auteurs :
- le caractère « bridé » des Jetson par rapport à un déploiement TensorRT INT8 ;
- l'incohérence de la colonne Time ;
- la non-comparabilité avec les mAP des papiers FPGA ;
- l'analogie avec Vitis AI et FINN.
