---
id: 2008-liu-isolation-forest
fiche: done
date: 2026-09-29
---

# Isolation Forest

Fei Tony Liu, Kai Ming Ting, Zhi-Hua Zhou, 2008, 2008 Eighth IEEE International Conference on Data Mining 413-422. https://doi.org/10.1109/ICDM.2008.17
Type : conférence (ICDM 2008)

## Problème

Les détecteurs d'anomalies à modèle construisent un profil du normal, puis signalent ce qui s'en
écarte : ils ne sont pas optimisés pour isoler les anomalies (fausses alarmes ou oublis) et coûtent
cher en grande dimension ou sur de gros volumes (distances, densités) (§1).

## Méthode

**iForest** : isoler les anomalies plutôt que profiler le normal, en exploitant le fait qu'elles
sont « few and different » (§1-4).

- **iTree** : partition récursive aléatoire (attribut tiré au hasard, seuil tiré entre min et max)
  jusqu'à isoler chaque point ou atteindre une hauteur limite ; les anomalies sont isolées près de
  la racine (§2, Fig. 1).
- **Score** s(x, n) = 2^(−E(h(x))/c(n)), avec h(x) la longueur de chemin et c(n) = 2H(n−1) − 2(n−1)/n
  la longueur moyenne d'une recherche infructueuse dans un arbre binaire ; s → 1 pour une anomalie,
  s ≪ 0,5 pour un point normal, s ≈ 0,5 partout s'il n'y a pas d'anomalie nette (Eq. 1-2).
- **Sous-échantillonnage** : chaque arbre est construit sur ψ = 256 points tirés sans remise, avec
  une hauteur limite ⌈log₂ ψ⌉ ; t = 100 arbres. Le sous-échantillonnage réduit les effets de
  *swamping* et de *masking* (§3, §4.1).
- Complexité : O(tψ log ψ) à l'entraînement, O(nt log ψ) à l'évaluation ; modèle < 511·t·b octets
  pour ψ = 256 (b = taille d'un nœud) (§4, §6).
- Évaluation : 11 jeux réels (KDD Cup 99 Http et Smtp, ForestCover, Shuttle, Mammography,
  Annthyroid, Satellite, Pima, Breastw, Arrhythmia, Ionosphere) et Mulcross (synthétique), labels
  d'anomalie utilisés seulement pour l'AUC ; comparaison à ORCA (k-NN), LOF et Random Forests
  (§5, Table 2).

## Plateforme et implémentation

Cluster Linux, un seul thread à 2,3 GHz (§5). Pas d'implémentation embarquée ; précision numérique
n/r. Code : non publié (n/r dans le texte).

## Résultats

AUC (Table 3) :

| Jeu | iForest | ORCA | LOF | RF |
|---|---|---|---|---|
| Http (KDD99) | **1,00** | 0,36 | NA | NA |
| ForestCover | **0,88** | 0,83 | NA | NA |
| Mulcross | **0,97** | 0,33 | NA | NA |
| Shuttle | **1,00** | 0,60 | 0,55 | NA |
| Mammography | **0,86** | 0,77 | 0,67 | NA |
| Pima | 0,67 | **0,71** | 0,49 | 0,65 |
| Ionosphere | 0,85 | **0,92** | 0,89 | 0,85 |

- Temps total sur Http : 15,6 s pour iForest contre 9487 s pour ORCA (Table 3) ; ψ × 64 ne
  multiplie le temps que par 1,6 (§6).
- AUC quasi optimale dès ψ = 128 (Http) ou 512 (ForestCover) (§5.2, Fig. 6).
- **Entraînement sur données normales seules** : AUC 0,9997 → 0,9919 (Http) et 0,8817 → 0,8802
  (ForestCover), récupérée en augmentant ψ (§5.4).
- 506 attributs de bruit ajoutés : sélection de sous-espace par kurtosis, temps < 30 s (§5.3,
  Fig. 7).

→ reportés dans `benchmarks.csv` : 3 lignes (iForest : ForestCover, Mammography, Shuttle ; AUC × 100,
Table 3), `high` (Table 3 lisible malgré le désalignement des colonnes de temps).

## Limites et critique

- Données tabulaires statiques, sans dimension temporelle ; les anomalies sont des classes
  minoritaires de jeux de classification, pas des défauts réels de machines.
- ORCA a été réglé avec N = n/8 (son réglage par défaut donne une AUC de 0,5) : sensible au
  paramétrage (§5).
- LOF et RF ne sont testés que sur une partie des jeux (coût mémoire ou temps).
- Partitions alignées sur les axes : difficultés connues sur des anomalies qui ne se séparent
  qu'en combinaison d'attributs (déduit ; limite reprise par les variantes ultérieures).
- Pas de mécanisme de mise à jour en flux : le modèle est statique (déduit).

## Pertinence pour la thèse

Détecteur d'anomalies non supervisé de référence, cité dans la bibliographie du stage : entraînable
sur données normales seules (§5.4), sans calcul de distance, avec un modèle borné (≈ 511 nœuds par
arbre pour ψ = 256). Sur MCU, 100 arbres de 511 nœuds de quelques octets représentent plusieurs
centaines de Ko, ce qui impose de réduire t ou ψ (déduit). C'est une baseline naturelle face à un
autoencodeur embarqué pour la détection de défauts sur features vibratoires, mais il ne s'adapte pas
à la dérive sans réentraînement (déduit).

## Gaps identifiés

- iForest en flux, avec mise à jour incrémentale sous dérive : non traité ici.
- Empreinte mémoire d'un iForest réduit (t, ψ) sur MCU pour la PdM.
- Comparaison iForest / autoencodeur / Mahalanobis sur features de vibration.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Table 2 reconstruite par PyMuPDF ; colonnes de temps de
la Table 3 en partie désalignées ; §3 (exemple de la Fig. 4) tronqué ; figures non disponibles.
Déduit et non affirmé par les auteurs : empreinte mémoire sur MCU, limites des partitions alignées
sur les axes, absence de mise à jour en flux.
