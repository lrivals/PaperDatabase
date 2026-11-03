---
id: arxiv-1802.04712-attention-deep-multiple-instance-learning
fiche: done
date: 2026-11-03
---

# Attention-based Deep Multiple Instance Learning

Maximilian Ilse, Jakub M. Tomczak, Max Welling, 2018, arXiv preprint. https://arxiv.org/abs/1802.04712
Type : preprint non relu par les pairs

## Problème

Apprendre une étiquette unique par « sac » d'instances (MIL) sans étiquettes d'instances, avec des opérateurs d'agrégation max et mean fixes et non entraînables, et sans interprétabilité : seule l'approche par scores d'instances en offre, mais sa précision au niveau instance est faible (§1, citant Kandemir & Hamprecht 2015).

## Méthode

- Étiquette du sac modélisée par une loi de Bernoulli de paramètre θ(X), entraînée par log-vraisemblance (§2.1).
- Décomposition en trois étapes via le théorème des fonctions symétriques : embedding des instances f, agrégation invariante par permutation σ, classifieur de sac g (§2.1-2.2).
- Contribution : agrégation par moyenne pondérée, poids a_k = softmax(wᵀ tanh(V h_k)) (éq. 7-8), et variante à portes (gated) avec sigmoïde (éq. 9). Les poids somment à 1 et servent de proxy d'importance des instances (§2.4).
- Approche « embedding-level » (agrégation avant le classifieur) comparée à « instance-level » (agrégation des scores) ; dimension L de V testée à 64, 128, 256, effet mineur (§4).
- Toolflow : n/r (non pertinent).

## Plateforme et implémentation

Matériel d'entraînement, latence, puissance : n/r. Code publié : n/r (non mentionné dans le texte lu). Réseaux : LeNet5 pour MNIST-BAGS (Tables 8-9), modèle de Sirinukunwattana et al. 2016 pour les images histologiques (§4.3), architecture MI-Net pour les jeux classiques (§4.1).

## Résultats

- Jeux MIL classiques (MUSK1/2, FOX, TIGER, ELEPHANT) : l'attention est « comparable » aux meilleures méthodes classiques ; chiffres de la Table 1 non extraits (corps absent), donc non repris (§4.1).
- MNIST-BAGS (AUC, Fig. 1-3) : meilleure que les autres méthodes en petit échantillon (50-150 bags à ~10 instances ; 50-100 bags à ~50 instances), SVM meilleur à grand échantillon ; embedding > instance ; mean moins bon que max (§4.2). Valeurs numériques dans des figures sans données extraites : non reprises.
- BREAST CANCER (Table 2, 58 images, 672 patches 32x32 par sac, moyenne de 5 runs) : accuracy Gated-Attention 0.755, Attention 0.745, Embedding+mean 0.741, Instance+mean 0.672, Instance+max 0.614, Embedding+max 0.607 ; recall Gated-Attention 0.731, AUC 0.799 (Table 2).
- COLON CANCER (Table 3) : corps du tableau tronqué et désaligné (lignes Attention absentes), valeurs non reprises ; le texte dit seulement que la méthode est la meilleure (§4.3).
- Heatmaps d'attention proches de la vérité terrain sur le colon (Fig. 5), qualitatif.
→ reportés dans `benchmarks.csv` : aucune ligne ajoutée par cet agent ; 6 lignes proposées (BREAST CANCER, Table 2) à l'agent principal.

## Limites et critique

- Tâche et données médicales (histopathologie, MNIST) : aucune évaluation sur des plantes ; transfert à vérifier.
- Jeux minuscules (58 images pour BREAST CANCER) ; écarts entre Attention, Gated et Embedding+mean de l'ordre des erreurs standard (Table 2), donc peu concluants. Embedding+max « échoue presque complètement » sur BREAST CANCER (§4.3), ce qui suggère un entraînement instable plutôt qu'une limite du max.
- MI-SVM non évalué sur les jeux histologiques (temps d'entraînement) (§4).
- Pas de calibration (ECE), pas de rejet/OOD, pas d'évaluation hors domaine ; poids d'attention non validés quantitativement comme explication (heatmaps qualitatives).
- Pas de coût de calcul ni d'inférence embarquée.

## Pertinence pour la thèse

Axe `calibration-decision` : l'agrégation entraînable (attention) est une candidate pour décider par capture à partir de plusieurs feuilles/crops (alternative à max, k feuilles, top-k, moyenne), et les poids d'attention peuvent désigner les crops déterminants ou à écarter. Déduit, non affirmé par les auteurs : l'application aux feuilles et la réduction des fausses alertes. Reste ouvert : le comportement sur PlantDoc, la calibration du score de sac, le rejet des crops hors distribution, le coût sur Hailo/RPi (le module d'attention est petit mais non mesuré ici).

## Gaps identifiés

- Aucune évaluation MIL/attention sur des images de plantes ou de feuilles dans cet article.
- Calibration et choix de seuil du score de sac non traités.
- Robustesse de l'attention au rejet de crops inexploitables non testée.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier ; extraction grobid, ok). Tableaux sans corps extrait : Table 3 (désaligné, partiel), Table 5, 6, 9 ; Table 1 absente du texte, valeurs non lues. Annexes (Fig. 6-10, Tables 7-11, résultats détaillés MNIST) non disponibles dans le texte.
Ce qui suit est déduit et non affirmé par les auteurs : la pertinence pour l'agrégation de feuilles, l'interprétation de l'échec d'Embedding+max, l'absence de code publié (non mentionné).
