---
id: arxiv-2012.07177-simple-copy-paste-strong-data
fiche: done
date: 2026-10-05
---

# Simple Copy-Paste is a Strong Data Augmentation Method for Instance Segmentation

Golnaz Ghiasi, Yin Cui, Aravind Srinivas, Rui Qian, Tsung-Yi Lin, Ekin D Cubuk, Quoc V Le, Barret Zoph, 2020, arXiv preprint. https://arxiv.org/abs/2012.07177
Type : preprint non relu par les pairs (arXiv 2012.07177, publié ensuite à CVPR 2021 : à vérifier, non indiqué dans `metadata.json`)

## Problème

Annoter des masques d'instances est coûteux (22 heures d'annotateur par 1000 masques pour COCO, §1), et les modèles sont gourmands en données et faibles sur les classes rares. Les auteurs étudient systématiquement le Copy-Paste (coller des objets d'une image dans une autre) comme augmentation « object-aware », en contestant l'idée des travaux antérieurs (Contextual Copy-Paste, InstaBoost) qu'il faut modéliser le contexte visuel pour choisir où coller (§1, §2).

## Méthode

Recette complète (§3, Annexe A), très simple :

1. Tirer deux images au hasard ; appliquer à chacune un scale jittering aléatoire et un flip horizontal.
2. Choisir un **sous-ensemble aléatoire** des objets de l'image source et les coller à **positions aléatoires** sur l'image cible, sans modéliser le contexte : girafes et joueurs de foot à des échelles incohérentes sont acceptés (§3, Fig. 2). Environ la moitié des images générées ont des objets collés dans une scène « non appariée » intérieur/extérieur (46,8 %, Annexe C, Table 12).
3. Mettre à jour les annotations : supprimer les objets totalement occultés, recalculer masques et boîtes des objets partiellement occultés (§3).

Points de recette mesurés :

- **Sélection des objets** : coller un sous-ensemble aléatoire bat « un seul objet » et « tous les objets » de l'image source ; le hasard apporte un gain (Annexe A, Table 10 : valeurs non extraites).
- **Blending** : composition `I1×α + I2×(1−α)` avec α le masque binaire ; flou gaussien sur α pour adoucir les bords, mais **sans blending** les résultats sont identiques (§3, Annexe A). Le flou gaussien des objets collés « n'est pas bénéfique » ; pas de transformation géométrique type rotation (§2).
- **Scale jittering** : SSJ (0,8–1,25) ou LSJ (0,1–2,0), padding gris (Fig. 3). L'essentiel du gain de LSJ vient de son application à l'**image principale** ; élargir la plage sur l'image collée n'apporte que +0,3 box AP / +0,2 mask AP (Annexe A, Table 11, tableau à confiance moyenne). Avec SSJ sur l'image principale, le résultat baisse de 1,9 box AP.
- **Combinaison avec d'autres augmentations** : additif avec SSJ et LSJ (Fig. 5) ; **MixUp n'aide pas avec LSJ** et ne sert qu'en régime peu de données (§4.2, §4.3). Additif avec initialisation aléatoire comme avec pré-entraînement ImageNet, et avec des schedules plus longs (576 époques depuis zéro avec LSJ+Copy-Paste contre 96 avec SSJ, §4.1-4.2). Mosaic (YOLOv4) est cité comme apparenté à CutMix mais **jamais comparé** (§2).
- **Self-training Copy-Paste** : un modèle enseignant entraîné avec Copy-Paste pseudo-étiquette des images non annotées ; on colle des instances de vérité terrain sur images COCO et pseudo-étiquetées, puis on entraîne l'élève (§3, §4.4). Coller dans les deux types d'images est le meilleur (Table 3) ; coller des objets pseudo-étiquetés dans COCO n'apporte rien (§4.4).

## Plateforme et implémentation

Pas de matériel embarqué. Mask R-CNN (ResNet-50/101 ou EfficientNet-B7, FPN) et Cascade Mask R-CNN EfficientNet-B7 NAS-FPN ; batch 256, lr 0,32, sync BN, entraînement jusqu'à convergence (§4.1). Données : COCO (118k images), COCO non étiqueté (120k) et Objects365 (610k) pour le self-training, LVIS v1.0, VOC pour le transfert (§4.1). Surcoût : aucun à l'inférence, et aucun en entraînement selon les auteurs (§5), mais schedules nettement plus longs (§4.1). Code : l'extrait lu ne donne pas de lien (note de bas de page non reproduite dans `fulltext.md`) ; n/r.

## Résultats

Gains en détection (box AP) ; tous sur COCO val sauf mention contraire.

| Configuration | Sans Copy-Paste | Avec | Source |
|---|---|---|---|
| 7 modèles (R50/R101/Eff-B7, 640 à 1280 px), base LSJ | 47,2 à 52,9 | +1,0 à +1,5 box AP (moyenne +1,3), +0,8 mask AP | Table 1, §4.2 |
| Régime 10 % de COCO, Eff-B7 FPN 640 | SSJ / LSJ | +6,9 / +4,8 box AP | §4.3, Fig. 5 |
| 75 % de COCO + Copy-Paste + LSJ | = 100 % de COCO + LSJ (AP similaire) | efficacité en données ≈ x1,33 ; « 2× » vs SSJ (Fig. 1) | §4.3, §1 |
| Self-training (COCO val, Eff-B7) | 48,5 base ; self-training +1,5 | self-training + Copy-Paste 51,4 (+2,9) | §4.4, Table 3 |
| SOTA COCO test-dev, Cascade Eff-B7 NAS-FPN 1280 | 54,8 | 56,0 (Copy-Paste), 57,3 (+ self-training) ; 49,1 mask AP | Table 4 |
| Transfert VOC07 (pré-entraînement COCO) | 88,6 AP50 / 75,0 AP | 89,3 / 76,5 | Table 5 |

**Classes rares et longue traîne (LVIS v1.0, mask AP)** :

- Single-stage, Eff-B7 FPN 640 : Copy-Paste +1,6 AP, APr 9,7 → 12,8 ; RFS fait mieux sur APr (15,4) mais moins sur AP/APc/APf ; **RFS + Copy-Paste : 30,1 AP, APr 18,4 (+2,4 AP, +8,7 APr)** (Table 8, texte).
- Two-stage (class-balanced loss, β = 0,999, fine-tuning du classifieur seul) : Copy-Paste 33,0 AP, APr 27,3 (+2,3), APc +2,6 ; **RFS nuit** en deux étapes (30,1 AP) et RFS + Copy-Paste (32,0) est inférieur à Copy-Paste seul (Table 9).
- Modèles complets (Table 7) : Eff-B7 NAS-FPN 1280 passe de 34,7 à 38,1 mask AP, APr 26,0 → 32,1 (+6,1) ; ResNet-50 FPN : APr 22,2 → 26,5. APr 32,1 dépasse de +3,6 le vainqueur LVIS 2020 (28,5, sans TTA).
- COCO : Copy-Paste améliore tous les classes sauf « hair drier » ; les gains relatifs les plus forts concernent les classes de plus faible AP de base (moyenne de 5 runs, Fig. 6).

→ reportés dans `benchmarks.csv` : 33 lignes proposées dans `.cache/bench/arxiv-2012.07177-simple-copy-paste-strong-data.csv` (Table 1 ×14 en box AP COCO ; Table 4 ×3 ; Table 7 ×8 ; Tables 8 et 9 ×8, mask AP LVIS), à intégrer par l'agent principal.

## Limites et critique

- **Tâche = segmentation d'instances.** Le papier ne mesure jamais un détecteur bbox seul ni YOLO ; les box AP viennent de Mask R-CNN/Cascade, entraînés avec supervision de masques. Le transfert à une tête de détection est une inférence.
- **Le collage exige des masques.** Les auteurs calculent α à partir de masques de vérité terrain. Avec des boîtes seules, on colle le rectangle (comportement type CutMix / Cut-Paste), ce qui introduit du fond ; ce cas n'est pas évalué ici.
- **Coût d'entraînement caché** : schedules de 576 époques (contre 96) pour LSJ + Copy-Paste (§4.1), alors que les auteurs disent « pas de surcoût » (§5). Les comparaisons « entraîner jusqu'à convergence » favorisent les augmentations fortes ; budget de calcul égal non étudié.
- **Pas de comparaison avec Mosaic ni CutMix**, seulement avec MixUp (Fig. 5) : on ne sait donc pas si Copy-Paste bat Mosaic, augmentation par défaut de YOLO.
- **Résultats SOTA non strictement comparables** (le papier le dit : codebases, schedules et augmentations diffèrent, §4.5) ; comparaison à YOLOv4-P7 (55,8, TTA) faite à 1536 vs 1280 px.
- Gain sur classes rares LVIS fortement lié au rééquilibrage : en single-stage, Copy-Paste seul n'atteint pas RFS sur APr ; pas de mesure d'écart-type sauf Fig. 6 (5 runs). Pas de données sur de petits jeux (< 10 % COCO) ni sur de petits objets en particulier (Table 13 non extraite).
- Tables 5, 8 et 12 : corps lu mais « sans corps extrait » ou imparfait selon `extraction.warnings` ; Table 11 reconstruite par PyMuPDF (confiance moyenne). Table 10 (ablation du sous-ensemble et du blending) et Table 13 (tailles) sans chiffres exploitables : conclusions retenues du texte seul.

## Pertinence pour la thèse

**Pertinence pour le thème (données YOLO).**

- **AUGMENTER** : recette de référence pour Copy-Paste. Paramètres directement réutilisables : sous-ensemble aléatoire d'objets, positions aléatoires sans modèle de contexte, scale jittering large (0,1–2,0) **sur l'image principale**, flip, mise à jour des annotations (retirer les objets entièrement masqués, recadrer les boîtes des objets partiels), blending facultatif. En Ultralytics : paramètre `copy_paste` (nécessite des segments) à combiner à `scale` large ; à valider par ablation sur la cible.
- **Dans quel cas l'appliquer** : (1) peu de données (le gain croît quand le dataset diminue : +4,8 à +6,9 box AP à 10 % de COCO) ; (2) classes rares ou longue traîne (APr jusqu'à +6,1 en deux étapes, +8,7 avec RFS en une étape) ; (3) quand on peut s'offrir un entraînement long (le gain augmente avec les époques). Moins utile si Mosaic + scale jitter donnent déjà la diversité, ce que ce papier ne tranche pas.
- **Transposable à un détecteur bbox seul (déduit)** : le principe (coller des instances d'une image dans une autre, mélange avec scale jittering, mise à jour des boîtes par occultation) ne dépend pas de la tête de masque. Pour obtenir des masques à bas coût : SAM pour dériver un masque d'une boîte, ou polygones sur une fraction du jeu ; sans masque, coller des crops rectangulaires (risque de fond parasite, à tester). Les expériences sur la valeur de α et de la plage de scale sur l'image principale sont directement reprenables.
- **PRÉ-ANNOTER** : le self-training Copy-Paste est additif : coller des objets de vérité terrain sur des images pseudo-étiquetées (+2,9 box AP au total sur COCO, Table 3) ; **ne pas** coller des objets pseudo-étiquetés dans les images étiquetées (§4.4). Utile quand on dispose de beaucoup d'images non annotées.
- **CONSTRUIRE un dataset** : pour une nouvelle classe rare, annoter peu d'instances (masquées ou boîtes) et les coller sur des arrière-plans variés est une piste ; le papier montre le bénéfice sur LVIS mais ne teste pas explicitement « une classe nouvelle avec 10 exemples ».
- **PRÉTRAITER** : Copy-Paste avec LSJ sur 640 à 1280 px : les gains tiennent pour toutes les résolutions testées (Table 1) ; pas d'analyse spécifique aux petits objets.

## Gaps identifiés

- Copy-Paste vs Mosaic/MixUp/CutMix avec un détecteur type YOLO (bbox seul), à budget d'entraînement égal.
- Copy-Paste à partir de boîtes seulement, ou de masques SAM, sur les petits objets (VisDrone) : non mesuré.
- Interaction avec le rééquilibrage (RFS, class-balanced loss) : résultats contraires en une et deux étapes ; peu éclairé hors LVIS.
- Gain à très petit nombre d'instances par classe (< 100) : non mesuré (10 % de COCO reste ~11 800 images).

## Statut de lecture

Papier complet (`fulltext.md` lu en entier ; extraction GROBID). Tables 5, 8, 12 et la Table 10 sont partiellement illisibles : conclusions de l'Annexe A prises du texte. Table 11 reconstruite par PyMuPDF (confiance moyenne). Ce qui suit est déduit et non affirmé par les auteurs : transposabilité à un détecteur bbox seul, équivalence « 75 % de COCO + Copy-Paste ≈ 100 % + LSJ » exprimée en facteur ×1,33, le parallèle avec l'augmentation `copy_paste` d'Ultralytics, la publication à CVPR 2021, l'absence de lien de code.
