---
id: arxiv-1908.03195-lvis-dataset-large-vocabulary-instance
fiche: done
date: 2026-10-05
---

# LVIS: A Dataset for Large Vocabulary Instance Segmentation

Agrim Gupta, Piotr Dollár, Ross Girshick, 2019, arXiv preprint. https://arxiv.org/abs/1908.03195
Type : preprint non relu par les pairs (version à mi-parcours : 5k images val annotées deux fois pour l'analyse, release v0.5 de 82k images en annexe A ; le dataset final prévu fait 164k images et ~2 M de masques).

## Problème

La détection / segmentation d'instances est évaluée soit avec peu de catégories (80 dans COCO), soit avec beaucoup d'exemples par classe. Or la longue traîne est « inescapable » : annoter plus d'images ne fait que révéler de nouvelles catégories rares (§1). Il manque un benchmark à grand vocabulaire (>1000 catégories) où les exemples par classe sont rares. Deux verrous de construction : (1) l'évaluation est injuste quand un objet peut légitimement porter plusieurs étiquettes (chevauchement, parent-enfant, synonymes : « toy deer », car/vehicle, backpack/rucksack ; §2.1, Fig. 2) ; (2) annoter 164k images avec 1000+ catégories, exhaustivement, est infaisable et ambigu (§2.1).

## Méthode

**Principe « evaluation-first »** (§2) : définir d'abord tâche et métrique (segmentation d'instances, AP COCO), puis concevoir le pipeline de collecte qui produit exactement ce que l'évaluation exige.

**Dataset fédéré** (§2.2). Pour chaque catégorie c, deux sous-ensembles disjoints d'images : un ensemble positif P_c exhaustivement annoté pour c, et un ensemble négatif N_c où c n'apparaît pas. L'évaluation de c ne se fait que sur P_c ∪ N_c ; une détection de c hors de ce périmètre n'est pas évaluée. L'appartenance aux ensembles n'est pas divulguée au test : le détecteur doit prédire toutes les catégories partout. Effets : plus d'obligation d'annoter toutes les classes sur toutes les images (|P_c ∪ N_c| << |D|), sous-échantillonnage des classes fréquentes (person = 30 % de COCO ; pour LVIS, aucune catégorie ne devrait dépasser ~3 % des ~2 M d'instances estimées), et liberté de ne garder que les cas à accord inter-annotateurs suffisant.

**Annotations non exhaustives** (§2.3). Un booléen e_c^i par (image, catégorie) indique si l'exhaustivité est vérifiée : vrai dans 91 % des cas. Sinon (typiquement les foules), les faux positifs de c ne sont pas comptés sur cette image, mais le rappel l'est. Contraste avec COCO (max 10-15 instances + « crowd regions ») et Open Images v4 (label « group of c » à partir de 5 instances). Pas de traitement spécial de la hiérarchie : le détecteur doit sortir la catégorie la plus spécifique et les plus générales (canoe et boat). Synonymes : chaque catégorie est un synset WordNet.

**Pipeline d'annotation en 6 étapes** (§3.1, Fig. 4), sans algorithme d'apprentissage pour pré-annoter :
1. Object spotting : annotateur pointe un objet et le nomme (autocomplétion sur synonymes + définitions) ; image revisitée itérativement, retirée après 3 « skip » ; exécuté deux fois et seules les catégories nommées dans les deux passes sont gardées (accord sur le nom).
2. Marquage exhaustif des instances (points) : chaque paire (i, c) est envoyée à 5 annotateurs, qui vérifient la définition puis marquent toutes les instances ; ensemble positif plafonné à 1 % des images du dataset.
3. Segmentation : un annotateur vérifie la catégorie et dessine un polygone détaillé par instance.
4. Vérification de segments : jusqu'à 5 annotateurs notent le masque avec une grille ; rejet si 2 ou plus refusent (donc accepté si 4 sur 5 d'accord) ; boucle 3-4 répétée 4 fois sur les seuls rejetés ; >99 % des objets marqués obtiennent un masque de qualité.
5. Vérification de rappel complet : jusqu'à 5 annotateurs, 4 doivent juger l'annotation exhaustive, dès que 2 disent non le flag e_c^i passe à faux.
6. Négatifs : images tirées au hasard dans D \ P_c, jusqu'à 5 annotateurs demandent si c apparaît ; un seul « oui » rejette l'image ; cible |N_c| = 1 % des images.

**Contrôle qualité** : « gold set » inséré dans chaque étape (étapes 2-6) pour noter les annotateurs et router le travail vers les fiables ; tâche d'entraînement initiale et nombre moyen de sommets par polygone suivi à l'étape 3 ; taux de rejet de l'étape 4 comme indicateur de fiabilité ; les annotateurs peu fiables de l'étape 3 ne jugent pas à l'étape 4. En annexe A, pour la v0.5 : passe de contrôle manuelle par catégorie (vote inclure/exclure sur la cohérence visuelle) qui retire ~18 % des catégories et ~10 % des instances étiquetées.

**Vocabulaire** (§3.2) : 8,8k synsets WordNet (noms concrets) réduits par deux passes de spotting sur 10k images COCO, puis édition manuelle : 1723 synsets (borne supérieure du nombre de catégories).

**Classes rare / commune / fréquente** (§4.3) : définies par le nombre d'images d'entraînement contenant la catégorie : rare 1-10, commune 11-100, fréquente >100 ; sert aux AP désagrégés (AP_r, AP_c, AP_f).

## Plateforme et implémentation

Pas de plateforme matérielle (travail de dataset). Baselines : Mask R-CNN avec Detectron2 (promis open source « later this year »), puissance/FPS n/r. Données et annotations publiques : http://www.lvisdataset.org (release v0.5 ; challenge LVIS à ICCV 2019, annexe A). Code du pipeline d'annotation : non publié d'après le texte.

## Résultats

- **Statistiques** (5000 images, val COCO 2017 annotées deux fois ; §4.1) : 977 catégories, 11,2 instances et 3,4 catégories par image en moyenne, max 294 instances par image ; médiane de 9 instances par catégorie (longue traîne) ; objets plus petits que dans COCO (objets occupant presque toute l'image ~10x moins fréquents) ; distribution spatiale des centres plus diverse que COCO et Open Images (Fig. 5).
- **Release v0.5** (annexe A) : 82k images annotées (57k train, 20k test, 5k val), 1230 catégories après contrôle qualité, val 830 catégories et 51k instances, train 694k instances. ~75 % des catégories apparaissent dans 100 images d'entraînement ou moins. Répartition rare/commune/fréquente : train 25,6/36,9/37,5 % ; val 15,6/36,8/47,6 % ; test 28,6/29,5/41,9 % (Fig. 12, lecture du fragment de tableau ; val/test cités 15,1 % et 28,2 % de rares dans le texte, §C.1).
- **Reproductibilité du pipeline** (§4.2) : sur deux annotations indépendantes (étapes 2-5), IoU masque moyen 0,85 et F1 moyen 0,87 ; ~50 % des instances appariées ont un IoU >90 % ; ~75 % des paires (image, catégorie) ont F1 parfait. Appariement à IoU >= 0,5.
- **Qualité vs experts** (Table 1a, 100 instances de surface >32² px) : IoU masque moyen LVIS 0,90-0,92 (IC95 % bootstrap), contre 0,83-0,87 pour COCO et 0,84-0,88 pour ADE20K ; qualité de frontière moyenne 0,87-0,91 vs 0,77-0,82 (COCO) et 0,83-0,87 (ADE20K) ; complexité de frontière plus élevée (6,35-7,07 contre 5,59-6,04 pour COCO, Table 1b).
- **Validation du protocole fédéré** (Table 2) : trois Mask R-CNN COCO évalués sur les catégories COCO avec annotations LVIS ou COCO : mask AP 34,4 vs 34,1 (R50), 36,0 vs 36,0 (R101), 41,7 vs 41,2 (X101-64x4d) : le protocole fédéré creux redonne les résultats de l'annotation dense. Simulations sur COCO (Fig. 8) : AP baisse d'environ 2 points absolus quand |N_c| passe de 50 à 5k ; |P_c| de 80 suffit pour un AP stable. Entraîner Mask R-CNN sur 1k images fait passer le mask AP COCO val de 36,4 % à 9,8 % (§4.3).
- **Baselines v0.5** (annexe B, mask AP, Mask R-CNN R50-FPN) : réglage COCO par défaut (seuil de score 0,05, 100 détections/image) AP 14,8 %, AP_r 0,6-0,8 % (Table 3a) ; seuil 0 et 300 détections : AP 21,0 %, AP_r 3,2 % (5 runs) ; repeat factor sampling t = 0,001 : AP 23,2 %, AP_r 13,4 % (Table 3b) ; class-aware sampling : AP 18,7 %, AP_r 8,5 %, pire que le baseline sur AP_c et AP_f ; + scale jitter 24,4 % ; + R101 26,0 % ; + ResNeXt-101-32x8d 27,1 % (Table 3c).
- **Biais val/test** (§C) : à catégories fixes, l'AP baisse quand l'ensemble d'évaluation grandit (val 5k : 24,4 % AP pour R50 ; test 20k : 18,4 %, Table 4) car la proportion de catégories rares augmente ; le classement des trois modèles est conservé.

→ reportés dans `benchmarks.csv` : 6 lignes proposées (baselines Mask R-CNN du §B, Tables 3a-3c), détaillées dans `.cache/bench/` ; pas de FPS ni de puissance. Les valeurs de Tables 3b-3c sont à `confidence: high` mais le corps du Table 4 est fragmentaire (non repris).

## Limites et critique

- Preprint à mi-parcours : l'analyse porte sur 5k images (val COCO) et sur la v0.5 (~50 % du total prévu) ; les statistiques finales (164k images, ~2 M de masques) sont des cibles, pas des mesures.
- Le protocole fédéré suppose une collecte de négatifs vérifiés : ils sont tirés au hasard et plafonnés à 1 % des images ; avec peu de négatifs par classe, l'AP est sensible (baisse de ~2 points entre |N_c| = 50 et 5k) et biaisée à la hausse sur petits jeux d'évaluation (§C.2). Les catégories rares sont évaluées sur très peu d'exemples, d'où l'AP global seul renvoyé par le serveur d'évaluation (§2.3).
- Les accords inter-annotateurs sont mesurés au niveau du pipeline complet (IoU 0,85, F1 0,87), pas par classe : on ne sait pas si l'accord chute sur les classes rares ; la comparaison aux experts repose sur 100 instances de grande taille (>32² px) : les petits objets sont exclus.
- Pas de nombre d'heures ou de coût d'annotation rapporté dans le texte lu (n/r).
- Environ 18 % des catégories et 10 % des instances sont retirés par un jugement manuel de cohérence visuelle après coup (annexe A) : la qualité des catégories reste subjective.
- Les baselines utilisent des hyperparamètres d'inférence modifiés (seuil 0, 300 détections) : comparer avec un AP COCO à réglage par défaut est trompeur. Résultats sur LVIS non comparables aux métriques de détection par boîtes (YOLO) : ici AP de masque, avec flag d'exhaustivité.
- Aucune mesure sur des détecteurs de type YOLO ; transfert à la détection par boîtes déduit, non affirmé.

## Pertinence pour la thèse

Pour **CONSTRUIRE** un dataset de détection : le modèle fédéré est applicable à tout cas à nombreuses classes et peu de budget. On garantit l'exhaustivité par classe sur un sous-ensemble P_c et des négatifs vérifiés N_c, on sous-échantillonne les classes fréquentes (plafond ~1 % des images par classe), et on évalue sans pénaliser les classes non vérifiées par image. À appliquer quand le vocabulaire dépasse quelques dizaines de classes ou quand certaines classes sont ambiguës ou synonymes. Le format YOLO standard suppose au contraire que toutes les classes sont annotées dans toutes les images : un dataset fédéré exige une gestion de masque de perte par classe/image (déduit, non traité par le papier). **ANNOTER** : protocole en étapes séparées (spotting, marquage exhaustif, dessin, vérification, rappel, négatifs), vérification par vote d'annotateurs (4 sur 5), gold sets et suivi des taux de rejet : un modèle de contrôle qualité transférable à des annotations par boîte (les étapes 3-4 deviennent un dessin de boîte puis une vérification). Le flag « non exhaustif » pour les foules est une alternative aux crowd regions de COCO. **PRÉTRAITER / AUGMENTER** : peu direct ; seul levier de données testé : le repeat factor sampling (r_c = max(1, t/f_c) selon le texte de l'annexe B.2, voir remarque ci-dessous) qui fait passer AP_r de 3,2 % à 13,4 % ; à appliquer pour tout dataset déséquilibré (le papier le présente comme racine carrée inverse de la fréquence) ; le scale jitter apporte +1,2 AP (Table 3c). La partition rare/commune/fréquente (1-10, 11-100, >100 images) fournit un vocabulaire pour rapporter l'AP par fréquence de classe.

Remarque : le texte donne r_c = max(1, t/f_c) (annexe B.2) tout en parlant d'heuristique « racine carrée inverse » : la formule est probablement r_c = max(1, sqrt(t/f_c)) (déduit, la racine a pu être perdue à l'extraction) ; à vérifier avant d'implémenter.

## Gaps identifiés

- Nombre d'instances par classe nécessaire pour atteindre un AP donné pour un détecteur de type YOLO sur la longue traîne : non mesuré ici (AP_r 13,4 % avec Mask R-CNN seulement).
- Aucune étude de l'accord inter-annotateurs par classe ou sur petits objets ; aucune donnée de coût (temps/dollars).
- Formats : pas de traduction explicite d'un dataset fédéré vers des labels YOLO avec classes non annotées (masquage de la perte).

## Statut de lecture

Papier complet (fulltext.md lu en entier, extraction grobid ; Table 4 sans corps extrait, seulement un fragment ; figures sans légende : valeurs lues dans le texte). Corps des tableaux 1 à 3 non marqués « reconstruit » ; recoupés avec le texte (Tables 2 et 3).
Ce qui suit est déduit et non affirmé par les auteurs : l'application du modèle fédéré à des labels YOLO et au masquage de la perte, la transposition du pipeline à des boîtes englobantes, la pertinence pour des détecteurs de type YOLO.
