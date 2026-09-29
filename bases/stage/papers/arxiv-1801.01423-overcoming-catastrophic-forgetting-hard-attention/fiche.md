---
id: arxiv-1801.01423-overcoming-catastrophic-forgetting-hard-attention
fiche: done
date: 2026-09-29
---

# Overcoming Catastrophic Forgetting with Hard Attention to the Task

Joan Serra, Didac Suris, Marius Miron, Alexandros Karatzoglou, 2018, International Conference on Machine Learning (ICML). https://arxiv.org/abs/1801.01423
Type : conférence

## Problème

Préserver les tâches passées sans gêner l'apprentissage de la tâche courante (Abstract). Le
rejeu et le pseudo-rejeu imposent de retraiter d'anciens exemples ; la régularisation
structurelle (EWC, SI) ou l'allocation de sous-réseaux (PNN, PathNet, PackNet, DEN)
demandent de pré-assigner de la capacité ou reposent sur des heuristiques (§1, §3).

## Méthode

- **Hard Attention to the Task (HAT)** : pour chaque couche l et tâche t, un embedding de
  tâche e_l^t passe par une sigmoïde très raide, a_l^t = σ(s·e_l^t), qui multiplie les sorties
  des unités (masque quasi binaire, par unité) ; dernière couche = tête multi-head (§2.2, éq. 1).
- Attention cumulée a_l^≤t = max(a_l^t, a_l^≤t−1) ; les gradients des poids sont multipliés par
  1 − min(a_l,i^≤t, a_l−1,j^≤t) : les poids reliant des unités utiles aux anciennes tâches sont
  figés (§2.3, éq. 2).
- Recuit de s au sein de chaque époque de 1/s_max à s_max (éq. 3) et compensation du gradient
  des embeddings (§2.4-2.5).
- Régularisation L1 pondérée des masques pour réserver de la capacité aux tâches futures
  (§2.6, éq. 4-5).
- Deux hyperparamètres : stabilité s_max (400) et compressibilité c (0,75) ; plages sûres
  s_max ∈ [25, 800], c ∈ [0,1 ; 2,5] (§4.3, Fig. 4).
- Nouvelle métrique : ratio d'oubli ρ normalisé entre classifieur aléatoire (−1) et
  multitâche (0) (§4, éq. 6).
- Protocole principal : séquences aléatoires de 8 jeux (CIFAR-10/100, FaceScrub,
  FashionMNIST, NotMNIST, MNIST, SVHN, TrafficSigns) en 32×32×3, 10 graines, réseau type
  AlexNet 7,1 M paramètres pour toutes les méthodes (§4).

## Plateforme et implémentation

Entraînement sur une NVIDIA Pascal Titan X (Table 5). PyTorch 0.2.0 (§4). Code annoncé
public (§1, lien en note non extrait).

## Résultats

- Ratio d'oubli ρ après 2 et 8 tâches : HAT −0,02 / −0,06 ; meilleurs concurrents EWC −0,08 à
  t = 2 et PNN −0,11 à t = 8 ; SGD −0,20 / −0,66 ; LwF −0,14 / −0,80 (Table 1) → réduction de
  l'oubli de 75 % et 45 % (§4.1).
- CIFAR incrémental (10 tâches) : HAT ρ ≤10 = −0,09 contre −0,18 pour EWC (§4.2).
- Permuted MNIST, 10 tâches : HAT-small 91,6 % (0,1 M), HAT-medium 97,4 % (0,7 M),
  HAT-large 98,6 % (5,8 M) contre SI 97,1 et EWC 96,9 à 5,8 M (Table 7).
- Split MNIST (2 tâches) : 99,0 % contre 94,9 % pour CAB (Table 8).
- Compression mono-tâche par les masques : réseau réduit à 1,2-21,4 % de sa taille avec
  une précision proche (p. ex. CIFAR-100 52,7 → 49,1 % à 21,4 % ; MNIST 99,5 → 99,4 % à
  1,2 %) (Table 4).
- Temps d'entraînement (Titan X, 8 tâches) : HAT 2,2 h, 11,7 ms par batch avant + arrière,
  contre EWC 3,9 h / 19,7 ms et SGD 1,4 h / 6,6 ms (Table 5).

→ reportés dans `benchmarks.csv` : 3 lignes (Permuted MNIST small et large, Table 7 ; Split
MNIST, Table 8 ; `high`). Les baselines de ces tableaux sont reprises de la littérature.

## Limites et critique

- **Identifiant de tâche requis** à l'inférence (embeddings par tâche + têtes multiples) :
  inutilisable tel quel quand la tâche ou le régime n'est pas connu.
- Les chiffres Permuted et Split MNIST des concurrents sont **repris** d'autres papiers
  (Table 7-8), avec des architectures appariées en nombre de paramètres seulement.
- Grille d'hyperparamètres des baselines sur une seule graine (§4).
- Tables 3 et 6 tronquées dans l'extraction (HAT absent des lignes extraites de la Table 6).

## Pertinence pour la thèse

Représentant de la famille « architecture / masques » de la bibliographie du stage. Les
masques binaires par unité sont très compacts (quelques bits par unité et par tâche) et
figent explicitement des poids : piste intéressante pour un MCU où l'on veut éviter de
stocker un Fisher par poids (déduit). La dépendance au label de tâche limite l'usage en
maintenance prédictive, où le régime courant doit être inféré.

## Gaps identifiés

- HAT sans identifiant de tâche (inférence du régime) : non traité.
- Masquage par unité comme alternative bon marché à EWC sur MCU : non étudié.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, annexes comprises). Tables 3 et 6 tronquées,
Table 8 partielle ; lien du code en note de bas de page non extrait.
Déduit et non affirmé par les auteurs : l'intérêt mémoire face à EWC sur MCU.
