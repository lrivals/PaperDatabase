---
id: 2015-allegra-virtual-unrolling-x-ray-computed
fiche: done
date: 2026-11-17
benchmarks: none
---

# Virtual unrolling using X-ray computed tomography

D. Allegra, E. Ciliberto, P. Ciliberto, F.L.M. Milotta, G. Petrillo, F. Stanco, C. Trombatore, 2015, 2015 23rd European Signal Processing Conference (EUSIPCO). https://doi.org/10.1109/eusipco.2015.7362908
Type : article de conférence (EUSIPCO, revu par les pairs)

## Problème

Lire un rouleau de papyrus sans le dérouler physiquement, geste invasif qui risque de détruire un objet fragile (Introduction) ; le déroulage « Oslo » des années 1980 sur deux rouleaux d'Herculanum en a détruit une partie (§2). Verrou posé par les auteurs : avec un scanner CT médical de faible résolution (1 à 2 pixels par épaisseur de feuillet), les spires se touchent ou s'interrompent, et le logiciel du scanner produit un déroulage approximatif avec des parties manquantes (Introduction ; §3, Fig. 1).

## Méthode

Méthode semi-automatique en 2D par morphologie mathématique, en trois étapes (§4, Fig. 4) :
- **Sélection d'une bonne coupe** (§4.1) : gamma γ = 2 et étirement de contraste, seuillage d'Otsu, squelettisation, détection des points de branchement (recouvrements de feuillets). Score = distance euclidienne au point (0, A), où A est le nombre moyen normalisé de points du squelette : peu de branchements, nombre de points proche de la moyenne.
- **Reconstruction de la spirale de cette coupe** (§4.2) : branchements supprimés (voisinage 3 × 3), détection des extrémités, point de départ et d'arrivée donnés par l'opérateur (seule étape manuelle). Aux ruptures, le pixel d'intensité maximale du voisinage 3 × 3 est choisi, pondéré par 8 masques directionnels dérivés d'un filtre gaussien (Fig. 3).
- **Déroulage** (§4.3, §5) : le chemin de la coupe de référence sert de prototype pour les coupes voisines, par propagation : pour chaque point, maximum d'intensité sur 3 pixels le long du gradient (3 ou 5 selon la résolution). L'empilement des chaînes de pixels ordonnées donne l'image déroulée.

## Plateforme et implémentation

Pas de FPGA : fiche de méthode logicielle. Scanner : GE Optima 660 (CT médical), résolution isotrope minimale 0,35 mm, jusqu'à 128 projections par rotation (§3). Matériel de calcul, temps d'exécution, langage : n/r. Code : non publié. Jeu de test : un seul papyrus modèle fabriqué par les auteurs selon la méthode de Pline l'Ancien, avec un hiéroglyphe de Thoutmosis III peint à l'ocre et à la colle naturelle (Introduction) ; 259 coupes de 512 × 512, rognées à 175 × 175 (§5).

## Résultats

- Pour la coupe choisie, 0 point de branchement et un nombre de points de squelette proche de la moyenne (§5, Fig. 5). Un exemple de mauvaise coupe, avec recouvrements, est montré (Fig. 6).
- Les 259 spirales sont déroulées par propagation ; l'image obtenue est comparée au papyrus déroulé d'origine, et « many symbols » communs sont encadrés (§5, Fig. 7-8). La conclusion affirme que beaucoup de symboles deviennent visibles malgré la faible résolution (§6).
- Aucune métrique quantitative (précision, distorsion, taux de symboles retrouvés, temps) : la qualité est jugée visuellement.
→ reportés dans `benchmarks.csv` : aucune ligne. Le papier ne rapporte aucune mesure de performance ; seuls des paramètres d'acquisition et un résultat visuel existent, hors colonnes du schéma. D'où `benchmarks: none`.

## Limites et critique

- Évaluation qualitative sur un seul échantillon, fabriqué (hors papyrus antique), sans vérité terrain, sans mesure de distorsion ni de fidélité du déroulage.
- Hypothèse forte : les coupes adjacentes sont presque identiques (§4), donc le chemin d'une coupe sert de prototype. Elle ne tiendrait pas pour une forme qui varie le long de l'axe ; les auteurs ne la testent pas.
- Traitement 2D coupe par coupe, sans segmentation de surface 3D ; les cas de spires fortement mal espacées ne sont pas traités (§2, §6, aveu des auteurs). Étape manuelle : deux points par rouleau.
- Contraste favorable : l'encre ocre est plus dense que le support et visible en CT (Introduction). Déduit : la situation est bien plus favorable que celle de l'encre carbonée d'Herculanum, sans contraste d'absorption. Les auteurs notent que d'autres pigments ne sont pas visibles aux rayons X.
- Rouleau de laboratoire, non carbonisé, non écrasé ; résolution 0,35 mm, soit environ 40 fois plus grossière que les 8-9 µm des scans d'Herculanum (déduit en comparant avec le profil de la base, non affirmé par les auteurs).
- Pas de comparaison chiffrée avec les travaux cités (graph cut sur micro-CT, méthode manuelle) ; pas de code publié.

## Pertinence pour la thèse

Travail précoce et modeste de l'axe `virtual-unwrapping` : il illustre le déroulage par suivi de la spirale dans chaque coupe, avec propagation d'une coupe à l'autre, ancêtre simple du suivi de surface et des champs de nombre d'enroulement. Intérêt surtout historique et pédagogique pour Elder-scrolls : il montre la frontière entre CT médical (coupes 2D, 0,35 mm) et micro-CT 8-9 µm, et le recours à des pigments denses (hypothèse non valable pour l'encre carbonée). Il laisse ouvert : segmentation 3D, spires qui se touchent, mesure de la distorsion, validation quantitative, encre sans contraste.

## Gaps identifiés

- Pas de métrique ni de jeu de référence pour comparer des déroulages sur rouleaux modèles (papyrus fabriqués avec vérité terrain connue).
- Effet de la résolution du scanner (0,35 mm contre 8-9 µm) sur la lisibilité du déroulage : non quantifié.
- Passage de pigments minéraux denses à l'encre carbonée : non traité.

## Statut de lecture

Papier complet (fulltext.md lu en entier). Extraction `pymupdf`, `extraction.ok` à `false` : les figures et légendes sous-panneaux sont tronquées, ligatures perdues (« classi cation » : 4 fragments non réparés), aucun tableau de résultats dans le papier. Valeurs numériques lues dans le texte (§3, §5) ; aucune table.
Ce qui suit est déduit et non affirmé par les auteurs : le rapport de résolution avec Herculanum, le contraste avec l'encre carbonée, la filiation vers les méthodes actuelles.
