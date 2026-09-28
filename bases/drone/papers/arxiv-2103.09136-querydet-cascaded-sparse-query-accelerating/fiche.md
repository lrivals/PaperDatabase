---
id: arxiv-2103.09136-querydet-cascaded-sparse-query-accelerating
fiche: done
date: 2026-09-28
---

# QueryDet: Cascaded Sparse Query for Accelerating High-Resolution Small Object Detection

Chenhongyi Yang, Zehao Huang, Naiyan Wang, 2021, arXiv preprint. https://arxiv.org/abs/2103.09136
Type : preprint non relu par les pairs (d'après `metadata.json` ; une version publiée existe
peut-être, à vérifier : le texte extrait ne donne pas de venue).

## Problème

Les petits objets demandent des cartes de caractéristiques haute résolution, mais le coût
des têtes de détection croît au carré avec la résolution. Ajouter un niveau P2 à RetinaNet
représente environ 300 % de FLOPs et de mémoire en plus dans la tête, et fait passer
l'inférence de 13,6 à 4,85 FPS sur une NVIDIA 2080Ti (§1). La tête P3 représente déjà près
de la moitié des FLOPs ; avec P2, P2 et P3 en représentent 75 % (§3.1, Fig. 2). Or les
petits objets sont spatialement épars : l'essentiel de ce calcul porte sur du fond (§1).

## Méthode

- **Cascade Sparse Query (CSQ)** : une « query head », parallèle aux têtes de
  classification et de régression, prédit sur un niveau basse résolution P_l une heatmap de
  présence de petits objets. Les positions au-dessus du seuil σ sont projetées sur leurs
  4 voisins de P_{l-1} (Éq. 1). Les têtes n'y sont calculées qu'à ces positions, en
  convolution éparse (spconv), avec les poids des têtes denses (§3.2).
- **En cascade** : les requêtes de P_{l-2} ne viennent que des positions retenues sur
  P_{l-1}, ce qui évite l'explosion du nombre de positions (§3.2).
- **Entraînement** : focal loss sur une carte binaire autour des centres des petits objets
  (Éq. 2-4). Les pertes des niveaux sont repondérées par β_l, qui croît linéairement de 1 à
  3 sur COCO et de 1 à 2,6 sur VisDrone ; sans cela, P2 domine l'entraînement (§3.3, §4.1).
- **Réglages** : σ = 0,15, requête à partir de P4, contexte de 5×5 autour de chaque
  position (§4.1, Table 6). Base RetinaNet ResNet-50 ; généralisé à FCOS (Table 8) et au
  RPN de Faster R-CNN (Table 9).
- Sur VisDrone, chaque image est coupée en 4 patches sans recouvrement pour
  l'entraînement (§4.1). Pas de quantification ni d'élagage : les auteurs disent la méthode
  compatible avec ces techniques sans le tester (§1).

## Plateforme et implémentation

- PyTorch + Detectron2, entraînement sur 8 NVIDIA 2080Ti en précision mixte (§4.1).
- Plateforme d'inférence : NVIDIA 2080Ti, dite explicitement seulement pour l'exemple
  RetinaNet+P2 de l'introduction (§1), dont les chiffres coïncident avec la Table 1. Pour
  VisDrone (Table 2) et les backbones légers (Table 7), la plateforme n'est pas redite
  (n/r). Batch d'inférence, précision d'inférence et résolution des Tables 1-2 : n/r.
- Aucune plateforme embarquée (Jetson, FPGA, MCU) testée. Puissance : n/r.
- Code publié : https://github.com/ChenhongyiYang/QueryDet-PyTorch (Abstract).

## Résultats

| Config. | Jeu | AP | AP_S | FPS | Source |
|---|---|---|---|---|---|
| RetinaNet R50 | COCO mini-val | 37,46 | 22,64 | 13,60 | Table 1 |
| QueryDet sans CSQ (P2) | COCO | 38,53 | 24,64 | 4,85 | Table 1 |
| QueryDet avec CSQ | COCO | 38,36 | 24,33 | 14,88 | Table 1 |
| QueryDet (3x) avec CSQ | COCO | 39,34 | 24,91 | 15,94 | Table 1 |
| RetinaNet R50 | VisDrone val | 26,21 (AP50 44,90) | n/r | 2,63 | Table 2 |
| QueryDet sans CSQ | VisDrone | 28,35 (AP50 48,21) | n/r | 1,16 | Table 2 |
| QueryDet avec CSQ | VisDrone | 28,32 (AP50 48,14) | n/r | 2,75 | Table 2 |
| RetinaNet MobileNetV2 → QueryDet CSQ | COCO | 26,72 → 28,94 | 15,27 → 15,74 | 17,75 → 21,66 | Table 7 |
| RetinaNet ShuffleNetV2 → QueryDet CSQ | COCO | 23,04 → 25,85 | 12,01 → 12,81 | 17,45 → 20,02 | Table 7 |
| FCOS → QueryDet (FCOS) CSQ | COCO | 38,37 → 39,49 | 22,34 → 24,81 | 17,06 → 14,40 | Table 8 |
| Faster R-CNN QueryDet, sans → avec CSQ | COCO | 38,47 (AP_S 22,98) | n/r | 17,57 → 19,03 | §4.4 (Table 9 non extraite) |

- CSQ ramène la part de P2+P3 dans les FLOPs de 74 % à environ 1 % (§4.2, Fig. 2).
- Le gain de vitesse de la partie haute résolution est de 3,0× en moyenne sur COCO et de
  2,3× sur VisDrone (Abstract) ; 4,1× avec MobileNetV2 et 3,8× avec ShuffleNetV2 (§4.4).
- Ablation (Table 3, §4.3) : P2 sans repondération fait **perdre** 1,34 AP ; la
  repondération ramène à 38,11 ; la query head ajoute 0,42 AP et 1,58 AP_S.
- Départ de requête : P4 est le plus rapide (14,88 FPS), P3 donne 11,51 FPS (Table 4).
  CSQ bat les variantes Crop Query (10,49 FPS) et Complete Convolution Query (8,73 FPS)
  (Table 5).

→ reportés dans `benchmarks.csv` (fichier du lot) : 6 lignes. VisDrone avec et sans CSQ
(Table 2, `medium` : tableau reconstruit par PyMuPDF, recoupé par le §4.2 et un second
extrait du même tableau) ; COCO 1x avec et sans CSQ (Table 1, 2080Ti d'après §1) ; COCO
MobileNetV2 et ShuffleNetV2 avec CSQ (Table 7, plateforme n/r).

## Limites et critique

- **Rien d'embarqué** : toutes les vitesses sont mesurées sur GPU de bureau (2080Ti,
  250 W de TDP, ordre de grandeur connu, non donné par le papier). L'affirmation « ready to
  deploy on edge devices » (§4.4) n'est étayée par aucune mesure sur Jetson, FPGA ou MCU.
  Cas typique de résultat de bureau présenté comme utilisable en embarqué.
- **VisDrone reste très lent** : 2,75 FPS même avec CSQ (Table 2), à une résolution
  d'entrée non précisée dans le texte extrait (la Fig. 4 évoque 1600 à 2400 px). Le « new
  state-of-the-art » est affirmé sans tableau de comparaison avec d'autres méthodes
  VisDrone dans le texte extrait.
- **La convolution éparse est défavorable aux accélérateurs** : l'accélération repose sur
  spconv (gather/scatter, indices irréguliers), dont le gain sur FPGA ou NPU n'est pas
  acquis (déduit). Le gain est aussi dépendant du contenu : une scène dense en petits
  objets (foule, parking vu de drone) réduit l'épargne, et de grands objets mal activés
  ralentissent l'inférence (§4.5). Latence donc variable d'une image à l'autre, non
  mesurée (pire cas, gigue).
- Le gain porte sur la tête seule : avec un backbone lourd (R50), le coût du backbone
  n'est pas touché (§4.4).
- AP COCO-style [.5:.95] sur VisDrone, non comparable à un mAP@0.5 de papiers YOLO drone.
  AP_S non rapporté sur VisDrone (seulement AR), alors que c'est le cœur du sujet.
- Un seul run, sans variance ; baseline RetinaNet retrainée par les auteurs.
- Typo dans le texte : « improved to 2.3× from 1.16 FPS from 2.75 FPS » (§4.2) ; la Table 2
  donne 1,16 → 2,75 FPS (2,4×), et le RetinaNet sans P2 tourne à 2,63 FPS.

## Pertinence pour la thèse

- **Axe `drone-detection`** : idée structurante pour le gap « tête P2 non portée sur
  FPGA ». QueryDet montre que le coût de P2 est surtout spatial et évitable : on peut
  obtenir le gain d'AP_S de P2 (+2,0 AP_S sur COCO, Table 1) au coût d'un détecteur sans
  P2.
- Ouvre une question matérielle directe : **calcul épars guidé par requête sur FPGA**.
  Un FPGA peut, en principe, exploiter une sparsité spatiale structurée par tuiles mieux
  qu'un GPU (déduit, non testé dans le papier). Variante plus compatible matériel : Crop
  Query sur tuiles fixes (Table 5), proche de AutoFocus ou du découpage en tuiles de
  UFPMP-Det.
- Le papier ne dit rien de la puissance, de la latence pire cas ni du comportement sur une
  vraie plateforme de drone : tout reste à mesurer.

## Gaps identifiés

- **Calcul épars (query/tuiles) pour petits objets jamais évalué sur FPGA / Jetson /
  MCU** : QueryDet ne donne que des FPS sur 2080Ti.
- **Latence dépendante du contenu** : aucune mesure de la gigue ni du pire cas quand la
  scène est dense ; critique pour un budget temps réel à bord.
- **AP_S non rapporté sur VisDrone** malgré le sujet « petits objets » : à rapprocher du
  gap mAP_small.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). Les légendes de
tableaux sont décalées dans l'extraction (le corps de la Table 7 apparaît sous la légende
de la Table 6, etc.) ; les attributions ci-dessus suivent le contenu et le texte. La
Table 2 (VisDrone) est reconstruite par PyMuPDF, mais ses valeurs sont recoupées par un
second extrait identique et par le §4.2. La Table 9 (Faster R-CNN) n'a pas de corps
extrait : seuls les chiffres cités au §4.4 sont connus. La Table 3 (ablation) n'a pas de
corps exploitable (le corps affiché est celui de la Fig. 4) ; ses chiffres viennent du §4.3.
La section « Spatial… » des travaux liés est tronquée.

Ce qui suit est déduit et non affirmé par les auteurs :
- la plateforme d'inférence 2080Ti pour la Table 1 (déduite du §1, chiffres identiques) ;
- l'inadéquation de spconv aux accélérateurs et l'intérêt d'une version par tuiles sur FPGA ;
- la variabilité de latence selon la densité de la scène ;
- l'existence éventuelle d'une version publiée du papier.
