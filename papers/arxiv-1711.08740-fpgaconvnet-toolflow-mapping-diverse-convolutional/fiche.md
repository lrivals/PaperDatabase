---
id: arxiv-1711.08740-fpgaconvnet-toolflow-mapping-diverse-convolutional
fiche: done
date: 2026-09-24
---

# fpgaConvNet: A Toolflow for Mapping Diverse Convolutional Neural Networks on Embedded FPGAs

Stylianos I. Venieris, Christos-Savvas Bouganis, 2017, NIPS 2017 Workshop on Machine Learning on the Phone and other Consumer Devices. <https://arxiv.org/abs/1711.08740>
Type : conférence (article de workshop NIPS 2017, 4 pages ; DOI n/r). C'est la
présentation « toolflow » de fpgaConvNet, **distincte** de l'article de référence FCCM 2016
(*fpgaConvNet: A Framework for Mapping Convolutional Neural Networks on FPGAs*, DOI
10.1109/FCCM.2016.22). Ce dernier est absent de la base (paywall IEEE) alors que 6 papiers du
corpus le citent.

## Problème

Les CNN se complexifient et les besoins varient selon l'application : haut débit pour la
vidéosurveillance, faible latence pour la voiture autonome. Leur placement sur un FPGA est
un espace de conception trop vaste pour être exploré à la main. Il faut un outil qui
automatise ce placement en optimisant la métrique voulue : débit, latence, ou les deux
(§1).

## Méthode

- **Modèle Synchronous Dataflow (SDF)** (§2.1-2.3) :
  - chaque couche est traduite en une chaîne de blocs matériels paramétrables ;
  - un nœud SDF par bloc ;
  - le design est décrit par une matrice de topologie Γ (débits de données), et la charge
    de travail par une matrice W (Fig. 1).
- **Quatre transformations algébriques** sur le modèle SDF (§2.4, Fig. 2) :
  1. *graph partitioning with reconfiguration* : le réseau est coupé en profondeur, avec
     une architecture et un bitstream par partition. La reconfiguration complète du FPGA
     est amortie par le traitement par lots, ce qui vise le débit ;
  2. *coarse-grained folding* : nombre d'unités par couche ;
  3. *fine-grained folding* : parallélisme du produit scalaire dans une unité de
     convolution ;
  4. *weights reloading* : une architecture flexible unique exécute toutes les partitions
     en rechargeant les poids, **sans reconfiguration**, ce qui vise la latence (réf. [10]).
- L'exploration est un problème d'optimisation : estimateurs analytiques de débit et de
  latence, et modèles de ressources (§2.4).
- Entrée : un modèle Caffe. Réseaux gérés :
  - à connectivité régulière : AlexNet, VGG16 ;
  - à connectivité irrégulière : Inception, ResNet, DenseNet. Les auteurs présentent le
    premier placement de DenseNet-161 sur FPGA (§1).

## Plateforme et implémentation

- FPGA : Xilinx Zynq **Z7045**, à 125 MHz pour la comparaison à 5 W. Pic de 270 GOp/s, bande
  passante mémoire de 4,2 GB/s (§3.1).
- Arithmétique : virgule fixe 16 bits (FXP16) (§3.1).
- Baseline : NVIDIA Tegra X1 (TensorRT, cuDNN v6, FP16), à 76,8 MHz pour le budget de
  5 W (79 GFLOPS, 12,8 GB/s), puis à 998 MHz pour le pic de performance par watt (§3.1).
- **Puissance** : mesurée « via un power monitor » sur les deux plateformes, **puissance
  de repos soustraite**, soit la puissance dynamique de la carte (§3.1). Instrument et
  durée : n/r.
- Ressources FPGA (LUT, DSP, BRAM) : n/r.
- Code : non publié d'après le texte (aucun lien).

## Résultats

- **Même budget de 5 W** (§3.1, Fig. 3) :
  - applications orientées débit : jusqu'à **5,53×** le débit du Tegra X1, 3,32× en moyenne
    (3,07× en moyenne géométrique) ;
  - applications orientées latence (batch 1, légende de Fig. 3b) : jusqu'à **6,65×**,
    3,95× en moyenne (3,43× en moyenne géométrique).
- **GPU à pleine fréquence** (998 MHz) : gain en GOp/s/W de 1,17× (1,12× en moyenne
  géométrique) en débit et de 1,70× (1,36×) en latence (§3.1).
- Réseaux évalués : AlexNet, VGG16, GoogLeNet, DenseNet-161. Le débit ou la latence par
  réseau n'apparaît que dans la Fig. 3, non lisible dans l'extraction : n/r ici.

→ reportés dans `benchmarks.csv` : **aucune ligne**. Le papier ne donne que des ratios par
rapport au Tegra X1. Les valeurs absolues (GOp/s, FPS, latence par réseau) sont dans la
Fig. 3 seulement, et aucune ressource FPGA n'est rapportée. Les chiffres absolus sont à
chercher dans l'article FCCM 2016 et la version TNNLS de fpgaConvNet (hors base).

## Limites et critique

- **Papier de workshop** : pas de chiffres absolus dans le texte, pas de ressources, pas
  de précision (le FXP16 est supposé sans perte, rien n'est mesuré).
- **Comparaison au GPU** :
  - point fort : c'est l'un des rares papiers du corpus à mesurer un GPU embarqué, à
    budget de puissance égal, avec la même méthode de mesure (idle soustrait) des deux
    côtés ;
  - mais le Tegra X1 bridé à 76,8 MHz est un point de fonctionnement artificiel ;
  - FP16 contre FXP16 : précisions comparables, mais les frameworks diffèrent (TensorRT
    contre accélérateur sur mesure) ;
  - le gain en GOp/s/W à pleine fréquence est modeste (1,12× en moyenne géométrique).
- **Puissance dynamique seulement** : soustraire le repos avantage les deux plateformes et
  masque la consommation réelle de la carte. Non comparable au P_wall de FINN
  (arxiv-1612.07119), qui inclut ~7 W de repos (déduit).
- **Reconfiguration complète amortie par lots** : pour la latence à batch 1, elle est
  remplacée par le rechargement des poids. Le coût de ce rechargement n'est pas chiffré
  ici.
- Pas de quantification sous 16 bits : FINN-R le relève (« fpgaConvNet is not
  quantization-aware », arxiv-1809.04570, §2.2).

## Pertinence pour la thèse

C'est la troisième lignée de toolflows dataflow, à côté de FINN et hls4ml. Son apport
spécifique : **exécuter sur un petit FPGA des réseaux qui ne tiennent pas on-chip**, par
partitionnement plus reconfiguration (débit) ou par rechargement des poids (latence). Cela
répond directement au gap « réseaux qui ne tiennent pas en mémoire du FPGA », que FINN
laisse ouvert (§6) et que l'offload multicouche de FINN-R traite mal. Autres points utiles
(déduits) :
- le protocole « même budget de puissance que le GPU embarqué » est un modèle pour la
  comparaison KV260 / Jetson Orin Nano ;
- l'optimisation explicite débit contre latence correspond au besoin d'une détection YOLO
  à batch 1.

## Gaps identifiés

- Combinaison **quantification agressive + partitionnement / rechargement des poids** : non
  traitée. fpgaConvNet est en FXP16 ; FINN et FINN-R sont quantifiés, mais supposent que le
  réseau tient on-chip ou utilisent un offload peu performant.
- **Détection d'objets** : absente (classification uniquement), alors que l'intérêt du
  mode latence est le temps réel.
- Coût du rechargement des poids et de la reconfiguration non chiffré dans ce papier.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier ; papier de 4 pages). Défauts d'extraction :
- une section numérotée non détectée (« 2 Synchronous Dataflow Modelling », rattachée
  au §1) ;
- matrices de la Fig. 1 illisibles ;
- valeurs de la Fig. 3 absentes.
Déduit et non affirmé par les auteurs :
- puissance dynamique non comparable au P_wall de FINN ;
- pertinence pour le gap « réseaux hors on-chip » et pour la comparaison KV260 / Jetson.
