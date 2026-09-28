---
id: 2022-liu-sf-yolov5-lightweight-small-object
fiche: done
date: 2026-09-28
---

# SF-YOLOv5: A Lightweight Small Object Detection Algorithm Based on Improved Feature Fusion Mode

Haiying Liu, Fengqian Sun, Jason Gu, Lixia Deng, 2022, Sensors 22(15), 5817. https://doi.org/10.3390/s22155817
Type : article de journal

## Problème

Les détecteurs généralistes (YOLOv5) sont conçus pour toutes les échelles ; dans les scènes
denses en petits objets, ils sont peu précis et gaspillent du calcul sur la branche des
grands objets (Abstract, §1). Les auteurs veulent un YOLOv5 **allégé et spécialisé petits
objets**.

## Méthode

SF-YOLOv5 (« Small-Fast »), à partir de YOLOv5s (§3, Fig. 4) :
1. **Suppression de la couche C5** (dernier sous-échantillonnage du backbone) et de la
   sortie P5 : seules C3 et C4 alimentent la fusion. Les couches 7-8 du backbone pèsent à
   elles seules ~2,36 M paramètres (Table 2) (§3.1).
2. **PB-FPN** : chemin de fusion dérivé de PANet et BiFPN, avec un chemin supplémentaire
   haut → bas et des branches latérales vers les niveaux bas (§3.2, Fig. 6, Éq. 2-3).
3. **SPPF entre le neck et chaque tête** de prédiction (§3.3, Fig. 8).

Variante **SF-YOLOv5L** (coefficients d'échelle portés de (0,33 ; 0,25) à (1 ; 1)) pour se
comparer aux gros modèles (§4.6), et **SF-YOLOv5-P5** (tête P5 rétablie) pour VOC2012
(§4.7). Pas de quantification ni de pruning ; NMS YOLOv5 standard (§2.2). Pas de tête P2 :
l'allègement se fait en retirant la tête des grands objets, pas en ajoutant une tête fine.

## Plateforme et implémentation

- Poste Windows 10, 16 GB, CPU AMD 4800H, **GPU NVIDIA RTX 2060**, PyTorch + CUDA 11.1,
  300 époques, mosaic (§4.1). Les temps d'inférence des Tables 3-4 sont vraisemblablement
  mesurés sur cette RTX 2060 (non dit explicitement ; batch n/r).
- Aucun déploiement embarqué. Puissance : n/r.
- Code : non publié (aucun lien dans le texte).

## Résultats

Jeu principal : sous-ensemble filtré de **WIDER FACE** (visages ; 4 441 images
d'entraînement, 1 123 de validation) (§4.2).

| Modèle | mAP@0.5 | mAP@0.5:0.95 | Params (M) | GFLOPs | Temps (ms) | Source |
|---|---|---|---|---|---|---|
| YOLOv5s | 69,7 | 35,5 | 7,01 | 15,8 | 13,1 | Table 3 |
| SF-YOLOv5 | 71,3 | 36,3 | 2,23 | 13,8 | 12,2 | Table 3 |
| YOLOv7-tiny | 68,4 | 33,0 | 6,01 | 13,0 | 13,9 | Table 3 |
| SF-YOLOv5L | 75,1 | 39,7 | 15,5 | 91,2 | 49,4 | Table 3 |
| YOLOv7 | 76,1 | 39,5 | 36,5 | 103,2 | 18,0 | Table 3 |

Ablation (Table 3, §4.5) : retirer C5 (YOLOv5-N5) divise les paramètres par ~3,7
(7,01 → 1,88 M) pour +0,2 mAP@0.5 et −0,2 mAP@0.5:0.95 ; PB-FPN +0,9 / +0,7 ; SPPF
+0,5 / +0,3.

Autres jeux (Table 4) : **VisDrone** SF-YOLOv5 34,3 mAP@0.5 / 18,2 mAP@0.5:0.95 /
11,5 ms contre YOLOv5s 33,0 / 17,9 / 12,6 ms ; TinyPerson 20,0 / 6,5 / 11,0 ms contre
18,7 / 6,0 ; VOC2012 (SF-YOLOv5-P5) 61,2 / 38,3 / 24,8 ms contre 60,8 / 37,0.

→ reportés dans `benchmarks.csv` : 5 lignes — SF-YOLOv5 et SF-YOLOv5L sur WIDER FACE
filtré (Table 3), SF-YOLOv5 sur VisDrone et TinyPerson, SF-YOLOv5-P5 sur VOC2012
(Table 4, `confidence: medium` car l'en-tête de la Table 4 est mal extrait).

## Limites et critique

- **Gains faibles** : +1,3 point de mAP@0.5 sur VisDrone (Table 4), sans répétitions ni
  écart-type ; la réduction de latence (−6,9 %) est bien plus modeste que celle des
  paramètres (−68,2 %), car les FLOPs ne baissent que de 12,7 % (Table 3) : les couches
  retirées sont lourdes en paramètres mais légères en calcul.
- **SF-YOLOv5L plus lent que YOLOv7** (49,4 ms contre 18,0 ms) malgré moins de FLOPs
  (Table 3) : le « Fast » ne tient pas pour la grande variante, point non discuté.
- **Jeu principal hors drone** (visages WIDER FACE, filtré par les auteurs selon des
  critères non chiffrés) ; VisDrone n'est qu'un test de généralisation, sans split,
  résolution d'origine ni mAP par classe précisés.
- **Pas de mAP_small** : l'amélioration « petits objets » n'est pas isolée par taille.
- **« Déployable sur appareils mobiles »** (§4.4) affirmé sans aucune mesure embarquée :
  GPU RTX 2060 seulement.
- Suppression de P5 : pertinente pour des scènes ne contenant que de petits objets, mais
  pénalise les drones proches ou grands objets (la variante VOC doit rétablir P5).

## Pertinence pour la thèse

- Axe `drone-detection` : illustre une piste **inverse de la tête P2** : spécialiser un
  YOLO pour les petits objets en **retirant** la branche P5, ce qui réduit fortement les
  paramètres (donc la mémoire des poids, critère clé sur FPGA/MCU) (déduit).
- Point de mesure VisDrone (34,3 % mAP@0.5 avec 2,24 M paramètres, Table 4) comparable aux
  YOLO légers du corpus, mais sur GPU de bureau.
- Laisse ouvert : effet de la quantification sur ce modèle, latence sur cible embarquée,
  mAP_small.

## Gaps identifiés

- **Paramètres ≠ latence** : la réduction de 68 % des paramètres ne donne que −7 % de
  latence GPU ; sur accélérateur limité en mémoire (FPGA, MCU), l'effet pourrait être
  inverse — non mesuré.
- **Ablation « supprimer P5 vs ajouter P2 »** sur VisDrone, sous contrainte embarquée :
  absente de ce papier ; à croiser avec les YOLO drone à tête P2.
- mAP_small non rapporté (même constat que dans la plupart des YOLO allégés).

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). L'Abstract est
tronqué (« Compared with the classical YOLOv5, the » : chiffres de fin manquants). La
Table 4 est signalée « sans corps extrait » mais ses lignes apparaissent dans le texte avec
un en-tête mal découpé ; ses valeurs ont été lues avec prudence (ordre des colonnes
déduit de la Table 3).

Ce qui suit est déduit et non affirmé par les auteurs :
- la mesure des temps d'inférence sur la RTX 2060 ;
- l'intérêt de la suppression de P5 pour la mémoire des poids sur FPGA / MCU ;
- l'effet potentiellement différent sur accélérateur limité en mémoire.
