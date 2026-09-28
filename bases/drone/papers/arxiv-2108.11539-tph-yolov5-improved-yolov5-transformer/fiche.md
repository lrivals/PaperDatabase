---
id: arxiv-2108.11539-tph-yolov5-improved-yolov5-transformer
fiche: done
date: 2026-09-28
---

# TPH-YOLOv5: Improved YOLOv5 Based on Transformer Prediction Head for Object Detection on Drone-captured Scenarios

Xingkui Zhu, Shuchang Lyu, Xu Wang, Qi Zhao, 2021, arXiv preprint. https://arxiv.org/abs/2108.11539
Type : preprint non relu par les pairs (rapport de challenge VisDrone 2021 ; une version
atelier ICCV 2021 existe probablement, non mentionnée dans le texte, à vérifier)

## Problème

Sur images de drone, trois difficultés : **variation d'échelle violente** (altitude
variable), **forte densité** d'objets (occlusions), **grandes zones couvertes** avec
éléments géographiques trompeurs ; le flou de mouvement s'y ajoute (Abstract, §1, Fig. 1).
Les détecteurs conçus pour COCO / VOC s'y transposent mal (§1).

## Méthode

- Base **YOLOv5x** (CSPDarknet53 + SPP, neck PANet), choisie car > 1,5 point d'AP devant
  s, m, l sur VisDrone (§3.1).
- **4e tête de prédiction** sur une carte haute résolution, pour les objets minuscules
  (la « tête P2 ») (§3.2).
- **Transformer Prediction Heads (TPH)** : blocs encodeurs transformer (attention
  multi-têtes + MLP) à la fin du backbone et dans les têtes, sur les cartes basse
  résolution pour limiter coût et mémoire ; certains retirés quand l'entrée grandit
  (§3.2, Fig. 3-4).
- **CBAM** (attention canal puis spatiale) dans le neck (§3.2, Fig. 5).
- **Bag of tricks** : MixUp + Mosaic + distorsions ; objets < 3 px masqués en gris à
  l'entraînement (+0,2 mAP) ; **ms-testing** (6 versions de l'image : 1,3 / 1 / 0,83 /
  0,67 + flip, fusion NMS) ; **ensemble de 5 modèles** fusionnés par WBF ; **classifieur
  ResNet18** auto-entraîné sur patchs 64×64 pour les classes confondues (tricycle /
  awning-tricycle), +0,8 à 1,0 point d'AP (§1, §3.2, §4.1).
- Entraînement 65 époques, Adam, côté long **1536 px**, batch 2 (§4.1).

## Plateforme et implémentation

**NVIDIA RTX 3090** pour l'entraînement et le test, PyTorch 1.8.1 (§4.1). Vitesse (FPS),
latence, mémoire, puissance : **n/r**. Coût : YOLOv5x 219,0 GFLOPs → 259,0 avec la 4e
tête (607 → 719 couches) → 237 avec les blocs transformer (705 couches) (§4.3). Code : non
mentionné dans le texte extrait (n/r).

## Résultats

- **VisDrone2021-DET test-challenge** : ensemble **mAP 39,18 %** (mAP@[.5:.95]), contre
  37,37 pour DPNetV3 (SOTA 2020) ; **5e** du challenge 2021, à 0,25 point du premier
  (39,43) (Abstract, §4.2, Table 1). AP50 : 62,05 (fragment de Table 1, attribution à
  confirmer).
- **test-dev**, mAP par modèle (Table 3) :

| Modèle | Réglage | mAP (all) | car | bicycle | awning-tricycle |
|---|---|---|---|---|---|
| TPH-YOLOv5-1 | 1920, poids égaux | 34,90 | 65,99 | 15,21 | 22,11 |
| TPH-YOLOv5-2 | 1536, poids égaux | 34,29 | 67,63 | 14,17 | 20,48 |
| TPH-YOLOv5-3 | 1920, poids ∝ 1/labels | 34,68 | 48,88 | 19,26 | 35,65 |
| TPH-YOLOv5-4 | 1536, poids ∝ 1/labels | 34,17 | 49,99 | 17,62 | 32,21 |
| TPH-YOLOv5-5 | backbone YOLOv5l, 1536 | 33,04 | 63,05 | 13,10 | 21,06 |
| Ensemble | WBF des 5 | 37,32 | 68,94 | 15,69 | 24,72 |

- Gain annoncé face à YOLOv5 : « about 7 % » (Abstract ; Table 2, ablation, non
  extraite).
- La 4e tête améliore fortement le mAP sur petits objets (§4.3, qualitatif, Fig. 9) ; les
  blocs transformer augmentent le mAP tout en réduisant GFLOPs et couches (§4.3).

→ reportés dans `benchmarks.csv` : 7 lignes, toutes sur RTX 3090, FPS n/r : ensemble
test-challenge (39,18, `medium`, texte §4.2) ; ensemble et 5 modèles sur test-dev
(37,32 ; 34,90 ; 34,29 ; 34,68 ; 34,17 ; 33,04 ; Table 3, `high`).

## Limites et critique

- **Rapport de challenge orienté précision, aucune contrainte embarquée** : entrée 1536 à
  1920 px, YOLOv5x à ~237-259 GFLOPs, ms-testing ×6, ensemble ×5, classifieur
  supplémentaire : le résultat principal (39,18) coûte de l'ordre de 30 inférences
  YOLOv5x par image (déduit). Aucune vitesse rapportée, même sur RTX 3090.
- **Titre trompeur pour la thèse** : « drone-captured scenarios » désigne les images, pas
  un calcul à bord.
- **Ablation (Table 2) non extraite** : la contribution isolée de la tête P2, des TPH et de
  CBAM n'est pas lisible ; le « about 7 % » ne dit pas s'il s'agit de points ou de relatif.
- **Pas de mAP_small** ni d'AP par taille, alors que la 4e tête vise les objets minuscules ;
  l'argument petits objets est qualitatif (Fig. 9).
- Comparaison aux scores de challenge d'années précédentes (mêmes données, VisDrone
  2019-2021 identiques, §4) : acceptable, mais les méthodes comparées utilisent aussi des
  ensembles de tailles différentes (non détaillé).
- Pondération des classes : gain sur classes rares (bicycle, awning-tricycle), perte nette
  sur « car » (−17 points, Table 3) : le mAP global cache ces arbitrages.

## Pertinence pour la thèse

- **Axe `drone-detection`** : c'est **la** référence de l'architecture « YOLO drone SOTA »
  visée par l'hypothèse de gaps.md : **tête P2 + blocs transformer + attention (CBAM)**.
  Tout projet de portage FPGA d'un YOLO drone doit se positionner par rapport à elle.
- Donne un repère de coût : la tête P2 ajoute ~40 GFLOPs (+18 %) à YOLOv5x, les TPH en
  retirent ~22 (§4.3). Pour l'embarqué, la question est la même à l'échelle
  YOLOv5n/s, **non traitée ici**.
- Suite directe dans la base : TPH-YOLOv5++ (2023-zhao-tph-yolov5-boosting-object-detection,
  Remote Sensing 2023), qui s'attaque au coût.

## Gaps identifiés

- **TPH-YOLOv5 (tête P2 + transformer) sur FPGA / Jetson** : aucune mesure de vitesse ni
  de puissance ; confirme l'hypothèse « les YOLO drone SOTA ne sont presque jamais portés
  sur FPGA ».
- **Coût matériel des blocs transformer dans la tête** (attention, LayerNorm, softmax) sur
  accélérateur embarqué : non évalué.
- **Gain de la tête P2 sur mAP_small** : non chiffré ici ; à mesurer avec quantification.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). **Tables 1 et 2 sans
corps extrait** : Table 1 partiellement recollée dans le texte de §4.2 (scores des
méthodes antérieures, dernière colonne AP50 de DPNetV3 et ligne TPH-YOLOv5 perdues sauf un
« 62,05 » isolé) ; **Table 2 (ablation) absente**. Table 3 lisible. Une partie de §4.3
(effet de l'ensemble) est rejetée dans les légendes de figures.

Ce qui suit est déduit et non affirmé par les auteurs :
- le coût d'environ 30 inférences YOLOv5x par image pour le résultat challenge ;
- l'attribution de 62,05 à l'AP50 de TPH-YOLOv5 ;
- la publication en atelier ICCV 2021.
