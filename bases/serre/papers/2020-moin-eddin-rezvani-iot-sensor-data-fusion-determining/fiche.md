---
id: 2020-moin-eddin-rezvani-iot-sensor-data-fusion-determining
fiche: done
date: 2026-10-29
benchmarks: none
---

# IoT-Based Sensor Data Fusion for Determining Optimality Degrees of Microclimate Parameters in Commercial Greenhouse Production of Tomato

Sayed Moin-Eddin Rezvani, Hamid Zare Abyaneh, Redmond R Shamshiri, Siva K Balasundram, Volker Dworak, Mohsen Goodarzi, Muhammad Sultan, Benjamin Mahns, 2020, Sensors 20(22):6474 (MDPI, revue à comité de lecture ; la venue vient du numéro de pagination du texte, `metadata.json` ne la porte pas). https://doi.org/10.3390/s20226474
Type : journal

## Problème

Dans une serre commerciale de tomate (Iran, 4333 m²), les consignes de T, HR et VPD ne sont pas tenues et le chauffage/refroidissement est piloté par minuterie. Les auteurs veulent mesurer la variation spatiale et temporelle du microclimat et la résumer en un indice normalisé 0–1 (« Optimality Degree », OptDeg) lisible par un exploitant (§1, §2.1, résumé 000.1).

## Méthode

- Réseau de 20 nœuds sans fil (LoRaWAN, 433 MHz) sur deux hauteurs, plus station météo extérieure ; passerelle LoRaWAN avec Raspberry Pi Zero ; enregistreurs redondants à stockage embarqué ; tableau de bord web et application Android (§2.2, 007.1). Mesure à 1 Hz, moyennes minute et horaire calculées sur le nœud (§2.2-2.3). Résolution déclarée 0,01 °C et 1 % HR ; capteurs certifiés lors d'un étalonnage officiel (Leibniz, Potsdam) (006.4).
- OptDeg : fonctions d'appartenance par stade de croissance (3 stades notés GS1, GS2, GS3-5) et condition lumineuse (soleil, nuageux, nuit) ; OptDeg = 1 dans la plage optimale, 0 à la valeur « d'échec », interpolation linéaire (T, HR) ou exponentielle (VPD) entre les deux (Tables 2-3, 009.4). VPD = (1 − HR/100) × 0,611 × exp(17,27 T / (T + 237,3)) (Éq. 1, 010.0).
- Quatre campagnes d'un jour : 10 et 17 janvier, 10 juin, 29 juillet 2018 (§3). Traitement hors ligne sous MATLAB Simulink (AAF). Chauffage par aérothermes, extraction forcée, pas de pad humide.

## Plateforme et implémentation

Nœuds ADP-AgroTech (Adaptive AgroTech, Malaisie), alimentés par batterie LiPo 3,7 V 1200 mAh et solaire, boîtier IP68 ; passerelle sur Raspberry Pi Zero, boîtier IP66 (§2.2, 007.1). Pas de puissance mesurée. Code et matériel : fournisseur commercial, personnalisés ; outil AAF/OptDeg sous MATLAB, non publié ici (renvoi aux réf. [16,17]). Pas d'inférence embarquée.

## Résultats

- OptDeg moyens T / HR / VPD : 0,67 / 0,94 / 0,94 en janvier ; 0,45 / 0,36 / 0,42 en juin ; 0,44 / 0,00 / 0,12 en juillet (résumé, 000.1).
- Moyennes saison froide à 1,4 et 2,2 m : T 0,65 et 0,73, HR 0,935 et 0,94, VPD 0,92 et 0,985 ; saison chaude : T 0,455 et 0,43, HR 0,215 et 0,16, VPD 0,295 et 0,245 (§5, 028.1).
- Même avec un OptDeg moyen de 0,8 à 1, des zones et des heures descendent sous 0,3 (« points critiques ») (§5, 028.1).
- Juillet : température horaire moyenne de 19,6 à 51,2 °C, VPD horaire maximal 5,61 kPa (§3.2, Table 4).
- Pas de ligne `benchmarks.csv` : étude de terrain sans modèle ni mesure de performance de calcul (`benchmarks: none`). Le corps de la Table 4 n'est pas extrait.

## Consignes chiffrées

Valeurs vérifiées dans le texte ; les bornes détaillées de la Table 1 (par stade et lumière) n'ont pas de corps extrait : `n/r`, jamais estimées. Valeurs reprises par les auteurs de leurs réf. [16,26,29] (pas de mesure propre). Tomate de serre commerciale.

| espèce | stade | grandeur | optimal | marginal / limite | unité | condition | chunk_id |
|---|---|---|---|---|---|---|---|
| tomate | début de croissance (GS1) | température | 24,0–26,1 | échec 9 et 35 | °C | OptDeg = 1 dans l'optimum, 0 aux valeurs d'échec | 014.2 |
| tomate | végétatif à fructification mûre | température | 24–27 | n/r | °C | lumière du jour (« sun ») | 009.2 |
| tomate | stade non précisé | température | n/r | maximum à ne pas dépasser : 35 | °C | texte, saison chaude | 021.0 |
| tomate | stade non précisé | température, minimum de jour | n/r | 19 (« daytime minimum ») | °C | saison froide | 014.5 |
| tomate | stade non précisé | humidité relative | 60–80 | n/r | % | saison froide | 014.1 |
| tomate | stade non précisé | VPD | n/r | > 2 : forte transpiration, fermeture stomatique | kPa | été, jours chauds ; le papier renvoie à [29] pour la plage | 009.3 |
| tomate | tous | VPD, humidité de substrat, CO₂, DLI, photopériode, pH, EC | n/r | n/r | n/r | non traités | n/r |

Écart avec SerreIA (`edge/controller/recettes.yaml`, tomate-standard) : SerreIA fixe, pour la croissance, jour 20–26 °C, nuit 16–18 °C, HR 60–75 %, et pour floraison/fructification jour 21–27 °C, HR 55–70 %. L'optimum de jour de cet article (24–27 °C, 009.2) est dans la plage SerreIA ; l'optimum de début de croissance (24,0–26,1 °C, 014.2) est plus étroit et plus chaud que la plage semis de SerreIA (jour 20–25 °C), et sa limite haute d'échec de 35 °C n'a pas d'équivalent dans le fichier. HR 60–80 % (014.1) déborde de 5 points la borne haute de croissance de SerreIA (75 %) et de 10 points celle de fructification (70 %) : à ne pas reprendre telle quelle, la règle mildiou de `risk.py` (HR > 90 % pendant plus de 10 h) y suffit. Pas de comparaison possible sur VPD, CO₂, DLI, pH, EC (absents de `recettes.yaml` pour le VPD, non traités ici).

## Limites et critique

- Quatre journées seulement, une seule serre (climat iranien, 1617 m), pas de données de rendement : l'OptDeg n'est jamais relié à une mesure de croissance ou de qualité des fruits dans ce papier ; sa validité dépend des réf. [16,26,29,31], des mêmes auteurs.
- Les plages de référence (Table 1) ne sont pas dans le texte extrait ; les courbes d'appartenance de Tables 2-3 sont écrites de façon peu lisible dans l'extraction.
- Constats de commande (minuteries, absence de refroidissement évaporatif) : conclusions du terrain, non testées par un essai de contrôle ; la recommandation d'un pad humide reste une inférence des auteurs (§4, 5).
- Étalonnage « certifié » invoqué mais sans protocole ni incertitude chiffrée de la chaîne complète (006.4). Pas de taux de perte de paquets LoRa ni de portée rapportés dans les sections lues.
- Perspective annoncée : couplage avec un modèle CFD (028.2).

## Pertinence pour la thèse

Pour SerreIA, intérêt modeste mais concret : (1) l'idée d'un indice 0–1 par grandeur et stade, plus parlant que la violation binaire d'une plage, comme score de risque pour `risk.py` et comme résumé que l'agent LLM présente à l'humain ; (2) la fusion de nœuds répartis sur deux hauteurs montre un écart horizontal et vertical réel de T, HR, VPD, donc un point de mesure unique est insuffisant pour des consignes strictes ; (3) la formule du VPD (010.0) à ajouter si le contrôleur raisonne en VPD. L'architecture LoRaWAN n'est pas celle de SerreIA (ESP32 + MQTT, un seul site) ; peu de transfert direct. Ouvert : calibration de l'indice, lien avec le rendement.

## Gaps identifiés

- Plages de VPD par stade et lumière absentes de `recettes.yaml` et non extraites ici (Table 1) : à chercher dans la réf. [29] du papier.
- Aucune mesure reliant un indice d'optimalité au rendement.
- Hétérogénéité spatiale (sous 0,3 localement) : combien de capteurs pour une petite serre ?

## Statut de lecture

Sections lues : résumé, §2.1-2.3, §3.1-3.5 (par extraits), §4, §5 ; passages vérifiés par `bin/pdb verify`. Extraction : GROBID, texte dupliqué par endroits ; tableaux Table 1 et Table 4 sans corps extrait (cités par la légende seule), Tables 2-3 en texte brut peu lisible. Papier lu en extraits ciblés, non intégralement.
Déduit et non affirmé par les auteurs : tout le paragraphe « Écart avec SerreIA » et la section « Pertinence » ; type `journal` déduit du format MDPI « Sensors 2020, 20, 6474 ».
