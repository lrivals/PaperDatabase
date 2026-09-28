---
id: 2018-flamand-gap-8-risc-v-soc
fiche: done
date: 2026-09-28
---

# GAP-8: A RISC-V SoC for AI at the Edge of the IoT

Eric Flamand, Davide Rossi, Francesco Conti, Igor Loi, Antonio Pullini, Florent Rotenberg, Luca Benini, 2018, 2018 IEEE 29th International Conference on Application-specific Systems, Architectures and Processors (ASAP) 1-4. https://doi.org/10.1109/ASAP.2018.8445101
Type : conférence (papier court, 4 pages)

## Problème

Les nœuds IoT sur batterie, conçus pour des années d'autonomie, se limitent à des capteurs à
faible débit (température, pression). Traiter à la source des capteurs riches (image, son,
vibrations) exige plus de 1 GOPS dans une enveloppe de quelques mW (Abstract, §I). La
transmission brute coûte trop d'énergie radio ; une signature extraite est au moins
5 ordres de grandeur plus petite qu'une image (§I).

## Méthode

Présentation d'un SoC, issu de la plateforme open source PULP :
- **Fabric Controller** (§II-A) : MCU RISC-V avec extensions DSP, 512 kB de L2, uDMA
  pour les périphériques (QSPI, I2C, I2S, caméra). Il dispose d'une interface **PWM
  4 canaux pour le contrôle moteur**, « for use in applications such as drones ».
- **Cluster** de 8 cœurs RISC-V (RV32IMC étendu : boucles matérielles, SIMD 4×8 bits ou
  2×16 bits, MAC en un cycle), L1 partagée à accès en un cycle, synchronisation matérielle
  et clock-gating par cœur (§II-B). Mémoire sans cache de données : les transferts sont
  explicites par DMA.
- **HWCE** (Hardware Convolution Engine) : une convolution 5×5, ou trois 3×3, par cycle
  sur des opérandes de 4, 8 ou 16 bits (§II-C). Gain d'efficacité énergétique de 4 à 5×
  face au logiciel parallèle, jusqu'à 10× avec des poids de 8 ou 4 bits (Fig. 2).
- **Gestion d'énergie** : DC/DC intégré (1,0-1,2 V), deux domaines tension-fréquence
  (FLL), sommeil profond à 3,6 µW, ou 30 µW avec rétention complète de la L2 ; transitions
  en 100 à 150 µs (§II-D).
- **Outillage** : GCC 7.1, OpenMP, PULP-OS ou Mbed. Un **outil d'autotiling** génère le
  code C et les transferts DMA pour tenir dans la L1, et sert de backend à l'export depuis
  TensorFlow (§III, fusionné au §II-D dans l'extraction ; Fig. 3). C'est l'ancêtre de
  GAPflow.

## Plateforme et implémentation

- Silicium **TSMC 55 nm LP** (§I). Puces prototypes mesurées (§IV). Surface et fréquence
  maximale : dans la Fig. 4, non extraite (n/r).
- Crête (Table I, à 100 MHz) : 9,2 GMAC/s en 8×8 bits (SoC 0,4 + cluster 3,2 + HWCE 5,6)
  et 11,2 GMAC/s en 16×4 bits via le HWCE. L'Abstract annonce **10 GMAC/s à 90 MHz et
  1,0 V**, avec **600 GMAC/s/W**, dans une enveloppe de 75 mW au pire cas.
- Modes de puissance (Table II) : FC seul, 27 mW (1,0 V, 150 MHz) ; FC + cluster, 37 mW
  (1,0 V, 150/90 MHz) ; FC + cluster, **75 mW** (1,2 V, 250/170 MHz), « at maximum
  computing workload ». Méthode de mesure non décrite (portée de la puissance :
  `unspecified`).
- Code et outils : PULP est open source (§I), le SDK GAP8 n'est pas référencé par un lien
  dans le texte extrait.

## Résultats

- **CIFAR-10** avec HWCE : **650 µs à 100 MHz, 15 mW, 10 µJ** par inférence (§IV).
  Selon les auteurs, plus de 700 jours sur une pile AAA à 10 inférences par seconde.
  Architecture du réseau et précision : n/r.
- **Passage à l'échelle** : accélérations quasi idéales de 1 à 8 cœurs sur des noyaux
  d'analyse de données (§IV), et gain de 10× du cluster + HWCE face à un seul cœur sur
  des CNN réels (§V). Les Tables III et IV (cycles par noyau, cycles pour 3 CNN dont
  TextReco, en 16 bits) sont **absentes de l'extraction**.
- Comparaison qualitative avec Mia Wallace, Fulmine, mote SoC et CEVA-XM4 : sommeil
  profond plus d'un ordre de grandeur plus bas, efficacité en crête « similaire » (§IV).

→ reportés dans `benchmarks.csv` (fichier du lot) : 1 ligne (CIFAR-10, 0,65 ms, 15 mW
`unspecified`, §IV, `medium`). Les crêtes de la Table I ne sont pas des configurations
d'inférence, et ne sont pas reportées.

## Limites et critique

- **Chiffres de crête hétérogènes** : 10 GMAC/s à 90 MHz (Abstract) contre 9,2 ou
  11,2 GMAC/s à 100 MHz (Table I) selon la précision. Le §IV écrit « peak performance of
  10 GMAC/s/W », qui est une unité erronée. Le 600 GMAC/s/W est une efficacité de crête du
  HWCE, pas celle d'un réseau complet (déduit).
- **Aucune détection d'objets** ni réseau réaliste de vision embarquée : CIFAR-10
  (32 × 32) seulement, sans précision, et des cycles sur 3 CNN dans une table non
  extraite.
- **Mesure de puissance non décrite** : puce seule ou avec DC/DC, à quelle température ?
  Les 15 mW de CIFAR-10 sont à 100 MHz, sans tension précisée.
- Papier de 4 pages écrit par le concepteur commercial (GreenWaves) : comparaison avec
  les concurrents seulement qualitative.
- Pas de mesure sur drone ni de débit caméra ; la mention des drones se limite au PWM.

## Pertinence pour la thèse

- **Référence matérielle de la gamme nano (mW)** pour l'axe `nano-drone` : c'est la puce
  de l'AI-deck du Crazyflie, utilisée par la plupart des travaux nano-drone du corpus
  (par exemple arxiv-2301.12175 : SSD-MobileNetV2 à 1,6 FPS pour 134 mW à la carte). Elle
  fixe les ordres de grandeur : 512 kB de L2, 64 kB de L1, environ 10 GMAC/s de crête et
  moins de 75 mW au pire cas.
- Montre dès 2018 que la **gestion explicite de la mémoire** (autotiling L3/L2/L1) est le
  cœur de l'effort de portage. Ce point est commun avec les accélérateurs FPGA dataflow,
  et utile pour comparer les chaînes d'outils (déduit).
- Ne dit rien de la détection de petits objets ni de la fiabilité.

## Gaps identifiés

- **Écart entre crête (GMAC/s) et débit réel sur détecteur** : aucun chiffre de détection
  ici ; les papiers applicatifs en donnent (par exemple 5,3 MAC/cycle mesurés pour
  SSD-MbV2 1,0× dans arxiv-2301.12175, Table II).
- **Mesures de puissance non normalisées** en gamme nano : puissance de la puce (ce
  papier) contre carte AI-deck (papiers applicatifs). Même problème de portée que pour
  les FPGA.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). La section III
(« Programming GAP-8 ») n'est pas détectée comme titre : son texte est rattaché au §II-D.
Les Tables III et IV (benchmarks en cycles) et la Fig. 4 (caractéristiques de la puce)
n'ont pas de contenu extrait : leurs chiffres manquent. Les Tables I et II sont lues.

Ce qui suit est déduit et non affirmé par les auteurs :
- le caractère « crête HWCE » du 600 GMAC/s/W ;
- la filiation autotiler → GAPflow ;
- l'usage du GAP8 dans l'AI-deck (connu par arxiv-2301.12175, non dit ici) ;
- l'affiliation commerciale (GreenWaves) des auteurs, absente du texte extrait.
