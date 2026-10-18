---
id: arxiv-2001.06303-detection-tracking-meet-drones-challenge
fiche: done
date: 2026-10-18
---

# Detection and Tracking Meet Drones Challenge

Pengfei Zhu, Longyin Wen, Dawei Du, Xiao Bian, Heng Fan, Qinghua Hu, Haibin Ling, 2020, arXiv preprint. https://arxiv.org/abs/2001.06303
Type : preprint non relu par les pairs (version arXiv v3 du 4 oct. 2021 ; une version en revue existe probablement, mais le texte ne la mentionne pas : à vérifier)

## Problème

Les détecteurs et trackers génériques sont sous-optimaux sur les images de drone : points de vue arbitraires, grandes variations d'échelle selon l'altitude, flou de bougé (§1). Les auteurs attribuent le retard au manque de jeux de données drone publics, volumineux et annotés à la main (§1, §2.3). Le papier présente le jeu VisDrone, résume trois éditions de challenge (ECCV 2018, ICCV 2019, ECCV 2020, plus de 100 équipes) et analyse les méthodes soumises (Abstract, §1). Pour cette base : c'est la description de référence de la constitution et de l'annotation de VisDrone-DET, le jeu de petits objets le plus utilisé avec YOLO.

## Méthode

Papier dataset + synthèse de challenge, sans méthode propre.

**Constitution du jeu (§1, §3, Fig. 1)**
- 263 clips vidéo (179 264 images) et 10 209 images fixes, plus de 2,5 millions de boîtes, 10 catégories, 14 villes chinoises (Tianjin, Hongkong, Daqing, Ganzhou, Guangzhou, Jincang, Liuzhou, Nanjing, Shaoxing, Shenyang, Nanyang, Zhangjiakou, Suzhou, Xuzhou), scènes urbaines et rurales, denses et clairsemées, météo et éclairages variés (Fig. 1, §1).
- Capteurs : drones DJI Mavic et série Phantom (3, 3A, 3SE, 3P, 4, 4A, 4P) ; résolution maximale 3840 × 2160 en vidéo, 2000 × 1500 en image fixe (légende Fig. 1). Modèle de caméra, focale, altitude de vol : n/r.
- Splits DET : 6 471 train / 548 val / 1 580 test-challenge / 1 610 test-dev (§4.1). Les images de train, val et test sont prises à des lieux différents mais avec des scènes et attributs similaires (§3). Vérité terrain du test cachée pour éviter le sur-apprentissage ; données externes autorisées si déclarées (§3).
- VID et MOT : 96 clips, 5 catégories (piéton, voiture, van, bus, camion) : 56 train (24 198 images), 7 val (2 846), 16 test-challenge (6 322), 17 test-dev (6 635) (§5.1, §7). SOT : 167 séquences, 139 276 images ; 25 séquences longues (82 644 images) ajoutées en 2019 (§6.1).

**Annotation (§3, §4.1, §5.1)**
- Boîtes englobantes annotées à la main, image par image, puis contrôle croisé (cross-checking) pour la qualité (§3). Pas de taux d'accord inter-annotateurs, pas de nombre d'annotateurs, pas d'outil nommé : n/r.
- Coût : plus de 6 000 heures de travail (§8), soit, rapporté aux 2,5 M de boîtes (toutes tâches confondues), un ordre de grandeur de quelques secondes par boîte (calcul à partir de deux chiffres du papier, non affirmé par les auteurs).
- 10 classes DET : pedestrian, person, car, van, bus, truck, motor, bicycle, awning-tricycle, tricycle. Règle pedestrian / person : un humain debout ou qui marche est « pedestrian », sinon « person » (note 6, §4.3). Les véhicules rares (machineshop truck, forklift, tanker) sont ignorés, c'est-à-dire non annotés comme classe (§4.1).
- Deux attributs par boîte : occlusion (aucune 0 %, partielle ]0, 50 %], forte ]50, 100 %]) et troncature (part de l'objet hors cadre, estimée par un humain). Toute instance tronquée à plus de 50 % est exclue de l'évaluation (§4.1).
- Zones ignorées (ignored regions) annotées par image en VID/MOT (§5.1) ; pour DET, le texte ne le dit pas : n/r.
- Attributs de séquence SOT : 12, repris d'UAV123 (§6.1).

**Distribution des classes et des tailles**
- Déséquilibre fort : en DET, awning-tricycle a plus de 40 fois moins d'instances que car (§4.1) ; en VID, plus de 50 fois plus de trajectoires de voitures que de bus en train (§5.1). Les effectifs par classe et par degré d'occlusion sont donnés seulement en Fig. 2 et Fig. 4 (graphiques non extraits) : n/r.
- Taille des objets : « extremely small scale of objects » (§4.4) ; aucune distribution chiffrée (ni histogramme de tailles, ni AP_small / AP_medium) dans le texte : n/r. Longueur des trajectoires de 1 à 1 255 images (§5.1).
- Table 1 : VisDrone-DET est annoncé à 10 209 images, 10 catégories, 2000 × 1500 de résolution max (colonne « avg. #labels/categories » 54,2 k, extraction ambiguë, non reprise).

**Recettes de données des équipes (§4.3, §4.4, §4.5, §6.4, §8)** : le papier les cite sans ablation chiffrée, sauf mention contraire.
- Test multi-échelle : « most of the submitted methods use multi-scale testing » en 2018 (§4.4).
- Pyramides de caractéristiques et suppression des niveaux hauts du FPN pour les petits objets (HAL-Retina-Net, §4.4).
- Découpage en sous-images (sub-image splitting) et Mosaic, combinés à Cascade R-CNN avec convolutions déformables (CDNet, CascadeAdapt, 2020) (§4.4). Gain isolé : n/r.
- Active learning conduit avec augmentation (ACM-OD, 2019, AP 29,13) (§4.4) ; Mean Teacher pour entraîner Cascade DetectoRS (TAUN, 2020, AP 34,54) (§4.4). Gains isolés : n/r.
- Super-résolution (deep back-projection) pour agrandir l'image avant FPN déformable (DDFPN, 2018) (§4.4).
- SNIPER (chips de 512 × 512 échantillonnés sur une pyramide d'échelles) et Mosaic de YOLOv4 sont décrits comme stratégies générales (Fig. 3 / encart « other strategies ») ; ClusDet et AutoFocus pour la recherche de régions denses de petits objets (§4.3).
- Ensembles de détecteurs (DPNet : trois backbones) ; données externes autorisées si déclarées (§3). Les auteurs concluent qu'il est difficile d'apprendre des représentations de petits objets depuis ImageNet ou COCO génériques et appellent à des jeux dédiés (§8).
- Remède d'annotation proposé pour les foules d'objets occultés : une grande boîte avec un compte pour le groupe, car la NMS supprime des vrais positifs ; nécessiterait une métrique localisation + comptage (§4.5, Fig. 3). Segmentation grossière suggérée pour les objets non rigides (person, bicycle) (§4.5).

## Plateforme et implémentation

Aucune plateforme embarquée. Seule indication : les méthodes VID tournent à moins de 10 fps sur une GTX 1080Ti de station de travail (§5.3). Vitesse et puissance des autres tâches : n/r. Données et résultats : https://github.com/VisDrone/VisDrone-Dataset (Abstract) et http://www.aiskyeye.com/ (§3). Code des équipes : non publié dans le papier.

## Résultats

Protocole : AP COCO (AP@[.5:.95], AP50, AP75, AR1 à AR500) (§4.2). Meilleurs résultats du test-challenge DET (équipes tierces, pas des baselines des auteurs) :

| Édition | Méthode | AP | AP50 | Source |
|---|---|---|---|---|
| 2018 | HAL-Retina-Net | 31,88 | 46,18 | Table 2 |
| 2019 | DPNet-ensemble | 29,62 | 54,00 | Table 2 |
| 2020 | DroneEye2020 (Cascade R-CNN + DetectoRS) | 34,57 | 58,21 | Table 2 |

Autres tâches (équipes tierces) : VID DBAI-Det 29,22 AP en 2019 (Table 3) ; MOT COFE 61,88 AP en 2020 (Table 4) ; SOT SMILEv2 55,5 / 91,9 (succès / précision) sur le test-challenge 2019 (§6.4).

Baselines test-dev évalués par les auteurs, AP COCO (Table 2 puis Table 3) : DET CornerNet 23,43, Light-RCNN 22,08, FPN 22,06, Cascade R-CNN 21,80, DetNet 20,07, RefineDet 19,89, RetinaNet 18,94 ; VID FGFA 14,44, D&T 14,21, FPN 12,93, CenterNet 12,35, CornerNet 12,29, Faster R-CNN 10,25. Les détecteurs vidéo dépassent les détecteurs image (§5.3).

Points sur les petits objets : le meilleur détecteur 2020 reste sous 25 % de mAP sur person et bicycle (§4.5), toutes les méthodes VID sous 15 % sur ces deux classes (§5.4). Texte contre tableau : le §4.4 cite un Cascade R-CNN de base à 16,09 % de mAP pour le challenge 2020 alors que la Table 2 donne 21,80 sur test-dev ; les deux ensembles de test diffèrent, sans précision sur la configuration (incohérence apparente, non résolue).

Lignes ajoutées dans `benchmarks.csv` (proposées à l'agent principal) : 13 lignes, les baselines test-dev des auteurs en DET (7, Table 2) et VID (6, Table 3). Aucune ligne pour les équipes du challenge. Pas de plateforme, vitesse ni puissance (`n/r`), donc des lignes de précision seule.

## Limites et critique

- **Annotation peu documentée** : pas d'accord inter-annotateurs, pas de taux d'erreurs trouvées au contrôle croisé, pas d'outil ni de consignes détaillées publiées dans ce papier, pas de politique écrite pour les foules (chaque vélo occulté est une boîte, d'où le problème de NMS soulevé par les auteurs, §4.5). Le coût en heures n'est donné que pour l'ensemble du jeu (§8).
- **Pas de distribution de tailles chiffrée** ni d'AP_small dans les tableaux, malgré l'accent sur les petits objets ; effectifs par classe seulement en figures.
- **Recettes des équipes sans ablation** : augmentation, découpage et active learning sont cités comme composants d'une soumission complète, jamais isolés. Le gain d'un Mosaic ou d'un découpage ne peut pas être lu ici. Les gains en 2020 viennent aussi du cadre Cascade R-CNN et de DetectoRS (§4.4).
- **Protocole AP COCO** (moyenne sur IoU 0,5:0,95), non comparable aux mAP@0.5 souvent rapportés pour YOLO sur VisDrone. Les soumissions visent l'exactitude, pas l'efficacité (§8) : ensembles, test multi-échelle, inutilisables sur du matériel contraint.
- **Tables 2 et 3** : les colonnes AR sont décalées dans l'extraction ; seuls AP et AP50 sont repris. Table 1 également ambiguë.
- **Évolution des splits** : le test-challenge SOT change entre 2018 et 2019 (§6.1). Les images de test-challenge DET ne sont pas publiques (étiquettes cachées) ; les chiffres des papiers YOLO sont en général sur val ou test-dev.
- **Biais de domaine** (déduit) : drones grand public DJI, Chine seulement, scènes urbaines et routières, vue à altitude moyenne ; peu de classes d'objets rares.

## Pertinence pour cette base

**CONSTRUIRE.** Référence pour constituer un jeu de petits objets aériens : plusieurs villes, deux familles de capteurs DJI, lieux différents entre train / val / test (pas de fuite de scène entre splits, §3), test caché avec serveur d'évaluation, ordre de grandeur de coût (plus de 6 000 h pour 2,5 M de boîtes). À appliquer quand on prépare un split pour un jeu à scènes corrélées (vidéos, sites) : découper par lieu, pas par image. Le déséquilibre (40× à 50×) dit qu'un jeu réaliste de drone urbain est dominé par car et pedestrian ; prévoir des stratégies de classes rares (voir axe `imbalance-small`).

**ANNOTER.** Le schéma de labels est un modèle de consignes : 10 classes avec règle explicite pour les cas ambigus (pedestrian / person), classes rares exclues plutôt que mal étiquetées, occlusion en trois niveaux, troncature estimée à la main avec seuil d'exclusion de 50 % à l'évaluation, zones ignorées en vidéo, contrôle croisé. À appliquer pour tout jeu YOLO à foules ou petits objets où l'on veut mesurer par attribut. Le §4.5 pose la question non résolue de l'annotation de groupe (boîte + compte) contre une boîte par instance. Format de fichier YOLO : n/r dans ce papier.

**PRÉTRAITER.** Pas de résolution d'entraînement ni de tuilage chiffrés, mais la mention récurrente de découpage en sous-images, de test multi-échelle, de chips de 512 × 512 (SNIPER) et de super-résolution oriente vers le tuilage pour des images de 2000 × 1500 contenant des objets de quelques pixels. À rapprocher des fiches SAHI et ClusDet de la base ; l'ablation manque ici.

**AUGMENTER.** Les équipes 2020 les mieux classées combinent Mosaic et découpage avec Cascade R-CNN, et ACM-OD associe active learning et augmentation ; TAUN utilise Mean Teacher. Aucune ablation : ne pas citer ces gains comme mesurés. Utile surtout comme indice de ce qui se fait en pratique pour VisDrone, à vérifier par les papiers dédiés (Mosaic / Copy-Paste, tuilage).

**Qualité des labels.** Le jeu est annoté à la main et recoupé ; aucune estimation du bruit. À citer comme jeu de référence supposé propre, non audité ici.

## Gaps identifiés

- **Aucune ablation de données sur VisDrone-DET** dans ce papier : gain du Mosaic, du découpage, du multi-échelle, de l'active learning. À chercher dans les papiers dédiés de la base.
- **Pas de distribution de tailles ni d'AP_small chiffrés** : impossible d'en déduire la proportion d'objets sous 32 × 32 px.
- **Politique d'annotation des foules** : aucune évaluation de la boîte de groupe avec compte (§4.5, proposé seulement).
- **Qualité des labels VisDrone** : pas de mesure d'erreur ni d'accord ; à croiser avec la littérature sur les erreurs de benchmarks.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). Les figures (Fig. 2 effectifs par classe et occlusion, Fig. 4, Fig. 5, Fig. 6) ne sont pas lisibles : leurs valeurs sont `n/r`. Tables 2 et 3 : colonnes AR décalées, AP et AP50 lisibles. Table 1 partiellement ambiguë.

Déduit et non affirmé par les auteurs :
- la publication probable en revue ;
- l'ordre de grandeur du temps d'annotation par boîte ;
- l'absence de fuite de scène entre splits (le texte dit lieux différents, la conclusion pratique est la nôtre) ;
- le biais de domaine (Chine, DJI, urbain) ;
- l'incompatibilité des méthodes gagnantes avec un usage embarqué ;
- la non-comparabilité avec les mAP@0.5 des papiers YOLO ;
- le fait que les recettes d'augmentation des équipes n'ont pas été isolées par ablation (le papier n'en rapporte pas).
