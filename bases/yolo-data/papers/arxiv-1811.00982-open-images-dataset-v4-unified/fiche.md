---
id: arxiv-1811.00982-open-images-dataset-v4-unified
fiche: done
date: 2026-10-05
---

# The Open Images Dataset V4: Unified image classification, object detection, and visual relationship detection at scale

Alina Kuznetsova, Hassan Rom, Neil Alldrin, Jasper Uijlings, Ivan Krasin, Jordi Pont-Tuset, Shahab Kamali, Stefan Popov, Matteo Malloci, Alexander Kolesnikov, Tom Duerig, Vittorio Ferrari, 2018, arXiv preprint. https://doi.org/10.1007/s11263-020-01316-z (DOI de la version journal ultérieure, d'après `metadata.json` ; le texte lu est le preprint arXiv 1811.00982)
Type : preprint non relu par les pairs

## Problème

Les datasets de détection existants sont petits (COCO : 886k boîtes ; ILSVRC-Det : 534k ; Table 6) ou
biaisés par un choix de classes a priori. Les auteurs veulent un dataset à très grande échelle
(9,2 M d'images, 15,4 M de boîtes sur 600 classes, 30,1 M de labels d'image sur 19 794 classes,
375k relations visuelles ; Abstract, §1) avec des annotations unifiées sur les mêmes images, et
posent la question de fond : comment annoter à cette échelle à un coût et une qualité acceptables ?

## Méthode

Tout le papier est une méthodologie de constitution et de contrôle qualité.

**Images (§2.1).** Flickr CC-BY (nov. 2015), sans liste de classes ni de tags préalable
(statistiques de classes « naturelles ») ; suppression du contenu inapproprié, des quasi-doublons
et des images présentes ailleurs sur Internet (pour favoriser les scènes complexes) ; copies
1600HQ (côté long <= 1600 px, JPEG q90) et 300K (~300 000 px, q72). Split train / val / test :
9 011 219 / 41 620 / 125 436 (§2.1).

**Labels d'image (§2.3) : générés par machine puis vérifiés par humains.** Un classifieur
(variante Inception-V2 entraînée sur JFT, > 300 M d'images bruitées) propose des labels candidats ;
val/test : tous les labels de score > 0,5 sont vérifiés (§2.3.1). Train : des dizaines de
classifieurs, candidats choisis par échantillonnage stratifié sur le logit (largeur de strate
w = 2, k = 10 images par strate), ce qui donne un mélange de positifs faciles / négatifs durs en
confiance haute et de positifs durs / négatifs faciles en confiance basse (§2.3.2). Vérification
humaine par vote majoritaire : 7 annotateurs crowdsourcés, ou 3 internes pour les classes
difficiles et 1 pour les classes faciles, dont les boxables (§2.3.3). Résultat : labels positifs
ET négatifs vérifiés ; tout label non vérifié est « inconnu » (annotation non exhaustive).
Part de labels crowdsourcés : 5,5 M sur 27,9 M en train (~20 %, Table 4), < 1 % en val/test.

**Boîtes (§2.4).** Définition donnée aux annotateurs : « la plus petite boîte contenant toutes
les parties visibles de l'objet » ; 2 exemples parfaits par classe (600 classes), erreurs
courantes montrées pour 20 % des classes (pilotes), un annotateur travaille sur une seule classe
à la fois (§2.4.1). Cas limites culturels (la main incluant ou non le bras, Fig. 6).
- *Extreme clicking* : 90 % des boîtes (§2.4.2). 4 clics sur les points extrêmes haut / bas /
  gauche / droite de l'objet. Formation automatisée : 10 objets pour chacune des 20 classes VOC
  avec retour automatique, puis qualification de 800 boîtes (IoU > 0,84 avec la vérité et <= 20 s
  par boîte). Il n'y a donc pas de vérification a posteriori des boîtes.
- *Box verification series* : ~10 % des boîtes de train (1,5 M, historiquement les premières ;
  §2.4.3, « Historical process »). Un Faster R-CNN (Inception-ResNet) propose une boîte à partir
  du label d'image, l'annotateur l'accepte (IoU > 0,7 avec une boîte parfaite imaginaire) ou la
  rejette ; 4 tentatives au plus, les boîtes rejetées élaguent l'espace de recherche, le détecteur
  est réentraîné périodiquement. Taux d'acceptation 48 % (détecteur initial) puis 70 % (final).
  Les annotateurs sont formés sur 360 boîtes VOC (retour toutes les 9 réponses ; 3 tours ; 80 %
  qualifiés ; Fig. 10).
- Les 13,1 M de boîtes restantes en train, ainsi que tout val/test, sont en extreme clicking, pour
  tous les labels positifs ; la boîte existe donc même si la série de vérification a échoué (§2.4.3).
- *Dé-duplication hiérarchique* (§2.4.4) : en train, on supprime avant annotation les labels
  parents d'un label enfant déjà présent (animal si zebra) ; en val/test, on annote tout puis on
  retire le parent s'il recouvre un enfant à IoU > 0,8.
- *Attributs* (§2.4.5) : GroupOf (> 5 instances qui s'occultent fortement, une seule boîte),
  Partially occluded, Truncated, Depiction (dessin, statue), Inside ; plus le mode de production
  de la boîte (verification series ou extreme clicking).

**Relations visuelles (§2.5)** : 326 triplets candidats, boîtes appariées si elles se
recouvrent après agrandissement de 20 %, puis vérification humaine (2,6 s par triplet ; taux
d'acceptation 28,2 % en moyenne, Table 1). Hors du cœur de cette base.

**Métrique (§5.2.1).** mAP VOC 2012 modifiée : détections des classes non annotées ignorées,
détection d'une classe à label négatif = faux positif, AP des classes parents calculée avec
leurs descendants, boîtes GroupOf traitées avec un poids w (w = 1 retenu : au moins une
détection dans la boîte).

## Plateforme et implémentation

Papier de dataset, pas d'implémentation embarquée. Détecteurs de référence : Faster R-CNN
Inception-ResNetV2 et SSD MobileNetV2 (depth 1,0, entrée 300 x 300), pré-entraînés ILSVRC-2012,
8 à 20 M de pas sur 8-24 GPU (Tesla P100/V100), vitesse d'inférence mesurée sur Titan X Pascal
(§5.2.2, Table 14 dont le corps n'a pas été extrait : valeurs n/r). Données et annotations
publiées sur https://g.co/dataset/openimages/ (§1) ; code d'entraînement : non publié d'après le
texte (détecteurs et classifieurs « Google-internal », §2.3.2).

## Résultats

Qualité et coût de l'annotation (le cœur utile) :

| Mesure | Valeur | Source |
|---|---|---|
| Temps moyen par boîte, extreme clicking | 7,4 s (dessin seul 25,5 s pour ILSVRC) | §2.4.2 |
| Total ILSVRC par boîte (médiane) | 42 s = 25,5 dessin + 9,0 vérification + 7,8 contrôle des autres instances | §2.4.2 |
| Vérification d'une boîte proposée | 3,5 s ; 8,5 s par boîte produite (échecs inclus) | §2.4.3 |
| Précision des boîtes (1 classe donnée, > 26 000 boîtes, 150 classes, expert) | 97,7 % ; erreurs : imprécise 1,1 %, mauvaise classe 1,1 %, multi-objets 0,1 % | Table 12, §4.1 |
| Rappel des boîtes (pour un label d'image positif) | 98,2 % | Table 12, §4.3 |
| Accord géométrique, extreme clicking (50 000 boîtes redessinées) | IoU moyen 0,87 (PASCAL : 0,88) | §4.2 |
| Accord géométrique, box verification series (1 % redessiné) | IoU moyen 0,77 | §4.2 |
| Entraîner sur boîtes vérifiées vs dessinées (mêmes instances) | écart < 0,001 mAP OI | §4.2 |
| Rappel des labels d'image (boxables), toutes classes d'objets | 43 % ; 59 % sans les objets « difficult » ; COCO : 83 % | §4.3 |
| Précision / rappel des attributs | « high nineties » pour la plupart ; Depiction rappel 92 % ; Inside précision 67 % ; Building 100 % / 83 % | §4.1 (Table 13 sans corps) |

Statistiques utiles à l'entraînement : fréquence des attributs en train : Occluded 66,06 %,
Truncated 25,09 %, GroupOf 5,99 %, Depiction 5,45 %, Inside 0,24 % (Table 7 ; COCO crowd :
1,17 %). 43 % des boîtes occupent moins de 1 % de l'aire de l'image (§3.2, Fig. 20). Boîtes par
image : 8,4 en train, 4,9 / 5,0 en val/test V4 (V5 : 7,3 / 7,5 ; Table 5, Table 8) ; jusqu'à 742
boîtes dans une image (§3.2). Le nombre de boîtes par classe est très déséquilibré : 3 505 362
instances pour l'agglomérat de classes « personne » contre 257 253 pour COCO, mais 517 classes
dépassent la plus rare de COCO (198 instances ; §3.2).

Effet de la quantité de données (§5.2.2, Fig. 30, valeurs lues sur figure donc n/r) : Faster
R-CNN continue de progresser jusqu'à 14,6 M de boîtes (sous-ensembles 10k, 100k, 1M, 14,6M) ;
SSD MobileNetV2 sature vers 1 M de boîtes. Labels d'image : plus de labels vérifiés = meilleur
mAP, et les négatifs vérifiés comptent surtout à saturation des positifs (§5.1, Fig. 28).
Effet de la métrique : ignorer les classes non annotées est le composant qui change le plus le
score (Fig. 29).

Détection fine sans boîtes fines (§6.1, Table 17, mAP@0,5 ; baselines = sous-classe aléatoire
uniforme / la plus fréquente / aléatoire selon le prior, toutes < 0,05) : Car 0,287 (57 classes),
Cat 0,231 (61), Dog 0,272 (33), Flower 0,594 (102). Un seul objet de la classe boîte dans l'image
permet de lui transférer les labels d'image plus fins.

Visual relationship detection (Table 15) : FREQ 5,36 mAP, FREQ-OVERLAP 8,19, BAR-CNN 14,63.

→ reportés dans `benchmarks.csv` : 9 lignes proposées (4 fine-grained détection, Table 17 ;
5 relations visuelles, Table 15) ; pas de ligne pour les courbes de Fig. 28-30 (valeurs non
lisibles en texte) ni pour la Table 14 (corps absent).

## Limites et critique

- Le dataset n'est **pas exhaustif** au niveau image : rappel des labels d'image 43 % (59 % sans
  objets difficiles), contre 83 % pour COCO (§4.3). Une classe absente des labels n'est pas
  « absente de l'image » : seuls les négatifs vérifiés le garantissent. Un détecteur de type
  YOLO entraîné tel quel avec une perte standard pénalise ces objets non annotés comme fond ;
  la métrique OI (§5.2.1) ignore les classes non annotées, la perte YOLO d'Ultralytics non
  (déduit, non affirmé par les auteurs).
- La qualité est mesurée sur 150 classes seulement (ordre alphabétique) et 100 images par classe,
  jugées par des experts dont l'accord entre eux n'est pas rapporté (§4.1).
- Les boîtes sont dessinées par des annotateurs internes à Google, formés et qualifiés : le coût
  de 7,4 s n'inclut pas la formation ni la qualification (800 boîtes), et ne se transpose pas à
  un crowdsourcing non formé (le papier ne le teste pas pour les boîtes).
- Val/test V4 moins denses en boîtes que train (5 contre 8,4 par image) : biais de mesure
  corrigé seulement en V5 (Table 8).
- Les attributs : définition de GroupOf (> 5 instances) différente de crowd COCO ; Inside peu
  fiable (précision 67 %, §4.1).
- Preprint ; les expériences de détection utilisent des modèles internes non reproductibles ;
  la courbe de Fig. 30 n'est pas chiffrée dans le texte.
- Comparaison de temps biaisée : les 42 s d'ILSVRC sont une médiane reprise d'un autre papier
  (§2.4.2), contre une moyenne mesurée ici.

## Pertinence pour la thèse

Thème de la base : préparer des données pour la détection YOLO. Ce que le papier apprend :

- **CONSTRUIRE** : pas de liste de classes imposée par la collecte ; filtrage des doublons et des
  images simples ; 2 résolutions (1600HQ / 300K). Beaucoup de données restent utiles pour un
  modèle large (Faster R-CNN progresse jusqu'à 14,6 M de boîtes) mais un petit modèle sature
  tôt (SSD MobileNetV2 vers 1 M de boîtes, §5.2.2) : pour un YOLO « nano » embarqué, quelques
  millions de boîtes suffisent déjà (déduit : pas testé sur YOLO).
- **ANNOTER** : (1) extreme clicking : 7,4 s par boîte contre 25,5 s pour le dessin classique,
  IoU entre annotateurs 0,87 ; à utiliser dès que l'on a > quelques milliers de boîtes à dessiner
  à la main, avec une phase de formation automatique avec retour. (2) Pré-annotation par un
  détecteur puis vérification binaire (accepter si IoU > 0,7) : 8,5 s par boîte produite,
  IoU 0,77 avec une boîte dessinée, et même mAP à l'entraînement (< 0,001 d'écart, §4.2) : à
  appliquer quand on a un détecteur initial (même faible : 48 % d'acceptation au départ) et des
  labels d'image ; les 77 % d'IoU suffisent pour entraîner. (3) Consignes : « plus petite boîte
  contenant toutes les parties visibles », 2 exemples parfaits par classe, erreurs courantes
  montrées avant la séance, une classe à la fois ; prévoir des cas culturels / ambigus.
- **Contrôler la qualité** : mesurer la précision (97,7 %) et le rappel (98,2 %) des boîtes sur
  un échantillon revu par un expert (100 images par classe), l'accord géométrique par
  redessinage (50 000 boîtes) et le rappel des labels d'image sur 100 images à deux experts :
  protocole directement réutilisable sur un dataset maison. Les erreurs de boîte dominantes sont
  l'imprécision et la mauvaise classe (1,1 % chacune).
- **Attributs et usage à l'entraînement** : Occluded (66 %) et Truncated (25 %) sont très
  fréquents ; ils ne sont pas utilisés par les auteurs pour pondérer l'entraînement (le texte
  ne rapporte aucune ablation sur leur usage en entraînement : n/r). Usage décrit : GroupOf à
  l'évaluation (w = 0 région ignorée, w = 1 une détection requise dans la boîte) ; les images
  avec > 80 boîtes (jusqu'à 742) suggèrent de marquer GroupOf pour réduire le coût (Fig. 15).
  Pour un format YOLO (bbox normalisées, pas d'attributs), le choix pratique à retenir est de
  traiter les GroupOf comme des boîtes uniques d'un groupe (ou de les exclure / ignorer en
  perte) : déduit, à tester.
- **Labels partiels** : explicites sur positifs / négatifs vérifiés, évaluation qui ignore les
  classes non annotées (Fig. 29, effet le plus fort) ; à répliquer si l'on fusionne des datasets
  à classes différentes ou si l'on annote seulement un sous-ensemble de classes par image.
- **Hiérarchie de classes** : dé-duplication des parents ; à copier pour éviter deux boîtes sur
  un même objet (animal + zebra) quand on fusionne des taxonomies.
- **AUGMENTER / PRÉTRAITER** : n'apporte rien directement (pas d'augmentation décrite). La
  taille des boîtes (43 % < 1 % de l'aire) signale un régime petits objets (voir tiling / SAHI).
- Pistes : la transformation d'image-labels fins en boîtes fines (§6.1) est un moyen
  d'enrichir un dataset sans redessiner de boîtes.

Reste ouvert : le gain d'une pré-annotation modèle-fondation moderne (SAM, open-vocabulary) par
rapport à l'extreme clicking, le coût en conditions non formées, et l'impact des attributs en
perte d'entraînement.

## Gaps identifiés

- Aucune mesure de l'effet de l'usage des attributs (Occluded, Truncated, GroupOf) dans la perte
  d'entraînement d'un détecteur (le papier ne l'évalue qu'en métrique).
- Coût par boîte avec des annotateurs non formés (crowd) ou avec SAM : non couvert ici.
- Pas d'étude du bruit résiduel (1,1 % imprécises + 1,1 % mauvaise classe) sur la mAP de YOLO.
- Sur-représentation des négatifs vérifiés : effet sur la perte de classification de YOLO non testé.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). Tableaux sans corps extrait
(avertissement de `metadata.json`) : Tables 1, 4, 5, 7, 9, 10, 12, 14, 17, 19 listées « sans
corps » mais leur contenu est en partie récupéré en fin de `fulltext.md` ; Table 13 (précision /
rappel par attribut) et Table 14 (paramètres, vitesse) : chiffres exacts non lus, seules les
valeurs citées dans le texte sont reprises ; Tables 15 et 17 lues dans un corps reconstruit (colonnes
à vérifier). Les courbes de Fig. 28, 29, 30 ne sont pas chiffrées : n/r.
Ce qui suit est déduit et non affirmé par les auteurs : l'effet des labels non annotés sur la
perte YOLO, l'adéquation à un YOLO nano, le traitement de GroupOf pour un format YOLO, et la
transposition du coût de 7,4 s hors d'un contexte d'annotateurs internes formés.
