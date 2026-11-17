---
id: 2012-mills-apocalypto-revealing-unreadable
fiche: done
date: 2026-11-17
benchmarks: none
---

# Apocalypto: Revealing the unreadable

David Mills, Oksana Samko, Paul Rosin, Kate Thomas, Tim Wess, Graham Davis, 2012, Proc. SPIE 8506 (Developments in X-Ray Tomography VIII), 85060A. https://doi.org/10.1117/12.928917
Type : article de conférence (actes SPIE) ; court, présentation de projet, la description complète du déroulage est renvoyée à un article à venir (§2).

## Problème

Des documents sur parchemin ou papier dégradés (rouleaux, parchemins pliés dont les couches ont adhéré) ne peuvent être lus ni manipulés sans dommage permanent (Abstract, §1). L'encre ferro-gallique, cause majeure de dégradation, fournit aussi le contraste aux rayons X, mais en très faible quantité : il faut un scanner à très haut rapport de contraste et sans artefacts (Abstract).

## Méthode

- Scan XMT (micro-CT) avec le scanner TDI (time-delay integration) en développement à Queen Mary, qui supprime les artefacts en anneau et élargit le champ au-delà du capteur CCD ; bruit comparable au synchrotron, plus lent (§1).
- Post-traitement en six étapes : débruitage, segmentation, construction de surface, aplatissement, projection des données, génération d'image (Abstract). Seules ces étapes sont nommées ; leurs algorithmes ne sont pas décrits (§2 : « forthcoming paper »).
- Cas d'étude : rouleau du Norfolk Record Office (100 x 10 mm, encre ferro-gallique, parchemin vers 1850, très serré et déshydraté, feuille métallique sur un bord, inclusions à haut Z) (§2). Segmentation par « combinaison de méthodes automatiques et d'intervention manuelle » ; environ une semaine de traitement par l'équipe de Cardiff (§2).
- Vérification : le rouleau est ensuite déroulé physiquement (humidification, aplatissement) pour confirmer le texte (§2, Fig. 4).
- Étude de dommages : diffraction X, FTIR (ACP) et analyses biochimiques, sans altération détectable du collagène ; résultats préliminaires, à publier (§3).

## Plateforme et implémentation

Pas de FPGA. Scanner : XMT TDI (MuCAT2 utilisé ; MuCAT3 à géométrie équiangulaire en cours) de Queen Mary, source laboratoire, pas de synchrotron ; énergie et tension du tube : n/r. Scan : 36 h, 7707 projections, voxel de 15 µm ; reconstruction rétroprojection filtrée cône-faisceau sur GPU (§2). Matériel de calcul de la segmentation : n/r. Visualisation : TomView, Drishti. Code : non publié ; données : n/r.

## Résultats

- Encre détectée sur le rouleau, artefacts de la feuille métallique minimes (§2, Fig. 2).
- Image déroulée virtuellement lisible (Fig. 3), puis texte confirmé par le déroulage physique, sans connaissance préalable du contenu (§2, Fig. 4). Texte lu : n/r dans le papier (figures non lisibles dans l'extraction).
- Pas de dommage détectable sur parchemin ancien ou moderne scanné, selon des études non encore publiées ; assombrissement visible seulement sur un échantillon saturé d'eau après 6 h de scan (§3, Abstract).
- Aucune ligne de `benchmarks.csv` : le papier ne rapporte aucune métrique d'évaluation (précision, erreur, débit) ; seuls des paramètres d'acquisition et des résultats qualitatifs existent. D'où `benchmarks: none`.

## Limites et critique

- Papier de présentation : pas de métrique, pas de description des algorithmes de segmentation ni d'aplatissement, pas d'évaluation de la distorsion ; renvoi à un article ultérieur (§2).
- Un seul rouleau, petit et récent (vers 1850), à encre ferro-gallique de bon contraste : cas bien plus favorable que l'encre carbonée d'Herculanum (déduit).
- Segmentation partiellement manuelle, une semaine de travail pour un petit rouleau ; passage à l'échelle non traité.
- Validation par déroulage physique : possible ici, impossible pour les rouleaux d'Herculanum (déduit).
- Étude de dommages préliminaire et non publiée dans le papier ; l'innocuité n'est pas démontrée ici.
- Scan de plus d'une journée (36 h) : coût d'acquisition élevé.

## Pertinence pour la thèse

Précurseur du déroulage virtuel par micro-CT de laboratoire (avant Seales 2016) : même chaîne segmentation, aplatissement, projection, avec validation par vérité terrain physique. Pour Elder-scrolls : illustre le signal d'encre par absorption (métallique), absent d'Herculanum où l'encre est carbonée ; confirme que la segmentation est l'étape dure (surfaces en contact) ; l'argument de non-dommage des rayons X est utile côté papyrologie/conservation. Peu exploitable quantitativement.

## Gaps identifiés

- Aucune métrique publiée de segmentation ou de déroulage pour comparer les pipelines (ici absente).
- Transfert du contraste d'une encre ferrique à une encre carbonée : non traité.
- Validation par déroulage physique non transposable aux rouleaux fermés.

## Statut de lecture

Papier complet (fulltext.md lu en entier). Extraction `pymupdf`, `extraction.ok` à `false` : figures non lisibles, un fragment de texte OCR illisible (Fig. 4), ligatures partiellement réparées ; aucun tableau.
Déduit et non affirmé par les auteurs : le contraste avec l'encre carbonée d'Herculanum, l'impossibilité d'une validation physique sur Herculanum, le caractère précurseur vis-à-vis de Seales 2016.
