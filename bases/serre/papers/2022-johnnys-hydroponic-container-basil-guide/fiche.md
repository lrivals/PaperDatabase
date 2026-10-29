---
id: 2022-johnnys-hydroponic-container-basil-guide
fiche: done
date: 2026-10-29
benchmarks: none
---

# Hydroponic & Container Basil: Variety Selection Guide

Johnny's Selected Seeds (auteur institutionnel), 2022, grower guide commercial, DOI : n/r, URL : n/r.
Type : littérature grise, **source commerciale** d'un semencier (rapport technique non relu par les pairs, sans méthode ni données d'essai publiées).

## Problème

Aider un producteur à choisir une variété de basilic (Genovese, Italian Large Leaf…) selon le produit final (plante en pot, feuilles, baby-leaf), la vigueur, la résistance aux maladies, avec des conseils de culture en conteneur et en hydroponie (2022-johnnys#000.0, #004.0).

## Méthode

Aucune méthode expérimentale. Le guide s'appuie sur des « essais de producteurs hydroponiques indépendants » combinés aux connaissances du semencier et de ses fournisseurs, sans données ni protocole (§Variety Recommendations, 2022-johnnys#003.0). Le tableau comparatif des variétés est un PDF externe, absent du texte extrait.

## Plateforme et implémentation

Sans objet (pas de matériel). Code/bitstream : non publiés, sans objet.

## Résultats

Consignes générales pour le basilic hydroponique (§Tips for Hydroponic Growers, 2022-johnnys#008.0) : température 18-21 °C (65-70 °F), pH 5,8-6,2, lumière minimum 14 h/jour, DLI minimum 12 mol/m²/j « ou plus », EC 1,0-1,4 mS/cm, plus élevée en hiver qu'en été. Cycle d'environ 28 jours en hydroponie dans des conditions optimales (2022-johnnys#000.0). Maladies : mildiou du basilic (« basil downy mildew », un oomycète) et fusariose, graines testées sans Fusarium, variétés résistantes proposées (2022-johnnys#005.0). Conseil : cultiver le basilic isolé des autres cultures pour ajuster solution nutritive et environnement (2022-johnnys#009.0).
→ reportés dans `benchmarks.csv` : aucune ligne (aucune mesure de modèle).

## Consignes chiffrées

Cultures hydroponiques, uniquement conditions « générales recommandées » ; aucune plage jour/nuit, aucun stade, aucune humidité.

| espèce | stade | grandeur | optimal | marginal / limite | unité | condition | chunk_id |
|---|---|---|---|---|---|---|---|
| basilic | n/r (culture entière) | température | 18-21 (65-70 °F) | n/r | °C | hydroponie, jour/nuit non distingués | 2022-johnnys#008.0 |
| basilic | n/r | pH | 5,8-6,2 | n/r (« légèrement plus haut » en aquaponie / bio, valeur n/r) | pH | hydroponie | 2022-johnnys#008.0 |
| basilic | n/r | EC | 1,0-1,4 | n/r (plus haut en hiver, valeur n/r) | mS/cm | selon saison | 2022-johnnys#008.0 |
| basilic | n/r | photopériode | ≥ 14 | n/r | h/jour | minimum | 2022-johnnys#008.0 |
| basilic | n/r | DLI | ≥ 12 | n/r (« ou plus ») | mol/m²/j | minimum | 2022-johnnys#008.0 |
| basilic | n/r | humidité relative | n/r | n/r | % | n/r | n/r |
| basilic | n/r | humidité / conditions du mildiou | n/r | n/r | n/r | non traité | n/r |

**Écart avec SerreIA** (`edge/controller/recettes.yaml`, `basilic-standard`, stade croissance) :
- Température : recette jour 20-27 / nuit 16-20 °C ; guide 18-21 °C sans distinction jour/nuit : la plage jour de SerreIA monte jusqu'à 27 °C, au-dessus de la recommandation (déduit, comparaison indicative).
- pH : recette 5,8-6,5 vs 5,8-6,2 : borne haute plus large.
- EC : recette 1,0-1,6 vs 1,0-1,4 (le guide module selon la saison, la recette est fixe) : borne haute plus large, pas de modulation saisonnière.
- Photopériode : recette 16 h vs minimum 14 h : compatible.
- DLI cible : recette 15 vs minimum 12 mol/m²/j : compatible (cible au-dessus du minimum).
- Humidité 50-70 % : non couverte par ce guide (n/r) ; humidite_sol 40-65 % sans objet en hydroponie.

## Limites et critique

Source commerciale d'un vendeur de semences : conseils génériques, non sourcés, sans protocole ni variance ; le guide encourage à faire ses propres essais (§Tips for Hydroponic Growers). Pas de stade, pas de jour/nuit, pas d'humidité ni de VPD, pas de CO₂. Le mildiou n'est que nommé : ni agent (Peronospora belbahrii non cité dans le texte), ni conditions d'infection (humidité, durée d'humectation), ni seuil ; il ne permet pas de valider la règle HR>90 % >10 h de `risk.py`. Les valeurs ne sont pas comparables à des mesures de serre réelle (hydroponie, variétés Johnny's).

## Pertinence pour la thèse

Baseline de pratiques pour le basilic de SerreIA (axes `crop-practices`, `climate-control`) : recoupement avec `recettes.yaml` pour pH, EC, photopériode et DLI ; à croiser avec une source académique avant de resserrer les bornes. Apport sanitaire limité : confirme que le mildiou est une des deux maladies principales du basilic (2022-johnnys#005.0), donc justifie une classe/règle dédiée.

## Gaps identifiés

- Consignes basilic jour/nuit, humidité et VPD absentes : source académique à chercher.
- Conditions d'infection du mildiou du basilic (HR, durée d'humectation, T°) pour valider `risk.py`.
- Modulation saisonnière de l'EC (hiver vs été) : non implémentée dans `recettes.yaml`.

## Statut de lecture

Papier complet (7 Ko, lu via Read ; chunks cités vérifiés par `pdb verify`,). Texte GROBID, tableau des variétés et tableau des taux de semis (« Seeding Basil ») sans valeurs exploitables. Déduit et non affirmé par les auteurs : tout l'écart avec SerreIA, et la remarque sur la compatibilité des cibles DLI/photopériode.
