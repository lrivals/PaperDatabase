---
id: 2021-xu-dac-sdc-low-power-object
fiche: done
date: 2026-09-26
---

# DAC-SDC Low Power Object Detection Challenge for UAV Applications

Xiaowei Xu, Xinyi Zhang, Bei Yu, Xiaobo Sharon Hu, Christopher Rowen, Jingtong Hu, Yiyu Shi, 2021, IEEE Transactions on Pattern Analysis and Machine Intelligence 43(2), 392-403. https://doi.org/10.1109/TPAMI.2019.2932429
Type : article de journal (IEEE TPAMI, relu par les pairs). Compte rendu de compétition
(DAC System Design Contest 2018), rédigé par les organisateurs.

## Problème

Les benchmarks de détection (ImageNet, PASCAL VOC) ne jugent que la précision. Pour les
drones, il faut aussi le débit temps réel et l'énergie sur plateforme embarquée (§1). Les
auteurs présentent un concours qui évalue conjointement **précision, débit et énergie** sur
deux plateformes imposées (Jetson TX2 et PYNQ-Z1), avec un jeu d'images de drone, et
analysent les solutions gagnantes.

## Méthode

- **Tâche** : détection d'**un seul objet** par image (objet spécifique, pas une catégorie),
  images 640 × 360 prises par drone (DJI), 12 catégories / 95 sous-catégories, 150 k images,
  70 % entraînement / 30 % test caché (§2.1, §3). Objets très petits : la plupart occupent
  1-2 % de l'image (§3).
- **Plateformes** (§2.2) : PYNQ-Z1 (XC7Z020-1CLG400C : 53 K LUT, 220 DSP, 630 Ko BRAM,
  512 Mo DDR3 ; « environ 1-4 W ») et Jetson TX2.
- **Évaluation** (§2.3) : IoU moyen ; débit minimal 20 FPS (GPU) et 5 FPS (FPGA), avec
  pénalité proportionnelle en dessous (Eq. 2) ; énergie sur tout le jeu de test, mesurée par
  les moniteurs internes pour le TX2 et par un **wattmètre** pour la carte FPGA (échantillonné
  à « 0,01 Hz » selon le texte). Score total = IoU × (1 + ES), avec ES logarithmique en
  énergie relative à la moyenne des équipes (Eq. 3-6), bases log différentes pour FPGA (2)
  et GPU (10).
- Analyse statistique par bootstrap (20 000 tirages, IC 99,9 %) (§5.1.1).
- Analyse des méthodes des 3 meilleures équipes par catégorie (§4) et des résultats par
  catégorie, taille d'objet, luminosité et quantité d'information (§5).

## Plateforme et implémentation

Implémentations des équipes, pas des auteurs. Côté FPGA (§4.2, Table 1) :

| Équipe | Réseau | Précision | Flot | LUT / FF / BRAM / DSP |
|---|---|---|---|---|
| TGIIF (1er) | SSD élagué (14,2× moins de paramètres, 10× moins d'opérations) | 8 bits fixe | Verilog | 83,89 % / 54,24 % / 78,93 % / 100 % |
| SystemsETHZ (2e) | SqueezeNet + YOLO, « halfFire » binaires, 18 conv. | 8 bits (1re couche) / 5 bits (activations) / binaire | HLS | 88 / 62 / 77 / 78 % |
| iSmart2 (3e) | MobileNet + YOLO, IP de convolution séparable réutilisée | n/r | HLS | 63 / 22 / 95 / 86 % |
| traix | SSD | 16 bits fixe | HLS | 90 / – / 90 / 90 % |

Toutes les équipes FPGA redimensionnent l'image sur l'ARM et stockent les cartes
intermédiaires en DDR (§4.2). Code et jeu d'entraînement des 3 premiers de chaque catégorie :
https://github.com/xyzxinyizhang/2018-DAC-System-Design-Contest (§1).

## Résultats

- Participation : 24 équipes sur 53 ont abouti côté GPU, 7 sur 61 côté FPGA (§4.1, §4.2).
  Tiny YOLO domine côté GPU (§4.1).
- FPGA (§5.2.1) :
  - TGIIF : IoU **0,6238**, **11,96 FPS** ;
  - SystemsETHZ : IoU 0,4919, 25,97 FPS ;
  - iSmart2 : IoU 0,5733, 7,35 FPS ;
  - traix : IoU 0,6100 (FPS n/r dans le texte).
- GPU : meilleurs IoU, puissance et FPS **observés** (pas pour une même équipe) : 0,6975,
  4 834 mW, 58,91 FPS (§5.1.1, Fig. 9).
- Puissances et énergies par équipe : en Fig. 9 et Fig. 12, **non extraites** → `n/r`.
- Enseignement des auteurs : le FPGA atteint « presque la même précision » pour 1/3 à 1/2 de
  l'énergie du GPU, avec un FPS plus faible (§5.3). Cet énoncé n'est pas chiffré dans le texte
  extrait.
- Difficultés : petits objets, objets similaires, faible luminosité (§5.1.2-5.1.5, §5.3).

→ reportés dans `benchmarks.csv` : **4 lignes** — les 4 équipes FPGA dont l'IoU est donné
dans le texte (TGIIF, SystemsETHZ, iSmart2, traix). Mesures faites par les organisateurs sur
un protocole commun, d'où leur intérêt, mais ce ne sont pas des travaux des auteurs.
Puissance et ressources absolues `n/r` (figures non extraites, ressources en %). Aucune
ligne GPU : les valeurs données sont des maxima par métrique, pas des configurations.

## Limites et critique

- **Métrique de précision atypique** : IoU moyen d'un seul objet par image, sans mAP ; non
  comparable aux mAP COCO / VOC des autres papiers.
- **Score composite** avec bases log différentes pour FPGA et GPU : le classement ne se
  transpose pas d'une catégorie à l'autre ; les auteurs comparent pourtant FPGA et GPU en
  énergie (§5.3) sans chiffres dans le texte.
- Échantillonnage de puissance FPGA à « 0,01 Hz » : soit une coquille (100 Hz ?), soit une
  mesure très grossière (déduit, à vérifier dans le PDF).
- Plateformes 2018 (Zynq-7020, TX2) ; aucun contrôle des modes de puissance du TX2, ce qui
  explique la grande dispersion côté GPU (§5.1.1).
- Chiffres détaillés (puissance, énergie, score) seulement dans les figures ou sur le site
  du concours.

## Pertinence pour la thèse

Référence pour l'axe `platforms` et le protocole expérimental : c'est l'un des rares
contextes où **FPGA embarqué et Jetson sont mesurés par un tiers selon le même protocole**
(même jeu, même mesure d'énergie, débit minimal imposé). Les solutions FPGA gagnantes (SSD
élagué 8 bits, SqueezeNet binaire + YOLO, MobileNet + YOLO) servent de points de départ
historiques pour la détection de petits objets sur Zynq. Les éditions suivantes du DAC-SDC
(SkyNet, iSmart…) prolongent cette ligne (déduit, à vérifier avant de les citer).

## Gaps identifiés

- Protocole commun FPGA vs GPU embarqué : existe ici (2018) mais reste rare dans la
  littérature ; à reproduire sur Kria KV260 contre Jetson Orin (déduit).
- Détection de **petits objets** vus de drone sur FPGA : difficulté majeure identifiée, peu
  traitée par les accélérateurs YOLO génériques.
- Absence de mAP standard : résultats difficilement comparables au reste du corpus.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Fig. 9 et Fig. 12 (puissance, énergie, scores
par équipe) non extraites ; §5.3 tronqué au début (texte des exemples difficiles fusionné).
Déduit et non affirmé par les auteurs : coquille probable sur 0,01 Hz ; continuité avec
les éditions suivantes du concours ; transposition du protocole au KV260.
