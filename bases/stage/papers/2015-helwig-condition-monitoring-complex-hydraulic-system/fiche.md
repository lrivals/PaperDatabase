---
id: 2015-helwig-condition-monitoring-complex-hydraulic-system
fiche: done
date: 2026-09-29
benchmarks: none
---

# Condition monitoring of a complex hydraulic system using multivariate statistics

Nikolai Helwig, Eliseo Pignanelli, Andreas Schütze, 2015, 2015 IEEE International Instrumentation and Measurement Technology Conference (I2MTC) Proceedings 210-215. https://doi.org/10.1109/I2MTC.2015.7151267
Type : conférence (I2MTC 2015) — article de banc d'essai et de jeu de données

## Problème

L'analyse vibratoire, efficace pour les machines tournantes, ne suffit pas pour les systèmes
hydrauliques (fuite de pompe, fuite d'accumulateur…), qu'il faut diagnostiquer à partir des capteurs
de procédé. Les auteurs veulent une chaîne d'apprentissage **automatique** (extraction et sélection
de features, classification) facilement transposable à d'autres systèmes (§I).

## Méthode

Ce que l'article **définit** :

- **Banc hydraulique** à défauts **réversibles** : circuit de travail (pompe principale de 3,3 kW,
  charge par limiteur de pression proportionnel) et circuit de refroidissement-filtration (§III,
  Fig. 2).
- **Capteurs** : pression PS1-PS6, débit FS1-FS2, température TS1-TS5, puissance électrique EPS1,
  vibration VS1, contamination particulaire et paramètres d'huile ; de 100 Hz (pression) à 1 Hz
  (température) ; plus des **capteurs virtuels** (rendement de refroidissement, puissance de
  refroidissement, rendement système) (§III).
- **Quatre défauts simulés avec plusieurs niveaux de gravité**, combinés entre eux (Table I) :
  refroidisseur (puissance 0,6-2,2 kW), valve (courant de commande), fuite interne de pompe
  (orifices de dérivation), fuite de gaz des accumulateurs (pressions de précharge 90 à 115 bar).
- **Cycle de travail de 60 s** en 13 intervalles, **fixe** ou à charges **pseudo-aléatoires**
  (120-140 bar) (§IV, Fig. 3).
- **Chaîne d'analyse** : 1323 features temporelles et 1197 fréquentielles par cycle (médiane,
  variance, pente, position du maximum, asymétrie, aplatissement par capteur et par intervalle) ;
  sélection des 20 features les plus corrélées au défaut (Pearson ou Spearman) ; **LDA** puis
  classifieur par **distance de Mahalanobis** ; validation LOOCV (§II, §IV) ; Matlab R2012.

## Plateforme et implémentation

Banc instrumenté, automate Beckhoff CX5020, transfert EtherCAT vers un PC, pilotage des scénarios
sous LabVIEW (§III). Analyse hors ligne sous Matlab. Pas d'implémentation embarquée du diagnostic.

## Résultats

Taux de classification (%) avec 20 features temporelles, LDA + Mahalanobis (Table III) :

| Composant | Cycle fixe | Cycle pseudo-aléatoire |
|---|---|---|
| Refroidisseur | 100 | 100 |
| Valve | 100 | 100 |
| Pompe (fuite interne) | 97,9 | 72,3-73,6 |
| Accumulateur (fuite de gaz) | 88,8-90,4 | ≈ 54 |

- Features fréquentielles moins robustes aux charges aléatoires (valve 49-61 %) (Table III).
- ANN et SVM ne font pas mieux en cycle aléatoire (moyennes 81-83 %) (Table IV).
- Features de distribution sur une fenêtre de plusieurs cycles (1 à 60) : **+25 %** pour la pompe et
  **+40 %** pour l'accumulateur (§IV, Fig. 4-5).

Pas de ligne dans `benchmarks.csv`, conformément au profil pour les papiers de jeux de données : la
fiche décrit le banc et les données (`benchmarks: none`).

## Limites et critique

- Défauts simulés sur un banc (réversibles, contrôlés), pas de dégradation naturelle.
- Validation LOOCV sur des cycles successifs d'un même essai : cycles fortement corrélés, donc
  estimation probablement optimiste (déduit).
- Le jeu de données n'est pas décrit comme publié dans cet article ; sa diffusion publique (dépôt
  UCI « Condition monitoring of hydraulic systems ») est postérieure (à vérifier).
- Pas de pronostic (RUL) : diagnostic de l'état et de la gravité uniquement.

## Pertinence pour la thèse

Article de référence d'un jeu **multicapteurs de procédé** (pression, débit, température, puissance)
avec défauts combinés et niveaux de gravité : complément utile aux jeux vibratoires (PRONOSTIA,
Paderborn). Les changements de charge (cycle fixe vs aléatoire) constituent une dérive de régime
bien identifiée, exploitable comme scénario d'adaptation ou de CL (déduit). La chaîne LDA +
Mahalanobis est une baseline légère, embarquable sur MCU, face à laquelle situer un réseau appris
en continu (déduit) ; elle illustre l'usage direct de la distance de Mahalanobis (1936, dans la
base).

## Gaps identifiés

- Robustesse du diagnostic aux changements de régime de charge : fortement dégradée pour la pompe et
  l'accumulateur (Table III).
- Adaptation en ligne du diagnostic lors de l'ajout d'un nouveau défaut (annoncée en §V, non
  évaluée).

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Table III reconstruite par PyMuPDF (en double à
l'extraction) ; la numérotation des sections est perturbée (§IV fusionnée avec §III) ; figures non
disponibles.
Déduit et non affirmé par les auteurs : corrélation des cycles en LOOCV, usage en scénario de dérive,
diffusion ultérieure du jeu.
