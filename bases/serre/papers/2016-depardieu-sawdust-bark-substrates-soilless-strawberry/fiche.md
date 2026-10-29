---
id: 2016-depardieu-sawdust-bark-substrates-soilless-strawberry
fiche: done
date: 2026-10-29
benchmarks: none
---

# Sawdust and Bark-Based Substrates for Soilless Strawberry Production: Irrigation and Electrical Conductivity Management

Claire Depardieu, Valérie Prémont, Carole Boily, Jean Caron, 2016, PLOS ONE 11(4), e0154104. https://doi.org/10.1371/journal.pone.0154104
Type : article de revue (relu par les pairs).

## Problème

Produire des fraises (cv. Seascape, plants à racines nues) hors-sol au Québec sur des substrats organiques bon marché (mélange tourbe-sciure PS25, écorce vieillie AB) à la place de la fibre de coco (CF), en trouvant les seuils d'irrigation (potentiel matriciel) et la gestion de l'EC qui donnent les mêmes rendements. Questions : PS25 égale-t-il CF/AB ? Doubler l'engrais par rapport à l'EC recommandé 0,6-1,8 dS/m améliore-t-il rendement et qualité ? (§Introduction)

## Méthode

Trois essais : Exp. 1 (serre, avril-juin 2011, 2 seuils d'irrigation par substrat, 72 j), Exp. 2 (multi-tunnel commercial, mai-oct. 2011), Exp. 3 (serre, janv.-avril 2012, deux niveaux de fertilisation F1 recommandé CTIFL / F2 double). Irrigation déclenchée par tensiomètres sans fil (Hortau TX3) dans la zone racinaire ; EC et pH du lysimètre (EC lys) et de l'extrait saturé (EC SSE) ; courbes de rétention (van Genuchten), porosité d'air. Plan en blocs, SAS MIXED (§Methodology).

## Plateforme et implémentation

Sans objet (pas de calcul embarqué). Instrumentation : tensiomètres Hortau TX3, goutteurs 2 L/h par plante (Exp. 1), système PRIVA pour le climat, lampes sodium. Code/données : non publiés (tableaux supplémentaires S1/S2 de PLOS ONE pour le programme de fertigation).

## Résultats

- Exp. 1 : un sol plus humide (déclenchement à -1,0 kPa CF ; -1,5 kPa AB et PS25, contre -1,5 et -2,5 kPa) augmente la croissance et le rendement total à j72 (§Experiment 1, Fig. 2A). PS25 limité au début par l'immobilisation de N, P, S : engrais initial nécessaire.
- Exp. 2 : rendement cumulé commercialisable 289-343 g/plante en 135 j, sans différence entre substrats ; PS25 économise 5,6-11 % d'eau avec tapis capillaire (§Exp. 2, Table 4).
- Exp. 3 : doubler l'engrais (N 2,9-6,1 mmol/L F1 vs 5,8-12,2 F2) n'améliore ni rendement ni qualité ; AB donne les meilleurs rendements ; CF accumule Na/Cl (§Exp. 3, Table 5).
- Recommandation Québec : EC d'irrigation 1,0-1,5 dS/m (§Economical implications).
→ reportés dans `benchmarks.csv` : aucune ligne (agronomie, pas de modèle ni de métrique de la grille ; `benchmarks: none`).

## Limites et critique

- Une seule variété (Seascape, jour-neutre), un seul climat (Québec), substrats locaux : les seuils en kPa dépendent de la courbe de rétention du substrat, pas transposables à un autre substrat sans mesure.
- Seuils d'irrigation différents entre expériences (Exp. 1 : -1,5 / -2,5 ; Exp. 2 : -1,5 puis -1,8 ; Exp. 3 : -1,5) : « optimal » est celui de l'Exp. 1 (court, 72 j), pas une optimisation fine.
- Climat serre peu détaillé : pas de VPD, pas de DLI, pas de CO2 ; températures et HR sont des consignes des essais, pas des optimums testés.
- Substrat en sac (CF) vs conteneurs rigides (PS25, AB) : volumes et hauteurs différents, confondus avec l'effet substrat.
- Pas de seuil de risque maladie. Pas de teneur en eau volumique cible : seul le potentiel matriciel est donné (la teneur en eau n'est pas utilisée comme seuil de déclenchement).

## Pertinence pour SerreIA

SerreIA n'a pas de recette fraise : ce papier donne la base d'une recette `fraise` hors-sol. Reprise concrète :
- irrigation par seuil de potentiel matriciel (tensiomètre) plutôt que par minuterie : déclenchement à -1,0 à -1,5 kPa (coco/substrat très aéré), -1,5 à -1,8 kPa (substrat tourbe/écorce) ;
- EC d'apport 0,6 en reprise montant à 1,6, puis 1,0-1,5 (1,2 en fructification) ; pH solution 5,0-6,6 (cible 5,5-5,8 ; substrat réglé à 5,5/5,8) ;
- fraction de drainage visée ~20 % du volume apporté, avec contrôle de l'EC du drainat (alarme si dérive : accumulation de sels observée à partir de 8-9 semaines) ;
- consignes climat de serre indicatives : jour 19-23 / nuit 12-17 °C, HR 50-60 %.
Les sondes capacitives de SerreIA (`humidite_sol` en %) ne remplacent pas un tensiomètre : si SerreIA reste en teneur en eau, il faut une courbe de rétention du substrat choisi pour convertir le seuil en %.

## Consignes chiffrées

Espèce : fraise (Fragaria × ananassa 'Seascape'), hors-sol, serre/tunnel. `n/r` : non rapporté.

| espèce | stade | grandeur | optimal | marginal / limite | unité | condition | chunk_id |
|---|---|---|---|---|---|---|---|
| fraise | établissement/production | seuil d'irrigation (potentiel matriciel), coco CF | -1,0 | -1,5 (plus sec : moins de rendement) | kPa | Exp. 1 | 2016-depardieu#007.0 |
| fraise | établissement/production | seuil d'irrigation, PS25 et AB | -1,5 | -2,5 (plus sec : moins de rendement) | kPa | Exp. 1 | 2016-depardieu#007.0 |
| fraise | fructification | seuil d'irrigation, PS25 et AB / CF | -1,8 / -1,0 | n/r | kPa | Exp. 2, ajusté au stade | 2016-depardieu#007.0 |
| fraise | production | seuil d'irrigation, CF / PS25-AB | -1,2 / -1,5 | n/r | kPa | Exp. 3 | 2016-depardieu#007.1 |
| fraise | tous | teneur en eau volumique comme seuil | n/r | n/r | % | n/r | n/r |
| fraise | établissement | EC apport | 0,6 puis jusqu'à 1,6 | n/r | dS/m | progressif, programme CTIFL | 2016-depardieu#007.0 |
| fraise | floraison, fructification | EC apport | 1,2 | n/r | dS/m | programme CTIFL | 2016-depardieu#007.0 |
| fraise | tous (recommandation) | EC apport | 1,0-1,5 | > 2,5 nocif (sol) | dS/m | Québec ; limite citée de la littérature (sol) | 2016-depardieu#016.1 ; 2016-depardieu#001.2 |
| fraise | tous | EC recommandé (réf. citée) | 0,6-1,8 | n/r | dS/m | réf. [32] | 2016-depardieu#002.0 |
| fraise | tous | pH solution nutritive observé | 5,0-6,6 | n/r | pH | plage mesurée, non un optimum testé | 2016-depardieu#007.1 |
| fraise | tous | fraction de drainage | ~20 | n/r | % du volume apporté | contrôle journalier du drainat | 2016-depardieu#007.1 |
| fraise | végétatif | azote total solution | 2,9-5,8 | n/r | mmol/L | PS25, AB, CF | 2016-depardieu#016.1 |
| fraise | fructification | azote total solution | 4,7-6,1 | n/r | mmol/L | idem | 2016-depardieu#016.1 |
| fraise | tous | porosité d'air substrat | > 20 | < 20 : risque d'hypoxie racinaire | % v/v | substrat | 2016-depardieu#010.0 |
| fraise | Exp. 1-2 | T° air consigne | jour 21-23 / nuit 17 | n/r | °C | HR 50 % ; consigne, non optimum testé | 2016-depardieu#006.0 |
| fraise | Exp. 3 (jan.-mars) | T° air consigne | jour 16 / nuit 12 | n/r | °C | HR 60 % | 2016-depardieu#006.3 |
| fraise | Exp. 3 (mars-avril) | T° air consigne | jour 19-20 / nuit 12-14 | n/r | °C | HR 50 % | 2016-depardieu#006.3 |
| fraise | Exp. 1 | éclairage d'appoint | coupé si PAR > 1200 | n/r | µmol m-2 s-1 | lampes sodium 10h30-16h | 2016-depardieu#006.1 |
| fraise | Exp. 3 | photopériode artificielle | 9h-21h (lampes) | n/r | h | n/r pour la durée totale du jour | 2016-depardieu#006.3 |
| fraise | tous | T° racines, VPD, DLI, CO2, seuils de risque maladie | n/r | n/r | n/r | non traités | n/r |

Écart avec SerreIA : pas de recette fraise dans `recettes.yaml` (tomate, laitue, basilic seulement). Comparaison indicative : EC 1,0-1,5 (fraise) est proche de laitue/basilic (1,0-1,6) et bien en dessous de la tomate (2,0-3,5) ; pH 5,0-6,6 recouvre les plages SerreIA (5,6-6,5) ; HR 50-60 % cohérente avec laitue/basilic (50-70) ; température jour 16-23 °C plus fraîche que basilic (20-27). Écart majeur : le critère d'irrigation est un potentiel matriciel en kPa, alors que `humidite_sol` de SerreIA est une teneur en eau en %.

Recette `fraise` proposée (à valider, valeurs du papier sauf mention) : `temperature: {jour: [19, 23], nuit: [12, 17]}`, `humidite: [50, 60]`, `ec: [1.0, 1.5]` (0,6 à la reprise), `ph: [5.5, 6.3]` (plage mesurée 5,0-6,6 ; le haut de 6,3 est un choix prudent, non du papier), drainage 20 %, déclenchement -1,5 kPa. `photoperiode_h`, `dli_cible`, `co2_max` : à compléter depuis d'autres sources (n/r ici).

## Gaps identifiés

- Consignes strawberry hors-sol : DLI, photopériode, VPD, T° racines absents de ce papier.
- Seuils de risque maladie (botrytis, oïdium) sur fraise sous abri : absents de la base à ce stade.
- Conversion potentiel matriciel -> teneur en eau volumique par substrat pour des sondes capacitives.

## Statut de lecture

papier complet (texte intégral lu par sections ; Tables 1, 3, 5 partiellement illisibles à l'extraction, seuls Tables 2 et 4 lus ; ligatures perdues à l'extraction, 4 fragments non réparés).
Déduit et non affirmé par les auteurs : « optimal » = seuil de l'Exp. 1 donnant les meilleurs résultats (les auteurs parlent de conditions plus humides « optimales » dans l'abstract) ; proposition de recette fraise et comparaison avec SerreIA ; pH cible 5,5-5,8 (valeurs de préparation des substrats, 5,5 et 5,8, §Growing media) ; tableau climat = consignes des essais.
