---
id: arxiv-1612.07119-finn-framework-fast-scalable-binarized
fiche: done
date: 2026-09-24
---

# FINN: A Framework for Fast, Scalable Binarized Neural Network Inference

Yaman Umuroglu, Nicholas J. Fraser, Giulio Gambardella, Michaela Blott, Philip Leong, Magnus Jahre, Kees Vissers, 2016, FPGA '17: ACM/SIGDA International Symposium on Field-Programmable Gate Arrays. DOI 10.1145/3020078.3021744 — texte lu : version arXiv https://arxiv.org/abs/1612.07119
Type : conférence (FPGA '17, relue par les pairs ; la version lue est le preprint arXiv, qui porte la mention « To appear in » FPGA 2017, §1)

## Problème

Les CNN en virgule flottante demandent des millions de paramètres et des milliards
d'opérations par image ; or des réseaux entièrement binarisés (BNN : poids et activations
sur 1 bit) atteignent une précision correcte. Les auteurs veulent exploiter ce fait sur
FPGA, où le pic binaire est très supérieur au pic virgule fixe et où un BNN tient en
mémoire on-chip. Selon eux, aucun travail publié n'avait encore implanté un BNN
entièrement binarisé sur FPGA (§2.3).

## Méthode

- **Analyse roofline** (§3.1, Fig. 1) sur une Zynq UltraScale+ ZU19EG : 66 TOPS en binaire,
  soit ~16× le pic 8 bits ; AlexNet binarisé = 7,4 Mo de paramètres (contre 50 Mo en 8 bits),
  donc tenable on-chip. Estimation de ~35 000 images/s à 75 % du pic — calcul, pas mesure.
- **Compromis précision / taille** (§3.2, Table 1) : sur MNIST, un BNN a besoin de 2 à 11×
  plus de paramètres et d'opérations qu'un réseau flottant pour la même précision, écart
  jugé compensé par le gain ~16× en débit.
- **Architecture en flux hétérogène** (§4.1, Fig. 2) : un moteur de calcul par couche,
  reliés par des flux on-chip, tous les poids en OCM, un bitfile par topologie. Implémenté
  en Vivado HLS.
- **Optimisations propres aux BNN** (§4.2) :
  - accumulation par popcount : environ moitié moins de LUT et FF qu'une accumulation
    signée (128 bits : 376 LUT / 29 FF contre 759 LUT / 84 FF à 200 MHz, §4.2.1) ;
  - batchnorm + signe remplacés par un seuil (6 LUT au lieu de 2 DSP / 55 FF / 40 LUT,
    §4.2.2) ;
  - max-pooling réduit à un OU booléen (§4.2.3).
- **Bibliothèque matérielle** (§4.3) :
  - MVTU (Matrix-Vector-Threshold Unit) : P PE × S voies SIMD, XNOR-popcount-seuil,
    à la fois weight- et output-stationary ;
  - SWU (Sliding Window Unit) : convolution abaissée en produit matriciel, canaux
    entrelacés ;
  - unité de pooling à line buffers.
- **Folding** (§4.4) : P et S par couche, fixés pour équilibrer les débits (F_n · F_s ≈
  F_clk / FPS visé). Version simplifiée de l'approche de fpgaConvNet ([27]), limitée au
  folding des produits matrice-vecteur.
- Entrée : un BNN entraîné sous Theano (méthode de Courbariaux et al. [5]) et un FPS cible ;
  sortie : une description C++ synthétisable (Fig. 4, légende partiellement extraite).

## Plateforme et implémentation

- Carte Xilinx ZC706, SoC Zynq-7000 **Z7045** (2 × Cortex-A9, 218 600 LUT, 545 BRAM), Ubuntu
  15.04 sur l'ARM, Vivado / Vivado HLS 2016.3, 200 MHz (§5.1).
- Protocole de mesure (§5.1) : 10 000 images de test en DRAM ; débit chronométré par l'hôte.
  Deux puissances, moyennées sur 10 s :
  - **P_chip**, rails de l'alimentation FPGA lus via PMBus ;
  - **P_wall**, carte entière au wattmètre mural.
  La carte consomme ~7 W au repos (§5.2.2).
- Topologies (§5.1, Table 2) :
  - SFC et LFC : MLP 3 × 256 et 3 × 1024 neurones, entrée MNIST binarisée ;
  - MFC : 3 × 512 (§5.2.1) ;
  - CNV : 3 × (conv3×3, conv3×3, maxpool) avec 64-128-256 canaux, puis 2 FC de 512. Pour
    CNV, la première couche reçoit des pixels 24 bits et la dernière sort des valeurs sur 16
    bits.
- Scénarios (§5.1) : `max` = débit maximal ; `fix` = 9 000 FPS imposés (flux 640 × 480 à
  30 FPS découpé en tuiles 32 × 32).
- Code / bitstream : non publiés d'après le texte extrait (aucun lien). Déduit, non affirmé
  par le papier : le dépôt FINN de Xilinx est apparu ensuite ; le vérifier avant de le citer.

## Résultats

Puissance dans `benchmarks.csv` : **P_wall (carte entière)**. P_chip est donné ci-dessous.

| Prototype | Dataset | Précision (§5.1 / Table 4) | FPS | Latence | LUT | BRAM | P_chip | P_wall | GOPS |
|---|---|---|---|---|---|---|---|---|---|
| SFC-max | MNIST | 95,83 % | 12 361 k | 0,31 µs | 91 131 | 130,5 (§5.2.3) ¹ | 7,3 W | 21,2 W | 8 265 |
| LFC-max | MNIST | 98,4 % | 1 561 k | 2,44 µs | 82 988 | 396 | 8,8 W | 22,6 W | 9 086 |
| MFC-max | MNIST | 97,69 % (err. 2,31) | 6 238 k | n/r | n/r | 95 % des BRAM (§5.2.1) | 11,3 W | 28,5 W | 11 613 |
| CNV-max | CIFAR-10 / SVHN | 80,1 % / 94,9 % | 21,9 k | 283 µs | 46 253 | 186 | 3,6 W | 11,7 W | 2 465,5 |
| SFC-fix | MNIST | 95,83 % | 12,2 k | 240 µs | 5 155 | 15,5 (§5.2.3) ¹ | 0,4 W | 8,1 W | n/r |
| LFC-fix | MNIST | 98,4 % | 12,2 k | 282 µs | 5 636 | 114,5 | 0,8 W | 7,9 W | n/r |
| CNV-fix | CIFAR-10 / SVHN | 80,1 % / 94,9 % | 11,6 k | 550 µs | 29 274 | 152,5 | 2,3 W | 10 W | n/r |

Sources : Table 3 et Table 4, sauf mention. DSP : n/r pour tous les prototypes.

¹ Dans la Table 3 extraite, la colonne BRAM est mal alignée : 4,5 pour SFC-max et 16 pour
SFC-fix. Le texte (§5.2.3) donne 130,5 et 15,5 ; j'ai retenu le texte, avec `confidence:
medium` pour ces deux lignes. À vérifier sur le PDF.

Autres résultats :

- **Roofline mesurée** (Fig. 9, texte de légende déplacé par l'extraction) :
  - SFC-max : 8,2 TOPS, limité par la mémoire ;
  - LFC-max : 9,1 TOPS (46 % du roofline), limité par les ressources (BRAM) ;
  - CNV-max : 2,5 TOPS, limité par l'architecture (la SWU est le goulot) ;
  - MFC-max : 11,6 TOPS (§5.2.1).
- **Efficacité énergétique** (§5.2.2) :
  - SFC-max : 583 066 FPS/W sur la puissance totale ;
  - SFC-max ralenti à 250 kHz (« SFC-smax ») : 15 731 FPS pour 0,2 W de P_chip, plus de 2×
    plus efficace que SFC-fix. Pour les auteurs, mieux vaut paralléliser et baisser
    l'horloge.
- **Efficacité d'usage** (§5.2.3) :
  - taux d'occupation des unités de calcul : ~70 % (CNV), ~80 % (SFC), ~90 % (LFC) ;
  - minimum de 1,83 LUT par opération à P = 64 pour une couche FC 256 × 256 (Fig. 11).
- **Comparaison** (§5.3, Table 4) : débit 48× (SFC-max) et 6× (LFC-max) supérieur à
  Alemdar et al. sur MNIST ; CNV-max 17× / 8× au-dessus de TrueNorth (CIFAR-10 / SVHN),
  9,44× au-dessus d'Ovtcharov et al., 2,2× au-dessus de CaffePresso (Hegde et al.).

→ reportés dans `benchmarks.csv` : **8 lignes** — SFC-max, LFC-max, MFC-max, CNV-max
(CIFAR-10), CNV-max (SVHN), SFC-fix, LFC-fix, CNV-fix (CIFAR-10). Pour CNV-fix, seule la
ligne CIFAR-10 est reportée : le papier ne donne la précision que par topologie, et
l'appliquer à SVHN serait une déduction.

## Limites et critique

- **Petits problèmes** : MNIST, CIFAR-10 et SVHN en 32 × 32. La précision CIFAR-10 (80,1 %)
  est loin de l'état de l'art de l'époque ; le passage à AlexNet ou ImageNet est annoncé
  comme travail futur (§6). Les débits spectaculaires (12 M images/s) concernent un MLP
  sur MNIST.
- **Comparaison biaisée** (Table 4) : elle mélange des précisions de 1 à 32 bits, des
  puissances puce et mur, et des plateformes très différentes (TrueNorth, DSP Keystone-II,
  Parallella). Plusieurs GOPS de l'état de l'art sont des estimations des auteurs (« ∼ »).
  Le débit est comparé à précision souvent inférieure (« within 3 % », §5.3).
- **Puissance** : les auteurs donnent P_chip et P_wall, ce qui est rare et louable. Mais
  P_wall est dominée par les ~7 W de repos de la ZC706 : un FPS/W « carte » n'est pas
  transposable à une carte embarquée plus sobre (déduit).
- **Latence** mesurée par l'hôte sur un lot de 10 000 images en DRAM : ce n'est pas un
  pipeline caméra de bout en bout ; aucun coût d'I/O réel.
- **Pas de baseline GPU mesurée** : seule une estimation roofline K40 (~16 666 images/s
  pour AlexNet binarisé, §3.1). Aucune comparaison Jetson (déduit : il faudrait une mesure
  dans les mêmes conditions).
- **Hypothèse forte** : tous les paramètres en OCM d'un seul FPGA (§6). Cela exclut les
  réseaux profonds de vision (YOLO, AE convolutifs sur images de taille réelle).
- Un bitfile par topologie : pas de reconfiguration à chaud (§4.1).
- Code et bitstream non publiés dans le papier.

## Pertinence pour la thèse

C'est le papier fondateur du toolflow FINN (axe `toolflows`), cité par 6 papiers du corpus.
Il fixe trois idées reprises partout ensuite : l'architecture dataflow « une couche = un
moteur », le folding P × S, et le remplacement batchnorm → seuil. À lire avec FINN-R
(arxiv-1809.04570), qui étend FINN à la quantification multi-bits, et à comparer avec
hls4ml (arxiv-2103.05579, arxiv-2512.01463), qui applique le même principe « une couche =
un bloc ».

Pour la thèse (déduit) :
- le protocole P_chip / P_wall est un modèle à reprendre pour l'expérience de référence
  sur KV260 ;
- un BNN tout on-chip est une piste pour de petits autoencodeurs ou classifieurs
  embarqués ;
- en revanche, FINN seul ne suffit pas pour YOLO à pleine résolution.

## Gaps identifiés

- Détection d'objets (YOLO) en BNN / FINN : non traitée, seulement de la classification
  32 × 32.
- Réseaux qui ne tiennent pas en OCM : non traités, l'accès mémoire externe est reporté
  en travail futur (§6).
- Pas de comparaison mesurée avec un GPU ou un SoC embarqué (Jetson) dans les mêmes
  conditions.
- Métriques de puissance non comparables d'un papier à l'autre : P_chip contre P_wall,
  avec ~7 W de repos. Cela étaye le gap sur l'absence de protocole de mesure commun.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Extraction GROBID correcte dans l'ensemble,
avec quelques défauts :
- colonnes de la Table 3 mal alignées (BRAM de SFC-max et SFC-fix contradictoires avec
  §5.2.3) ;
- légendes des Figures 4 à 6 fusionnées ;
- texte de §5.2.1 déplacé dans les légendes de figures ;
- Figure 9 non lisible.
Déduit et non affirmé par les auteurs :
- la précision des prototypes `fix` est celle de la topologie (même réseau, mêmes poids) ;
- P_wall dominée par le repos de la carte ;
- non-transposabilité à YOLO ;
- existence ultérieure d'un dépôt FINN.
