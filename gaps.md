# Carte des gaps

Zones non couvertes et verrous repérés dans le corpus. Mis à jour par `/paper-gaps` à partir
des fiches `done` et de `benchmarks.csv`. Chaque gap cite les `paper_id` qui l'étayent et
distingue ce qui est lu de ce qui est déduit.

Format d'une entrée :

```
### <intitulé du gap>
- Constat : ce que montre le corpus (paper_id, section source).
- Ce qui manque : la question laissée ouverte.
- Statut : hypothèse (déduite de la bibliographie de départ) | étayé (fiches done).
- Piste : expérience ou lecture pour le confirmer.
```

---

Mise à jour du 24/09/2026 : 11 fiches `done` sur 12 (fpgaConvNet reste à ficher), 35 lignes
dans `benchmarks.csv`. **Réserve générale** : le corpus est petit et biaisé par la
bibliographie de départ.
- `autoencoder-fpga` n'a qu'un papier ; 20 des 35 lignes de benchmark viennent de FINN et
  FINN-R.
- Un gap qui ne repose que sur l'absence de papiers dans la base reste une `hypothèse`.
- Un gap `étayé` est constaté dans les fiches. Cela ne prouve pas son absence dans la
  littérature.

## Autoencodeurs

### Autoencodeurs sur FPGA appliqués aux images
- Constat :
  - les seuls autoencodeurs du corpus traitent des signaux 1D ou des données de
    physique : AE dense 32 → 2 sur PolarFire (arxiv-2602.15751, Table 1 et texte) ;
    autoencodeur d'anomalies sur jets et AE ASIC 65 nm (arxiv-2103.05579, Fig. 3 et
    §4.3.2) ;
  - hls4ml 2025 ne publie aucun autoencodeur convolutionnel d'images de taille réaliste et
    reconnaît une limite de synthèse des gros modèles (arxiv-2512.01463, §11) ;
  - dans `basicStart.txt` (résumés), le seul cas « image » passe par des scalogrammes de
    signaux 1D (CAE sur PYNQ-Z2, non ingéré).
- Recherche OpenAlex du 24/09/2026 (`/paper-discover autoencoder-fpga`, métadonnées
  OpenAlex non vérifiées, papiers non lus). Résultats :
  - **nuance** : les autoencodeurs d'images sur FPGA existent sous un autre vocabulaire,
    la **compression d'image apprise** (base VAE) : *F-LIC: FPGA-based Learned Image
    Compression with a Fine-grained Pipeline* (IEEE A-SSCC 2022, DOI
    10.1109/a-sscc56115.2022.9980666) ; *FPGA Codec System of Learned Image Compression
    With Algorithm-Architecture Co-Optimization* (IEEE JETCAS 2024, DOI
    10.1109/jetcas.2024.3386328) ;
  - la requête « image anomaly detection autoencoder FPGA » ne renvoie **aucune**
    implémentation FPGA sur images, seulement des revues et des travaux 1D (vibrations,
    réseau, physique) ;
  - les AE FPGA trouvés restent sur signaux 1D ou données tabulaires : *Edge-Compatible
    Convolutional Autoencoder Implemented on FPGA for Anomaly Detection in Vibration
    Condition-Based Monitoring* (IEEE Sensors Letters 2022, DOI 10.1109/lsens.2022.3159972),
    AE au LHC (arXiv 2108.03986).
- Ce qui manque : un CAE / VAE sur images ou vidéo réelles pour la **détection
  d'anomalies visuelles** (pas la compression), avec latence et puissance mesurées sur
  FPGA embarqué. La compression apprise montre que le calcul est faisable, mais sur des
  puces et avec des objectifs (débit de codec) différents.
- Statut : étayé dans le corpus (3 fiches) et conforté par la recherche ciblée pour la
  détection d'anomalies visuelles. Reformulé : le gap porte sur l'**anomalie visuelle**,
  pas sur « l'image » en général.
- Piste : ajouter 2108.03986 (arXiv) ; récupérer F-LIC et le codec JETCAS 2024 (IEEE,
  accès université) pour mesurer ce que la compression apprise sur FPGA apporte à un CAE
  de détection d'anomalies.

## YOLO et détection sur FPGA

### Pas de protocole de mesure commun pour YOLO sur FPGA
- Constat :
  - YOLOv5 sur KV260 (arxiv-2507.18174) : précision de classification mesurée sur 72
    images, variante YOLOv5 n/r, puissance sans méthode (Table I) ;
  - le survey arxiv-2509.04153 compare des designs YOLO sans conditions homogènes de
    puissance, mAP ou résolution (Tables VII-IX, constat déduit) ;
  - Tincy YOLO n'est rapporté qu'en GOp/s, sans FPS ni latence (arxiv-1809.04570,
    Table 5) ;
  - le problème existe déjà en 2018 (arxiv-1806.01683) ;
  - dans `benchmarks.csv`, sur 4 lignes de détection, **1 seule donne un FPS** et aucune
    ne donne de latence.
- Ce qui manque : mAP sur split officiel, variante et résolution déclarées, FPS et latence
  à batch 1, puissance carte au wattmètre et puissance puce par télémétrie — ensemble, pour
  une même carte.
- Statut : étayé (4 fiches + `benchmarks.csv`).
- Piste : expérience de référence YOLOv5 INT8 via Vitis AI sur KV260 avec ce protocole,
  plus un Jetson Orin Nano dans les mêmes conditions (SETUP §9). Modèle de protocole
  puissance : FINN, qui donne P_chip (PMBus) et P_wall (wattmètre) (arxiv-1612.07119, §5.1).

### Détection absente des toolflows dataflow quantifiés
- Constat :
  - FINN ne traite que la classification 32 × 32 (arxiv-1612.07119, §5.1) ;
  - FINN-R ne passe Tincy YOLO (W1A3, mAP 50,1) qu'en *multilayer offload* sur les cartes
    embarquées, avec des prédictions de performance à 66-68 % (arxiv-1809.04570, §5.1,
    Table 5) ;
  - hls4ml : aucun détecteur publié (arxiv-2103.05579 ; arxiv-2512.01463, §11).
- Ce qui manque : un YOLO moderne (v5 / v8) en dataflow quantifié (FINN ou hls4ml) sur SoC
  embarqué, comparé à Vitis AI (DPU) sur la même carte.
- Statut : étayé (4 fiches).
- Piste : chercher des travaux FINN / hls4ml pour la détection postérieurs à 2020
  (`/paper-discover` avec « YOLO FINN » et « hls4ml object detection »).

### Interaction PS-PL et post-traitement sur SoC FPGA
- Constat : la gestion temps réel PS-PL (RTOS, priorités, WCET) pour plusieurs modèles
  vidéo n'est pas traitée, selon les auteurs du survey (arxiv-2509.04153, §III-B). Le
  post-traitement (NMS, association) souvent fait en Python sur le PS fait chuter le débit
  de 195 à 24 FPS dans un exemple cité (arxiv-2509.04153, §VI-C).
- Ce qui manque : une mesure bout en bout (capture → PL → post-traitement → sortie) sur
  SoC, avec partitionnement PS / PL justifié.
- Statut : étayé, mais sur l'affirmation d'un seul survey, et le chiffre de débit vient
  d'un travail cité ([125]), non lu.
- Piste : lire la référence [125] de arxiv-2509.04153 ; instrumenter la latence bout en
  bout dans l'expérience KV260.

## Mesure et comparaison

### Pas de baseline GPU / Jetson mesurée dans les mêmes conditions
- Constat : aucune comparaison Jetson ou GPU mesurée dans FINN (seulement une estimation
  roofline K40, arxiv-1612.07119, §3.1), FINN-R (arxiv-1809.04570), YOLOv5 KV260
  (arxiv-2507.18174), hls4ml (arxiv-2103.05579, arxiv-2512.01463). Seul ImageHD compare à
  un Jetson AGX Orin, en PyTorch à batch 1 (arxiv-2604.21280). Dans `benchmarks.csv`, 3
  lignes sur 35 ont une baseline GPU ou Jetson, toutes de ce papier.
- Ce qui manque : même modèle, même précision numérique, même batch, même méthode de
  puissance, sur FPGA embarqué et Jetson.
- Statut : étayé (6 fiches + `benchmarks.csv`).
- Piste : volet Jetson Orin Nano de l'expérience de référence.

### Puissance : puce contre carte, estimée contre mesurée
- Constat :
  - FINN : P_chip et P_wall, avec ~7 W de repos pour la ZC706 (arxiv-1612.07119, §5.1,
    §5.2.2) ;
  - FINN-R : puissance « carte » sans méthode, rien sur AWS F1 (arxiv-1809.04570, §5.3) ;
  - ImageHD : énergie FPGA estimée par outil (arxiv-2604.21280) ;
  - hls4ml 2021 et 2025 : aucune mesure de puissance (arxiv-2103.05579,
    arxiv-2512.01463) ;
  - dans `benchmarks.csv`, `power_w` vaut `n/r` sur 12 lignes sur 35, et la nature puce /
    carte n'est connue que par la fiche.
- Ce qui manque : une convention de mesure (et une colonne ou une note puce / carte dans
  `benchmarks.csv`).
- Statut : étayé (5 fiches).
- Piste : ajouter à DATA_MODEL §7 une mention puce / carte / estimée pour `power_w`.

## Toolflows

### Pas de comparaison croisée hls4ml / FINN / Vitis AI sur un même CNN et une même carte
- Constat : les papiers d'outils ne se comparent pas entre eux sur un modèle commun
  (arxiv-2512.01463 ; arxiv-2103.05579, qui liste FINN et fpgaConvNet sans les mesurer).
  FINN-R se compare en GOp/s à des travaux hétérogènes (arxiv-1809.04570, Table 5).
- Ce qui manque : un même CNN, une même carte, les trois flots ; puis ressources, latence,
  puissance et précision.
- Statut : hypothèse. Un comparatif hls4ml / FINN (Springer) figure dans `basicStart.txt`
  mais n'est pas ingéré (paywall) : il pourrait combler ce gap.
- Piste : récupérer ce PDF par l'accès université et le déposer dans `inbox/`.

### Réseaux qui ne tiennent pas on-chip : limite du dataflow
- Constat :
  - FINN suppose tous les paramètres en OCM ; la mémoire externe est reportée en travail
    futur (arxiv-1612.07119, §6) ;
  - l'offload multicouche de FINN-R est peu prévisible (48 à 70 % de justesse) et 3× plus
    lent que Jiao et al. sur Zynq 7020 (arxiv-1809.04570, §5.3, Table 5) ;
  - hls4ml a des limites de synthèse sur les gros modèles (arxiv-2512.01463, §11).
- Ce qui manque : un flot quantifié qui garde les avantages du dataflow pour des réseaux
  de vision profonds sur petite puce (ZU3EG / KV260).
- Statut : étayé (3 fiches).
- Piste : ficher fpgaConvNet (arxiv-1711.08740), qui traite la reconfiguration quand le
  design ne tient pas.

### Estimation de puissance et de latence dans les toolflows
- Constat : FINN-R ne gère que les contraintes de ressources et de débit ; latence et
  puissance sont reportées à plus tard (arxiv-1809.04570, §4). Aucune mesure de puissance
  dans hls4ml 2025 (arxiv-2512.01463).
- Ce qui manque : un modèle de puissance validé sur carte, intégré au flot.
- Statut : hypothèse pour l'état actuel (le FINN d'aujourd'hui n'est pas dans le corpus).
- Piste : vérifier la documentation et les publications du FINN actuel.

### NAS matériel-aware ciblant les FPGA
- Constat : absent du survey embarqué arxiv-2411.01431. hls4ml ne cite que des prédicteurs
  de ressources pour des MLP (rule4ml, arxiv-2512.01463).
- Statut : hypothèse (absence dans deux papiers seulement).
- Piste : recherche ciblée « hardware-aware NAS FPGA latency predictor ».

## Apprentissage continu embarqué

### Pas de comparaison MCU / FPGA / Jetson pour un même algorithme de CL
- Constat : O-FSCIL est mesuré sur MCU GAP9 seulement (arxiv-2403.07851) ; ImageHD sur
  ZCU104 contre CPU, GPU et Jetson, mais pas contre un MCU (arxiv-2604.21280) ; le survey
  arxiv-2411.01431 n'a pas de chiffres système pour le CL.
- Ce qui manque : un même algorithme de CL (SLDA, replay latent, FSCIL) mesuré sur les
  trois cibles, énergie par classe ajoutée comprise.
- Statut : étayé (3 fiches).
- Piste : *A TinyML Platform for On-Device Continual Learning With Quantized Latent
  Replays* (arXiv 2110.10486, candidat de `bin/pdb discover`, à vérifier) ; l'accélérateur
  SLDA de `basicStart.txt` (paywall).

### CL sur FPGA : précision faible et énergie estimée
- Constat : ImageHD fait du clustering non supervisé à 26,89 % d'ACC sur CIFAR-10, avec une
  énergie estimée et non mesurée sur carte (arxiv-2604.21280, Table VII).
- Ce qui manque : la frontière précision / énergie d'un CL supervisé sur la même carte.
- Statut : étayé (1 fiche).
- Piste : ajouter Chameleon (TCAD 2024, `basicStart.txt`, paywall).

### CL limité à la classification
- Constat : FSCIL et ImageHD traitent la classification ou le clustering d'images, pas la
  détection (arxiv-2403.07851, arxiv-2604.21280).
- Ce qui manque : l'incrémental de classes en détection (YOLO) sur cible embarquée.
- Statut : étayé (2 fiches). Question de thèse candidate, au croisement des axes
  `yolo-fpga` et `continual-learning`.
- Piste : recherche « class-incremental object detection edge FPGA ».

## Surveys

### Les FPGA absents des surveys « embarqué »
- Constat : le survey *Efficient Deep Learning Infrastructures for Embedded Computing
  Systems* ne couvre ni toolflow ni accélérateur FPGA (arxiv-2411.01431, fiche
  « Limites »).
- Ce qui manque : une synthèse qui place les FPGA face aux MCU et aux GPU embarqués sur des
  critères communs.
- Statut : étayé (1 survey). C'est un argument de positionnement pour une thèse, pas un
  verrou technique.
- Piste : citer ce manque dans l'état de l'art du pré-projet.
