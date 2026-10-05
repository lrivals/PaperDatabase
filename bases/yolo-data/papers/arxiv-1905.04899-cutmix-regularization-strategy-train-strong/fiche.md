---
id: arxiv-1905.04899-cutmix-regularization-strategy-train-strong
fiche: done
date: 2026-10-05
---

# CutMix: Regularization Strategy to Train Strong Classifiers with Localizable Features

Sangdoo Yun, Dongyoon Han, Seong Joon Oh, Sanghyuk Chun, Junsuk Choe, Youngjoon Yoo, 2019, arXiv preprint. https://arxiv.org/abs/1905.04899
Type : preprint non relu par les pairs

## Problème

Les méthodes de regional dropout (Cutout, etc.) améliorent généralisation et localisation, mais
elles remplacent les zones supprimées par des pixels noirs ou du bruit, ce qui gaspille des pixels
d'entraînement (§1). Mixup utilise tous les pixels mais produit des images non naturelles,
ambiguës localement (§1, §3.2). Question : garder l'effet de regional dropout sans perdre de pixels.

## Méthode

- Recette (§3.1) : pour deux échantillons (x_A, y_A) et (x_B, y_B) d'un même mini-batch,
  x = M ⊙ x_A + (1−M) ⊙ x_B et ỹ = λ y_A + (1−λ) y_B, avec M un masque binaire rectangulaire.
- λ ~ Beta(α, α), α = 1 (donc uniforme) dans toutes les expériences. Boîte : r_x ~ U(0, W),
  r_y ~ U(0, H), r_w = W√(1−λ), r_h = H√(1−λ) : l'aire collée vaut 1−λ et garde le rapport
  d'aspect de l'image (Eq. 2). Annexe A (Algorithm A1) : λ est recalculé après découpe de la
  boîte pour égaler le ratio d'aire exact (boîte tronquée aux bords). Aucun coût de calcul notable (§3.1).
- Comparaison : Cutout supprime la zone ; Mixup interpole les pixels ; CutMix colle une zone
  réelle d'une autre image et mélange les labels au prorata de l'aire (Table 1, §3.2).
- Ablations (CIFAR-100, Table 8, Fig. 3) : α = 1,0 est le meilleur sur {0,1…4,0} ; appliquer
  CutMix sur l'image (niveau 0) bat les niveaux de features ; les variantes (centre gaussien
  15,95 %, taille fixe 16×16 14,97 %, label one-hot 15,89 %, label 0,5/0,5 15,17 %, planifié
  14,72 %) sont toutes moins bonnes que CutMix de base (14,47 %). Le mélange de label
  proportionnel à l'aire compte.
- Les expériences de détection ne modifient pas l'entraînement du détecteur : CutMix sert
  uniquement au pré-entraînement ImageNet du backbone (§4.3).

## Plateforme et implémentation

PyTorch, plateforme NSML de NAVER (§4). Ressource matérielle : n/r. Code et modèles
pré-entraînés publiés : https://github.com/clovaai/CutMix-PyTorch (§4). Pas d'implémentation
de CutMix à l'intérieur d'un détecteur (boîtes à remapper) dans ce papier.

## Résultats

Classification (pour mémoire) :
- ImageNet ResNet-50 : erreur top-1 23,68 % (baseline) vs 21,40 % avec CutMix (Table 3), soit
  −2,28 pts ; Mixup 22,58 %, Cutout 22,93 %, Feature CutMix 21,80 % (Table 3). ResNet-101 :
  21,87 -> 20,17 % (Table 4).
- CIFAR-100 PyramidNet-200 : 16,45 -> 14,47 % ; Mixup (α=1) 15,63 %, Cutout 16,53 % (Table 5,
  corps de tableau non extrait dans les légendes mais valeurs présentes dans le texte extrait).
  CIFAR-10 : 3,85 -> 2,88 % (Table 7).

Localisation faiblement supervisée (WSOL, classes seules, §4.2, Table 9, métrique Loc Acc) :

| Modèle | CUB200-2011 | ImageNet |
|---|---|---|
| ResNet-50 + CAM (baseline) | 49,41 | 46,30 |
| + Mixup | 49,30 | 45,84 |
| + Cutout | 52,78 | 46,69 |
| + CutMix | 54,81 | 47,25 |
| VGG-GAP + CAM | 37,12 | 42,73 |
| + Mixup | 41,73 | 42,54 |
| + Cutout | 44,83 | 43,13 |
| + CutMix | 52,53 | 43,45 |

Le texte annonce +5,4 pts (CUB) et +0,9 pt (ImageNet) en moyenne (§1) et +5,51 / +1,41 pts de
CutMix sur Mixup (§4.2). Mixup dégrade la localisation du baseline sur ResNet-50 (et sur ImageNet VGG-GAP).
CutMix est présenté comme comparable aux méthodes WSOL dédiées (ACoL, ADL, HaS, SPG) (§4.2).

Transfert vers la détection (§4.3, Table 10) : backbone ResNet-50 (au lieu de VGG-16)
initialisé avec un modèle ImageNet pré-entraîné par Mixup, Cutout ou CutMix, puis fine-tuning de
SSD et de Faster R-CNN sur Pascal VOC 2007+2012 trainval, évaluation mAP sur VOC07 test
(détails en Annexe C, non extraite). Résultat qualitatif : Cutout et Mixup n'améliorent pas
la détection par rapport au pré-entraînement standard ; CutMix améliore SSD et Faster R-CNN (§4.3).
Chiffre global : « +1 mAP » sur Pascal VOC (§1, résumé). Les mAP absolus par méthode et par
détecteur sont dans Table 10, dont le corps n'est pas extrait : `n/r` ici. Captioning MS-COCO
(NIC) : BLEU-4 22,9 -> 24,9 (CutMix), Mixup 23,2, Cutout 24,0 (Table A1).

Robustesse (§4.4) : CutMix améliore FGSM, occlusion et détection OOD (Tables 11-12, corps non
extraits) ; non repris ici.

→ reportés dans `benchmarks.csv` (proposés par l'agent) : 5 lignes (4 WSOL Table 9, 1 détection
VOC avec valeur `n/r`, confidence medium).

## Limites et critique

- Le gain en détection (+1 mAP) vient d'un pré-entraînement de classification, pas d'un CutMix
  appliqué pendant l'entraînement du détecteur : le papier ne dit rien de CutMix sur images
  avec boîtes (remappage des boîtes, objets coupés, boîtes quasi vides). Pour YOLO, c'est
  une inférence, non un résultat. Mosaic / Copy-Paste sont des alternatives pensées pour la détection.
- Détection testée uniquement sur Pascal VOC (SSD et Faster R-CNN ResNet-50), pas sur COCO, pas
  de petits objets, pas de YOLO. Gain modeste (+1 mAP) et sans barres d'erreur ni nombre
  de graines pour la détection (n/r) ; classification : « trois essais, meilleure performance
  pendant l'entraînement » (Table 5), c'est-à-dire un optimum sur le test, biais optimiste.
- Comparaisons avec Mixup et Cutout : mêmes hyperparamètres de base mais réglages propres
  (taille Cutout 112×112 sur ImageNet, α testés 0,5 et 1) ; les baselines marquées * sont
  reprises des articles originaux (autres conditions d'entraînement, par ex. DropBlock 270 époques).
- Entraînements longs (300 époques ImageNet) : CutMix demande plus d'époques pour converger (§4.1.1).
- WSOL : gain net surtout sur CUB200-2011 ; sur ImageNet, CutMix avec VGG-GAP (43,45) reste
  sous les méthodes dédiées ACoL/ADL/SPG (44,9-48,6, Table 9).
- Preprint, mais code publié.

## Pertinence pour la thèse

- **CONSTRUIRE** : n'ajoute rien sur la constitution de datasets ; les expériences de caption
  et de WSOL montrent qu'un jeu de classes seules peut suffire à localiser (supervision faible).
- **ANNOTER** : WSOL (Table 9) = localiser sans boîtes, utile comme alternative d'annotation faible
  ou pour générer des boîtes grossières à partir de CAM (à valider : non testé ici).
- **PRÉTRAITER** : rien.
- **AUGMENTER** : recette simple (λ~U(0,1), boîte d'aire 1−λ, label mélangé à l'aire), sans coût.
  À appliquer en pré-entraînement de backbone de classification, ou comme référence conceptuelle
  avant d'adapter à la détection : le papier montre que le même mélange (coller des régions
  réelles) bat Mixup et Cutout sur les tâches où la localisation compte, et que Cutout/Mixup
  peuvent dégrader le transfert détection. Cas d'usage : peu d'images, backbone à entraîner
  soi-même ; si on part d'un backbone ImageNet déjà publié, le gain ne s'applique pas sans re-pré-entraînement
  (déduit). Pour YOLO, CutMix existe comme augmentation de détection dans d'autres travaux
  (YOLOv4 le cite) : voir la fiche YOLOv4.
- Reste ouvert : comparaison CutMix / Mosaic / Copy-Paste au sein d'un détecteur, avec mise à jour des boîtes.

## Gaps identifiés

- Aucune mesure de CutMix appliqué directement à l'entraînement d'un détecteur (avec boîtes) dans ce papier.
- Gain de détection non chiffré dans nos sources extraites (Table 10) : à relire dans le PDF si besoin.
- Pas d'évaluation sur petits objets ni sur COCO.

## Statut de lecture

papier complet (`fulltext.md`, grobid ; extraction.ok = true). Tableaux sans corps extrait : Tables 4, 5,
6, 7, 8, 11, 12 (valeurs lues dans le texte reconstruit, à vérifier), et Table 10 (détection VOC)
dont les mAP absolus manquent, ainsi que l'Annexe C (réglages de fine-tuning SSD / Faster R-CNN).
Table 1 (aperçu) non extraite aussi. Déduit et non affirmé par les auteurs : l'applicabilité à
YOLO / à un entraînement de détecteur, la conversion en augmentation avec boîtes, l'usage de
CAM pour pré-annoter, le fait que le gain ne s'applique qu'avec re-pré-entraînement du backbone.
