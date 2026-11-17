---
id: 2026-nexusai-kevin-vesuvius-ink-bench-volumetric-ink
fiche: done
date: 2026-11-17
---

# vesuvius-ink-bench: volumetric ink-detection benchmarking and low-VRAM inference for Herculaneum scroll CT

nexusai-kevin, 2026, GitHub (commit 6bd16ff893, 2026-11-16). https://github.com/nexusai-kevin/vesuvius-ink-bench/tree/6bd16ff8936575cfa7db1b4a54b2555d5d2d820a
Type : dépôt GitHub communautaire du Vesuvius Challenge (`repo`), non relu par les pairs ; tous les chiffres sont auto-déclarés par l'auteur (README, reports/benchmark_report.md). Pas de DOI ni d'arXiv.

## Problème

Rendre l'inférence de détection d'encre du Vesuvius Challenge exécutable sur une carte grand public (< 3 GiB de VRAM annoncés) en streamant les volumes OME-Zarr publics (AWS Open Data) plutôt qu'en les téléchargeant, et fournir une suite de validation reproductible (débit, VRAM, raccords entre tuiles, score contre des labels d'encre) (README §Quick Start, §Reproducible Validation Suite).

## Méthode

Réimplémentation du modèle officiel `VillaInkResNet3D` (ResNet3D-152 + décodeur 3D FPN, 976 tenseurs, chargement `weights_only=True`, `strict=True`) avec le checkpoint `scrollprize/ink_canonical_2um` (`r152_3ddec_v2_l5_epoch13.ckpt`, epoch 13) (README §Key Architecture; report §1). Aucun entraînement : l'apport est l'ingénierie d'inférence. Lecteur OME-Zarr (v2/v3) avec cache LRU en RAM hôte (budget 16 GiB), tuiles 64x128x128 de stride 32/64/64, batch 8, bfloat16, fusion par fenêtres de Hann séparables 3D + Z (report §2-§3). Sorties : carte 2D de probabilité d'encre (TIFF 16 bits, PNG, Zarr) et prédictions 3D par tranches de profondeur (README §Quick Start). Détail de la projection 3D vers 2D (« DepthAttentionCollapse ») : nommé, non décrit.

## Plateforme et implémentation

GPU NVIDIA RTX 5080 16 Go, Windows 11, Python 3.12.13, PyTorch 2.11.0+cu128, CUDA 12.8, graine 42, tampons épinglés (report §1). RAM hôte DDR5 (cache 16 GiB). Code publié sous licence MIT à https://github.com/nexusai-kevin/vesuvius-ink-bench ; poids : checkpoint officiel scrollprize (MIT), téléchargé automatiquement ; données : EduceLab-Scrolls / AWS Open Data (CC BY-NC 4.0) (README §License). Entrées : PHerc0332 (volume 2,399 µm, 78 keV, niveau 2, forme 8398x3941x3941, uint8) et PHercParis4 (2,4 µm) (report §2, §5).

## Résultats

Validation contre labels (PHercParis4, segment 20230702185753, ROI 109x512x512, fraction d'encre 27,98 %) (report §5, `2026-nexusai-kevin#004.0`) : ROC-AUC 0,9546 ; au seuil 0,50 : F0.5 0,7903, Dice/F1 0,8271, IoU 0,7052 ; au seuil 0,70 : F0.5 0,8724, Dice 0,8491, IoU 0,7377. Pic VRAM sur cette ROI : 3121,41 MiB alloués / 3444 MiB réservés (report §5).

Débit sur PHerc0332 niveau 2, ROI 128x384x384, 75 tuiles : 83 196 727,9 voxels de tuile/s (79,34 tuiles/s) ; 19 385 945,7 voxels de ROI/s ; temps GPU 0,9453 s ; pic VRAM 2506,13 MiB alloués / 2912 MiB réservés (report §3, `2026-nexusai-kevin#003.0`). Flux froid S3 : 1,7517 s pour 18 MiB ; lecture à chaud du cache : 0,00886 s (2,13 Go/s, taux de succès 50 %) (report §2, `2026-nexusai-kevin#002.0`).

Raccords : gradient de bord de tuile 0,114695 (sans fusion) contre 0,000661 (Hann 3D+Z), ratio bord/intérieur 122,4066x contre 0,3466x ; « réduction 99,42 % » (report §4, `2026-nexusai-kevin#003.0`).

→ reportés dans `benchmarks.csv` (par l'agent principal, via le CSV du scratchpad) : 7 lignes : ROC-AUC 0,9546 ; F0.5 0,7903 (th 0,5) ; Dice 0,8271 ; IoU 0,7052 ; F0.5 0,8724 (th 0,7, seuil choisi sur la ROI) ; débit 83 196 727,9 voxels/s ; pic VRAM 2506,13 MiB. Aucun chiffre de latence/puissance (`n/r`).

## Limites et critique

- Auto-déclaré, non relu ; un seul auteur, un seul run, pas de barre d'erreur ni de répétition.
- Validation sur **une seule ROI** (109x512x512) d'un seul segment ; ni rouleau, ni région tenus à l'écart déclarés. Le checkpoint `ink_canonical_2um` a pu voir PHercParis4 à l'entraînement (déduit : provenance des données d'entraînement non documentée ici), donc ROC-AUC/F0.5 peuvent être optimistes et ne démontrent pas la généralisation.
- Le « F0.5 optimal » (0,8724, th = 0,70) est un seuil choisi sur les mêmes labels que l'évaluation : borne haute, non comparable à un score à seuil fixé a priori. Même ROC-AUC dans les deux colonnes (attendu, indépendant du seuil).
- Labels `inklabels.zarr` : nature (IR, manuels, pseudo-labels) non dite ; critère de projection 2D vs labels 2D non précisé. Aucune comparaison à un autre modèle, ni au pipeline officiel sur la même ROI : on ne sait pas si l'implémentation reproduit les scores officiels (la conformité n'est affirmée que par le chargement strict des poids).
- Incohérence : le README annonce « under 3 GiB VRAM » alors que le pic sur la ROI de validation est de 3121,41 MiB alloués (> 3072 MiB) (report §5). Le chiffre < 3 GiB vaut seulement pour la ROI PHerc0332.
- « Réduction 99,42 % » : correspond à la baisse du gradient de bord (0,114695 -> 0,000661), pas à celle du ratio (122,4x -> 0,35x = 99,72 %, calcul déduit). La métrique de raccord est un indicateur de lissage, pas de qualité d'encre ; le gradient intérieur double (0,000937 -> 0,001906) : le lissage dilue peut-être du détail.
- Débit : un seul run, ROI minuscule (18 MiB), mesure GPU seule ; ne couvre pas le temps total (flux S3 1,75 s ≈ 2 fois le temps GPU de 0,95 s). Le cache à chaud n'a que 50 % de succès. Le niveau 2 de l'OME-Zarr n'est pas converti en µm/voxel (le volume est à 2,399 µm au niveau 0, résolution du niveau 2 : n/r). Pas de baseline CPU / autre GPU. Constat de résolution : tout est à 2,4 µm, rien sur la détection à 8-9 µm (cœur de la question de la base).
- URI du report §5 `vesuvius-challenge-opendata` (sans tiret) différent du bucket `vesuvius-challenge-open-data` du README : coquille probable (déduit).

## Pertinence pour la thèse

Faible à moyenne pour le thème : utilitaire d'inférence et banc de référence de l'encre à 2,4 µm, utile comme point de départ reproductible (poids officiels, streaming Zarr, 16 Go de GPU compatibles avec notre RTX 5090 32 Go) et comme exemple de validation sur labels (ROC-AUC, F0.5). N'apporte rien sur la super-résolution 9 -> 2,4 µm, la segmentation de feuillets, l'aplatissement ou la validation à l'aveugle ; ne traite pas la détection d'encre à 8-9 µm. Ne répond pas aux faux positifs (pas de test placebo ni de lecture inversée).

## Gaps identifiés

- Aucune évaluation sur rouleau/région tenus à l'écart avec ce checkpoint (risque de fuite non levé).
- Performance de l'encre à 8-9 µm (résolution des scans First Letters) : non mesurée ici.
- Pas de calibration ni d'incertitude de la carte de probabilité.

## Statut de lecture

Papier complet (fulltext.md lu en entier, 188 lignes). Extraction `pymupdf`, `extraction.ok` à `false` : texte plausiblement complet mais des tableaux sont aplatis (tableaux README et report lus comme texte, chiffres recoupés entre README et report). Déduit et non affirmé par les auteurs : possible fuite d'entraînement sur PHercParis4, optimisme du F0.5 à seuil optimal, origine du 99,42 %, coquille du bucket, absence de comparaison à l'implémentation officielle.
