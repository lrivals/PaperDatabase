---
id: arxiv-2103.08295-tinyol-tinyml-online-learning-microcontrollers
fiche: done
date: 2026-09-29
---

# TinyOL: TinyML with Online-Learning on Microcontrollers

Haoyu Ren, Darko Anicic, Thomas A. Runkler, 2021, arXiv preprint. https://arxiv.org/abs/2103.08295
Type : preprint non relu par les pairs

## Problème

Les solutions TinyML n'exécutent que l'inférence : le modèle, entraîné hors ligne puis
flashé, reste statique, alors que chaque machine diffère, que les données de terrain ne
peuvent pas être stockées ni facilement remontées, et que la distribution dérive (concept
drift) (§I).

## Méthode

- **TinyOL** : une couche supplémentaire, en RAM, ajoutée à la sortie d'un réseau figé en
  Flash (ou remplaçant sa dernière couche) ; elle apprend **en ligne, échantillon par
  échantillon**, par SGD, puis l'échantillon est jeté (§III-A, Alg. 1).
- Normalisation par moyenne et variance glissantes ; inférence puis mise à jour si un label est
  disponible ; ajout de neurones de sortie à l'arrivée d'une nouvelle classe (§III-A).
- Cas 1, *fine-tuning* : la dernière couche (sigmoïde) d'un autoencodeur de détection
  d'anomalies est réentraînée sur le terrain, cible = entrée (§III-B1, éq. 2-5).
- Cas 2, *classification multi-anomalies* : sortie de l'encodeur + erreur de reconstruction →
  couche softmax apprise en ligne, qui s'agrandit à chaque nouvelle classe (normal, stuck,
  tilted) (§III-B2, éq. 6-8).
- Implémentation C++ ; données d'un accéléromètre 3 axes fixé sur un ventilateur USB (§III-C).

## Plateforme et implémentation

- Arduino Nano 33 BLE Sense : Cortex-M4 à 64 MHz, 256 Ko de SRAM (§III-C). Puce nRF52840 :
  déduite de la carte, non écrite.
- Précision numérique : n/r (flottant vraisemblable, non dit). Mémoire occupée : n/r.
- Entraînement piloté par Bluetooth (§IV-B). Consommation : n/r.
- Code : non publié (« open source » annoncé en perspective, §V).

## Résultats

- Dérive réelle : après avoir replacé la carte sur le ventilateur, la distribution de l'erreur
  de reconstruction des données normales s'écarte de celle d'entraînement, un seuil fixe
  génère trop de fausses alarmes ; après 2000 itérations de fine-tuning en ligne, les deux
  distributions se superposent (§IV-B, Fig. 7) — qualitatif.
- Temps par itération sur 3000 échantillons (µs, moyenne / médiane / min / max) : inférence
  1748 / 1648 / 1403 / 1991 ; inférence + apprentissage en ligne 1921 / 1800 / 1404 / 3357
  (Table I) → surcoût moyen ≈ 10 % (calcul déduit).
- Classification : le macro-F1 en ligne croît avec le nombre d'échantillons ; la classe normale
  a toujours le meilleur F1 ; l'apprentissage hors ligne fait mieux au-delà de 50 époques
  (Fig. 8) — valeurs n/r.

→ reportés dans `benchmarks.csv` : 2 lignes (latence inférence et inférence + mise à jour,
Table I reconstruite par PyMuPDF, `medium`).

## Limites et critique

- Évaluation **qualitative** (histogrammes, courbes) sur un seul banc maison ; aucun F1 chiffré
  dans le texte.
- Seule la dernière couche apprend : l'encodeur figé extrait mal les features des classes
  anormales (reconnu §IV-C).
- Aucune protection contre l'oubli : l'apprentissage séquentiel classe par classe est exposé à
  l'oubli catastrophique, non mesuré (déduit).
- Pas de mesure de mémoire, d'énergie ni de précision numérique.

## Pertinence pour la thèse

Référence directe du stage : premier travail d'apprentissage en ligne sur MCU Cortex-M4,
appliqué à la surveillance vibratoire, et motivé par la dérive entre machines. Il montre la
faisabilité (≈ 1,9 ms par mise à jour) mais laisse ouverts l'oubli catastrophique, la
quantification (perspective « 8-bit MCUs », §V) et la mise à jour au-delà de la dernière
couche — exactement ce que traite une régularisation type EWC en INT8 (déduit).

## Gaps identifiés

- Apprentissage en ligne sur MCU sans mécanisme anti-oubli : aucune mesure de BWT.
- Entraînement en précision réduite sur MCU : annoncé, non fait.
- Pas de protocole de dérive contrôlée ni de détection de dérive déclenchant la mise à jour.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). La fin de §III-C (description du ventilateur et des
données) est tronquée à l'extraction ; Table I reconstruite par PyMuPDF.
Déduit et non affirmé par les auteurs : puce nRF52840 ; surcoût ≈ 10 % ; exposition à l'oubli.
