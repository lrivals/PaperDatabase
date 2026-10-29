---
id: 2017-zhang-vapour-pressure-deficit-control-relation
fiche: done
date: 2026-10-29
benchmarks: none
---

# Vapour pressure deficit control in relation to water transport and water productivity in greenhouse tomato production during summer

Dalong Zhang, Qingjie Du, Zhi Zhang, Xiaocong Jiao, Xiaoming Song, Jianming Li, 2017, Scientific Reports 7, 43461. https://doi.org/10.1038/srep43461
Type : article de revue (journal), relu par les pairs.

## Problème

Réguler le VPD (déficit de pression de vapeur) devrait réduire le moteur de la transpiration,
donc la consommation d'eau de la plante, mais l'eau de brumisation consommée pour réguler le
VPD n'est pas prise en compte dans cette hypothèse. Les auteurs posent le compromis entre
transpiration évitée et eau de brumisation ajoutée comme « très incertain » (#001.0).

## Méthode

Deux serres voisines identiques (15 × 10 × 3,5 m, Yangling, Chine, mars-juin 2016), tomate
cv. DiFen en pots de 40 cm, 3 plantes m-2, 2 inflorescences gardées par plante, 90 jours après
repiquage environ (#009.1). Traitement « VPD haut » : serre non régulée, VPD de midi 4-5 kPa.
Traitement « VPD bas » : brumisation (binary fluid mist, 2-6 MPa, gouttes 25,8-66,2 µm),
déclenchée quand le VPD dépasse 1,2 kPa et coupée à 0,5 kPa, visant 1-2 kPa à midi
(#009.2). Plan en blocs complets randomisés, 5 répétitions par traitement, 10 plantes par bloc
(#009.2). Sol maintenu à 85-90 % de la capacité au champ, irrigation = transpiration, mesurée
par pesée quotidienne des pots (#009.1). Mesures : potentiel hydrique foliaire, conductance
hydraulique, température de canopée (thermomètre IR), CWSI, échanges gazeux (LI-6400),
biomasse, rendement, WUE.

## Plateforme et implémentation

Pas de plateforme matérielle de calcul. Capteurs T/HR/lumière ZDR-20j à 2,5 m de hauteur au
centre de chaque serre, pas de 10 min, étalonnés avant l'essai (#009.2) ; VPD calculé à partir
de T et HR instantanées. Régulation par brumisation haute pression avec seuils d'hystérésis
(on 1,2 kPa / off 0,5 kPa). Code ou données brutes : non publiés (matériel supplémentaire
cité, non lu ici).

## Résultats

Traitement VPD bas par rapport au témoin VPD haut :
- VPD moyen 11:00-15:00 : 4,5 → 1,6 kPa ; HR de midi 42,5 → 61,6 % ; T air de midi 38,5 → 31,3 °C (#002.0) ; rayonnement inchangé (#002.0).
- Midi : Ψfeuille -1,47 → -1,03 MPa ; K plante 8,73 → 11,8 mmol m-2 s-1 MPa-1 ; T canopée 33,7 → 31,3 °C ; CWSI 0,367 → 0,272 ; RWC 78,2 → 84,6 % (Table 1, #019.0). Ψ de pré-aube sans écart (NS).
- Conductance stomatique, photosynthèse et CO2 intercellulaire plus hauts ; transpiration foliaire et WUE intrinsèque plus bas (Fig. 2, #003.0), sans valeurs numériques dans le texte.
- Biomasse de plante entière +27,3 % ; biomasse racinaire plus faible (Fig. 3, #004.0). Rendement par plante +22,7 % ; acidité et sucres des fruits sans écart (Fig. S3, #004.1).
- Transpiration cumulée -19,9 % par plante ; WUE irrigation biomasse +36,8 %, rendement +39,1 % (Fig. 5-6, #005.0).
- Eau de brumisation cumulée 31,8 kg m-2 ; économie nette d'eau positive seulement à partir de 9 plantes m-2 (négative en dessous, donc négative dans l'essai à 3 plantes m-2) (Fig. 7, #005.1, #007.1).

Aucune configuration de type benchmark matériel : `benchmarks: none`, rien ajouté à `benchmarks.csv`.

## Consignes chiffrées

| espèce | stade | grandeur | optimal | marginal / limite | unité | condition | chunk_id |
|---|---|---|---|---|---|---|---|
| tomate (cv. DiFen) | croissance et fructification (jusqu'à ~90 j après repiquage) | VPD, consigne de midi | 1-2 | témoin non régulé 4-5 : stress hydrique (CWSI 0,367, Ψ -1,47 MPa) | kPa | midi, serre en été ; brumisation | #009.2 |
| tomate | idem | VPD, seuils de brumisation | on > 1,2 ; off à 0,5 | n/r | kPa | hystérésis du régulateur (« valeurs recommandées pour la tomate ») | #009.2 |
| tomate | idem | VPD mesuré 11-15 h | 1,6 (traité) | 4,5 (non traité) | kPa | jour ensoleillé | #002.0 |
| tomate | idem | HR de midi | 61,6 | 42,5 | % | midi, traité vs non traité | #002.0 |
| tomate | idem | T air de midi | 31,3 (traité) | 38,5 (non traité) ; T > 35 observée au témoin | °C | midi, jour ensoleillé ; effet du refroidissement évaporatif | #002.0 |
| tomate | idem | T canopée de midi | 31,3 | 33,7 | °C | midi | #019.0 |
| tomate | idem | CWSI de midi | 0,272 | 0,367 | sans unité | midi | #019.0 |
| tomate | germination / semis (4 semaines, 4 vraies feuilles) | T jour / nuit | 22 / 18 | n/r | °C | chambre de culture | #009.0 |
| tomate | semis | PPFD | 400 | n/r | µmol m-2 s-1 | lampes fluorescentes blanches ; photopériode n/r | #009.0 |
| tomate | croissance | humidité du substrat | 85-90 | n/r | % capacité au champ | pots 40 cm, pesée quotidienne | #009.1 |
| tomate | croissance | densité de plantation | ≥ 9 pour économie nette d'eau positive avec brumisation | 3 : économie nette négative | plantes m-2 | brumisation à efficacité d'évaporation faible | #007.1 |
| tomate | n/r | DLI, photopériode, CO2 ambiant, pH, EC, T racinaire | n/r | n/r | n/r | non rapportés (CO2 400 ppm uniquement dans la chambre de mesure foliaire) | #010.0 |

Écart avec SerreIA : les recettes tomate (`tomate-standard`, croissance/fructification) donnent
T jour 20-26/21-27 °C et HR 55-75 % mais n'ont pas de consigne de VPD. Converties en VPD (calcul
de ma part, déduit, pas dans le papier), HR 55-70 % à 21-27 °C équivaut à environ 0,95-1,6 kPa : la
plage de recettes.yaml tombe dans la cible 1-2 kPa de l'article, et son plafond d'HR (70 %) reste
sous l'arrêt de brumisation à 0,5 kPa (HR ~84 % à 25 °C). Écart majeur : l'article ne couvre que
l'été chaud (témoin 38,5 °C, traité 31,3 °C, au-dessus du plafond jour de 27 °C de SerreIA) et
ne donne ni DLI, ni photopériode, ni pH/EC, ni plage de HR optimale ; il ne permet de valider
aucune de ces plages. Sur le mildiou (HR > 90 % plus de 10 h à 10-25 °C) : un VPD bas pousse
l'HR vers ce seuil, l'article ne l'évoque pas et son optimum de 1-2 kPa est loin de HR > 90 % (VPD
< 0,3 kPa à 25 °C, déduit).

## Limites et critique

- Une seule espèce, un seul cultivar, un seul site et une seule saison (printemps-été 2016) ; deux serres seulement (un traitement par serre, blocs à l'intérieur : pseudo-réplication possible, non discutée).
- Plantes en pots avec sol bâché, irrigation = transpiration mesurée : le gain d'eau d'irrigation (-19,9 %) est un résultat de bilan physiologique, pas d'un pilotage d'irrigation réel.
- Le VPD n'est pas isolé : la brumisation baisse aussi T air (-7,2 °C à midi) et T feuille ; l'effet « VPD » est confondu avec l'effet « température ». Les auteurs ne séparent pas les deux.
- Densité de 3 plantes m-2 : l'économie nette d'eau y est négative ; le seuil de 9 plantes m-2 est une extrapolation d'un modèle empirique (hypothèse de croissance et microclimat identiques, Fig. 7), non testée.
- Brumisation à grosses gouttes, faible efficacité d'évaporation ; mouillage du feuillage non évalué, donc aucun lien avec le risque de maladie fongique. Un seul capteur par serre à 2,5 m.
- Consignes données uniquement pour le VPD et la phase estivale ; pas de comparaison entre niveaux intermédiaires (deux niveaux seulement, pas de courbe réponse).

## Pertinence pour SerreIA

À reprendre concrètement :
1. Ajouter une consigne VPD au contrôleur (tomate) : cible 1-2 kPa à midi, avec hystérésis humidification on > 1,2 kPa / off à 0,5 kPa (#009.2). Le VPD se calcule à partir des capteurs T/HR déjà sur le bus MQTT.
2. Utiliser le VPD comme variable de décision de l'agent LLM et des règles d'été (T > 35 °C, VPD > 4 kPa : régime de stress, CWSI 0,37 contre 0,27) plutôt que HR seule.
3. Garde-fou mildiou : tout humidificateur ou brumisateur doit respecter la règle HR > 90 % pendant plus de 10 h, car l'article ne mesure pas le risque fongique ; seuil d'arrêt bas (0,5 kPa) à vérifier contre cette règle.
4. Bilan d'eau : compter l'eau d'humidification dans l'efficience d'eau de SerreIA ; à faible densité elle annule le gain d'irrigation (#007.1).
5. Gain attendu à citer prudemment : rendement +22,7 %, biomasse +27,3 % en été chaud, à ne pas extrapoler à des serres tempérées régulées.

## Gaps identifiés

- VPD optimal par stade de tomate (semis, floraison, fructification) : l'article ne distingue pas les stades ; recettes.yaml n'a pas de VPD.
- Effet couplé VPD / risque mildiou et botrytis (HR élevée, mouillage du feuillage) : non traité.
- Laitue hydro et basilic : aucune consigne VPD ici.
- VPD et T séparés (essai factoriel) : confusion non levée.

## Statut de lecture

papier complet (140 lignes de `fulltext.md` lues ; extraction grobid ok). Matériel supplémentaire
(Fig. S1-S5, Table S1-S2, Note 1) non disponible : les valeurs des figures 2-7 ne sont donc pas
lues, seulement les pourcentages du texte. Déduit et non affirmé par les auteurs : conversion des
plages d'HR de recettes.yaml en VPD ; confusion VPD/température ; lien avec la règle mildiou ;
densité d'économie d'eau nulle à 9 plantes m-2 est affirmée par les auteurs (modèle empirique).
