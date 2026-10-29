---
id: 1990-hochmuth-fertilizer-management-greenhouse-vegetables-florida
fiche: done
date: 2026-10-29
benchmarks: none
---

# Fertilizer Management for Greenhouse Vegetables-Florida Greenhouse Vegetable Production Handbook, Vol 3 1

G. J. Hochmuth, 1990 (date de la première édition ; le texte cite le site « [January 2012] » (§More Information), donc une version révisée par l'éditeur existe probablement, date de révision exacte `n/r`), UF/IFAS EDIS HS787, Florida Greenhouse Vegetable Production Handbook vol. 3. DOI/URL : n/r.
Type : littérature grise (guide de vulgarisation universitaire), ni article ni preprint, non évalué par les pairs.

## Problème

Guide pratique de fertilisation des légumes de serre en Floride (tomate surtout, concombre, feuillus) en hydroponie (NFT) et en substrat (laine de roche, perlite, tourbe) : quoi apporter, à quelles concentrations, comment formuler, mélanger, mesurer et corriger la solution nutritive.

## Méthode

Pas de protocole expérimental : synthèse d'expert. Contenu : rôle et carences des 13 éléments minéraux ; matières fertilisantes ; formules de solution nutritive (Tables 3 à 8, dont deux d'après J.B. Jones 1983) ; calcul de stocks (exemple 150 ppm N/Ca/K, dilution 1:100) ; qualité de l'eau ; pH ; mesure par EC vs analyse ppm ; automatisation de la fertigation ; sels solubles ; vidange hebdomadaire de la cuve ; analyse foliaire et jus de pétiole (Table 9) ; pulvérisations foliaires.

## Plateforme et implémentation

Sans objet (aucun matériel d'IA). Systèmes de culture visés : NFT, laine de roche, perlite, tourbe. Code/données : non publiés.

## Résultats

Pas de résultats expérimentaux mesurés. Valeurs de référence principales (détail et sources dans « Consignes chiffrées ») :
- Formules 4 et 5 de tomate en 5 stades A à E : N 65 à 148 ppm, K 120 à 208 ppm, P 50 ppm, pH 5,5, EC approx. 0,8 à 2,0 dS/m (§Table 6/7, chunks 033.2, 034.1, 034.2).
- pH du milieu : 5,5 à 6,5 (§Media Reaction) ; solution hydro 5,6 à 6,0 (§Nutrient Deficiencies).
- Jus de pétiole de tomate, NO3-N 1000-1200 ppm puis 700-900 ppm en récolte (Table 9).
→ reportés dans `benchmarks.csv` : aucune ligne (pas de résultat expérimental ; schéma de benchmarks sans objet pour une recommandation agronomique). `benchmarks: none`.

## Limites et critique

- Contexte Floride (eau de puits riche en Ca, forte ventilation, fortes températures) : l'auteur dit lui-même de ne pas suivre à la lettre les programmes nordiques (§Soluble Salt Effects) ; transposition à une serre tempérée/ESP32 à valider.
- Les formules viennent en partie de J.B. Jones 1983 : source ancienne, non rejouée ici.
- Les tableaux 3 à 5 n'ont pas de corps extrait (`extraction.warnings`) ; les tableaux 6 et 7 sont partiels. Les libellés des stades A à E ne sont pas donnés dans le texte extrait.
- Aucune consigne climatique (T° air, HR, VPD, DLI, photopériode) hors CO2 qualitatif : le guide ne couvre que la nutrition.
- L'auteur déconseille de piloter la nutrition à l'EC seule (§Measuring Solution Nutrient Concentration) : message important pour un contrôleur à base de sonde EC.
- Pas de baseline ni de comparaison ; recommandations non justifiées par des essais cités.

## Pertinence pour SerreIA

Reprises concrètes pour SerreIA :
1. Garde-fous de l'actionneur pH/EC : fenêtre pH 5,5 à 6,5 (milieu) et 5,6 à 6,0 (hydro) ; alerte si pH du substrat > 7,0 (perte de solubilité P et micronutriments).
2. EC substrat vs EC apportée : écart max ± 1,0 dS/m, sinon l'apport par irrigation est trop gros (écart < -1,0) ou trop faible (> +1,0) ; règle directement codable pour une zone substrat.
3. EC de l'eau d'appoint > 1,5 dS/m = mauvaise qualité : test de l'eau d'entrée.
4. Vidange hebdomadaire de la cuve (pH 5,8 à 6,0, 25 à 50 ppm Ca la nuit) pour les zones hydro (laitue, basilic).
5. Courbe de montée en concentration de la tomate (N, K, EC par stade A à E) pour affiner les plages `ec` de `recettes.yaml`, et sauf-ce-que-dit l'auteur : ne pas piloter à l'EC seule, d'où cadre pour l'agent LLM (demander une analyse ppm).
6. Risque physiologique : humidité élevée -> tip burn de la laitue (Ca mal transporté) ; blossom-end-rot de la tomate lié au Ca ; CO2 à n'injecter que le jour, aérations fermées.

Écart avec SerreIA : voir la ligne dédiée dans « Consignes chiffrées ».

## Gaps identifiés

- Aucune consigne T°/HR/VPD/DLI chiffrée dans ce guide : à chercher dans les autres volumes du handbook (production de tomate, vol. 3, ou chapitre « General Aspects of Plant Growth », absents de la base).
- Basilic, fraise : non traités ; laitue seulement via la formule 3 (tableau sans corps extrait).
- EC de la solution par stade pour la tomate : un seul jeu de formules (Floride).

## Statut de lecture

Papier complet, lu par morceaux sans ouvrir le PDF (`fulltext.md` lu en sections ; extraction GROBID, ligatures perdues sur 3 fragments). Tableaux 2 à 5 sans corps extrait : non lus. Déduit, non affirmé par l'auteur : conversion 60 F ≈ 15,6 °C et 55 F ≈ 12,8 °C (arithmétique) ; l'ordre croissant des stades A à E (suggéré par les valeurs, libellés absents) ; assimilation des formules 4 et 5 à des consignes de croissance de tomate de serre.

## Consignes chiffrées

| espèce | stade | grandeur | optimal | marginal / limite | unité | condition | chunk_id |
|---|---|---|---|---|---|---|---|
| tomate | n/r | T° air | n/r | n/r | °C | n/r | n/r |
| tomate | semis | T° du milieu (racines) | n/r | ne pas descendre sous 60 F (soit environ 15,6 °C ; valeur d'origine 60 F) pendant de longues périodes | °F | surtout pendant le développement des plantules ; P moins absorbé en milieu froid | 1990-hochmuth#002.1 |
| légumes (dont tomate) | n/r | T° du milieu : NH4 mieux absorbé que NO3 | n/r | sous 55 F (environ 12,8 °C ; valeur d'origine 55 F) | °F | milieu froid | 1990-hochmuth#002.2 |
| tous | n/r | HR | n/r | HR élevée : tip burn de la laitue (pas de seuil chiffré) | n/r | transpiration trop faible pour amener le Ca | 1990-hochmuth#003.0 |
| tous | n/r | VPD, DLI, photopériode | n/r | n/r | n/r | n/r | n/r |
| tous | n/r | CO2 | n/r (aucune consigne chiffrée) | injecter seulement ventilation arrêtée et de jour | n/r | Floride : injection peu efficace (forte ventilation) | 1990-hochmuth#001.1 |
| hydro (tous) | n/r | pH solution | 5,6 à 6,0 | n/r | pH | pour favoriser l'absorption de P | 1990-hochmuth#002.0 |
| substrat tourbe | n/r | pH du milieu | 5,5 à 6,5 | ne pas surchauler la tourbe | pH | culture en bac/sac | 1990-hochmuth#002.0 |
| tous | n/r | pH du milieu (absorption) | 5,5 à 6,5 | au-dessus de 7,0 : micronutriments et P moins solubles | pH | n/r | 1990-hochmuth#009.0 |
| tous | n/r | pH d'acidification de l'eau riche en HCO3 | 5,6 à 6,0 | HCO3 > 30 à 60 ppm : pH en hausse | pH ; ppm | acide nitrique, phosphorique ou sulfurique | 1990-hochmuth#008.0 |
| tomate | A | N, P, K, Ca, pH, EC (formule 4) | N 65, P 50, K 120, Ca 80 ; pH 5,5 ; EC 0,8 | n/r | ppm ; dS/m | laine de roche, perlite, NFT | 1990-hochmuth#033.2 |
| tomate | E | N, P, K, Ca, pH, EC (formule 4) | N 148, P 50, K 208, Ca 127 ; pH 5,5 ; EC 2,0 | n/r | ppm ; dS/m | idem ; stades B, C, D intermédiaires (EC 1,0 ; 1,4 ; 1,6) | 1990-hochmuth#033.2 |
| tomate | A | N, P, K, Ca, pH, EC (formule 5) | N 68, P 50, K 121, Ca 58 ; pH 5,5 ; EC 0,8 | n/r | ppm ; dS/m | idem | 1990-hochmuth#034.1 |
| tomate | E | N, P, K, Ca, pH, EC (formule 5) | N 140, P 50, K 199, Ca 121 ; pH 5,5 ; EC 1,8 | n/r | ppm ; dS/m | idem ; stades B, C, D : EC 0,9 ; 1,3 ; 1,5 | 1990-hochmuth#034.2 |
| tomate | transplant à 2e bouquet | NO3-N / K du jus de pétiole | NO3-N 1000-1200 ; K 4500-5000 | n/r | ppm | Table 9 | 1990-hochmuth#036.0 |
| tomate | 2e à 5e bouquet | NO3-N / K du jus de pétiole | NO3-N 800-1000 ; K 4000-5000 | n/r | ppm | Table 9 | 1990-hochmuth#036.0 |
| tomate | récolte (déc.-juin) | NO3-N / K du jus de pétiole | NO3-N 700-900 ; K 3500-4000 | n/r | ppm | Table 9 | 1990-hochmuth#036.0 |
| tous | n/r | EC de l'eau d'appoint | n/r | > 1,5 : mauvaise qualité | dS/m | pour la plupart des cultures de serre | 1990-hochmuth#007.1 |
| substrat (laine de roche, perlite) | n/r | écart EC substrat vs EC apportée | n/r | ne pas dépasser ± 1,0 | dS/m | EC < -1,0 : trop d'apport par arrosage ; > +1,0 : pas assez | 1990-hochmuth#014.1 |
| tomate vs laitue | n/r | tolérance aux sels | tomate plus tolérante que concombre, poivron, laitue (pas de seuil chiffré) | sels : risque accru début automne et fin printemps | n/r | forte T° et rayonnement | 1990-hochmuth#014.0 |
| tous | n/r | irrigation (besoin en eau) | n/r | jusqu'à 2 quarts d'eau par plante et par jour | quart/plante/jour | plante adulte, fort rayonnement, T° élevée | 1990-hochmuth#007.0 |
| hydro NFT | n/r | vidange de cuve | 1 fois par semaine ; eau à pH 5,8 à 6,0 avec 25 à 50 ppm Ca la nuit | n/r | semaine ; ppm | la solution est jetée au moins hebdomadairement en Floride | 1990-hochmuth#015.0 |
| tous | n/r | seuils de risque maladie (humectation, HR) | n/r | n/r | n/r | n/r | n/r |

Écart avec SerreIA (`recettes.yaml`, tomate-standard) : pH recette 5,8 à 6,3 contre 5,5 à 6,5 (milieu) et formules à pH 5,5 : recette plus étroite et décalée vers le haut ; EC recette 2,0 à 3,0 (croissance) et 2,5 à 3,5 (floraison, fructification) contre EC approx. 0,8 à 2,0 (formule 4) ou 0,8 à 1,8 (formule 5) : écart majeur, la recette est de 0,5 à 1,5 dS/m plus haute que ce guide (guide pour la Floride, climat chaud, qui prévient que les programmes nordiques sont souvent excessifs ; l'auteur ne chiffre pas de maximum d'EC de solution). Laitue-hydro : recette pH 5,6 à 6,2 contre 5,6 à 6,0 (hydro) : cohérent. Pas de consigne T° air, HR, DLI ou photopériode à comparer ; T° de milieu 60 F environ 15,6 °C sans équivalent dans les recettes (températures racinaires absentes de `recettes.yaml`). Règle mildiou « HR > 90 % plus de 10 h à 10–25 °C » : non traitée par ce guide.
