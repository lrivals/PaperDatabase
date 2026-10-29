---
id: 2026-ceac-hydroponic-tomato-intensive-workbook
fiche: done
date: 2026-10-29
benchmarks: none
---

# Hydroponic Tomato Production Intensive Workbook 2026

UA-CEAC (University of Arizona Controlled Environment Agriculture Center ; recettes : T. Hooks 2025 ; texte de pilotage : M. H. Jensen), 2026, workbook d'atelier de formation (« CEAC Intensive Workshop »). DOI/URL : n/r.
Type : littérature grise (support de formation), non relu par les pairs ; sa partie « steering » est un texte ancien de Jensen reproduit.

## Problème

Former des cultivateurs à la tomate hydroponique sous serre : calcul des solutions nutritives (recettes par phase) et conduite de la plante (équilibre génératif/végétatif, effeuillage). Pas de question de recherche.

## Méthode

Pas de méthode expérimentale. Contenu : (1) description de la serre pédagogique (TGH, §About the Teaching Greenhouse) ; (2) recettes nutritives « Tomato Recipe 1 - Vegetative » etc. avec calcul de la solution mère (« Step 1 Stock Volume (L): 303 », 2026-ceac#002.0) ; (3) tableau d'éléments en ppm par phase : Propagation (semaines 0-4), 1. Vegetative (4-8), 2. Generative (8-12), 3. Balanced (12+) (2026-ceac#009.0) ; (4) texte de Jensen sur le pilotage de la plante (2026-ceac#005.0, #007.0, #007.1) et tableau 1 caractéristiques génératif vs végétatif (2026-ceac#010.0) ; (5) zone de récolte : plante de 8 pieds à 24 feuilles, ~2,5 ft de zone de récolte par effeuillage de 8 feuilles, 16 feuilles conservées (2 par truss) (2026-ceac#007.1, #008.0).

## Plateforme et implémentation

Serre TGH : 5 400 sqft en dents de scie, régulation Ridder, refroidissement pad-and-fan, chauffage au gaz par aérothermes, fertigation Ridder, capacité 800-1200 plantes grimpantes (2026-ceac#000.0). Pas de code ni de données publiés.

## Résultats

Aucun résultat mesuré. Seules valeurs numériques exploitables du texte extrait : cf. « Consignes chiffrées ». Le corps des tableaux de recettes (ppm par élément et par phase, EC, pH), le tableau 2 « Steering plant growth for maximum yield » (qui chiffre vraisemblablement T° jour/nuit, CO2, HR, EC, irrigation) et les consignes climat/VPD sont ABSENTS de l'extraction.
→ reportés dans `benchmarks.csv` : aucune ligne (document de formation, aucune mesure).

## Limites et critique

- Extraction très incomplète (voir Statut de lecture) : l'essentiel des chiffres utiles manque ; ne pas conclure que le workbook ne les donne pas.
- Source pédagogique, sans protocole ni référence pour les valeurs ; le texte de Jensen est un guide de pratique pour grande serre chauffée avec variété beefsteak, contexte Arizona.
- Conseils qualitatifs mais non chiffrés dans le texte disponible : écart jour/nuit plus grand, stress hydrique/salin/froid orientent vers le génératif ; conditions « tropicales » vers le végétatif (2026-ceac#007.0).

## Pertinence pour SerreIA

- Reprise concrète, qualitative : la grille génératif/végétatif (tableau 1, 2026-ceac#010.0) sert de checklist d'observation de la caméra/agent LLM (feuilles plates/claires vs enroulées/sombres, distance fleurs-sommet) pour décider de rapprocher ou d'écarter les consignes jour/nuit et l'EC, leviers que le contrôleur à règles possède déjà (température, EC, irrigation).
- Phasage nutritif : l'idée de 4 phases à 4 semaines (propagation, végétatif, génératif, équilibré) peut cadencer les stades de `tomate-standard` (semis, croissance, floraison, fructification) ; les valeurs ppm/EC restent à récupérer dans le PDF.
- Effeuillage : règle de 2 feuilles par truss (16 feuilles sur 8 trusses) et zone de récolte basse (~1/3 du couvert) : tâche à suggérer par l'agent LLM à l'opérateur ; pas de consigne actionneur.
- Ne pas reprendre de ce papier de seuil climat, VPD ni mildiou : absents.

## Gaps identifiés

- Les consignes chiffrées de la recette Hooks 2025 (ppm par élément, EC, pH par phase, climat, VPD) à relever depuis le PDF avec `/table-review` ou une extraction manuelle.
- Aucune règle chiffrée de risque maladie dans ce workbook.

## Consignes chiffrées

| espèce | stade | grandeur | optimal | marginal / limite | unité | condition | chunk_id |
|---|---|---|---|---|---|---|---|
| tomate | toutes | T° air jour/nuit | n/r (écart jour/nuit élevé = plus génératif, sans valeur) | n/r | °C | n/r | 2026-ceac#007.0 |
| tomate | toutes | T° racines, HR, VPD, DLI, photopériode, CO2 | n/r | n/r | n/r | n/r | n/r |
| tomate | toutes | pH, EC par stade | n/r (corps des tableaux non extrait) | n/r | n/r | n/r | 2026-ceac#009.0 |
| tomate | propagation / végétatif / génératif / équilibré | durée des phases nutritives | 0-4 / 4-8 / 8-12 / 12+ | n/r | semaines | recette Hooks 2025 (1/2x en propagation, d'après l'en-tête extrait) | 2026-ceac#009.0 |
| tomate | toutes | volume de solution mère (étape 1) | 303 | n/r | L | recette de démonstration TGH | 2026-ceac#002.0 |
| tomate | croissance | feuilles par plante, pieds de 8 ft | 24 avant effeuillage, 16 après (2 par truss) | n/r | feuilles | zone de récolte ~2,5 ft, 8 feuilles retirées | 2026-ceac#007.1, 2026-ceac#008.0 |
| tomate | toutes | seuils de risque maladie | n/r | n/r | n/r | n/r | n/r |

Écart avec SerreIA : impossible à chiffrer, aucune plage T°/HR/DLI/pH/EC lisible dans l'extraction ; seul constat : pas de contradiction avec `tomate-standard` (écart jour/nuit de 4 à 9 °C dans recettes.yaml, cohérent avec la logique de pilotage décrite). Règle mildiou « HR > 90 % plus de 10 h à 10-25 °C » : non traitée.

## Statut de lecture

papier complet (fulltext.md de ~6 ko, 11 sections lues en entier) ; `paper.pdf` non ouvert. Extraction GROBID, mais les tableaux (recettes nutritives en ppm par élément, tableau 2 de pilotage, probablement consignes climat) sont perdus ou réduits à des en-têtes : 25 pages de PDF pour ~6 ko de texte. Le PDF doit être relu manuellement (ou `/table-review`) avant d'utiliser ce papier comme source de consignes. Déduit et non affirmé : le fait que le tableau 2 contienne T°/CO2/HR/EC/irrigation (seule sa légende « Steering plant growth for maximum yield » est lue) ; « 1/2x » = demi-concentration en propagation (lu dans l'en-tête, non expliqué).
