---
id: arxiv-1803.03243-domain-adaptive-faster-r-cnn
fiche: done
date: 2026-10-18
---

# Domain Adaptive Faster R-CNN for Object Detection in the Wild

Yuhua Chen, Wen Li, Christos Sakaridis, Dengxin Dai, Luc Van Gool, 2018, arXiv preprint. https://arxiv.org/abs/1803.03243
Type : preprint non relu par les pairs

## Problème

Un détecteur entraîné sur un domaine source perd beaucoup de performance sur un domaine cible
visuellement différent (style, éclairage, taille des objets, caméra, météo, synthétique vs réel)
(Intro, Fig. 1). Collecter des données cibles annotées est jugé coûteux (annoter des bbox est
« expensive and time consuming », Intro). Les auteurs posent donc l'adaptation non supervisée :
images + labels côté source, images cibles sans aucun label (§4).

## Méthode

Faster R-CNN (§3.1) augmenté de deux classifieurs de domaine entraînés de façon adversariale
(couche d'inversion de gradient, GRL) : au niveau image (un classifieur par activation de la carte
de caractéristiques, donc par patch ; style, échelle, éclairage ; Eq. 6) et au niveau instance
(vecteurs de caractéristiques par ROI ; apparence, taille ; Eq. 7). Une régularisation de
consistance rapproche les deux classifieurs pour rendre le RPN invariant au domaine (Eq. 8).
Perte totale `L_det + λ(L_img + L_ins + L_cst)`, λ = 0,1 (§4.3, §5.1). À l'inférence, les
composants d'adaptation sont retirés : détecteur Faster R-CNN inchangé, poids adaptés (Fig. 2).
Réglages : entrée redimensionnée à 500 px de côté court, batch de 2 images (une source, une cible),
50k itérations à 0,001 puis 20k à un pas réduit, init ImageNet (§5.1).

## Plateforme et implémentation

Détecteur à deux étages, backbone non précisé dans le texte extrait (un VGG-M plus petit n'est cité
que pour l'étude d'échelle, §5.4) ; matériel d'entraînement n/r. Code publié : non mentionné dans
`fulltext.md`.

## Résultats

Métrique : AP / mAP à IoU 0,5 (§5.1). Aucune annotation cible utilisée. « Gain » = différence
absolue en points d'AP.

| Scénario (source → cible) | Sans adaptation | Adaptation complète | Gain | Source |
|---|---|---|---|---|
| SIM10k (synthétique, GTAV) → Cityscapes val, AP voiture | 30,12 | 38,97 | +8,85 (texte : « +8.8% ») | Table 1, §5.2.1 |
| Cityscapes → Foggy Cityscapes val, mAP 8 classes | 18,8 | 27,6 | +8,8 (texte : « +8.6% ») | Table 2 (illisible en partie), §5.2.2 |
| KITTI → Cityscapes, AP voiture | 30,2 | 38,5 | +8,3 | Table 3, §5.2.3 |
| Cityscapes → KITTI, AP voiture | 53,5 | 64,1 | +10,6 | Table 3, §5.2.3 |

Ablation SIM10k → Cityscapes (Table 1, §5.2.1) : image seul 33,03 (+2,9) ; instance seul 35,79
(+5,6) ; image + instance 37,86 (+7,7) ; avec consistance 38,97 (+8,8).
Ablation KITTI ↔ Cityscapes (Table 3) : deux variantes à un seul composant donnent 36,6 / 34,6
(K→C) et 60,9 / 57,6 (C→K) ; l'attribution image vs instance est perdue dans le tableau
reconstruit (voir Limites). Les deux composants combinés : 37,3 (K→C), 62,7 (C→K).
Qualité des propositions du RPN (K→C, Table 4) : meilleur recouvrement moyen des 300 premières
propositions 18,8 → 28,5 (sans consistance) → 30,3 (avec).
Échelle (Fig. 4, §5.4, courbes non lisibles dans le texte) : le Faster R-CNN non adapté « chute
nettement » quand l'échelle des images cibles diffère de celle de la source (500 px) ; le modèle
adapté profite de la haute résolution cible (200 à 1000 px). Aucune valeur chiffrée lisible.
Analyse d'erreurs (Fig. 3, K→C) : chaque composant augmente les détections correctes et réduit les
faux positifs ; l'alignement instance donne plus d'erreurs « background » que l'alignement image.

Ampleur du décalage de domaine (ce que mesure le Faster R-CNN non adapté) : la chute n'est pas
quantifiée par rapport à un entraînement sur le domaine cible (aucune borne supérieure « oracle »
rapportée). On ne lit que les écarts avant/après adaptation : +8 à +11 points d'AP, soit +29 %
(SIM10k), +47 % (météo, mAP), +27 % (K→C) et +20 % (C→K) en relatif (calculs déduits des Tables 1
à 3).

→ reportés dans `benchmarks.csv` : 11 lignes proposées (SIM10k → Cityscapes : 5 ; Cityscapes →
Foggy : 2 ; K→C : 2 ; C→K : 2). Les lignes à un seul composant des Tables 2 et 3 sont omises car
leur attribution est ambiguë. Toutes en `confidence: medium` (tableaux reconstruits par PyMuPDF).

## Limites et critique

- Le texte ne donne aucun chiffre « entraîné et testé sur la cible avec labels » : impossible de
  dire quelle part de l'écart est récupérée ; on ne sait pas ce que coûterait d'annoter le domaine
  cible. Déduit : l'écart à l'oracle reste probablement grand (AP voiture 38,97 sur Cityscapes
  contre un détecteur supervisé non rapporté ici).
- Tables 1, 3 et 4 « reconstruites par PyMuPDF : à vérifier » ; Table 2 en partie illisible : les
  mAP par classe sont mélangées entre lignes, et l'attribution image vs instance des lignes
  intermédiaires n'est pas fiable. Valeurs de la Table 2 retenues : baseline 18,8 et complet 27,6
  seulement. Incohérence : le texte annonce +8,6 pour la météo alors que 27,6 − 18,8 = 8,8.
- Foggy Cityscapes est un brouillard simulé sur de vraies scènes (§5.2.2), pas du vrai brouillard ;
  le gain réel sous brume n'est pas démontré.
- Cityscapes n'est pas un jeu de détection : les bbox sont les rectangles englobants des masques
  d'instances (§5.2.1) ; une seule classe (voiture) pour SIM10k et KITTI.
- Un seul détecteur (Faster R-CNN à deux étages), 500 px, IoU 0,5 ; aucune évaluation sur un
  détecteur monoétage de type YOLO. Pas de comparaison à d'autres méthodes dans le texte extrait
  (les tableaux évoquent « other baselines » sans les donner), pas de barres d'erreur ni de graines.
- Preprint ; le texte ne mentionne pas de code publié.

## Pertinence pour la thèse

Pour CONSTRUIRE un dataset : le décalage de domaine est un coût de mesure, pas une hypothèse. Un
détecteur entraîné sur du synthétique (SIM10k, 10 000 images GTAV, 58 701 voitures, §5.2.1)
atteint 30,12 AP voiture sur Cityscapes réel, et une simple adaptation sans label cible monte à
38,97 ; la caméra seule fait perdre autant (30,2 pour K→C contre 53,5 pour C→K : l'asymétrie
montre aussi que la direction compte, le dataset cible ou source plus simple donne un meilleur
chiffre). À réserver aux cas où l'on ne peut pas annoter le domaine cible : si on le peut, annoter
quelques images cibles est l'alternative que ce papier ne mesure pas. Pour ANNOTER : à budget
nul, l'adaptation sans label récupère 8 à 11 points, mais le papier ne dit pas combien d'images
cibles étiquetées feraient mieux ; à tester avant de renoncer à annoter. Pour PRÉTRAITER : la
résolution relative source/cible compte (§5.4) : le modèle non adapté s'effondre si l'échelle des
images cibles diffère de celle d'entraînement, donc garder la même résolution d'entrée
(letterbox, tiling) en entraînement et en déploiement, ou adapter. Pour AUGMENTER : les gains
viennent d'un entraînement adversarial et non d'une augmentation ; ce n'est pas un substitut au
Mosaic ou à la randomisation de domaine. Cas d'usage : nouvelle caméra, météo différente,
pré-entraînement sur synthétique, quand seules des images cibles non étiquetées existent. Laisse
ouvert : transfert à YOLO et aux petits objets, comparaison à quelques centaines de labels cibles,
combinaison avec des pseudo-labels.

## Gaps identifiés

- Aucune mesure de l'écart source → cible face à un entraînement supervisé sur la cible, donc du
  nombre d'images cibles annotées qui égalerait l'adaptation non supervisée.
- Pas de test sur détecteurs monoétage (YOLO) ni sur petits objets.
- Domaine météo simulé seulement (Foggy Cityscapes), pas de brouillard réel.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier ; backend grobid). Tables 1, 3, 4 reconstruites par
PyMuPDF, à vérifier ; Table 2 partiellement illisible (colonnes mélangées), seules les valeurs
de baseline (18,8) et du modèle complet (27,6) sont retenues, et 27,6 est recoupé indirectement
avec le texte (écart +8,6 annoncé contre 8,8 calculé) ; Fig. 3 et 4 non lisibles en chiffres.
Ce qui suit est déduit et non affirmé par les auteurs : les gains relatifs en pourcentage ; la
lecture de l'asymétrie K→C / C→K comme effet de direction ; l'absence de code publié (non
mentionné dans le texte lu) ; l'écart probable à l'oracle supervisé.
