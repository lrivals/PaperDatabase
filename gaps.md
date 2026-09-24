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

Mise à jour du 24/09/2026 (5e passage) : 24 fiches `done` sur 28, 109 lignes dans
`benchmarks.csv`. Fiches ajoutées depuis le 2e passage :
- 2022-feng-benchmark-analysis-yolo-performance-edge ;
- arxiv-2211.11647-benchmarking-edge-computing-devices-grape ;
- 2025-el-zeinaty-designing-object-detection-models-tinyml ;
- 2023-zhai-fpga-vehicle-detection-tracking-accelerator ;
- arxiv-2110.15352 (MCUNetV2) et arxiv-2306.00001 (TinyissimoYOLO) ;
- arxiv-2108.03986 (autoencodeurs au LHC) ;
- 2023-shuvo, 2024-mittal et 2025-hozhabr (surveys).

**Réserve générale** : le corpus est petit et biaisé par la bibliographie de départ.
- `autoencoder-fpga` n'a que deux papiers, tous deux sur données de physique.
- `benchmarks.csv` est déséquilibré : 24 des 109 lignes viennent de Feng et al. (Jetson et
  VPU, sans mAP), 20 de FINN et FINN-R.
- Restent à ficher : arxiv-2010.15277, arxiv-2206.15472, arxiv-2409.07114 (CL et
  entraînement sur MCU) et 2023-cui (survey d'anomalie visuelle).
- 5e passage : fiches arxiv-2502.15737 (Orin, TensorRT INT8) et arxiv-2409.16808 (mAP
  COCO sur Orin et Hailo).
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
- Constat (fiche du 3e passage, arxiv-2108.03986-autoencoders-fpgas-real-time-unsupervised) :
  - AE et VAE pour la détection d'anomalies au trigger du LHC, sur des données
    **tabulaires** 19 × 3 traitées comme une image 2D (§III) ;
  - le seul modèle convolutionnel (CNN AE) est aussi le seul à dépasser le budget : 47 %
    des LUT d'un VU9P, II de 895 ns, sur une entrée de seulement 20 × 3 (Table III) ;
  - trois idées transposables à un CAE d'images (§IV, §VI) :
    - score d'anomalie calculé sur puce ;
    - VAE réduit à l'encodeur, avec score D_KL ;
    - PTQ préféré au QAT quand le QAT déstabilise le score.
- Ce qui manque : un CAE / VAE sur images ou vidéo réelles pour la **détection
  d'anomalies visuelles** (pas la compression), avec latence et puissance mesurées sur
  FPGA embarqué. La compression apprise montre que le calcul est faisable, mais sur des
  puces et avec des objectifs (débit de codec) différents.
- Statut : étayé dans le corpus (4 fiches) et conforté par la recherche ciblée pour la
  détection d'anomalies visuelles. Reformulé : le gap porte sur l'**anomalie visuelle**,
  pas sur « l'image » en général.
- Piste : récupérer F-LIC et le codec JETCAS 2024 (IEEE, accès université) pour mesurer ce
  que la compression apprise sur FPGA apporte à un CAE de détection d'anomalies. Point de
  départ possible : la branche hls4ml `AE_L1_paper` (arxiv-2108.03986, §IX), dont les
  couches de score seraient à porter sur un CAE d'images, sur Kria.

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
  - le même défaut se retrouve hors FPGA et dans les designs FPGA récents :
    - Feng et al. mesurent une « mean confidence », pas une mAP ; leurs Jetson tournent
      sans TensorRT, en FP16 ; puissance JTOP contre wattmètre USB, portée non dite
      (2022-feng-benchmark-analysis-yolo-performance-edge, §3.2, §4.1, Table 3) ;
    - Magalhães et al. ne chronomètrent que le cœur du réseau, hors pré- et
      post-traitement ; ils mélangent FP16 (TX2) et INT8 (FPGA, TPU) ; leurs chiffres ne
      sont publiés qu'en figures (arxiv-2211.11647, §2.5, §3, Fig. 6-7) ;
    - Zhai et al. donnent une AP@0.5 sur UA-DETRAC à une seule classe (pas COCO), une
      puissance sans méthode, et des baselines Jetson et Vitis AI reprises d'autres papiers
      avec d'autres modèles (2023-zhai-fpga-vehicle-detection-tracking-accelerator,
      Table 7, Table 8) ;
    - côté MCU, le tableau comparatif d'El Zeinaty et al. ne donne ni latence ni énergie
      (2025-el-zeinaty-designing-object-detection-models-tinyml, Table 8) ;
  - dans `benchmarks.csv`, sur 71 lignes de détection :
    - 49 donnent un FPS et 21 une latence ;
    - **15 seulement ont une mAP COCO**, toutes d'Alqahtani et al., un preprint, sur Jetson
      et Hailo, précision numérique non déclarée ;
    - **aucune ligne FPGA n'a de mAP COCO**. Les mAP FPGA du corpus sont sur UA-DETRAC
      (Zhai) ou VOC (FINN-R).
- Ce qui manque : mAP sur split officiel, variante et résolution déclarées, FPS et latence
  à batch 1, puissance carte au wattmètre et puissance puce par télémétrie — ensemble, pour
  une même carte.
- Statut : étayé (8 fiches + `benchmarks.csv`). Le défaut n'est pas propre au FPGA : il
  touche aussi les benchmarks Jetson, VPU et MCU.
- Piste : expérience de référence YOLOv5 INT8 via Vitis AI sur KV260 avec ce protocole,
  plus un Jetson Orin Nano dans les mêmes conditions (SETUP §9). Modèle de protocole
  puissance : FINN, qui donne P_chip (PMBus) et P_wall (wattmètre) (arxiv-1612.07119, §5.1).

### Détection absente des toolflows dataflow quantifiés
- Constat :
  - FINN ne traite que la classification 32 × 32 (arxiv-1612.07119, §5.1) ;
  - FINN-R ne passe Tincy YOLO (W1A3, mAP 50,1) qu'en *multilayer offload* sur les cartes
    embarquées, avec des prédictions de performance à 66-68 % (arxiv-1809.04570, §5.1,
    Table 5) ;
  - hls4ml : aucun détecteur publié (arxiv-2103.05579 ; arxiv-2512.01463, §11) ;
  - fpgaConvNet (FXP16, non quantifié en dessous) n'évalue que des classifieurs (AlexNet,
    VGG16, GoogLeNet, DenseNet-161), alors que son mode « latence » vise le temps réel
    (arxiv-1711.08740, §3.1).
- Ce qui manque : un YOLO moderne (v5 / v8) en dataflow quantifié (FINN ou hls4ml) sur SoC
  embarqué, comparé à Vitis AI (DPU) sur la même carte.
- Point de comparaison disponible : un design HLS **maison** (hors toolflow) fait tourner un
  YOLOv3-tiny élagué en INT16 à 91,65 FPS sur XC7Z035, pour 12,51 W de puissance « full »
  sans méthode décrite (2023-zhai-fpga-vehicle-detection-tracking-accelerator, Table 8).
  Il sert de référence à battre pour un flot dataflow quantifié.
- Statut : étayé (5 fiches).
- Piste : chercher des travaux FINN / hls4ml pour la détection postérieurs à 2020
  (`/paper-discover` avec « YOLO FINN » et « hls4ml object detection »).

### Interaction PS-PL et post-traitement sur SoC FPGA
- Constat : la gestion temps réel PS-PL (RTOS, priorités, WCET) pour plusieurs modèles
  vidéo n'est pas traitée, selon les auteurs du survey (arxiv-2509.04153, §III-B). Le
  post-traitement (NMS, association) souvent fait en Python sur le PS fait chuter le débit
  de 195 à 24 FPS dans un exemple cité (arxiv-2509.04153, §VI-C).
- Constat (ajouté au 3e passage) :
  - Zhai et al. placent le NMS et Deepsort sur l'ARM, sans dire s'ils sont inclus dans les
    FPS (2023-zhai-fpga-vehicle-detection-tracking-accelerator, §3.3) ;
  - Magalhães et al. excluent explicitement pré- et post-traitement (OpenCV, sur CPU) de
    leurs mesures, sur toutes les cibles (arxiv-2211.11647, §2.4-2.5).
- Contre-exemples cités par 2025-hozhabr-survey-real-time-object-detection (§V-A), non
  lus à la source :
  - Anupreetham et al. [67] : NMS **pipeliné sur FPGA** (Stratix 10), 2,13 ms de bout en
    bout ;
  - D. Zhang et al. [86] : système entièrement sur FPGA, post-traitement compris, sans
    CPU (KC705, YOLOv3-tiny 8 bits, 65 FPS, 12 W système).
  Le NMS matériel existe donc, mais pas sur les SoC embarqués du corpus (Zynq, Kria).
- Ce qui manque : une mesure bout en bout (capture → PL → post-traitement → sortie) sur
  SoC, avec partitionnement PS / PL justifié.
- Statut : étayé (4 fiches). Le chiffre de débit de 195 à 24 FPS vient toujours d'un
  travail cité ([125]), non lu. Nuancé : des solutions de NMS matériel existent sur FPGA
  de centre de calcul ou de milieu de gamme.
- Piste : lire la référence [125] de arxiv-2509.04153 ; ajouter [67] et [86] de
  2025-hozhabr (références dans son `refs.jsonl`) ; instrumenter la latence de bout en
  bout dans l'expérience KV260.

## Mesure et comparaison

### Précision non vérifiée sur la cible après compilation et quantification
- Constat :
  - Feng et al. : après conversion OpenVINO, YOLOv3-tiny tombe à **0 % de confiance
    moyenne** sur RPi + NCS2, contre 59,7 % sur Jetson, à cause des couches Region de
    Darknet coupées par le Model Optimizer. Les auteurs ne l'ont vu que parce qu'ils
    comparaient plusieurs cibles (2022-feng-benchmark-analysis-yolo-performance-edge,
    Table 3, §4.1, §5) ;
  - Magalhães et al. (arxiv-2211.11647) :
    - la quantification post-entraînement du compilateur Edge TPU réduit précision et
      rappel (§3) ;
    - le modèle ne se compile pas sur Jetson Nano, faute de mémoire, ni en INT8 sur TX2
      (§3, §4) ;
    - le DPU impose une modification d'architecture (duplication de P6, §2.3) ;
  - Zhai et al. rapportent une AP@0.5 **identique à trois décimales** en FP32 et en INT16
    (0,711 et 0,599) et ne disent pas où elle est mesurée
    (2023-zhai-fpga-vehicle-detection-tracking-accelerator, Table 8). Déduit : AP
    probablement mesurée en flottant, hors FPGA ;
  - Rey et al. mesurent la mAP par configuration et, vraisemblablement, par carte (INT8 :
    0,7968 sur Nano, 0,7970 sur NX). La quantification post-entraînement INT8 de TensorRT
    coûte **de 6,4 à 12,3 points de mAP50-95** (YOLOv8n : de 84,2 à 71,9), sur un jeu
    pourtant facile, alors que la discussion la dit sans perte notable
    (arxiv-2502.15737-performance-analysis-you-only-look, Table 4, §6) ;
  - Alqahtani et al. rapportent des mAP **identiques** sur Jetson Nano et Orin Nano (§IV-C),
    ce qui ne permet pas de savoir si la mesure a été faite sur chaque carte ; sur Coral,
    la chute de YOLOv8 mélange conversion TFLite et résolution 320
    (arxiv-2409.16808-comprehensive-evaluation-deep-learning-object, Key Insight 3) ;
  - YOLOv5 sur KV260 : précision mesurée sur 72 images seulement (arxiv-2507.18174,
    Table I).
- Ce qui manque : un protocole qui mesure la mAP **sur la cible**, sur le split officiel,
  après chaque étape de la chaîne (quantification, compilation, partitionnement). Et une
  analyse de ce que chaque toolflow (Vitis AI, FINN, hls4ml, OpenVINO, TensorRT) change au
  graphe et à la précision.
- Statut : étayé (5 fiches), en partie déduit pour Zhai et al. Rey et al. en donnent la mesure la plus nette côté Jetson. C'est peut-être
  le gap le plus directement exploitable : il se vérifie expérimentalement à faible coût.
- Piste : dans l'expérience de référence KV260, évaluer la mAP COCO val sur la carte
  elle-même (sorties du DPU relues, NMS compris) et la comparer à la mAP du modèle flottant
  et du modèle quantifié simulé. Chercher les travaux sur la « quantization accuracy gap
  on-device » et la vérification post-compilation.

### Pas de baseline GPU / Jetson mesurée dans les mêmes conditions
- Constat : aucune comparaison Jetson ou GPU mesurée dans FINN (seulement une estimation
  roofline K40, arxiv-1612.07119, §3.1), FINN-R (arxiv-1809.04570), YOLOv5 KV260
  (arxiv-2507.18174), hls4ml (arxiv-2103.05579, arxiv-2512.01463). Seul ImageHD compare à
  un Jetson AGX Orin, en PyTorch à batch 1 (arxiv-2604.21280). fpgaConvNet mesure un Tegra X1
  (TensorRT, FP16) à budget de puissance égal (5 W) avec la même méthode (repos soustrait),
  mais ne publie que des ratios : jusqu'à 6,65× en débit, et seulement 1,12× (moyenne
  géométrique) en GOp/s/W face au GPU à pleine fréquence (arxiv-1711.08740, §3.1).
- Constat (ajouté au 3e passage) : les premiers chiffres Jetson du corpus ne comblent pas le
  gap.
  - Feng et al. mesurent Jetson Nano et Xavier NX (20 lignes de `benchmarks.csv`) sans
    TensorRT, en FP16, sans mAP, avec une puissance de portée inconnue
    (2022-feng-benchmark-analysis-yolo-performance-edge, §3.2, §4). Ce ne sont pas des
    baselines « état de l'art Jetson ».
  - Magalhães et al. comparent TX2, Coral, ZCU104 et KV260 sur le même modèle et le même
    jeu de données, avec mAP et puissance mesurée à l'entrée de la carte. Mais seule une
    Jetson de 2017 a tourné, sans INT8, et les valeurs ne sont qu'en figures
    (arxiv-2211.11647, §2.5, §3).
  - Zhai et al. comparent leur FPGA à une Jetson Nano **reprise d'un autre papier**, avec un
    modèle non élagué 2,5 fois plus lourd
    (2023-zhai-fpga-vehicle-detection-tracking-accelerator, Table 7).
  - Deux baselines Orin ajoutées au 5e passage, **complémentaires mais chacune
    incomplète** :
    - Rey et al. : Orin Nano et Orin NX avec TensorRT **FP32, FP16 et INT8**, puissance
      par **télémétrie** (tegrastats), énergie par inférence. Par exemple YOLOv8n INT8
      sur Orin NX : 65,8 FPS, 10,3 W, 0,18 J. Mais la mAP est calculée sur un jeu privé
      très facile, pas sur COCO (arxiv-2502.15737-performance-analysis-you-only-look,
      Table 4) ;
    - Alqahtani et al. : **mAP COCO val** sur Orin Nano, Jetson Nano et Hailo-8, et
      énergie **hors repos** au wattmètre USB. Par exemple YOLOv8n sur Orin Nano : mAP 31,
      16 ms. Mais la précision TensorRT n'est pas déclarée, il n'y a aucune puissance en
      W, et c'est un preprint (arxiv-2409.16808-comprehensive-evaluation-deep-learning-object,
      §IV).
  - Aucune source ne réunit encore Orin + TensorRT INT8 déclaré + mAP COCO + puissance de
    carte en W.
- Ce qui manque : même modèle, même précision numérique, même batch, même méthode de
  puissance, sur FPGA embarqué et Jetson.
- Statut : étayé (12 fiches + `benchmarks.csv`), **partiellement comblé** côté Jetson.
  Combiner les deux sources donne un ordre de grandeur Orin exploitable, mais pas une
  baseline à protocole unique. Côté FPGA, aucune source ne mesure dans les mêmes
  conditions. Seul fpgaConvNet suit le bon protocole, sur un GPU de 2015.
- Piste : volet Jetson Orin Nano de l'expérience de référence, sur le modèle de fpgaConvNet :
  même budget de puissance, même méthode de mesure, chiffres absolus publiés.

### Puissance : puce contre carte, estimée contre mesurée
- Constat :
  - FINN : P_chip et P_wall, avec ~7 W de repos pour la ZC706 (arxiv-1612.07119, §5.1,
    §5.2.2) ;
  - FINN-R : puissance « carte » sans méthode, rien sur AWS F1 (arxiv-1809.04570, §5.3) ;
  - fpgaConvNet : puissance de carte **moins le repos** (arxiv-1711.08740, §3.1), une
    troisième convention ;
  - ImageHD : énergie FPGA estimée par l'analyseur Vitis (arxiv-2604.21280) ;
  - YOLOv5 KV260 et O-FSCIL : puissance sans méthode décrite (arxiv-2507.18174, Table I ;
    arxiv-2403.07851, §VI-C) ;
  - hls4ml 2021 et 2025 : aucune mesure de puissance (arxiv-2103.05579,
    arxiv-2512.01463).
  - Feng et al. : JTOP sur les Jetson, « USB dynamometer » sur le RPi, portée non dite ;
    les Tables 5-6 ne donnent que la puissance du GPU seul
    (2022-feng-benchmark-analysis-yolo-performance-edge, §4, Tables 3-6) ;
  - Zhai et al. : « Full Power » (~12,5 W) et « Dynamic Power » (~1,3 W) sans méthode. La
    comparaison avec les travaux antérieurs se fait en GOPS/W **dynamiques**, ce qui exclut
    le statique qui domine (2023-zhai-fpga-vehicle-detection-tracking-accelerator,
    Table 8, §4.4) ;
  - Magalhães et al. mesurent à l'entrée de la carte (multimètre, V puis I), la bonne
    portée, mais ne publient pas les valeurs dans le texte (arxiv-2211.11647, §2.5,
    Fig. 12) ;
  - Colonne `power_scope` ajoutée à `benchmarks.csv` (DATA_MODEL §7, 24/09/2026). Sur 109
    lignes : 16 `board`, **14 `chip`** (Rey et al., tegrastats et PMIC du RPi 5, Jetson
    et RPi seulement), 24 `unspecified` (Feng 12, Zhai 8, O-FSCIL 3, YOLOv5 KV260 1),
    3 `estimated`, 52 sans puissance (`n/r`). **Aucune ligne FPGA n'est en `chip` ni en
    `board-dynamic`.** TinyissimoYOLO mesure bien
    sur le MCU seul (portée puce), mais en énergie par inférence, sans puissance en watts :
    `power_w` y vaut donc `n/r`. Les 16 lignes `board`
    viennent toutes de FINN et FINN-R, sur des cartes anciennes (ZC706, PYNQ-Z1,
    Ultra96). Les ajouts de ce passage n'ont fait qu'augmenter les `unspecified`.
- Ce qui manque : des mesures `chip` et `board` sur la même carte récente, pour séparer ce
  qui revient à l'accélérateur de ce qui revient à la plateforme. Aucune ligne du corpus ne
  permet de comparer deux papiers à portée de puissance égale sur une cible actuelle
  (Kria, Versal).
- Appui publié : une revue de Proc. IEEE note qu'un processeur peut annoncer une très
  faible consommation sans compter les accès à la mémoire externe, et qu'il faut séparer
  résultats simulés et mesurés (2023-shuvo-efficient-acceleration-deep-learning-inference,
  §IX-I).
- Statut : étayé (12 fiches + `benchmarks.csv`, désormais mesurable par `power_scope`).
- Piste : dans l'expérience KV260, relever les deux portées (télémétrie de la puce et
  wattmètre de carte) et la puissance de repos, pour pouvoir en déduire aussi la valeur
  `board-dynamic`.

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
  - hls4ml a des limites de synthèse sur les gros modèles (arxiv-2512.01463, §11) ;
  - fpgaConvNet est le seul du corpus à traiter explicitement ce cas (arxiv-1711.08740,
    §2.4) :
    - découpage en profondeur avec une reconfiguration complète par partition, amortie
      par batch (débit) ;
    - ou rechargement des poids dans une architecture flexible unique (latence, batch 1).
    Il ne chiffre ni le coût de la reconfiguration ni celui du rechargement dans ce papier,
    et reste en FXP16 : FINN-R note qu'il n'est pas « quantization-aware »
    (arxiv-1809.04570, §2.2).
- Ce qui manque : **la combinaison des deux lignées**. D'un côté la quantification
  agressive de FINN / FINN-R, qui suppose un réseau tenant on-chip ou passe par un offload
  peu performant ; de l'autre le partitionnement et le rechargement des poids de
  fpgaConvNet, en 16 bits. Il faut les réunir pour un réseau de vision profond (YOLO,
  autoencodeur convolutif) sur petite puce (ZU3EG / KV260), avec le coût du rechargement
  mesuré à batch 1.
- Statut : étayé (4 fiches). La combinaison est absente du corpus ; son absence dans la
  littérature reste une hypothèse (les versions ultérieures de fpgaConvNet et de FINN ne
  sont pas dans la base).
- Piste : ajouter l'article FCCM 2016 et la version journal de fpgaConvNet, et chercher
  « fpgaConvNet quantization » et « FINN external memory weights » (`/paper-discover`). Un
  candidat de thèse : un flot quantifié à rechargement des poids pour la détection à
  batch 1 sur KV260.

### Estimation de puissance et de latence dans les toolflows
- Constat : FINN-R ne gère que les contraintes de ressources et de débit ; latence et
  puissance sont reportées à plus tard (arxiv-1809.04570, §4). Aucune mesure de puissance
  dans hls4ml 2025 (arxiv-2512.01463).
- Ce qui manque : un modèle de puissance validé sur carte, intégré au flot.
- Statut : hypothèse pour l'état actuel (le FINN d'aujourd'hui n'est pas dans le corpus).
- Piste : vérifier la documentation et les publications du FINN actuel.

### NAS matériel-aware ciblant les FPGA
- Constat :
  - absent du survey embarqué arxiv-2411.01431 ;
  - hls4ml ne cite que des prédicteurs de ressources pour des MLP (rule4ml,
    arxiv-2512.01463) ;
  - El Zeinaty et al. décrivent la NAS « hardware-aware » pour la détection (MCUNet,
    MicroNets, ProxylessNAS, et leur propre NAS guidée par LLM sur STM32H7), **uniquement
    pour MCU**. Le FPGA n'est cité qu'en perspective (CFU Playground)
    (2025-el-zeinaty-designing-object-detection-models-tinyml, §6.4.2, §8).
- Statut : hypothèse (absence dans trois papiers). La méthode existe côté MCU ; son
  transfert au FPGA, où la latence dépend du mapping, n'est pas couvert dans le corpus.
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

### Surveys : « embarqué » sans FPGA, ou « FPGA » sans comparaison chiffrée entre plateformes
Reformulé au 3e passage. L'intitulé précédent, « Les FPGA absents des surveys
« embarqué » », était trop fort : 2025-hozhabr le contredit en partie, puisque c'est un
survey dédié au FPGA.
- Constat :
  - surveys « embarqué » où le FPGA est absent ou marginal :
    - arxiv-2411.01431 : ni toolflow ni accélérateur FPGA (fiche « Limites ») ;
    - 2025-el-zeinaty-designing-object-detection-models-tinyml : FPGA cité en perspective
      seulement (§6.1.3, §8) ;
    - 2024-mittal-comprehensive-survey-deep-learning-lightweight : un paragraphe (§4.3.3),
      et des FPS sans plateforme associée (Tables 5-6) ;
    - 2023-shuvo-efficient-acceleration-deep-learning-inference : une sous-section
      (§XI-C1), et des tableaux comparatifs perdus à l'extraction ;
  - surveys dédiés au FPGA, sans comparaison **chiffrée** avec Jetson ou MCU :
    - 2025-hozhabr-survey-real-time-object-detection : comparaison qualitative seulement
      (Table 5), gains face au GPU repris d'auteurs qui ont comparé à des GPU non
      optimisés ;
    - arxiv-2509.04153 et arxiv-1806.01683.
- Ce qui manque : une synthèse **quantitative** qui place FPGA, Jetson et MCU à NPU sur des
  critères communs : même tâche, même mAP, même portée de puissance.
- Statut : étayé (7 surveys). C'est un argument de positionnement pour une thèse, pas un
  verrou technique.
- Piste : citer ce manque dans l'état de l'art du pré-projet. La mesure de référence KV260 /
  Orin / MCU (docs/experiences/kv260-map-sur-cible.md, §8) y répondrait en partie.

### Détection sur MCU et sur petit FPGA : aucune passerelle
- Constat :
  - côté MCU, les détecteurs compressés tiennent en 53 à 511 kB de SRAM, pour 55 à
    789 MMACs et 51 à 75 % de mAP VOC (MCUNetV2-YOLOv3, XiNet-YOLOv7, TinyissimoYOLO), mais
    sans latence ni énergie dans le tableau comparatif
    (2025-el-zeinaty-designing-object-detection-models-tinyml, Table 8) ;
  - côté FPGA, un YOLOv3-tiny élagué à 0,735 GOP (environ 370 MMACs si 1 MAC compte pour
    2 opérations, conversion déduite, entrée 416×416) tourne à 91,65 FPS sur XC7Z035 pour
    12,51 W
    (2023-zhai-fpga-vehicle-detection-tracking-accelerator, Table 8) ;
  - aucun papier du corpus ne fait tourner un même détecteur compressé sur MCU **et** sur
    FPGA ;
  - MCUNetV2 ne donne **ni latence ni énergie** pour la détection (seulement paramètres,
    MACs, pic de SRAM et mAP VOC 20 classes : 64,6 % en 247 kB sur Cortex-M4)
    (arxiv-2110.15352-mcunetv2-memory-efficient-patch-inference, Table 3) ;
  - TinyissimoYOLO donne latence et énergie **sur le MCU seul** :
    - MAX78000 : 5,5 ms et 196 µJ par inférence ;
    - STM32H7A3 : 359 ms ;
    - Apollo4b : 6,1 mJ.
    Mais c'est à 88×88, sur VOC réduit à 3 classes et à 3 objets par image (58,5 %)
    (arxiv-2306.00001-tinyissimoyolo-quantized-low-memory-footprint, §III, Table II) ;
  - les mAP VOC du Tableau 8 de 2025-el-zeinaty ne sont donc pas comparables entre elles
    (20 classes pour MCUNetV2, 3 pour TinyissimoYOLO). La valeur citée pour TinyissimoYOLO
    (56,4 %) ne correspond d'ailleurs à aucune des trois valeurs de la version AICAS 2023 ;
  - ordre de grandeur (déduit, tâches non comparables) : environ 136 mJ par image pour le
    YOLOv3-tiny FPGA de Zhai et al., contre 196 µJ pour TinyissimoYOLO sur MAX78000.
- Ce qui manque : pour un même détecteur (par exemple MCUNetV2-YOLOv3 ou TinyissimoYOLO),
  la frontière latence / énergie / mAP sur MCU (GAP9, STM32N6 avec NPU) et sur petit FPGA
  (Zynq-7020, KV260), avec la même définition de la mAP et la même portée d'énergie (puce).
  On saurait alors à partir de quel budget (résolution, nombre de classes) le FPGA devient
  intéressant face à un MCU doté d'un accélérateur CNN.
- Statut : hypothèse (déduite de 4 fiches ; l'absence de portage FPGA de ces réseaux n'est
  constatée que dans le corpus). Côté MCU, seul TinyissimoYOLO fournit des mesures d'énergie.
- Piste : porter TinyissimoYOLO (environ 29 M MACs, 398 kB de poids, déduit) sur un petit
  FPGA avec FINN ou hls4ml, et mesurer l'énergie par inférence en portée puce. Avant cela,
  chercher un portage existant (`/paper-discover "TinyissimoYOLO FPGA"`, « MCUNet FPGA »).
