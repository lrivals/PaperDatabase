---
id: 2025-cebolla-alemany-short-term-forecasting-predictive-control
fiche: done
date: 2026-10-29
benchmarks: none
---

# Short-term forecasting and predictive control of rooftop greenhouse microclimate using multi-horizon machine learning models

Joaquim Cebolla-Alemany, Yunyao Cheng, Laia Pintó-Espín, Michele Albano, Marcel Macarulla, Santiago Gassó-Domingo, 2025, venue : n/r dans le texte extrait (le préfixe DOI `atech` suggère Smart Agricultural Technology : déduit, à vérifier). https://doi.org/10.1016/j.atech.2025.101733
Type : article de revue (déduit du DOI Elsevier ; non confirmé par le texte).

## Problème

Serre sur toit intégrée à un bâtiment (faible inertie thermique, échanges intérieur/extérieur rapides) : prévoir la température intérieure à 5, 10 et 15 min pour une commande prédictive de la ventilation (#000.0, #005.1). Cadre « data-driven MPC » compatible jumeau numérique.

## Méthode

- Données : 1 an à pas de 5 min, T, HR, ePAR intérieures, état du ventilateur, + station météo à 400 m (T, HR, vent, rayonnement) (#004.1). 1 030 797 points, 916 256 après dédoublonnage, 36 573 points réparés (#011.0). Interpolation temporelle puis KNN (k = 5) (#005.0).
- Entrées engineered : cibles t+h, h ∈ {5, 10, 15} min ; lags {5, 10, 15, 20, 30} min ; différences d'ordre 1 ; moyenne/écart-type glissants sur N ∈ {6, 12, 24} pas (30, 60, 120 min) ; écarts intérieur-extérieur (T, HR) ; variables actionneur (minutes depuis dernier on/off, somme glissante) (#005.2).
- Sept régresseurs, un par horizon : DT, RF, GBR, XGBoost, LightGBM, SVR-RBF, MLP ; split 80/20 et validation croisée à fenêtre glissante, score MAE ; SHAP pour l'interprétabilité (#006.1, #006.2). Hyperparamètres : n/r dans le texte lu (config YAML).
- Commande : ventilateur on/off, consigne 26 °C, bande ±1 °C, comparée à la moyenne des trois prévisions ; « prévision corrigée » (mesure réelle à t substituée à la prévision en entrée du multi-pas) (#009.0). Variante floue Mamdani : trois termes (bas ≤ 16–20 °C, optimal 18–27 °C triangulaire sommet 23 °C, haut ≥ 26–30 °C), sortie binarisée à 0,5 (#009.2). Coûts : énergie = 0,2 × marche × 5 min ; pénalité = max(0, |T − 26| − 1) (#010.0).

## Plateforme et implémentation

Serre Venlo de 15 m² (5 × 3 m), polycarbonate 10 mm, toit de l'ESEIAAT/UPC à Terrassa (Espagne), ventilation mécanique 5760 m³/h, ventilateur 0,75 kW ; capteurs Apogee SME-600 (intérieur) et Davis Vantage Pro2 (extérieur) (#004.1). Matériel d'inférence (CPU/GPU/MCU) : n/r ; seuls les temps d'entraînement sont donnés (#012.0). Puissance du calculateur : n/r. Code publié : n/r dans le texte lu.

## Résultats

Table 4 (test, température intérieure en °C) (#032.0, #032.1) :

| Modèle | MAE +5 | RMSE +5 | MAE +10 | RMSE +10 | MAE +15 | RMSE +15 |
|---|---|---|---|---|---|---|
| LightGBM | 0,280 | 0,638 | 0,310 | 0,703 | 0,311 | 0,728 |
| XGBoost | 0,281 | 0,643 | 0,320 | 0,724 | 0,321 | 0,740 |
| RF | 0,286 | 0,678 | 0,317 | 0,729 | 0,334 | 0,758 |
| MLP | 0,335 | 0,857 | 0,354 | 0,771 | 0,372 | 0,855 |
| DT | 0,347 | 0,810 | 0,367 | 0,835 | 0,358 | 0,859 |

R² de LightGBM : 0,993 / 0,992 / 0,991 (+5/+10/+15 min) (#012.0, #012.2). Pas de baseline persistance ni de réseau récurrent (LSTM/GRU) : n/r.
- Entraînement 5 min : XGBoost 4,2 s (validation croisée) + 0,8 s ; LightGBM 8,0 s + 1,0 s ; SVR-RBF 411 s + 270 s (#012.0).
- Erreurs : majoritairement dans ±0,2 °C ; MAE horaire maximale d'environ 0,9 °C à 14 h ; pires erreurs à plus de 25 °C et autour de la consigne (commutations du ventilateur) (#013.1). Test indépendant de 33 jours (31 mars-2 mai) hors entraînement/validation, évalué qualitativement (graphique) : pas de métrique chiffrée (#013.2).
- Commande : le flou réduit le coût cumulé de plus de 65 % sur une journée de 24 h (#014.2) ; « plus de 60 % d'économie d'énergie » dans le résumé et la conclusion (#018.1). Le contrôleur à seuil est observé, le flou est simulé (#014.0). Littérature citée : 10-30 % pour le MPC en serre de taille comparable (#017.0).
→ reportés dans `benchmarks.csv` : aucune ligne (modèles de régression de température sur CPU, sans latence, fps ni puissance ; tableau MAE/RMSE laissé dans la fiche, la grandeur n'entre pas dans le vocabulaire de benchmarks).

## Limites et critique

- Horizon de 5 à 15 min seulement : très court devant la dynamique de la serre et loin d'un +1 h/+6 h ; l'écart entre horizons est minime (MAE 0,28 → 0,31), ce qui suggère que le modèle exploite surtout l'inertie récente (lags, état du ventilateur), sans baseline de persistance pour le vérifier (déduit).
- Une seule serre, un an, un lieu, une culture ; volume minimal de données non étudié (#017.2).
- Un seul jour de commande évalué, flou simulé et non appliqué ; l'économie de 60-65 % tient surtout aux commutations du seuil nu (pas d'hystérésis ni de temps minimal marche/arrêt) : baseline faible (déduit). Pénalités de confort de définitions différentes entre seuil et flou (#010.0), donc non strictement comparables.
- Seule la température est prévue ; HR, rayonnement et CO₂ en travaux futurs (#018.3). Pas de comparaison à des réseaux séquentiels malgré leur citation en introduction (#002.2).
- Hyperparamètres et code : n/r.

## Pour SerreIA

- **`edge/controller/forecast.py` (GRU, 24 h à 10 min, +1 h/+6 h)** : ajouter comme baselines de validation, avant de justifier le GRU, une persistance et un LightGBM/XGBoost à features construites (lags 5-30 min, moyennes glissantes 30/60/120 min, écarts int-ext, état des actionneurs). Ici LightGBM atteint MAE 0,28-0,31 °C à +5/+15 min (#032.0, #032.1) avec 4 à 8 s d'entraînement (#012.0), exécutable sur le Pi 5 sans torch. Métrique de validation : MAE/RMSE par horizon, sur un bloc de test final contigu (pas de fuite), plus validation croisée à fenêtre glissante (#006.1).
- **Horizons** : le papier ne dit rien de +1 h/+6 h ; ne pas extrapoler ses erreurs. Ajouter dans `forecast.py` un horizon court (+5 à +15 min) pour la commande, +1 h pour l'anticipation (ventilation préventive HR, risque mildiou dans `risk.py`).
- **Entrée « état des actionneurs »** : le papier en fait une entrée explicite (minutes depuis le dernier on/off, somme glissante) (#005.2) et attribue les pires erreurs aux commutations du ventilateur (#013.1) ; le plan GRU de SerreIA les prévoit déjà, à conserver et à ablater.
- **Commande** : prévision corrigée (mesure remplaçant la prévision à t, #009.0) = pratique à reprendre dans `rules.py` si on boucle la prévision ; éviter le on/off nu : hystérésis ou logique floue (3 termes, binarisation à 0,5, #009.2) pour réduire les commutations du ventilateur. À mesurer dans `sim/` : nombre de commutations par jour et coût énergie + pénalité (#010.0).
- **Écart de domaine** : serre de 15 m² en climat méditerranéen, consigne 26 °C ±1 °C (tomate) ; recalibrer les seuils par culture. Interprétabilité SHAP utile pour la traçabilité des décisions (docs/10) et pour la validation humaine.
- Pièges : fuite temporelle (split aléatoire), imputation (interpolation puis KNN) à reproduire à l'identique en ligne, derive saisonnière non évaluée sur un an unique.

## Gaps identifiés

- Aucune comparaison publiée ici GRU/LSTM vs arbres boostés, ni persistance, aux horizons 1 h et 6 h en serre.
- Commande prédictive validée sur une seule journée ; pas d'essai réel du flou.
- Prévision multivariée (HR, CO₂, rayonnement) et multi-actionneurs : travaux futurs de l'article.

## Statut de lecture

Papier complet (sections 1-5 lues par recherche et lecture par tranches ; introduction et références seulement survolées). Extraction grobid ; Table 2 (liste de métriques) sans corps extrait, sans conséquence ; Table 4 recoupée avec le texte.
Ce qui suit est déduit et non affirmé par les auteurs : venue et type (d'après le DOI), absence de baseline de persistance (non mentionnée), faiblesse de la baseline à seuil, extrapolation aux horizons +1 h/+6 h, reprises pour SerreIA.
