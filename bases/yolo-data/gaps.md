# Carte des gaps

Zones non couvertes et verrous repérés dans le corpus. Mis à jour par `/paper-gaps` à partir
des fiches `done` et de `benchmarks.csv`. Chaque gap cite les `paper_id` qui l'étayent et
distingue ce qui est lu de ce qui est déduit.

Format d'une entrée :

```
### <intitulé du gap>
- Constat : ce que montre le corpus (paper_id, section source).
- Ce qui manque : la question laissée ouverte.
- Statut : hypothèse (déduite de la bibliographie de départ) | étayé (fiches done).
- Piste : expérience ou lecture pour le confirmer.
```

---

Carte du 18/10/2026, **1ʳᵉ passe** : 44 fiches `done` et 425 lignes de benchmark (41 papiers ;
le survey `arxiv-1909.00169`, `arxiv-1708.02750` et `arxiv-2201.07425` n'ont pas de ligne).

**Portée des statuts.** « Étayé » signifie que plusieurs fiches constatent le manque dans les
papiers lus : mesure absente, limite reconnue par les auteurs, ou case vide de `benchmarks.csv`
recoupée par les sections « Limites et critique » et « Gaps identifiés ». Cela ne prouve pas que
le travail n'existe nulle part. Le corpus compte 44 papiers. Il reste biaisé par la sélection de
départ : des papiers fondateurs (2014-2023), beaucoup de Faster R-CNN, Mask R-CNN et RetinaNet,
et peu de YOLO récents. Un gap qui ne repose que sur l'absence d'un type de papier dans la base
reste une **hypothèse**. Les identifiants sont abrégés en `arxiv-AAMM.NNNNN` (préfixe du
`paper_id` complet, voir [INDEX.md](INDEX.md)) ; Objects365 s'écrit `2019-shao-objects365`.

### Chiffres de couverture (`benchmarks.csv`, 425 lignes)

| Constat | Valeur |
|---|---|
| Lignes dont le modèle est un YOLO | **42 / 425 (9,9 %)**, tirées de 7 papiers : YOLOv2 (`1612.08242`, `1803.11365`), YOLOv3 (`1804.02767`, `1902.04103`), YOLOv4 (`2004.10934`), YOLOv5 (`2406.05412`), YOLOv8m (`2309.11069`) |
| Lignes YOLOv5 ou plus récent (famille Ultralytics) | **15** (Select-Mosaic 10, Dynamic Tiling 5) ; un seul papier a pour toolflow Ultralytics |
| Familles de détecteurs | Faster R-CNN 135 · Mask R-CNN 67 · RetinaNet 45 · YOLO 42 · FCOS 16 · Cascade 16 · SSD 15 · (Grounding) DINO 15 · autres ou classification 74 |
| Lignes YOLO par axe | augmentation 23 · prétraitement 24 · imbalance-small 31 · datasets 7 · annotation 1 · synthetic-da 1 · **auto-labelling 0 · active-learning 0 · label-quality 0** (un papier peut relever de plusieurs axes) |
| Jeux | COCO 161 · VOC 59 · LVIS 42 · aérien 67 (VisDrone 34, DOTA 18, AI-TOD 8, UAVDT 6, xView 1) · conduite et autres domaines 77 · classification 19 |
| Domaine industriel / médical | **1 ligne** (jeu propriétaire de pièces automobiles, `2303.06999`) / **0** |
| Axe active-learning | 21 lignes, dont 20 sur VOC ; 0 sur YOLO, 0 sur un jeu aérien |
| Axe auto-labelling (semi-supervisé, modèles fondation) | 108 lignes, 66 sur COCO ; 0 sur YOLO, **0 sur un jeu aérien** |
| Lignes avec une précision par taille d'objet (AP_S, mAP_small, AP50s) | **29 / 425**, issues de 4 papiers (dont 23 de `1902.07296`) ; 2 seulement sur un YOLO |
| Lignes avec écart-type ou intervalle | **0** |
| `confidence` = medium | 225 / 425 (53 %), surtout des tableaux reconstruits à l'extraction |
| `baseline` = n/r | 51 / 425 |

Familles de détecteurs et de jeux déduites du texte libre des colonnes `model` et `dataset`
(regroupement approximatif, script en lecture seule).

---

## 1. Couverture croisée détecteur × technique × jeu

### Techniques de données jamais évaluées sur un YOLO
- Constat : aucune ligne YOLO pour Copy-Paste (`2012.07177`, Limites), la politique AutoAugment de
  détection (`1906.11172`, Gaps), le semi-supervisé (`2005.04757`, `2102.09480`, `2106.09018`,
  `2207.02541` : « Gaps identifiés » de chacun), l'active learning (`1801.05124`, `1905.03677`,
  `2103.10374`, `2104.02324`, Gaps), la correction ou la détection du bruit de labels
  (`2003.01285`, `2303.06999`, Gaps ; `2211.13993` n'entraîne que Faster R-CNN, Limites), la
  longue traîne (`2003.05176`, Gaps : ni EQL ni RFS sur YOLO), la randomisation de domaine
  (`1804.06516`, Gaps) et l'adaptation de domaine adversariale (`1803.03243`, Gaps). Seule
  `1803.11365` a une ligne YOLOv2 (DT+PL, 39,9 mAP sur Clipart1k), avec un gain plus petit que
  sur SSD (Pertinence).
- Ce qui manque : savoir si les gains mesurés sur détecteurs à deux étages ou à ancres se
  transposent à un YOLO à une étape, sans ancres, avec Mosaic et assignation dynamique. Plusieurs
  fiches notent que la méthode n'est pas transposable telle quelle : RoI pooling (`2003.01285`),
  propositions (`1801.05124`), perte par boîte à deux étages (`2303.06999`).
- Statut : **étayé** (≥ 12 fiches).
- Piste : reproduire 3 techniques (Copy-Paste, pseudo-labels hors ligne façon STAC, sélection
  CALD) sur un YOLOv8n/s Ultralytics, sur VOC puis sur VisDrone.

### YOLO récents : deux papiers, un jeu et un détecteur chacun
- Constat : les 15 lignes YOLOv5/v8 viennent de `2406.05412` (YOLOv5, une graine, gains
  +0,38 AP50 sur VisDrone, Limites) et de `2309.11069` (YOLOv8m, VisDrone seul, Table 1 non
  extraite, Limites). `1902.04103` « ne couvre pas Mosaic de YOLOv4/v5 ni les pipelines
  Ultralytics » (Limites) ; le survey date de 2019 et ignore YOLOv4+, ATSS/SimOTA/TAL
  (`1909.00169`, Limites).
- Ce qui manque : une ablation propre de la recette de données Ultralytics (Mosaic, MixUp,
  copy_paste, close_mosaic, échelle) sur des jeux variés.
- Statut : **étayé**.
- Piste : `/paper-discover "YOLO data augmentation ablation"` ; à défaut, ablation maison
  multi-graines.

### Domaines de déploiement absents (industriel, médical, infrarouge)
- Constat : 1 ligne industrielle, 0 médicale. Les fiches signalent que le transfert hors images
  naturelles n'est pas testé : `1906.11172` (aérien, industriel ; Limites), `1803.11365`
  (infrarouge, aérien, médical ; Limites), `2106.09018` (pas de décalage de domaine ; Limites),
  `2102.09480` (Gaps), `2303.05499` (ODinW proche de 0 sur les domaines éloignés ; Limites),
  `1805.00123` (industrie, EPI ; Gaps, déduit).
- Ce qui manque : les gains de chaque technique sur un jeu de domaine de quelques milliers
  d'images, cas typique d'un projet YOLO.
- Statut : **étayé** pour l'absence de test dans les papiers lus ; l'absence de papiers de
  domaine dans la base reste une hypothèse.
- Piste : requête OpenAlex « industrial defect detection YOLO dataset annotation augmentation ».

### Jeux aériens : seuls le tiling et Mosaic y sont mesurés
- Constat : les 67 lignes aériennes portent sur le tiling (`2202.06934`, `2309.11069`,
  `1904.08008`), Select-Mosaic (`2406.05412`) et les augmentations OBB de DOTA (`2102.12219`,
  Faster R-CNN seulement). VisDrone n'a aucune ablation de données (`2001.06303`, Gaps) ; UAVDT
  aucun test d'augmentation ou de rééquilibrage (`1804.00518`, Gaps). Copy-Paste sur VisDrone
  (`2012.07177`, Gaps), active learning sur petits objets (`2104.02324`, `2103.10374`, Gaps) et
  semi-supervisé aérien (`2207.02541`, `2106.09018`, Gaps) : non mesurés.
- Ce qui manque : semi-supervisé, active learning, Copy-Paste et nettoyage des labels sur
  VisDrone/DOTA avec un YOLO.
- Statut : **étayé**.
- Piste : pseudo-labels + tiling sur VisDrone-DET avec YOLOv8 (tuiles 640).

---

## 2. Interactions non mesurées

### Copy-Paste, Mosaic, MixUp et CutMix à budget égal
- Constat : Copy-Paste n'est comparé qu'à MixUp (`2012.07177`, Limites) ; CutMix n'est testé
  qu'en pré-entraînement de classification (`1905.04899`, Limites) ; mixup est l'astuce la plus
  rentable des BoF mais jamais face à Mosaic (`1902.04103`, Gaps) ; MixUp/DropBlock n'ajoutent
  rien à la politique apprise (`1906.11172`, Pertinence) ; MixUp ne vient pas de la détection
  (`1710.09412`, Gaps) ; le gain isolé de Mosaic n'est pas lisible (`2004.10934`, Limites).
- Ce qui manque : un plan factoriel des augmentations de mélange sur un YOLO, à nombre
  d'époques égal (les schedules de Copy-Paste montent à 576 époques, `2012.07177`, Limites).
- Statut : **étayé** (6 fiches).
- Piste : ablation 2×2×2 (Mosaic, MixUp, copy_paste) sous Ultralytics, 3 graines.

### Pseudo-labels et augmentations fortes de type YOLO
- Constat : le semi-supervisé utilise des augmentations fortes sans Mosaic, MixUp ni Copy-Paste
  (`2102.09480`, Pertinence ; `2005.04757`, Gaps : « Mosaic comme augmentation forte ? ») ;
  Dense Teacher n'est pas évalué sur YOLO avec Mosaic (`2207.02541`, Gaps) ; Soft Teacher ne
  sort pas de Faster R-CNN (`2106.09018`, Gaps). Seule interaction mesurée : Copy-Paste sur
  images pseudo-étiquetées, +2,9 box AP (`2012.07177`, Pertinence).
- Ce qui manque : la vue faible/forte quand l'augmentation de base d'un YOLO est déjà Mosaic.
- Statut : **étayé**.
- Piste : `/paper-discover "semi-supervised YOLO pseudo-label mosaic"`.

### Tiling × augmentation × recette d'entraînement
- Constat : SF (tuiles à l'entraînement) n'est comparé ni à Mosaic ni à Copy-Paste
  (`2202.06934`, Gaps) ; Select-Mosaic n'est comparé ni au tiling ni à Copy-Paste
  (`2406.05412`, Gaps) ; Dynamic Tiling garde Mosaic/MixUp à 20 % sans les isoler
  (`2309.11069`, Pertinence) ; le copy-paste de petits objets n'est pas comparé au tiling à coût
  de calcul égal (`1902.07296`, Gaps).
- Ce qui manque : pour les petits objets, savoir lequel des leviers rapporte le plus à coût égal
  (tiling, résolution d'entrée, Copy-Paste, Mosaic biaisé), et comment ils se combinent.
- Statut : **étayé** (4 fiches).
- Piste : sur VisDrone, YOLOv8 en 640 tuilé, 1280 plein cadre, + copy_paste, + Select-Mosaic.

### Bruit des labels × semi-supervisé, focal loss et assignation
- Constat : l'interaction entre boîtes manquantes et focal loss n'est pas mesurée (`1708.02002`,
  Gaps) ; la sensibilité d'ATSS au bruit des boîtes n'est pas testée (`1912.02424`, Gaps) ; la
  part de faux négatifs dans les pseudo-labels n'est pas quantifiée (`2005.04757`, Gaps) ; le
  seul bruit réel de `2003.01285` est un pseudo-labelling (Limites) ; seuil et calibration du
  teacher ne sont pas étudiés (`2106.09018`, Gaps).
- Ce qui manque : l'effet d'un jeu humain bruité sur la boucle de pseudo-labels d'un YOLO
  (amplification ou correction).
- Statut : **étayé**.
- Piste : injecter des drops/shifts (typologie de `2303.06999`) dans 10 % de COCO et lancer un
  semi-supervisé.

### Active learning × semi-supervisé, pré-annotation et augmentation
- Constat : la combinaison active learning + pseudo-labels/SAM est un gap explicite
  (`2104.02324`, Gaps) ; pas de comparaison des labels d'image à l'active learning
  (`1803.11365`, Gaps) ; l'effet de l'augmentation sur la mesure de stabilité LS n'est pas testé
  (`1801.05124`, Gaps) ; l'interaction avec l'augmentation d'entraînement non plus
  (`2103.10374`, Gaps).
- Ce qui manque : une boucle « pré-annoter le facile, faire annoter l'incertain » évaluée de bout
  en bout.
- Statut : **étayé**.
- Piste : `/paper-discover "active learning semi-supervised object detection"`.

### Rééquilibrage × augmentation de mélange
- Constat : l'interaction d'EQL avec Mosaic/Copy-Paste, qui changent la fréquence effective des
  classes, n'est pas étudiée (`2003.05176`, Gaps) ; Copy-Paste + RFS donne des résultats
  contraires en une et deux étapes (`2012.07177`, Gaps).
- Ce qui manque : une règle de rééquilibrage quand l'augmentation duplique déjà des instances.
- Statut : **étayé** (2 fiches).
- Piste : RFS ± copy_paste sur un sous-ensemble à longue traîne (LVIS-like) avec YOLO.

---

## 3. Régimes de données

### Gain selon la taille du jeu : courbes rares et bornées à ~5 000 images
- Constat : seule courbe explicite : AutoAugment de 5K à 23K images, RetinaNet entraîné de zéro
  (`1906.11172`, Gaps). Copy-Paste descend à 10 % de COCO, soit ~11 800 images (`2012.07177`,
  Gaps). Le semi-supervisé s'arrête à 1-10 % de COCO (`2207.02541`, `2106.09018`, Gaps). Pas de
  régime peu de données pour les BoF (`1902.04103`, Gaps), Mosaic (`2004.10934`, Gaps), le
  pré-entraînement Objects365 (`2019-shao-objects365`, Gaps : courbe 1K-100K non mesurée) ni
  CrowdHuman (`1805.00123`, Gaps).
- Ce qui manque : des gains mesurés sous 2 000 images, le régime courant d'un projet YOLO.
- Statut : **étayé** (7 fiches).
- Piste : courbe 250/500/1K/2K images × {aucune, Mosaic, Mosaic + copy_paste} sur un jeu de
  domaine.

### Nombre minimal d'images ou d'instances par classe
- Constat : non mesuré pour un YOLO sur la longue traîne (`1908.03195`, Gaps) ; pas de guide du
  nombre d'images annotées minimal par classe (`2102.09480`, Gaps) ; gain sous 100 instances par
  classe non mesuré (`2012.07177`, Gaps) ; nombre minimal d'images réelles après du synthétique
  non chiffré (`1804.06516`, Gaps). Le critère COCO de ~5 000 instances par catégorie est un
  critère d'inclusion, pas une mesure (`1405.0312`, Pertinence).
- Ce qui manque : la question de recherche n° 1 du profil n'a aucune réponse chiffrée dans la
  base.
- Statut : **étayé** (5 fiches).
- Piste : requête OpenAlex « how many training images per class object detection learning
  curve ».

### Petits modèles et cible embarquée
- Constat : Objects365 n'est testé ni sur YOLO ni sur modèles compacts (`2019-shao-objects365`,
  Limites et Gaps) ; SSD MobileNetV2 sature vers 1 M de boîtes alors que Faster R-CNN progresse
  (`1811.00982`, Pertinence) ; le gain de mixup est faible sur un petit modèle propre
  (`1710.09412`, Pertinence, déduit) ; aucun coût de tiling sur Jetson (`2309.11069`, Gaps) ;
  le coût linéaire de SAHI n'est pas chiffré (`2202.06934`, Limites).
- Ce qui manque : le profil cite l'embarqué, mais les techniques sont mesurées sur des modèles
  de 50 à 340 M de paramètres.
- Statut : **étayé** (5 fiches).
- Piste : refaire les ablations d'augmentation avec YOLOv8n contre YOLOv8l.

### Annoter quelques images cibles ou adapter le domaine
- Constat : aucun chiffre « supervisé sur la cible », donc pas d'équivalent en images annotées
  (`1803.03243`, Limites et Gaps) ; pas de comparaison à quelques centaines de boîtes cibles
  (`1803.11365`, Gaps) ; courbe de fine-tuning réel non lisible (`1804.06516`, Limites).
- Ce qui manque : le seuil à partir duquel annoter vaut mieux que l'adaptation de domaine ou le
  synthétique.
- Statut : **étayé** (3 fiches, tout l'axe synthetic-da).
- Piste : SIM10k → Cityscapes avec 0/50/200/1 000 images cibles annotées, YOLO.

---

## 4. Métriques et comparabilité

### AP par taille d'objet rarement rapporté
- Constat : 29 lignes sur 425. VisDrone ne donne pas d'AP_small (`2001.06303`, Limites et
  Gaps) ; Select-Mosaic revendique les petits objets sans AP_small (`2406.05412`, Limites) ;
  pas de mAP_small pour les BoF (`1902.04103`, Gaps) ; Table 13 (tailles) de Copy-Paste non
  extraite (`2012.07177`, Limites) ; SAHI en AP50 seulement (`2202.06934`, Limites).
- Ce qui manque : le gain sur petits objets des techniques censées les viser.
- Statut : **étayé**.
- Piste : exiger AP_S et AP_tiny (protocole AI-TOD) dans les ablations maison.

### Aucune variance, ablations à un seul run
- Constat : 0 ligne avec écart-type. Un seul run ou pas de variance : `1708.02002`,
  `1710.09412`, `1804.06516`, `1902.07296`, `1902.04103`, `1906.11172`, `1912.02424`,
  `2003.01285`, `2003.05176`, `2309.11069`, `2406.05412` (Limites de chacun). Les écarts discutés
  (0,1 à 0,6 point) sont souvent sous le bruit de graine probable. Exceptions : les folds de
  `2005.04757` (Table 1 seulement), `2207.02541` et `2102.09480` ; 3 à 5 essais en active
  learning (`1905.03677`, `2103.10374`, `2104.02324`), sans écart-type lisible.
- Ce qui manque : un ordre de grandeur du bruit de graine sur VOC, COCO et VisDrone pour
  départager les techniques.
- Statut : **étayé** (≥ 11 fiches).
- Piste : 5 graines d'un YOLOv8s de référence sur VOC et VisDrone.

### Réglages faits sur le jeu de test
- Constat : meilleure époque de test (`1710.09412`, Limites), meilleure performance pendant
  l'entraînement (`1905.04899`, Limites), arrêt quand le test sature (`1804.06516`, Limites), lr
  changé à cause de l'Ideal case (`1803.11365`, Limites), S choisi sur les mesures rapportées
  (`2406.05412`, Limites), validation corrigée différente par variante (`2211.13993`, Limites).
- Ce qui manque : des gains mesurés sur un test tenu à part.
- Statut : **étayé** (6 fiches).
- Piste : relever le split d'évaluation dans chaque nouvelle fiche.

### Gains annoncés incohérents avec les tableaux, gains relatifs présentés comme absolus
- Constat : SAHI, résumé contre Table 1 (« +6,8 AP » introuvable, `2202.06934`, Limites) ;
  AutoAugment, « plus de 70 % » contre +34 % (`1906.11172`, Limites) ; DA Faster, +8,6 contre
  8,8 (`1803.03243`, Limites) ; Soft Teacher, +1,8 contre +2,0 (`2106.09018`, Limites) ; STAC,
  résumé contre §4.2 (`2005.04757`, Limites) ; Select-Mosaic, +2,17 contre +1,51
  (`2406.05412`, Limites) ; LAAL, 96,5/81,9 % attribués à des jeux inversés et relatifs
  (`1801.05124`, Limites) ; les « 5 % » des BoF comparent à une autre implémentation
  (`1902.04103`, Limites) ; « 7,1 %/9,7 % » relatifs (`1902.07296`, Limites) ; pourcentages
  ambigus de CALD (`2103.10374`, Limites).
- Ce qui manque : toujours citer les tableaux, en points absolus.
- Statut : **étayé** (10 fiches).
- Piste : `bin/pdb bench --check` sur les lignes de ces papiers.

### Protocoles et baselines non comparables
- Constat : AP@0.7 sur UAVDT (`1804.00518`, Limites), mMR sur CrowdHuman (`1805.00123`,
  Limites), AP COCO sur VisDrone contre mAP@0.5 des papiers YOLO (`2001.06303`, Limites).
  Baselines faibles : flip + jitter seulement (`1906.11172`, Limites), grille sans recouvrement
  comme baseline de découpage (`1904.08008`, Limites). Budgets d'entraînement différents :
  `2012.07177`, `2102.09480` (STAC 6x contre 3x), `2202.06934` (SF ajoute des tuiles),
  `2207.02541` (schedules plus longs) (Limites).
- Ce qui manque : comparer entre papiers sans `bin/pdb bench --comparable` est trompeur.
- Statut : **étayé**.
- Piste : ajouter une colonne `iou_protocol` ou `epochs` à `benchmarks.csv` (proposition, à
  valider).

---

## 5. Coût humain de l'annotation

### Coût mesuré seulement sur des scènes simples
- Constat : coûts chiffrés dans 6 papiers : vérification oui/non, 1,6 s (`1602.08405`) ;
  extreme clicking, 7 s et ~150 $ pour 5 000 images (`1708.02750`) ; 7,4 s par boîte et 8,5 s en
  vérification (`1811.00982`) ; 14 s par masque SAM (`2304.02643`) ; 2,99 s contre 15,81 s par
  boîte avec tracker (`2201.07425`) ; heures globales COCO et VisDrone (`1405.0312`,
  `2001.06303`). Ils portent sur VOC, une instance par classe (`1708.02750`, `1602.08405`,
  Limites) ou sur des annotateurs formés (`1811.00982`, `2304.02643`, Limites). Coût n/r pour
  UAVDT (`1804.00518`, Gaps), CrowdHuman (`1805.00123`, Gaps), DOTA/OBB (`2102.12219`, Gaps),
  Objects365 (`2019-shao-objects365`, Gaps) et LVIS (`1908.03195`, Gaps).
- Ce qui manque : le coût par boîte en scène dense, sur petits objets, en vue aérienne et en
  OBB, cas où il est le plus élevé.
- Statut : **étayé** (≥ 8 fiches).
- Piste : chronométrer l'annotation de 50 images VisDrone en bbox, en OBB et avec SAM.

### Active learning compté en images, avec un oracle simulé
- Constat : budget en nombre d'images, pas en boîtes ni en temps (`1905.03677`, `2103.10374`,
  `2104.02324`, Limites et Gaps) ; annotation simulée par les labels du benchmark (`1801.05124`,
  Limites ; `2103.10374`, oracle parfait). La sélection peut favoriser les images à nombreuses
  boîtes (`1905.03677`, Limites, déduit).
- Ce qui manque : l'économie réelle d'heures d'annotation.
- Statut : **étayé** (4 fiches, tout l'axe).
- Piste : rejouer CALD en comptant les boîtes sélectionnées.

### Accord inter-annotateurs et coût de revue
- Constat : accord n/r pour Objects365, COCO (masques), CrowdHuman, UAVDT, DOTA et VisDrone
  (Limites de `2019-shao-objects365`, `1405.0312`, `1805.00123`, `1804.00518`, `2102.12219`,
  `2001.06303`) ; revue manuelle sans accord inter-relecteurs (`2303.06999`, Limites) ; temps de
  revue n/r (`2211.13993`, Gaps). Mesuré seulement dans `1811.00982` (IoU 0,87), `1908.03195`
  (IoU 0,85, F1 0,87, objets > 32² px seulement), `2304.02643` (85-91 %) et indirectement
  `1708.02750` (88 % entre experts PASCAL).
- Ce qui manque : le plafond de qualité atteignable sur petits objets et le coût d'un
  contrôle qualité.
- Statut : **étayé**.
- Piste : double annotation de 100 images d'un jeu maison, IoU par taille d'objet.

### Pré-annotation par modèle fondation : qualité des boîtes non mesurée
- Constat : la qualité des boîtes Grounding DINO comme pseudo-labels d'un YOLO n'est pas mesurée
  (`2303.05499`, Gaps) ; ni celle des boîtes issues des masques SAM (`2304.02643`, Gaps) ; pas
  de comparaison à SAM ou Grounding DINO (`2207.02541`, `1708.02750`, Gaps ; `1811.00982`,
  Pertinence « reste ouvert ») ; le biais d'un pré-annotateur sur le jeu final n'est pas mesuré
  (`2201.07425`, Gaps). Seule mesure : la vérification de boîtes d'un détecteur donne la même mAP
  (`1811.00982`, Pertinence).
- Ce qui manque : le meilleur point d'entrée d'un projet (zero-shot puis correction contre
  extreme clicking contre SAM au clic).
- Statut : **étayé** (6 fiches).
- Piste : `/paper-discover "auto-labeling Grounding DINO SAM YOLO training"`.

---

## 6. Qualité des labels

### Sensibilité d'un YOLO au bruit réel (objets manquants, boîtes lâches)
- Constat : la dégradation n'est chiffrée que sur Faster R-CNN, avec un bruit synthétique
  uniforme et sans objets manquants (`2003.01285`, Limites et Gaps) ; les erreurs simulées sont
  indépendantes de l'image (`2303.06999`, Limites) ; le bruit est une permutation symétrique en
  classification (`1710.09412`, Limites) ; le bruit résiduel d'Open Images n'est pas relié à la
  mAP d'un YOLO (`1811.00982`, Gaps) ; les boîtes manquantes sont les moins bien détectées
  (AUROC 0,71, `2211.13993`, Limites) ; aucun seuil de bruit en pixels pour les petits objets
  (`2003.01285`, Gaps).
- Ce qui manque : une table « taux de bruit → perte de mAP » pour YOLO, par type d'erreur et
  taille d'objet.
- Statut : **étayé** (5 fiches).
- Piste : injection contrôlée de drops/shifts/flips (typologie `2303.06999`) sur VOC avec
  YOLOv8.

### Gain réel du nettoyage
- Constat : aucun réentraînement sur labels corrigés (`2303.06999`, Gaps) ; le gain de CLOD est
  une borne haute, appariée à une version relue par des humains (`2211.13993`, Limites) ;
  rappel sur erreurs réelles inconnu (`2303.06999`, `2211.13993`, Gaps) ; pas de comparaison
  nettoyage contre perte tolérante au bruit (`2211.13993`, Gaps).
- Ce qui manque : combien de mAP rapporte une heure de revue guidée.
- Statut : **étayé** (2 fiches).
- Piste : relire les 2,8 % d'annotations signalées par CLOD sur un sous-ensemble et
  réentraîner.

### Consignes pour foules, occlusions, troncatures et très petits objets
- Constat : la boîte de groupe avec compte n'est pas évaluée (`2001.06303`, Gaps, §4.5) ; la
  boîte complète occultée est bruitée sans mesure d'accord (`1805.00123`, Gaps) ; l'usage des
  attributs Occluded/Truncated/GroupOf en perte n'est pas évalué (`1811.00982`, Gaps) ; pas de
  consigne pour objets tronqués et < 10 px (`2102.12219`, Gaps) ; seuil des zones ignorées non
  défini (`1804.00518`, Gaps) ; les erreurs dominantes viennent d'incohérences de consignes
  (`2211.13993`, Pertinence).
- Ce qui manque : l'effet mesuré de chaque consigne sur la mAP d'un YOLO, qui n'a ni
  `iscrowd` ni zone ignorée.
- Statut : **étayé** (6 fiches).
- Piste : VisDrone avec zones ignorées masquées ou converties en fond, YOLOv8.

### Labels partiels ou fédérés vers le format YOLO
- Constat : un jeu fédéré exige un masque de perte par classe et par image, absent du format
  YOLO (`1908.03195`, Pertinence et Gaps) ; une perte YOLO standard pénalise les classes non
  annotées comme fond (`1811.00982`, Limites, déduit) ; EQL dépend des négatifs image du
  protocole LVIS (`2003.05176`, Limites) ; le mélange d'images avec boîtes et d'images avec
  labels seuls n'a été validé que par une heuristique (`1612.08242`, Gaps).
- Ce qui manque : une recette pour fusionner des jeux aux classes différentes sous Ultralytics.
- Statut : **étayé** (4 fiches).
- Piste : requête OpenAlex « merging object detection datasets partial annotations missing
  labels ».

---

## 7. Prétraitement, ancres, augmentation, synthétique, déséquilibre

### Tiling : taille de tuile, recouvrement, boîtes coupées, fusion
- Constat : un seul réglage de tuile et de recouvrement par jeu (`2202.06934`, Limites ;
  `2102.12219`, Limites ; `2309.11069`, Gaps) ; règle pour les boîtes coupées n/r et pas de
  traitement des objets coupés (`2202.06934`, Pertinence et Limites ; `2102.12219`, Gaps ;
  `2309.11069`, Limites) ; fusion NMS jamais comparée à WBF ou Soft-NMS (`2202.06934`, Gaps) ;
  confusion entre tuilage et résolution effective, pas de comparaison à iso-calcul
  (`2202.06934`, Limites ; `1902.07296`, Gaps) ; cluster contre SAHI non comparé (`1904.08008`,
  Gaps).
- Ce qui manque : une règle de choix de tuile et de recouvrement selon la taille des objets,
  pour un export YOLO.
- Statut : **étayé** (5 fiches).
- Piste : grille tuile {320, 640, 1024} × recouvrement {0, 25, 50 %} sur VisDrone.

### Ancres k-means et assignation sur un jeu de domaine
- Constat : l'effet des ancres k-means est donné en IoU moyen, jamais en mAP (`1612.08242`,
  Gaps) ; le nombre d'ancres n'est pas ablaté (`1804.02767`, Gaps) ; la méthode des ancres
  optimisées n'est pas décrite (`2004.10934`, Gaps) ; +10 % d'AP par réglage des ancres, sans
  détail (`1804.00518`, Limites) ; ATSS n'est pas comparé aux ancres k-means de YOLO
  (`1912.02424`, Gaps) ; les seuils IoU d'assignation ne sont pas ablatés (`1708.02002`, Gaps).
- Ce qui manque : savoir s'il faut encore recalculer les ancres quand l'assignation est
  dynamique (TAL, SimOTA), et l'effet sur les petits objets.
- Statut : **étayé** (6 fiches) ; l'absence de papier TAL/SimOTA est une hypothèse (voir §8).
- Piste : YOLOv5 ancres COCO contre ancres k-means sur DOTA-HBB ou VisDrone.

### Mosaic : paramètres et effet isolé non documentés
- Constat : paramètres de Mosaic non décrits, cases d'ablation perdues (`2004.10934`, Limites) ;
  effet selon la taille du jeu et des objets absent (`2004.10934`, Gaps) ; les augmentations de
  YOLOv2/v3 ne sont pas documentées (`1612.08242`, Limites ; `1804.02767`, Gaps) ; gain de
  Select-Mosaic dans le bruit (`2406.05412`, Limites).
- Ce qui manque : l'effet de Mosaic seul sur un petit jeu, et la date à laquelle l'arrêter
  (close_mosaic).
- Statut : **étayé** (4 fiches).
- Piste : relire la Table 4 de YOLOv4 sur le PDF (hors règle de base, à demander) ou faire
  l'ablation maison.

### Copy-Paste sans masques
- Constat : le collage exige des masques ; avec des bbox seules, le fond est embarqué et non
  testé (`1902.07296`, Limites ; `2012.07177`, Limites et Gaps) ; dériver des masques avec SAM
  est une idée déduite (`2304.02643`, Pertinence ; `2012.07177`, Pertinence).
- Ce qui manque : le cas courant d'un jeu YOLO en bbox seules.
- Statut : **étayé** (3 fiches).
- Piste : comparer copy_paste rectangle, masques SAM et polygones sur un jeu bbox.

### Synthétique : une classe, brouillard simulé, pas de génératif
- Constat : l'axe ne compte que 3 papiers (36 lignes, une ligne YOLO). DR testé sur la voiture
  seule et 500 images KITTI (`1804.06516`, Limites) ; brouillard simulé seulement (`1803.03243`,
  Gaps) ; DR multi-classes et YOLO non couverts (`1804.06516`, Gaps) ; pas de comparaison à un
  Copy-Paste de vrais objets (`1804.06516`, Gaps).
- Ce qui manque : synthétique multi-classes pour un YOLO, et données issues de modèles
  génératifs (diffusion).
- Statut : **étayé** pour l'étroitesse des tests ; **hypothèse** pour le génératif (aucun
  papier dans la base).
- Piste : requête OpenAlex « diffusion model synthetic data object detection training ».

### Déséquilibre de classes pour un YOLO à peu de classes, mesure du déséquilibre
- Constat : aucun papier ne mesure les remèdes de classification (sur-échantillonnage,
  class-balanced) sur un YOLO ; la mesure quantitative du déséquilibre d'un jeu est une question
  ouverte (`1909.00169`, Gaps, §9.2) ; EQL et RFS ne sont pas testés sur YOLO ni pour un jeu à
  peu de classes (`2003.05176`, Gaps et Pertinence) ; la formule de RFS est à vérifier
  (`1908.03195`, Pertinence) ; la focal loss ne traite que le déséquilibre avant/arrière-plan
  (`1708.02002`, Gaps) et a coûté ~2 points à YOLOv3 (`1804.02767`, Pertinence).
- Ce qui manque : une règle « quand rééquilibrer » pour un jeu de 5 à 20 classes.
- Statut : **étayé** (5 fiches).
- Piste : lire « Class-balanced loss based on effective number of samples » (voir Pistes).

### Remèdes signalés manquants par le survey
- Constat : `1909.00169` (Pertinence, liste « Manquants dans la base ») : OHEM, GHM, PISA,
  Libra R-CNN, SNIP/SNIPER, pertes IoU (GIoU, CIoU), Guided Anchoring/FreeAnchor,
  class-balanced loss, SMOTE adapté à la détection, synthèse GAN et PSIS, assignation
  hongroise (DETR). Ses questions ouvertes : orientation et position des objets comme
  déséquilibre (§6.5), consensus sur le seuil IoU positif/négatif (§9.3).
- Ce qui manque : ces papiers dans la base, surtout SNIP/SNIPER (justification de la résolution
  et du tiling).
- Statut : **hypothèse** (absence dans la base, signalée par une seule fiche).
- Piste : `bin/pdb base scan`, puis `/paper-add` pour SNIP et SNIPER (cités dans
  `external_refs.csv`).

### Code et outils non publiés
- Constat : code de méthode non publié ou non trouvé : `1602.08405`, `1708.02750`, `1710.09412`,
  `1801.05124`, `1803.03243`, `1804.06516`, `1902.07296`, `1905.03677`, `2003.01285` (annoncé),
  `2012.07177`, `2103.10374`, `2309.11069` (section « Plateforme et implémentation » de chacun).
  Les outils d'annotation sont rarement publiés : interface COCO n/r (`1405.0312`), outil SAM
  propriétaire (`2304.02643`), SATA n/r (`2201.07425`), pipeline LVIS non publié
  (`1908.03195`). Les modèles d'Open Images sont internes à Google (`1811.00982`). Code publié et
  vérifiable : SAHI, CLOD (GPL v3), MI-AOD, Dense Teacher, STAC, EQL, ATSS, GluonCV (BoF),
  Darknet, Grounding DINO, SAM.
- Ce qui manque : tout l'axe active learning, sauf MI-AOD, et le copy-paste de petits objets
  sont à réimplémenter.
- Statut : **étayé** (12 fiches).
- Piste : avant tout essai, privilégier les techniques à code publié (SAHI, CLOD, MI-AOD).

---

## 8. Thèmes du profil sans papier dédié

Tous ces gaps sont des **hypothèses** : le profil les annonce, mais aucun papier de la base ne les
traite. Les fiches ne les évoquent qu'en passant ou par déduction.

### Format des labels YOLO et conversion
- Constat : les conversions sont toujours « à faire, déduit » : `iscrowd` absent du format
  Ultralytics (`1405.0312`, Pertinence) ; boîte complète qui sort de l'image (`1805.00123`,
  Pertinence) ; boîtes `[x, y, w, h]` en pixels (`2201.07425`, Pertinence) ; format YOLO n/r
  (`2001.06303`, Pertinence). Aucune mesure des erreurs de conversion (clipping, arrondis,
  classes décalées).
- Statut : **hypothèse**.
- Piste : requête OpenAlex « annotation format conversion errors object detection dataset
  YOLO ».

### Letterbox contre redimensionnement simple
- Constat : le mot n'apparaît que dans deux fiches, comme une absence (`1708.02002`,
  Pertinence) ou une déduction (`1803.03243`, Pertinence) ; SAM utilise un padding 1024
  (`2304.02643`, Pertinence).
- Statut : **hypothèse**.
- Piste : requête OpenAlex « letterbox resizing aspect ratio object detection accuracy ».

### Split train/val/test et fuites entre splits
- Constat : les bonnes pratiques sont décrites mais jamais mesurées : split par photographe et
  par date (`1405.0312`), par séquence et par lieu (`1804.00518`, `2001.06303`), par scène
  (Kitti dans `2303.06999`) ; risque de fuite avec le split aléatoire de xView (`2202.06934`,
  Limites, déduit).
- Statut : **hypothèse** (deux fiches signalent le risque par déduction, aucune ne le mesure).
- Piste : sur UAVDT, comparer un split aléatoire par image et un split par séquence.

### OBB pour YOLO
- Constat : DOTA recommande l'OBB pour les objets tournés et denses, mais uniquement avec
  Faster R-CNN (`2102.12219`, Limites) ; pas de comparaison OBB contre HBB à coût d'annotation
  égal (`2102.12219`, Gaps) ; le survey cite l'orientation comme déséquilibre ouvert
  (`1909.00169`, Gaps).
- Statut : **hypothèse**.
- Piste : requête OpenAlex « oriented bounding box YOLO aerial annotation HBB versus OBB ».

### Vidéo contre images isolées
- Constat : les images successives sont corrélées et gonflent le jeu sans diversité
  (`2201.07425`, Pertinence ; `1804.00518`, Limites, déduit) ; risque de doublons en active
  learning sur vidéo (`1905.03677`, Pertinence, déduit).
- Ce qui manque : un taux d'échantillonnage des images de vidéo pour un YOLO.
- Statut : **hypothèse**.
- Piste : requête OpenAlex « frame sampling video object detection training set redundancy ».

### Images de fond et part d'images sans objet
- Constat : le déséquilibre avant/arrière-plan relève de la perte, pas de la collecte
  (`1708.02002`, Pertinence, déduit) ; DOTA inclut des images à faible ratio d'objets
  (`2102.12219`, Pertinence) ; l'effet de la sur-représentation des négatifs vérifiés n'est pas
  testé (`1811.00982`, Gaps).
- Statut : **hypothèse**.
- Piste : requête OpenAlex « background images negative samples proportion YOLO training ».

### Assignation dynamique (TAL, SimOTA) et YOLO sans ancres
- Constat : plusieurs fiches renvoient à TAL ou SimOTA « à chercher » (`1708.02002`,
  `1804.02767`, `1912.02424`, `1902.07296`), sans papier dans la base.
- Statut : **hypothèse**.
- Piste : `/paper-discover "task-aligned assignment SimOTA YOLOX"`.

### Détecteurs à vocabulaire ouvert récents et distillation vers un YOLO
- Constat : seul Grounding DINO est dans la base ; la distillation de ses sorties vers un YOLO
  est déduite, non testée (`2303.05499`, Pertinence).
- Statut : **hypothèse**.
- Piste : requête OpenAlex « open-vocabulary detector pseudo-labels distillation real-time
  detector ».

---

## Pistes de lecture

Titres tirés de `external_refs.csv` (travaux cités par le corpus, absents de la base) ou requêtes
OpenAlex. Métadonnées à vérifier avant ajout.

1. « An analysis of scale invariance in object detection - SNIP » (2018) et « Sniper: Efficient
   multi-scale training » (2018) : justification de la résolution et du tiling (§7, survey).
2. « Cut, paste and learn: Surprisingly easy synthesis for instance detection » (2017) et
   « Modeling visual context is key to augmenting object detection datasets » (2018) :
   Copy-Paste sans modèle 3D, avec ou sans contexte (§7, Copy-Paste et synthétique).
3. « Training object detectors with noisy data » (arXiv 1905.07202) et « Pervasive label errors
   in test sets destabilize machine learning benchmarks » (arXiv 2103.14749) : bruit réel des
   labels (§6).
4. « Class-balanced loss based on effective number of samples » (2019) : rééquilibrage (§7).
5. « xView: Objects in context in overhead imagery » (arXiv 1802.07856) : jeu aérien utilisé par
   SAHI, absent de la base (§1, aérien).
6. « Best of both worlds: human-machine collaboration for object annotation » (2015) : coût de la
   pré-annotation avec humain dans la boucle (§5).
7. OpenAlex : « YOLOv5 YOLOv8 data augmentation ablation mosaic mixup copy-paste small dataset »
   (§1, §2).
8. OpenAlex : « semi-supervised object detection YOLO one-stage pseudo-label » et « active
   learning YOLO annotation cost » (§1, §2).
9. OpenAlex : « number of training images per class object detection learning curve » (§3).
10. OpenAlex : « oriented bounding box YOLO annotation » et « train test leakage object detection
    video frames split » (§8).
