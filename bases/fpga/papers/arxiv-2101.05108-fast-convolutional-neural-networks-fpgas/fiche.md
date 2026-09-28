---
id: arxiv-2101.05108-fast-convolutional-neural-networks-fpgas
fiche: done
date: 2026-09-26
---

# Fast convolutional neural networks on FPGAs with hls4ml

Thea Aarrestad, Vladimir Loncar, Nicolò Ghielmetti, Maurizio Pierini, Sioni Summers et al. (20 auteurs), 2021, Mach. Learn.: Sci. Technol. 2 045015 (2021). https://doi.org/10.1088/2632-2153/ac0ea1 (texte lu : version arXiv 2101.05108)
Type : article de journal (journal_ref arXiv)

## Problème

hls4ml visait jusque-là les réseaux denses pour le trigger L1 du LHC, avec une latence fixe de
l'ordre de la µs (§1). Les convolutions ne passent pas avec son approche « tout partitionné
en registres ». Une implémentation directe déroulée est limitée à moins de 4 096 itérations par
la limite de partitionnement de Vivado HLS, et im2col coûte O(K²HWC) de mémoire on-chip en
plus (§3). Objectif : des CNN à latence de l'ordre de la µs, entièrement on-chip, générés
automatiquement par hls4ml.

## Méthode

- **Convolution et pooling en flux** (`hls::stream`, synthétisés en FIFO) : une variante
  d'im2col qui traite un vecteur colonne à la fois, avec un buffer de fenêtre glissante de K²
  streams (§3, Fig. 1). La latence d'une couche est d'au moins HW cycles.
- **Instructions précalculées** : un masque binaire de K² bits indique à quelles positions de
  la fenêtre chaque pixel contribue. Ce masque supprime tout le code de branchement (bords,
  comptage), et le tableau d'instructions est compressé à 5 × 5 entrées pour un noyau 3 × 3 de
  stride 1, quelle que soit la taille d'image (§3, Fig. 2).
- **Modèle de référence** : classifieur SVHN 32 × 32 × 3, 3 blocs conv (16, 16 et 24 filtres,
  noyaux 3 × 3, max pool 2 × 2) et 2 couches denses (42 et 64). 12 858 poids, 1,71 MFLOP
  (Table 1).
- **Compression** :
  - élagage par magnitude à 50 %, avec l'API TensorFlow (§6) ;
  - PTQ par hls4ml de 16 à 1 bit, avec 6 bits entiers (§7.1) ;
  - QAT par QKeras de 16 à 3 bits, en ternaire et en binaire (§7.2) ;
  - quantification hétérogène par AutoQKeras : modèle AQ à (4, 16, 12) filtres et (15, 16)
    neurones (Table 2).
- **Toolflow** : hls4ml 0.5.0 puis Vivado HLS 2020.1 ; entièrement parallèle avec reuse
  factor R = 1, R étant augmenté pour les petites FPGA (§8).

## Plateforme et implémentation

- **Virtex UltraScale+ VU9P** (xcvu9p-flgb2104-2L) à 200 MHz. Résultats **après synthèse
  logique**, sans placement-routage ni exécution sur carte (§8).
- **Zynq XC7Z020** (xc7z020clg400-1, carte TUL PYNQ-Z2) à 100 MHz : le modèle QP 7 bits est
  « synthétisé et déployé » (§8, Table 4).
- **Puissance** : aucune mesure FPGA. Seule une énergie par couche est estimée par QTools pour
  un procédé 45 nm (Table 1, Table 2). Ce n'est pas une mesure FPGA ; elle n'est pas reportée
  en `power_w`.
- Code : hls4ml est open-source. Les modèles et le firmware du papier : n/r (aucun lien dans le
  texte extrait).

## Résultats

| Modèle (VU9P, R = 1) | Accuracy | DSP | LUT | BRAM | Latence | Source |
|---|---|---|---|---|---|---|
| BF 14 bits (PTQ) | 0,87 | 6 377 (93,2 %) | 228 823 | 66,5 | 1 035 cc (5,2 µs) | Table 3 |
| BP 14 bits (PTQ, élagué 50 %) | 0,93 | 3 341 | 145 089 | 66,5 | 1 035 cc (5,2 µs) | Table 3 |
| Q 7 bits (QAT) | 0,94 | 175 | 150 981 | 67,0 | 1 034 cc (5,2 µs) | Table 3 |
| QP 7 bits (QAT, élagué) | 0,94 | 174 | 111 152 | 67,0 | 1 035 cc (5,2 µs) | Table 3 |
| AQ (hétérogène) | 0,88 | 72 | 48 027 | 32,5 | 1 059 cc (5,3 µs) | Table 3 |
| AQP (hétérogène, élagué) | 0,88 | 70 | 38 795 | 30,5 | 1 059 cc (5,3 µs) | Table 3 |

- **XC7Z020, QP 7 bits** : 213 DSP (97 %), 48 259 LUT (91 %), 122 BRAM 18 kb (44 %),
  latence de 17 085 cycles (171 µs), 2 831 images/s (Table 4).
- En PTQ, plus aucun pouvoir discriminant sous 14 bits. En QAT, la précision tient jusqu'à
  3 à 4 bits ; en binaire, elle tombe à 72 % (64 % si élagué) (§7, §8, Fig. 11, Fig. 12).
- La latence (≈ 5 µs) ne dépend pas de la largeur de bits. Elle croît linéairement avec la
  taille d'entrée, la profondeur et R (§8, Fig. 14, 16, 17, 18).
- Le modèle AQ consomme environ 90 % d'énergie estimée en moins que le BF (QTools 45 nm,
  §7.2).

→ reportés dans `benchmarks.csv` : 7 lignes, 6 sur VU9P (Table 3) et 1 sur XC7Z020 (Table 4).
`confidence: high` (tableaux lus par GROBID) ; puissance n/r.

## Limites et critique

- **Tâche et échelle éloignées de la vision embarquée réelle** : classification de chiffres
  32 × 32, modèle de 12,9 k poids. Aucune détection, aucune entrée de résolution caméra.
  La Fig. 17 montre une latence linéaire en H × W (jusqu'à 256 × 256, une seule couche).
- **Ressources après synthèse logique seulement** sur VU9P : pas de placement-routage, pas de
  fréquence atteinte, pas d'exécution sur carte. Seul le XC7Z020 est déployé.
- **Aucune puissance FPGA.** L'« énergie » QTools est une estimation ASIC 45 nm, sans rapport
  avec la consommation d'une FPGA.
- **Aucune comparaison externe** : ni FINN, ni Vitis AI, ni GPU ou CPU. Les travaux liés de la
  §2 sont perdus en partie à l'extraction.
- **BF 14 bits à 0,87 contre BP 14 bits à 0,93** : le modèle élagué fait mieux que le non élagué
  en PTQ. Les auteurs l'attribuent aux erreurs d'arrondi (§8).
- Anomalie de ressources non expliquée (BF 12 bits, R = 1 contre R = 6, Annexe).

## Pertinence pour la thèse

C'est la référence du volet CNN de hls4ml : architecture streaming à fenêtre glissante, QAT
QKeras et quantification hétérogène, avec un point sur une petite FPGA (Zynq-7020 : 171 µs,
2 831 images/s). La recette QAT (précision intacte à 7 bits, DSP divisés par environ 36) est
directement transposable à un encodeur ou à un détecteur. En revanche, le papier ne dit rien
de la détection, des images de grande taille, de la puissance, ni des toolflows concurrents.
Le gap « comparaison croisée hls4ml / FINN / Vitis AI » reste entier.

## Gaps identifiés

- CNN hls4ml sur SoC embarqué : un seul point (XC7Z020), sans puissance et sans modèle plus
  gros que SVHN. Rien sur la détection (YOLO) par hls4ml.
- Pas de comparaison hls4ml / FINN / Vitis AI sur le même CNN et la même carte ; ce papier
  alimente ce gap déjà identifié.
- Streaming à la résolution d'une caméra : la latence linéaire en H × W n'est mesurée que pour
  une seule couche.

## Statut de lecture

Papier complet (`fulltext.md` en entier, extraction GROBID après ré-extraction). La section 2
(travaux liés) est en partie fusionnée dans l'introduction et tronquée. La fin de la §8 est
coupée au milieu d'une phrase (« For simplicity, we assume an input size of » ; la suite est
dans « Figures et tableaux »). Les tableaux 3 et 4 sont lus par GROBID, avec des colonnes
fusionnées mais des valeurs lisibles et cohérentes avec les pourcentages.
Ce qui suit est déduit et non affirmé par les auteurs : le facteur 36 environ de réduction des
DSP (6 377 → 175, BF 14 bits contre Q 7 bits) ; l'absence d'exécution sur carte pour le VU9P
(le texte dit « after logic-synthesis ») ; le jugement « éloigné de la vision embarquée ».
