---
id: arxiv-1904.08008-clustered-object-detection-aerial-images
fiche: done
date: 2026-10-18
---

# Clustered Object Detection in Aerial Images

Fan Yang, Heng Fan, Peng Chu, Erik Blasch, Haibin Ling, 2019, arXiv preprint. https://arxiv.org/abs/1904.08008
Type : preprint non relu par les pairs (dans `metadata.json`). Le texte extrait ne mentionne
pas de venue ; ClusDet est à notre connaissance paru à ICCV 2019 (non vérifié, à confirmer
avant de citer).

## Problème

Dans les images aériennes haute résolution (~2000×1500 px pour VisDrone), les objets sont
**petits** et **répartis de façon éparse et non uniforme** (§1). Le découpage uniforme en
tuiles (EIP, evenly image partition) aide les petits objets mais gaspille du calcul : avec une
grille, plus de 73 % des tuiles sont « sparse », dont 23 % vides (Fig. 1). Les objets étant
**groupés** (piétons sur les places, véhicules sur les routes), les auteurs veulent découper
autour de ces groupes plutôt que selon une grille.

## Méthode

ClusDet, bout en bout, trois sous-réseaux (§3, Fig. 2) :
- **CPNet** (cluster proposal) : type RPN, propose des **régions de groupes** ; conv 5×5 + deux
  conv 1×1 sur les features haut niveau (§3.2.1, §4.1). Vérité terrain des groupes générée par
  une « stratégie simple » décrite en matériel supplémentaire (non inclus) : aucun dataset
  public ne fournit de labels de groupes (§3.2.1).
- **ICM** (iterative cluster merging) : fusion non-max (seuil 0,7) jusqu'à TopN groupes
  (3 VisDrone, 2 UAVDT, 5 DOTA) (§3.2.2, §4.1).
- **ScaleNet** : régresse l'échelle moyenne des objets de chaque crop (FC 1024) ; puis
  **partition ou padding (PP)** : si l'échelle estimée dans l'espace d'entrée du détecteur est
  trop grande, le crop est complété par du padding (détections dans le padding ignorées), sinon
  il est coupé en deux crops égaux ; plage visée [70, 280] px (§3.3, Table 1).
- **DetecNet** : Faster R-CNN + FPN (Detectron, Caffe2) sur les crops ; fusion
  local/global par NMS 0,5 (§3.4, §4.1). Entrée 600×1000 (VisDrone, UAVDT), 1000×1000 (DOTA).
- Entraînement : données augmentées en découpant les images en **6 crops (VisDrone) ou 4
  (UAVDT) sans recouvrement**, choisis pour que la taille d'un crop ressemble à celle de COCO ;
  DOTA découpé avec l'outil fourni par les auteurs du dataset (§4.1).
- Efficacité mesurée par **#img** (images globales + crops passés au détecteur) et temps moyen
  par image globale avec ses crops (§4.4).

## Plateforme et implémentation

Aucune cible embarquée : entraînement sur 2 GPU, temps d'inférence sur une **GTX 1080 Ti**
(légende Table 1). Précision numérique n/r. Code annoncé sur https://github.com/fyangneil
(Abstract), dépôt précis n/r.

## Résultats

VisDrone (validation, faute de serveur de test ouvert, §4.2), entrée 600×1000, R-50 (Table 1) :

| Méthode | #img | AP | AP50 | APs | APl | s/img (1080 Ti) |
|---|---|---|---|---|---|---|
| FRCNN+FPN, image entière | 548 | 21,4 | 40,7 | 11,7 | 54,7 | 0,055 |
| + EIP (découpage uniforme) | 3 288 | 21,1 | 44,0 | 14,4 | 30,0 | 0,330 |
| DetecNet + CPNet (crops de groupes, redimensionnés) | 1 945 | 25,6 | 47,9 | 16,2 | 53,7 | 0,195 |
| + ScaleNet (PP) = ClusDet | 2 716 | 26,7 | 50,6 | 17,6 | 51,4 | 0,273 |

- Même ordre avec X-101 : image entière 21,8 AP / 0,156 s ; EIP 24,4 / 0,936 s ; CPNet 27,6 /
  0,554 s ; ClusDet 28,4 AP, 53,2 AP50, APs 19,1 / 0,773 s (Table 1).
- Multi-échelle + box voting : ClusDet X-101 **32,4 AP** / 56,2 AP50 (Table 2) ; le gain
  multi-échelle ne profite pas aux méthodes avec EIP (crops agrandis à l'extrême, faux
  positifs) (§4.6).
- Effet de l'EIP : #img x6 (3 288 contre 548), APs +2,7 mais APl 54,7 → 30,0 : les grands
  objets sont coupés en morceaux (§4.5). Les crops de groupes ne dégradent pas APl (53,7).
- ScaleNet : #img passe de 1 945 à 2 716 car PP coupe certains crops ; AP50 +2 à 3 points selon
  le backbone, APs +1,6 sur X-101 (§4.5).
- TopN : au-delà de 4, le nombre d'images croît mais l'AP fluctue autour de 27 (Fig. 7, §4.5) ;
  la fusion ICM est « critique » pour le coût.
- UAVDT (test, R-50) : ClusDet 13,7 AP avec 25 427 images contre 11,0 (15 069) pour
  FRCNN+FPN et 6,6 (60 276) avec EIP (Table 3) ; l'EIP dégrade car les véhicules sont au
  centre et se font couper (§4.6). Le texte (§4.6) cite 6,1 pour l'EIP, le tableau 6,6.
- DOTA (5 classes mobiles : 920 / 285 images) : ClusDet R-50 32,2 AP avec 1 055 images contre
  31,0 avec 2 838 pour FRCNN+FPN+EIP ; AP50 inférieur (47,6 contre 50,7), AP75 supérieur
  (39,2 contre 32,9) (Table 4, §4.6).

Lignes de `benchmarks.csv` : 8 existantes (VisDrone R-50 / R-101 / X-101, X-101 multi-échelle,
UAVDT R-50, DOTA R-50 / R-101 / X-101), `confidence: high`, non modifiées ; 13 lignes
proposées ajoutent les configurations d'ablation manquantes (baselines sans découpage, EIP et
CPNet sans ScaleNet sur VisDrone, baselines UAVDT et DOTA), toutes issues des Tables 1, 3 et 4.

## Limites et critique

- **« Efficacité » mesurée en nombre de crops**, pas en coût réel : ClusDet R-50 prend 0,273
  s/img contre 0,055 s sans découpage, soit ~5× plus lent que la baseline globale (Table 1,
  rapport déduit) ; il n'est plus rapide que l'EIP (0,330 s) que de 17 %. Le gain de calcul
  est modeste face à l'EIP (2 716 contre 3 288 crops) ; il est net sur DOTA (1 055 contre 2 838).
- L'EIP comparé est une grille **sans recouvrement** (6 crops sur VisDrone), pas un tiling
  chevauchant avec fusion, et sans réglage de la taille des tuiles : la baseline de découpage
  est la plus simple possible (déduit de §4.1).
- Une partie du gain vient du **contexte** (le détecteur sur crops de groupes le modélise
  implicitement, §4.5) et de l'entraînement sur crops : on ne peut pas isoler « où couper »
  de « comment redimensionner » sans l'ablation CPNet seul, qui existe (25,6 AP) mais avec un
  redimensionnement non décrit en détail.
- Évaluation VisDrone sur la **validation** (548 images), pas sur le test ; TopN réglé par jeu
  de données (3 / 2 / 5), donc non transférable tel quel.
- DOTA filtré aux classes « groupables », ce qui favorise la méthode (§4.2).
- Baselines UAVDT reprises de [8] (sauf FRCNN+FPN), conditions non homogènes (§4.6).
- Détecteur deux étages, modèle entraîné de bout en bout avec la détection : le module de
  découpage n'est pas un prétraitement indépendant du détecteur. Les labels de groupes
  (supplément) sont dérivés des boîtes existantes, donc aucun surcoût d'annotation, mais le
  procédé exact est n/r.
- Pas d'étude sur détecteur un étage (YOLO), ni sur un dataset à objets non groupés.

## Pertinence pour ce thème

Pour **PRÉTRAITER** (axe `preprocessing`) un dataset d'images haute résolution à petits objets :
- **Cluster contre grille.** Découper autour des zones denses plutôt que sur une grille évite
  les tuiles vides (23 % sur VisDrone) et ne coupe pas les grands objets : APl reste à 53,7
  avec crops de groupes contre 30,0 avec EIP (Table 1). À appliquer quand les objets sont
  concentrés (foules, trafic) ; à éviter, ou à comparer, quand ils sont centrés ou épars.
  Sur UAVDT, la grille fait tomber l'AP de 11,0 à 6,6 (Table 3) : un découpage uniforme n'est
  pas gratuit.
- **Compromis précision / crops / temps** (R-50, VisDrone, Table 1) : 548 crops 21,4 AP
  0,055 s ; 1 945 crops 25,6 AP 0,195 s ; 2 716 crops 26,7 AP 0,273 s ; 3 288 crops 21,1 AP
  0,330 s. Le meilleur rapport est CPNet seul ; ScaleNet coûte +771 crops et 0,078 s pour
  +1,1 AP. Plafond : TopN > 4 n'apporte plus d'AP (Fig. 7).
- **Redimensionnement de chaque crop** : cibler une taille d'objet dans [70, 280] px après
  redimensionnement (partition si les objets seraient trop petits, padding sinon) plutôt qu'un
  resize fixe du crop à la taille d'entrée. Règle réutilisable à la main, sans ScaleNet, si
  l'échelle moyenne des objets du crop est connue.
- **Pour AUGMENTER / construire l'entraînement** : le papier entraîne sur des crops
  non recouvrants (6 par image VisDrone) dimensionnés comme des images COCO ; c'est une
  augmentation par découpage, mais son effet seul n'est pas isolé (§4.1).
- **Différence avec SAHI pour un praticien** (déduit, SAHI n'est pas dans ce papier) : SAHI
  est un découpage uniforme chevauchant appliqué à l'inférence sur n'importe quel détecteur
  déjà entraîné, sans entraînement ; ClusDet impose d'entraîner CPNet et ScaleNet avec le
  détecteur, mais réduit le nombre de crops et évite de couper les objets. Pour un modèle
  YOLO déjà entraîné, SAHI est directement utilisable ; ClusDet est un schéma à reproduire
  (crops de groupes tirés d'une première passe globale, fusion NMS) et n'a pas de code
  vérifié ici.
- Rien sur l'annotation : les groupes sont dérivés des boîtes existantes (détail n/r).

## Gaps identifiés

- Comparaison directe cluster / SAHI (tuiles chevauchantes) à détecteur et entrée identiques :
  absente de ce papier.
- Découpage adaptatif avec un détecteur un étage de type YOLO : non traité ; coût réel en
  latence au-delà du nombre de crops : non mesuré pour les crops de groupes sans ScaleNet
  hors Table 1.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). Matériel
supplémentaire (vérité terrain des groupes, détails NMM) non inclus dans le texte. Tables 1 à 4
extraites avec corps ; Table 2 : quelques lignes multi-échelle sans marque distinctive dans
l'extraction (identifiées par la légende et par la Table 1).

Ce qui suit est déduit et non affirmé par les auteurs :
- la venue ICCV 2019 ;
- le « ~5× plus lent » (0,273 / 0,055) et le « 17 % » (0,273 / 0,330) ;
- le caractère non chevauchant de l'EIP de comparaison au-delà des 6 / 4 crops
  d'entraînement ;
- toute comparaison avec SAHI, absent du papier.
