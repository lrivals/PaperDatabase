---
id: 2025-verde-sub-terahertz-radar-imaging-ancient
fiche: done
date: 2026-11-15
benchmarks: none
---

# Sub-terahertz Radar Imaging of Ancient Herculaneum Papyrus Scrolls reveals Adhesion to Substrate after Unrolling

Federica Verde, Sofia Ceccarelli, Valeria Giliberti, Francesco Vitucci, Costanza Miliani, Graziano Ranocchia, Michele Ortolani, 2025, International Conference on Infrared, Millimeter, and Terahertz Waves (IRMMW-THz). https://doi.org/10.1109/irmmw-thz61557.2025.11319600
Type : conférence (résumé étendu de 2 pages ; non vérifié s'il est relu par les pairs).

## Problème

Les rouleaux d'Herculanum déroulés au XVIIIe siècle ont été collés sur carton puis montés sur cadres de bois ou de métal. Les conservateurs doivent cartographier les zones adhérentes au carton avant toute intervention (Abstract, §I). Il s'agit de conservation de papyrus déjà déroulés physiquement, pas de lecture de rouleaux fermés.

## Méthode

Radar FMCW à 0,3 THz, bande passante 27 GHz, monté sur bras robotisé (TeraScan Arm 300, Lytid), deux lentilles en Téflon (f = 37 mm, D = 45 mm, N.A. > 0,5), rétrodiffusion, balayage XY au pas de 1 mm, plan focal à -5/+5 mm de la surface (§II). Pré-traitement des formes d'onde, 100 tranches Z (35 mm) conservées, ACP sur toutes les formes d'onde simultanément, deux premières composantes retenues ; classification des pixels en deux clusters (K-means) sur les poids PC1/PC2 (§II, Fig. 2). Validation par inspection visuelle comme « vérité terrain » sur un cas (Abstract, §II).

## Plateforme et implémentation

Instrument de laboratoire, pas d'inférence embarquée ni de GPU. Radar installé à l'Officina dei Papiri, Bibliothèque nationale de Naples (Fig. 1). Résolution en Z numérique 0,35 mm, épaisseur du plan focal optique estimée à environ 2 mm, bruit typique à -30 dB du pic principal (§II). Environ 2 h pour 100x100 mm² (§II). Code, données et classification : non publiés (rien d'indiqué).

## Résultats

- Les pixels forment deux clusters : bleu (PC1 élevé, forte section efficace) = zones détachées ; rouge = zones fermement adhérentes (§II, Fig. 2(b)). Les zones apparaissent allongées perpendiculairement au sens d'enroulement et sont invisibles dans l'image visible (Fig. 2(a)).
- PC2 plus dispersé dans le cluster non adhérent (Fig. 2(c)) ; hypothèse de diffusions multiples entre papyrus décollé et carton (§II).
- Aucune métrique quantitative de classification (exactitude, accord, taux d'erreur) n'est rapportée : n/r.
→ reportés dans `benchmarks.csv` : aucune ligne (voir `benchmarks: none`) ; pas de configuration chiffrée comparable (pas de métrique de performance, pas de baseline).

## Limites et critique

- Validation sur « un cas », comparaison visuelle qualitative, sans chiffre ni intervalle (§II, Abstract).
- Les zones collées sont trop petites pour être classées séparément ; « adhérent » ne signifie pas « collé » (§II).
- Le K-means à deux clusters impose la dichotomie ; l'explication par diffusions multiples est une hypothèse des auteurs.
- Portée limitée à un fragment : généralisation à d'autres papyrus, colles ou conditions d'humidité non évaluée.
- Pas de code ni de données publiés.

## Pertinence pour la thèse

Hors du cœur de la base (tomographie X et encre) : modalité non ionisante, appliquée à des rouleaux déjà déroulés, pour la conservation. Utile comme contexte papyrologique (Herculanum, ERC GreekSchools, Officina dei Papiri) et comme rappel que la validation repose sur une vérité terrain physique. Pas de lien direct avec la détection d'encre ni le déroulage virtuel. Ouvert : couplage avec CT/segmentation, état de conservation des rouleaux restants.

## Gaps identifiés

- Aucune évaluation quantitative de la modalité THz radar dans la base ; pas de comparaison avec le CT ni l'imagerie multispectrale.
- Mesure de l'état de conservation (adhérence, décollement) absente du corpus.

## Statut de lecture

Papier complet (2 pages ; extraction pymupdf, `extraction.ok` à false : texte possiblement mal découpé, en-tête et note de licence IEEE entrelacés ; Fig. 2 absente du texte, lue seulement via sa légende dans le corps).
Ce qui suit est déduit et non affirmé par les auteurs : l'absence de lien avec l'encre/le CT ; le classement de la validation comme qualitative (les auteurs ne donnent pas de chiffre).
