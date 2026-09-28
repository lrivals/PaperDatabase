---
id: arxiv-2407.02405-tiny-pulp-dronets-squeezing-neural
fiche: done
date: 2026-09-28
---

# Tiny-PULP-Dronets: Squeezing Neural Networks for Faster and Lighter Inference on Multi-Tasking Autonomous Nano-Drones

Lorenzo Lamberti, Vlad Niculescu, Michał Barcis, Lorenzo Bellone, Enrico Natalizio, Luca Benini, Daniele Palossi, 2024, arXiv preprint. https://arxiv.org/abs/2407.02405
Type : preprint non relu par les pairs (papier court, 4 pages ; venue n/r dans le texte).

## Problème

PULP-Dronet (CNN de navigation end-to-end sur nano-drone, GAP8) occupe **320 kB de
poids** et un pic de **400 kB** sur les 512 kB de L2 du GAP8, pour 41 MMAC par image
(§II) : il ne reste pas de place pour d'autres tâches (détection, odométrie…). Les auteurs
veulent réduire drastiquement ce coût pour permettre le **multitâche** à bord d'un
nano-drone.

## Méthode

- Constat : PULP-Dronet **sur-apprend** (BCE de validation qui croît, Fig. 1) et est
  **creux** : jusqu'à 92 % de neurones jamais actifs dans le dernier by-pass (Table I).
- Deux leviers (§II) :
  1. facteur γ ∈ {0,125 ; 0,25 ; 0,5 ; 1} sur le nombre de canaux de toutes les couches ;
  2. **suppression des branches by-pass** (ResNet peu profond : pas de disparition du
     gradient, gradient moyen 0,055 sur la couche la plus atténuée).
- Même entraînement que PULP-Dronet : perte MSE (angle) + β·BCE (collision), hard
  negative mining (§I-II). Jeu de 64 k images d'entraînement et 7 k de validation (§II).
- Déploiement en **virgule fixe** sur GAP8 (§II) ; nombre de bits et outil de déploiement
  n/r dans le texte.

## Plateforme et implémentation

- **GAP8** (GreenWaves, 1 Fabric Controller + cluster 8 cœurs, 512 kB L2) ; deux points de
  fonctionnement : efficace (FC 50 MHz, CL 100 MHz, 1,0 V) et performance max (FC 250 MHz,
  CL 175 MHz, 1,2 V) (§III-B).
- **Puissance mesurée sur les rails du SoC** (FC et cluster séparément) avec un RocketLogger
  à 64 ksps (§III-B, Fig. 3) → portée `chip`. Consommation du drone entier n/r.
- Entrée 200×200×1 (§III-B). Code / modèles : non mentionnés dans le texte (n/r).
- Le drone porteur (27 g, d'après la description de PULP-Dronet, §I) n'est pas utilisé en
  vol dans ce papier.

## Résultats

| Modèle | Taille | MAC | Pic mémoire (dyn.) | Latence EE / max | FPS EE / max | Source |
|---|---|---|---|---|---|---|
| PULP-Dronet (γ=1) | 320 kB | 41 M | 400 kB | 96 / 52 ms | 10 / 19 | §II, §III-B |
| Tiny-PULP-Dronet (γ=0,125, sans by-pass) | **6,4 kB** | **1,5 M** | 80,1 kB | **11,3 / 6,3 ms** | **89 / 160** | §III-A, §III-B |

- Réduction ×50 en taille, ×27 en MAC, mais seulement **×8,5 en latence** : la première
  convolution 5×5 (1 MMAC, 70 % des opérations) prend ~75 % du temps ; layout HWC à 4
  canaux de sortie et marshaling (45 % du temps de la couche) (§III-B).
- Énergie : **34 mW, 0,38 mJ / image** en mode efficace ; 0,63 mJ / image en mode max
  (§III-B).
- Qualité : RMSE (angle) similaire ou meilleure jusqu'à γ = 0,25 ; accuracy de collision
  ~0,91 avec by-pass, **0,88** pour le plus petit modèle sans by-pass ; dégradation max
  « 6 % » (§III-A, §IV, Fig. 2). Valeurs par γ uniquement en figure (n/r).
- BCE de validation minimale 0,052 (tiny) vs 0,064 (baseline) ; MSE 0,01 pour les deux
  (§II).

→ reportés dans `benchmarks.csv` : 4 lignes (Tiny-PULP-Dronet et PULP-Dronet, chacun aux
deux points de fonctionnement du GAP8), `confidence: medium` (texte). Puissance `chip`
uniquement pour le mode efficace (voir incohérence ci-dessous).

## Limites et critique

- **Pas de vol** : l'abstract annonce « similar flight performance as PULP-Dronet », mais
  le texte ne rapporte **aucun essai en vol** ; seules RMSE / accuracy hors ligne sont
  données.
- **Incohérence de puissance** : en mode max, « same average power » (34 mW) est
  incompatible avec 0,63 mJ en 6,3 ms (≈ 100 mW, déduit). Puissance max laissée en n/r.
- **Multitâche non démontré** : c'est la motivation, mais aucune seconde tâche n'est
  exécutée en parallèle.
- Accuracy 0,88 vs ~0,91 : une baisse de 3 points sur la détection de collision n'est pas
  anodine pour la sécurité ; la « dégradation max 6 % » n'est pas détaillée.
- Puissance mesurée au SoC seulement : la caméra, la radio et surtout les moteurs du
  nano-drone dominent le budget (déduit ; non chiffré ici).
- Papier court, sans comparaison à d'autres réseaux compacts (MobileNet, NAS) ni à d'autres
  MCU (GAP9, STM32).

## Pertinence pour la thèse

- Axe `nano-drone` : point de référence **gamme mW** (34 mW SoC, 0,38 mJ / inférence,
  jusqu'à 160 FPS sur GAP8) à mettre en regard de la gamme W des FPGA (≈ 10 W pour
  2025-elhence) — trois ordres de grandeur d'écart pour une tâche beaucoup plus simple
  (navigation 200×200 en niveaux de gris vs détection 640×640).
- Méthode transposable à la détection : **analyse de sparsité d'activation** pour choisir
  la largeur, et suppression des branches parallèles pour réduire le pic mémoire (utile
  aussi sur FPGA dataflow où chaque branche coûte des buffers).
- Montre que le goulot devient la **première couche** et le layout mémoire, pas les MAC :
  argument à reprendre pour tout accélérateur embarqué.

## Gaps identifiés

- Multitâche réel (navigation + détection) sur GAP8 avec budget mémoire et latence mesurés.
- Validation en vol de modèles « squeezed » et mesure de l'effet sur la vitesse de vol sûre
  (lien avec le modèle F-1, 2020-krishnan).
- Puissance système (drone entier) plutôt que SoC.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). Le début de §II
(description de PULP-Dronet) est extrait en fin d'introduction, et la phrase sur la plage de
γ est coupée par le paragraphe « Sparsity ». Les valeurs par γ (Fig. 2) ne sont connues
que qualitativement.

Ce qui suit est déduit et non affirmé par les auteurs :
- la puissance ≈ 100 mW en mode max (calcul énergie / latence) ;
- l'absence de vol (constat sur le texte extrait) ;
- la domination du budget par les moteurs ;
- la comparaison de gamme de puissance avec 2025-elhence.
