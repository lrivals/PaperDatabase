---
id: 2024-nguyen-fpga-soc-implementation-yolov4-flying
fiche: done
date: 2026-09-28
---

# FPGA-SoC implementation of YOLOv4 for flying-object detection

Dai-Duong Nguyen, Dang-Tuan Nguyen, Minh-Thuy Le, Quoc-Cuong Nguyen, 2024, Journal of Real-Time Image Processing 21(3), 63. https://doi.org/10.1007/s11554-024-01440-w
Type : article de journal

## Problème

Détecter des **objets volants** (drones à voilure tournante ou fixe, oiseaux, avions de
chasse, hélicoptères), souvent petits, en temps réel et à faible consommation sur FPGA
plutôt que sur GPU (§1). Le verrou annoncé est le coût en ressources flottantes et les
opérateurs YOLOv4 non supportés par le DPU Xilinx (§3.2).

## Méthode

- **Jeu de données** : fusion de 4 jeux publics (DUT Anti-UAV, deux jeux d'avions
  militaires, Flying Object) et de 11 095 images collectées sur Internet, pré-étiquetées par
  un YOLOv4 puis corrigées à la main. Total : 34 000 images, 5 classes, de 640×512 à
  8508×5939 ; test de 2000 images issues de vidéos séparées (§3, Table 1).
- **Sélection de modèle** sur GPU : YOLOv3, YOLOv4, leurs versions tiny et des versions
  tiny « **3L** » avec une troisième tête YOLO pour les petits objets (§3.2.4). Entrée
  **640×480** (4:3) pour ne pas déformer l'image (§3.3).
- **Adaptation au DPU** : Mish → LeakyReLU ; noyaux SPP 5/9/13 → **5/6/8** (max 8 sur le
  DPU) ; suppression du *group by channel* de YOLOv4-tiny (§3.2.1-3.2.2).
- **Pruning** de filtres par norme L1, ratio 0,6 retenu : −51 % de paramètres et de BFLOPS
  (64,2 M → 31,5 M ; 105,9 → 52,1 BFLOPS), mAP test@0.5 de 88,53 à 87,68 % sur GPU (Table 6).
- **Seuils** : conf = 0,15, NMS = 0,25, choisis sur le jeu de test (Tables 7-8). Les
  auteurs notent que l'évaluation passe alors en **mAP@0.25** (§3.5).
- **Toolflow** : Darknet → Keras → TensorFlow 1.15 frozen graph, **PTQ INT8 Vitis AI**
  (640 images de calibration), compilation DPU, application C++ multi-thread avec
  2 cœurs DPU (§4).

## Plateforme et implémentation

- **Puce** : Zynq UltraScale+ **XCZU7EV-2FFVC1156E** (kit ZCU104), 4× Cortex-A53, **2 cœurs
  DPU** (maximum permis par les ressources selon les auteurs, §4.3). Configuration DPU
  (B4096 ou autre), fréquence, LUT/DSP/BRAM : **n/r**.
- **Gamme de puissance : FPGA (W), carte de développement complète.** La puissance est
  mesurée **à la prise** (wattmètre TS-836, moyenne toutes les 3 s sur la vidéo), donc
  carte entière avec son alimentation → `power_scope = board`. Au repos : 16,1 W (§5.3).
  Côté GPU, la GTX 1650 est aussi mesurée à la prise (portable entier), la RTX 2080 Ti par
  logiciel (NVTOP) (§5.3).
- Post-traitement (NMS) sur les A53 : ~3,9 ms par image (Table 12).
- Code, jeu de données, bitstream : **non publiés** (rien dans le texte).

## Résultats

Vitesse mesurée sur une vidéo HD 1280×720 de 2747 images, batch 1 (§3.4, §5.2).

| Modèle (ZCU104, INT8) | mAP@0.25 test FP32 → FPGA | FPS 1 thread / 4 threads | E2E 1 thread (ms) | P 1 / 4 threads (W, prise) |
|---|---|---|---|---|
| YOLOv4 | 90,37 → 83,70 | 9,2 / 17,9 | 107,94 | 23,1 / 30,1 |
| YOLOv4-pruned | 89,02 → 82,41 | 15,0 / 29,0 | 66,53 | 21,2 / 27,9 |
| YOLOv4-tiny 3L | 78,50 → 72,24 | 52,1 / 125,0 | 19,18 | 19,4 / 26,4 |

Sources : Table 11 (mAP), Table 13 (FPS), Table 12 (latence), Table 15 (puissance). Le
passage au FPGA coûte **6 à 7 points de mAP** (val : 95,54 → 88,21 pour YOLOv4) ; la
conversion Darknet → TF seule ne coûte rien (Table 10), la perte vient donc de la PTQ INT8
et de la compilation (déduit des Tables 10-11).

**Baselines GPU** (mêmes modèles FP32, Darknet) : RTX 2080 Ti, 66,9 FPS et 255,4 W pour
YOLOv4 ; GTX 1650, 16,5 FPS et 93,7 W (Tables 5, 14). Les auteurs concluent à une
efficacité FPS/W 2-3× supérieure à la RTX 2080 Ti et 3-4× à la GTX 1650 (§5.3, Fig. 12) ;
pruning : FPS/W de 0,6 → 1,04 (§5.3).

→ reportés dans `benchmarks.csv` : 6 lignes (3 modèles × {1 thread/1 DPU, 4 threads/2 DPU}),
`power_scope = board`, confidence `high`.

## Limites et critique

- **mAP@0.25 sur un jeu propre avec seuils réglés sur le test** : les chiffres ne sont
  comparables à aucun autre papier, et le choix de conf/NMS sur le jeu de test (Tables 7-8)
  biaise l'évaluation à la hausse. Incohérence mineure : YOLOv4-tiny 3L à 78,95 % en
  Table 9 et 78,50 % en Table 11.
- **Puissance à la prise, repos compris** : 16,1 W au repos pour 26 à 30 W en charge. La
  part dynamique de l'inférence est donc ~10-14 W (déduit). Le kit ZCU104 n'est pas un
  système embarquable sur drone. La comparaison est aussi hétérogène : GPU de portable
  à la prise, RTX 2080 Ti par logiciel.
- **Baselines GPU inadaptées à l'embarqué** : FP32 Darknet sur GPU de bureau/portable, sans
  TensorRT INT8 ni Jetson. Le gain d'efficacité serait bien plus faible face à une Jetson
  Xavier/Orin en INT8 (déduit, non mesuré).
- **Ressources FPGA et configuration DPU non rapportées** : impossible de reproduire ou de
  comparer à d'autres implémentations DPU.
- **Latence avec 4 threads non mesurée** : le débit de 17,9 FPS vient du parallélisme
  inter-images (2 DPU) ; la latence par image reste ~108 ms pour YOLOv4 (Table 12).
- **Point de vue non défini** : images d'Internet et de jeux au sol (DUT Anti-UAV). Il
  s'agit de fait d'un détecteur **sol → air** ou générique, jamais testé à bord (déduit).
- Pas de mAP_small, bien que le papier vise les petits objets (définis en §3.5 comme
  16×16 à 42×42 px en 640×480) : l'effet de la quantification sur ces objets est jugé
  seulement visuellement (Fig. 10).

## Pertinence pour la thèse

- **Cas typique de l'axe `drone-fpga`** : YOLOv4 complet porté sur DPU Vitis AI, avec une
  analyse honnête de ce que coûte chaque étape (conversion, PTQ INT8). La perte de
  6-7 points de mAP en PTQ est une donnée utile pour l'hypothèse « effet de la
  quantification sur les petits objets ».
- Fournit la décomposition **E2E = DPU + CPU** (Table 12) : le post-traitement sur
  A53 est négligeable (~4 ms) sur ce cas, ce qui nuance le gap « NMS sur PS ».
- Montre la **tête supplémentaire (3L)** pour petits objets sur DPU : la question « tête P2
  sur FPGA » y est touchée de loin (3e tête sur un modèle tiny).
- Contre-drone : utile surtout comme contre-exemple de détecteur **non embarqué** ;
  il faudrait le transposer à un SoC embarquable (KV260, Ultra96) avec un jeu air → air.

## Gaps identifiés

- **Perte PTQ par taille d'objet non mesurée** : 6-7 points de mAP globaux, mais aucun
  mAP_small (confirme l'hypothèse de départ).
- **QAT non essayée** alors que la perte PTQ est notable (§4.2 : choix explicite de la PTQ).
- **Puissance embarquée non évaluée** : mesure à la prise d'un kit de développement ; pas
  de mesure sur SoC embarquable, pas d'impact sur l'autonomie.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). La section 3 n'est
pas détectée comme titre ; la liste des jeux publics et la configuration matérielle
d'entraînement sont partiellement perdues. Table 1 : la ligne « Helicopter » est
incomplète. La Table 4 (AP par classe) est mal découpée : noms de modèles tronqués,
illisibles par modèle.

Ce qui suit est déduit et non affirmé par les auteurs :
- l'origine de la perte de mAP (PTQ et compilation plutôt que conversion) ;
- la puissance dynamique (~10-14 W) ;
- l'écart probable face à une Jetson INT8 ;
- le caractère sol → air / générique du détecteur.
