---
id: arxiv-2209.06918-nanoflownet-real-time-dense-optical
fiche: done
date: 2026-09-28
---

# NanoFlowNet: Real-time Dense Optical Flow on a Nano Quadcopter

Rik J Bouwmeester, Federico Paredes-Vallés, Guido C H E De Croon, 2022, arXiv preprint. https://arxiv.org/abs/2209.06918
Type : preprint non relu par les pairs (version arXiv ; une publication en conférence
n'est pas mentionnée dans le texte extrait, à vérifier)

## Problème

Les nano-quadricoptères (~30 g, ~10 cm) ont trop peu de charge utile et de calcul pour les
méthodes de navigation par vision classiques (cartes, stéréo, LiDAR) (§I). Le flot
optique est un indice monoculaire clé pour l'évitement d'obstacles, mais les réseaux de
flot optique, même « rapides », tournent à quelques dizaines de FPS sur GPU de bureau avec
des millions de paramètres, incompatibles avec l'embarqué (§I). Les auteurs visent le
**premier flot optique dense (par pixel) temps réel** sur un microprocesseur ultra-basse
consommation (§I, §II-A).

## Méthode

- Architecture dérivée de **STDC-Seg** (segmentation temps réel) : toutes les
  convolutions en **depthwise separable**, filtres ÷ 4 ; variante **NanoFlowNet-s** à
  filtres ÷ 2 supplémentaires (§III). Encodeur + module de fusion multi-niveaux + **tête
  de détail utilisée seulement à l'entraînement** (Fig. 1).
- **Guidage par frontières de mouvement** : la tête de détail apprend les motion
  boundaries du jeu (Focal Loss) au lieu des bords par Laplacien de STDC-Seg ; coût nul à
  l'inférence (§III-A).
- **Module STDC stridé réorganisé** : la convolution pointwise coûteuse déplacée après
  l'average pooling ; −50 % de MAC en stage 1, −10 % en stages 2-3 (§III-B, Fig. 2-3).
- **Entrée réduite** : ~qqVGA (160×120), niveaux de gris (−2/3 de mémoire d'entrée ; −14 %
  de L2 sur l'AI-deck), première convolution supprimée (§III-C, §IV-D2).
- Entraînement : FlyingChairs2 (300 époques) puis FlyingThings3D (200 époques) ; baseline
  FlowNet2-s réentraînée et réduite (**FlowNet2-xs**) sur les mêmes données (§IV-A).
- Déploiement : **GAPflow** (NNTool + AutoTiler), **quantification post-entraînement 8
  bits**, SQNR moyen 10 sur MPI Sintel (§IV-D2).
- Application : évitement d'obstacles par **équilibre du flot gauche / droite** (taux de
  lacet ∝ différence des sommes de flot) + **oscillations verticales actives** pour
  générer du flot ; le CNN et le calcul de l'erreur tournent sur le GAP8, la commande sur
  le Crazyflie (§IV-D1).

## Plateforme et implémentation

- **GreenWaves GAP8** sur **Bitcraze AI-deck** (FC 250 MHz, cluster 8 cœurs 230 MHz,
  VDD 1,2 V), caméra monochrome HM01B0 en fenêtre + binning, recadrage 112×160 ; porteur
  **Crazyflie 2.x** + flow-deck, **34 g** au total (§IV-D, Fig. 6). Gamme nano (mW,
  déduit : la puissance n'est pas mesurée dans le papier).
- Latence GPU : NVIDIA GTX 1070 Max-Q (portable), TensorFlow 2.8 + TensorRT 7.2.2,
  batch 1 (§IV-A).
- Puissance / énergie : **n/r**. Mémoire (L1/L2) utilisée : n/r en valeur absolue.
- Code : non mentionné dans le texte extrait (n/r).

## Résultats

- Débit sur GAP8 : **5,5 à 9,3 FPS** selon la variante (§I) ; NanoFlowNet niveaux de gris
  **5,57 FPS**, couleur 5,18 FPS (112×160, thread vision inclus) (Table IV). FlowNet2-xs
  ne tient pas en mémoire sur le GAP8 ; ses 3 premières/dernières couches seules
  tournent à 4,96 FPS (§IV-B).
- GPU portable : **141 FPS** (96×224), niveaux de gris comme couleur (Table IV).
- Précision (MPI Sintel train, EPE en px, plus bas = mieux, à la résolution native) :
  NanoFlowNet niveaux de gris **7,122 (clean) / 7,979 (final)** ; couleur 7,726 / 8,344
  (Table IV) ; meilleur que FlowNet2-xs avec < 10 % de ses paramètres, NanoFlowNet-s moins
  bon, 27 % des paramètres de NanoFlowNet (§IV-B, Table I non extraite).
- Ablation guidage (Table II) : aucun 7,636 / 8,119 ; Laplacien 7,404 / 8,141 ; frontières
  de mouvement 7,122 / 7,979. Module STDC réorganisé plus rapide et plus précis (Table III
  non extraite).
- Vol : environnement ouvert, batterie vidée **sans collision** ; environnement encombré,
  résultats variables (évite un obstacle pour foncer dans le suivant), trajectoires en
  spirale (§IV-D4, Fig. 8). Aucune métrique chiffrée (taux de succès, distance, vitesse).

→ reportés dans `benchmarks.csv` : 4 lignes : GAP8 INT8 niveaux de gris (5,57 FPS) et
couleur (5,18 FPS), précision n/r (EPE non mesurée après quantification) ; GTX 1070 Max-Q
niveaux de gris (EPE 7,122, 141 FPS) et couleur (EPE 7,726, 141 FPS). `confidence:
medium` : le corps de la Table IV est extrait sous la légende de la Table III.

## Limites et critique

- **« Real-time » à 5,6 FPS** : suffisant pour l'évitement lent démontré, pas pour du vol
  agile ; le seuil n'est pas justifié par une dynamique de vol (déduit).
- **Pas de mesure de puissance ni d'énergie** sur le GAP8, alors que « ultra-low power »
  est l'argument ; la consommation de l'AI-deck face au budget des moteurs n'est pas
  discutée.
- **EPE après quantification INT8 non rapportée** : seul le SQNR (10) est donné ; les EPE
  sont celles du modèle GPU.
- **Baseline unique et affaiblie** : FlowNet2-xs, version réduite par les auteurs de
  FlowNet2-s ; pas de comparaison à un flot optique classique (Lucas-Kanade, capteur
  PMW3901 du flow-deck) sur GAP8 ou STM32 (déduit).
- **Évaluation en vol qualitative** : quelques trajectoires OptiTrack, aucun taux de
  collision ni nombre d'essais.
- EPE à résolution native pour comparer à la littérature, alors que le réseau travaille à
  basse résolution : les auteurs le disent (§III-C), mais la comparaison aux travaux
  publiés reste impossible (§IV-A).

## Pertinence pour la thèse

- **Axe `nano-drone`** : exemple de référence d'un **CNN dense (sortie par pixel) sur
  GAP8** en vol, avec chaîne complète GAPflow + PTQ 8 bits et contraintes mémoire L2
  explicites. Point de comparaison pour tout détecteur sur GAP8 (gamme mW).
- **Axe `tracking-navigation`** : flot optique comme représentation intermédiaire pour
  la navigation, plutôt que l'end-to-end (PULP-DroNet) (§II-A).
- Les techniques de réduction (depthwise, entrée niveaux de gris, tête de détail
  seulement à l'entraînement) sont transposables à un détecteur léger (déduit).
- Hors détection : pas d'apport direct à `drone-detection` ni `drone-fpga`.

## Gaps identifiés

- **Énergie par inférence sur GAP8 non mesurée** : manque récurrent des papiers
  nano-drone quand l'argument est la basse consommation.
- **Effet de la quantification INT8 sur la précision dense** : non mesuré (SQNR seul) ;
  même manque que pour mAP_small sur les détecteurs.
- **Métriques système absentes** : ni vitesse de vol sûre, ni taux de collision, ni
  autonomie, malgré un vol réel (hypothèse « métriques système » de gaps.md).

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). **Tables I à IV mal
extraites** : le corps affiché sous « TABLE I » est celui de la Table II (guidage) et le
corps sous « TABLE III » est celui de la Table IV (couleur / niveaux de gris) ; **les corps
des Tables I (résultats principaux, paramètres, FlowNet2-xs, NanoFlowNet-s) et III (module
STDC) sont absents**. L'équation (1) de la stratégie de contrôle est perdue.

Ce qui suit est déduit et non affirmé par les auteurs :
- la réaffectation des corps de tableaux (fondée sur les en-têtes de colonnes) ;
- la gamme de puissance mW de l'AI-deck ;
- l'insuffisance de 5,6 FPS pour un vol agile ;
- la transposabilité des techniques à un détecteur.
