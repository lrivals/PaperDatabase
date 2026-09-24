---
id: 2023-shuvo-efficient-acceleration-deep-learning-inference
fiche: done
date: 2026-09-24
---

# Efficient Acceleration of Deep Learning Inference on Resource-Constrained Edge Devices: A Review

Md. Maruf Hossain Shuvo, Syed Kamrul Islam, Jianlin Cheng, Bashir I. Morshed, 2023, Proceedings of the IEEE 111(1), 42-91. https://doi.org/10.1109/JPROC.2022.3226481
Type : article de journal (revue ; l'export IEEE date le volume de 2023, OpenAlex indiquait
2022)

## Problème

Selon les auteurs, aucune revue ne couvre toute la chaîne de l'inférence de réseaux
profonds sur équipement edge : conception du modèle, compression, co-design, outils
logiciels, plateformes matérielles, métriques, défis (§II). L'entraînement est hors champ,
supposé fait ailleurs.

## Méthode

Revue, sans expérience propre. Elle couvre :
- l'IA edge (cache, entraînement, inférence, déport de calcul, §III) ;
- le ML classique sur edge (§IV) ;
- la conception de modèles (NAS, convolutions compactes, RNN optimisés, §VI) ;
- la compression (pruning, quantification, partage de poids, optimisation des MAC, calcul
  approximatif ou stochastique, KD, techniques adaptatives et early exit, §VII) ;
- la parcimonie dans les accélérateurs (§VIII) ;
- **les métriques (§IX)** ;
- les outils : OpenVINO, MATLAB DL HDL Toolbox, X-CUBE-AI, DNNDK, TensorRT, CDNN, Qualcomm
  NPS, Stratus HLS (§X) ;
- les plateformes : CPU / GPU, SoC / ASIC, FPGA et CGRA, VPU, MCU, mémoire émergente
  (§XI) ;
- l'edge distribué (§XII), des cas d'usage (§XIII), et **12 défis (§XIV)**.

## Plateforme et implémentation

Pas d'implémentation propre. Côté FPGA (§XI-C1), une seule sous-section, qui cite :
- VGG-16 8 bits sur Zynq-7020 à 84 GOPS [315] ;
- Lite-CNN INT8 sur XC7Z020 à 408 GOPS crête et 33 GOPS/W.
Le tableau des FPGA (Table 8) et les tableaux comparatifs (Tables 6 à 10) sont perdus à
l'extraction.

## Résultats

Chiffres repris des travaux cités, sans vérification :
- **Coût énergétique des opérations (§VII-B, d'après [118]) :**
  - une addition INT8 coûte 30 fois moins d'énergie et 116 fois moins de surface qu'une
    addition FP32 ;
  - une multiplication 8 bits en virgule fixe coûte 18,5 fois moins d'énergie et 27,4 fois
    moins de surface qu'en FP32.
- **Accélérateurs cités (§XI-B, §XI-C2) :**
  - Eyeriss : 166 GOPS/W pour 278 mW sur AlexNet ;
  - Thinker : 590 GOPS/W pour 335 mW ;
  - SNAP : 21,55 TOPS/W, ResNet-50 élagué à 348 mW.
- **Jetson TX2 :** environ 15 W en inférence (§XI-A).

→ reportés dans `benchmarks.csv` : aucune ligne. C'est une revue, et ses tableaux
comparatifs sont perdus à l'extraction.

## Limites et critique

- **Largeur plutôt que profondeur :** l'ensemble du pipeline est couvert, mais chaque
  plateforme en quelques paragraphes. Le FPGA occupe une sous-section, sans analyse des
  toolflows (FINN-R n'est cité qu'en passant, §XIV-B ; hls4ml est absent du texte extrait).
- **Aucune comparaison chiffrée homogène entre plateformes** dans le texte. Les chiffres
  sont juxtaposés, avec des métriques différentes (GOPS, GOPS/W, TOPS/W, FPS) et des
  nœuds technologiques différents (ASIC en 16 à 65 nm contre FPGA).
- La **Table 6** (comparaison des plateformes par métrique) est justement celle qui
  aurait servi, et elle n'est pas lisible dans l'extraction.
- **Revue de 2022-2023 :** pas de Jetson Orin, de Kria ni de MCU à NPU récents.

## Pertinence pour la thèse

- **§IX-I « Test Setup » (lu) :** « un processeur peut annoncer une très faible
  consommation sans compter les accès à la mémoire externe » ; il faut distinguer
  résultats **simulés** et **mesurés**. C'est une citation de revue relue (Proc. IEEE) qui
  appuie directement la colonne `power_scope` et le gap « puissance puce contre carte ».
- **§XIV-C « Developing Benchmarks » (lu) :** manque de standards d'évaluation
  universels ; la plupart des évaluations se font sur AlexNet et VGG16 avec ImageNet.
  C'est un appui publié au gap « protocole de mesure ».
- **§XIV-B :** l'outillage de portage automatique vers FPGA et CGRA est jugé « moins
  efficace ». C'est un appui au gap toolflows.
- **§XIV-J :** l'apprentissage « lifelong » n'est « pas conçu pour les équipements edge ».
  C'est un appui à l'axe `continual-learning`.
- **Carte de référence** des outils de déploiement (§X), utile pour la partie état de
  l'art.

## Gaps identifiés

- **FPGA absents des surveys « embarqué » :** nuance. Le FPGA est présent, mais
  marginal (une sous-section), et comparé seulement de manière qualitative. C'est le même
  constat que arxiv-2411.01431 et 2024-mittal.
- **Puissance et protocole :** fournit une source publiée pour les deux gaps (§IX-I,
  §XIV-C).
- **Apprentissage continu embarqué :** identifié par les auteurs comme ouvert (§XIV-J).

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). Les Tables 1 à 10 sont
absentes de l'extraction, à part leurs légendes.

Ce qui suit est déduit et non affirmé par les auteurs :
- le lien entre §IX-I et `power_scope` ;
- l'absence de hls4ml (constatée seulement dans le texte extrait) ;
- le caractère daté des plateformes couvertes.
