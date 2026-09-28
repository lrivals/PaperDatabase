---
id: arxiv-2011.07317-memory-efficient-dataflow-inference-deep
fiche: done
date: 2026-09-26
---

# Memory-Efficient Dataflow Inference for Deep CNNs on FPGA

Lucian Petrica, Tobias Alonso, Mairin Kroes, Nicholas Fraser, Sorin Cotofana, Michaela Blott, 2020, arXiv preprint. https://arxiv.org/abs/2011.07317
Type : **preprint non relu par les pairs** (version arXiv). Une version publiée en conférence
(ICFPT 2020 ?) est possible mais **non vérifiée** ; les métadonnées portent l'avertissement
« à vérifier à la main ».

## Problème

Les accélérateurs **dataflow** (une unité de calcul par couche, poids en mémoire on-chip,
style FINN) offrent la meilleure latence et la meilleure efficacité énergétique, mais ne
passent pas à l'échelle : la **mémoire on-chip (OCM)** est le goulot (§I, Table I : BRAM de
78 à 100 % sur Zynq 7020 pour BNN-Pynq). La cause : les formes des mémoires de poids,
dictées par le parallélisme (PE × SIMD), les noyaux 3 × 3 et l'élagage, correspondent mal aux
blocs BRAM de 18 Kb, dont une grande partie reste vide (§II-B, Eq. 1).

## Méthode

- **ResNet-50 quantifié pour FINN** (Brevitas) : poids des ResBlocks binaires (W1) ou
  ternaires (W2), première et dernière couches en INT8, activations 2 bits (4 bits autour des
  additions résiduelles) (§III-A). Précision ImageNet top-1 / top-5 : 67,27 / 87,64 % (W1A2)
  et 69,85 / 89,38 % (W2A2).
- Implémentation dataflow avec la bibliothèque HLS de FINN, composants ajoutés en C++
  (seuillage, duplication de flux, addition) ; poids en BRAM, activations, FIFO et dernière
  couche en URAM ; floorplan manuel sur Alveo U250 (§III-B, Fig. 5).
- **FCMP (Frequency Compensated Memory Packing)** (§IV) :
  - MVAU scindé en un bloc mémoire (lecture des poids en flux) et un bloc calcul, dans deux
    îlots d'horloge GALS reliés par des FIFO asynchrones AXI-Stream ;
  - mémoire cadencée R_F fois plus vite que le calcul, donc 2·R_F ports virtuels par BRAM
    (Eq. 2) ;
  - regroupement des tampons de poids par algorithme génétique ([18]) jusqu'à H_B = 3 ou 4
    tampons par BRAM (Table III), avec un streamer RTL adaptatif pour les ratios
    fractionnaires (Fig. 7b).
- Toolflow : **FINN** (HLS) + streamer Verilog publié sur GitHub (§V ; lien en note non
  extrait).

## Plateforme et implémentation

- Embarqué : Zynq **XC7Z020** et **XC7Z012S**, accélérateurs CNV-W1A1 / CNV-W2A2 de BNN-Pynq
  (CIFAR-10) (§V).
- Datacenter : **Alveo U250** et **U280** (UltraScale+), Vitis 2019.2 (§III-B).
- RN50-W1A2 sur U250 (Table II) : 195 MHz, 1 027 kLUT, 3 870 BRAM18, 1 611 DSP.
- Puissance : « Max Power » 71 W (Table II), méthode non décrite → `unspecified`.
- Code : une variante de RN50-W1A2 « available online » (§III-B) et le streamer RTL sur
  GitHub (§V) ; liens en notes de bas de page non extraits.

## Résultats

- **RN50-W1A2 sur U250** (Table II) : 67,3 % top-1, **2 703 FPS**, **1,9 ms** de latence
  minimale, 18,3 TOp/s, 71 W max. Contre DoReFaNet-DF (FINN) : +17 points de top-1 ; contre
  ShuffleNetV2-W1A8 [16] : un peu moins précis et moins rapide, mais +25 % en FPS/MHz (§III-B).
- **Efficacité mémoire** (Table IV) :
  - CNV-W1A1 : 126 → 96 BRAM (E 67,6 → 88,7 %) pour 3,9 kLUT de plus (P4) ;
  - CNV-W2A2 : 208 → 188 BRAM (E 79,9 → 88,4 %) ;
  - RN50-W1A2 : 2 320 → 1 632 BRAM sur U250 (E 52,9 → 75,3 %) ; 1 327 BRAM, E 92,6 %, sur
    U280.
  Soit jusqu'à 30 % d'OCM en moins pour environ 5 % de LUT en plus (§I).
- **Implémentation** (Table V) :
  - CNV-W1A1-P4 porté du 7020 au **7012S** sans perte de débit (100 / 200 MHz, LUT 90 %,
    BRAM 97 %) ;
  - RN50-W1A2-U250-P4 : −12 % de débit (183 / 363 MHz) ;
  - RN50-W1A2-U280-P4 : −32 % (138 / 373 MHz, 99 % des LUT), contre −51 % par simple repli
    (folding ×2), soit 38 % plus rapide que le repli ;
  - RN50-W2A2-U250-P4 : synthétisé mais non placé (LUT devenues le goulot).

→ reportés dans `benchmarks.csv` : **3 lignes** — RN50-W1A2 sur U250 (Table II, la seule
configuration avec FPS, latence et ressources absolus), RN50-W1A2-U280-P4 et
CNV-W1A1-7012S-P4 (Table V : débit relatif seulement, FPS absolu `n/r`). Les autres entrées
des Tables IV-V ne concernent que le sous-système mémoire ou ne sont pas implémentées.

## Limites et critique

- **Preprint** non relu (au moins cette version).
- Puissance « Max Power » sans méthode ; une Alveo à 71 W n'est pas comparable à un SoC
  embarqué.
- FPS des configurations empaquetées donnés seulement en relatif (δFPS) ; aucune latence
  mesurée pour les variantes P4.
- Comparaisons de la Table II entre cartes différentes (AWS F1, VCU108, U250) et réseaux
  différents ; les auteurs le reconnaissent en partie (§III-B).
- Côté embarqué, seuls CNV (CIFAR-10, 79,54 %) : ResNet-50 dataflow reste réservé aux
  très grandes cartes.
- Fermeture de timing difficile à 2× la fréquence sur puces multi-SLR (§V, §VI).

## Pertinence pour la thèse

Travail de l'équipe FINN (AMD/Xilinx Research, axe `toolflows`) : il identifie **la BRAM
comme goulot du dataflow** et donne une technique générique (sur-cadencer la mémoire,
regrouper les tampons) pour faire tenir un accélérateur sur une puce plus petite. C'est
directement pertinent pour faire tenir un YOLO ou un encodeur FINN sur KV260, dont la
BRAM/URAM est limitée (déduit). C'est aussi la première démonstration d'un ResNet-50 entier
en dataflow single-chip.

## Gaps identifiés

- FCMP appliqué à la **détection** (YOLO) ou aux autoencodeurs en dataflow : non traité
  (classification seulement).
- Empaquetage des **activations** (FIFO, line buffers) : laissé en travail futur (§VI).
- Intégration automatique de FCMP dans l'exploration de FINN (floorplan multi-SLR) : travail
  futur (§VI).
- Pas de mesure de puissance sur SoC embarqué.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Début de §II (A) fusionné dans la Table I,
fin de §III (topologie ResNet) tronquée ; notes de bas de page (liens GitHub) non extraites.
Déduit et non affirmé par les auteurs : publication en conférence possible (à vérifier) ;
intérêt pour KV260.
