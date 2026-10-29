---
id: 2020-hemming-cherry-tomato-production-intelligent-greenhouses
fiche: done
date: 2026-10-29
benchmarks: none
---

# Cherry Tomato Production in Intelligent Greenhouses-Sensors and AI for Control of Climate, Irrigation, Crop Yield, and Quality

Silke Hemming, Feije De Zwart, Anne Elings, Anna Petropoulou, Isabella Righini, 2020, Sensors 20(22), 6430. https://doi.org/10.3390/s20226430
Type : article de revue (MDPI Sensors), relu par les pairs ; expérience en serre, six compartiments de 96 m² (§2.1, #003.0).

## Problème

Les serres ont besoin de contrôle autonome et distant (main-d'œuvre qualifiée rare, COVID-19). Question : des équipes d'IA, pilotant à distance un compartiment de serre pendant six mois de tomate cerise, font-elles mieux que des producteurs néerlandais ? Critère : profit net, sous contrainte de qualité (Brix) et de ressources (Abstract, §1).

## Méthode

Second « Autonomous Greenhouse Challenge » (WUR, Bleiswijk, NL). Cinq équipes (Automatoes, AiCU, DIGILOG, IUA.CAAS, The Automators) pilotent chacune un compartiment (306, 302, 305, 304, 301) ; le compartiment 303, conduit par des producteurs, sert de référence (§2.2, #003.0). Tomate cerise « Axiany » greffée Maxifort, semée le 19/10/2019, plantée le 16/12/2019, récolte du 13/02 au 29/05/2020 (§2.4).

- Actionneurs pilotés par les équipes : lampes HPS et LED (4 canaux), écrans énergie et occultant, T° mini des deux circuits de chauffage, ouverture mini des ouvrants, T° de ventilation, consigne de déficit d'humidité (g/m³), CO₂ (ppm), intervalle entre irrigations (min), composition, EC et pH de la solution (§2.2).
- Capteurs standard (échange toutes les 5 min) : météo extérieure et prévisions, climat intérieur (T°, humidité absolue, CO₂, état des lampes et écrans), fertigation (apport, drainage, EC et pH du drain, EC, pH et T° dans le slab) (§2.3, #005.1). Capteurs ajoutés au choix des équipes : boîtes aspirées, PAR, pyranomètres, balances de slab, flux de sève, diamètre de tige, thermomètre IR, caméras RGB et thermiques, capteurs de teneur en eau du substrat (§2.3 ; §4.2).
- Observations de culture saisies à la main chaque semaine sur tablette (10 plantes : élongation, diamètre de tige, durée de croissance du fruit, formation des bouquets) ; charge en fruits estimée ; qualité en laboratoire (Brix, acidité, jus, fermeté) (§2.4).
- Algorithmes des équipes : systèmes hybrides mêlant règles d'expert, contrôle et prédiction : MPC, NMPC, DeePC, LSTM et BiLSTM, apprentissage par renforcement, imitation learning (#004.2). L'équipe 306 (meilleur profit) : trois niveaux de décision, stratégique (nombre de tiges, effeuillage, ratio T°-lumière), tactique (consignes de base sur 24 h d'après prévisions météo) et opérationnelle ; MPC et DeePC ; irrigation fondée sur le rayonnement solaire cumulé et le gradient de teneur en eau du slab après la dernière irrigation ; ouverture directe des ouvrants au lieu de la T° de ventilation et de la bande P (#031.3, #031.4). Les équipes ont pu s'entraîner avant l'essai sur un greenhouse virtuel (jumeau KASPRO + INTKAM) (§4.2).
- Évaluation : profit net = revenu (kg × prix selon Brix et saison) − coûts (jeunes plants, électricité, chauffage, CO₂, eau, nutriments, main-d'œuvre) (§2.6) ; analyse de sensibilité par le jumeau numérique (lumière ±3 h/j, CO₂ -100 à +50 ppm et capacité 50 à 200 kg/ha/h, T° ±2 °C) (§2.7, #025.2).

## Plateforme et implémentation

Serre haute technologie vitrée, 6 compartiments de 96 m² (#003.0) : 6 lampes HPS (100 µmol/m²/s) et 8 LED multispectres (0 à 109 µmol/m²/s), chauffage par rail au sol (180 W/m²) et au niveau de la culture (30 W/m²), ventilation continue en toit avec filet anti-thrips, brumisation (330 g/m²/h max), apport de CO₂ (15 g/m²/h max), culture sur laine de roche (Grodan GT Master), gouttiers surélevés, goutteurs sur pompe tout ou rien (§2.1). Interface : LetsGrow.com (API REST) vers un calculateur Hoogendoorn (§2.2). Pas de matériel embarqué ni de FPGA. Jeu de données public (DOI 10.4121/uuid:88d22c60-21b3-4ea8-90db-20249a5be2a7) ; code des équipes non publié dans le papier (n/r).

## Résultats

Classement au profit net (Table 3, #136.0), €/m², 16/12/2019 au 29/05/2020 :

| Équipe | Coûts | Revenu | Profit net |
|---|---|---|---|
| 306 | 26,07 | 37,22 | 6,86 |
| 302 | 25,04 | 35,27 | 6,27 |
| 305 | 28,64 | 35,09 | 3,59 |
| 304 | 25,36 | 33,00 | 3,35 |
| 301 | 29,58 | 36,73 | 3,19 |
| 303 (référence humaine) | 29,38 | 35,56 | 3,10 |

Les cinq équipes d'IA dépassent la référence (« All AI operated greenhouses were able to reach higher net profits than the reference », #024.1). Le profit de 306 vaut 2,2 fois celui de la référence (6,86 / 3,10, calcul de la fiche).

Efficacité des ressources (Table 2, #135.0), par kg de tomate : chaleur (MJ), électricité (kWh), CO₂ (kg), eau (L), nutriments (g) :

| Équipe | Chaleur | Électricité | CO₂ | Eau | Nutriments |
|---|---|---|---|---|---|
| 306 | 12,9 | 18,7 | 0,63 | 25,0 | 83,0 |
| 302 | 18,5 | 17,6 | 0,74 | 25,2 | 81,0 |
| 301 | 25,3 | 19,9 | 0,87 | 25,9 | 78,0 |
| 304 | 25,9 | 17,7 | 0,56 | 26,9 | 90,0 |
| 305 | 12,8 | 24,0 | 0,72 | 27,9 | 100,0 |
| 303 (réf.) | 33,0 | 19,0 | 0,60 | 27,4 | 99,0 |

- Ce qui a fait la différence. La référence est la pire en efficacité (chauffage, eau, nutriments les plus élevés) malgré une production élevée (§3.4, #135.0). Son doublement de la densité de tiges à 8,0 tiges/m² en fin de cycle (pour deux bouquets de plus par tige) a fait grimper la main-d'œuvre et baissé le profit (§3.3, #019.0). L'équipe 306 combine T° élevées, humidité haute et ventilation limitée, d'où la meilleure efficacité de chauffage malgré ses T° les plus hautes (23,25 °C de moyenne, Table 1) (§3.1, #011.2), une charge en fruits moyenne, une densité de 5,85 tiges/m² dès fin mars, un apport d'eau faible (430 L/m² d'absorption contre 450 en moyenne, #013.0) et une qualité élevée en début de saison, quand les prix sont les plus hauts (§3.3). La conduite de culture (densité de tiges, charge en fruits, date d'étêtage) pèse autant que le climat (§5).
- Eau. Apport de 533 L/m² (302) à 832 L/m² (304) ; absorption de 334 à 537 L/m² après réutilisation du drainage (#013.0).
- CO₂. Dosage de 7,2 kg/m² (303) à 11,7 kg/m² (301) (#025.2). Réduire le CO₂ réduit la production, jusqu'à 0,72 kg/m² soit 1,80 €/m² pour 301, bien plus que l'économie de CO₂ à 0,08 €/kg ; en monter le dosage rapporte peu : les équipes étaient près de l'optimum (#025.2). En été, le CO₂ ajouté s'échappe par les ouvrants (#029.4).
- Lumière. Levier le plus fort du profit net, devant CO₂ et T° (§3.6, §5). Un algorithme d'optimisation des heures de lampe simule +3,6 €/m² pour 302 (le moins éclairé) et +1,4 €/m² pour 306 (un peu moins de lumière au début, un peu plus à la fin) (#027.0). Les jeunes plantes sont limitées par les puits (« sink limited ») : de la lumière en plus coûte sans gain ; sur plante adulte, limitée par la source, elle est rentable (#030.2, #030.3).
- Température. Cadence de formation des bouquets de 1,1 par semaine à 19 °C de moyenne journalière à 1,47 par semaine à 24 °C (#030.0). Sur ±2 °C, simulation : gains de profit faibles (§3.6).
- Qualité. Brix moyen 8,7 et matière sèche 9,0 %, sans effet de l'EC du drain sur le Brix pour cette variété (#029.2). L'équipe 305 a le Brix et la saveur les plus hauts mais un profit moyen (3,59, #089.0).
- Rendement en kg/m² : n/r en valeur dans le texte (courbes seules, Fig. 16). Table 1 (#133.0) : bouquets par tige de 21,7 (304) à 23,8 (301), fruits/m² de 1165 (302) à 1577 (301), T° moyenne de l'air de 21,34 à 23,25 °C.
- Humain dans la boucle : aucune équipe n'a atteint l'autonomie complète, toutes gardent un humain dans la décision (#032.0), et les opérations de culture (effeuillage, taille des fruits) restent manuelles sur instructions hebdomadaires (§2.2).

→ reportés dans `benchmarks.csv` : aucune ligne (les colonnes de `benchmarks.csv` décrivent des modèles embarqués ; ces résultats de serre sont repris ci-dessus et dans les consignes).

## Consignes chiffrées

Le papier ne publie pas de plages de consigne par stade : les consignes d'équipes sont des courbes (Fig. 3 à 11) non extraites en texte. Seules les valeurs ci-dessous sont dans le texte ; les autres grandeurs valent `n/r`. Vérifié par `bin/pdb verify`.

| espèce | stade | grandeur | optimal | marginal / limite | unité | condition | chunk_id |
|---|---|---|---|---|---|---|---|
| tomate cerise Axiany | cycle complet | T° air moyenne (réalisée, 6 équipes) | 21,34 à 23,25 (306 : 23,25, meilleur profit) | n/r | °C | moyenne sur le cycle, jour et nuit confondus | 133.0 |
| tomate cerise | génératif | T° air jour / nuit | n/r | n/r | °C | n/r | n/r |
| tomate cerise | génératif | cadence de formation des bouquets | 1,1 (19 °C) à 1,47 (24 °C) | n/r | bouquets/semaine | T° moyenne journalière, linéaire | 030.0 |
| tomate | tout stade | plage où la photosynthèse varie peu avec la T° | 18 à 24 | n/r | °C | citation [62] ; la T° joue surtout sur la respiration d'entretien | 030.0 |
| tomate cerise | tout stade | humidité (HR ou déficit) | n/r (l'équipe 306 laisse monter l'humidité et limite la ventilation pour économiser du chauffage) | n/r | g/m³ (déficit) | n/r | 011.2 |
| tomate cerise | tout stade | VPD | n/r | n/r | kPa | n/r | n/r |
| tomate cerise | tout stade | CO₂ réalisé pendant la photopériode | 600 à 900 (milieu de saison) | 400 à 600 en fin de saison (fenêtres ouvertes) | ppm | période d'éclairage | 012.0 |
| tomate cerise | tout stade | dosage de CO₂ cumulé | 7,2 (303) à 11,7 (301) | n/r | kg/m² | cycle complet ; capacité max installée 15 g/m²/h | 025.2 |
| tomate cerise | tout stade | sensibilité CO₂ simulée | n/r | consigne -100 ppm : perte jusqu'à 0,72 kg/m² (1,80 €/m²) | ppm, kg/m² | simulation INTKAM | 025.2 |
| tomate cerise | adulte | éclairage artificiel : heures de lampe | n/r | n/r | h/j | simulation ±3 h/j : effet sur le profit supérieur à CO₂ et T° ; lampes surtout hiver et début de printemps, pas en été | 027.0 |
| tomate cerise | juvénile | éclairage artificiel | n/r | rien à gagner (limitation par les puits) | n/r | plantes jeunes | 030.2 |
| tomate cerise | tout stade | part de PAR venant des lampes | 41 % (302, 304) à 48 % (305) | n/r | % du PAR total | cycle complet | 011.2 |
| tomate cerise | tout stade | DLI, photopériode | n/r | n/r | mol/m²/j, h | n/r | n/r |
| tomate cerise | tout stade | apport d'irrigation | 533 (302) à 832 (304) ; moyenne d'absorption 450 ; 306 : 430 | n/r | L/m² | cycle complet, laine de roche, drainage réutilisé | 013.0 |
| tomate cerise | tout stade | pH, EC (apport et drain) | n/r (EC du drain « assez stable » selon les équipes, valeurs en figure) | n/r | n/r | un pic d'EC chez 305 sans effet net sur le Brix | 015.1 |
| tomate cerise | fruit | Brix moyen | 8,7 | n/r | °Brix | tous compartiments ; sans effet de l'EC du drain | 029.2 |
| tomate cerise | tout stade | densité de tiges | 2,6 à 4,0 initiale ; 4,5 à 5,8 en cours de cycle ; 306 : 5,85 depuis fin mars | 8,0 (référence, fin de cycle) : coût de main-d'œuvre trop haut | tiges/m² | haut-fil, 2 tiges par jeune plant | 007.1 |
| tomate cerise | tout stade | charge en fruits | 500 à 800 | n/r | fruits/m² | taille des fruits par les équipes | 007.1 |
| tomate cerise | bouquet | fruits par bouquet | n/r | 16 (bouquet simple), 20 (bouquet fendu), contrainte du protocole | fruits/bouquet | récolte par bouquet | 029.1 |
| tomate cerise | tout stade | seuil de risque maladie | n/r | n/r | n/r | n/r | n/r |

Écart avec SerreIA (recette `tomate-standard`, `recettes.yaml`, lecture seule) : (1) T° : la moyenne réalisée de 21,3 à 23,3 °C du papier tombe dans les plages jour 20-27 / nuit 16-19 °C de SerreIA, mais le papier ne donne aucun jour/nuit ni stade et la meilleure équipe est la plus chaude (23,25 °C), alors que SerreIA vise en moyenne un peu moins : pas de contradiction, simplement non comparable. (2) CO₂ : le papier réalise 600 à 900 ppm et juge qu'au-delà le gain est négligeable ; le `co2_max` de 1200 ppm de SerreIA est donc un plafond sans intérêt économique en serre fermée, et en été le CO₂ fuit par les ouvrants. (3) HR 55-75 % de SerreIA : n/r dans le papier, qui indique seulement qu'une humidité haute avec peu de ventilation économise du chauffage. (4) DLI 20-25 mol/m²/j, photopériode 14-16 h, pH 5,8-6,3, EC 2,0-3,5 : n/r dans le papier. (5) Écart majeur : le papier travaille en serre haute technologie avec éclairage d'appoint HPS/LED, chauffage et CO₂, sur laine de roche ; SerreIA est plus petite et sans valeurs de ce papier pour les stades. Aucune règle mildiou (HR > 90 % plus de 10 h à 10-25 °C) n'est dans ce papier : n/r.

## Limites et critique

- Un seul site, une seule saison (hiver-printemps), une variété de tomate cerise, cinq équipes, sans répétition : le classement tient à la conduite de culture autant qu'à l'algorithme, que le papier ne sépare pas. Pas de test statistique.
- Aucune ablation des algorithmes : on ne sait pas si MPC, DeePC, LSTM ou RL expliquent les écarts. Le papier note que toutes les équipes combinent règles d'expert, IA et humain dans la boucle (#032.0).
- Les équipes ont pu s'entraîner sur le même jumeau KASPRO-INTKAM qui sert ensuite à l'analyse de performance (§4.2, §2.7) ; la sensibilité (CO₂, T°, lumière) est simulée et non mesurée. Le modèle sous-estime la production de fin de cycle après étêtage (§3.6).
- Le profit dépend de prix et de coûts fixés par les organisateurs (§2.6) ; coûts d'investissement exclus. Incohérence interne : Table 3 donne un profit net inférieur à revenu − coûts (306 : 37,22 − 26,07 = 11,15, annoncé 6,86), sans explication dans le texte, et le texte attribue au compartiment 302 des coûts de 33,0 €/m² là où Table 3 donne 25,04 (33,0 correspond à la chaleur de 303 en Table 2). À vérifier avant de citer les profits en valeur absolue ; l'ordre du classement suit bien la colonne de profit.
- Tableaux 1 reconstruits par PyMuPDF (avertissement d'extraction) : les chiffres de Table 1 ne sont pas des figures lues mais retrouvées par `verify`.
- Le papier ne mesure pas l'effet des maladies (jumeau « ignore pests and diseases », §2.7) ni la consommation des capteurs.

## Pertinence pour SerreIA

Ce que SerreIA peut en reprendre concrètement :
1. Architecture de décision à trois niveaux (stratégique : culture ; tactique : consignes de base sur 24 h d'après prévisions ; opérationnel : boucle courte), cohérente avec le contrôleur à règles plus prévision GRU de SerreIA ; l'agent LLM pourrait tenir le niveau stratégique avec validation humaine (#031.3).
2. Capteurs jugés utiles par les équipes, à hiérarchiser pour l'ESP32 : T°, humidité et CO₂ aspirés à plusieurs hauteurs, PAR intérieur, EC, pH et T° dans le substrat, apport et drainage, poids de gouttière, diamètre de tige ; les caméras RGB servent à inspecter et à compter les fruits (§4.2). Faire passer le capteur de drainage et le PAR avant les capteurs de crop.
3. Une règle d'éclairage fondée sur le stade : pas de lumière d'appoint sur plantes juvéniles (aucun gain), oui sur plante adulte, jamais en été (#030.3, #027.0). À encoder dans `recettes.yaml` si SerreIA a des lampes (par stade `croissance` contre `fructification`).
4. Pas de sur-dosage de CO₂ (#025.2, #029.4) : garder `co2_max` bas et couper le dosage ouvrants ouverts.
5. Efficacité à suivre comme indicateurs d'agent : MJ, kWh, L, g de nutriments par kg de tomate (Table 2) ; référence humaine 33,0 MJ/kg et 27,4 L/kg, meilleure équipe 12,9 MJ/kg et 25,0 L/kg (#135.0). Eau : 25 à 28 L/kg est un ordre de grandeur pour tomate haute technologie sur laine de roche, pas pour la serre de SerreIA.
6. Humidité haute et ventilation limitée économisent du chauffage mais montent le risque fongique : aucune donnée de maladie dans le papier, donc la règle mildiou de SerreIA reste à sourcer ailleurs.
7. Jeu de données public du défi (DOI ci-dessus), exploitable pour entraîner ou valider la GRU de prévision et le contrôleur en simulation.

## Gaps identifiés

- Consignes numériques par stade (T° jour/nuit, HR/VPD, DLI, EC, pH) pour la tomate cerise : absentes ; à chercher dans le jeu de données public (séries 5 min) ou la première édition (concombre) du défi.
- Lien entre humidité haute de gestion et risque de maladie en serre à IA : non traité.
- Ablation des algorithmes (MPC contre RL contre règles) : absente.
- Valeur de l'humain dans la boucle pour un agent LLM : le papier la constate, ne la mesure pas.

## Statut de lecture

papier complet par sections lues (Résumé, §1, §2.1 à 2.7, §3.1 à 3.6, §4.1, §4.2, §5, Tables 1 à 3) via `bin/pdb search`, `show` et lecture par plages ; les légendes des figures A1 à A9 et Fig. 3 à 23 n'ont pas été lues en valeurs (courbes). Extraction GROBID correcte, avec le texte des sections répété plusieurs fois dans `fulltext.md` (doublons de découpage). Déduit et non affirmé par les auteurs : le ratio 2,2 entre profits ; l'attribution du bon résultat de 306 à la combinaison de choix listée plus haut (les auteurs la décrivent sans la démontrer) ; les recommandations pour SerreIA.
