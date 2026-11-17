---
id: 2017-baum-revealing-hidden-text-rolled-folded
fiche: done
date: 2026-11-17
benchmarks: none
---

# Revealing hidden text in rolled and folded papyri

Daniel Baum, Norbert Lindow, Hans-Christian Hege, Verena Lepper, Tzulia Siopi, Frank Kutz, Kristin Mahlow, Heinz-Eberhard Mahnke, 2017, Applied Physics A 123:171. https://doi.org/10.1007/s00339-017-0808-6
Type : article de journal (Applied Physics A, revu par les pairs ; reçu 29/11/2016, accepté 24/01/2017)

## Problème

Des papyrus égyptiens roulés, pliés ou en petits paquets ne peuvent être ouverts sans dommage ; les auteurs veulent accéder au texte par tomographie et dépliage/déroulage virtuels (Abstract, §1). Difficultés propres au papyrus : deux couches de lanières orthogonales qui compliquent la distinction écriture/support pour les encres peu absorbantes, et séparation physique fréquente des deux couches (§1). Le cas des paquets pliés (plusieurs plis) n'avait pas été traité : les auteurs revendiquent un premier essai (Abstract, §6).

## Méthode

Deux approches, avec interaction manuelle (§3) :
- **Approche 1 (rouleau, ou pli unique en éventail)** : surface médiane définie par des contours polygonaux ouverts, dessinés à la main dans quelques coupes transversales, interpolés linéairement entre elles et extrapolés aux extrémités ; même nombre de points par contour, d'où un maillage quadrangulaire implicite N x M (N = K + 2) (§3, §4). Aplatissement puis rendu volumique du voisinage.
- **Approche 2 (plis multiples, ex. « magic fold »)** : dépliage itératif qui inverse chaque pli jusqu'à retomber sur une topologie de rouleau, puis Approche 1. Deux contours par coupe : axe médian du paquet (aplati en conservant les longueurs de segments) et contour extérieur (déformé le plus rigidement possible) ; Moving Least Squares (Schäfer et al.) pour la déformation d'image, avec recherche inverse des valeurs dans l'image précédente (§3).
- **Aplatissement à distorsion réduite** : placement initial dans le plan à partir des distances 3D, puis relaxation itérative de type masse-ressort (le déplacement d'un sommet = moyenne des vecteurs vers ses ~8 voisins, de longueur égale aux distances 3D) ; mouvement refusé s'il crée une intersection ou un quadrilatère concave ; arrêt sur seuil de distorsion moyenne ou nombre d'itérations (§4). LSCM cité comme alternative possible, non testée.

## Plateforme et implémentation

Pas de FPGA : méthode logicielle. Scanner : GE Phoenix Nanotom s (Museum für Naturkunde Berlin), micro-CT de laboratoire, anode W, 50 kV, 150 µA, 1440 projections, 1 s par projection ; filtre aluminium de 50 µm pour réduire l'intensité sous le seuil K du Fe (§2).
- Papyrus ancien (paquet ÄM 185/B L301, Ashmunein 1904/5, 3,7 x 3,7 cm, ~0,5 cm d'épaisseur) : voxel effectif 7,53 µm, 4 fractions de scan ; XRF portable (Niton XL3t) indiquant du Fe, donc possible encre ferro-gallique ; coupe tomographique avec taches blanches « possiblement dues au Fe » et une couche interne extraite montrant la structure des fibres (Fig. 1). Aucun texte lu.
- Maquettes : papyrus moderne écrit au cinabar (HgS) et au minium (Pb3O4) pour un contraste d'absorption maximal ; rouleau 9,17 µm en 2 fractions ; paquet plié en « magic fold » (§2, Fig. 2-3).
- Code : logiciel non nommé, non publié, aucun lien (déduit : pas de dépôt mentionné). Matériel de calcul : n/r. Matériel supplémentaire (vidéos, Figure S1) non fourni dans le texte.

## Résultats

Résultats qualitatifs et quelques temps de travail ; pas de métrique d'évaluation (§5).
- Rouleau maquette : 3 contours manuels d'environ 180 points, moins de 15 min de travail manuel et moins d'1 min de calcul pour le déroulage (§5, Fig. 4b). Seule une partie du rouleau est scannée.
- Paquet « magic fold » : 2 itérations de l'Approche 2 puis déroulage ; 3 à 5 contours d'environ 200 points par itération ; environ 35 contours de ~200 points pour le déroulage final ; 8 à 10 h de travail manuel au total (§5).
- Relaxation : 2000 itérations « usuellement suffisantes », quelques secondes pour l'exemple de la Fig. 6d ; la Fig. 6a montre de fortes distorsions réduites en 6b (visuel, non chiffré) (§4, §5).
- Dépliage complet d'un paquet plié selon deux plis perpendiculaires présenté comme une première (§6).
- Papyrus ancien : seule une coupe et une couche interne sont montrées ; la lecture de l'écriture n'est pas démontrée (Fig. 1).

Aucune ligne de `benchmarks.csv` : le papier ne rapporte ni précision, ni distorsion mesurée, ni vérité terrain ; seuls des temps de travail manuel et des paramètres d'acquisition existent, hors du schéma (colonnes orientées modèle/plateforme/précision). D'où `benchmarks: none`.

## Limites et critique

- Évaluation purement visuelle : la distorsion est définie (différence moyenne de distances voisines 2D/3D, §4) mais jamais rapportée ; pas de comparaison à une méthode existante.
- Démonstration sur maquettes à encre rouge très absorbante, volontairement séparée du problème de la détection d'encre ; le papyrus ancien scanné n'a livré aucun texte (Fig. 1). Déduit : le titre « Revealing hidden text » est donc surtout une promesse, pas un résultat sur document réel.
- Fort travail manuel (8-10 h pour un petit paquet), reconnu par les auteurs ; automatisation renvoyée à des travaux futurs (§6).
- Distorsions cumulées à chaque étape de dépliage (§4) ; l'effet sur la lisibilité de vraies lettres n'est pas testé.
- Pas de code publié ; pas de métrique pour comparer à En-Gedi ou aux travaux ultérieurs. Pas de paramétrisation globale (LSCM seulement évoquée).

## Pertinence pour la thèse

Axe `virtual-unwrapping` (et `mesh-flattening` pour l'aplatissement) : ancêtre manuel du pipeline segment, aplatissement, rendu ; la relaxation masse-ressort précède ARAP/SLIM/flatboi ; les contours interpolés entre coupes ressemblent aux annotations éparses suivies de propagation. Il pose aussi le cadre de dépliage de documents pliés, absent des rouleaux d'Herculanum (peu pertinent pour les rouleaux, utile pour les fragments pliés). Comme En-Gedi, il suppose un contraste d'encre (Hg, Pb, Fe) que l'encre carbonée d'Herculanum n'offre pas ; le papier cite pourtant la détection d'encre carbonée par contraste de phase (réf. 6, §1). Laisse ouvert : automatisation, mesure de distorsion, résolution 7-9 µm sur vrais papyrus.

## Gaps identifiés

- Aucune métrique publiée de distorsion d'aplatissement ni de comparaison entre méthodes de dépliage.
- Dépliage de documents à plis multiples : aucune automatisation ni validation sur document antique lisible.
- Lien entre contraste d'encre (XRF préalable pour trier les candidats) et choix de la modalité CT : à relier à l'axe ink-detection.

## Statut de lecture

Papier complet (fulltext.md lu en entier). Extraction `pymupdf`, `extraction.ok` à `false` : texte potentiellement mal découpé (résumé et affiliations en désordre, µ conservé, formules d'indices dégradées) ; figures et matériel supplémentaire absents du texte.
Ce qui suit est déduit et non affirmé par les auteurs : l'absence de lecture sur le papyrus ancien ; l'absence de code publié ; le contraste avec l'encre carbonée d'Herculanum ; les filiations vers ARAP/SLIM/flatboi.
