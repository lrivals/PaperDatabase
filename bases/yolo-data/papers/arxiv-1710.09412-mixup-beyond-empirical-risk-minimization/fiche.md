---
id: arxiv-1710.09412-mixup-beyond-empirical-risk-minimization
fiche: done
date: 2026-10-05
---

# mixup: Beyond Empirical Risk Minimization

Hongyi Zhang, Moustapha Cisse, Yann N Dauphin, David Lopez-Paz, 2017, arXiv preprint (la version lue porte l'en-tête « Published as a conference paper at ICLR 2018 »). https://arxiv.org/abs/1710.09412
Type : preprint non relu par les pairs selon `metadata.json` (publication ICLR 2018 indiquée dans l'en-tête du texte, venue non reportée dans les métadonnées : à vérifier).

## Problème

Les grands réseaux entraînés par minimisation du risque empirique (ERM) mémorisent les données, y compris les labels corrompus, et sont sensibles aux exemples adversariaux (Résumé, §1). Les auteurs proposent une augmentation « vicinale » générique, indépendante du domaine. Papier de **classification** : la base ne le garde que comme augmentation transférable à la détection (profile.md, « Inclus »).

## Méthode

Recette (§1-2, Fig. 1a) :

- On forme des exemples virtuels `x = λ·x_i + (1-λ)·x_j`, `ỹ = λ·y_i + (1-λ)·y_j`, avec `y` en one-hot, et `λ ~ Beta(α, α)`, `α ∈ (0, ∞)`. α règle la force de l'interpolation ; α → 0 redonne l'ERM (§2).
- Implémentation : quelques lignes de PyTorch ; un seul minibatch est mélangé avec sa propre permutation aléatoire (une seule file de données, même résultat que deux chargeurs, I/O réduite) (§2).
- Variantes testées en préliminaire : combinaison de 3 exemples ou plus (Dirichlet) sans gain supplémentaire mais plus coûteuse ; interpoler seulement entre exemples de même classe ne donne pas le gain de mixup (§2, Table 5).

**Choix de α** (mesuré) :

| Cadre | α | Source |
|---|---|---|
| ImageNet-2012 | 0,1 à 0,4 améliore l'ERM ; α grand sous-apprend ; utilisé : 0,2 (ResNet-50/101), 0,4 (ResNeXt-101) | §3.1, Table 1 |
| CIFAR-10/100 | α = 1 (λ uniforme sur [0,1]) | §3.2 |
| Google commands | 0,1 ou 0,2 ; 5 époques de warm-up sans mixup | §3.3 |
| Labels corrompus CIFAR-10 | 8 à 32 (essais : 1, 2, 8, 32) | §3.4 |

Tendance (§5) : quand α augmente, l'erreur d'entraînement sur données réelles monte et l'écart de généralisation baisse. Les auteurs n'ont pas de théorie du « sweet spot » et conjecturent que les modèles de plus forte capacité tolèrent mieux un grand α (§5). Les modèles de plus forte capacité ou entraînés plus longtemps profitent le plus (§3.1).

## Plateforme et implémentation

Entraînement : Caffe2, minibatch 1 024, données parallèles pour ImageNet (GPU non précisé) ; PyTorch sur un Nvidia Tesla P100 pour CIFAR (§3.1-3.2). Le surcoût de calcul est présenté comme minimal (§2, §5), sans mesure chiffrée. Code : seul l'extrait de la Fig. 1a est dans le papier ; aucun dépôt cité dans le texte lu (cité à `n/r`).

## Résultats

Erreurs en % (plus bas = mieux), mixup contre ERM.

- **ImageNet-2012, top-1 (Table 1, extraction PyMuPDF/GROBID à vérifier)** : ResNet-50 90 ép. 23,5 → 23,3 ; ResNet-101 90 ép. 22,1 → 21,5 ; ResNeXt-101 64x4d 90 ép. 20,4 → 19,8 ; à 200 ép. : ResNet-50 23,6 → 22,1, ResNet-101 22,0 → 20,8, ResNeXt-101 32x4d 21,3 → 20,1. Le gain croît avec la capacité et la durée d'entraînement (§3.1). Les ERM de la Table 1 à 90 ép. sont repris de Goyal et al. / Xie et al.
- **CIFAR-10/100** : « significativement meilleur » que l'ERM pour PreAct ResNet-18, WideResNet-28-10, DenseNet ; les valeurs ne sont que dans la Fig. 3a, non extraites (`n/r`) (§3.2).
- **Labels corrompus, CIFAR-10, PreAct ResNet-18 (Table 2 reconstruite, lignes 50 % et 80 % à recouper avec le PDF)** : erreur de test meilleure époque / dernière époque.

| Corruption | ERM | ERM + dropout | mixup | mixup + dropout |
|---|---|---|---|---|
| 20 % | 12,7 / 16,6 | 8,8 / 10,4 | 5,9 / 6,4 (α=8) | 6,2 / 6,2 (α=4, p=0,1) |
| 50 % | 18,8 / 44,6 | 14,1 / 15,5 (p=0,8) | 11,3 / 12,7 (α=32) | 10,9 / 10,9 (α=8, p=0,3) |
| 80 % | 36,5 / 73,9 | 30,9 / 35,1 (p=0,8) | 25,3 / 30,9 (α=32) | 24,0 / 24,8 (α=8, p=0,3) |

  Lecture des auteurs (§3.4) : l'ERM surapprend les labels corrompus quand le learning rate baisse (< 0,01) ; mixup avec grand α (8 ou 32) bat le dropout, tout en gardant une faible erreur sur les labels réels ; mixup + dropout est le meilleur et les deux sont compatibles. Hypothèse des auteurs : un grand α éloigne les exemples virtuels des exemples d'entraînement et rend la mémorisation plus difficile (§3.4). Erreur d'entraînement sur labels corrompus au dernier époque : 83-88 % pour les méthodes régularisées, soit peu de mémorisation ; ERM : 0,28 % pour 20 % (valeurs 50-80 % ERM illisibles).
- **Ablation CIFAR-10 (Table 5, médiane des 10 dernières époques)** : ERM 5,53 (wd 1e-4) / 5,18 (wd 5e-4) ; mixup toutes classes + paires aléatoires 4,24 / 4,68 ; mixup + KNN 4,98 / 5,26 ; entrées seules sans mélange des labels, 5,17 à 5,55 ; label smoothing 5,02 à 5,34 ; bruit gaussien σ=0,2 : 7,16 / 7,24 ; interpolation de représentations latentes : 4,44 (couche 1) à 5,95 (couche 4). Mixup le meilleur, mixer les labels est nécessaire, SMOTE sans gain notable, et mixup préfère un weight decay faible (1e-4) quand l'ERM préfère 5e-4 (§3.8).
- Autres : Google commands VGG-11 test 4,6 → 3,4 (α=0,2) (Table 4, tableau mal extrait, LeNet ne progresse pas) ; ImageNet adversarial (ResNet-101) : FGSM top-1 90,7 → 75,2 en boîte blanche (Table 3) ; UCI : mieux sur 4 jeux sur 6 (§3.6) ; GAN toy (§3.7). Hors thème.

→ reportés dans `benchmarks.csv` : 9 lignes proposées (ImageNet x4, labels corrompus x4, ablation x1). Colonnes matérielles à `n/r`.

## Limites et critique

- Tâche de classification, images à une seule étiquette, résolutions 32x32 à 224x224 : aucune expérience de détection, de localisation ou de segmentation. Les auteurs disent eux-mêmes que l'extension aux problèmes structurés (segmentation) est « moins évidente » (§5).
- Les labels corrompus sont des **permutations aléatoires symétriques** de la classe, bruit dont le modèle est le plus simple. Le bruit réel d'annotation de détection (boîtes décalées, objets manquants, classes confondues) est structuré et n'est pas testé.
- L'avantage « labels bruités » dépend d'un α très grand (8-32) choisi sur le jeu de test (meilleure époque rapportée) ; pas de jeu de validation propre décrit pour ces hyperparamètres. Le « best test error » est un oracle ; la dernière époque est plus honnête (voir ERM 80 % : 36,5 vs 73,9).
- Un seul réseau (PreAct ResNet-18) et un seul jeu (CIFAR-10) pour le bruit de labels ; une seule graine, sans écart-type rapporté.
- Comparaisons ImageNet : ERM de référence repris de la littérature à 90 ép. (autres frameworks) ; gains parfois très faibles (ResNet-50 90 ép. : 0,2 point).
- Pas de code publié autre que l'extrait ; pas de mesure du surcoût.

## Pertinence pour le thème

Axe `augmentation` : MixUp est cité parmi les augmentations de la base (profile.md). Ce papier est la **source du principe** (pas la version détection). Ce qu'il apprend pour AUGMENTER un dataset :

- **Lu** : λ ~ Beta(α, α), `x` et `y` mélangés linéairement ; α entre 0,1 et 0,4 sur ImageNet ; α = 1 sur petit jeu de données ; mélange de toutes classes, entrées et labels ensemble ; surcoût faible ; gain croissant avec la capacité du modèle et la durée d'entraînement ; régularisation forte (weight decay à réduire).
- **Lu, labels bruités** : avec 20-80 % de labels aléatoires, mixup (α grand) réduit la mémorisation et garde une erreur de test proche de celle du dropout combiné, surtout en dernière époque (Table 2, §3.4). Cadre : classification symétrique, voir limites.

**Déduit (non affirmé par les auteurs, à ne pas citer comme résultat du papier)** pour une base de labels de détection :

- Pour la détection, les labels sont des boîtes, pas un vecteur one-hot : le mélange `λ·y_i + (1-λ)·y_j` se transpose en **conservant les deux ensembles de boîtes** (réunion des annotations des deux images) avec la fusion pondérée des images ; c'est le choix des implémentations de détection, pas décrit ici. Lien à vérifier dans les papiers de détection de la base (YOLOv4, §2 Mosaic/CutMix) avant de s'appuyer dessus.
- En détection, la valeur de α et le fait d'utiliser MixUp en fin d'entraînement ne sont pas fixés par ce papier : α = 8-32 testé en bruit de labels est une plage de classification, à ne pas importer telle quelle. En détection, la recette courante de la littérature est α bien plus faible ; à vérifier (non lu ici).
- Cas d'usage, déduit : jeu **petit** ou **bruité**, modèle de forte capacité entraîné longtemps (le papier montre que ces cas profitent le plus), avec précaution pour les petits objets (une boîte fantôme semi-transparente peut dégrader la localisation : hypothèse non testée).
- Contre-indication déduite : sur jeu propre et petit modèle (cible embarquée), le gain mesuré est faible (ResNet-50 : 0,2 point à 90 ép., §3.1) ; Copy-Paste (fiche voisine) indique que MixUp n'aide pas avec LSJ et seulement en régime de peu de données (cité dans la fiche Copy-Paste, non vérifié ici).

## Gaps identifiés

- Aucune mesure en détection (mAP, mAP_small) de MixUp avec α, ni de sa robustesse à du bruit de boîtes : à chercher dans YOLOX / YOLOv4 / Ultralytics ou à mesurer.
- Pas de modèle de bruit de labels réaliste (boîtes décalées, manquantes) : relier à l'axe `label-quality`.
- Interaction MixUp / Mosaic / Copy-Paste non couverte ici.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier ; backend grobid, `ok: true`). Tables à corps mal reconstruit : Table 2 (lignes 50 % et 80 % lues avec un désordre de colonnes, recoupées avec le texte du §3.4, valeurs de la dernière époque et meilleure époque à vérifier au PDF), Table 3/4 (corps partiel). Valeurs CIFAR de la Fig. 3a non extraites (`n/r`).
Ce qui suit est déduit et non affirmé par les auteurs : tout le contenu de « Pertinence » marqué Déduit (transposition à la détection, α en détection, cas d'usage, contre-indications) ; l'analyse « best epoch = oracle sur le jeu de test » dans « Limites » est une lecture du protocole décrit en §3.4 (« best test error »).
