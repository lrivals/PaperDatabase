---
id: 2008-saxena-damage-propagation-modeling-aircraft-engine
fiche: done
date: 2026-09-29
benchmarks: none
---

# Damage Propagation Modeling for Aircraft Engine Run-to-Failure Simulation

Abhinav Saxena, Kai Goebel, Don Simon, Neil Eklund, 2008, International Conference on Prognostics and Health Management (PHM). https://doi.org/10.1109/PHM.2008.4711414
Type : conférence (PHM 2008) — article de jeu de données

## Problème

Le pronostic guidé par les données manque de données run-to-failure publiques : les données réelles
contiennent rarement l'évolution d'un défaut jusqu'à la panne, et les flottes instrumentées ne sont
pas publiées. Sans jeu commun, les approches ne sont pas comparables (§I). Les auteurs génèrent par
simulation les données du premier challenge PHM (PHM'08).

## Méthode

Ce que l'article **définit** :

- **Pronostic** : estimation de la durée de vie restante (RUL), en cycles ; la fin de vie dépend de
  seuils opérationnels (§II).
- **Simulateur C-MAPSS** (Commercial Modular Aero-Propulsion System Simulation, MATLAB/Simulink) :
  turboréacteur double flux de 90 000 lb de poussée, en boucle fermée avec son contrôleur ; 14 entrées
  (débit carburant + 13 modificateurs de santé de fan, LPC, HPC, HPT, LPT) ; 21 des 58 sorties
  retenues (§III-A, Tables 1-2).
- **Modèle de dégradation** : indice de santé h(t) = 1 − d − exp(a·t^b) sur le rendement et le débit
  du module dégradé (Eq. 4-6), avec usure initiale d ∈ [0 ; 1 %], a ∈ [0,001 ; 0,003], b ∈ [1,4 ; 1,6]
  (Eq. 9-10) ; seule la dégradation du **HPC** est simulée pour le challenge (§V-C).
- **Indice de santé global** H(t) = minimum des marges opérationnelles normalisées (stall fan, LPC,
  HPC et marge EGT) ; **panne quand H = 0** ; limites : 15 % de marge au décrochage et ≈ 2 % pour
  l'EGT (Eq. 7-8, §V-D).
- **Bruit** : usure initiale aléatoire, bruit de processus (mélange de deux gaussiennes, qui inclut la
  maintenance entre vols et rend la dégradation non monotone localement), bruit de mesure (§V-B,
  Fig. 5).
- **Scénario** : flotte de moteurs, un instantané par vol, **6 conditions de vol** (altitude 0-42 kft,
  Mach 0-0,84, TRA 20-100) (§V-D, §VI).
- **Découpage** : apprentissage jusqu'à la panne ; test et validation tronqués avant la panne ; RUL
  de 10 à 150 cycles en test et de 6 à 190 en validation (élargissement non annoncé aux
  participants) (§VI).
- **Score asymétrique** qui pénalise exponentiellement les prédictions tardives plus que les
  précoces ; les auteurs suggèrent en plus de pondérer les RUL courtes et d'ajouter une mesure de
  corrélation entre unités (§VII, Fig. 9-11).

## Plateforme et implémentation

Simulation C-MAPSS en MATLAB/Simulink, mode batch (§III). Données publiées pour le challenge PHM'08
(dépôt de données de pronostic de la NASA, cité en [1]).

## Résultats

Pas de résultat de méthode : l'article décrit le générateur et les données. Aucune ligne dans
`benchmarks.csv`, conformément au profil de la base pour les papiers de jeux de données
(`benchmarks: none`).

## Limites et critique

- Données **simulées** : dégradation exponentielle imposée et bruit gaussien supposé, faute de
  données réelles pour calibrer le bruit (§V-B).
- Un seul module dégradé (HPC) dans les données du challenge ; les sous-jeux FD001-FD004 utilisés
  ensuite dans la littérature (1 ou 6 conditions, 1 ou 2 modes de défaut, par exemple chez Shah 2025)
  ne sont pas décrits dans cet article (déduit).
- Coefficients du score : la légende de la Fig. 9 donne a₁ = 10 et a₂ = 13, alors que la littérature
  ultérieure (par exemple Shah 2025) applique 13 aux prédictions précoces et 10 aux tardives ; la
  formule (Eq. 11) est illisible à l'extraction : convention à vérifier dans le PDF.
- L'étiquette RUL linéaire jusqu'à zéro ne correspond pas à la réalité d'une dégradation qui ne
  commence qu'après une phase saine ; d'où la RUL plafonnée (125 ou 130 cycles) adoptée plus tard
  (déduit).

## Pertinence pour la thèse

Article de référence du jeu **C-MAPSS**, utilisé par les travaux de CL pour la RUL de la base
(Maschler, Shah) et cité par Hurtado 2023 comme l'un des deux seuls jeux PdM valables comme
benchmark. Il fixe ce qu'il faut citer pour décrire les données (C-MAPSS, 21 capteurs, 6 conditions
de vol, panne quand l'indice de santé atteint zéro, score asymétrique). Les changements de
conditions opératoires entre sous-jeux sont la source de « tâches » naturelle pour un scénario
d'apprentissage continu sur la RUL (déduit).

## Gaps identifiés

- Données réelles run-to-failure publiques toujours rares (§I).
- Pas de protocole CL standard sur C-MAPSS (ordre des sous-jeux, métriques d'oubli).

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Équations 1-11 en partie illisibles à l'extraction ;
Table 1 sans corps propre (liste des entrées en texte continu), Table 2 partielle ; figures non
disponibles.
Déduit et non affirmé par les auteurs : lien avec les sous-jeux FD001-FD004, plafonnement de la RUL,
usage comme tâches de CL.
