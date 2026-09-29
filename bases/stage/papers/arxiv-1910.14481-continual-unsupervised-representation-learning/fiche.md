---
id: arxiv-1910.14481-continual-unsupervised-representation-learning
fiche: done
date: 2026-09-29
---

# Continual Unsupervised Representation Learning

Dushyant Rao, Francesco Visin, Andrei A Rusu, Yee Whye Teh, Razvan Pascanu, Raia Hadsell, 2019, arXiv preprint. https://arxiv.org/abs/1910.14481
Type : preprint non relu par les pairs (version arXiv)

## Problème

Le CL suppose le plus souvent des tâches étiquetées, des frontières connues et une
supervision par classe. Les auteurs posent le problème du CL **non supervisé** : ni identité
ni frontière de tâche, ni label de classe, avec des changements brutaux, progressifs, ou des
données mélangées (Abstract, §1).

## Méthode

**CURL** : VAE à latent en mélange de gaussiennes, où la variable catégorielle y fait office
de « tâche » inférée (§2.1, Fig. 1-2) :

- Modèle génératif y ~ Cat(π), z ~ N(μ(y), σ²(y)), x ~ Bernoulli(μ(z)) ; posteriori
  q(y|x) (tête softmax d'inférence de tâche) et q(z|x, y) (une tête par composante) ; ELBO
  marginalisé sur les K composantes (Eq. 2-3).
- **Expansion dynamique** (§2.3) : les échantillons d'ELBO < c_new (−200) vont dans un
  buffer ; quand il atteint N_new, une nouvelle composante est créée, initialisée depuis la
  composante la plus proche, puis ajustée sur le buffer. Coût ≈ 10⁴ paramètres par
  composante contre ≈ 2,5·10⁶ pour le modèle partagé.
- **Mixture Generative Replay (MGR)** (§2.4) : alternance de batchs réels et générés par un
  instantané du modèle, les composantes étant tirées selon leur usage passé ; instantané
  pris soit à période fixe, soit **juste avant chaque expansion** (sans connaissance des
  frontières de tâche).
- Évaluation : précision de clustering (composante → classe majoritaire) et erreur k-NN
  dans l'espace latent ; réglages i.i.d., séquentiel et *continuous drift* (classes
  introduites progressivement) sur MNIST et Omniglot (§4.1).

## Plateforme et implémentation

Entraînement sur un GPU Tesla V100 par graine ; 1 h (SplitMNIST supervisé), 3 h (MNIST
séquentiel), 10 h (Omniglot) ; marginalisation sur toutes les composantes = goulot
d'étranglement (Annexe C). Encodeur MLP {1200, 600, 300, 150}, K max = 25, latent de
dimension 32 (C.1). Aucune implémentation embarquée ; précision numérique n/r. Code : non
publié (n/r dans le texte).

## Résultats

- MNIST séquentiel : précision de clustering jusqu'à 84 % selon le seuil d'expansion
  (12 à 71 composantes) ; 51 % sans expansion ; 77 % avec expansion à 25 composantes contre
  51 % pour 25 composantes fixes (§4.3, Fig. 4).
- Oubli faible : les classes anciennes restent bien modélisées, les confusions portent sur
  des classes proches (3/5, 7/9) (§4.2, Fig. 3).
- Dérive continue ≥ changements brutaux en général (§4.4, Table 2). MGR avec instantané à
  l'expansion récupère l'essentiel des performances de l'instantané aux frontières connues
  (§4.3, Table 1).
- Représentation apprise en séquentiel, erreur 10-NN : 4,50 % sur MNIST (latent 50) contre
  4,23 % pour CURL i.i.d. ; 78,80 % sur Omniglot (latent 100) contre 72,51 % i.i.d. (Table 4).
- SplitMNIST supervisé : CURL n'est battu que par iCaRL en class-incremental (§4.5) —
  valeurs n/r (Table 3 absente de l'extraction).

→ reportés dans `benchmarks.csv` : 2 lignes (MNIST séquentiel : erreur 10-NN, Table 4,
`high` ; précision de clustering maximale, §4.3, `medium`).

## Limites et critique

- Validation sur MNIST et Omniglot seulement, données binaires et très discriminantes par
  les pixels bruts (erreur k-NN ≈ 3 % sur MNIST, Table 4, Annexe A.4).
- Le coût d'inférence croît avec le nombre de composantes (marginalisation), goulot reconnu
  (Annexe C).
- Le rejeu génératif demande de conserver un instantané complet du modèle : mémoire
  doublée (déduit).
- Le seuil d'expansion règle à la fois capacité et précision (§4.3) ; il est choisi sur
  l'ensemble de validation.
- Table 3 (comparaison supervisée) absente de l'extraction.

## Pertinence pour la thèse

Pertinence méthodologique : deux mécanismes transposables à la détection de dérive
non supervisée — (1) un buffer d'échantillons « mal expliqués » (ELBO sous un seuil) qui
déclenche l'expansion, équivalent à un détecteur de nouveauté par vraisemblance ; (2) la
consolidation déclenchée par ce même détecteur plutôt que par une frontière de tâche connue.
Pour un MCU, le rejeu génératif et la marginalisation sur K composantes semblent trop coûteux
(déduit), mais l'idée de déclencher la mise à jour sur une chute de vraisemblance rejoint la
détection d'anomalies par erreur de reconstruction.

## Gaps identifiés

- CL non supervisé sur séries temporelles de capteurs (vibrations, RUL) : non traité.
- Détection de nouveauté par seuil d'ELBO comparée aux détecteurs de dérive classiques.
- Coût mémoire/calcul du rejeu génératif à budget embarqué.

## Statut de lecture

Papier complet, annexes comprises (`fulltext.md` lu en entier). Tables 1-3 partiellement ou
pas extraites (valeurs de Table 2 sans en-têtes de colonnes) ; figures non disponibles.
Déduit et non affirmé par les auteurs : doublement mémoire du rejeu génératif, lien avec la
détection d'anomalies par reconstruction, transposition MCU.
