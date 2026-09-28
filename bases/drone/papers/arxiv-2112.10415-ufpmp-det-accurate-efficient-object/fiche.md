---
id: arxiv-2112.10415-ufpmp-det-accurate-efficient-object
fiche: done
date: 2026-09-28
---

# UFPMP-Det: Toward Accurate and Efficient Object Detection on Drone Imagery

Yecheng Huang, Jiaxin Chen, Di Huang, 2021, arXiv preprint. https://arxiv.org/abs/2112.10415
Type : preprint non relu par les pairs selon `metadata.json`. Le format et les références
évoquent une version AAAI 2022, non confirmée par le texte extrait : à vérifier.

## Problème

Deux verrous de la détection sur images de drone (Introduction) :
1. **Beaucoup de très petits objets**. Les approches coarse-to-fine (ClusDet, DMNet)
   découpent l'image en sous-régions encore riches en fond, puis font une inférence par
   sous-région : c'est coûteux.
2. **Classes proches et forte variabilité intra-classe** (pedestrian vs person, tricycle vs
   awning-tricycle), aggravées par l'altitude, l'angle et la météo. Selon les auteurs, ce
   problème est ignoré par la littérature.

## Méthode

- **Unified Foreground Packing (UFP)** :
  1. un détecteur grossier propose des boîtes, agrandies d'un facteur β = 1,5 (Table 9) ;
  2. l'algorithme glouton FRG les fusionne en régions quand |A|+|B| ≥ |C|, C étant la
     boîte englobante (Algorithme 1) ;
  3. les petites régions sont agrandies pour égaliser les échelles ;
  4. toutes les régions sont **assemblées en une seule mosaïque** (méthode PHSPPOG), sur
     laquelle le détecteur fin ne tourne **qu'une fois** (section « Unified Foreground
     Packing »).
- **Multi-Proxy Detection Network (MP-Det)** :
  - tête de classification à K proxies par classe, inspirée de SoftTriple (Éq. 2) ;
  - anti-effondrement des proxies par un transport optimal (Sinkhorn), dont les marginales
    sont estimées par un « Bag-of-Instance-Words » : file de N = 200 caractéristiques par
    classe, K-means (Éq. 3-4, Table 8) ;
  - perte contrastive (Éq. 5) ; K estimé par DBSCAN sur des caractéristiques de GFL v1.
- Détecteur de base GFL (MMDetection), 60 époques. Entrée 1333 × 800 sur VisDrone,
  1000 × 600 sur UAVDT (Implementation Details). Le surcoût est à l'entraînement seulement
  (27,5 h contre 33 h), sans coût en test selon les auteurs.
- Ni quantification ni élagage.

## Plateforme et implémentation

- Temps d'inférence mesurés sur **une GTX 1080 Ti** (section « Comparison… », Table 3).
  Pas de plateforme embarquée. Puissance, batch et précision numérique : n/r.
- Code : non mentionné dans le texte extrait (seul le lien MMDetection est en note).

## Résultats

VisDrone val, AP / AP50 / AP75 (Table 1) :

| Backbone | UFPMP-Det | +MS | Meilleur concurrent cité |
|---|---|---|---|
| ResNet-50 | 36,6 / 62,4 / 36,7 | 37,4 / 63,7 / 37,7 | AMRNet 31,7 / 52,7 / 33,1 |
| ResNet-101 | 37,5 / 63,2 / 38,3 | 38,7 / 65,1 / 39,4 | AMRNet 31,7 ; HRDNet 31,4 |
| ResNeXt-101 | 39,2 / 65,3 / 40,2 | 40,1 / 66,8 / 41,3 | SAIC-FPN 35,7 / 62,3 / 35,1 |

- **UAVDT** (ResNet-50, Table 2) : 24,6 / 38,7 / 28,0, contre 18,2 / 30,4 / 19,8 pour
  ARMNet (+6,4 AP).
- **Efficacité** (Table 3, VisDrone, GTX 1080 Ti) : 1096 images assemblées et 0,152 s,
  contre 2716 images et 0,273 s pour ClusDet, 2736 images et 0,290 s pour DMNet. Le
  backbone de cette mesure n'est pas précisé.
- **Ablation UFP** (Faster-RCNN R50, Table 4) : UFP donne 30,6 AP avec 1096 images, contre
  26,7 pour ClusDet et 28,2 pour DMNet.
- **Taux de premier plan** (Table 5) : de 10,2 à 24,5 % sur VisDrone ; la part de petits
  objets COCO passe de 68,56 à 6,96 %. Sur UAVDT : de 5,11 à 22,98 %, et de 74,87 à
  0,64 % de petits objets.
- **Ablation MP-Det** (R101, Table 6) : base 29,6 → +UFP 36,6 → +MP-Head 37,0 → +BoIW 37,5.
  UFP apporte l'essentiel, MP-Det seulement +0,9 AP.

→ reportés dans `benchmarks.csv` (fichier du lot) : 5 lignes. VisDrone R50, R101 et
ResNeXt-101 (Table 1), UAVDT R50 (Table 2), toutes `high` ; latence de 152 ms sur
GTX 1080 Ti (Table 3, `medium`, tableau reconstruit par PyMuPDF mais recoupé par un second
extrait identique).

## Limites et critique

- **« Efficient » relatif, sur GPU de bureau** : 0,152 s par image (Table 3, unité
  d'après la légende) sur GTX 1080 Ti, soit moins de 7 images/s (calculé ici). La
  comparaison ne porte que sur ClusDet et DMNet, eux aussi multi-passes, et pas sur un
  détecteur mono-passe à haute résolution. Le coût du détecteur grossier est-il compté ? n/r.
- **Latence dépendante du contenu** : le nombre et la taille des régions, donc la taille
  de la mosaïque, varient d'une image à l'autre (déduit). Ni pire cas ni gigue.
- **AP_S non rapporté**, alors que la méthode cible les petits objets. La Table 5 montre
  que le « gain » vient surtout de l'agrandissement des objets, qui ne sont plus petits
  dans la mosaïque.
- **Comparaisons hétérogènes** : les concurrents de la Table 1 ont des détecteurs de base
  et des résolutions variés. Le meilleur backbone (ResNeXt-101) et la multi-échelle
  gonflent les chiffres de tête. VisDrone est évalué sur la **validation**, le test
  n'étant pas public selon les auteurs.
- Petites incohérences entre tables : ClusDet AP75 = 24,4 (Table 1) contre 24,7
  (Table 4). Baseline+UFP R101 à 36,6 (Table 6), identique au résultat final R50.
- Pas de code annoncé dans le texte extrait.

## Pertinence pour la thèse

- **Axe `drone-detection`** : UFP est une alternative à la tête P2 pour les petits objets.
  On garde un détecteur à résolution fixe et on agrandit les zones d'intérêt. Ce schéma
  est **potentiellement plus favorable au FPGA** que P2 (déduit) : une mosaïque de taille
  fixe garde un calcul dense et régulier, contrairement à la convolution éparse de
  QueryDet (arxiv-2103.09136).
- Mais le pipeline est en deux passes (détecteur grossier puis détecteur fin), avec une
  étape de packing algorithmique (FRG, PHSPPOG) sur CPU, séquentielle et de coût variable :
  à mesurer avant tout portage embarqué.
- MP-Det (+0,9 AP) apporte peu pour un coût d'entraînement élevé ; sans intérêt matériel
  identifié.

## Gaps identifiés

- **Coarse-to-fine / packing jamais évalué sur plateforme embarquée** (Jetson, FPGA) :
  seul le GTX 1080 Ti est mesuré.
- **Coût du détecteur grossier et du packing non isolé** dans le temps d'inférence.
- **AP_S absent** des papiers « petits objets » sur VisDrone et UAVDT : même constat que
  pour QueryDet ; lien avec le gap mAP_small.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). La section « Foreground
Region Scale Equalization » est tronquée : la formule d'agrandissement est absente. Le
début de la comparaison avec l'état de l'art est déplacé sous les figures. Les Tables 3,
5 et 8 sont reconstruites par PyMuPDF, mais recoupées par un second extrait lisible.
La Table 9 (β) n'a pas de corps propre ; ses valeurs apparaissent sous la légende de la
Table 8 et sont confirmées par le texte pour β = 1,5.

Ce qui suit est déduit et non affirmé par les auteurs :
- le débit (moins de 7 images/s) calculé à partir de 0,152 s ;
- la variabilité de latence selon le contenu ;
- l'adéquation relative de la mosaïque au FPGA comparée à la convolution éparse ;
- la venue AAAI 2022.
