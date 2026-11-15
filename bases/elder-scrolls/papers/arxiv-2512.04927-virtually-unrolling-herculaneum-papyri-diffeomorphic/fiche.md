---
id: arxiv-2512.04927-virtually-unrolling-herculaneum-papyri-diffeomorphic
fiche: done
date: 2026-11-15
---

# Virtually Unrolling the Herculaneum Papyri by Diffeomorphic Spiral Fitting

Paul Henderson (University of Glasgow), 2025, arXiv:2512.04927 (https://arxiv.org/abs/2512.04927). Venue : WACV 2026, DOI 10.1109/wacv61042.2026.00619 (d'après OpenAlex, communiqué par l'agent principal, non vérifié dans le texte ; le texte lu est la version arXiv). Type : conférence ; la version lue est le preprint arXiv.

## Problème

Dérouler virtuellement un rouleau d'Herculanum est un traçage manuel très long sur des scans de plusieurs gigavoxels. Les méthodes automatiques existantes sont ascendantes (heuristiques sans objectif défini, sorties fragmentées ou avec trous), échouent sur les zones brisées ou très compressées et n'ont aucune notion que le rouleau était une feuille unique enroulée (§1, §2). Les prédictions U-Net de surface actuelles ne donnent pas une surface propre dont on puisse « lire » un maillage : feuillets en contact, ruptures, fragments parasites (Fig. 2d, §1).

## Méthode

- Approche descendante, à modèle : une spirale d'Archimède extrudée (un seul paramètre ω, sens d'enroulement supposé connu) est déformée par un difféomorphisme T = T_aff ∘ T_flow ∘ T_gap (§5.1-5.2). T_aff : échelle et translation par tranche z ; T_flow : champ de vitesses 3D (grilles fine et grossière, interpolation trilinéaire, 16 pas d'Euler explicites ; scaling-and-squaring jugé instable) ; T_gap : champ d'échelle des écarts entre enroulements. La surface est garantie variété continue, sans intersection (§5.4).
- Entrées : prédictions nnU-Net v2 publiques (surface, fibres horizontales et verticales), entraînées sur une petite fraction de PHerc. Paris 4 (§4). Post-traitement : seuil à 50 %, composantes connexes (2D par tranche pour les surfaces), squelettisation, extraction itérée du plus long chemin, normales par Sobel, numéros d'enroulement relatifs par lancer de rayons et vote (§4). Le fitting ne charge aucun volume.
- Optimisation : Adam, lr 5e-4, 20 000 itérations ; pertes L_normal, L_radius, L_windings (robustes aux optima locaux, insensibles à la « phase » des feuillets), puis L_distance en seconde moitié, L_horizontal/L_vertical (orientation par fibres), régularisations L_stretch et L_center (§5.3). Pas de labels propres : s'appuie sur les prédictions existantes (labels manuels d'origine = n/r ici).
- Maillage : quadrangles échantillonnés sur la spirale puis transformés ; les coordonnées UV sont (θ, z) de l'espace canonique ; SLIM optionnel en post-traitement (§5.4).

## Plateforme et implémentation

- Scans : EduceLab-Scrolls, micro-CT synchrotron 54 keV, 7,91 µm/voxel (§3). PHerc. Paris 4 : 14376 × 7888 × 8096 voxels, région centrale évaluée 13600 × 4200 × 3600 (~30 enroulements) ; PHerc. 172 : 21000 × 6700 × 9100 (§3).
- Calcul : une RTX 3090 ; 19 h pour PHerc. Paris 4 dont 16 h de post-traitement des sorties nnU-Net et ~3 h de fitting (§6, Computational cost). Temps et matériel de PHerc. 172 : n/r.
- Code publié : https://github.com/pmh47/spiral-fitting (note de bas de page §6). Modèles et prédictions nnU-Net : https://dl.ash2txt.org/community-uploads/bruniss/scrolls/s1/ (note §4). Détails d'hyperparamètres dans le supplément (non lu).

## Résultats

Évaluation sur la région centrale de PHerc. Paris 4 contre un maillage manuel de référence (~30 enroulements, des centaines d'heures d'annotation, §3). Métriques (plus bas = mieux) : WJF, MRWD, ChD (chamfer unidirectionnel vérité terrain → prédiction), AD (défaut angulaire), Str (étirement) (§6).

| Variante | WJF % | MRWD | ChD | AD | Str |
|---|---|---|---|---|---|
| Ours (full) | 3,20 | 7,64 | 5,29 | 0,0568 | 1,239 |
| + SLIM | – | – | – | 0,0933 | 1,031 |
| sans normales | 3,08 | 8,41 | 5,75 | 0,0546 | 1,223 |
| sans n° d'enroulement relatifs | 2,77 | 25,67 | 7,72 | 0,0556 | 1,166 |
| sans perte de distance | 3,90 | 7,46 | 5,93 | 0,0535 | 1,172 |
| ThaumatoAnakalyptor | – | – | 5,59 | 0,1567 | 1,027 |

(Table 1, corps reconstruit par PyMuPDF : colonnes possiblement décalées ; les variantes « sans perte d'orientation des fibres » et « sans pertes de fibres » ne sont pas reprises ici.) Le modèle complet bat ThaumatoAnakalyptor en ChD et AD, étire un peu plus (Str), écart quasi comblé avec SLIM (§6). Table 2 (paramétrisation) : sans gap expander ChD 4,59 / WJF 3,59 % ; flow seul ChD 4,78 / WJF 3,43 % ; complet ChD 5,29 / WJF 3,20 %, la composition améliore surtout WJF (§6, Table 2 ; lecture des lignes ✓ ambiguë).
Qualitatif : PHerc. Paris 4 couverture bien supérieure à la vérité terrain (Fig. 6) ; ink TimeSformer pré-entraîné (modèle de [33]) appliqué à la surface déroulée révèle des lignes de lettres grecques (Fig. 4) ; PHerc. 172 : spirale couvrant presque tout le rayon et lettres visibles (Fig. 5), sans vérité terrain ni métrique.
→ reportés dans `benchmarks.csv` : 6 lignes (fichier de l'agent, confidence medium).

## Limites et critique

- Un seul rouleau (région de PHerc. Paris 4) et une seule comparaison automatique (ThaumatoAnakalyptor) ; PHerc. 172 seulement qualitatif. Pas d'évaluation sur rouleau tenu à l'écart au sens ML : les nnU-Net d'entrée ont été entraînés sur une fraction de PHerc. Paris 4 lui-même (§4), recouvrement avec la zone évaluée non précisé (déduit : risque de biais optimiste).
- Vérité terrain = maillage manuel partiel ; ChD unidirectionnel (VT → prédiction) ne pénalise pas une surface en excès, et la couverture supérieure n'est pas mesurée. Unités de ChD/MRWD non précisées (n/r).
- Pour ThaumatoAnakalyptor, seuls 3 métriques sont comparables ; la comparaison porte sur un maillage direct vs une spirale, avec AD et Str qui varient fortement selon l'étape SLIM.
- Limites des auteurs : pertes L1 contradictoires, la surface « erre » entre deux vrais enroulements ; hypothèse d'une feuille unique enroulée (pas de plis) (§7).
- 16 h sur 19 h vont au post-traitement ; la qualité reste tributaire des prédictions nnU-Net. L'absence de validation de la lisibilité (pas de métrique d'encre) : l'encre est seulement montrée qualitativement (Fig. 4, 5).

## Pertinence pour la thèse

Directement sur la chaîne visée de la base : ajustement de spirale global à partir de prédictions de surface/fibres, aplatissement avec distorsion bornée (SLIM, Str, AD), PHerc. Paris 4 (objectif du projet). Fournit un baseline publié avec code pour comparer des contraintes globales (nombre d'enroulement relatif, orientation par fibres) et une alternative aux méthodes locales. Laisse ouvert : zones écrasées/jonctions, robustesse à des prédictions plus contradictoires (Lp<1, lagrangien augmenté), validation à l'aveugle de la lecture.

## Gaps identifiés

- Évaluation sur plusieurs rouleaux avec vérité terrain indépendante des données d'entraînement des nnU-Net.
- Comparaison à d'autres pipelines automatiques et semi-automatiques (champs de nombre d'enroulement, Lasagna) sur les mêmes métriques.
- Lien entre qualité de surface (ChD, WJF) et qualité de l'encre détectée ; pas mesuré ici.
- Rouleaux repliés ou plusieurs feuilles : non traité.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction PyMuPDF, `extraction.ok` à false : tableaux reconstruits, équations dégradées, supplément et Table 1 à vérifier). Déduit et non affirmé par les auteurs : risque de recouvrement entre données d'entraînement nnU-Net et région évaluée ; asymétrie du ChD ; lecture des lignes de Table 2 ; venue WACV 2026/DOI repris des consignes (OpenAlex), non lus dans le papier.
