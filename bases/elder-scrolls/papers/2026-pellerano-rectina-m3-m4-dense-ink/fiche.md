---
id: 2026-pellerano-rectina-m3-m4-dense-ink
fiche: done
date: 2026-11-17
---

# Rectina m3 and m4, dense ink readers for Herculaneum papyri rebuilt on current renders

Giovanni Pellerano, 2026, GitHub (evilaliv3/vesuvius-challenge-pipeline, results/db27c806-rectina). https://github.com/evilaliv3/vesuvius-challenge-pipeline/tree/7cb4e44/results/db27c806-rectina
Type : preprint non relu par les pairs (article de 17 pages hébergé sur GitHub, « not yet published », mis à jour le 10 nov. 2026 ; chiffres auto-déclarés, auteur unique).

## Problème

Détecter, pour chaque point d'une surface de papyrus segmentée, s'il porte de l'encre carbonée, sans contraste d'absorption net en micro-CT (Introduction, citant les organisateurs). L'article reconstruit la deuxième paire de checkpoints (m3, m4) du lecteur d'encre « Rectina » (m1 et m2 : article antérieur de l'auteur), et les compare aux lecteurs publiés Reader v2 et Reader v3 sur 14 unités d'évaluation. Il ne revendique ni nouvelle architecture, ni résultat hors de ces 14 unités, ni probabilité calibrée (§I).

## Méthode

- Réseau hybride 3D/2D de `villa` (ink detection), lu sur 17 plans de profondeur, une probabilité par pixel de la surface (§III). Entraînement depuis des poids aléatoires sur des labels composites denses : 87 segments de 8 rouleaux, dont 59 avec corrections de décalage et 28 avec labels publiés (§IV).
- Rendus bicubiques des 87 segments refaits avec le moteur `villa` actuel (24 re-rendus car l'ancien binaire était décalé d'environ 1,5 voxel au niveau 2) (§III).
- Deux ajouts via un patch de 3 fichiers (24 insertions, 4 suppressions) : plafond de revisite 0,5 dans l'échantillonneur (tirage pondéré par `physical_weight_power`) et augmentation gamma masquée et bornée (§II).
- Chaîne en étapes : s1 (78 125 itérations, patchs 128 px, batch 64), ft116k (12 000), s2 (40 000) donnent m3 ; s3 (30 000 itérations, 256 px, batch 10) et s4 (20 000, 384 px) à partir de m3 donnent m4. SGD, fp16, graine 42, weight decay 3e-5, label smoothing 0,5, checkpoint = dernier pas de l'étape, sans sélection sur la validation (§V, Annexe A). Schéma d'étapes en grandes tuiles repris de Reader v3 (§I).
- Mesure : 7 départs de 17 plans par unité, cartes calculées sur GPU, scores sur CPU ; AUC ROC contre le masque organisateur, AUC sur traits fins, « encre fausse » à rappel 80 % (§VI).
- Évaluation : 8 unités « tenues à l'écart » (segments de rouleaux d'entraînement, labels de l'auteur ; 6 à 116 keV, 2 à 113 keV) et 6 unités de contrôle (labels organisateurs pour ag1, ag2, w00, 0343 ; labels communauté pour w058, w060) (§VI, §VII-A).

## Plateforme et implémentation

- Matériel : « graphics processors of remote machines » pour les cartes (modèle, durée d'entraînement, temps d'inférence : n/r) ; scores sur CPU (§VI). Données à environ 9 µm (« 9 um class », §IX) ; source du scan hors synchrotron n/r dans l'article hors énergies 113/116 keV (§VI).
- Logiciel : `villa` main (commit 7e6b82164) + patch (sha256 c5622564771a) ; données du serveur dl.ash2txt.org (§IV, Annexe A).
- Publication : poids et model cards sur Hugging Face, dépôt `evilaliv3/rectina`, dossiers `m3` et `m4`, licence CC BY-NC 4.0 ; code de la recette sous MIT (§XI). Fichiers d'étude (units.csv, control-units.csv…) dans le dépôt GitHub de l'article ; l'article ne contient ni volumes ni labels (§XI).
- Non testé : lecteur public de l'article antérieur, inférence CPU, autres rendus, échelles autres que ~9 µm (§IX).

## Résultats

AUC moyenne sur 8 unités tenues à l'écart : Reader v3 0,8547 ; Reader v2 0,8421 ; m3 0,8532 ; m4 0,8637 (§VII, §VIII).

| Comparaison (AUC) | 8 tenues | 6 contrôles | 14 unités | source |
|---|---|---|---|---|
| m4 > Reader v3 | 6/8, médiane +0,0065 | 4/6, médiane +0,0008 | 10/14, moy. +0,0056, méd. +0,0049 | §VIII, Résumé |
| m4 > Reader v2 | 6/8, médiane +0,0249 | 5/6, médiane +0,0115 | 11/14, moy. +0,0175, méd. +0,0159 | §VIII |
| m3 > Reader v3 | 4/8, médiane -0,0033 | 2/6, médiane -0,0077 | 6/14, moy. -0,0047 | §VII |
| m3 > Reader v2 | 6/8, médiane +0,0115 | 3/6, médiane -0,0022 | 9/14, moy. +0,0072, méd. +0,0089 | §VII |

- Contrôles à labels organisateurs (4 unités) : moyenne 0,8735 (m4), 0,8639 (m3), 0,8736 (v3), 0,8596 (v2) ; m4 vs v3 : 2/4, différence moyenne -0,0001 (§VIII-A, §VII-A).
- AUC traits fins, moyenne 14 unités : v2 0,8595 ; v3 0,8706 ; m3 0,8666 ; m4 0,8764 (§VII, §VIII). Encre fausse à rappel 80 % (moyenne, moins = mieux) : v3 0,2458 ; v2 0,2704 ; m3 0,2525 ; m4 0,2315 (§VII, §VIII).
- Sensibilité au décalage de label (unité w00) : décaler le label au maillage (7,06 px) change l'AUC de +0,0022 (m4), +0,0010 (m3), -0,0006 (v3) (§IV).
- Modèles M7/M8 (fenêtres recentrées) : pas de gain (0,8513 contre 0,8673 pour m4 sur 7 unités) (§X). Combinaisons de lecteurs : gain moyen maximal +0,0039 sur m4 seul (§X, Annexe B).
- Les corps des Tables I à IV (valeurs par unité) manquent dans `fulltext.md` ; seuls les chiffres du texte sont utilisés.

→ reportés dans `benchmarks.csv` (par l'agent principal, à partir du fichier scratchpad `bench/2026-pellerano-rectina-m3-m4-dense-ink.csv`) : 8 lignes, `confidence: medium` (chiffres du texte) :
m4 et m3, AUC moyenne 8 unités tenues à l'écart (0,8637 ; 0,8532) ; m4 et m3, AUC moyenne 4 contrôles à labels organisateurs (0,8735 ; 0,8639) ; m4 et m3, AUC traits fins moyenne 14 unités (0,8764 ; 0,8666) ; m4 et m3, encre fausse à rappel 80 % moyenne 14 unités (0,2315 ; 0,2525).

## Limites et critique

- Preprint non relu, auteur unique, chiffres auto-déclarés, métrique propre de l'auteur, pas celle du concours (§X). Les scores sont lus par un outil depuis des CSV de l'étude (Annexe D) mais ne sont pas indépendamment reproduits.
- Une graine par checkpoint, aucune ablation : les changements (rendus, plafond de revisite, gamma masqué, version du code, s1 neuf) sont simultanés, aucun gain n'est attribuable (Résumé, §X). Bruit mesuré : écart-type 0,013 de l'exactitude équilibrée de validation, pas de bruit AUC ; l'auteur dit lui-même que des écarts de quelques millièmes ne sont pas un résultat (§X). Or le gain de m4 sur v3 est +0,0056 en moyenne, et +0,0008 en médiane sur les contrôles : sous le seuil de résolution (déduit).
- Les unités « tenues à l'écart » sont des segments de rouleaux d'entraînement (pas un rouleau tenu à l'écart) : fuite de domaine possible entre segments voisins d'un même volume ; la vérification de recouvrement compare seulement les identifiants (§VII-A). Ce n'est pas un test de transfert à un rouleau inédit.
- Comparaison de contrôles biaisée : rendus refaits pour m3/m4, mais Reader v2/v3 lus sur d'anciens rendus ; l'unité 0343 diffère de son ancien rendu pour une cause non prouvée (§VII-A, §X). Les labels des contrôles sont de trois natures (organisateurs manuels, masque des lettres approuvées connu par une image d'annonce, communauté) ; seules 4 unités sur 6 ont des labels organisateurs, et le découpage a été fait après les scores (§VII-A).
- Labels d'entraînement : 11 segments sur 87 contrôlés pour leur placement, 13 seulement contrôlables ; pour les 28 segments à labels publiés, un décalage éventuel n'est pas établi ; sources des labels non épinglées (§IV, §X). Décalage de 7 px mesuré sur w00 (§IV).
- Le AUC par unité dépend d'une fenêtre choisie (une par unité pour les tenues à l'écart) et d'un fond différent selon le type d'unité (« far negatives » pour les contrôles, tout le fond du masque de validation pour les tenues) : ces deux AUC ne sont pas comparables entre eux (Légende Table I).
- Bloc 113 keV : 2 unités d'un seul rouleau, rien à en conclure (§X). Rien sur la calibration, l'incertitude, la lisibilité réelle des lettres, les placebos ou une validation à l'aveugle.
- Reproductibilité : poids et recette publiés avec empreintes (§XI, Annexe D), mais matériel d'entraînement et durée n/r. Baseline GPU non pertinent ici ; coût de calcul non comparé.

## Pertinence pour le thème

Rattaché à `ink-detection` (cœur) et `validation-fp` (méthode de comparaison paire à paire avec contrôles, mesure de la sensibilité au décalage de label, aveu du bruit), avec `label-efficiency` (labels composites denses, corrections de décalage) et `domain-transfer` (contrôles hors segments d'entraînement, blocs d'énergie). Utile pour Elder-scrolls : recette reproductible d'un lecteur d'encre à ~9 µm partant de `villa` (même pile que Reader V3), avec poids publiés (CC BY-NC) ; confirme que l'entraînement en grandes tuiles (s3, s4) donne un gain d'AUC modeste et non établi ; fournit un protocole de comparaison honnête à imiter (même scorer, mêmes unités, avertissements). Reste ouvert : tout gain sous le bruit, aucun transfert à un rouleau inédit, rien sur la super-résolution 9 → 2,4 µm.

## Gaps identifiés

- Bruit AUC entre graines non mesuré : répéter l'entraînement (≥3 graines) avant de classer des lecteurs d'encre.
- Aucun lecteur n'est évalué sur un rouleau entièrement tenu à l'écart avec labels organisateurs (6 contrôles seulement, dont 2 communautaires).
- Pas de calibration ni d'incertitude des cartes ; pas de test placebo ni de lecture inversée.
- Effet des rendus (bicubique, décalage de 1,5 voxel) sur l'AUC non isolé.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Extraction `pymupdf`, `extraction.ok: false` : les corps des Tables I à IV et VI à VII sont absents, les figures 1 à 12 ne sont que des légendes, le texte est en places tronqué ou mélangé (« above Reader on 6 14 », fragments « 0.8383 (-0.0000) ») ; les chiffres par unité ne sont donc pas lus. Seuls les chiffres du texte courant sont utilisés (confidence medium).
Déduit et non affirmé par les auteurs : le gain de m4 sur v3 est sous le seuil de résolution de l'étude ; fuite de domaine possible entre segments d'un même volume ; non-comparabilité des AUC entre unités tenues à l'écart et contrôles.
