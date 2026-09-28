---
id: arxiv-2502.15737-performance-analysis-you-only-look
fiche: done
date: 2026-09-24
---

# A Performance Analysis of You Only Look Once Models for Deployment on Constrained Computational Edge Devices in Drone Applications

Lucas Rey, Ana M Bernardos, Andrzej D Dobrzycki et al., 2025, Electronics 2025, 14(3), 638. https://doi.org/10.3390/electronics14030638
Type : article de journal. La fiche est rédigée sur la version arXiv 2502.15737.

## Problème

Quelle plateforme embarquée et quelle précision numérique choisir pour faire tourner YOLOv8
à bord ou à proximité d'un drone (§1) ? Les auteurs posent aussi la question du coût de
bout en bout (communication comprise) face au cloud (§5).

## Méthode

- **Modèles :** YOLOv8n et YOLOv8s, entrée 640×640, entraînés sur un **jeu de données
  propre** (§3.1) :
  - 6000 images intérieures prises par des drones DJI Tello, annotées à la main ;
  - des robots TurtleBot servent de cibles ;
  - AdamW, 100 époques, augmentation mosaic ;
  - seuil de confiance 0,5 et IoU 0,7 en validation.
- **Précisions :** FP32, FP16 et INT8 par quantification post-entraînement sous TensorRT
  (via ONNX) sur les Jetson. FP32 seulement sous NCNN sur le RPi 5 : FP16 et INT8 n'ont pas
  fonctionné (§3.1.3, §4.1).
- **Mesures en isolé (§3.2, §4, Table 3) :**
  - MIS (FPS de l'inférence seule) ;
  - IPM (inférences par minute, entrées-sorties comprises) ;
  - puissance moyenne ;
  - énergie par inférence, EPI = P × 60 / IPM ;
  - mAP50 et mAP50-95.
- **Puissance :** **tegrastats** sur les Jetson, **`vcgencmd pmic_read_adc`** sur le
  RPi 5, moyennée sur 5000 images (§3.2, §4.3).
- **Pipeline réel (§5) :** station sol → WebSocket → Jetson ou cloud (AWS SageMaker,
  Triton, GPU T4, région eu-west-2 depuis Madrid). Mesures du RTT, du temps de traitement
  et de la communication.

## Plateforme et implémentation

| Carte | CPU | GPU | RAM | Puissance typique (constructeur) |
|---|---|---|---|---|
| Jetson Orin Nano | 6 × A78AE | Ampere, 1024 cœurs + 32 Tensor Cores | 8 GB | 7-15 W |
| Jetson Orin NX | 8 × A78AE | Ampere, 2048 cœurs + 64 Tensor Cores | 16 GB | 10-25 W |
| Raspberry Pi 5 | 4 × A76, 2,4 GHz | VideoCore VII, non utilisé | 8 GB | 5-7 W |

(Table 2)

- **Mode de puissance nvpmodel des Jetson :** n/r. Il fixe pourtant la puissance maximale,
  donc les FPS.
- **Code et jeu de données :** non publiés (aucun lien dans le texte extrait).

## Résultats

Table 4 (inférence seule, batch n/r, entrée 640) :

| Carte | Modèle | Précision | mAP50-95 | MIS (FPS) | P (W) | EPI (J) |
|---|---|---|---|---|---|---|
| Orin Nano | v8s | FP32 | 86,08 | 27,00 | 8,790 | 0,379 |
| Orin Nano | v8s | FP16 | 86,22 | 37,90 | 7,836 | 0,302 |
| Orin Nano | v8s | INT8 | 79,68 | 41,20 | 7,257 | 0,223 |
| Orin Nano | v8n | FP32 | 84,22 | 37,00 | 8,345 | 0,245 |
| Orin Nano | v8n | FP16 | 84,39 | 40,00 | 7,422 | 0,208 |
| Orin Nano | v8n | INT8 | 71,90 | 44,90 | 7,483 | 0,185 |
| Orin NX | v8s | FP32 | 86,10 | 35,65 | 14,155 | 0,399 |
| Orin NX | v8s | FP16 | 86,20 | 48,24 | 12,815 | 0,279 |
| Orin NX | v8s | INT8 | 79,70 | 56,32 | 11,002 | 0,233 |
| Orin NX | v8n | FP32 | 84,20 | 52,19 | 12,480 | 0,235 |
| Orin NX | v8n | FP16 | 84,40 | 58,82 | 10,853 | 0,203 |
| Orin NX | v8n | INT8 | 71,90 | 65,83 | 10,305 | 0,179 |
| RPi 5 | v8s | FP32 | 86,20 | 7,32 | 5,422 | 1,498 |
| RPi 5 | v8n | FP32 | 84,40 | 8,47 | 5,441 | 0,738 |

Autres résultats :
- **Temps d'itération moyens (§4, Fig. 4) :**
  - Orin Nano : de 23,16 ms (v8n INT8) à 42,97 ms (v8s FP32) ;
  - Orin NX : de 15,16 à 27,79 ms ;
  - RPi 5 : 118 ms (v8n) et 211 ms (v8s).
- **Pipeline réel sur Orin NX (Table 5) :** RTT de 29,95 ms (v8n INT8) à 48,97 ms
  (v8s FP32), traitement de 14,29 à 26,50 ms. Le RPi 5 n'a pas pu tenir le pipeline (§5.1).
- **Edge contre cloud (Orin Nano, v8s FP16, §5.2) :**
  - RTT : 35,09 ms en edge contre 348,21 ms en cloud ;
  - traitement : 32,59 ms en edge contre 6,82 ms en cloud ;
  - communication : 2,50 ms contre 341,41 ms.

→ reportés dans `benchmarks.csv` : 14 lignes (Table 4), `power_scope = chip`.
- **Pourquoi `chip` :** la puissance vient d'une télémétrie embarquée (tegrastats, PMIC du
  RPi 5), ce qui correspond à la définition `chip` de DATA_MODEL §7. Voir la réserve sur
  cette portée dans « Limites ».
- **Latence :** la colonne `latency_ms` reprend le « temps d'itération moyen » du §4 quand
  il est donné (10 lignes sur 14).
- **Confiance :** 6 lignes sont en `medium`. Ce sont les cellules fusionnées par
  l'extraction (v8s INT8 et v8n FP32 sur Nano et sur NX, les deux lignes du RPi 5). Je les
  ai séparées dans l'ordre des colonnes, et la relation EPI = P × 60 / IPM concorde pour
  les 14 lignes à 0,001 près.

## Limites et critique

- **mAP sur un jeu privé et très facile** (intérieur, une seule cible, mAP50 d'environ
  0,97 en FP32). Elle **ne se compare pas** aux mAP COCO des papiers FPGA, et la mAP COCO
  que je cherchais n'est **pas** dans ce papier.
- **Précision mesurée par cible (point positif) :** les valeurs INT8 diffèrent très
  légèrement entre Nano et NX (0,7968 et 0,7970), ce qui suggère une évaluation sur chaque
  carte (déduit). La perte due à la quantification INT8 est **forte** :
  - YOLOv8n : de 84,2 à 71,9 de mAP50-95 ;
  - YOLOv8s : de 86,1 à 79,7.
  Cette perte n'est pas négligeable, contrairement à ce que dit la discussion : « without a
  significant loss of accuracy » (§6).
- **Portée de la puissance :** tegrastats mesure les rails du module Jetson (SoC et
  mémoire), pas la carte entière. Ce n'est donc pas une mesure au wattmètre à l'entrée de
  la carte (déduit : le texte ne précise pas quels rails). Le mode nvpmodel n'est pas
  indiqué.
- **Unité erronée :** la colonne « Energy Consumption (W·s) » de la Table 4 est en réalité
  une puissance moyenne en W. Le texte le dit (« consumes 14.155 W », §4.3), et le calcul
  de l'EPI le confirme.
- **Incohérences dans le texte :**
  - §6 attribue 35,65 FPS et 0,8420 à « YOLOv8n_FP32 » sur NX, alors que la Table 4 donne
    35,65 FPS pour v8s FP32 et 52,19 FPS pour v8n FP32 ;
  - la Table 7 recommande l'Orin Nano + v8n INT8 avec « mAP50 0,8272 », mais présente
    ailleurs 0,7190 comme mAP50 alors que c'est la mAP50-95.
- **MIS contre temps d'itération :** sur Orin Nano, v8n INT8 affiche 44,9 FPS en MIS, mais
  23,16 ms d'itération, soit environ 43 FPS. C'est cohérent. Sur RPi 5 en revanche,
  7,32 FPS contre 211 ms (environ 4,7 FPS) : les deux mesures n'ont pas le même périmètre.
- **Batch non indiqué**, et pas de comparaison FPGA : les auteurs la citent seulement en
  perspective (§6).

## Pertinence pour la thèse

- **Première baseline Jetson Orin du corpus** avec TensorRT FP16 et INT8, une puissance
  par télémétrie et une énergie par inférence.
- **Ordre de grandeur utile :**
  - YOLOv8n INT8 sur Orin NX : 65,8 FPS, environ 10,3 W, 0,18 J par inférence ;
  - Orin Nano : 44,9 FPS, environ 7,5 W.
  C'est à comparer aux 12,5 W et environ 136 mJ par image du YOLOv3-tiny FPGA de Zhai
  (modèles et jeux de données différents, déduit).
- **Argument pour le gap « précision sur cible » :** même avec TensorRT, la
  quantification post-entraînement INT8 coûte 6 à 12 points de mAP50-95 sur un jeu
  pourtant facile. D'où l'intérêt de mesurer la précision après compilation (protocole
  KV260).

## Gaps identifiés

- **Baseline Jetson :** partiellement comblé. Orin, TensorRT INT8 et puissance
  télémétrique sont là. Manquent une mAP COCO et une puissance de carte au wattmètre.
- **Précision après quantification :** mesurée ici, et forte (jusqu'à −12,3 points) ;
  étaye le gap.
- **Coût de bout en bout :** le RTT du pipeline est environ 2 à 3 fois le temps
  d'inférence seule (Table 5 contre Fig. 4). La mesure « inférence seule » surestime le
  débit réel.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, version arXiv, extraction GROBID `ok`). Le
Tableau 6 (edge contre cloud) est vide dans l'extraction : ses valeurs viennent du texte
du §5.2.

Ce qui suit est déduit et non affirmé par les auteurs :
- la mesure de la précision par carte ;
- la portée « module » de tegrastats ;
- le mauvais libellé de la colonne W·s (confirmé par calcul) ;
- les comparaisons avec Zhai et al.
