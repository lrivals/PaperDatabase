---
id: 2026-snyder-scroll-label-snap-snapping-approximate
fiche: done
date: 2026-11-17
---

# scroll-label-snap: snapping approximate recto-surface labels back onto the papyrus surface in Herculaneum scroll CT

A. Q. Snyder, 2026, GitHub. https://github.com/aqsnyder/scroll-label-snap/tree/e03c4c088c6f27e6edaf0502015a863f505e772b
Type : dépôt GitHub communautaire du Vesuvius Challenge (commit e03c4c088c, 2026-11-11), converti en PDF (README + `results/review_2026_11.md`, `ink_test.md`, `ink_test_0841.md`). Travail en cours vers un prix de progression ; non relu par les pairs, chiffres tous auto-déclarés (certains issus d'une revue automatique par Claude Code commandée par l'auteur, « no person has checked this write-up »).

## Problème

Les modèles de segmentation de surface sont entraînés sur des labels tracés à la main qui dérivent hors de la vraie surface du papyrus ; les organisateurs citent la qualité des labels comme un goulot du déroulage et suggèrent le « label snapping » (README, intro). L'auteur vise à replacer les labels recto approximatifs (cubes de labels et maillages tifxyz de VC3D) sur la face recto réelle.

## Méthode

Pour chaque cube : échantillonnage de la surface tous les ~3 voxels, normales tirées de la forme de la bande de label, orientation cohérente le long puis entre feuillets (le recto de chaque tour fait face au centre), score de décalage de -4 à +4 voxels (bord en marche + corrélation avec un profil de coupe appris), puis choix global par coupe de graphe exacte (Ishikawa) avec lissage L1, limite dure de 1 voxel entre voisins, rappel faible vers l'original et pénalité de déplacement vers l'extérieur (garde « inside-the-sheet », v2) (README §How it works). Les labels « flaggés » (face de polarité opposée) sont signalés pour revue humaine. Pour les maillages tifxyz : densification (~3 voxels), snap, puis réajustement sur la grille d'origine (~20 voxels) ; trois sorties : drop-in 20 voxels, fine 5 voxels, dense (README §Snapping traced meshes). Baseline : port du raffineur VC3D (ObjAlphaCompRefinement), seuils par défaut puis mieux réglés. Outil `smooth_snap.py` : lissage des déplacements sur ~1 vertex.

## Plateforme et implémentation

Calcul : CPU seul (Python, NumPy/zarr). Ryzen AI Max+ 395, 12 workers : 892 cubes (116 millions d'échantillons) en 15,8 h CPU, ~1,3 h réelles ; un cube 320³ prend 30-120 s par cœur, ~1 GB par worker (README §The whole dataset, §Usage). Maillage entier w035 (3,1 M d'échantillons) en 7 min avec 8 workers (§A whole segment). Tests d'encre sur un PC Windows, CPU seul, modèle `ink_9um` (`ink_test.md`). Données : cubes de labels Vesuvius (Hugging Face, CC BY-NC 4.0, 892 paires) ; PHerc. 0139 (w035, w052, 9,362 µm) ; PHerc. 0841. Code publié : https://github.com/aqsnyder/scroll-label-snap (le script de la revue de novembre n'est pas committé) ; poids : sans objet (méthode non apprise ; l'ink_9um utilisé pour les tests n'est pas fourni ici).

## Résultats

- Cubes, test de dérive (dérive lisse std 1,5 voxel, corr. 40), points « de confiance » : snapper dans 1 voxel de l'original 89% en développement (20 cubes) contre un raffineur VC3D bien réglé 80%, mais une recherche par échantillon sans graphe atteint 94% (README §Drift test). Erreur moyenne 0,52 contre 0,68 voxel (dév.), 0,55 contre 0,73 (100 cubes held-out) ; seuils par défaut de VC3D : 9% (dév.) contre 18% (held-out) avant réglage (README §Drift test).
- Revues aveugles de labels : 92% de préférence pour le label snappé (98 contre 8), relecteur unique = auteur (README §Result of review v1) ; 90% (63 contre 7), relectrice indépendante (README §Review v2).
- Maillage w052 (tenu à l'écart) : papyrus du côté recto 70% -> 93% ; w035 55% -> 88% (sortie dense, README §Snapping traced meshes). Auto-référent : le snapper optimise ce bord.
- Encre w052 (pré-enregistré) : carte du maillage original préférée 75 fois contre 31 (29% pour le snappé, IC95% 21-39%, p = 2,3e-5) ; AUC w035 0,998 -> 0,995 (`ink_test.md` §Primary/Secondary outcome). PHerc. 0841 : ΔAUC snappé - tracé poolé +0,011, aucun écart détectable (lire 0 ± 0,05) (`ink_test_0841.md` §A).
- Topologie (892 cubes) : les composantes notables passent de 6 827 à 5 424, 1 438 fusions de feuillets dans 559 cubes, tunnels dans les 892 cubes (`review_2026_11.md` §Topology).
- Face contre référence indépendante (deux scans plus résolus, PHerc. 0139, 173 vertices) : 18% à moins de 1 voxel contre 17% avant snap (README §Status).
→ reportés dans `benchmarks.csv` (par l'agent principal, depuis le fichier scratchpad) : 8 lignes — dérive dév. 89%, erreur moyenne dév. 0,52 et held-out 0,55, w052 recto 93%, revue encre 29%, revue v1 92%, revue v2 90%, ΔAUC PHerc. 0841 +0,011.

## Limites et critique

- Dépôt communautaire, non relu, tout auto-déclaré ; la revue de novembre est elle-même automatique (Claude Code) et non vérifiée par un humain. Résultats exploratoires majoritaires ; seuls les tests pré-enregistrés ont valeur confirmatoire.
- Résultat principal négatif pour l'encre : la géométrie s'améliore (bord de densité mieux placé) mais l'encre n'est pas mieux lue (75 contre 31) ; l'auteur recommande de ne pas utiliser les maillages snappés pour la détection d'encre. Cause non établie (cartes plus sombres, bosses à l'échelle du vertex ; le lissage retient 35-43% du gain à la face).
- Le test de dérive est circulaire : les points de confiance sont choisis par le même score de bord que le snapper optimise ; une recherche par échantillon sans coupe de graphe le bat (94% contre 89%) et l'ordre s'inverse selon la définition de la confiance (85,5% contre 82,2%). Il ne classe donc pas les méthodes. Le test mesure la cohérence, non l'exactitude par rapport à la vraie face.
- Les revues aveugles de labels : relecteur unique et auteur (v1), une seule relectrice (v2), bords en escalier révélateurs en v1, garde v2 choisie après avoir vu les pertes (chiffres optimistes) ; les cubes dev ont servi au réglage ; l'ensemble held-out est désormais consommé. Accord inter-relecteurs de la revue encre faible (kappa 0,12).
- Contre une référence indépendante (Chase, 2 scans) : 18% contre 17%, pas de gain à la face ; la revue topologique montre tunnels et fusions de feuillets introduits par le déplacement non rigide.
- Bug de transfert de profondeur découvert après coup (jusqu'à 19,5% de touches perdues sur la sortie dense) ; les résultats 0841 corrigés sont post hoc ; des pertes poolées jusqu'à ~0,09 AUC restent permises par les intervalles. Les tableaux de `fulltext.md` ont perdu des colonnes à la conversion PDF (voir Statut de lecture).
- Une seule architecture d'encre (ink_9um, deux graines), un segment held-out, un rouleau non vu : rien de général. Pas de comparaison avec d'autres travaux de raffinement de surface de la communauté ; VC3D jamais ouvert sur les sorties ; métriques officielles (TopoScore, VOI) non exécutées.

## Pertinence pour la thèse

Apport à `virtual-unwrapping` : un cas d'étude honnête (résultat négatif pré-enregistré) montrant qu'optimiser la position de surface sur le bord de densité ne suffit pas pour la lisibilité de l'encre, et que les métriques de géométrie (cohérence de dérive, papyrus côté recto) ne prédisent pas l'encre. Utile pour la qualité des labels de surface (problème ouvert 2026) et comme référence de validation (revue aveugle, pré-enregistrement). Reste ouvert : revue aveugle à affichage apparié pour séparer « plus sombre » de « moins lisible », référence de position indépendante de la CT, préservation de la topologie des labels.

## Gaps identifiés

- Comparaison à affichage apparié (même niveau) des cartes d'encre snappées et originales.
- Mesure de position de surface indépendante du critère optimisé (deux résolutions de scan, vérité de terrain).
- Effet de la correction de labels sur la topologie des cubes (tunnels, fusions) et sur les pertes d'entraînement, avec TopoScore/VOI.
- Résolution de l'ambiguïté « face lointaine / gap traversé » des labels flaggés.

## Statut de lecture

Papier complet (tout `fulltext.md` lu ; backend d'extraction `pymupdf`, `ok: false`, aucune section détectée). Les tableaux de résultats (drift test, cohérence, comparaisons de maillage, v1 contre v2) sont tombés en désordre dans le texte extrait : plusieurs cellules (valeurs du raffineur, du snapper held-out, de la cohérence) manquent ; seules les valeurs rédigées en prose sont retenues et les autres sont `n/r`. Ce qui suit est déduit et non affirmé par les auteurs : le caractère « circulaire » du test de dérive est reformulé d'après la revue de novembre qui le dit lui-même ; l'écart de 9-10 points avec le raffineur est celui du texte (README §Drift test) ; la qualification « négatif » du résultat encre est la formulation de l'auteur, non une interprétation externe.
