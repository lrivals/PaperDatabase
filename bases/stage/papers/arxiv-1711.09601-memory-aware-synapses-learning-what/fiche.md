---
id: arxiv-1711.09601-memory-aware-synapses-learning-what
fiche: done
date: 2026-09-29
---

# Memory Aware Synapses: Learning What (not) to Forget

Rahaf Aljundi, Francesca Babiloni, Mohamed Elhoseiny, Marcus Rohrbach, Tinne Tuytelaars, 2018, European Conference on Computer Vision (ECCV). https://arxiv.org/abs/1711.09601
Type : conférence

## Problème

Avec une capacité de modèle finie et un flux de tâches illimité, tout préserver est
impossible : il faut choisir quoi oublier (Abstract, §1). Les méthodes de régularisation
existantes (EWC, SI) calculent l'importance des poids à partir de la perte, donc avec des
labels et pendant l'entraînement ; SI sous-estime l'importance des poids peu déplacés d'un
réseau pré-entraîné (§2).

## Méthode

- **Memory Aware Synapses (MAS)** : importance d'un paramètre = sensibilité de la **sortie**
  du réseau (et non de la perte) à ce paramètre, moyennée sur les données :
  Ω_ij = (1/N) Σ_k ‖∂F(x_k; θ)/∂θ_ij‖ (§4.1, éq. 2).
- Pour une seule passe arrière : gradient de la norme ℓ2² de la sortie (un scalaire par
  échantillon) au lieu du vecteur de sortie (§4.1).
- **Non supervisé et en ligne** : Ω se calcule sur des données sans label (entraînement,
  validation ou test), et peut s'adapter aux conditions de déploiement (§4.2, §4.4).
- Pénalité : L(θ) = L_n(θ) + λ Σ Ω_ij (θ_ij − θ*_ij)², Ω cumulé d'une tâche à l'autre (éq. 3).
- Variante locale **l-MAS** : couche par couche ; avec ReLU, Ω_ij = moyenne de y_i·y_j, soit une
  règle de Hebb (§4.3, annexe B).
- Mémoire hors ligne : poids + importances, comme SI ; SI demande en plus un accumulateur
  pendant l'entraînement (annexe C2).

## Plateforme et implémentation

Aucune plateforme matérielle (n/r). AlexNet pré-entraîné ImageNet, SGD 100 époques, batch
200 (§5.1) ; VGG-16 pour les faits (§5.2). Code : n/r dans le texte extrait.

## Résultats

- 2 tâches (AlexNet, multi-head avec oracle de tâche) : MAS a la plus faible baisse sur la
  1re tâche dans 3 séquences sur 4 (−0,4 ; −0,7 ; −0,8 points) ; EWC meilleur sur
  Scenes → Birds (−0,8 contre −1,4) (Table 2).
- Ω calculé sur train, test (sans label) ou les deux : résultats proches ; l-MAS oublie ≈ 3 %
  contre ≈ 1 % pour MAS (Table 3, §5.1).
- Norme ℓ2² vs sortie vectorielle : baisse 0,50 % ± 0,19 contre 0,51 % ± 0,18, n fois plus
  rapide (§5.1).
- 8 tâches : précision moyenne MAS 52,69 %, SI 50,49, EBLL 50,29, EWC 50,0, LwF 49,49,
  IMM 43,41, Finetune 32,67 ; oubli moyen −0,49 % (SI −1,27, EWC −3,18) (Fig. 5, Table C1).
- MAS est la méthode (hors Finetune) qui consomme le moins de mémoire (Fig. 4) ; valeurs en
  Mo seulement sur figure (Fig. C1).
- λ = 1 sans réglage ; faible sensibilité autour de 1 sur 5 tâches Permuted MNIST (Fig. 6).
- Adaptation : importance calculée sur une seule classe (Krishna Kamal) → oubli 2 % sur
  cette classe contre 8 % sur Flowers entier, et 84 % sur la dernière tâche au lieu de 69 %
  (§5.1).
- Faits (6DS, 4 tâches, embedding partagé) : MAP global 0,29 (MAS), 0,25 (SI), 0,18
  (Finetune) ; 0,30 avec Ω sur train + test (§5.2, Table 4). Sous-ensemble « sport » : 0,50
  contre ≈ 0,20 pour SI et Finetune (Fig. 7).

→ reportés dans `benchmarks.csv` : 2 lignes (8 tâches, Table C1, `high` ; faits 6DS split 1,
Table 4 reconstruite par PyMuPDF, `medium`, MAP exprimé en % : 29).

## Limites et critique

- Protocole **multi-head avec oracle de tâche** (§5.1) : task-incremental, cas facile.
- Écarts faibles (≈ 1-2 points) entre MAS, SI et EWC, sans écart-type sur la plupart des
  expériences (3 essais seulement pour ℓ2²).
- λ non réglé pour MAS mais réglé pour SI et EWC (§5.1) : la comparaison n'est pas
  symétrique, ce qui peut jouer dans les deux sens.
- Mémoire comparée sur une figure, sans valeur exacte dans le texte.

## Pertinence pour la thèse

Troisième méthode de régularisation du stage. Son intérêt pour l'embarqué est double :
l'importance se calcule **sans label**, sur les données vues en service, et d'une seule passe
arrière ; le stockage hors ligne est le même que SI (poids + importances). Sur un capteur de
maintenance, cela permettrait d'ajuster l'importance aux conditions réelles de
fonctionnement (déduit). Classification uniquement ; rien sur la régression ou les séries
temporelles.

## Gaps identifiés

- MAS non supervisé sur flux de capteurs sans labels (cas PdM) : non évalué.
- Pas de mesure de coût (temps, mémoire) sur plateforme contrainte.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, annexes B-F comprises). Table 1 (propriétés des
méthodes) mal extraite ; Table 4 reconstruite par PyMuPDF.
Déduit et non affirmé par les auteurs : intérêt pour la maintenance prédictive embarquée.
