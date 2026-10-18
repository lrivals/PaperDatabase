---
id: arxiv-2102.12219-object-detection-aerial-images-large
fiche: done
date: 2026-10-18
---

# Object Detection in Aerial Images: A Large-Scale Benchmark and Challenges

Jian Ding, Nan Xue, Gui-Song Xia, Xiang Bai, Wen Yang, Micheal Ying Yang, Serge Belongie, Jiebo Luo, Mihai Datcu, Marcello Pelillo, Liangpei Zhang, 2021, arXiv preprint (métadonnées : DOI 10.1109/TPAMI.2021.3117983, donc version publiée dans TPAMI ; la version lue est l'arXiv). https://arxiv.org/abs/2102.12219
Type : preprint non relu par les pairs (version arXiv lue).

## Problème

Les images aériennes posent des difficultés propres : orientations arbitraires, très fortes variations d'échelle, densités d'objets non uniformes, grands rapports d'aspect (Fig. 1, §1). Il manquait un grand jeu annoté en boîtes orientées (OBB) ; xView et DIOR sont en boîtes horizontales (HBB) (§1, §2.2). Les bibliothèques de détection ne géraient pas l'OBB et les baselines n'étaient pas comparables (§1). Les images sont très grandes (jusqu'à 20 000 × 20 000 px) et ne tiennent pas en mémoire GPU (§2.3).

## Méthode

Contribution surtout de données (DOTA-v2.0), plus une bibliothèque et des baselines.

- **Collecte** (§3.1) : Google Earth, satellites GF-2 et JL-1, images aériennes CycloMedia (Rotterdam, vues obliques à environ 45° et nadir). Google Earth : images de 800×800 à 4000×4000 ; GF-2 et CycloMedia gardent leur taille d'origine (typiquement 29 200×27 620 et 7 360×4 912). Choix de sources multiples contre les biais de capteur et de résolution.
- **Catégories** (§3.2) : 18 classes, choisies pour leur fréquence et leur utilité ; les « stuff » (harbor, airport) sont retenues car leurs bords sont assez nets.
- **Annotation OBB** (§3.3) : boîte = 4 sommets (x_i, y_i), ordre horaire. Les annotateurs cliquent les 4 coins ; pour les classes dont la forme s'éloigne d'un rectangle, 4 points clés sur l'objet convertis en OBB (ex. avion : tête, deux bouts d'ailes, queue). Ambiguïté de l'ordre des points (4 permutations équivalentes) : pour les classes avec tête et queue (helicopter, large vehicle, small vehicle, harbor), le premier point marque la « tête » ; pour les autres (soccer-ball field, swimming pool, bridge), point en haut à gauche. Pipeline : outil sur mesure, exemples par des experts en interprétation d'images aériennes, formation de volontaires (Wuhan University), évaluation puis répartition en groupes « plain » et « senior » ; annotations initiales du groupe plain, double vérification par les seniors et les auteurs, renvoi des images non conformes.
- **Erreurs d'annotation** (§3.3, Discussion) : objets manquants (surtout minuscules, proportion jugée négligeable, non chiffrée) et boîtes imprécises (ambiguïté de bord, occultation).
- **Statistiques** (§4) : résolution (GSD) connue pour 30 % des images (GF-2 0,81 m/px, JL-1 0,72, CycloMedia 0,1, Google Earth 0,1 à 4,5) ; utile pour filtrer des outliers de taille ou normaliser l'échelle (§4.2). Orientations uniformes dans [-π, π] (§4.3, Fig. 1g). Taille par hauteur de HBB (§4.4), rapport d'aspect des OBB et des HBB (§4.5), densité par distance au plus proche voisin de même classe (§4.6).
- **Découpage** (§5.2) : patchs 1024×1024, pas de 824 (donc recouvrement de 200 px ; l'ancien pas était de 512, [14]). À l'inférence : mêmes patchs, détections ramenées aux coordonnées de l'image d'origine, puis NMS (seuil 0,3 en HBB, 0,1 en OBB). Multi-échelle : images redimensionnées à [0,5, 1,0, 1,5] avant découpage. La boîte à outils fournit découpage et fusion (§5.3). Les auteurs disent suivre la solution « naïve » de découpage (§2.3).
- **Baselines** : 10 algorithmes, plus de 70 configurations, dans MMDetection étendu (têtes OBB, RoI Align tourné) ; métrique mAP VOC07, IoU entre polygones convexes pour l'OBB (§5.1). 4 GPU, batch total 8, lr 0,01, schéma « 1× » sauf RetinaNet « 2× » (§5.2).

## Plateforme et implémentation

Détection sur GPU, pas de FPGA. Vitesse d'inférence sur un NVIDIA Tesla V100, images 1024×1024 (Table 6) ; puissance : n/r. Bibliothèque de code et kit de développement publiés (site DOTA : https://captain-whu.github.io/DOTA/, liens indiqués en notes 2, 7, 8 du texte) ; serveur d'évaluation en ligne. Images de test-dev et test-challenge sans annotations (§4.7).

## Résultats

Dataset (Table 1, Table 5) : 11 268 images, 1 793 658 instances, 18 classes (DOTA-v1.0 : 2 806 images, 188 282 instances, 15 classes ; DOTA-v1.5 : 402 089 instances, 16 classes). Instances par image : 159,18 (v2.0), 67,10 (v1.0), contre 7,19 pour COCO et 2,42 pour VOC (Table 1). Découpage v2.0 : 268 627 instances en train, 81 048 en val, 353 346 en test-dev, 1 090 637 en test-challenge ; les parts train/val sont volontairement plus petites que le test contre le surapprentissage (Table 5).

Déséquilibre (Table 5, v2.0) : small vehicle 1 235 658 instances, ship 251 883, large vehicle 89 353 ; helicopter 893, helipad 611.

Tailles (hauteur du HBB, Table 4) : petites (10-50 px) 0,77, moyennes (50-300) 0,22, grandes (>300) 0,01 en v2.0 ; COCO 0,43 / 0,49 / 0,08 ; VOC 0,14 / 0,61 / 0,25. Rapport de foreground (Table 3) : 0,037 Google Earth, 0,003 GF&JL, 0,033 aérien CycloMedia, 0,016 au total en v2.0 (0,042 en v1.5) : beaucoup de fond, plus proche de l'usage réel.

Baselines (Table 6, OBB mAP, V100) : Faster R-CNN OBB + RoI Transformer 73,76 (v1.0), 65,03 (v1.5), 52,81 (v2.0) à 12,4 fps ; Faster R-CNN OBB 47,31 à 14,1 fps (v2.0) ; Mask R-CNN 49,47 à 9,7 fps (v2.0). Les scores baissent de v1.0 à v2.0 (jeu plus difficile).

Pratiques de données mesurées :
- Annoter les objets minuscules : AP de small vehicle avec RoI Transformer, 77,45 (v1.0) contre 52,05 (v1.5) (§6.1.6) ; rappel très faible sous ~10 px (Fig. 12, §6.1.7).
- Exclure les très petites instances à l'entraînement (v1.5, v2.0) : sans grand effet sur le HBB mAP (51,08 ; 51,35 ; 50,71 selon le seuil, Table 10). Seuils et détecteur non détaillés.
- Ablation sur DOTA-v1.5 avec Faster R-CNN OBB + RoI Transformer (Table 12, OBB mAP) : base 65,03 ; 67,57 ; 69,44 ; 73,62 ; 76,43 ; 77,60 pour, dans l'ordre des colonnes, recouvrement 200 → 512, multi-échelle train, multi-échelle test, rotation train, rotation test. Les cases cochées ne sont pas lisibles dans l'extraction : le caractère cumulatif est déduit (voir doutes). Rotation à l'entraînement : angle continu dans [-π, π] ; pour les images avec roundabout ou storage tank, rotation parmi 4 angles (§6.1.5). Rotation au test : 4 angles, fusion par NMS.
- Challenge DOAI 2019 (v1.5, Tables 12 et 14) : modèle unique avec augmentations, 77,60 OBB et 78,88 HBB (Table 14) ; 173 inscrits, 13 équipes valides en OBB, 22 en HBB (§6.3). Le texte cite 76,43 OBB et 77,24 HBB pour « les mêmes réglages » (§6.3).
- Têtes : la tête masque dépasse la tête OBB de 0,57 point en v2.0 (Mask R-CNN contre Faster R-CNN H-OBB) mais 4 fps plus lent (§6.1.1). Nombre de propositions : optimum à 8 000 en v2.0 contre 300 pour VOC ; 2 000 retenu (§6.1.4).
- OBB contre HBB : sur les objets denses (large vehicle), +8 points d'AP pour Faster R-CNN OBB sur Faster R-CNN en v1.0 (§6.1.6) ; le NMS HBB supprime des véhicules adjacents (§6.1.7).

Lignes ajoutées dans `benchmarks.csv` (proposées à l'agent principal) : 13 lignes (Table 12 : 6 ; Table 6 : 4 ; Table 10 : 3). Les valeurs de Table 12 ont `confidence: medium` (cases cochées illisibles). Les Tables 7, 8, 9 et 14 sont partiellement extraites, aucune valeur par classe n'a été reprise.
→ reportés dans `benchmarks.csv` : voir `.cache/bench/arxiv-2102.12219-object-detection-aerial-images-large.csv`.

## Limites et critique

- Rien de ces consignes n'est mesuré par ablation de l'annotation elle-même : pas de comparaison OBB contre HBB à détecteur égal sur la qualité du dataset, pas de mesure d'accord inter-annotateurs, pas de taux d'erreurs d'annotation (« proportion négligeable », sans chiffre, §3.3). Le contrôle qualité est décrit (double vérification) mais non quantifié.
- Aucune notion « difficult » ni consigne explicite pour les objets tronqués ou occultés n'apparaît dans le texte. Seul indice : le recouvrement de 200 px des patchs est présenté comme remède aux grands objets coupés au bord (§6.1.5). Les détails sont probablement dans le kit de développement, non lu.
- Découpage : une seule configuration de taille (1024) ; le gain isolé du recouvrement (200 → 512) est mélangé dans une ablation, non isolé d'autres facteurs de taille de patch ; aucun test d'autres tailles de patch.
- Table 12 : ordre cumulatif déduit, une seule architecture, sur v1.5 (pas v2.0). Les gains d'augmentation sont donc spécifiques au domaine aérien (rotations libres) et ne se transposent pas aux images de scène au sol.
- Comparaison des mAP entre versions de DOTA : les jeux changent (v2.0 a beaucoup plus de petites instances et de fond), pas comparable en valeur absolue. L'écart au challenge (76,43 contre 77,60) suggère des réglages différents selon le passage (§6.3 contre Table 14).
- Tous les modèles sont à deux étages sur ResNet-50, pas de YOLO ; aucune puissance mesurée. Transfert à YOLO déduit seulement.
- Version arXiv non relue ; le DOI renvoie à la version TPAMI.

## Pertinence pour la thèse

Pour le thème de la base (préparer un jeu de détection YOLO) :

- **CONSTRUIRE** : mélanger des sources (capteurs, résolutions) et inclure des images à faible ratio de foreground (0,003 à 0,033) pour garder des négatifs réalistes ; choisir les classes selon leur fréquence et leur utilité ; garder train/val plus petits que le test. Les classes rares (helipad 611, helicopter 893) restent très faibles face à small vehicle (1,2 M) : déséquilibre assumé, non traité.
- **ANNOTER** : quand les objets sont tournés et denses (bateaux, véhicules, hangars), l'OBB à 4 coins est préférable : le HBB rend les objets voisins inséparables et le NMS HBB supprime des détections. Règle d'ordre des points à fixer avant d'annoter (tête d'abord pour les classes orientées, sinon coin haut-gauche). Pour les formes non rectangulaires, annoter des points clés puis convertir. Pipeline de contrôle à reprendre : exemples par experts, formation, double revue, renvoi. À appliquer si le jeu YOLO vise des vues aériennes ou des objets très inclinés (le format Ultralytics OBB à 4 coins normalisés est proche).
- **PRÉTRAITER** : pour des images de plus de ~4000 px, découper en patchs 1024×1024 avec recouvrement (200 px ici), remapper les boîtes dans l'image d'origine et appliquer un NMS global ; seuil de NMS plus bas en OBB (0,1) qu'en HBB (0,3). Annoter ou non les objets de moins de 10 px : coûteux (AP -25 points sur small vehicle) mais l'exclusion à l'entraînement change peu le résultat (Table 10).
- **AUGMENTER** : sur ce domaine, rotation aléatoire continue et multi-échelle (0,5 / 1,0 / 1,5) sont les plus gros gains mesurés (65,03 vers 77,60 en cumulé, Table 12), plus fort recouvrement des patchs ; test multi-échelle et rotation au test coûtent du temps d'inférence. À appliquer quand l'orientation est libre (vue de dessus) ; inutile voire nuisible pour des scènes soumises à la gravité (déduit).
- Ouvert : pas de pratique explicite pour objets tronqués ou « difficult » ; pas de Mosaic, MixUp, Copy-Paste ; pas de YOLO.

## Gaps identifiés

- Effet de la taille de patch et du recouvrement isolés (tiling) pour un détecteur one-stage de type YOLO.
- Mesure de la qualité d'annotation OBB (accord entre annotateurs, taux d'erreurs), et comparaison OBB contre HBB à coût d'annotation égal.
- Consignes pour objets tronqués par le découpage et par le bord de l'image ; traitement des objets minuscules (<10 px).
- Augmentations de type Mosaic ou Copy-Paste sur jeux aériens, absentes de ce papier.

## Statut de lecture

papier complet (`fulltext.md` lu en entier, extraction GROBID). Les tableaux 7, 8, 9 (AP par classe), 13 et 14 sont mal extraits (corps fragmentés) : aucune valeur par classe n'a été reprise. Table 12 : les cases cochées sont perdues.
Ce qui suit est déduit et non affirmé par les auteurs : l'ordre cumulatif des augmentations de Table 12 (colonnes dans l'ordre des lignes de la table, dernière colonne égale au 77,60 de Table 14) ; le recouvrement de 200 px (824 contre 1024) ; la transposition à YOLO et à des images prises au sol ; l'absence de consigne « difficult » (non trouvée dans le texte, peut exister dans le kit de développement) ; le détecteur et les seuils de Table 10 (non précisés).
