---
id: 2026-ruiconte-ink-swarm-argus-v1-v2
fiche: done
date: 2026-11-17
---

# ink-swarm: Argus V1 and V2 ink-detection checkpoints for Herculaneum scroll surface volumes

ruiconte, 2026, GitHub (commit d38015a0ba). https://github.com/ruiconte/ink-swarm/tree/d38015a0ba09a009bdf64bc8535877a041a7edda
Type : dépôt GitHub communautaire du Vesuvius Challenge (README + v2/README), non relu par les pairs ; tous les chiffres sont auto-déclarés.

## Problème

Fournir des checkpoints d'encre « drop-in » (même réseau et même format que `reader-v3.pth`) pour des volumes de surface à l'échelle 9 µm. V1 (entraîné sur des rendus poolés issus de scans 2,4 µm) perdait contre Reader V3 sur les scans natifs 113 keV (PHerc0841 AUC 0.869 vs 0.913) (README §Argus V2, 2026-ruiconte#000.0) ; V2 vise à corriger cet écart de domaine (résolution/format de rendu), tout en contrôlant l'hallucination par un test d'ordre des couches inversé.

## Méthode

- Réseau : `vesuvius_unet_3d_stem_2d`, 34,6 M de paramètres, fenêtre de 17 couches centrée sur la surface, normalisation MAD robuste (1-99 %), tuiles 256 px (README §Argus V1).
- V1 : base `ink9um-dense dense9um-all7-step075000.pth` (domenicor046) ; 8 fine-tunes de 8 000 itérations (batch 8, lr 2.5e-4 ou 5e-4, 4 seeds chacun), pseudo-labels denses, perte BCE (label smoothing 0.5) + Dice ; données PHerc0139, PHerc1667, PHerc Paris 4, PHerc0814 (rendus 2,4 µm poolés, 21 couches) ; **weight soup** des 8 runs (Wortsman et al. 2022). Le depth flip de la recette de référence est retiré : avec flip, AUC en ordre inversé 0.79 ; sans, 0.53 (README §Argus V1, 2026-ruiconte#001.0).
- V2 : Reader V3 (domenicor046) affiné sur scans natifs 8-9 µm, 12 000 itérations, tuiles 256 px, batch 8, SGD lr 2.5e-4, BCE + Dice, pas de depth flip ; données : 30 % aléatoire, par blocs, de la zone supervisée de 70 segments natifs de `reader-v2-labels` (PHerc0139, 0814, 0500P2 à 113 keV ; 0009B, 0343P à 116 keV ; 0172 à 53 keV) ; sélection du checkpoint sur 3 segments tenus à l'écart (README §Argus V2, 2026-ruiconte#000.2).
- Évaluation : tuiles 256 px, TTA 8x, seuil de « fond marqué encre » = seuil à 80 % de rappel propre à chaque modèle ; contrôle placebo par inversion de l'ordre des couches.

## Plateforme et implémentation

Matériel d'entraînement/inférence : n/r. Logiciels : PyTorch, zarr, etc. ; compatible HerculeX, ink-sdk, tout outil chargeant Reader V3. Poids publiés (MIT) : https://huggingface.co/ruiconte/argus-v1 et https://huggingface.co/ruiconte/argus-v2 ; code (prep.py, dense_prep.py, heldout_prep.py, eval_all.py, heldout_eval.py, val256.py, train.py, soup.py, native_v2_prep.py, seg_eval.py) dans https://github.com/ruiconte/ink-swarm. Scans : Vesuvius Challenge open data (113/116/53 keV selon rouleau).

## Résultats

Les tableaux de métriques du README ont été perdus à la conversion PDF (extraction PyMuPDF, `extraction.ok` faux) : seuls les chiffres cités en prose sont disponibles.

- V1 sur PHerc0841 w00 natif (jamais vu) : AUC 0.869 vs 0.913 pour Reader V3 (2026-ruiconte#000.0) ; best Dice 0.758 vs 0.767, fond marqué encre 8.9 % vs 8.5 % (README §Where Argus is weaker, 2026-ruiconte#000.4).
- Contrôle placebo : AUC en ordre inversé 0.53 sans depth flip contre 0.79 avec (2026-ruiconte#001.0).
- Crop central PHerc0139 w053 (3072 px, non vierge selon la carte 1 µm) : V1 marque 14.9 % vs 10.0 % pour Reader V3 ; en ordre inversé 1.1 % vs 2.7 % ; V1 retrouve 80 % de l'encre de la carte 1 µm vs 61 % (2026-ruiconte#000.4, #000.5).
- V2 : moyenne de 3 fenêtres (-2/0/+2) sur PHerc0841 natif : AUC 0.928 vs 0.922 pour Reader V3 ; gain d'environ 1 point d'AUC pour les deux modèles (2026-ruiconte#000.2). Sur PHerc1447 w058, AUC de V2 inférieur de « 0.2 points » à Reader V3, mais Dice/bAcc/fond meilleurs ; sur les 3 masques de validation officiels (rendus poolés), V1 > Reader V3 > V2 en pratique (2026-ruiconte#000.1).
→ reportés dans `benchmarks.csv` (par l'agent principal, depuis le CSV du scratchpad) : 7 lignes (V1 AUC 0841, Dice 0841, fond 0841, AUC inversé, crop w053 14.9 %, rappel w053 80 %, V2 AUC 0.928).

## Limites et critique

- Dépôt communautaire, non relu, chiffres auto-déclarés, un seul auteur ; comparaison à Reader V3 et à d'autres checkpoints de la communauté par le même auteur, avec son code d'évaluation.
- Labels de test : « team labels » (2026-09-18) et labels raffinés de tiers (YoussefMoNader, CC BY-NC) sur un petit nombre de segments (PHerc0841 w00, PHerc1447 w058/w060, crop w053) ; pas d'intervalles de confiance ni de seeds d'évaluation.
- Les écarts sont parfois minces (0.928 vs 0.922) et Reader V3 reste meilleur sur Dice/fond à 0841 pour V1 ; V2 est plus faible sur 1447 w058 (AUC) et sur les masques officiels : pas de modèle dominant, l'auteur le reconnaît.
- L'inversion de l'ordre des couches est un contrôle utile, mais l'auteur admet qu'il n'y a pas de labels humains dans les zones marquées en plus : « leads to check, not readings » ; l'absence d'hallucination de texture n'est donc pas prouvée.
- Les seuils « 80 % recall » propres à chaque modèle et la dépendance au format de rendu (2,4 µm poolé vs natif) rendent les chiffres non comparables d'une table à l'autre et avec d'autres papiers (autres labels, résolutions, métriques).
- V1 a perdu contre Reader V3 sur natif : le transfert 2,4 µm -> 9 µm par rendus poolés n'est pas acquis ; V2 corrige en entraînant directement sur natif.
- Matériel et temps de calcul : n/r.

## Pertinence pour la thèse

Apport direct à l'axe détection d'encre et transfert de domaine : cas concret où un modèle entraîné sur rendus 2,4 µm perd sur scans natifs 8-9 µm (donc sur les rouleaux non lus), et correctif par fine-tuning natif ; recette utile (weight soup, suppression du depth flip, TTA, moyenne de fenêtres de profondeur) et, pour la validation/faux positifs, un contrôle placebo par inversion de l'ordre des couches. Laisse ouvert : preuve humaine des marques supplémentaires, comparaison sur un jeu de test commun, calibration et incertitude.

## Gaps identifiés

- Pas de comparaison à labels humains indépendants des « leads » supplémentaires (faible précision prouvée).
- Pas de barres d'erreur ni de test sur plusieurs rouleaux natifs tenus à l'écart (seulement 0841 et 1447).
- Pas de coût matériel/temps documenté.
- Question du transfert 2,4 -> 9 µm sans fine-tuning natif non résolue.

## Statut de lecture

papier complet (README.md et v2/README.md lus en entier, 11,9 ko). Extraction pymupdf, `extraction.ok` faux : les corps des tableaux de métriques (colonnes, valeurs) ont disparu ; seules les valeurs données en prose sont utilisées. Déduit et non affirmé : l'attribution du chiffre AUC inversé 0.53 à un jeu précis (non précisé), les rôles (baseline) des modèles dans les tableaux perdus, et l'interprétation de « 0.2 points ».
