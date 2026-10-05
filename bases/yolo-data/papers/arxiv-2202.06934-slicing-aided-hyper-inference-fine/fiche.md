---
id: arxiv-2202.06934-slicing-aided-hyper-inference-fine
fiche: done
date: 2026-10-05
---

# Slicing Aided Hyper Inference and Fine-tuning for Small Object Detection

Fatih Cagatay Akyon, Sinan Onur Altinuc, Alptekin Temizel, 2022, arXiv preprint. https://doi.org/10.1109/ICIP46576.2022.9897990 (arXiv 2202.06934)
Type : `preprint` dans `metadata.json` (non relu par les pairs sous cette forme), mais le DOI
est celui d'**IEEE ICIP 2022** : une version en conférence existe (déduit du préfixe du DOI).

## Problème

Les détecteurs pré-entraînés sur COCO ou VOC (images de l'ordre de 640×480, objets couvrant
en moyenne 60 % de la hauteur de l'image) échouent sur les **petits objets dans des images
haute résolution** de drones et de caméras de surveillance. Entraîner directement en haute
résolution coûte cher en mémoire (§1). Les deux jeux de test ont des objets de largeur
< 1 % de celle de l'image (§4).

## Méthode

Cadre **générique, indépendant du détecteur**, en deux briques (§3, Fig. 2).

**Recette, d'après les auteurs :**

| Paramètre | VisDrone2019-DET | xView |
|---|---|---|
| Tuiles d'entraînement (SF) | côté tiré au hasard entre 480 et 640 px (§4) | entre 300 et 500 px (§4) |
| Redimensionnement à l'entraînement | tuile redimensionnée, ratio conservé, largeur 800 à 1333 px (§3, §4) | idem |
| Tuiles d'inférence (SAHI) | 640×640 (§4) | 400×400 (§4) |
| Recouvrement (PO) | 25 % entre tuiles à l'inférence (§4) | idem |
| Image entière (FI) | passe optionnelle en plus des tuiles (§3) | idem |
| Fusion | NMS sur les prédictions des tuiles (et de FI), remises aux coordonnées de l'image d'origine ; Tm = 0,5 (§3, §4) | idem |

- **SF (slicing aided fine-tuning)** : le jeu d'entraînement est **augmenté** avec des tuiles
  (images et annotations découpées ensemble, §4). Les images d'origine restent dans le
  jeu, pour les gros objets (§3). Les bornes [Mmin, Mmax] et [Nmin, Nmax] sont des
  hyperparamètres (§3). Les auteurs notent que, plus les tuiles sont petites, plus les
  gros objets risquent de ne plus tenir dans une tuile (§3).
- **SAHI** : l'image est découpée en l tuiles M×N, redimensionnées en conservant le
  ratio, inférées indépendamment (§3). Seuil Td de suppression par score : valeur `n/r`.
  Taille de redimensionnement des tuiles à l'inférence : `n/r` (§3 dit seulement « resized
  while preserving the aspect ratio »).
- **Slicing à l'entraînement vs à l'inférence** : les deux sont indépendants. SAHI seul
  marche **sans réentraînement** (abstract, §3) ; SF seul (inférence sur image entière)
  donne déjà un gain, mais le meilleur résultat combine les deux (Table 1).
- Hyperparamètres d'entraînement : SGD, lr 0,01, momentum 0,9, weight decay 1e-4, warmup
  linéaire 500 itérations, décroissance exponentielle aux époques 16 et 22 (§4). Nombre
  total d'époques `n/r`.
- Détecteurs : FCOS, VFNet, TOOD sous MMDetection (§4) ; intégration annoncée dans
  Detectron2 et YOLOv5 (abstract), sans résultat chiffré sur YOLOv5.

## Plateforme et implémentation

- Plateforme matérielle : `n/r`. Aucun temps d'inférence, aucune mémoire, aucune puissance.
  Les auteurs écrivent seulement que le temps de calcul **croît linéairement** avec le
  nombre de tuiles, à mémoire constante, et que les tailles de tuile permettent d'arbitrer
  calcul et mémoire selon la plateforme (§5).
- **Code publié** : https://github.com/obss/sahi (bibliothèque) et
  https://github.com/fcakyon/sahi-benchmark (configs, scripts de conversion et
  d'évaluation, résultats) (§4).

## Résultats

Protocole COCO, **AP50** global et par taille (s, m, l), 500 détections maximum (§4). Test
sur VisDrone2019-DET **test-dev** (Table 1) ; xView avec découpage aléatoire 75/25 non
standard, évalué sur la part de validation (Table 2, Fig. 4). Baseline = inférence sur
l'image entière (FI) du même détecteur fine-tuné sans tuiles (§4).

**Gain par configuration, VisDrone test-dev, AP50 (AP50s entre parenthèses) (Table 1)**

| Configuration | FCOS | VFNet | TOOD |
|---|---|---|---|
| FI (baseline) | 25,8 (14,2) | 28,8 (16,8) | 29,4 (18,1) |
| SAHI + PO | 29,0 (18,9) | 32,0 (21,4) | 32,5 (22,8) |
| SAHI + FI + PO | 31,0 (19,8) | 33,9 (22,4) | 34,7 (23,8) |
| SF + FI (pas de tuiles à l'inférence) | n/r | n/r | 36,8 (24,4) |
| SF + SAHI + PO | 38,1 (25,7) | 41,9 (29,7) | 43,1 (31,7) |
| SF + SAHI + FI + PO | 38,5 (25,9) | 42,2 (29,6) | 43,5 (31,7) |

Ablations supplémentaires, TOOD seul (Table 1) : SAHI sans PO 31,9 ; SAHI + FI sans PO 34,6 ;
SF + SAHI sans PO 42,5 ; SF + SAHI + FI sans PO 43,4.

Lecture des effets (gains recalculés à partir de la Table 1) :
- **SAHI seul, sans réentraînement** : +5,2 (FCOS), +5,1 (VFNet), +5,3 (TOOD) d'AP50 avec
  FI + PO. L'AP50s gagne +5,6 à +5,7 points.
- **SF seul** (TOOD) : +7,4 d'AP50 (29,4 → 36,8), avec la meilleure AP50l du tableau
  (66,4). Slicer en plus à l'inférence ajoute encore +6,7 (36,8 → 43,5).
- **Cumul SF + SAHI + FI + PO** : +12,7 / +13,4 / +14,1 (FCOS / VFNet / TOOD).
- **FI** : aide les gros objets (TOOD + SAHI+PO 43,6 d'AP50l → 50,3 avec FI ; SF+SAHI+PO
  60,2 → 65,4) et coûte peu ou rien aux petits (Table 1, §4). Sur xView, FI baisse
  légèrement l'AP global (TOOD SF+SAHI 19,4 → 19,2) mais améliore AP50l (14,2 → 14,7).
- **PO 25 %** : +0,1 à +0,6 d'AP50 sur VisDrone (TOOD sans SF) (+0,6 TOOD SF+SAHI), +1,2 à +1,7
  sur xView (Table 2). Il améliore petits et moyens objets mais peut réduire AP50l (TOOD
  SAHI+FI : 53,1 → 50,3), à cause de faux positifs de tuiles sur de gros objets (§4).

**xView (Table 2, `medium`)** : la baseline FI est quasi nulle (AP50 2,1 à 2,2 ; AP50s 0,1 à
0,5), le fine-tuning par tuiles est donc indispensable. SF + SAHI : 15,8 (FCOS), 16,0
(VFNet), 19,4 (TOOD) ; avec PO : 17,1, 17,7, **20,6 (TOOD, meilleur résultat, AP50s 14,9)**.
Les auteurs notent que xView est très déséquilibré (60 classes) et attribuent à la focal
loss de FCOS et TOOD leurs bons résultats (§4, interprétation des auteurs, non testée).

Lignes dans `benchmarks.csv` : 4 déjà présentes (meilleure configuration par détecteur sur
VisDrone, TOOD sur xView). Lignes proposées en complément, pour mesurer l'effet de chaque
brique (`.cache/bench/`) : SAHI + FI + PO sans SF pour les trois détecteurs, et TOOD + SF
+ FI sans tuiles à l'inférence (Table 1, `high`).

## Limites et critique

- **Aucun coût mesuré.** SAHI multiplie les passes par le nombre de tuiles (§5, « linearly »),
  plus une passe FI. Nombre de tuiles par image, temps, mémoire : `n/r`.
- **Chiffres du résumé en partie incohérents avec la Table 1** (recalcul). « +6,8 AP » pour
  FCOS avec SAHI ne correspond à aucune ligne (SAHI+PO : +3,2 ; SAHI+FI+PO : +5,2). Le
  cumul TOOD « 14,5 » est 14,1 dans la table. La conclusion annonce « +14,5 % pour les
  petits objets » et « +2,9 % » dus au recouvrement : la Table 1 donne +13,6 d'AP50s
  (TOOD) et au plus +1,7 pour PO. Préférer les tableaux.
- **AP50 seulement**, pas d'AP50:95 : l'effet du recouvrement et de la NMS de fusion sur la
  localisation fine n'est pas visible.
- **Confusion résolution / tuilage** : les baselines FI sont affinées sans tuiles. Le gain
  de SF peut venir en partie de la résolution effective plus élevée (largeur 800-1333 px
  appliquée à des tuiles). Pas de comparaison à un entraînement en haute résolution à coût
  égal (déduit).
- SF **ajoute** des tuiles au jeu : le nombre d'itérations et d'images vues change entre
  baseline et SF, et la quantité d'images/tuiles générées par image est `n/r` (déduit : la
  comparaison n'est pas à budget d'entraînement égal).
- Pas d'ablation sur la taille des tuiles ni sur le taux de recouvrement (un seul réglage,
  25 %, par jeu) : les valeurs 640/400 et 25 % sont des choix, pas des optima démontrés.
- Fusion par NMS entre tuiles non comparée à d'autres (Soft-NMS, WBF, etc.) : le
  papier l'annonce comme piste future (§5). Pas de traitement spécifique des objets coupés
  par les bords de tuile.
- Découpage xView aléatoire (risque de fuite entre tuiles voisines d'une même scène, déduit),
  non comparable à d'autres travaux.
- Aucun résultat avec un détecteur YOLO, malgré l'intégration annoncée.

## Pertinence pour cette base

**Construire.** Pas de contribution de collecte. Montre seulement que, pour des jeux
d'images haute résolution à petits objets (VisDrone, xView), le jeu d'entraînement doit
contenir des tuiles ET les images entières (les gros objets l'exigent, §3).

**Annoter.** Les annotations sont découpées avec les images (§4) : un label tronqué par la
frontière d'une tuile est conservé tel quel selon le papier, règle de conservation des
boîtes coupées `n/r` (à fixer pour un export au format YOLO ; l'implémentation SAHI
est à consulter, non lue ici).

**Prétraiter (cœur du papier).** Recette de référence pour le tiling :
1. À l'inférence : tuiles de 640×640 (VisDrone) ou 400×400 (xView), recouvrement 25 %,
   NMS de fusion à 0,5, passe sur l'image entière en plus si des gros objets existent.
   Gain de +5 points d'AP50 sans réentraînement (Table 1).
2. Si l'on peut réentraîner : gain bien plus fort (+12,7 à +14,1) et indispensable quand
   les objets sont minuscules (xView : de ~2 à 15,8-20,6, Table 2).
3. Garder les images entières dans le jeu et la passe FI à l'inférence, sinon l'AP des gros
   objets baisse (§3, §4).

**Augmenter.** SF est une augmentation par recadrage à échelle aléatoire (côté 480-640 /
300-500 px, puis zoom à 800-1333 px de large). Ses effets sont mesurés par ablation
(Table 1), mais pas contre Mosaic ou une autre augmentation, ni sur un YOLO.

**Quand l'appliquer** : images dont la largeur dépasse nettement l'entrée du réseau et dont
les objets font < 1 % de la largeur (critère du papier, §4) ; pas pour des objets grands,
où PO et les tuiles dégradent légèrement AP50l. Limite pratique : coût linéaire en
nombre de tuiles, non chiffré. Renvoi : les autres papiers de la base sur la résolution
d'entrée et les petits objets (à croiser par `bin/pdb search`).

## Gaps identifiés

- Tiling pour un détecteur YOLO au format Ultralytics (labels normalisés) : règle pour les
  boîtes coupées, tuiles de fond, ratio tuiles/images entières : non traité ici.
- Choix de taille de tuile et de recouvrement par ablation (un seul réglage par jeu).
- Tiling d'entraînement contre augmentation classique (Mosaic, Copy-Paste), à budget égal.
- Fusion des prédictions (NMS contre WBF, etc.) : non comparée.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). Table 2 : corps
reconstruit par Docling, à vérifier, et fusionné avec celui de la Table 1 à l'extraction ; il
est identifié par ses valeurs, cohérentes avec le texte (§4 : « FI increases large object AP
by up to 3.3% », « 25% overlap … up to 1.7% »), d'où `confidence: medium` pour xView.
Fig. 1, 3 et 4 (analyse d'erreurs) : légendes lues, images non lues.

Déduit, non affirmé par les auteurs :
- la publication à ICIP 2022 (DOI) ;
- tous les gains « recalculés » (différences de valeurs de la Table 1) et les incohérences
  avec le résumé et la conclusion ;
- l'effet de la résolution effective dans le gain de SF, le budget d'entraînement non égal ;
- les recommandations d'application pour la préparation d'un jeu au format YOLO.
