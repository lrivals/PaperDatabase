---
id: 2021-kang-remaining-useful-life-rul-prediction
fiche: done
date: 2026-09-29
---

# Remaining Useful Life (RUL) Prediction of Equipment in Production Lines Using Artificial Neural Networks

Ziqiu Kang, Cagatay Catal, Bedir Tekinerdogan, 2021, Sensors. https://doi.org/10.3390/s21030932
Type : article de journal

## Problème

Prédire la RUL d'équipements de ligne de production pour planifier la maintenance, avec des
méthodes plus légères que l'apprentissage profond, qui demande beaucoup de données, un réglage
d'hyperparamètres lourd et un coût de calcul élevé (§1, §2).

## Méthode

- **Données** : C-MAPSS (NASA), sous-jeux FD001 à FD004 (1 ou 6 conditions, 1 ou 2 modes de défaut)
  (§3, Table 1).
- **Prétraitement** : suppression des variables constantes, normalisation (z-score ou min-max, la
  meilleure étant retenue), **PCA** avec autant de composantes que de features (§4.1).
- **Indice de santé (HI) interpolé** : les N premiers cycles de chaque moteur reçoivent HI = 1 et les
  N derniers HI = 0 ; une régression linéaire interpole les autres points ; un second modèle (MLP,
  RF, SVR ou LR) est réentraîné sur tout le jeu étiqueté (§4, §4.2-4.3).
- **RUL** : un polynôme d'ordre 2 est ajusté aux HI prédits d'un moteur de test ; son intersection
  avec l'axe des cycles donne le cycle de panne, d'où la RUL (Eq. 3-5, Fig. 7).
- **MLP** : 24-20-5-1, tanh, Adam, taux 3·10⁻⁵ (Table 4) ; RF à 100 arbres de profondeur 6, SVR RBF
  (γ = 0,1) choisis par grid search (§4.2) ; validation croisée à 5 plis, arrêt précoce.

## Plateforme et implémentation

Matériel n/r (PC). Aucune implémentation embarquée ; précision numérique n/r. Code : non publié.

## Résultats

MSE de RUL sur les jeux de test (cycles², plus bas = mieux), Table 5 :

| Modèle | FD001 | FD002 | FD003 | FD004 |
|---|---|---|---|---|
| LR | 668 | 1031 | 1332 | 2181 |
| LR + PCA | 558 | 748 | 1387 | 1904 |
| **MLP + PCA** | **509** | **746** | n/r (cellule vide) | **1427** |
| RF + PCA | 701 | 857 | 1895 | 1994 |
| SVR + PCA | 800 | 776 | 1089 | 1575 |

- MLP + PCA donne les plus faibles MSE, mais n'est pas nettement meilleur que LR + PCA (§6.1).
- MSE plus faible pour les moteurs de test de plus de 100 cycles (par exemple 499 contre 668 pour LR
  sur FD001) : les séries courtes donnent de mauvaises extrapolations (§5, Fig. 13-14).
- Les jeux à deux modes de défaut (FD003, FD004) sont les plus difficiles (§6.1).

→ reportés dans `benchmarks.csv` : 3 lignes (MLP + PCA, MSE de RUL sur FD001, FD002 et FD004,
Table 5), `medium` (sous-tableaux non étiquetés à l'extraction, attribution (C) = MLP déduite de
l'ordre de la légende).

## Limites et critique

- **Affirmation erronée** : « the RUL was not provided in training datasets » (§1, §4) ; or les
  moteurs d'entraînement de C-MAPSS vont jusqu'à la panne, donc la RUL de chaque cycle est connue
  (déduit) ; tout l'échafaudage HI/interpolation contourne un problème qui n'existe pas.
- MSE de 509 sur FD001, soit une RMSE ≈ 22,6 cycles (calcul déduit), nettement moins bonne que les
  RMSE de 12 à 16 couramment publiées ; les auteurs ne se comparent **à aucune méthode de la
  littérature** (§6.1).
- Pas de score asymétrique C-MAPSS ; métrique MSE seulement.
- Tableau de résultats incomplet (FD003 manquant pour MLP) ; texte fortement dupliqué dans la
  version extraite (version de relecture « FOR PEER REVIEW » mêlée).
- « Production lines » dans le titre, mais aucune donnée de ligne de production : uniquement des
  turboréacteurs simulés.

## Pertinence pour la thèse

Faible comme référence de performance, utile comme exemple de chaîne légère (PCA + petit MLP de
≈ 600 paramètres, calcul déduit de la Table 4) pour la RUL sur C-MAPSS, compatible avec un MCU. Il
illustre l'effet des conditions opératoires multiples (FD002/FD004) sur la difficulté, cas où
l'apprentissage continu par condition est pertinent (déduit). À citer avec précaution, compte tenu
des limites méthodologiques.

## Gaps identifiés

- Comparaison des approches légères (PCA + MLP) avec l'état de l'art sur C-MAPSS, avec le score
  asymétrique.
- RUL par modèle léger embarqué, avec adaptation par condition opératoire.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Texte en grande partie dupliqué (fusion d'une version de
relecture) ; Tables 2-3 sans corps ; sous-tableaux de la Table 5 non étiquetés pour (C) ; une cellule
manquante ; figures non disponibles.
Déduit et non affirmé par les auteurs : erreur sur l'absence de RUL, RMSE équivalente, nombre de
paramètres du MLP.
