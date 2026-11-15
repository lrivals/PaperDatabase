---
id: 2018-liu-robust-virtual-unrolling-historical-parchment
fiche: done
date: 2026-11-15
---

# Robust Virtual Unrolling of Historical Parchment XMT Images

Chang Liu, Paul L. Rosin, Yu-Kun Lai, Weiduo Hu, 2018, IEEE Transactions on Image Processing 27(4):1914-1926. https://doi.org/10.1109/tip.2017.2783626
Type : article de journal (revue à comité de lecture ; version étendue d'un article de conférence, réf. [21] du papier).

## Problème

Dérouler virtuellement des rouleaux de parchemin fragiles, impossibles à ouvrir physiquement, à partir de
tranches de micro-tomographie X (XMT) : les couches varient en épaisseur, contiennent des textures
internes et collent entre elles par endroits (« fused regions »). Le verrou posé par les auteurs est une
segmentation topologiquement correcte des couches, préalable à l'aplatissement et à la révélation du
texte (Abstract, §I). Cas d'étude : le rouleau de Bressingham (1408-9, ~270 mm de large, fusionné dès
~100 mm du début) (§I).

## Méthode

Pipeline par tranche puis inter-tranches (§II-III) :
1. Seuillage d'Otsu ; le filtrage CED a été testé et jugé inutile (§II, Table III).
2. Connexion des couches brisées à l'aide du squelette de la tranche précédente (seuil de rapport 0,5) (§II-A).
3. Détection des « junction sections » (s = 15 pixels, angle < 120°) et des régions fusionnées (§II-B.1-2).
4. Courbes « as parallel as possible » (forme close par multiplicateurs de Lagrange) et énergie de forme gaussienne
   (sigma = m/3, m = épaisseur de couche : 14 px pour les trois rouleaux de Samko, 11 px pour Bressingham)
   (§II-B.3-4).
5. Appariement global des junction sections par l'algorithme blossom d'Edmonds, coût H avec lambda = 1 (§II-B.5) ;
   reconnexion des squelettes (§II-B.6).
6. Aplatissement : plus long chemin du squelette, alignement de tranches adjacentes par programmation dynamique
   (variante de DTW, tau = 0,45, complexité O(n_i n_{i+1})), puis « ink projection » : intensité maximale le long
   de la normale sur d = m (pas 0,25 voxel, interpolation trilinéaire), inversion et contraste (§III).

Aucun apprentissage : méthode géométrique et d'optimisation classique.

## Plateforme et implémentation

PC de bureau à 2,9 GHz (processeur non précisé), pas de GPU mentionné (§IV). Scans XMT acquis à la School of
Medicine and Dentistry, QMUL (réf. [7]) ; résolution voxel, tension, source : n/r dans ce papier. Code ou
données publiés : non mentionnés (n/r).

## Résultats

- Trois rouleaux de Samko et al. : petit 708 tranches 430x430, moyen 700 tranches 530x530, grand 423 tranches
  1702x1732 ; plus grande région fusionnée : 3 couches (§IV). Bressingham : 3070 tranches 1256x816, plus
  grande région fusionnée > 6 couches, épaisseur moyenne ~6 px, image doublée avant traitement (§IV).
- Segmentation évaluée sur 12 images par jeu (3 rouleaux) et 14 tranches (Bressingham), vérité terrain manuelle,
  mesures RI, VI, P, R, F (Tables I-III). Les corps des Tables I à IV ne sont pas extraits dans `fulltext.md` :
  leurs valeurs sont n/r ici. Texte seulement : Baum et al. est meilleur sur petit et moyen rouleau, la méthode est
  proche du meilleur ; elle est la plus satisfaisante sur le grand rouleau (§IV) ; sur Bressingham, elle
  l'emporte en RI, VI, P et F, avec P/R/F proches pour toutes les méthodes (§IV, Table II).
- Segmentation topologiquement correcte sur les 3070 tranches de Bressingham, là où la version conférence [21]
  échoue sur quelques tranches (§IV, Fig. 22).
- Temps : petit rouleau 22,8 s contre 6,4 h pour Samko et al. [12] ; Bressingham 2,56 h contre 4,5 semaines (§IV,
  chunk 2018-liu#030.0). Introduction du facteur : « 300-1 000 fois plus rapide » (§III).
- Table IV : corrélation de Pearson entre photographie d'une partie visible et reconstructions ; scores
  « généralement faibles », méthode légèrement meilleure que Baum et al., écart faible ; les trous de Baum
  couvrent moins de 5 % de l'image (§IV) ; valeurs n/r (corps non extrait).
- Lisibilité : « nombreux blocs de texte avec lettres visibles », évaluation qualitative seulement (§IV, Fig. 23-25).
→ reportés dans `benchmarks.csv` : 2 lignes (temps de déroulage, petit rouleau et Bressingham).

## Limites et critique

- Évaluation de la segmentation sur très peu d'images (12 et 14) ; aucune mesure de lisibilité du texte ni
  d'OCR : la preuve de correction est visuelle (Fig. 23-25).
- Table IV : une corrélation photographie/rayons X est peu informative (les auteurs le reconnaissent) et
  n'a pu être calculée que si le recalage est possible ; les méthodes de Samko et des snakes échouent à ce
  recalage.
- Comparaison avec Baum et al. : 35 clés initialisées à la main pour Bressingham, alors que la méthode des
  auteurs est automatique ; comparaison à effort humain inégal, mais en leur défaveur de Baum.
- Hypothèse d'une couche unique de parchemin, d'un écrit sur une seule face (d = m « pour un parchemin à face
  unique ») et de tranches voisines très similaires ; pas de mesure sur papyrus, encre non carbonée ni
  résolutions modernes (déduit).
- Temps mesurés sur un PC sans détail de CPU ; le facteur de gain dépend du matériel de Samko (non précisé ici).
- Pas de code publié mentionné ; pas d'incertitude ni de faux positifs sur le texte restitué.

## Pertinence pour la thèse

Travail fondateur du déroulage virtuel de rouleaux en XMT (axe `virtual-unwrapping`) : segmentation 2D tranche par
tranche avec contraintes topologiques, puis aplatissement par squelette et projection d'encre. Il pose les
difficultés (couches collées, couches brisées, grandes déformations) que le Vesuvius Challenge traite en 3D
avec des méthodes apprises. Il laisse ouvert le passage à l'échelle des rouleaux enroulés très serrés,
l'absence de métrique de lisibilité et la validation quantitative du texte (déduit pour la comparaison).
Axe secondaire : `ct-imaging` (acquisition XMT du parchemin).

## Gaps identifiés

- Pas de métrique standard de qualité du déroulage (hors RI/VI de segmentation et corrélation photo).
- Aucun test sur matériau carbonisé (papyrus d'Herculanum) ni sur d'autres résolutions que celles de QMUL.
- Absence de code et de données publiés (n/r).

## Statut de lecture

Papier complet (fulltext.md lu en entier, extraction `pymupdf`, `extraction.ok: false`) : le texte peut être
mal découpé ; ligatures partiellement réparées, 10 fragments non réparés. Le corps des Tables I, II, III et IV
est absent du texte extrait : leurs valeurs ne sont pas rapportées ici.
Ce qui suit est déduit et non affirmé par les auteurs : limites d'applicabilité aux papyrus carbonisés,
absence de code publié (simplement non mentionné), comparaison d'effort humain, lien avec le Vesuvius Challenge.
