---
id: 2026-betka-herculex-virtual-unwrapping-whole-herculaneum
fiche: done
date: 2026-11-17
---

# HerculeX: virtual unwrapping of whole Herculaneum scrolls on Apple silicon

Adam Betka, 2026, GitHub (commit eace0b23ac, 2026-11-17). https://github.com/adambetka2/HerculeX/tree/eace0b23ac4e9f95d10d185f08be743f0d0af961
Type : dépôt de code communautaire du Vesuvius Challenge (README + docs techniques convertis en PDF), non relu par les pairs ; tous les chiffres sont auto-déclarés par l'auteur (en-tête du document).

## Problème

Dérouler automatiquement des rouleaux d'Herculanum entiers à partir du seul scan CT brut, sans segmentation manuelle, maillages publiés ni prédictions de surface, puis lire l'encre, sur un ordinateur portable (README §Overview). Verrou visé : les méthodes qui font croître les surfaces de façon gloutonne accumulent des erreurs de enroulement ; l'auteur pose le déroulage comme un problème d'optimisation en nombres entiers (README, intro).

## Méthode

Pipeline en 6 étapes (README §Overview, chunk 2026-betka#000.2) : (1) lecture du scan OME-Zarr à ~19 µm/voxel (niveau 1 d'un scan 9,4 µm) par requêtes d'intervalle d'octets ; (2) nœuds de feuillet par cellule de 8 voxels : tenseur de structure (orientation) + pics du profil d'intensité le long de la normale, un nœud par feuillet traversé, un thread-group Metal par cellule (§How it works, Sheet nodes) ; (3) graphe : arêtes de feuillet si normales à moins de 30° ; rayons le long de la normale (premier feuillet rencontré = un tour plus loin) ; orientation des normales vers l'extérieur par une coupe minimale ; (4) niveaux d'enroulement entiers f par patch : min Σ w·ρ(f_b − f_a − k), ρ = valeur absolue ; LP dual d'un flot de coût minimal donc optimum entier, résolu par simplexe réseau en C avec certificat ; deux sens d'enroulement testés, 8 résolutions avec votes repondérés aléatoirement, pièces construites sur les arêtes conservées par les 8 (chunk 2026-betka#000.4) ; (5) pièces aplaties « isométriquement » en grille tifxyz au pas des nœuds, trous ≤ 3 cellules comblés par remplissage harmonique, pièce valide si ≥ 70 % des paires voisines à ±10 % du pas ; un cadre par scan, pièces jointes aux coutures par les arêtes de feuillet, placement par tour et angle (chunk 2026-betka#000.5) ; (6) 31 couches le long des normales, face écrite identifiée par la direction des fibres de la couche externe, encre par Reader v3 (fenêtre de 17 couches, tuiles 512 px, tige 3D en Metal, corps 2D sur Neural Engine en demi-précision), visionneuse web à pyramide de tuiles et outil d'étiquetage (spots) avec balayage en profondeur −15…+15 (spots/README).

## Plateforme et implémentation

Une seule machine : MacBook Pro M1 Pro, 10 cœurs, 16 Go (README §Results) ; pics mémoire 3 à 8 Go par étape ; ~40 Go de disque par rouleau + 25 Go de CT en transit, plusieurs centaines de Go de CT téléchargés par rouleau (§Get started). Logiciels : Python 3.11 (uv), C, Objective-C, kernels Metal, job board maison (GPU / Neural Engine / lien réseau partagés). Code publié sous licence MIT : https://github.com/adambetka2/HerculeX ; poids Reader v3 (Domenico Russo) téléchargés à une révision épinglée avec contrôle SHA-256 ; données de scan Vesuvius Challenge. Portage CUDA décrit comme tâche pour un agent de codage (non réalisé ; `portable_reader.py` lit déjà Reader v3 en PyTorch) (§Port to CUDA).

## Résultats

Mesures sur le MacBook Pro M1 Pro, 8 rouleaux sans maillage publié (README §Results) :
- Surface mise à plat : 69 290 cm² au total (PHerc0125 9 801 ; 0175B 10 824 ; 0191 11 775 ; 0358 8 507 ; 0813 8 849 ; 0826 5 720 ; 0846B 6 064 ; 1203 7 750), dont 39 428 cm² en mosaïques ≥ 4 cm² (chunk 001.1). La somme des colonnes retombe sur les totaux (mosaïques : 39 430 recalculé vs 39 428, arrondi).
- Durée : ~2 h de CT à feuillet posé pour un scan à 9,4 µm (README, intro, chunk 000.1). Les heures par rouleau du tableau (par ex. « 1,3¹ », « 1,7¹ ») sont illisibles après extraction (colonnes perdues) : n/r.
- Isométrie : 81 à 86 % des paires de points voisins à ±10 % du pas ; 96 à 99 % des pièces passent le contrôle (82 550 pièces) (§Results, Geometry, chunk 001.1).
- Contre maillages d'experts (crops de développement) : part correcte / part erronée = PHerc1667 0,716 / 0,046 ; PHerc0139 0,625 / 0,064 ; PHercParis4 0,747 / valeur tronquée dans le texte extrait (n/r) (chunk 001.2).
- Lettres atteintes par la surface : 91 % des nœuds du maillage publié de PHerc0343 First Letters ; signal d'encre conservé : 89 % vs maillage publié lu par le même modèle (chunk 001.2).
→ reportés dans `benchmarks.csv` : lignes à ajouter par l'agent principal depuis `scratchpad/bench/2026-betka-herculex-virtual-unwrapping-whole-herculaneum.csv` (8 lignes : surface totale, mosaïques ≥ 4 cm², isométrie, part correcte et part erronée PHerc1667, 91 % des nœuds, 89 % de signal d'encre, durée ~2 h).

## Limites et critique

- Dépôt non relu par les pairs, chiffres auto-déclarés, aucune comparaison à un autre pipeline (villa, Lasagna, méthodes des Progress Prizes) ni baseline de temps ; le « sans maillage publié » n'est pas mis à l'épreuve par un benchmark commun.
- Aveu de l'auteur (§Known limitations) : sur les 8 rouleaux déroulés, rien ne mesure si chaque pièce est sur le bon enroulement ; le cadre du scan ne tient pas toutes les jonctions entre coutures, une grande mosaïque peut joindre deux enroulements, l'ordre le long du rouleau est approximatif. Les 69 290 cm² sont donc une surface produite, pas une surface correcte.
- Les scores contre maillages d'experts viennent des contrôles de développement ; pas de jeu d'exclusion (« holdout ») pour la géométrie. Les seuils (70 % de paires à ±10 %) ont pu être réglés sur ces mêmes contrôles : risque de sur-ajustement (déduit).
- Part correcte 0,625 à 0,747 : un quart à plus d'un tiers de la surface n'est ni correcte ni identifiée comme erronée (déduit des deux colonnes ; définition exacte non donnée). « Isométrique » = 81-86 % à ±10 % : distorsion non bornée pour le reste, métrique non comparable à l'erreur d'aplatissement SLIM/ARAP des autres papiers de la base.
- Encre : Reader v3 utilisé sans réentraînement ; aucune métrique de lisibilité (lettres, CER, validation à l'aveugle) sur les 8 rouleaux ; « 89 % du signal d'encre conservé » est défini vaguement (métrique non précisée). Pas de test placebo ni de contrôle de faux positifs, alors que les cartes d'encre de rouleaux entiers sont montrées en violet.
- Le temps annoncé est difficile à comparer : le temps de 2 h exclut peut-être la détection de feuillets pour certains rouleaux (note ¹ du tableau) et le téléchargement de plusieurs centaines de Go de CT est requis (§Get started).
- Résolution : détection de feuillets à ~19 µm (scan 9,4 µm sous-échantillonné ×2), donc pas de test à 2,4 µm ni de super-résolution.

## Pertinence pour la thèse

Axe virtual-unwrapping, par une approche alternative aux champs d'enroulement et level sets : solution exacte et certifiée d'un problème L1 en entiers (flot de coût minimal), proche en esprit des « optimisations sur graphe » du profil. Utile à Elder-scrolls pour : (a) la comparaison de pipelines de segmentation sans maillages (zones écrasées, jonctions) ; (b) les métriques de contrôle sur rouleau synthétique à enroulement connu (`calibration/unwrap`) et le protocole « part correcte / part erronée » contre maillages d'experts ; (c) l'outil de spots et de balayage en profondeur (−15…+15) pour la validation d'encre, avec le cadre First Letters (10 lettres lisibles en 4 cm²) ; (d) la lecture de la face écrite par la direction des fibres. Laisse ouvert : la validité des enroulements sur rouleaux sans vérité terrain, la vérification de l'encre (axe validation-fp), le portage hors Apple silicon (CUDA/RTX 5090 non fait). Code ouvert et reproductible en principe sur Mac seulement.

## Gaps identifiés

- Aucune mesure d'exactitude d'enroulement sur rouleaux sans maillage publié ; pas de holdout géométrique.
- Pas de comparaison directe HerculeX vs pipeline villa / Lasagna sur les mêmes crops et mêmes métriques.
- Cartes d'encre de rouleaux entiers sans validation à l'aveugle ni test placebo.
- Pas de version CUDA publiée : reproduction sur la RTX 5090 à tenter.

## Statut de lecture

Papier complet (fulltext.md lu en entier ; README.md et 4 README de dossiers). Extraction : backend pymupdf, `extraction.ok: false`, aucune section détectée ; le tableau « Whole scrolls » est perdu en colonnes (colonne « Voxel size » vide, heures par rouleau incertaines), le texte de la ligne PHercParis4 est tronqué : valeurs concernées en n/r.
Ce qui suit est déduit et non affirmé par les auteurs : les risques de sur-ajustement des seuils, le quart à plus d'un tiers de surface ni correcte ni erronée, la non-comparabilité avec SLIM/ARAP, le fait que le temps de 2 h soit incomplet, et l'absence de comparaison à d'autres pipelines (absence constatée dans le texte, non commentée par l'auteur).
