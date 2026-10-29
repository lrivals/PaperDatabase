---
id: 2026-garcia-berries-controlled-environment-agriculture
fiche: done
date: 2026-10-29
benchmarks: none
---

# Berries in CEA: production, nutrient requirement and irrigation (short-course slides)

Karla Garcia, 2026, University of Arizona CEAC, short course (diapositives). Pas de DOI ni d'URL.
Type : littérature grise (diapositives de formation), non relue par les pairs ; adaptée en partie de Garcia et Kubota 2017 et du Kubota Lab (Ohio State), sources non détaillées.

## Problème

Donner aux producteurs des repères pratiques pour la fraise (et un peu la myrtille) en environnement contrôlé : nutrition (pH, EC), irrigation, lumière (quantité, qualité), humidité, pollinisation. Pas de question de recherche formulée.

## Méthode

Sans objet (diapositives de synthèse, pas d'expérience propre). Les valeurs sont des recommandations ou des résultats cités (Proefcentrum Hoogstraten pour le far-red ; Garcia et Kubota 2017 pour la photosynthèse matinale), sans protocole ni effectifs.

## Plateforme et implémentation

Sans objet (pas de calcul embarqué). Irrigation décrite : injecteurs ou goutte-à-goutte, substrat en pot (2 goutteurs par pot de 25 L pour la myrtille). Code et données : non publiés.

## Résultats

Pas de mesure de modèle. Recommandations fraise (détail dans « Consignes chiffrées ») :
- EC : sensible aux sels, risque de goût « water-rich » au-delà de 1,2 dS/m, recommandé ≤ 1 dS/m (2026-garcia#000.0).
- Irrigation : ~30 ml par apport, 6 à 12 apports/jour, ~200-400 ml/plante/jour, drainage visé 20-30 % (2026-garcia#000.0).
- Lumière : 200-250 µmol m-2 s-1 en indoor/appoint ; DLI serre 17-20 mol m-2 j-1 (2026-garcia#001.0) ; spectre 7 % bleu, 16 % vert, 72 % rouge, 5 % far-red (2026-garcia#002.0).
- Nuit : brumisation sous gouttière pour 95 % HR au niveau plante, au moins 3 h par nuit, climats secs (2026-garcia#005.0).
→ reportés dans `benchmarks.csv` : aucune ligne (aucune mesure de modèle).

## Limites et critique

Texte fragmentaire : diapositives sans phrases complètes, la section « Humidité » (2026-garcia#003.0) est vide, le tableau/figure est réduit à une légende (2026-garcia#005.0), la fin du contenu pH (valeurs cibles) est absente. Aucune plage de pH cible chiffrée, aucune température (air ou racines), aucune photopériode. Sources des chiffres non citées (sauf Hoogstraten, Garcia et Kubota 2017). Le blueberry est mélangé au fraise dans la même diapositive (2026-garcia#000.0), à ne pas confondre. Recommandations de producteurs, sans incertitude.

## Consignes chiffrées

Espèce : fraise, culture hors-sol en serre ou indoor (CEA). `n/r` : non rapporté. Myrtille (hors périmètre SerreIA) : apports ≤ 15 min, ~0,15 inch/h, drainage 10-20 % (2026-garcia#000.0), non repris dans le tableau.

| espèce | stade | grandeur | optimal | marginal / limite | unité | condition | chunk_id |
|---|---|---|---|---|---|---|---|
| fraise | tous | EC solution | ≤ 1 | > 1,2 : goût « water-rich », « irrigation with water CAUTION » | dS/m | recommandé | 2026-garcia#000.0 |
| fraise | tous | pH substrat/solution | n/r (dérive normale : lente hausse par absorption de NO3) | baisse = anormal (racines oxydées ou vieilles, bactéries) | pH | pas de valeur cible chiffrée | 2026-garcia#000.0 |
| fraise | tous | volume par apport | ~30 (injecteurs : ~33) | n/r | ml | fréquent plutôt que peu de gros apports | 2026-garcia#000.0 |
| fraise | tous | nombre d'apports | 6 à 12 | n/r | /jour | plante sensible à l'humidité du substrat | 2026-garcia#000.0 |
| fraise | tous | volume par plante | 200 à ~400 | n/r | ml/plante/jour | augmenter la fréquence si besoin | 2026-garcia#000.0 |
| fraise | tous | fraction de drainage | 20-30 | n/r | % | cible de réglage de la fréquence | 2026-garcia#000.0 |
| fraise | tous | intensité lumineuse | 200-250 | plus sensible à l'excès que d'autres cultures (valeur n/r) | µmol m-2 s-1 | indoor et appoint | 2026-garcia#001.0 |
| fraise | tous | DLI | 17-20 | n/r (indoor : DLI plus bas parfois meilleur, valeur n/r) | mol m-2 j-1 | serre | 2026-garcia#001.0 |
| fraise | tous | spectre | 7 % B, 16 % V, 72 % R, 5 % far-red | n/r | % | essai Hoogstraten, effet sur morphologie, rendement | 2026-garcia#002.0 |
| fraise | nuit | HR niveau plante | 95 (brumisation) | n/r | % | ≥ 3 h/nuit, climats secs, induit la guttation | 2026-garcia#005.0 |
| fraise | floraison | ruches | 6 000-8 000 abeilles / 1 000 m2 | n/r | abeilles | densité 8-10 plantes/m2 | 2026-garcia#004.0 |
| fraise | tous | T° air, T° racines, photopériode, HR jour, VPD, CO2 | n/r | n/r | n/r | non rapportés | n/r |

Écart avec SerreIA : `recettes.yaml` n'a pas de recette fraise (tomate, laitue, basilic). Pour compléter la recette proposée dans 2016-depardieu : EC `ec: [1.0, 1.5]` de Depardieu reste cohérente avec la limite haute de ce papier (≤ 1, alerte à 1,2), il faut plutôt viser `ec: [0.8, 1.2]` avec alerte à 1,2 ; `dli_cible` : 17-20 en serre (2026-garcia#001.0), à abaisser en indoor (valeur n/r) ; drainage 20-30 % (Depardieu ~20 %) ; irrigation par petits apports de ~30 ml, 6-12/jour, au lieu d'un seuil horaire de laitue. Toujours n/r : `photoperiode_h`, `co2_max`, température racines, pH cible.

## Pour SerreIA (en plus)

Brumisation nocturne (95 % HR, 3 h) est un cas où la règle mildiou `risk.py` (HR > 90 % > 10 h) ne doit pas déclencher : 3 h < 10 h, mais à surveiller pour botrytis (non traité ici). Vérifier la règle fraise avant d'activer la brumisation.

## Gaps identifiés

- Température de l'air et des racines, photopériode, pH cible, VPD pour la fraise : absents ici (diapositive Humidité vide).
- Spectre far-red à 5 % : pas de source primaire dans la base (Proefcentrum Hoogstraten).

## Statut de lecture

papier complet (fulltext.md de 44 lignes, lu en entier ; texte fragmentaire : diapositives, section « Humidité » vide, figures non extraites, extraction grobid ok).
Déduit et non affirmé par les auteurs : l'écart avec SerreIA, les plages `ec: [0.8, 1.2]` proposées, la remarque sur la règle mildiou ; « optimal » = valeur recommandée dans la diapositive.
