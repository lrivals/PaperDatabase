---
id: arxiv-2003.01285-noise-resistant-object-detection-noisy
fiche: done
date: 2026-10-18
---

# Towards Noise-resistant Object Detection with Noisy Annotations

Junnan Li, Caiming Xiong, Richard Socher, Steven Hoi, 2020, arXiv preprint. https://arxiv.org/abs/2003.01285
Type : preprint non relu par les pairs

## Problème

Entraîner un détecteur quand les annotations mêlent bruit de classe (mauvais label) et bruit de boîte (localisation imprécise), sans aucune annotation propre disponible (§1). Les méthodes existantes de bruit de labels visent la classification ; les approches faiblement/semi-supervisées exigent des annotations propres (§1). La perte de classification ne distingue pas un mauvais label d'une mauvaise boîte (§1).

## Méthode

Faster R-CNN (ResNet-50 + FPN, mmdetection, Precise RoI-Pooling), deux têtes de détection divergentes. Après un warm-up sur les annotations bruitées, alternance par mini-batch : correction des annotations (modèle fixe), puis entraînement sur les annotations corrigées (§3.1, Alg. 1).
1. CA-BBC (correction de boîte indépendante de la classe) : un pas de gradient sur la boîte pour minimiser le désaccord entre les deux classifieurs et leur score « fond » ; boîte rejetée si les deux scores fond dépassent 0,9 (§3.2).
2. Distillation à deux têtes : soft label = moyenne des deux prédictions et du label, puis sharpening (T = 0,4), et affinage de la boîte par les offsets des deux têtes (ρ = 0,5) (§3.3).
Hyper-paramètres λ = 0,1, α ∈ {0, 100, 200} choisis sur 10 % des données d'entraînement propres, utilisées seulement pour la validation (§4.2). Surcoût d'entraînement environ 24 %, aucun surcoût à l'inférence avec la première tête (§4.2).

Bruit injecté (§4.1) : bruit de label symétrique (Nl % des échantillons tirés au hasard reçoivent une autre classe, Nl de 0 à 60 %) ; bruit de boîte (toutes les coordonnées perturbées uniformément de ±Nb % de la largeur/hauteur, Nb de 0 à 40 %). À Nb = 40 %, l'IoU moyen entre boîte bruitée et boîte propre vaut 0,45 (§4.1). Bruit « machine » : un Faster R-CNN entraîné sur 10 % de COCO train2017 (40,5 mAP@.5 en validation) annote les 123k images de COCO unlabeled2017 (§4.1).

## Plateforme et implémentation

GPU/puissance : n/r. Code annoncé (« will be released »), lien non donné dans le texte lu : publication non vérifiée. Entraînement SGD, lr 0,02, momentum 0,9, weight decay 1e-4 (§4.2).

## Résultats

Dégradation du détecteur standard (« vanilla ») et récupération par la méthode, mAP@.5.

PASCAL VOC (train 07+12 trainval, test VOC07 ; Table 2). Propre : vanilla 78,2, méthode 80,1.

| Bruit boîte Nb | Bruit label Nl | Vanilla | Méthode | NOTE-RCNN (meilleur concurrent) |
|---|---|---|---|---|
| 0 % | 20 % | 72,9 | 79,1 | 76,7 |
| 0 % | 40 % | 69,3 | 77,7 | 74,9 |
| 0 % | 60 % | 62,1 | 74,1 | 69,9 |
| 20 % | 20 % | 70,7 | 76,7 | 73,7 |
| 20 % | 40 % | 66,9 | 74,8 | 70,1 |
| 40 % | 0 % | 59,3 | 71,9 | 63,4 |
| 40 % | 20 % | 54,2 | 70,6 | 61,5 |
| 40 % | 40 % | 50,0 | 69,1 | 57,8 |
| 40 % | 60 % | 45,9 | 64,5 | 53,7 |

Lecture (chiffres de Table 2, écarts calculés ici) : le bruit de boîte fait plus mal que le bruit de label à taux égal. Label seul à 40 % : -8,9 points ; boîte seule à 40 % : -18,9 points ; les deux à 40 % : -28,2 points (vanilla). La méthode ramène ce dernier cas à -11,0 points sous le propre (69,1 contre 80,1 ; contre vanilla propre 78,2 : -9,1). Le texte dit environ +20 % de mAP sur vanilla et plus de 10 % sur NOTE-RCNN à Nb = 40 %, Nl ∈ {40, 60} % (§4.4). Sur données propres, +1,9 mAP (80,1 contre 78,2), attribué aux soft labels (§4.4).

CA-BBC seul (Table 1, VOC) : Nb 40 %, Nl 0/20/40 % : 67,8 / 64,7 / 61,7 contre vanilla 59,3 / 54,2 / 50,0 ; à Nb 20 % le gain est de 0,6 à 1,7 point seulement. Maximiser seulement l'objectness (sans terme de désaccord) donne 63,2 / 59,6 / 55,7 à Nb 40 % (Table 1).

Ablation (Table 4, corps reconstruit par PyMuPDF : à vérifier ; recoupé avec Table 2, ligne « Ours » identique) : une seule tête 59,1 à Nb 40 %, Nl 60 % ; deux têtes 60,3 ; + CA-BBC 64,5 ; + ensemble des deux têtes à l'inférence 65,4. Sans CA-BBC, la perte est surtout marquée à Nb 40 % (§4.5). Température T acceptable entre 0,2 et 0,6 (Fig. 5a, lue dans le texte seulement).

MS-COCO (train2017, val2017 ; Table 3, dont l'en-tête est perdu dans l'extraction : colonnes rattachées via le texte §4.4, le -24,8 et le -7,1 sont retrouvés). Propre : 54,5 mAP@.5, 31,4 mAP@[.5,.95].

| Bruit | Vanilla mAP@.5 / @[.5,.95] | Méthode mAP@.5 / @[.5,.95] |
|---|---|---|
| Nb 20 %, Nl 20 % | 47,9 / 23,9 | 53,5 / 27,7 |
| Nb 40 %, Nl 40 % | 29,7 / 10,3 | 47,4 / 21,2 |
| Annotations machine | 41,5 / 21,5 | 46,5 / 23,2 |

À 40 %/40 %, vanilla perd 24,8 points de mAP@.5 par rapport au propre, la méthode 7,1 (§4.4). Avec bruit machine (détecteur à 40,5 mAP@.5), le gain est de +5,0 mAP@.5 (Table 3).

→ reportés dans `benchmarks.csv` : 12 lignes proposées dans `.cache/bench/arxiv-2003.01285-noise-resistant-object-detection-noisy.csv` (8 VOC, 4 COCO), à intégrer par l'agent principal.

## Limites et critique

- Détecteur à deux étages (Faster R-CNN) uniquement, avec Precise RoI-Pooling : la méthode n'est pas transposable telle quelle à YOLO (une passe, pas de RoI pooling ni de têtes jumelles) ; le papier ne teste aucun détecteur monoétage. Déduit, non affirmé.
- Bruit synthétique : label symétrique uniforme et bruit de boîte uniforme indépendant. Ce n'est pas le bruit humain réel (confusions entre classes voisines, boîtes systématiquement lâches, objets manquants, occultations). Le cas des objets non annotés (faux négatifs) n'est pas simulé ; seul le rejet de faux positifs est traité (§3.2).
- Le seul bruit réel est du pseudo-labeling par un détecteur à 40,5 mAP@.5 : cas utile mais particulier.
- Les hyper-paramètres sont réglés sur 10 % de données propres (§4.2) : contradiction partielle avec « aucune annotation propre » (§1).
- Baselines adaptées par les auteurs au cadre bruité (Co-teaching, SD-LocNet, NOTE-RCNN, §4.4), pas reprises de leur papier d'origine.
- Une seule exécution par cellule, pas d'écart-type rapporté (n/r). Les écarts de 0,1 à 0,6 point (Table 1, Nb 20 %) sont donc sans valeur.
- Preprint, code non vérifié disponible. Table 4 : corps reconstruit, chiffres recoupés avec Table 2 (identiques sur la ligne « Ours »).
- Les % de bruit de boîte sont relatifs à la taille de la boîte : pour de petits objets, le même % correspond à quelques pixels, effet non étudié.

## Pertinence pour la thèse

Pour ANNOTER / vérifier la qualité des labels d'un dataset de détection :
- Ordre de grandeur de ce que le bruit coûte à un détecteur de type Faster R-CNN : un bruit de boîte de ±20 % coûte 2,7 mAP@.5 sur VOC (75,5 contre 78,2 à Nl 0, Table 2), ±40 % coûte 18,9 ; 20 % de labels faux coûtent 5,3 ; 40 % de labels faux 8,9 (Table 2, calculs ici). Priorité pratique : la précision des boîtes importe plus que la pureté des classes, jusqu'à ces taux. Inférence à partir de VOC/Faster R-CNN, à ne pas extrapoler sans test à YOLO.
- Sur COCO, 40 % de bruit des deux types fait chuter la mAP@[.5,.95] de 31,4 à 10,3 (Table 3) : le critère strict de localisation souffre le plus ; avec la correction, 21,2.
- Un dataset dont les boîtes sont décalées de l'ordre de 20 % et dont 20 % des labels sont faux reste utilisable (vanilla : -7,5 points sur VOC, -6,6 sur COCO mAP@.5 ; avec correction : -3,4 et -1,0). Au-delà de 40 % de bruit de boîte, un entraînement standard devient peu fiable.
- Pour PRÉ-ANNOTER (pseudo-labels) : des annotations produites par un détecteur à 40,5 mAP@.5 donnent, avec l'entraînement standard, 41,5 mAP@.5 sur val2017, et 46,5 avec la correction (Table 3) : le bruit machine se corrige.
- Pour AUGMENTER : le résultat annexe des soft labels (+1,9 sur données propres, §4.4) est un effet proche du label smoothing, applicable en principe sans bruit, non testé sur YOLO ici.
- Quand l'appliquer : lorsqu'on dispose de beaucoup d'annotations bon marché (crowd rapide, pseudo-labels) et d'un détecteur à deux étages ; sinon, la valeur du papier est son tableau de dégradation. Laisse ouvert : détecteurs monoétages/YOLO, bruit réaliste, objets manquants, petits objets.

## Gaps identifiés

- Sensibilité de YOLO (Ultralytics) à des taux contrôlés de bruit de label et de boîte : aucun chiffre ici, seulement Faster R-CNN.
- Bruit réaliste (annotateurs humains, boîtes lâches, objets non annotés) non simulé ici.
- Seuil de bruit de boîte en pixels pour les petits objets.
- Correction de bruit sur détecteur monoétage.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction grobid ok). Table 3 : en-tête perdu, colonnes rattachées via le texte (§4.4) ; Table 4 : corps reconstruit par PyMuPDF, recoupé avec Table 2. Fig. 5a (courbe en T) non lisible : seule la plage 0,2 à 0,6 du texte est reprise.
Ce qui suit est déduit et non affirmé par les auteurs : écarts de points calculés à partir des tableaux (différences entre cellules), conclusion « boîte plus nuisible que label », non-transposabilité à YOLO, remarque sur les petits objets.
