# État de l'art de départ — vision embarquée sur drone

> **Statut : source de départ, non vérifiée.** Texte fourni le 2026-09-28, rédigé à partir de
> résumés, extraits et pages d'éditeur seulement. Les ⚠️ et les chiffres restent à vérifier
> sur les papiers ingérés (fiches `done`, `benchmarks.csv`). Ne pas citer ce document comme
> source : citer le papier.

---

## 1. Benchmarks et challenges de référence

| Réf. | Contenu | Pourquoi c'est central |
|---|---|---|
| Zhu, Wen, Du, Bian, Fan, Hu, Ling, *Detection and Tracking Meet Drones Challenge*, IEEE TPAMI 44(11), 2022 — arXiv 2001.06303 | VisDrone, avec quatre pistes : détection sur image, détection vidéo, suivi mono-objet et multi-objets | C'est le dataset de facto pour les YOLO « drone » |
| Xu, Zhang, Yu, Hu, Rowen, Hu, Shi, *DAC-SDC Low Power Object Detection Challenge for UAV Applications*, IEEE TPAMI 43(2), 2021 — DOI 10.1109/TPAMI.2019.2932429 | 95 catégories, 150k images ; plateformes TX2 et PYNQ-Z1 ; plus de 110 équipes de 12 pays | C'est le **seul benchmark qui impose un FPGA** et mesure l'énergie |
| Zhang J. et al., *A comprehensive analysis of DAC-SDC FPGA low power object detection challenge*, Sci. China Inf. Sci., 2024 — DOI 10.1007/s11432-023-3958-4 | Analyse de cinq éditions du challenge, centrée sur le co-design algorithme/matériel sur plateformes edge pour images d'UAV | Sert de survey FPGA/drone |
| Jia, Xu, Hu et al., *Low-power object-detection challenge on unmanned aerial vehicles*, Nat. Mach. Intell. 4, 2022 | Commentaire sur le challenge (cité dans l'analyse SCIS) | Non lu |
| Huang et al., *Anti-UAV410*, IEEE TPAMI 46(5), 2024 ; Zhang et al., *WebUAV-3M*, IEEE TPAMI 45(7), 2023 | Benchmarks de suivi : infrarouge thermique anti-drone pour l'un, suivi UAV à l'échelle du million pour l'autre | Axe tracking et anti-drone |
| ⚠️ Du et al., *The Unmanned Aerial Vehicle Benchmark: Object Detection and Tracking* (UAVDT), ECCV 2018 | Véhicules vus de drone | Deuxième dataset standard |

## 2. YOLO (et assimilés) déployés sur FPGA pour drone — le cœur de ta thèse

| Réf. | Modèle / quantif. | Plateforme | Performances | Dataset / toolflow | Code |
|---|---|---|---|---|---|
| **SkyNet** — Zhang X. et al., MLSys 2020, arXiv 1909.09709 | Réseau bottom-up type YOLO. 12 couches conv, 1,82 Mo de paramètres | Ultra96 + TX2 | IoU 0,716 à 25,05 FPS sur Ultra96 ; IoU 0,731 à 67,33 FPS sur TX2. Puissance : n.d. dans les extraits | DAC-SDC ; HLS | Oui (GitHub) |
| **Calì, Falaschetti, Biagetti**, *Optimized Implementation of YOLOv3-Tiny…*, Electronics 14(20), 2025 — DOI 10.3390/electronics14203993 | YOLOv3-tiny, QAT Brevitas | Zynq-7020 (Z-turn) | 208 FPS à 200 MHz pour 2,55 W ; FPS/W 3 à 7× supérieur aux autres FPGA de la littérature ; vitesse proche d'un Coral Edge TPU | VisDrone (classe « car » seule) ; **FINN** | n.d. |
| **Nguyen, Nguyen, Le, Nguyen**, *FPGA-SoC implementation of YOLOv4 for flying-object detection*, JRTIP 21(3), 2024 — DOI 10.1007/s11554-024-01440-w | YOLOv4 | FPGA-SoC | Non lu (article en accès fermé) | Détection anti-drone | ? |
| **Elhence, Panda, Chamola, Sikdar**, *FPGA-Accelerated YOLOX With Enhanced Attention Mechanisms for Real-Time Wildfire Detection on AAVs*, IEEE TIM 74, 2025 — DOI 10.1109/TIM.2025.3556164 | YOLOX + attention | FPGA (n.d.) | Non lu | Feux de forêt | ? |
| **SATAY** — Montgomerie-Corcoran, Toupas, Yu, Bouganis, ICFPT 2023, arXiv 2309.01587 | YOLOv3 à v8, architecture streaming entièrement on-chip, DSE automatique | Plusieurs FPGA | Performances et énergie jugées compétitives face aux GPU | Pas spécifique drone ; toolflow | ? |
| **Yu & Bouganis**, *A Parameterisable FPGA-Tailored Architecture for YOLOv3-Tiny*, ARC 2020 — DOI 10.1007/978-3-030-44534-8_25 | YOLOv3-tiny | Zedboard (Z-7020) | Latence 290× meilleure que le processeur ARM ; mAP 30,9 % contre 33,4 % | COCO ; HLS | Oui, bitstream inclus |
| **[preprint]** *No Attention, No Problem: DPU-Aware Attention Approximation in Modern YOLO on FPGA*, arXiv 2607.13106, 2026 | YOLO récent avec attention | DPU Vitis AI | Non lu | Titre seulement | ? |

**Lecture critique :**
- Chez Calì et al., les chiffres de précision sont problématiques. Après pruning, la précision tombe de 67,06 % à 48,16 % et le rappel de 38,44 % à 17,16 %. Les chiffres de débit sont aussi incohérents : le texte mentionne 134 FPS atteints avec un driver bare-metal, contre 208 FPS dans le résumé. Il faut donc vérifier la configuration exacte.
- SkyNet et DAC-SDC utilisent de l'**IoU mono-objet**, pas du mAP multi-classe. Ce n'est donc pas comparable aux résultats VisDrone.

## 3. YOLO « spécialisés drone » (évalués surtout sur GPU de bureau)

| Réf. | Base | Idée clé | Résultat annoncé |
|---|---|---|---|
| **SlimYOLOv3** — Zhang, Zhong, Li, ICCVW 2019 — DOI 10.1109/ICCVW.2019.00011 | YOLOv3 | Pruning de canaux par régularisation L1 | −90,8 % de FLOPs, −92 % de paramètres, ~2× plus rapide, précision comparable (VisDrone2018) |
| **TPH-YOLOv5** — Zhu, Lyu, Wang, Zhao, ICCVW 2021 — DOI 10.1109/ICCVW54120.2021.00312 | YOLOv5 | Tête supplémentaire, têtes Transformer, CBAM | AP 39,18 % sur DET-test-challenge ; 5e à VisDrone 2021 |
| **TPH-YOLOv5++** — Zhao, Liu, Lyu, Wang, Zhang, Remote Sensing 15(6), 2023 — DOI 10.3390/rs15061687 | TPH-YOLOv5 | Transformer asymétrique inter-couches | Non lu |
| **Drone-YOLO** — Zhang Z., Drones 7(8), 2023 — DOI 10.3390/drones7080526 | YOLOv8 | RepVGG, fusion « sandwich », tête petits objets | +13,4 % mAP50 sur VisDrone-test ; version tiny à 5,25 M paramètres |
| **Efficient YOLOv7-Drone** — Fu, Wei, Yuan, Liang, Bo, Drones 7(10), 2023 — DOI 10.3390/drones7100616 | YOLOv7 | Suppression de la tête P5, ajout d'une tête P2 | Non lu |
| **GCL-YOLO** — Cao, Bao, Shang, Yuan, Cheng, Remote Sensing 15(20):4932, 2023 | YOLO | Réseau allégé à base de GhostConv | Non lu |
| **SF-YOLOv5** — Liu, Sun, Gu, Deng, Sensors 22(15):5817, 2022 | YOLOv5 | Fusion de features allégée pour petits objets | Non lu |
| **Improved YOLOv5** — Jung & Choi, Applied Sciences 12(14), 2022 — DOI 10.3390/app12147255 | YOLOv5 | Conditions variées | Non lu |
| YOLOv8n petits objets, Int. J. Comput. Intell. Syst., 2024 (auteurs non relevés, à vérifier) | YOLOv8n | Couche de détection supplémentaire, CondConv, Wise-IoU | 37,6 % mAP pour 3 M paramètres (VisDrone) |
| **[preprint]** YOLO-Drone, arXiv 2304.06925 | Darknet59 | MSPP-FPN, perte GIoU | 53 FPS et mAP 34,04 % sur UAVDT |
| **[preprint]** YOLO-Drone (GhostHead), arXiv 2511.10905 | YOLOv11n | Tête Ghost | +0,5 point de mAP50 seulement (gain marginal) |
| **[preprint]** DroneScan-YOLO, arXiv 2604.13278 | YOLOv8 | Redondance, objets minuscules | Souligne que le stride minimal de 8 px de YOLOv8 pénalise les très petits objets |
| **[preprint]** DEAL-YOLO, arXiv 2503.04698 | YOLO | Localisation d'animaux | Non lu |

## 4. Hors YOLO (à connaître pour situer ta thèse)

- **UFPMP-Det** — Huang, Chen, Huang, AAAI 2022 — DOI 10.1609/aaai.v36i1.19986. Détecteur efficace sur imagerie drone. Vérifié via une liste de références.
- **HRFPN** — Chen et al., IEEE TCSVT 2020. FPN haute résolution pour petits objets. Vérifié via une liste de références.
- ⚠️ **SAHI** — Akyon, Altinuc, Temizel, ICIP 2022. Slicing à l'inférence, très utilisé avec YOLO sur VisDrone.
- ⚠️ **QueryDet** — Yang, Huang, Wang, CVPR 2022, et **ClusDet** — Yang et al., ICCV 2019. Détection en cascade ou sur régions pour petits objets.
- ⚠️ **DroNet** (navigation) — Loquercio et al., IEEE RA-L 2018. Et sa version MCU **PULP-DroNet** — Palossi et al., IEEE IoT Journal 2019, sur GAP8. C'est **le pont direct avec ton profil TinyML**.
- ⚠️ **HiFT** — Cao et al., ICCV 2021. Suivi aérien temps réel (labo de C. Fu, Tongji).

## 5. Gaps repérés (déductions, à confirmer par lecture)

1. **Décalage algorithme/matériel.** Les YOLO drone SOTA (têtes P2, Transformer, CBAM) ne semblent presque jamais portés sur FPGA. Les implémentations FPGA restent sur YOLOv3/v4-tiny.
2. **Quantification et petits objets.** Aucune étude trouvée mesurant l'effet INT8/INT4 sur le mAP_small de VisDrone. Calì et al. suggèrent une forte chute du rappel.
3. **Haute résolution.** Tiling type SAHI et tête P2 impliquent de grandes feature maps, donc une forte pression sur la BRAM. Je n'ai trouvé aucun travail FPGA sur ce point.
4. **Métriques non comparables.** On mélange IoU mono-objet (DAC-SDC), mAP VisDrone et FPS sans puissance mesurée à la carte.
5. **Apprentissage continu à bord du drone.** Rien trouvé dans cette recherche, ce qui ne prouve pas que ça n'existe pas.

## Pistes de suite
1. **Lire** SkyNet puis l'analyse DAC-SDC de SCIS 2024 : c'est la meilleure entrée sur le co-design FPGA/drone.
2. **Reproduire** Calì et al. (Brevitas + FINN sur Zynq-7020, VisDrone « car »), en mesurant proprement mAP, puissance et latence. Cela correspond directement à ton expérience en QAT INT8.
3. **Expérience originale** : Drone-YOLO-nano ou YOLOv8n-P2 en INT8 via Vitis AI sur KV260, comparé à un Jetson Orin Nano. Le rapporter en mAP_small VisDrone et en GOPS/W. Cela attaque directement les gaps 1 et 2.

---

# Volet électronique et architecture de calcul pour drones

## Plan proposé pour l'état de l'art

| Axe | Contenu | Où en est la biblio |
|---|---|---|
| A. Perception IA | YOLO drone, petits objets, datasets | §1–4 ci-dessus |
| B. Accélérateurs embarqués | FPGA, ASIC, MCU parallèle, neuromorphique | Ci-dessous |
| C. Co-design système drone | Calcul ↔ énergie ↔ dynamique de vol | Ci-dessous |
| D. Fiabilité du calcul embarqué | Erreurs matérielles, sûreté | Ci-dessous |

## B. Accélérateurs matériels embarqués sur drone

| Réf. | Type | Tâche | Chiffres clés |
|---|---|---|---|
| **Navion** — Suleiman, Zhang, Carlone, Karaman, Sze, IEEE JSSC 54, 2019, pp. 1106–1119 — DOI 10.1109/JSSC.2018.2886342 (version VLSI 2018 : DOI 10.1109/VLSIC.2018.8502279) | ASIC 65 nm | Odométrie visuelle-inertielle (VIO) pour nano-drone | Stéréo 752×480 à 20 fps pour 2 mW en moyenne ; pic à 171 fps pour 24 mW. Compression et sparsité réduisent la mémoire on-chip de 4,1×. Présenté comme le premier système VIO entièrement intégré en ASIC |
| **PULP-DroNet** — Palossi, Loquercio, Conti, Flamand, Scaramuzza, Benini, IEEE IoT J 6(5), 2019, pp. 8357–8371 — DOI 10.1109/JIOT.2019.2917066 | MCU parallèle RISC-V (GAP8) | Navigation CNN end-to-end, Crazyflie 27 g | DroNet à 6 fps pour 64 mW, jusqu'à 18 fps pour ~3,5 % du budget de puissance du drone. Code, datasets et réseaux publiés |
| ⚠️ Flamand et al., *GAP-8: A RISC-V SoC for AI at the Edge of the IoT*, IEEE ASAP 2018 | SoC | Plateforme | Cité dans les références ; non lu |
| **Lamberti et al.**, *Bio-inspired Autonomous Exploration Policies with CNN-based Object Detection on Nano-drones*, DATE 2023 ; et *Tiny-PULP-Dronets*, AICAS 2022 | GAP8 / GAP9 | Détection + navigation multi-tâches | Selon des slides (source secondaire) : détection à 1,6 Hz sur GAP8 contre 11 Hz sur GAP9 |
| **[preprint]** Marra, Motetti, Burrello, Macii, Poncino, Jahier Pagliari, *BlankSkip*, arXiv 2603.28149 | GAP8 (Crazyflie 2.1) | Détection avec early-exit | +24 % de débit moyen pour une perte de 0,015 mAP face à un MobileNet-SSD statique |
| **Paredes-Vallés, Hagenaars, Dupeyroux, Stroobants, Xu, de Croon**, *Fully neuromorphic vision and control for autonomous drone flight*, Science Robotics 9(90), 2024 — DOI 10.1126/scirobotics.adi0591 | Neuromorphique (Loihi) + caméra événementielle | Égo-mouvement → commandes de vol | SNN de 28 800 neurones à 200 Hz ; 0,94 W au repos, plus seulement 7 à 12 mW pour exécuter le réseau |
| Vitale, Renner, Nauer, Scaramuzza, Sandamirskaya, *Event-driven vision and control for UAVs on a neuromorphic chip*, ICRA 2021 | Neuromorphique | Contrôle | Vérifié via une liste de références ; non lu |
| DAC-SDC, SkyNet, Calì et al. | FPGA | Détection | Voir §2 |

**Remarque critique sur Paredes-Vallés et al. :** l'essentiel de la puissance (0,94 W) est de la consommation statique du chip Loihi. Le gain énergétique affiché n'est donc réel que si ce coût de repos est amorti.

## C. Co-design système : calcul, énergie et vol

| Réf. | Apport | Pourquoi c'est important pour toi |
|---|---|---|
| **MAVBench** — Boroujerdian, Genc, Krishnan, Cui, Faust, Janapa Reddi, IEEE/ACM MICRO 2018, pp. 894–907 | Simulateur en boucle fermée et suite de benchmarks. Met en évidence une relation inattendue entre calcul et énergie totale du drone ; une conception efficace améliore la consommation batterie jusqu'à 1,8× | Justifie qu'un accélérateur plus efficace allonge **l'autonomie de vol**, pas seulement le débit |
| **F-1 roofline** — Krishnan, Wan, Bhardwaj, Whatmough, Faust, Wei, Brooks, Janapa Reddi, IEEE Computer Architecture Letters 19(1), 2020, pp. 38–42 | Modèle « roofline » liant fréquence capteur, performance de calcul et dynamique du drone | Relie les FPS de YOLO à la vitesse de vol sûre |
| Krishnan, Wan, Bhardwaj, Jadhav, Faust, Janapa Reddi, *Roofline Model for UAVs*, ISPASS 2022, pp. 162–174 — arXiv 2204.10898 | Validation en vol réel du F-1 : erreur de 5,1 à 9,5 % ; outil web Skyline | Outil directement réutilisable |
| ⚠️ Wan, Lele, Yu, Liu, Wang, Reddi, Hao, Raychowdhury, *Robotic computing on FPGAs: current progress, research challenges, and opportunities*, 2022 (probablement IEEE AICAS, à vérifier) | Survey FPGA pour la robotique | Cadre général FPGA/robotique |
| P. Xu, *FPGA-based UAV Heterogeneous Computing Platform Architecture*, ICCIA 2021 — DOI 10.1109/ICCIA52886.2021.00056 | Architecture hétérogène FPGA pour drone | Non lu ; prénom de l'auteur incomplet |

## D. Fiabilité du calcul embarqué

- **Ahmed & Jenihhin**, *A Survey on UAV Computing Platforms: A Hardware Reliability Perspective*, Sensors 22(16):6286, 2022 — DOI 10.3390/s22166286 (open access).
  - Le survey note que la fiabilité matérielle des plateformes de calcul UAV était négligée par les revues précédentes, et propose un modèle de fiabilité cross-layer.
  - Il décompose le drone en modules : calculateur de vol, communication, GPS et payload de calcul intensif (accélérateur de réseaux de neurones). Les erreurs matérielles, transitoires ou permanentes, y provoquent des défaillances.
  - C'est un bon point d'entrée vers les labos « test et sûreté », dont le LIRMM, qui est très fort sur ce sujet.

## Gaps transverses (déductions à confirmer)

1. **Métrique système absente.** Les papiers YOLO/FPGA donnent des FPS et des FPS/W, mais pas l'impact sur l'autonomie ou la vitesse de vol sûre. Or MAVBench et F-1 fournissent précisément ce cadre.
2. **Fiabilité des accélérateurs YOLO sur FPGA embarqué.** Les erreurs transitoires dans la mémoire de configuration ou les BRAM ne sont traitées dans aucun des travaux YOLO/drone trouvés.
3. **Pas de comparaison unifiée entre gammes.** Nano (GAP8, mW), FPGA (W) et Jetson (~10 W) ne sont jamais comparés sur la même tâche de détection.
4. **La détection d'objets reste le maillon faible sur nano-drone** : de l'ordre de 1 à 10 Hz.

## Pistes de suite

1. **Lire** Ahmed & Jenihhin (open access) puis MAVBench. Ces deux textes donnent la problématique « système » qui manque aux papiers YOLO.
2. **Expérience** : prendre l'accélérateur YOLOv3-tiny de Calì et al. et le passer dans le modèle F-1/Skyline, pour traduire ses FPS en vitesse de vol sûre face à un Jetson. Ce serait une contribution originale et peu coûteuse.
3. **Contact labo** : le LIRMM (équipes test/fiabilité) correspond bien au gap 2 et se trouve à Montpellier.

---

# Listes 3 et 4 — contre-drone et autres fonctions d'IA embarquée

> Même statut que ci-dessus : résumés, extraits et pages d'éditeur uniquement, texte fourni le
> 2026-09-28. ⚠️ = à vérifier ; **[preprint]** = non revu par les pairs.

**Remarque de cadrage :** en anti-drone, la plupart des travaux supposent un capteur **au sol**. Pour ta thèse, il faut distinguer le **sol → air** (station fixe) de l'**air → air** (le détecteur est embarqué sur un drone intercepteur). C'est ce second cas qui relève vraiment de l'IA embarquée.

## Liste 3 — Contre-drone (anti-UAV) par IA

**Benchmarks et surveys**

| Réf. | Type | Contenu |
|---|---|---|
| Jiang, Wang, Peng, Yu, Wang, Xing, Li, Guo, Ye, Jiao, Zhao, Han, *Anti-UAV: A Large-Scale Benchmark for Vision-Based UAV Tracking*, IEEE TMM 25, 2023, pp. 486–500 | Sol → air, RGB + IR | Plus de 300 paires de vidéos et 580k boîtes annotées ; tracker DFSC ; code GitHub |
| Huang et al., *Anti-UAV410*, IEEE TPAMI 46(5), 2024 | Infrarouge thermique | Suivi de drones (déjà cité) |
| Svanström, Englund, Alonso-Fernandez, *Real-Time Drone Detection and Tracking With Visible, Thermal and Acoustic Sensors*, ICPR 2020 (publié 2021), pp. 7265–7272 — DOI 10.1109/ICPR48806.2021.9413241 | Multi-capteurs | La caméra thermique fait aussi bien que le visible malgré une résolution plus faible ; la fusion réduit les fausses alarmes. Dataset de 650 vidéos IR/visible (drones, oiseaux, avions, hélicoptères) + audio, sur Zenodo |
| Isaac-Medina, Poyser, Organisciak, Willcocks, Breckon, Shum, *Unmanned aerial vehicle visual detection and tracking using deep neural networks: A performance benchmark*, ICCVW 2021, pp. 1223–1232 | Benchmark | Non lu |
| **[preprint]** *Securing the Skies: A Comprehensive Survey on Anti-UAV Methods, Benchmarking, and Future Directions*, arXiv 2504.11967 | Survey | Non lu |
| **[preprint]** *Vision-Based Anti Unmanned Aerial Technology: Opportunities and Challenges*, arXiv 2507.10006 | Survey | Non lu |

**Air → air (drone qui détecte un drone)** : le plus pertinent pour l'embarqué.

| Réf. | Apport |
|---|---|
| Zheng, Chen, Lv, Li, Lan, Zhao, *Air-to-Air Visual Detection of Micro-UAVs: An Experimental Evaluation of Deep Learning*, IEEE RA-L 6(2), 2021, pp. 1020–1027 — DOI 10.1109/LRA.2021.3056059 | Dataset **Det-Fly** (plus de 13 000 images d'un drone cible filmé par un autre drone) et évaluation de 8 détecteurs deep learning |
| Ashraf, Sultani, Shah, *Dogfight: Detecting Drones from Drones Videos*, CVPR 2021 — DOI 10.1109/CVPR46437.2021.00699 | Méthode en deux étapes avec attention spatio-temporelle, frontières de mouvement et I3D sur des cuboïdes de 8 frames. **Très coûteux : ce n'est pas embarquable tel quel** |
| Guo, Zheng, Zhang, Gao, Zhao, *Global-Local MAV Detection under Challenging Conditions based on Appearance and Motion*, IEEE T-ITS 25(9), 2024 | Apparence + mouvement ; non lu |
| Zheng et al., *Detection, localization, and tracking of multiple MAVs with panoramic stereo camera networks*, IEEE TASE, 2022 | Non lu |
| **[preprint]** *Real-Time Detection for Small UAVs: Combining YOLO and Multi-frame Motion Analysis*, arXiv 2411.02582 | Non lu |

**Détecteurs YOLO anti-drone (légers ou matériels)**

| Réf. | Modèle | Plateforme |
|---|---|---|
| Nguyen, Nguyen, Le, Nguyen, *FPGA-SoC implementation of YOLOv4 for flying-object detection*, JRTIP 21(3), 2024 — DOI 10.1007/s11554-024-01440-w | YOLOv4 | **FPGA-SoC**, le seul trouvé |
| Liu, Fan, Ouyang, Li, *Real-time small drones detection based on pruned YOLOv4*, Sensors, 2021 | YOLOv4 élagué | Non lu |
| Du, Wu, Dai, Xie, Hu, Wei, *F-YOLOv7: fast and robust real-time UAV detection*, Computing 107(1), 2025 | YOLOv7 | Non lu |
| Yu & Mo, *YOLO-GCOF: A lightweight low-altitude drone detection model*, IEEE Access, 2025 | YOLO allégé | Non lu |
| Gao, Tang, Li, Wang, Qiu, Chen, Mei, *A novel dataset and detection method for unmanned aerial vehicles using an improved YOLOv9 algorithm*, Sensors 24(23):7512, 2024 | YOLOv9 | Non lu |
| Seidaliyeva, Akhmetov, Ilipbayeva, Matson, *Real-time and accurate drone detection in a video with a static background*, Sensors 20(14):3856, 2020 | Non lu | — |

**Gaps contre-drone (déductions) :**
- Presque tous les détecteurs sont évalués sur GPU de bureau. Un seul travail FPGA a été trouvé, et il est en accès fermé.
- La fusion multi-capteurs (Svanström) n'a jamais été implémentée sur matériel embarqué dans les travaux trouvés.
- En air → air, les méthodes les plus précises exploitent le mouvement multi-frame, ce qui est coûteux en mémoire. C'est une vraie question d'architecture pour un FPGA.

## Liste 4 — Autres fonctionnalités d'IA embarquée sur drone

| Fonction | Réf. | Plateforme / chiffres |
|---|---|---|
| **Vol agile en environnement inconnu** | Loquercio, Kaufmann, Ranftl, Müller, Koltun, Scaramuzza, *Learning High-Speed Flight in the Wild*, Science Robotics 6(59), 2021 — DOI 10.1126/scirobotics.abg5810 | CNN entraîné uniquement en simulation par imitation d'un expert privilégié ; transfert zero-shot en forêt dense, sur neige et dans des bâtiments effondrés. Capteurs et calcul entièrement à bord ; code et données publiés |
| **Course de drones** | Kaufmann, Bauersfeld, Loquercio, Müller, Koltun, Scaramuzza, *Champion-level drone racing using deep reinforcement learning*, Nature 620, 2023, pp. 982–987 — DOI 10.1038/s41586-023-06419-4 | Swift : RL en simulation + données réelles, bat trois champions humains en course réelle en ne s'appuyant que sur les capteurs embarqués |
| Course (survey) | Hanover, Loquercio, Bauersfeld, Romero, Penicka, Song, Cioffi, Kaufmann, Scaramuzza, *Autonomous Drone Racing: A Survey*, IEEE T-RO 40, 2024, pp. 3044–3067 | Survey |
| **Suivi d'objet aérien** | Cao, Fu, Ye, Li, Li, *HiFT: Hierarchical Feature Transformer for Aerial Tracking*, ICCV 2021, pp. 15457–15466 — DOI 10.1109/ICCV48922.2021.01517 | Les auteurs revendiquent le premier déploiement d'un Siamese-Transformer sur plateforme embarquée en temps réel ; code publié |
| Suivi (variantes) | Cao, Fu, Ye, Li, Li, *SiamAPN++*, IROS 2021, pp. 3086–3092 ; Cao et al., *TC-Track*, CVPR 2022 | Non lus |
| **Navigation sur nano-drone** | PULP-DroNet (Palossi et al., IEEE IoT J 2019) ; Tiny-PULP-Dronets (Lamberti et al., AICAS 2022) | Voir liste précédente |
| **Estimation de pose humaine** | Palossi et al., *Fully Onboard AI-Powered Human-Drone Pose Estimation on Ultralow-Power Autonomous Flying Nano-UAVs* (PULP-Frontnet), IEEE IoT J | Crazyflie 2.1 de 27 g en boucle fermée ; erreur médiane de position 41 cm à bord contre 26 cm avec un capteur idéal ; code publié |
| **Exploration + détection multi-tâches** | Lamberti et al., DATE 2023 ; **[preprint]** BlankSkip (arXiv 2603.28149) | Voir liste précédente |
| **Essaims** | Pourjabar et al., *Land & Localize: An Infrastructure-free and Scalable Nano-Drones Swarm with UWB-based Localization*, DCOSS 2023 | GAP8 (détection + évitement de collision) et localisation UWB entre drones ; source : slides |
| **Contrôle neuromorphique** | Paredes-Vallés et al., Science Robotics 2024 | Voir liste précédente |
| **Odométrie visuelle-inertielle (ASIC)** | Navion (Suleiman et al., JSSC 2019) | Voir liste précédente |
| **Surveillance feux de forêt** | Elhence, Panda, Chamola, Sikdar, IEEE TIM 74, 2025 — DOI 10.1109/TIM.2025.3556164 | YOLOX sur FPGA ; non lu |
| **Faune** | **[preprint]** DEAL-YOLO, arXiv 2503.04698 | Non lu |
| ⚠️ **Flot optique** | Bouwmeester et al., *NanoFlowNet: Real-time Dense Optical Flow on a Nano Quadcopter* (probablement ICRA 2023) | Cité dans des slides ; venue à vérifier |

**Lecture critique :** les travaux de Zurich (Loquercio, Kaufmann) utilisent des calculateurs embarqués de classe Jetson, donc de l'ordre de 10 W. Ils ne sont pas directement comparables à l'échelle nano (mW) ou à l'échelle FPGA. Il faut toujours préciser la gamme de puissance quand on les cite.

## Pistes de suite
1. **Lire Det-Fly (RA-L 2021).** Le dataset est public, et c'est le point d'entrée naturel pour un YOLO air → air embarqué.
2. **Expérience** : entraîner YOLOv8n ou YOLOv3-tiny sur Det-Fly, puis le quantifier en INT8 et le déployer sur KV260 via Vitis AI. À comparer à un Jetson et, si possible, au travail de Nguyen et al. C'est un angle « contre-drone embarqué sur FPGA » encore peu occupé d'après cette recherche.
3. **Lire HiFT** pour comprendre comment les laboratoires de tracking aérien mesurent le « temps réel embarqué », puis vérifier sur quelle plateforme exacte ils l'annoncent.
