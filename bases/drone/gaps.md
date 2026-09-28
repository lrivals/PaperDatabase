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

Carte du 28/09/2026, **2ᵉ passe** : 73 fiches `done` et 324 lignes de benchmark (58 papiers).
La 1ʳᵉ passe, faite le même jour, ne reposait que sur l'état de l'art de départ.

**Portée des statuts.** « Étayé » signifie que plusieurs fiches constatent le manque dans les
papiers lus (mesure absente, limite reconnue par les auteurs). Cela ne prouve pas que le travail
n'existe nulle part. Le corpus compte 73 papiers et reste biaisé par la bibliographie de départ,
avec peu de papiers FPGA propres au drone. Un gap qui ne repose que sur l'absence d'un type de
papier dans la base reste une **hypothèse**.

### Chiffres de couverture (`benchmarks.csv`, 324 lignes)

| Constat | Valeur |
|---|---|
| Lignes avec `power_w` = n/r | 222 / 324 (69 %) |
| Portée de puissance renseignée | board 51 · chip 20 · unspecified 29 · estimated 2 |
| Lignes avec `latency_ms` = n/r | 243 / 324 (75 %) |
| Lignes avec une précision par taille d'objet (AP_S, mAP_small) | **0** |
| Papiers mesurés sur GPU / CPU de bureau | 31 · FPGA 10 · Jetson 14 · MCU / nano 10 · ASIC 1 · neuromorphique 2 · autre edge 3 |
| Jeux drone (VisDrone, UAVDT, DAC-SDC, Det-Fly, Anti-UAV…) mesurés sur cible embarquée | DAC-SDC (IoU mono-objet, 3 papiers), VisDrone restreint à la classe voiture (2025-cali), VisDrone sur TX2 sans puissance (2023-zhang-drone-yolo) ; **aucun jeu contre-drone air → air** |

Familles de plateformes déduites du texte libre de la colonne `platform` (regroupement
approximatif).

---

### Décalage algorithme / matériel
- Constat : les YOLO drone de l'état de l'art ne sont mesurés que sur GPU de bureau. C'est le cas
  de TPH-YOLOv5 (arxiv-2108.11539 ; 2023-zhao-tph-yolov5), Drone-YOLO (2023-zhang-drone-yolo, TX2
  sans puissance), GCL-YOLO (2023-cao), Efficient YOLOv7-Drone (2023-fu), DroneScan-YOLO
  (arxiv-2604.13278), DEAL-YOLO (arxiv-2503.04698) et YOLO-Drone (arxiv-2511.10905). Les
  implémentations FPGA du corpus restent sur YOLOv3-tiny, YOLOv4 ou YOLOX : 2025-cali, 2024-nguyen,
  2025-elhence. Frein structurel lu : FINN 0.10 ne gère pas les topologies FPN / PAN ni la tête P2
  (2025-cali, fiche « Gaps »). Nuance : arxiv-2607.13106 remplace l'attention par des blocs
  compatibles DPU, mais sans évaluation sur VisDrone ni mAP_small.
- Ce qui manque : le portage d'une tête P2 ou d'un bloc d'attention sur FPGA embarqué, avec une
  précision mesurée sur un jeu drone.
- Statut : **étayé**.
- Piste : Drone-YOLO-nano ou YOLOv8n-P2 en INT8 sur KV260 (Vitis AI), contre la même chose sous
  hls4ml / FINN ; mesurer le mAP VisDrone avant et après.

### Quantification et petits objets
- Constat : aucune des 324 lignes de benchmark ne rapporte d'AP_S ou de mAP_small. Dans les
  papiers qui quantifient, la perte n'est donnée que globalement :
  - 2024-nguyen : 6 à 7 points de mAP après PTQ, sans détail par taille ;
  - 2025-cali : 41,8 → 17,7 % de mAP, où l'architecture et le W4A4 sont confondus, sans ablation ;
  - 2024-zhang-dac-sdc et arxiv-1909.09709 (SkyNet, Table 7) : IoU moyen seulement ;
  - arxiv-2502.15737 : jusqu'à −12,3 points après INT8, en mAP global.

  Même dans les papiers dédiés aux petits objets, l'AP_S n'est pas rapporté :
  arxiv-2103.09136, arxiv-2112.10415, arxiv-2604.13278, 2025-yu-yolo-gcof, arxiv-2001.06303.
- Ce qui manque : le mAP_small en fonction de la précision numérique (FP32 → INT8 → INT4) et de
  la méthode (PTQ, QAT), sur VisDrone ou Det-Fly.
- Statut : **étayé**.
- Piste : balayage PTQ / QAT d'un YOLO drone sur VisDrone, avec rapport de l'AP_S (protocole
  COCO), sur la carte même.

### Haute résolution, tête P2 et mémoire on-chip
- Constat : la tête P2 produit des cartes de 160 × 160 (2023-zhang-drone-yolo, 2023-cao) et
  DroneScan travaille à 1280 px (arxiv-2604.13278). Le coût mémoire de ces choix n'est quantifié
  sur aucune cible embarquée. DEAL-YOLO (arxiv-2503.04698) retire P5 et ajoute P2 : les
  paramètres baissent, mais les activations augmentent vraisemblablement (déduit).
- Ce qui manque : la pression BRAM / URAM d'une tête P2 ou d'une entrée haute résolution sur SoC
  FPGA embarqué.
- Statut : **étayé** (coût non mesuré dans les papiers lus) ; l'absence de tout travail FPGA
  sur ce point reste une hypothèse.
- Piste : relevé des tailles d'activation par couche pour YOLOv8n et YOLOv8n-P2 ; comparer au
  budget BRAM d'un ZU3EG ou d'un KV260.

### Nombre de paramètres ou FLOPs ≠ latence sur cible *(nouveau)*
- Constat :
  - SF-YOLOv5 (2022-liu-sf-yolov5) : −68 % de paramètres pour seulement −7 % de latence GPU ;
  - F-YOLOv7 (2025-du, Table 2) : moins de FLOPs sans gain de débit ;
  - SlimYOLOv3 (arxiv-1907.11093) : FLOPs non proportionnels à la latence ;
  - YOLO-GCOF (2025-yu) : évalué seulement en GFLOPs, alors que la cible annoncée est un
    Raspberry Pi 4B.

  Ces quatre papiers mesurent sur GPU de bureau.
- Ce qui manque : la latence réelle des YOLO « légers » pour drone (GhostConv, depthwise,
  convolution creuse) sur FPGA, NPU ou MCU, là où l'effet peut s'inverser (déduit).
- Statut : **étayé**.
- Piste : trois variantes légères d'un même YOLO profilées sur KV260 (DPU) et Jetson Orin
  (TensorRT), à précision égale.

### Post-traitement sur le PS : un goulot de bout en bout *(nouveau)*
- Constat : les délais hors inférence dominent souvent le temps total.
  - 2025-cali (Table 10) : NMS + décodage des boîtes ≈ 26 ms, contre 6 ms d'inférence.
  - arxiv-2509.04153 (§VI-C) : le débit chute de 195 à 24 FPS quand le post-traitement tourne
    en Python sur le PS.
  - arxiv-2502.15737 (Table 5 contre Fig. 4) : le temps aller-retour du pipeline vaut 2 à 3 fois
    le temps d'inférence seul.
  - 2024-zhang-dac-sdc : le FPS 2022 exclut les E/S.
  - 2025-elhence : Soft-NMS sur le PS.
  - arxiv-2607.13106 (§V) : une tête sans NMS n'est annoncée qu'en perspective.
- Ce qui manque : un NMS matériel (ou une tête sans NMS) sur SoC embarqué, avec une latence
  mesurée de la caméra à la sortie.
- Statut : **étayé**.
- Piste : lire les références [67] et [86] de 2025-hozhabr (NMS pipeliné, système tout-FPGA) ;
  instrumenter le pipeline complet de 2025-cali.

### Calcul adaptatif ou épars jamais évalué à bord *(nouveau)*
- Constat : plusieurs méthodes concentrent le calcul sur les régions utiles pour les petits
  objets : tuilage SAHI (arxiv-2202.06934), requêtes éparses QueryDet (arxiv-2103.09136),
  clusters ClusDet (arxiv-1904.08008), coarse-to-fine UFPMP-Det (arxiv-2112.10415), early-exit
  BlankSkip (arxiv-2603.28149). Toutes sont mesurées sur GPU de bureau, sauf BlankSkip (GAP8,
  2 classes en intérieur). Aucune ne rapporte la latence au pire cas ni la gigue dans une scène
  dense (arxiv-2103.09136, arxiv-2603.28149).
- Ce qui manque : le coût réel (latence moyenne et au pire cas, énergie par image 4K) de ces
  schémas sur FPGA, Jetson ou nano.
- Statut : **étayé**.
- Piste : SAHI à tuiles fixes contre sauts de tuiles vides, sur KV260, à budget de temps fixe.

### Métriques non comparables
- Constat :
  - le protocole AP@0.7 d'UAVDT diffère de l'AP@0.5 repris ensuite (arxiv-1804.00518) ;
  - arxiv-2411.02582 évalue à un seuil IoU de 0,1 sur un jeu privé ;
  - DAC-SDC utilise l'IoU mono-objet (2024-zhang-dac-sdc, arxiv-1909.09709) ;
  - le split, la résolution et le nombre d'epochs VisDrone varient d'un papier à l'autre
    (arxiv-2511.10905) ;
  - chaque jeu contre-drone a ses propres annotations et métriques (arxiv-2103.17242) ;
  - la définition de la mAP change même entre les versions de TinyissimoYOLO
    (arxiv-2306.00001).

  Côté puissance, 69 % des lignes sont en n/r. Les puissances renseignées mêlent puce (GAP8,
  Loihi) et carte : 2018-flamand, arxiv-2303.08778, arxiv-1612.07119.
- Ce qui manque : un protocole commun (métrique, résolution, portée de la puissance).
- Statut : **étayé**.
- Piste : remplir `power_scope` systématiquement ; fixer une grille de mesure pour les
  expériences de la thèse.

### Benchmarks sans métrique d'efficacité *(nouveau)*
- Constat : les grands benchmarks du domaine ne donnent ni FPS ni puissance ni plateforme
  embarquée.
  - VisDrone 2018-2020 (arxiv-2001.06303, §8).
  - Anti-UAV (arxiv-2101.08466) et Anti-UAV410 (2024-huang).
  - WebUAV-3M (arxiv-2201.07425).
  - Det-Fly (2021-zheng), évalué sur GPU seulement.
  - Le survey arxiv-2507.10006 (§V-A) le signale lui-même : « Lack of Real-Time Benchmarking ».
- Ce qui manque : une piste « efficacité » (FPS, W, plateforme) dans les benchmarks drone et
  contre-drone.
- Statut : **étayé**.
- Piste : vérifier les éditions de VisDrone postérieures à 2021, que les auteurs annonçaient
  (arxiv-2001.06303, §8).

### Métrique système absente
- Constat : les papiers YOLO/FPGA donnent des FPS, parfois des W, mais jamais l'effet sur
  l'autonomie ni sur la vitesse de vol sûre : 2025-cali, 2025-elhence, 2024-zhang-dac-sdc,
  2024-nguyen. Le cadre existe :
  - MAVBench (arxiv-1905.06388) : temps de mission, énergie, vitesse sûre ;
  - le modèle F-1 (2020-krishnan, arxiv-2204.10898) ;
  - le modèle latence → vitesse max (arxiv-2110.05113, §S5).

  Aucun de ces cadres ne contient de FPGA. Côté nano, la part du calcul dans le budget énergie
  est mesurée : 1,67 % (arxiv-2301.12175, Table IV) ; décomposition masse et calcul
  (arxiv-1805.01831, Table IV). Aucun équivalent n'existe pour un module FPGA ou Jetson sur un
  drone de taille moyenne. 2021-guo propose une plateforme FPGA + GPU sans aucune mesure.
- Ce qui manque : traduire les FPS et W d'un accélérateur en vitesse de vol sûre et en
  autonomie. Relier aussi la précision de détection à la réussite de la mission : les modèles
  F-1 ignorent la qualité de perception (arxiv-2204.10898), et un réseau plus rapide peut moins
  bien suivre la cible (arxiv-2103.10873, Table IV : 135 Hz moins bon que 48 Hz).
- Statut : **étayé**.
- Piste : placer 2025-cali et 2025-elhence (FPS, W carte, masse de la carte) sur la roofline F-1
  (arxiv-2204.10898), avec le modèle de vitesse de arxiv-2110.05113.

### Fiabilité des accélérateurs de détection sur drone
- Constat : le survey 2022-ahmed (§5.2, §6) ne recense aucune étude d'injection de fautes ou de
  radiations sur un détecteur de type YOLO en contexte drone : seuls des CNN de classification
  sont cités. Le coût de la redondance (TMR, DPR) en autonomie n'y est pas quantifié, et le
  modèle cross-layer reste un concept. MAVBench cite les soft errors comme extension non
  réalisée (arxiv-1905.06388, §VI-C). arxiv-2205.07149 met en avant la sûreté du FPGA sans la
  confronter aux erreurs de configuration. L'axe `reliability` ne compte que 2 papiers.
- Ce qui manque : l'injection de fautes sur un accélérateur de détection pour drone, avec une
  métrique de mission.
- Statut : **étayé** (lu dans 2022-ahmed et arxiv-1905.06388 ; le corpus reste mince sur l'axe).
- Piste : `/paper-discover reliability` ; LIRMM (labs.md).

### Pas de comparaison entre gammes de puissance
- Constat : nano (GAP8, mW), FPGA (W) et Jetson (~10 W) ne sont presque jamais comparés sur la
  même tâche. TinyissimoYOLO (arxiv-2306.00001) évalue à 88 × 88 sur 3 classes, ce qu'aucun
  design FPGA du corpus ne reprend. La seule comparaison FPGA, Jetson et MCU sur une même tâche
  (2025-elhence : KV260, ZCU104, Jetson Nano, STM32H7) donne des chiffres MCU invraisemblables
  (15 FPS, « 0,28 TOPS »), relevés dans la fiche. Les surveys ne comparent pas les plateformes
  chiffres à l'appui (2025-hozhabr, arxiv-2205.07149).
- Ce qui manque : un banc unifié, où le même réseau et la même entrée sont mesurés sur les
  trois gammes avec la même portée de puissance.
- Statut : **étayé**.
- Piste : porter TinyissimoYOLO sur un petit FPGA (FINN ou hls4ml) et mesurer l'énergie par
  inférence à la puce, comme sur GAP8.

### Détection et navigation sur le même budget *(nouveau)*
- Constat : les accélérateurs du corpus ne traitent qu'une seule tâche. Navion
  (2019-suleiman) fait de la VIO à 2 mW, sans détection. Tiny-PULP-Dronet (arxiv-2407.02405) et
  PULP-Dronet (arxiv-1805.01831) font de la navigation mono-tâche. 2021-guo propose contrôle et
  vision sur une plateforme hétérogène, sans mesure. arxiv-2205.07149 envisage le partage du FPGA
  par reconfiguration partielle, sans évaluation.
- Ce qui manque : détection et navigation (ou VIO) sur un même accélérateur embarqué, avec
  mesure de l'interférence et de l'ordonnancement (WCET, PS-PL : arxiv-2509.04153, §III-B).
- Statut : **étayé**.
- Piste : lire les références de arxiv-2205.07149 sur la reconfiguration partielle.

### Suivi embarqué sans puissance ni FPGA *(nouveau)*
- Constat : les trackers aériens mesurés sur Jetson ne donnent que des FPS, ni W ni mode de
  puissance : SiamAPN++ (arxiv-2106.08816, 34,9 FPS sur Xavier), HiFT (arxiv-2108.00202, 31,2 FPS),
  TCTrack (arxiv-2203.01885). WebUAV-3M (arxiv-2201.07425, §5.6) montre que la précision chute
  sous 30 px en FP32, sans étude de quantification. Aucun tracker siamois ni transformer n'est
  porté sur FPGA ou MCU. D'après la fiche TCTrack, les poids dynamiques sont peu compatibles avec
  les flots à poids figés (déduit, à vérifier).
- Ce qui manque : un tracker aérien sur FPGA ou nano, avec énergie par image et précision
  mesurée sur la cible.
- Statut : **étayé**.
- Piste : HiFT (attention peu profonde sur de petites cartes) en candidat FPGA.

### Apprentissage continu à bord du drone
- Constat : aucun papier du corpus ; la base `fpga` couvre l'apprentissage continu embarqué hors
  drone.
- Statut : hypothèse (absence dans la base, qui ne prouve rien).
- Piste : `/paper-discover "continual learning UAV onboard"` ; `bin/pdb base scan --from fpga`.

### Contre-drone : évalué sur GPU de bureau
- Constat : les détecteurs anti-drone du corpus sont évalués sur GPU de bureau ou sur portable :
  - Liu 2021, YOLOv4 élagué (2021-liu-real-time-small-drones) ;
  - F-YOLOv7 (2025-du, RTX 4090) ;
  - YOLO-GCOF (2025-yu, GFLOPs seulement) ;
  - Gao 2024 (2024-gao, RTX 4060 portable) ;
  - Det-Fly (2021-zheng) ;
  - Dogfight (arxiv-2103.17242, sans FPS) ;
  - MAV-VID (arxiv-2103.13933, GPU non précisé).

  Seul travail FPGA : 2024-nguyen (ZCU104), mais en sol → air, avec une puissance n/r mesurée à
  la prise d'un kit de développement. arxiv-2411.02582 mesure sur Jetson avec TensorRT, sans
  latence par étage.
- Ce qui manque : un détecteur anti-drone mesuré sur matériel embarqué (FPS, puissance carte,
  AP sur un jeu air → air).
- Statut : **étayé**.
- Piste : YOLOv8n entraîné sur Det-Fly, INT8 sur KV260, contre Jetson Orin, avec puissance à
  la carte des deux côtés.

### Détecteur air → air embarqué sur intercepteur *(nouveau, principal gap contre-drone)*
- Constat : sur 17 papiers contre-drone, 11 portent le tag `ground-to-air`. Les références
  air → air (Det-Fly 2021-zheng, Dogfight arxiv-2103.17242, arxiv-2312.11008) n'ont pas de coût
  embarqué mesuré. Les deux surveys le confirment : aucun des travaux qu'ils citent ne rapporte
  de plateforme embarquée ni de puissance (arxiv-2507.10006, arxiv-2504.11967). Le survey UZH
  (arxiv-2301.01755, §VIII) cite la détection d'adversaires air → air à haute vitesse comme
  question ouverte. Il manque aussi un jeu air → air multi-classes (oiseaux, avions) pour mesurer
  les fausses alarmes d'un intercepteur (2024-gao).
- Ce qui manque : un détecteur air → air sur SoC embarqué, avec AP, FPS, W et latence de bout
  en bout.
- Statut : **étayé**.
- Piste : c'est la question de thèse la plus nette de la base. Commencer par Det-Fly sur
  KV260.

### Fusion multi-capteurs contre-drone sur matériel embarqué
- Constat : la fusion IR + visible + audio de arxiv-2007.07396 tourne sur un portable au sol.
  À bord d'un drone porteur, l'audio est vraisemblablement inutilisable à cause du bruit des
  hélices (déduit, fiche arxiv-2007.07396). Le coût de deux détecteurs en parallèle n'est pas
  mesuré. La fusion RGB-IR non alignée d'Anti-UAV reste proposée sans être traitée
  (arxiv-2101.08466).
- Ce qui manque : un pipeline de fusion visible + thermique sous contrainte de puissance à bord.
- Statut : hypothèse (un seul papier de fusion, sol → air).
- Piste : `/paper-discover "RGB thermal fusion drone detection onboard"`.

### Air → air : coût du mouvement multi-frame
- Constat : en air → air, les méthodes les plus précises exploitent le mouvement : Dogfight
  (I3D sur des fenêtres de 8 frames, arxiv-2103.17242), arxiv-2312.11008 (DNN + mouvement) et
  arxiv-2411.02582 (YOLO + flot optique + Kalman). Aucune ne donne la latence par étage ni un
  portage FPGA. La soustraction de fond ne fonctionne pas avec une caméra en mouvement
  (2020-seidaliyeva, 2025-du, 2023-zheng-mavs).
- Ce qui manque : une architecture embarquée qui tienne le tampon temporel et la compensation
  d'ego-motion, avec une mesure par étage.
- Statut : **étayé** (coût non mesuré dans les 3 papiers) ; l'architecture FPGA reste une
  hypothèse.
- Piste : profiler le pipeline de arxiv-2411.02582 sur Jetson, étage par étage ; estimer le
  tampon on-chip de 8 frames à 640 px.

### Code et bitstreams rarement publiés
- Constat : d'après un relevé automatique de la section « Plateforme » des fiches, environ 42
  sur 73 disent le code non publié, 22 pointent vers un dépôt, et 9 sont indéterminées (relevé
  approximatif, à vérifier). Aucun bitstream FPGA n'est signalé comme publié dans les fiches FPGA
  lues (2025-cali, 2025-elhence, 2024-nguyen, 2024-zhang-dac-sdc).
- Ce qui manque : des implémentations embarquées reproductibles.
- Statut : étayé (relevé approximatif).
- Piste : distinguer « code d'entraînement » et « design matériel » lors des prochaines fiches.
