---
id: arxiv-2308.07070-local-iterative-extraction-2d-manifolds
fiche: done
date: 2026-11-15
---

# A Local Iterative Approach for the Extraction of 2D Manifolds from Strongly Curved and Folded Thin-Layer Structures

Nicolas Klenert, Verena Lepper, Daniel Baum, 2023, arXiv preprint (arXiv:2308.07070) ; publié dans IEEE TVCG 2023 selon OpenAlex (non vérifié dans le texte lu, qui porte le gabarit « TVCG 201x »). https://arxiv.org/abs/2308.07070
Type : preprint non relu par les pairs (version arXiv lue) ; DOI de l'article publié : n/r.

## Problème

Extraire en 3D une variété 2D ouverte et orientable qui approxime un document fin (papyrus, parchemin, papier, feuilles d'argent ou de plomb) fortement courbé ou plié, à partir de scans µCT bruités avec couches serrées, ruptures, séparation/fusion de couches (Abstract, §1). Les méthodes de crêtes fondées sur la Hessienne sont sensibles au bruit ; la méthode d'Algarni et Sundaramoorthi [1], globale, « prend des raccourcis » vers la couche voisine dans les structures repliées sur elles-mêmes (§6). Besoin : un surface garantie orientable pour pouvoir ensuite déplier virtuellement.

## Méthode

Algorithme (§3) : champ de probabilité p dérivé du volume par écrêtage linéaire dans un intervalle choisi par l'utilisateur (§3.1). Pour chaque graine s : fast marching dans p avec coût c = (1-p)/p, arrêt à une distance maximale d définie par l'utilisateur (règle : 5 à 10 fois l'épaisseur de la couche, §4) ; isosurface du champ de temps ; étiquetage de cette isosurface en deux régions séparées par une crête 1D, via deux pôles placés le long du vecteur propre dominant du tenseur de structure, puis remplissage (flooding) selon la distance (§3.5) ; propagation des deux étiquettes à l'intérieur de la région marchée ; la surface est l'interface entre les deux étiquettes. Fusion des patchs par champs d'étiquettes avec temps d'arrivée minimal (§3.6) et graphe de voisinage des graines pour éviter les surfaces parasites (§3.7) ; marching cubes modifié. Seule une graine initiale est requise : placement automatique itératif des graines suivantes (à 10 % de la distance de marche du bord, à 30-50 % des graines existantes, §4) ; interaction manuelle possible (ajout/suppression de graines). Entrée : volume scalaire ; pas de labels appris ; aucune partie apprise (méthode classique). Garantie : variété 2D orientable (§1, §3.6) ; hypothèse : le document est orientable et intersecte complètement l'isosurface (§3.5).

## Plateforme et implémentation

Données : µCT de laboratoire, résolutions µm/voxel n/r. Feuille d'argent pliée de 2000 ans (musée de Kalkriese), volume 375×271×614 ; papyrus grec plié deux fois en directions orthogonales (Louvre, [26]), volume 454×107×374 (§5.2). Pas de rouleau enroulé ; pas de scan synchrotron mentionné ; énergie n/r. Matériel : Intel Core i9-10980XE, RTX 3090 24 Go, 128 Go RAM (§5) ; l'usage du GPU par la méthode n'est pas précisé. Code : non publié (aucun lien dans le texte lu) ; seules les données synthétiques « Plane » et le tableur d'analyse sont publiés sur figshare (https://doi.org/10.6084/m9.figshare.23600115, CC BY 4.0, Supplemental Materials). Évaluation : synthétique (vérité terrain connue) et réel (aucune vérité terrain, §5).

## Résultats

- Synthétique « Plane » : 7 variantes (bruit gaussien 10 %, bruit simplex 30 %/50 %, déformation) ; la méthode donne toujours une surface topologiquement équivalente à un plan, Schultz et al. [35] produit soupe de triangles et trous (Fig. 4). À faible bruit, elle est moins précise que [35] (pas de précision sous-voxel) ; plus précise avec fort bruit ou déformation ; analyse quantitative dans le Supplementary Material (non fourni), non lue (§5.1.1).
- Feuille pliée simple : surface sans trou, un seul patch ; [9] et [35] laissent trous et patchs parasites (Fig. 5).
- Dragon de Stanford (grille 841×599×388) : 820 graines automatiques en plus d'une graine manuelle, sans artefact, contrairement à [35] (§5.1.3, Fig. 6).
- Feuille d'argent : [35] donne une surface non orientable ; la méthode reconstruit trois pièces, une entièrement automatique, deux semi-automatiques (Fig. 7, Fig. 1).
- Papyrus doublement plié : surface orientable réussie ; [9] échoue à produire une surface connexe, [35] mélange les couches (Fig. 9). Calcul à partir de l'ensemble des graines : 3 minutes (§5.2). Prétraitement manuel : valeurs mises à 0 là où le document est trop proche de lui-même, appliqué à toutes les méthodes (§5.2.2).
- Vitesse : 0,2 s environ pour ajouter une graine et mettre à jour la surface (§6) ; patch de la méthode [1] amélioré de plus de 15 minutes à quelques secondes sur la feuille d'argent (§5).
→ reportés dans `benchmarks.csv` : 2 lignes (temps papyrus ; temps par graine). Aucune métrique de précision de surface rapportée dans le texte principal.

## Limites et critique

- Évaluation surtout qualitative et visuelle sur les cas réels ; pas de vérité terrain réelle ; tableaux quantitatifs relégués au Supplementary Material.
- Comparaisons : Schultz et al. [35] avec paramètre de force réglé à la main (150 à 12 000) ; [9] non quantifiable ; [1] non inclus dans la comparaison quantitative (§5).
- Préparation manuelle des données papyrus (zones mises à 0) : la robustesse « sans contraintes » est relativisée.
- Pas de précision sous-voxel ; surfaces parfois trop étendues aux bords ; incapable de produire des surfaces non orientables ; échec attendu pour structures tangentiellement connectées (§6, §7).
- Goulot mémoire : champs de temps et d'étiquettes volumineux (§7). Volumes testés petits (≈ 10^7 à 10^8 voxels) comparés à un scan de rouleau d'Herculanum (déduit, non testé).
- Pas de code publié (reproductibilité limitée).

## Pertinence pour la thèse

Pertinente pour l'axe surface-segmentation et le déroulage : méthode classique sans apprentissage, garantie d'orientabilité, interactive (graines), qui traite des couches serrées et repliées, analogue aux zones écrasées et kolleseis des rouleaux (déduit). Utilisable comme contrainte de topologie ou étape de reconstruction après une carte de probabilité de feuillets (ex. sortie d'un U-Net 3D) ; le champ p est justement une probabilité (déduit, non essayé par les auteurs). Laisse ouvert : passage à l'échelle d'un rouleau complet, usage sur des scans synchrotron 8-9 µm, comparaison quantitative avec les approches Vesuvius.

## Gaps identifiés

- Aucune évaluation sur rouleau enroulé ni sur scan synchrotron ; pas de métrique quantitative sur données réelles.
- Couplage d'une carte de probabilité apprise (nnU-Net, U-Net 3D) avec une extraction à garantie topologique : non testé.
- Surfaces non orientables et structures tangentiellement connectées : non traitées.

## Statut de lecture

Papier complet (fulltext.md lu en entier). Extraction : backend pymupdf, `extraction.ok` false : les sections numérotées 2, 3, 4 n'ont pas été détectées (leur texte est rattaché à la section précédente) ; le texte est cependant présent et lisible. Supplementary Material (Sect. S1 à S4, analyse quantitative) non disponible dans le texte : non lu.
Déduit et non affirmé par les auteurs : analogie avec les kolleseis, usage avec une carte de probabilité apprise, comparaison d'échelle avec les rouleaux d'Herculanum, venue IEEE TVCG (OpenAlex).
