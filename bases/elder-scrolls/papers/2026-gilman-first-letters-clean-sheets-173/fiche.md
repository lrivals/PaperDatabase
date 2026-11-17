---
id: 2026-gilman-first-letters-clean-sheets-173
fiche: done
date: 2026-11-17
---

# first-letters-clean-sheets: 173 self-traced clean single-sheet surface patches on 13 First Letters-eligible Herculaneum scrolls

Jack Gilman, Andrew Gilman, 2026, GitHub. https://github.com/Ahggggg/first-letters-clean-sheets/tree/978e8d5e2e26eb195dd848c57a32830e875435a3
Type : dépôt GitHub communautaire (Vesuvius Challenge), commit 978e8d5e2e du 2026-11-01 ; **non relu par les pairs, tous les chiffres sont auto-déclarés** (README.md, recipe/README.md, onsheet/README.md convertis en PDF).

## Problème

Contribution au Progress Prize d'octobre 2026 (README §Status) : fournir des morceaux de surface de rouleau « propres » (une seule feuille de papyrus, sans pli ni arête étirée) sur les rouleaux éligibles First Letters, pour y chercher des lettres. Verrou : les maillages publics ou auto-générés traversent souvent plusieurs couches (surfaces « tourbillonnantes »), ce qui rend toute lecture d'encre inutile (README §Where tracing worked, §The on-sheet score).

## Méthode

- Seeds posées par règle fixe sur la prédiction de surface publique m7 (une graine « bande plane » par cellule de 384 voxels, la plus plate d'abord), croissance de 75 générations avec `vc_grow_seg_from_seed` (villa, image Docker volume-cartographer) ; ~400 traces, 173 patchs gardés (README §How a patch was made, 000-001).
- Audit de maillage : nœud propre si fini, normale à ≤ 30° de ses voisines, arête ≤ 1,5 × médiane, un seul côté de « frame » (normale vers/loin de l'axe supposé au centre XY du volume : règle grossière). Patch = plus grand rectangle propre ≥ 1,0 cm2 (001.0).
- Lecture : rendu de 28 plans le long de la normale (9,4 µm/pixel), Reader v2 et d9v4C dans les deux ordres de couches ; ordre « frame-correct » choisi par la règle du projet. Reader V3 (Russo) ajouté pour les 79 patchs passant le contrôle de contraste de LynnHenry (002.3-002.5). Convention F/R inversée pour `vc_render_tifxyz` par défaut (001.1-001.2).
- Contrôle CT : 10 coupes par patch, inclinaison des couches par tenseur de structure, avec contrôles plats et tourbillonnants (001.3-001.4).
- Score « on-sheet » par tuile de 256 px (cohérence d'orientation d'harmonique 4, contraste en profondeur, texture), classement de 120 surfaces publiques tierces (003.2, onsheet/README).

## Plateforme et implémentation

- Calcul : portable 4 coeurs CPU (5 CPU et 14 Go donnés à Docker Desktop), Windows, aucun GPU pour le tracé ; ~15-20 min par traceur, quatre en parallèle, ~1,5 h pour un bloc de 16 traces, ~6 Go de téléchargement par bloc (recipe §What we did, 004.2). Lecture Reader V3 : GPU Intel Arc, FP32, batch 4 (002.4). Logiciels : villa (`vc_grow_seg_from_seed`, `vc_render_tifxyz`), Reader v2 (DomRusso2/reader-v2), Reader V3 (domenicor046/reader-v3 @aee1d64), d9v4C (TAUIL).
- Code publié (MIT : code/, recipe/, checks/) et données dérivées (CC BY-NC 4.0 : patchs tifxyz, images, tables) sur https://github.com/Ahggggg/first-letters-clean-sheets. Non publiés : piles de 28 plans et cartes pleine résolution (~6 Go), cartes V3 float16 (~0,9 Go). Le renderer 28 plans et les lecteurs sont du code projet / poids publics tiers. `fetch_mirror.py` et `trace_round.py` sont des copies nettoyées non relancées sous cette forme (§How to reproduce).

## Résultats

- 173 patchs, 355,0 cm2 au total (1,0-8,4 cm2 chacun, médiane 1,7), sur 13 rouleaux, scans à 9,362 ou 8,64 µm (README §en-tête, §Honest limits ; 000.0).
- Rendement très variable selon l'ancrage du bloc : blocs ancrés sur la plus forte densité de prédiction publique, 2,9 cm2 pour 32 traces (PHerc0125, 0257) et 0 cm2 pour 16 traces (contrôle PHerc0813) ; blocs ancrés sur le meilleur maillage du score on-sheet, 24,6 cm2 pour 24 traces (PHerc0813) ; PHerc0826 : 75,8 / 40,7 / 27,1 cm2 pour trois runs de 32 traces. Expériences uniques ; Spearman 0,30 entre score de l'ancre et rendement (003.0). Nouveaux blocs du 2e run : PHerc0175A 32,7 ; 0211 23,6 ; 1203 14,3 ; 0306B 11,6 ; 0191 7,5 ; 0483B 6,6 ; 0846B 2,3 ; 0490B 0 (003.1).
- Coupes CT : inclinaison médiane |tilt| 0,97° sur 1 730 coupes, contre 1,01° pour 3 surfaces plates et 4,70° pour 3 tourbillonnantes (rapport 4,6) ; 131 patchs sur 173 sous 1,3° ; 13 patchs à ≥ 2° (flag post hoc) (001.4, 002.0). Mais 58 % des coupes de patchs dépassent le seuil de 20 voxels fixé à l'avance (77 % des contrôles plats, 90 % des tourbillonnants) : l'attente « 80 % sous 20 voxels » n'est pas tenue ; la mesure écarte un tourbillon grossier, elle ne prouve pas la monocouche (001.5).
- Part des nœuds sur la prédiction m7 : médiane 0,67 (minimum 0,15) ; 5 patchs < 0,30 (002.0-002.1).
- Cartes d'encre Reader v2 / d9v4C : part de pixels > 0,5 de médiane 0,051 (max 0,49), part > 0,8 nulle partout ; blobs et speckle, **aucune lettre** (002.1). Reader V3 sur 79 patchs (162,33 cm2) : 0,095 (pondéré pixel) en ordre frame-correct contre 0,104 dans l'autre ; ordre correct plus lumineux sur 42 patchs sur 79 seulement (002.4-002.5). Pas de témoin d'encre connue sur ces rouleaux.
- Score on-sheet : écriture connue tenue à l'écart 0,74 / 0,74 / 0,96, nuls mélangés 0,000 et 0,005, mais AUC 0,875 seulement sur 6 surfaces vues à l'œil ; 15 surfaces sur 120 atteignent 0,5 de part ; 199,5 sur 1 007,5 cm2 passent (003.2).
→ reportés dans `benchmarks.csv` (par l'agent principal) : 6 lignes candidates (aire cumulée 355,0 cm2 ; |tilt| patchs 0,97° ; |tilt| contrôles tourbillonnants 4,70° ; part d'encre > 0,5 médiane 0,051 ; part V3 > 0,5 0,095 ; AUC on-sheet 0,875).

## Limites et critique

Dépôt communautaire non relu, chiffres auto-déclarés, une seule équipe (un portable). Les auteurs sont eux-mêmes prudents : un maillage propre n'est pas prouvé sur une seule couche (6 des 24 maillages officiels PHerc0826 passent aussi un rectangle de 4 cm2), l'accord avec la prédiction m7 est de l'auto-cohérence (même outil, même prédiction), la règle de frame suppose l'axe au centre XY du volume, les traces ne sont pas reproductibles au bit près (~2,4 voxels de médiane). La mesure d'inclinaison ne tranche pas (laminations visibles sur toute la profondeur, couches espacées de 10-12 voxels) ; les contrôles (3 plats, 3 tourbillonnants) ont été choisis à l'œil, et les 13 patchs ≥ 2° sont un seuil post hoc. Le score on-sheet est un filtre grossier (AUC 0,875, une surface tourbillonnante notée 0,35 au-dessus d'une plate à 0,14). Les cartes d'encre sont des sorties de modèles non entraînés pour ce régime, sans témoin ; « aucune lettre » ne dit pas que l'écriture est absente. Lecture visuelle : 90 premiers patchs en trois passes (dont deux à l'aveugle), 83 ajoutés en une passe non aveugle. Résultat négatif utile : à 8,6-9,4 µm sur ces surfaces automatiques, les modèles existants ne produisent rien de lisible. Nombres de patchs par rouleau du tableau README incomplets (3 lignes vides, somme des cellules ≠ 173) ; non vérifié ailleurs. Aucune comparaison à un autre traceur : « not a new tracing method ».

## Pertinence pour la thèse

Appuie directement la chaîne visée (surface m7 → traçage → rendu → lecteurs) : donne 173 patchs mono-surface candidats sur 13 rouleaux éligibles, une recette reproductible sur CPU, et un protocole de validation (inclinaison en coupe CT, contrôles plats/tourbillonnants, fraction de cartes d'encre au-dessus de seuils) pour la thèse « surface propre avant détection d'encre ». Il documente aussi un piège d'orientation (ordre F/R de `vc_render_tifxyz`). Reste ouvert : preuve de monocouche, témoin d'encre sur ces rouleaux, lettres.

## Gaps identifiés

- Critère indépendant et prouvé de « une seule couche » (la mesure d'inclinaison ne sépare pas une couche de ses voisines).
- Absence de témoin d'encre connue sur les rouleaux 8-9 µm : on ne sait pas quoi attendre des lecteurs.
- Seuils de probabilité d'encre non calibrés (parts > 0,5 de 5 à 10 % sur des surfaces sans lettres identifiées).
- Convention de frame / ordre des couches à normaliser entre outils (villa, rendus projet).

## Statut de lecture

Papier complet (`fulltext.md` lu en entier ; extraction `pymupdf`, `ok: false`, aucune section détectée, images omises : pas de tableaux, QA pictures non vues).
Déduit et non affirmé par les auteurs : la lecture critique sur le rôle d'un résultat négatif, les gaps ci-dessus, la remarque sur les cellules vides du tableau par rouleau. Chunk_ids : forme courte `#00x.y` du paper.
