---
id: 2023-wu-laboratory-field-unsupervised-domain-adaptation
fiche: done
date: 2026-10-29
---

# From Laboratory to Field: Unsupervised Domain Adaptation for Plant Disease Recognition in the Wild

Xinlu Wu, Xijian Fan, Peng Luo, Sruti Das Choudhury, Tardi Tjahjadi, Chunhua Hu, 2023, Plant Phenomics 5, 0038. https://doi.org/10.34133/plantphenomics.0038
Type : article de revue (relu par les pairs)

## Problème

Un classifieur de maladies entraîné sur des images de laboratoire (PlantVillage, PVD : fond uni, une feuille) perd sa validité sur des images de terrain (fond complexe, plusieurs feuilles, flou, feuille partielle). Les auteurs veulent adapter le modèle sans étiqueter la cible (UDA), en visant trois difficultés qu'ils jugent absentes des UDA génériques : grand écart inter-domaines, grande variance intra-classe dans un domaine, frontières floues entre classes (2023-wu#000.0, résumé ; développé dans l'introduction).

## Méthode

MSUN (Multi-Representation Subdomain Adaptation Network with Uncertainty regularization), non adversarial. Un backbone CNN g, un module « Inception Adaptation Network » h (noyaux de tailles variées, représentations multiples), un classifieur c (2023-wu#006.0). Trois ajouts à la perte de classification : alignement des sous-domaines (par classe, avec pseudo-labels de la cible) par LMMD sur chaque représentation ; régularisation d'incertitude par minimisation d'entropie sur la cible (poids γ) ; pondération λ des pertes d'adaptation (2023-wu#010.0). Backbone ResNet-50 préentraîné ImageNet, pool5 comme représentation ; images 256 redimensionnées puis rognées 224, flip aléatoire ; SGD momentum 0,9, lot équilibré source/cible, 200 époques, lr du classifieur ×10, λ en rampe 0→1, γ par grille (0,1 retenu) (2023-wu#013.0, #013.1, #016.0). Toolflow : PyTorch 1.9.

## Plateforme et implémentation

Entraînement sur « NVIDIA GeForce GTX 3080TI » (sic, RTX 3080 Ti probable), 24 Go de RAM, i7-11700K (2023-wu#013.0). Temps d'entraînement, mémoire GPU et nombre de paramètres de h : n/r. Pas d'inférence embarquée : latence, FPS, puissance n/r. Code : non mentionné dans le texte lu.

## Résultats

Jeu source : PVD pour les 4 expériences ; cibles non étiquetées pendant l'entraînement : PlantDoc rogné (C-PD), Plant-Pathology (pommier, PP), Corn-Leaf-Diseases, Tomato-Leaf-Diseases (Kaggle). Métrique : exactitude (%) moyenne, comparaison à Baseline sans DA, DAN, D-CORAL, DANN, DAAN, DSAN, MRAN, tous en ResNet (2023-wu#012.0).
- PVD→C-PD : 5 601 images PlantDoc rognées retenues sur 8 897 (27 classes, 13 espèces), source réduite à 20 % de PVD (10 033 images) pour limiter le surapprentissage (2023-wu#011.1, #011.3, Table 1). Baseline 30,78 %, MSUN 56,06 % (Table 5, 2023-wu#030.0) ; meilleur concurrent DSAN 42,87 %.
- PVD→PP : baseline 39,27 %, MSUN 72,31 % (3 classes, Table 6, 2023-wu#031.0).
- PVD→Corn : baseline 75,96 %, MSUN 96,78 % (Table 7).
- PVD→Tomato : baseline 21,46 %, MSUN 50,58 % (5 classes, Table 8, 2023-wu#033.0).
- Ablation sur C-PD : +MUL-REP 41,26 ; +LMMD seul 43,59 ; les deux 51,65 ; +entropie 56,06 (Table 9, 2023-wu#034.0). L'entropie seule apporte 4,4 points.
→ reportés dans `benchmarks.csv` : 6 lignes proposées à l'agent principal (pas écrites ici).

## Limites et critique

- Le test est sur les mêmes images cibles non étiquetées que l'adaptation (transductif) ; aucun découpage train/test de la cible n'est décrit (n/r). Le gain mesure l'adaptation à ce lot précis, pas la généralisation à du terrain nouveau.
- Ne retient que des classes communes à PVD et à la cible, rognées par boîtes d'annotation PlantDoc (images aux boîtes erronées retirées à la main) : tâche fermée de classification de maladie par espèce, pas détection « sain/anormal ».
- Baseline faible et seul le ResNet-50 testé ; le gain se mesure par rapport à un source-only sans augmentation, sans remplacement de fond, sans préentraînement plus riche. Les parades « bon marché » ne sont pas comparées à l'UDA.
- Le Table 5 « Average » (56,06) est inférieur à toutes les colonnes d'espèces listées (seules 6 espèces sur 13 sont montrées) : moyenne sur 27 classes présumée, non décrite. Table 8 mal extraite (colonnes décalées, légende de tableau avec avertissement d'extraction) : chiffres par classe douteux, l'exactitude finale concorde avec l'ablation (Table 9).
- Résultats en exactitude seule, absolue de 56 % : inutilisable en pratique ; pas de calibration (ECE), de rappel/précision ni de seuil. Pas de variance sur plusieurs graines.
- Coût : les cibles doivent être disponibles à l'entraînement, 200 époques ; il faut réentraîner à chaque nouveau domaine.

## Pour SerreIA

Ce que le projet peut reprendre :
- **Méthode** : LMMD (alignement de sous-domaines par classe) et entropie sur la cible sont des pertes ajoutées à l'entraînement, indépendantes du backbone (calculées sur les features). Portage sur EfficientNet-B0 plausible dans `vision/train/train_classifier.py` et `vision/models/multihead.py` (déduit : le papier teste uniquement ResNet-50). Le module Inception h n'est utile que si on veut les « représentations multiples » ; il ajoute des paramètres, à ne pas garder si l'on veut un HEF simple.
- **Expérience à faire** : cible non étiquetée = images PlantDoc (ou photos réelles de la serre, sans étiquette) ; source = PlantVillage+CCMT ; comparer, dans `vision/eval/cross_domain_eval.py`, (a) baseline actuel, (b) entropie seule (la plus simple, +4,4 points ici), (c) DSAN/LMMD, (d) remplacement de fond prévu mais jamais testé. L'ordre d'effet de l'entropie et du LMMD (Table 9) dit où chercher le gain. Nécessite une évaluation sur un découpage de PlantDoc non utilisé pour l'adaptation, sinon le chiffre est flatté comme ici.
- **Métrique** : en plus de l'exactitude, garder le rappel, la précision, la spécificité, l'ECE de `vision/eval/metrics.py` et `temperature.py` : l'UDA peut améliorer l'exactitude tout en laissant le classifieur trop confiant. Ne pas adopter l'exactitude moyenne comme critère de réussite.
- **Edge** : si h est écarté à l'inférence (non précisé, à vérifier dans le code des auteurs), l'UDA ne coûte rien au déploiement Hailo-8L INT8 : seul l'entraînement change (déduit).
- **Comparabilité** : les chiffres du papier ne sont pas comparables à ceux de SerreIA. Test sur PlantDoc rogné (27 classes, 5 601 images) mais en exactitude multi-classe avec source réduite à 20 % de PVD, transductif, alors que SerreIA mesure rappel 0,986 / précision 0,679 / F1 0,264 en binaire sain/anormal, hors domaine strict, avec EfficientNet-B0 et PV+CCMT. Seule la qualitative se transfère : source-only sur PlantDoc s'effondre (30,78 % ici), l'UDA donne +25 points absolus dans le meilleur cas.

## Gaps identifiés

- Aucun gain d'UDA mesuré sur un backbone léger (EfficientNet, MobileNet) ni sous quantification INT8.
- UDA non comparée au remplacement de fond ni à l'augmentation de fond.
- Pas de calibration ni de rejet évalués après adaptation.
- Évaluation transductive : généralisation à des images de terrain non vues non mesurée.

## Statut de lecture

Papier complet lu par sections via `fulltext.md` (extraction grobid, ok ; tableaux Table 2 et un tableau de calcul sans corps extrait ; Table 8 à colonnes décalées par l'extraction).
Déduit et non affirmé par les auteurs : portabilité sur EfficientNet-B0 et coût nul à l'inférence ; moyenne de Table 5 sur 27 classes ; GPU = RTX 3080 Ti ; caractère transductif du test (aucun découpage décrit) ; code non publié (non trouvé).
