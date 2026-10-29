---
id: 2022-liu-model-methodology-early-warning-detection
fiche: done
date: 2026-10-29
benchmarks: none
---

# A model-based methodology for the early warning detection of cucumber downy mildew in greenhouses: An experimental evaluation

Ran Liu, Hui Wang, José Luis Guzmán, Ming Li, 2022, Computers and Electronics in Agriculture (venue déduite du préfixe du DOI, absente de metadata.json). https://doi.org/10.1016/j.compag.2022.106751
Type : article de revue (déduit de la venue).

## Problème

Les modèles d'alerte au mildiou alimentés par des capteurs en temps réel (humectation foliaire, HR, T°) ne préviennent pas l'infection : l'alerte arrive quand la période d'infection est déjà en cours ou terminée, et une panne de capteur interrompt les rapports (#004.1). Les auteurs veulent une alerte avancée pour le mildiou du concombre en serre (2-3 jours) en couplant un modèle de climat de serre et un modèle de maladie, alimentés par la seule prévision météo extérieure (#000, #013.0).

## Méthode

Chaîne en quatre blocs, recalculée toutes les heures en horizon glissant : prévision météo Weatherbit à 3 jours (#005) → modèle physique 1D du climat de serre (bilans d'énergie et de vapeur ; cinq entrées transitoires : T° et HR extérieures, rayonnement solaire, vent, configuration des ouvrants, #011.0) → HR et T° intérieures prévues sur 72 h → modèle de maladie à deux étages (#004.0, #007.0).
- Infection : positive si LWD ≥ 2 h avec TLWD (T° moyenne pendant l'humectation) dans [5, 30] °C, et LWD × TLWD ≥ 40 h·°C (éq. 1, §2.2). Le texte extrait est tronqué à cet endroit (« when the 1)) ») : la forme exacte de la condition est reconstruite à partir de l'éq. 1.
- LWD : soit capteur de feuille artificielle (résistance électrique), soit durée continue de HR au-dessus d'un seuil (#004.0). En mode prévision, deux seuils de HR : 90 % (Zhao et al. 2011, serres chinoises) et 92,85 % calibré par arbre de décision (DLT) sur mars-avril 2021 (#004.2, #012.0).
- Incubation : après l'infection, on intègre un taux horaire y = f(T° horaire moyenne) (éq. 2) ; les symptômes sont prévus quand ∑y ≥ 1. À 20 °C, y = 0,015 par heure, soit 67 h (#004.0). Modèle déclenché deux semaines après le repiquage.
- Deux approches comparées : classique (capteurs indoor mesurés, fig. 2a) et proposée (prévision, fig. 2b).

## Plateforme et implémentation

Pas de calcul embarqué. Serre solaire chinoise de 50 m × 7 m (Changping, Beijing), concombre « Jingyan Mini II » repiqué le 4 mars 2021, goutte-à-goutte (#003.0). Station Davis-6162 au centre à 1 m (T° ±0,5 °C, HR ±3 %, feuille artificielle 0-15), station extérieure Davis Vantage Pro2 Plus, acquisition toutes les 15 min, observation visuelle quotidienne des symptômes (#003.0). Code publié : n/r (non mentionné dans les passages lus).

## Résultats

- Prévision météo vs mesure extérieure (73 échantillons, 25-30 avril) : RMSE T° 2,5-4,5 °C, HR 25-37 %, vent 2,5-3 m/s, rayonnement 182-262 W/m² (#010.0).
- Modèle de serre avec entrées mesurées : RMSE T° 2,5 °C, HR 18,6 % sur 6 jours (#011.0). Avec prévision à 3 jours : RMSE T° 2,1-3,7 °C (moyenne 2,6), HR 14,6-35,4 % (moyenne 21,5 %) (#011.1).
- Méthode classique (capteur) : deux conditions d'infection idéales les 15 et 16 avril = faux positifs ; la troisième, débutant le 20 avril 20:15, avec fin d'incubation le 24 avril 11:15, coïncide avec la première observation de symptômes le 24 avril (#009.0). Probabilité d'occurrence après alerte positive de 68-96 % dans d'autres serres en 2006-2007 (Zhao et al. 2011, cité, non mesuré ici) (#009.0).
- Méthode proposée, seuil HR 90 % : premier rapport positif le matin du 20 avril, fin d'incubation prévue le 23 avril 18:00, soit un jour avant l'observation (#012.1). Seuil 92,85 % : premier rapport dans la nuit du 20 avril, fin d'incubation prévue le 24 avril 11:00, conforme à l'observation et à la prédiction capteur (11:15) (#012.1).
- Humectation prévue vs mesurée, nuit du 20-21 avril : 11,5 h (90 %) et 11 h (92,85 %) prédites, contre quatre périodes discontinues mesurées ; 24 avril : 7,3 h et 6,4 h prédites, 7,5 h mesurées (#012.0).
- Les auteurs concluent que la prévision donne le même effet que les capteurs, avec un préavis de 2 à 3 jours (#013.0).
→ reportés dans `benchmarks.csv` : aucune ligne (mesures de modèle prédictif de serre, pas de précision de classifieur ni de latence/puissance de plateforme) ; `benchmarks: none`.

## Limites et critique

- Un seul événement d'infection validé, une seule serre, une seule saison de ~2 mois (les auteurs le reconnaissent : « short production season », #013.0). Pas de taux de détection, de faux positifs ni de précision/rappel : performance rapportée par cas (2 faux positifs en méthode capteur ; « several false-positive reports » dans l'abstract, #000.0, sans décompte pour la méthode prévision).
- Le seuil de 92,85 % est calibré sur les mêmes données (mars-avril 2021) que celles de l'évaluation : risque de sur-ajustement, non testé hors échantillon.
- Erreurs de HR prévue importantes (RMSE 15-35 %) : la justesse du résultat dépend d'un seuil net à 90 / 92,85 %, très sensible à ce biais ; les auteurs le jugent « suffisant » sans analyse de sensibilité.
- Le gain « 2-3 jours » vient de l'horizon de prévision (72 h), pas d'un modèle plus fin ; l'écart avec le capteur à 90 % est d'un jour trop tôt.
- Modèle de climat physique à recaler par serre (« calibration is necessary », #004.2) ; transposition à une petite serre sans ouvrants motorisés ni prévision locale : non évaluée.
- Les valeurs déduites sont signalées dans le statut de lecture.

## Pertinence pour SerreIA

Apport direct à `risk.py` : un modèle d'alerte à deux étages (infection puis incubation) avec seuils chiffrés d'humectation et de T°, une preuve que HR > 90 % comme proxy d'humectation fonctionne sur un cas (mais un seuil calibré à 92,85 % colle mieux), et le principe d'une alerte avancée par simulation à 72 h plutôt que réactive. Espèce : concombre, absent des cultures de SerreIA (tomate, laitue, basilic, fraise) ; les seuils ne se transfèrent pas tels quels (voir plus bas).

## Consignes chiffrées

Modèle d'alerte du mildiou (Pseudoperonospora cubensis) du concombre en serre ; toutes les valeurs viennent de l'article, `n/r` sinon.

| espèce | stade | grandeur | optimal | marginal / limite | unité | condition | chunk_id |
|---|---|---|---|---|---|---|---|
| concombre | après repiquage + 2 sem. | début du modèle de maladie | n/r | déclenché 2 semaines après repiquage | semaines | modèle d'infection | 2022-liu#004.0 |
| concombre | infection | LWD minimale | n/r | ≥ 2 | h | condition d'infection | 2022-liu#004.0 |
| concombre | infection | TLWD (T° pendant l'humectation) | n/r | 5 à 30 | °C | condition d'infection | 2022-liu#004.0 |
| concombre | infection | LWD × TLWD | n/r | ≥ 40 | h·°C | éq. 1, avec LWD ≥ 2 h et 5 ≤ TLWD ≤ 30 °C | 2022-liu#004.0 |
| concombre | infection | seuil HR pour estimer LWD (littérature) | n/r | 90 | % | serres chinoises (Zhao et al. 2011) | 2022-liu#004.2 |
| concombre | infection | seuil HR pour estimer LWD (calibré DLT) | n/r | 92,85 | % | données mars-avril 2021, serre de Beijing | 2022-liu#012.0 |
| concombre | incubation | taux horaire y | n/r | 0,015 | h⁻¹ | T° horaire constante de 20 °C ; symptômes quand ∑y ≥ 1 | 2022-liu#004.0 |
| concombre | incubation | durée jusqu'à ∑y = 1 | n/r | 67 | h | T° horaire constante de 20 °C | 2022-liu#004.0 |
| concombre | incubation | taux y vs T° | n/r | n/r (éq. 2, formule extraite partiellement lisible, non recopiée) | n/r | fonction de la T° horaire moyenne | 2022-liu#004.0 |
| concombre | infection | LWD minimale citée (littérature) | n/r | 2 | h | Cohen 1977, Neufeld & Ojiambo 2012 (cités) | 2022-liu#009.1 |
| concombre | toutes | pas de calcul | n/r | 1 | h | recalcul horaire, horizon glissant 72 h | 2022-liu#007.0 |
| concombre | toutes | période d'acquisition des capteurs | n/r | 15 | min | station Davis-6162 | 2022-liu#003.0 |
| concombre | toutes | préavis d'alerte | n/r | 2 à 3 | jours | prévision météo à 3 jours | 2022-liu#013.0 |

Performance de l'alerte (mesures rapportées, une serre, un événement) :

| méthode | premier rapport positif | fin d'incubation prévue | écart à l'observation (24 avril) | faux positifs | chunk_id |
|---|---|---|---|---|---|
| capteurs (LWD mesurée) | 20 avril 20:15 | 24 avril 11:15 | ≈ 0 (coïncide) | 2 (15 et 16 avril) | 2022-liu#009.0 |
| prévision, HR > 90 % | matin du 20 avril | 23 avril 18:00 | un jour plus tôt | n/r | 2022-liu#012.1 |
| prévision, HR > 92,85 % | nuit du 20 avril | 24 avril 11:00 | conforme | n/r | 2022-liu#012.1 |

Erreurs des entrées (RMSE) : prévision météo T° 2,5-4,5 °C, HR 25-37 % (#010.0) ; serre simulée avec prévision T° moyenne 2,6 °C, HR moyenne 21,5 % (#011.0).

### Écart avec SerreIA

Règle de `risk.py` (lue dans `/home/leonard/Documents/Perso/SerreIA/edge/controller/risk.py` et `serre.yaml`, `risque: hr_humectation 90, humectation_h 10, t_min 10, t_max 25`) : humectation = durée continue de HR > 90 %, `conditions = T_moy_12h ∈ [10, 25] °C ET (humectation ≥ 10 h OU (vision mildiou confirmée sur 3 captures ET HR > 85 %))`. Score = min(1, h/10) × (1 si T ok sinon 0,3), +0,5 si vision. Réponse : ventilation 15 min, au plus une fois par heure, + alerte.

| point | Liu et al. 2022 | SerreIA `risk.py` |
|---|---|---|
| Humectation | LWD ≥ 2 h (seuil minimal de l'infection) | ≥ 10 h : cinq fois plus long |
| Seuil HR | 90 % (littérature) ou 92,85 % calibré | 90 % fixe, sans calibration locale |
| Température | TLWD dans [5, 30] °C pendant l'humectation, et LWD × TLWD ≥ 40 h·°C | moyenne glissante de 12 h dans [10, 25] °C (non restreinte à la période humide) |
| Dynamique | infection puis incubation (∑y ≥ 1, 67 h à 20 °C) donnant une date de symptômes | pas d'incubation ; alerte tant que les conditions durent |
| Anticipation | prévision 72 h, alerte 2-3 jours avant les symptômes | réactif : déclenche après 10 h d'humectation observée, donc après le début de l'infection |
| Capteurs | HR + T° + feuille artificielle (ou simulation si capteur en panne) | HR + T°, pas de capteur d'humectation foliaire |
| Vision | aucune | confirmation visuelle (3 captures, score > 0,6) abaisse la condition d'humectation |
| Évaluation | un cas, 2 faux positifs côté capteurs | aucune évaluation chiffrée connue |

Remarque : les 10 h de SerreIA correspondent à la règle agronomique générique codée en dur ; l'article n'en donne pas l'origine et n'utilise pas ce seuil. Comparer deux plages de T° (10-25 °C pour SerreIA, 5-30 °C pour Liu) vaut pour des espèces et des pathogènes différents (mildiou de la tomate/pomme de terre Phytophthora vs. P. cubensis du concombre) : la similarité des seuils n'est pas une validation croisée.

### Pour SerreIA

Remplacer la règle `humectation ≥ 10 h` par un modèle à deux étages configurable dans `regles.yaml` / `recettes.yaml` par culture : (1) infection si LWD ≥ 2 h (seuil minimal) avec LWD × TLWD ≥ 40 h·°C, T° prise pendant l'humectation et non en moyenne 12 h ; (2) incubation par accumulation horaire ∑y(T°) pour afficher une date de symptômes prévue et un état « infection en cours / incubation » ; (3) seuil de HR d'humectation calibré sur les données SerreIA (arbre de décision sur HR vs capteur de feuille, par ex. 92,85 % chez Liu) plutôt que 90 % fixe, en ajoutant si possible un capteur de feuille artificielle pour étalonner. (4) Pour l'anticipation, alimenter le modèle avec une prévision de HR/T° intérieure (la GRU de SerreIA ou un modèle physique + prévision météo) à 24-72 h, recalculée toutes les heures. Garder la vision comme confirmation indépendante. Les paramètres (TLWD, 40 h·°C, éq. 2) sont ceux du concombre : à recaler pour tomate, laitue, basilic et fraise avant usage ; l'article ne donne aucune valeur pour ces espèces.

## Gaps identifiés

- Pas de taux de détection ni de faux positifs sur plusieurs événements : un seul cas validé.
- Seuils d'infection du mildiou (LWD, TLWD, incubation) pour tomate, laitue, basilic, fraise : absents de ce papier.
- Alerte avancée à partir d'une prévision de climat intérieur (modèle physique ou GRU) : évaluation sur petite serre non motorisée à faire.

## Statut de lecture

Papier complet (fulltext.md lu par sections ciblées ; il n'a que ~29 Ko, extraction GROBID, `extraction.ok` vrai). Équation 2 (taux d'incubation y = f(T°)) mal extraite : forme exacte non recopiée, seule la valeur 0,015 h⁻¹ à 20 °C est reprise. La condition d'infection (éq. 1) est reconstruite à partir d'un texte tronqué. Venue et type déduits du préfixe du DOI, non affirmés par metadata.json. Le fait que les seuils ne se transfèrent pas aux cultures de SerreIA, la comparaison avec `risk.py` et la note « Pour SerreIA » sont des inférences, pas des affirmations des auteurs.
