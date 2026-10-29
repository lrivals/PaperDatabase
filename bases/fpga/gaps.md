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

Mise à jour du 26/10/2026 (9e passage) : **114 fiches `done` sur 114**, **308 lignes** dans
`benchmarks.csv` (55 papiers). Nouveautés depuis le 8e passage :
- les trois papiers fondateurs YOLO (arxiv-1506.02640, arxiv-1612.08242, arxiv-1804.02767),
  sans ligne de benchmark : ils ne changent aucun gap (baselines GPU Titan X) ;
- l'axe **`failure-prediction`** (8 fiches : arxiv-2603.25499 KGFP, arxiv-1910.04851
  ConfidNet, arxiv-2403.02886, arxiv-1901.09192 SelectiveNet, arxiv-1706.04599,
  arxiv-1906.02530, arxiv-1709.01686 BranchyNet, arxiv-1703.09844 MSDNet), ajouté avec le
  draft de sujet ARCYS (profile.md, 25/10/2026) ;
- hls4ml 2018 (arxiv-1804.06913, 2 lignes, estimations HLS) et l'étude SEU d'un BNN FINN
  sur Ultra96 (arxiv-2404.01757, sans ligne).

Changements de ce passage :
- **section nouvelle** « Prédiction d'échec, sorties anticipées et moniteur sur cible »,
  **6 gaps** au croisement du sujet ARCYS : 5 étayés dans le corpus (dont 3 restent en
  hypothèse pour la littérature) et 1 en hypothèse (fiabilité du moniteur) ;
- **l'axe `timing-analysis` (base.json) ne contient aucun papier** : tout gap temporel
  repose sur des remarques de fiches d'autres axes. Il reste donc en hypothèse pour la
  littérature (corpus vide, pas preuve d'absence) ;
- **nuancés ou étendus** : « Aucun détecteur d'objets quantifié… » (KGFP surveille un
  YOLOv8, mais sur GPU), « Fiabilité SEU… » (injection CRAM + FF sur FINN, arxiv-2404.01757),
  « Critère de criticité… » (étiquette « au moins une personne manquée » de KGFP),
  « Moniteurs d'exécution… » (+7 fiches), « Argument FPGA contre GPU… » (hls4ml,
  arxiv-1905.04223 §7.4), « Détecteurs de personnes quantifiés… » (première métrique de
  personnes manquées, hors FPGA), « Estimation de puissance et de latence dans les
  toolflows » (écart HLS / implémentation de hls4ml) ;
- **aucun gap supprimé** : aucune des 13 fiches nouvelles n'en contredit un ;
- au total, **42 gaps**.

Réserve propre à ce passage : les 8 fiches `failure-prediction` sont de l'apprentissage
automatique **logiciel** (aucune plateforme, aucune ligne de benchmark), 7 sur 8 en
classification. Les travaux de prédiction de faux négatifs de détecteur cités par KGFP
(§2.2, chunk 2603.25499#003.0-1) ne sont pas dans la base : Yang et al. 2021 (Sensors
21(8):2819, « Introspective false negative prediction for black-box object detectors in
autonomous driving »), Yatbaz et al. (moniteur de couches précoces de détecteurs 3D),
DECIDER (Subramanyam et al., ECCV), Torpmann-Hagen et al. 2025 (IEEE Access 13). Références
tirées de la bibliographie de KGFP, non vérifiées.

Mise à jour du 01/10/2026 (8e passage) : **101 fiches `done` sur 101**, **299 lignes** dans
`benchmarks.csv` (54 papiers, dont **216 lignes FPGA** issues de 44 papiers). Soixante
fiches ajoutées depuis le 7e passage, dont les 29 de l'axe `safety-certification` et les 5 de
`person-detection`, ajoutés au profil le 29/09/2026 avec le thème de thèse.

Changements de ce passage :
- **deux sections nouvelles**, 13 gaps :
  - « Sûreté, fiabilité et certification » : 9 gaps, tous étayés dans le corpus (la
    correspondance avec les normes industrielles reste une hypothèse pour la
    littérature) ;
  - « Détection de personnes en milieu industriel » : 4 gaps, dont 3 étayés ;
- au total, **36 gaps**, dont 29 étayés et 7 en hypothèse (ou étayés seulement en partie) ;
- **supprimé** : « Autoencodeur complet (encodeur + décodeur) sur une petite FPGA ». Il est
  contredit par arxiv-2407.17647 : CAE complet, score par erreur de reconstruction, sur DPU
  de ZCU104 (§III-D, §IV). Il l'est aussi, pour la compression, par arxiv-2503.04832
  (encodeur et décodeur sur ZCU102, Table X). Ce qui en reste, le coût des déconvolutions
  sur une puce plus petite, passe dans le premier gap des autoencodeurs ;
- **reformulés**, car une fiche contredit leur forme du 7e passage :
  - « Apprentissage embarqué par rétropropagation sur FPGA ». EF-Train
    (arxiv-2202.10935, §3) et Chameleon (2024-aggarwal, §IV) font bien FP / BP / WU sur
    ZCU102. Le gap devient : rétropropagation lente, en flottant, énergie non mesurée ;
  - « CL sur FPGA : précision faible et énergie estimée ». SLDA sur ZCU102 atteint 78,79 %
    sur CoRE50 (2021-piyasena-accelerating, Table V). Le gap devient : énergie de portée non
    précisée ;
- **nuancés** par de nouveaux contre-exemples partiels :
  - AE d'anomalies visuelles sur FPGA (arxiv-2407.17647) ;
  - précision sur cible : deux détecteurs mesurés sur la carte (arxiv-2304.11580,
    arxiv-2607.13106) ;
  - dataflow quantifié sur SoC : YOLOv3-tiny FINN sur Zynq-7020 (arxiv-2609.24757) ;
  - protocole de mesure : arxiv-2304.11580 et MLPerf Tiny (arxiv-2206.11791) ;
  - comparaison hls4ml / FINN sur une même carte (arxiv-2206.11791) ;
  - CL limité à la classification : RILOD (arxiv-1904.00781) et arxiv-2409.01872 traitent
    la détection, mais sans FPGA ;
  - petits objets (SkyNet, arxiv-1909.09709) ;
  - NAS sur FPGA (arxiv-2206.11791, arxiv-1909.09709) ;
- **étendus** : puissance (recompte), métriques flatteuses, code publié, post-traitement,
  réseaux qui ne tiennent pas on-chip, baseline Jetson, surveys, passerelle MCU ↔ FPGA.

**Réserve générale** : le corpus reste petit et biaisé par la bibliographie de départ.
- Effectifs par axe (fiches `done`, un papier pouvant porter plusieurs axes) :
  - `platforms` 44 ;
  - `safety-certification` 29 ;
  - `toolflows` 23 ;
  - `surveys` 18 ;
  - `yolo-fpga` 18 ;
  - `autoencoder-fpga` 15 ;
  - `continual-learning` 15, dont 7 sans FPGA ;
  - `person-detection` 5. C'est l'axe le plus mince : un seul papier y mesure un
    détecteur sur FPGA (arxiv-2607.13106, preprint).
- `benchmarks.csv` est déséquilibré :
  - 5 papiers fournissent 90 lignes sur 299 : 2022-feng 24 (Jetson et VPU, sans mAP),
    arxiv-2607.13106 23 (preprint), arxiv-2409.16808 15, arxiv-2502.15737 14 et SATAY 14 ;
  - les 29 fiches de sûreté ne donnent que **4 lignes** (2020-libano 2, arxiv-1912.07394 1,
    arxiv-2406.12362 1). Le schéma n'a pas de colonne pour les métriques de fiabilité (FIT,
    AVF, section efficace, taux de SDC) ni pour le coût d'un moniteur. L'axe sûreté est
    donc invisible dans le CSV (déduit) ;
  - les précisions de détection de personnes sur GPU sont exclues du CSV. La suggestion de
    profil correspondante est reportée (profile.md).
- Confiance : 140 lignes sur 299 sont en `medium` et 1 en `low` (arxiv-2301.07050). Les
  `medium` viennent souvent de tableaux reconstruits par Docling ou PyMuPDF : 15 lignes pour
  arxiv-2409.16808, 14 pour SATAY, 7 pour 2021-piyasena-fpga, 6 chacun pour
  arxiv-2502.15737, 2024-zhang, arxiv-2403.18921, arxiv-2503.04832 et arxiv-2609.24757.
- Preprints non relus parmi les sources nouvelles les plus citées ici : arxiv-2607.13106,
  arxiv-2609.24757, arxiv-2503.04832, arxiv-2403.18921, arxiv-2202.10935,
  arxiv-2304.06052, arxiv-2409.01872, arxiv-1904.00781.
- Toutes les fiches sont faites. Les prochains apports viendront de nouveaux papiers
  (`/paper-discover`).
- Un gap qui ne repose que sur l'absence de papiers dans la base reste une `hypothèse`. Un
  gap `étayé` est constaté dans les fiches, ce qui ne prouve pas son absence dans la
  littérature. C'est particulièrement vrai pour la sûreté : aucun texte normatif (IEC 61508,
  ISO 13849, ISO/IEC TR 5469, ISO 10218) n'est dans la base, seulement des documents qui
  les citent.

Passages précédents (résumé) :
- 2e au 5e : Feng, Magalhães, El Zeinaty, Zhai, MCUNetV2, TinyissimoYOLO, AE au LHC,
  surveys Shuvo / Mittal / Hozhabr, Rey, Alqahtani ;
- 6e : SATAY, Que 2024 (VAE), hls4ml CNN, F-LIC, Φ-Sat-2 ;
- 7e (26/09/2026, 41 fiches, 172 lignes) : AE d'images à petite échelle (Manjunath,
  2301.07050, Malviya), ONLAD, REQ-YOLO, DAC-SDC, FCMP, Campos, QLR-CL ; 4 gaps ajoutés
  (AE complet, rétropropagation sur FPGA, dérive, petits objets).

### Couverture croisée de `benchmarks.csv` (8e passage)

Lignes par tâche et classe de plateforme. Le classement est fait par mots-clés des colonnes
`task` et `platform` et reste donc approximatif.
- « Petite FPGA » regroupe Zynq-7000, Zynq UltraScale+ (ZCU102 et ZCU104 compris), Kria,
  PYNQ, Ultra96, Artix et PolarFire.
- « Grosse FPGA » regroupe Virtex, Kintex, Alveo, AWS F1, ainsi que la cible n/r de hls4ml.
- « CL / entraînement » inclut l'entraînement embarqué hors CL (EF-Train, 256 KB).

| Tâche | Petite FPGA / SoC | Grosse FPGA | Jetson | MCU | ASIC | Autre | Total |
|---|---|---|---|---|---|---|---|
| Détection (dont suivi, OBB) | 61 | 26 | 47 | 5 | 0 | 13 (CPU, GPU, RPi, VPU, Hailo) | 152 |
| Classification | 30 | 32 | 0 | 2 | 0 | 0 | 64 |
| Anomalie (AE, OS-ELM) | 7 | 9 | 2 | 0 | 0 | 0 | 18 |
| Autoencodeur (autre usage) | 7 | 3 | 0 | 0 | 1 | 0 | 11 |
| Compression d'image | 6 | 4 | 0 | 0 | 0 | 3 (VPU, GPU, CPU) | 13 |
| CL / entraînement | 26 | 0 | 2 | 5 | 3 | 0 | 36 |
| Autre (segmentation, action) | 2 | 3 | 0 | 0 | 0 | 0 | 5 |

Évolution depuis le 7e passage :
- Compression d'image × petite FPGA passe de 0 à 6 lignes (arxiv-2503.04832, ZCU102) ;
- Anomalie × Jetson passe de 0 à 2 (arxiv-2407.17647, Xavier NX) ;
- CL × Jetson passe de 0 à 2 (2024-aggarwal, Jetson Nano) ;
- CL × petite FPGA passe de 3 à 26 (Piyasena ×2, Chameleon, EF-Train).

Cases vides ou quasi vides :
- **Détection × apprentissage continu** : 0 ligne, toutes plateformes confondues. RILOD et
  arxiv-2409.01872 n'ont pas de ligne (aucune mesure exploitable sur cible) ;
- **Anomalie × MCU** : 0 ligne ;
- **FPGA × MCU dans un même papier** : aucun papier ;
- **Orin × FPGA dans un même papier** : aucun. Les seules lignes Orin viennent de
  arxiv-2409.16808 et arxiv-2502.15737, sans FPGA. Quatre papiers comparent une FPGA à un
  Jetson plus ancien : arxiv-1909.09709 (TX2), arxiv-2304.11580 (AGX Xavier),
  arxiv-2407.17647 (Xavier NX) et 2024-aggarwal (Nano) ;
- **Sûreté** : aucune ligne de détection issue d'un papier de fiabilité ou de vérification ;
- **Personnes** : 6 lignes de précision sur un jeu de personnes (arxiv-2607.13106,
  Table II, CPU contre FPGA INT8 non distingués dans le CSV) et 2 lignes de débit sur la
  vidéo PETS2009 avec une puissance estimée par Vivado.

Toolflow × tâche, sur les 216 lignes FPGA :
- détection (87) : HLS maison 31, Vitis AI 29, SATAY 14, FINN 9, RTL 4. **hls4ml : 0** ;
- classification (62) : FINN 35, hls4ml 20, autres 7 ;
- anomalie (16) : hls4ml 9, HLS maison 6, Vitis AI 1 ;
- AE autre (10) : RTL 5, hls4ml 5 ;
- compression d'image (10) : Vitis AI 6, n/r 4 ;
- CL / entraînement (26) : HLS maison 21, Vitis AI + HLS 4, RTL 1 ;
- Vitis AI n'avait que 2 lignes au 7e passage ; il en a 38 maintenant, dont 23 de
  arxiv-2607.13106.

Métriques absentes, sur les 216 lignes FPGA (`n/r` ou vide) :

| Colonne | FPS | latence | puissance | précision | LUT | DSP | BRAM |
|---|---|---|---|---|---|---|---|
| n/r | 132 | 88 | 101 | 48 | 89 | 99 | 95 |

Les 87 lignes FPGA de détection emploient **15 libellés de précision différents** :
mAP@0.5:0.95, mAP50 COCO, mAP VOC, AP UA-DETRAC à une classe, IoU DAC-SDC, « accuracy »
(TP + TN)/…, etc. Seules 32 lignes portent une mAP COCO ou une mAP@0.5:0.95.

Parmi les 7 lignes « anomalie » sur petite FPGA, une seule porte sur des images 2D réelles
(arxiv-2407.17647, hyperspectral). Les autres portent sur :
- des signaux de calorimètre (arxiv-2602.15751) ;
- des vibrations (2022-malviya) ;
- de l'audio (arxiv-2206.11791) ;
- des ondes gravitationnelles (2024-que) ;
- des données tabulaires (2019-tsukada).

## Autoencodeurs

### Autoencodeurs sur FPGA appliqués aux images (détection d'anomalies visuelles)
- Constat (passages 1 à 6) :
  - AE du corpus sur signaux 1D ou données de physique : AE dense sur PolarFire
    (arxiv-2602.15751, Table 1), anomalies sur jets (arxiv-2103.05579, Fig. 3), AE et VAE
    au trigger du LHC sur données tabulaires 19 × 3, dont le seul CNN AE dépasse le budget
    (47 % des LUT d'un VU9P pour une entrée 20 × 3) (arxiv-2108.03986, §III, Table III) ;
  - hls4ml 2025 ne publie aucun CAE d'images de taille réaliste (arxiv-2512.01463, §11) ;
  - **F-LIC** : compression apprise (hyper-prior, donc VAE) sur images 720p et 1080p, à 40,69
    et 19,15 fps en encodage, en Fix8, sur VCU118, codage entropique sur l'hôte
    (2022-sun-f-lic-fpga-learned-image, Fig. 6, Fig. 7) ;
  - VAE complet sur séries temporelles d'ondes gravitationnelles
    (2024-que-low-latency-variational-autoencoder-fpgas, §IV-A) ;
  - Φ-Sat-2 compresse des images par CAE sur une **VPU**, pas sur FPGA
    (2023-guerrisi-artificial-intelligence-board-image-compression, §III-C).
- Constat (7e passage). Des AE d'images sur petite FPGA, à petite échelle et sans usage
  d'anomalie visuelle :
  - encodeur ternaire 120 × 120 sur Artix-7
    (2021-manjunath-energy-efficient-edgeai-autoencoder-accelerator, §VI, Table 5) ;
  - CAE de débruitage MNIST sur XCZU7EV (arxiv-2301.07050, §IV-B, Table II) ;
  - CAE d'anomalies sur scalogrammes de vibrations
    (2022-malviya-edge-compatible-convolutional-autoencoder-implemented, §II-B) ;
  - ONLAD (2019-tsukada, Table 2), SSAE de Coutinho (2019-coutinho, §III-A), ECON-AE
    (2024-campos, §7).
- Constat (8e passage, 7 fiches) :
  - **contre-exemple partiel : arxiv-2407.17647**. Un CAE de 2,95 M de paramètres, sur
    entrée 144 × 144, détecte des artefacts dans des images hyperspectrales par seuil sur
    l'erreur de reconstruction. Il tourne en INT8 sur le DPU B4096 d'une ZCU104 : 4,0 ms,
    21,52 mJ par inférence, 5,38 W sur les rails PMBus (§IV-B, Table VI) ;
  - ses limites : le seuil est choisi sur les données d'évaluation (§III-C) ; le jeu est très
    déséquilibré (837 anomalies pour 79 à 89 normales, Table IV) ; la PTQ seule donne
    F1 = 0, et il faut un fine-tuning (Table III) ;
  - **LIC sur SoC** : CAE + hyperprior distillé, sur 3 DPU de ZCU102, à 43,63 FPS en
    encodage et 30,5 en décodage. GDN est implanté comme opérateur personnalisé
    (arxiv-2503.04832, §III-B, Table VII, Table X ; preprint) ;
  - quantification de LIC seulement simulée, sans mesure FPGA (arxiv-2511.17135, Table I) ;
  - VAE de compression et de détection de défauts capteur, hls4ml, 105 valeurs en entrée
    (arxiv-2411.01118, §3.1) ;
  - le survey 2023-cui (MVTec AD, AUROC ~96-99, Table 10) ne donne aucun coût matériel. Les
    méthodes à banque de patchs y sont coûteuses en mémoire (§IV)
    (2023-cui-survey-unsupervised-anomaly-detection-algorithms) ;
  - MLPerf Tiny : l'« anomaly detection » est un AE dense sur spectrogrammes audio
    (arxiv-2206.11791, Table 5).
- Bilan des 15 fiches `autoencoder-fpga` :
  - compression d'images : oui, sur grosse FPGA (F-LIC), sur SoC via DPU (arxiv-2503.04832)
    ou sur VPU (Φ-Sat-2) ;
  - **anomalie d'images sur FPGA embarquée : un seul cas**, hyperspectral, avec seuil réglé
    sur le test (arxiv-2407.17647) ;
  - anomalie visuelle sur images RGB réelles ou vidéo (MVTec, scène industrielle) : aucune.
- Ce qui manque :
  - un CAE ou VAE d'anomalie visuelle sur images RGB réelles, évalué sur un benchmark
    standard (MVTec AD) avec seuil fixé hors du test, AUROC mesurée sur la carte ;
  - la puissance de carte ;
  - sur une puce plus petite que la ZCU104 (KV260) ou en dataflow (hls4ml, FINN), le coût
    des déconvolutions et de l'upsampling mesuré. Cette partie reprend le gap supprimé
    « AE complet sur petite FPGA ».
- Statut : étayé (15 fiches) pour l'anomalie visuelle RGB sur FPGA embarquée. Nuancé par
  arxiv-2407.17647, contre-exemple partiel (hyperspectral, DPU, protocole de seuil faible).
- Piste :
  - reprendre la chaîne d'arxiv-2407.17647 (CAE INT8, Vitis AI, fine-tuning) sur MVTec AD
    et sur KV260 ;
  - comparer au score D_KL d'arxiv-2108.03986 (§IV) et à un encodeur seul. Le CAE servirait
    aussi de moniteur OOD du YOLO (voir la section Sûreté).

### Compression apprise embarquée complète (codage entropique compris)
- Constat :
  - F-LIC laisse le range coding sur le PC hôte (2022-sun-f-lic-fpga-learned-image, Fig. 1) ;
  - Φ-Sat-2 n'a pas de codage entropique, avec un taux ×8 fixe, sur VPU
    (2023-guerrisi-artificial-intelligence-board-image-compression, §II-A, §III-A) ;
  - ECON-AE compresse sans codage entropique (2024-campos-end-end-codesign-hessian-aware, §7) ;
  - (8e passage) arxiv-2503.04832 donne les FPS des transformées sur ZCU102, mais la fiche
    ne dit pas où se fait le codage entropique. Son énergie (2,88 J/frame à 43,6 FPS)
    implique ~125 W, ce qui est incompatible avec une ZCU102 : la méthode de mesure n'est
    pas décrite (déduit par la fiche, Table VII).
- Ce qui manque : une chaîne complète (transformées + codage entropique) sur plateforme
  embarquée à faible consommation, avec l'énergie par image mesurée.
- Statut : hypothèse (4 fiches).
- Piste : lire le codec JETCAS 2024 (DOI 10.1109/jetcas.2024.3386328, non ingéré).

### VAE complet en matériel pour un espace latent de grande dimension
- Constat : le seul VAE qui échantillonne en matériel a un latent de dimension 1 ; une
  unité avec son GRNG prend 113 DSP (2024-que-low-latency-variational-autoencoder-fpgas,
  §IV-B, Table III). Les autres VAE évitent l'échantillonnage (arxiv-2108.03986, §IV ;
  arxiv-2411.01118 utilise une KLD clipée comme score).
- Ce qui manque : le coût d'un GRNG parallèle pour un latent d'image (centaines à milliers
  de dimensions).
- Statut : hypothèse (2 fiches). Inchangé sur le fond.
- Piste : extrapoler le coût du GRNG de Que 2024 et le comparer au score D_KL déterministe.

## YOLO et détection sur FPGA

### Pas de protocole de mesure commun pour YOLO sur FPGA
- Constat (passages 1 à 7, résumé ; détail dans les fiches citées) :
  - 2022-feng (§4.1), arxiv-2211.11647 (§2.5), 2023-zhai (Table 8), SATAY (Tables III-IV),
    arxiv-1809.04570 (Table 5), arxiv-2507.18174 (Table I) ;
  - DAC-SDC est un protocole commun, mais en IoU mono-objet
    (2021-xu-dac-sdc-low-power-object, §2.3) ;
  - REQ-YOLO donne une latence égale à la somme des couches
    (2019-ding-req-yolo-resource-aware-efficient, §6.2).
- Constat (8e passage, 13 fiches de plus) :
  - **arxiv-2304.11580 est un contre-exemple partiel**. Son cadre mesure la mAP sur la
    cible, avec un hôte séparé. Il compare YOLOv4 sur ZCU104 (DPU) et sur AGX Xavier
    (TensorRT FP32 / FP16 / INT8), puissance de carte au multimètre, repos déduit (§4.1,
    Table 1). Ses limites :
    - un modèle, deux cartes ;
    - 416 contre 512 ;
    - pré- et post-traitement optimisés pour le DPU, en numpy sur le Jetson (Table 2) ;
    - moyennes sur 6 passes, sans pire cas ;
  - MLPerf Tiny avec EEMBC EnergyRunner / Joulescope, sur Pynq-Z2 et Arty A7, mais en
    classification et en AD audio (arxiv-2206.11791, Table 5) ;
  - les autres papiers de détection restent hétérogènes :
    - 2024-yan (YOLOv5s, mAP VOC, 12,3 W sans méthode, Table 3) ;
    - 2024-zhang (GOP/s, FPS n/r, Table 3) ;
    - 2025-kim (12,64 s par image, mAP n/r) ;
    - 2026-fata (« accuracy » (TP + TN)/… au lieu d'une mAP, Eq. 4) ;
    - arxiv-1909.09709 (IoU, batch 4) ;
    - arxiv-2006.08357 (AP50 à 256 × 256, incohérences résumé / tables) ;
    - arxiv-2609.24757 (lot de 100 images, seuils fixés par les auteurs) ;
    - arxiv-2607.13106 (FPS mesurés sur une autre vidéo que la précision) ;
  - 2025-hozhabr propose le pixel throughput et distingue temps réel dur et mou (§II-C2),
    mais ne normalise ni la mAP ni la portée de puissance ;
  - **15 libellés de précision** pour 87 lignes FPGA de détection (couverture croisée
    ci-dessus).
- Ce qui manque :
  - mAP sur le split officiel, variante et résolution déclarées ;
  - FPS et latence à batch 1 de bout en bout, **avec pire cas et gigue** ;
  - puissance de carte au wattmètre et de puce par télémétrie ;
  - le tout pour une même carte récente (KV260) face à un Orin.
- Statut : étayé (24 fiches). arxiv-2304.11580 et DAC-SDC montrent que le protocole est
  faisable ; aucun travail ne le réunit en entier.
- Piste :
  - partir du cadre d'arxiv-2304.11580 (hôte séparé, mAP sur cible) et du protocole
    d'arxiv-2409.16808 (repos soustrait, 3 répétitions) ;
  - y ajouter P_chip / P_wall à la manière de FINN (arxiv-1612.07119, §5.1) et une
    distribution de latence (p99, max).

### Détection en dataflow quantifié sur SoC FPGA embarqué
Reformulé au 6e passage (contredit dans sa forme générale par SATAY), nuancé au 8e.
- Constat (passages 1 à 7) :
  - SATAY sur ZCU104 avec YOLOv5n seulement, tous les poids on-chip
    (2023-montgomerie-corcoran-satay-streaming-architecture-toolflow-accelerating, §IV-C) ;
  - FINN-R : Tincy YOLO en offload (arxiv-1809.04570, Table 5) ;
  - REQ-YOLO sur Virtex-7 (2019-ding, Table 2) ;
  - DAC-SDC sur Zynq-7020 (2021-xu, §4.2) ;
  - aucun toolflow ne visait la détection en 2018 (2018-venieris, §2.6).
- Constat (8e passage) :
  - **arxiv-2609.24757 (preprint)** : YOLOv3-tiny allégé en **w2a4 via Brevitas et FINN** sur
    PYNQ-Z1 (XC7Z020). Il fait 35,66 FPS, 2,91 W au rail 12 V, 0,594 mAP@0,5 VOC et 0,492 sur
    COCO filtré, et reste à ≈ 0,006 de mAP du flottant avec QAT, contre ≈ 0,17 en PTQ
    (§IV-B, §V-VI). Ses limites :
    - classes de véhicules seulement ;
    - ressources n/r (Table I non extraite) ;
    - lot de 100 images ;
  - SMOF (fpgaConvNet + éviction off-chip) : YOLOv8n à 184 fps, mais sur VCU118, pas sur SoC
    (arxiv-2403.18921, Table V ; preprint) ;
  - CoDeNet : détecteur sans NMS en 4 / 8 bits sur Ultra96, 4,6 à 9,3 fps en 512 × 512
    (arxiv-2006.08357, Tables 3 et 5) ;
  - côté DPU, sans dataflow : YOLOv8 / v11 / v26 nano sur ZCU104 (arxiv-2607.13106),
    YOLOv3-Tiny élagué sur KV260, 24,3 FPS (2026-fata, Table 8). Côté HLS maison : YOLOv5s
    INT4 sur ZCU102 (2024-yan).
- Ce qui manque : un YOLO v5 / v8 en dataflow quantifié (SATAY, FINN ou hls4ml) sur **KV260
  ou Zynq-7020**, en W4 à W8, comparé à Vitis AI sur la même carte, sur classe « personne ».
- Statut : étayé (13 fiches). Nuancé : le dataflow quantifié existe sur Zynq-7020 pour un
  YOLOv3-tiny allégé (arxiv-2609.24757), pas pour un YOLO récent ni face au DPU.
- Piste :
  - reproduire arxiv-2609.24757 (FINN, w2a4) puis SATAY sur KV260, face au DPU ;
  - appliquer l'empaquetage FCMP (arxiv-2011.07317) et l'éviction SMOF (arxiv-2403.18921).

### Petits objets vus de drone sur FPGA
Nouveau au 7e passage, nuancé au 8e.
- Constat :
  - DAC-SDC : objets de 1 à 2 % de l'image ; les FPGA redimensionnent sur l'ARM
    (2021-xu-dac-sdc-low-power-object, §3, §4.2, §5.2.3) ;
  - (8e passage) SkyNet est conçu en partie pour les petits objets : 31 % des boîtes font
    moins de 1 % de l'image (§5.2), d'où un bypass avec space-to-depth. L'effet de la
    quantification n'est donné qu'en IoU globale, pas par taille d'objet
    (arxiv-1909.09709, Table 7).
- Ce qui manque : l'effet de la résolution, du redimensionnement et de la quantification
  mesuré **par taille d'objet** sur FPGA. C'est aussi le cas des personnes éloignées d'une
  caméra fixe (déduit).
- Statut : étayé (2 fiches) pour l'absence de mesure par taille ; hypothèse pour le reste.
- Piste : métriques COCO AP_small sur la cible, dans l'expérience KV260.

### Interaction PS-PL et post-traitement sur SoC FPGA
- Constat (passages 1 à 7) :
  - de 195 à 24 FPS à cause d'un suivi en Python sur le PS (arxiv-2509.04153, §VI-C) ;
  - NMS et Deepsort sur l'ARM (2023-zhai, §3.3) ;
  - pré- et post-traitement exclus (arxiv-2211.11647, §2.4) ;
  - SATAY (§III-A) ; REQ-YOLO (Table 1) ; Zhang 2015 (§2.1).
- Constat (8e passage) :
  - **NMS en matériel** : 845 boîtes en 0,38 ms. Latence de bout en bout de 15,2 ms pour
    YOLOv3-Tiny, mais sur Kintex-7 avec MicroBlaze, sans SoC ARM
    (2024-zhang-end-end-acceleration-yolo-object, Table 2, Table 5) ;
  - débit de bout en bout limité par le post-traitement CPU : 34,05 FPS E2E pour YOLOv26n
    sur ZCU104 (arxiv-2607.13106, §IV-C) ;
  - post-traitement ARM ≈ 4,7 ms (arxiv-2609.24757) ;
  - sur Jetson, le post-traitement numpy pèse plus que l'inférence (arxiv-2304.11580,
    Table 2) ;
  - RTT ≈ 2-3 fois le temps d'inférence seul (arxiv-2502.15737, Table 5, Fig. 4) ;
  - détecteur sans NMS (CenterNet) : première couche sur l'ARM (arxiv-2006.08357) ;
  - gestion temps réel PS-PL (RTOS, priorités, WCET) non traitée dans la littérature selon
    arxiv-2509.04153 (§III-B) ;
  - concaténation et détection sur le PS (2025-kim).
- Ce qui manque : une mesure de bout en bout (capture → PL → post-traitement → sortie) sur
  SoC, avec un partitionnement PS / PL justifié et une borne de latence.
- Statut : étayé (14 fiches).
- Piste : porter le post-traitement matériel de 2024-zhang (8 893 LUT, Table 2) sur KV260 à
  côté du DPU, et mesurer le gain de latence et de gigue.

## Mesure et comparaison

### Précision non vérifiée sur la cible après compilation et quantification
- Constat (passages 1 à 7) :
  - OpenVINO fait tomber YOLOv3-tiny à 0 % de confiance (2022-feng, Table 3) ;
  - la PTQ INT8 de TensorRT coûte de 6,4 à 12,3 points de mAP50-95, alors que les auteurs
    concluent « sans perte significative » (arxiv-2502.15737, Table 4, §6) ;
  - AP FP32 = INT16 (2023-zhai, Table 8) ; mAP identiques sur deux Jetson (arxiv-2409.16808) ;
  - simulation ONNX Runtime (SATAY, §IV-A) ; C++ généré (arxiv-2101.05108, §8) ;
  - ONLAD, REQ-YOLO, Campos ;
  - contre-exemples sur petits modèles : Malviya (−3,8 points) et Coutinho.
- Constat (8e passage) :
  - **deux détecteurs mesurés sur la carte, contre-exemples partiels** :
    - arxiv-2304.11580 : le Vitis AI Quantizer fait perdre 2,2 points de mAP sur YOLOv4, la
      compilation DPU en retire encore. Tous les modèles TensorRT dépassent les modèles
      Vitis AI (37,5 contre 38,6 en INT8) (§4.3, Table 1) ;
    - arxiv-2607.13106 (preprint) : mAP@0.5:0.95 sur CPU contre FPGA INT8, avec des écarts
      **imprévisibles**. YOLOv11n perd 2 points sur VOC ; YOLOv8n passe de 0,60 à 0,45 sur
      VOC et de 0,64 à 0,34 sur KITTI. Les modifications pour le DPU (ReLU, attention
      approchée) coûtent ≈ 3 points de plus (Table I, Table II) ;
  - autres pertes mesurées :
    - AE INT8 en PTQ seule, F1 = 0 ; il faut un fine-tuning (arxiv-2407.17647, Table III) ;
    - SkyNet, IoU 0,741 → 0,727 en FM9/W11 (arxiv-1909.09709, Table 7) ;
    - YOLOv8n en bfp8 : 35,10 contre 37,10 (arxiv-2403.18921, Table III) ;
  - non mesurée ou non comparable :
    - 2026-fata (pas de baseline FP32, « accuracy » mal définie) ;
    - arxiv-2609.24757 (écart QAT / flottant du modèle final non rapporté) ;
    - 2024-yan (−1,5 point VOC, sans dire si la mesure est faite sur carte).
- Ce qui manque : la mAP mesurée **sur la cible**, étape par étape (quantification,
  compilation, modifications d'opérateurs, post-traitement), pour un YOLO récent sur
  KV260. Il faudrait aussi expliquer les écarts imprévisibles d'arxiv-2607.13106.
- Statut : étayé (20 fiches). Nuancé : deux mesures sur carte de détecteurs existent
  désormais, et elles confirment des pertes de 1 à 30 points selon le modèle et le jeu.
  C'est aussi un problème de certification : voir « Chaîne de preuve d'équivalence ».
- Piste : évaluer la mAP COCO val sur la carte, sorties du DPU relues et NMS compris, face
  au modèle flottant et au modèle quantifié simulé. Cela reste le gap le plus directement
  exploitable.

### Pas de baseline GPU / Jetson mesurée dans les mêmes conditions
- Constat (passages 1 à 7) :
  - fpgaConvNet face à un Tegra X1 bridé (arxiv-1711.08740, §3.1) ;
  - Feng sans TensorRT ;
  - Rey et Alqahtani sur Orin, incomplets (arxiv-2502.15737, arxiv-2409.16808) ;
  - SATAY et REQ-YOLO face au TX2 ;
  - DAC-SDC (2018).
- Constat (8e passage) :
  - **arxiv-2304.11580** : même YOLOv4, ZCU104 contre AGX Xavier (TensorRT INT8). Le Jetson
    est plus rapide (22,0 contre 54,42 ms) et a une meilleure mAP ; FPS/W 2,05 contre 1,31
    (Table 1). Ce sont de grosses cartes de développement, pas un Orin ;
  - arxiv-2407.17647 : ZCU104 (DPU) contre Xavier NX en INT8, bridé à 10 W, avec des
    portées différentes (PMBus contre jtop) (Table VI) ;
  - SkyNet : même modèle sur TX2 et Ultra96, mesuré par les organisateurs de DAC-SDC
    (arxiv-1909.09709, Tables 5-6) ;
  - Chameleon : ZCU102 à 413 ms par image d'entraînement contre 33 ms sur Jetson Nano,
    mais batch 1 contre batch 8 (2024-aggarwal, Table VI) ;
  - baselines faibles ou reprises : Jetson Nano en FP32 (2024-zhang, §5.3) ; CPU / GPU
    repris de [18] (2024-yan, Table 3) ; GPU de bureau (2026-fata, Table 10) ; aucune
    (2025-kim, arxiv-2609.24757, arxiv-2607.13106, arxiv-2403.18921).
- Ce qui manque : même modèle, même précision numérique, même batch, même méthode de
  puissance, sur FPGA embarquée **et Jetson Orin**.
- Statut : étayé (27 fiches). Partiellement comblé (arxiv-2304.11580, AGX Xavier). Aucune
  source ne compare un Orin à une FPGA embarquée (couverture croisée).
- Piste : le volet Orin Nano de l'expérience de référence, sur le modèle
  d'arxiv-2304.11580.

### Puissance : puce contre carte, estimée contre mesurée
- Constat (recompte du 8e passage, 299 lignes dont 216 FPGA) :
  - lignes FPGA :
    - **46 `board`** (9 papiers) : 2024-zhang 10, FINN 8, FINN-R 8, Elastic-DF 8,
      arxiv-2609.24757 6, arxiv-2304.11580 3, Zhang 2015, ONLAD et CoDeNet 1 chacun ;
    - **1 `chip`** : arxiv-2407.17647, rails PMBus de la ZCU104 ;
    - 52 `unspecified` ;
    - 16 `estimated` : EF-Train 6, Manjunath 4, ImageHD 3, arxiv-2607.13106 2, Que 2024 1 ;
    - **101 sans puissance** (`n/r`) ;
  - hors FPGA, les lignes `chip` viennent de Jetson Orin (arxiv-2502.15737, 12), du RPi 5 et
    de VEGA (arxiv-2110.10486).
- Nouvelles portées non comparables (8e passage) :
  - 2024-zhang donne **les deux** sur la même carte (7,8 W puce estimée par Vivado, 12,3 W
    carte au wattmètre, KC705, Table 3). C'est la seule paire puce / carte FPGA du corpus,
    mais la puce est estimée ;
  - puissance relative (moins le repos) donnée dans la fiche d'arxiv-2304.11580 (§4.1), sans
    colonne `board-dynamic` dans le CSV ;
  - « 3x moins de puissance » d'arxiv-2607.13106 : estimation Vivado comparée à SATAY ;
  - Chameleon : énergie par image sans méthode ; Piyasena : rails de la carte, portée non
    dite ; EF-Train : rapport Vivado ;
  - 2,88 J/frame physiquement incompatible avec une ZCU102 (arxiv-2503.04832, Table VII).
- Ce qui manque : `chip` **mesurée** et `board` sur la même carte récente (Kria, Versal).
- Statut : étayé (40 fiches + `benchmarks.csv`). Amélioré mais non résolu : les lignes
  `board` passent de 18 à 46, et la seule ligne FPGA `chip` mesurée est sur ZCU104.
- Piste : dans l'expérience KV260, relever la télémétrie de la puce, le wattmètre de carte
  et la puissance au repos.

### Métriques flatteuses et comparaisons biaisées
Étendu aux 7e et 8e passages.
- Constat (passages 1 à 7) :
  - latence amortie (2024-que, §IV-E) ; GOP/s/DSP (SATAY, Table III) ;
  - GOPS/W dynamiques (2023-zhai) ; « mean confidence » (2022-feng) ;
  - GOPS projetés (2019-coutinho, Tables 16-17) ; tableau incohérent (arxiv-2301.07050) ;
  - TDP (2015-zhang) ; 4 W supposés (arxiv-2110.10486) ; REQ-YOLO.
- Constat (8e passage) :
  - « +29 % vs Vitis AI » = GOPS/DSP face à un YOLOv3 d'un autre travail, pas une mesure
    sur la même carte (2024-yan, Table 2) ;
  - « −26 % FF, −15 % DSP » face à des designs bien plus rapides, avec un autre modèle
    (2025-kim, Table 9) ;
  - « 70x / 37x » face à un CPU et un GPU de bureau, sans portée de puissance (2026-fata,
    Table 10) ;
  - ImageHD : gains ×258-383 qui mélangent une estimation FPGA et des mesures CPU / GPU
    (arxiv-2604.21280) ;
  - TinyCL : 35x (§I-B) contre 58x (résumé) (arxiv-2402.09780) ;
  - « 10,65x » de SMOF en GOP/s, sur des UNet de tailles différentes (arxiv-2403.18921, §V-D) ;
  - arxiv-2507.18174 conclut à l'efficacité, mais sa Table I la contredit (2,6 FPS/W, moins
    que quatre des cinq travaux cités) ;
  - écarts de chiffres entre résumé et texte : arxiv-2607.13106 (≈ 5 % contre ≈ 7 %),
    arxiv-2006.08357, arxiv-2503.04832 (43 / 44 / 43,63 FPS) ;
  - survey qui en tire des recommandations (arxiv-2509.04153, §VI-A).
- Ce qui manque : un jeu de métriques imposé (latence batch 1, débit, énergie de carte par
  inférence, précision sur cible) et la relecture des comparaisons publiées à cette aune.
  Venieris proposait déjà ce jeu en 2018 (2018-venieris, §3.1).
- Statut : étayé (20 fiches). Constat méthodologique.
- Piste : recalculer les rapports annoncés quand les données le permettent, pour l'état de
  l'art du pré-projet.

### Code et bitstreams rarement publiés
- Constat, sur les fiches expérimentales `done` :
  - **aucun bitstream publié** dans tout le corpus (recherche sur les 101 fiches) ;
  - code propre au papier publié ou annoncé :
    - (passages précédents) arxiv-2211.11647, arxiv-1809.04570 (en partie),
      arxiv-2108.03986, 2019-ding, 2021-xu, arxiv-2011.07317, 2024-campos ;
    - (8e passage) SMOF (arxiv-2403.18921, GitHub) ; Chameleon (2024-aggarwal, GitHub
      annoncé) ; SkyNet (arxiv-1909.09709, lien absent du texte extrait) ;
      arxiv-1912.07394 (s'appuie sur FINN public) ; hors FPGA, arxiv-1904.08653 (GitLab),
      arxiv-2011.10671 (pod_compare), 2024-rech (scripts CAROL), données CrowdHuman
      (arxiv-1805.00123) ;
  - non publiés (8e passage) :
    - détection : 2024-yan, 2024-zhang, 2025-kim, 2026-fata, arxiv-2607.13106,
      arxiv-2609.24757, arxiv-2304.11580 ;
    - AE et compression : arxiv-2407.17647, arxiv-2503.04832, arxiv-2511.17135 ;
    - entraînement et CL : arxiv-2202.10935, 2021-piyasena-accelerating, arxiv-2604.21280 ;
    - sûreté : arxiv-2406.12362, 2020-libano.
- Ce qui manque : projet, bitstream et scripts de mesure pour revérifier les chiffres sur
  carte. Pour la certification, c'est aussi une condition de traçabilité (déduit).
- Statut : étayé (environ 55 fiches expérimentales). La lecture se limite au texte extrait :
  les liens en note de bas de page sont souvent perdus.
- Piste : publier le projet, le bitstream et les scripts de l'expérience KV260.

## Toolflows

### Pas de comparaison croisée hls4ml / FINN / Vitis AI sur un même CNN et une même carte
- Constat :
  - aucun papier d'outil ne compare deux flots mesurés (arxiv-2512.01463, arxiv-2103.05579,
    arxiv-1809.04570, arxiv-2101.05108, SATAY §II-C) ;
  - Venieris compile des chiffres publiés sans relancer les outils (2018-venieris, §2.6) ;
  - Campos exporte en QONNX mais n'évalue que hls4ml (2024-campos, §2.3) ;
  - (8e passage) **contre-exemple partiel : MLPerf Tiny**. hls4ml et FINN sont mesurés sur la
    même carte (Pynq-Z2) avec la même méthode EEMBC : IC CIFAR-10 à 27,3 ms et 44 330 µJ
    (hls4ml) contre 1,5 ms et 2 535 µJ (FINN). Mais les modèles diffèrent (58 k paramètres
    sur 8-12 bits contre 1,5 M binaires), c'est de la classification, et il n'y a pas de
    Vitis AI (arxiv-2206.11791, Table 5) ;
  - (8e passage) QONNX : FINN n'ingère que ReLU, hardtanh et identité (§VI-D) ; SiLU et
    LeakyReLU ne sont pas listés (arxiv-2206.07527) ;
  - (8e passage) le DPU impose des modifications d'opérateurs aux YOLO récents (ReLU,
    attention approchée) (arxiv-2607.13106). Le DPU et le dataflow n'acceptent donc pas le
    même modèle (déduit).
- Ce qui manque : un même CNN de détection, une même carte, les trois flots ; ressources,
  latence, puissance et précision.
- Statut : étayé (12 fiches) dans le corpus. Nuancé par arxiv-2206.11791 (hls4ml contre FINN,
  classification, modèles différents).
- Piste : QONNX vers FINN et hls4ml, plus Vitis AI, sur KV260, pour un YOLO à opérateurs
  compatibles (ReLU) : expérience de thèse candidate.

### Réseaux qui ne tiennent pas on-chip : limite du dataflow
- Constat (passages 1 à 7) :
  - FINN suppose tout en OCM (arxiv-1612.07119, §6) ;
  - offload de FINN-R peu prévisible (arxiv-1809.04570) ;
  - fpgaConvNet partitionne (arxiv-1711.08740) ; SATAY jusqu'à 26 MB on-chip ;
  - FCMP : jusqu'à 30 % d'OCM en moins (arxiv-2011.07317, Tables IV-V) ;
  - REQ-YOLO (2019-ding, §5).
- Constat (8e passage) :
  - **SMOF** : éviction off-chip en DDR et compression des activations dans fpgaConvNet.
    Gain jusqu'à 1,3x sur UNet ; la reconfiguration pèse 31 % de la latence à batch 1
    d'UNet3D ; la performance dépend du taux de compression et varie selon l'image
    (arxiv-2403.18921, Fig. 6-8, Table IV) ;
  - **Elastic-DF** : partitionnement de FINN sur plusieurs SLR ou FPGA (Alveo, 100 GbE)
    (2021-alonso-elastic-df-scaling-performance-dnn, Tables 4-5) ;
  - 2026-fata : YOLOv3-Tiny élagué sur KV260, avec BRAM et URAM à 100 % et une allocation
    mémoire contournée via `arch.json`, décrite qualitativement (Table 9) ;
  - MCUNetV2 : l'inférence par patchs divise le pic mémoire par 3,7 à 8,0. Sa transposition
    à la BRAM d'un dataflow n'est pas couverte (hypothèse de la fiche, arxiv-2110.15352,
    Fig. 5).
- Ce qui manque : la combinaison « quantification agressive (FINN) + empaquetage (FCMP) ou
  éviction (SMOF) » pour un YOLO ou un CAE sur KV260, avec le coût mesuré à batch 1 **et sa
  variabilité temporelle**.
- Statut : étayé (13 fiches). La combinaison est absente du corpus.
- Piste : SMOF est open source ; l'essayer sur ZCU102 puis KV260 avec un YOLOv8n quantifié.

### Estimation de puissance et de latence dans les toolflows
- Constat :
  - FINN-R : ressources et débit seulement (arxiv-1809.04570, §4) ;
  - hls4ml 2025 : aucune puissance (arxiv-2512.01463) ;
  - Campos : latences HLS (2024-campos, §6.2) ; Manjunath : Vivado (§VIII-A) ;
  - (8e passage) SMOF : ni puissance ni énergie (arxiv-2403.18921) ;
  - (8e passage) le dimensionnement automatique des FIFO de FINN donne 35 FPS contre 22 en
    manuel. La fiche souligne l'écart entre estimation et mesure (arxiv-2609.24757, §V) ;
  - (8e passage) modèles analytiques validés sur carte, mais hors toolflow : EF-Train (écart
    1,05 % sur AlexNet, arxiv-2202.10935, Table 6) ; arxiv-2503.04832 (−3,4 à −16,1 %,
    Table V) ;
  - (8e passage) hls4ml mesure enfin une énergie, avec EEMBC, dans MLPerf Tiny
    (arxiv-2206.11791) ;
  - (9e passage) hls4ml d'origine : les ressources de la Table 2 sont des estimations de
    synthèse Vivado HLS ; sur un réseau plus petit implémenté, les FF estimés sont 2 à 4 fois
    trop hauts et les LUT aussi surestimées ; l'horloge visée (5 ns) a dû être relâchée à
    8 ns à l'implémentation (arxiv-1804.06913, §3.2-3.3, Fig. 16-17). Les 2 lignes du CSV
    portent cette réserve.
- Ce qui manque : un modèle de puissance validé sur carte, intégré au flot.
- Statut : hypothèse pour l'état actuel des outils. Étayé (7 fiches) pour le constat
  « estimation non validée » dans les papiers.
- Piste : vérifier la documentation actuelle de FINN et de hls4ml.

### NAS et quantification mixte guidées par le matériel sur FPGA
- Constat :
  - absent du survey arxiv-2411.01431 ; NAS hardware-aware côté MCU (2025-el-zeinaty,
    §6.4.2) ;
  - quantification mixte Hessienne + ILP vers hls4ml, sur MLP (2024-campos, Table 2) ;
  - REQ-YOLO, quantification par couche (2019-ding, §5.1) ;
  - (8e passage) **NAS bayésienne (KerasTuner)** sur un ResNet-8 pour hls4ml, sur Pynq-Z2 :
    83,5 % contre 87,0 % pour la référence (arxiv-2206.11791, §3.1) ;
  - (8e passage) **SkyNet** : co-design bottom-up guidé par la latence estimée en HLS,
    pour la détection (arxiv-1909.09709, §4) ;
  - (8e passage) précision mixte 8 / 32 bits pour la couche GDN (arxiv-2503.04832, §III-D),
    mixte simulée seulement (arxiv-2511.17135).
- Ce qui manque : une NAS ou une quantification mixte guidée par la latence ou la puissance
  **mesurées** sur FPGA embarquée, pour un détecteur récent.
- Statut : hypothèse pour la NAS de détection. Nuancé : NAS sur FPGA (classification) et
  co-design de détecteur (SkyNet, latence estimée) existent.
- Piste : HAWQ + ILP (Campos) sur la tête d'un YOLO, puis génération avec FINN ou hls4ml
  via QONNX.

## Apprentissage continu embarqué

### Pas de comparaison MCU / FPGA / Jetson pour un même algorithme de CL
- Constat :
  - O-FSCIL sur GAP9 seulement (arxiv-2403.07851) ; QLR-CL sur VEGA contre STM32L4
    (arxiv-2110.10486, Table IV) ; ImageHD sur ZCU104 contre CPU / GPU / Jetson
    (arxiv-2604.21280) ; ONLAD contre CPU / GPU (2019-tsukada) ;
  - (8e passage) SLDA sur ZCU102 contre ARM A53 et Xavier NX : FPGA 24x plus rapide que
    l'A53 en PlasticCov, mais **le CPU bat le FPGA en StaticCov** (2,80 contre 4,76 µs)
    (2021-piyasena-accelerating, Table IV) ;
  - (8e passage) Chameleon : ZCU102, Jetson Nano (batch 8) et EdgeTPU **simulé**
    (2024-aggarwal, Table VI) ;
  - (8e passage) côté MCU seul : 256 KB (arxiv-2206.15472, STM32F746), TinyCL en ASIC
    (arxiv-2402.09780).
- Ce qui manque : un même algorithme de CL mesuré sur les trois cibles.
- Statut : étayé (9 fiches). Aucun papier n'a à la fois une FPGA et un MCU
  (couverture croisée).
- Piste : porter SLDA (2021-piyasena-accelerating) ou QLR-CL sur KV260, sur un Orin et sur
  GAP9, avec la même mesure de puissance.

### Apprentissage par rétropropagation sur SoC FPGA : lent, en flottant, énergie non mesurée
Nouveau au 7e passage, reformulé au 8e. L'ancienne forme (« les apprentissages sur FPGA du
corpus évitent la rétropropagation ») est contredite par arxiv-2202.10935 et 2024-aggarwal.
- Constat :
  - **EF-Train** : FP / BP / WU sur PYNQ-Z1 et ZCU102, en **FP32**, data reshaping. Il fait
    28,15 GFLOPS et 2,08 ms par image à batch 128 sur ZCU102 ; précision 64,82 % sur FPGA
    contre 65,22 % sur V100 (CIFAR-10). Puissance tirée du rapport Vivado
    (arxiv-2202.10935, §6.3, Table 7 ; preprint) ;
  - **Chameleon** : accélérateur FP / BP / WU en **FP16** sur ZCU102 pour le replay latent.
    Il prend 413 ms et 1,22 J par image, contre 33 ms sur Jetson Nano ; les auteurs
    reconnaissent que le GPU est plus rapide (2024-aggarwal, §IV-A, Table VI, §V-D) ;
  - ONLAD (OS-ELM) et ImageHD (HDC) évitent la rétropropagation ; SLDA n'apprend que la
    dernière couche, avec l'inversion de covariance sur l'ARM
    (2021-piyasena-accelerating, §V) ;
  - la seule rétropropagation INT8 du corpus tourne sur MCU (arxiv-2206.15472) ou sur ASIC
    (arxiv-2110.10486, arxiv-2402.09780).
- Ce qui manque : une rétropropagation de la queue d'un réseau en précision réduite (INT8,
  sparse update) sur SoC FPGA, à latence compatible avec le flux vidéo, avec l'énergie
  mesurée.
- Statut : étayé (7 fiches).
- Piste : l'étage figé sur le DPU et la queue apprise en PL. Combiner le graphe backward
  statique de arxiv-2206.15472 et l'accélérateur de Chameleon.

### Adaptation à la dérive pour la détection d'anomalies embarquée
- Constat :
  - ONLAD est le seul travail au croisement CL × AE sur FPGA. L'AUC passe de 0,55-0,59 à
    0,78-0,90 sous dérive simulée (2019-tsukada, Table 5) ;
  - Malviya fixe son seuil une fois pour toutes (μ + σ) (2022-malviya, §III) ;
  - (8e passage) arxiv-2407.17647 fixe aussi un seuil unique, réglé sur le test (§III-D) ;
  - (8e passage) Chameleon s'adapte au domaine (domain-IL, CORe50), mais en classification
    (2024-aggarwal) ;
  - (8e passage) le survey 2023-cui ne discute ni calibration du seuil ni FAR / MAR
    (§VI-B).
- Ce qui manque : un détecteur d'anomalies visuelles embarqué qui adapte son modèle ou son
  seuil à la dérive (éclairage, usure), sur FPGA.
- Statut : hypothèse (5 fiches). Lien avec les moniteurs d'exécution (section Sûreté) :
  adapter le seuil d'un moniteur pose la même question de certification.
- Piste : ONLAD appliqué aux caractéristiques d'un encodeur CNN figé, sur KV260.

### CL sur FPGA : énergie de portée non précisée ou estimée
Reformulé au 8e passage (ancien intitulé : « CL sur FPGA : précision faible et énergie
estimée »). La partie « précision faible » est contredite par 2021-piyasena-accelerating
(78,79 % objet / 89,46 % catégorie, CoRE50, DPU + SLDA, Table V) et par 2024-aggarwal
(79,48 %, Table II).
- Constat :
  - ImageHD : 26,89 % d'ACC en clustering, énergie estimée par l'analyseur Vitis
    (arxiv-2604.21280, Table VII) ;
  - ONLAD : puissance de carte mesurée (3,1 W), précision en logiciel (2019-tsukada) ;
  - SLDA : 9,00 W et 0,056 J par image pour le système DPU + PlasticCov, lus sur les rails,
    portée non dite (2021-piyasena-accelerating, Table V) ;
  - Chameleon : 1,22 J par image, méthode non décrite (2024-aggarwal, Table VI) ;
  - EF-Train : rapport Vivado (arxiv-2202.10935).
- Ce qui manque : la frontière précision / énergie d'un CL mesurée à la carte et à la puce
  sur la même plateforme.
- Statut : étayé (6 fiches).
- Piste : remesurer SLDA sur ZCU102 ou KV260 avec wattmètre et télémétrie.

### CL limité à la classification
- Constat :
  - FSCIL, ImageHD, QLR-CL, SLDA (CoRE50, CUB200), Chameleon, TinyCL, distilled replay et
    EF-Train font de la classification (arxiv-2403.07851, arxiv-2604.21280,
    arxiv-2110.10486, 2021-piyasena-accelerating, 2021-piyasena-fpga, 2024-aggarwal,
    arxiv-2402.09780, arxiv-2409.07114, arxiv-2202.10935) ;
  - ONLAD fait de l'anomalie non visuelle ;
  - (8e passage) **la détection incrémentale existe, mais sans FPGA** :
    - RILOD sur Jetson TX2 : 233 s d'entraînement en edge seul, VOC 19+1 mAP 65,0 avec
      distillation (arxiv-1904.00781, Table 7, §6.2.4 ; preprint) ;
    - Latent Distillation avec NanoDet : −56 % de FLOPs par mise à jour, sans aucune mesure
      sur cible ; l'implantation tinyML est renvoyée aux travaux futurs
      (arxiv-2409.01872, Table 3, §6 ; preprint) ;
  - le survey class-IL (arxiv-2010.15277) ne traite la détection qu'en §4 et exclut
    l'online ;
  - 2023-zhai bascule dynamiquement entre modèles (sans apprentissage) ;
  - la couverture croisée n'a **aucune ligne** détection × apprentissage continu.
- Ce qui manque : l'incrémental de classes en détection (YOLO) sur FPGA, avec latence et
  énergie de mise à jour.
- Statut : étayé (13 fiches). Nuancé : algorithmes de détection incrémentale disponibles
  (RILOD, LD) mais jamais sur FPGA. Question de thèse candidate (`yolo-fpga` ×
  `continual-learning`), en tension avec la certification (section Sûreté).
- Piste : LD (arxiv-2409.01872) sur une tête YOLO / NanoDet, backbone figé sur DPU, tête en
  PL ou PS.

## Surveys

### Surveys : « embarqué » sans FPGA, ou « FPGA » sans comparaison chiffrée entre plateformes
- Constat :
  - « embarqué » sans FPGA ou presque : arxiv-2411.01431, 2025-el-zeinaty (§8),
    2024-mittal (§4.3.3), 2023-shuvo (§XI-C1) ;
  - « FPGA » sans comparaison chiffrée avec Jetson ou MCU : 2025-hozhabr (Table 5),
    arxiv-2509.04153 (Tables VII-IX hétérogènes, §VI-A), arxiv-1806.01683,
    2018-venieris ;
  - (8e passage) surveys de sûreté **sans FPGA quantifié** : 2023-ruospo ne cite que de
    petits classifieurs ; 2024-rech est centré GPU et traite le FPGA brièvement (§IV-C.1) ;
    arxiv-1812.08342 et 2020-schwalbe n'ont aucun matériel ;
  - (8e passage) surveys d'application sans matériel : 2023-cui (anomalie visuelle),
    arxiv-2010.15277 (class-IL), arxiv-2001.04193 (Re-ID, §4.3.5).
- Ce qui manque : une synthèse quantitative FPGA / Jetson / MCU à NPU sur des critères
  communs, **et** une synthèse « sûreté × accélérateur FPGA de détection ».
- Statut : étayé (16 surveys). Argument de positionnement.
- Piste : citer ces deux manques dans l'état de l'art du pré-projet.

### Détection sur MCU et sur petit FPGA : aucune passerelle
- Constat :
  - côté MCU : MCUNetV2, XiNet, TinyissimoYOLO (2025-el-zeinaty, Table 8 ;
    arxiv-2110.15352, Table 3 ; arxiv-2306.00001, Table II) ;
  - côté petit FPGA : 2023-zhai, arxiv-2101.05108, DAC-SDC (2021-xu, §4.2) ;
  - (8e passage) YOLOv3-tiny allégé en w2a4 sur XC7Z020 à 2,91 W : c'est le premier
    détecteur dataflow de la base de taille proche d'un MCU, mais sans portage MCU
    (arxiv-2609.24757) ;
  - (8e passage) NPU edge : Hailo-8 mesuré, mAP COCO 32 (arxiv-2409.16808, §IV) ;
  - aucun papier n'a de lignes à la fois FPGA et MCU (couverture croisée).
- Ce qui manque : pour un même détecteur compressé, la frontière latence / énergie / mAP sur
  MCU (GAP9, STM32N6) et sur petit FPGA, à portée d'énergie égale.
- Statut : hypothèse (8 fiches).
- Piste : porter TinyissimoYOLO, ou le LP-YOLO Slim d'arxiv-2609.24757, sur les deux
  familles.

## Sûreté, fiabilité et certification

Section nouvelle au 8e passage (29 fiches `safety-certification`). Réserve : aucun texte
normatif n'est dans la base. Les constats portent sur ce que disent les guides (EASA, AMLAS,
DEEL), les surveys et les études de fiabilité.

### Aucun détecteur d'objets quantifié sur FPGA dans les travaux de fiabilité, de vérification ou de surveillance
- Constat :
  - **fiabilité matérielle sur FPGA, toujours sur de petits classifieurs** :
    - Iris ANN (19 poids) et CNN MNIST (1 848 poids) sur Zynq
      (2019-libano-selective-hardening-neural-networks-fpgas, §I, §III) ;
    - CNN et HNN MNIST, 233 ns par inférence ; les auteurs admettent que ce n'est pas
      transférable à YOLO (2020-libano-understanding-impact-quantization-accuracy-radiation,
      §V) ;
    - QNN FINN MNIST et CIFAR-10 sur ZCU104
      (arxiv-1912.07394-efficient-error-tolerant-quantized-neural, §V) ;
  - **fiabilité hors FPGA**, sur classifieurs : AlexNet, ConvNet et NiN simulés
    (2017-li-understanding-error-propagation-deep-learning, §4) ; AlexNet et VGG-16 CIFAR-10
    sous PyTorch (arxiv-1912.00941-ft-clipact-resilience-analysis-deep, §V) ;
  - les surveys de résilience ne citent pas de YOLO sur FPGA (2023-ruospo, 2024-rech,
    §IV-C.1) ;
  - **vérification formelle** sur MLP et BNN MNIST (arxiv-1702.01135, arxiv-1709.06662,
    arxiv-2012.08185) ;
  - **moniteurs d'exécution** sur classifieurs : MNIST, CIFAR, GTSRB, données tabulaires
    (arxiv-1610.02136, arxiv-1809.06573, arxiv-1911.09032, arxiv-2005.13166) ;
  - YOLO apparaît dans les travaux de sûreté, mais **sur GPU** :
    - Gaussian YOLOv3 sur GTX 1080 Ti (arxiv-1904.04620, §4) ;
    - YOLOv3-tiny « certifié » ED-324 / ARP6983 sur Jetson AGX Xavier
      (arxiv-2406.12362, §V) ;
    - prédiction conforme sur YOLOv5m sans plateforme (arxiv-2304.06052) ;
    - (9e passage) moniteur de personnes manquées KGFP sur YOLOv8l gelé, GPU non précisé,
      sans quantification (arxiv-2603.25499, §3.2, « Plateforme ») ;
  - (9e passage) la seule nouvelle étude de fiabilité sur FPGA reste un classifieur : BNN
    FINN entièrement connecté sur MNIST, ~93 %, Ultra96 (arxiv-2404.01757, §II-C) ;
  - inversement, **aucun des 18 papiers `yolo-fpga` ne traite la sûreté**. 2026-fata
    renvoie la tolérance aux fautes en perspective (§VI) ; 2024-zhang, 2025-kim, 2024-yan,
    arxiv-2609.24757 et arxiv-2607.13106 n'en disent rien.
- Ce qui manque : un YOLO quantifié sur SoC FPGA soumis à injection de fautes, à
  vérification (même partielle) et à un moniteur d'exécution, avec une métrique de
  détection.
- Statut : étayé (27 fiches). C'est le croisement central de la thèse : les deux moitiés
  existent, séparément.
- Piste : choisir un YOLOv3-tiny / v8n sur KV260 comme objet commun aux expériences de
  fiabilité, de mAP sur cible et de moniteur.

### Fiabilité SEU à l'échelle d'un détecteur : criticité par couche, TMR sélectif, DPU contre dataflow
- Constat :
  - **la criticité varie par couche**. Sur le CNN, la FC finale (IP2) est la plus
    vulnérable. Le TMR sélectif sur IP2 masque ~40 % des fautes pour 8 % de surcoût ; le TMR
    complet n'a pas pu être testé faute de LUT (2019-libano, §V-C, Fig. 6, Table I) ;
  - **les couches convolutives ne sont pas naturellement tolérantes** : jusqu'à ~10,8 points
    perdus avec un canal bloqué (CNV, Table II). La réplication sélective coûte 49,87 à
    173,47 % de MAC, contre 200 % pour le TMR complet (Table III) (arxiv-1912.07394) ;
  - les **modèles de fautes sont incomplets** :
    - BRAM exclue de l'injection, alors que les poids y résident (2019-libano, §III-A ;
      2020-libano) ;
    - stuck-at de canal, avec les SEU en travail futur (arxiv-1912.07394, §VII) ;
    - latches et buffers seulement, sans logique de contrôle ni configuration FPGA
      (2017-li, §4.3) ;
    - fautes de poids logicielles (arxiv-1912.00941) ;
    - fautes uniques seulement (2019-libano, arxiv-1912.07394, arxiv-2404.01757) ;
    - (9e passage) **contre-exemple partiel** : la mémoire de configuration (CRAM, par
      émulation FREtZ, 194 031 fautes, marge 0,3 %) et les FF (simulation exhaustive) d'un
      BNN FINN sont injectées. Mais réseau MNIST, une seule configuration PE/SIMD, aucun
      essai sous faisceau (arxiv-2404.01757, §III, Tables II-III) ;
  - (9e passage) **la criticité varie aussi dans le temps** : les erreurs critiques viennent
    surtout des ~50 premiers cycles de la couche 0 ; des crashes (timeouts, 1,06 % des
    fautes CRAM, 1,51 % des FF) viennent de la logique de contrôle, même d'une couche pas
    encore démarrée (arxiv-2404.01757, §IV-B, Fig. 4, Tables II-III). Un crash est une
    défaillance temporelle, pas une erreur de classe (déduit) ;
  - **la quantification déplace le risque** : section efficace estimée 39 % plus basse pour
    le réseau binarisé, mais une part d'erreurs critiques de 38 % contre 26 %
    (2020-libano, §IV-B) ;
  - le **DPU** (moteur programmable) n'a jamais été comparé au **dataflow** en logique
    pure du point de vue des SEU (2020-libano, gaps). Aucun papier n'injecte de fautes
    dans un DPU ;
  - des **mitigations légères** existent hors FPGA :
    - détecteur SED par bornes d'activation, rappel ~92,5 %, FIT d'Eyeriss réduit de 8,55
      à 0,35 (2017-li, §6.2) ;
    - clipping d'activations (arxiv-1912.00941) ;
    - ABFT et cohérence temporelle recensés (2024-rech) ;
    - aucune n'est combinée au TMR sélectif ni chiffrée en ressources FPGA ;
  - côté FPGA durci : PolarFire (flash) est « tenu aux radiations », mais sans test en
    faisceau ; la logique utilisateur reste sensible aux SEU (arxiv-2602.15751, §6.3).
- Ce qui manque :
  - une campagne d'injection (configuration, BRAM, multi-fautes) sur un YOLO INT8, en DPU
    et en dataflow (FINN) ;
  - la criticité par couche mesurée en mAP et en personnes manquées ;
  - un durcissement sélectif (TMR, clipping, SED) chiffré en LUT / BRAM ;
  - l'effet de la précision et du folding (PE/SIMD) sur la vulnérabilité, promis en travail
    futur par arxiv-2404.01757 (§V).
- Statut : étayé (10 fiches).
- Piste :
  - méthode de 2019-libano (ICAP / Pblocks, criticité par couche) appliquée au YOLOv3-tiny
    FINN d'arxiv-2609.24757 et au DPU de 2026-fata ;
  - injection hybride selon la cartographie de 2023-ruospo (logiciel, puis bitstream).

### Critère de criticité d'erreur pour la détection de personnes et lien FIT / précision → SIL / PL
- Constat :
  - le **critère d'erreur critique** des études de fiabilité est celui d'un classifieur :
    changement de la classe prédite (2019-libano, Limites) ; chute de précision ≥ 2 %
    arbitraire (arxiv-1912.07394, Limites) ; seuil 90 % → 88 % posé sans réponse
    (2023-ruospo) ;
  - 2024-rech propose un critère par seuil de Jaccard sur les boîtes : non-détection, faux
    positif, mauvaise classe. Il n'est relié ni à la SIL ni au PL ;
  - **aucun papier ne traduit un FIT ou une section efficace en SIL / PL** :
    - 2017-li reste en FIT et ISO 26262 (§1, §4.7) ;
    - 2019-libano le laisse ouvert (Limites) ;
    - 2024-rech s'arrête au FIT / ASIL ;
  - au sol (13 n/cm²/h), le risque d'un classifieur est dominé par son inexactitude, pas par
    les radiations. Les auteurs proposent le MEBF pour combiner les deux
    (2020-libano, §IV-B, Fig. 5-6) ;
  - **l'asymétrie non-détection / fausse alarme** est posée par les guides :
    - métriques asymétriques (2020-easa-concepts-design-assurance-neural-networks, §8.1.1) ;
    - perte asymétrique (arxiv-2103.10529-white-paper-machine-learning-certified,
      §4.2.4.2) ;
    - exemple d'ordre de grandeur : un obstacle par minute et une erreur de 10^-3 donnent
      6·10^-2 défaillances par heure (arxiv-2103.10529, §4.2.4.4) ;
    - mais la prédiction conforme ne couvre que les vrais positifs, ni les faux négatifs
      ni les faux positifs (arxiv-2304.06052, §4.1-4.2) ;
  - « détecter une personne » est inspécifiable au sens d'ISO 26262 (arxiv-1709.02435,
    §III-C) ;
  - (9e passage) KGFP fournit une **première définition opérationnelle** : une image est
    « non sûre » si au moins une personne est manquée (IoU < 0,5, seuil de confiance 0,5)
    (arxiv-2603.25499, §3.1, Éq. 1, §4.1). Elle reste tout-ou-rien, au niveau de l'image,
    sans distance, zone ni persistance sur plusieurs images (fiche, Limites). Le papier
    invoque le SIL 4 (§1) sans aucun argument d'assurance ;
  - (9e passage) BNN FINN : « critique » = mauvaise classe MNIST, les crashes sont comptés à
    part (arxiv-2404.01757, §IV) ; les critères de prédiction d'échec du corpus sont
    symétriques (erreur 0/1 : arxiv-1901.09192 §2 ; TCP : arxiv-1910.04851 §2.1 ; règle de
    Chow : arxiv-2403.02886 §3.3.2).
- Ce qui manque : une définition de l'erreur dangereuse d'un détecteur de personnes (personne
  manquée sur N images consécutives, dans une zone, à une distance), et une chaîne de calcul
  du taux de défaillance dangereuse par heure qui combine l'inexactitude du modèle et les
  fautes matérielles, comparable aux cibles SIL / PL.
- Statut : étayé (15 fiches) pour l'absence de traduction. Les valeurs cibles des normes
  ne sont pas dans la base : leur usage reste à vérifier dans les textes.
- Piste :
  - partir du MEBF de 2020-libano et du calcul horaire de arxiv-2103.10529 ;
  - définir la non-détection de personne au niveau de la séquence (vote multi-images,
    arxiv-2102.01564, Ex. 46).

### Chaîne de preuve d'équivalence modèle → bitstream et qualification des toolflows
- Constat :
  - **l'étape « implémentation » est renvoyée à plus tard par tous les guides** :
    - la conformité du matériel spécialisé (FPGA) à DO-254 « will not be addressed »
      (§4.2.3) ; la vérification de l'inférence est un travail futur (§6.5) ; la
      quantification est seulement « à valider » (§6.1) (2020-easa) ;
    - IMP-06, préservation des propriétés après transformation, n'a pas de MOC abouti ;
      l'implémentation FPGA est renvoyée à AMC 20-152A
      (2024-easa-concept-paper-guidance-level-1) ;
    - la qualification d'outils (DO-178C §12.2, TQL) est citée sans application aux
      toolflows FPGA (2024-easa-concepts-design-assurance-neural-networks, §3.7.1, §3.7.3) ;
    - AMLAS n'a pas d'étape plateforme pour la quantification ou la HLS
      (arxiv-2102.01564) ;
    - DEEL pose la robustesse après quantification comme défi (§4.8.3.2) (arxiv-2103.10529) ;
  - **les rares implémentations traçables ne sont pas sur FPGA** :
    - ACETONE génère du C traçable (DO-178C) avec un WCET par OTAWA, mais en FP32 sur CPU ;
      la préservation sémantique est validée par tests, pas prouvée (§4.2), et le WCET est
      calculé sur une cible (lpc2138) différente de celle mesurée
      (2022-de-albuquerque-silva-acetone-predictable-programming-framework-ml) ;
    - YOLOv3-tiny selon ED-324 / ARP6983 : la traçabilité s'arrête aux pilotes NVIDIA
      (§VI), et le FP16 est validé par tests (arxiv-2406.12362) ;
  - **les toolflows FPGA ne fournissent aucune garantie de conversion** :
    - QONNX ne garantit pas formellement l'arrondi et la saturation entre outils (déduit
      par la fiche, arxiv-2206.07527) ;
    - MLPerf Tiny ne vérifie pas l'équivalence QAT → RTL (arxiv-2206.11791) ;
    - le DPU impose un modèle modifié, différent du modèle de référence, avec des écarts de
      précision imprévisibles (arxiv-2607.13106, Table II) ;
    - l'opérateur GDN personnalisé dans le flot Vitis AI pose la question de sa
      qualification (arxiv-2503.04832) ;
    - le DSP packing INT4 pose un risque d'équivalence bit-exacte (déduit, 2024-yan) ;
  - la vérification formelle bit-exacte du réseau quantifié existe sur petit réseau
    (arxiv-2012.08185), mais son lien avec la RTL ou le bitstream n'est pas démontré.
- Ce qui manque :
  - une chaîne de preuve modèle entraîné → modèle quantifié (QONNX) → HLS / RTL → bitstream,
    avec équivalence bit-exacte vérifiée au moins par tests exhaustifs sur les couches ;
  - une analyse de qualification (TQL) d'un toolflow (FINN ou Vitis AI).
- Statut : étayé (14 fiches). Question de thèse candidate.
- Piste :
  - comparer, sur un YOLO FINN, les sorties bit à bit du modèle QONNX exécuté en logiciel
    et du bitstream (cosimulation, puis carte) ;
  - documenter ce qui relèverait d'une qualification d'outil. FINN, dataflow et open
    source, est plus inspectable que le DPU (déduit).

### Vérification formelle non scalable aux CNN de détection
- Constat :
  - Reluplex : ~300 ReLU (ACAS Xu, 6 couches cachées), timeouts sur φ7, en arithmétique
    flottante (arxiv-1702.01135-reluplex-efficient-smt-solver-verifying, §6, §8) ;
  - BNN : ~500 neurones denses, aucune convolution ; sur MNIST-back-image, plus de la moitié
    non résolue en 300 s dès ε = 3
    (arxiv-1709.06662-verifying-properties-binarized-deep-neural, §4, Table 2) ;
  - réseau quantifié bit-exact (52 650 paramètres, 4 couches denses) : 55,7 % (MNIST) et
    40,9 % (Fashion-MNIST) de cas résolus à ε = 4. Le problème est PSPACE-hard
    (arxiv-2012.08185-scalable-verification-quantized-neural-networks, Limitations,
    Hardness) ;
  - le survey arxiv-1812.08342 juge la vérification complète non scalable (§4.3, §8.5) ;
  - les propriétés vérifiées sont des robustesses L∞, sans lien avec un danger
    (arxiv-2012.08185, arxiv-1709.06662) ;
  - la piste « vérifier des sous-composants » est suggérée par les fiches d'arxiv-2012.08185
    et d'arxiv-1702.01135 (déduit).
- Ce qui manque :
  - une vérification bornée de **composants** d'un détecteur : tête, NMS, moniteur, couche
    binarisée ;
  - des propriétés pertinentes pour la détection de personnes ;
  - ou, à défaut, des garanties statistiques (prédiction conforme) en complément.
- Statut : étayé (4 fiches). La littérature récente (α,β-CROWN, Marabou) n'est pas dans
  la base : hypothèse pour l'état de l'art actuel.
- Piste : `/paper-discover "verification quantized neural network convolutional"` ;
  vérifier formellement un moniteur ou un post-traitement implanté en RTL, plus petit que le
  réseau.

### Moniteurs d'exécution (OOD, incertitude, prédiction conforme) non portés sur FPGA
- Constat :
  - **les moniteurs existent, en logiciel, sur classifieurs** :
    - MSP (arxiv-1610.02136) ;
    - patrons d'activation en BDD : même à γ = 3, 45 % des alertes ne sont pas des erreurs
      (arxiv-1809.06573, Limites) ;
    - boîtes d'abstraction, τ réglé par jeu (arxiv-1911.09032, §4.1) ;
    - ECDF, avec une fenêtre de 1 500 échantillons et une exactitude minimale surestimée
      (arxiv-2005.13166, §4.1, §4.3) ;
  - **sur détecteurs, sans cible embarquée** :
    - incertitude de localisation de Gaussian YOLOv3 pour +0,04 % de FLOPs
      (arxiv-1904.04620) ;
    - comparaison MC-Dropout / ensembles / Direct Modeling sur RetinaNet
      (arxiv-2011.10671, §IV) ;
    - prédiction conforme sur YOLOv5m, α = 0,1, garantie marginale, hypothèse
      d'échangeabilité violée à long terme (arxiv-2304.06052, §6) ;
  - **scores candidats déjà calculés sur FPGA, sans usage de moniteur** :
    - erreur de reconstruction d'un CAE sur DPU (arxiv-2407.17647) ;
    - D_KL ou KLD clipée en hls4ml (arxiv-2108.03986, arxiv-2411.01118) ;
    - Mahalanobis de SLDA proposé en §6.2.3, non réalisé (2021-piyasena-fpga) ;
  - **les guides demandent ces moniteurs, sans implantation** :
    - EXP-05 à EXP-07 (2024-easa-concept-paper) ;
    - OOD et incertitude (2024-easa-concepts) ;
    - discriminateur OOD (2020-easa) ;
    - défi ouvert §8.8 (arxiv-1812.08342) ;
    - MD01 / MD03 / MD04 (arxiv-1905.04223) ;
    - monitorage hors ODD en travail futur (arxiv-2406.12362, §VI) ;
  - aucun coût matériel (LUT, BRAM, latence) n'est mesuré pour un moniteur ; aucun moniteur
    n'est évalué sur near-OOD réalistes (éclairage, EPI, occultation) ;
  - (9e passage) **les nouvelles fiches `failure-prediction` confirment le constat** :
    - ConfidNet, SelectiveNet, FMFP, temperature scaling : logiciel seul, plateforme n/r
      (arxiv-1910.04851, arxiv-1901.09192, arxiv-2403.02886, arxiv-1706.04599,
      « Plateforme ») ;
    - les méthodes les plus fiables sous décalage (ensembles, M = 5 suffit) coûtent k passes
      ou k modèles, en formules seulement (arxiv-1906.02530, §5, Table S1) ;
    - à l'inverse, le temperature scaling est un scalaire sur les logits, sans effet sur
      l'argmax (arxiv-1706.04599, §4.2) ; FMFP ne change que les poids (déduit par la fiche,
      arxiv-2403.02886) ; leur coût FPGA serait quasi nul, mais n'est pas mesuré ;
    - **avertissement** : calibrer ou utiliser un score OOD dégrade souvent la prédiction
      d'échec (AURC ×10³ de 9,52 à 16,27 avec mixup, ResNet110 CIFAR-10 ; arxiv-2403.02886,
      Table 1). Un moniteur doit donc être évalué en AURC / AUROC d'erreur, pas en ECE ;
    - KGFP bat GRAM, KNN et ViM (AUROC sûr / non sûr 92,9 % contre 52,5 à 54,3 %), mais ces
      baselines sont non supervisées (arxiv-2603.25499, Table 2, §5.3).
- Ce qui manque : des moniteurs légers (MSP, boîtes, patrons, conformal, reconstruction)
  implantés à côté d'un YOLO sur FPGA, comparés à ressources égales. Il faut mesurer la
  latence ajoutée, l'effet de l'INT8 sur leur calibration, et le taux de détection des
  erreurs à taux de fausse alarme fixé.
- Statut : étayé (27 fiches). Le volet « prédiction d'échec de détecteur » est détaillé dans
  la section « Prédiction d'échec, sorties anticipées et moniteur sur cible ».
- Piste :
  - commencer par la prédiction conforme d'arxiv-2304.06052 : une marge additive après
    inférence, calibrée hors ligne (déduit par la fiche) ;
  - puis le moniteur à boîtes d'arxiv-1911.09032 sur les activations du YOLO, en PL.
    Mesurer le surcoût sur KV260.

### Correspondance des cadres aéronautique et automobile avec les normes industrielles
- Constat :
  - les cadres du corpus viennent de l'aéronautique (EASA concept paper, CoDANN I et II,
    ED-324 / ARP6983) ou de l'automobile (ISO 26262) :
    2024-easa-concept-paper, 2020-easa, 2024-easa-concepts, arxiv-2406.12362,
    arxiv-1709.02435, 2020-schwalbe ;
  - les cadres génériques restent aussi centrés aéronautique / ferroviaire / automobile :
    AMLAS (arxiv-2102.01564), DEEL (arxiv-2103.10529), desiderata (arxiv-1905.04223) ;
  - aucun ne fait la correspondance avec IEC 61508, ISO 13849, IEC 62061, ISO/IEC TR 5469 ou
    ISO/PAS 8800. Elle est citée comme gap par les fiches 2020-easa,
    2024-easa-concept-paper, arxiv-1709.02435, arxiv-2102.01564 et arxiv-2103.10529 ;
  - le seul papier du cadre robotique industriel (ISO 10218, ISO/TS 15066) date de 2018 et
    est antérieur aux détecteurs profonds. Il ne discute ni SIL ni PL. Les solutions
    certifiées sont propriétaires, à capteurs 3D (2018-halme-review-vision-safety-systems-human) ;
  - le niveau d'assurance accessible au non-supervisé est limité à DAL D
    (2024-easa-concept-paper, Foreword, §B.4).
- Ce qui manque : une correspondance objectif par objectif (learning assurance, ODD, IMP-xx,
  EXP-xx) vers IEC 61508-3 / ISO 13849-1 et ISO/IEC TR 5469, pour une fonction de sécurité
  de type « arrêt sur détection de personne » (ISO 10218 / TS 15066).
- Statut : étayé (11 fiches) pour l'absence dans le corpus ; **hypothèse** pour la
  littérature, car les normes et les travaux industriels récents (ISO/IEC TR 5469,
  ISO/PAS 8800) ne sont pas ingérés.
- Piste : ajouter à la base ISO/IEC TR 5469 (ou une présentation publique) et des travaux
  sur la sécurité machine avec ML ; construire le tableau de correspondance comme livrable
  du pré-projet.

### Argument FPGA contre GPU pour la certification : déterminisme, WCET et gigue non mesurés
- Constat :
  - **l'argument est posé, sans mesure** :
    - CoDANN II argumente pour le FPGA contre le GPU face aux objectifs COTS de l'AMC
      20-152A et de l'AMC 20-193 : microcode secret, DVFS, multicœur (§3.2.2, Annexe B).
      C'est une position d'entreprise (Daedalean), non étayée par des mesures
      (2024-easa-concepts, Limites) ;
    - l'ordre de grandeur demandé, 10 TOPS et 100 M de paramètres pour 6 img/s en 12 Mpixels
      (§3.2.2), n'est confronté à aucune plateforme ;
  - **côté GPU**, la traçabilité bloque aux pilotes (arxiv-2406.12362, §VI) et le WCET n'est
    établi que sur CPU (2022-de-albuquerque-silva-acetone, §4.2) ;
  - **côté FPGA, les mesures publiées sont des moyennes** :
    - 6 passes (arxiv-2304.11580) ; vidéo de 795 frames (arxiv-2607.13106) ;
    - latence variable selon la vidéo (2026-fata, Fig. 14) ;
    - latence d'une architecture streaming qui dépend du taux de compression des
      activations, avec reconfiguration (arxiv-2403.18921, Fig. 8, Table IV) ;
    - aucun papier ne donne de pire cas, de p99 ni de gigue de bout en bout ;
  - la distinction temps réel dur / mou est posée par 2025-hozhabr (§II-C2), et le WCET PS-PL
    est signalé non traité par arxiv-2509.04153 (§III-B) ;
  - les atouts supposés (FSM déterministe, dataflow à latence fixe, floorplan explicite,
    chaîne 100 % matérielle) sont des déductions des fiches 2025-kim, arxiv-2206.11791,
    2021-alonso et 2024-zhang, pas des affirmations mesurées ;
  - (9e passage) hls4ml donne une latence calculable par couche (Éq. 2.4 : 75 ns pour
    R = 1), mais à l'horloge de la synthèse HLS (5 ns), relâchée à 8 ns à l'implémentation
    (arxiv-1804.06913, §3.2-3.3) ; aucune borne n'est démontrée ;
  - (9e passage) arxiv-1905.04223 (§7.4, chunk 1905.04223#047.1) juge que le ML n'ajoute pas
    de difficulté au WCET, car l'effort de calcul serait indépendant de l'entrée. Cette
    prémisse tombe pour les réseaux à sorties anticipées (arxiv-1709.01686,
    arxiv-1703.09844), le NMS et le suivi sur le PS (déduit) ;
  - (9e passage) sur CPU, le point fixe 16 bits d'une couche réduit l'OWCET observé de 29 %
    et la dispersion (arxiv-2406.12362, §V-B, Fig. 11) : seul lien chiffré du corpus entre
    quantification et pire cas, observé et non analytique.
- Ce qui manque : une mesure de distribution de latence (max, p99.9, gigue) de bout en bout,
  sur FPGA (DPU et dataflow) et sur Jetson Orin, pour un même YOLO, avec et sans charge du
  PS. Il faudrait aussi un WCET analytique pour le dataflow.
- Statut : étayé (14 fiches). L'axe `timing-analysis` ne contient aucun papier : hypothèse
  pour la littérature (WCET de DNN sur SoC FPGA, contention mémoire, multi-DPU).
- Piste : ajouter à l'expérience KV260 contre Orin des traces de latence sur 10⁵ images.
  Comparer DPU, FINN et TensorRT. Question de thèse candidate : « le FPGA rend-il la borne
  de latence d'un détecteur démontrable ? ».

### Apprentissage en ligne exclu des cadres de certification : tension avec l'axe CL
- Constat :
  - **exclusion explicite** : « online learning (also known as continual or adaptive
    learning) … will not be accepted by EASA at this stage » (2024-easa-concept-paper,
    §C.1, MOC LM-02) ;
  - CoDANN suppose un système gelé (§2.6, §4.2.1) et reporte la recertification après
    ré-entraînement (§7.1.3) (2020-easa) ;
  - CoDANN II se limite à l'apprentissage hors ligne (2024-easa-concepts, §3.2) ;
  - AMLAS et DEEL se limitent au supervisé hors ligne (arxiv-2102.01564 ;
    arxiv-2103.10529, §1.3) ;
  - **côté CL, aucune fiche ne traite la non-régression, le versionnage ou le rollback** :
    2021-piyasena-fpga (Limites), 2024-aggarwal, arxiv-1904.00781, arxiv-2202.10935,
    arxiv-2206.15472, arxiv-2402.09780, arxiv-2409.07114 et arxiv-2409.01872 le signalent
    tous comme gap ;
  - des schémas en partie figés sont notés comme plus prévisibles, mais sans argument de
    certification :
    - SLDA StaticCov (2021-piyasena-fpga) ;
    - backbone gelé avec tête apprise (2021-piyasena-accelerating) ;
    - graphe backward compilé statiquement (arxiv-2206.15472, déduit) ;
    - mise à jour hors ligne (arxiv-2202.10935, déduit) ;
  - l'architecture évolutive de arxiv-2409.07114 (croissance du modèle) est jugée peu
    compatible avec un FPGA à architecture fixe et avec la certification (déduit par la
    fiche).
- Ce qui manque : un schéma d'apprentissage continu « certifiable par construction ». Par
  exemple :
  - un backbone gelé et certifié, une tête adaptée sous contraintes ;
  - un moniteur de non-régression sur un jeu de référence embarqué ;
  - un rollback, et un mode « proposer hors ligne, valider, déployer » ;
  - le surcoût de chaque élément mesuré sur FPGA.
- Statut : étayé (13 fiches). Question de thèse candidate. Elle relie les axes
  `continual-learning` et `safety-certification`, aujourd'hui disjoints.
- Piste : SLDA StaticCov sur DPU + PL (2021-piyasena-accelerating), avec un test de
  non-régression automatique avant activation des nouveaux paramètres. Mesurer le coût et
  la latence de validation.

## Prédiction d'échec, sorties anticipées et moniteur sur cible

Section nouvelle au 9e passage, liée au draft de sujet ARCYS (profile.md, 25/10/2026).
Réserve : les 8 fiches `failure-prediction` sont logicielles, 7 sur 8 en classification ;
l'axe `timing-analysis` est vide. Les travaux de prédiction de faux négatifs de détecteur
cités par KGFP ne sont pas dans la base (voir l'en-tête du 9e passage).

### Aucun moniteur de faux négatifs de détecteur mesuré sur matériel
- Constat :
  - le seul moniteur de personnes manquées du corpus (KGFP) n'a **aucune mesure de coût** :
    tête de 2,6 M de paramètres, plus un DINO ViT-B de 86 M en seconde passe ; « la latence
    vient surtout des backbones », sans chiffre de latence ni de FLOPs ; GPU non précisé
    (arxiv-2603.25499, §5.2, §6, chunk 2603.25499#026.1 ; preprint) ;
  - les moniteurs de classification ont un coût annoncé, jamais mesuré : ConfidNet « aussi
    rapide » que le réseau, sans chiffre, et un encodeur dupliqué après fine-tuning
    (arxiv-1910.04851, §2.2, §3.2) ; tête de sélection FC 512 + sigmoïde non chiffrée
    (arxiv-1901.09192, §6.3) ; prédiction conforme « légère » non mesurée
    (arxiv-2304.06052, §1) ;
  - l'outil le plus proche de la forme d'un tel moniteur (petit MLP en virgule fixe) est
    hls4ml : MLP de 4 389 paramètres, 75 ns, mais en estimation HLS, sur Kintex et pour la
    physique des particules (arxiv-1804.06913, Table 2, §3.3) ;
  - aucune ligne de `benchmarks.csv` ne porte sur un moniteur.
- Ce qui manque : un moniteur de faux négatifs (tête légère sur les features du détecteur)
  implanté à côté d'un YOLO INT8 sur SoC FPGA, avec LUT / DSP / BRAM, latence ajoutée et
  puissance, comparé à KGFP sur les mêmes étiquettes (COCO person, IoU 0,5).
- Statut : étayé (6 fiches) dans le corpus. **Hypothèse** pour la littérature : Yang et al.
  2021 (Sensors) et Yatbaz et al. (moniteur de couches précoces) ne sont pas dans la base.
- Piste : reproduire KGFP (code publié, Fraunhofer GitLab) avec une tête légère sans DINO,
  puis la passer en hls4ml ou en PL à côté du DPU de la KV260.

### Prédiction d'échec ciblée sur le faux négatif : un seul travail, moniteur externe sur détecteur gelé
- Constat :
  - KGFP est le seul papier qui prédit l'échec « personne manquée » d'un détecteur
    (arxiv-2603.25499, §3.1). Mais :
    - le détecteur est gelé, seul le moniteur est entraîné (§4) ;
    - la décision est prise au niveau de l'image, sans localisation (§5.1) ;
    - hors distribution, le rappel tombe à 34,2 % en moyenne sur COCO-O, alors que la
      conclusion annonce 85 % (fiche, Limites ; §5.1) ;
    - images isolées, pas de flux vidéo ni de taux d'alarme par heure (fiche, Limites) ;
  - les méthodes d'apprentissage conjoint existent, mais **en classification et avec un
    risque symétrique** : SelectiveNet apprend prédiction et rejet ensemble (risque 0/1,
    arxiv-1901.09192, §4) ; ConfidNet apprend la TCP sur les features du modèle (perte L2,
    erreur de classe quelconque, arxiv-1910.04851, §2) ;
  - la prédiction conforme sur YOLO ne couvre pas les faux négatifs (arxiv-2304.06052,
    §4.1-4.2) ; Gaussian YOLOv3 ne modélise que l'incertitude de localisation
    (arxiv-1904.04620) ;
  - aucun papier n'emploie une perte asymétrique qui pénalise le faux négatif d'une classe
    critique, alors que les guides la demandent (2020-easa §8.1.1 ; arxiv-2103.10529,
    §4.2.4.2).
- Ce qui manque : un moniteur entraîné **avec** le détecteur (perte conjointe, comme
  SelectiveNet), ciblé sur la personne manquée, localisé (par région ou par échelle de la
  FPN) et évalué sur flux (alarmes successives, délai de détection de l'échec).
- Statut : étayé (8 fiches).
- Piste : ajouter à un YOLOv8n une tête de sélection par échelle, entraînée conjointement
  avec une perte pondérée sur les personnes manquées ; comparer à KGFP (gelé, externe) sur
  COCO person et CrowdHuman.

### Sorties anticipées jamais utilisées comme alerte conservatrice
- Constat :
  - dans le corpus, une sortie anticipée sert à **gagner du temps** : BranchyNet sort si
    l'entropie du softmax est sous un seuil choisi « au coude » précision / temps, sur les
    données d'évaluation (arxiv-1709.01686, §III-C, §IV) ; MSDNet cale ses seuils sur max
    softmax pour un budget moyen, en supposant une probabilité de sortie constante
    (arxiv-1703.09844, §4.1) ;
  - aucun des deux ne mesure l'erreur parmi les échantillons sortis tôt (fiches, Limites) ;
    les deux sont en classification ; la détection est un travail futur
    (arxiv-1709.01686, §VI ; arxiv-1703.09844, §6) ;
  - un seuil de confiance suppose une confiance fiable, or :
    - les réseaux modernes sont surconfiants, ECE de 4 à 10 % (arxiv-1706.04599, §5,
      Table 1) ;
    - la calibration se dégrade sous décalage pour toutes les méthodes (arxiv-1906.02530,
      §5) ;
    - calibrer n'aide pas à prédire l'échec (arxiv-2403.02886, Table 1) ;
  - seul SelectiveNet donne un seuil avec une borne (calibration de la couverture, Hoeffding,
    arxiv-1901.09192, §5), en i.i.d. et sur une sortie unique ;
  - la règle de rejet de Chow et le cadre risque-couverture (arxiv-2403.02886, §3.3.2) sont
    transposables à un rejet « vers le réseau complet ou vers l'alarme » (déduit par la
    fiche).
- Ce qui manque : une sortie anticipée dont le rôle est inversé : signaler tôt un échec
  probable (personne manquée), avec un seuil réglé pour le rappel des échecs à taux de
  fausse alarme fixé, et une garantie de calibration (jeu séparé, borne de couverture).
- Statut : étayé (6 fiches) pour l'usage « raccourci de calcul » et l'absence d'usage
  conservateur dans le corpus. **Hypothèse** pour la littérature : les détecteurs à sorties
  anticipées récents ne sont pas dans la base.
- Piste : `/paper-discover "early exit object detection"` et « early exit uncertainty
  safety » ; question de thèse candidate : « une sortie anticipée peut-elle borner le délai
  d'alerte d'un échec de détection, sans raccourcir la décision nominale ? ».

### Pire cas temporel des sorties anticipées et délai de réaction de bout en bout
- Constat :
  - les gains des sorties anticipées sont des **moyennes** : 2 à 6 fois sur CPU et GPU, à
    batch 1 ; un lot plus grand réduit le gain (arxiv-1709.01686, Table I, Fig. 3) ; en
    mode anytime, le budget de MSDNet est une variable aléatoire, pas une borne
    (arxiv-1703.09844, §3) ;
  - le pire cas d'un réseau à sorties anticipées est le réseau complet plus les branches
    traversées (déduit, fiches arxiv-1709.01686 et arxiv-1703.09844) ;
  - la prémisse « calcul indépendant de l'entrée, donc WCET sans difficulté propre au ML »
    (arxiv-1905.04223, §7.4) ne tient plus avec des sorties anticipées (déduit) ;
  - KGFP propose de ne vérifier qu'une image sur N pour amortir le coût
    (chunk 2603.25499#026.1), ce qui allonge le délai de détection de l'échec, non étudié ;
  - le corpus n'a aucune mesure de délai de réaction de bout en bout (caméra → détection →
    moniteur → alarme) ; les seuls pire cas sont un OWCET observé sur CPU
    (arxiv-2406.12362, §V-B) et un WCET OTAWA sur une autre cible que celle mesurée
    (2022-de-albuquerque-silva-acetone) ;
  - l'axe `timing-analysis` ne contient aucun papier.
- Ce qui manque : une borne de délai de réaction pour un détecteur avec moniteur et sorties
  anticipées sur SoC FPGA, qui distingue chemin nominal, chemin d'alerte et interférences
  PS / PL (DDR partagée, post-traitement sur l'ARM).
- Statut : étayé (6 fiches) pour l'absence dans le corpus. **Hypothèse** pour la
  littérature, puisque l'axe `timing-analysis` est vide.
- Piste : `/paper-discover timing-analysis` (requête de base.json : « WCET analysis neural
  network inference FPGA SoC ») ; mesurer sur KV260 la distribution de latence avec et sans
  branche de sortie anticipée, sous charge du PS.

### Effet de la quantification sur la prédiction d'échec et les décisions critiques
- Constat :
  - **aucun travail de prédiction d'échec ou de calibration ne quantifie** : KGFP, ConfidNet,
    SelectiveNet, FMFP, temperature scaling, Ovadia (arxiv-2603.25499, arxiv-1910.04851,
    arxiv-1901.09192, arxiv-2403.02886, arxiv-1706.04599, arxiv-1906.02530 :
    « Plateforme », « Limites ») ; l'effet des minima plats sur la quantification est une
    hypothèse de la fiche d'arxiv-2403.02886 ;
  - côté FPGA, la quantification est évaluée sur des **moyennes** : rapport d'AUC
    99,68 % à `<16,6>` (arxiv-1804.06913, Table 2) ; mAP après PTQ INT8 avec des écarts
    imprévisibles selon le modèle (arxiv-2607.13106, Table II) ; FP16 / point fixe validés
    par tests (arxiv-2406.12362) ;
  - le seul résultat sur la **gravité** des erreurs : le réseau binarisé a une section
    efficace plus basse mais une part d'erreurs critiques de 38 % contre 26 %
    (2020-libano, §IV-B) ;
  - la MSP, base de nombreux seuils, dépend de la calibration des logits, que l'INT8 peut
    modifier (déduit par la fiche d'arxiv-1610.02136).
- Ce qui manque : mesurer, sur un détecteur de personnes, ce que l'INT8 / INT4 change (1) au
  taux de personnes manquées, au-delà de la mAP, (2) à la séparation du score du moniteur
  (AUROC d'échec, AURC) et (3) aux seuils des sorties anticipées calés en flottant.
- Statut : étayé (9 fiches). Question de thèse candidate, au croisement des rôles de
  M. Lauer et A. Dion (profile.md).
- Piste : sur le YOLOv8n de la piste précédente, comparer flottant, PTQ INT8 Vitis AI et
  QAT FINN : rappel des personnes, AUROC du moniteur, recalibration de la température par
  précision.

### Fiabilité matérielle du moniteur et redondance sélective guidée par le moniteur
- Constat :
  - les études SEU portent sur le réseau principal ; aucune n'injecte de fautes dans un
    moniteur ou dans une branche de sortie anticipée (arxiv-2404.01757, gaps de la fiche ;
    2019-libano ; arxiv-1912.07394) ;
  - la criticité est localisée (couche 0, premiers cycles, logique de contrôle :
    arxiv-2404.01757, §IV-B ; FC finale : 2019-libano, §V-C) et la réplication sélective
    coûte 49,87 à 173,47 % de MAC (arxiv-1912.07394, Table III) ;
  - les guides proposent moniteur de sortie, n-version et repli sûr (arxiv-1905.04223,
    §7.4.2 ; Doer / Checker, 2020-easa §6.6), sans coût ni couplage avec la redondance ;
  - la distinction entre erreur de perception (KGFP), anomalie d'exécution (SEU critique)
    et défaillance temporelle (crash par timeout, arxiv-2404.01757, Tables II-III) n'est
    faite par aucun papier dans un même cadre (déduit du croisement des fiches).
- Ce qui manque : une architecture où le moniteur déclenche la redondance (ré-exécution,
  TMR temporaire) seulement quand l'échec est probable, avec le moniteur lui-même durci et
  son taux de défaillance compté.
- Statut : **hypothèse** (5 fiches), car elle repose sur l'absence de travaux de ce type
  dans la base.
- Piste : campagne d'injection FREtZ (méthode d'arxiv-2404.01757) sur un moniteur hls4ml
  isolé, puis sur l'ensemble détecteur + moniteur en FINN.

## Détection de personnes en milieu industriel

Section nouvelle au 8e passage. L'axe `person-detection` ne compte que 5 fiches. Plusieurs
constats viennent aussi des fiches `safety-certification` et `yolo-fpga`.

### Pas de jeu de données ni de cas d'assurance pour la détection de personnes en zone industrielle
- Constat :
  - **jeux de personnes du corpus, aucun industriel** :
    - CrowdHuman : images web de foule ; la surveillance n'apparaît que comme mot-clé de
      collecte (§3.1) ; pas de vidéo, d'EPI ni de condition industrielle. Baselines lourdes
      (FPN, mMR 50,42, Table 7) (arxiv-1805.00123-crowdhuman-benchmark-detecting-human-crowd) ;
    - Re-ID : campus, rues, aéroports ; aucun jeu industriel, avec EPI ou uniformes
      (arxiv-2001.04193-deep-learning-person-re-identification, §4.3.1) ;
    - le seul jeu « personnes CCTV » d'un travail FPGA est un jeu maison (CCTV + VOC, 18 820
      images), non publié (arxiv-2607.13106, §III-A) ;
  - **exigences posées, sans jeu de données** :
    - occultations, lumière et poussière, sans critère quantitatif (2018-halme) ;
    - AMLAS donne l'exemple « identifier toute personne présente dans la zone définie »,
      sans étude de cas (arxiv-2102.01564, Ex. 7) ;
    - aucun cas de détection de personnes dans DEEL (§4.4.2.1) (arxiv-2103.10529) ;
  - le cas complet le plus proche, YOLO + ED-324 sur Jetson, porte sur des drones, sans
    métrique publiée ni complétude du jeu (arxiv-2406.12362, §I-A, §VI) ;
  - le cas ferroviaire de prédiction conforme (feux, 3 414 images) est l'analogue le plus
    proche d'un cas d'assurance de détection (arxiv-2304.06052, §2.2).
- Ce qui manque :
  - un jeu de personnes en zone industrielle : caméra fixe en hauteur, EPI (casque, gilet),
    occultation par machines, éclairage dégradé, personnes éloignées ;
  - un ODD décrit ;
  - un cas d'assurance (AMLAS) qui en dérive les exigences de données et de vérification.
- Statut : étayé (8 fiches) dans le corpus. **Hypothèse** pour la littérature : les jeux
  industriels et EPI publics (par exemple les jeux de détection de casques) ne sont pas
  dans la base.
- Piste : `/paper-discover "PPE detection dataset construction site helmet"` et « worker
  detection industrial safety dataset ». Rédiger un ODD d'exemple selon AMLAS, stage 1-2.

### Détecteurs de personnes quantifiés sur FPGA : un seul travail, sans métrique de non-détection
- Constat :
  - **un seul papier mesure un détecteur de personnes sur FPGA** : YOLOv8 / v11 / v26
    nano INT8 sur ZCU104. Il obtient mAP@0.5:0.95 de 0,66 à 0,79 sur un jeu de personnes et
    34,05 FPS de bout en bout, avec une puissance estimée par Vivado
    (arxiv-2607.13106, Table II, §IV-C ; preprint, jeu non publié) ;
  - les autres détecteurs FPGA du corpus portent sur des véhicules (2023-zhai, 2025-kim,
    arxiv-2609.24757), des défauts de PCB (2024-yan), VOC (2026-fata, 2024-zhang), des
    vignes (arxiv-2211.11647) ou des drones (2021-xu, arxiv-1909.09709) ;
  - TinyissimoYOLO inclut la classe « person » parmi 3 classes VOC, sur MCU
    (arxiv-2306.00001, Table II) ;
  - **les métriques sont des moyennes** :
    - mAP ;
    - mMR moyennée sur les FPPI, sans non-détection au pire cas (arxiv-1805.00123,
      Limites) ;
    - « accuracy » (2026-fata) ;
    - aucun taux de personnes manquées à taux de fausse alarme fixé, par distance ou par
      niveau d'occultation, **sur FPGA**. (9e passage) KGFP mesure le rappel des personnes
      parmi les images acceptées à 5 % de FPR (64,3 % → 84,5 % sur COCO val ; 34,2 % en
      moyenne sur COCO-O), mais sur GPU, YOLOv8l flottant, images isolées COCO
      (arxiv-2603.25499, §5.1 ; preprint) ;
  - CrowdHuman fournit des boîtes tête / visible / corps entier, signaux redondants pour un
    moniteur (déduit par la fiche, arxiv-1805.00123).
- Ce qui manque : un YOLO de personnes quantifié sur KV260, évalué sur CrowdHuman (ou un jeu
  industriel) par le rappel à FPPI fixé, par taille et par occultation. Il faut le faire
  sur la cible, pas seulement en logiciel.
- Statut : étayé (10 fiches).
- Piste : réentraîner un YOLOv8n à opérateurs compatibles DPU (recette d'arxiv-2607.13106)
  sur CrowdHuman. Mesurer le MR⁻² et le rappel à 0,1 FPPI sur KV260, en flottant et en INT8.

### Chaîne détection → suivi → ré-identification sur FPGA
- Constat :
  - suivi Deepsort sur l'ARM, FPS de bout en bout inconnu (2023-zhai, §3.3) ;
  - suivi en Python sur le PS, de 195 à 24 FPS (arxiv-2509.04153, §VI-C) ;
  - suivi SiamRPN++ avec SkyNet, mais sur GPU 1080Ti (arxiv-1909.09709, Tables 8-9) ;
  - Re-ID : la dimension embarquée n'est traitée qu'en quelques lignes, sans latence ni
    puissance (§4.3.5). La mise à jour incrémentale sur la cible est évoquée (§3.5,
    §4.3.4) (arxiv-2001.04193) ;
  - CoDeNet, détecteur sans NMS, est noté comme simplifiant la chaîne (déduit,
    arxiv-2006.08357).
- Ce qui manque : la partie « identification » du cas d'application. C'est une chaîne
  détection + suivi + Re-ID sur SoC FPGA, avec latence de bout en bout et énergie, et une
  analyse de ce que chaque étage apporte à la sûreté (vote temporel, persistance d'une
  personne entre images).
- Statut : étayé (4 fiches) pour l'absence de chaîne complète. Hypothèse pour la Re-ID
  sur FPGA (aucun papier).
- Piste : `/paper-discover "person re-identification FPGA"`. Mesurer d'abord un suivi simple
  (SORT) sur le PS de la KV260, à côté du DPU.

### Robustesse adverse des détecteurs de personnes quantifiés et embarqués
- Constat :
  - un patch imprimé d'environ 40 × 40 cm cache une personne à YOLOv2 en boîte blanche ;
    la transférabilité n'est pas quantifiée (arxiv-1904.08653, §4, §6) ;
  - le survey Re-ID mentionne la robustesse adverse sans l'évaluer (arxiv-2001.04193,
    §2.4.2) ;
  - le survey arxiv-1812.08342 recense des défenses, toutes logicielles et en classification ;
  - aucun papier n'étudie l'effet de la quantification INT8 / binaire ou de la compilation
    FPGA sur la vulnérabilité aux patchs, ni une défense à l'exécution compatible avec le
    temps réel embarqué.
- Ce qui manque : l'évaluation d'attaques physiques (patch, vêtement) sur un YOLO de
  personnes quantifié sur FPGA, et le comportement des moniteurs d'exécution face à elles.
- Statut : hypothèse (3 fiches). Volet *security*, secondaire selon profile.md.
- Piste : rejouer le patch d'arxiv-1904.08653 (code GitLab publié) sur le YOLO quantifié de
  l'expérience KV260, avec et sans moniteur.
