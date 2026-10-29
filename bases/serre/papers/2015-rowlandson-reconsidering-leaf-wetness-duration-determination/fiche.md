---
id: 2015-rowlandson-reconsidering-leaf-wetness-duration-determination
fiche: done
date: 2026-10-29
benchmarks: none
---

# Reconsidering Leaf Wetness Duration Determination for Plant Disease Management

Tracy Rowlandson, Mark Gleason, Paulo Sentelhas, Terry Gillespie, Carla Thomas, Brian Hornbuckle. Plant Disease 99(3), 310–319, 2015. https://doi.org/10.1094/PDIS-05-14-0529-FE
Type : article de revue (feature article / synthèse), relu par les pairs.

## Problème

La durée d'humectation foliaire (LWD) conditionne le risque de nombreuses maladies fongiques et bactériennes, mais ce n'est pas une mesure météo standard (#002.2). Les capteurs électroniques posent des problèmes de peinture, placement, calibration et maintenance (#004.2). Les auteurs demandent s'il faut continuer à les utiliser ou passer à des estimations par modèle.

## Méthode

Revue de littérature, sans expérience propre. Elle couvre : les sources d'humectation (pluie, brouillard, irrigation, rosée, guttation) ; les capteurs (mécaniques, grille résistive/impédance) et leurs pièges ; les modèles : « no fewer than 20 models » (#006.2), physiques (bilan d'énergie, une ou deux sources), empiriques (seuil d'HR) et hybrides (CART/SLD, logique floue) (#006.2, #006.3, #007.0).

## Plateforme et implémentation

Sans objet (pas d'implémentation). Pas de code. Capteurs cités : Campbell 237-L, Decagon (Fig. 6) ; station météo à 1,5 m (#009.2).

## Résultats

- Modèle empirique : LWD = nombre d'heures où HR à 1,5–2,0 m est ≥ 90 % (#006.4). Valable seulement dans la région de calibration ; seuil ajusté à 83 % (Ames, Iowa), 85 % (Elora, Ontario), 92 % (Florence, Italie), 90 % (Piracicaba, Brésil) (#006.5, Fig. 11).
- Avec le seuil de 90 % unique, le modèle sous-estime la LWD aux États-Unis, au Canada et au Brésil et la surestime en Italie ; avec un seuil propre à chaque site, la précision est « acceptable » (#009.1). Aucune valeur d'erreur (MAE, RMSE) n'est donnée dans cette revue : `n/r`.
- Modèles physiques : précis mais dépendants de nombreuses variables météo, et de la qualité de ces données (#009.0) ; deux sources : il faut texture et humidité du sol (#006.3). Impraticables pour les utilisateurs finaux.
- CART/SLD : entrées vent, dépression du point de rosée, T°, HR ; classe les heures en probable / improbable / incertain, puis deux équations empiriques donnent la durée (#007.0).
- Recommandation : utiliser le modèle à seuil d'HR, avec un seuil local trouvé par observation visuelle (apparition des gouttelettes = début ; fin = au moins 80 % de la canopée sèche), seuil attendu entre 80 et 95 %, mesuré sur au moins cinq occasions (#009.2).
- Capteurs : erreur capteur/observation visuelle < 1 h selon l'angle (#005.0) ; repeindre au moins une fois par an (#005.1) ; peinture gris très clair (#004.2) ; dew maximal aux 3/4 de la hauteur de canopée (#004.4).
→ reportés dans `benchmarks.csv` : aucune ligne (revue sans mesure propre).

## Consignes chiffrées

| espèce | stade | grandeur | optimal | marginal / limite | unité | condition (jour/nuit, lumière…) | chunk_id |
|---|---|---|---|---|---|---|---|
| générique (toutes cultures) | n/r | seuil d'HR proxy de l'humectation (provisoire) | 90 | n/r | % HR | HR mesurée à 1,5–2,0 m ; LWD = nb d'heures ≥ seuil | 2015-rowlandson#006.4 |
| générique | n/r | seuil d'HR recalibré, Ames (Iowa) | 83 | n/r | % HR | seuil par site, extérieur | 2015-rowlandson#006.5 |
| générique | n/r | seuil d'HR recalibré, Elora (Ontario) | 85 | n/r | % HR | idem | 2015-rowlandson#006.5 |
| générique | n/r | seuil d'HR recalibré, Florence (Italie) | 92 | n/r | % HR | idem | 2015-rowlandson#006.5 |
| générique | n/r | seuil d'HR recalibré, Piracicaba (Brésil) | 90 | n/r | % HR | idem | 2015-rowlandson#006.5 |
| générique | n/r | plage attendue du seuil d'HR local | n/r | 80 à 95 (plus haut en climat humide) | % HR | à établir par observation visuelle ≥ 5 occasions | 2015-rowlandson#009.2 |
| générique | n/r | critère de fin d'humectation (observation) | n/r | ≥ 80 % de la canopée sèche | % canopée | début = première apparition de gouttelettes | 2015-rowlandson#009.2 |
| générique | n/r | hauteur de mesure T°/HR | 1,5 | n/r | m | norme station météo (WMO) | 2015-rowlandson#009.2 |
| générique | n/r | hauteur du dew maximal dans la canopée | ~0,75 de la hauteur | n/r | fraction | canopées denses | 2015-rowlandson#004.4 |
| générique | n/r | T° d'infection, durée LWD minimale par pathogène | n/r | n/r | n/r | seulement en Fig. 1 / Table 1 (non chiffrés dans le texte) | n/r |
| toutes | n/r | T° air/racines, VPD, DLI, photopériode, CO₂, pH, EC, irrigation | n/r | n/r | n/r | n/r | n/r |

Écart avec SerreIA : la règle de SerreIA (`RisqueCfg` : hr_humectation 90 %, humectation_h 10 h, 10–25 °C ; vision_rules : HR > 85 % ou humectation > 10 h) reprend le seuil provisoire de 90 % du papier, mais comme valeur fixe. Le papier montre que ce seuil varie de 83 à 92 % selon le site et recommande de le calibrer localement (≥ 5 observations visuelles) ; il ne chiffre ni les 10 h ni la plage 10–25 °C (renvoi à Fig. 1 / Table 1, sans valeur dans le texte). Le papier est écrit pour des cultures de plein champ : en serre, toute extrapolation de 90 % est non couverte (déduit).

## Limites et critique

- Revue sans protocole de recherche ; erreurs des modèles non chiffrées dans le texte (elles sont dans Sentelhas et al. 2008, citée Fig. 11).
- Plein champ et vergers uniquement : la serre (pas de rosée par rayonnement vers le ciel, pas de pluie, ventilation et brumisation propres) n'est pas traitée (déduit).
- La recommandation « HR seule » est un compromis de standardisation ; elle ignore le vent, la dépression du point de rosée et la T° de feuille que les modèles hybrides utilisent.
- Table 1 (systèmes d'alerte) reconstruite par PyMuPDF : non exploitée ici, chiffres à vérifier.

## Pertinence pour SerreIA

Base directe pour remplacer la règle de mildiou codée en dur :
1. Faire du seuil `hr_humectation` un paramètre calibré par serre : relever sur ≥ 5 événements l'humectation observée (début des gouttelettes, fin à 80 % de feuilles sèches, #009.2) et chercher le seuil dans 80–95 %, au lieu de 90 % fixe.
2. Mesurer HR/T° à hauteur de canopée plutôt qu'à 1,5 m de station ; vu que la serre est un microclimat, le seuil serait à recalibrer (déduit).
3. Option plus robuste : modèle hybride type CART/SLD (dépression du point de rosée, vent, T°, HR), calculable avec les capteurs ESP32 existants plus un anémomètre ; ou capteur d'humectation peint (gris clair, recalibré chaque année, #004.2, #005.1) pour valider le proxy.
4. Le seuil de durée (10 h) et la fenêtre de T° doivent venir d'une autre source (courbes LWD–T° par pathogène, non chiffrées ici).
5. Valider la règle sur les ~5 événements ci-dessus avant de laisser l'agent agir automatiquement.

## Gaps identifiés

- Valeurs LWD minimale / T° d'infection pour Phytophthora infestans, Botrytis, mildiou de la laitue et du basilic en serre : à chercher (papier source de la Fig. 1).
- Précision (MAE) des modèles de LWD en serre : n/r.
- Consignes de culture (T°, VPD, DLI, pH, EC) : hors périmètre de ce papier.

## Statut de lecture

Sections lues : tout le texte via recherche ciblée et `show` (chunks #002, #004–#009, #017) ; `fulltext.md` non lu en entier (consigne de la base). Extraction grobid, Table 1 reconstruite par PyMuPDF (non exploitée).
Déduit et non affirmé par les auteurs : l'inapplicabilité des conclusions à la serre ; la recalibration du seuil à hauteur de canopée ; l'usage d'un anémomètre sur ESP32 ; la comparaison avec la règle SerreIA.
