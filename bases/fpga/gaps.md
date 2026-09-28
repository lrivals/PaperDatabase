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

Mise à jour du 26/09/2026 (7e passage) : **41 fiches `done` sur 45**, **172 lignes** dans
`benchmarks.csv` (31 papiers, dont 101 lignes FPGA). Douze fiches ajoutées à ce passage :
- autoencodeurs : 2019-coutinho (SSAE), 2019-tsukada (ONLAD), 2021-manjunath (CAE ternaire),
  2022-malviya (CAE vibrations), arxiv-2301.07050 (CAE débruitage) ;
- YOLO et détection : 2019-ding (REQ-YOLO), 2021-xu (DAC-SDC) ;
- toolflows et architecture : 2015-zhang (roofline), 2018-venieris (survey),
  2024-campos (HAWQ → hls4ml), arxiv-2011.07317 (FCMP) ;
- apprentissage continu : arxiv-2110.10486 (QLR-CL sur VEGA).

Changements de ce passage :
- **nuancé** : « Autoencodeurs sur FPGA appliqués aux images ». Des AE d'images existent
  sur petite FPGA (Manjunath, 2301.07050), mais aucun ne détecte d'anomalies visuelles ;
- **nouveaux gaps** :
  - autoencodeur complet (encodeur + décodeur) sur une petite FPGA ;
  - apprentissage embarqué par rétropropagation sur FPGA ;
  - adaptation à la dérive pour la détection d'anomalies ;
  - petits objets vus de drone ;
- **étendus** avec de nouveaux constats :
  - puissance (recompte) ;
  - métriques flatteuses (+6 fiches) ;
  - code publié ;
  - comparaison croisée des toolflows (Venieris lu) ;
  - réseaux qui ne tiennent pas on-chip (FCMP, REQ-YOLO) ;
  - précision sur cible (contre-exemples : Coutinho et Malviya la mesurent) ;
- **aucun gap supprimé**. Aucune fiche n'en contredit un entièrement.

**Réserve générale** : le corpus est petit et biaisé par la bibliographie de départ.
- Effectifs par axe (fiches `done`) :
  - `platforms` 24 ;
  - `toolflows` 14 ;
  - `autoencoder-fpga` 11, dont une hors FPGA (Φ-Sat-2) ;
  - `yolo-fpga` 8 ;
  - `surveys` 8 ;
  - `continual-learning` 5, dont 2 hors FPGA.
- `benchmarks.csv` reste déséquilibré :
  - 24 lignes de Feng et al. (Jetson, VPU, sans mAP), 20 de FINN / FINN-R, 14 de SATAY ;
  - 75 lignes sur 172 sont en `medium` et 1 en `low` (arxiv-2301.07050), souvent parce
    que leurs tableaux ont été reconstruits par Docling ou PyMuPDF.
- Restent à ficher :
  - 2023-cui (survey d'anomalie visuelle industrielle, **directement utile** au premier
    gap) ;
  - arxiv-2010.15277 (survey CIL) ;
  - arxiv-2206.15472 (entraînement dans 256 KB) ;
  - arxiv-2409.07114 (CL sur MCU).
- Un gap qui ne repose que sur l'absence de papiers dans la base reste une `hypothèse`. Un
  gap `étayé` est constaté dans les fiches, ce qui ne prouve pas son absence dans la
  littérature.

Passages précédents (résumé) :
- 2e au 5e : Feng, Magalhães, El Zeinaty, Zhai, MCUNetV2, TinyissimoYOLO, AE au LHC,
  surveys Shuvo / Mittal / Hozhabr, Rey, Alqahtani ;
- 6e : SATAY, Que 2024 (VAE), hls4ml CNN, F-LIC, Φ-Sat-2.

### Couverture croisée de `benchmarks.csv` (7e passage)

Lignes par tâche et classe de plateforme. Le classement est fait par mots-clés de la
colonne `platform` et reste donc approximatif. « Petite FPGA » regroupe Zynq-7000, Zynq
UltraScale+, Kria, PYNQ, Artix et PolarFire.

| Tâche | Petite FPGA / SoC | Grosse FPGA | Jetson | MCU | ASIC | Autre |
|---|---|---|---|---|---|---|
| Détection | 18 | 15 | 42 | 5 | 0 | 11 (RPi, VPU, Hailo) |
| Classification | 19 | 20 | 0 | 2 | 0 | 0 |
| Anomalie (AE, OS-ELM) | 5 | 7 | 0 | 0 | 0 | 0 |
| Autoencodeur (autre usage) | 7 | 3 | 0 | 0 | 1 | 0 |
| Compression d'image | 0 | 4 | 0 | 0 | 0 | 3 (VPU, GPU, CPU) |
| Apprentissage continu / incrémental | 3 | 0 | 0 | 4 | 3 | 0 |

Cases vides ou quasi vides :
- **Anomalie × Jetson ou MCU** : aucune baseline hors FPGA pour les AE d'anomalie ;
- **Compression d'image × petite FPGA** : 0 ligne ;
- **Apprentissage continu × Jetson** : 0 ligne ;
- **Détection × apprentissage continu** : 0 ligne, toutes plateformes confondues.

Parmi les 5 lignes « anomalie » sur petite FPGA, aucune ne porte sur des images réelles :
signaux de calorimètre (arxiv-2602.15751), vibrations (2022-malviya) et ONLAD, dont les
données sont tabulaires ou des images aplaties (2019-tsukada).

Toolflow × tâche, sur les 101 lignes FPGA :
- détection : SATAY 14, HLS maison 13, FINN 3, Vitis AI 2, RTL 1 ;
- classification : FINN 20, hls4ml 16 ;
- anomalie / AE : hls4ml 10, HLS maison 7, RTL 5 ;
- **Vitis AI n'a que 2 lignes**, toutes deux de détection (arxiv-2507.18174), alors que
  c'est le flot par défaut du KV260.

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
- Constat (7e passage, 6 fiches). Des **AE d'images sur petite FPGA** existent, mais aucun
  ne sert à la détection d'anomalies visuelles :
  - **encodeur convolutif ternaire** sur images 120 × 120 RGB (simulateur Miniworld), sur
    Artix-7, pour fournir un latent à un agent RL, avec la puissance estimée par Vivado
    (2021-manjunath-energy-efficient-edgeai-autoencoder-accelerator, §VI, Table 5) ;
  - **CAE de débruitage** sur MNIST bruité, sur XCZU7EV. Sa « précision » n'est pas
    définie et son tableau est incohérent (arxiv-2301.07050, §IV-B, Table II) ;
  - **CAE d'anomalies** sur des vibrations encodées en scalogrammes 64 × 64 (PYNQ-Z2).
    L'image n'y est qu'un encodage d'une série temporelle
    (2022-malviya-edge-compatible-convolutional-autoencoder-implemented, §II-B) ;
  - ONLAD : AE OS-ELM d'anomalies sur données tabulaires ou MNIST aplati
    (2019-tsukada-neural-network-device-learning-anomaly, Table 2) ;
  - le « SSAE » de Coutinho n'est qu'un classifieur MLP sur MNIST, sans reconstruction
    (2019-coutinho-deep-neural-network-hardware-implementation, §III-A, §V-D) ;
  - ECON-AE compresse des données de calorimètre, encodeur seul
    (2024-campos-end-end-codesign-hessian-aware, §7).
- Bilan des 11 fiches `autoencoder-fpga` :
  - compression d'images : oui, sur grosse FPGA (F-LIC) ou sur VPU (Φ-Sat-2) ;
  - encodage d'images sur petite FPGA : oui, mais à petite échelle (MNIST 28 × 28 ou
    120 × 120) ;
  - **détection d'anomalies visuelles par AE sur FPGA : toujours aucune.**
- Ce qui manque : un CAE ou VAE sur images ou vidéo réelles, pour la **détection
  d'anomalies visuelles**, avec PSNR / AUROC mesurés sur la cible, et latence et puissance
  de carte mesurées sur FPGA embarquée.
- Statut : **étayé (11 fiches)** pour l'anomalie visuelle sur FPGA embarquée. Contredit pour
  « l'image » en général, par F-LIC (grosse FPGA) et, à petite échelle, par Manjunath et
  arxiv-2301.07050. Le survey d'anomalie visuelle industrielle 2023-cui, pas encore fiché,
  dira quels modèles AE seraient les candidats.
- Piste :
  - point de départ : l'encodeur ternaire paramétrable de Manjunath (PE × largeur mémoire),
    le score d'anomalie on-chip de arxiv-2108.03986 (§IV) et le décodeur layer-wise de F-LIC ;
  - expérience : un CAE d'anomalie visuelle (MVTec AD) sur KV260, avec AUROC mesurée sur la
    carte et puissance de carte ;
  - lecture : le codec JETCAS 2024 (DOI 10.1109/jetcas.2024.3386328, non ingéré).

### Autoencodeur complet (encodeur + décodeur) sur une petite FPGA
Nouveau au 7e passage.
- Constat : les AE FPGA du corpus n'implantent le plus souvent qu'une moitié du réseau, ou
  le coupent en deux :
  - encodeur seul :
    - Manjunath, car le décodeur est inutile pour le RL
      (2021-manjunath-energy-efficient-edgeai-autoencoder-accelerator, §VII) ;
    - ECON-AE (2024-campos-end-end-codesign-hessian-aware, §7) ;
    - VAE réduit à l'encodeur, avec un score D_KL (arxiv-2108.03986, §IV) ;
  - encodeur et décodeur dans **deux bitstreams séparés** sur PYNQ-Z2. La latence de 5,9 ms
    ne compte pas la reconfiguration entre les deux (déduit)
    (2022-malviya-edge-compatible-convolutional-autoencoder-implemented, §III, §IV-B) ;
  - F-LIC implante les deux transformées, mais sur VCU118 (2022-sun-f-lic-fpga-learned-image).
- Ce qui manque : un AE convolutif complet, dont la reconstruction sert au score
  d'anomalie, dans un seul bitstream sur Zynq ou Kria, avec le coût des déconvolutions et
  de l'upsampling mesuré.
- Statut : étayé (5 fiches) dans le corpus. Pour la littérature, c'est une hypothèse.
- Piste : dimensionner un CAE de type MVTec sur KV260 avec les ressources de Malviya
  (40 k LUT pour l'encodeur seul, sur Zynq-7020) comme borne basse. Tester le score
  « encodeur seul » (distance dans le latent) face au score par reconstruction.

### Compression apprise embarquée complète (codage entropique compris)
- Constat :
  - F-LIC laisse le range coding sur le PC hôte (2022-sun-f-lic-fpga-learned-image, Fig. 1) ;
  - Φ-Sat-2 n'a pas de codage entropique, avec un taux ×8 fixe, sur VPU
    (2023-guerrisi-artificial-intelligence-board-image-compression, §II-A, §III-A) ;
  - (7e passage) ECON-AE compresse des données de détecteur sans codage entropique, et
    seul son encodeur est mesuré (2024-campos-end-end-codesign-hessian-aware, §7).
- Ce qui manque : une chaîne complète (transformées + codage entropique) sur plateforme
  embarquée à faible consommation, avec l'énergie par image mesurée.
- Statut : hypothèse (3 fiches).
- Piste : lire le codec JETCAS 2024 ; chercher « learned image compression FPGA entropy
  coding hardware ».

### VAE complet en matériel pour un espace latent de grande dimension
- Constat : le seul VAE qui échantillonne en matériel a un latent de dimension 1 ; une
  unité avec son GRNG prend 113 DSP (2024-que-low-latency-variational-autoencoder-fpgas,
  §IV-B, Table III). Les autres VAE évitent l'échantillonnage (arxiv-2108.03986, §IV).
- Ce qui manque : le coût d'un GRNG parallèle pour un latent d'image (centaines à milliers
  de dimensions).
- Statut : hypothèse (1 fiche). Inchangé.
- Piste : extrapoler le coût du GRNG de Que 2024 et le comparer au score D_KL déterministe.

## YOLO et détection sur FPGA

### Pas de protocole de mesure commun pour YOLO sur FPGA
- Constat (passages 1 à 6, résumé ; le détail est dans les fiches citées) :
  - YOLOv5 sur KV260 : précision sur 72 images, puissance sans méthode
    (arxiv-2507.18174, Table I) ;
  - le survey arxiv-2509.04153 compare des designs sans conditions homogènes ;
  - Tincy YOLO n'est donné qu'en GOp/s (arxiv-1809.04570, Table 5) ;
  - « mean confidence » au lieu d'une mAP (2022-feng, §4.1) ;
  - chronométrage du seul cœur du réseau (arxiv-2211.11647, §2.5) ;
  - AP à une seule classe (2023-zhai, Table 8) ;
  - SATAY : « mAP∗ » ou mAP50, puissance sans méthode (2023-montgomerie-corcoran,
    Tables III-IV).
- Constat (7e passage) :
  - **DAC-SDC est un contre-exemple partiel.** C'est un protocole commun, mesuré par les
    organisateurs, pour la PYNQ-Z1 et le TX2 : jeu de test caché, débit minimal imposé,
    énergie au wattmètre (2021-xu-dac-sdc-low-power-object, §2.3). Ses limites :
    - la métrique est un IoU d'un seul objet par image, pas une mAP ;
    - le score composite a des bases log différentes pour le FPGA et le GPU ;
    - l'échantillonnage de puissance est donné à « 0,01 Hz » (coquille probable) ;
    - les puissances par équipe ne sont qu'en figures (Fig. 12, non extraite) ;
  - REQ-YOLO : seules les pertes de mAP **relatives** sont dans le texte ; la mAP absolue
    est en Fig. 10. La latence est la **somme des latences par couche**, hors PCIe et NMS
    (2019-ding-req-yolo-resource-aware-efficient, §6.2, Table 1) ;
  - dans `benchmarks.csv`, sur 103 lignes de détection, 29 viennent d'une FPGA. Parmi ces
    29, 14 ont une mAP COCO (toutes de SATAY), 4 un IoU DAC-SDC et 2 une mAP VOC sans
    valeur (REQ-YOLO).
- Ce qui manque : mAP sur le split officiel, variante et résolution déclarées, FPS et latence
  à batch 1 de bout en bout, puissance de carte au wattmètre et de puce par télémétrie,
  le tout pour une même carte récente.
- Statut : **étayé (11 fiches)**. DAC-SDC montre qu'un protocole commun est faisable (2018,
  plateformes anciennes), mais aucun travail du corpus ne le reprend avec une mAP standard.
- Piste : expérience de référence YOLOv5 / v8 INT8 via Vitis AI sur KV260, plus un Jetson
  Orin Nano, avec le protocole DAC-SDC (jeu caché, énergie mesurée) complété par une mAP
  COCO. Protocole de puissance : celui de FINN, qui donne P_chip et P_wall
  (arxiv-1612.07119, §5.1).

### Détection en dataflow quantifié sur SoC FPGA embarqué
Reformulé au 6e passage, car la forme générale est contredite par SATAY
(2023-montgomerie-corcoran-satay-streaming-architecture-toolflow-accelerating, §IV).
- Constat (6e passage et avant) :
  - SATAY vise surtout de grosses FPGA ; sur SoC, seule la ZCU104 est testée, avec YOLOv5n,
    et tous les poids restent on-chip (Table IV, §IV-C) ;
  - FINN traite la classification 32 × 32 (arxiv-1612.07119) ; FINN-R ne passe Tincy YOLO
    qu'en offload multicouche (arxiv-1809.04570, Table 5) ;
  - hls4ml et fpgaConvNet ne publient aucun détecteur (arxiv-2512.01463, §11 ;
    arxiv-1711.08740).
- Constat (7e passage) :
  - REQ-YOLO compresse Tiny YOLO (matrices bloc-circulantes, quantification mixte ADMM)
    pour que **tous les poids tiennent en BRAM**. Mais c'est sur un Virtex-7 PCIe (6,6 Mo
    de BRAM, 21 W), pas sur un SoC (2019-ding-req-yolo-resource-aware-efficient, §5,
    Table 2) ;
  - DAC-SDC : détecteurs HLS ou RTL maison sur Zynq-7020, avec cartes intermédiaires en DDR.
    TGIIF (SSD élagué 8 bits, RTL) fait IoU 0,62 à 11,96 FPS ; SystemsETHZ (SqueezeNet
    binaire + YOLO) fait 25,97 FPS (2021-xu-dac-sdc-low-power-object, §4.2, §5.2.1) ;
  - le survey de Venieris confirme qu'en 2018 aucun toolflow ne visait la détection
    (2018-venieris-toolflows-mapping-convolutional-neural-networks, §2.6, §3.1).
- Ce qui manque : un YOLO v5 / v8 en dataflow quantifié (SATAY, FINN ou hls4ml) sur **SoC
  à mémoire on-chip limitée** (KV260, Zynq-7020), en W4 à W8, comparé à Vitis AI sur la
  même carte.
- Statut : étayé (10 fiches) dans sa forme « sur SoC embarqué ».
- Piste :
  - reproduire SATAY sur ZCU104 puis KV260 ;
  - comparer au DPU ;
  - appliquer l'empaquetage mémoire FCMP (arxiv-2011.07317) pour repousser la limite
    on-chip.

### Petits objets vus de drone sur FPGA
Nouveau au 7e passage.
- Constat : sur le jeu DAC-SDC, la plupart des objets occupent 1 à 2 % de l'image
  (640 × 360). La précision chute pour les petits objets, sur GPU comme sur FPGA. Les
  meilleurs FPGA redimensionnent l'image sur l'ARM avant traitement
  (2021-xu-dac-sdc-low-power-object, §3, §4.2, §5.2.3).
- Ce qui manque : un détecteur FPGA embarqué conçu pour les petits objets (haute
  résolution, tuilage, FPN), avec l'effet du redimensionnement mesuré.
- Statut : hypothèse (1 fiche).
- Piste : chercher les éditions suivantes du DAC-SDC (SkyNet, iSmart ; non vérifiées) via
  `/paper-discover "DAC-SDC FPGA"`.

### Interaction PS-PL et post-traitement sur SoC FPGA
- Constat (passages 1 à 6) :
  - post-traitement en Python sur le PS : de 195 à 24 FPS dans un exemple cité
    (arxiv-2509.04153, §VI-C, référence [125] non lue) ;
  - NMS et Deepsort sur l'ARM, inclus ou non dans les FPS : on ne sait pas
    (2023-zhai, §3.3) ;
  - pré- et post-traitement exclus des mesures (arxiv-2211.11647, §2.4) ;
  - SATAY ne dit pas où se fait la NMS (§III-A) ;
  - F-LIC laisse le codage entropique sur l'hôte ;
  - NMS matériel sur Stratix 10 ou KC705, cité par 2025-hozhabr (§V-A), non lu.
- Constat (7e passage) :
  - REQ-YOLO : latence = Σ couches, sans NMS ni transfert PCIe
    (2019-ding-req-yolo-resource-aware-efficient, Table 1) ;
  - DAC-SDC : les meilleures équipes FPGA redimensionnent sur l'ARM et stockent les
    activations en DDR (2021-xu-dac-sdc-low-power-object, §4.2) ;
  - le roofline de Zhang et al. ne modélise que les convolutions ; pooling et FC sont
    exclus (2015-zhang-optimizing-fpga-accelerator-design-deep, §2.1).
- Ce qui manque : une mesure de bout en bout (capture → PL → post-traitement → sortie) sur
  SoC, avec un partitionnement PS / PL justifié.
- Statut : étayé (7 fiches).
- Piste : instrumenter la latence de bout en bout dans l'expérience KV260 ; lire [125] de
  arxiv-2509.04153.

## Mesure et comparaison

### Précision non vérifiée sur la cible après compilation et quantification
- Constat (passages 1 à 6) :
  - OpenVINO fait tomber YOLOv3-tiny à 0 % (2022-feng, Table 3) ;
  - compilateur Edge TPU et DPU (arxiv-2211.11647, §2.3, §3) ;
  - AP FP32 = INT16 à trois décimales (2023-zhai, Table 8) ;
  - la PTQ INT8 de TensorRT coûte de 6,4 à 12,3 points de mAP50-95
    (arxiv-2502.15737, Table 4) ;
  - mAP identiques sur deux Jetson (arxiv-2409.16808) ;
  - quantification simulée par ONNX Runtime (SATAY, §IV-A) ;
  - comparaison au C++ généré, pas au FPGA (arxiv-2101.05108, §8).
- Constat (7e passage) :
  - ONLAD : les AUC sont mesurées en TensorFlow, pas sur le cœur en virgule fixe 32 bits
    (2019-tsukada-neural-network-device-learning-anomaly, §5, §6) ;
  - REQ-YOLO : seule la perte **relative** de mAP due à la quantification est donnée
    (2019-ding-req-yolo-resource-aware-efficient, §6.2) ;
  - Campos : précisions issues de l'entraînement, latences **estimées par HLS**, aucune
    exécution sur carte (2024-campos-end-end-codesign-hessian-aware, §6.2) ;
  - arxiv-2301.07050 : « accuracy » d'un débruiteur, non définie ;
  - **contre-exemples** : deux petits modèles mesurent bien la précision sur FPGA et
    montrent une perte :
    - Malviya : 85,02 % sur FPGA contre 88,8 % sur CPU, en virgule fixe 23 bits
      (2022-malviya-edge-compatible-convolutional-autoencoder-implemented, §IV-B) ;
    - Coutinho : 93,38 % contre 93,4 %
      (2019-coutinho-deep-neural-network-hardware-implementation, §V-D1).
- Ce qui manque : la mAP ou l'AUROC mesurée **sur la cible**, après chaque étape
  (quantification, compilation, partitionnement), pour des modèles de vision réalistes.
- Statut : **étayé (11 fiches)**. Nuancé : la vérification sur cible se fait pour de petits
  modèles (MLP, CAE minuscule), et c'est justement là qu'elle révèle une perte
  (−3,8 points chez Malviya).
- Piste : évaluer la mAP COCO val sur la carte, sorties du DPU relues et NMS compris, face
  au modèle flottant et au modèle quantifié simulé. C'est le gap le plus directement
  exploitable.

### Pas de baseline GPU / Jetson mesurée dans les mêmes conditions
- Constat (passages 1 à 6) :
  - fpgaConvNet suit le bon protocole, face à un Tegra X1 de 2015
    (arxiv-1711.08740, §3.1) ;
  - Feng : Jetson sans TensorRT ;
  - Magalhães : TX2, valeurs en figures ;
  - Zhai : Jetson reprise d'un autre papier ;
  - Rey et Alqahtani sur Orin, chacun incomplet (arxiv-2502.15737, arxiv-2409.16808) ;
  - SATAY : TX2 (Table IV) ;
  - F-LIC : Xavier NX.
- Constat (7e passage) :
  - **DAC-SDC** : protocole commun PYNQ-Z1 / TX2, avec l'énergie mesurée par les
    organisateurs, mais sur des plateformes de 2018 et avec des chiffres en figures. Les
    auteurs affirment que le FPGA consomme 1/3 à 1/2 de l'énergie du GPU pour une précision
    proche, sans chiffre dans le texte (2021-xu-dac-sdc-low-power-object, §5.3) ;
  - REQ-YOLO : TX2 et GTX 1070 mesurés par les auteurs sur le même modèle ; TX2 à
    28,4 FPS, TensorRT non mentionné (2019-ding-req-yolo-resource-aware-efficient,
    Table 2) ;
  - ONLAD : CPU / GPU en TensorFlow à batch 1, dominés par les surcoûts d'appel
    (2019-tsukada-neural-network-device-learning-anomaly, §6.2.1) ;
  - Zhang 2015 : Xeon seulement, énergie tirée du TDP
    (2015-zhang-optimizing-fpga-accelerator-design-deep, Table 8).
- Ce qui manque : même modèle, même précision numérique, même batch, même méthode de
  puissance, sur FPGA embarquée **et Jetson Orin**.
- Statut : **étayé (20 fiches)**. Partiellement comblé côté Jetson (Rey, Alqahtani) et côté
  protocole (DAC-SDC, 2018). Aucune source ne compare un Orin à une FPGA embarquée.
- Piste : le volet Orin Nano de l'expérience de référence, sur le modèle de DAC-SDC et de
  fpgaConvNet.

### Puissance : puce contre carte, estimée contre mesurée
- Constat (recompte du 7e passage, 172 lignes dont 101 FPGA) :
  - lignes FPGA :
    - **18 `board`** : FINN 8, FINN-R 8, Zhang 2015 1 (VC707, 18,61 W), ONLAD 1
      (PYNQ-Z1, 3,1 W au wattmètre, ARM compris) ;
    - **0 `chip` et 0 `board-dynamic`** ;
    - 31 `unspecified` ;
    - 8 `estimated` (Manjunath par Vivado, Que 2024, ImageHD) ;
    - 44 sans puissance (`n/r`) ;
  - les 17 lignes `chip` viennent toutes de Jetson, du RPi 5 ou d'un ASIC. La nouvelle
    source est VEGA, qui mesure le courant de la puce à 62 mW
    (arxiv-2110.10486-tinyml-platform-device-continual-learning, §V-D).
- Nouvelles portées non comparables (7e passage) :
  - Coutinho : puissance **dynamique** de quelques mW, méthode non décrite, comparée à
    des puissances totales d'autres travaux
    (2019-coutinho-deep-neural-network-hardware-implementation, Table 16) ;
  - ONLAD : carte (3,1 W) contre CPU seul (s-tui) et GPU seul (nvidia-smi)
    (2019-tsukada-neural-network-device-learning-anomaly, §6.4) ;
  - QLR-CL : puce mesurée (62 mW) contre 4 W « d'enveloppe » supposés pour le Snapdragon
    (arxiv-2110.10486, §V-E) ;
  - REQ-YOLO, Malviya, arxiv-2301.07050 (« on-chip ») et arxiv-2011.07317 (« Max
    Power ») : puissance sans méthode ;
  - DAC-SDC : wattmètre sur la carte PYNQ, mais valeurs en figures (2021-xu, §2.3).
- Ce qui manque : `chip` et `board` sur la même carte récente (Kria, Versal).
- Statut : **étayé (26 fiches + `benchmarks.csv`)**. Aggravé : parmi les 12 nouvelles
  fiches, seule ONLAD décrit une mesure de carte FPGA.
- Piste : dans l'expérience KV260, relever la télémétrie de la puce, le wattmètre de carte
  et la puissance au repos.

### Métriques flatteuses et comparaisons biaisées
Étendu au 7e passage (ancien intitulé : « Métriques flatteuses : latence amortie,
GOP/s/DSP, puissance dynamique »).
- Constat (6e passage) :
  - « latence » = débit inverse (2024-que, §IV-E) ;
  - GOP/s/DSP qui efface la précision (SATAY, Table III) ;
  - GOPS/W dynamiques (2023-zhai, Table 8) ;
  - « mean confidence » (2022-feng, §4.1).
- Constat (7e passage) :
  - Coutinho compare des GOPS **projetés** sur un FPGA hypothétique à 10 000 PE (VU440) à
    des GOPS **mesurés** de CNN, et revendique un gain de puissance de ≈ 1 000× en mettant
    sa puissance dynamique face à des puissances totales
    (2019-coutinho-deep-neural-network-hardware-implementation, Tables 16-17) ;
  - arxiv-2301.07050 range Zhang 2015 (AlexNet, convolutions seules) parmi les « CNN
    autoencoder models », classe un K80 comme « ASIC (28 nm) » et donne une ligne
    physiquement incohérente (22 000 GOP/s pour 1 137 ms) (Table II) ;
  - Manjunath recalcule en TOP/J l'efficacité d'autres travaux à partir de leurs FPS/W, et
    compare classification 32 × 32 et encodeur 120 × 120
    (2021-manjunath-energy-efficient-edgeai-autoencoder-accelerator, §VIII-C, Table 7) ;
  - Zhang 2015 estime l'énergie CPU à partir du TDP (95 W)
    (2015-zhang-optimizing-fpga-accelerator-design-deep, §5.2, Table 8) ;
  - QLR-CL suppose une enveloppe de 4 W pour le Snapdragon (arxiv-2110.10486, §V-E) ;
  - REQ-YOLO se compare à Zynq-YOLO et Virtex-YOLO sans mettre la précision en regard
    (2019-ding-req-yolo-resource-aware-efficient, Table 2).
- Ce qui manque : un jeu de métriques imposé (latence batch 1, débit, énergie de carte par
  inférence, précision sur cible) et la relecture des comparaisons publiées à cette aune.
  Venieris et al. proposaient déjà ce jeu en 2018
  (2018-venieris-toolflows-mapping-convolutional-neural-networks, §3.1) ; il n'est
  repris par aucune fiche du corpus.
- Statut : **étayé (10 fiches)**. C'est un constat méthodologique.
- Piste : l'état de l'art du pré-projet peut s'appuyer sur la grille de Venieris §3.1, et
  recalculer les rapports annoncés quand les données le permettent.

### Code et bitstreams rarement publiés
- Constat, sur les 33 fiches expérimentales `done` (surveys exclus) :
  - **aucun bitstream publié** explicitement. arxiv-2011.07317 annonce une variante de
    RN50-W1A2 « available online », sous une forme non précisée (§III-B) ;
  - code propre au papier publié ou annoncé dans 7 cas :
    - arxiv-2211.11647 (GitLab) ;
    - arxiv-1809.04570 (en partie) ;
    - arxiv-2108.03986 (branche hls4ml) ;
    - 2019-ding (GitHub, vraisemblablement l'entraînement seulement, résumé) ;
    - 2021-xu (code des 3 meilleures équipes de chaque catégorie, §1) ;
    - arxiv-2011.07317 (streamer RTL, §V) ;
    - 2024-campos (extension HAWQ → QONNX annoncée open source, lien non extrait) ;
  - non publiés (7e passage) : 2015-zhang, 2019-coutinho (vidéo seulement), 2019-tsukada,
    2021-manjunath, 2022-malviya, arxiv-2301.07050, arxiv-2110.10486 (lien non extrait) ;
  - passages précédents : 2022-feng, 2023-zhai, arxiv-1612.07119, arxiv-1711.08740,
    arxiv-2306.00001, arxiv-2502.15737, arxiv-2507.18174, arxiv-2604.21280, 2024-que,
    2022-sun, 2023-guerrisi.
- Ce qui manque : projet, bitstream et scripts de mesure pour revérifier les chiffres sur
  carte.
- Statut : étayé (33 fiches). La lecture se limite au texte extrait : les liens en note de
  bas de page sont souvent perdus.
- Piste : publier le projet, le bitstream et les scripts de l'expérience KV260.

## Toolflows

### Pas de comparaison croisée hls4ml / FINN / Vitis AI sur un même CNN et une même carte
- Constat :
  - aucun papier d'outil ne compare deux flots mesurés (arxiv-2512.01463, arxiv-2103.05579,
    arxiv-1809.04570, arxiv-2101.05108, SATAY §II-C) ;
  - (7e passage) le **survey de Venieris, désormais lu**, confirme le constat pour 2018 :
    - les chiffres sont repris des publications ou des auteurs, aucun outil n'est relancé ;
    - la comparaison se limite aux paires CNN-FPGA identiques, faute d'outils publics ;
    - puissance et précision sont absentes des tableaux
      (2018-venieris-toolflows-mapping-convolutional-neural-networks, §2.6, §2.7) ;
    - les auteurs sont aussi ceux de fpgaConvNet (biais possible, déduit) ;
  - (7e passage) Campos exporte vers QONNX, format lisible par FINN et hls4ml, mais n'évalue
    que hls4ml (2024-campos-end-end-codesign-hessian-aware, §2.3, §5).
- Ce qui manque : un même CNN, une même carte, les trois flots ; ressources, latence,
  puissance et précision.
- Statut : étayé (9 fiches) dans le corpus ; hypothèse pour la littérature. Un comparatif
  hls4ml / FINN (Springer, `basicStart.txt`) n'est pas ingéré (paywall).
- Piste : QONNX rend techniquement faisable un même modèle vers FINN et hls4ml. C'est une
  expérience de thèse candidate sur KV260, avec Vitis AI en référence.

### Réseaux qui ne tiennent pas on-chip : limite du dataflow
- Constat (passages 1 à 6) :
  - FINN suppose tout en OCM (arxiv-1612.07119, §6) ;
  - l'offload de FINN-R est peu prévisible (arxiv-1809.04570, §5.3) ;
  - fpgaConvNet partitionne ou recharge, en FXP16 (arxiv-1711.08740, §2.4) ;
  - SATAY garde les poids on-chip jusqu'à 26 MB (§IV-C) ;
  - F-LIC met les poids en DDR, sur VCU118 ;
  - hls4ml CNN tient sur XC7Z020 en augmentant le reuse factor (arxiv-2101.05108,
    Table 4).
- Constat (7e passage) :
  - **FCMP** (équipe FINN) identifie la BRAM comme le goulot du dataflow. Le rendement
    d'occupation des BRAM tombe à ~50 % sur ResNet-50 (52,9 % sur U250). En sur-cadençant
    la mémoire et en regroupant les tampons, les auteurs économisent jusqu'à 30 % d'OCM
    pour ~5 % de LUT. CNV passe ainsi du 7020 au 7012S sans perte de débit, mais ResNet-50
    reste sur Alveo (71 W) (arxiv-2011.07317-memory-efficient-dataflow-inference-deep,
    §II-B, Table IV, Table V). C'est un preprint ;
  - REQ-YOLO tient on-chip par compression structurée (bloc-circulant + FFT)
    (2019-ding-req-yolo-resource-aware-efficient, §5) ;
  - Venieris : dans les architectures streaming, un bitstream par CNN et une taille bornée
    par l'OCM, en particulier pour Haddoc2 et FINN (2018-venieris, §2.3, §2.8) ;
  - FCMP laisse l'empaquetage des **activations** (FIFO, line buffers) en travail futur
    (arxiv-2011.07317, §VI).
- Ce qui manque : la combinaison « quantification agressive (FINN) + empaquetage mémoire
  (FCMP) ou rechargement des poids (fpgaConvNet) » pour un réseau de vision profond
  (YOLO, CAE) sur une petite puce (KV260), avec le coût mesuré à batch 1.
- Statut : étayé (10 fiches). La combinaison est absente du corpus ; son absence dans la
  littérature reste une hypothèse.
- Piste : `/paper-discover "fpgaConvNet quantization"`, « FINN external memory weights ».
  Candidat de thèse : un flot dataflow quantifié pour la détection ou un CAE, qui tient sur
  KV260 grâce à FCMP et au streaming partiel des poids.

### Estimation de puissance et de latence dans les toolflows
- Constat :
  - FINN-R ne gère que les ressources et le débit (arxiv-1809.04570, §4) ;
  - hls4ml 2025 ne mesure aucune puissance (arxiv-2512.01463) ;
  - (7e passage) Campos donne des latences **estimées par Vivado HLS** et aucune
    puissance, et s'appuie sur un travail antérieur pour dire que l'estimation est fiable
    sur cette tâche (2024-campos-end-end-codesign-hessian-aware, §6.1, §6.2) ;
  - Manjunath estime la puissance par Vivado sans validation sur carte
    (2021-manjunath-energy-efficient-edgeai-autoencoder-accelerator, §VIII-A).
- Ce qui manque : un modèle de puissance validé sur carte, intégré au flot.
- Statut : hypothèse pour l'état actuel des outils (le FINN d'aujourd'hui n'est pas dans le
  corpus). Étayé (4 fiches) pour le constat « estimation non validée » dans les papiers.
- Piste : vérifier la documentation actuelle de FINN et de hls4ml.

### NAS et quantification mixte guidées par le matériel sur FPGA
Élargi au 7e passage (ancien intitulé : « NAS matériel-aware ciblant les FPGA »).
- Constat :
  - absent du survey arxiv-2411.01431 ;
  - prédicteurs de ressources MLP seulement dans hls4ml (arxiv-2512.01463) ;
  - NAS hardware-aware seulement côté MCU (2025-el-zeinaty, §6.4.2) ;
  - (7e passage) **quantification mixte automatique guidée par la Hessienne**, résolue par
    ILP sous budget de BOPs, jusqu'au firmware hls4ml : −95,7 % de DSP pour −1,07 point sur
    un MLP (2024-campos-end-end-codesign-hessian-aware, §4.2.2, Table 2). Mais seulement
    sur un MLP et un encodeur à 2 couches ;
  - REQ-YOLO choisit la quantification couche par couche selon la ressource (DSP ou LUT)
    (2019-ding-req-yolo-resource-aware-efficient, §5.1) ;
  - Venieris place la co-conception réseau-matériel en horizon (2018-venieris, §3.2).
- Ce qui manque : une NAS ou une quantification mixte guidée par la latence ou la puissance
  **mesurées** sur FPGA embarquée, pour un CNN de vision.
- Statut : hypothèse pour la NAS. Nuancé : la quantification mixte automatique vers FPGA
  existe (Campos), sur de petits modèles.
- Piste : appliquer HAWQ + ILP (Campos) à un encodeur convolutif ou à une tête YOLO, puis
  générer avec hls4ml ou FINN via QONNX.

## Apprentissage continu embarqué

### Pas de comparaison MCU / FPGA / Jetson pour un même algorithme de CL
- Constat :
  - O-FSCIL sur MCU GAP9 seulement (arxiv-2403.07851) ;
  - ImageHD sur ZCU104, face au CPU, au GPU et au Jetson (arxiv-2604.21280) ;
  - (7e passage) **QLR-CL** : VEGA (ASIC PULP 22 nm) face au STM32L4 avec le **même
    code**, 65× plus rapide et 37× plus économe. Aucune FPGA
    (arxiv-2110.10486-tinyml-platform-device-continual-learning, §V-E, Table IV) ;
  - (7e passage) **ONLAD** : FPGA (PYNQ-Z1) face au CPU et au GPU en TensorFlow ; ni MCU ni
    Jetson (2019-tsukada-neural-network-device-learning-anomaly, §6).
- Ce qui manque : un même algorithme de CL mesuré sur les trois cibles.
- Statut : **étayé (5 fiches)**. Aucune des 5 fiches CL ne couvre plus de deux familles de
  plateformes.
- Piste : porter QLR-CL (étage figé INT8) ou ONLAD sur KV260 et sur un Jetson Orin, avec la
  même mesure de puissance. L'accélérateur SLDA de `basicStart.txt` reste derrière un
  paywall.

### Apprentissage embarqué par rétropropagation sur FPGA
Nouveau au 7e passage.
- Constat : les apprentissages sur FPGA du corpus **évitent la rétropropagation** :
  - ONLAD met à jour des poids de sortie par moindres carrés récursifs (OS-ELM, batch 1,
    sans inversion matricielle), avec des poids d'entrée aléatoires figés
    (2019-tsukada-neural-network-device-learning-anomaly, §3.1, §3.3) ;
  - ImageHD fait de l'hyperdimensionnel (arxiv-2604.21280) ;
  - la seule rétropropagation embarquée du corpus (queue de MobileNet-V1 en FP32) tourne
    sur **VEGA, un ASIC multicœur RISC-V**
    (arxiv-2110.10486-tinyml-platform-device-continual-learning, §IV-B) ;
  - Venieris jugeait l'entraînement sur FPGA « à peine exploré » en 2018
    (2018-venieris-toolflows-mapping-convolutional-neural-networks, §3.2, objectif 5).
- Ce qui manque : un apprentissage continu par rétropropagation d'une queue de réseau (type
  QLR-CL) sur SoC FPGA. L'étage figé INT8 serait accéléré en PL ; la mise à jour se ferait
  sur le PS ou dans un moteur PL, avec la latence par événement et l'énergie mesurées.
- Statut : étayé (4 fiches) dans le corpus ; hypothèse pour la littérature (les papiers
  d'entraînement sur FPGA ne sont pas ingérés ; arxiv-2206.15472, entraînement sur MCU, est
  à ficher).
- Piste : `/paper-discover "on-device training FPGA backpropagation"`. **Question de thèse
  candidate** (voir les pistes en fin de passage).

### Adaptation à la dérive pour la détection d'anomalies embarquée
Nouveau au 7e passage.
- Constat :
  - ONLAD est le seul travail du corpus au croisement `continual-learning` ×
    `autoencoder-fpga`. Son mécanisme d'oubli fait passer l'AUC de 0,55-0,59 sans oubli à
    0,78-0,90 sous dérive simulée (2019-tsukada-neural-network-device-learning-anomaly,
    Table 5) ;
  - les données sont tabulaires ou des images aplaties ; la dérive est simulée par
    permutation de classes ; le modèle n'a qu'une couche cachée (§5.1, §5.2) ;
  - Malviya évoque la surveillance de machines, dont l'état dérive, mais fixe son seuil
    une fois pour toutes (μ + σ) (2022-malviya, §III).
- Ce qui manque : un détecteur d'anomalies visuelles embarqué qui adapte son modèle ou son
  seuil à la dérive (éclairage, usure), sur FPGA.
- Statut : hypothèse (2 fiches).
- Piste : ONLAD appliqué aux caractéristiques d'un encodeur CNN figé, sur KV260.

### CL sur FPGA : précision faible et énergie estimée
- Constat :
  - ImageHD : 26,89 % d'ACC, énergie estimée (arxiv-2604.21280, Table VII) ;
  - (7e passage) ONLAD a une puissance de carte mesurée (3,1 W) mais n'évalue la précision
    qu'en logiciel, sans latence absolue dans le texte (2019-tsukada, §6.2, §6.4).
- Ce qui manque : la frontière précision / énergie d'un CL supervisé mesurée sur la même
  carte.
- Statut : étayé (2 fiches).
- Piste : Chameleon (TCAD 2024, paywall).

### CL limité à la classification
- Constat : FSCIL, ImageHD et QLR-CL (Core50) font de la classification ; ONLAD fait de
  l'anomalie sur données non visuelles (arxiv-2403.07851, arxiv-2604.21280,
  arxiv-2110.10486, 2019-tsukada). La couverture croisée de `benchmarks.csv` n'a **aucune
  ligne** détection × apprentissage continu.
- Ce qui manque : l'incrémental de classes en détection (YOLO) sur cible embarquée.
- Statut : étayé (4 fiches). Question de thèse candidate (`yolo-fpga` × `continual-learning`).
- Piste : « class-incremental object detection edge FPGA ».

## Surveys

### Surveys : « embarqué » sans FPGA, ou « FPGA » sans comparaison chiffrée entre plateformes
- Constat :
  - « embarqué » sans FPGA ou presque : arxiv-2411.01431, 2025-el-zeinaty (§8),
    2024-mittal (§4.3.3), 2023-shuvo (§XI-C1) ;
  - « FPGA » sans comparaison chiffrée avec Jetson ou MCU : 2025-hozhabr (Table 5),
    arxiv-2509.04153, arxiv-1806.01683 ;
  - (7e passage) Venieris : dédié aux toolflows FPGA, sans GPU ni puissance ni précision
    dans ses tableaux comparatifs
    (2018-venieris-toolflows-mapping-convolutional-neural-networks, Tables 2-5).
- Ce qui manque : une synthèse quantitative FPGA / Jetson / MCU à NPU sur des critères
  communs.
- Statut : étayé (8 surveys). Argument de positionnement.
- Piste : citer ce manque dans l'état de l'art du pré-projet.

### Détection sur MCU et sur petit FPGA : aucune passerelle
- Constat :
  - côté MCU : MCUNetV2, XiNet et TinyissimoYOLO (2025-el-zeinaty, Table 8 ;
    arxiv-2110.15352, Table 3 ; arxiv-2306.00001, Table II) ;
  - côté FPGA : YOLOv3-tiny élagué sur XC7Z035 (2023-zhai, Table 8) ;
  - CNN minuscule sur XC7Z020 (arxiv-2101.05108, Table 4) ;
  - (7e passage) DAC-SDC ajoute des détecteurs compressés sur Zynq-7020 : SqueezeNet
    binaire + YOLO avec 64 Ko de poids et 154 M multiplications, à 25,97 FPS
    (2021-xu-dac-sdc-low-power-object, §4.2, §5.2.1). Ce sont des tailles de l'ordre de
    celles des MCU, mais sans portage MCU ;
  - (7e passage, hors détection) QLR-CL fait l'exercice MCU contre ASIC avec le même code,
    mais pas contre une FPGA (arxiv-2110.10486, §V-E) ; le CAE de Malviya (8 755
    paramètres) tiendrait sur un MCU, sans que ce soit mesuré (déduit, 2022-malviya).
- Ce qui manque : pour un même détecteur compressé, la frontière latence / énergie / mAP sur
  MCU (GAP9, STM32N6) et sur petit FPGA, à portée d'énergie égale.
- Statut : hypothèse (6 fiches).
- Piste : porter TinyissimoYOLO ou le réseau SystemsETHZ (code DAC-SDC publié, 2021-xu §1)
  sur FPGA et sur MCU.
