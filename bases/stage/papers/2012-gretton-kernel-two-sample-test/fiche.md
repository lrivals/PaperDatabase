---
id: 2012-gretton-kernel-two-sample-test
fiche: done
date: 2026-09-29
benchmarks: none
---

# A Kernel Two-Sample Test

Arthur Gretton, Karsten M. Borgwardt, Malte J. Rasch, Bernhard Schölkopf, Alexander Smola, 2012, Journal of Machine Learning Research 13. https://jmlr.org/papers/v13/gretton12a.html
Type : article de journal

## Problème

Décider, à partir de deux échantillons X ~ p et Y ~ q, si p = q (test à deux échantillons), en
multivarié, en grande dimension avec peu d'échantillons, et même sur des données structurées
(graphes), sans passer par une estimation de densité (§1, §3).

## Méthode

- **MMD (Maximum Mean Discrepancy)** : MMD[F, p, q] = sup_{f∈F} (E_p f − E_q f) (Déf. 2). Quand F
  est la boule unité d'un RKHS, MMD² = ‖μ_p − μ_q‖²_H, distance entre les **plongements moyens**
  des distributions (Lemme 4) ; pour un noyau universel ou caractéristique (gaussien, Laplace),
  MMD = 0 ⟺ p = q (Th. 5).
- Estimateurs : non biaisé MMD²_u (somme de U-statistiques, Eq. 3-4) et biaisé MMD_b (Eq. 5),
  en O((m + n)²) ; fonction témoin f*(t) ∝ moyenne de k(xᵢ, t) − moyenne de k(yⱼ, t) (§2.3).
- **Trois tests** :
  - deux tests **sans hypothèse de distribution** fondés sur des bornes de grandes déviations
    (McDiarmid sur MMD_b, Cor. 9 ; Hoeffding sur MMD²_u, Cor. 11), conservateurs (§4) ;
  - un test **asymptotique** sur MMD²_u, dont la loi nulle est une somme pondérée de χ² ; seuil
    par bootstrap ou par ajustement de courbes de Pearson sur les moments (§5, Th. 12-13).
- **Statistique linéaire** MMD²_l : moyenne de h sur des paires disjointes, O(m) en temps et
  **O(1) en mémoire**, asymptotiquement gaussienne, adaptée aux flux (§6, Lemme 14).
- Liens : Kolmogorov-Smirnov et Earth-Mover (Wasserstein) sont des MMD pour d'autres classes de
  fonctions (§7.2) ; HSIC (indépendance) et détection d'outliers sont des cas voisins (§7.4, §7.6).
- Largeur du noyau gaussien : heuristique de la médiane des distances (§8).

## Plateforme et implémentation

Implémentation Matlab publiée (www.gatsby.ucl.ac.uk/~gretton/mmd/mmd.htm, §1). Pas d'évaluation
embarquée ; coûts en temps de calcul relatifs (Fig. 6).

## Résultats

- Gaussiennes en dimension jusqu'à 2500, 250 échantillons : MMD²_u (Pearson) égale le t-test en
  basse dimension et le surpasse en haute dimension ; la statistique linéaire reste compétitive
  (§8.1, Fig. 5).
- Intégration de données (Table 1) : sur des jeux de grande dimension et petite taille (puces à ADN
  de 12 600 dimensions pour 25 échantillons), les tests asymptotiques rejettent à tort p = q dans
  ≈ 5 % des cas (niveau nominal) et acceptent à tort p = q dans 0 à 3,4 % des cas ; les tests par
  bornes sont trop conservateurs.
- Appariement d'attributs de bases de données par méthode hongroise sur MMD : 90 à 100 % de
  correspondances correctes, y compris sur graphes de protéines (Table 3).
- À gros volume, la statistique linéaire atteint une erreur de type II donnée à moindre coût que
  le test quadratique, en regardant plus de données (§8.3, Fig. 6).

→ aucune ligne dans `benchmarks.csv` : référence de méthode statistique (test d'hypothèse), sans
modèle d'apprentissage ni configuration comparable aux autres lignes (`benchmarks: none`).

## Limites et critique

- Coût quadratique du test principal ; la version linéaire perd en puissance à taille égale.
- Choix du noyau (largeur) par heuristique ; l'effet d'un noyau choisi sur l'échantillon testé
  sur la loi nulle n'est pas entièrement analysé (§8, Annexe C).
- Test « à deux échantillons » par lots : il ne dit pas **quand** la distribution a changé ;
  l'appliquer en ligne demande des fenêtres, avec leurs propres compromis (déduit).
- Les tests par bornes, rigoureux, sont souvent inutilisables en pratique (trop conservateurs).

## Pertinence pour la thèse

Référence de méthode pour la détection de dérive non supervisée : comparer une fenêtre récente de
features capteurs à une fenêtre de référence par MMD détecte des changements de distribution
multivariés que les tests univariés (KS par dimension, comme KSWIN) manquent. La statistique
linéaire en O(1) de mémoire (§6) est la variante réaliste sur MCU, avec un noyau gaussien calculé
en virgule fixe (déduit). Le lien MMD ↔ KS ↔ Wasserstein (§7.2) permet de situer les détecteurs de
la base dans un même cadre.

## Gaps identifiés

- MMD linéaire en flux sur MCU (coût du noyau, précision INT8) comme déclencheur de mise à jour :
  non évalué.
- Choix en ligne de la largeur du noyau sous dérive.
- Comparaison MMD / KSWIN / Page-Hinkley sur séries de vibrations.

## Statut de lecture

Papier complet, annexes de preuves comprises (`fulltext.md` lu en entier). Plusieurs équations et
passages de preuve fragmentés à l'extraction ; Tables 1-3 lisibles ; figures non disponibles.
Déduit et non affirmé par les auteurs : usage en fenêtres glissantes, implémentation MCU.
