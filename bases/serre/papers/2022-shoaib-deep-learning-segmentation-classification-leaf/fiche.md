---
id: 2022-shoaib-deep-learning-segmentation-classification-leaf
fiche: done
date: 2026-10-29
---

# Deep learning-based segmentation and classification of leaf images for detection of tomato plant disease

Muhammad Shoaib, Tariq Hussain, Babar Shah, Ihsan Ullah, Sayyed Mudassar Shah, Farman Ali, Sang Hyun Park, 2022, Frontiers in Plant Science 13. https://doi.org/10.3389/fpls.2022.1031748
Type : article de journal (relu par les pairs)

## Problème

Classer les maladies de la tomate sur PlantVillage en isolant d'abord la feuille du fond par segmentation (U-Net), pour que le classifieur apprenne sur la zone utile ; trois tâches : 2 classes (sain/malade), 6 classes (sain + 5 familles d'agents), 10 classes (sain + 9 maladies) (Abstract, #000.1 ; §Methodology, #007.0).

## Méthode

- Segmentation : U-Net original et « Modified U-Net » (23 couches de convolution), trois pertes (NLL, CE, MSE) ; masques de vérité terrain fournis avec PlantVillage (#008.0, #018.0).
- Classification : InceptionNet 1, 2, 3 (familles EfficientNet-like à échelle composée, Table 1), appliquées aux images segmentées ; Score-CAM pour visualiser la zone d'attention (#020.0).
- Données : PlantVillage tomate, 18 159 images + masques ; entraînement 13 082, validation 1 447, test 3 628 (Table 3, #033.0) ; validation croisée 5 plis pour la segmentation (#011.0) ; augmentation (rotation 5-15°, échelle, translation) pour équilibrer les classes (#010.0).
- Entraînement : SGDM, lr 1e-4, 45 époques (segmentation) / 50 (classification), batch 32 / 64 (Table 5, #034.0).

## Plateforme et implémentation

PC avec 64 Go de RAM et NVIDIA RTX 2080 Ti 11 Go, PyTorch, Python 3.7 (#014.1). Aucune mesure edge ; « inference time » défini comme temps de test d'une image (#016.0), unité non précisée (n/r). Puissance : n/r. Code et poids : non publiés (aucun lien trouvé dans le texte). Déploiement embarqué annoncé comme travail futur (#022.1).

## Résultats

- Segmentation (jeu PlantVillage, validation) : Modified U-Net + NLL : val. accuracy 98,88 %, IoU 98,65, Dice 98,91 (Table 6, #035.0) ; le texte et l'abstract donnent 98,66 / 98,5 / 98,73 (#018.0, #000.1) : incohérence interne. U-Net original : 96,33-96,62 % (Table 6).
- Classification sur images segmentées (Table 7, #036.0, #036.1) : 2 classes InceptionNet-2 99,92 ± 0,01 % (InceptionNet-1 99,74 ± 0,03) ; 6 classes InceptionNet-3 99,32 ± 0,14 % (InceptionNet-1 97,12 ± 0,9) ; 10 classes InceptionNet-2 99,90 ± 0,4 % (InceptionNet-1 99,61 ± 0,06). Le texte annonce d'autres valeurs : InceptionNet1 99,95 % (2 classes) et 99,12 % (6 classes), InceptionNet3 99,999 % (10 classes) (#019.1, #000.1, #021.1) ; contradiction avec la Table 7 non résolue.
- Apport de la segmentation : **aucun tableau ne compare images segmentées et non segmentées**. Le texte dit « when non-segmented pictures were used, the results were superior » (#019.0), formulation ambiguë (peut être une coquille pour « segmented »). Seul argument en faveur de la segmentation : Score-CAM, qualitatif, la segmentation aide à apprendre de « germane areas » (#020.0, Fig. 8-10).
- Table 4 sans corps extrait (formules des métriques seulement, #032.0).
→ reportés dans `benchmarks.csv` : 6 lignes (voir retour de l'agent, à coller par l'agent principal).

## Limites et critique

- Test **in-domain** : tirage aléatoire dans PlantVillage (3 628 images), même distribution que l'entraînement. Les auteurs reconnaissent que PlantVillage est collecté en un lieu et sur des variétés précises (#021.2). Pas de test hors domaine (PlantDoc, terrain).
- Fuite probable (déduit, non affirmé) : PlantVillage contient plusieurs vues de la même feuille ; aucune déduplication ni découpage par feuille n'est décrit, d'où des scores à 99,x % qui mesurent la mémorisation autant que la généralisation.
- Les images « non segmentées » de PlantVillage ont déjà un fond uniforme : l'ablation (absente) aurait de toute façon peu de signal sur le problème du fond de terrain.
- Chiffres contradictoires entre abstract, texte et tables (segmentation, Table 7) ; ablation segmentation/non-segmentation non chiffrée.
- Pas de calibration, pas de seeds multiples, intervalles « 90 CI » non définis ; pas de baseline sans segmentation ni d'autres architectures de référence.
- Table 8 (comparaison à l'état de l'art) non retrouvée dans le texte extrait ; non exploitée.

## Pertinence pour SerreIA

Pertinence moyenne et surtout négative : l'article ne démontre pas que la segmentation aide, et ses chiffres sont in-domain PlantVillage, donc non comparables aux résultats PlantDoc de SerreIA. Il confirme le cadre du problème (scores ~99 % sur PlantVillage) sans donner de parade à l'écart de domaine. Axe : `disease-classif`.

## Pour SerreIA

- **Comparabilité** : non. Test = 3 628 images PlantVillage tomate, tirage aléatoire (in-domain, entraînement PlantVillage) (#033.0) ; SerreIA teste hors domaine sur PlantDoc (rappel 0,986, précision 0,679, spécificité 0,50, ECE 0,13/0,30). Accuracy 99 % ici vs F1 classe 0,264 chez SerreIA : même ordre de grandeur de fossé que celui que SerreIA cherche à expliquer, pas un résultat comparable. Mono-culture (tomate), 10 classes, pas de classe « hors distribution ».
- **Ce qui est reprenable** : (1) l'idée « isoler la feuille avant de classer » correspond au second étage YOLOv8n de feuilles + classifieur (`vision/eval/two_stage.py`) ; l'article n'en prouve pas le gain, il faut le mesurer ; (2) Score-CAM pour vérifier que le classifieur regarde la feuille et non le fond : l'équivalent est `vision/eval/gradcam.py` à appliquer aux faux positifs PlantDoc/images saines, métrique : part de l'attention (masse Grad-CAM) tombant hors du masque feuille.
- **Expérience à faire** (que l'article n'a pas faite) : ablation à un seul facteur sur le test PlantDoc : EfficientNet-B0 sur image entière vs sur crop/masque de feuille (masque via U-Net ou SAM, ou remplacement de fond avec `data/backgrounds/`, à créer, appliqué dans `vision/datasets/augment.py`), avec le même entraînement PlantVillage+CCMT ; métriques : spécificité à rappel fixé, F1 classe, ECE avant/après temperature scaling (`vision/eval/temperature.py`, `cross_domain_eval.py`), et taux de faux positifs sur images saines (42 % à battre).
- **Coût edge** : le papier ne donne aucune latence embarquée (RTX 2080 Ti seulement) ; un U-Net en plus du classifieur n'est pas chiffrable pour RPi 5 + Hailo-8L ; ne rien en déduire pour le HEF INT8.
- **À éviter** : reprendre les 99 % comme objectif ; découper train/test par feuille/plante, pas par image, pour ne pas reproduire une fuite PlantVillage (cf. `vision/datasets/near_duplicates.py`).

## Gaps identifiés

- Aucun chiffre de gain de la segmentation/suppression de fond mesuré hors domaine dans ce papier : à reporter dans `gaps.md` (remplacement de fond et masque feuille sur PlantDoc).
- Pas de latence edge pour un pipeline segmentation + classification.

## Statut de lecture

Sections lues par recherche ciblée (pdb search/show) sans lecture intégrale de `fulltext.md` : Abstract, Introduction, Méthodologie, Données, Expériences, Résultats, Discussion, Conclusions, Tables 2 à 7. Extraction GROBID ok ; Table 4 sans corps extrait ; Table 8 non retrouvée ; Table 7 reconstruite par extraction, valeurs recoupées avec le texte (qui diverge).
Déduit et non affirmé par les auteurs : fuite de données possible entre train et test ; absence de gain démontré de la segmentation ; unité du temps d'inférence ; absence de code publié (non trouvé dans le texte).
