---
id: arxiv-2211.11647-benchmarking-edge-computing-devices-grape
fiche: done
date: 2026-09-24
---

# Benchmarking Edge Computing Devices for Grape Bunches and Trunks Detection using Accelerated Object Detection Single Shot MultiBox Deep Learning Models

Sandro Costa Magalhães, Filipe Neves Santos, Pedro Machado, António Paulo Moreira, Jorge Dias, 2022, Engineering Applications of Artificial Intelligence 117, 105604 (2022). arXiv 2211.11647
Type : article de journal. La fiche est rédigée sur la version arXiv, qui peut différer de la version publiée.

## Problème

Un robot agricole en plein champ a peu d'énergie, et on ne sait pas quel type d'accélérateur
embarqué convient à la détection d'objets en temps quasi réel (§1). Les travaux cités
comparent surtout des Jetson entre eux, ou des modèles légers (YOLO, SSD MobileNet). Les
auteurs comparent GPU embarqués, TPU et FPGA (DPU) sur un **gros** détecteur, RetinaNet
ResNet-50. Cible applicative : environ 5 FPS suffisent à un robot à 0,5 m/s dans une vigne
(§1).

## Méthode

- Modèle : RetinaNet ResNet-50 (TensorFlow 2 / Keras), backbone pré-entraîné ImageNet,
  fine-tuning sur VineSet (§2.3). Hyperparamètres choisis par Keras Tuner (Hyperband),
  entraînement sur RTX 3090.
- Modification pour Vitis AI : une ReLU doit suivre directement une autre opération. Les
  auteurs dupliquent donc la convolution P6 du FPN pour que tout le cœur du réseau tienne
  sur le DPU, sans repli CPU (§2.3, Fig. 3).
- Chaînes de déploiement (§2.4) :
  - GPU : TF-TRT (FP32 / FP16 / INT8) ;
  - Coral : Edge TPU Compiler (INT8) ;
  - FPGA : Vitis AI 1.4 (INT8).
  La quantification est post-entraînement, avec un jeu de calibration tiré du train set.
- Mesure (§2.5) :
  - **seul le cœur du réseau est chronométré** : pré- et post-traitement (OpenCV, sur CPU)
    exclus ;
  - temps moyen par image, après 50 images de chauffe ;
  - précision, rappel, F1 et mAP à IoU 0,5, seuil de confiance 30 % (§4) ;
  - puissance à vide et en inférence, **à l'entrée de la carte**, au multimètre Fluke 175 :
    V puis I mesurés séparément, P = V·I (§2.5).

## Plateforme et implémentation

- GPU embarqués : Jetson TX2. Les Jetson Nano 2 GB et 4 GB ont été **exclues** : le
  modèle n'a pas pu être converti par TF-TRT, faute de mémoire (§3, §4). La TX2 non plus
  n'a pas pu produire d'INT8.
- TPU : Coral Dev Board.
- FPGA : AMD-Xilinx ZCU104 (2 cœurs DPU) et Kria KV260 (1 cœur DPU), avec l'image PetaLinux
  standard où toutes les ressources sont actives (§4).
- Référence : RTX 3090, présentée comme non comparable (§3).
- Ressources FPGA (LUT, DSP, BRAM) et fréquence du DPU : n/r.
- Code : publié sur https://gitlab.inesctec.pt/agrob/xilinx-acc2021 (§5). Tutoriel de
  déploiement Vitis AI en [14]. Bitstream : n/r (DPU standard AMD-Xilinx).

## Résultats

La plupart des résultats sont donnés **uniquement en figures** (Fig. 4 à 10, Fig. 12), dont
l'extraction ne récupère pas les valeurs. Le texte ne donne que ceci :

| Mesure | Valeur | Source |
|---|---|---|
| FPS des GPU embarqués | 3 à 5 FPS | Abstract |
| FPS des FPGA | 14 à 25 FPS | Abstract |
| ZCU104, 2 DPU | 25 FPS | §3 |
| FPGA à 1 DPU vs TX2 | 5,6× plus rapide que TX2 FP32, 3,4× plus rapide que TX2 FP16 et que le TPU | §3 |
| TX2 FP16 vs FP32 | ×1,6 | §3 |
| TPU | efficacité « similaire » à la TX2 | Abstract |
| Puissance TPU et GPU | « environ 5 W » ; en inférence, toutes les cartes consomment à peu près autant | Abstract, §3 (Fig. 12) |
| Précision | F1 d'environ 70 %, mAP d'environ 60 %, écarts entre cartes « non significatifs » | Abstract |
| Pire précision | TPU (la quantification réduit rappel et précision) | §3 |
| Meilleure précision embarquée | TX2 | §3 |
| RTX 3090 : TF-TRT FP32 vs TensorFlow 2 | ×10 | §3 (Fig. 5) |
| RTX 3090 : TF-TRT FP16 vs TensorFlow 2 | ×26 | §3 (Fig. 5) |

→ reportés dans `benchmarks.csv` : 1 ligne, ZCU104 2 DPU, 25 FPS (§3, Fig. 7,
`confidence: medium`). Les autres configurations n'ont pas de valeur exacte dans le texte :
elles ne sont pas reportées. Les déduire des rapports × l'abstract serait une estimation,
d'ailleurs incohérente : 14 FPS / 5,6 donnerait environ 2,5 FPS pour la TX2 FP32, sous la
fourchette « 3 à 5 FPS » de l'abstract.

## Limites et critique

- **Chiffres exacts absents du texte :** l'essentiel est en graphiques. Il faudrait lire les
  Fig. 6, 7 et 12 sur le PDF pour compléter `benchmarks.csv`, avec `confidence: low`
  (lecture de graphique).
- **Temps d'inférence du cœur seul**, hors pré- et post-traitement (les auteurs le disent,
  §2.5). Le NMS de RetinaNet n'est pas compté : le FPS de bout en bout sera plus bas, surtout
  sur les cartes à CPU faible (KV260, Coral).
- **Précisions différentes selon la plateforme :** INT8 sur FPGA et TPU, FP32 / FP16 sur la
  TX2. La comparaison de vitesse mélange donc l'effet du matériel et celui de la
  quantification.
- **Baseline Jetson faible :** seule la TX2 (2017) a tourné, pas de Xavier ni d'Orin, pas
  d'INT8. Le « FPGA 5,6× plus rapide » est obtenu contre une Jetson ancienne en FP32.
- **Puissance :** mesure `board` à l'entrée, mais avec V et I relevés séparément (pas de
  wattmètre intégrateur). La PetaLinux standard gonfle la puissance des FPGA (§4). Aucune
  valeur par carte dans le texte.
- **Jeu de données :** VineSet avec erreurs d'annotation suspectées (§4) ; test réduit à
  1125 images après retrait des images augmentées (§2.2). Seuil de confiance fixé à 30 %
  sans optimisation.

## Pertinence pour la thèse

- Rare comparaison, sur **le même modèle et le même jeu de données**, de FPGA (ZCU104, KV260),
  Edge TPU et Jetson, avec une **mAP** mesurée et une puissance à l'entrée de la carte.
- Montre le coût d'adaptation d'un modèle au DPU Vitis AI : modification d'architecture
  (§2.3), quantification post-entraînement obligatoire.
- Code publié : c'est une base de départ reproductible pour un protocole de mesure KV260 vs
  Jetson.
- Même constat que Feng et al. (2022-feng-benchmark-analysis-yolo-performance-edge) :
  la chaîne de compilation, et pas seulement le matériel, détermine ce qui tourne (Nano
  exclue, TX2 sans INT8, TPU dégradé).

## Gaps identifiés

- **Protocole de mesure :** étaye le gap existant. Même un benchmark multi-plateformes
  soigné exclut pré- et post-traitement, mélange FP16 et INT8, et publie ses chiffres en
  graphiques seulement.
- **Coût de bout en bout :** il manque une mesure avec NMS et pré-traitement sur l'embarqué.
  Déduit : sur KV260, ce coût CPU pourrait réduire l'avantage du DPU.
- **Faisabilité des gros détecteurs :** ils (ResNet-50) ne sont pas compilables sur
  les petites Jetson par manque de mémoire (§4). À recouper avec les gros modèles sur
  FPGA.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, version arXiv, extraction GROBID `ok`). Les
valeurs des figures sont absentes du texte extrait et n'ont pas été lues.

Ce qui suit est déduit et non affirmé par les auteurs :
- l'incohérence entre les rapports × et la fourchette de l'abstract ;
- l'effet probable du NMS sur le FPS de bout en bout ;
- la faiblesse de la TX2 comme baseline ;
- le rapprochement avec Feng et al.
