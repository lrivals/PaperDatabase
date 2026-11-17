---
id: 2026-de-meij-pherc-0306b-winding-w040-row
fiche: done
date: 2026-11-17
---

# PHerc. 0306B, winding w040: a row of letters, with segments, labels and predictions

David de Meij, Nicolas Brown, Nataliia Bazaka, 2026, GitHub (commit 9aee0e66f3, 2026-11-04). https://github.com/daviddemeij/pherc0306b-partial-letters-w040/tree/9aee0e66f3d7c437329104ec961623c4f0d181a5
Type : dépôt GitHub communautaire du Vesuvius Challenge (`repo`), non relu par les pairs ; tous les chiffres sont auto-déclarés (README §en-tête). Documents convertis : README.md et reader-v3-screen/README.md.

## Problème

Les auteurs annoncent une rangée de lettres sur le winding w040 du rouleau PHerc. 0306B (bloc inférieur, z 6912–9216, scan 20250521133212, 8,64 µm) et publient de quoi la vérifier, la réutiliser ou la prolonger : segments, labels, prédictions brutes, figures (README §intro). Ils ne prétendent pas à une lecture : « Five letters, three of them uncertain. This is not a reading » (README §Limits).

## Méthode

Chaîne décrite en 8 étapes (README §How it was made) :
- Surface : windings w040/w041 issus d'un ajustement de spirale lasagna (villa `fit_spiral`) sur le bloc z 6912–9216, aplatis et accrochés à la prédiction de surface m7 des organisateurs. Le maillage est coupé à un angle fixe, d'où la fin de w040 juste après γ ; la même feuille continue en w041, qui colle avec un résidu médian d'environ 2 voxels (18 µm) (étapes 1-3, `2026-de-meij#000.3`). Dans la figure, w041 est placé par une seule translation entière (5466, 187) px, sans déformation ; un écart d'environ 0,3 mm subsiste au raccord.
- Rendu : 66 couches le long de la normale, pas de 1 voxel, échantillonnées au niveau 0 du volume masqué public.
- Encre : Reader v3 (HF `domenicor046/reader-v3`, rév. aee1d64) à des décalages de profondeur de −4 à +2 voxels, sur les deux faces : « reading » et « blind » (ordre des couches inversé).
- Paire de profondeurs : par pixel, meilleure moyenne de deux profondeurs adjacentes (un trait vu à deux profondeurs garde sa force, une tache vue à une seule est divisée par deux), après moyenne sur 8 flips/transpositions à d−2, d0, d+1 ; même règle sur la face aveugle comme témoin (`code/depthpair.py`).
- Affichage : jaune clair sur la moyenne des couches CT 31–35, sans seuil.
- Labels : cinq lettres marquées à la main par D. de Meij sur les cartes Reader v3 de profondeur 0, le 22 octobre 2026 : χ et θ « sûres », π, λ, γ « incertaines », avec boîtes en pixels plats de w040 (README §The letters, `2026-de-meij#000.1`). Ce sont des observations, pas une sortie de modèle.

Vérifications (README §Checks, `2026-de-meij#000.4`, `#000.5`) : reconstruction indépendante de la rangée (prédictions de feuillet « Socratic » neuves, maillage en cubes et assemblage ScrollFiesta), à 1,4 voxel médian de w040, où Reader v3 montre les mêmes lettres aux mêmes endroits avec une face aveugle « presque vide » ; témoin de face aveugle (taches dispersées mais aucune forme de lettre de la rangée, panneau D) ; orientation de lecture vérifiée géométriquement (z vers le bas, angle croissant vers la droite, comme sur leur page W073 dont la lecture a été confirmée indépendamment) ; placement de la feuille d'après le profil CT le long de la normale : feuille à 1–4 voxels de la surface, voisines à 11–13 voxels vers l'intérieur et 17–20 vers l'extérieur, traits plus brillants sur la face externe (+3 à +9 voxels).

Extension : « Reader v3 production screen » (reader-v3-screen/README.md) : 536 sections de production, 1 072 TIFF (deux directions, profondeur 0) plus 925 TIFF supplémentaires, soit 1 997 TIFF en 12 ZIP, 11 812 543 798 octets ; couverture partielle de z2304–13824, rien pour z0–2304 ni z13824–15898 (`2026-de-meij#001.1`). Recette de production : dalle rendue de 18 couches, profondeur 0, batch 8, deux directions, sans TTA, recouvrement 0,5 avec fenêtre de Hann (`#001.2`).

## Plateforme et implémentation

Matériel de calcul (GPU, temps d'inférence) : `n/r`. Logiciels : villa `fit_spiral`, VC3D (commit 41701aa), villa commit 0fb38c4, ScrollFiesta, Reader v3 (poids sur Hugging Face, SHA-256 ea405417…). Code publié (MIT, `code/` : stitch_w040.py, make_w040_figure.py, depthpair.py, select_w040.py, remote_w040.sh, render_w040.py) ; données, figures et labels en CC BY-NC 4.0. Le README précise que le code est « celui qui a tourné dans le dépôt de laboratoire », chemins relatifs. Lien : dépôt GitHub ci-dessus.

## Résultats

- Cinq lettres : χ (sûre, 2,29 × 3,05 mm), π (incertaine, 2,32 × 2,65), λ (incertaine, 2,16 × 3,23), θ (sûre, 2,70 × 2,70), γ (incertaine, 2,26 × 2,76) (README §The letters, `2026-de-meij#000.1`). Centre 3-D (5166, 4399, 8345) voxels. Autre encre, plus faible et fragmentée, à gauche de χ et sur w041 à 1,5–3 cm à droite de γ, non labellisée.
- Raccord w041/w040 : résidu médian ≈ 2 voxels (18 µm) (README §How it was made, étape 3, `#000.3`).
- Reconstruction indépendante : 1,4 voxel médian de w040 (README §Checks, `#000.4`).
- Aucune métrique de détection (précision, AUC, F1, CER) n'est rapportée : les résultats sont qualitatifs (figures).
- Autres modèles 9 µm publics (Reader v2, dense-native, ink_9um, v8-in) « plus bruités » sur ce rouleau selon les auteurs, sans chiffres (README §Limits, `2026-de-meij#001.0`).
→ reportés dans `benchmarks.csv` : 2 lignes proposées (agent principal) : résidu médian w041/w040 (2 voxels) ; distance médiane de la reconstruction ScrollFiesta (1,4 voxel). Sources : README, confidence medium.

## Limites et critique

- Dépôt communautaire, auto-déclaré, non relu ; pas de lecture revendiquée. Trois lettres sur cinq incertaines ; χ, à mi-distance de la feuille externe voisine, est la moins sûre (README §Checks).
- Un seul modèle (Reader v3) ; aucune validation en aveugle par tiers, pas de k-fold ni test placebo en dehors du témoin de face aveugle. Les labels sont posés par l'un des auteurs sur les cartes du modèle : risque de circularité (déduit).
- Le témoin aveugle montre des taches dispersées et, côté w041, des « blobs » ; l'ensemble repose sur un jugement visuel sans seuil ni métrique.
- Incohérence apparente à clarifier : w041 est présenté comme la continuation de w040 (résidu ≈ 2 voxels), mais la reconstruction ScrollFiesta du raccord « found the neighbouring sheet there (about 10–15 voxels away), not this one » ; la continuation droite est donc une translation entière unique de w041, pas une surface nouvelle (README §Limits). La partie droite est la moins fiable.
- Le résidu d'environ 2 voxels et l'écart de 0,3 mm au raccord ne sont pas des erreurs de segmentation mesurées contre une vérité terrain.
- Pas de contraste CT visible hors modèle : la pertinence de l'encre dépend entièrement de Reader v3.
- Screen de production : couverture partielle, fenêtres/orientations propres à chaque source (« do not impose a single display flip »), noms « reading/opposite » purement calculatoires ; une partie des TIFF supplémentaires n'a pas de hash préexistant indépendant (reader-v3-screen/README.md §Files and verification).

## Pertinence pour la thèse

Utile à l'axe détection d'encre à 8–9 µm (signal conservé à 8,64 µm avec un modèle générique 9 µm), à la validation (témoin de face aveugle, reconstruction de surface indépendante, contrôle de profondeur de la feuille) et à la segmentation de surface (raccord de windings, fit_spiral + m7, ScrollFiesta). Les 1 072 cartes de production et les maillages tifxyz publiés sont réutilisables comme référence de Reader v3 sur PHerc. 0306B. Reste ouvert : lecture du texte, validation quantitative, effet de la résolution (pas de comparaison 2,4 µm).

## Gaps identifiés

- Aucune métrique de détection d'encre ni intervalle d'incertitude sur ce rouleau ; labels non indépendants du modèle.
- Contrôle de faux positifs standardisé (témoin aveugle chiffré, test placebo) absent.
- Raccord entre windings consécutifs coupés à un angle fixe : translation unique, sans recalage ni mesure d'erreur.

## Statut de lecture

papier complet (README.md et reader-v3-screen/README.md ; extraction pymupdf, `extraction.ok` faux, sections non détectées, images omises : figures et panneaux A-E non lus). Les tailles en mm des lettres sont cohérentes avec 8,64 µm/px (vérifié par calcul). Déduit et non affirmé par les auteurs : le risque de circularité des labels, l'incohérence signalée sur le raccord w041, l'absence de métrique.
