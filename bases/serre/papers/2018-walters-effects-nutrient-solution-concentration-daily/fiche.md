---
id: 2018-walters-effects-nutrient-solution-concentration-daily
fiche: done
date: 2026-10-29
benchmarks: none
---

# Effects of Nutrient Solution Concentration and Daily Light Integral on Growth and Nutrient Concentration of Several Basil Species in Hydroponic Production

Kellie J. Walters, Christopher J. Currey, 2018, HortScience 53(9), 1319-1325. https://doi.org/10.21273/HORTSCI13126-18
Type : article de revue (relu par les pairs).

## Problème

Les producteurs hydroponiques règlent la solution nutritive sur l'EC, parfois plus basse en été (forte lumière) qu'en hiver, mais aucune étude à comité de lecture ne quantifiait l'effet de l'EC sous différents DLI pour le basilic en recirculation (#001.2). Objectif : effet de l'EC et du DLI sur la croissance et la composition minérale de trois basilics (#000.0).

## Méthode

Basilic sweet ('Nufar'), lemon ('Lime') et holy ('Holy'), 3 semaines en NFT après transplantation (production commerciale de 3-4 semaines, #006.0). Plan factoriel en blocs : 5 EC (0,5 ; 1,0 ; 2,0 ; 3,0 ; 4,0 dS/m) x 2 DLI (cible 7 et 15 mol/m2/j, réels 6,6-7,4 et 14,5-15,7, Table 1), 3 répétitions dans le temps, 10 plantes par système et par espèce (§Materials and Methods). EC et pH ajustés chaque jour, donc EC constante. Mesures : masse fraîche et sèche, hauteur, noeuds, ramifications, SPAD, minéraux foliaires (Table 3 à 5, Fig. 1-4).

## Plateforme et implémentation

Deux serres en verre à Ames (Iowa, 42,0 N), chauffage à eau chaude, brumisation, rideaux d'ombrage, lampes HPS (180 umol/m2/s, 06h-22h) pilotées par ARGUS Titan (#002.2). NFT : gouttières de 203 cm, pente 3 %, 1 L/min par gouttière, réservoir de 151 L, solution aérée (O2 8,3 ppm), 22,1 degC (#002.2, #002.4). Engrais 16N-1,8P-14,3K. Code : sans objet.

## Résultats

- L'EC (0,5-4,0) n'affecte ni la masse, ni la hauteur, ni la ramification des trois espèces ; le DLI si (#000.0, #005.1).
- Sweet basil, DLI 7 vs 15 : masse fraîche 12,5 vs 30,5 g, sèche 0,9 vs 2,5 g, hauteur 13,2 vs 15,9 cm, ramifications 0,0 vs 2,3, SPAD 25,7 vs 34,1 (Table 4, #014.1). Lemon : 6,2 vs 18,9 g frais (Table 4). Holy : 6,4 vs 19,7 g (Table 4, #014.2).
- Pas d'interaction EC x DLI (#008.0).
- L'EC modifie la composition foliaire : N, P, S, Cu augmentent avec l'EC, Mg et Ca diminuent (#005.1, #000.1). N sweet +0,7 point de % de 0,5 à 4,0.
- Teneurs globalement dans les plages de suffisance, sans carence visible ; K très élevé (4,2-7,6 % contre 2,0 % recommandé), attribué à l'apport de carbonate de potassium pour le pH (#007.1).
→ reportés dans `benchmarks.csv` : aucune ligne (colonnes FPGA/accuracy sans objet ; voir front-matter `benchmarks: none`).

## Consignes chiffrées

| espèce | stade | grandeur | optimal | marginal / limite | unité | condition (jour/nuit, lumière…) | chunk_id |
|---|---|---|---|---|---|---|---|
| basilic (sweet, lemon, holy) | croissance NFT, 3 sem. après transplantation | EC solution | pas d'optimum : croissance identique de 0,5 à 4,0 | n/r (aucune baisse de croissance à 0,5 ni à 4,0) | dS/m | EC maintenue constante, DLI 7 ou 15 | 2018-walters#000.0 |
| basilic | idem | DLI | 15 (réel 14,5-15,7) : x2,4 en masse fraîche sweet vs 7 | 7 (réel 6,6-7,4) : croissance fortement réduite | mol/m2/j | 16 h, HPS 180 umol/m2/s en appoint | 2018-walters#014.1 |
| basilic | croissance | DLI requis (classification « medium-to-high light ») | > 10 pour une qualité bonne ou excellente | n/r | mol/m2/j | citant Faust 2011, Beaman, Chang ; non testé directement | 2018-walters#006.3 |
| basilic | croissance | photopériode | 16 | n/r | h | lumière naturelle + HPS 06h-22h | 2018-walters#002.2 |
| basilic | croissance | T° air | 21 +/- 1 (réel 21,4-22,0) | n/r (un seul niveau testé) | degC | moyenne journalière, pas de consigne jour/nuit rapportée | 2018-walters#002.2 |
| basilic | croissance | T° solution (racines) | 22,1 +/- 0,5 | n/r | degC | chauffage/refroidisseur en continu | 2018-walters#002.4 |
| basilic | croissance | pH solution | 6,0 | n/r | pH | ajusté chaque jour (K2CO3 / H3PO4 + acide citrique) | 2018-walters#002.3 |
| basilic | croissance | O2 dissous | 8,3 +/- 0,2 | n/r | ppm | aération permanente | 2018-walters#002.4 |
| basilic | croissance | débit NFT | 1 | n/r | L/min par gouttière | gouttières 10 cm, pente 3 % | 2018-walters#002.2 |
| basilic sweet | croissance | N foliaire (diagnostic) | 4 à 6 (Bryson 2014, sol extérieur) | holy et lemon dépassent 6 si EC >= 2,0 ou DLI haut | % MS | mesuré 3 sem. après transplantation | 2018-walters#007.0 |
| basilic | croissance | P foliaire | 0,6 à 1,0 | mesuré 1,1 à 2,0, sans toxicité visible | % MS | idem | 2018-walters#007.1 |
| basilic | croissance | Mg foliaire | 0,6 à 1,0 | sweet et lemon au niveau ou sous la plage, sans symptôme | % MS | Mg et Ca baissent quand l'EC monte | 2018-walters#007.1 |
| basilic | tout | HR, VPD, CO2, irrigation (hors NFT), seuil maladie | n/r | n/r | n/r | non rapportés | n/r |

Écart avec SerreIA (`basilic-standard`, stade croissance) : EC 1,0-1,6 dS/m : compatible, mais l'article ne la « tranche » pas, il montre que 0,5 à 4,0 donnent la même croissance (3 semaines, EC constante, 3 espèces ; #000.0) ; la plage de SerreIA est donc non limitante, pas validée comme optimum, et l'économie d'engrais est possible jusqu'à 0,5-1,0. pH 5,8-6,5 : contient les 6,0 de l'article. DLI cible 15 : égale au DLI haut testé, supérieure au seuil de 10. Photopériode 16 h : identique. T° jour 20-27, nuit 16-20 : l'article ne rapporte qu'une moyenne de 21 degC, dans la plage ; il n'apporte rien sur le jour/nuit ni sur l'HR (50-70 %). T° racines : non présente dans SerreIA, 22 degC proposable. Aucun écart majeur ; seul manque dans SerreIA : le seuil bas de DLI (10) comme alerte.

## Limites et critique

- Un seul cultivar par espèce, saison d'hiver (oct.-déc. 2014), 3 répétitions, 3 semaines : pas de conclusion sur des cycles plus longs ; Suh et Park (1997) trouvent un effet de l'EC sur 8,5 semaines (#006.0).
- EC maintenue constante chaque jour ; sans cette régulation, les résultats ne s'appliquent pas (#008.0).
- DLI obtenu avec HPS et ombrage : T° et spectre non découplés du DLI ; une seule T° moyenne.
- K foliaire très au-dessus de la norme, biais dû au pH-up au carbonate de potassium (#007.1).
- Aucun critère de qualité sensorielle ou d'huiles essentielles ; recommandations foliaires issues de basilic de pleine terre.
- Les auteurs recommandent des essais sur site (#008.0).

## Pertinence pour SerreIA

- Plage EC : garder 1,0-1,6 pour le basilic mais ne pas la présenter comme un optimum ; on peut descendre vers 0,5-1,0 sans perte de croissance (économie d'engrais, solution commune avec la laitue, #000.0, #008.0).
- Règle de DLI : le DLI est le levier de croissance (x2,4 en masse fraîche de 7 à 15) ; le contrôleur doit prioriser la lumière d'appoint plutôt que modifier l'EC en saison (#008.0). Ajouter une alerte DLI < 10 (#006.3).
- Pas de modulation saisonnière de l'EC à coder pour le basilic.
- Valeurs de consigne reprenables : pH 6,0, solution à 22 degC, O2 > 8 ppm, flux NFT 1 L/min par gouttière (#002.2-#002.4).
- Pour l'agent LLM : une EC en limite basse n'est pas un défaut de croissance, mais surveiller Mg/Ca à EC haute (#005.1).

## Gaps identifiés

- Optimum d'EC du basilic sur cycle long (> 5 semaines) et en tâche récoltée plusieurs fois.
- Consignes jour/nuit, HR et VPD pour le basilic en serre : non couvertes par ce papier.
- Effet de l'EC sur la qualité (arôme, huiles essentielles) non mesuré.

## Statut de lecture

papier complet (texte intégral lu ; Tables 3-5 et Fig. 1-4 uniquement via les légendes et le texte, Table 3 sans corps extrait, Table 2 tronquée).
Déduit et non affirmé par les auteurs : l'interprétation « plage non limitante, non optimum » pour SerreIA ; le rapprochement avec recettes.yaml ; le facteur x2,4 (30,5 / 12,5, les auteurs écrivent +144 %).
