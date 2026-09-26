---
id: 2019-ding-req-yolo-resource-aware-efficient
fiche: done
date: 2026-09-26
---

# REQ-YOLO: A Resource-Aware, Efficient Quantization Framework for Object Detection on FPGAs

Caiwen Ding, Shuo Wang, Ning Liu, Kaidi Xu, Yanzhi Wang, Yun Liang, 2019, Proceedings of the 2019 ACM/SIGDA International Symposium on Field-Programmable Gate Arrays 33–42. https://doi.org/10.1145/3289602.3293904
Type : conférence (FPGA '19, relue par les pairs)

## Problème

Les systèmes autonomes (drones, robots) exigent une détection d'objets temps réel et sobre
en énergie. Les réseaux binaires (BNN, XNOR-Net) réduisent mémoire et calcul, mais perdent
en précision sur les grands jeux de données et laissent les DSP du FPGA inutilisés (§1).
Les auteurs notent aussi le manque de travaux d'accélération de la **détection** (et non de
la classification) sur FPGA, et l'absence de quantification pensée en fonction des
ressources matérielles (§1).

## Méthode

- Réseau : **Tiny YOLO (YOLOv2-tiny)**, 9 couches conv., entrée 416 × 416 (§2.1).
- **Compression par matrices bloc-circulantes** sur les couches conv. (§3) : seul le vecteur
  index de chaque bloc est stocké ; la multiplication devient FFT → produit élément par
  élément → IFFT (Eq. 4). Six modèles de tailles de bloc différentes ; YOLO-3 (taille de
  bloc 16) retenu (§6.1, Table 1).
- **Quantification hétérogène par ADMM, directement dans le domaine fréquentiel** (§4.1-4.2) :
  par couche, soit quantification à pas constant (multiplications sur DSP, « mode 1 »),
  soit puissances de deux mixtes (primaire + secondaire, décalages sur LUT, « mode 2 »,
  Fig. 4). Choix par couche selon la sensibilité et une marge de perte de précision
  (Fig. 6, Algorithme 1), pour équilibrer DSP et LUT.
- **Tous les poids en BRAM** : pas d'accès DDR pendant l'inférence ; poids chargés depuis
  l'hôte via PCIe (§5, §5.2).
- PE « FFT → MAC → IFFT » à deux modes (Fig. 8) ; pipelines intra- et inter-niveaux (§5.4) ;
  partage des DSP48E1 en tranches 8 bits (§5.5.1) ; stockage de N/2 + 1 coefficients grâce à
  la symétrie hermitienne (§5.5.2).
- Génération de code C/C++ par gabarits puis HLS (Xilinx SDx) (§5.6). NMS en post-traitement
  (§6.1), sans préciser s'il tourne sur l'hôte (probable, déduit).

## Plateforme et implémentation

- Carte Alpha Data **ADM-PCIE-7V3** (Virtex-7 **XC7VX690T**, 6,6 Mo BRAM, 16 Go DDR3),
  PCIe Gen3 × 8, hôte Intel Core i7-4790, **200 MHz**, SDx 2017.4 (§6.3.1, Table 2).
- Ressources : pourcentages donnés en Fig. 11, non extraits → LUT, DSP, BRAM `n/r` ici.
- Taille de modèle YOLO-3 : 5,93 Mb (pas constant) et 4,95 Mb (hétérogène) (Table 1).
- Puissance : 23 W et 21 W (Table 2) ; méthode de mesure non décrite pour le FPGA (pour les
  GPU, « we … measure … power consumption (W) », §6.3.2) → portée `unspecified`.
- Code : lien donné dans le résumé (https://github.com/Anonymous788/heterogeneous_ADMM_YOLO),
  vraisemblablement la partie entraînement / quantification ; bitstream non publié.

## Résultats

| Configuration | FPS | Latence (Σ couches) | Puissance | FPS/W |
|---|---|---|---|---|
| FPGA-YOLO0 (pas constant) | 208,2 (Table 2) | 4,801 ms (Table 1) | 23 W | 9,1 |
| FPGA-YOLO1 (hétérogène) | 314,2 (Table 2) | 3,184 ms (Table 1) | 21 W | 15,0 |
| GTX 1070 (même modèle, auteurs) | 220,8 | n/r | 140 W | 1,6 |
| Jetson TX2 (même modèle, auteurs) | 28,4 | n/r | 10,8 W | 2,6 |

- Précision : perte supplémentaire due à la quantification de 32 à 6 bits de 0,73 % (mAP,
  PASCAL VOC) et 0,2 % (IOU, DataDJI) ; 32 bits flottants → 8 bits fixes : +0,07 % de perte
  seulement (§6.2). Les **mAP absolues** sont en Fig. 10, non extraite → `n/r`.
- Hétérogène vs pas constant : 1,5× en performance, 1,6× en efficacité (§6.3.1).
- ≥ 10× plus rapide que Virtex-YOLO [33] (21 FPS) et Zynq-YOLO [15] (8 FPS) (Table 2).
- FPGA-YOLO1 : 9,4× l'efficacité du GTX 1070 et 5,8× celle du TX2 ; ≥ 7,3× plus rapide que
  le TX2 pour ≤ 2,1× plus de puissance (§6.3.2).
- Couches 0-3 limitées par la communication, 4-8 par le calcul (§6.3.1, Table 1).

→ reportés dans `benchmarks.csv` : **2 lignes** — FPGA-YOLO0 et FPGA-YOLO1, Tiny YOLO
(YOLOv2-tiny) compressé, XC7VX690T, PASCAL VOC, Table 1-2.

## Limites et critique

- **Précision absolue non lisible dans le texte** : seules des pertes relatives sont
  données ; impossible de situer la mAP face aux autres Tiny YOLO.
- **Bit-width implémenté non précisé** dans le texte extrait (6 ou 8 bits ?) ; activations
  non décrites.
- **Latence = somme des latences par couche** (Table 1) : ni transfert PCIe de l'image, ni
  NMS, ni post-traitement ne sont comptés (déduit du tableau).
- **Puissance** : méthode non décrite ; 21-23 W pour une carte PCIe de datacentre, loin de
  l'embarqué visé en introduction (drones). Comparaison à des GPU de bureau (GTX 1070, TDP
  élevé) et à un TX2 non optimisé (pas de TensorRT mentionné : les 28,4 FPS du TX2 sont
  vraisemblablement sous-optimaux, déduit).
- Comparaison FPGA biaisée : Virtex-YOLO et Zynq-YOLO sont des travaux antérieurs sur
  puces plus petites (Zynq 7020) et réseaux non compressés ; la précision n'est pas mise en
  regard.
- Dépend d'une hypothèse forte : modèle compressé tenant entièrement en BRAM (6,6 Mo).
- DataDJI : jeu de données sans point de comparaison.

## Pertinence pour la thèse

Travail de référence de l'axe `yolo-fpga` : l'un des premiers accélérateurs Tiny YOLO avec
co-conception compression / matériel, et une vraie comparaison GPU embarqué (TX2). Deux idées
réutilisables (déduit) : (1) choisir la quantification couche par couche selon la ressource
(DSP vs LUT) et non uniformément ; (2) tout garder on-chip grâce à une compression
structurée. En revanche, la plateforme (Virtex-7 PCIe, 21 W) n'est pas embarquée : il
faudrait vérifier si l'approche tient sur un KV260 (≈ 4,6 Mo de BRAM+URAM, à vérifier).

## Gaps identifiés

- Compression bloc-circulante / FFT pour la détection sur SoC FPGA embarqué (Zynq
  UltraScale+, Kria) : non évaluée ici.
- Coût du post-traitement (NMS) et des transferts hôte non mesuré, comme dans beaucoup de
  papiers YOLO-FPGA.
- Protocole de puissance non décrit : illustre à nouveau l'absence de mesure standard.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Section 6 partiellement désordonnée
(début de §6 et §6.1 mêlés) ; Figures 10 et 11 (précisions absolues, ressources) non
extraites ; bit-width final non trouvé.
Déduit et non affirmé par les auteurs : NMS sur l'hôte ; latence hors transferts et
post-traitement ; TX2 sans TensorRT ; code GitHub limité à l'entraînement ; capacité
mémoire du KV260.
