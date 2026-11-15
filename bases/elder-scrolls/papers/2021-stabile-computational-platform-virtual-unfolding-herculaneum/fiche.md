---
id: 2021-stabile-computational-platform-virtual-unfolding-herculaneum
fiche: done
date: 2026-11-15
benchmarks: none
---

# A computational platform for the virtual unfolding of Herculaneum Papyri

Sara Stabile, Francesca Palermo, Inna Bukreeva, Daniela Mele, Vincenzo Formoso, Roberto Bartolino, Alessia Cedola, 2021, Scientific Reports 11:1695. https://doi.org/10.1038/s41598-020-80458-z
Type : article de journal (Scientific Reports, accès libre CC BY 4.0)

## Problème

Dérouler virtuellement des fragments de papyrus carbonisés d'Herculanum (feuillets compressés, collés, très déformés) : segmentation d'une feuille isolée puis aplatissement posent problème et limitent la partie de papyrus qu'on peut dérouler (résumé, Introduction). Cas visé en priorité : la scorza, couche externe du rouleau, la plus abîmée mais porteuse d'informations (auteur, titre, longueur de l'œuvre). L'encre carbonée n'est pas détectée en micro-CT d'absorption ; la détection d'encre est discutée, pas traitée.

## Méthode

Pipeline en 5 étapes (Fig. 2) : acquisition et reconstruction tomographique, extraction de surface, maillage, aplatissement, texturation (Materials and methods).
- Reconstruction : XPCT par propagation (PBI) avec récupération de phase de Paganin (TIE, δ/β constant) puis rétroprojection filtrée (STP) ; micro-CT : FDK (NRecon), sans récupération de phase.
- Segmentation : semi-manuelle. Seuillage global (Otsu cité) puis masque binaire, repérage manuel du feuillet (ligne verte, Fig. 3a), valeurs de gris réassignées à la surface ; macros ImageJ et Python maison. Les auteurs jugent une procédure automatique impossible (Discussion).
- Maillage : nuage de points, normales, reconstruction de Poisson « screened » (MeshLab).
- Aplatissement : paramétrisation conforme, LSCM et ABF comparées (Blender). Coupes manuelles du maillage aux bords et aux zones de recouvrement avant paramétrisation (Discussion).
- Entrées : volumes tomographiques bruts. Pas de labels, pas d'apprentissage : aucun modèle entraîné.
- Critère de qualité : cartes de distorsion en aire (Fig. 5, 6) et motif de fibres en croisillon (fibres horizontales au recto, verticales au verso) après aplatissement.

## Plateforme et implémentation

- PHerc.1103 : fragment de scorza, 3 × 5,5 cm² ; XPCT synchrotron ESRF ID17 (Grenoble), 80 keV monochromatique (Si(111)), distance échantillon-détecteur 10 m, pixel effectif 47 × 47 µm², champ ~1 mm (vertical) × 75 mm (horizontal), 4 scans verticaux (Data acquisition).
- PHerc.110 : fragment ~4 × 4 cm², détaché d'un rouleau déroulé en 1867 ; micro-CT de laboratoire Bruker SkyScan 1172 (Université de Bari), tube polychromatique, 60 kV, 167 mA [sic], 2400 ms, filtre 0,5 Al, pixel 12 × 12 µm², un seul scan (Data acquisition).
- Matériel de calcul et temps de calcul : n/r.
- Code : « ad hoc computational programs developed by us and free software » ; les auteurs disent fournir « an accessible algorithm » mais aucun lien ni dépôt n'est donné (code non publié, d'après le texte). Données : n/r, aucun lien. Fragments conservés à l'Officina dei Papiri Ercolanesi, Bibliothèque nationale de Naples.

## Résultats

Résultats qualitatifs uniquement, sur deux fragments.
- PHerc.1103 : LSCM et ABF donnent des résultats similaires ; distorsions plus marquées aux bords haut et bas (Fig. 5). Les deux méthodes sont jugées satisfaisantes.
- PHerc.110 : distorsions inhomogènes ; LSCM plus déformée en bas (fibres courbées), ABF meilleure (fibres droites) (Fig. 6, Discussion).
- Feuillets aplatis à croisillon régulier de fibres, pris comme preuve de la justesse de l'aplatissement (Fig. 7).
- Aucune valeur chiffrée de distorsion (stretch, angle), de temps ou de taux de réussite n'est rapportée ; échelles de couleur seules.
- Évaluation : sur les mêmes deux fragments qui servent à développer la méthode ; aucune région ni aucun rouleau tenu à l'écart. Vérité terrain : aucune (critère visuel indirect : orthogonalité des fibres). Aucun texte ou encre n'est lu.
→ reportés dans `benchmarks.csv` : aucune ligne (pas de configuration chiffrée ; article non survey).

## Limites et critique

- Pas de métrique quantitative ni de baseline : la comparaison LSCM/ABF est visuelle sur deux échantillons.
- Segmentation semi-manuelle et coupes manuelles : non scalable, non reproductible en l'état (opérateur, seuil non donné) ; contraste avec les approches automatiques ultérieures sur de grands rouleaux (déduit).
- Le critère des fibres en croisillon est une validation indirecte : il atteste la conformité locale mais pas l'absence de distorsion d'échelle (LSCM/ABF sont conformes, pas isométriques ; les auteurs le reconnaissent). Les surfaces restent « uneven and irregular » ce qui complique la lecture.
- Résolutions modestes (47 µm effectif en XPCT, 12 µm en micro-CT), loin des 8-9 µm du Vesuvius Challenge (déduit) ; les auteurs disent que la détection d'encre fiable exigera une résolution XPCT supérieure.
- Fragments (3-5 cm) et non rouleaux entiers ; les cas de spirale enroulée, de jonctions ou de courbure serrée ne sont pas traités.
- Incohérences du texte extrait : la légende de la Fig. 7 parle de « XPCT » pour les deux feuillets alors que PHerc.110 est en micro-CT ; la numérotation des panneaux des Fig. 5/6 dans le texte diffère de celle des légendes ; 167 mA pour un tube de 60 kV paraît improbable (à vérifier, probablement µA).
- Pas de code ni de données publiés.

## Pertinence pour la thèse

Pertinence pour la chaîne Elder-scrolls (aplatissement, SLIM/flatboi) : référence historique d'un pipeline de déroulage de fragments d'Herculanum (axes virtual-unwrapping, mesh-flattening). Apport : comparaison LSCM vs ABF sur surfaces extraites, usage des cartes de distorsion en aire et des fibres croisées recto/verso comme contrôle de qualité de l'aplatissement, idée réutilisable pour valider un maillage aplati sans vérité terrain. Les auteurs suggèrent de tester aussi un modèle physique de matériau (MM, ref. 9 : Parker, Seales, Shor). Laisse ouvert : automatisation, mesure quantitative de la distorsion, passage aux rouleaux entiers, détection d'encre, lien avec la papyrologie (la scorza comme source d'informations).

## Gaps identifiés

- Aucune mesure quantitative de distorsion ni comparaison à ARAP/SLIM ou à la modélisation de matériau : à croiser avec les travaux d'aplatissement du Vesuvius Challenge.
- Segmentation automatique des feuillets compressés de fragments de scorza non traitée.
- Détection d'encre sur ces fragments non abordée (XPCT à plus haute résolution requise selon les auteurs).

## Statut de lecture

Papier complet (fulltext.md lu en entier). Attention : extraction `pymupdf` avec `ok: false`, aucune section détectée ; l'équation 1 (Paganin) est illisible dans le texte extrait, les figures ne sont pas lues (seulement leurs légendes et le texte).
Ce qui suit est déduit et non affirmé par les auteurs : le caractère non scalable de la segmentation, l'écart de résolution avec le Vesuvius Challenge, la comparaison aux méthodes ultérieures, l'incohérence probable de l'unité du courant (167 mA).
