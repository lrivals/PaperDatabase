---
id: 2020-miller-maximizing-productivity-greenhouse-grown-hydroponic
fiche: done
date: 2026-10-29
benchmarks: none
---

# Maximizing Productivity of Greenhouse-grown Hydroponic Lettuce during Winter

Alexander Miller, Petrus Langenhoven, Krishna Nemali, 2020, HortScience 55(12), 1963–1969. https://doi.org/10.21273/HORTSCI15351-20
Type : article de revue (journal), relu par les pairs.

## Problème

L'éclairage d'appoint (SL) et le chauffage rendent la laitue de serre hivernale coûteuse dans le nord des États-Unis ; peu de données guident le choix de la composition spectrale du SL, du chauffage (air ou racines), du système hydroponique (PS) et du cultivar (§Introduction, 2020-miller#001.1).

## Méthode

Serre en verre (lieu : n/r dans les passages lus ; Purdue, Indiana, déduit de l'adresse de l'auteur), janvier-février 2019, air maintenu sous-optimal : 15,0 °C jour, 12,6 °C nuit, 13,7 °C sur 24 h ; HR non contrôlée, 31,7 % en moyenne (2020-miller#003.0). Plan en split-plot, 4 répétitions, 1536 plantes (2020-miller#004.4) : 3 éclairages (NSL sans SL ; WSL spectre large R35:G42:B23 la nuit ; PSL spectre étroit R90:G0:B10 la nuit, LED Fluence Ray 44), 2 températures de solution (chauffée à 20 °C par résistance : mesurée 18,8 °C ; non chauffée : 13,2 °C), 2 PS (CFT, racines immergées ; NFT, racines partiellement dans l'air), 8 cultivars (2020-miller#004.0, #004.2, #004.3). Semis en cubes de rockwool, transplantation à 10 jours, récolte au 40e jour (2020-miller#003.1, #005.0). Mesures : masse sèche aérienne (SDW, g/m²) et teneur en eau (SWC, %), densité 44 (NFT) et 42 (CFT) plantes/m² (2020-miller#005.0).

## Plateforme et implémentation

Sans objet (pas de calcul embarqué). Matériel : capteurs Apogee (quantique SQ110, T° ST110) sur enregistreur Campbell CR1000x, relevés horaires moyennés par jour (2020-miller#005.0). Code et données : non publiés.

## Résultats

- SDW maximale avec PSL + solution chauffée à 18,8 °C ; sans SL, la solution chauffée n'apporte pas de gain significatif (2020-miller#007.0, #009.0).
- Avec SL, SDW plus élevée même avec solution non chauffée (2020-miller#007.0).
- PSL > WSL de +47 % (CFT) et +42 % (NFT) ; PSL > NSL de +228 % (CFT) et +51 % (NFT) (2020-miller#007.2).
- Gain de la solution chauffée plus fort en CFT qu'en NFT (SDW et SWC) ; CFT > NFT même sans chauffage (2020-miller#007.1, #008.0).
- Effet du chauffage présent chez tous les cultivars verts, absent chez 3 cultivars rouges sur 4 (Navara, Alkindus, Breen) (2020-miller#007.4).
- Les valeurs absolues de SDW/SWC ne figurent que dans les figures 3-5 et les Tables 2A-C, illisibles dans le texte extrait : non relevées ici.
→ reportés dans `benchmarks.csv` : aucune ligne (étude agronomique, pas de FPS/précision de modèle ; `benchmarks: none`).

## Consignes chiffrées

| espèce | stade | grandeur | optimal | marginal / limite | unité | condition (jour/nuit, lumière…) | chunk_id |
|---|---|---|---|---|---|---|---|
| laitue | croissance (10 à 40 j après semis) | T° air | 20–24 (littérature citée) | mesuré 12,2–15,2 (journalière), moyenne 13,7 : « bien en dessous de l'optimal » | °C | serre d'hiver ; jour 15,0, nuit 12,6 (moyennes mesurées) | 2020-miller#006.1 ; 2020-miller#003.0 |
| laitue | croissance | T° solution (racines) | 18,8 (chauffée, consigne 20) donne la SDW max avec PSL | 13,2 (non chauffée) : gain absent sans SL ; plage mesurée 16,5–21,3 (chauffée), 11,6–15,8 (non chauffée) | °C | air à 13,7 °C ; effet plus fort en CFT qu'en NFT | 2020-miller#004.3 ; 2020-miller#006.2 ; 2020-miller#009.0 |
| laitue | croissance | T° air avec racines à 24 °C | rendements comparables entre 17 et 24 (Thompson et al., 1998, cité) | n/r | °C | beurre (butterhead), solution à 24 °C | 2020-miller#001.3 |
| laitue | croissance | HR | n/r | non contrôlée, 31,7 ± 12,81 en moyenne | % | serre d'hiver, pas de seuil de risque testé | 2020-miller#003.0 |
| laitue | croissance | VPD | n/r | n/r | kPa | n/r | n/r |
| laitue | croissance | DLI | 12–15 (littérature citée) | 5,8 ± 1,75 (soleil seul, « près de la moitié de l'optimal ») ; SL : 12,4 ± 1,50 (WSL), 11,9 ± 2,63 (PSL) ; soleil mesuré 3,0–10,2 | mol·m⁻²·j⁻¹ | SL apportait 6,56 (WSL) et 6,04 (PSL) la nuit | 2020-miller#001.0 ; 2020-miller#006.0 ; 2020-miller#006.1 ; 2020-miller#004.2 |
| laitue | croissance | photopériode | 24 (PSL, WSL : SL nocturne prolongeant le jour) | 10,5 (NSL, soleil seul) | h | éclairage continu testé, pas de comparaison 16 h | 2020-miller#004.2 |
| laitue | croissance | spectre du SL | R90:G0:B10 (PSL) > R35:G42:B23 (WSL) | bleu > 15 % du total : croissance végétative réduite (Zhang et al., 2018, cité) | % R:G:B | SL nocturne ; soleil intérieur R35:G34:B31 | 2020-miller#004.1 ; 2020-miller#006.3 |
| laitue | croissance | CO2 | n/r | n/r | ppm | non étudié | n/r |
| laitue | croissance | pH | n/r | n/r | n/r | non rapporté | n/r |
| laitue | pépinière (0–10 j) | EC solution | 0,25 | n/r | dS·m⁻¹ | solution diluée (22 mg·L⁻¹ N), cubes rockwool | 2020-miller#003.1 |
| laitue | croissance | EC solution (programme) | 0,5–0,75 (j 1–20) ; 0,75–1,0 (j 21–30) ; 1,0–2,0 (j 31–40) | dérive > 2,0 au jour 35 par évaporation : correction à l'eau claire ; moyenne 0,98 ± 0,229 | dS·m⁻¹ | ajustée à la croissance, non comparée à d'autres valeurs | 2020-miller#006.0 |
| laitue | croissance | densité | 44 (NFT), 42 (CFT) | n/r | plantes·m⁻² | non variée comme facteur | 2020-miller#005.0 |
| laitue | croissance | irrigation / débit | n/r | n/r | n/r | CFT inondé en continu, NFT en film (pompes 530 L/h, réservoirs 76 L) | 2020-miller#003.1 |
| laitue | croissance | seuils de risque maladie | n/r | n/r | n/r | non traité | n/r |

**Écart avec SerreIA** (recette `laitue-hydro`, stade croissance : T° jour 16–22 °C, nuit 12–16 °C, HR 50–70 %, photopériode 16 h, DLI cible 14, pH 5,6–6,2, EC 1,0–1,6) :
- T° air : l'optimal cité par Miller (20–24 °C) dépasse la plage jour de SerreIA (16–22) ; la plage nuit (12–16) recoupe la nuit de l'essai (12,6 °C). Écart marginal sur le jour, mais l'article ne teste pas l'air à 20–24 °C : valeur de revue, pas résultat.
- DLI : cible 14 de SerreIA dans l'intervalle 12–15 cité par Miller. Accord.
- Photopériode : 16 h dans SerreIA, 24 h dans l'essai (SL nocturne) : non comparable, Miller ne teste pas 16 h.
- EC : SerreIA 1,0–1,6 ; Miller applique 0,5–1,0 jusqu'au jour 30 puis 1,0–2,0 (moyenne 0,98) : la recette n'a pas de programme par âge ; sa borne basse 1,0 serait trop haute pour les 30 premiers jours.
- T° solution : absente de `recettes.yaml` ; Miller montre un gain à 18,8 °C contre 13,2 °C. Lacune de la recette.
- HR : SerreIA 50–70 % ; Miller 31,7 % non contrôlée, sans effet mesuré. pH, CO2, VPD : n/r.

## Limites et critique

- Un seul site, un seul hiver (janv.-févr. 2019), une seule saison ; DLI solaire très bas (5,8) : les conclusions valent pour un DLI total de 12 environ obtenu par SL nocturne, pas pour un DLI proche de la cible via le soleil.
- Facteurs confondus : le SL ajoute lumière (DLI 5,8 → 12) et photopériode (10,5 → 24 h), donc les gains PSL/WSL contre NSL mélangent quantité de lumière et durée ; l'article ne sépare pas ces effets. PSL et WSL diffèrent aussi par la dose (6,04 contre 6,56) et le spectre.
- Le chauffage de la solution n'est pas comparé à un chauffage de l'air à coût énergétique égal ; l'énergie consommée n'est pas mesurée, alors que l'argument est économique.
- Pas de CO2, de densité, de VPD, de pH (non rapporté) : le titre « maximiser la productivité » porte sur 4 facteurs seulement.
- HR non contrôlée (31,7 %), peu représentative d'une serre fermée ; pas d'effet sur le risque maladie.
- SDW/SWC en valeur absolue visibles seulement dans les figures ; les 8 cultivars sont déjà présélectionnés, ce qui réduit les écarts.

## Pertinence pour SerreIA

Ce que SerreIA peut reprendre concrètement pour la laitue hydro :
- Ajouter une consigne de T° de solution (~18–20 °C, mesurée 18,8 °C) dans `laitue-hydro` et une sonde de T° de réservoir : le gain est avéré en hiver, surtout si les racines sont immergées (CFT/DWC, pas NFT) et seulement si l'éclairage est suffisant (2020-miller#009.0).
- Règle de couplage pour le contrôleur : ne chauffer la solution que si le DLI cumulé (soleil + SL) est > ~12 mol·m⁻²·j⁻¹ ; sans SL le chauffage racinaire est sans effet significatif (2020-miller#007.0).
- Cible DLI 14 de la recette cohérente avec 12–15 ; le SL peut combler un DLI solaire de 3–10 (2020-miller#006.0).
- Programme EC par âge (0,25 en pépinière ; 0,5–0,75 ; 0,75–1,0 ; 1,0–2,0) et alerte de dérive d'EC par évaporation (2020-miller#006.0), utile à l'agent LLM comme règle de vérification.
- Spectre du SL : privilégier rouge dominant (R90:B10) ; non applicable si SerreIA n'a qu'un éclairage blanc.
- Prudence : ne pas copier l'optimal d'air 20–24 °C ni 24 h de photopériode comme résultats de ce papier. Aucune règle HR, VPD, pH, maladie : pour le mildiou (HR > 90 % plus de 10 h à 10–25 °C) l'article n'apporte rien.

## Gaps identifiés

- Consigne de T° de solution absente de `recettes.yaml` (laitue-hydro) ; chercher des valeurs optimales de zone racinaire.
- Pas de comparaison chauffage racinaire contre chauffage de l'air en énergie et en rendement.
- Effet CO2 et densité sur la laitue d'hiver : non couvert (à chercher dans la base).
- Effet photopériode 16 h contre 24 h à DLI égal : non testé.

## Statut de lecture

Papier complet, lu par passages (`pdb show`, chunks 000 à 013), sans lecture intégrale de `fulltext.md`. Extraction GROBID correcte. Les valeurs de Fig. 1-5 et Tables 1-2 ne sont pas lisibles dans le texte : non relevées.
Déduit et non affirmé par les auteurs : l'interprétation de l'écart avec `recettes.yaml`, la règle de couplage chauffage/DLI (déduite de l'interaction lumière × température de solution), l'idée que le CFT correspond au DWC de SerreIA, et que la dose lumineuse et la photopériode sont confondues dans le SL.
