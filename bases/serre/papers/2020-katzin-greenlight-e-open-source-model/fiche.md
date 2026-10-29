---
id: 2020-katzin-greenlight-e-open-source-model
fiche: done
date: 2026-10-29
benchmarks: none
---

# GreenLight — An open source model for greenhouses with supplemental lighting: Evaluation of heat requirements under LED and HPS lamps

David Katzin, Simon Van Mourik, Frank Kempkes, Eldert J. Van Henten, 2020, Biosystems Engineering 194 (2020) 61-81 (venue lue dans les en-têtes de page du texte). https://doi.org/10.1016/j.biosystemseng.2020.03.010
Type : article de revue (relu par les pairs ; journal déduit du pied de page, `venue` absent de l'extraction GROBID).

## Problème

Peu de modèles de climat de serre décrivent l'effet de l'éclairage d'appoint, et aucun les LED : sur 30 modèles recensés, deux traitent les lampes HPS, aucun les LED (Introduction, #003). Les LED émettent peu de chaleur radiative, surtout convective, et fonctionnent à basse température, ce qui change la demande de chauffage. Les modèles usuels supposent qu'une fraction constante de l'électricité chauffe l'air (Introduction).

## Méthode

GreenLight étend le modèle de Vanthoor (2011) : bilans d'énergie, de carbone et de vapeur (§2.1, #005). Le modèle de Vanthoor a 13 états de température (couverture extérieure et intérieure, air du haut, écran thermique, air principal, couvert, tuyaux, sol, 5 couches de sol) ; GreenLight en ajoute 4 : lampes, inter-lampes, tuyaux de culture, écran d'occultation (§2.1.1, #006). Quatre commandes en 0..1 sont ajoutées (lampes, inter-lampes, vanne chaudière-tuyaux de culture, écran d'occultation).
Modèle de lampe : 15 paramètres pour les lampes de plafond (puissance électrique, surface, transmissivité et réflectivité PAR/NIR/FIR, rendements électrique vers PAR et NIR, photons par joule, émissivités, fraction de refroidissement actif, capacité thermique, coefficient d'échange convectif) ; la lampe a sa propre température (§2.1.2, #007). Flux : PAR et NIR vers couvert et sol, FIR vers cinq surfaces, convection vers l'air, refroidissement actif.
Calibration : paramètres de structure pris des plans ; les paramètres de ventilation (fuites, décharge, vent, flux d'écrans) sont calibrés pas à pas sur le CO₂ des périodes sombres, pour éviter injection et assimilation (§2.2.1, #009.3-009.4). Le reste est celui de la serre néerlandaise de Vanthoor. Lampes : HPS à environ 150 °C, LED à environ 55 °C sans refroidissement, temps de chauffe 1 h / 30 min (#012.0).

## Plateforme et implémentation

Pas de matériel embarqué : modèle de simulation en MATLAB R2019b, bâti sur le framework DyMoMa (open source), publié sur https://github.com/davkat1/GreenLight (§2.3, #016.0). Licence : n/r dans le texte. Données de l'essai : non publiées dans le papier.
Essai (§2.2, #008) : tomate (cv. Sunstream), Bleiswijk (Pays-Bas), 20 oct. 2009 - 9 fév. 2010 (112 jours, pas de 5 min) ; deux compartiments de 144 m² chacun, l'un avec HPS (110 W/m², 1,8 µmol/J), l'autre avec LED refroidies à l'eau (116 W/m², 1,6 µmol/J) ; PPFD 170 µmol m⁻² s⁻¹ ; CO₂ 1000 ppm. Entrées simulées : rayonnement global, T° extérieure, pression de vapeur, vent, températures des tuyaux, ouvertures de toit et d'écrans, état des lampes, injection de CO₂ (§2.2.3, #013).

## Résultats

- Erreur sur le chauffage : 7 à 50 MJ m⁻² sur la saison, contre 350 MJ m⁻² d'écart entre compartiments (§3, #017.0). L'abstract écrit « 8-51 W m⁻² », soit 1-12 % des valeurs mesurées ; unité incohérente avec le texte, à vérifier.
- RMSE de T° de l'air : 1,74 à 2,04 °C (abstract, 2020-katzin#000.0) ; RMSE d'HR : 5,52 à 8,5 % (pourcentage de saturation) ; RRMSE sous 10 %, sauf l'HR du compartiment HPS un peu au-dessus (Discussion, #018.0). Biais d'HR : +5,84 % (HPS) et +2,35 % (LED) (#018.2). CO₂ moins bien prédit en période éclairée (#017.1).
- Bilan énergie : HPS 1097 MJ/m² (435 chauffage, 662 lampes) ; LED 1461 MJ/m² (785 chauffage, 676 lampes, 426 extraits par refroidissement), net LED 1035 (§3, #017.2). Répartition de la sortie des lampes (Table 4) : HPS 36 % PAR, 22 % NIR, 32,5 % FIR, 9,5 % convectif ; LED 31 % PAR, 2 % NIR, 2,37 % FIR, 1,63 % convectif, 63 % refroidissement.
- Le corps de la Table 3 n'est pas extrait (légende seule) : les valeurs par compartiment ci-dessus viennent de l'abstract, du texte et de la Discussion.
→ reportés dans `benchmarks.csv` : aucune ligne (papier de modélisation, pas de benchmark de modèle ML/FPGA/edge ; erreurs reportées ci-dessus).

## Limites et critique

- Une seule expérience, une seule culture (tomate), paramètres en grande partie estimés et non mesurés ; pas d'analyse de sensibilité (Discussion, #018).
- Pas de validation séparée : calibration (ventilation) et évaluation portent sur les mêmes 112 jours.
- HR surestimée : transpiration mal modélisée (spectre ignoré, couvert en une seule couche) (#018.2-018.3). CO₂ moins fiable.
- Compartiments de 144 m² sous verre néerlandais, ventilation par ouvrant de toit : transposition à une mini-serre de quelques m² non testée (déduit).
- Modèle complexe : 17 températures, centaines de paramètres. Sans les données, la reproduction exige l'appendice et le code.
- Les LED refroidies à l'eau de l'essai ne représentent pas les LED passives d'une serre amateur (déduit).

## Pertinence pour la thèse

Axe `climate-control` de la base serre : référence de modèle physique de serre éclairée, avec erreurs de T° et d'HR de référence (RMSE environ 2 °C et 5,5 à 8,5 % d'HR) à ne pas chercher à battre sans calibration sur site. Utile comme source du simulateur et comme environnement de MPC/RL (niveau 3 de SerreIA).

## Pour SerreIA

État actuel (`sim/model.py`) : T° du premier ordre (constante de temps, hausse solaire, chauffage, ventilation), HR/pH/EC simplifiés. Ce que GreenLight/Vanthoor suggèrent, par priorité pour une petite serre amateur (LED, pas de gaz). Les points ci-dessous sont des recommandations déduites du modèle ; le papier ne traite pas une mini-serre.

1. **LED : séparer la puissance électrique en PAR, NIR, FIR et convectif, avec une température de lampe.** Un seul état T_lamp avec capacité thermique et coefficient d'échange convectif (#007.3, #012.0). Pour des LED passives (non refroidies), la chaleur est essentiellement convective et la lampe monte vers 55 °C en environ 30 min (#012.0) : cela remplace le « 100 % LED chauffe l'air » implicite. Table 4 : LED à 31 % PAR, 2 % NIR, 2,4 % FIR, 1,6 % convectif, 63 % refroidissement ; sans refroidissement, la fraction restante part en chaleur dans la serre (déduit).
2. **Bilan d'énergie multi-nœuds réduit : air, couvert végétal, couverture (intérieur/extérieur), sol** (#006.0, #020.0), plutôt que le seul premier ordre. Sans écrans ni tuyaux ni 5 couches de sol : garder T_air, T_can, T_cov, T_floor (1 à 2 couches). Les échanges FIR avec le ciel et la couverture comptent la nuit.
3. **Ventilation : débit de fuite plus débit par ouvrant** (coefficients de fuite et de décharge, effet du vent), à calibrer sur des nuits fermées (#009.3-009.4). Calibrer sur le CO₂ des périodes sombres est un protocole réutilisable ; avec un capteur CO₂, la méthode s'applique telle quelle.
4. **Humidité : bilan de vapeur avec transpiration du couvert, condensation sur la couverture et échange par ventilation** (modèle Vanthoor, appendices de Vanthoor et al. 2011, non dans la base). C'est le point faible de GreenLight (HR surestimée, #018.2) : prévoir un facteur de calibration de la transpiration, éventuellement fonction du PPFD et du LAI. Cohérent avec S3 (humidité absolue conservée, VPD exposé).
5. **Paramètres à ajouter** : surface de couverture, hauteur et volume d'air, coefficient d'échange couverture-air (3,5 W m⁻² K⁻¹ dans l'essai, #009), transmission PAR/NIR de la couverture, rendement électrique-PAR des LED (efficacité en µmol/J de la fiche constructeur), capacité thermique de l'air, du couvert et du sol.
6. **Code ouvert** : MATLAB (R2019b), DyMoMa, https://github.com/davkat1/GreenLight (#016.0) ; licence n/r (à vérifier sur GitHub). Pas de portage Python indiqué dans le papier. Le lien est réutilisable pour les équations et valeurs par défaut ; une réécriture Python (SciPy `solve_ivp` ou Euler) est nécessaire pour `sim/model.py` (déduit). Les appendices de Vanthoor et al. 2011 manquent à la base : candidat pour `/paper-discover`.
7. **Validation proposée** : reprendre les métriques du papier (§2.2.3, #013.2) : ME, RMSE, RRMSE sur T_air et HR, au pas de 5 min, en entrant les mesures extérieures et les états d'actionneurs réels. Cibles de comparaison : RMSE T° d'environ 2 °C, HR d'environ 5,5 à 8,5 % d'HR, RRMSE sous 10 % (#018.0). Calibrer sur des nuits (ventilation fermée), évaluer sur des jours non utilisés pour la calibration, ce que le papier ne fait pas (déduit). Garder `--modele simple` en base de comparaison (docs/18 S3).

## Gaps identifiés

- Aucun modèle de serre de petite taille (quelques m², LED seules, sans chauffage) validé dans la base ; GreenLight cible de grandes serres néerlandaises.
- Transpiration sous LED : surestimation d'HR non résolue (#018.2).
- Manque dans la base : Vanthoor et al. 2011 (modèle de base, appendices).

## Statut de lecture

Sections lues : Abstract, Introduction, §2 (méthode, évaluation), §3, Discussion, début de l'Appendice A, via lecture par plages de `fulltext.md` et `pdb search` ; les tableaux 1, 2, 3 et A2 n'ont pas de corps extrait (« légende seule »), seule la Table 4 est lisible. Extraction GROBID (`extraction.ok` vrai).
Ce qui suit est déduit et non affirmé par les auteurs : l'applicabilité à une mini-serre, les recommandations « Pour SerreIA », la séparation calibration/validation, l'absence de portage Python, la licence non lue.
