---
id: arxiv-1706.08840-gradient-episodic-memory-continual-learning
fiche: done
date: 2026-09-29
---

# Gradient Episodic Memory for Continual Learning

David Lopez-Paz, Marc'Aurelio Ranzato, 2017, Advances in Neural Information Processing Systems (NeurIPS). https://arxiv.org/abs/1706.08840
Type : conférence

## Problème

L'apprentissage supervisé classique (ERM) suppose des données iid et plusieurs passes ; un
apprenant continu voit au contraire un flux ordonné, une seule fois, avec une mémoire limitée
(§1). La littérature évalue peu de tâches, beaucoup d'exemples, plusieurs passes et une seule
métrique (précision moyenne) (§2).

## Méthode

- **Cadre d'évaluation** : matrice R (précision sur la tâche j après la tâche i) et trois
  métriques : **ACC** (moyenne finale), **BWT** (backward transfer, négatif = oubli), **FWT**
  (forward transfer) (§2, éq. 2-4). Protocole : une seule passe, mini-batchs de 10, tâche
  identifiée par un descripteur t.
- **Gradient Episodic Memory (GEM)** : mémoire épisodique de M exemples (m = M/T par tâche,
  les derniers vus) ; les pertes sur la mémoire de chaque ancienne tâche servent de
  **contraintes d'inégalité** : elles ne doivent pas augmenter (§3, éq. 6).
- Contraintes linéarisées : produit scalaire ⟨g, g_k⟩ ≥ 0 entre le gradient courant et celui
  de chaque ancienne tâche ; en cas de violation, projection du gradient sur le plus proche
  gradient admissible par un **QP dual** à t−1 variables (§3, éq. 7-11). Petit biais γ vers le
  transfert positif.
- Permet un transfert arrière positif, contrairement à la distillation (§3).
- Architectures : MLP 2×100 ReLU (MNIST), ResNet18 réduit ×3 avec une tête par tâche
  (CIFAR-100) ; SGD, grille d'hyperparamètres (§4.2, annexe A).

## Plateforme et implémentation

Temps d'entraînement mesurés sur **CPU** (modèle n/r) (Table 1). Code publié :
https://github.com/facebookresearch/GradientEpisodicMemory (§1).

## Résultats

- CIFAR-100 incrémental, ACC selon la mémoire : GEM 0,487 / 0,579 / 0,633 / 0,654 pour
  200 / 1280 / 2560 / 5120 exemples ; iCaRL 0,436 / 0,494 / 0,500 / 0,508 (Table 2).
- MNIST Rotations, ACC/BWT selon le nombre d'époques par tâche (1 / 2 / 5) : GEM 0,86/+0,05,
  0,88/+0,02, 0,89/−0,02 ; EWC 0,55/−0,19, 0,59/−0,17, 0,61/−0,11 ; borne iid
  0,83 / 0,87 / 0,89 (Table 3).
- Temps CPU d'entraînement (MNIST, s) : permutations single 11, EWC 179, GEM 77 ;
  rotations single 11, EWC 169, GEM 135 (Table 1).
- Résultats ACC/BWT/FWT de toutes les méthodes : Fig. 1 (valeurs lisibles seulement dans les
  matrices de l'annexe B, dont l'extraction est illisible).

→ reportés dans `benchmarks.csv` : 2 lignes (CIFAR-100 mémoire 5120, Table 2 ; MNIST
Rotations 1 époque, Table 3 ; `high`).

## Limites et critique

- Coût : une passe arrière **par ancienne tâche** à chaque itération (les auteurs le citent
  comme point faible, §6) et un QP à résoudre ; croît avec le nombre de tâches.
- Mémoire « derniers exemples » naïve ; pas d'étude de sélection (§3, §6).
- Descripteur de tâche fourni (et tête par tâche sur CIFAR) : scénario task-incremental.
- EWC évalué ici dans un protocole une seule passe, mini-batch 10, pour lequel il n'a pas été
  conçu : sa faiblesse (Table 3) est en partie un effet de protocole (déduit).

## Pertinence pour la thèse

Représentant de la famille « rejeu par contrainte de gradient » et surtout source des
**métriques ACC/BWT/FWT**, reprises par la plupart des papiers de CL embarqué du corpus. Pour
un MCU, GEM est coûteux (stockage d'exemples + gradients par tâche + QP) : il sert de
référence haute plutôt que de candidat (déduit). Protocole « une seule passe » proche du cas
flux de capteurs.

## Gaps identifiés

- GEM/A-GEM sous contrainte mémoire de quelques kilo-octets : non étudié.
- Métriques BWT/FWT jamais déclinées pour la régression (RUL) dans ce papier.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Les matrices R de l'annexe B sont extraites en
vrac (nombres sans structure) : non exploitées. Fig. 1 non chiffrée dans le texte.
Déduit et non affirmé par les auteurs : l'effet du protocole sur EWC ; l'inadaptation au MCU.
