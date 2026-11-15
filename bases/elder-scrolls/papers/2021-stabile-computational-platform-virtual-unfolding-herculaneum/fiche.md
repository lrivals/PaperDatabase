---
id: 2021-stabile-computational-platform-virtual-unfolding-herculaneum
fiche: done
date: 2026-11-15
benchmarks: none
---

# A computational platform for the virtual unfolding of Herculaneum Papyri

Sara Stabile, Francesca Palermo, Inna Bukreeva, Daniela Mele, Vincenzo Formoso, Roberto Bartolino, Alessia Cedola, 2021, Scientific Reports 11:1695. https://doi.org/10.1038/s41598-020-80458-z
Type : article de journal (relu par les pairs ; accès ouvert CC BY 4.0)

## Problème

Dérouler virtuellement des fragments de papyrus d'Herculanum très compacts (nombreuses couches collées, structure « convoluted and deformed at a small and large scale », Results, Fig. 3), en particulier la *scorza* (partie externe du rouleau, la plus endommagée). Les auteurs posent que la segmentation et l'aplatissement sont les verrous qui empêchent de dérouler de grandes portions (Abstract). Le contraste de l'encre carbonée, trop faible en micro-CT d'absorption, est discuté mais pas traité (Discussion).

## Méthode

Pipeline en cinq étapes (Fig. 2, Materials and methods) :

1. Acquisition : micro-CT de laboratoire (PHerc.110) ou tomographie à contraste de phase par propagation, XPCT (PHerc.1103).
2. Reconstruction : XPCT = récupération de phase de Paganin (TIE, hypothèse d'un matériau quasi homogène à δ/β constant) puis rétroprojection filtrée (STP, SYRMEP Tomo Project) ; micro-CT = FDK (NRecon, Bruker).
3. Extraction de surface **semi-manuelle** : seuillage global (Otsu, réf. 23) donnant un masque binaire, puis isolement d'un feuillet ; macros ImageJ et code Python maison. Les auteurs écrivent qu'une procédure automatique ne peut pas être appliquée (Discussion).
4. Maillage triangulaire : nuage de points, normales, reconstruction de Poisson « screened » (MeshLab).
5. Aplatissement par paramétrisation conforme, LSCM et ABF (implémentations de Blender), après des coupes **manuelles** du maillage aux endroits de distorsion maximale (bords, recouvrements) ; puis texturage (re-affectation des niveaux de gris).

Critère de validation du déroulage : les fibres. Un feuillet bien aplati doit montrer un motif croisé régulier (fibres horizontales au recto, verticales au verso, Discussion, Fig. 5b,d, Fig. 7).

## Plateforme et implémentation

- PHerc.110 (~4 × 4 cm², détaché d'un rouleau partiellement déroulé en 1867) : Bruker SkyScan 1172 (Univ. Bari), tube microfocus polychromatique, taille de pixel 12 × 12 µm², 60 kV, « 167 mA » (tel qu'écrit ; unité probablement fautive), exposition 2400 ms, filtre 0,5 Al, champ 50 × 50 mm², un seul scan (Materials and methods, X-ray microtomography).
- PHerc.1103 (3 × 5,5 cm², scorza) : ESRF ID17, XPCT par propagation, 80 keV (monochromateur Si(111)), distance échantillon-détecteur 10 m, pixel effectif 47 × 47 µm², champ ~1 mm (vertical) × 75 mm (horizontal), quatre scans verticaux (Materials and methods, XPCT).
- Matériel et temps de calcul : n/r.
- Code : « ad hoc computational programs developed by us and free software », « we provide an accessible algorithm that can be reproduced » (Discussion), mais aucun dépôt ni lien dans le texte : code non publié à notre connaissance.

## Résultats

Résultats qualitatifs seulement ; aucun tableau.

- ABF et LSCM donnent des résultats similaires sur PHerc.1103 : distorsions plus notables près des bords haut et bas sur les cartes (Fig. 5), les auteurs ne peuvent pas dire laquelle est meilleure.
- Sur PHerc.110, ABF est meilleur que LSCM : LSCM déforme davantage le bas de la carte (fibres courbées), ABF concentre ses distorsions en haut à gauche (Fig. 6).
- Les meilleurs feuillets aplatis des deux fragments montrent un motif croisé régulier, que les auteurs prennent comme preuve de justesse (Fig. 7).
- Les feuillets segmentés de PHerc.1103 ne sont pas montrés (Results). Aucune lettre ni texte n'est lu ; seules des lettres grecques visibles à l'œil nu sur PHerc.110 sont mentionnées (Fig. 1c).

→ reportés dans `benchmarks.csv` : aucune ligne. Le papier ne rapporte aucune valeur numérique de distorsion, de précision de segmentation ou de temps : les cartes de distorsion sont des figures à échelle de couleur, sans statistique (Fig. 5, 6). Rien à saisir sans estimer sur image, ce qui est interdit (`n/r`).

## Limites et critique

- Évaluation purement qualitative et visuelle : pas de métrique de distorsion (aire, angle, longueur) rapportée, pas de comparaison chiffrée LSCM/ABF, pas de vérité terrain de surface. Inférence : comparaison non reproductible chiffre à chiffre, et non comparable aux métriques du corpus (ChD, angular defect sur PHerc. Paris 4, arxiv-2512.04927).
- Critère « motif croisé de fibres » : nécessaire mais non suffisant (il valide l'orthogonalité locale, pas l'absence de distorsion d'échelle ; les méthodes conformes préservent les angles, donc ce critère est partiellement tautologique pour LSCM/ABF, déduit).
- Pipeline manuel : seuil global, sélection de feuillet et coupes du maillage faits à la main ; les auteurs reconnaissent l'absence de solution automatique. Ne passe pas à l'échelle d'un rouleau entier (fragments de ~4 cm seulement, quelques feuillets).
- Les coupes manuelles créent des discontinuités visibles (Discussion) ; compromis distorsion/coupes non quantifié.
- Un seul feuillet par fragment montré ; effectif de deux fragments, deux scanners, deux résolutions (12 µm lab vs 47 µm effectif XPCT) : les deux fragments ne sont donc pas comparables entre eux.
- Pas de détection d'encre : les auteurs disent que l'encre carbonée n'est pas détectable en micro-CT et qu'il faudrait de l'XPCT à plus haute résolution (Discussion). Le texte n'est pas lu.
- Pas de code ni de données publiés ; matériel de calcul n/r.
- Les auteurs notent eux-mêmes qu'il n'existe pas de méthode universelle et suggèrent de tester d'autres paramétrisations (modèle physique de matériau, réf. 9, Discussion). ARAP/SLIM, utilisés par le projet, ne sont pas testés.

## Pertinence pour la thèse

Pertinence pour Elder-scrolls (axes `mesh-flattening`, `surface-segmentation`, `virtual-unwrapping`, `ct-imaging`, `papyrology`) :

- Référence de base, antérieure au Vesuvius Challenge, de l'aplatissement conforme (LSCM, ABF) de feuillets de papyrus d'Herculanum, avec cartes de distorsion. Utile pour justifier le choix SLIM/flatboi : LSCM et ABF sont des points de comparaison documentés, et leur sensibilité à la géométrie (aucune méthode universelle) est un argument.
- Le test des fibres croisées (recto horizontal, verso vertical) est un contrôle de qualité simple et indépendant de l'encre, à rapprocher des champs de fibres de Lasagna.
- Confirme que le seuillage global et la segmentation manuelle ne tiennent pas dans les zones écrasées : motive les méthodes de segmentation automatiques du projet.
- Résolutions 12 µm (lab) et 47 µm effectifs (XPCT) : bien plus grossières que les 8–9 µm des scans du Challenge, donc peu de transfert quantitatif.
- Limite : aucun chiffre exploitable, aucune détection d'encre.

## Gaps identifiés

- Métrique quantitative de distorsion (aire/angle/longueur) comparant LSCM, ABF, ARAP, SLIM sur de vrais feuillets d'Herculanum : absente de ce papier.
- Critère de validation d'un aplatissement indépendant des méthodes conformes (le motif de fibres ne suffit pas).
- Automatisation de la coupe du maillage avant paramétrisation (ici manuelle).

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Avertissement d'extraction : backend `pymupdf`, `extraction.ok: false`, aucune section détectée ; l'équation (1) de phase retrieval est illisible dans le texte extrait ; les figures ne sont pas lues (légendes seulement), donc les observations sur les cartes de distorsion reprennent le texte des auteurs.
Ce qui suit est déduit et non affirmé par les auteurs : l'impossibilité de comparer leurs résultats aux métriques ChD/angular defect ; le caractère partiellement tautologique du critère des fibres pour des méthodes conformes ; l'absence de code publié (aucun lien dans le texte) ; l'unité « mA » probablement erronée.
