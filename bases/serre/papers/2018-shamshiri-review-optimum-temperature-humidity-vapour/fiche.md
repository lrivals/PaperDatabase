---
id: 2018-shamshiri-review-optimum-temperature-humidity-vapour
fiche: done
date: 2026-10-29
benchmarks: none
---

# Review of optimum temperature, humidity, and vapour pressure deficit for microclimate evaluation and control in greenhouse cultivation of tomato: a review

Redmond Ramin Shamshiri, James W. Jones, Kelly R. Thorp, Desa Ahmad, Hasfalina Che Man, Sima Taheri. *International Agrophysics* 32(2), 287-302, 2018. DOI 10.1515/intag-2017-0005.
Type : article de revue (survey), relu par les pairs.

## Problème

Les publications recommandent des valeurs de T, HR et VPD différentes pour la tomate de serre selon le stade et la lumière. Les auteurs veulent les rassembler en valeurs optimales, marginales et de défaillance, et en tirer des fonctions d'appartenance (degré d'optimalité 0-1) pour évaluer l'écart du microclimat à l'optimum (Résumé).

## Méthode

Revue de littérature, sans protocole de sélection décrit. Découpage en cinq stades (germination/jeunes feuilles 25-35 j, végétatif 20-25 j, floraison 20-30 j, début fructification 20-30 j, fructification mûre 15-20 j) (§Growth stages, 2018-shamshiri#002.0). Synthèse de T air et racines (Table 1), HR et VPD (Tables 2-3), puis rappel du DSS HYTODMOD (El-Attal 1995 ; Short 2005, cultivar « Caruso »), des fonctions OptVPD (Shamshiri 2017b) et de TOMGRO réduit (Jones 1999) (§HYTODMOD, 2018-shamshiri#007.0). Équation de VPD (polynôme en T, `VPD = es(T)(1-HR/100)`) et Table 5 de combinaisons T/HR/VPD (2018-shamshiri#016).

## Plateforme et implémentation

Sans objet (revue). Modèles décrits : DSS HYTODMOD/OptVPD/TOMGRO interfacés sous SIMULINK (Shamshiri 2017a) ; code non publié dans cet article.

## Résultats

Tout est rapporté d'autres sources (pas de mesure propre, sauf l'exemple de deux serres vides tropicales : PE sans refroidissement T 68-70 °C, VPD moyen max 13,6 kPa ; polycarbonate + refroidissement évaporatif T 25-40 °C, VPD max 3,9 kPa, §Microclimate evaluation, 2018-shamshiri#008.x).
Points forts : VPD optimal 0,3-1,0 kPa selon les sources ; VPD seul ne peut servir de retour d'une boucle fermée car non unique (0,85 kPa = 15 °C/50 % ou 34 °C/84 %) (2018-shamshiri#008.0) ; brumisation pour passer de VPD 1,4 à 0,8 kPa : +17,3 % de biomasse, +12,35 % de rendement (Lu 2015, 2018-shamshiri#008.0) ; VPD < 0,43 kPa : champignons et carences minérales ; < 0,2 kPa : infection la plus grave (2018-shamshiri#011.0).
→ reportés dans `benchmarks.csv` : aucune ligne (survey, valeurs reprises de la littérature).

## Consignes chiffrées

Espèce : tomate de serre. Les tableaux 1, 2 et 4 du papier (optimal/marginal/défaillance par stade, DSS de Short) n'ont pas de corps dans l'extraction : seules les valeurs du texte sont relevées. Les valeurs sont celles d'auteurs cités par la revue, pas des mesures des auteurs.

| espèce | stade | grandeur | optimal | marginal / limite | unité | condition | chunk_id |
|---|---|---|---|---|---|---|---|
| tomate | cycle entier | T air | 17-27 | marginal 10 et 35 (Kittas 2005) | °C | n/r | 2018-shamshiri#003.0 |
| tomate | cycle entier | T air | 18,3-32,2 (Hochmuth) | n/r | °C | saison entière | 2018-shamshiri#003.0 |
| tomate | cycle entier | T air | 17-28 côtier ; 17-22 intérieur | tolérable 12 et 32 | °C | moyenne ambiante (Baudoin 2013) | 2018-shamshiri#003.0 |
| tomate | cycle entier | écart jour/nuit (périodicité thermique) | 5-7 | n/r | °C | n/r | 2018-shamshiri#003.1 |
| tomate | cycle entier | T air | n/r | > 26 = défaillance ; > 25 baisse probable ; serre ne doit pas dépasser 30-35 | °C | Kittas 2005 | 2018-shamshiri#003.1 |
| tomate | germination | T air | 25 | n/r | °C | n/r | 2018-shamshiri#003.2 |
| tomate | semis | T air | n/r | nuit min 18 ; jour max 27 | °C | croissance des plants | 2018-shamshiri#003.2 |
| tomate | semis | T air | 16-18,5 (Jones 2013) | n/r | °C | n/r | 2018-shamshiri#003.2 |
| tomate | feuilles/trusses | T air | 22 | n/r | °C | Sato 2000 | 2018-shamshiri#003.0 |
| tomate | nouaison / grossissement fruit | T air | 22-26 (ajout de fruits) ; 22-25 (croissance, nouaison) | nouaison optimale <= 26, échoue vers 32 | °C | Sato 2000 ; Adams 2001 | 2018-shamshiri#003.0 |
| tomate | cycle (Jones 2013) | T air jour / nuit | jour 21-29,5 ; nuit 18,5-21 ; moyenne 18,5-26,5 | n/r | °C | jour/nuit | 2018-shamshiri#003.2 |
| tomate | cycle | T canopée | 20-22 | n/r | °C | n/r | 2018-shamshiri#003.3 |
| tomate | germination / rendement max / développement | T air | rendement max 20-25 | bornes marginales : germination 16-30 ; développement 12-30 | °C | climat tropical humide (simulation) | 2018-shamshiri#003.3 |
| tomate | cycle | T racines | 27 (Jones) ; 25 (Ntatsi) ; 23 en été (Li) | 15 sous-optimal (croissance réduite) | °C | n/r | 2018-shamshiri#004.0 |
| tomate | germination | T sol | 29,5 (émergence 5-7 j) ; plage 16-29,5 | min 8-10 ; max tolérable 35 | °C | n/r | 2018-shamshiri#004.0 |
| tomate | développement / floraison / récolte | T sol | nuit-nuageux : 13-14 / 15-16 / 20-22 ; soleil : 17-20 / 19-22 / 23-25 | sol > 14 si HR 70-90 % | °C | nuit ou nuageux vs soleil (Baudoin 2013) | 2018-shamshiri#004.0 |
| tomate | cycle entier | HR | 50-70 ; pollinisation meilleure vers 60 | plage « appropriée » ASABE 60-90 | % | n/r | 2018-shamshiri#005.0 |
| tomate | cycle | HR | 55-90 sans effet négatif sur la photosynthèse (VPD 0,2-1,0) | > 90 : sensibilité du pollen à la chaleur | % | n/r | 2018-shamshiri#010.0 |
| tomate | floraison | HR | 60-70 (meilleure fécondation que 30-40) | > 90 défavorable | % | n/r | 2018-shamshiri#010.0 |
| tomate | cycle | VPD | 0,5-0,8 (Barker) ; 0,4-0,79 (Omafra) | n/r | kPa | évite fruits rétrécis et champignons | 2018-shamshiri#005.3 |
| tomate | pollinisation | VPD | 0,2-1,0 | n/r | kPa | prévention champignons | 2018-shamshiri#005.3 |
| tomate | bouturage | VPD | 0,3-0,5 | n/r | kPa | peuplement dense | 2018-shamshiri#005.4 |
| tomate | cycle | VPD | 0,75-1,06 (Just4Growers) ; 0,5-1,2 (Argus) | marginal 0,45-1,25 ; 0,4-1,37 (Argus) | kPa | n/r | 2018-shamshiri#006.0 |
| tomate | cycle | VPD seuil de commande | n/r | < 0,45 : déshumidifier ; > 1,25 : humidifier/brumiser | kPa | pratique de producteur (blog) | 2018-shamshiri#006.0 |
| tomate | cycle | VPD jour/nuit | 0,8 jour et nuit (photosynthèse et rendement > 0,5) | 0,35-1,0 jour, 0,2-0,7 nuit testés : VPD bas réduit LAI et rendement | kPa | Iraqi 1995 ; Barker 1990 | 2018-shamshiri#005.3 |
| tomate | cycle | risque maladie (VPD) | n/r | < 0,43 : champignons et carences ; < 0,2 : infection la plus nuisible ; < 0,2 ou > 2,2 : risque accru | kPa | n/r | 2018-shamshiri#011.0 |
| tomate | cycle | VPD haut (arides) | n/r | 3-5 : blossom-end rot, fermeture stomatique | kPa | climat aride | 2018-shamshiri#011.0 |
| tomate | reproductif | risque thermique | n/r | rendement -12,6 % par 1,2 °C au-dessus de 25 (optimum 23,5, défaillance 30) ; < 14 ou > 26 : fruits parthénocarpiques ; < 12,7 nuit : chute des fleurs ; > 35 : nouaison réduite ; < 10-12 plusieurs jours : productivité réduite | °C | modèle non linéaire de Sato 2000 | 2018-shamshiri#009.0 |
| tomate | cycle | CO2, DLI, photopériode, pH, EC, irrigation | n/r | n/r | n/r | non traités (rayonnement global min 2,34 kWh/m²/j, §003, Baudoin) | 2018-shamshiri#003.1 |

Valeurs vérifiées par `bin/pdb verify` sur chaque extrait (toutes `OK`).

**Écart avec SerreIA** (`recettes.yaml`, tomate-standard) : SerreIA règle l'HR à 55-80 % et T jour à 20-27 °C selon le stade, T nuit 16-20 °C. La revue donne HR optimale 50-70 % (2018-shamshiri#005.0) : SerreIA est plus humide, surtout au semis (65-80 %) et en croissance (60-75 %), au-dessus de la plage 50-70. T jour de SerreIA (20-27) tient dans 17-27 °C ; T nuit 16-19 est proche de 18-21 de Jones 2013 mais SerreIA descend à 16, près de la zone « blossom drop » sous 12,7-14 °C : marge faible. Au semis, SerreIA nuit 18-20 colle au min 18 de la revue. SerreIA n'a pas de consigne de VPD ni de T racines : la revue propose VPD 0,5-1,2 kPa, T racines 23-27 °C. Règle mildiou SerreIA (HR > 90 % plus de 10 h à 10-25 °C) : HR 90 % donne VPD 0,317 kPa à 25 °C (Table 5, 2018-shamshiri#016) ; le seuil de 0,43 kPa de la revue correspond à environ 86 % à 25 °C (calcul à partir de la table, déduit). La règle SerreIA est donc moins précoce que le seuil VPD de la revue ; à basse T (10-15 °C) un même HR donne un VPD très faible, ce que la règle en HR seul ne distingue pas.

## Limites et critique

- Compilation sans méthode de sélection ni pondération : plusieurs sources sont des blogs ou documents commerciaux (Just4Growers, Argus, Factsheet) et des valeurs se contredisent (HR 50-70 vs 60-90 ; T optimale 17-27 vs 18,3-32,2).
- Tomate seule, serres tempérées/tropicales ; aucune valeur pour laitue, basilic, fraise ; ni CO2, DLI, pH, EC, irrigation.
- Le DSS « Caruso » est validé par quatre producteurs sur une serre de 7,3 m² : validation faible. Les fonctions d'appartenance (Figs 2-3) sont des images sans valeurs extraites.
- Les valeurs de VPD marginales dépendent de la lumière et du stade ; le papier les donne souvent sans distinction.
- Tableaux 1, 2, 4 sans corps extrait : le détail par stade manque dans la base.

## Pertinence pour SerreIA

Reprise concrète :
- Ajouter une consigne VPD à `tomate-standard` (cible 0,5-1,2 kPa ; alarme < 0,45 et > 1,25 comme déclencheurs déshumidification / brumisation), calculée depuis T et HR avec l'équation du papier, sans l'utiliser seule en boucle fermée (2018-shamshiri#008.0).
- Revoir la plage HR (55-80 % actuel) vers 50-70 %, en particulier au semis et en croissance.
- Compléter la règle mildiou : en plus de HR > 90 % pendant plus de 10 h, signaler VPD < 0,43 kPa (champignons) et < 0,2 kPa (cas grave).
- Ajouter T racines/solution (23-27 °C) et un plancher de T nuit (> 14 °C ; chute des fleurs sous 12,7 °C).
- Table 5 utilisable comme test unitaire du calcul de VPD du contrôleur.
- L'agent LLM peut citer les seuils et leur source ; les valeurs de producteurs (blogs) doivent rester marquées comme faibles.

## Gaps identifiés

- Consignes comparables pour laitue hydro, basilic et fraise (VPD, T racines) absentes de cette revue.
- Pas de valeur pour CO2, DLI, photopériode, pH, EC pour la tomate.
- Tables 1, 2, 4 de l'article à relire sur l'image (`/table-review`) pour les bornes par stade et par lumière.

## Statut de lecture

papier complet (extraction GROBID ; corps des tableaux 1, 2 et 4 absents, Figs 2-4 sans valeurs).
Déduit et non affirmé par les auteurs : l'équivalent HR du seuil VPD 0,43 kPa à 25 °C ; la comparaison avec `recettes.yaml` et la règle mildiou ; la qualification des sources comme faibles.
