---
id: arxiv-1801.05124-localization-aware-active-learning-object
fiche: done
date: 2026-10-18
---

# Localization-Aware Active Learning for Object Detection

Chieh-Chi Kao, Teng-Yok Lee, Pradeep Sen, Ming-Yu Liu, 2018, arXiv preprint. https://arxiv.org/abs/1801.05124
Type : preprint non relu par les pairs

## Problème

L'annotation d'un détecteur est chère : tracer une boîte serrée coûte environ 10 fois plus qu'une
question à choix multiple (§1), et tracer une boîte « de zéro » prend 20 s en moyenne contre 2 s
pour vérifier qu'une boîte est serrée (§5, citant [29] et [20]). L'active learning existant
pour la détection ne mesure que l'incertitude de classification (§1, §2). Les auteurs veulent des
mesures d'incertitude de **localisation**, calculables sans vérité terrain, pour choisir quelles
images annoter.

## Méthode

Boucle (§3.1, Fig. 1) : détecteur de base entraîné sur un petit lot annoté, scoring du pool non
annoté, sélection d'un sous-ensemble, annotation humaine, ré-entraînement ; un cycle = un « round ».
Granularité : **image entière** (pas de sélection de boîtes).

- **Incertitude de classification (C)** : U_B(B) = 1 - P_max(B) par boîte ; U_C(image) = max sur les
  boîtes de l'image (§3.1). C'est le baseline.
- **Localization Tightness (LT/C)** (§3.2) : T(B) = IoU(boîte finale, proposition de région dont
  elle est issue) ; score de boîte J = |T + P_max - 1| (Éq. 1), score d'image = min sur les boîtes ;
  on annote les images à score **bas**. Cible les incohérences classification/localisation :
  classe certaine mais boîte lâche (P_max=1, T=0) ou boîte serrée mais classe incertaine. Exige un
  détecteur à propositions (Faster R-CNN), inapplicable à SSD/YOLO (§4).
- **Localization Stability (LS)** (§3.3) : bruit gaussien ajouté aux pixels à N=6 niveaux
  (écarts-types 8, 16, 24, 32, 40, 48 sur [0,255]) (§4.1) ; pour chaque boîte de référence, la boîte
  bruitée de plus fort IoU est retenue ; S_B = IoU moyen sur les niveaux (Éq. 2) ; S_I(image) =
  moyenne des S_B pondérée par P_max (Éq. 3). Applicable à tout détecteur, y compris sans
  propositions. Combinaison **LS+C** : score = U_C - lambda * S_I, lambda = 1 (§4) ; on annote les
  scores **hauts** (classe incertaine et localisation instable).
- Variantes : LS seul, LT/C(GT) (tightness calculée avec la vérité terrain, borne haute), 3in1
  (C + LS + LT) (§4, annexe C).

Protocole (§4) : le « pool non annoté » est le train set d'un jeu déjà annoté, les boîtes servent
d'annotation sans humain.

| Jeu | Pool | Test | Budget initial | Pas | Rounds | Essais | Entraînement |
|---|---|---|---|---|---|---|---|
| VOC2012, FRCNN-VGG16 (§4.1) | train 5 717 | val 5 823 | 500 | 200 | 15 | 5 | 20 époques |
| VOC2007, FRCNN-VGG16 (§4.2) | trainval 5 011 | test 4 952 | 500 | 200 | 15 | 5 | idem 4.1 |
| MS COCO, FRCNN-VGG16 (§4.3) | train 80k | val 40k | 5 000 | 1 000 | 4 | 3 | 12 époques |
| VOC2007, SSD 300x300 (§4.4) | trainval 5 011 | test 4 952 | 500 | 200 | 15 | 5 | 40 000 itérations |

FRCNN : entrée redimensionnée à 600 px sur le petit côté (§4.1). Baselines : Random (R) et C.

## Plateforme et implémentation

Sans objet (pas de matériel embarqué). Détecteurs : Faster R-CNN (RoI warping) et SSD, backbone
VGG16 préentraîné (§4). Temps : propagation avant FRCNN 137 ms/image, soit 82,5 % du temps de C seul ;
LT/C coûte autant que C, LS coûte plusieurs passes du détecteur (une par niveau de bruit, plus la
référence) (§5). Code : non publié d'après le texte (aucun lien dans `fulltext.md`) ; déduit.

## Résultats

Gain **par rapport à C** (économie relative d'annotation, moyenne sur la zone mesurée, Fig. 5b/7b) :
- VOC2012 : LS+C +96,5 %, LT/C +36,3 % (§4.1).
- VOC2007 : LS+C +81,9 %, LT/C +45,2 % (§4.2). Attention : le résumé inverse les deux jeux
  (96,5 % pour 2007, 81,9 % pour 2012) ; le corps du texte fait foi ici, à vérifier.
- SSD / VOC2007 : pour atteindre la performance du hasard entre 2 300 et 3 500 images, LS+C
  économise 12-22 % des images contre 6-15 % pour C ; LS+C « 29,0 % mieux » que C en moyenne (§4.4).

Gain **par rapport au hasard (R)** :
- Résumé : jusqu'à 25 % de données annotées en moins ; §5 : « 20-25 % d'images à annoter en
  moins ». Ces valeurs maximales ne sont pas données par jeu dans le texte (lues sur les courbes, non
  accessibles ici) : n/r par jeu, sauf COCO.
- COCO : C n'apporte rien par rapport à R (Fig. 8a) ; LS+C économise 5 % d'annotation par rapport à R (§4.3).

mAP après 3 rounds, soit 1 100 images annotées (moyenne de 5 essais) :

| Méthode | VOC2012 val (Table 1) | VOC2007 test (Table 2) |
|---|---|---|
| R (hasard) | 52,9 | 57,3 |
| C | 54,0 | 57,8 |
| LS+C | 55,3 | 59,4 |
| LT/C | 54,7 | 58,6 |

Classes difficiles (AP < 40 % en R) : sur VOC2012 (5 classes), LS+C gagne +3,95 points d'AP sur C
contre +0,38 pour les 15 autres ; sur VOC2007 (4 classes) +3,94 contre +0,95 (§4.1, §4.2). C est en
moyenne 0,50 pt sous le hasard sur les classes difficiles de VOC2012 (§4.1). LT/C(GT) fait mieux que
tout le reste (§4.1) ; LT/C estimé s'en approche entre 500 et 1 100 images. LS+C > LS seul et > C
seul (annexe C). 3in1 n'améliore pas LS+C : les cues de localisation ne sont pas complémentaires
(annexe C). Les images choisies par C et LS+C se recouvrent à 34,0 % (Table 5 ; la Table 6, reconstruite
par PyMuPDF, a les mêmes valeurs, à vérifier).

→ reportés dans `benchmarks.csv` : lignes proposées (5) dans `.cache/bench/arxiv-1801.05124-localization-aware-active-learning-object.csv` : LS+C et LT/C sur VOC2012 et VOC2007 (mAP à 1 100 images, Tables 1-2) et LS+C sur COCO (économie 5 %, §4.3). Baseline C et R en colonne `baseline`.

## Limites et critique

- Annotation simulée : les boîtes du dataset sont utilisées comme « annotation » ; aucun annotateur
  réel, donc aucun coût d'annotation mesuré, ni effet du bruit humain.
- Petits budgets : 500 à 1 700 images sur VOC, pool de 5 à 6 k images ; extrapolation à de grands
  jeux non démontrée (COCO : gain de 5 % seulement, 4 rounds, 3 essais).
- Détecteurs anciens (FRCNN/SSD VGG16, 2018) ; aucun détecteur de type YOLO ni anchor-free. LT/C
  est inapplicable sans étage de propositions ; seul LS s'applique, et ses gains n'ont été mesurés
  sur SSD que sur VOC2007.
- LS multiplie le coût de scoring (N+1 passes par image du pool) ; le papier n'en donne pas le temps
  total, seulement 137 ms par passe FRCNN (§5). Le surcoût est jugé négligeable face à l'annotation
  humaine (argument de coût, pas mesuré).
- « Amélioration relative de 96,5 % » est une métrique relative à C (économie moyenne d'images), pas
  un gain de mAP : le gain absolu de mAP est de 1,3 à 1,6 point à 1 100 images (Tables 1-2). Résumé et
  corps du texte attribuent 96,5 / 81,9 % à des jeux inversés.
- Hypothèse de LS : détecteur sensible au bruit gaussien ; les auteurs montrent que AlexNet/VGG16/
  ResNet101 perdent 23-37 % de top-1 avec le bruit maximal (annexe B) ; si l'augmentation (Mosaic,
  jitter) rend le détecteur robuste, LS tend vers 1 et retombe sur C (§5) : à vérifier pour YOLO
  (déduit).
- Tables 3, 4, 7 sans corps extrait : chiffres des variantes LS et 3in1 non lus ; Table 1 et Table 2
  proviennent du texte extrait (Table 2 mal formatée, valeurs de mAP en dernière colonne).
- Préprint, pas de code publié, écarts-types entre essais seulement en figures.

## Pertinence pour la thèse

**Construire / annoter** : quand le budget d'annotation est limité, ce papier donne une recette
pour choisir les images à annoter, avec un détecteur déjà entraîné sur ~500 images : score
U_C - S_I (classe incertaine + boîtes instables sous bruit). À appliquer quand le pool non annoté
est grand et la boîte coûteuse (fort coût par image, classes rares ou difficiles : le gain porte
surtout sur les classes dont l'AP est < 40 %, +3,9 pt d'AP). Pour YOLO : seul LS+C est
directement utilisable (pas de propositions), il demande N passes d'inférence par image du pool
(6 niveaux de bruit dans le papier). **Prétraiter** : la sélection ne change pas le format ; elle
décide quoi envoyer à l'annotation. **Augmenter** : LS suppose que le détecteur n'est pas
résilient au bruit ; l'interaction avec une augmentation photométrique/bruit n'est pas testée.
**Limite d'application** : gain mesuré uniquement par rapport au hasard et à C sur 3 jeux
(VOC07/12, COCO) avec FRCNN/SSD ; chiffres non transférables tels quels à YOLO. Voir aussi
`pdb cited-by` pour les travaux postérieurs.

## Gaps identifiés

- Active learning pour détecteurs de type YOLO / anchor-free avec comparaison à des stratégies
  récentes (diversité, embeddings) : non couvert par ce papier.
- Coût réel (temps humain) de l'annotation sélectionnée vs aléatoire, avec annotateurs réels.
- Effet de l'augmentation (Mosaic, bruit) sur la mesure de stabilité LS.
- Sélection à l'échelle de la boîte plutôt que de l'image (non traité).

## Statut de lecture

Papier complet (`fulltext.md` lu, extraction grobid ok). Tables 3, 4, 7 sans corps extrait : variantes
LS/3in1 et essai unique non lus en chiffres. Table 6 reconstruite par PyMuPDF (à vérifier). Les
courbes (Fig. 5-9, 13-17) ne sont pas lisibles : économies par round non relevées. Déduit et non
affirmé par les auteurs : absence de code publié, inapplicabilité de LT/C aux détecteurs à une étape
(les auteurs l'écrivent pour SSD, extension à YOLO déduite), interaction LS / augmentation, gain
absolu de mAP calculé par différence des Tables 1-2.
