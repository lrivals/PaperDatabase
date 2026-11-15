---
id: 2018-rosin-virtual-recovery-content-x-ray
fiche: done
date: 2026-11-15
benchmarks: none
---

# Virtual Recovery of Content from X-Ray Micro-Tomography Scans of Damaged Historic Scrolls

Paul L. Rosin, Yu-Kun Lai, Chang Liu, Graham R. Davis, David Mills, Gary Tuson, Yuki Russell, 2018, Scientific Reports. https://doi.org/10.1038/s41598-018-29037-x
Type : article de journal (relu par les pairs ; Open Access CC BY 4.0)

## Problème

Des documents historiques (parchemins) trop fragiles pour être ouverts restent inaccessibles. La chaîne standard est : scan, séparation parchemin/air, segmentation des couches, aplatissement, projection de l'encre. Les auteurs désignent la segmentation des couches comme le verrou : couches fusionnées par humidité, compression ou feu, parfois sans séparation réelle dans les données, couches cassées, plusieurs feuilles qui se touchent (Introduction). Les méthodes antérieures (Samko et al. 2014 ; Liu et al. 2018) supposent une épaisseur de couche identique et connue, fragmentent les régions fusionnées fines et exigent un re-liage sujet aux erreurs topologiques ; Liu et al. n'ont déroulé qu'environ un tiers du rouleau de Bressingham.

## Méthode

Pipeline presque entièrement automatique, traité coupe par coupe sur la pile 3D, avec propagation de la coupe précédente (Methods, « Virtual Unrolling ») :
- seuillage d'Otsu parchemin/air, puis détection des jonctions (coins de frontière) qui signalent des couches fusionnées ;
- propagation du squelette du fond de la coupe i-1 vers la coupe i (Éq. 1) pour apparier les jonctions et initialiser les courbes de frontière manquantes ;
- optimisation des courbes : carte d'énergie de forme E = d_max - D (D = transformée en distance, Éq. 2), courbe minimisant ∫E + β∫‖p″‖² (Éq. 3-4) à extrémités fixes, pour séparer la région fusionnée en couches « aussi régulières que possible », sans épaisseur connue a priori ; 3 cycles d'optimisation circulaire suffisent en pratique ;
- connexion des couches cassées via les squelettes de la coupe précédente, l'enveloppe convexe et le squelette du fond (Éq. 5), puis croissance de graines pour la segmentation finale, multi-feuilles possible ;
- projection d'encre : chaque squelette devient une ligne de l'image de sortie, alignement des squelettes voisins par programmation dynamique (distorsion minimale, surface non supposée développable), puis projection maximale des intensités le long des normales (encre de fer dense, donc forte absorption). Recto et verso séparés pour les documents recto-verso.
Les détails des règles et du schéma d'optimisation sont dans le matériel supplémentaire (SI), non disponible ici.

## Plateforme et implémentation

- Scanner : MuCAT 2 (Queen Mary University of London), générateur microfocus X-tek 225 kV, caméra CCD refroidie Spectral Instruments en mode TDI, scintillateur CsI, distance source-scintillateur 24 cm, pixel effectif 60 µm ; voxel reconstruit réglable de 5 à 40 µm (Methods, XMT).
- Bressingham (1408-9, ~270 mm de large, fusionné par humidité) : 30 kV, 540 µA, voxel 30 µm ; 12 + 5 blocs de 2007 projections, ~7 h par bloc ; 4 volumes (de 1186 × 966 × 1228 à 1356 × 770 × 3684 voxels) ; 9938 coupes (Discussion).
- Diss Heywood (XVIe s., brûlé, 4 feuilles enroulées) : 40 kV, 405 µA, voxel 35 µm ; 7 + 7 blocs de 2511 projections, ~3 jours ; 2 volumes (1780 × 1830 × 4012 et 1480 × 1880 × 4032) ; 8044 coupes.
- Calcul : ~4 min par coupe, ~3 semaines par rouleau ; matériel non précisé ; code Matlab non optimisé (Discussion).
- Code : « disponible sur demande » ; données : sur demande, serveur QMUL (Code/Data availability). Non publiés en ligne.
- Puissance / FPS : sans objet (n/r).

## Résultats

- Bressingham : déroulage complet, texte interprétable (compte de bailli daté de Michaelmas 9 Henry IV, 1409) ; environ 15-30 % du texte lisible obtenu, le reste perdu dans les zones fusionnées compactes (zones sombres de la Fig. 3 où toute l'encre est perdue) et les trous (Results, Fig. 3). Validation visuelle sur la partie déroulée physiquement : texte en grande partie retrouvé, avec perte de contraste d'encre (déjà présente dans le scan brut, attribuée à l'encre) et distorsion géométrique des lignes (squelettes imprécis dans les zones sous-contraintes) (Fig. 4).
- Diss Heywood : déroulage complet, mais la feuille visualisée contient du texte superposé de la feuille voisine (erreurs de segmentation entre feuilles qui se touchent) ; quelques éléments lisibles (Heywood Hall, Curia Generalis, « Item I give devise », un nom Thomas Richards ou Richardson) (Fig. 6-7).
- Épaisseur de couche : ~7 voxels (minimum ~3) pour Diss Heywood ; ~5 voxels en moyenne pour Bressingham, localement ~0,5 ; Bressingham sur-échantillonné 2× en largeur/hauteur avant traitement (Discussion).
- Intervention manuelle : 1 coupe d'initialisation par volume ; corrections sur 14 sur 9938 coupes (Bressingham) et 15 sur 8044 (Diss Heywood) (Discussion).
- Revendication : segmentation correcte tant que les couches font plus d'un voxel ; démontrée dans le SI, non vérifiable ici. La comparaison expérimentale avec Liu et al. est aussi dans le SI.
→ reportés dans `benchmarks.csv` : aucune ligne (voir Limites).

## Limites et critique

- Aucune métrique quantitative de segmentation ni de lisibilité (pas de vérité terrain, pas de comparaison chiffrée dans le corps du texte) : la validation est visuelle et qualitative. Seul chiffre de résultat : « 15-30 % du texte lisible » pour Bressingham, plage non définie (lisible selon qui, sur quelle surface). Pas de ligne `benchmarks.csv` justifiable : colonnes orientées FPGA, aucune métrique comparable à d'autres papiers.
- Le contraste d'encre repose sur du fer gallique dense (forte absorption X, projection par maximum) : l'approche ne transfère pas telle quelle à l'encre carbonée des papyrus d'Herculanum, sans contraste d'absorption (déduit, le papier ne cible pas Herculanum).
- Segmentation propagée coupe à coupe : dépendance à l'initialisation manuelle de chaque volume, et accumulation d'erreurs possible (déduit) ; la jonction entre volumes est faite après déroulage.
- Hypothèse d'absence de grande déformation d'échelle : les coupes le long d'un axe doivent donner des sections transversales (Methods).
- Coût : ~3 semaines par rouleau sur Matlab non optimisé ; matériel non précisé.
- Superposition de texte entre feuilles voisines non résolue pour Diss Heywood.
- Reproductibilité faible : code et données seulement sur demande ; détails de l'algorithme dans le SI.
- Résolution 30-35 µm, scan de laboratoire 30-40 kV, très éloignée des 8-9 µm du Vesuvius Challenge (synchrotron).

## Pertinence pour la thèse

Axe principal : `virtual-unwrapping` (travail de référence sur des rouleaux fusionnés de géométrie difficile) ; secondaire : `surface-segmentation` (propagation de squelette, séparation de couches fusionnées par énergie de forme, objectif d'épaisseur localement uniforme). Il traite le même verrou que les zones « écrasées » et les jonctions du projet Elder-scrolls (couches qui se touchent, feuillets compressés) avec une approche classique, sans apprentissage ; la propagation coupe à coupe et l'énergie de forme sont à comparer aux champs de nombre d'enroulement et aux modèles 3D. Ne couvre ni la détection d'encre carbonée, ni la super-résolution, ni le transfert de domaine. Laisse ouvert : transfert à des rouleaux de papyrus, évaluation quantitative, passage à l'échelle.

## Gaps identifiés

- Absence de métrique commune d'évaluation du déroulage et de la lisibilité (pas de vérité terrain) : comparer segmentations classiques et apprises sur un même rouleau.
- Séparation de feuilles qui se touchent (Diss Heywood) non résolue : écart à confronter aux méthodes d'instances 3D.
- Effet de la résolution (30-35 µm ici contre 8-9 µm) sur la segmentation de couches fines (Bressingham ~0,5-5 voxels) non étudié.

## Statut de lecture

papier complet (`fulltext.md` lu en entier). Extraction PyMuPDF (`backend: pymupdf`, `ok: false`, aucune section détectée) : texte plausible mais figures absentes, équations 3-4 et lettres grecques dégradées ; le matériel supplémentaire (SI) n'est pas disponible, donc règles de jonction, schéma d'optimisation, comparaison avec Liu et al. et démonstration « plus d'un voxel » non lues.
Ce qui suit est déduit et non affirmé par les auteurs : non-transfert à l'encre carbonée des papyrus ; accumulation d'erreurs par propagation ; absence de comparaison chiffrée (constat sur le texte lu, pas sur le SI).
