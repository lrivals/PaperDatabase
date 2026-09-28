---
id: 2023-cao-gcl-yolo-ghostconv-lightweight-yolo
fiche: done
date: 2026-09-28
---

# GCL-YOLO: A GhostConv-Based Lightweight YOLO Network for UAV Small Object Detection

Jinshan Cao, Wenshu Bao, Haixing Shang, Ming Yuan, Qian Cheng, 2023, Remote Sensing 15(20), 4932. https://doi.org/10.3390/rs15204932
Type : article de journal

## Problème

Les images de drone contiennent beaucoup de petits objets (quelques pixels), denses,
occultés, flous, à échelles variables. Les YOLO sont conçus pour des scènes naturelles
(COCO, VOC) et gaspillent leurs paramètres sur les gros objets. Les plateformes drone ont
des ressources de calcul et de stockage limitées : les auteurs cherchent un détecteur
**léger** et plus précis sur petits objets (§1).

## Méthode

YOLOv5 (v7.0) redessiné, en quatre tailles N/S/M/L par coefficients de largeur et de
profondeur (Table 1) :
- **backbone GhostConv** : ghost bottlenecks G-Bneck1 (stride 1, extraction) et G-Bneck2
  (stride 2, sous-échantillonnage, avec attention ECA), module **ELAG3** (ELAN + G-Bneck1)
  à la place des CSP-Bottleneck, **GSPPF** (SPPF à GhostConv) (§3.2, Fig. 4-6) ;
- **neck ELA-PAN** : ajout d'une **tête P2** (stride 4, 160×160) et **suppression de la tête
  P5** (stride 32), qui portait environ 75 % des paramètres des têtes (§3.3, Table 2) ;
- perte de localisation **Focal-EIOU** au lieu de CIOU (§3.4, Éq. 5-6).

Entraînement depuis zéro, 300 epochs, SGD, entrée 640×640, sans poids pré-entraînés, sur
2 × RTX 3060 (§4.3). Aucune quantification, aucun portage embarqué.

## Plateforme et implémentation

Aucune implémentation embarquée. Entraînement sur 2 × NVIDIA GeForce RTX 3060 (Ubuntu 20.04,
PyTorch 1.8, CUDA 11.1, §4.3). Le matériel utilisé pour mesurer les FPS, la taille de batch
et la précision numérique ne sont **pas précisés** (n/r) ; puissance n/r. Code : non
mentionné dans le texte extrait (non publié à notre connaissance).

## Résultats

VisDrone-DET2021 (test ou val non précisé), 640×640 (Table 3) :

| Réseau | Params (M) | GFLOPs | FPS | mAP50 (%) |
|---|---|---|---|---|
| YOLOv5-N / GCL-YOLO-N | 1,77 / 0,43 | 4,2 / 3,2 | 68 / 58 | 26,4 / 31,7 |
| YOLOv5-S / GCL-YOLO-S | 7,04 / 1,64 | 15,8 / 10,7 | 60 / 53 | 32,7 / 39,6 |
| YOLOv5-M / GCL-YOLO-M | 20,89 / 4,30 | 48,0 / 25,9 | 57 / 48 | 36,4 / 43,2 |
| YOLOv5-L / GCL-YOLO-L | 46,15 / 8,76 | 107,8 / 50,7 | 53 / 42 | 38,7 / 45,7 |

- Ablation (Table 4, §4.5) : GhostConv seul fait chuter le mAP50 de 32,7 à 28,8 ; l'ajout
  de P2 et la suppression de P5 apportent l'essentiel du gain (+5,6 pts mAP50, +3,7 pts
  mAP50-95 selon le texte). Le bas de la Table 4 est tronqué à l'extraction.
- Face aux réseaux légers sur VisDrone (Table 5) : GCL-YOLO-S 39,6 % mAP50 contre 39,2
  (YOLOv8-S, 11,1 M params) et 36,8 (YOLOv7-Tiny).
- UAVDT (sous-ensemble à 20 % des images, construit par les auteurs, §4.1) : GCL-YOLO-S
  31,6 % mAP50, 54 FPS, contre 29,8 (YOLOv5-S) et 31,9 (YOLOv8-S) (Table 6).
- Contre les grands réseaux (RSOD, SlimYOLOv3, DMNet, TOOD, VFNet, TridentNet) :
  GCL-YOLO-L « second-highest » (§4.7.1) ; la Table 7 est absente du texte extrait.
- Coût : −7 FPS pour GCL-YOLO-S par rapport à YOLOv5-S, attribué à la tête P2 (§5).

→ reportés dans `benchmarks.csv` : 5 lignes (GCL-YOLO-N, -S, -M, -L sur VisDrone, Table 3 ;
GCL-YOLO-S sur UAVDT, Table 6). Plateforme d'inférence n/r.

## Limites et critique

- **« Léger » mesuré en paramètres, pas en latence embarquée.** Les FPS sont mesurés sur un
  GPU de bureau non précisé (les auteurs n'indiquent que les RTX 3060 d'entraînement), sans
  batch ni précision. Ils baissent alors que les GFLOPs baissent : la tête P2 à 160×160
  coûte en mémoire et en accès, ce qu'un compte de FLOPs ne voit pas (déduit, cohérent avec
  §5). Sur un FPGA ou un MCU, c'est précisément ce coût d'activation qui domine (déduit).
- **Aucune mesure sur plateforme drone** : reconnu par les auteurs (§6). Aucun Jetson,
  aucune puissance, aucune quantification.
- **UAVDT non standard** : sous-ensemble à 20 % construit par les auteurs, donc non
  comparable aux chiffres UAVDT publiés ailleurs.
- **Baselines ré-entraînées depuis zéro** sans poids pré-entraînés (§4.3) : choix
  « équitable » mais qui peut désavantager les réseaux plus gros (YOLOv8-S) (déduit).
- Pas de mAP_small rapporté, alors que le papier cible les petits objets ; pas d'écart-type
  entre entraînements.
- Split VisDrone utilisé pour l'évaluation (val ou test-dev) non précisé.

## Pertinence pour la thèse

- Exemple type de la famille « YOLO drone avec tête P2 » (axe `drone-detection`) : le gain
  vient surtout de P2 + suppression de P5, une recette réutilisable et bon marché en
  paramètres (1,64 M pour GCL-YOLO-S).
- **Candidat intéressant pour un portage FPGA** (déduit) : peu de paramètres (tient en BRAM
  une fois quantifié), mais activation P2 volumineuse et GhostConv/ECA/depthwise moins
  efficaces sur DPU. C'est exactement l'hypothèse de `gaps.md` : ces YOLO drone ne sont pas
  portés sur FPGA, et leur coût réel (latence, énergie) reste inconnu.
- Illustre l'écart entre « léger » (params, FLOPs) et « rapide sur cible » (FPS qui baissent).

## Gaps identifiés

- YOLO drone SOTA à tête P2 non porté sur FPGA / Jetson / MCU : aucune latence ni puissance
  embarquée (confirme l'hypothèse de départ).
- Effet de la quantification sur le mAP (et le mAP_small) de ces architectures légères :
  non mesuré.
- Coût mémoire de la tête P2 (activations 160×160) sur cible embarquée : non quantifié.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). Le texte contient de
nombreux doublons de paragraphes (artefacts d'extraction). Le bas de la Table 4 (lignes
A4 à A7) est tronqué et la **Table 7** (comparaison aux grands réseaux) est absente du texte
extrait : leurs chiffres n'ont pas été lus.

Ce qui suit est déduit et non affirmé par les auteurs :
- le coût mémoire de la tête P2 comme cause de la baisse de FPS sur cible embarquée ;
- l'intérêt et les difficultés d'un portage FPGA ;
- le désavantage possible des baselines ré-entraînées sans pré-entraînement ;
- l'absence de code publié (rien n'est mentionné dans le texte).
