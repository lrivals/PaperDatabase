---
id: 2016-seales-damage-discovery-virtual-unwrapping-reading
fiche: done
date: 2026-11-15
benchmarks: none
---

# From damage to discovery via virtual unwrapping: Reading the scroll from En-Gedi

W. Brent Seales, C. Seth Parker, Michael Segal, Emanuel Tov, Pnina Shor, Yosef Porath, 2016, Science Advances 2(9), e1601247. https://doi.org/10.1126/sciadv.1601247
Type : article de journal (Science Advances, revu par les pairs)

## Problème

Le rouleau d'En-Gedi (parchemin, ancien, carbonisé et écrasé en blocs de charbon qui se désagrègent au toucher) ne peut être ni déroulé ni manipulé : son texte à l'encre est inaccessible (Introduction). Les auteurs posent le verrou d'un pipeline complet, non invasif, qui part d'un volume 3D non structuré et aboutit à des images 2D lisibles dont chaque pixel reste vérifiable. Les approches antérieures traitent des matériaux non endommagés (Samko et al.) ou un texte gravé en métal qui offre une morphologie (Barfod et al.) (Discussion).

## Méthode

Cadre « virtual unwrapping » en trois étapes (Introduction ; Materials and Methods) :
- Scan micro-CT du rouleau (volume = repère de toutes les transformations).
- **Segmentation** : maillage triangulé construit par croissance de région. Tenseur de structure 3D (éq. 1) pour estimer la normale (éq. 2) ; chaîne de particules poussée par trois forces : « gravité » le long de l'axe du rouleau (éq. 3), ressorts entre voisins (éq. 4), saillance du tenseur (éq. 5). Paramètres : raideur 0,5, facteur a = 0,3, séparation initiale d'1 voxel (§Segmentation, Methods). Correction manuelle quand la chaîne franchit des couches. Environ 140 petites segmentations (§Merging).
- **Texturing** : valeur d'intensité par point du maillage, filtre de voisinage directionnel (ligne de 7 voxels le long de la normale, bidirectionnelle, filtre Max car l'encre est plus dense que le parchemin) (§Texturing, Fig. 6-7).
- **Flattening** : modèle physique masse-ressort (Bullet Physics, soft body, position-based dynamics) : bord épinglé, déroulage par gravité, plaquage sur un plan, relaxation (§Flattening).
- **Merging** : 140 segmentations fusionnées en maillage en 7 grandes surfaces, aplaties et texturées, puis fusion de textures en « master view ». Fusions faites à la main (MeshLab, Photoshop) (§Merging).
- **Chaîne de provenance** : chaque pixel du master view est remonté vers ses voxels d'origine (Fig. 8), pour permettre la vérification indépendante.

## Plateforme et implémentation

Pas de FPGA : fiche de méthode logicielle. Scanner : Bruker SkyScan 1176 in vivo micro-CT, tube microfocus PANalytical, caméra Princeton Instruments ; résolution maximale 9 µm, 18 µm utilisés pour tous les scans (§Volumetric scan ; chunk 2016-seales#014.4). Scan de calibration : 50 kV, 500 mA (sic), 350 ms, filtre 0,2 Al ; scan final : 4 champs décalés, 45 kV, 555 mA (sic), 230 ms ; reconstruction NRecon, TIFF 16 bits. Source laboratoire, pas de synchrotron. Matériel de calcul et temps : n/r. Code : non publié ; les scans et résultats sont archivés à l'Université du Kentucky (http://vis.uky.edu/virtual-unwrapping/engedi2016/, données sur demande pour le complément).

## Résultats

- Cinq spires complètes du rouleau restituées ; deux colonnes d'écriture hébraïque lisibles (Results, Fig. 9).
- Texte identifié comme le livre du Lévitique, plus ancien exemplaire pentateuchal trouvé dans une arche sainte (Results). Datation radiocarbone : IIIe ou IVe siècle de notre ère (table S1, hors du papier).
- Feuille de 35 lignes : 18 préservées, 17 reconstruites ; 33 à 34 lettres et espaces par ligne (Results).
- Master view : 18 µm/voxel isométrique, soit environ 1410 pixels par pouce ; surface déroulée environ 94 cm² ; lettres de 1,5 à 2 mm ; 16 bits (Methods, chunk 2016-seales#014.3). Les valeurs « 18 mm » du texte extrait sont des µm (µ perdu à l'extraction) ; cohérent avec 25 400 / 18 = 1411 ppi.
- Texte déchiffré identique au cadre consonantique du texte massorétique (Results).
- Aucune métrique d'évaluation quantitative : la qualité est jugée par consensus de l'équipe (« équivaut aux meilleures photos du XXIe siècle »).
→ reportés dans `benchmarks.csv` : aucune ligne (voir ci-dessous).

Aucune ligne de `benchmarks.csv` : le papier ne rapporte ni précision, ni débit, ni latence, ni ressources ; seuls des paramètres d'acquisition et un résultat textuel qualitatif existent, hors colonnes du schéma. D'où `benchmarks: none`.

## Limites et critique

- Évaluation qualitative uniquement : pas de vérité terrain, pas de métrique de segmentation ou d'aplatissement, pas de mesure de la distorsion (Discussion en reconnaît le besoin) ; les auteurs « tolèrent l'erreur géométrique » au profit de la lisibilité (Introduction).
- Pipeline très manuel : correction des chaînes, fusions à la main (MeshLab, Photoshop), paramètres réglés par essais et erreurs (§Segmentation, Methods) ; pas d'automatisation, temps de travail n/r.
- Lisibilité assistée par l'encre dense (métal supposé, fer ou plomb) ; la composition de l'encre reste inconnue (Introduction). Déduit : c'est un cas bien plus favorable que l'encre carbonée d'Herculanum, qui n'a pas ce contraste d'absorption.
- 17 lignes sur 35 sont reconstruites, non lues ; l'attribution « équivaut à la photo » n'est pas quantifiée.
- Pas de code publié, reproductibilité limitée aux données archivées.

## Pertinence pour la thèse

Travail fondateur de l'axe `virtual-unwrapping` : il fixe la décomposition segmentation, texturing, flattening, merging, ainsi que l'exigence de provenance (pixel vers voxel) qui prépare la validation de faux positifs. Pour Elder-scrolls : le tenseur de structure et la croissance de région sont des ancêtres des méthodes de suivi de surface ; l'aplatissement par masse-ressort précède SLIM/ARAP ; le texturing directionnel avec filtre Max est l'ancêtre des sous-volumes le long de la normale utilisés pour l'encre. Il laisse ouvert : encre carbonée sans contraste (Herculanum), résolution 8-9 µm (ici 18 µm), automatisation, mesure de distorsion.

## Gaps identifiés

- Aucune métrique publiée de qualité de segmentation ou d'aplatissement pour comparer les pipelines.
- Passage de l'encre métallique dense (En-Gedi) à l'encre carbonée d'Herculanum : le signal exploité diffère, non traité ici.
- Provenance pixel vers voxel : à relier aux exigences de validation à l'aveugle et de faux positifs.

## Statut de lecture

Papier complet (fulltext.md lu en entier). Extraction `pymupdf`, `extraction.ok` à `false`, aucune section détectée, µ perdu à l'extraction (« mm » pour µm, « mA » probablement µA) : texte potentiellement mal découpé, les figures et le complément (table S1) ne sont pas dans le texte.
Ce qui suit est déduit et non affirmé par les auteurs : la correction « 18 mm = 18 µm » et « mA = µA » ; le contraste avec l'encre carbonée d'Herculanum ; les filiations vers les méthodes actuelles (SLIM, ARAP, sous-volumes d'encre).
