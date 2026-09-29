---
id: 2019-su-robust-anomaly-detection-multivariate-time
fiche: done
date: 2026-09-29
---

# Robust Anomaly Detection for Multivariate Time Series through Stochastic Recurrent Neural Network

Ya Su, Youjian Zhao, Chenhao Niu, Rong Liu, Wei Sun, Dan Pei, 2019, Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining 2828–2837. https://doi.org/10.1145/3292500.3330672
Type : conférence (KDD 2019)

## Problème

Les équipements industriels (serveurs, engins spatiaux, moteurs) sont surveillés par des séries
temporelles multivariées ; leurs anomalies doivent être détectées au niveau de l'entité, sans
labels, alors que ces séries sont à la fois **stochastiques** et **fortement dépendantes dans le
temps**. Les méthodes existantes sont soit déterministes (LSTM-NDT, EncDec-AD), soit stochastiques
sans dépendance temporelle (DAGMM, LSTM-VAE) (§1, §2).

## Méthode

**OmniAnomaly** : réseau récurrent stochastique qui apprend les motifs normaux et détecte par
probabilité de reconstruction (§3-4) :

- **qnet** : GRU sur la fenêtre x_{t−T:t} ; la variable latente z_t dépend de l'état GRU e_t **et
  de z_{t−1}** (connexion des variables stochastiques) ; posterior rendu non gaussien par un
  **planar normalizing flow** de longueur 20 (Eq. 3) ;
- **pnet** : z_t reliés par un modèle d'état linéaire gaussien, puis GRU et couche dense pour
  reconstruire x_t (Eq. 4) ; entraînement par ELBO (Eq. 5).
- **Score** S_t = log p(x_t | z_{t−T:t}) ; anomalie si S_t sous un seuil fixé automatiquement par
  **Peaks-Over-Threshold** (théorie des valeurs extrêmes, loi de Pareto généralisée ajustée sur la
  queue basse des scores) (§4.3-4.4, Eq. 6-7).
- **Interprétation** : le score se décompose par dimension ; les dimensions de plus faible
  probabilité de reconstruction expliquent l'anomalie (§4.5, Eq. 8).
- Évaluation : SMAP et MSL (NASA) et SMD (serveurs, 28 machines × 38 métriques, 5 semaines, publié) ;
  précision, rappel, F1 avec **point-adjust** (un segment d'anomalie est compté détecté si un seul de
  ses points l'est) (§5.1, Annexe A).

## Plateforme et implémentation

GPU NVIDIA GTX 1080 Ti ; 48, 11 et 87 min par époque (SMAP, MSL, SMD) (Annexe B). Fenêtre de 100 pas,
GRU et couches denses de 500 unités, latent de dimension 3 (Annexe B). Aucune implémentation
embarquée. Code et jeu SMD publiés sur GitHub (§1).

## Résultats

- F1 global (union des trois jeux) : **0,86**, soit +0,09 sur la meilleure baseline (LSTM-NDT)
  (Abstract, §5.2.1) ; F1_best 0,8871 contre 0,8012 (§5.2.1).
- F1 avec seuil POT (Table 3) : SMAP 0,8434 ; MSL 0,8989 ; SMD 0,8857 (F1_best 0,8535 ; 0,9014 ;
  0,9620).
- Précision et rappel > 0,74 sur les trois jeux, seul modèle dans ce cas (§5.2.1 ; Table 2 absente
  de l'extraction).
- Ablations : GRU > LSTM > RNN ; connexion des z et planar NF améliorent F1_best, peu sur MSL
  (§5.2.2, Fig. 5).
- Interprétation sur SMD : HitRate@100 % = 0,80 et HitRate@150 % = 0,89, contre 0,50 et 0,62 pour
  LSTM-VAE (§5.2.3).

→ reportés dans `benchmarks.csv` : 3 lignes (F1 avec seuil POT sur SMAP, MSL et SMD, Table 3),
`medium` (Table 3 reconstruite par PyMuPDF, recoupée avec le texte).

## Limites et critique

- **Point-adjust** : il gonfle fortement les scores (une seule détection valide tout un segment),
  ce qui rend ces F1 non comparables aux évaluations point par point (déduit ; limite largement
  relevée depuis dans la littérature).
- Modèle lourd (GRU 500 unités, flow de longueur 20), entraîné des dizaines de minutes par époque
  sur GPU : inadapté à un MCU en l'état (déduit).
- Seuil POT et modèle appris hors ligne, réentraînés « une fois par semaine ou par mois » (§3.1) :
  pas d'adaptation en ligne à la dérive.
- Table 2 (précision, rappel, F1 par méthode) absente de l'extraction.

## Pertinence pour la thèse

Référence de détection d'anomalies non supervisée sur séries temporelles multivariées de capteurs,
avec deux idées transposables : le seuil automatique par POT (EVT), léger et utilisable sur MCU pour
fixer le seuil d'une erreur de reconstruction, et l'interprétation par dimension (quel capteur
explique l'alarme). Le modèle lui-même est hors budget MCU ; un autoencodeur réduit ou TinyOL
(dans la base) sont les équivalents embarqués (déduit). Jeux SMAP/MSL/SMD utiles comme benchmarks
d'anomalies multivariées.

## Gaps identifiés

- Version embarquée (quantifiée, réduite) d'un détecteur récurrent stochastique sur MCU.
- Mise à jour en ligne du modèle et du seuil POT sous dérive (le papier réentraîne hors ligne).
- Évaluation sans point-adjust sur séries de PdM.

## Statut de lecture

Papier complet, annexes comprises (`fulltext.md` lu en entier). Table 2 absente ; Table 3
reconstruite par PyMuPDF ; équations 3a et une partie de §4.1 tronquées ; figures non disponibles.
Auteurs, venue et DOI repris des métadonnées (non contrôlés dans le texte extrait, qui n'a pas
d'en-tête).
Déduit et non affirmé par les auteurs : effet du point-adjust, inadéquation MCU.
