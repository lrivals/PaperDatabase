---
id: arxiv-1805.00123-crowdhuman-benchmark-detecting-human-crowd
fiche: done
date: 2026-10-18
---

# CrowdHuman: A Benchmark for Detecting Human in a Crowd

Shuai Shao, Zijian Zhao, Boxun Li, Tete Xiao, Gang Yu, Xiangyu Zhang, Jian Sun, 2018, arXiv preprint. https://arxiv.org/abs/1805.00123
Type : preprint non relu par les pairs (DOI : n/r)

## Problème

Les benchmarks de détection de personnes (Caltech, KITTI, CityPersons, COCOPersons) sous-représentent les foules : 0,32 à 6,47 personnes par image (§1, Table 2) et très peu de paires fortement recouvertes (0,02 / 0,02 / 0,32 paires par image à IoU > 0,5 pour Caltech / COCOPersons / CityPersons, §1). Leurs protocoles autorisent en outre à annoter une foule comme une seule région ignorée, donc exclue de l'entraînement et de l'évaluation (§1, §2.1). Les auteurs avancent aussi que les boîtes très recouvertes sont supprimées par la NMS, qui devient sensible à son seuil : un seuil bas fait chuter le rappel, un seuil haut ajoute des faux positifs (§1).

## Méthode

Construction d'un jeu de données (axe datasets, annotation).

- **Collecte** : ~60 000 images candidates récupérées sur Google Images avec ~150 requêtes (plus de 40 villes, activités, points de vue dont « surveillance »), au plus 500 images par requête pour équilibrer ; filtrage des images à peu de personnes ou peu de recouvrement ; ~25 000 images retenues, tirées au hasard en 15 000 / 4 370 / 5 000 (train / val / test) (§3.1). Annotations de test non publiques, serveur d'évaluation (§4.2).
- **Annotation, trois boîtes par personne liées entre elles** (§3.2) : (1) boîte du corps entier, exhaustive ; si la personne est partiellement occultée, l'annotateur doit compléter la partie invisible. Pas de rapport d'aspect fixe, contrairement à CityPersons (ligne tête-pieds, ratio 0,41) ; (2) les instances sont découpées, puis envoyées à d'autres annotateurs pour la boîte visible ; (3) même découpe pour la boîte de la tête. Toutes les annotations sont revérifiées par au moins un autre annotateur.
- **Régions ignorées** : les objets ressemblant à des humains (statues) reçoivent une étiquette spécifique et sont ignorés à l'évaluation, selon le protocole Caltech (§3.2). Table 2 : 99 227 régions ignorées pour 339 565 personnes en train. Les auteurs ne décrivent pas de consigne chiffrée sur quand ignorer une foule ; leur but déclaré est d'annoter toutes les personnes (« exhaustively », §1).
- **Niveaux d'occlusion** : bare (occlusion <= 30 %), partial (30 % à 70 %), heavy (> 70 %) (§3.3). Ratio visible = boîte visible / boîte complète (Fig. 3).
- **Baselines** : Faster R-CNN + FPN et RetinaNet + FPN, ResNet-50 (§4.1). Ancres du corps entier : ratios h/w {1, 1.5, 2, 2.5, 3}, RoI non rognées à l'image car des boîtes complètes sortent de l'image ; visible et tête : {1:2, 1:1, 2:1} (§4.3, §4.4). Entrée : petit côté 800 px, grand côté <= 1400 px (CrowdHuman, COCO) ; Caltech 2x, CityPersons 1x, Brainwash 640x480 (§4.3). 600 k itérations (FPN) / 750 k (RetinaNet), lr 0,02, SGD, 8 GPU, 2 images par GPU (1 pour CityPersons), pas de multi-échelle (§4.3). Métriques : mMR (log-average miss rate sur FPPI de 1e-2 à 1e0, plus bas = mieux), AP, rappel (§4.2).
- **Généralisation** : préentraînement CrowdHuman puis fine-tuning sur COCOPersons, Caltech, CityPersons, Brainwash (§4.5).

## Plateforme et implémentation

Sans objet pour l'embarqué : 8 GPU, modèle exact n/r (§4.3). Pas de puissance, de latence ni de FPS. Données : https://sshao0516.github.io/CrowdHuman/ (Abstract) ; code et modèles annoncés « will be released » (§5), non vérifié ici. Licence du jeu de données : non discutée.

## Résultats

Statistiques du jeu (train sauf mention, Table 2) :

| | Caltech | KITTI | CityPersons | COCOPersons | CrowdHuman |
|---|---|---|---|---|---|
| images | 42 782 | 3 712 | 2 975 | 64 115 | 15 000 |
| personnes | 13 674 | 2 322 | 19 238 | 257 252 | 339 565 |
| régions ignorées | 50 363 | 45 | 6 768 | 5 206 | 99 227 |
| personnes / image | 0,32 | 0,63 | 6,47 | 4,01 | 22,64 |

- 470 k personnes en train + val (Abstract). Texte : « ~7 » personnes/image pour CityPersons (§3.3), 6,47 en Table 2.
- **Occlusion** : bare 29,89 % et partial 32,13 % pour CrowdHuman contre 46,79 % et 24,19 % pour CityPersons (§3.3) : niveaux plus équilibrés, CityPersons concentré sur la faible occlusion. Le pourcentage heavy n'est pas donné dans le texte (Fig. 3, n/r).
- **Recouvrement par paire** (paires par image, Table 4, Cal / City / COCO / CrowdHuman) : IoU > 0,3 : 0,06 / 0,96 / 0,13 / 9,02 ; > 0,5 : 0,02 / 0,32 / 0,02 / 2,40 ; > 0,7 : 0,00 / 0,08 / 0,00 / 0,33 ; > 0,9 : 0,00 / 0,00 / 0,00 / 0,01. Triplets (Table 5, corps de tableau ambigu dans l'extraction) : IoU > 0,1 : 0,02 / 0,30 / 0,02 / 8,70 ; > 0,3 : 0,00 / 0,04 / 0,00 / 0,51 ; > 0,5 : 0,00 / 0,00 / 0,00 / 0,03. Les auteurs concluent que les triplets sont quasi absents des jeux antérieurs (§3.3).
- **Baselines sur CrowdHuman val** (rappel / AP / mMR) : corps visible, FPN 91,51 / 85,60 / 55,94, RetinaNet 90,96 / 77,19 / 65,47 (Table 6) ; corps entier, FPN 90,24 / 84,95 / 50,42, RetinaNet 93,80 / 80,83 / 63,33 (Table 7) ; tête, FPN 81,10 / 77,95 / 52,06, RetinaNet 78,43 / 71,36 / 60,64 (Table 8, valeurs lues dans le texte du §4.5 à cause de l'extraction). FPN bat RetinaNet dans les trois cas. Le corps entier est jugé plus difficile que le visible (§4.4) ; le mMR le plus bas est pourtant celui du corps entier, ce que le papier ne commente pas.
- **Difficulté relative** : le même FPN obtient mMR 10,08 sur Caltech et 14,81 sur CityPersons (Table 7), contre 50,42 sur CrowdHuman.
- **Effet du préentraînement CrowdHuman** (mMR, fine-tuning sur le jeu cible ; FPN) :

| Cible | Entraîné sur la cible seule | Crowd => cible | CrowdHuman seul, sans fine-tuning | Source |
|---|---|---|---|---|
| Caltech (reasonable) | 10,08 | 3,46 | 8,81 | Table 10 |
| CityPersons | 14,81 | 10,67 | 21,18 | Table 11 |
| COCOPersons | 41,89 | 39,79 | n/r | Table 9 |
| Brainwash (têtes) | 19,77 | 17,24 | n/r | Table 12 |

  Le gain est massif sur Caltech (-6,6 points), net sur CityPersons (-4,1), faible sur COCOPersons (-2,1, AP 83,83 -> 85,02) et Brainwash (-2,5). Autres références du papier : CityPersons=>Caltech 5,1, Repulsion 4,0 (Caltech) et 13,2 (CityPersons) (Tables 10, 11). Sur Caltech, CrowdHuman seul fait déjà mieux (8,81) que Caltech seul (10,08), mais pas sur CityPersons (21,18 contre 14,81) : le transfert direct dépend du jeu cible.
- **NMS en scène dense** : le papier n'en fait aucune mesure. L'effet du seuil de NMS est affirmé dans l'introduction (§1) comme motivation, sans expérience ni chiffre ; ne pas le citer comme résultat.
- Lignes proposées pour `benchmarks.csv` (12, mMR, plus bas = mieux) : Tables 6, 7, 8 (2 modèles chacune), Tables 9 à 12 (transfert).

## Limites et critique

- Baselines lourdes (ResNet-50 FPN / RetinaNet, 800x1400 px, GPU) : aucune donnée pour un YOLO ; le transfert n'est mesuré qu'avec FPN (§4.5). Déduit : l'amplitude du gain pour un détecteur de type YOLO n'est pas établie.
- Le gain de préentraînement est comparé à un baseline entraîné sur la cible seule avec le même schéma d'itérations ; le papier ne sépare pas l'effet de la quantité de données de celui de la densité ou des trois boîtes (déduit). Les jeux cibles utilisent des protocoles d'ancres et de résolution propres (§4.3).
- Annotation du corps entier occulté : variance entre annotateurs reconnue (§4.4) ; aucun accord inter-annotateurs chiffré, aucun coût ni temps d'annotation rapporté.
- Images web (Google Images), non vidéo ; biais de requêtes (150 mots-clés) et possibles doublons entre jeux non discutés. Licence non discutée. Seule la classe « personne » ; pas de format YOLO fourni (conversion à faire, déduit).
- Le texte extrait est tronqué (§4.4 Head Detection, §4.5) et les Tables 5, 8 mélangent leurs légendes avec d'autres blocs ; mMR de la boîte tête lu dans le texte du §4.5.
- Métrique mMR (Caltech) non comparable à l'AP COCO ni à mAP@0.5 d'autres bases ; ne pas la comparer entre papiers sans protocole commun.

## Pertinence pour cette base

Ce que le papier apprend, par étape :

- **CONSTRUIRE** : pour un détecteur de personnes ou d'objets en scène dense, le filtrage par densité et recouvrement (garder les images à beaucoup de personnes ou de recouvrement, §3.1) donne un jeu avec 22,64 personnes/image et 2,40 paires à IoU > 0,5 par image, contre 0,32 pour CityPersons (Tables 2, 4). Mesurer ces deux statistiques (personnes/image, paires par IoU, répartition bare/partial/heavy) sur son propre jeu permet de savoir s'il représente des foules. Plafonner le nombre d'images par requête (500) équilibre la diversité (§3.1).
- **ANNOTER** : trois boîtes liées par instance (complète avec complétion de la partie occultée, visible, tête), obtenues en rognant chaque instance pour les deux dernières, double vérification par un second annotateur (§3.2). Éviter de marquer une foule comme région ignorée : le papier montre que les jeux antérieurs perdent ainsi l'essentiel des cas difficiles ; réserver « ignore » aux objets ressemblant à des humains (statues). Pas de ratio fixe pour la boîte complète. Pour YOLO (bbox normalisées, une classe), choisir explicitement la boîte entraînée (visible ou complète) car elles ont des statistiques différentes ; la boîte complète sort de l'image, ce qui exige de la tolérer à la conversion (§4.4, déduit pour le format YOLO).
- **PRÉTRAITER** : le papier fixe le grand côté à 1400 px et les ratios d'ancres au corps humain ({1, 1.5, 2, 2.5, 3}) pour les boîtes complètes, {1:2, 1:1, 2:1} pour visible et tête (§4.3) : à reprendre comme point de départ pour des ancres ou un clustering, sans valider le choix pour YOLO (déduit).
- **AUGMENTER** : rien (pas d'augmentation étudiée ; multi-échelle volontairement désactivé, §4.3).
- **Quand l'appliquer** : détection de personnes ou de têtes en foule ou occultée (surveillance, comptage, piétons) ; peu de données cibles : préentraîner sur CrowdHuman avant le fine-tuning, gain mMR de 6,6 points sur Caltech et 4,1 sur CityPersons, plus faible (2 à 2,5 points) sur COCOPersons et Brainwash (Tables 9 à 12) ; évaluer la robustesse à l'occultation avec des sous-ensembles par taux de visibilité. Moins utile pour des objets isolés ou éparses. Pour les têtes, la boîte tête et la boîte visible fournissent un signal redondant (déduit).

## Gaps identifiés

- Pas de mesure de l'effet de la NMS (seuil, variantes) en scène dense, pourtant donnée comme motivation (§1) : à mesurer sur un YOLO.
- Pas d'évaluation du préentraînement CrowdHuman avec un détecteur de type YOLO, ni en régime de peu de données cibles (taille du fine-tuning non variée).
- Pas de coût ni de temps d'annotation des trois boîtes, ni d'accord inter-annotateurs, alors que la boîte complète occultée est jugée bruitée (§4.4).
- Secteur industriel dangereux, EPI, machines occultantes : non couverts (déduit).

## Statut de lecture

papier complet (fulltext.md lu en entier, extraction grobid, `extraction.ok` vrai). Le texte est tronqué en plusieurs endroits (§4.4 Head Detection, §4.5) ; les légendes des Tables 5 et 8 sont mélangées à d'autres blocs et plusieurs corps de tableaux sont signalés « sans corps extrait » dans `extraction.warnings` alors qu'ils sont présents : association tableau-légende déduite de l'ordre (Table 5 par ses valeurs d'IoU, Table 8 par le texte du §4.5). La part heavy de la Fig. 3 est n/r. Déduit et non affirmé par les auteurs : transfert vers YOLO, usage tête+visible comme signal redondant, conversion au format YOLO, secteur industriel non couvert.
