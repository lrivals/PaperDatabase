---
id: 2019-santiago-integrated-pest-management-manual-greenhouses
fiche: done
date: 2026-10-29
benchmarks: none
---

# Santiago E.Z., Whitworth J., Holly S.-K. — Integrated Pest Management Manual for Greenhouses (2019)

Evy Z. Santiago (dir. Jeff Whitworth, Holly Schwarting-Kansas), University of Nebraska-Lincoln, Master's report (programme Entomology à distance), printemps 2019. DOI / URL : n/r.
Type : rapport de master, littérature grise, non relu par les pairs.

## Problème

Manuel de protection intégrée (IPM) pour serre de R&D : les ravageurs piqueurs-suceurs (aleurodes, pucerons, thrips, acariens) y sont plus problématiques qu'au champ (milieu chaud et humide, isolement des ennemis naturels, génération continue ; §Introduction, 001.0). Le seuil d'acceptation est très bas en serre de R&D.

## Méthode

Compilation bibliographique (pas d'expérience propre) : biologie de 5 espèces (thrips Frankliniella occidentalis, acarien Tetranychus urticae, pucerons Schizaphis graminum et Rhopalosiphum padi, aleurode Bemisia tabaci), dépistage, lutte biologique, lutte chimique, pratiques culturales. Les pucerons sont des espèces de céréales (blé, sorgho), pas de tomate/laitue.

## Plateforme et implémentation

Sans objet (pas de matériel ni de code ; n/r).

## Résultats

Pas de mesure propre. Les valeurs numériques sont reprises de la littérature citée (voir tableau). Hors tableau : un adulte de Delphastus catalinae mange jusqu'à 160 œufs ou 12 larves d'aleurode par jour (017.0) ; Orius insidiosus plus de 20 thrips par jour (013.0). Cycle thrips 7 à 13 jours à 26-29 °C (001.2), puceron greenbug adulte en 5 j à 24-30 °C (003.1), génération d'acarien 15 à 28 j (002.2).
→ reportés dans `benchmarks.csv` : aucune ligne (manuel, aucune configuration rapportée par les auteurs).

## Consignes chiffrées

Adaptées à la protection intégrée : une ligne par ravageur ou procédé.

| ravageur | méthode de dépistage (pièges, fréquence) | seuil d'intervention | auxiliaire de lutte biologique | conditions favorables (T°, HR) | chunk_id |
|---|---|---|---|---|---|
| tous (général) | passage 1 fois par semaine, plus souvent si foyer ; inspection visuelle + cartes collantes ; marquer les lieux infestés | « seuil accepté » non chiffré ; traitement chimique juste après l'avoir atteint | lâchers planifiés, avant détection ou dès les premiers thrips | serre chaude et humide, génération continue toute l'année | 007.0, 018.0, 013.0 |
| aleurode (B. tabaci) | carte jaune 24 × 20 cm, verticale, bord haut au niveau de la canopée ou un peu au-dessus ; 1 carte par 3-5 m ; variante : 5 cartes par 667 m² (5 points ou « Z »), renouvelées tous les 10 j | 0,25-0,5 adulte/cm² sur carte : lutte biologique ; 3-4 adultes/cm² : lutte chimique | Encarsia formosa (parasitoïde, le plus utilisé) ; Delphastus catalinae (160 œufs ou 12 larves/j) ; Amblydromalus limonicus ; Amblyseius swirskii (aleurode et thrips) | n/r pour l'aleurode ; stress hydrique et excès d'azote l'avantagent (019.1) | 008.0, 017.0, 019.1 |
| thrips (F. occidentalis) | loupe ; souffler sur fleurs et points de croissance pour les faire bouger ; cartes bleues (+ kairomone verbenone : captures accrues ; LED bleue 445 nm : ×2) ; traces : fèces noires, zones argentées | n/r (aucun seuil chiffré) | Orius insidiosus (> 20 thrips/j) ; Neoseiulus (1-10 jeunes thrips/j, ratio proie:prédateur 1:2, larves L1 seulement) ; Hypoaspis (sol, nymphes/pupes, 1 lâcher par culture) ; Thripobius semiluteus (parasitoïde de thrips de serre, nymphes) ; A. swirskii | cycle en 7-13 j à 26-29 °C ; adulte jusqu'à 45 j ; létal à 104 °F (40 °C) avec HR 10 % (vide sanitaire) | 009.0, 008.1, 013.0, 013.1, 001.2, 019.0 |
| acarien (T. urticae) | loupe, secouer le feuillage sur papier blanc ; dessous des feuilles, feuilles basses puis hautes ; indice GNDVI multispectral (Hermann 2011) ; pas de carte collante | pas de seuil serre ; pour le sorgho (champ) : insecticide à 30 % de feuilles à symptômes | Phytoseiulus persimilis (flambée ; exige T < 80 °F ≈ 27 °C et HR 60-80 %) ; Mesoseiulus longipes (plus chaud, HR plus basse) ; Neoseiulus californicus (survit sans proie) ; Feltiella acarisuga | cycle 1-3 sem selon T° ; « temps sec et chaud » + stress hydrique favorisent l'acarien | 010.0, 010.2, 014.0, 019.1 |
| pucerons | inspection visuelle d'abord (dessous, tiges, jeunes pousses : miellat, exuvies, enroulement) ; cartes jaunes horizontales au sommet du pot, secours seulement (fiables surtout en hiver) | n/r | coccinelles, chrysopes, syrphes, nabidés, parasitoïdes (Aphelinidae, Aphidiidae, Braconidae), champignons entomopathogènes | greenbug : seuil de développement 3,5-6 °C, max 37 °C, optimum 24-30 °C | 009.2, 012.0, 003.1 |

Valeurs hors ravageurs : excès d'azote augmente aleurodes et pucerons et le miellat ; irrigations à caler pour éviter le stress hydrique (019.1) ; vide sanitaire d'une semaine avant culture (019.0).
Les valeurs ci-dessus sont vérifiées par `bin/pdb verify` ; les seuils pour tomate, laitue, basilic ou fraise : n/r.

**Écart avec SerreIA** (lecture seule de `recettes.yaml` et `regles.yaml`) : le manuel ne chiffre aucune consigne climatique de culture (T° jour/nuit, VPD, DLI, pH, EC : n/r), donc rien à comparer aux plages des recettes. Seul recoupement de climat : P. persimilis veut HR 60-80 % et T < 27 °C (014.0), compatible avec les HR de la tomate en croissance (60-75 %), pas avec la laitue (50-70 %, bas de plage). Règle « nuisible → brumisation 30 s » (`regles.yaml`) : défendable seulement pour l'acarien (le papier lie sécheresse et chaleur à sa reproduction, 019.1, et ses auxiliaires demandent HR 60-80 %), mais le manuel ne propose jamais la brumisation comme moyen de lutte ; elle est inutile contre thrips, aleurodes et pucerons. Déduit : elle élève l'HR, donc le risque de mildiou et de botrytis (règle HR > 90 % sur plus de 10 h), à plafonner.

## Limites et critique

- Compilation sans méthode ni mesure ; seuils d'origine disparate (Chine pour les cartes aleurodes, champ de sorgho pour 30 %).
- Pucerons et acarien décrits surtout sur céréales (blé, sorgho, maïs, soja), peu transposables à la tomate, la laitue, le basilic ou la fraise.
- Aucun seuil chiffré pour thrips, pucerons, acarien en serre ; aucune consigne de climat.
- Extraction : texte avec bruit (en-têtes répétés au milieu des phrases), tableau et figure sans légende exploitable.
- Pas de code, pas de reproductibilité (sans objet).

## Pertinence pour SerreIA

Reprise concrète : (1) un calendrier de dépistage hebdomadaire et un compte de cartes collantes par m² ; (2) seuils aleurodes 0,25-0,5 adulte/cm² (biologique) et 3-4 (chimique), applicables si une caméra compte les insectes sur cartes jaunes ; (3) cartes bleues pour thrips ; (4) fenêtre climatique des auxiliaires (P. persimilis HR 60-80 %, < 27 °C) à ne pas casser par le contrôleur ; (5) vide sanitaire de 7 jours et chauffage à 40 °C, HR 10 % en fin de culture ; (6) alerte « stress hydrique » à lier à la règle nuisible. Pour l'agent LLM : liste de ravageurs et symptômes (miellat, stippling, toiles, zones argentées) comme garde-fou de diagnostic, avec validation humaine. La règle brumisation reste limitée à l'acarien (voir l'écart ci-dessus).

## Gaps identifiés

- Seuils d'intervention chiffrés en serre pour thrips, acariens, pucerons sur tomate, laitue, basilic, fraise.
- Lien quantitatif entre HR/VPD et pression ravageur, pour justifier ou non la brumisation.
- Détection automatique de ravageurs (caméra sur cartes collantes) : non couvert.

## Statut de lecture

Papier complet, lu par sections avec offset (extraction grobid, ok). Consignes vérifiées par `bin/pdb verify` : le vérificateur retrouve aussi la citation dans les passages voisins, les chunk_id cités sont ceux du passage principal. Déduits et non affirmés par les auteurs : pertinence pour SerreIA, risque fongique lié à la brumisation, équivalence 80 °F ≈ 27 °C et 104 °F ≈ 40 °C.
