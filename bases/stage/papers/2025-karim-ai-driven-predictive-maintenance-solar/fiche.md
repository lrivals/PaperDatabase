---
id: 2025-karim-ai-driven-predictive-maintenance-solar
fiche: done
date: 2026-09-29
benchmarks: none
---

# AI-Driven Predictive Maintenance for Solar Inverter Systems

Md Asif Karim, 2025, TechRxiv preprint. https://doi.org/10.36227/techrxiv.175977633.34528041/v1
Type : preprint non relu par les pairs (TechRxiv)

## Problème

Les onduleurs sont les composants les plus défaillants des installations photovoltaïques (plus de
la moitié des interventions non planifiées, selon les références citées) ; leur surveillance repose
sur des alarmes à seuil, réactives. L'auteur veut un cadre de maintenance prédictive : détection de
défauts, détection d'anomalies et prédiction de RUL (§I-A, §I-B).

## Méthode

Cadre en trois couches (§III, Fig. 1-3) :

- **Modélisation physique** sous MATLAB/Simulink : panneau à modèle à une diode, convertisseur
  élévateur avec MPPT Perturb & Observe, onduleur à pont IGBT en SPWM, modèle thermique ; défauts
  simulés (vieillissement de condensateur, dégradation ou court-circuit d'IGBT, surchauffe, circuit
  ouvert) (§III-B).
- **Prétraitement** : filtrage (moyenne glissante, ondelettes), normalisation, fenêtrage ; features
  statistiques, fréquentielles (harmoniques, entropie spectrale) et temps-fréquence (énergie de
  paquets d'ondelettes, STFT) (§III-C, Table 1).
- **Modèles** : SVM, forêts aléatoires, gradient boosting et CNN pour la classification ;
  autoencodeur et OC-SVM pour les anomalies ; LSTM et GRU pour la RUL (§III-D).
- Validation annoncée en trois étapes : simulation, données réelles d'industriels et de sites,
  comparaison à des alarmes à seuil (§III-F).

## Plateforme et implémentation

MATLAB/Simulink et bibliothèques Python (§I-C). Aucun matériel, aucune mesure de coût. Code et
données : non publiés.

## Résultats

Uniquement **qualitatifs** (§IV) : CNN > RF > SVM en classification ; autoencodeur > OC-SVM en
détection d'anomalies ; LSTM a la RMSE la plus basse en RUL, GRU plus rapide et « attractive for
deployment in embedded hardware ». Seul chiffre extrait : SVM 82 % en détection de défauts, dans
une Table 2 tronquée. Aucune ligne dans `benchmarks.csv` : pas de valeur exploitable ni de protocole
décrit (`benchmarks: none`).

## Limites et critique

- **Aucun protocole expérimental** : ni taille des jeux, ni découpage, ni hyperparamètres, ni
  métriques chiffrées (hormis une valeur tronquée) ; les « données réelles » de validation ne sont ni
  décrites ni sourcées (§III-F).
- Résumé absent à l'extraction (remplacé par l'avertissement TechRxiv) ; numérotation des
  contributions incomplète (§I-D).
- Affirmations générales (« demonstrate the superiority ») sans support chiffré ; pas de relecture
  par les pairs.
- La phrase sur le déploiement embarqué des GRU n'est étayée par aucune mesure.

## Pertinence pour la thèse

Très faible comme source de résultats : à ne citer, au mieux, que comme exemple de domaine
d'application (onduleurs PV) de la PdM, avec la mention « preprint non relu ». Il illustre, en
creux, le manque de protocole des travaux applicatifs, qui justifie des évaluations chiffrées et
reproductibles (déduit).

## Gaps identifiés

- Jeux de données publics de défauts d'onduleurs PV : non fournis.
- Mesures embarquées (latence, mémoire) des modèles LSTM/GRU pour la RUL de composants électroniques.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Résumé non extrait ; Table 2 tronquée après la première
ligne ; figures non disponibles.
Déduit et non affirmé par l'auteur : faiblesse de preuve, usage limité comme référence.
