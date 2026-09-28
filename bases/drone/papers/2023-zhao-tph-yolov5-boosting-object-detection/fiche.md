---
id: 2023-zhao-tph-yolov5-boosting-object-detection
fiche: done
date: 2026-09-28
---

# TPH-YOLOv5++: Boosting Object Detection on Drone-Captured Scenarios with Cross-Layer Asymmetric Transformer

Qi Zhao, Binghao Liu, Shuchang Lyu, Chunlei Wang, Hong Zhang, 2023, Remote Sensing 15(6), 1687. https://doi.org/10.3390/rs15061687
Type : article de journal (extension de TPH-YOLOv5, ICCVW 2021 [20])

## Problème

Trois difficultés des images de drone : forte variation d'échelle (altitude, tangage),
objets minuscules et denses avec occlusions, grandes scènes confuses (§1, Fig. 1). La
version précédente, TPH-YOLOv5, les traitait par une tête de prédiction supplémentaire
(P2 « tiny »), au prix de +60 % de mémoire GPU et d'environ −50 % de FPS, et de nombreux
faux positifs sur les jeux peu denses comme UAVDT (§1, §3.3.1).

## Méthode

- **TPH-YOLOv5** (base YOLOv5x) : 4 têtes (tiny, small, medium, large), têtes à
  **transformer** (ViT puis Swin), **CBAM**, augmentation de données, multi-scale testing
  fusionné par WBF, ensemble de modèles, classifieur auxiliaire tricycle / awning-tricycle
  (§3.2).
- **TPH-YOLOv5++** : suppression de la tête tiny ; un module **CA-Trans** (cross-layer
  asymmetric transformer) injecte l'information du chemin tiny (K, V) dans le chemin small
  (Q) par une **sparse local attention (SLA)** limitée à un voisinage a×b (2×2 retenu), puis
  un extracteur d'information « asymétrique » (AFE) qui inverse la matrice de relation
  (§3.3, Fig. 6-8, Algorithm 1, Éq. 12-14).
- Entraînement : poids partiellement transférés de YOLOv5x, Adam, 65 epochs, entrée
  1536×1536, batch 2 sur VisDrone ; 30 epochs, entrée 1024, batch 4 sur UAVDT (§4.1.2).

## Plateforme et implémentation

GPU de bureau uniquement : **NVIDIA RTX 3090 Ti** pour l'entraînement et le test (§4.1.2).
Précision, batch d'inférence, prise en compte du NMS / WBF dans les FPS : n/r. Puissance :
n/r. Aucune plateforme embarquée. **Code publié** : https://github.com/cv516Buaa/tph-yolov5
(§1).

## Résultats

| Config. | Jeu | AP (%) | AP50 | AP75 | GFLOPs | FPS | Source |
|---|---|---|---|---|---|---|---|
| YOLOv5x | VisDrone test-dev | 28,9 | 45,4 | 30,8 | 200,2 | 13,68 | Table 5 |
| TPH-YOLOv5 (Swin+CBAM) | VisDrone test-dev | 34,0 | 53,2 | 35,8 | 315,4 | 7,36 | Table 5 |
| TPH-YOLOv5++ | VisDrone test-dev | 33,1 | 52,1 | 35,1 | 207,0 | 11,86 | Table 5 |
| TPH-YOLOv5 | UAVDT test | 26,9 | 41,3 | 32,7 | 556,6 | 25,12 | Table 6 |
| TPH-YOLOv5++ | UAVDT test | 30,1 | 43,5 | 34,3 | 293,2 | 42,19 | Table 6 |

- VisDrone 2021 test-challenge : TPH-YOLOv5 39,18 % AP, 4e place (§4.2 ; corps de la
  Table 1 non extrait). Le résumé donne 39,43 % pour la 1re place.
- VisDrone val : TPH-YOLOv5 42,1 % AP, TPH-YOLOv5++ 41,4 % (Table 2), au-dessus
  d'UFPMP-Net (39,2).
- Test-dev : les deux restent sous ViT-YOLO (38,5 % AP, Table 3).
- La tête P2 seule : +2,1 pts AP, mémoire GPU 4279 → 4667 Mo, FPS 13,68 → 10,89 (Table 5).
- Voisinage SLA : (2,2) retenu ; (4,4) et (6,6) font monter la mémoire à 7475 et 12185 Mo
  (§4.3.4 ; corps de la Table 8 non extrait).

→ reportés dans `benchmarks.csv` : 5 lignes (TPH-YOLOv5 Swin+CBAM et TPH-YOLOv5++ sur
VisDrone test-dev, Table 5 ; les deux sur UAVDT, Table 6 ; TPH-YOLOv5 sur le
test-challenge, §4.2), toutes sur RTX 3090 Ti.

## Limites et critique

- **Aucun résultat embarqué** : 7 à 12 FPS sur une RTX 3090 Ti (~450 W de TDP, déduit) pour
  VisDrone à 1536×1536. Transposé sur un Jetson ou un FPGA, ce modèle à ~200-300 GFLOPs
  serait loin du temps réel (déduit). « Improve the detection speed » s'entend uniquement
  relativement à TPH-YOLOv5 sur GPU de bureau.
- **Comparaisons SOTA hétérogènes** : les chiffres des concurrents (Tables 2-4) sont repris
  de leurs papiers, à résolutions, backbones et stratégies (crops, ensembles) différents.
  Le 39,18 % du challenge a vraisemblablement été obtenu avec les « tricks » annoncés en §1
  (ms-testing, ensemble, classifieur auxiliaire), pas avec le modèle seul (déduit : la
  configuration exacte de la soumission n'est pas détaillée).
- **Incohérence apparente** : TPH-YOLOv5 affiche 556,6 GFLOPs et 25 FPS sur UAVDT (entrée
  1024) contre 315,4 GFLOPs et 7,4 FPS sur VisDrone (entrée 1536) (Tables 5-6) ; la façon de
  compter n'est pas expliquée.
- FPS sans batch ni précision déclarés ; le coût du post-traitement (NMS, WBF, ms-testing)
  n'est pas isolé.
- Le gain de TPH-YOLOv5++ sur VisDrone est négatif en précision (−0,9 pt AP) : l'intérêt est
  l'efficacité, pas la précision, sauf sur UAVDT.

## Pertinence pour la thèse

- **Référence centrale de la famille « YOLO drone SOTA à tête P2 + Transformer »**, exactement
  celle que l'hypothèse de `gaps.md` dit jamais portée sur FPGA. Sert de borne haute de
  précision sur VisDrone / UAVDT et de repère de coût (GFLOPs, mémoire) pour un portage.
- L'analyse du coût de la tête P2 (Table 5) et l'idée de la remplacer par un transfert
  d'information vers P3 (CA-Trans) sont directement pertinentes pour un co-design matériel :
  réduire la résolution des activations traitées est ce qui compte sur FPGA (déduit).
- Code publié : base de reproduction possible (entraînement, puis quantification / export).

## Gaps identifiés

- Portage de TPH-YOLOv5 / TPH-YOLOv5++ (attention, Swin, CBAM) sur Jetson, FPGA ou NPU :
  absent ; coût de la SLA sur accélérateur inconnu.
- Effet de la quantification INT8 sur l'AP des petits objets pour ces modèles : non mesuré.
- Aucune mesure de puissance, même sur GPU.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). Manques signalés :
corps de la **Table 1** (classement du challenge) absent ; **Table 8** (voisinage SLA)
sans corps, seuls les chiffres cités dans le texte sont lus ; la Table 7 est présente
malgré l'avertissement, mais colonnes partiellement fusionnées. La section 4 n'a pas été
détectée comme titre ; une partie de §3.3.3 (fin de l'Algorithm 1, Éq. 8-11) est mêlée à
§4.1.1. La phrase « decreases the FPS to 10.14% and 7.67% » (§4.3.4) est ambiguë
(probablement 10,14 et 7,67 FPS).

Ce qui suit est déduit et non affirmé par les auteurs :
- la configuration (tricks) de la soumission au challenge ;
- l'éloignement du temps réel sur Jetson / FPGA et le TDP de la RTX 3090 Ti ;
- l'intérêt de CA-Trans pour un co-design matériel ;
- l'interprétation de la phrase sur les FPS de la Table 8.
