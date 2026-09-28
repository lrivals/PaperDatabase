---
id: arxiv-2306.00001-tinyissimoyolo-quantized-low-memory-footprint
fiche: done
date: 2026-09-24
---

# TinyissimoYOLO: A Quantized, Low-Memory Footprint, TinyML Object Detection Network for Low Power Microcontrollers

Julian Moosmann, Marco Giordano, Christian Vogt, Michele Magno, 2023, IEEE AICAS 2023 (d'après le DOI 10.1109/AICAS57966.2023.10168657). arXiv 2306.00001
Type : conférence. La fiche est rédigée sur la version arXiv, un papier court de 4 pages. Une
version IEEE Access 2024, citée par 2025-el-zeinaty avec d'autres chiffres, est un travail
distinct, absent de la base.

## Problème

Faire de la détection d'objets multi-classes sur des MCU de quelques milliwatts, avec moins
de 0,5 Mo de mémoire pour les poids (§I). Selon les auteurs, les travaux de compression
négligent souvent la vitesse d'inférence au profit de la précision.

## Méthode

- **Réseau inspiré de YOLOv1 (§II-A, Fig. 1) :**
  - entrée 88×88, imposée par la limite 90×91 de l'accélérateur du MAX78000 ;
  - convolutions 3×3 uniquement, de 16 à 128 canaux, max-pooling toutes les deux couches ;
  - une couche dense de 256, puis une sortie YOLOv1 en grille 4 × 4.
- **Variantes :** B = 2 boîtes par cellule pour une classe (visages), B = 1 pour trois
  classes (VOC), afin de tenir dans les 442 kB de poids du MAX78000 (§II-A, §II-C).
- **Entraînement :** 350 époques en flottant, puis 300 en quantization-aware training (QAT)
  INT8 ; SGD (§II-B).
- **Données (§II-B) :**
  - WiderFace, avec des restrictions à 10 ou 5 visages maximum par image ;
  - Pascal VOC réduit à 3 classes (person, chair, car) et à 3 objets maximum par image.
- **Déploiement :** TensorFlow Lite Micro sur Cortex-M ; outils Analog Devices pour
  l'accélérateur du MAX78000 (§II-C).

## Plateforme et implémentation

| MCU | Cœur | Tension, fréquence |
|---|---|---|
| MAX78000 | accélérateur CNN intégré | 1,2 V, 50 MHz |
| STM32H7A3 | Cortex-M7 | 3,3 V, 192 MHz |
| STM32L4R9 | Cortex-M4F | 3,3 V, 120 MHz |
| Apollo4b | Cortex-M4F | 1,8 V, 192 MHz |

(§III)

- **Puissance :** mesurée sur **le MCU seul** (« power consumption of the µCs only »,
  §III), selon la méthode de Giordano et al. [27]. C'est une portée puce, mais le texte ne
  donne pas de puissance en watts : seulement une énergie par inférence et des µW/MHz.
- **Mémoire :** 422 kB de poids pour une classe, 398 kB pour trois ; entrée de 25 kB ;
  350 kB de RAM suffisent sur Cortex-M (§III).
- **Code :** non publié (aucun lien dans le texte). Un démonstrateur MAX78000FTHR avec
  capteur CameraCubeChip est décrit (§II-C).

## Résultats

- **MAX78000 :** 5,5 ms par inférence, 107 MAC/cycle, **196 µJ par inférence** (§III,
  Fig. 2). Jusqu'à 180 FPS (Abstract, cohérent avec 1/5,5 ms).
- **STM32H7A3 :** 359 ms par inférence, le deuxième plus rapide (§III). Le MAX78000 est
  plus de 65 fois plus rapide.
- **Apollo4b :** le plus sobre en puissance (59 µW/MHz), mais 6,1 mJ par inférence, soit
  32 fois l'énergie du MAX78000 (§III).
- **STM32L4R9 :** valeurs en figure seulement.
- **Précision :**
  - WiderFace : 45,3 % de mAP sur le jeu complet, jusqu'à 75,4 % sur le jeu restreint
    (Table I) ;
  - VOC 3 classes : **58,5 %** au total ; person 57,4 %, chair 30,2 %, car 65,1 %
    (Table II).
- Les deux réseaux (1 et 3 classes) ont des performances de latence et d'énergie
  « exactement » identiques (§III).

→ reportés dans `benchmarks.csv` : 3 lignes (MAX78000, STM32H7A3, Apollo4b), avec la mAP
VOC 3 classes de la Table II. Elles sont en `confidence: medium`, parce que latence et
énergie viennent du texte qui commente la Fig. 2. L'énergie par inférence figure dans la
colonne `model`, faute de colonne dédiée. `power_w` vaut `n/r` : la puissance en watts
n'est pas donnée, et la déduire de E / t serait une estimation.

## Limites et critique

- **mAP incohérente dans le papier :** 58,5 % (Table II), « jusqu'à 57 % » (§III) et 59 %
  (conclusion). Le survey 2025-el-zeinaty cite encore une autre valeur, 56,4 % avec une
  entrée 112×112, qui vient probablement de la version IEEE Access 2024.
- **mAP non comparable au reste du corpus :** 3 classes sur 20 et au plus 3 objets par
  image, avec une entrée 88×88. Cette mAP ne se compare **pas** aux 64,6-68,3 % de
  MCUNetV2 sur VOC 20 classes, alors que le Tableau 8 de 2025-el-zeinaty les aligne.
- **MACs non rapportés dans cette version.** Déduit : 107 MAC/cycle × 50 MHz × 5,5 ms, soit
  environ 29 M MACs, dans l'ordre de grandeur des 32 à 57 MMACs cités par 2025-el-zeinaty.
- **Comparaison équitable entre MCU** (même réseau, même méthode de mesure), mais sans
  baseline hors MCU (Jetson, FPGA).
- La mAP n'est pas remesurée par cible : elle vient du modèle QAT, sans vérification après
  déploiement sur chaque MCU (déduit ; même motif que le gap « précision non vérifiée sur
  la cible »).
- Papier court : peu de détails sur le NMS et sur la méthode exacte de mesure de puissance.

## Pertinence pour la thèse

- **Premier point MCU mesuré en énergie et en latence dans le corpus :** 196 µJ et 5,5 ms
  sur MAX78000, en portée puce. Face au YOLOv3-tiny FPGA de Zhai et al. (91,65 FPS pour
  12,51 W, soit environ 136 mJ par image, déduit), l'écart d'énergie par inférence est
  d'environ trois ordres de grandeur. Mais les tâches ne sont pas comparables (88×88 et
  3 classes contre 416×416 et UA-DETRAC).
- Montre que l'**accélérateur CNN intégré au MCU**, et non le cœur Cortex-M, fait la
  différence (×65 en latence). Les MCU avec NPU (MAX78000, GAP9, STM32N6) sont les vrais
  concurrents d'un petit FPGA pour la détection à très basse consommation.

## Gaps identifiés

- **Passerelle MCU ↔ FPGA :** précise le gap. Latence et énergie existent côté MCU, mais à
  une résolution (88×88) et une tâche (3 classes) qu'aucun design FPGA du corpus
  n'évalue. Pour une comparaison valable, il faudrait porter le **même** TinyissimoYOLO
  sur un petit FPGA (FINN ou hls4ml, qui conviennent à un réseau aussi petit) et mesurer
  l'énergie par inférence en portée puce, comme ici.
- **Protocole de mesure :** même dans la TinyML, la définition de la mAP (classes retenues,
  nombre d'objets, résolution) varie d'un papier à l'autre et d'une version à l'autre du
  même travail.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, version arXiv, extraction GROBID `ok`). Les
valeurs des Fig. 2 a-d ne sont connues que par le texte qui les commente.

Ce qui suit est déduit et non affirmé par les auteurs :
- les environ 29 M MACs ;
- les environ 136 mJ par image pour Zhai et al., et l'écart d'énergie ;
- l'origine de la valeur 56,4 % de 2025-el-zeinaty ;
- l'absence de remesure de la mAP par cible ;
- l'adéquation à FINN ou hls4ml.
