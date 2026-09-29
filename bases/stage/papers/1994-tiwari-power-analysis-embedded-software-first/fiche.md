---
id: 1994-tiwari-power-analysis-embedded-software-first
fiche: done
date: 2026-09-29
benchmarks: none
---

# Power analysis of embedded software: a first step towards software power minimization

V. Tiwari, S. Malik, A. Wolfe, 1994, IEEE Transactions on Very Large Scale Integration (VLSI) Systems 2(4), 437-445. https://doi.org/10.1109/92.335012
Type : article de journal

## Problème

Les outils d'analyse de puissance n'existent qu'aux niveaux circuit et porte, inutilisables pour
estimer la consommation d'un **logiciel** sur un processeur du commerce dont on n'a pas le
layout. Il manque une méthode pour attribuer un coût énergétique à un programme (Abstract, §I).

## Méthode

**Modèle énergétique au niveau instruction**, construit par mesure (§II-III) :

- Mesure du courant moyen de la CPU (ampèremètre intégrateur, fenêtre de 100 ms) pendant qu'une
  boucle répète une instruction ou une courte séquence ; E = I × V_CC × N × τ (§II-A, §II-B).
- **Coût de base** par instruction : courant de la boucle × nombre de cycles ; boucles de 120
  instances, assez longues pour amortir le branchement, assez courtes pour éviter les défauts de
  cache (§III-A).
- **Effets inter-instructions** ajoutés : état du circuit entre deux instructions différentes
  (5 à 30 mA, ≈ 15 mA en moyenne, ajouté forfaitairement), stalls de pipeline (≈ 250 mA par cycle
  de stall de prefetch), défauts de cache (≈ 216 mA par cycle de pénalité) (§III-B).
- **Estimation d'un programme** : découpage en blocs de base, somme des coûts de base pondérée par
  le nombre d'exécutions (profileur), + surcoût d'état, + stalls, + pénalité de cache (simulateur)
  (§IV, Fig. 2).
- Modèle de la mémoire DRAM (courant de repos 77 ou 5,3 mA selon le mode page ; accès en page
  hit ou miss) (§V).

## Plateforme et implémentation

- **Intel 486DX2-S** à 40 MHz, 3,3 V, sur carte d'évaluation mobile avec 4 Mo de DRAM ; courant
  CPU et DRAM mesurés séparément du reste de la carte (portée « puce + DRAM ») (§II-B).
- Validation aussi sur **Fujitsu SPARClite 934** (RISC), détaillée dans une autre publication [9]
  (§VII).
- Outillage : ampèremètre numérique, analyseur logique pour le temps d'exécution. Code : sans
  objet.

## Résultats

- Variation du coût de base avec les opérandes : ≤ 14 mA (< 5 %) ; avec l'adresse mémoire :
  ≈ 3,5 % (§III-A, Table II).
- Instructions sur registres ≈ 300 mA ; lectures mémoire en cache ≥ 430 mA ; écritures ≥ 530 mA
  (§VI-B).
- Estimation vs mesure : 384,0 mA estimés contre 385,0 mA mesurés sur l'exemple (§IV, Table IV) ;
  **écart < 3 %** pour les programmes sans stall ni défaut de cache (§IV).
- Réordonner les instructions ne change le courant que de ≤ 2 % sur le 486DX2 (§VI-A).
- Réécriture guidée par le modèle (allocation de registres, suppression d'accès mémoire) :
  **−40,6 % d'énergie** sur un tri par tas (sort) et ≈ −33 % sur « circle » (§VI-B, Table V).

→ aucune ligne dans `benchmarks.csv` : référence de méthode (mesure et modèle d'énergie
logicielle), sans modèle d'apprentissage ni tâche d'IA (`benchmarks: none`).

## Limites et critique

- Processeurs de 1994 (CISC à cache, 40 MHz) : les valeurs absolues ne se transposent pas à un
  Cortex-M ; seule la méthode est réutilisable.
- Mesure par ampèremètre moyenné, sans intervalle de confiance rigoureux (± 1 mA observé, §III-A).
- Les effets de stall et de cache sont difficiles à prévoir statiquement, principale source
  d'erreur reconnue (§IV).
- Détails du SPARClite renvoyés à une autre publication.

## Pertinence pour la thèse

Référence de méthode pour mesurer l'énergie d'un logiciel embarqué : le principe « coût par
instruction ou par noyau × nombre d'exécutions » et la mesure du courant sur une boucle répétée
s'appliquent directement à l'estimation du coût d'une mise à jour EWC sur MCU (coût d'un pas de
gradient, du calcul de la Fisher, de la pénalité). Il justifie aussi que les accès mémoire
dominent le coût énergétique, argument pour garder poids et Fisher en SRAM et en INT8 (déduit).

## Gaps identifiés

- Modèle d'énergie au niveau noyau (conv, dense, rétropropagation) pour l'apprentissage sur
  Cortex-M : à construire selon cette méthode.
- Coût énergétique relatif des accès mémoire vs calcul pour l'entraînement INT8 sur MCU.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Tables I-III partiellement illisibles (OCR de
l'éditeur) ; numéros de sections mal détectés ; figure 1 extraite en fragments.
Déduit et non affirmé par les auteurs : transposition à un Cortex-M et à l'apprentissage continu.
