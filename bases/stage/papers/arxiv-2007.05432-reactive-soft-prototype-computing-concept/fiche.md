---
id: arxiv-2007.05432-reactive-soft-prototype-computing-concept
fiche: done
date: 2026-09-29
---

# Reactive Soft Prototype Computing for Concept Drift Streams

Christoph Raab, Moritz Heusinger, Frank-Michael Schleif, 2020, Neurocomputing 416. https://doi.org/10.1016/j.neucom.2019.11.111
Type : article de journal

> Axe « quantization » retiré à la fiche : il avait été déduit à l'ingestion de « Learning *Vector
> Quantization* », qui désigne ici une famille de classifieurs à prototypes, pas la quantification des
> poids.

## Problème

Dans les flux non stationnaires, les classifieurs doivent détecter la dérive et s'adapter vite sans
perdre en stabilité ; les détecteurs usuels (ADWIN, DDM, EDDM) surveillent la performance et
réagissent peu, et les stratégies d'adaptation par prototypes supposent toutes les classes
présentes dans le lot récent (§1, §2).

## Méthode

**RRSLVQ** (Reactive Robust Soft Learning Vector Quantization) = détecteur **KSWIN** + adaptation
des prototypes d'un RSLVQ (§4, Alg. 1) :

- **KSWIN** (§4.1) : fenêtre glissante Ψ de n = 300 points ; fenêtre R des r = 30 plus récents et
  fenêtre W de 30 points tirés uniformément dans le reste ; **test de Kolmogorov-Smirnov par
  dimension**, dérive si sup|F_W − F_R| > √(−ln α / r) (Eq. 4-5) ; α corrigé par Bonferroni-Dunn :
  α* = 0,05/60 ≈ 0,0001. Surveille p(X), donc la dérive « virtuelle » aussi, sans labels.
- **RSLVQ** (§4.2) : prototypes gaussiens (variance commune σ), mise à jour en ligne par gradient
  à momentum de type Adadelta (Eq. 9-12) ; prédiction = prototype le plus proche (Eq. 13).
- **Adaptation** (§4.3) : à chaque détection, tous les prototypes sont remplacés par la moyenne
  de R (sans tenir compte des classes), puis réentraînés sur les points étiquetés de R ;
  robuste aux classes absentes.
- **Stabilité** (§4.4, Lemme 4.2) : sous une hypothèse de proportionnalité des priors entre
  concepts, le modèle réadapté sur R a un risque au plus égal à celui de l'ancien modèle, donc
  les faux positifs de KSWIN « ne nuisent pas ».
- Complexité : O(m) par pas sans dérive, O(r·m) à la dérive ; mémoire O(d·(m + n)) flottants
  (§4.5).
- Protocole : 8 générateurs synthétiques (SEA, MIXED, RTG, RBF, HYPER) dont des versions à dérive
  **récurrente fréquente**, et 6 flux réels (COVTYPE, ELEC, POKER, GMSC, AIR, SQRE) ; précision
  « interleaved test-then-train » sur 10⁶ échantillons ; scikit-multiflow (§5.1).

## Plateforme et implémentation

PC (matériel n/r) ; implémentation dans scikit-multiflow (KSWIN y est intégré, d'après l'usage du
framework, §4.3, §5). Mémoire et temps mesurés en Python (Fig. 6-7), constants pendant la dérive
pour les variantes RSLVQ. Précision numérique : float. Aucune implémentation embarquée ; les
auteurs recommandent de borner d·(m + 300) à la capacité mémoire (§4.5).

## Résultats

- **Détecteurs** (16 flux, 400 004 dérives) : KSWIN a 20 659 vrais positifs contre 71 pour
  ADWIN, 33 pour EDDM et 0 pour DDM, mais 51 040 faux positifs ; taux de détection ≈ 5 % contre
  ≈ 0,001 % (Table 2, §5.2). Associé à Naive Bayes, KSWIN a la meilleure moyenne mais n'est
  premier que sur 4 flux sur 16 (Table 3, absente de l'extraction).
- **Classifieurs**, précision moyenne (Table 4) :

| | ARF | SAMKNN | HAT | RSLVQ | RRSLVQ | OzaBagAdwin |
|---|---|---|---|---|---|---|
| Moyenne réels | 75,7 | 84,8 | 75,5 | 57,9 | 68,4 | 75,6 |
| Moyenne synthétiques | 80,8 | 86,3 | 73,0 | 69,0 | 80,7 | 81,8 |
| Moyenne globale | 79,1 | 85,8 | 73,8 | 65,3 | 74,6 | 79,7 |

- COVTYPE : 36 % (RSLVQ) → 73 % (RRSLVQ) (§5.3). RRSLVQ reste stable pendant les dérives
  récurrentes, là où les variantes Adwin-RSLVQ et Incremental-RSLVQ chutent (Fig. 5).

→ reportés dans `benchmarks.csv` : 2 lignes (RRSLVQ, précision moyenne sur flux synthétiques et
réels, Table 4), `medium` (légendes des Tables 4 et 5 inversées à l'extraction ; chiffres
recoupés avec le texte §5.3).

## Limites et critique

- KSWIN a **plus de faux positifs que de vrais positifs** ; le papier s'appuie sur le Lemme 4.2
  pour dire qu'ils ne coûtent rien, mais ce lemme repose sur une hypothèse forte
  (p₂(x) = δ·p₁(x)).
- Tests KS par dimension, sans correction de la dépendance entre dimensions ; coûteux en grande
  dimension (d tests à chaque pas).
- RRSLVQ reste nettement sous SAMKNN et sous ARF/OZA sur les flux réels (Table 4).
- Remplacer tous les prototypes à chaque détection = oubli total du concept précédent :
  inadapté aux dérives récurrentes lentes, où l'ancien concept revient (déduit).
- Texte « 81 % » attribué à RRSLVQ en moyenne globale (§5.3) alors que la Table 4 donne 74,6 %
  global et 80,7 % sur les synthétiques.

## Pertinence pour la thèse

Référence directe pour le volet **détection de dérive** : KSWIN est un détecteur non supervisé,
simple (tri et comparaison de deux fenêtres de 30 valeurs par dimension), à mémoire bornée, qui
surveille la distribution des entrées plutôt que l'erreur — adapté à un capteur sans labels.
Transposable sur MCU pour déclencher la mise à jour d'un modèle (et le recalcul de la Fisher d'un
EWC), à condition de maîtriser son taux de fausses alarmes, par exemple avec un vote sur
plusieurs fenêtres (déduit). Le schéma « détection → réinitialisation » est en revanche l'opposé
d'une stratégie anti-oubli.

## Gaps identifiés

- KSWIN sur séries de vibrations multicapteurs et sur MCU (coût d des tests, taux de fausses
  alarmes) : non évalué.
- Couplage détecteur de dérive → consolidation (EWC) plutôt que réinitialisation.
- Comparaison KSWIN vs Page-Hinkley / ADWIN sur données de pronostic.

## Statut de lecture

Papier complet, annexes comprises (`fulltext.md` lu en entier). Table 3 absente ; les légendes des
Tables 4 (précision) et 5 (kappa) sont inversées à l'extraction et la Table 5 (kappa) manque ;
début de §4.3 tronqué.
Déduit et non affirmé par les auteurs : oubli total à la réinitialisation, transposition MCU.
