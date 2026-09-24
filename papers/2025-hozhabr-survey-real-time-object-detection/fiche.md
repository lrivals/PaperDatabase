---
id: 2025-hozhabr-survey-real-time-object-detection
fiche: done
date: 2026-09-24
---

# A Survey on Real-Time Object Detection on FPGAs

Seyed Hani Hozhabr, Roberto Giorgi, 2025, IEEE Access 13, 38195-38238. https://doi.org/10.1109/ACCESS.2025.3544515
Type : article de journal (survey)

## Problème

Selon les auteurs, aucune revue n'était dédiée à la détection d'objets **temps réel** sur
FPGA ; la plus proche, Zeng et al. [14], ne traite pas l'aspect temps réel (§I-C, §I-D).
Ils distinguent temps réel **dur** et **mou**, et contestent l'usage courant de « temps
réel » au sens de « au moins 30 FPS » (§II-B, §II-C2).

## Méthode

Survey, sans expérience propre. Il couvre :
- les détecteurs (non-DNN, deux étages, un étage, transformers) et leur aptitude au FPGA
  (§II-A, Table 2, Fig. 3) ;
- les métriques, avec une métrique proposée : le **pixel throughput** = FPS × pixels par
  image, en MPPS, pour comparer des travaux à résolutions différentes (§II-C2, Éq. 2) ;
- les architectures : moteur unique ou streaming (§IV-A, Table 7) ;
- les techniques côté modèle (pruning, quantification, KD, HW-NAS) et côté implémentation
  (réutilisation de données, Winograd, FFT, réseaux systoliques, transformations de
  boucles, roofline, pipeline) (§IV-B, Table 8, Fig. 12) ;
- des études de cas (§V-A), un comparatif trié par pixel throughput (§V-B, Tables 9-10,
  Fig. 18-19), des défis et des perspectives (§VI).

## Plateforme et implémentation

Pas d'implémentation propre. Les plateformes recensées sont uniquement AMD-Xilinx et
Intel-Altera (§V-B, Table 10). La Table 6 (cartes FPGA et ressources) est perdue à
l'extraction.

## Résultats

Études de cas citées (§V-A), chiffres repris des travaux originaux :

| Travail | Cible | Modèle, précision | FPS | Autres |
|---|---|---|---|---|
| Fan et al. [47] | ZC706 | SSD, élagué, 8 bits partiel | 64,8 | 15,43 ms ; 9,9 W |
| Nguyen et al. [15] | VC707 | YOLOv2, W1 / A3-6 | 66 | 51,68 % mAP ; 8,7 W ; streaming |
| Hao et al. [183] | PYNQ-Z1 | co-search (DAC-SDC) | 29,7 | efficacité 3,1 à 3,8 fois celle d'une Jetson TX2 à IoU égal |
| Wang et al. [73] | Arria-10 | YOLOv2, élagué, INT8 | 61,9 | 81,92 GOPS/W |
| Chang et al. [82] | ZCU102 | YOLOv3, précision mixte | 22 | 49,7 % mAP |
| Cai et al. [68] | XC7Z045 | MobileNetV3-SSDLite, Winograd | 33,14 | |
| Huang et al. [184] | Ultra96 | convolutions déformables | 32,2 | 5,6 W |
| Liew et al. [215] | Zynq US+ | YOLOv4, INT8 + KD | 33,34 | −8 % puis +2,5 % de précision |
| Jain et al. [77] | XC7Z035 | tiny-YOLOv2, W8 / A16, QAT | 23 | 57,1 % |
| Suh et al. [69] | ZU3EG | SSD, UniPOT 8 bits | n/r | 88,42 % mAP (jeu drone propre) ; 79 GOPS/W |
| Anupreetham et al. [67] | Stratix 10 | SSD + **NMS pipeliné** | n/r | **2,13 ms de bout en bout** ; 22,8 % mAP COCO |
| D. Zhang et al. [86] | KC705 (XC7K325T) | YOLOv3-tiny 8 bits, **tout sur FPGA, post-traitement compris** | 65 | 401 GOPS ; 12 W système |

Le comparatif principal (Tables 9 et 10, Fig. 18-19) n'est **pas dans le texte extrait**.

→ reportés dans `benchmarks.csv` : aucune ligne. C'est un survey : les travaux cités sont
à ficher à la source, et ses tableaux comparatifs sont perdus à l'extraction.

## Limites et critique

- **Le pixel throughput normalise la résolution, pas le reste.** Précision, mAP (VOC,
  COCO ou jeu propre), portée de la puissance et batch restent non harmonisés. L'étude de
  cas Suh et al. (88,42 % de mAP sur un jeu drone privé) côtoie Anupreetham et al. (22,8 %
  sur COCO) sans mise en garde explicite dans le texte extrait.
- **Puissance :** les W cités (9,9 ; 8,7 ; 5,6 ; 12 « système ») sont repris sans portée ;
  un seul est explicitement « entire system » (D. Zhang [86]).
- **Comparaison avec les autres plateformes qualitative seulement :** FPGA contre ASIC, GPU
  et CPU dans la Table 5. Les gains face au GPU sont ceux annoncés par les auteurs cités
  (par exemple Nguyen [15] contre une Titan X en FP32, ou Fan [47] contre une Titan X
  Pascal), donc face à des baselines non optimisées (déduit).
- **Plaidoyer pro-FPGA** : « FPGAs have emerged as the optimal hardware platform » (§IV-B),
  sans comparaison mesurée avec les Jetson récentes ni avec les MCU à NPU.
- **Pas de toolflow dataflow quantifié** (FINN, hls4ml) dans les études de cas retenues.
  Les outils sont surtout Vitis AI / DPU et du HLS maison (Annexe B).

## Pertinence pour la thèse

- **La revue la plus directement dans l'axe `yolo-fpga`** du corpus, avec une taxonomie
  exploitable (moteur unique contre streaming ; techniques côté modèle et côté
  implémentation).
- **Deux références à ajouter en priorité** pour le gap « post-traitement » :
  Anupreetham et al. [67] et D. Zhang et al. [86].
- **La distinction temps réel dur / mou** et la critique du critère des 30 FPS (§II-C2)
  sont réutilisables dans la problématique : latence et gigue, pas seulement débit.
- Le **pixel throughput** est une normalisation simple à reprendre dans `benchmarks.csv`
  (colonne dérivée possible : FPS × résolution), en gardant ses limites en tête.

## Gaps identifiés

- **FPGA absents des surveys « embarqué » :** **nuance.** Des surveys dédiés aux FPGA
  existent (celui-ci, arxiv-2509.04153, arxiv-1806.01683), mais ils ne comparent pas
  quantitativement FPGA, Jetson et MCU. Le gap se reformule : les surveys sont soit
  « embarqué » sans FPGA, soit « FPGA » sans comparaison chiffrée entre plateformes.
- **Post-traitement sur le PS :** des contre-exemples existent, avec un NMS pipeliné sur
  FPGA [67] et un système entièrement sur FPGA [86]. Le gap n'est donc pas une absence
  totale dans la littérature, mais une absence de ces solutions sur SoC embarqué avec
  mesure de latence de bout en bout (à vérifier en lisant [67] et [86]).
- **Transformers de détection sur FPGA :** aucune implémentation temps réel recensée par
  les auteurs (§II-A2c). Même constat que 2025-el-zeinaty côté MCU.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). Les Tables 1 à 10 sont
absentes ou vides dans l'extraction, sauf les légendes. Le comparatif chiffré (Tables 9-10)
n'a donc pas été lu. La section I n'a pas été détectée comme titre.

Ce qui suit est déduit et non affirmé par les auteurs :
- le caractère non optimisé des baselines GPU citées ;
- la reformulation du gap « surveys » ;
- l'intérêt de [67] et [86] pour le gap « post-traitement ».
