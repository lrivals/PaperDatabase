---
id: 2013-brechner-cornell-hydroponic-lettuce-handbook
fiche: done
date: 2026-10-29
benchmarks: none
---

# Hydroponic Lettuce Handbook

Melissa Brechner, A. J. Both. Cornell University, Controlled Environment Agriculture program (handbook), 2013. DOI / URL : n/r.
Type : report (littérature grise, manuel technique non relu par les pairs ; aucune méthode expérimentale).

## Problème

Fournir à de petites exploitations un système de serre hydroponique (étang flottant / DWC) produisant de la laitue pommée 365 jours par an, avec une croissance quotidienne prévisible grâce au contrôle de l'environnement, éclairage d'appoint et ombrage mobile compris (Abstract, 2013-brechner#000).

## Méthode

Description d'un système opérationnel : pépinière de 11 jours (bancs ebb-and-flood, 2013-brechner#002), puis étang flottant avec un seul re-espacement au jour 21 (2013-brechner#010), pilotage informatique de l'éclairage au DLI cible (2013-brechner#012), capteurs en boîte aspirée (PAR, T air et solution, HR, CO2, pH, OD, EC ; 2013-brechner#017). Aucune expérience, aucun témoin, aucun effectif rapporté : les valeurs sont celles « qui ont fonctionné » pour les auteurs.

## Plateforme et implémentation

Serre Cornell CEA, cultivar Boston bibb (2013-brechner#011). Pépinière : banc de 2,5 x 1,3 m, irrigué par subirrigation 2 à 4 fois par jour pendant environ 15 min, 250 L de solution pour ~2000 plants sur 11 jours (2013-brechner#003). Étang : revêtement polyéthylène 0,5 mm (2013-brechner#009) ; exemple 1245 têtes/jour pour 660 m2 (2013-brechner#040). Éclairage HPS/MH ; ventilateur de pales vertical 140 ft3/min (2013-brechner#012). Code / bitstream : sans objet. Logiciels de contrôle cités : Argus, Hortimax, Priva (2013-brechner#017).

## Résultats

Pas de résultats mesurés : le document donne des consignes (voir « Consignes chiffrées »). Cycle : 11 jours en pépinière, jours 11-21 étang à 97 plants/m2, re-espacement à 38 plants/m2, jours 21-35 étang final (2013-brechner#010), soit 35 jours de semis à récolte (déduit de « day 21 through day 35 »).
→ reportés dans `benchmarks.csv` : aucune ligne (pas de configuration mesurée ; `benchmarks: none`).

## Consignes chiffrées

| espèce | stade | grandeur | optimal | marginal / limite | unité | condition | chunk_id |
|---|---|---|---|---|---|---|---|
| laitue (Boston bibb) | pépinière j1 | PAR instantané | >= 50 | n/r | µmol/m2/s | 24 premières heures, évite l'étiolement et le dessèchement du substrat | 2013-brechner#006 |
| laitue | pépinière j2-j11 | PAR instantané | 250 | lampes à remplacer sous ~200 | µmol/m2/s | photopériode 24 h | 2013-brechner#007, #007 |
| laitue | pépinière | DLI | ~22 | tolère 30 (anecdotique) | mol/m2/j | photopériode plus courte acceptable si DLI total identique | 2013-brechner#007 |
| laitue | pépinière | photopériode | 24 | plus courte si intensité compensée | h | éclairage continu | 2013-brechner#007 |
| laitue | pépinière | irrigation | 2 à 4 fois/j, ~15 min | n/r | cycles/j | subirrigation ebb-and-flood | 2013-brechner#003 |
| laitue | pépinière | durée | 11 | n/r | jours | semis à transfert en étang | 2013-brechner#002 |
| laitue | étang | éclairage d'appoint | 100-200 | n/r | µmol/m2/s | au niveau des plants | 2013-brechner#011 |
| laitue | étang | DLI (naturel + appoint) | 17 | 15 (tipburn selon cultivar) | mol/m2/j | avec flux d'air vertical ; cultivar Boston bibb | 2013-brechner#011 |
| laitue | étang | DLI sans flux d'air | 12 | n/r | mol/m2/j | cultivar Ostinata, plus commercialisé | 2013-brechner#012 |
| laitue | étang | flux d'air vertical | 140 | n/r | ft3/min (~4 m3/min, converti) | ventilateur de pales ; favorise transpiration, Ca, évite tipburn | 2013-brechner#012 |
| laitue | étang | densité | 97 (j11-21) puis 38 | n/r | plants/m2 | re-espacement au jour 21 | 2013-brechner#010 |
| laitue | étang | durée | 21 j (j11-21) puis 14 j (j21-35) | n/r | jours | 35 j au total | 2013-brechner#010 |
| laitue | étang | oxygène dissous | 8 (7-10) | >= 4 ppm (satisfaisant) ; ~0 sans apport | ppm | O2 pur ; pas d'avantage à 20 | 2013-brechner#022 |
| laitue | étang | pH | 5,8 | 5,6-6,0 acceptable | - | carences hors plage | 2013-brechner#023 |
| laitue | tous | CO2 | 1000-1500 (accélère la croissance) | ~100 ppm = épuisement en serre fermée par jour clair ; extérieur ~390 | ppm | CO2 liquide ; chauffages au gaz déconseillés (contaminants) | 2013-brechner#020 |
| laitue | tous | HR | n/r | HR élevée : moins de transpiration, botrytis et mildiou favorisés (seuil n/r) | % | qualitatif | 2013-brechner#019 |
| laitue | tous | T air jour / nuit | n/r | n/r | °C | « consigne à contrôler » sans valeur | 2013-brechner#018 |
| laitue | tous | T solution / racines | n/r | n/r | °C | idem | 2013-brechner#018 |
| laitue | tous | EC | n/r | n/r | µS/cm | seulement : soustraire l'EC de l'eau source, corriger à l'eau pure ou au stock concentré | 2013-brechner#024 |
| laitue | tous | VPD | n/r | n/r | kPa | absent | n/r |
| laitue | tous | photopériode étang | n/r | n/r | h | DLI visé par cumul, durée non fixée | 2013-brechner#012 |

Écart avec SerreIA (recette `laitue-hydro` : T jour 16-22 / nuit 12-16 °C, HR 50-70 %, photopériode 16 h, DLI 14, pH 5,6-6,2, EC 1,0-1,6) : le papier ne fournit ni T, ni HR, ni EC, qui restent donc non sourcés. Recouvrement : pH (5,6-6,0, optimum 5,8, plage SerreIA un peu plus large vers le haut). Écart majeur : DLI cible 14 (SerreIA) contre 17 mol/m2/j (Cornell, avec flux d'air) ; le papier note que 15 est déjà le maximum avant tipburn pour certains cultivars et 12 sans flux d'air : 14 est prudent, mais le papier suggère de lier le plafond DLI au flux d'air. Photopériode : 24 h en pépinière contre 16 h SerreIA (stade semis non couvert par la recette, qui n'a que « croissance »). OD (7-10 ppm), densité et cycle de 35 jours : absents de la recette.

## Limites et critique

- Littérature grise : valeurs « ce qui a marché chez nous », pas d'essai comparatif, pas d'incertitude. Les auteurs précisent eux-mêmes que le DLI sans/avec flux d'air dépend du cultivar, de l'espacement et du flux, et que les maxima/minima de flux d'air n'ont pas été établis (2013-brechner#012).
- Cultivars spécifiques (Boston bibb, Ostinata aujourd'hui indisponible) : transposition à d'autres laitues à vérifier.
- Plusieurs sections de capteurs/pompes sont vides à l'extraction ; les paramètres surveillés (T, HR, CO2...) sont listés sans plages. Pas de seuil température, HR, EC : le manuel ne peut pas servir de baseline pour ces grandeurs.
- Conditions de système DWC avec O2 pur, serre vitrée avec ombrage mobile : non transposables telles quelles à une serre à ressources limitées.

## Pertinence pour SerreIA

Reprise concrète : (1) tester le DLI cible laitue à 15-17 mol/m2/j seulement si un flux d'air vertical est présent, sinon rester à 12-14 (2013-brechner#011, #012) ; règle « DLI > 15 sans brassage = risque tipburn » à ajouter à l'agent ; (2) pH cible 5,8 et alarme hors 5,6-6,0 (2013-brechner#023) ; (3) alarme oxygène dissous < 4 ppm, cible 7-10 pour DWC (2013-brechner#022) ; (4) enrichissement CO2 1000-1500 ppm si la serre est fermée, avec l'idée qu'un épuisement vers 100 ppm limite la photosynthèse (2013-brechner#020) ; (5) soustraire l'EC de l'eau source avant comparaison à la consigne (2013-brechner#024) ; (6) gérer deux stades (pépinière 11 j à 24 h / 250 µmol/m2/s, puis croissance, densité divisée par ~2,5 au jour 21). Limite : pas de T/HR/EC.

## Gaps identifiés

- Consignes T air jour/nuit, T solution, HR, EC et VPD pour laitue hydroponique : à chercher dans d'autres sources (non couvertes ici).
- Lien DLI maximum - flux d'air - tipburn, quantifié par cultivar.

## Statut de lecture

papier complet (fulltext.md lu en entier ; extraction grobid ok, corps de tableaux manquant pour deux éléments : Construction/Figure 12 et une figure sans légende, sans chiffres perdus identifiés ; équation du PAR horaire illisible, `( ) ( ) ( ) ( )`).
Déduit, non affirmé : durée totale de 35 jours ; conversion 140 ft3/min en m3/min ; comparaison à recettes.yaml.
