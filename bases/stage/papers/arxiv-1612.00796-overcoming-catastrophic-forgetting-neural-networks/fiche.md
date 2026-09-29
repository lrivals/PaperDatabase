---
id: arxiv-1612.00796-overcoming-catastrophic-forgetting-neural-networks
fiche: done
benchmarks: none
date: 2026-09-29
---

# Overcoming Catastrophic Forgetting in Neural Networks

James Kirkpatrick, Razvan Pascanu, Neil Rabinowitz, Joel Veness, Guillaume Desjardins, Andrei A. Rusu, Kieran Milan, John Quan, Tiago Ramalho, Agnieszka Grabska-Barwinska, Demis Hassabis, Claudia Clopath, Dharshan Kumaran, Raia Hadsell, 2017, Proceedings of the National Academy of Sciences. https://doi.org/10.1073/pnas.1611835114
Type : article de journal

## Problème

Les réseaux de neurones entraînés séquentiellement sur plusieurs tâches oublient les
précédentes (oubli catastrophique) : les poids utiles à la tâche A sont modifiés pour la
tâche B (§1). Le rejeu de toutes les données passées (« system-level consolidation ») exige une
mémoire proportionnelle au nombre de tâches, jugée impraticable (§1).

## Méthode

- **Elastic Weight Consolidation (EWC)** : pénalité quadratique qui retient chaque paramètre
  près de sa valeur après la tâche A, pondérée par son importance (§2, éq. 3) :
  L(θ) = L_B(θ) + Σ_i λ/2 · F_i (θ_i − θ*_A,i)².
- Justification bayésienne : le postérieur p(θ|D_A) sert de prior pour la tâche B ;
  approximation de Laplace → gaussienne de moyenne θ*_A et de précision diagonale donnée par
  la **diagonale de la matrice d'information de Fisher** F, calculable avec des dérivées
  premières seulement, semi-définie positive (§2).
- Plusieurs tâches : une pénalité par tâche, ou une seule (somme de quadratiques) (§2).
- Supervisé : MLP ReLU entièrement connecté sur Permuted MNIST (§2.1, §4.1) ; comparé à SGD
  seul, L2 uniforme et SGD + dropout (p = 0,2 en entrée, 0,5 ailleurs, early stopping).
- Renforcement : DQN (Double Q-learning) sur 10 jeux Atari tirés parmi 19, reconnaissance de
  tâche par un modèle génératif (HMM + Dirichlet-multinomial, « Forget Me Not »), gains et
  biais propres à chaque jeu, Fisher recalculé à chaque changement de tâche sur 100
  mini-batchs du replay buffer, multiplicateur λ = 400, EWC activé après 20 M d'images par jeu
  (§2.2, §4.2, Table 2).
- Coût annoncé : linéaire en nombre de paramètres et d'exemples (§3). Stockage par synapse :
  poids, ancre et importance (« the weight itself, its variance and its mean », §3).

## Plateforme et implémentation

Aucune plateforme matérielle décrite : travail algorithmique (n/r). Code : non publié (aucune
mention). Taille exacte du MLP MNIST : n/r dans le texte extrait (Table 1 réduite à un
fragment).

## Résultats

Tous les résultats sont donnés sous forme de courbes, sans valeur chiffrée dans le texte :
- Permuted MNIST, 3 tâches : SGD oublie A ; L2 protège A mais n'apprend pas B ; EWC garde A et
  apprend B (Fig. 2A).
- Jusqu'à 10 permutations : EWC garde une précision moyenne proche de la tâche unique, SGD +
  dropout décroche (Fig. 2B) ; valeurs n/r.
- Recouvrement des matrices de Fisher : les couches proches de la sortie sont partagées même
  pour des tâches très différentes (Fig. 2C).
- Atari : sans EWC, l'agent n'apprend jamais plus d'un jeu (score humain normalisé total < 1
  sur 10) ; avec EWC, plusieurs jeux sont appris ; donner le vrai label de tâche n'apporte
  qu'un gain modeste (§2.2, Fig. 3B). EWC n'atteint pas le score de 10 DQN séparés (§2.2).
- Perturbation des poids : le Fisher diagonal est un bon indicateur d'importance, mais
  perturber dans son noyau dégrade autant que selon l'inverse du Fisher → l'incertitude est
  sous-estimée (§2.2, Fig. 3C).

→ reportés dans `benchmarks.csv` : aucune ligne (`benchmarks: none`) — pas de valeur
numérique dans le texte, seulement des courbes.

## Limites et critique

- Aucun chiffre dans le texte : la comparaison avec d'autres méthodes de CL doit passer par
  les reproductions ultérieures (SI, MAS, surveys De Lange 2021 et Wang 2023).
- Scénario **task-incremental / domain-incremental** (Permuted MNIST, sortie partagée) : ne dit
  rien du class-incremental, où EWC est connu pour échouer (déduit de la littérature ultérieure,
  non affirmé ici).
- Les auteurs reconnaissent la faiblesse de l'estimation ponctuelle (Laplace) : incertitude
  sous-estimée (§3, Fig. 3C).
- Coût mémoire : une ancre et un Fisher par paramètre et par tâche (ou une pénalité fusionnée),
  soit ×3 le stockage des poids (§3) — non discuté en termes de contraintes embarquées.
- λ choisi par recherche d'hyperparamètres (§2.2) ; sensibilité non rapportée.

## Pertinence pour la thèse

Référence fondatrice de la régularisation en apprentissage continu, et méthode centrale du
stage (article « EWC INT8 sur MCU »). Elle fixe la formule de la pénalité et le Fisher
diagonal que l'implémentation embarquée doit approximer ; le surcoût mémoire (ancre + Fisher
par poids) est précisément ce qui pèse sur un microcontrôleur et motive la quantification
INT8 de ces tenseurs. Le papier ne traite ni de séries temporelles, ni de régression (RUL),
ni de contraintes matérielles.

## Gaps identifiés

- Coût mémoire et calcul d'EWC (Fisher + ancre) jamais évalué sous contrainte embarquée ni en
  précision réduite dans le papier d'origine.
- Pas d'évaluation en régression ni en changement de domaine progressif (dérive), cas typique
  de la maintenance prédictive.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, y compris annexes 4.1-4.3). La Table 1
(hyperparamètres MNIST) est réduite à un fragment dans l'extraction.
Déduit et non affirmé par les auteurs : l'échec d'EWC en class-incremental (littérature
ultérieure) ; l'interprétation « ×3 le stockage » (le papier parle de trois valeurs par synapse).
