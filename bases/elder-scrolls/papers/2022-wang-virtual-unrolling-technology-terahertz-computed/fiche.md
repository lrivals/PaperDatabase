---
id: 2022-wang-virtual-unrolling-technology-terahertz-computed
fiche: done
date: 2026-11-17
---

# Virtual unrolling technology based on terahertz computed tomography

Tianyi Wang, Kejia Wang, Kaigang Zou, Sishi Shen, Yongqiang Yang, Mengting Zhang, Zhengang Yang, Jinsong Liu, 2022, Optics and Lasers in Engineering 151 (2022) 106924. https://doi.org/10.1016/j.optlaseng.2021.106924
Type : article de journal (revu par les pairs)

## Problème

L'inspection non invasive de reliques aux formes particulières (documents pliés, rouleaux) reste un verrou à cause de la diversité des formes et de l'occlusion (Abstract). Le déroulage virtuel existe en rayons X, mais le X est coûteux (grandes installations) et peut accélérer le vieillissement de la cellulose (Introduction). Les méthodes THz TDS/FMCW ne conviennent pas aux surfaces courbes : le SNR chute avec la profondeur et les couches profondes sont occultées (Introduction). Les auteurs visent un déroulage virtuel en THz CT, sans ionisation, d'un objet multicouche ; leur tentative précédente par détection de bords échoue sur plusieurs couches (Introduction).

## Méthode

Objet abstrait en « Curve Extrude Structure » (courbe plane extrudée), la coupe est traitée comme une « carte topographique » : l'information est portée par la crête (ridgeline) de chaque coupe (§2.2.1). Pipeline en 4 étapes :
- Reconstruction par FBP (filtre rampe) ; ART essayé et écarté : qualité inférieure et calcul 10 fois plus long à 10 itérations (§2.2.2, §4.1).
- Suppression des artefacts « métalliques » : segmentation k-means++ (3 classes : air, support, contenu), reprojection, retrait de la trace dans le sinogramme, inpainting de Criminisi modifié (priorité P = C/D au lieu de C×D, pour ne pas régénérer le métal), re-reconstruction (§2.2.3, §4.1).
- Détection de crête (Steger, sous-pixel, espace d'échelle gaussien, Hessienne) puis squelette à 1 pixel par K3M modifié (§2.2.4).
- Assemblage MGDE (Match-Graft based on Dynamic Exemplar) : la ligne la plus complète sert d'exemplaire, chaque segment incomplet est apparié par somme de distances euclidiennes et greffé, l'exemplaire est mis à jour à chaque itération (§2.2.5). L'image déroulée empile les profils dans l'ordre des coupes (§4.1).

## Plateforme et implémentation

Pas de FPGA ; méthode logicielle sur un banc THz maison. THz CT à onde continue 0,3 THz, 0,3 mW, diode Gunn + multiplieur (émetteur), diode Schottky + détecteur à verrouillage (SR830) ; faisceau d'environ 5 mm au plan de l'échantillon ; pas de scan 0,5 mm (x), 2 mm (y), 2° (θ) (§3.1). Échantillon : toile de 300 µm peinte de trois lettres T, H, Z (bleu outremer, environ 1 mm), collée sur un support 3D en spirale d'Archimède, 8 mm entre spires, θ de 3π à 6π (§3.2). 26 coupes, 141×141 px, durée du scan environ 80 h (§3.2, §4.1). Calcul : Intel i7-7700 3,6 GHz, 16 Go, Matlab ; quelques dizaines de secondes par coupe hors réglage des paramètres, quelques secondes pour l'assemblage (§4.2). Code non publié ; données sur demande aux auteurs (Data availability).

## Résultats

- Les trois lettres sont reconnaissables dans l'image déroulée (§4.2, Fig. 11a) ; image déformée légèrement, bords de lettres plus brillants que l'intérieur (§4.1).
- Contre l'image de transmission THz du même système : PSNR 14,0524 et SSIM 0,3874 (§4.2). Les auteurs n'interprètent pas ces valeurs ; la référence est elle-même une image dégradée, ce n'est pas une vérité terrain.
- Les SSIM des lignes de crête recollées par MGDE, comparées à la ligne la plus complète (couche 1), dépassent 0,8 sur les 5 couches montrées ; certaines lignes incomplètes sont déformées (Appendice 4, Fig. A.4).
- Suppression des artefacts : efficace visuellement, avec un bruit de reconstruction accru (grandes zones à reconstruire) (Appendice 3) ; pas de métrique.
→ reportés dans `benchmarks.csv` : 2 lignes (PSNR 14,0524 ; SSIM 0,3874, §4.2, `confidence: medium`, texte et non tableau). Ligne retenue malgré le faible intérêt : seul chiffre de qualité du papier. `power_scope` : n/r.

## Limites et critique

- Une seule maquette, trois lettres, écartement de 8 mm choisi pour « éviter le problème de résolution THz » (§3.2) : très loin d'un rouleau réel (spires serrées de quelques centaines de µm). Les auteurs reconnaissent que l'élargissement et les artefacts fusionnent les couches quand l'espacement diminue (§5).
- Évaluation faible : PSNR et SSIM par rapport à une image de transmission, pas de vérité terrain, pas d'ablation chiffrée (MAS, MGDE), pas de mesure de distorsion ; ART vs FBP jugés visuellement.
- Le signal extrait est la crête d'intensité du profil (le pigment est plus absorbant), non une encre carbonée sans contraste : déduit, transfert incertain à Herculanum.
- Pipeline semi-manuel : réglage de paramètres par coupe, segmentation avec nombre de classes connu a priori, MGDE exige qu'une coupe soit complète (§5). Scan de 80 h pour 26 coupes de 141×141 px.
- Résolution de l'image finale bornée par celle de la THz CT ; hauteur = nombre de coupes (26) (§4.1, §5).
- Code non publié, données sur demande.

## Pertinence pour la thèse

Cas limite de l'axe `virtual-unwrapping` : déroulage hors rayons X, sur maquette, par suivi de profil en 2D coupe par coupe, donc très éloigné du suivi de feuillet 3D du Vesuvius Challenge. Utile pour trois points : (1) l'idée de ne suivre que la crête par coupe, ancêtre simple de la segmentation de surface ; (2) la modélisation des artefacts de type métal par inpainting de sinogramme, lié à `ct-imaging` ; (3) MGDE, recollement de profils incomplets à partir de coupes voisines, comparable à l'interpolation entre coupes dans les pipelines de segmentation. Ne répond ni à l'encre carbonée, ni à la résolution 8-9 µm, ni à l'aplatissement 3D.

## Gaps identifiés

- Aucune évaluation de déroulage virtuel sur un objet réel à spires serrées hors rayons X ; pas de métrique de distorsion.
- Segmentation de feuillet par crête 2D coupe par coupe : cohérence 3D non traitée (relation entre coupes laissée en perspective, §5).
- Artefacts de scan et leur effet sur la continuité des couches : pas de comparaison avec les artefacts réels des scans d'Herculanum.

## Statut de lecture

Papier complet (fulltext.md lu en entier, appendices compris). Extraction `pymupdf`, `extraction.ok` à `false` : ligatures « fi/ﬁ » dupliquées, formules partiellement perdues (éq. de K3M, matrice N), figures absentes ; pas de tableau. Section « 4.4.x » numérotée ainsi dans le texte pour 4.1.
Ce qui suit est déduit et non affirmé par les auteurs : le rapprochement avec le suivi de surface et l'interpolation entre coupes ; le contraste d'absorption plus favorable que l'encre carbonée d'Herculanum ; l'écart de réalisme (8 mm contre quelques centaines de µm) ; l'interprétation de PSNR/SSIM comme indicateurs faibles.
