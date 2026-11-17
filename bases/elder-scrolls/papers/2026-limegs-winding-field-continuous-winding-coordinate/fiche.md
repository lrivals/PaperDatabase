---
id: 2026-limegs-winding-field-continuous-winding-coordinate
fiche: done
date: 2026-11-17
---

# winding-field: continuous winding-coordinate fields over predicted scroll surfaces and reproducible evaluation

LimeGS, 2026, GitHub (commit 1e2724412e, 2026-11-16). https://github.com/LimeGS/winding-field/tree/1e2724412e3df52a8d9cd6ddc2bbafcf4586c465
Type : dépôt GitHub communautaire du Vesuvius Challenge (README + benchmarks/winding/README.md + docs/PERFORMANCE_V3.md + DATASET.md) ; logiciel expérimental, non relu par les pairs, tous les chiffres sont auto-déclarés. Pas de DOI ni d'arXiv.

## Problème

Compter les enroulements (« winding counting ») d'un rouleau à partir de surfaces prédites : retrouver une coordonnée de couche continue W(x) sur tout le volume, quasi constante le long d'un feuillet et augmentant d'environ 1 en passant au feuillet suivant (README §The current method). Les observations (orientation de surface, densité de couches, fibres tracées) sont bruitées et ne forment pas un champ de gradient cohérent : les intégrer chemin par chemin accumule de la dérive. Les auteurs posent aussi le verrou ouvert : rendre cette cohérence fidèle au vrai décompte physique (README §The current method).

## Méthode

Estimation conjointe d'un champ phi (W = phi / sheet_step) qui équilibre l'accord avec les gradients locaux (normales prédites x densité de couches) et la variation le long des fibres ; une référence grossière commune porte origine et échelle vers des raffinements fins (README §The current method). Solveur linéaire (CG, préconditionneur Jacobi par défaut, spectral DCT/DST optionnel en CPU float64), résolution par blocs reprenables, contraintes de fibres (AFV, base SQLite de fibres) ; méthode globale par défaut « B2 », variantes B1/B3/B3-R/B4 (DATASET.md ; docs/PERFORMANCE_V3.md §Contracts). Gauge : zéro numérique par défaut, ancres extérieures explicites sinon (DATASET.md §Anchors). Séparation producteur / évaluateur : `evaluate.py` note un champ sauvegardé contre un « cas » gelé et hashé, sans importer le solveur (benchmarks/winding/README.md).

Évaluateur : cas v2 (frame, voxel_um, transformation native->monde, population, hashes des artefacts), contrôles « constant » et « compressé x0,1 » pour détecter l'effondrement de séparation, et aucun score combiné qui masquerait le compromis cohérence/séparation (benchmarks/winding/README.md §Numerical comparison). Résultat PASS_EVALUATED = évaluation achevée, pas acceptation physique.

## Plateforme et implémentation

Python 3.11/3.12, PyTorch, NumPy, SciPy ; Linux/macOS, CUDA optionnel ; mesures de performance sur Apple M2 Pro (12 CPU logiques), macOS arm64, 1 thread (docs/PERFORMANCE_V3.md §Local results). Mesure fine : scroll PHerc. Paris 4, grille fine 19,2 µm (champ global B2 à 307,2 µm, CT à 9,6 µm/pixel) (README). Aucune mesure sur GPU de la machine cible (pas de run CUDA/MPS : docs/PERFORMANCE_V3.md §Local results). Code publié sous MIT sur GitHub (LimeGS/winding-field) ; CLI séparée `winding-field-cli` (extraction de surface, aplatissement, rendu CT). AFV réels, poids de modèles, annotations et runs non distribués ; tests sur fixtures synthétiques (README §Data and contribution).

## Résultats

Mesure à grille fine, Paris 4, 19,2 µm, checkpoint partiel du 20/10/2026, AFV de Bruniss (snapshot 2026-10-13) : 792 595 / 2 154 184 paires sélectionnées couvertes (36,8 %) (README §Fine-grid measurement). Dérive intrafibre (|phi(a)-phi(b)| / 1,1925, en feuillets nominaux), médiane / p90 / p99 : 0,155 / 0,538 / 1,291 pour 0,5-1,5 mm ; 0,732 / 2,066 / 4,538 pour 10-15 mm ; 1,336 / 3,343 / 6,109 pour 30-45 mm (même section). La dérive croît avec la distance le long de la fibre et les erreurs longues restent importantes (les auteurs le disent). Ce sont des mesures de développement pouvant inclure les fibres d'ajustement, sans holdout indépendant ni validation physique (même section).

Performance du solveur, fixtures synthétiques 32³, médiane en ms (docs/PERFORMANCE_V3.md §Local results) : Consensus20k 605,8 (Jacobi) -> 97,8 (spectral + indices) ; Pairs 103,0 -> 14,9 ; itérations Jacobi -> spectral 302 -> 12 (Pairs), 162 -> 21 (Consensus) ; résidu vrai < 1e-8 dans les deux cas ; champs non identiques bit à bit (écart max 2,5e-8 à 1e-7). Résultat négatif déclaré : l'index spatial perd environ 39 % sur la fixture de groupes denses inter-blocs (115,6 contre 83,0 ms) ; reste optionnel. Démo synthétique du banc : 6/6 paires de fibres couvertes, 3/3 séparations correctes, 0/3 pour les deux contrôles d'effondrement (README §Generate and evaluate), chiffres explicitement illustratifs.

→ reportés dans `benchmarks.csv` (via l'agent principal ; fichier scratchpad `bench/2026-limegs-….csv`) : 7 lignes : dérive médiane aux portées 0,5-1,5, 10-15 et 30-45 mm (chunk 2026-limegs-winding-field-continuous-winding-coordinate#000.4) ; couverture 36,8 % (#000.4) ; temps Consensus20k et Pairs spectral (#005.0) ; itérations Consensus 162 -> 21 (#005.1).

## Limites et critique

- Dépôt communautaire, non relu, chiffres auto-déclarés, pas de DOI ; état « expérimental » revendiqué par les auteurs ; maintenance « best-effort ».
- La mesure fine est un checkpoint partiel (la campagne relancée s'est arrêtée avant de valider un nouveau bloc) ; seulement 36,8 % des paires sont couvertes et les non couvertes restent au dénominateur sans remplissage depuis le grossier ; les statistiques portent donc sur les paires couvertes, potentiellement les plus faciles (déduit).
- Pas de holdout : les fibres d'évaluation peuvent avoir servi à l'ajustement ; la dérive intrafibre est une métrique de cohérence, pas de vérité terrain physique (un champ constant donne 0). Aucune mesure de séparation entre feuillets voisins n'est rapportée sur Paris 4 ; les contrôles de séparation et d'effondrement ne sont montrés que sur la démo synthétique. L'identité physique des feuillets reste « non vérifiée » (README).
- Dérive médiane de 0,73 feuillet à 10-15 mm et 1,34 à 30-45 mm : à ces portées l'erreur est de l'ordre d'un tour entier, donc un décompte d'enroulements fiable n'est pas démontré (déduit à partir des chiffres de la table).
- Les gains de performance (6x à 7x) sont mesurés sur fixtures synthétiques, CPU Apple M2 Pro mono-thread, sans scan réel ni GPU ; l'accélération CPU n'implique pas d'accélération GPU (docs/PERFORMANCE_V3.md). Les blocs n'acceptent que Jacobi : le gain spectral ne s'applique pas à la route par blocs utilisée pour les grandes grilles (déduit de §Blocks). Comparaisons uniquement à leur propre version antérieure (82e0496), pas à d'autres méthodes.
- Aucune comparaison avec les autres approches de segmentation/déroulage (nnU-Net m7, Lasagna, level sets, ARAP/SLIM).
- Détails numériques à noter : le diviseur 1,192497988541921 est la valeur d'un feuillet nominal fixée par calibration, dont la justification physique n'est pas donnée ici (« calibration records provenance; it does not certify correctness »).

## Pertinence pour le thème

Contribue à l'axe validation-fp : le dépôt fait de la rigueur d'évaluation son objet (cas gelé et hashé, split réservé, contrôles constant/compressé, refus d'un score combiné, « PASS_EVALUATED n'est pas une acceptation physique »). C'est un modèle réutilisable pour valider les surfaces et décomptes de l'équipe. Côté chaîne visée, il se place entre la prédiction de surface (normales, densité de couches, champs Lasagna) et l'ajustement de spirale, comme alternative aux level sets et au suivi de fibres. Il laisse ouvert le point central : prouver que W reflète le vrai numéro de feuillet sur un rouleau réel, avec holdout et métrique de séparation.

## Gaps identifiés

- Aucune mesure de séparation entre feuillets voisins sur rouleau réel (seulement synthétique) ; pas d'évaluation sur zone réservée.
- Coordonnée globale vs. repliements, cassures et topologie du rouleau : cités comme ouverts (patchs liés ou coupures) sans résultat.
- Comparaison à d'autres estimateurs de décompte d'enroulements (champs de nombre d'enroulement dans la littérature, level sets).

## Statut de lecture

Papier complet : tout `fulltext.md` lu (README.md, benchmarks/winding/README.md, docs/PERFORMANCE_V3.md, DATASET.md). Extraction pymupdf, `extraction.ok` faux et « aucune section détectée » : les passages sont dans un seul bloc préambule, le texte peut être mal découpé ; les tableaux sont reconstruits en texte plat (aucune légende ni corps de tableau à vérifier séparément) ; images omitées (illustrations Paris 4 non lisibles).
Déduit et non affirmé par les auteurs : paires couvertes possiblement biaisées vers les plus faciles ; dérive de l'ordre d'un tour entier aux grandes portées donc décompte non démontré ; gain spectral inapplicable à la route par blocs ; absence de comparaison à des méthodes tierces (absence dans le texte, pas dans le dépôt entier).
