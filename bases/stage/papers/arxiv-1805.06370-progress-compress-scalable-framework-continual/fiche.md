---
id: arxiv-1805.06370-progress-compress-scalable-framework-continual
fiche: done
benchmarks: none
date: 2026-09-29
---

# Progress & Compress: A Scalable Framework for Continual Learning

Jonathan Schwarz, Wojciech Czarnecki, Jelena Luketina, Agnieszka Grabska-Barwinska, Yee Whye Teh, Razvan Pascanu, Raia Hadsell, 2018, International Conference on Machine Learning (ICML). https://arxiv.org/abs/1805.06370
Type : conférence

## Problème

Concilier les desiderata du CL, souvent contradictoires : pas d'oubli, transfert avant et
arrière positif, passage à l'échelle en nombre de tâches, pas de labels de tâche (§1).
EWC accumule des régularisateurs qui sur-contraignent le réseau ; les Progressive Nets
croissent quadratiquement avec le nombre de tâches (§1).

## Méthode

- **Progress & Compress (P&C)** : deux colonnes de taille fixe, une **knowledge base** (KB) et
  une **colonne active**, entraînées en alternance (§2, Fig. 1).
- Phase *progress* : KB figée ; la colonne active apprend la nouvelle tâche sans contrainte,
  en réutilisant les features de la KB par des adaptateurs latéraux (MLP, 1×1 conv) comme
  les Progressive Nets (§2.1, éq. 1). Réinitialiser la colonne active entre tâches est
  recommandé pour des tâches diverses.
- Phase *compress* : distillation (KL, température τ) de la colonne active vers la KB,
  protégée par **online EWC** (§2.2, éq. 2).
- **Online EWC** : une seule ancre (dernier MAP θ*_{i−1}) et un Fisher cumulé
  F*_i = γ F*_{i−1} + F_i, avec γ < 1 pour un oubli progressif et contrôlé ; Fisher normalisés
  par tâche ; coût constant en nombre de tâches ; nécessite de connaître les **frontières** de
  tâche, pas leur identité (§4, éq. 8-9).
- Expériences : Omniglot (50 alphabets, CNN 4×64), 6 jeux Atari et 8 labyrinthes 3D
  (actor-critic distribué), 4 graines en RL (§5, annexe C).

## Plateforme et implémentation

Aucune plateforme matérielle décrite (n/r). Code : non mentionné.

## Résultats

- Omniglot, rétention de la première tâche : pas de différence notable entre EWC et online
  EWC ; LwF bon jusqu'à 5 tâches puis décroche ; P&C comparable à online EWC seul (Fig. 2a).
- Transfert avant sur Atari, en % de la performance mono-tâche après 1 à 5 tâches
  précédentes : P&C (colonne réinitialisée) 127 / 129 / 125 / 129 / 128 ; fine-tuning
  117 / 125 / 117 / 105 / 98 ; EWC 55 / 53 / 53 / 50 / 54 ; online EWC 53 / 53 / 49 / 50 / 57
  (Table 1). Les deux EWC montrent un transfert négatif de plus de 40 % (§5.2).
- Labyrinthes : P&C au niveau du fine-tuning en transfert avant, online EWC en dessous (Fig. 3).
- Omniglot, performance finale sur les 50 alphabets : P&C a la meilleure moyenne, online EWC
  compétitif (Table 2 — corps du tableau non extrait) (§5.3).
- Annexe A (Permuted MNIST, MLP 30-30-10) : avec peu d'itérations EWC retient mieux les
  anciennes tâches que online EWC (Fig. 5-6).

→ reportés dans `benchmarks.csv` : aucune ligne (`benchmarks: none`) — Table 1 en % de la
performance mono-tâche (ratio), Table 2 non extraite, le reste en figures.

## Limites et critique

- Table 2 (Omniglot) absente de l'extraction : l'affirmation « P&C meilleur » n'est pas
  vérifiable ici.
- Double réseau pendant l'apprentissage (KB + colonne active + adaptateurs) : empreinte
  mémoire au moins doublée par rapport à EWC (déduit).
- Frontières de tâche supposées connues (§6).
- Recentrage de l'ancre sur le dernier MAP : les tâches anciennes sont moins protégées
  (discuté §4, annexe A).

## Pertinence pour la thèse

Source de l'**online EWC** (un seul Fisher cumulé avec facteur d'oubli γ), la variante qui
rend EWC compatible avec une mémoire fixe : c'est celle qu'une implémentation MCU d'EWC
doit adopter pour ne pas stocker un Fisher par tâche (déduit). Le facteur γ offre aussi un
oubli contrôlé, utile quand le régime d'une machine évolue. Le schéma à deux colonnes est en
revanche trop coûteux pour un MCU.

## Gaps identifiés

- Online EWC sous dérive progressive sans frontières de tâche nettes (détectées par un test de
  dérive) : piste évoquée par les auteurs (§6), non évaluée.
- Coût mémoire d'online EWC en précision réduite : non étudié.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, annexes A-C). Table 2 réduite à son titre ;
annexe C.2 tronquée.
Déduit et non affirmé par les auteurs : empreinte mémoire doublée ; pertinence MCU.
