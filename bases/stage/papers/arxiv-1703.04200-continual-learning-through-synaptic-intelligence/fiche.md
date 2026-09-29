---
id: arxiv-1703.04200-continual-learning-through-synaptic-intelligence
fiche: done
benchmarks: none
date: 2026-09-29
---

# Continual Learning Through Synaptic Intelligence

Friedemann Zenke, Ben Poole, Surya Ganguli, 2017, International Conference on Machine Learning (ICML). https://arxiv.org/abs/1703.04200
Type : conférence

## Problème

Les réseaux de neurones oublient les tâches passées quand la distribution des données change
au cours de l'apprentissage (§1). Les auteurs reprochent à EWC de calculer l'importance des
poids hors ligne, en fin de tâche, par un Fisher diagonal dont le calcul exact est linéaire en
nombre de sorties (§2, §3).

## Méthode

- **Synaptic Intelligence (SI)** : chaque paramètre accumule **en ligne**, pendant
  l'entraînement, sa contribution à la baisse de la perte, ω_k = −Σ g_k(t)·Δθ_k(t) (intégrale de
  chemin du gradient, éq. 1-3). Aucun gradient supplémentaire n'est nécessaire (annexe C).
- En fin de tâche : importance normalisée Ω_k = Σ_ν ω_k^ν / ((Δ_k^ν)² + ξ), Δ_k étant le
  déplacement total du paramètre sur la tâche, ξ un amortissement (éq. 5) ; puis ω remis à 0.
- Pénalité quadratique de même forme qu'EWC : L̃ = L_µ + c Σ_k Ω_k (θ̃_k − θ_k)², ancre θ̃ =
  paramètres en fin de tâche précédente, c force de consolidation (éq. 4).
- Analyse théorique : sur une perte quadratique, Ω se ramène au Hessien diagonal (Hessien
  diagonal ou de rang 1) (§4, éq. 11-14). L'empirical Fisher est nul au minimum, alors que
  l'intégrale de chemin reste proportionnelle au Hessien (annexe C).
- État par synapse : valeur courante, ancre, importance (et ω en cours) (§1, §6).
- Expériences (§5) : Split MNIST (5 tâches binaires, MLP 2×256, multi-head, ξ = 10⁻³, Adam,
  10 époques) ; Permuted MNIST (MLP 2×2000, c = 0,1, ξ = 0,1, 20 époques, état d'Adam
  conservé) ; Split CIFAR-10/100 (CNN Keras 4 conv + 2 denses, CIFAR-10 puis 5 tranches de
  10 classes de CIFAR-100, multi-head, n = 5 répétitions).

## Plateforme et implémentation

Aucune plateforme matérielle : travail algorithmique (n/r). Code : non mentionné dans le texte
extrait.

## Résultats

Résultats essentiellement graphiques :
- Split MNIST : sans consolidation, les deux premières tâches retombent au hasard après les
  5 tâches ; avec SI, dégradation mineure (Fig. 3) ; valeurs n/r.
- Permuted MNIST (10 tâches) : SI et EWC (courbe reprise de Kirkpatrick 2017) gardent une
  précision élevée, SGD et SGD + dropout s'effondrent ; SI est « seulement un peu en dessous »
  de l'entraînement joint (Fig. 4, §5.2) ; valeurs n/r.
- Split CIFAR-10/100 : SI meilleur que sans consolidation sur toutes les tâches sauf la
  dernière, et meilleur ou égal à l'entraînement from scratch en validation (sauf CIFAR-10)
  (Fig. 6, §5.3).
- Split CIFAR-10 à 2 tâches : +≈ 4,5 % de précision de validation sur la tâche B avec SI,
  interprété comme un meilleur transfert (annexe B, Fig. 7).

→ reportés dans `benchmarks.csv` : aucune ligne (`benchmarks: none`) — résultats en courbes ;
le seul chiffre (≈ 4,5 %) est un écart, pas une précision.

## Limites et critique

- Protocole **multi-head** (task-incremental) pour Split MNIST et CIFAR : le label de tâche est
  connu au test, ce qui facilite nettement le problème (déduit ; scénario identifié comme le
  plus facile par la littérature ultérieure, p. ex. De Lange 2021).
- Comparaison à EWC sur une courbe **reprise** du papier d'EWC, pas réentraînée (Fig. 4).
- ω surestime l'importance réelle à cause du bruit de SGD, d'où c < 1 réglé par grille (§3).
- Aucun coût mémoire ou temps mesuré, alors que l'argument principal est l'efficacité en ligne.

## Pertinence pour la thèse

Deuxième méthode de régularisation de référence du stage, directement comparable à EWC.
Son calcul d'importance **en ligne, sans passe supplémentaire** est attractif pour un MCU
(pas de phase Fisher en fin de tâche), mais il coûte un accumulateur de plus par paramètre et
dépend de la trajectoire d'optimisation, ce qui interagit avec la quantification des mises
à jour (déduit). Le papier ne traite ni la régression ni les séries temporelles.

## Gaps identifiés

- Estimation d'importance en ligne (SI) sous arithmétique entière / mises à jour quantifiées :
  non étudiée ; l'accumulation g·Δθ est sensible à l'arrondi (déduit).
- Pas d'évaluation hors classification multi-head (single-head, régression, dérive progressive).

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, annexes A-C comprises).
Déduit et non affirmé par les auteurs : la facilité du protocole multi-head ; la sensibilité de
SI à la quantification des mises à jour.
