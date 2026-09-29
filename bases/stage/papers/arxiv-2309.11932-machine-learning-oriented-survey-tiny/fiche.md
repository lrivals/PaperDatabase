---
id: arxiv-2309.11932-machine-learning-oriented-survey-tiny
fiche: done
date: 2026-09-29
---

# A Machine Learning-Oriented Survey on Tiny Machine Learning

Luigi Capogrosso, Federico Cunico, Dong Seon Cheng, Federico Fummi, Marco Cristani, 2023, IEEE Access. https://doi.org/10.1109/ACCESS.2024.3365349
Type : article de journal (survey systématique PRISMA)

## Problème

Le TinyML est surtout décrit sous l'angle matériel ou applicatif ; il manque une revue centrée sur
les **algorithmes d'apprentissage** utilisables sur appareils à quelques Ko de mémoire et quelques
mW (§I-A, §II).

## Méthode

- Revue systématique **PRISMA** sur Web of Science, Scopus, IEEE Xplore, ScienceDirect et Google
  Scholar, janvier 2018 – septembre 2023 : 4233 notices → 172 articles retenus (§III, Fig. 3).
- Trois flux de conception : orienté ML, orienté matériel, **co-design** (§IV, Fig. 4).
- Taxonomie (Fig. 5) :
  - optimisation de modèle : élagage, **quantification (QAT, PTQ)**, distillation, HPO (§V-A,
    Table 1) ;
  - conception de modèle : NAS, fonctions d'activation rationnelles, convolutions séparables,
    attention (§V-B, Table 2) ;
  - algorithmes d'apprentissage : supervisé, non supervisé (détection d'anomalies), auto-supervisé,
    RL profond, faiblement supervisé, méta-apprentissage, **apprentissage continu** (§V-C, Table 3).
- Matériel (CPU/MCU, GPU, FPGA, TPU) et outils (TFLite Micro, uTensor, Edge Impulse, ELL,
  X-CUBE-AI, uTVM, MinUn) (§VI, Table 4).

## Plateforme et implémentation

Sans objet (survey).

## Résultats

Aucun résultat chiffré propre ni ligne dans `benchmarks.csv` (survey). Constats :
- Le CL est l'un des algorithmes les plus étudiés en TinyML (« popularité H », Table 3) ; la
  régularisation est citée comme approche prometteuse pour les MCU, avec un exemple sur MCU
  (réf. [149] : reconnaissance de gestes par accéléromètre) ; rejeu latent quantifié en INT8 sous
  64 Mo ([147], vraisemblablement Ravaglia et al. 2021 d'après la description — nom non donné dans
  le texte), Train++ et TyBox (rejeu) ; TinyTL et TinyOL (§V-C7).
- La détection d'anomalies domine les applications TinyML, souvent en non supervisé (§V-C2, §VII).
- Élagage, quantification et distillation sont très étudiés ; HPO, SSL et apprentissage faiblement
  supervisé le sont peu (§VII, Tables 1-3).
- Problèmes ouverts : benchmarks, mémoire, qualité des données, absence de modèle de référence et
  de jeu de données public de référence (« What's the ImageNet of TinyML? ») (§VII).

## Limites et critique

- Couverture large mais superficielle : chaque technique reçoit un paragraphe, sans comparaison
  quantitative ni tableau de performances.
- Quelques classements discutables : TinyTL rangé dans les « dynamic architectures » alors qu'il
  gèle les poids et règle les biais (§V-C7) ; GPU et TPU présentés comme bons choix TinyML, à
  l'écart de la définition en mW rappelée en §I.
- Les tableaux de « popularité » (H/M/L) ne sont pas définis quantitativement.
- 549 articles exclus car d'accès payant (§III) : biais de sélection.

## Pertinence pour la thèse

Survey de cadrage TinyML côté algorithmes : il situe l'apprentissage continu et la quantification
parmi les sujets majeurs du TinyML et recense des travaux CL sur MCU (TinyOL, Ravaglia, Train++,
TyBox). Il donne des références pour l'état de l'art du manuscrit, mais pas de chiffres
comparatifs ; les travaux primaires sont à lire pour les résultats (déduit).

## Gaps identifiés

- Pas de benchmark de référence pour l'entraînement ou le CL sur MCU (§VII).
- Apprentissage auto-supervisé et faiblement supervisé très peu explorés en TinyML (§VII).
- Pas de jeu de données public de référence pour les capteurs TinyML (§VII).

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). §VI-B (GPU) partiellement déplacé à l'extraction ;
figures non disponibles.
Déduit et non affirmé par les auteurs : nécessité de revenir aux sources primaires pour les chiffres.
