---
id: arxiv-2110.15352-mcunetv2-memory-efficient-patch-inference
fiche: done
date: 2026-09-24
---

# MCUNetV2: Memory-Efficient Patch-based Inference for Tiny Deep Learning

Ji Lin, Wei-Ming Chen, Han Cai, Chuang Gan, Song Han, 2021, NeurIPS 2021. arXiv 2110.15352
Type : conférence. La venue NeurIPS 2021 vient de 2025-el-zeinaty (Table 8) et n'est pas
imprimée dans la version arXiv lue.

## Problème

Sur MCU, la mémoire limitante est la **SRAM des activations**, pas le nombre de paramètres.
Et la distribution mémoire des CNN est très déséquilibrée : pour MobileNetV2, les 5
premiers blocs dépassent 450 kB, alors que le reste tient dans 256 kB (§1, Fig. 1). Cela
force de petites résolutions d'entrée, ce qui pénalise surtout la détection, plus sensible
à la résolution que la classification (§1, Fig. 2).

## Méthode

- **Inférence par patchs** pour l'étage initial : les n premiers blocs sont exécutés sur p ×
  p régions spatiales qui se recouvrent, le reste couche par couche (§3.1, Fig. 3). Le pic
  mémoire baisse, au prix d'un recalcul dans les zones de recouvrement.
- **Redistribution du champ récepteur :** noyaux plus petits et moins de blocs dans l'étage
  par patchs, plus de blocs ensuite. Pour MobileNetV2, le surcoût de calcul passe de 10 % à
  3 % (§3.2, Table 1).
- **Recherche conjointe architecture + ordonnancement :** recherche évolutionnaire sur un
  super-réseau (espace de type MnasNet, résolution r de 96 à 256, largeur par bloc) et
  sur (p, n), sous contraintes de SRAM, de Flash et de latence (§3.3).
- **Déploiement :** INT8, TinyEngine étendu à l'inférence par patchs. La détection utilise
  une tête YOLOv3 (§4, §4.3).

## Plateforme et implémentation

- MCU : STM32F412 (Cortex-M4, 256 kB SRAM, 1 MB Flash), STM32F746 (Cortex-M7, 320 kB) et
  STM32H743 (Cortex-M7, 512 kB SRAM, 2 MB Flash) (§4).
- Mémoire : profils analytiques (somme des activations) et **mesures sur la carte** (SRAM
  et Flash réellement utilisées, tampons compris) (§4).
- Fréquence d'horloge : n/r. Puissance et énergie : **non mesurées**.
- Code : n/r dans le texte extrait. Une démo vidéo est annoncée, sans lien conservé.

## Résultats

Détection sur Pascal VOC (Table 3, INT8, tête YOLOv3) :

| Modèle | MCU | Param. | MACs | Pic SRAM | mAP VOC |
|---|---|---|---|---|---|
| MbV2 + CMSIS [30] | H743 | 0,87 M | 34 M | 519 kB | 31,6 % |
| MCUNet [30] | H743 | 1,20 M | 168 M | 466 kB | 51,4 % |
| **MCUNetV2-H7** | H743 | 0,67 M | 343 M | 438 kB | **68,3 %** |
| **MCUNetV2-M4** | F412 | 0,47 M | 172 M | 247 kB | **64,6 %** |

Autres résultats :
- **Classification ImageNet (Table 2) :** 71,8 % en top-1 sur H743 (256 M MACs, SRAM
  465 kB) et 64,9 % sur F412 (119 M MACs, SRAM 196 kB).
- **VWW :** plus de 90 % sous 32 kB de SRAM (§4.2, Fig. 7).
- **Pic mémoire (analytique, entrée 224, patchs 4 × 4) :** divisé par 3,7 à 8,0 pour 8 à
  17 % de calcul en plus (Fig. 5).
- **Pic mémoire sur la carte :** divisé par 4 à 6 sur STM32F746 (Fig. 6).
- **Surcoût de latence :** réduit à 4 % avec MbV2-RD (Fig. 6). C'est un pourcentage, sans
  temps absolu.
- **Détection de visages (WIDER FACE, Tables 4 et 7) :** MCUNetV2-S obtient 0,85 / 0,81 /
  0,55 (Easy / Medium / Hard) avec 168 kB en INT8.

→ reportés dans `benchmarks.csv` : 4 lignes (2 en détection sur VOC, Table 3 ; 2 en
classification sur ImageNet, Table 2). **FPS, latence et puissance valent `n/r` partout** :
le papier ne les donne pas pour ces modèles. Paramètres, MACs et pic de SRAM sont dans la
colonne `model`, faute de colonne dédiée.

## Limites et critique

- **Ni latence ni énergie pour la détection.** La contribution est la mémoire. Le temps
  d'inférence n'apparaît qu'en graphiques (VWW, Fig. 7 ; surcoût relatif, Fig. 6) et
  l'énergie jamais. On ne peut donc pas dire si MCUNetV2-H7, à 343 M MACs, tourne en temps
  réel. Par ordre de grandeur (déduit), un Cortex-M7 à quelques centaines de MHz traite
  343 M MACs en plusieurs centaines de millisecondes.
- **Protocole VOC non précisé** (VOC 2007 ou 2012, résolution retenue par la recherche) et
  NMS non décrit. Les mAP VOC ne se comparent pas aux AP COCO.
- **Comparaisons :** les baselines sont les travaux antérieurs du même groupe (MCUNet) ou
  des combinaisons MbV2 + bibliothèque, sur le même MCU : c'est équitable sur la
  contrainte mémoire. Les gains de mAP (+16,9 points) mélangent toutefois architecture,
  résolution et ordonnancement.
- Les données supplémentaires (pseudo-code, ablations) ne sont pas dans le texte extrait.

## Pertinence pour la thèse

- **Le verrou mémoire des activations en tête de réseau est aussi celui des FPGA
  embarqués** en mode dataflow : FINN suppose tout en mémoire on-chip (gap « réseaux qui ne
  tiennent pas on-chip »). L'inférence par patchs est une piste transposable aux BRAM et
  URAM d'un petit FPGA (déduit, non traité par les auteurs).
- **Point de référence MCU pour la détection :** 64,6 % de mAP VOC en 247 kB sur un
  Cortex-M4 à environ 4 $. C'est ce qu'un FPGA doit battre en latence ou en énergie pour
  se justifier sur un budget comparable.

## Gaps identifiés

- **Passerelle MCU ↔ FPGA :** le gap reste ouvert, et ce papier ne fournit pas la latence
  ni l'énergie attendues côté MCU. Pour comparer, il faudrait **mesurer soi-même**
  MCUNetV2-YOLOv3 sur STM32H743 (latence, énergie).
- **Inférence par patchs sur FPGA :** l'ordonnancement spatial par patchs pour réduire le
  pic de BRAM d'un accélérateur dataflow n'est pas couvert dans le corpus (hypothèse).

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, version arXiv, extraction GROBID `ok`). La
section 3.1 n'a pas été détectée comme titre, et son texte est rattaché à l'introduction.
Les valeurs des figures (latence VWW, surcoûts mesurés) ne sont pas dans le texte extrait.

Ce qui suit est déduit et non affirmé par les auteurs :
- l'ordre de grandeur de latence sur Cortex-M7 ;
- la transposition au FPGA ;
- le prix de l'H743 et du F412 est affiché par les auteurs (Table 3), mais sa comparaison
  avec le prix d'un FPGA est de moi.
