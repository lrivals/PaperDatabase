---
id: arxiv-1809.04570-finn-r-end-end-deep
fiche: done
date: 2026-09-24
---

# FINN-R: An End-to-End Deep-Learning Framework for Fast Exploration of Quantized Neural Networks

Michaela Blott, Thomas B. Preußer, Nicholas J. Fraser, Giulio Gambardella, Kenneth O'Brien, Yaman Umuroglu, Miriam Leeser, Kees Vissers, 2018, ACM Transactions on Reconfigurable Technology and Systems 11(3). DOI 10.1145/3242897 — texte lu : version arXiv <https://arxiv.org/abs/1809.04570>
Type : article de journal (ACM TRETS, relu par les pairs ; la version lue est le preprint arXiv)

## Problème

Étant donné un réseau et des contraintes (plateforme, ressources, débit), quelle est la
meilleure implémentation matérielle possible ? L'espace de conception d'un QNN (réseau
quantifié à précision réduite) est vaste : précisions, architectures, plateformes. Évaluer
l'impact sur la précision demande un entraînement, et évaluer l'impact matériel une
implémentation complète (§1). FINN, dans sa première version (arxiv-1612.07119), ne
gérait que des BNN entièrement binarisés et une seule architecture : FINN-R l'étend.

## Méthode

- **Microbenchmarks et modèle de coût d'opération** (§3.1, Fig. 5) :
  - le coût en LUT d'un produit scalaire est proportionnel à C = N · W · A, en RTL comme
    en HLS ;
  - le HLS coûte 45 % de LUT de plus que le VHDL ;
  - des poids bipolaires {-1, 1} coûtent +35 % de LUT par rapport à des entiers 1 bit
    (sauf en activations 1 bit), puis +20 % par pas vers le ternaire et le 2 bits.
- **Modèle de coût par couche** (§3.2, éq. 1-5) :
  - trois degrés de parallélisme : P (PE, canaux de sortie), Q (voies SIMD, canaux
    d'entrée) et M (pixels de sortie en parallèle) ;
  - LUT_MVU = c0 + c1 · M · P · Q · W · A, prédiction à ±30 % de la synthèse (Fig. 9) ;
  - coût fixe d'une SWU : 426 LUT en DF, contre 1 050 LUT + 15 DSP en MO ;
  - le coût des seuils croît exponentiellement avec la précision des activations, ce qui
    rend l'approche impraticable bien au-dessus de 4 bits.
- **Deux architectures d'accélérateur** (§3.3, Fig. 10) :
  - **Dataflow (DF)** : un moteur par couche, débits équilibrés ; c'est le principe de
    FINN.
  - **Multilayer Offload (MO)** : une partie du pipeline est réutilisée en boucle avec les
    feature maps en mémoire externe, pour les réseaux trop gros pour le DF.
- **Coût des « shells » (infrastructure de plateforme)** (§3.4) :
  - PYNQ / Ultra96 : 8 BRAM18 et 2,6 kLUT ;
  - AWS F1 : 1 090 BRAM18 et 297 kLUT (PCIe, DMA, contrôleurs DDR).
- **Outil structuré comme un compilateur** (§4, Fig. 4, inspiré de LLVM) :
  - frontends BinaryNet, Darknet et Tensorpack ;
  - représentation intermédiaire (IR) qui connaît la quantification de chaque nœud ;
  - passes :
    - quantification directe 8 bits des couches d'entrée et de sortie ;
    - *streamlining* : les facteurs d'échelle sont absorbés dans des seuils multi-niveaux,
      et le maxpool est déplacé après la quantification ;
    - analyse de ressources ;
    - génération DF ou ordonnancement MO ;
  - backends PYNQ-Z1, Ultra96 et AWS F1 (§4.1-4.3).
- **Algorithme d'équilibrage DF** (§4.4, Alg. 1) : partir du parallélisme minimal, élargir
  la couche goulot tant que les ressources le permettent ; sinon, repli sur MO.
- **Limites annoncées** : seules les contraintes de ressources et de débit sont gérées. La
  latence, l'estimation de puissance et l'exploration automatique de l'espace de
  conception sont reportées à plus tard (§4).

## Plateforme et implémentation

- Plateformes (§5.1, Table 3) :
  - **AWS F1** : XCVU9P, 16 nm, 1 180 kLUT, 4 320 BRAM ;
  - **Ultra96** : Zynq UltraScale+ XCZU3EG, 16 nm, 71 kLUT, 432 BRAM ;
  - **PYNQ-Z1** : Zynq-7000 XC7Z020, 28 nm, 53,2 kLUT, 280 BRAM.
- Réseaux (§5.1) :
  - **MLP-4** : identique à celui de FINN ;
  - **CNV-6** : classifieur CIFAR-10 / GTSRB / SVHN. Le dataset des mesures n'est pas
    précisé dans le texte extrait.
  - **Tincy YOLO** : Tiny YOLO modifié. Première et dernière couches en poids 8 bits,
    W1A3 ailleurs, leaky-ReLU remplacé par ReLU, largeurs et strides modifiés. Cela donne
    36 % d'opérations en moins, pour un mAP qui passe de 57,1 % à 50,1 %. Dataset : PASCAL
    VOC (§6).
  - **DoReFa-Net/PF** : AlexNet W1A2, première et dernière couches en 8 bits, 3 premières
    couches élaguées de 30 %. Cela donne 56 % d'opérations en moins et +0,2 point de
    top-1 ; top-5 de 74,0 %, contre 73,1 % pour DoReFa W1A2 et 77,4 % en flottant.
- Puissance : mesurée « au niveau carte » sur les plateformes embarquées seulement. Sur
  AWS F1, aucune mesure disponible (§5.3). Méthode de mesure (instrument, durée) : n/r.
- Code : les topologies et une partie des implémentations sont sur GitHub (réf. [32],
  §5.1 et §6). L'open-sourcing du framework est annoncé « en cours » (§6). URL exacte : n/r
  dans le texte extrait.

## Résultats

Table 5, performances mesurées (entre parenthèses : justesse de la prédiction FINN-R) :

| Réseau | Plateforme (archi) | MHz | BRAM18 | LUT | GOp/s | W (carte) | GOp/s/W | Précision |
|---|---|---|---|---|---|---|---|---|
| MLP-4 | AWS F1 (DF) | 232,9 | 1 652 | 337 753 | 50 776 (79 %) | n/r | n/r | W1A1 |
| MLP-4 | Ultra96 (DF) | 300 | 417 | 38 205 | 5 110 (75 %) | 11,8 | 433 | W1A1 |
| MLP-4 | PYNQ-Z1 (DF) | 100 | 220 | 25 358 | 974 (99 %) | 2,5 | 390 | W1A1 |
| CNV-6 | AWS F1 (DF) | 237 | 1 888 | 332 637 | 12 109 (98 %) | n/r | n/r | W1A1 |
| CNV-6 | Ultra96 (DF) | 300 | 283 | 41 733 | 2 318 (99 %) | 10,7 | 217 | W1A1 |
| CNV-6 | PYNQ-Z1 (DF) | 100 | 242 | 25 770 | 341 (99 %) | 2,25 | 152 | W1A1 |
| Tincy YOLO | AWS F1 (DF) | 249,8 | 2 638 | 242 457 | 5 271 (93 %) | n/r | n/r | W1A3 |
| Tincy YOLO | Ultra96 (MO) | 220 | 316 | 40 808 | 288 (68 %) | 9,7 | 30 | W1A3 |
| Tincy YOLO | PYNQ-Z1 (MO) | 100 | 280 | 46 507 | 133 (66 %) | 2,5 | 53 | W1A3 |
| DoReFa-Net/PF | AWS F1 (DF) | 155,8 | 1 332 | 476 970 | 11 431 (92 %) | n/r | n/r | W1A2 |
| DoReFa-Net/PF | Ultra96 (MO) | 220 | 432 | 36 249 | 400 (70 %) | 10,2 | 39 | W1A2 |
| DoReFa-Net/PF | PYNQ-Z1 (MO) | 100 | 278 | 35 657 | 129 (48 %) | 2,5 | 51 | W1A2 |

- Les ressources FINN-R incluent-elles le shell (297 kLUT sur AWS F1, §3.4) ? `n/r` : la
  note † de la Table 5 ne vise que les travaux cités. À vérifier sur le PDF.
- Justesse des prédictions (§5.3) : de 75 à 99 % en DF. En MO, les prédictions s'écartent
  davantage, faute de bien modéliser la mémoire externe ; le pire cas est DoReFa sur
  PYNQ-Z1 (48 %), à cause d'une réorganisation mémoire faite sur l'hôte.
- Records annoncés (§5.3) :
  - 50 TOp/s (MLP) et 12 TOp/s (CNN) sur AWS F1 ;
  - meilleure efficacité : 433 GOp/s/W (MLP, Ultra96) ;
  - DoReFa-Net à 11,43 TOp/s ; selon les auteurs, 22 TOp/s à 300 MHz (extrapolation non
    mesurée).
- Comparaisons (§5.3) : plus de 10× plus rapide que les solutions dataflow sur ZC706 ;
  Nakahara et al. et Zhao et al. (Zedboard) jusqu'à 2× plus lents ; 4× plus rapide que
  Yonekawa et al. (ZCU102) sur CNV. En revanche, Jiao et al. atteignent 410,2 GOp/s
  (DoReFa, Zynq 7020), contre 129 GOp/s pour FINN-R en MO : FINN-R est battu sur ce point.
- Absents du texte extrait : les **FPS**, la **latence** et la précision de MLP-4 et CNV-6
  (Table 4). Aucun DSP n'est rapporté (« non pertinents » hors couches 8 bits, §5.2).

Unités : la colonne BRAM compte des **BRAM18** (Table 5), alors que FINN compte des BRAM de
36 Kb (Table 3). Les deux ne sont pas directement comparables.

→ reportés dans `benchmarks.csv` : 12 lignes, une par ligne « FINN-R » de la Table 5.
Les précisions ne sont remplies que pour Tincy YOLO (mAP 50,1, §5.1) et DoReFa-Net/PF
(top-5 74,0, §5.1). Le dataset est `n/r` pour MLP-4, CNV-6 et DoReFa-Net/PF (non explicite
dans le texte extrait).

## Limites et critique

- **Métrique GOp/s seule** : ni FPS ni latence. Or les opérations binaires et les
  opérations 8 ou 16 bits ne se valent pas. Comparer 50 TOp/s binaires à 1,9 TOp/s en
  W8A16 (Wei et al.) mélange des unités non équivalentes (déduit).
- **Tableau comparatif hétérogène** (Table 5) : précisions de W1A1 à W16A16 ; puissances
  carte, PMBus (Prost-Boucle) ou absentes (AWS) ; valeurs estimées « ∼ » pour certains
  travaux cités ; fréquences différentes. Les auteurs reconnaissent eux-mêmes que
  l'efficacité n'est pas comparable avec Prost et al. (§5.3).
- **Mesure de puissance** : dite « au niveau carte » (§5.3), sans instrument ni durée
  précisés (contrairement à FINN, qui détaillait P_chip et P_wall). Rien sur AWS F1.
- **Tincy YOLO** : 50,1 % de mAP (métrique exacte et split non précisés dans le texte
  extrait), pour seulement 133 à 288 GOp/s en embarqué. Aucun FPS n'est donné, alors que
  c'est la métrique qui compte pour la détection en temps réel. Aucune comparaison
  Jetson / GPU.
- **MO peu performant** sur petites cibles : Jiao et al. font 3× mieux sur un Zynq 7020 ;
  le goulot vient de l'hôte ARM (§5.3).
- **Pas d'estimation de puissance ni de latence** dans l'outil (§4) ; les prédictions MO
  sont peu fiables (de 48 à 70 %).
- **Précision** : la Table 4 est absente de l'extraction, ce qui empêche de relier les
  performances aux précisions obtenues pour MLP-4 et CNV-6.

## Pertinence pour la thèse

C'est le pont entre FINN (BNN pur, arxiv-1612.07119) et les outils actuels (FINN open
source, hls4ml). Il apporte :
- des **modèles de coût** LUT et BRAM réutilisables pour dimensionner un accélérateur
  avant synthèse ;
- l'arbitrage **dataflow / offload multicouche**, central pour placer un YOLO ou un
  autoencodeur convolutif sur une petite puce (Ultra96 ≈ ZU3EG, proche de la gamme Kria
  KV260 — rapprochement déduit) ;
- un **premier YOLO quantifié** (Tincy YOLO, W1A3) sur SoC Zynq embarqué, repère
  historique de l'axe `yolo-fpga`.

À comparer avec hls4ml (arxiv-2103.05579, arxiv-2512.01463), qui applique aussi le principe
« une couche = un bloc » mais vise la très faible latence, et avec fpgaConvNet
(arxiv-1711.08740), dataflow mais sans quantification (§2.2).

## Gaps identifiés

- **YOLO sur FPGA sans FPS ni latence mesurés** : Tincy YOLO n'est rapporté qu'en GOp/s.
  Cela étaye le gap « pas de protocole de mesure commun pour YOLO sur FPGA ».
- **Estimation de puissance et de latence absente** des toolflows dataflow à l'époque :
  à vérifier dans FINN actuel et dans hls4ml 2025.
- **Architecture MO mal servie** sur petits SoC : les réseaux profonds de vision qui ne
  tiennent pas on-chip restent un verrou pour le dataflow quantifié.
- Aucune comparaison mesurée avec un Jetson ou un GPU embarqué.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Défauts d'extraction :
- **Table 4** (entraînement et précision des réseaux) absente ;
- fin de §5.1 et début de §5.2 fusionnés (texte tronqué) ;
- Figures 1 à 3 et 5 à 10 illisibles ou limitées à leur légende ;
- corps de l'Algorithme 1 partiellement en légende.
Déduit et non affirmé par les auteurs :
- non-équivalence des GOp/s entre précisions ;
- proximité Ultra96 / KV260 ;
- dataset ImageNet probable pour DoReFa-Net/PF (non reporté dans `benchmarks.csv`).
