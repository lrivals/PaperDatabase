---
id: 2018-savvas-application-soilless-culture-technologies-modern
fiche: done
date: 2026-10-29
benchmarks: none
---

# Application of soilless culture technologies in the modern greenhouse industry – A review

Dimitrios Savvas, Nazim Gruda, 2018, European Journal of Horticultural Science 83(5), 280–293.
DOI 10.17660/eJHS.2018/83.5.2. Type : revue (journal), relue par les pairs.

## Problème

Faire le point sur les technologies de culture hors-sol (SCS) pour serres : systèmes en eau et sur
substrat, substrats, composition et contrôle de la solution nutritive (NS), irrigation et
automatisation, avec l'objectif de découpler la culture du sol (pathogènes, salinité, fertilité).

## Méthode

Revue narrative (pas de protocole de sélection). Parcours : systèmes ouverts/fermés, WCS (flottant, NFT,
aéroponie, Table 1), substrats (laine de roche, perlite, coco, biochar), composition de la NS et
cibles dans la zone racinaire (Table 3, tomate, climat méditerranéen), contrôle nutritionnel en
système fermé (mélange drainage/eau, concentrations d'absorption, Fig. 3-5), irrigation
(fréquence par rayonnement ou évapotranspiration, dose par fraction d'eau facilement
disponible).

## Plateforme et implémentation

Sans objet (revue agronomique). Aucun code publié.

## Résultats

Pas de résultats propres ; repères quantitatifs de la littérature, relevés dans « Consignes
chiffrées ». Points saillants :
- La NS apportée n'est qu'un moyen ; la cible est la solution de la zone racinaire, estimée via le drainage (DS) (025.0, 025.1).
- Drainage : 15 / 30 / 45 % testés en concombre ; 20-30 % de DS ajoutés lors du pilotage par rayonnement (029.1, 036.0).
- Système fermé : si Na+/Cl- de l'eau > 1-3 mmol/L, vidange périodique inévitable (008.1) ; la consigne d'EC doit monter progressivement pour limiter les rejets (030.1, Fig. 5B).
- Irrigation : déclenchement avant -5 kPa, ou dès 0,2-0,4 de l'EAW consommée ; durée Ti par formule (éq. 2) (038.0, 035.3).
- Évapotranspiration : modèle de Baille et al. (1994) dérivé de Penman-Monteith, E fonction de G, DPV, LAI (éq. 3) (036.1).
→ reportés dans `benchmarks.csv` : aucune ligne (revue ; pas de configuration propre aux auteurs).

## Consignes chiffrées

Corps de la Table 3 (EC, pH, macro/micronutriments tomate, végétatif/reproductif) **non extrait** : seule la légende existe (025.2). Aucune valeur de cette table n'est donc reprise.

| espèce | stade | grandeur | optimal | marginal / limite | unité | condition | chunk_id |
|---|---|---|---|---|---|---|---|
| générique hydro | n/r | pH zone racinaire | 5,5-6,5 | 5,0-5,5 et 6,5-7,0 tolérés ; <5 ou >7 : croissance freinée | pH | zone racinaire, hydro | 026.2 |
| générique hydro | n/r | pH zone racinaire (risque haut) | n/r | >7,0 : carences P, Fe, Mn, Cu, Zn | pH | SCS | 026.2 |
| générique hydro | n/r | pH zone racinaire (risque bas) | n/r | <5,0 : toxicité Mn/Al, lésion H+ | pH | SCS | 026.2 |
| générique substrat | n/r | pH milieu racinaire | 5,5-6,0 | n/r | pH | disponibilité optimale des nutriments, substrat chimiquement actif | 013.0 |
| tomate | végétatif / reproductif | EC, pH, macro/micro NS | n/r (Table 3 sans corps) | n/r | dS/m ; mmol/L | climat méditerranéen | 025.2 |
| générique | n/r | EC zone racinaire | n/r | au-delà d'un seuil : rendement en baisse ~linéaire ; effet pire à forte lumière / faible HR | dS/m | seuil par espèce non chiffré | 026.1 |
| générique | n/r | NaCl eau d'irrigation, système ouvert | n/r | seuil 3-10 | mmol/L | selon l'espèce | 026.1 |
| générique | n/r | Na+/Cl- eau, système fermé | n/r | >1-3 : vidange périodique nécessaire | mmol/L | selon sensibilité au sel | 008.1 |
| concombre | n/r | taux de drainage testés | n/r | 15, 30, 45 | % de l'apport | recirculation, effet sur concentrations d'absorption | 029.1 |
| générique | n/r | drainage ajouté (pilotage par rayonnement) | +20 à 30 | n/r | % de DS en plus de la consommation | irrigation déclenchée par cumul de rayonnement | 036.0 |
| générique substrat | n/r | tension d'eau, déclenchement | avant -5 kPa | n/r | kPa | substrat | 038.0 |
| générique substrat | n/r | fraction d'EAW consommée déclenchant l'irrigation | 0,2-0,4 | n/r | fraction | arrêt à capacité du conteneur | 038.0 |
| tomate | long terme | lessivage NO3-N, système ouvert | n/r | peut dépasser 380 | kg/ha/an | vidange du DS | 008.1 |
| toutes | n/r | T° air, T° racines, T° NS, HR, DPV, DLI, photopériode, CO2 | n/r | n/r | n/r | n/r (seule mention : T° élevée de la NS limite l'O2 en système flottant, 009.0, sans valeur) | 009.0 |

Vérifié par `pdb verify` (OK) : 026.2 (pH 4 valeurs), 013.0, 038.0 (2), 036.0, 026.1, 008.1 (2), 029.1.

Écart avec SerreIA : recettes.yaml fixe pH 5,8-6,3 (tomate), 5,6-6,2 (laitue), 5,8-6,5 (basilic) : tous inclus dans la plage optimale 5,5-6,5 de Savvas, donc cohérents (les bornes SerreIA sont plus serrées, sans conflit). EC de recettes.yaml (tomate 2,0-3,5 ; laitue et basilic 1,0-1,6) : non comparable, Table 3 sans corps. Seuil de déclenchement d'irrigation : recettes.yaml donne humidite_sol 40-75 % (tomate, basilic) sans équivalent en kPa ni en fraction d'EAW ; Savvas donne -5 kPa / 0,2-0,4 d'EAW. Aucune valeur de climat (T°, HR, DLI, photopériode) dans le papier.

## Limites et critique

- Revue narrative, sans méthode de sélection ; valeurs de Table 3 inaccessibles ici (corps non extrait) : l'essentiel des cibles EC/nutriments tomate manque.
- Cibles issues de la tomate en climat méditerranéen, sur substrat (Savvas 2013, 2017) ; pas de valeurs pour laitue hydro, basilic ni fraise.
- Aucune consigne climatique (T°, HR, DPV, DLI, photopériode, CO2).
- Seuils d'EC à partir desquels le rendement chute non chiffrés dans le texte.
- Les plages de pH sont génériques (« la plupart des cultures »), citées d'Adams (2002).

## Pertinence pour SerreIA

- pH : plage générique 5,5-6,5 (026.2) valide les consignes pH de recettes.yaml pour les trois cultures hydro ; alerte de sécurité possible à <5,0 / >7,0 (risques décrits).
- Régulation EC/pH par injection en boucle fermée sur la mesure de la solution sortante (007.0) : architecture de référence pour le contrôleur à règles.
- Recirculation : mélange drainage/eau visant une EC cible (Fig. 3A/B), consigne d'EC relevée progressivement quand Na+/Cl- s'accumule (030.1), vidange quand Na+/Cl- > 1-3 mmol/L (008.1) : règle de purge applicable si SerreIA recircule.
- Irrigation substrat (tomate, basilic) : déclencher avant -5 kPa ou à 20-40 % d'EAW consommée (038.0) ; ajouter 20-30 % de drainage (036.0) ; ET par Baille (DPV, rayonnement, LAI, 036.1) pour l'agent LLM.
- Laitue/basilic en eau : risque d'hypoxie si la NS est chaude (009.0) ; à surveiller sans seuil chiffré.

## Gaps identifiés

- Cibles EC et macronutriments par culture hydro (laitue, basilic, fraise) : à chercher ailleurs (Table 3 sans corps ici).
- Consignes de T° de la solution/racines et d'O2 dissous : n/r.
- Seuils de déclenchement d'irrigation en % d'humidité capacitive (sondes) vs kPa : conversion absente.

## Statut de lecture

Sections lues (via recherche et lecture de passages) : systèmes ouverts/fermés, WCS, substrat chimique, composition et ajustement de la NS, contrôle en système fermé, irrigation (fréquence, dose), conclusions. Pas relu intégralement. Corps de la Table 3 non extrait (extraction grobid) : valeurs absentes. Déduit, non affirmé par les auteurs : la comparaison avec recettes.yaml et les usages proposés pour SerreIA.
