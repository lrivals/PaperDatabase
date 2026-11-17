---
id: 2005-lin-opaque-document-imaging-building-images
fiche: done
date: 2026-11-17
benchmarks: none
---

# Opaque Document Imaging: Building Images of Inaccessible Texts

Yun Lin, W. Brent Seales, 2005, Proceedings of the Tenth IEEE International Conference on Computer Vision (ICCV'05). https://doi.org/10.1109/iccv.2005.182
Type : article de conférence (ICCV'05, revu par les pairs)

## Problème

Construire une image lisible d'un document opaque, roulé ou plié (rouleau de papyrus, livre fermé), à partir d'un scan volumétrique pénétrant (CT), sans l'ouvrir ni le toucher (Abstract, Introduction). Le problème est posé en trois sous-problèmes : localiser la surface dans le volume de voxels (segmentation), générer une texture sur cette surface, la mapper en 2D. Les travaux antérieurs de numérisation de documents sont 2D ou limités à des pages planes ou courbées (correction de page curl) (Related Work). Cas visés : papyrus du British Museum non déroulés, rouleaux d'Herculanum, momie de Belgrade (Fig. 1-2).

## Méthode

Cadre en boucle itérative (§3.1) :
- **Localisation de surface** : contour actif « 2,5 D » (extension de [13, 1], optimisation gloutonne [19]). Énergie E1(V,S) = I(V,S) + C(S), avec I = −α|∇V|² (attire la surface vers les forts gradients d'intensité) et C(S) lissage (dérivées premières et secondes selon u, v : élasticité β, rigidité λ, torsion λuv) (§3.2, éq. 1-2). Initialisation par contours saillants sur coupes 2D reliés entre coupes ; semi-automatique : l'utilisateur fixe des points « snakeable » ou « movable ».
- **Texturage** : filtre sur V et S donnant une carte T1 non régularisée (surface = maillage triangulé).
- **Régularisation (aplatissement)** : approximation d'une application conforme par un système masse-ressort (déroulage : un bord tenu, le reste tombe sous gravité simulée) ; conserve les longueurs d'arêtes donc approximativement les angles, mais pas strictement conforme (§3.3-3.5). Donne T2, l'image du texte.
- **Contour guidé par la texture** : la surface est déplacée le long de sa normale ; la mesure de netteté (FFT, entropie du spectre normalisé, E2 = −E) sert de critère, mise à jour acceptée si E2 baisse (§3.6). Un critère plus riche (reconnaissance de motifs, expert) est prévu mais non implémenté.

## Plateforme et implémentation

Pas de FPGA : méthode logicielle. Scanner CT « sur mesure », jusqu'à 5 µm de résolution (§3) ; échantillons scannés à environ 12 µm par voxel (§Experimental Results). Matériel de calcul, temps de calcul, langage : n/r. Code : non publié.

## Résultats

- Expériences sur des répliques : bande de papyrus roulée et ruban de Möbius en papyrus, encre à la noix de galle, noyés dans une sphère de polyuréthane (Fig. 3) ; tests préalables sur rouleaux de toile et papyrus irréguliers (non détaillés).
- Échantillon roulé : texte des spires internes illisible sans régularisation ; l'image finale T2 est lisible : « Educe: Enhanced Digital Unwrapping for Conservation and Exploration » (§Experimental Results, Fig. 4).
- Ruban de Möbius (encre des deux côtés) : voxels difficiles à exploiter ; coupes en direction variable pour le contour actif ; image finale avec bleed-through, attribué à la résolution du scan (Fig. 4).
- Résultats purement qualitatifs : aucune métrique, aucun temps.
→ reportés dans `benchmarks.csv` : aucune ligne (le papier ne rapporte aucune valeur chiffrée de performance ; seuls des paramètres d'acquisition et des images). D'où `benchmarks: none`.

## Limites et critique

- Évaluation qualitative sur deux répliques fabriquées, sans vérité terrain, sans mesure de distorsion ni de précision de segmentation ; pas de comparaison à une autre méthode.
- Matériau favorable : encre à la noix de galle (déduit : contraste d'absorption bien supérieur à l'encre carbonée d'Herculanum), papyrus propre, couches nettes, pas d'écrasement ni de fusion de spires.
- Semi-manuel : initialisation et points mobiles réglés par l'utilisateur ; paramètres α, β, λ non donnés.
- Masse-ressort : approximation de conforme, distorsion non quantifiée ; critère de netteté générique, pas de signal d'encre propre.
- Aucun test sur un vrai rouleau antique ; les auteurs le disent « nécessaire mais non suffisant » (Conclusions). Pas de code, pas de données.

## Pertinence pour la thèse

Ancêtre fondateur de la chaîne de lecture virtuelle (Seales, Kentucky) : même décomposition segmentation de surface, texturage, aplatissement, que reprendra le cadre de 2016 (En-Gedi) puis les travaux sur Herculanum. Pour Elder-scrolls : le contour actif 2,5 D précède le suivi de surface automatique, le masse-ressort précède SLIM/ARAP (déduit), l'idée de régler la position de la surface par un critère d'image préfigure l'optimisation sur la qualité de texture. Laisse ouvert : encre carbonée à faible contraste, rouleaux écrasés, automatisation, mesure de distorsion, résolution (12 µm ici).

## Gaps identifiés

- Aucune métrique de distorsion ni de qualité de segmentation pour comparer les premières méthodes d'aplatissement.
- Valider sur des échantillons à encre carbonée (proxy d'Herculanum), non traité ici.
- Bleed-through à double face lié à la résolution : lien avec l'axe super-résolution.

## Statut de lecture

Papier complet (fulltext.md lu en entier). Extraction `pymupdf`, `extraction.ok` à `false` : sections numérotées non détectées, formules et algorithme glouton partiellement dégradés, figures absentes du texte (Fig. 3-4 seulement par leurs légendes).
Ce qui suit est déduit et non affirmé par les auteurs : l'avantage de contraste de l'encre à la noix de galle sur l'encre d'Herculanum ; les filiations vers SLIM/ARAP et le suivi de surface moderne ; l'absence de distorsion mesurée (non mentionnée plutôt que niée).
