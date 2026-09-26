---
id: 2023-zhai-fpga-vehicle-detection-tracking-accelerator
fiche: done
date: 2026-09-24
---

# FPGA-Based Vehicle Detection and Tracking Accelerator

Jiaqi Zhai, Bin Li, Shunsen Lv, Qinglei Zhou, 2023, Sensors 23(4), 2208. https://doi.org/10.3390/s23042208
Type : article de journal (MDPI *Sensors*)

## Problème

Détection et suivi multi-véhicules pour le comptage de trafic, sur un FPGA embarqué, à
faible puissance et haut débit (§1). Selon les auteurs, les travaux FPGA sur les « gros »
YOLO restent théoriques et ne sont pas déployés dans un scénario applicatif réel (§1,
§2.4).

## Méthode

- **Modèles :** YOLOv3 et YOLOv3-tiny, entrée 416×416, entraînés sur UA-DETRAC avec les 4
  catégories fusionnées en une seule, « car » (§4.2).
- **Compression :**
  - pruning structuré par canaux : régularisation L1 des facteurs d'échelle de la BN, seuil
    dynamique trouvé par recherche dichotomique à partir de 50 %, puis fine-tuning par KD
    (§3.1.1, Fig. 2) ;
  - quantification en virgule fixe 16 bits dynamique, avec une position de virgule Q
    optimisée par couche pour les poids, biais, entrées-sorties et résultats
    intermédiaires (§3.1.2).
- **Suivi :** Deepsort, avec un réseau d'apparence réentraîné sur un jeu RE-ID construit
  depuis UA-DETRAC (1053 identités, 606 007 images, entrée 128×128) (§3.2).
- **Accélérateur, écrit en HLS (Vivado HLS 2021.2) :**
  - deux moteurs de convolution : Im2col + GEMM pour les 1×1, Winograd pour les 3×3
    (§3.5) ;
  - fusion convolution + max-pooling, pipeline à 4 étages (§3.4.4) ;
  - BN fusionnée dans les poids (§3.6) ;
  - réorganisation des poids en mémoire, double buffer ping-pong ;
  - transfert multi-canal DMA avec Tx = 32, Ty = 4, n = 4, m = 2 (§3.4.3).
- **Répartition hôte / FPGA (§3.3) :** l'hôte (ARM) fait le pré-traitement, la
  quantification des entrées, le **NMS** et Deepsort ; le FPGA calcule convolution,
  pooling et upsampling.
- **Configurabilité :** YOLOv3 et YOLOv3-tiny sont chargés tous deux en mémoire. Le système
  bascule sur tiny au-delà de 15 véhicules sur 10 images consécutives, et sur YOLOv3 à la
  main par nuit ou pluie (§3.4.1).

## Plateforme et implémentation

- **Puce :** Zynq-7000 XC7Z035-FFG676-2 (§4.1).
- **Fréquence :** 210 MHz en FP32 et 230 MHz en INT16 avec un module (Table 8) ; 200 et
  209 MHz avec deux modules (Table 9).
- **Ressources pour un module (Table 8)** :

| Précision | LUT | FF | DSP | BRAM |
|---|---|---|---|---|
| FP32 | 38 336 (22,3 %) | 62 988 (18,3 %) | 301 (33,8 %) | 98,5 (19,7 %) |
| INT16 | 38 228 (22,2 %) | 42 853 (12,5 %) | 144 (16,2 %) | 132,5 (26,5 %) |

  Le tableau ne donne qu'une colonne de ressources par précision : l'accélérateur est
  partagé par les deux modèles (lecture de la Table 8, cohérente avec la Table 9).
- **Ressources pour deux modules (Table 9) :**
  - FP32 : 89 014 LUT, 602 DSP, 230,5 BRAM ;
  - INT16 : 91 108 LUT, 294 DSP, 263 BRAM.
- **Puissance :** « Full Power » et « Dynamic Power » rapportées, **sans méthode de
  mesure** (ni wattmètre, ni outil Vivado cité) → `power_scope = unspecified`.
- **Code et bitstream :** non publiés (aucun lien dans le texte).

## Résultats

Un module, modèles élagués (Table 8) :

| Modèle | Précision | AP@0.5 | FPS | GOP/s | Full / dyn. (W) |
|---|---|---|---|---|---|
| YOLOv3 | FP32 | 71,1 | 2,12 | 41,39 | 13,29 / 1,80 |
| YOLOv3-tiny | FP32 | 59,9 | 59,14 | 43,47 | 12,92 / 1,48 |
| YOLOv3 | INT16 | 71,1 | 3,23 | 63,51 | 12,73 / 1,52 |
| YOLOv3-tiny | INT16 | 59,9 | 91,65 | 67,91 | 12,51 / 1,31 |

Deux modules (Table 9) :
- YOLOv3-tiny INT16 : **168,72 FPS**, 124,01 GOP/s, 15,18 W. C'est le chiffre de
  l'abstract, suffisant pour 6 flux à 25 FPS.
- YOLOv3 INT16 : 5,95 FPS.

Compression (§4.2) :
- YOLOv3 : taille −85 %, AP@0.5 +0,04, calcul de convolution −70,4 % ;
- YOLOv3-tiny : taille −98,2 %, AP −0,026, calcul −86,5 % (0,735 GOP, contre environ 5,44 GOP
  pour un YOLOv3-tiny standard, déduit du facteur 7,4 cité au §4.4) ;
- le Tableau 4 (tailles, paramètres) était perdu à l'extraction. *Mise à jour du 26/09/2026* :
  corps reconstruit par Docling (à vérifier). Ses valeurs recoupent celles ci-dessus :
  AP@0.5 0,671 → 0,711 (YOLOv3) et 0,625 → 0,599 (tiny), 0,735 BFLOPs. La légende que
  GROBID lui associe (« Meanings of the variables ») semble être celle d'un autre tableau :
  à contrôler sur le PDF.

Comparaison entre plateformes (Table 7, YOLOv3-tiny élagué) :

| Plateforme | FPS | W | GOPS/W |
|---|---|---|---|
| Ryzen 7 5800H | 10,01 | 45 | 0,16 |
| RTX 2060 | 112,87 | 160 | 0,52 |
| ZCU102 + Vitis AI, yolov3-adas-pruned-0.9 (5,5 GOP) | 84,1 | n/r | 3,71 |
| Jetson Nano, réf. [45] (1,81 GOP) | 17 | 10 | 3,08 |
| Ce travail (Zynq-7000) | 91,65 | 12,51 | 5,43 |

Suivi (Table 6) : RE-ID Deepsort améliore la MOTA sur les trois séquences, de 66,8 à
67,5 %, de 65,2 à 69,6 % et de 39,2 à 40,5 %. Taux de comptage en pic de trafic (§4.3) :
96,15 % (YOLOv3) et 92,3 % (tiny) de jour, 81,8 % et 75,8 % par temps de pluie.

→ reportés dans `benchmarks.csv` : 8 lignes
- 4 lignes à un module (Table 8), avec l'AP@0.5 ;
- 4 lignes à deux modules (Table 9), sans AP (non donnée dans cette table).

## Limites et critique

- **Précision non vérifiée après quantification (déduit) :** l'AP@0.5 est **identique** en
  FP32 et en INT16 (0,711 et 0,599, Table 8). Soit elle a été mesurée hors FPGA (en
  flottant) puis recopiée, soit la quantification n'a exactement aucun effet. Le texte ne
  dit pas où l'AP est mesurée. Les taux de comptage du §4.3 ne précisent pas la plateforme
  non plus.
- **FPS partiels :** le NMS et Deepsort tournent sur l'ARM (§3.3). Rien ne dit s'ils sont
  inclus dans les FPS : le débit de bout en bout du détecteur-suiveur est inconnu.
- **Baselines biaisées (Table 7) :**
  - CPU et GPU exécutent le même YOLOv3-tiny élagué, ce qui est équitable ;
  - mais la ligne Jetson Nano est reprise d'un autre papier [45], avec un modèle non élagué
    (1,81 GOP contre 0,735) ;
  - la ligne ZCU102 utilise un autre modèle (yolov3-adas, 5,5 GOP).
  Le gain de 5× en FPS sur la Jetson vient donc surtout du pruning, pas du FPGA. De plus,
  la RTX 2060 est **plus rapide** (112,87 contre 91,65 FPS), ce que le texte présente
  comme un « débit similaire ».
- **Puissance :** « Full Power » d'environ 12,5 W pour 1,3 W de puissance dynamique. Le
  fixe domine, ce qui suggère une mesure de carte, mais la méthode n'est pas dite. La
  comparaison en « dynamic GOPS/W » avec [14] et [37] (Table 8) exclut le statique et
  avantage ce travail.
- **mAP non comparables :** UA-DETRAC à une seule classe contre COCO ou VOC pour les
  références de la Table 8. Les auteurs le reconnaissent en creux (§4.4).
- **Pas de code ni de bitstream.**

## Pertinence pour la thèse

- **Référence YOLO sur Zynq-7000 chiffrée :** design HLS maison (pas FINN ni Vitis AI),
  ressources complètes, FPS, GOP/s et puissance. Premier point de comparaison concret pour
  YOLOv3-tiny sur FPGA d'entrée de gamme dans `benchmarks.csv`.
- **Levier du pruning :** il montre que le gain dominant vient de la compression, qui
  divise le calcul par 7,4, plus que de l'architecture matérielle.
- **Idée de système :** la bascule dynamique entre deux modèles selon le contexte
  (trafic, météo) est un exemple de système adaptatif, relié aux questions d'apprentissage
  continu.

## Gaps identifiés

- **Précision après compilation (nouveau) :** l'AP n'est pas remesurée sur la cible après
  quantification (FP32 = INT16 à trois décimales). Même motif que Feng et al. (0 % de
  confiance après OpenVINO) et que 2211.11647 (TPU dégradé).
- **Protocole de mesure :** étaye le gap existant. Puissance sans méthode, FPS sans
  post-traitement, baselines reprises de papiers tiers avec d'autres modèles.
- **Détection + suivi sur FPGA de bout en bout :** Deepsort reste sur le CPU. Un
  détecteur-suiveur entièrement sur FPGA, avec latence de bout en bout mesurée, n'est pas
  couvert dans le corpus (déduit).

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). Le Tableau 4
(résultats de compression), perdu à l'extraction, a été reconstruit par Docling le
26/09/2026 (voir Résultats, à vérifier). Les Tableaux 8 et 9 ont été relus
colonne par colonne : l'ordre FP32 v3 / FP32 tiny / INT16 v3 / INT16 tiny est confirmé par
la Table 7 (91,65 FPS à 12,51 W).

Ce qui suit est déduit et non affirmé par les auteurs :
- l'hypothèse d'une AP non remesurée après quantification ;
- l'attribution du gain sur la Jetson au pruning ;
- le fait que la « Full Power » soit une mesure de carte ;
- les environ 5,44 GOP du YOLOv3-tiny standard (0,735 × 7,4) ;
- le partage des ressources entre les deux modèles.
