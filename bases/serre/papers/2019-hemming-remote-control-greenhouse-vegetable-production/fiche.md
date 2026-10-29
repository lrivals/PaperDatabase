---
id: 2019-hemming-remote-control-greenhouse-vegetable-production
fiche: done
date: 2026-10-29
benchmarks: none
---

# Remote Control of Greenhouse Vegetable Production with Artificial Intelligence-Greenhouse Climate, Irrigation, and Crop Production

Silke Hemming, Feije de Zwart, Anne Elings, Isabella Righini, Anna Petropoulou, 2019, Sensors 19(8):1807 (revue à comité de lecture ; venue déduite du numéro de pagination « Sensors 2019, 19, 1807 » dans le texte, absente de `metadata.json`). https://doi.org/10.3390/s19081807
Type : article de revue (Sensors, MDPI). Données publiées : doi 10.4121/uuid:e4987a7b-04dd-4c89-9b18-883aad30ba9a.

## Problème

Peut-on piloter à distance, par des algorithmes d'IA, la serre (climat, irrigation, fertigation, consignes de culture) d'une culture commerciale pendant plusieurs mois, avec un rendement comparable à celui de producteurs experts ? Les travaux antérieurs d'IA en serre ne portaient que sur peu de variables et sur des durées courtes (§1).

## Méthode

Concours « Autonomous Greenhouse » 2018 (Wageningen) : 5 équipes (Sonoma, iGrow, deep_greens, The Croperators, AiCU) plus un compartiment de référence conduit par des producteurs néerlandais, 6 compartiments identiques de 96 m² (76,8 m² cultivés), concombre « Hi-Power » en hors-sol laine de roche, 14 août – 7 décembre 2018 (§2.1, §2.3, Fig. 1).
- Interface : consignes (tuyaux de chauffage, température de ventilation, ouverture minimale, déficit d'humidité, écrans, éclairage 0/100 %, CO₂, intervalle d'irrigation) envoyées via LetsGrow.com à un ordinateur climatique Hoogendoorn ; consignes et mesures échangées toutes les 5 min ; EC, pH et composition de la solution ajustables sur analyse du drainage toutes les deux semaines (§2.2).
- Algorithmes : régression dynamique, DRL/DDPG, GAN, CNN, RNN, apprentissage bayésien par renforcement (Sonoma, avec politique experte codée à la main sans apprentissage continu en ligne) ; entraînement initial sur données synthétiques des modèles KASPRO (climat) et INTKAM (culture) (§2.4, §4.2).
- Notation : 50 % profit net, 20 % durabilité, 30 % jury sur l'algorithme (§2.5). Analyse a posteriori : échange de stratégies (culture, lumière, CO₂) entre compartiments avec KASPRO + INTKAM (§2.6).
- Décisions de culture (taille des feuilles et fruits) : fixées par des politiques d'experts pour toutes les équipes sauf The Croperators (§4.2).

## Plateforme et implémentation

Pas de FPGA. Actionneurs standard de serre haute technologie : chauffage rail (180 W/m²) et chauffage culture (30 W/m²), ventilation continue, deux écrans, éclairage HPS 187 µmol/m²/s, brumisation (330 g/m²/h max), CO₂ (15 g/m²/h max) (§2.1). Capteurs standard : météo extérieure et prévisions, T° et déficit d'humidité intérieurs, PAR, apport, drainage, EC et pH du drainage (§2.2). Capteurs additionnels au choix : caméras RGB et thermiques, rayonnement net, zone racinaire, poids culture et substrat, diamètre de tige, sève, réseaux sans fil T/HR/lumière. Code des équipes : non publié dans l'article ; seules les données le sont.

## Résultats

Sources : Tableau 1 (chunk 2019-hemming#065.0), Tableau 2 (2019-hemming#064.0), §3.

| Équipe | Profit net €/m² | Revenu €/m² | Chauffage kWh/kg | Électricité kWh/kg | CO₂ kg/kg | Eau L/kg |
|---|---|---|---|---|---|---|
| Sonoma | 24,78 | 49,60 | 2,49 | 3,59 | 0,20 | 4,91 |
| Référence (producteurs) | 21,18 | 43,94 | 3,20 | 3,02 | 0,20 | 5,52 |
| iGrow | 20,03 | 42,95 | 2,94 | 3,12 | 0,20 | 5,89 |
| The Croperators | 17,15 | 42,82 | 4,87 | 3,82 | 0,29 | 5,98 |
| AiCU | 15,10 | 36,21 | 3,13 | 3,17 | 0,26 | 7,62 |
| deep_greens | 7,38 | 31,88 | 13,61 | 4,39 | 0,47 | 5,87 |

Ce qui a fait la différence (§3, §4.1) :
- Sonoma (gagnante) : lumière maximale (DLI le plus élevé par éclairage artificiel) avec température et CO₂ optimisés, CO₂ augmenté en continu ; consommation la plus basse de chauffage, CO₂ et eau par kg ; électricité moyenne (3,59 kWh/kg contre 3,02 pour la référence). Règle empirique citée : +1 % de lumière donne +1 % de rendement (§4.1) ; électricité bon marché dans le concours.
- Référence : démarrage plus lent (peu de lumière artificielle au début, pour préparer la culture à l'automne), mais le moins de fruits avortés et la meilleure efficacité d'usage de la lumière presque tout le cycle ; électricité la plus basse.
- AiCU : densité de fruits la plus forte, T° basse et DLI faible, d'où un taux d'avortement très élevé, une faible efficacité lumineuse et la pire consommation d'eau (7,62 L/kg).
- The Croperators : environ 30 % de fruits avortés (taille des fruits inadaptée, CO₂ bas), rattrapage en doublant le CO₂ en fin de culture ; taches fongiques en novembre, réponse : arrêt de la brumisation, ouverture des deux ventilations et tuyau rail minimum à 40 °C, avec hausse forte de l'énergie de chauffage.
- deep_greens : air très chaud (cycle du fruit 13,4 j), chauffage 13,61 kWh/kg ; panne de liaison de commande et irrigation presque nulle plusieurs jours en octobre, d'où un creux de récolte jamais rattrapé (profit 7,38).
- Échange de stratégies (modèle) : la référence, iGrow et AiCU auraient gagné avec la stratégie lumière de Sonoma ; une forte densité de fruits ne paie qu'avec lumière, T° et CO₂ élevés (§3, Fig. 13-14). Échanger les stratégies CO₂ a peu changé la production (§4.1).
- Capteurs (§4.3) : aucune corrélation entre nombre ou type de capteurs additionnels et résultat. iGrow, sans aucun capteur additionnel, s'approche de la référence (20,03 contre 21,18). Sonoma n'utilisait qu'un capteur d'humectation foliaire en plus ; ses 8 caméras RGB n'ont pas servi à l'algorithme. The Croperators, avec le plus de capteurs (gouttière de pesée, diamètre de tige, sève), n'en ont tiré aucun avantage net. Les mesures de croissance (élongation, formation de feuilles) étaient prises à la main : les auteurs jugent essentiel de les automatiser.

→ reportés dans `benchmarks.csv` : aucune ligne ajoutée par cet agent. Les colonnes du fichier sont conçues pour des systèmes embarqués ; les chiffres ci-dessus sont des résultats agronomiques (propositions de lignes dans le retour à l'agent principal). `benchmarks: none` au front-matter en attendant.

## Consignes chiffrées

Papier sur le concombre (culture non visée par SerreIA) : il ne publie quasiment aucune plage de consigne par stade (les consignes des équipes sont dans des figures non extraites). Valeurs relevées, `n/r` ailleurs.

| espèce | stade | grandeur | optimal | marginal / limite | unité | condition (jour/nuit, lumière…) | chunk_id |
|---|---|---|---|---|---|---|---|
| concombre | végétatif/fructification | T° air (consigne de l'équipe The Croperators, pendant la lutte contre les taches fongiques) | 19 (nuit) ; 25 (jour) | n/r | °C | nov. 2018, ventilation ouverte, tuyau rail min. 40 °C | 2019-hemming#013.2 |
| concombre | fructification | température minimale du tuyau rail | 40 (valeur appliquée, pas un optimum) | n/r | °C | maintien de la T° pendant la ventilation, pour réduire HR | 2019-hemming#013.2 |
| concombre | fructification | durée de croissance du fruit | 17,3 (moyenne) ; 13,4 (deep_greens, air chaud) ; 21,6 (AiCU, air frais) | 11 à 24 (extrêmes) | jours | corrélée à la T° moyenne, valeur de T° n/r (Fig. 10) | 2019-hemming#012.2 |
| concombre | toute la culture | densité de tiges | 3,3 (Sonoma, gagnante) | 2,6 à 3,6 (plage testée) ; référence 2,5 | tiges/m² | forte densité utile seulement avec lumière, T° et CO₂ élevés | 2019-hemming#006.0 |
| concombre | toute la culture | éclaircissage des fruits | 50 % constant ou 50/67 % alternés | n/r | % de fruits retirés | ~30 % de fruits avortés chez The Croperators (charge trop forte) | 2019-hemming#007.1 |
| concombre | toute la culture | réponse à la lumière | +1 % de lumière = +1 % de rendement (règle empirique citée) | n/r | % / % | cycle d'automne, éclairage HPS | 2019-hemming#017.3 |
| concombre | toute la culture | HR, déficit d'humidité, VPD | n/r | n/r (HR trop haute : taches fongiques, valeur n/r) | n/r | consigne de déficit d'humidité en g/m³, valeurs n/r | n/r |
| concombre | toute la culture | DLI, photopériode, CO₂ (ppm), EC, pH, irrigation | n/r (courbes en Fig. 4, 8, 12 non extraites) | n/r | n/r | n/r | n/r |
| concombre | toute la culture | capacités des actionneurs | éclairage 187 ; brumisation 330 ; CO₂ 15 | n/r | µmol/m²/s ; g/m²/h ; g/m²/h | maximum installé, pas une consigne | 2019-hemming#002.0 |

Écart avec SerreIA : pas de recette concombre dans `recettes.yaml` ; comparaison indirecte seulement. Les 19 °C nuit et 25 °C jour de The Croperators tombent dans les plages de la recette tomate (jour 20-26 / 21-27 °C ; nuit 16-19 °C) pour la nuit et à peu près dedans pour le jour, mais le concombre n'est pas la tomate : à ne pas importer. Pour le risque maladie, le papier ne donne aucun seuil HR, durée ou température : la règle mildiou de SerreIA (HR > 90 % plus de 10 h à 10-25 °C) ne peut être ni confirmée ni infirmée ; il dit seulement qu'une détection visuelle de taches fongiques a déclenché une baisse d'HR par ventilation plus chauffage.

## Limites et critique

- Une seule culture (concombre), une seule saison (automne), un seul site, un essai sans répétition par équipe : pas de test statistique ; écarts de profit entre référence (21,18) et iGrow (20,03) ou The Croperators (17,15) faibles.
- Le jeu de prix et le coût de l'électricité (faible) étaient fixés par le concours ; le coût en capital est exclu. Le profit de Sonoma dépend de ce prix : avec une électricité chère, la stratégie « maximum de lumière » peut ne pas payer (les auteurs le notent, §4.1).
- La politique de Sonoma est une politique experte codée à la main (§4.2) : l'article ne démontre donc pas la supériorité de l'apprentissage ; les décisions de culture sont aussi expertes pour 4 équipes sur 5.
- Seul KASPRO + INTKAM, sans maladies ni ravageurs ni carence d'eau ou de nutriments, sert à expliquer les écarts ; le modèle n'explique pas deep_greens (§3). Les échanges de stratégies ne sont pas croisés entre lumière, culture et CO₂.
- Les consignes et courbes décisives (DLI, CO₂, T°, irrigation) sont dans des figures que l'extraction ne restitue pas ; Tableaux 1 et 2 extraits sans bruit mais « Sonoma » apparaît à 24,78 ou « 24,78 » selon le chunk (coquille d'extraction).
- Table 1 : « CO₂ le plus bas » attribué à Sonoma dans le texte, alors qu'il est à égalité (0,20) avec la référence et iGrow.
- Pas de code publié par les équipes.

## Pertinence pour SerreIA

SerreIA (tomate, laitue hydro, basilic, fraise ; contrôleur à règles, agent LLM) peut en reprendre concrètement :
1. Le protocole d'évaluation : comparer le contrôleur à une référence « conduite manuelle » sur profit net et sur énergie, CO₂ et eau par kg (Tableaux 1 et 2), en notant les ressources par kg de produit plutôt que par m².
2. Une architecture à 3 niveaux (The Croperators, §4.2) : couche haute lisible (objectifs journaliers), couche intermédiaire (trajectoires), couche basse (consignes) ; proche du schéma règles + agent LLM avec validation humaine de SerreIA.
3. Des garde-fous issus d'échecs : coupure de liaison de commande et irrigation presque nulle plusieurs jours (deep_greens) ont ruiné le résultat : alarme sur irrigation absente, mode dégradé si le lien MQTT tombe ; la réaction à des taches fongiques (arrêt brumisation, ventilation, chauffage de maintien) comme règle de repli à tester avec la règle mildiou.
4. Le message sur les capteurs : le meilleur résultat n'a pas exigé de capteurs sophistiqués (Sonoma : un capteur d'humectation foliaire ; iGrow : aucun) ; aucune raison d'alourdir le matériel de SerreIA tant que le temps de réponse des mesures de croissance reste manuel.
5. L'importance de la lumière et du CO₂ comme leviers de rendement (valable qualitativement pour la tomate et le basilic), et l'équilibre charge en fruits / lumière (tomate : taille des fruits ou des fleurs). Les chiffres concombre ne sont pas transposables.
Ce que le papier laisse ouvert : aucune plage de consigne par stade, rien sur laitue, basilic ou fraise, rien sur pH/EC cibles ni sur un modèle de risque maladie.

## Gaps identifiés

- Consignes chiffrées détaillées de l'équipe gagnante (jeu de données publié sous doi 10.4121) : à récupérer pour obtenir des plages réelles de T°, HR, CO₂, DLI.
- Aucun seuil de risque maladie (HR, durée) : à chercher dans la littérature phytopathologie.
- Pas de comparaison de coût avec électricité chère ; sensibilité du profit au prix de l'énergie non traitée.
- Capteurs de croissance automatiques (élongation, fruits) : manque identifié par les auteurs.

## Statut de lecture

Papier complet, lu par sections via `Read` ; tableaux 1 et 2 relus par `bin/pdb show`. Les figures (3-14, A1-A5) ne sont pas extraites : leurs valeurs (DLI, CO₂ en ppm, T° moyennes, irrigation, avortements) ne sont pas lues ; seul le texte qui les décrit est rapporté. Extraction GROBID `ok`, avertissement « tableaux sans corps extrait » concerne des légendes sans valeurs utiles ici. Déduit et non affirmé par les auteurs : l'écart avec SerreIA, la remarque sur l'électricité chère, la pertinence pour tomate/basilic, le fait que les politiques de Sonoma n'apprennent pas en ligne (les auteurs disent qu'elle s'appuie sur une politique experte « sans apprentissage continu »).
