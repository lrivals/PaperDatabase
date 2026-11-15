---
id: 2026-seiler-model-carbonized-papyrus-scroll-opens
fiche: done
date: 2026-11-15
---

# A model carbonized papyrus scroll opens a novel path to identifying readable scrolls of the Herculaneum Library

Douglas Seiler, Jacob Michael LaManna, Michael McOsker, David Kreimer, Michael Cyrus Daugherty, Jens Dopke, 2026, PLoS ONE 21(9): e0353485. https://doi.org/10.1371/journal.pone.0353485
Type : article de journal (PLoS ONE, relu par les pairs ; reçu 14/03/2026, accepté 24/06/2026).

## Problème

En CT, l'encre carbonée n'a quasiment aucun contraste d'absorption avec le papyrus carbonisé, d'où un S/N très faible (§1). Les auteurs posent deux questions : (1) un ajout de plomb (agent de contraste X, détecté par XRF synchrotron dans deux fragments d'Herculanum, réf. [3]) rend-il l'encre lisible ? (2) comment obtenir des jeux de données à vérité terrain connue, sans risquer de rouleaux antiques, pour développer et scorer des algorithmes de lecture ?

## Méthode

Pas d'algorithme d'apprentissage : c'est un protocole de fabrication et de test. Rouleau modèle : papyrus égyptien moderne, encre au carbone (Platinum Carbon Ink, sans plomb par ICP-OES, <0,4 µg/g, §2.2), écrite au calame, avec ajout de nitrate de plomb à des concentrations calibrées (§2.3, §3.2) ; carbonisation en conteneur d'acier semi-scellé, faible oxygène (§2.4). Cible : 100 µg Pb par 2 µL, soit environ 100 µg/cm2, pour égaler la densité surfacique de Brun et al. (84 ± 5 µg/cm2) (§3.2). Entrées : radiographies 2D de fragments (flat-field, soustraction du noir) et tomographie 3D du rouleau ; labels : le texte écrit avant carbonisation (photo optique pré-carbonisation, Fig 6a). Reconstruction : code Python + Astra Toolbox ; déroulage par un programme maison (splines le long de la spirale, interpolation sur les normales) (§2.5). Dépistage XRF portable sur fragments plats (Bruker Tracer) et sur le rouleau (Olympus Innov-X DS-4000CC) (§2.6).

## Plateforme et implémentation

Scan : micro-CT de laboratoire (non synchrotron), NIST NeXT, tube à réflexion X-Ray Worx 225 kV, anode tungstène, utilisé à 30 kV et 1,3 mA (spectre calculé avec SpekPy, Fig 2d) ; détecteur : scintillateur Gd2O2S 20 µm + caméra ZWO ASI6200MM 62 Mpx + objectif Nikon 58 mm ; pixel effectif 18 µm, champ 172,4 x 114,9 mm (§2.5). 1001 projections sur 360 degrés, 5 s chacune (environ 83 min de pose, déduit). Source à 400 mm du rouleau, détecteur à 500 mm. Objet : un seul rouleau modèle, diamètre 40 mm, longueur 110 mm, tube phénolique central (Fig 2). Taille de voxel reconstruite : n/r (le pixel de 18 µm est celui du détecteur ; l'agrandissement est faible). Matériel de calcul et temps de reconstruction/déroulage : n/r. Code : reconstruction et déroulage « custom », non publiés (aucun lien). Données : https://doi.org/10.18434/mds2-4227 (Data availability statement) ; je n'ai pas vérifié ce qu'elles contiennent (volumes, projections ou photos).

## Résultats

- Radiographie 2D de fragments carbonisés : les deux lignes sans plomb sont invisibles ; les lignes à 200 µg/cm2 ont le meilleur contraste ; la plus faible concentration testée, 25 µg/cm2, reste détectable (§3.4, Fig 6, Conclusions). Aucun traitement algorithmique supplémentaire.
- Tomographie du rouleau modèle : le plomb est visible dès les projections brutes (Fig 7) ; après reconstruction et déroulage, le texte « the children of » se lit sans amélioration (§3.4, Fig 8c). Le rouleau n'est pas lisible en entier dans la figure rapportée (« possible to automate enhancement… with additional algorithms »).
- XRF portable Bruker sur fragments plats 4x4 cm (lettre de 1 cm) : signal fiable à 200, 100, 50 et 20 µg/cm2, décroissant avec la concentration ; témoin à 0 : aucun signal (§3.3). XRF Olympus sur le rouleau modèle : plomb détecté à plusieurs positions (§3.4, Fig 9).
- Encre sans plomb en 3D : non testée de façon rapportée ; les auteurs l'évoquent seulement comme perspective (« detection of lead-free ink through structural resolution », §3.4). Aucune métrique quantitative de lisibilité (CER, SNR, corrélation).
- Évaluation : pas de découpage train/test ; aucune donnée tenue à l'écart ; vérité terrain = texte connu écrit à la main avant carbonisation, comparaison visuelle uniquement.
→ reportés dans `benchmarks.csv` : 2 lignes (seuils de détection du plomb : radiographie 2D, §3.4 ; XRF portable, §3.3) ; fichiers bench transmis à l'agent principal.

## Limites et critique

- Preuve de concept qualitative : un seul rouleau, un seul extrait lisible (« the children of »), pas de métrique, pas d'évaluation à l'aveugle (pourtant proposée en §4 comme usage futur).
- Résolution et énergie très éloignées du synchrotron : tube à 30 kV et pixel de 18 µm, contre 7,91 à 9 µm et énergies bien plus élevées pour les scans d'Herculanum (comparaison déduite, non faite par les auteurs). Le contraste du plomb à 30 kV est exagéré par rapport à un scan haute énergie : extrapolation à la CT synchrotron non démontrée (les auteurs l'affirment comme hypothèse, §1).
- Représentativité : encre moderne colloïdale avec nitrate de plomb soluble ; le plomb antique (origine inconnue, peut-être siccatif, §3.2) a une chimie et une répartition différentes (pénétration dans la fibre ?). Teneur calibrée sur une seule référence (Brun et al., fragment le plus riche, 84 µg/cm2 ; l'autre est à 16 µg/cm2). Carbonisation de laboratoire dont la fidélité (température, déformation, délaminage) n'est pas validée quantitativement : seule une ressemblance visuelle et de densité est affirmée.
- XRF : testé sur fragments plats à lettre isolée ; sur le rouleau, détection qualitative seulement, sans seuil ni géométrie réelle d'un rouleau antique (rayon, épaisseur, plomb d'autres sources, blindage par les couches). Aucune évaluation de faux positifs/négatifs ; pas de dépistage d'un échantillon antique.
- Le cas difficile (encre carbone seule) est mentionné comme ligne de base mais aucun résultat n'est rapporté : l'apport pour les algorithmes d'encre sans contraste reste à démontrer.

## Pertinence pour la thèse

Pour Elder-scrolls, intérêt surtout méthodologique : (1) idée de rouleaux modèles à vérité terrain connue pour valider à l'aveugle et mesurer les faux positifs d'un détecteur d'encre (axe validation-fp), ce qui manque aux rouleaux réels ; (2) donnée utile pour la question de la résolution : on pourrait scanner un rouleau modèle à plusieurs résolutions (2,4 / 9 µm) pour tester la super-résolution sans risque d'hallucination non détectée ; (3) piste de présélection par XRF pour les 19 rouleaux éligibles. Limite : le scan est à 18 µm / 30 kV, sans encre carbone seule, donc ne se transpose pas directement aux données synchrotron du Vesuvius Challenge ; ne fournit pas de méthode de détection.

## Gaps identifiés

- Aucun rouleau modèle à encre carbone seule avec lecture 3D quantitative (SNR, CER) : le cas pertinent pour la majorité des rouleaux.
- Pas de scan multi-résolution ni synchrotron d'un rouleau modèle : transfert de domaine et super-résolution non testables avec ce jeu.
- Dépistage XRF d'un rouleau antique réel : seuils, géométrie, faux positifs non évalués.
- Fidélité de la carbonisation de laboratoire (déformations, empilement des couches) non validée contre les segmentations de rouleaux réels.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Extraction pymupdf (`extraction.ok` = false) : texte probablement complet mais les légendes de figures sont courtes et les figures (Fig 6 à 9) ne sont pas lisibles dans le texte ; aucun tableau de chiffres dans le papier. Déduit et non affirmé par les auteurs : la durée d'acquisition totale (1001 x 5 s), la comparaison de résolution et d'énergie avec les scans synchrotron, l'idée d'un scan multi-résolution et les usages pour la super-résolution et la validation à l'aveugle (cf. toutefois §4 pour la validation à l'aveugle). Le contenu du jeu de données déposé n'a pas été vérifié.
