---
id: 2018-rosin-virtual-recovery-content-x-ray
fiche: done
date: 2026-11-15
---

# Virtual Recovery of Content from X-Ray Micro-Tomography Scans of Damaged Historic Scrolls

Paul L. Rosin, Yu-Kun Lai, Chang Liu, Graham R. Davis, David Mills, Gary Tuson, Yuki Russell, 2018, Scientific Reports. https://doi.org/10.1038/s41598-018-29037-x
Type : article de journal (relu par les pairs). Hors Herculanum : deux rouleaux de parchemin anglais (encre ferro-gallique), mais le pipeline déroulage virtuel est le prédécesseur direct des méthodes de segmentation de feuillets du Vesuvius Challenge.

## Problème

Le goulot d'étranglement du déroulage virtuel n'est plus le scan mais le traitement d'image : la segmentation des couches de parchemin, difficile quand les couches sont fusionnées (humidité, feu, compression), cassées ou absentes (Introduction). Les travaux antérieurs (Samko et al. 2014, Liu et al. 2018) supposent une épaisseur de couche identique et connue, fragmentent les couches dans les zones fusionnées fines, et ne réutilisent pas la coupe précédente ; ils ne déroulent qu'environ un tiers du rouleau Bressingham.

## Méthode

Pipeline à base de traitement d'image classique, sans apprentissage ni labels (Methods) :
- entrée : pile de coupes 2D transversales du volume XMT (hypothèse : pas de grande déformation d'ensemble, le rouleau est scanné selon son axe) ; seuillage d'Otsu initial parchemin/air ;
- les coupes sont traitées en séquence : détection des jonctions (couches fusionnées), propagation du squelette (fond et premier plan) de la coupe i-1 vers la coupe i pour apparier les jonctions et initialiser les courbes de frontière manquantes (Éq. 1) ;
- optimisation de type contour actif : les courbes de séparation d'une région fusionnée sont optimisées pour répartir les couches « aussi uniformément que possible » (carte d'énergie par transformée de distance, Éq. 2-4, terme de courbure pondéré par β), sans épaisseur connue a priori ; 3 cycles suffisent ;
- reconnexion des couches cassées à partir du squelette précédent, enveloppe convexe et squelette du fond, puis croissance de graines pour la segmentation finale ; gère plusieurs feuilles (Diss Heywood : 4 feuilles) ;
- aplatissement : chaque squelette devient une ligne de l'image de sortie, alignement des squelettes voisins par programmation dynamique (surface non supposée développable) ; projection d'encre : projection en intensité maximale le long des normales (l'encre ferro-gallique est dense, donc brillante en XMT).
Les initialisations manuelles : une coupe segmentée à la main par volume (2 ou 4 volumes par rouleau).

## Plateforme et implémentation

- Scanner : MuCAT 2 XMT de laboratoire (Queen Mary Univ. of London), source microfocus 225 kV X-tek, caméra CCD refroidie en mode TDI, scintillateur CsI ; pixel effectif 60 µm, voxel reconstruit réglable de 5 à 40 µm (Methods).
- Bressingham (manuscrit de 1408-9, ~270 mm de large, fusionné par l'humidité) : 30 kV, 540 µA, voxel 30 µm ; 12 + 5 blocs de 2007 projections (~7 h/bloc) ; 4 volumes (p. ex. 1186x966x1228 à 1356x770x3684 voxels) ; 9938 coupes (Methods, Discussion).
- Diss Heywood (16e s., brûlé, 4 feuilles soudées) : 40 kV, 405 µA, voxel 35 µm ; 7 + 7 blocs de 2511 projections (~3 jours) ; 2 volumes (1780x1830x4012 et 1480x1880x4032) ; 8044 coupes (Methods, Discussion).
- Calcul : ~4 min par coupe, ~3 semaines par rouleau, Matlab non optimisé ; matériel de calcul n/r (Discussion).
- Code et données : « sur demande » seulement, non publiés (Code/Data availability).

## Résultats

- Bressingham : déroulage complet, texte lisible (compte de manoir de 1409, Fig. 3-4), validé par comparaison à la partie physiquement déroulable (Fig. 4) ; seulement ~15-30 % du texte lisible est récupéré, à cause des zones fusionnées compactées (perte totale d'encre) et des trous (Results). Distorsion géométrique (lignes courbées) due aux squelettes imprécis ; encre atténuée visible dès le scan brut.
- Diss Heywood : déroulage possible mais la feuille visualisée contient du texte superposé de la feuille voisine (Fig. 6) ; lecture partielle : Curia Generalis, « Item I give devise », un nom (Thomas Richards ?) (Fig. 7).
- Intervention manuelle : 14 coupes sur 9938 (Bressingham) et 15 sur 8044 (Diss Heywood), hors initialisation par volume (Discussion).
- Garantie annoncée : segmentation correcte si les couches font plus d'un voxel d'épaisseur (Diss Heywood ~7 voxels, minimum ~3 ; Bressingham ~5, jusqu'à 0,5 voxel aux endroits abrasés, d'où un sur-échantillonnage x2 en largeur et hauteur) (Discussion). La comparaison à Liu et al. est dans le SI (non lu).
- Évaluation : pas de métrique quantitative de lisibilité, de segmentation ou de distorsion ; validation visuelle sur le même rouleau, aucun jeu tenu à l'écart. Vérité terrain : lecture humaine du texte visible (Bressingham, partie déroulée).
→ reportés dans `benchmarks.csv` : 2 lignes (taux d'interventions manuelles et durée par coupe, Discussion).

## Limites et critique

- Aucun chiffre de précision de segmentation : le gain sur Liu et al. n'est pas quantifié dans le corps du papier (SI non disponible dans `fulltext.md`).
- Le texte récupéré (15-30 % sur Bressingham) reste partiel ; chevauchement entre feuilles non résolu sur Diss Heywood.
- Repose sur un fort contraste d'encre (fer, XMT 30-40 kV) : très différent de l'encre carbonée d'Herculanum, sans contraste d'absorption. Le résultat ne dit rien de la détection d'encre au sens du Challenge.
- Hypothèse d'une géométrie sans grande déformation, coupes traitées dans un seul axe, initialisation manuelle par volume ; temps de calcul de 3 semaines par rouleau.
- Code non publié (sur demande), reproductibilité limitée. Deux objets seulement, pas de comparaison à d'autres méthodes sur un jeu commun.

## Pertinence pour la thèse

Pertinence pour le Vesuvius Challenge : ancêtre des chaînes de segmentation de feuillets (propagation coupe à coupe, séparation de couches fusionnées, reconnexion de couches cassées, aplatissement par alignement de squelettes). Il montre aussi que la segmentation reste le facteur limitant de la lecture, et que les zones compactées/fusionnées font perdre l'encre : problème comparable aux zones « écrasées » et aux kolleseis des rouleaux d'Herculanum. Idées transférables : propagation de l'état de la coupe précédente, énergie de centre de couche par transformée de distance, épaisseur localement uniforme sans épaisseur imposée. Limites pour l'usage direct : pas d'apprentissage, méthode 2D par coupes, encre dense.

## Gaps identifiés

- Pas de comparaison quantitative entre méthodes classiques de segmentation de couches fusionnées et méthodes apprises (nnU-Net, etc.) sur un même jeu.
- Pas de métrique de distorsion de l'aplatissement ni de métrique de lisibilité standardisée.

## Statut de lecture

papier complet (`fulltext.md` lu en entier ; extraction PyMuPDF, `extraction.ok` à false : les équations 1-5 sont mal rendues, les figures et le SI ne sont pas lus).
Ce qui suit est déduit et non affirmé par les auteurs : le lien avec le Vesuvius Challenge, l'absence de transfert à l'encre carbonée, et l'idée de transfert (kolleseis, zones écrasées).
