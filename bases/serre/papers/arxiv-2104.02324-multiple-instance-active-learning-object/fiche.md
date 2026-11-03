---
id: arxiv-2104.02324-multiple-instance-active-learning-object
fiche: done
date: 2026-11-03
---

# Multiple instance active learning for object detection

Tianning Yuan, Fang Wan, Mengying Fu, Jianzhuang Liu, Songcen Xu, Xiangyang Ji, Qixiang Ye, 2021, arXiv preprint (CVPR-style, venue n/r dans `metadata.json`). https://arxiv.org/abs/2104.02324 (DOI : aucun)
Type : preprint non relu par les pairs

## Problème

Les méthodes d'active learning pour la détection résument l'incertitude de l'image par la moyenne (ou la somme) des incertitudes d'instances / de pixels ; or l'immense majorité des instances (~100k ancres par image, §3.3) est du fond, qui bruite l'incertitude d'image et la rend incohérente avec l'incertitude d'instance (§1, Fig. 1). Il manque une méthode d'active learning « au niveau instance » spécifique à la détection (§1, §2.2). Objectif : choisir quelles images faire annoter (§3.1).

## Méthode

Détecteur RetinaNet avec deux classifieurs d'instances adverses f1, f2 et un régresseur (§3.2), plus un classifieur MIL f_mil en parallèle (§3.3). Chaque image est un « sac » d'instances, les ancres de la feature map sont les instances.

- **IUL (instance uncertainty learning)** : l'incertitude d'une instance = écart de prédiction |f1 − f2| (Eq. 3). Phase « max » : g (extracteur) figé, f1/f2 ajustés sur le non-étiqueté pour maximiser l'écart tout en gardant la loss de détection sur l'étiqueté (Eq. 2). Phase « min » : f1/f2 figés, g minimise l'écart pour aligner distributions étiquetée / non étiquetée (Eq. 4). Plusieurs allers-retours par cycle (§3.2).
- **IUR (instance uncertainty re-weighting)** : le classifieur MIL produit un score de classe d'image (Eq. 5) ; une loss de classification d'image (Eq. 6) supprime les instances de fond ; l'incertitude est pondérée par ce score (Eq. 7-9). Sur le non-étiqueté, pseudo-labels d'image binarisés à 0,5 sur le score max d'instance (Eq. 10).
- **Sélection** : dans chaque image, somme des top-k incertitudes d'instance (k = 10k sur ~100k, λ = 0,5, §4.1 ; Tab. 4) ; les images retenues rejoignent l'ensemble étiqueté (§3.4). La mention « top-k » est dite sans préciser « somme » ou « moyenne » : formulation n/r.

Protocole d'active learning (§4.1) :

| Cadre | Init (aléatoire) | Pas par cycle | Budget final | Cycles |
|---|---|---|---|---|
| VOC07+12 trainval (16 551 images d'après §4.1 : 5011 + 11540), RetinaNet R50 | 5,0 % | 2,5 % | 20,0 % | 6 (déduit : 5,0 → 20,0 par pas de 2,5, 7 points, Tab. 3/4) |
| COCO train 117k, RetinaNet | 2,0 % | 2,0 % | 10,0 % | 4 (déduit, 5 points) |
| VOC, SSD VGG-16 (protocole LL4AL / CDAL) | 1k images | 1k images | n/r | n/r |

Entraînement par cycle : 26 epochs, batch 2, lr 0,001 puis 0,0001 après 20 epochs, momentum 0,9, weight decay 0,0001 (RetinaNet) ; SSD : 300 epochs, batch 32 (§4.1). Comparaison à random, entropy (entropie moyenne des instances), Core-set, LL4AL, CDAL ; 5 répétitions, moyenne, même graine (§4.1).

## Plateforme et implémentation

Entraînement / évaluation sur GPU TITAN V (§4.2) ; ni fps, ni latence, ni puissance rapportés (`power_scope` : n/r). Aucune cible embarquée : le coût porte sur l'entraînement par cycle. Code publié : https://github.com/yuantn/MI-AOD (abstract). Temps de calcul : Tab. 5 (corps non extrait ; le texte dit seulement que MI-AOD coûte moins que CDAL aux premiers cycles, §4.3).

## Résultats

Les courbes principales (Fig. 5 : VOC/RetinaNet, VOC/SSD, COCO/RetinaNet) sont des figures dont les valeurs ne sont pas dans `fulltext.md` ; seuls les écarts cités en texte sont lisibles.

- VOC, RetinaNet : MI-AOD dépasse l'état de l'art de 18,08 %, 7,78 % et 5,19 % à 5,0 %, 7,5 % et (probablement) 10,0 % d'images, et CDAL de 3,20 % en mAP à un autre budget (le texte du §4.2 est tronqué à cet endroit : budget du 5,19 % et du 3,20 % n/r avec certitude). Écarts en points de mAP supposés, la nature (points ou relatif) n'est pas précisée.
- VOC, SSD : meilleur que l'état de l'art « dans presque tous les cycles » (§4.2), valeurs n/r.
- COCO : écart sur Core-set +0,6 / +0,5 / +2,0 et sur CDAL +0,6 / +1,3 / +2,6 à 2,0 %, 4,0 %, 10,0 % d'images (§4.2). mAP absolue COCO n/r (figure).
- Valeurs absolues VOC/RetinaNet de MI-AOD complet (Tab. 4, ligne λ = 0,5, k = 10k ; colonnes 5,0 → 20,0 % d'images, lecture reconstruite du fragment) : 47,18 / 58,41 / 64,02 / 67,72 / 69,79 / 71,07 / 72,27 mAP.
- Aléatoire à 20 % : 67,09 mAP (§4.3) ; MI-AOD complet +5,18 pts (72,27 − 67,09, calcul de la fiche). Part des annotations : n/r (le papier ne l'exprime pas) ; lecture déduite : à 20 % MI-AOD dépasse l'aléatoire, mais l'économie à iso-mAP n'est pas calculée par les auteurs. L'aléatoire à 20 % étant à 67,09, le MI-AOD atteint ce niveau vers 12,5 % d'images (67,72, Tab. 4) selon une lecture approximative des deux sources, soit ~37 % d'annotations en moins : **déduit, non affirmé**.
- Entraînement avec 100 % des images : l'ajout d'IUR donne 78,37 vs 77,28 sans (+1,09, §4.3).
- Ablation (Tab. 1 sans corps, Tab. 3 lisible) : IUL seul +2,97 vs aléatoire à 20 % (70,06 vs 67,09, §4.3) mais ≈ aléatoire aux premiers cycles ; IUR améliore les trois premiers cycles de 5,04 à 17,09 pts (§4.3). Tab. 3 (IUR seul, mAP à 5,0 → 20,0 %) : poids 1/∅ 30,09 → 67,20 ; poids ŷf1/∅ 31,67 → 67,30 ; poids 1 sur X_L 42,52 → 68,32 ; poids ŷcls sur X 47,18 → 68,48. Le meilleur poids est le score de classification d'image. Noter que 70,06 (IUL, §4.3) et 67,20 (« IUL » §4.3 et Tab. 3 ligne 1) sont difficiles à concilier : incohérence ou configuration différente, n/r.
- Tab. 2 : IUL seul sur CIFAR-10 / ResNet-18, 2 % d'échantillons : 58,07 vs 51,01 (+7,06 pts, §4.3), hors détection.
- Hyperparamètres (Tab. 4) : λ = 0,5, k = 10k optimaux ; k = 1 → 70,33 à 20 %, k = 100 → 71,47, k = N → 72,03 ; λ = 0,2 → 72,06 ; fragment partiel (lignes de λ = 1 : 71,62).
- Analyse : MI-AOD sélectionne plus d'instances vraies positives à chaque cycle que les autres (Fig. 7, §4.4).

→ `benchmarks.csv` contient déjà 8 lignes de ce papier (importées de `yolo-data`, 7 budgets VOC/RetinaNet de 5,0 à 20,0 % d'images + 100 % des images ; Tab. 4 reconstruit et §4.3, confiance `medium`). Cette relecture propose les mêmes 8 valeurs avec les colonnes optionnelles renseignées (`chunk_id` 2104.02324#023.0 et #010.1, `metric_def`, `dataset_split`, `input_res`, `batch`) ; aucun remplacement fait ici. Pas de ligne COCO/SSD : valeurs en figure seulement.

## Limites et critique

- Preprint ; les chiffres COCO et SSD ne sont accessibles qu'en figure ou en écarts : impossible d'en tirer des valeurs absolues ici (`n/r`). Le budget exprimé en % d'images, pas en nombre de boîtes ni en temps d'annotation : on ne sait pas si les images sélectionnées sont plus coûteuses à annoter (plus d'objets).
- Détecteur RetinaNet R50 (anchor-based, focal loss), pas YOLO ; transfert aux détecteurs YOLO sans ancres / avec Mosaic non testé. Le pas de sélection est donné en pourcentage ; le budget initial de 5 % (≈ 800 images VOC) est déjà non négligeable.
- L'entraînement de MI-AOD (phases max/min, classifieur MIL) est plus complexe et ajoute un coût de calcul (Tab. 5, non lisible) ; l'économie d'annotation est à mettre en regard.
- Gains très élevés en « point de mAP » à 5 % (18,08) viennent de la faiblesse des baselines à très petit budget ; à budget élevé les écarts se resserrent (COCO +0,5 à +2,6 pts). La comparaison avec CDAL et LL4AL suit le protocole SSD de ces papiers (init 1k), pas celui de RetinaNet, donc les deux jeux de courbes ne sont pas comparables entre eux.
- Aucun test sur petit objets, domaines spécifiques (drone, industriel) ni sur des données déséquilibrées ; pas de validation avec de vrais annotateurs (les labels sont ceux du benchmark, supposés propres).
- Reproductibilité : code public, 5 répétitions moyennées, mais pas d'écarts-types dans le texte.

## Pertinence pour la base serre

Relu pour SerreIA (axe `active-labelling` ; l'axe `calibration-decision` déduit automatiquement est retiré : le papier ne traite ni calibration, ni seuils, ni OOD). Le papier est écrit pour la détection d'objets (RetinaNet, VOC/COCO), pas pour la classification de maladies ni pour des plantes : aucune donnée agricole (§4.1).

- **Apprentissage actif pour étiqueter des images de serre** : choisir quelles captures faire annoter quand le budget est serré (déduit : utile si le détecteur de feuilles du pipeline en deux étages doit être entraîné sur peu de boîtes ; gain surtout à petit budget, 5 à 10 % du pool, §4.2). Transfert à un classifieur (EfficientNet-B0) non testé ; seul indice : IUL seul sur CIFAR-10 / ResNet-18, +7,06 pts à 2 % d'échantillons (Tab. 2, §4.3).
- **Lien avec l'agrégation multi-instances** (question de recherche du profil) : le MIL ici sert à pondérer des incertitudes d'ancres pour choisir des images, pas à agréger des prédictions de feuilles en une décision par capture ; analogie de sac d'instances seulement (déduit).
- **Limites pour le projet** : pas de domaine de plantes, pas de petits objets feuillus, étiquettes de benchmark supposées propres ; coût d'entraînement par cycle (Tab. 5 illisible) à comparer à l'annotation d'une serre de petite taille, où le pool est peut-être trop petit pour que l'active learning vaille le coût (déduit). Code publié (https://github.com/yuantn/MI-AOD, abstract) : reproductible sur PlantDoc ou CCMT sans travail de recherche.

## Gaps identifiés

- Active learning sur images de plantes (feuilles, PlantDoc/CCMT, captures de serre) : aucune mesure ici ; gap pour l'axe `active-labelling`.
- Active learning avec un détecteur de la famille YOLO (sans ancres, Mosaic) : aucune mesure ici.
- Budget exprimé en boîtes ou en temps d'annotation, pas en pourcentage d'images.
- Combinaison active learning + pseudo-labels / SAM (annoter seulement ce qui est incertain, pré-annoter le reste).
- Domaines à petits objets (VisDrone) et classes déséquilibrées.

## Statut de lecture

papier complet (`fulltext.md` lu en entier, extraction grobid, ok ; fiche importée de `yolo-data`, parties factuelles revérifiées contre `fulltext.md`). Tab. 1, Tab. 4 (partiellement), Tab. 5 « sans corps extrait » : Tab. 1 et 5 illisibles (`n/r`), Tab. 4 et Tab. 3 reconstitués depuis des fragments (confiance moyenne : les colonnes sont supposées être 5,0 → 20,0 %). Fig. 5 (courbes principales) illisible. Un fragment orphelin « .18 56.94 64.44 67.70 69.58 70.67 72.12 » (probable ligne de Tab. 1) n'est pas attribuable : non utilisé.
Ce qui suit est déduit et non affirmé par les auteurs : nombre de cycles (6 VOC, 4 COCO) ; économie d'annotation (~12,5 % vs 20 %) ; lecture des colonnes de Tab. 4 ; budget du 5,19 % et du 3,20 % du §4.2 (texte tronqué) ; différence 5,18 pts à 20 % ; transferts à la serre (section Pertinence).
