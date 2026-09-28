---
id: arxiv-1909.09709-skynet-hardware-efficient-method-object
fiche: todo
date: 2026-09-28
---

> **Importée de la base `drone` le 2026-09-28.** Cette fiche a été écrite pour une autre base (autre thème) : pertinence à réévaluer ici, puis `fiche: done` via `/paper-fiche`. Statut d'origine : done.

# SkyNet: a Hardware-Efficient Method for Object Detection and Tracking on Embedded Systems

Xiaofan Zhang, Haoming Lu, Cong Hao, Jiachen Li, Bowen Cheng, Yuhong Li, Kyle Rupnow, Jinjun Xiong, Thomas Huang, Honghui Shi, Wen-Mei Hwu, Deming Chen, 2019, arXiv preprint. https://arxiv.org/abs/1909.09709
Type : preprint arXiv selon `metadata.json` ; le texte porte toutefois la mention « Proceedings of the 3rd MLSys Conference, Austin, TX, USA, 2020 » (§1, bloc d'affiliation) : version publiée en conférence, métadonnées à corriger.

## Problème

Concevoir un détecteur à la fois précis et efficace pour GPU et FPGA embarqués. Les
auteurs critiquent le flot **top-down** habituel (partir d'un DNN de référence précis, puis
compresser et implémenter) : (1) sensibilités logiciel et matériel difficiles à équilibrer
pendant la compression, d'où des allers-retours coûteux ; (2) choix du DNN de référence
hasardeux, car la précision sur ImageNet ne prédit pas celle sur une tâche réelle (§3,
Table 2 : ResNet-50 à 0,32 d'IoU contre SkyNet à 0,73 sur DAC-SDC).

## Méthode

- **Flot bottom-up en trois étapes** (§4, Fig. 3) : (1) sélection de **Bundles** (blocs de
  couches = IP matérielles) évalués sur la cible réelle (latence GPU et FPGA, ressources
  FPGA), puis entraînés vite dans des « esquisses » de DNN ; (2) recherche
  **hardware-aware par PSO par groupes** (canaux par Bundle, position des poolings),
  fitness = précision + α·(latence estimée − cible) (§4.2, Éq. 1, Algorithme 1) ; latence
  FPGA estimée via un template d'accélérateur à IP partagées (Hao et al., 2019) et l'outil
  HLS ; (3) ajout de fonctions si le budget le permet.
- **Architecture retenue** : Bundle = DW-Conv3 + PW-Conv1 + BN + ReLU6, empilé 6 fois ;
  entrée 3×160×360 ; modèle C avec **bypass** du Bundle #3 vers le #6 et **réordonnancement
  des feature maps** (space-to-depth) pour les petits objets ; tête YOLO sans
  classification, 2 ancres (§5, Table 3, Fig. 4-5).
- Motivation petits objets : 91 % des boîtes DAC-SDC font moins de 9 % de l'image et 31 %
  moins de 1 % (§5.2, Fig. 6).
- **GPU (TX2)** : FP32, cuDNN ; pipeline multithread (chargement + pré-traitement,
  inférence, post-traitement), ×3,35 face à l'exécution série (§6.3, Fig. 10).
- **FPGA (Ultra96)** : quantification FM 9 bits / poids 11 bits (schéma 1) ; fusion
  Conv+BN ; **batch + tiling** de 4 images assemblées pour réutiliser les poids chargés
  depuis la DRAM (BRAM de 0,95 Mo seulement) ; une IP partagée par toutes les couches ;
  partition CPU (pré/post-traitement) / FPGA en pipeline (§6.4, Fig. 9-10).
- Extension au **suivi** : SkyNet comme backbone de SiamRPN++ et SiamMask sur GOT-10k (§7).

## Plateforme et implémentation

- **NVIDIA Jetson TX2** (GPU 665 GFLOPS crête à 1300 MHz selon les auteurs, §6.4), FP32.
- **Ultra96** (pic théorique 144 GOPS à 200 MHz, §6.4) ; la puce (Zynq UltraScale+ ZU3EG)
  n'est pas nommée dans le texte. Fréquence effective, LUT, DSP, BRAM consommés : n/r.
  Toolflow : accélérateur IP HLS maison (template de Hao et al. 2019).
- Suivi : une NVIDIA **1080Ti** de bureau (Tables 8-9).
- Puissance : mesurée par les organisateurs de DAC-SDC sur le jeu de test caché
  (Tables 5-6, §6.5) ; méthode et portée (carte ou puce) n/r dans ce texte →
  `unspecified`.
- Code : « Open-source code can be found at this link » (§1), lien absent du texte
  extrait. Bitstream : n/r.

## Résultats

DAC-SDC'19, jeu de test caché de 50 k images (Tables 5-6, §6.5) :

| Plateforme | IoU | FPS | Puissance | Score total |
|---|---|---|---|---|
| TX2 GPU, FP32 | 0,731 | 67,33 | 13,50 W | 1,504 (1er) |
| Ultra96 FPGA, FM9/W11 | 0,716 | 25,05 | 7,26 W | 1,526 (1er) |

- Face aux autres équipes FPGA 2019 : XJTU Tripler 0,615 IoU à 50,91 FPS et 9,25 W ;
  SystemsETHZ 0,553 à 55,13 FPS et 6,69 W (Table 6). SkyNet gagne par la précision, pas
  par le débit.
- Validation (Table 4) : SkyNet C-ReLU6 0,741 d'IoU (1,82 Mo de paramètres) ; ReLU6 vaut
  +0,02 à +0,03 d'IoU face à ReLU pour chaque modèle.
- Quantification (Table 7) : FP32 0,741 → FM9/W11 0,727 → FM8/W10 0,680.
- Suivi sur 1080Ti (Tables 8-9) : SiamRPN++ SkyNet AO 0,364 à 41,22 FPS contre ResNet-50
  0,365 à 25,90 FPS ; SiamMask SkyNet AO 0,390 à 30,15 FPS contre ResNet-50 0,380 à
  17,44 FPS ; paramètres ÷37,20 (Abstract).

→ reportés dans `benchmarks.csv` : 4 lignes — TX2 (Table 5), Ultra96 (Table 6), et les
deux trackers SiamRPN++ / SiamMask avec backbone SkyNet sur 1080Ti (Tables 8, 9).

## Limites et critique

- **IoU mono-objet (DAC-SDC)** : non comparable à un mAP multi-classe VisDrone ;
  l'ablation (Table 4) est sur la validation, les résultats finaux sur le test caché.
- **Aucune ressource FPGA rapportée** (LUT, DSP, BRAM, fréquence réelle) : impossible de
  situer l'efficacité de l'accélérateur ni de le reproduire à partir du papier.
- **Batch de 4 sur FPGA** : les 25,05 FPS sont un débit en lot ; la latence par image
  n'est pas donnée (n/r), alors que c'est ce qui compte en boucle de vol (déduit).
- **Puissance sans portée** : 13,50 W (TX2) et 7,26 W (Ultra96) mesurés par les
  organisateurs, méthode non décrite ici. Le score DAC-SDC pondère l'énergie par un
  logarithme (Éq. 4) : la précision domine, et l'Ultra96 de SkyNet consomme plus que les
  équipes 2018 sur PYNQ-Z1 (2,45 à 4,20 W, Table 6, plateforme différente).
- **Comparaison de backbones biaisée** (Table 2) : ResNet-34/50 à 0,26-0,32 d'IoU sur
  DAC-SDC paraît anormalement bas, sans détail d'entraînement ; cela sert l'argument
  contre le flot top-down (déduit).
- Gamme de puissance : Jetson (13,5 W) et FPGA (7,3 W), toutes deux au-dessus d'un
  budget nano-drone ; aucune mesure à bord d'un drone.

## Pertinence pour la thèse

- **Référence historique de l'axe `drone-fpga`** : gagnant DAC-SDC'19 dans les deux
  pistes, avec la même architecture sur GPU et FPGA — rare comparaison à modèle égal
  TX2 contre Ultra96 (FPS/W : 4,99 contre 3,45, calculé à partir des Tables 5-6, déduit).
- Le **co-design bottom-up** (Bundle = IP, recherche avec latence mesurée) est une
  méthode directement réutilisable pour concevoir un détecteur drone pour FPGA.
- Montre concrètement l'effet de la quantification sur l'IoU (Table 7) — mais sur un
  objet unique, pas sur un mAP_small.
- Le bypass + réordonnancement (space-to-depth) est une solution petits objets **légère
  et portée sur FPGA**, contrepoint à la tête P2 des YOLO drone SOTA.

## Gaps identifiés

- **Quantification → petits objets** : Table 7 mesure la chute d'IoU globale, pas par
  taille d'objet ; l'effet sur les objets < 1 % de l'image (31 % du jeu) reste inconnu.
- **Latence par image sur FPGA** en mode batch = 1 : non rapportée.
- **Multi-classe / multi-objets** : SkyNet ne traite qu'un objet par image ; son passage
  à VisDrone n'est pas étudié ici.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). L'avertissement
signale la Table 9 « sans corps extrait », mais son corps est présent et lu. Une partie
de §4.1-4.2 est mélangée à la légende de la Fig. 3, et §6.4.2 est tronqué (« the inter-
tween adjacent… »). La Figure 8 et les détails de mémoire hiérarchique manquent.

Ce qui suit est déduit et non affirmé par les auteurs :
- la puce ZU3EG de l'Ultra96 ;
- les FPS/W calculés (Tables 5-6) ;
- le caractère « débit en lot » des 25,05 FPS FPGA (le batch est décrit, mais son effet
  sur la latence n'est pas chiffré) ;
- le soupçon de baselines ResNet sous-entraînées (Table 2).
