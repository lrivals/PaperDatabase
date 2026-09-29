---
id: 1936-mahalanobis-generalised-distance-statistics
fiche: done
date: 2026-09-29
benchmarks: none
---

# On the Generalised Distance in Statistics

P. C. Mahalanobis, 1936, Proceedings of the National Institute of Sciences of India 2(1), 49-55. Réimpression : Sankhyā A 80 (2018), S1-S7, https://doi.org/10.1007/s13171-019-00164-5
Type : article de journal (texte original de 1936, lu dans la réimpression de 2018)

## Problème

Mesurer la « distance » entre deux populations statistiques normales à P variables corrélées, de
façon à pouvoir comparer des populations (l'auteur l'avait déjà fait en 1930 pour des variables
indépendantes, réf. Journ. Asiat. Soc. Bengal) (§1-2).

## Méthode

Ce que l'article **définit** :

- **Population normale à P variables** décrite par ses P moyennes et sa matrice de dispersion
  (variances et corrélations), soit P(P+1)/2 paramètres de dispersion (§1).
- **Champ statistique** : à chaque point, un jeu de paramètres qui définit une population (un
  « nuage de densité ») (§2).
- **Statistique Δ² généralisée** : pour deux populations de **même dispersion**, distance entre
  leurs moyennes pondérée par l'**inverse de la matrice de dispersion commune**, ce qui généralise
  au cas corrélé la formule pour variables indépendantes (§2, Eq. 2.5-2.7). C'est ce que l'on
  appelle aujourd'hui la distance de Mahalanobis (dénomination moderne, pas dans le texte).
- Analogie formelle : P·Δ² joue le rôle de ds² en relativité restreinte, et la matrice de
  dispersion celui du tenseur métrique ; passer à des variables indépendantes équivaut à passer en
  coordonnées galiléennes (§2-3).
- **Estimation sur échantillons** (§4) :
  - dispersion supposée connue (poolée sur de nombreux échantillons) : statistique D² corrigée
    pour que son espérance soit Δ² ; moments donnés, loi exacte obtenue par R. C. Bose (fonction de
    Bessel d'argument imaginaire), tables de seuils à 5 et 1 % annoncées ;
  - dispersion et moyennes toutes deux estimées : loi exacte inconnue, moments exacts de Bose en
    annexe (cas indépendant).
- **Champ généralisé** où la dispersion varie avec la moyenne : Δ² reste un élément de ligne
  différentiel dont l'intégrale dépend du chemin ; distribution « under investigation » (§5).
- Annexe : autre approche esquissée (superposer deux populations par translation, compression et
  rotation) (Annexe).

## Plateforme et implémentation

Sans objet (article théorique). Travail du Statistical Laboratory, Presidency College, Calcutta.

## Résultats

Résultats théoriques : définition de Δ², estimateur sans biais D², ses moments et, via Bose, sa loi
exacte quand la dispersion est connue (§4). Aucune ligne dans `benchmarks.csv` (référence de
méthode statistique, conformément au profil de la base, `benchmarks: none`).

## Limites et critique

- Suppose des populations **normales** ; le cas de dispersions différentes n'est qu'esquissé (§5).
- La loi exacte avec dispersion estimée reste inconnue dans l'article (§4).
- **Formules non disponibles** dans le texte extrait (OCR sans décodage des équations) : la forme
  exacte de Δ² ci-dessus est décrite en mots d'après le texte, pas recopiée ; à vérifier dans le
  PDF avant toute citation d'équation.

## Pertinence pour la thèse

Référence fondatrice citée dans la bibliographie du stage : la distance de Mahalanobis sert de
score d'anomalie (écart d'une observation à la moyenne d'un régime normal, pondéré par la
covariance) et de classifieur par distance (utilisée par Helwig 2015 après une LDA, dans la base).
Sur MCU, elle ne demande qu'un vecteur moyen et une matrice de covariance inverse (P² valeurs pour P
features), et peut se mettre à jour en ligne ; c'est une baseline naturelle de détection
d'anomalies ou de dérive face à un autoencodeur (déduit). Le cas « dispersion qui varie avec la
moyenne » (§5) évoque les régimes de fonctionnement multiples d'une machine (déduit).

## Gaps identifiés

- Distance de Mahalanobis avec covariance mise à jour en ligne sous dérive, en précision réduite
  sur MCU.
- Comparaison Mahalanobis / autoencodeur / Isolation Forest sur features vibratoires.

## Statut de lecture

Papier complet lu, mais sur un texte **OCR** (Docling + RapidOCR, 29/09/2026) : nombreuses fautes de
reconnaissance, équations non décodées, numéros des §2 à 4 perdus puis reconstitués. Trace brute
dans `ocr_docling.json`.
Déduit et non affirmé par l'auteur : dénomination « distance de Mahalanobis », usages en détection
d'anomalies et sur MCU.
