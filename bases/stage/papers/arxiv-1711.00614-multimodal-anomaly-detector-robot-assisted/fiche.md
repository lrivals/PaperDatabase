---
id: arxiv-1711.00614-multimodal-anomaly-detector-robot-assisted
fiche: done
date: 2026-09-29
---

# A Multimodal Anomaly Detector for Robot-Assisted Feeding Using an LSTM-based Variational Autoencoder

Daehyung Park, Yuuna Hoshi, Charles C Kemp, 2017, arXiv preprint. https://arxiv.org/abs/1711.00614
Type : preprint non relu par les pairs (version arXiv)

## Problème

Un robot d'assistance (ici pour nourrir une personne) doit détecter en ligne les exécutions
anormales à partir de signaux multimodaux hétérogènes (son, force, couples articulaires, positions).
Les approches existantes réduisent la dimension ou choisissent des features à la main, au risque de
perdre l'information utile (§I).

## Méthode

**LSTM-VAE** (§III) : VAE dont l'encodeur et le décodeur sont des LSTM (état conservé sur toute
l'exécution, pas de fenêtre glissante) :

- entraînement sur des exécutions **normales seules**, avec un critère **débruitant** (entrée
  bruitée par un bruit gaussien) (Eq. 2) ;
- **prior dépendant de la progression** : le centre de la gaussienne a priori se déplace linéairement
  de p₁ à p_T au fil de la tâche (Eq. 3, Fig. 3) ;
- décodeur produisant moyenne et covariance diagonale de la reconstruction ; latent de dimension 3
  (§III-C).
- **Score** = −log p(x_t ; μ_x, Σ_x), log-vraisemblance négative de l'observation (Eq. 6).
- **Seuil dépendant de l'état** : une SVR (noyau RBF) apprend, sur la validation, le score attendu
  en fonction de l'état latent z ; seuil η = f̂(z) + c (§IV-B).
- Données : robot PR2, 17 signaux (énergie sonore, force 3D, couples de 7 articulations, position de
  la cuillère et de la bouche) rééchantillonnés à 20 Hz ; 1555 exécutions de 24 participants, dont
  352 (160 anormales, 12 types d'anomalies) pour l'entraînement et le test, et 1203 normales pour le
  pré-entraînement ; validation croisée en laissant un participant de côté (§V).

## Plateforme et implémentation

Keras (LSTM avec état), Adam, taux 0,001 (§III-C). Exécution sur le PC du robot, détection à 20 Hz
(§V-D) ; matériel de calcul, latence et mémoire : n/r. Code : non publié.

## Résultats

AUC (Table I) :

| Entrées | Aléatoire | OSVM | HMM-GP | AE | EncDec-AD | LSTM-VAE |
|---|---|---|---|---|---|---|
| 4 features choisies | 0,512 | 0,743 | 0,812 | 0,812 | 0,800 | **0,856** |
| 17 signaux bruts (+ pré-entraînement) | 0,505 | 0,738 | N/A | 0,801 | 0,808 | **0,871** |

- Avec 17 signaux bruts, l'AUC est supérieure à celle obtenue avec les features choisies à la main
  (§VI).
- Le seuil dépendant de l'état donne plus de vrais positifs à taux de faux positifs égal qu'un
  seuil fixe (Fig. 8).

→ reportés dans `benchmarks.csv` : 2 lignes (LSTM-VAE, AUC avec 17 signaux et avec 4 features,
Table I), `high`.

## Limites et critique

- Une seule tâche, un seul robot, anomalies en partie provoquées sur consigne (§V-C) : validité
  hors laboratoire non démontrée.
- Métrique unique (AUC) : pas de délai de détection ni de taux de fausses alarmes à un point de
  fonctionnement donné, alors que la détection en ligne est l'objectif.
- Le texte attribue le second rang (écart de 0,044) à HMM-GP, alors que la Table I place l'AE à
  égalité ou légèrement devant (0,8123 contre 0,8121).
- Prior de progression : suppose une tâche de durée normalisée, avec un début et une fin connus,
  ce qui ne se transpose pas à une surveillance continue de machine (déduit).
- Coût d'inférence non rapporté.

## Pertinence pour la thèse

Référence de détection d'anomalies multicapteurs par reconstruction probabiliste, souvent citée
comme baseline (LSTM-VAE, repris par OmniAnomaly, Su 2019). Deux idées utiles pour la PdM : un
**seuil conditionné par l'état** (le score attendu varie selon le régime de fonctionnement), qui
limite les fausses alarmes sous changement de régime, et la fusion de capteurs bruts sans
ingénierie de features. Sur MCU, un LSTM-VAE est coûteux ; un seuil adaptatif par régime peut en
revanche accompagner un autoencodeur léger (déduit).

## Gaps identifiés

- Seuil adaptatif par régime pour la détection d'anomalies en PdM embarquée : non évalué.
- Détection en surveillance continue (sans début ni fin de tâche) avec LSTM-VAE.
- Coût embarqué d'un détecteur récurrent probabiliste.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Conclusion tronquée à l'extraction ; algorithmes en
fragments ; Table I lisible ; figures non disponibles.
Déduit et non affirmé par les auteurs : limites du prior de progression, transposition MCU.
