---
id: 2004-seales-digital-restoration-volumetric-scanning
fiche: done
date: 2026-11-17
benchmarks: none
---

# Digital Restoration Using Volumetric Scanning

W. Brent Seales, Yun Lin, 2004, JCDL '04, Tucson, Arizona, USA, June 7-11, 2004. https://doi.org/10.1145/996350.996380
Type : article de conférence (JCDL '04, revu par les pairs selon la venue ; non vérifié ici)

## Problème

Objets endommagés et fragiles (livres aux pages collées, parchemins ou papyrus enroulés, rouleaux carbonisés par la lave) dont le texte est inaccessible : les conservateurs doivent choisir entre conserver sans analyser ou détruire pour lire (Abstract, Introduction). Les restaurations numériques antérieures supposent des pages planes (2D) ou de forme régulière, cylindrique (3D par scanner de surface) ; elles ne traitent pas les objets impénétrables aux acquisitions de surface (Introduction).

## Méthode

Trois étapes : scan volumétrique, segmentation, restauration par simulation physique (Introduction ; §2-3).
- **Acquisition** par tomographie X (CT) : 20 à 120 keV, contraste d'absorption entre pigment, papier et papyrus ; l'encre métallique (fer-gallique) est supposée bien répondre, contrairement aux encres carbonées (§2.1).
- **Segmentation** : seuillage empirique matière / vide, puis maillage texturé. Texture « multi-couches » : voxels pris le long de la normale 3D de chaque triangle, avec trois réglages (nombre de couches, distance entre couches, filtre : moyenne, moyenne pondérée, max/min) (§2.2).
- **Déroulage** : système masse-ressort (ressorts structurels et de cisaillement), équation de Newton intégrée par Euler, point milieu ou Runge-Kutta d'ordre 4 ; aplatissement par gravité et collision avec un plan (coefficient de restitution kr = 0,1 « empirique ») ; déroulage par dynamique contrainte : particules d'un bord bloquées (§3.1-3.2).
- Logiciel interactif : choix des particules contraintes, paramètres de simulation, vue 3D (§3.3, Fig. 2). Le processus est « top-down » avec intervention de l'utilisateur (§3).

## Plateforme et implémentation

Pas de FPGA : méthode logicielle. Scanners : CT médical du UK Medical Center (1-2 mm par voxel au mieux, bande de toile peinte à l'huile, Fig. 3) ; scanner sur mesure d'environ 12 µm par voxel (réplique de papyrus, Fig. 4) ; des scanners sur mesure atteignant 5 µm sont mentionnés (§2.1, §4). Source de laboratoire, énergie des scans réalisés : n/r. Matériel de calcul, temps, taille des volumes : n/r. Code : non publié.

## Résultats

Résultats qualitatifs uniquement (§4) :
- Bande de toile enroulée (pigment à l'huile) : pigment visible en points brillants dans une coupe CT, déroulage simulé en trois étapes, texture résultante obtenue sans toucher à la réplique (Fig. 3).
- Réplique de papyrus à environ 12 µm par voxel : fibres du papyrus et symboles visibles ; bande déroulée d'environ 2 pouces sur 11 pouces, superposée à la photo de contrôle, « alignement bon » (Fig. 4, §4). Comparaison visuelle seulement.
- Aucune ligne dans `benchmarks.csv` : le papier ne rapporte aucune métrique (précision, erreur de distorsion, temps) ; seuls des paramètres d'acquisition et des constats visuels existent. D'où `benchmarks: none`.

## Limites et critique

- Évaluation purement visuelle, sans métrique de distorsion ni de segmentation ; pas de vérité terrain chiffrée ; un seul exemplaire par expérience (toile, papyrus).
- Objets de test : répliques fabriquées (peinture à l'huile sur toile, papyrus peint), pas de rouleau ancien ; l'encre de la réplique répond au CT, ce que les auteurs supposent aussi pour l'iron-gall (§2.1, « we believe »). Déduit : cas très favorable, loin de l'encre carbonée d'Herculanum (les auteurs notent d'ailleurs que les encres carbonées sont d'une autre nature).
- Segmentation par seuillage empirique et étape guidée par l'utilisateur : pas d'automatisation, robustesse aux spires serrées ou collées non traitée (la limite de résolution entre couches est seulement évoquée, §2.1).
- Mention de simulations préalables [22] pour mesurer la distorsion et la résolution ; non détaillées ici.
- Pas de code ni de données publiés.

## Pertinence pour la thèse

Papier fondateur de l'axe `virtual-unwrapping` (premier jalon de Seales et al., avant En-Gedi 2016) : il pose la chaîne scan, segmentation, texture le long de la normale, déroulage physique. Pour Elder-scrolls : le texturing par couches le long de la normale est l'ancêtre des sous-volumes de surface utilisés pour la détection d'encre ; l'aplatissement masse-ressort précède SLIM/ARAP. Il laisse ouverts : l'encre carbonée sans contraste, l'échelle réelle (volumes de milliers de voxels de côté), l'automatisation de la segmentation et la mesure de distorsion.

## Gaps identifiés

- Aucune métrique de qualité d'aplatissement ou de distorsion dans ce papier : à comparer avec les méthodes ultérieures (SLIM, ARAP).
- Encre carbonée : le signal exploité (absorption de pigment métallique) ne s'applique pas à Herculanum.
- Interaction manuelle pour la segmentation : pas de stratégie pour les zones écrasées.

## Statut de lecture

Papier complet (fulltext.md lu en entier). Extraction `pymupdf`, `extraction.ok` à `false`, aucune section détectée ; ligatures partiellement réparées (« classi cation »…) ; texte potentiellement mal découpé, figures non lues (légendes seules).
Déduit et non affirmé par les auteurs : le contraste avec l'encre carbonée d'Herculanum ; les filiations vers SLIM/ARAP et les sous-volumes d'encre ; le caractère « réplique » défavorable à la généralisation.
