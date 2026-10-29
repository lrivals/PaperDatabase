---
id: 2023-ertle-reduced-daily-light-integral-end
fiche: done
date: 2026-10-29
benchmarks: none
---

# Reduced Daily Light Integral at the End of Production Can Delay Tipburn Incidence with a Yield Penalty in Indoor Lettuce Production

John Ertle, Chieri Kubota, 2023, HortScience 58(10), 1217–1225. https://doi.org/10.21273/HORTSCI17314-23
Type : article de revue (relu par les pairs)

## Problème

Le tipburn (carence localisée en Ca des jeunes feuilles en fin de pommaison) rend la laitue d'intérieur invendable. Baisser le DLI sur tout le cycle l'évite mais réduit fortement le rendement ; les auteurs testent une baisse du DLI limitée à la fin de production, période où le tipburn apparaît (000.0, 000.2).

## Méthode

Deux chambres de croissance, NFT, laitues Klee (très sensible) et Rex (modérément sensible), 34 plants/m², 2 répétitions (320 plantes) (002.2). Conditions inductrices de tipburn (jour 23 °C / 75 % HR / CO2 1000, nuit 19 °C) (013.0). DLI de 17,4 mol/m²/j pendant 16 j après repiquage, puis 100, 85, 70 ou 55 % (L100…L55) pendant les 12 derniers jours (003.1). Mesures : incidence, émergence, sévérité (% de feuilles atteintes), masses, échanges gazeux, Ca des feuilles, bilan économique simple.

## Plateforme et implémentation

Sans objet (agronomie). Chambres Conviron, LED Philips (19 % bleu, 10 % vert, 71 % rouge) à 50 cm du canal (002.0, 002.1). Pas de code publié ; protocole décrit.

## Résultats

- Sévérité Klee : 8 ± 2,1 % des feuilles à L55 contre 33 ± 3,5 % pour les autres niveaux ; Rex : 14 ± 2,8 % à L100 contre 2 ± 0,9 % pour les autres (000.1).
- Perte de rendement jusqu'à 22 % (Klee) et 26 % (Rex) à L55, linéaire avec le DLI (000.1, 006.0).
- Émergence du tipburn inchangée : 21 ± 3,0 j (Klee) et 23 ± 2,8 j (Rex) après repiquage (005.0) ; dès 17 j, un jour après la baisse de lumière, certaines plantes l'expriment (005.1), attribué à une réaction d'évitement de l'ombre (hypothèse des auteurs, 007.2).
- Économie d'électricité 0,51 à 1,53 $/m²/cycle ; gain net seulement pour Klee à L55 (+2,55 $/m²), perte de 14,96 $/m² pour Rex (008.0, 005.4).
- Aucune ligne dans benchmarks.csv : pas de configuration matérielle ; les valeurs agronomiques sont dans les consignes ci-dessous.

## Consignes chiffrées

| espèce | stade | grandeur | optimal | marginal / limite | unité | condition | chunk_id |
|---|---|---|---|---|---|---|---|
| laitue (Klee, Rex) | j0–16 après repiquage | DLI | 17,4 (induit le tipburn, choisi pour maximiser la croissance) | n/r | mol/m²/j | PPFD 301 µmol/m²/s, 16 h | 003.1 |
| laitue | j17–28 (fin) | DLI | 9,5 (L55) : seul niveau rentable, Klee seul | 14,7 / 12,1 : perte nette | mol/m²/j | PPFD ≈ 165 µmol/m²/s | 003.1, 008.0 |
| laitue (littérature citée) | cycle | DLI seuil tipburn | n/r | symptômes au-delà de 13 (24 h) ou 15 (16 h) | mol/m²/j | photopériode continue / 16 h ; valeur de Caplan 2018, Sago 2016, non mesurée ici | 000.2 |
| laitue (Sago 2016, cité) | cycle | DLI 13 vs 26 | n/r | 13 : -92 % de sévérité, -40 % de masse fraîche | mol/m²/j | lumière continue | 001.1 |
| laitue | cycle 28 j | photopériode | 16 | n/r | h | après repiquage (cycle de 28 j ; la conclusion parle de 42 j au total) | 002.2, 009.0 |
| laitue | pépinière | T° air jour / nuit | 23 / 19 | n/r | °C | 12 j, 16 h, semis 2 j à 20 °C en continu | 002.2 |
| laitue | après repiquage | T° air jour / nuit | 23 / 19 (consignes, induisent le tipburn) | n/r | °C | mesuré 22,8–23,7 / 18,9–19,3 | 013.0 |
| laitue | après repiquage | HR jour | 75 (consigne) | n/r | % | mesuré 73–83 | 013.0 |
| laitue | après repiquage | VPD jour | 0,87 (consigne ; mesuré 0,50–0,75) | n/r | kPa | | 013.0 |
| laitue | après repiquage | CO2 | 1000 | n/r | µmol/mol | jour, montée en 90–120 min | 003.0 |
| laitue | après repiquage | vitesse d'air | 0,16 horiz. / 0,07 vert. | n/r | m/s | | 003.0 |
| laitue | après repiquage | pH | 6,0 | ± 0,5 | n/a | NFT | 002.3 |
| laitue | après repiquage | EC | 2,0 | ± 0,2 | dS/m | NFT | 002.3 |
| laitue | après repiquage | solution | 182 N, 42 P, 152 K, 190 Ca, 42 Mg | n/r | mg/L | changée 1 fois/semaine | 002.3 |
| laitue | 1re semaine | irrigation | canal rempli à 80 % (3,74 L), vidé et renouvelé chaque jour | O2 dissous > 5 mg/L | | puis NFT en circulation continue | 002.3 |
| laitue | toutes | T° racines | n/r | n/r | | non rapportée | n/r |
| laitue | toutes | seuil de risque maladie | n/r | n/r | | non traité | n/r |

Écart avec SerreIA (laitue-hydro de recettes.yaml : T jour 16–22 / nuit 12–16 °C, HR 50–70 %, photopériode 16 h, DLI cible 14, pH 5,6–6,2, EC 1,0–1,6) : le papier travaille volontairement hors recette pour provoquer le tipburn, avec 23/19 °C (au-dessus des plages), HR 75 % (au-dessus de 70 %), DLI 17,4 puis 9,5–17,3 et EC 2,0 (au-dessus de 1,6). Photopériode (16 h) et pH 6,0 concordent. Le DLI cible SerreIA de 14 est au-dessus du seuil de tipburn de 13 (24 h) mais sous celui de 15 (16 h) cité par les auteurs : la recette est donc à la limite, à surveiller en fin de cycle.

## Limites et critique

Une seule espèce, deux cultivars, chambre de croissance, conditions choisies pour induire le tipburn : transfert à une serre (lumière naturelle, T° et HR variables) non démontré. Le bilan économique est simple (prix et coûts propres aux auteurs) ; les cultivars diffèrent (rentable pour Klee seulement). Les seuils 13/15 mol/m²/j sont repris de la littérature, non mesurés ici. Table 4 sans corps extrait : incidence et Ca non relus dans le tableau. Pas d'effet testé sur l'humidité ni la T° pour le tipburn.

## Pertinence pour SerreIA

SerreIA peut reprendre : (1) une règle de fin de cycle de la laitue-hydro : si le cultivar est sensible, réduire le DLI à environ 55 % (≈ 9,5 mol/m²/j) pendant les ~12 derniers jours ; sinon garder le DLI (perte de rendement de 26 % non rentable) ; (2) un plafond DLI de 13 à 15 mol/m²/j comme seuil d'alerte tipburn dans `recettes.yaml` (dli_cible 14) ; (3) un stade « finition » dans la recette laitue, avec une consigne de DLI propre ; (4) le fait que la baisse brutale de lumière peut déclencher du tipburn le jour suivant : préférer une rampe, à tester. Une lumière naturelle de serre ne se règle pas comme des LED : l'agent LLM devrait plutôt agir sur ombrage et lumière d'appoint, et sur l'humidité/transpiration (non étudiée ici).

## Gaps identifiés

Effet couplé DLI de fin de cycle et transpiration (HR, flux d'air) ; rampe de lumière plutôt que palier ; transfert en serre sous lumière naturelle ; seuils de tipburn par cultivar.

## Statut de lecture

Papier complet (par passages, via search/show : abstract, méthode, résultats, discussion, conclusion, Tables 1 et 4 partiellement). Table 4 sans corps extrait (Table 3 non relue en détail). Déduit et non affirmé par les auteurs : l'écart avec SerreIA, les usages proposés, la mention « 28 j de cycle » (006.0 dit 28 j après repiquage, la conclusion 42 j).
