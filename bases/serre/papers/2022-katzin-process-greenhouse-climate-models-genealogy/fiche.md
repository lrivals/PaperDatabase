---
id: 2022-katzin-process-greenhouse-climate-models-genealogy
fiche: done
date: 2026-10-29
benchmarks: none
---

# Process-based greenhouse climate models: Genealogy, current status, and future directions

David Katzin, Eldert J. Van Henten, Simon Van Mourik, 2022, Agricultural Systems (DOI et venue d'après `metadata.json` : venue `null`, DOI 10.1016/j.agsy.2022.103388). https://doi.org/10.1016/j.agsy.2022.103388
Type : article de revue (survey) ; le DOI Elsevier l'indique, la venue exacte n'est pas dans les métadonnées, à confirmer.

## Problème

Plus de 150 modèles de climat de serre sont publiés (plus de 70 dans la dernière décennie), sans
critère de choix pour un nouvel utilisateur (§1, 2022-katzin#001.2). Les auteurs veulent
expliquer cette prolifération et fournir un cadre de décomposition et de choix selon quatre
critères de Soltani et Sinclair : adéquation, complexité, validité, transparence (2022-katzin#001.3).
Périmètre : modèles à mécanisme, air de serre en « réservoir parfaitement agité » (CFD exclu).

## Méthode

- Recherche Web of Science du 6 octobre 2020, articles 2018-2020 : 80 résultats, 32 retenus (§3, 2022-katzin#023.0).
- Pour chaque modèle : objectif (analyse de système, exploration, commande, conception, calibration),
  type de serre, culture, équipements, statut (nouveau, réutilisé, paramétré, étendu, traduit),
  composition (bilans d'énergie, de vapeur d'eau, de CO2 ; rayonnement, ventilation, convection,
  chaleur latente, transpiration, photosynthèse), filiation (graphe d'héritage, Fig. 5) et validation
  (site, durée, variables, métriques) (§3.1-3.4).
- Cadre général : trois bilans, `dE/dt = Q_Sun + Q_Heat + Q_Lamp - Q_Vent - Q_Latent - Q_Con - Q_FIR - Q_Cool`, avec bilans de vapeur
  et de CO2 (Eq. 1, 2022-katzin#006.0). Deux exemples bornes : Van Henten (4 états : T, humidité,
  CO2, masse sèche ; 2022-katzin#007.0) et De Zwart / KASPRO (14 états : cover, air, culture, deux
  réseaux de chauffage, sol, 6 couches de sol ; §2.3.2).

## Plateforme et implémentation

Sans objet (revue). Code : les auteurs notent que le code de modèles de serre est rarement publié ;
exceptions citées : Altes-Buch 2019, Katzin 2020b, Körner et Holst 2017 (§5.5.2, 2022-katzin#044.0).
Les modèles d'Ahamed (2018) sont publiés en PDF seulement. Données publiques rares : Autonomous
Greenhouse Challenge et CEA Open Data (2022-katzin#044.1). Puissance : sans objet.

## Résultats

- Objectifs des 32 études : commande 11, conception 8, analyse de système 6, exploration 4,
  calibration 3 (§4.1, 2022-katzin#031.0). Statut : 11 nouveaux, 11 extensions, 9 réutilisations, 1 traduction.
- Culture : tomate 11 sur 32, 5 sans culture ; serres : Venlo, serres solaires chinoises, polyéthylène.
  Équipements : chauffage 19, éclairage 15, injection de CO2 12, brumisation 7, écrans 7 (§4.1).
- Composition (24 modèles analysés) : ventilation négligée 2, constante 5, entrée 8, calculée 9 ;
  chaleur latente absente 5 ; lampes : chaleur proportionnelle à la puissance dans 6 cas sur 9, et
  nulle dans 2 cas de LED ; 16 modèles sur 24 sans rendement ni dynamique lente (§4.2, 2022-katzin#032.0).
- Filiation : des modèles anciens (Albright 2001, Boulard 1996, De Zwart 1996, Van Henten 1994,
  Van Ooteghem 2007, Vadiee et Martin 2013) servent encore de base ; la réutilisation par d'autres
  équipes se limite à des modèles simples (§4.3, 2022-katzin#033.2).
- Validation : installations de 15 m2 (prototype) à 5760 m2 ; jeux de données petits ; RMSE (9 études sur 22)
  et NSE (8) les plus courants ; comparaison des performances « pratiquement impossible » (§4.4, 2022-katzin#034).
- Discussion : la complexité suit l'objectif (commande et calibration : modèles simples ; exploration :
  complexes) (§5.1, 2022-katzin#035.2) ; réduction de TOMGRO de 574 à 5 états avec de bonnes prédictions (§5.2) ;
  Vanthoor et al. 2011b ont utilisé un seul modèle avec quatre jeux de paramètres (Italie, Pays-Bas,
  Texas, Arizona) (2022-katzin#038.1).
→ reportés dans `benchmarks.csv` : aucune ligne (survey, pas de configuration propre ; `benchmarks: none`).

## Limites et critique

- Échantillon réduit : 32 études sur trois ans, requête Web of Science ; les modèles historiques
  ne sont pas évalués. L'attribution des objectifs est subjective (aveu des auteurs, §5.1).
- Aucune comparaison quantitative de précision entre modèles : les auteurs l'écartent faute de
  métriques et de données communes, et ne proposent pas de banc.
- Les modèles de commande ou de calibration, les plus proches de SerreIA, sont souvent non validés (§5.1).
- Les serres étudiées sont surtout des serres commerciales Venlo ou des serres solaires chinoises ; le
  cas d'une petite serre amateur de quelques m2 n'est pas traité. Aucune hydroponie (pH, EC) :
  ces dynamiques ne sont pas dans le périmètre (bilans d'énergie, d'eau, de CO2 de l'air).
- Le tableau 3 (composition) et le tableau 4 (validation) n'ont pas été relus en détail ; seuls les
  décomptes du texte sont repris.

## Pertinence pour la thèse

Thème de la base : contrôle climatique (axe `climate-control`) du projet SerreIA. Le papier donne
la carte des modèles de climat de serre et les critères de choix ; pas de contenu sur les
maladies, l'edge ou le LLM. Aide à justifier la complexité du simulateur utilisé pour tester le
contrôleur à règles puis une éventuelle MPC ou RL (niveau 3 de `sim/model.py`).

## Pour SerreIA

État actuel : `sim/model.py` est un modèle de zone à constantes de temps (T : relaxation vers l'extérieur,
excès solaire de 15 °C à 800 W/m2, excès de chauffage, ventilation en `(T - T_ext)/tau_vent`), HR par relaxation
vers un équilibre et pH, EC, niveau de cuve très simplifiés. C'est un modèle de type Van Henten sans CO2 dynamique
ni culture, donc dans la catégorie la plus répandue pour la commande (§4.2, §5.1).

Choix recommandé (déduit du papier, non affirmé par les auteurs pour une petite serre) : **ne pas adopter
De Zwart/KASPRO ni Vanthoor**, mais faire évoluer le modèle actuel vers un « Van Henten enrichi » avec
les bilans d'énergie et de vapeur d'eau en grandeurs physiques.

| Critère | Van Henten (4 états) | De Zwart / KASPRO (14 états) | Vanthoor (extension de Katzin 2020b) |
|---|---|---|---|
| Complexité | basse (2022-katzin#007.0) | haute, 6 couches de sol, écran, réseaux de chauffage (§2.3.2) | élevée, avec photosynthèse et rendement (déduit : pas lu dans le détail) |
| Paramètres à identifier | peu, mais agrégés (capacités, coefficients) (2022-katzin#042.1) | nombreux, beaucoup mesurables mais corrélés | nombreux, repris de la littérature pour 4 sites (2022-katzin#038.1) |
| Code ouvert | non précisé pour ces modèles ; Katzin 2020b cité parmi les exceptions (2022-katzin#044.0) | non cité | oui d'après Katzin 2020b, à vérifier |
| Petite serre | adapté à la commande, culture facultative | trop de sous-modèles inutiles (écran, boiler) | calibrée pour serres commerciales |
| Faiblesses | peu validé hors étude d'origine | validations rares et petites | idem |

Pourquoi : la thèse du papier est que les modèles de commande restent simples (§5.1, 2022-katzin#035.2),
que les paramètres d'un modèle simple se calibrent (§5.4.3) et que la validation est rare. Pour SerreIA,
le simulateur sert d'environnement de test de la logique (règles, sécurité, agent), pas de prédicteur absolu.

## Gaps identifiés

- Aucun modèle de petite serre amateur validé (quelques m2, LED, brumisation) dans ce papier : à chercher
- Hypothèse de serre « infiniment grande » (air parfaitement mélangé, effets des parois négligés) courante dans ces modèles (2022-katzin#003.2, rappelée en #039.4) : fausse pour quelques m², où les parois dominent les échanges ; ajouter un terme de conduction parois/volume au simulateur (déduit).
  (`/paper-discover` : Katzin 2020b, Vanthoor 2011, Van Henten 2003, modèles de serre à LED).
- Chaleur émise par des LED : le papier signale très peu de mesures systématiques (§5.5.1) : à mesurer sur la serre.
- Pas de modèle conjoint climat et solution nutritive (pH/EC) dans ce survey.

## Statut de lecture

Sections lues : Résumé, 1, 2.1-2.5 (extraits), 3, 4, 5, 6 (via `sed` par plages et `pdb search`) ; Tableaux 1 à 4 et figures non relus
(corps de tableaux mal extraits par GROBID). Pas un papier complet au sens strict.
Ce qui suit est déduit et non affirmé par les auteurs : le classement de SerreIA dans la catégorie « Van Henten enrichi » ; les
colonnes du tableau « Vanthoor » (complexité, code) ; l'inadéquation des modèles Venlo à une petite serre ; les
recommandations de la section « Pour SerreIA ».
