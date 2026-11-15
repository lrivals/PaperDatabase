---
id: 2015-barfod-revealing-text-complexly-rolled-silver
fiche: done
date: 2026-11-15
benchmarks: none
---

# Revealing text in a complexly rolled silver scroll from Jerash with computed tomography and advanced imaging software

Gry H. Barfod, John Møller Larsen, Achim Lichtenberger, Rubina Raja, 2015, Scientific Reports. https://doi.org/10.1038/srep17765
Type : article de journal (Sci. Rep., publié le 09/12/2015)

## Problème

Les amulettes en feuille de métal (plomb, argent, or) étaient roulées ou pliées et ne peuvent
être dépliées mécaniquement sans les détruire ; les auteurs cherchent à lire une feuille
d'argent de Jerash (Jordanie, avant 749 CE), pliée de façon irrégulière et déformée, avec 17
lignes gravées (p. 1-2). La technique antérieure de dépliage virtuel (rouleau mandéen en
plomb, polylignes dans VGStudio MAX) suppose un rouleau régulier et non déformé (p. 2).

## Méthode

Pas d'apprentissage : flux interactif manuel.
- Entrée : volume CT de la feuille (1 600 projections sur 360°) (§Methods).
- Segmentation manuelle : chaque ligne de texte est définie comme une « région d'intérêt »
  (ROI) avec l'outil de dessin 3D de VGStudio MAX 3 Beta ; les zones où deux feuilles se
  touchent demandent un travail long et laissent des « rayures » dues à l'outil (§Results).
- Les lignes sont vues isolément, recto et verso ; le verso (texte gravé en relief) est le plus
  lisible, l'image est à inverser en miroir (§Results).
- Dépliage par polylignes en complément, pour les lignes sur un pli : p. ex. ligne 9, 30
  polylignes d'environ 6 mm de 30 points (Fig. 7). Les polylignes ne sont pas calculées
  automatiquement : l'utilisateur les place.
- Labels / vérité terrain : aucun ; pas de lecture de référence (le texte est présumé
  pseudo-arabe, non lisible).
- Analyses de composition complémentaires (microsonde EMP, LA-ICPMS) sur fragments : sans lien
  avec l'imagerie 3D.

## Plateforme et implémentation

- Objet : feuille d'argent roulée (env. 0,15 mm d'épaisseur, 42 mm de long, 8 mm de diamètre,
  9,5 cm déroulée) dans un étui en plomb (1 mm, 50 mm, 17 mm de diamètre) (§Results).
- Scan : laboratoire (industriel), pas synchrotron. Phoenix GE v|tome|x M, tube microfocus
  300 kV, détecteur 2k ; 270 kV, 87 µA ; grossissement env. 8,5x ; voxel env. 23 µm ; réalisé
  par Vohtec (Garching) en février 2015 (§Methods).
- Calcul : volume d'environ 4 Go, analysable sur PC ou portable ordinaire ; les nombreuses
  polylignes ralentissent le système (§Discussion). Temps de travail : « très long », non
  chiffré (n/r).
- Logiciel : VGStudio MAX 3 Beta (Volume Graphics, Heidelberg), propriétaire, version bêta.
- Code et données : non publiés (aucun lien).

## Résultats

- Les 17 lignes sont segmentées et visualisées (Fig. 5-6) ; la résolution de 23 µm est jugée
  « plus qu'adéquate » (§Discussion). Résultat qualitatif : l'écriture est visible mais le
  texte est présumé pseudo-arabe plus des signes magiques (charaktêres), sans lecture
  possible (§Reading).
- Lettres : le signe en N de la ligne 6 mesure env. 3 x 5 mm (§Results).
- Aucune métrique (précision, erreur, comparaison à une lecture de référence) n'est rapportée.
- → reportés dans `benchmarks.csv` : aucune ligne (résultats uniquement qualitatifs et
  analyses de composition sans rapport avec une tâche évaluée ; `benchmarks: none`).

## Limites et critique

- Aucune évaluation quantitative ni validation : pas de donnée tenue à l'écart, pas de
  seconde lecture, pas de comparaison à une segmentation de référence ; un seul objet.
- Segmentation entièrement manuelle (outil de dessin 3D), très longue aux contacts entre
  feuilles ; pas de reproductibilité chiffrée ; outil propriétaire en version bêta.
- Les « rayures » dues à l'outil montrent un risque d'artefacts introduits par l'opérateur ;
  non quantifié.
- Cas favorable au contraste : métal gravé dans un matériau dense, donc fort contraste CT ;
  non transposable tel quel à une encre carbonée sans contraste sur papyrus (déduit ; les
  auteurs disent eux-mêmes que le cas n'est pas comparable, §intro).
- Le texte reste illisible : la méthode produit des images, pas une lecture validée.

## Pertinence pour la thèse

Travail précurseur, hors cœur du thème : il illustre le dépliage virtuel d'un objet enroulé
et déformé par segmentation volumique + dépliage local par polylignes, et cite le travail
sur les papyrus d'Herculanum (réf. 7-8) comme cas différent (§intro). Utile comme repère
historique pour l'axe virtual-unwrapping (segmentation surface par surface, avantage du verso
en relief, éclairage virtuel), et comme contre-exemple de ce que le projet cherche à
automatiser (segmentation manuelle contre prédiction de surface par apprentissage). Ne
contribue ni à la détection d'encre ni à la validation de lettres.

## Gaps identifiés

- Pas de segmentation automatique des feuilles en contact (ici manuelle) : renvoie à l'axe
  surface-segmentation.
- Aucune méthode de validation d'une lecture sur objet enroulé (pseudo-script non vérifiable).
- Pas de mesure de distorsion du dépliage par polylignes.

## Statut de lecture

papier complet (`fulltext.md` lu en entier). Extraction `pymupdf`, `extraction.ok` à `false`,
aucune section détectée : les Tableaux 1-2 (composition) sont partiellement illisibles ;
sans impact sur la fiche. Figures non consultées (texte seul).
Ce qui suit est déduit et non affirmé par les auteurs : le caractère favorable du contraste
métal/air, l'absence de transposabilité aux encres carbonées, le risque d'artefacts liés à
l'opérateur, la lecture comme contre-exemple de l'automatisation.
