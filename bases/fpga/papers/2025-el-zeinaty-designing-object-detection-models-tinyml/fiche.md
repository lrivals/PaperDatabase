---
id: 2025-el-zeinaty-designing-object-detection-models-tinyml
fiche: done
date: 2026-09-24
---

# Designing Object Detection Models for TinyML: Foundations, Comparative Analysis, Challenges, and Emerging Solutions

Christophe El Zeinaty, Wassim Hamidouche, Glenn Herrou, Daniel Menard, 2025, ACM Comput. Surv. 58(2), 50. https://doi.org/10.1145/3744339
Type : article de journal (survey, ACM Computing Surveys)

## Problème

Déployer la détection d'objets (OD) sur des microcontrôleurs (MCU) avec moins de 1 Mo de
mémoire (§1). Selon les auteurs, les surveys existants traitent surtout du backbone et
n'analysent pas les techniques d'optimisation pour la TinyML (Table 1). Ils couvrent donc
backbone, neck et head sous l'angle de quatre techniques : quantification, pruning,
distillation (KD) et NAS.

## Méthode

Survey, sans expérience propre. Plan :
- rappels sur l'OD et ses fonctions de perte (§2) ;
- jeux de données (§3) ;
- métriques (§4) : mAP VOC et COCO ; MACs / FLOPs (indépendants de la cible) ; mémoire,
  temps d'exécution et énergie (dépendants de la cible) ;
- plateformes TinyML (§5, Table 4) ;
- techniques d'optimisation (§6, Tables 5-6) ;
- détecteurs déployés sur MCU (§7, Tables 7-8) ;
- défis ouverts (§8).

Les chiffres sont repris des articles cités (note sous la Table 5) : les auteurs ne les
ont pas remesurés.

## Plateforme et implémentation

Pas d'implémentation propre. Plateformes recensées (Table 4, spécifications constructeur
et prix approximatifs) :

| Plateforme | Cœur | Fréquence | SRAM | Accélérateur IA |
|---|---|---|---|---|
| STM32H743 | Cortex-M7 | 480 MHz | 1 MB | non |
| STM32F746 | Cortex-M7 | 216 MHz | 320 KB | non |
| STM32N6 | Cortex-M55 + NPU | 800 MHz | 4,2 MB | oui |
| GAP9 | cluster RISC-V 8 cœurs | 175 MHz | 1,6 MB | oui |
| Kendryte K210 | RISC-V double cœur | 400 MHz | 512 KB | oui (KPU) |
| MAX78000 | Cortex-M4F | 100 MHz | 128 KB | oui (accélérateur CNN) |
| ESP32 | Tensilica LX6 double cœur | 240 MHz | 520 KB | non |
| Himax WE-I Plus | ARC EM9D DSP | 400 MHz | 2 MB | non |

Code : l'abstract annonce un « public repository » de suivi du domaine, mais le lien est
perdu dans le texte extrait (« Link »). À récupérer sur la page ACM.

## Résultats

Table 8 (détecteurs sur MCU, INT8 poids et activations, PASCAL VOC, chiffres repris des
articles cités) :

| Modèle | MCU | Entrée | MMACs | Pic SRAM | mAP VOC |
|---|---|---|---|---|---|
| MCUNetV1-YOLOv2 (NeurIPS 2020) | STM32H743 | 224×224 | 168 | 466 kB | 51,4 % |
| MCUNetV2-YOLOv3-M4 (NeurIPS 2021) | STM32F412 | 224×224 | 172 | 247 kB | 64,6 % |
| MCUNetV2-YOLOv3-H7 (NeurIPS 2021) | STM32H743 | 224×224 | 343 | 438 kB | 68,3 % |
| EtinyNet-SSD (AAAI 2022) | STM32H743 | 256×256 | 164 | 395 kB | 56,4 % |
| XiNet-YOLOv7-S (ICCV 2023) | STM32H743 | 256×256 | 80 | 53 kB | 54,0 % |
| XiNet-YOLOv7-M | STM32H743 | 384×384 | 220 | 138 kB | 67,0 % |
| XiNet-YOLOv7-L | STM32H743 | 416×416 | 789 | 511 kB | 74,9 % |
| TinyissimoYOLO (IEEE Access 2024) | GAP9 | 112×112 | 55 | n/r | 56,4 % |

Autres points :
- TinyissimoYOLO : de 441 k à 887 k paramètres et de 32 à 57 MMACs, contre 20 GMACs pour
  YOLOv1 ; QAT INT8 avec QuantLab (§7).
- MCUNetV1 : TinyEngine réduit la mémoire d'un facteur 3,4 et accélère de ×1,7 à ×3,3 (§7).
- MCUNetV2 : la convolution depthwise in-place réduit le pic mémoire d'un facteur 1,6 (§7).
- Travail des auteurs [164] : NAS guidée par LLM, avec KD depuis un ViT, sur STM32H7
  (contrainte de 320 KB de SRAM). Temps de recherche réduit de 12,5 à 1,5 jours (§6.4.2).

→ reportés dans `benchmarks.csv` : aucune ligne. C'est un survey : les chiffres viennent
des papiers cités, et chacun est à ficher à la source (MCUNetV2 et TinyissimoYOLO sont déjà
dans la base).

## Limites et critique

- **Ni latence, ni FPS, ni énergie dans la Table 8.** La comparaison des détecteurs sur MCU
  se limite à mAP, MMACs et pic de SRAM, alors que le §4.2 présente le temps d'exécution et
  l'énergie comme des métriques clés. Aucune comparaison temps réel entre détecteurs MCU
  n'est donc possible à partir de ce survey.
- **mAP non comparables entre lignes :**
  - résolutions de 112×112 à 416×416 ;
  - MCU différents (M4, M7, RISC-V GAP9) ;
  - protocoles VOC non précisés (07 ou 12, 11 points ou non) ;
  - les VOC mAP@0.5 ne sont pas comparables aux AP50:95 COCO de la Table 5 : même
    remarque que pour le corpus FPGA.
- **Valeurs à vérifier à la source :**
  - EtinyNet-SSD et TinyissimoYOLO ont exactement la même mAP (56,4 %) : coïncidence ou
    erreur de recopie ;
  - TinyissimoYOLO est daté « IEEE Access (2024) », alors que la version du corpus est
    arXiv 2306.00001 (AICAS 2023) : ce sont probablement deux publications différentes ;
  - la Table 5 est tronquée dans l'extraction.
- **FPGA à peine traité :** il n'apparaît qu'au détour du §6.1.3 (REQ-YOLO) et du §8
  (CFU Playground). Le survey ne compare pas MCU et FPGA.
- Pas d'analyse critique des protocoles de mesure des papiers cités.

## Pertinence pour la thèse

- Carte de référence pour le **bas de gamme MCU** de la vision embarquée, absent du corpus
  jusqu'ici. On y voit l'ordre de grandeur : 55 à 789 MMACs, 53 à 511 kB de SRAM, 51 à
  75 % de mAP VOC.
- Les défis du §8 (co-design matériel-logiciel, RISC-V, NAS « hardware-aware »,
  transformers sur MCU) recoupent les thématiques FPGA de la thèse.
- **Piste d'encadrement :** l'équipe INSA Rennes (Menard, Herrou) travaille sur la NAS
  hardware-aware pour STM32 [164] et publie en ACM CSUR. Voir [labs.md](../../labs.md).

## Gaps identifiés

- **Protocole de mesure :** étend le gap au monde MCU. Les tableaux comparatifs de
  détecteurs TinyML ne donnent ni latence ni énergie (Table 8).
- **Pas de passerelle MCU ↔ FPGA :** aucun papier du corpus ne compare un même détecteur
  compressé (MCUNetV2-YOLOv3, TinyissimoYOLO) sur MCU et sur petit FPGA (Zynq-7000, KV260)
  à mAP égale (déduit). Ce serait une expérience de thèse chiffrable.
- **Transformers de détection sur MCU :** les auteurs les jugent « largement inexplorés »
  (§8, point 9). Côté FPGA : à vérifier.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). Les Tables 5, 6 et 7
sont partiellement tronquées dans l'extraction.

Ce qui suit est déduit et non affirmé par les auteurs :
- la non-comparabilité des mAP entre lignes de la Table 8 ;
- le doute sur la valeur 56,4 % en double ;
- l'absence de passerelle MCU ↔ FPGA ;
- le rattachement à l'IETR (non imprimé dans le papier, voir labs.md).
