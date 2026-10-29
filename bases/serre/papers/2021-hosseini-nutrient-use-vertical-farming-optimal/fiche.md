---
id: 2021-hosseini-nutrient-use-vertical-farming-optimal
fiche: done
date: 2026-10-29
benchmarks: none
---

# Nutrient Use in Vertical Farming: Optimal Electrical Conductivity of Nutrient Solution for Growth of Lettuce and Basil in Hydroponic Cultivation

Hadis Hosseini, Vahi Mozafar, Hamid Reza Roosta, Hossein Shirani, Paulien C H Van De Vlasakker, Mohsen Farhangi, Antonio Ferrante, Miguel Guzmán, Roberta Bulgari, Stefania Toscano, 2021, Horticulturae 7(9):283 (venue absente de metadata.json : revue MDPI d'après le DOI, à vérifier). https://doi.org/10.3390/horticulturae7090283
Type : article de revue (d'après le DOI MDPI ; la venue n'est pas confirmée par metadata.json).

## Problème

Même dans une ferme verticale automatisée, l'EC de la solution nutritive se règle à la main ; les recommandations existantes (0,5–1,6 dS/m « selon les conditions », vulgarisation) sont larges (2021-hosseini#008.1). Les auteurs cherchent l'EC optimale du basilic et de la laitue en culture hydroponique « ebb-flow » en ferme verticale (2021-hosseini#001.2).

## Méthode

Cinq EC constantes (2,0 ; 1,2 ; 0,9 ; 0,7 ; 0,5 dS/m) de solution Hoagland diluée, maintenues par un doseur automatique (précision 2 %), plan en blocs complets randomisés, 4 répétitions (2021-hosseini#003.0). Basilic « Emily » et laitue « Batavia-Caipira ». Seule l'EC varie : pH 6, PPFD 215 ± 5,5 µmol m-2 s-1, photopériode 16:8 h, HR 50–60 %, CO2 450 ppm (2021-hosseini#003.0). Récolte 45 j (laitue) et 30 j (basilic) après transfert (2021-hosseini#004.0). Mesures : nombre de feuilles, masses fraîche/sèche feuilles et racines, surface foliaire, chlorophylle, azote Kjeldahl. ANOVA à deux facteurs, Tukey p < 0,05, régressions linéaire/quadratique/cubique/puissance choisies par R² ajusté (2021-hosseini#004.0).

## Plateforme et implémentation

Fermes verticales Vegger FlaxFarm VFF0105 à 5 niveaux (Pays-Bas, Ede), LED Philips ; racines inondées 5 fois par jour pendant 10 min (2021-hosseini#002.1). Code / données brutes : non publiés (tableaux d'ANOVA seulement).

## Résultats

- EC optimale conclue : basilic 1,2 dS/m, laitue 0,9 dS/m en ebb-flow (2021-hosseini#010.0). Pour la laitue, les paramètres de croissance sont maximaux à 0,9, avec chute nette de 0,9 à 0,5 (2021-hosseini#005.1).
- Basilic : hausse de 2 à 1,2 puis chute nette de 1,2 à 0,5 ; la masse fraîche et sèche à 2 dS/m reste cependant supérieure à celle à 1,2 selon le texte (2021-hosseini#005.1), alors que la discussion dit la productivité à 1,2 « légèrement supérieure » à celle à 2 (2021-hosseini#008.3) : incohérence interne.
- Au-dessus de 0,9 dS/m, pas de différence significative de croissance du basilic (2021-hosseini#008.2).
- Chlorophylle et azote foliaires croissent linéairement avec l'EC, pour les deux espèces (2021-hosseini#006.0) : l'EC « optimale » pour la biomasse n'est pas celle qui maximise le vert.
- Rester au-dessus de l'optimum nuit moins que rester en dessous ; 0,9 à 1,5 dS/m donne la même performance que l'optimum d'après la régression (2021-hosseini#010.0).
- Les protocoles Vegger fixaient 2 dS/m (basilic) et 1,5 (laitue) ; l'adoption des valeurs de l'étude aurait réduit la consommation de nutriments d'environ 20 % sans effet sur rendement et qualité, selon le responsable R&D de Vegger (affirmation industrielle, non mesurée dans l'article) (2021-hosseini#009.0).
- Les auteurs attribuent l'écart avec d'autres études (Solis-Toapanta : basilic meilleur au-dessus de 1,2 ; Wortman) à la technique de culture et à la durée d'inondation des racines : plus les racines sont inondées, plus l'EC optimale est basse (2021-hosseini#008.3, 2021-hosseini#008.4).
→ reportés dans `benchmarks.csv` : aucune ligne (pas de mesure de modèle, de latence ou de puissance).

## Limites et critique

- Un seul cultivar par espèce, un seul système (ebb-flow), une seule température/lumière, un seul essai, 4 répétitions : l'optimum n'est pas transférable tel quel à un autre système (NFT, goutte-à-goutte) ; les auteurs le disent (2021-hosseini#008.4).
- Cinq niveaux seulement, avec un pas inégal (écart 0,2 entre les niveaux bas), donc l'optimum est un des niveaux testés, pas un optimum continu ; le plus haut est 2,0, alors que d'autres travaux vont à 4 (voir ci-dessous).
- Incohérences de texte : température de jour 20 ± 1 °C (2021-hosseini#003.0) contre 24 ± 2 °C en 2.1 (2021-hosseini#002.1) ; la discussion cite des traitements « 2,0, 1,5 et 1 » qui ne sont pas ceux du protocole (2021-hosseini#008.2) ; les conclusions (0,9 pour la laitue, mais « 0,9–1,5 équivalent ») laissent une plage de fait plus large que le point annoncé.
- Corps des tableaux 1–6 non extrait (légendes seules) : les valeurs de masse par EC ne sont pas lisibles ici ; seules les conclusions du texte sont utilisées.
- Confrontation avec Walters 2018 (déduit, non affirmé par Hosseini) : Walters ne trouve aucun effet de l'EC (0,5–4,0 dS/m, NFT, serre, DLI 7 ou 15) sur la croissance de trois basilics (2018-walters#000.0). Hosseini trouve un effet net en dessous de 0,9 et aucun effet significatif au-dessus de 0,9 (2021-hosseini#008.2) : les deux sont compatibles sur la zone 1–4 dS/m (plateau), et le désaccord porte sur le bas de la plage (Walters 0,5 sans effet, Hosseini 0,5 sensiblement pénalisant). Explications possibles, non testées : NFT (racines en contact permanent) contre ebb-flow (5 × 10 min par jour, 2021-hosseini#002.1), cultivars, lumière (PPFD 215 µmol m-2 s-1 constant ici). Conclusion pratique : aucune des deux ne justifie un EC < 1,0 pour le basilic en général ; la zone 1,0–2,0 est sûre.
- Les valeurs d'EC sont celles de la solution d'entrée dosée ; le suivi de l'EC dans le bac (évaporation, absorption) n'est pas décrit (n/r).

## Consignes chiffrées

| espèce | stade | grandeur | optimal | marginal / limite | unité | condition | chunk_id |
|---|---|---|---|---|---|---|---|
| laitue (Batavia-Caipira) | récolte à 45 j après transfert | EC solution | 0,9 | 0,9–1,5 équivalent ; chute nette à 0,5 | dS/m | ebb-flow, Hoagland, pH 6, 20 °C jour | 2021-hosseini#010.0 |
| basilic (Emily) | récolte à 30 j après transfert | EC solution | 1,2 | 0,9–1,5 équivalent ; chute nette à 0,5 ; 2,0 sans différence significative au-dessus de 0,9 | dS/m | ebb-flow, Hoagland, pH 6, 20 °C jour | 2021-hosseini#010.0 |
| laitue, basilic | n/r | EC « recommandée » (vulgarisation, citée) | n/r | 0,5–1,6 | dS/m | selon conditions | 2021-hosseini#008.1 |
| laitue, basilic | n/r | EC des anciens protocoles Vegger | n/r | basilic 2 ; laitue 1,5 | dS/m | FlaxFarm | 2021-hosseini#009.0 |
| laitue, basilic | n/r | pH | 6 (fixe, non testé) | n/r | pH | un seul niveau | 2021-hosseini#003.0 |
| laitue, basilic | n/r | température jour / nuit | 20 ± 1 / 16 ± 2 (non testé) | n/r | °C | un seul niveau ; 2.1 donne 24 ± 2 le jour | 2021-hosseini#003.0 |
| laitue, basilic | n/r | humidité relative | 50–60 (non testée) | n/r | % | un seul niveau | 2021-hosseini#003.0 |
| laitue, basilic | n/r | PPFD / photopériode | 215 ± 5,5 / 16 h (non testés) | n/r | µmol m-2 s-1 / h | un seul niveau | 2021-hosseini#003.0 |
| laitue, basilic | n/r | CO2 | 450 (non testé) | n/r | ppm | un seul niveau | 2021-hosseini#003.0 |

Écart avec SerreIA (`edge/controller/recettes.yaml`) : laitue-hydro `ec: [1.0, 1.6]` contre optimum 0,9 et plage équivalente 0,9–1,5 : la borne basse 1,0 est cohérente, la haute 1,6 dépasse légèrement 1,5 (déduit : sans conséquence grave, car rester au-dessus de l'optimum est moins pénalisant, 2021-hosseini#010.0). basilic-standard `ec: [1.0, 1.6]` contre optimum 1,2 et plage 0,9–1,5 : recouvrement très bon ; la plage de SerreIA est plus basse que le protocole Vegger (2,0). pH 5,6–6,2 (laitue) et 5,8–6,5 (basilic) encadrent le pH 6 de l'étude. Température jour laitue 16–22 / basilic 20–27 °C, HR 50–70 % et DLI 14–15 : l'étude ne teste aucune de ces variables (20 °C, 50–60 %, 215 µmol m-2 s-1 × 16 h = 12,4 mol m-2 j-1, calcul déduit) ; son DLI est proche mais inférieur au 14–15 de SerreIA. Attention : l'optimum dépend du système (ebb-flow ici) ; si SerreIA utilise NFT ou DWC, cette valeur n'est qu'indicative.

## Pertinence pour SerreIA

Baseline de pratiques pour `recettes.yaml` : l'EC de la laitue et du basilic est confirmée dans [1,0 ; 1,6], avec un optimum mesuré en ferme verticale à 0,9 (laitue) et 1,2 (basilic). Pour le contrôleur (`edge/controller/rules.py`) : alarme d'EC basse sous 0,9 (chute nette de croissance) plutôt que sous 1,0 ; bande morte autour de 1,2. Pour l'agent LLM : citer cette source et l'écart avec Walters 2018 avant de proposer un changement d'EC. Piège : l'EC de commande (solution d'entrée) n'est pas celle du bac.

## Gaps identifiés

- Aucune étude de la base ne teste l'EC en NFT/goutte-à-goutte sur la laitue ; effet de l'EC en fonction de la durée d'inondation (hypothèse des auteurs, non testée).
- Interaction EC × DLI × température (Walters 2018 teste EC × DLI sur le basilic, pas la laitue).
- Consignes de fraise et tomate : hors de cette source.

## Statut de lecture

papier complet (texte principal ; corps des tableaux 1–6 et A1–A3 non extraits, sauf la composition de la solution en annexe).
Déduit et non affirmé par les auteurs : confrontation avec Walters 2018, lecture « plateau » du désaccord, calcul du DLI, écart avec `recettes.yaml`, type d'article (revue MDPI d'après le DOI).
