---
id: 2023-fu-efficient-yolov7-drone-enhanced-object
fiche: done
date: 2026-09-28
---

# Efficient YOLOv7-Drone: An Enhanced Object Detection Approach for Drone Aerial Imagery

Xiaofeng Fu, Guoting Wei, Xia Yuan, Yongshun Liang, Yuming Bo, 2023, Drones 7(10), 616. https://doi.org/10.3390/drones7100616
Type : article de journal (MDPI Drones)

## Problème

Les drones à voilure tournante bas coût ont peu de calcul ; leurs images contiennent
beaucoup de petits objets denses et un premier plan minoritaire (§1, Fig. 1). Les méthodes
précises (coarse-to-fine, Transformers) s'appuient sur des entrées haute résolution et sont
jugées trop coûteuses pour le temps réel à bord (§1, §2.2-2.3). Les auteurs veulent un
détecteur à **entrée basse résolution (640×640)** qui reste précis sur les petits objets.

## Méthode

Base : YOLOv7 standard (§3.1). Modifications (§3.2-3.4, Fig. 2) :
- **A — tête P2** ajoutée (features du stage 2 du backbone) pour les objets minuscules ;
- **B — tête P5 et stage 5 du backbone supprimés** : −56,29 % de paramètres (§3.2) ;
- **C — CBS entre backbone et neck** : réduction de canaux par 2 au lieu de 4, neck adapté ;
- **D — TGM-CESC** : convolution creuse (masque Gumbel-Softmax, dérivée de CEASC [21]) qui
  remplace RepConv dans la tête ; le masque est contraint pixel à pixel par une carte
  binaire premier plan / fond tirée des vérités terrain (perte type Dice, Éq. 2) ;
- **E — HCEM** : fusion descendante P2 → P3 → P4 (CBS stride 2 + concaténation, Éq. 6)
  pour compenser la perte d'information due au masque.
Perte totale L = L_det + L_norm + L_mask (Éq. 5). Entraînement 200 époques, batch 8, SGD,
640×640, pré-entraînement partiel YOLOv7 (§4.2).

## Plateforme et implémentation

- **GPU de bureau NVIDIA RTX 3090**, entraînement et test (§4.2). Aucune exécution sur
  plateforme embarquée (Jetson, FPGA, MCU).
- Précision numérique, batch d'inférence et méthode de mesure des FPS : n/r. Puissance : n/r.
- Code : non publié (aucun lien dans le texte).

## Résultats

VisDrone (validation, protocole des auteurs) et UAVDT :

| Config | Jeu | Entrée | AP (mAP@0.5:0.95) | AP50 | AP75 | Source |
|---|---|---|---|---|---|---|
| Efficient YOLOv7-Drone | VisDrone val | 640 | 32,1 | 53,6 | 32,5 | Table 2 |
| Efficient YOLOv7-Drone | VisDrone val | 1280 | 39,9 | 62,5 | 42,1 | Table 3 |
| id., multi-échelle (#) | VisDrone val | 1280 | 40,9 | 63,5 | 43,6 | Table 3 |
| Efficient YOLOv7-Drone | UAVDT | 640 | 20,0 | 36,0 | 20,1 | Table 4 |

Ablation (Table 5, VisDrone, RTX 3090) :

| Config | mAP | Params | GFLOPs | FPS |
|---|---|---|---|---|
| YOLOv7 baseline | 28,6 | 36,53 M | 103,3 | 212,76 |
| +A (P2) | 29,3 | 40,46 M | 118,2 | 136,99 |
| +A+B (sans P5) | 30,0 | 17,68 M | 115,2 | 166,67 |
| +A+B+C | 31,0 | 19,16 M | 153,1 | 138,89 |
| +A+B+C+D (TGM-CESC) | 31,5 | 29,99 M | 133,0 | 96,15 |
| +A+B+C+D+E (final) | 32,1 | 31,79 M | 144,6 | **89,29** |

- **mAP_small** : 19,4 % (baseline) → 20,3 % (+P2, Table 9) → 22,0 % (+A+B+C, Table 12) ;
  **n/r pour le modèle final**.
- Par tête (Table 10) : la tête P2 a un mAP_s de 12,2 % ; P5 n'est meilleure que P4 que sur
  les grands objets (58,2 contre 42,3 % mAP_l).
- TGM contre AMM (CEASC) : 29,4 contre 28,0 % mAP, AR +3,5 points (Table 14).
- Validation croisée 5 plis sur train+val VisDrone : 32,6 → 33,1 (+TGM-CESC) → 33,3 %
  (+HCEM) de mAP moyen (Tables 6-8), écarts de 0,5 et 0,2 point.

→ reportés dans `benchmarks.csv` : 3 lignes (640 VisDrone avec FPS de la Table 5 ; 1280
VisDrone et 640 UAVDT sans FPS), plateforme RTX 3090.

## Limites et critique

- **« Efficient » contredit par la Table 5** : le modèle final fait 144,6 GFLOPs contre
  103,3 pour YOLOv7, et **89 FPS contre 213 FPS** sur RTX 3090, soit 2,4 fois plus lent que
  la baseline. La convolution creuse réduit les GFLOPs par rapport à l'étape précédente mais
  réduit aussi les FPS (§4.4.1 le reconnaît). Le gain en efficacité n'existe que face aux
  méthodes coarse-to-fine haute résolution (Table 2), dont les FPS ne sont pas donnés.
- **Résultats sur GPU de bureau présentés comme adaptés au drone** : aucune mesure sur Jetson
  ou autre cible embarquée, aucune puissance. Le « temps réel » est affirmé sur RTX 3090
  (~350 W de TDP, déduit de la fiche NVIDIA, non dit dans le papier). Cas exclu par le profil
  pour les résultats « embarqués ».
- La convolution creuse n'accélère que si le matériel sait exploiter les masques ; sur GPU
  dense elle ralentit (déduit de la Table 5). Sur FPGA, elle demanderait un support dédié.
- **Comparaisons SOTA hétérogènes** : backbones, résolutions et même protocoles différents ;
  « all test results are based on the validation set » (§4.1). Les FPS des méthodes
  comparées sont absents des Tables 2-4.
- Incohérence : §4.4.1 dit que retirer P5 réduit « GPU memory overhead by 56.32% » alors que
  la Table 5 donne des paramètres (40,46 → 17,68 M) ; la mémoire GPU n'est pas tabulée.
  GFLOPs de A+B+C (153,1) supérieurs à ceux de A+B+C+D (133,0) : plausible (sparse), mais
  le calcul des GFLOPs creux n'est pas expliqué.
- Gains modestes (0,2 à 0,5 point en validation croisée) sans écart-type ni test
  statistique.

## Pertinence pour la thèse

- **Exemple type des YOLO drone SOTA** (tête P2, P5 supprimée, attention au premier plan)
  jamais portés sur cible embarquée : alimente l'hypothèse « tête P2 non portée sur FPGA »
  de `gaps.md`.
- Donne un **point de mAP_small** (19,4 → 22,0 % avec P2 et CBS, Tables 9 et 12), utile
  comme référence FP32 pour mesurer ensuite l'effet d'une quantification.
- L'idée « supprimer P5 et le stage 5 » (−56 % de paramètres, Table 5) est intéressante pour
  un portage FPGA (moins de poids en BRAM), à l'inverse de la tête P2 qui coûte en mémoire
  d'activations (déduit).
- La convolution creuse guidée par le premier plan est un levier matériel possible (calcul
  conditionnel sur FPGA), non évalué ici.

## Gaps identifiés

- **Tête P2 + suppression de P5 sur FPGA/Jetson** : aucune mesure embarquée ; coût en
  mémoire et en bande passante de la P2 inconnu.
- **Convolution creuse sur accélérateur** : le gain théorique ne se traduit pas en FPS sur
  GPU ; aucune étude sur FPGA dans ce papier.
- **mAP_small du modèle final** non rapporté, et aucune étude de quantification.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). Tables 9, 12 et 14
signalées sans corps extrait : leurs lignes sont pourtant présentes dans le texte extrait
(en-têtes coupés), chiffres lus ; la Table 13 (placement de TGM-CESC) n'a pas de corps.
L'algorithme 1 est tronqué dans l'extraction.

Ce qui suit est déduit et non affirmé par les auteurs :
- le ralentissement de 2,4× du modèle final face à YOLOv7 (calculé depuis la Table 5) ;
- le TDP de la RTX 3090 ;
- l'intérêt de la suppression de P5 pour un portage FPGA et le coût mémoire de la P2 ;
- l'inefficacité de la convolution creuse sur GPU dense.
