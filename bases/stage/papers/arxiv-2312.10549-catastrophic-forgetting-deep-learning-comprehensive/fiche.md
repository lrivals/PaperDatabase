---
id: arxiv-2312.10549-catastrophic-forgetting-deep-learning-comprehensive
fiche: done
date: 2026-09-29
---

# Catastrophic Forgetting in Deep Learning: A Comprehensive Taxonomy

Everton L Aleixo, Juan G Colonna, Marco Cristo, Everlandio Fernandes, 2023, arXiv preprint. https://arxiv.org/abs/2312.10549
Type : preprint non relu par les pairs selon les métadonnées. Le texte porte la mention « ©2023 The
Authors. Published by AI Access Foundation under CC BY 4.0 », ce qui laisse penser qu'il a été
publié par l'éditeur de JAIR (non vérifié).

## Problème

L'oubli catastrophique (CF) reste sans solution ni protocole d'évaluation consensuels ; les
surveys existants se limitent souvent à un scénario (task- ou class-incremental) ou à une
comparaison empirique (§1, §2). Les auteurs rappellent que trouver des paramètres qui évitent
l'oubli dans un modèle fixe est NP-difficile (réduction à SAT, Knoblauch et al. 2020) (§1).

## Méthode

Revue « systématique » selon Kitchenham & Charters (2007), plus de 230 travaux depuis 2012,
sans comparaison chiffrée, faute de protocole commun (§1, §4). Taxonomie en quatre familles plus
les hybrides (§3, Fig. 2) :

- **Rehearsal** (§3.1) : *pseudo-rehearsal* (données générées : GAN/DGR, VAE, inversion de
  modèle, prototypes bruités, hyperréseaux) et *mini-rehearsal* (coreset : GDumb, sélection par
  gradients, ExStream, herding, reservoir, MIR, GEM/A-GEM, LUCIR, BiC, prompts L2P).
- **Distance-based** (§3.2) : prototypes de classes, classifieurs cosinus, compensation de la
  dérive sémantique (SDC), apprentissage non supervisé des représentations.
- **Sub-networks** (§3.3) : *soft* (pénalité sur les poids importants : EWC, Predictive EWC,
  R-EWC, SI, MAS, VCL, Laplace-Kronecker, IMM, OWM, LwM) et *hard* (poids gelés : PathNet,
  PackNet, HAT, Piggyback, pruning).
- **Dynamic networks** (§3.4) : croissance du modèle (PNN, Expert Gate, DEN, NAS, LwF rangé ici
  car il ajoute une tête par tâche).
- **Hybrides** (§3.5) : iCaRL, EEIL, DER, Else-Net…
- Scénarios couverts en plus des classiques : online incremental, unbounded task incremental,
  data-free incremental (§2).

## Plateforme et implémentation

Sans objet (survey).

## Résultats

Aucun résultat chiffré propre ni ligne dans `benchmarks.csv` (survey sans comparaison
numérique, choix assumé, §1). Constats qualitatifs :
- **Soft sub-networks (EWC, SI…)** : efficaces quand la dérive entre tâches est faible (splits de
  MNIST), inefficaces quand les tâches viennent de domaines différents ; SI ou IMM à préférer
  quand le temps d'entraînement compte (§3.3.1).
- Limites d'EWC relevées : Fisher supposée diagonale, couches de batch normalization ignorées,
  coût du calcul de la Fisher en post-traitement ; Continual Normalization proposée contre la BN
  (§3.3.1).
- Les réseaux dynamiques sont peu adaptés à l'edge et au mobile, faute de place (§3.4) ; les
  sous-réseaux + rejeu (régularisation de la seule dernière couche + petit coreset) sont signalés
  comme adaptés aux ressources limitées (§3.5.4).
- Ces deux dernières années, la plupart des travaux utilisent une variante de mini-rehearsal
  (§4).

## Limites et critique

- « Systematic review » annoncé mais protocole (requêtes, bases, critères, nombre d'articles
  filtrés) non détaillé dans le texte.
- Pas de tableau de synthèse comparatif ; la taxonomie range EWC dans « sub-networks », à rebours
  de l'usage (famille « régularisation » chez De Lange et al.), et LwF dans « dynamic networks » :
  source de confusion pour la comparaison avec d'autres surveys.
- Aucune évaluation de coût (mémoire, énergie) malgré les mentions de l'edge computing.
- Séries temporelles et régression absentes ; focus vision, NLP, RL.

## Pertinence pour la thèse

Survey de cadrage générique, utile pour situer EWC parmi les « soft sub-networks » et en citer les
limites connues (Fisher diagonale, BN, coût, dérive de domaine forte). Deux points servent
directement l'argumentaire MCU : la remarque que la régularisation de la seule dernière couche,
avec un petit coreset, peut suffire (§3.5.4) et l'inadéquation des réseaux dynamiques à l'edge
(§3.4). Il ne couvre ni la PdM ni les séries temporelles (déduit de la lecture complète).

## Gaps identifiés

- Pas de protocole standard de mesure de l'oubli (§4) — à fortiori pour la régression.
- EWC et dérive de domaine forte entre tâches : cas d'échec signalé, peu étudié en PdM.
- Coût mémoire/énergie des familles de méthodes non comparé.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Quelques passages fusionnés à l'extraction (fin de
§3.1.2, légendes de figures) ; figures non disponibles.
Déduit et non affirmé par les auteurs : publication JAIR (d'après la mention d'éditeur),
absence de PdM et de séries temporelles.
