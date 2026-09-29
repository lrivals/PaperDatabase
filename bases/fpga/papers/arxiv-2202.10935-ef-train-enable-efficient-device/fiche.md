---
id: arxiv-2202.10935-ef-train-enable-efficient-device
fiche: done
date: 2026-09-29
---

# EF-Train: Enable Efficient On-device CNN Training on FPGA Through Data Reshaping for Online Adaptation or Personalization

Yue Tang, Xinyi Zhang, Peipei Zhou, Jingtong Hu, 2022, arXiv preprint. https://arxiv.org/abs/2202.10935
Type : preprint non relu par les pairs

## Problème

Adapter ou personnaliser un modèle directement sur un FPGA embarqué, sans renvoyer les données
au cloud, exige un accélérateur d'**entraînement** (forward FP, backward BP, weight update WU)
et non seulement d'inférence (§1). Deux verrous selon les auteurs : la complexité de calcul
(≈3× l'inférence, opérations plus variées) et le goulot de communication, car FP, BP et WU ont
des motifs d'accès mémoire différents, ce qui casse la continuité des adresses DRAM et fait
chuter le débit du DMA de ~8 Go/s à ~1 Go/s (§2.2, citant [26]). Les accélérateurs
d'entraînement existants ciblent des FPGA cloud ou quantifient sans preuve de précision sur
grands jeux de données (§2.2).

## Méthode

- **Noyau de convolution unifié à parallélisme par canaux** (Tm × Tn PE, arbre d'additionneurs)
  qui exécute FP, BP et WU avec les mêmes DSP ; noyaux séparés pour pooling et BN ; ReLU fusionné
  à l'écriture DRAM ; perte cross-entropy calculée sur le cœur ARM ; SGD (§3, Fig. 4).
  Précision **FP32 complète** (pas de quantification), 5 DSP par MAC (§5.2).
- **Data reshaping** (§4) : réorganisation des layouts DRAM des features et poids (continuité
  intra-tuile), avec Tm = Tn et Tc = C, réordonnancement des boucles (continuité inter-tuiles), et
  réutilisation des poids entre images d'un mini-batch (§4.3).
- **Modèle analytique de latence et de ressources** (Éq. 15-32) et outil de scheduling
  (Algorithme 1) fixant Tm, Tn, Tr, Tc, M_on ; bornes empiriques 80 % des DSP et 75 % des BRAM
  (§5.3).
- Flot : Vivado HLS (C vers IP), Vivado 2019.1, Xilinx SDK (§6). Le CPU place données et adresses
  DMA (calculées hors ligne) en DRAM (§3.1).

## Plateforme et implémentation

- **PYNQ-Z1** (Zynq-7000) et **ZCU102** (Zynq UltraScale+), horloge 100 MHz ; DMA 32 bits
  (PYNQ-Z1) ou 128 bits (ZCU102) (§6, §6.3). Références de puce exactes (XC7Z020, XCZU9EG) : n/r
  dans le texte.
- Ressources (Table 7, Table 8) : '1X' CNN 212 DSP / 123 BRAM (PYNQ-Z1), 1315 DSP / 324 BRAM
  (ZCU102) ; AlexNet 1513 DSP / 857 BRAM ; Vgg-16 1508 DSP / 787 BRAM ; LUT : n/r.
- **Puissance** : « puissance totale sur puce » lue dans le rapport de puissance Vivado après
  implémentation (§6.3) : c'est une estimation d'outil, pas une mesure → `estimated`.
- Code / bitstream : non publiés (aucun lien dans le texte).

## Résultats

- Effet du data reshaping sur les couches Conv d'AlexNet, ZCU102, batch 4 (Tables 3-5) :
  baseline BCHW 1 562 001 846 cycles (dont 1 494 958 747 de réallocation) ; baseline BHWC
  643 393 426 cycles ; après reshaping 72 534 495 cycles, puis 70 033 465 avec réutilisation des
  poids. Le gain vient de la suppression de la réallocation, la baseline ne gagnant rien en calcul
  pur (§6.1).
- Modèle de performance : écart total 1,05 % avec la mesure sur carte pour AlexNet (Table 6).
- '1X' CNN CIFAR-10, batch 128 (Table 7) : PYNQ-Z1 4,08 GFLOPS, 14,32 ms/image, 1,85 W,
  2,21 GFLOPS/W ; ZCU102 28,15 GFLOPS, 2,08 ms/image, 6,89 W, 4,09 GFLOPS/W. Baseline [22]
  (Stratix 10 GX, fixed 16 bits) : 163 GOPS, 20,6 W, 7,90 GOPS/W. Efficacité « nominale »
  (GOPS × précision) 130,88 contre 126,4 (×1,04).
- Précision après 50 époques sur '1X' : 64,82 % sur FPGA contre 65,22 % sur GPU V100 (§6.3).
- Grands réseaux ImageNet sur ZCU102 (Table 8, reconstruit par Docling : à vérifier) : AlexNet
  34,52 GFLOPS, 4,46 GFLOPS/W (batch 128) ; Vgg-16 46,99 GFLOPS, 6,09 GFLOPS/W (batch 16) ;
  Vgg-16 + BN 40,08 GFLOPS, 4,88 GFLOPS/W (batch 8). Les valeurs 46,99 / 6,09 sont confirmées
  par l'Abstract. AlexNet à batch 2 : plus de 32 GFLOPS (§6.3, Fig. 21).
- Comparaison à d'autres accélérateurs (Table 9, Table 10, Table 11) : LeNet-10 15,47 GFLOPS et
  2,17 GFLOPS/W contre 86,12 GFLOPS et 6,05 GFLOPS/W pour Chow et al. sur ZU19EG (Table 10).
  Les auteurs concèdent l'infériorité de DarkFPGA (8 bits, XCVU9P) en efficacité nominale
  (839,68 contre 194,88, Table 9).

→ reportés dans `benchmarks.csv` (via `bench_rows.csv`) : 6 lignes — '1X' CNN sur PYNQ-Z1 et
ZCU102 (Table 7), AlexNet, Vgg-16, Vgg-16 + BN (Table 8), LeNet-10 (Table 10).

## Limites et critique

- **Pas de matériel de classe MCU/edge réaliste** pour la puissance : puissance estimée par
  l'outil (`estimated`), non mesurée ; les GFLOPS/W ne sont pas comparables à des mesures carte
  d'autres papiers.
- **Comparaisons biaisées reconnues par les auteurs** : baselines sur Stratix 10 / XCVU9P
  (cloud), précisions différentes (fixed 16 / 8 bits contre FP32) ; le concept de
  « nominal throughput » (GOPS × largeur de bits) est une normalisation propre au papier, non
  standard (§6.3). Sur LeNet-10, EF-Train est nettement moins performant que Chow et al. (Table 10).
- **Aucun baseline GPU / Jetson** en débit ni en énergie ; le V100 ne sert qu'à valider la
  convergence (Fig. 20).
- Fréquence de 100 MHz seulement ; DRAM de la ZCU102 limite le batch (16 pour Vgg-16, 8 avec BN).
- Le débit atteint (≤ 47 GFLOPS) reste faible en absolu pour un entraînement ; la précision
  d'entraînement n'est vérifiée que sur '1X' / CIFAR-10 (64,82 %, niveau modeste) : aucune
  précision rapportée pour AlexNet / Vgg-16 sur ImageNet.
- Pas d'apprentissage continu proprement dit (pas d'oubli catastrophique, pas de
  class-incremental) : l'article fournit le substrat matériel, pas la stratégie d'adaptation.
- Aucun code publié : reproductibilité limitée. Table 8 et Table 2 reconstruites par Docling :
  chiffres recoupés avec le texte (§6.3) pour AlexNet et Vgg-16.

## Pertinence pour la thèse

Pertinence indirecte. Le papier relève de l'apprentissage embarqué (axe `continual-learning`)
et non de la sûreté : il montre qu'un fine-tuning en FP32 est faisable sur SoC FPGA
(ZCU102, ~7 W), utile si le YOLO de la thèse devait s'adapter à un site industriel donné
(éclairage, EPI, caméras). Pour une thèse « certifiable », l'entraînement en ligne est plutôt un
**risque** (le modèle certifié change) ; l'article oriente vers un mode « inférence figée /
mise à jour hors ligne » avec bascule de configuration, décrit en §1 (déduit pour l'implication de
certification). Détecteurs de type YOLO, quantification et fiabilité : non traités.

## Gaps identifiés

- Entraînement / adaptation embarqué **d'un détecteur** (YOLO) sur FPGA : ici uniquement
  classification (CIFAR-10, ImageNet en débit seul).
- Lien entre apprentissage sur cible et **certification** (versionnage, non-régression après
  mise à jour) : absent.
- Mesure de puissance réelle (`board`) de l'entraînement : absente, seulement estimation Vivado.
- Entraînement quantifié (INT8) avec preuve de précision sur grand jeu de données : cité comme lacune
  des travaux antérieurs (§2.2), non comblé.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). Table 8 et Table 2
reconstruits par Docling, valeurs recoupées avec le texte ; les figures (Fig. 18-21) et le
pseudo-code (Fig. 5, 15) sont absents ou fragmentaires ; les corps des Tables 3-6, 9-11 sont
lisibles. Les références de puce (XC7Z020, XCZU9EG), le nombre de LUT et la présence de code
sont non affirmés.
Ce qui suit est déduit et non affirmé par les auteurs : la portée `estimated` de la puissance
(déduite de « Vivado power report », §6.3) ; l'implication pour la certification ; l'absence de
baseline GPU en énergie.
