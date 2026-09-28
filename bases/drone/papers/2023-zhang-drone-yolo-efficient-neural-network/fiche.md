---
id: 2023-zhang-drone-yolo-efficient-neural-network
fiche: done
date: 2026-09-28
---

# Drone-YOLO: An Efficient Neural Network Method for Target Detection in Drone Images

Zhengxin Zhang, 2023, Drones 7(8), 526. https://doi.org/10.3390/drones7080526
Type : article de journal (MDPI Drones)

## Problème

Les images de drone diffèrent des jeux « photographe au sol » (COCO, VOC) : vue du dessus,
grandes scènes, objets petits, denses et superposés, éclairage difficile (§1). L'auteur
vise deux usages : traitement après le vol sur poste de bureau (précision maximale) et
traitement en vol sur calculateur embarqué (modèles à peu de paramètres) (§1).

## Méthode

Famille de 5 modèles (nano, tiny, small, medium, large) dérivés de YOLOv8 (Ultralytics
8.0.105) (§3, §4.1) :
- **Tête P2** : PAFPN étendu à 4 niveaux, avec une tête pour petits objets sur une carte de
  160 × 160 à partir de la sortie du stem (§3.2, §5).
- **Sandwich-fusion (SF)** : concatène les cartes de l'étage inférieur (via une convolution
  depthwise séparable à grand noyau : 33, 15 et 7 selon le niveau pour le modèle large),
  de l'étage courant et de l'étage supérieur suréchantillonné ; inspiré du BiC de YOLOv6 3.0
  (§3.2, Table 1).
- **RepVGG** en sous-échantillonnage entre les étages du backbone (re-paramétrisé en une
  seule 3 × 3 à l'inférence) (§3.1).
- Pas de mécanisme d'attention (§3, §5). Tête découplée et pertes (BCE, CIoU + DFL) de
  YOLOv8 inchangées (§3.3).
- Entraînement : 640 × 640, 300 époques, batch 8, **sans pré-entraînement** pour YOLOv8 et
  Drone-YOLO (§4.1, §4.4).

## Plateforme et implémentation

- Entraînement et évaluation de précision : GPU de bureau NVIDIA RTX 3080 Ti, PyTorch,
  CUDA 11.6 (§4.1).
- Test embarqué : NVIDIA Jetson TX2 (GPU Pascal 256 cœurs, 1,33 TFLOPS crête, 8 Go),
  JetPack 4.4.1, CUDA 10.2, cuDNN 8.0.0 (§4.1). Précision numérique, TensorRT ou non,
  taille de batch : n/r.
- Puissance : n/r (aucune mesure, ni sur TX2 ni sur GPU).
- Code et poids : non publiés (aucun lien dans le texte).

## Résultats

VisDrone2019-DET, entrée 640 × 640. « mAP 0.95 » désigne ici mAP@0.5:0.95 (§4.2).

| Modèle | Param. | test mAP50 | test mAP50:95 | val mAP50 | val mAP50:95 | TX2 (ms/image) |
|---|---|---|---|---|---|---|
| YOLOv8-n | 3,00 M | n/r | n/r | 34,0 (TX2) | 19,8 (TX2) | 30,8 |
| YOLOv8-s | 11,1 M | 30,9 | n/r | 39,5 (TX2) | 23,5 (TX2) | 62,1 |
| YOLOv8-l | 76,7 M | 35,9 | 21,2 | 43,7 | 26,9 | n/r |
| Drone-YOLO nano | 3,05 M | 31,0 | 17,5 | 38,1 | 22,7 | 127,4 |
| Drone-YOLO tiny | 5,35 M | 33,7 | 19,1 | 42,8 | 25,6 | 189,5 |
| Drone-YOLO small | 10,9 M | 35,6 | 20,4 | 44,3 | 27,0 | n/r |
| Drone-YOLO medium | 33,9 M | 38,9 | 22,5 | 48,6 | 30,1 | n/r |
| Drone-YOLO large | 76,2 M | 40,7 | 23,8 | 51,3 | 31,9 | n/r |

Sources : Table 4 (test), Table 5 (val), Table 6 (TX2, val).
- Le « +13,4 % » et le « +17,40 % » du résumé sont des **gains relatifs** : 40,7 contre
  35,9 et 51,3 contre 43,7 points de mAP50 (déduit du rapport des Tables 4 et 5).
- Ablation (val, Table 7) : la tête P2 apporte l'essentiel (mAP50 43,7 → 50,5) ; SF
  +0,2 point ; RepVGG +0,6 point.
- Sur val, MS-YOLOv7 [31] (53,1 mAP50) et ACAM-YOLO [30] (49,5, 15,9 M param.) restent
  meilleurs en mAP50 que Drone-YOLO small/medium (Table 5).
- mAP_small (AP_S) : n/r ; seuls des AP50 par classe sur test sont donnés en Fig. 9 (non
  extraite).

→ reportés dans `benchmarks.csv` : 7 lignes. Drone-YOLO nano, tiny, small, medium, large
sur VisDrone2019-test (mAP50, Table 4, GPU de bureau, FPS n/r) ; Drone-YOLO nano et tiny
sur Jetson TX2 (mAP50 val et latence, Table 6).

## Limites et critique

- **Le coût embarqué de la tête P2 et de SF est lourd et non discuté** : sur TX2,
  Drone-YOLO nano met 127,4 ms contre 30,8 ms pour YOLOv8-n à nombre de paramètres égal
  (4,1× plus lent), tiny 189,5 ms contre 62,1 ms pour YOLOv8-s (Table 6). L'auteur conclut
  pourtant à des « highly accurate results » sur TX2 (§5) sans commenter la latence. Le
  nombre de paramètres est un mauvais proxy du coût (carte P2 à 160 × 160, noyaux
  depthwise 33 × 33) ; les GFLOPs ne sont pas donnés.
- **Aucun des modèles n'est temps réel sur TX2** au sens de 30 FPS : 7,8 et 5,3 FPS
  (déduit de 127,4 et 189,5 ms). Pas de TensorRT ni de quantification mentionnés.
- **Mêmes mAP sur TX2 et sur GPU** (38,1/22,7 et 42,8/25,6, Tables 5 et 6) : soit les
  précisions sur TX2 n'ont pas été remesurées, soit l'inférence est en FP32 sans
  changement ; non précisé (déduit).
- **Baselines hétérogènes** : les chiffres des méthodes citées (Table 4-5) viennent des
  papiers d'origine, avec d'autres résolutions, pré-entraînements et protocoles ; YOLOv8
  est ré-entraîné **sans pré-entraînement**, ce qui peut le désavantager face à des
  chiffres publiés avec pré-entraînement (§4.1).
- **Gains relatifs présentés comme des gains absolus** dans le résumé (13,4 % et 17,40 %).
- Incohérences : 5,25 M (résumé) contre 5,35 M paramètres (Tables, §5) pour tiny ; YOLOv8-l
  à 26,9 (Table 5) contre 26,4 (Table 7) de mAP50:95 ; §5 dit « three-layer PAFPN » alors
  que §3.2 décrit une extension à 4 niveaux.
- Pas de puissance, pas de code, un seul auteur, pas de test en vol.

## Pertinence pour la thèse

- **Cas d'école de l'hypothèse « YOLO drone SOTA avec tête P2 rarement porté sur
  embarqué »** : ici il est porté sur Jetson TX2, et la mesure montre un surcoût de latence
  de ×3 à ×4 pour +4 à +5 points de mAP50. C'est un argument chiffré pour la thèse : la
  tête P2 est la brique qui fait gagner le plus en précision (Table 7) et aussi celle qui
  coûte le plus en calcul et en mémoire (déduit).
- Gamme de puissance : Jetson (~10 W, non mesuré). Rien sur FPGA ni MCU.
- Ne mesure ni mAP_small, ni l'effet de la quantification, ni une métrique système.

## Gaps identifiés

- **Tête P2 sur FPGA** : Drone-YOLO nano/tiny (3-5 M paramètres) seraient de bons
  candidats de taille à porter sur un FPGA embarqué, mais la carte P2 à 160 × 160 et les
  convolutions depthwise 33 × 33 posent un problème de mémoire tampon et d'efficacité DSP
  (déduit, à vérifier).
- **Paramètres ≠ latence** sur embarqué pour les YOLO drone : à documenter
  systématiquement (GFLOPs, trafic mémoire, latence mesurée).
- **mAP_small et quantification** : non mesurés, comme prévu par l'hypothèse de la base.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). Fig. 9 (AP50 par
classe sur test, incluant TPH-YOLOv5) non extraite : le « +9,1 % par rapport à
TPH-YOLOv5 » (§4.3) n'a pas pu être vérifié. Tables 2-3 partiellement désalignées à
l'extraction.

Ce qui suit est déduit et non affirmé par les auteurs : le caractère relatif des gains du
résumé ; les FPS sur TX2 (inverse des latences) ; l'hypothèse d'une inférence FP32 ou de
mAP non remesurées sur TX2 ; le coût mémoire de la tête P2 et des grands noyaux sur FPGA.
