---
id: 2026-gilman-spiral-fit-inputs-first-windings
fiche: done
date: 2026-11-17
---

# Spiral-fit inputs and first windings for PHerc. 1203, 1218, 1545 and 0846B

Jack Gilman, Andrew Gilman, 2026, GitHub (Ahggggg/spiral-tracks-four-scrolls, commit b6062e13cd, 2026-11-15). https://github.com/Ahggggg/spiral-tracks-four-scrolls/tree/b6062e13cd6c9a0d8beccb0e946e9afeb120cd7c
Type : dépôt GitHub communautaire du Vesuvius Challenge (README.md + MANIFEST.md), non relu par les pairs ; tous les chiffres sont auto-déclarés par les auteurs (`#000.0`).

## Problème

Pour quatre rouleaux (PHerc. 1203, 1218, 1545, 0846B), le jeu public de « tracks » pour l'ajustement de spirale (dl.ash2txt.org/datasets/spiral_datasets/) n'existe pas ; sans tracks, la « winners' lane » (recette de dépistage d'encre des gagnants de PHerc. 0306B) ne peut pas démarrer (README §Why this might be useful, `#000.3`). Les auteurs publient donc des tracks, un ajustement de spirale et trois enroulements par rouleau comme preuve que ces entrées sont utilisables.

## Méthode

- Tracks : extracteur de villa (`extract_surface_tracks`, `convert_track_store`, `build_track_crossings`) inchangé, sur la prédiction de surface publique m7 de chaque rouleau, avec les paramètres des tracks publiés de PHerc. 0358 (sous-échantillonnage 2, seuil de poussière 400, mode `interjoint`…) (README §How the tracks were made, `#001.0`). Une bande de 1 500 coupes par rouleau (+300 coupes de marge de chaque côté) (README §What is in this release, `#000.3`).
- Ajustement : villa spiral fit, 8 000 pas, un seul sens (anti-horaire vers l'extérieur), puis snap sur les feuillets prédits, aplatissement et rendu de trois enroulements (069, 070, 071) en 31 couches (`#001.0`).
- Umbilic : annotations communautaires de Drobkov pour 1545, 1218, 1203 ; pour 0846B, umbilic construit par les auteurs à partir des grilles de normales publiques, et normales produites avec `make_normals.py` des gagnants (non publiées) (README §What this shows, point 4, `#000.2`).
- Encre : Reader V3 (domenicor046) sur les 12 enroulements, dans les deux ordres de couches (24 cartes), lecture à l'œil par un seul lecteur ; cartes descriptives, pas un test d'encre (`#000.2`, `#002.0`).

## Plateforme et implémentation

- Tracks : portable, 4 processus CPU, WSL Ubuntu, 1,1 à 1,9 h par rouleau, sans GPU (README §How the tracks were made, `#001.0`).
- Fits : RTX 4090 louée, 65 / 71 / 67 / 90 min (1545 / 1218 / 1203 / 0846B), 0,96 / 1,05 / 1,00 / 1,33 USD, soit 4,34 USD au total ; le fit seul dure environ 37 min à 3,2-3,6 pas/s, 16,5-16,7 Go de GPU ; la durée de 0846B inclut ~12 min pour 320 tuiles de normales (`#001.0`, `#001.1`).
- Cartes d'encre : GPU de portable (Intel Arc, FP32), écart max GPU/CPU de 7e-7 sur six tuiles (`#001.1`).
- Publié : tracks (neuf fichiers `.vctracks`, `.dbm`, `.crossings.npz`), umbilics, job files, archives de fit et de rendu, 77 fichiers, 18,43 GiB, SHA-256 dans MANIFEST.md ; données CC BY-NC 4.0, code MIT ; `fetch_tracks.sh` fourni. Les cartes Reader V3 brutes, les normales de 0846B et les tracks pleine longueur (~110 Go, 53 bandes par rouleau) ne sont pas publiés (README §What is in this release, §Measured limits, `#000.4`, `#002.1`). Puissance : n/r (non pertinent).

## Résultats

Enroulements 069 / 070 / 071, valeurs lues dans les logs de fit et les rapports de snap (README §Results per scroll, `#001.4`, `#001.5`) :

| | 1545 | 1218 | 1203 | 0846B |
|---|---|---|---|---|
| Part de points avec un feuillet proche | 0,928 / 0,927 / 0,927 | 0,943 / 0,944 / 0,944 | 0,870 / 0,842 / 0,839 | 0,842 / 0,845 / 0,859 |
| Part snappée de ceux-ci | 1,000 (x3) | 1,000 (x3) | 0,940 / 0,897 / 0,887 | 0,968 / 0,968 / 0,972 |
| Décalage médian (voxels) | 2,06 / 1,86 / 1,78 | 2,12 / 1,98 / 1,91 | 2,89 / 2,79 / 2,01 | 2,65 / 2,79 / 2,17 |
| Décalage 90e percentile (voxels) | 5,07 / 4,81 / 4,85 | 4,90 / 4,82 / 4,71 | 7,33 / 6,00 / 5,47 | 7,75 / 7,31 / 6,09 |
| Aire rendue par enroulement | 8,62-8,85 cm² | ~13,6-14,0 cm² | 12,4-12,6 cm² | ~13,5-13,8 cm² |

- La perte baisse d'environ 96 % sur les quatre fits (README §What this shows, `#000.1`) ; les cases « loss at step 0 / 7,800 » du tableau sont vides dans le texte extrait.
- Pour 0846B, le fit laisse 11,2 % de ses 3 095 116 tracks (347 101) satisfaits et 54,4 % des points de tracks ; pas de chiffre équivalent pour les trois autres (`#002.0`).
- Cartes Reader V3 : sur les 24 cartes, blobs isolés ronds ou ovales de ~0,3 à 2 mm et quelques chaînes courtes, aucune rangée de formes de taille d'une lettre ; « Ink maps show a letter row ? no » pour les quatre rouleaux (`#000.2`, `#001.5`). Aucun texte n'est revendiqué.
- Écart avec l'extracteur publié (contrôle PHerc. 0358) : concordance des tracks verticaux (slab) de 67 à 78 %, mieux pour les rubans horizontaux (README §Measured limits, `#002.3`).

→ reportés dans `benchmarks.csv` (par l'agent principal, à partir du fichier du scratchpad) : 8 lignes, enroulement 070 de chaque rouleau, part snappée (1545 : 1,000 ; 1218 : 1,000 ; 1203 : 0,897 ; 0846B : 0,968) et décalage médian du snap en voxels (1,86 ; 1,98 ; 2,79 ; 2,79), `confidence: medium` (tableau aplati par PyMuPDF).

## Limites et critique

- Dépôt communautaire non relu, chiffres auto-déclarés, « personne en dehors des auteurs n'a lancé ces fichiers » (§Measured limits, `#002.4`).
- Un seul run (une graine, un sens, 8 000 pas), pas de comparaison à une reconstruction indépendante des mêmes enroulements ; les umbilics ne sont validés que par le fit lui-même. La part « snappée » mesure la cohérence interne avec les prédictions m7 et non l'exactitude géométrique ; aucune métrique de vérité terrain.
- Les enroulements sont jugés « sur du vrai papyrus » par un seul lecteur, à l'œil, à échelle réduite pour 0846B ; seule une partie des gros plans 20 µm a été examinée, aucun pour 0846B (§What the ink maps do and do not say, `#002.0`).
- Reader V3 : l'absence de lettres n'est pas une preuve d'absence d'encre ; les auteurs ignorent quel ordre de couches est le côté lecture, et les deux ordres ne coïncident pas (`#002.0`). Aucun taux de faux positifs n'est mesuré : c'est un constat descriptif sur la validation d'encre.
- Écart d'extracteur à 67-78 % sur les tracks verticaux : impact sur le fit inconnu (`#002.3`).
- Incohérences mineures : 0846B est dit « comparable à 1203 » puis 1203 « le plus faible des trois rouleaux Drobkov » (0846B n'est pas Drobkov) ; l'aire rendue de 1545 (~8,7 cm²) est nettement inférieure aux ~12,4-14 cm² des autres sans explication ; les lignes de perte du tableau sont vides ; l'avertissement de 1203 sur le nombre d'expandeurs d'enroulements n'a pas été testé.
- Les durées de fit incluent des tâches annexes (normales de 0846B) ; comparaison avec un fit local sur GPU 32 Go (RTX 5090) : déduit, non fait par les auteurs.

## Pertinence pour la thèse

Axe mesh-flattening (ajustement de spirale) : fournit des tracks de départ, un coût de calcul réel (~1-2 h CPU pour les tracks, ~1 h de GPU 4090 pour 8 000 pas, 16,5 Go) et un pipeline reproductible dans l'écosystème villa, utile à la chaîne visée du projet (prédiction de surface, ajustement de spirale, aplatissement, rendu, Reader V3). Axe validation-fp : résultat négatif honnête (blobs, pas de lettres) sur quatre rouleaux sans labels. Reste ouvert : validation indépendante des umbilics et du snap, vérité terrain, impact de l'écart d'extracteur, bandes autres que celles ajustées.

## Gaps identifiés

- Aucune métrique de vérité terrain de l'aplatissement ou du fit de spirale (cohérence interne seulement).
- Pas de protocole quantifié pour les cartes d'encre sans lettres (faux positifs, côté lecture inconnu).
- Impact de l'écart d'extracteur (67-78 % sur les tracks verticaux) sur la qualité du fit non évalué.
- Un seul run par rouleau, aucune répétition ni autre graine.

## Statut de lecture

papier complet (README.md et MANIFEST.md lus en entier). Extraction `pymupdf`, `ok: false`, aucune section détectée : le tableau « Results per scroll » est aplati, ses lignes de perte sont vides, les cellules sont à lire avec prudence (`confidence: medium`).
Ce qui suit est déduit et non affirmé par les auteurs : la comparaison avec un GPU local de 32 Go ; la lecture des incohérences ci-dessus ; la remarque que la part snappée n'est pas une mesure d'exactitude géométrique.
