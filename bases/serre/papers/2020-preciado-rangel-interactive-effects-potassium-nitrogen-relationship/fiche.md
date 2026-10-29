---
id: 2020-preciado-rangel-interactive-effects-potassium-nitrogen-relationship
fiche: done
date: 2026-10-29
benchmarks: none
---

# Interactive Effects of the Potassium and Nitrogen Relationship on Yield and Quality of Strawberry Grown Under Soilless Conditions

Pablo Preciado-Rangel, Enrique Troyo-Diéguez, Luis Alonso Valdez-Aguilar, José Luis García-Hernández, José Guadalupe Luna-Ortega, 2020, Plants (MDPI) 9(4):441 (venue absente de metadata.json : n/r). https://doi.org/10.3390/plants9040441
Type : article de revue (déduit du DOI MDPI ; non confirmé dans metadata.json)

## Problème

Effet de l'azote (NO3-) et du potassium (K+) de la solution nutritive, et de leur interaction, sur le rendement et la qualité (nutraceutique) de la fraise hors-sol (Abstract, 2020-preciado-rangel#000.0).

## Méthode

Plan complètement randomisé : 3 niveaux de NO3- (9, 12, 15 mol m-3) x 4 niveaux de K+ (5, 7, 9, 11 mol m-3) = 12 solutions, 10 répétitions par traitement, un pot par unité (§4.2, 2020-preciado-rangel#011.0). Base : solution universelle de Steiner modifiée ; micro-éléments (mg/L) Mn 1,6, Cu 0,11, B 0,865, Zn 0,023, Mo 0,048, Fe 5 ; potentiel osmotique -0,073 MPa, pH 5,5 ; 960 mL par plante et par jour, 8 irrigations de 2 min, drainage léger d'environ 20 % (2020-preciado-rangel#011.0). Fragaria x ananassa en sac de 10 L, perlite/sable 80/20, 9 plantes par m2 (2020-preciado-rangel#008.1).

## Plateforme et implémentation

Serre tunnel à Torreón (Mexique), sept. 2017 à fév. 2018 ; température moyenne jour 29,5 °C, nuit 18,4 °C (2020-preciado-rangel#008.0). Humidité, rayonnement, photopériode : n/r. Pas de matériel électronique ni de code.

## Résultats

- Rendement, nombre de fruits et fermeté les plus élevés à 12 et 15 mol m-3 de NO3- ; calibre et °Brix plus élevés à 9 (§2.1, 2020-preciado-rangel#002.0).
- Optimum de NO3- pour le rendement : 12 mol m-3 avec 11 mol m-3 de K+ (2020-preciado-rangel#002.1) ; °Brix maximal 10,6 à 11 mol m-3 de K+ (2020-preciado-rangel#002.2).
- Interaction N-K significative seulement sur le nombre de fruits : meilleure interaction à 7 mol m-3 de K+ avec 12 et 15 de NO3- (2020-preciado-rangel#004.0). Les ratios de Steiner donnent les rendements les plus élevés : NO3-/H2PO4-/SO4 2- = 60/5/35 et K+/Ca2+/Mg2+ = 35/45/20 mol m-3 (2020-preciado-rangel#004.0).
- Conclusions : l'optimum de N n'est pas atteint (tendance linéaire) ; 7 K + 12 N maximise rendement, capacité antioxydante et phénols ; 11 K maximise phénols (2020-preciado-rangel#015.0).
- Valeurs numériques de rendement (Table 1) : corps du tableau non extrait, n/r.
→ reportés dans `benchmarks.csv` : aucune (agronomie, pas de mesure de modèle).

## Limites et critique

Un seul cultivar (n/r dans les passages lus), un seul site chaud et sec (jour 29,5 °C), une saison. Les auteurs reconnaissent que l'optimum de N n'est pas atteint. Concentrations en mol m-3 (équivalent mmol/L), pas en EC : aucune valeur d'EC n'est rapportée, seulement un potentiel osmotique de -0,073 MPa ; ne pas convertir sans mesure. Les niveaux de K n'ont pas modifié les tendances numériques (analyse refaite par facteur, 2020-preciado-rangel#002.0). Table 1 et Table 3 sans corps extrait.

## Consignes chiffrées

| espèce | stade | grandeur | optimal | marginal / limite | unité | condition | chunk_id |
|---|---|---|---|---|---|---|---|
| fraise | n/r (fructification supposée, non dit) | pH solution nutritive | 5,5 | n/r | pH | solution ajustée, perlite/sable | 2020-preciado-rangel#011.0 |
| fraise | n/r | potentiel osmotique solution | -0,073 | n/r | MPa | EC non rapportée | 2020-preciado-rangel#011.0 |
| fraise | n/r | NO3- | 12 (rendement) ; 9 (°Brix) | 15 : rendement max mais qualité moindre | mol m-3 | avec K+ 7 à 11 | 2020-preciado-rangel#002.1 |
| fraise | n/r | K+ | 11 (rendement, °Brix, phénols) ; 7 (interaction N-K) | 5 testé, n/r | mol m-3 | NO3- 12 | 2020-preciado-rangel#015.0 |
| fraise | n/r | ratio NO3-/H2PO4-/SO4 2- | 60/5/35 | n/r | mol m-3 | Steiner | 2020-preciado-rangel#004.0 |
| fraise | n/r | ratio K+/Ca2+/Mg2+ | 35/45/20 | n/r | mol m-3 | Steiner | 2020-preciado-rangel#004.0 |
| fraise | n/r | temp. air jour / nuit | 29,5 / 18,4 (observées, pas des consignes) | n/r | °C | serre tunnel | 2020-preciado-rangel#008.0 |
| fraise | n/r | dose d'irrigation | 960 | n/r | mL/plante/jour | 8 x 2 min, drainage ~20 % | 2020-preciado-rangel#011.0 |

Écart avec SerreIA : `edge/controller/recettes.yaml` ne contient aucune recette `fraise` (tomate, laitue, basilic seulement). Pour une recette `fraise`, ce papier fournit pH 5,5 (les plages de tomate/basilic sont 5,8 à 6,5 et laitue 5,6 à 6,2) mais aucune EC (le champ `ec` reste à documenter ailleurs) ; ne pas convertir -0,073 MPa en dS/m sans source.

## Pertinence pour la thèse

Axe `climate-control` (nutrition hydro de la fraise). Faible : un seul essai N x K, sans EC ni stades. Utile pour pH 5,5 et le ratio Steiner (donner la proportion K/N au dosage de l'agent).

## Gaps identifiés

EC par stade pour la fraise hors-sol ; consignes de température/HR fraise ; valeurs de rendement de Table 1.

## Statut de lecture

Sections lues par passages : Abstract, Introduction, Results 2.1 et 2.3, Methods 4.1 et 4.2, Conclusions (chunks cités vérifiés). Discussion, Table 1 et Table 3 non lus (corps non extrait). Déduit et non affirmé : le stade (fructification) n'est pas donné ; l'équivalence mol m-3 / mmol L-1 est standard mais non écrite ici.
