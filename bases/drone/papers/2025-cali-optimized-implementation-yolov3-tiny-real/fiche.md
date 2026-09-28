---
id: 2025-cali-optimized-implementation-yolov3-tiny-real
fiche: done
date: 2026-09-28
---

# Optimized Implementation of YOLOv3-Tiny for Real-Time Image and Video Recognition on FPGA

Riccardo Calì, Laura Falaschetti, Giorgio Biagetti, 2025, Electronics 14(20), 3993. https://doi.org/10.3390/electronics14203993
Type : article de journal (MDPI Electronics), tiré du mémoire de master du premier auteur (§1)

## Problème

Les auteurs posent trois gaps (§2.5) : (i) la plupart des accélérateurs FPGA visent des
puces haut de gamme ; (ii) les chaînes de bout en bout, de l'entraînement au déploiement,
restent peu explorées ; (iii) peu de travaux donnent des comparaisons systématiques en FPS/W.
Ils veulent montrer qu'un FPGA **bas coût** (Zynq-7020, carte à ~150 €, §5.2) suffit pour de
la détection temps réel à bord d'un drone, en soignant l'implémentation (folding, FIFO,
DSP packing) plutôt que l'architecture du réseau (§2.5).

## Méthode

- **Modèle** : YOLOv3-Tiny 416×416 **fortement réduit** pour tenir dans FINN et en BRAM :
  suppression des upsampling/concaténations (donc **une seule tête de détection**, 13×13),
  nombre de filtres divisé par 5, couche Detect détachée et exécutée sur le PS (§3.1,
  Table 1). Architecture reprise de LPYOLO [63].
- **Quantification** : QAT Brevitas, première et dernière convolution en poids INT8, le reste
  en W4/A4 (§3.1.1). Totaux : 113,3 M MAC 4b-4b, 37,4 M MAC 8b-8b, 2,8 M MAC 4b-8b
  (Table 6). Entraînement sur **VisDrone-DET réduit à la seule classe « car »**, 300 époques,
  batch 64, sur une Tesla P100 Kaggle (§3.1.2-3.1.3, Table 3).
- **Toolflow** : FINN 0.10, architecture streaming dataflow. MVU en RTL (DSP packing,
  4 MAC/DSP48E1 en 4 bits, Table 4) ou en HLS style LUT pour éviter la saturation DSP ;
  SWG RTL en mode fenêtre parallèle ; folding itératif sur la couche la plus lente ;
  dimensionnement des FIFO par simulation RTL (pyverilator) ; tous les poids en BRAM
  (§3.5-3.8).
- **Post-traitement** (rescale, Detect, NMS, boîtes) sur le PS ARM en Python (Table 10).
- **Driver** « TPU-like » : serveur WebSocket sur la carte, client qui capture, envoie les
  images et affiche ; format de modèle `.fnn` rechargeable à chaud (§3.11).
- Baseline Coral Edge TPU : même YOLOv3-Tiny entraîné en FP32 puis PTQ INT8 (§3.3).

## Plateforme et implémentation

- **Puce** : Xilinx Zynq-7000 **XC7Z020CLG400-2** sur carte MYiR Z-turn Board V2 (1 GiB
  DDR3), PS dual Cortex-A9 à 750 MHz (§3). PL testée à 50, 100 et 200 MHz (Table 9).
- **Ressources** (Table 7) : 41 605 LUT (78,2 %), 204 DSP (92,73 %), 138 BRAM_18K (98,57 %
  de 140 selon les auteurs). La Table 16 donne pour le même design 37,9 K LUT et
  « 138 (18 K) » BRAM. Incohérence non expliquée (voir Limites).
- **Puissance** : **mesurée à la carte entière** via une alimentation de labo 5 V, courant
  relevé (§4.3, Fig. 18) → `power_scope = board`. Repos (bitstream non chargé) ≈ 1,9 W
  (PS + DDR) ; en inférence 2,12 / 2,38 / 2,55 W à 50 / 100 / 200 MHz (§4.3.2, Table 12
  suite). Part de la PL déduite par soustraction par les auteurs : 0,22 à 0,65 W (§4.3.1).
  Estimation Vivado : 3,358 W on-chip dont 1,496 W pour le PS7 (Table 12). La Table 11
  (Vivado par module) n'a pas de corps extrait.
- Température die mesurée 53,1 °C (caméra IR) contre 46,3 °C estimés par Vivado (§4.3.1).
- **Code publié** : https://github.com/sn0wst0rm/FINN-VisDrone-YOLO (réf. [62], code,
  notebooks d'entraînement, configurations de folding et FIFO). Bitstream : non mentionné
  explicitement ; le format `.fnn` en contient un, mais sa publication n'est pas affirmée.

## Résultats

Précision (Table 5, validation VisDrone, classe « car » seule) :

| Modèle | P | R | mAP@0.5 |
|---|---|---|---|
| YOLOv3-Tiny original | 67,06 % | 38,44 % | 41,76 % |
| YOLOv3-Tiny réduit (déployé) | 48,16 % | 17,16 % | **17,68 %** |

La réduction divise le rappel par ~2, ce que les auteurs attribuent à la perte de la seconde
branche multi-échelle (§4.1).

Débit et efficacité (Tables 9 et 14, `throughput_test()` avec données aléatoires en DRAM,
sans pré/post-traitement) :

| PL | Batch | FPS | Latence | P carte | FPS/W |
|---|---|---|---|---|---|
| 50 MHz | 1 | 43,91 | 22,77 ms | 2,12 W | 20,71 |
| 50 MHz | 100 | 52,21 | n/r | 2,12 W | 24,63 |
| 100 MHz | 1 | 86,47 | 11,56 ms | 2,38 W | 36,32 |
| 100 MHz | 100 | 104,39 | n/r | 2,38 W | 43,86 |
| 200 MHz | 1 | 164,79 | 6,07 ms | 2,55 W | 64,63 |
| 200 MHz | 100 | **208,69** | n/r | 2,55 W | **81,88** |

- Estimation FINN à 100 MHz : 462 FPS ; RTLSim : 134,8 FPS ; mesuré : 104,4 FPS (Table 8).
  Écart attribué surtout au StreamingMaxPool HLS, ~570 000 cycles au lieu de 216 320
  prédits (§3.7.2), qui divise le débit par 3,43 (§4.2.5). Un driver bare-metal C atteint
  134 FPS à 100 MHz (§4.2.5, sans tableau).
- **Chaîne complète** (driver Python FINN, batch 1, Table 10, à 200 MHz) : prétraitement
  32,2 ms, exécution driver 12,1 ms, NMS 9,2 ms, post-traitement total 25,8 ms. Le
  pré/post-traitement sur le PS pèse donc ~5 fois plus que l'inférence PL. Le driver
  réduit les FPS de 21 % à 50 MHz et de 50 % à 200 MHz (§4.2.6).
- **Bout en bout réseau** (§4.4) : 30 FPS en streaming caméra via Ethernet filaire (latence
  max ~13 ms) ; ~130 ms de latence max en WiFi.
- **Coral Edge TPU** (Table 15) : 103,2 FPS (9,69 ms) et 148,7 FPS (6,73 ms) ; puissances
  1,2 et 2,4 W **tirées de la datasheet, pas mesurées** ; 86,0 et 62,0 FPS/W.
- **Autres FPGA** (Table 16, chiffres repris des papiers cités) : LPYOLO sur Z7020, 19,12 FPS,
  7,97 FPS/W ; SATAY sur VCU118, 147 FPS, 3,43 FPS/W ; FINN-R Tincy-YOLO sur PYNQ-Z1,
  29,9 FPS. Les auteurs revendiquent ~10× le débit de LPYOLO et 7,3× son efficacité (§5.2).
- Essai qualitatif sur des images de drone propres (routes, parkings) : « almost all of the
  cars were correctly detected » (§4.5, Fig. 19), sans métrique.

→ reportés dans `benchmarks.csv` : 6 lignes (YOLOv3-Tiny réduit W4A4/W8, XC7Z020,
50/100/200 MHz × batch 1/100, Tables 9, 13, 14, 5 et 7 ; power_scope `board`).

## Limites et critique

- **Précision très faible et non comparable** : 17,68 % mAP@0.5 sur **une seule classe**
  (car) de VisDrone (Table 5). Ce n'est pas le mAP multi-classe VisDrone habituel ; la
  comparaison FPGA de la Table 16 écarte explicitement le mAP (« datasets … are different »,
  §5.2). Le gain de débit face à LPYOLO et SATAY se paie donc d'une précision non discutée.
  Le mAP_small n'est pas mesuré, alors que la tête P2 et la tête 26×26 sont justement
  supprimées.
- **L'affirmation « objets à échelle fixe à altitude standard »** (§4.1), qui justifie la tête
  unique, n'est pas étayée par une mesure : l'essai sur drone (§4.5) est qualitatif.
- **208 FPS ≠ débit applicatif** : c'est un test de débit en batch 100 sur données aléatoires.
  Le système réel (prétraitement + driver + post-traitement sur PS) tombe à ~30 FPS en
  streaming (§4.4). Le goulot est sur le PS, pas sur l'accélérateur.
- **Comparaison Coral biaisée** : puissance Coral issue de la datasheet (et « 1,2 W à
  250 MHz » extrapolée par les auteurs), contre une mesure carte entière côté FPGA. Le Coral
  exécute un modèle **non réduit** (entraînement FP32 séparé, §3.3), dont la précision n'est
  pas donnée.
- **Comparaison FPGA hétérogène** : SATAY en W8/A16 sur VCU118 à 42,9 W, FINN-R Tincy-YOLO
  en 1W3A ; puissances reprises sans portée. Les auteurs le reconnaissent en partie (§5.2).
- **Incohérences internes** : LUT 41 605 (Table 7) contre 37,9 K (Table 16) ; latence 6,07 ms
  (Table 15) contre 4,79 ms (Table 16, qui semble être 1/FPS en batch 100 : déduit) ;
  « 138 of the 140 available BRAM_18K » alors que le XC7Z020 a 140 BRAM36 soit 280 BRAM18
  (déduit de la fiche technique Xilinx, non vérifié dans le papier). La colonne `bram` du CSV
  reprend 138 tel quel.
- Le texte « outperforms … by a factor of three to seven in FPS/W » (résumé) ne colle pas
  avec la Table 16 (81,85 contre 3,43 à 11,96 FPS/W, soit 7 à 24 fois, ce que dit d'ailleurs
  §5.2).
- **Aucune mesure en vol** : pas de masse, pas d'autonomie, pas d'intégration sur drone
  (vidéo drone traitée hors ligne). Gamme de puissance : FPGA (~2,5 W carte).
- Pas de comparaison Jetson mesurée (mentionnée seulement qualitativement, §2.2).

## Pertinence pour la thèse

- **Point de référence bas coût pour l'axe `drone-fpga`** : un YOLO sur Zynq-7020 avec
  puissance carte mesurée, code publié, et un décompte honnête des étapes (estimation,
  RTLSim, mesure, driver) qui montre où se perd le débit (Tables 8 et 10). Utile pour
  argumenter que le goulot système d'un SoC FPGA est souvent le PS.
- **Illustre le gap « YOLO drone SOTA non portés sur FPGA »** : pour tenir dans FINN, il faut
  retirer la branche multi-échelle, l'inverse exact de ce que font les YOLO drone (tête P2).
  Limitation de FINN sur les topologies branchées explicitement citée (§3.1).
- Protocole réutilisable : puissance repos vs charge, FPS/W par fréquence et par batch.
- Laisse ouvert : précision multi-classe, mAP_small, NMS sur PL, métriques de vol.

## Gaps identifiés

- **Quantification et mAP_small** : non mesuré ; ici la perte (41,8 → 17,7 % mAP) mélange
  réduction d'architecture et quantification W4A4 sans ablation séparant les deux.
- **Topologies multi-échelles (FPN/PAN, tête P2) dans FINN** : non supportées en 0.10
  selon les auteurs → frein structurel au portage des YOLO drone.
- **Post-traitement sur PS** : NMS + boîtes ≈ 26 ms contre 6 ms d'inférence à 200 MHz
  (Table 10) ; aucun essai de NMS matériel.
- **Aucune métrique système** (autonomie, masse, vitesse de vol), comme prévu par
  l'hypothèse de `gaps.md`.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). Tables 3 (doublon),
11, 13 et 15 signalées « sans corps extrait » : la Table 11 (Vivado par module) manque ; les
valeurs de la Table 13 (puissance carte) sont reprises du texte (§4.3.2) et de la
Table 14 ; la Table 15 est partiellement lisible (valeurs Coral et FINN présentes). Des
sous-sections (3.1.2, 3.2, 3.4.2, 3.5.3, 4.2.4-4.2.6) sont mêlées aux tableaux dans
l'extraction.

Ce qui suit est déduit et non affirmé par les auteurs :
- l'incohérence BRAM (140 BRAM36 = 280 BRAM18 sur XC7Z020) ;
- l'interprétation de la latence 4,79 ms de la Table 16 comme 1/FPS ;
- le constat que le pré/post-traitement PS pèse ~5 fois l'inférence ;
- l'écart entre « three to seven » (résumé) et les ratios de la Table 16.
