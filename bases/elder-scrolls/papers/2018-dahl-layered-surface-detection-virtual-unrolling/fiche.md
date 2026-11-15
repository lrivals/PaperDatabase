---
id: 2018-dahl-layered-surface-detection-virtual-unrolling
fiche: done
date: 2026-11-15
benchmarks: none
---

# Layered Surface Detection for Virtual Unrolling

Vedrana Andersen Dahl, Anders Bjorholm Dahl, Camilla Himmelstrup Trinderup, Carsten Gundlach, 2018, 24th International Conference on Pattern Recognition (ICPR 2018, Pékin), IEEE. https://doi.org/10.1109/icpr.2018.8545715
Type : conférence (actes revus par les pairs ; venue déduite du bandeau du PDF, `metadata.json` donne le nom OpenAlex des actes)

## Problème

Dérouler virtuellement un objet mince enroulé à partir d'un volume (micro-CT) de façon automatique et robuste (§I). Les approches antérieures exigent soit une annotation manuelle lourde (manuscrit dense, [8] dans l'article), soit une segmentation binaire suivie d'une squelettisation, qui échoue quand les couches se touchent et se propage en erreurs (§I). Cas d'application des auteurs : une feuille de microélectronique roulée (substrat polymère tissé + couche métallique), pour inspecter et quantifier les fissures ; les rouleaux antiques carbonisés ne sont cités que comme motivation (§I).

## Méthode

- Modèle géométrique sans segmentation : détection de surfaces en couches optimales (« optimal net surface », Wu et Chen, par coupe minimale s-t, solveur Boykov-Kolmogorov), avec contraintes de lissage (Δx, Δy) et de recouvrement (δlow, δhigh) entre surfaces (§II-A).
- Dépliage en coordonnées cylindriques (r, θ, z) autour de l'axe du rouleau : la surface roulée devient K+1 couches obliques sur l'intervalle [θA, θB[ et K sur [θB, θA[, détectées comme deux problèmes de surfaces en couches, puis rechaînées en une seule courbe (§II-C).
- Entrées manuelles : deux clics (début et fin de la surface) sur la première coupe, et le nombre de tours (§II-D).
- Coût sur la surface : c = 1 − exp(−(U − µpolymère)²) (Éq. 1), filtré par gaussienne le long de la surface et différence de gaussiennes à la normale (§II-D). Les coupes suivantes sont échantillonnées le long des normales à la surface de la coupe précédente : une seule couche à détecter (§II-D).
- Lissage élasticité/rigidité (Euler arrière), maillage quad, redistribution à ~1 pixel pour limiter la distorsion, lissage selon j contre le biais (skew) (§II-D). Mesures de qualité par quad : aspect, aire, skew (§II-E).
- Seconde étape : trois surfaces simultanées (air/polymère, polymère/métal, métal/air) contraintes autour de la surface lisse, épaisseur du polymère quasi constante, métal d'épaisseur 0 à une borne (§II-F).

## Plateforme et implémentation

Calcul : n/r (ni matériel, ni temps d'exécution, ni mémoire). Acquisition : scanner micro-CT de laboratoire, volume de 1000³ voxels ; taille de voxel, énergie, scanner exact : n/r (§III). Code : non publié, aucun lien dans le papier.

## Résultats

Résultats uniquement qualitatifs sur un seul échantillon (§III) : séparation réussie des couches densément empilées (Fig. 4), surfaces connectées malgré les fissures du polymère, texture du tissu visible (Fig. 5), maillage original ~144 fois plus dense que celui de la Fig. 6. La qualité du maillage est donnée par des histogrammes de aspect/aire/skew (Fig. 7), proches de l'idéal 1 ; moyennes et écarts-types ne figurent que dans la figure, non lisibles dans le texte extrait : n/r ici. Le texte conclut à une « distorsion minimale » sans valeur chiffrée (§III).
→ reportés dans `benchmarks.csv` : aucune ligne (pas de tableau, pas de métrique de précision comparable ni de FPS/puissance ; `benchmarks: none`).

## Limites et critique

- Validation sur un seul objet, sans vérité terrain, sans baseline comparée ni mesure d'erreur de position : « robuste » et « extrêmement robuste » sont des affirmations non quantifiées (§III, §IV).
- Hypothèses fortes : une seule surface spiralée, centre d'enroulement à peu près connu, nombre de tours donné, contraste polymère/air net. Un rouleau d'Herculanum (feuillets compressés, déformés, fracturés, sans contraste entre couches) viole ces hypothèses ; non testé (déduit).
- Semi-automatique (deux clics + nombre de tours), malgré « automatique » dans l'abstract.
- Coupes traitées une à une (limite reconnue §II-D) ; le coût suppose un niveau de gris connu du polymère.
- Pas de code publié ; pas de temps de calcul ; l'extraction est en `pymupdf` avec `ok: false`.

## Pertinence pour la thèse

Travail fondateur de l'axe déroulage virtuel : formulation par coupe minimale avec contraintes de lissage et de recouvrement, qui évite la segmentation binaire et ses erreurs sur couches en contact, et mesures de distorsion du maillage (aspect, aire, skew) réutilisables pour valider un aplatissement. Il laisse ouvert l'essentiel du Vesuvius Challenge : feuillets écrasés, effondrement de spirale, fractures, absence de contraste, absence de validation sur papyrus réel.

## Gaps identifiés

- Aucune évaluation de méthodes de surface en couches (net surface / coupe minimale) sur des rouleaux d'Herculanum ; à confronter aux champs d'enroulement et aux méthodes par apprentissage.
- Indicateurs de distorsion de maillage (aspect, aire, skew) à comparer aux critères utilisés pour SLIM/flatboi.

## Statut de lecture

papier complet (304 lignes de `fulltext.md`). Extraction `pymupdf` avec `extraction.ok: false` : texte possiblement imparfait (formules d'Éq. 1 et Cin mal restituées, ligatures réparées sauf 5 fragments) ; figures non lues, donc valeurs de la Fig. 7 non reprises.
Ce qui suit est déduit et non affirmé par les auteurs : l'inadéquation aux rouleaux d'Herculanum (hypothèses violées) ; la nature « conférence » revue par les pairs d'après le bandeau ICPR 2018.
