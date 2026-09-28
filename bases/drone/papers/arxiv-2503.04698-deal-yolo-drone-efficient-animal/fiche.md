---
id: arxiv-2503.04698-deal-yolo-drone-efficient-animal
fiche: done
date: 2026-09-28
---

# DEAL-YOLO: Drone-based Efficient Animal Localization using YOLO

Aditya Prashant Naidu, Hem Gosalia, Ishaan Gakhar, Shaurya Singh Rathore, Krish Didwania, Ujjwal Verma, 2025, arXiv preprint. https://arxiv.org/abs/2503.04698
Type : preprint non relu par les pairs selon `metadata.json`. L'en-tête du PDF indique le
**workshop ICLR 2025 ML4RS** (Machine Learning for Remote Sensing), un format court de
workshop.

## Problème

Détection de **petits animaux** dans des images de drone pour la conservation de la faune.
Les cibles ne font que quelques pixels et subissent occlusions, camouflage et variations
d'éclairage. Il faut aussi rester **léger** en vue d'un déploiement sur UAV (§1).

## Méthode

Modifications de **YOLOv8-N** (§2, Fig. 1, Annexe A) :
- pertes **Wise-IoU + NWD** (Normalized Wasserstein Distance : les boîtes sont vues comme
  des gaussiennes, pour pondérer davantage le centre des petites boîtes) ;
- **suppression de l'échelle P5**, remplacée par P2 (« P2 for P5 »). Le SPPF passe de 1024
  à 512 canaux ;
- module **SSFF** (Scaled Sequence Feature Fusion, fusion multi-échelle par convolution 3D
  après lissage gaussien) ;
- **LDConv** (convolution déformable linéaire) dans la variante DEAL-YOLO-LD ;
- optimiseur **SOAP** au lieu d'Adam (§3) ;
- **inférence en deux passes** (« confidence-guided adaptive refinement ») : les
  détections sous un seuil de confiance sont recadrées, redimensionnées et réinférées,
  puis fusionnées par NMS (§2).

Entraînement sur des tuiles de 608×513 redimensionnées en 1280, test à 640 (Annexe B).

## Plateforme et implémentation

- **Aucune plateforme matérielle mentionnée**, ni pour l'entraînement ni pour l'inférence.
  Pas de FPS, pas de latence, pas de FLOPs, pas de puissance. L'« efficacité » est mesurée
  **uniquement en nombre de paramètres**.
- Code : non mentionné dans le texte extrait.

## Résultats

BuckTales (Table 1) :

| Modèle | Params (M) | P | R | mAP50 |
|---|---|---|---|---|
| YOLOv8-N | 3,006 | 70,7 | 41,8 | 42,8 |
| YOLOv9-T | 1,972 | 59,7 | 48,8 | **55,8** |
| YOLOv5-N | 2,504 | 46,9 | 53,1 | 48,7 |
| DEAL-YOLO | 0,994 | 75,3 | 58,2 | 48,5 |
| DEAL-YOLO, deux passes | 0,994 | 85,3 | 87,8 | 47,6 |

WAID (Table 2) :

| Modèle | Params (M) | P | R | mAP50 |
|---|---|---|---|---|
| YOLOv5-S | 7,2 | 96,9 | 92,9 | **96,3** |
| YOLOv8-N | 3,01 | 88,5 | 85,4 | 89,7 |
| DEAL-YOLO-LD | 0,914 | 91,1 | 88,9 | 93,4 |
| DEAL-YOLO | 0,994 | 92,0 | 88,8 | 93,3 |
| DEAL-YOLO-LD, deux passes | 0,914 | 95,2 | 94,8 | 90,5 |
| DEAL-YOLO, deux passes | 0,994 | 95,9 | 95,3 | 90,8 |

- Les paramètres baissent de 66,93 % (BuckTales) et de 69,59 % (WAID) par rapport à
  YOLOv8-N (§4).
- Ablations (Tables 3-4) : mAP50-95 de 26,0 → 37,6 dans la Table 4.
- Sensibilité à la résolution de test (Table 5) : sur BuckTales non tuilé, le mAP50
  s'effondre (moins de 8 à 2560 px). Les tuiles sont donc indispensables.

→ reportés dans `benchmarks.csv` : 4 lignes, toutes sur une plateforme `n/r`, avec
précision seulement :
- BuckTales : DEAL-YOLO (48,5) et DEAL-YOLO en deux passes (47,6), Table 1, `high` ;
- WAID : DEAL-YOLO (93,3) et DEAL-YOLO-LD (93,4), Table 2, `high`.

Les incohérences relevées ci-dessous rendent ces chiffres fragiles.

## Limites et critique

- **Allégations contredites par les tableaux.** « Outperforms these baselines by an average
  of 4.8% across all metrics » (§3), alors qu'en mAP50 sur BuckTales DEAL-YOLO (48,5) est
  **sous YOLOv9-T (55,8) et YOLOv5-N (48,7)** (Table 1). Sur WAID, il est sous YOLOv5-S,
  YOLOv7-T, ADD-YOLO et WILD-YOLO (Table 2).
- **L'inférence en deux passes fait baisser le mAP50** : de 48,5 à 47,6 sur BuckTales et de
  93,3 à 90,8 sur WAID. Elle ne fait monter que P et R, mesurés à un seuil de confiance non
  précisé. Pourtant, le texte présente les deux passes comme un gain (§3). Son coût (une
  seconde inférence par région) n'est pas mesuré.
- **Tables 3 et 4 probablement inversées** (déduit) : la Table 3, légendée « BuckTales »,
  donne des mAP50 d'environ 93, qui sont ceux de WAID (Table 2). La Table 4, légendée
  « WAID », a une première ligne identique au YOLOv8-N de BuckTales (70,7/41,8/42,8,
  Table 1). Dans la Table 3, les nombres de paramètres (0,994 contre 0,914) ne
  correspondent pas non plus aux colonnes cochées.
- **Réductions de paramètres incohérentes** : « 68 % » et « 87 % less parameters than
  YOLOv8n » (§3), contre 66,93 % et 69,59 % (§4, Abstract).
- **Comparaisons hétérogènes sur WAID** : chiffres des baselines repris de publications
  (« not all models have published the mAP50 »), donc protocoles différents.
- **Aucune métrique de coût réel.** Retirer P5 et ajouter P2 réduit les paramètres mais
  **augmente probablement les FLOPs** (cartes haute résolution), ce que le papier ne
  mesure pas (déduit). LDConv (déformable) est typiquement peu adapté aux accélérateurs
  (déduit).
- Annotations jugées imprécises par les auteurs eux-mêmes (Annexe C). L'évaluation en
  souffre.

## Pertinence pour la thèse

- **Axe détection drone et petits objets**, hors vision « véhicules » (faune). C'est un
  exemple de l'échange **P5 → P2**, qui réduit les paramètres pour les petits objets. Il
  illustre l'hypothèse du profil : les YOLO drone à tête P2 ne sont jamais évalués en
  FLOPs, latence ou énergie sur une cible embarquée.
- Pertes WIoU et NWD et inférence en deux passes : idées réutilisables. Mais les résultats
  présentés ici ne démontrent pas leur intérêt (voir Limites).
- **Faible valeur de preuve** : format workshop, tableaux incohérents.

## Gaps identifiés

- **Tête P2 sans P5 : coût réel inconnu.** Les paramètres baissent mais FLOPs et mémoire
  d'activations augmentent vraisemblablement. C'est à mesurer sur FPGA ou Jetson, et c'est
  directement lié à l'hypothèse « tête P2 non portée sur FPGA ».
- **Inférence en deux passes ou recadrage adaptatif** : coût en latence non mesuré.
  Question commune avec SAHI.
- **Détection de faune par drone embarquée** : aucun chiffre embarqué dans ce papier.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). Le titre du PDF porte
l'en-tête du workshop ICLR 2025 ML4RS. La fin de l'Annexe C est tronquée. La liste des
contributions (§1) ne compte qu'une puce. Les tableaux sont extraits avec leur corps, mais
les colonnes cochées des Tables 3-4 sont mal alignées.

Ce qui suit est déduit et non affirmé par les auteurs :
- l'inversion probable des Tables 3 et 4 ;
- la hausse probable des FLOPs avec P2 ;
- la faible adéquation de LDConv aux accélérateurs.
