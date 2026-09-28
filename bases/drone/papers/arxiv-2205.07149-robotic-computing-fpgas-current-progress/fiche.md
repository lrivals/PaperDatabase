---
id: arxiv-2205.07149-robotic-computing-fpgas-current-progress
fiche: done
date: 2026-09-28
---

# Robotic Computing on FPGAs: Current Progress, Research Challenges, and Opportunities

Zishen Wan, Ashwin Lele, Bo Yu, Shaoshan Liu, Yu Wang, Vijay Janapa Reddi, Cong Hao, Arijit Raychowdhury, 2022, arXiv preprint. https://arxiv.org/abs/2205.07149
Type : preprint non relu par les pairs (article de position / mini-survey de 4-5 pages ;
une version en conférence n'est pas mentionnée dans le texte extrait, à vérifier)

## Problème

Les robots (drones, voitures autonomes, robots logistiques) exigent un calcul temps réel
sous contraintes SWaP, sûr et adaptable (Abstract, §I). CPU trop lents (planification de
trajectoire en quelques secondes), GPU en centaines de ms pour des centaines de watts
(§I, [3], [4]), ASIC figés et vulnérables. Les auteurs défendent le **FPGA comme substrat
de calcul robotique** et dressent un état des lieux et une feuille de route (§I).

## Méthode

Article de position, sans expérience propre. Structure :
- **Pile robotique transverse** (§II, Fig. 1-2) : algorithmes (perception, localisation,
  planification et contrôle, apprentissage end-to-end) et couche système (ROS, graphe de
  calcul).
- **Travaux FPGA existants, surtout ceux des auteurs** (§III) : perception (ORB sur FPGA
  pour robots aériens et terrestres [20], [21] ; stéréo locale, globale par graph cut
  [23], semi-globale FP-Stereo [24], iELAS [25] ; CNN renvoyés à un autre survey [26]) ;
  localisation (bundle adjustment π-BA [27], Pisces [28], générateur Archytas [29],
  Eudoxus [21] qui unifie SLAM / Registration / VIO) ; planification (détection de
  collision, 16 µs [31] puis 2,3 µs [32] par requête) ; multi-robots (INCAME [33]) ;
  ROS sur FPGA [34]-[36].
- **Huit défis** (§IV) : reconfiguration partielle à l'exécution, bibliothèques de noyaux
  modulaires, SoC hétérogènes (OpenCL), intégration ROS, **benchmarking** des noyaux
  robotiques, flot de conception automatisé, RISC-V open source, **hardware-in-the-loop**
  et co-simulation boucle fermée (FireSim + AirSim).

## Plateforme et implémentation

Aucune implémentation propre. Aucun FPGA précis, ressource, fréquence ou puissance cités
pour les travaux recensés (n/r). Pas de code.

## Résultats

Chiffres cités (repris des travaux originaux, non vérifiés) :

| Élément | Chiffre | Source |
|---|---|---|
| Part de l'ORB dans la latence de localisation | 50-80 % | §III |
| Graph cut 3D parallèle (stéréo globale) | 166× vs CPU | §III, [23] |
| RRT sur CPU : part de la détection de collision | 99 % des instructions, 90 % du temps | §III |
| Requête de planification sur FPGA | 16 µs [31] ; 2,3 µs [32] | §III |
| Planification CPU / GPU | quelques s ; centaines de ms à centaines de W | §I, [3], [4] |

→ reportés dans `benchmarks.csv` : aucune ligne. C'est un survey / article de position :
les travaux cités sont à ficher à la source.

## Limites et critique

- **Plaidoyer pro-FPGA sans comparaison chiffrée** : aucune donnée de puissance, de
  ressources ni de latence face à une Jetson ou à un MCU ; le « hundreds of watts » des
  GPU vise des GPU de bureau, pas la gamme Jetson (~10 W) pertinente pour un drone
  (déduit).
- **Auto-référentiel** : la section III recense surtout les travaux des auteurs (Eudoxus,
  Archytas, π-BA, iELAS…) ; pas de méthode de sélection.
- **Très court** : aucun tableau comparatif, aucun critère de classement ; les CNN de
  perception sont renvoyés à un autre survey [26].
- **Détection d'objets quasi absente** : citée comme bloc fonctionnel (Fig. 2) mais
  aucun accélérateur de détection recensé.
- Sûreté et fiabilité revendiquées comme avantage du FPGA (reconfiguration pour
  « patcher ») sans aborder les soft errors de la configuration SRAM (déduit).

## Pertinence pour la thèse

- **Axe `system-codesign`** : les défis 5 (benchmarking des noyaux robotiques) et 8
  (**hardware-in-the-loop**, co-simulation FPGA + AirSim) formulent exactement le manque
  de métriques système des papiers YOLO / FPGA (hypothèse de gaps.md) ; citation utile
  pour motiver une évaluation en boucle fermée.
- **Axe `drone-fpga`** : cadre général pour placer un détecteur FPGA dans un SoC
  hétérogène (CPU + FPGA + accélérateurs) à bord, avec la reconfiguration partielle comme
  levier (partage temporel entre détection, SLAM et planification).
- **Axe `tracking-navigation`** : porte d'entrée vers les accélérateurs FPGA de
  localisation / planification (Eudoxus, Archytas) si la thèse élargit au-delà de la
  détection.
- Co-auteurs à noter pour `labs.md` : V. J. Reddi (Harvard), C. Hao et A. Raychowdhury
  (Georgia Tech), S. Liu, Y. Wang (Tsinghua) — hors France.

## Gaps identifiés

- **Aucune comparaison quantitative FPGA / Jetson / MCU** pour les noyaux robotiques d'un
  drone, même dans un survey dédié.
- **Partage d'un FPGA entre détection et navigation** (reconfiguration partielle,
  ordonnancement) : proposé comme perspective, pas évalué.
- **Hardware-in-the-loop avec FPGA pour drone** : annoncé nécessaire (§IV-8), aucun
  travail recensé ne le fait.
- **Fiabilité** : l'argument sûreté du FPGA n'est pas confronté aux erreurs de
  configuration (axe `reliability`).

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`, texte court). Fig. 1
et 2 connues par leurs légendes et un fragment du tableau de blocs fonctionnels.

Ce qui suit est déduit et non affirmé par les auteurs :
- le caractère auto-référentiel de la section III ;
- la cible GPU de bureau du chiffre « hundreds of watts » ;
- la limite fiabilité (soft errors de configuration) ;
- l'usage de la reconfiguration partielle pour partager le FPGA à bord d'un drone.
