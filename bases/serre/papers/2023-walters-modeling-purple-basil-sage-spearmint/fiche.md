---
id: 2023-walters-modeling-purple-basil-sage-spearmint
fiche: done
date: 2026-10-29
benchmarks: none
---

# Modeling purple basil, sage, spearmint, and sweet basil responses to daily light integral and mean daily temperature

Kellie J Walters, Sean Tarr, Roberto G Lopez, 2023, PLOS ONE 18(11), e0294905. https://doi.org/10.1371/journal.pone.0294905
Type : article de revue (journal), relu par les pairs.

## Problème

Température moyenne journalière (MDT) et DLI interagissent sur la croissance, le développement et la couleur des aromatiques. Les auteurs cherchent l'étendue de ces effets pour le basilic pourpre « Dark Opal », la sauge « Extrakta », la menthe verte « Spanish » et le basilic doux « Nufar », et l'effet sur la couleur du basilic pourpre. Hypothèse : la MDT optimale (MDT opt) croît avec le DLI (Intro, 2023-walters#001.3).

## Méthode

Culture hydroponique (tables à marée) dans cinq compartiments de serre à consignes de MDT de 23, 26, 29, 32 et 35 °C, avec trois DLI par compartiment (0, ~30, ~50 % d'ombrage) donnant 5 à 19 mol·m⁻²·j⁻¹ (§Materials and methods, 2023-walters#023.0). Récolte à 3 semaines (menthe, basilic doux), 4 (basilic pourpre) ou 5 (sauge) après repiquage ; deux répétitions dans le temps. Mesures : ramifications, hauteur, surface foliaire, masse fraîche, matière sèche, Fv/Fm, couleur (angle de teinte h°). Modèles de surface de réponse (Table 2) ; MDT opt et DLI opt obtenus en annulant les dérivées partielles du modèle de masse fraîche (§Fresh mass modeling, 2023-walters#011.3).

## Plateforme et implémentation

Serres de recherche (université d'État du Michigan, d'après les références du matériel ; non relevé dans le texte lu), capteurs thermocouples type E et capteur quantique LI-190R, enregistrement toutes les 15 s, moyennes horaires (2023-walters#003.0, 2023-walters#003.1). Pas de FPGA ni de calcul embarqué : sans objet. Code/modèle : coefficients publiés en Table 2, pas de code.

## Résultats

- Basilic doux : masse fraîche multipliée par 3 (+15 g) quand la MDT passe de 23,0 à 35,7 °C à DLI 5,5 (§Sweet basil, 2023-walters#008.0).
- MDT opt de la masse fraîche : basilic doux 32,6 → 35,5 °C quand le DLI passe de 6 à 11 ; sauge 27,5 → 23,5 ; menthe 30,4 → 27,8 quand le DLI passe de 6 à 18 (Fig. 9, 2023-walters#000.1).
- DLI opt : basilic doux 11,8 → 13,2 mol·m⁻²·j⁻¹ quand la MDT passe de 24 à 32 °C ; sauge 17,9 → 14,4 (Fig. 9, 2023-walters#011.3).
- Basilic pourpre : masse fraîche croissante sur toute la plage testée (MDT opt extrapolée 37,2 °C, jugée peu fiable) (2023-walters#011.0). Plus vert (h° 99 à 138) à ~35 °C quel que soit le DLI ; plus pourpre à ~25 °C avec DLI élevé (h° 335 à DLI 18,7 contre 98 à 5,0) (Abstract, 2023-walters#000.1).
- Ramification de toutes les espèces croissante avec la MDT de ~23 à 35 °C (Abstract).
→ reportés dans `benchmarks.csv` : aucune ligne (article agronomique, pas de benchmark de modèle ; `benchmarks: none`).

## Consignes chiffrées

| espèce | stade | grandeur | optimal | marginal / limite | unité | condition | chunk_id |
|---|---|---|---|---|---|---|---|
| basilic doux « Nufar » | croissance hydroponique (repiquage à récolte, 3 sem.) | MDT opt (masse fraîche) | 32,6 à 35,5 | n/r (supraoptimal non atteint au-delà de 35,7) | °C (T° moyenne 24 h) | DLI 6 → 11 mol·m⁻²·j⁻¹ ; l'optimum monte avec le DLI | 2023-walters#000.1 |
| basilic doux « Nufar » | croissance | DLI opt (masse fraîche) | 11,8 à 13,2 | n/r | mol·m⁻²·j⁻¹ | MDT 24 → 32 °C ; l'optimum monte avec la MDT | 2023-walters#011.3 |
| basilic (T b) | croissance | T° de base | 10,9 (Genovese) ; 10,9 / 11,3 / 11,6 / 12,1 (holy, Nufar, lemon « Sweet Dani », lemon « Lime ») | n/r | °C | valeurs citées d'études antérieures, pas mesurées ici | 2023-walters#001.3 |
| basilic (T opt, cité) | croissance | T° optimale d'après la littérature | 25 à 30 (Genovese, DLI 20-22) ; 29 à 35 (DLI 19,5) | T max « très élevée, rarement atteinte en CEA » (n/r en valeur) | °C | études citées (Chang ; Walters et Currey) | 2023-walters#001.4 |
| basilic pourpre « Dark Opal » | croissance | MDT opt (masse fraîche) | extrapolée 37,2 (non fiable) | n/r | °C | hors plage testée (22,9-35,0) | 2023-walters#011.0 |
| basilic pourpre | croissance | couleur (qualité) | pourpre à ~25 °C et DLI 18,7 (h° 335) | vert à ~35 °C (h° 99-138), quel que soit le DLI | °C / mol·m⁻²·j⁻¹ | compromis rendement / couleur | 2023-walters#000.1 |
| menthe « Spanish » | croissance | MDT opt (masse fraîche) | 30,4 à 27,8 | n/r | °C | DLI 6 → 18, l'optimum baisse | 2023-walters#000.1 |
| sauge « Extrakta » | croissance | MDT opt / DLI opt | 27,5 à 23,5 °C ; DLI opt 17,9 à 14,4 | n/r | °C ; mol·m⁻²·j⁻¹ | DLI 6 → 18 ; MDT 24 → 32 | 2023-walters#000.1, 2023-walters#011.3 |
| menthe, sauge (citées) | croissance | DLI opt de la littérature | 14,9 (menthe) ; 15,9 (sauge) | n/r | mol·m⁻²·j⁻¹ | étude citée [40], DLI testé 2 à 20 | 2023-walters#011.1 |
| aromatiques (propagation) | semis / bouturage | photopériode ; DLI cible ; MDT | 16 h ; 10 mol·m⁻²·j⁻¹ ; ~23 °C | n/r | h ; mol·m⁻²·j⁻¹ ; °C | éclairage HPS ~80 µmol·m⁻²·s⁻¹ | 2023-walters#003.1 |
| menthe (bouturage) | enracinement | VPD | 0,3 | n/r | kPa | bouturage sous brumisation et injection de vapeur, 1 semaine | 2023-walters#003.0 |
| toutes | croissance | T° jour / nuit séparées ; HR ; CO₂ ; pH ; EC ; irrigation | n/r | n/r | n/r | seule la MDT est pilotée (consigne par compartiment) ; T° de la solution mesurée (22 à 31 °C selon MDT, Table 1) mais non régulée | 2023-walters#024.0 |

Écart avec SerreIA : recette `basilic-standard` (croissance) = jour 20-27 °C, nuit 16-20 °C, HR 50-70 %, 16 h, DLI cible 15, pH 5,8-6,5, EC 1,0-1,6. Une MDT de ~21-24 °C (déduit de ces plages, non écrit dans le papier) est bien sous la MDT opt de masse fraîche du basilic doux (32,6 à 35,5 °C) ; la recette privilégie donc la qualité/économie d'énergie plutôt que le rendement maximal, ce que le papier n'évalue pas pour le basilic doux (seul le basilic pourpre est évalué en couleur). DLI cible 15 : légèrement au-dessus du DLI opt du basilic doux (11,8-13,2 à 24-32 °C) ; au-delà, gain de masse non démontré. Photopériode 16 h : concordante avec la propagation seulement ; HR, pH, EC, nuit : le papier ne dit rien (n/r).

## Limites et critique

- MDT seule : pas de séparation jour/nuit (DIF), pas de HR, VPD, CO₂ ni de pH/EC rapportés pour la phase de croissance dans les passages lus ; consignes non transposables telles quelles en consignes jour/nuit.
- Optimum défini sur la masse fraîche seule, à récolte fixe (3 à 5 semaines) : pas de qualité aromatique, pas de coût énergétique, pas de rendement par kWh.
- Le DLI s'obtient par ombrage : lumière naturelle de serre, ce qui lie DLI, rayonnement et température de feuille (feuille à 35,9 °C pour MDT 35 °C, Table 1) ; effet photopériode non séparé.
- MDT opt du basilic doux (35,5 °C) proche du haut de la plage testée (35,7 °C) : optimum à la limite expérimentale ; celui du basilic pourpre est extrapolé (37,2 °C).
- Un seul cultivar par espèce, deux répétitions, hydroponie à marée : généralisation à NFT ou goutte-à-goutte non prouvée.
- Les valeurs de T b et T opt dans l'introduction sont des citations d'autres études, pas des résultats ici.

## Pertinence pour SerreIA

- Basilic : fournit un modèle quantitatif (MDT opt croissante avec le DLI, DLI opt croissant avec la MDT) pour fixer la T° moyenne visée selon le DLI du jour. SerreIA peut remplacer la consigne fixe par une consigne MDT dépendant du DLI prévu (utile avec la prévision GRU), plafonnée par la qualité visée.
- Le DLI cible de 15 de la recette peut être abaissé à ~12-13 pour le basilic doux sans perte de masse prédite autour de 24-32 °C : économie d'éclairage d'appoint (à valider, données propres à « Nufar »).
- Basilic pourpre : au-dessus de ~30 °C la couleur vire au vert ; à garder en règle de qualité si SerreIA cultive une variété pourpre.
- T b ≈ 11 °C : base pour un calcul de degrés-jours (développement) et un plancher d'alerte froid de la recette.
- À ne pas reprendre : HR, pH, EC, photopériode de croissance, T° nuit : le papier n'en donne pas ; garder les sources de la recette.

## Gaps identifiés

- Consignes jour/nuit, HR/VPD, pH/EC et photopériode du basilic en croissance : absentes de ce papier, à chercher ailleurs pour étayer `recettes.yaml`.
- Optimum en rendement par énergie (chauffage + lumière) pour le basilic en serre : non traité.
- Modèle MDT-DLI pour laitue, tomate et fraise (autres cultures de SerreIA) : absent.

## Statut de lecture

Résumé et sections lues par passages : Abstract, Introduction (T b/T opt), Materials and methods (production, mesures), Results (sections basilic doux et pourpre en partie), Discussion (§Fresh mass modeling, Color), Table 1 (partiel). `extraction.backend` = grobid, ok. Papier non lu en entier : Table 2 (coefficients des modèles) et plusieurs figures non exploitées. Déduit et non affirmé par les auteurs : la MDT équivalente de la recette de SerreIA, l'affiliation des serres, le fait que la lumière soit naturelle (ombrage par toiles ; pas de précision sur l'appoint HPS en phase de croissance).
