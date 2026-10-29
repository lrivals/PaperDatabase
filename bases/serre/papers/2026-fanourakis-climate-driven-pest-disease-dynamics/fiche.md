---
id: 2026-fanourakis-climate-driven-pest-disease-dynamics
fiche: done
date: 2026-10-29
benchmarks: none
---

# Climate-Driven Pest and Disease Dynamics in Greenhouse Vegetables: A Review

Dimitrios Fanourakis, Theodora Makraki, Theodora Ntanasi, Evangelos Giannothanasis, Georgios Tsaniklidis, Dimitrios I Tsitsigiannis, Georgia Ntatsi, 2026, Horticulturae 12(4):415 (revue ; venue déduite du préfixe DOI 10.3390/horticulturae12040415, non confirmée dans `metadata.json`). https://doi.org/10.3390/horticulturae12040415
Type : revue de littérature (article de journal ; relecture par les pairs non vérifiée dans le texte)

## Problème

Comment les variables du microclimat de serre (T°, HR, VPD, lumière, CO₂) gouvernent l'épidémiologie des maladies et ravageurs de la tomate, du concombre et du poivron, et comment les utiliser en lutte intégrée « climat-adaptative » (#001, #013). Seules des études en serre sont incluses (Abstract, #000).

## Méthode

Revue narrative : sections par groupe (champignons/oomycètes §3, bactéries §4, virus §5, insectes/acariens/nématodes §6), interactions (§7, Table 6), synthèse microclimat (§8, Tables 7-8), saisons (§9, Table 9), systèmes d'aide à la décision (§10), gaps (§12). Pas de méta-analyse ni de protocole de recherche chiffré rapporté dans les passages lus. Les seuils sont des « plages indicatives » de tableaux (Tables 2-5) ; la source de chaque ligne est un renvoi bibliographique, pas une mesure propre.

## Plateforme et implémentation

Sans objet (revue, pas de matériel). Pas de code ni de données publiés ; matériel supplémentaire (Tables S1-S6) non fourni dans le corpus.

## Résultats

Tout est qualitatif ou en plages de tableaux. Constats principaux :
- Chaud et humide favorise champignons et bactéries ; air sec à VPD élevé favorise acariens, thrips et la transmission virale (Abstract, #000). Plage de gestion proposée : HR 60-75 % et VPD ≈ 0,6-1,0 kPa (§8, #013.2 ; Table 7, #035.0).
- Seuils par agent : voir « Consignes chiffrées ». Tables 1 et 5 : corps de Table 1 non extrait ; Table 5 lue via les chunks #031-#032 (extraction par morceaux, colonnes à vérifier).
- Table 7 : flux d'air modéré continu 0,2-0,5 m/s ; T° 22-28 °C ; CO₂ 700-900 µmol/mol comme plage « pression parasitaire minimale » (#035.0, #035.2).
- Table 8 : compromis rendement/phytosanitaire, p. ex. HR 70-85 % pour le rendement contre < 80 % pour la lutte contre Botrytis (#036.0).
- DSS : détection des périodes à risque fongique via T°, HR nocturne, déficit de point de rosée, chutes de VPD ; insectes via degrés-jours (§10, #016.0-#016.1).
→ reportés dans `benchmarks.csv` : aucune ligne (revue ; voir `benchmarks: none`).

## Consignes chiffrées

Cultures de l'article : tomate, concombre, poivron. Laitue, basilic et fraise (cultures SerreIA) : **absents** de l'article (aucune occurrence). Les plages sont celles des tableaux de l'article (indicatives, issues de la littérature citée), non mesurées par les auteurs. Durée d'humectation : `n/r` sauf mention. VPD en kPa ; « > » comme écrit dans le tableau.

| pathogène ou ravageur | culture | conditions favorables (T°, HR, VPD, humectation, durée) | seuil ou plage | levier climatique recommandé | chunk_id |
|---|---|---|---|---|---|
| Botrytis cinerea (pourriture grise) | tomate, concombre, poivron | 15-22 °C ; HR > 90 % ; VPD < 0,5 ; condensation / tissus sénescents ; durée n/r | HR < 85 % ; VPD 0,6-0,8 ; HR < 80 % cible Botrytis (Table 8) | ventilation nocturne (cycles chauffage-ventilation), éviter la condensation | #027.0, #036.0, #003.1 |
| Oïdium (Leveillula taurica, Podosphaera xanthii) | tomate, concombre, poivron | 20-28 °C ; HR 60-80 % ; VPD 0,6-1,0 ; pas d'eau libre requise, forte variation d'HR, faible UV, canopée dense ; durée n/r | éviter les variations brusques d'HR | HR stable, lumière/UV-B suffisants (> 500 µmol/m²/s via UV, Table 8), éviter l'ombrage excessif | #027.0, #003.1, #037.0 |
| Mildiou du concombre (Pseudoperonospora cubensis) | concombre | 15-20 °C ; HR > 95 % ; VPD < 0,4 ; humectation prolongée ; durée n/r | T > 22 °C ; HR < 90 % | irriguer tôt, séchage rapide des feuilles, nuits un peu plus chaudes, ventiler avant le lever du soleil | #027.0, #003.2 |
| Mildiou / Phytophthora infestans | tomate | 18-24 °C ; HR > 90 % ; VPD < 0,4 ; eau libre nécessaire ; durée n/r | T > 25 °C ; HR < 90 % | irriguer tôt, séchage rapide, baisse d'HR, brassage d'air, chauffage | #027.1, #003.3 |
| Cladosporium fulvum (cladosporiose) | tomate | 25-30 °C ; HR > 90 % ; VPD < 0,5 ; durée n/r | HR < 85 % (canopée) | renforcer la ventilation, réduire la densité | #027.1 |
| Fusarium oxysporum (fusariose) | tomate, poivron | 24-28 °C (zone racinaire) ; HR 70-80 % ; substrat trop humide, EC élevée | racines < 25 °C ; EC modérée | drainage, irrigation modérée | #027.1, #003.3 |
| Pythium, Phytophthora (pourritures racines/tige) | concombre, tomate, poivron (plantules) | 15-20 °C (zone racinaire) ; HR > 90 % ; substrat saturé | 20-24 °C racines ; éviter la sur-irrigation | drainage, limiter volume de fertigation | #027.2 |
| Sclerotinia sclerotiorum (moisissure blanche) | tomate, concombre, poivron | 18-22 °C ; HR > 90 % ; VPD < 0,5 | HR < 85 % | ventilation de la canopée basse, cycles chauffage-ventilation | #027.2 |
| Alternaria alternata, A. solani | tomate, poivron | 24-28 °C ; HR > 85 % ; VPD < 0,6 ; humectation | n/r (« éviter l'humectation ») | circulation d'air, éviter l'humectation | #027.2 |
| Pseudomonas syringae pv. tomato (tavelure bactérienne) | tomate | 18-24 °C ; HR > 85 % ; VPD < 0,6 | HR < 85 % | brassage d'air, éviter l'humectation, ventiler au crépuscule | #028.0 |
| Xanthomonas spp. (tache bactérienne) | tomate, poivron | 25-30 °C ; HR > 85 % ; VPD < 0,6 | HR < 85 % ; T < 26 °C | brassage d'air, éviter l'irrigation par aspersion | #028.0 |
| Clavibacter michiganensis (chancre bactérien) | tomate, poivron | 24-28 °C ; HR > 80 % ; VPD < 0,7 ; feuillage humide | HR < 80 % | éviter la manipulation de plantes humides (hygiène surtout) | #028.0 |
| Bemisia tabaci, Trialeurodes vaporariorum (aleurodes) | tomate, concombre, poivron | 25-32 °C ; HR 50-70 % ; VPD 0,8-1,2 | T < 28 °C | flux d'air continu, films transmettant l'UV, filets, lutte biologique | #031.0 |
| TYLCV (vecteur aleurode) | tomate, poivron | 25-30 °C ; HR 50-70 % ; VPD 0,8-1,2 | T < 28 °C | brassage d'air, filets anti-insectes | #029.0 |
| Tuta absoluta | tomate | 24-30 °C ; HR < 60 % ; VPD > 1,0 | HR 60-70 % | HR modérée, ventiler les pics de chaleur | #031.0 |
| Frankliniella occidentalis (thrips) | tomate, poivron | 22-30 °C ; HR < 60 % ; VPD > 1,0 | HR > 60 % ; VPD 0,6-1,0 | éviter la sécheresse excessive, réguler le VPD, filets | #031.1 |
| TSWV (vecteur thrips) | tomate, poivron | 20-26 °C ; HR < 60 % (vol du vecteur) ; VPD > 1,0 | HR 60-75 % | réduire le VPD | #029.0 |
| Tetranychus urticae (acarien tétranyque) | tomate, concombre | 28-35 °C ; HR < 50 % ; VPD > 1,2 ; une génération en 1-2 semaines | HR 60-70 % | HR modérée, réduire la T° foliaire, acariens prédateurs ; une déshumidification excessive peut favoriser les acariens | #032.0, #011.0 |
| Pucerons (Myzus persicae, Aphis gossypii) | tomate, concombre, poivron | 18-24 °C ; HR 60-80 % ; VPD 0,6-0,9 | n/r | ventilation, filets sur les ouvrants | #031.0 |
| Mineuses (Liriomyza spp.) | tomate, concombre, poivron | 22-28 °C ; HR 65-80 % ; VPD 0,6-1,0 | n/r | HR équilibrée, éviter l'engorgement | #032.0 |
| Nématodes à galles (Meloidogyne) | tomate, concombre, poivron | 25-30 °C (racines) ; humidité du sol proche de la capacité au champ | racines < 25 °C | drainage, solarisation, porte-greffes | #032.0 |

Règles transversales (toutes cultures de l'article) : HR > 85 % favorise champignons, oomycètes et bactéries ; HR < 55 % favorise acariens et thrips ; VPD < 0,4 favorise Botrytis, Phytophthora, Cladosporium ; VPD > 1,2 favorise acariens et thrips (Table 7, #035.0). Irrigation de nuit : augmente l'humectation et le risque (#035.2). Fenêtre critique d'infection = durée de la condensation après refroidissement nocturne (§8, #013.2). Durée de seuil explicite : humectation < 8 h pour la tache angulaire du concombre, rare si l'air circule (#005.2), seul chiffre de durée trouvé ; aucune durée d'humectation n'est donnée pour Botrytis ni le mildiou.

## Écart avec SerreIA

Règles lues (lecture seule) : `edge/controller/risk.py` (mildiou : humectation = durée au-dessus de `hr_humectation` ≥ `humectation_h` ; T° moyenne 12 h entre `t_min` et `t_max`, soit 10-25 °C d'après la consigne donnée ; ou vision confirmée 3 fois avec HR > 85 % ; réponse : ventilation préventive + alerte) et `edge/controller/regles.yaml` (mildiou : HR max abaissée de 10 points pendant 72 h ; oïdium : surveillance + recapture ; nuisible : brumisation 30 s ; virus et taches : isolement ou arrosage sur validation). Constat par comparaison avec les chiffres ci-dessus (déduction de ma part, pas affirmation des auteurs).

**Pathogènes ou ravageurs sans règle climatique dans SerreIA** (une seule règle climatique, mildiou) : Botrytis (cultures denses, 15-22 °C, HR > 90 %, VPD < 0,5), Cladosporium, Sclerotinia, Alternaria, bactéries (Pseudomonas, Xanthomonas), aleurodes, thrips, Tuta absoluta, TYLCV et TSWV, pucerons, Pythium/Fusarium (solution nutritive, température racinaire, saturation du substrat). Seul le mildiou est déclenché par le climat ; l'oïdium n'est qu'en surveillance vision.

**Conditions fausses ou incomplètes**
- Le seuil « HR > 90 % pendant > 10 h entre 10 et 25 °C » est compatible avec Phytophthora (18-24 °C, HR > 90 %) et Botrytis (15-22 °C, HR > 90 %) mais : la fourchette 10-25 °C est plus large que celle de l'article ; il ignore les mildious/pathogènes à T° plus chaude (Cladosporium 25-30 °C, Alternaria 24-28 °C, Xanthomonas 25-30 °C, qui exigent HR > 85-90 % ; le test sur T° moyenne 12 h les écarte) ; et il n'utilise ni VPD ni condensation (l'article met VPD < 0,4-0,6 et condensation nocturne au centre du risque, mais ne donne pas de durée). Le chiffre « 10 h » n'est pas retrouvé dans l'article (n/r).
- L'oïdium n'est pas favorisé par une HR basse au sens strict ni par une HR élevée prolongée : l'article donne 20-28 °C, HR 60-80 %, VPD 0,6-1,0, sans eau libre, avec fortes variations d'HR et peu d'UV (#027.0, #003.1). Une règle « HR > 90 % » ne le détecterait donc pas ; l'hypothèse « HR basse » n'est pas établie non plus par l'article. Un indicateur d'oïdium devrait utiliser la plage 60-80 %, la variabilité d'HR et la dose d'UV (n/r en seuil chiffré).
- Mildiou : HR max abaissée de 10 points est une manœuvre cohérente (cible Botrytis HR < 80-85 %, mildiou < 90 %) ; mais la durée de 72 h n'a pas de source dans l'article, et l'abaissement doit rester au-dessus de ≈ 60 % : sous HR < 55-60 % l'article place thrips, acariens et Tuta (#035.0, #031.0).
- Nuisible → brumisation 30 s : cohérent avec « HR 60-70 % » pour acariens (#032.0), mais l'article déconseille d'ignorer le couplage : la brumisation monte l'HR, donc le risque fongique la nuit ; à restreindre au jour, avec VPD > 1,2 et HR < 50 % comme déclencheur climatique (acarien). Elle ne vise pas aleurodes/thrips/Tuta, dont les conditions sont HR 50-60 %, VPD > 1,0.
- Aucune règle d'irrigation de nuit (l'article la désigne comme facteur de risque, #035.2) ni de pilotage du VPD, du brassage d'air (0,2-0,5 m/s, #035.0) ou de la température racinaire.
- Cultures : tomate seule couverte par l'article parmi celles de SerreIA ; **laitue hydroponique, basilic, fraise : aucune donnée**. Le risque oïdium/mildiou du basilic (Peronospora) ou de la fraise (Botrytis, oïdium) ne peut pas être calibré avec cet article.

## Limites et critique

- Plages indicatives issues de revues et d'études citées, d'origine variée (la section DSS note une calibration surtout nord-européenne, §10 #016.0) ; pas de cadre quantitatif, les auteurs reconnaissent « peu d'études donnent des fonctions continues » (§12). Aucune durée d'humectation ni de seuil dose-réponse pour les champignons.
- Incohérences internes possibles : Table 7 « RH > 85 % favorise les maladies » vs oïdium à HR 60-80 % ; Table 8 donne 0,8-1,2 kPa comme VPD de suppression (Cladosporium) alors que Table 7 donne 0,6-1,0 kPa ; à citer avec la table d'origine.
- Corps de Table 1 et de Table 5 signalés « sans corps extrait » (`extraction.warnings`) ; Table 5 retrouvée dans #031-#032 mais colonnes à revalider ; le texte « Table 5 » des légendes et les suppléments S1-S6 (seuils de degrés-jours) sont absents.
- Revue sans protocole PRISMA visible dans les passages lus ; tomate, concombre, poivron seulement.

## Pertinence pour la thèse

Pertinence pour SerreIA (profil : plages de consignes par espèce, contrôleur de règles) : source de seuils climatiques par agent pathogène pour la tomate, base d'une grille de risque (HR/VPD/T° par pathogène) et d'un compromis rendement/phytosanitaire (Table 8). Ne couvre pas laitue, basilic, fraise ; ne fournit pas de durée d'humectation ; ne remplace pas une source par espèce hydroponique.

## Gaps identifiés

- Seuils d'humectation (heures) par pathogène en serre : absents ici.
- Plages de risque pour laitue hydroponique, basilic, fraise (aucune dans l'article).
- Interaction brumisation/ventilation vs risque fongique nocturne (compromis non chiffré, Table 8 seulement).
- Règles climatiques pour thrips, aleurodes, Tuta absoluta non présentes dans SerreIA.

## Statut de lecture

Sections lues : Abstract, §2-§3 (via `fulltext.md`), tableaux 2 à 9, §8, §9, §10, §12 (lus par segments), §6 (acariens). Non lus en entier : §1, §4 à §7 hors tableaux, §11 ; Tables S1-S6 absentes. `extraction.backend` : grobid ; Tables 1 et 5 : corps non extrait ou partiel. Chaque valeur du tableau « Consignes chiffrées » est vérifiée avec `bin/pdb verify` sur le chunk indiqué (sous-chunk où la chaîne est retrouvée).
Déduit et non affirmé par les auteurs : la section « Écart avec SerreIA » (comparaison avec `risk.py` / `regles.yaml`), l'effet de la brumisation sur le risque fongique nocturne, la remarque sur le seuil de 10 h et les limites de la plage 10-25 °C.
