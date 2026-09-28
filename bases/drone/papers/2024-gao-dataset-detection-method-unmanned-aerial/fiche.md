---
id: 2024-gao-dataset-detection-method-unmanned-aerial
fiche: done
date: 2026-09-28
---

# A Novel Dataset and Detection Method for Unmanned Aerial Vehicles Using an Improved YOLOv9 Algorithm

Depeng Gao, Jianlin Tang, Hongqi Li, Bingshu Wang, Jianlin Qiu, Shuxi Chen, Xiangxiang Mei, 2024, Sensors 24(23), 7512. https://doi.org/10.3390/s24237512
Type : article de journal (MDPI Sensors)

## Problème

Détection de drones (anti-UAV) en lumière visible. Selon les auteurs, le radar est inefficace
contre les drones « low-slow-small » (§1). Ils posent deux verrous :
- **Les jeux anti-UAV ne contiennent que des drones**, ou des drones et des oiseaux
  (DVB-AVSS, DVB-ASSP). Un détecteur ainsi entraîné confond donc les drones avec d'autres
  objets volants : oiseaux, avions, hélicoptères (§1, §2.3, Tables 1-2).
- **Les métriques d'appariement de type IoU** (GIoU, DIoU, CIoU) sont trop sensibles à la
  position pour les très petites cibles. Elles pénalisent les petites boîtes lors de
  l'attribution des exemples positifs et négatifs (§4.2, §4.3).

## Méthode

- **Jeu Anti2** : 5062 images et 5828 boîtes réparties en 4 classes : 1688 UAV,
  1444 oiseaux, 1406 hélicoptères et 1320 avions (§3). Il agrège des jeux ouverts de détection
  (Real World, Det-Fly, SOD4SB, HelicoptersofDC, PD) et de suivi (Anti-UAV, BVD,
  DroneDetection), des vidéos Bilibili et YouTube, et des moteurs de recherche d'images.
  Annotation LabelImg au format YOLO. Fonds variés : ciel, nuages, mer, sol, herbe (§3,
  Fig. 1-3). Découpage aléatoire 6:2:2, soit 3038/1012/1012 images (§5.1).
- **DotD-YOLOv9-C** : YOLOv9-C (GELAN et branche auxiliaire PGI, retirée à l'inférence)
  inchangé, sauf dans l'assigner d'ancres. Celui-ci classe les prédictions avec la **Dot
  Distance** (DotD, Xu et al. [29]), soit exp(−D/S), où D est la distance euclidienne
  entre centres et S la taille moyenne des objets de la classe, au lieu de l'IoU (§4.2-4.3,
  Éq. 1-3). Aucune modification d'architecture : **le coût d'inférence est celui de
  YOLOv9-C** (déduit, les auteurs ne donnent pas de temps d'inférence).
- Entraînement : entrée 512×512, batch 2, 300 epochs, SGD, OneCycleLR, poids pré-entraînés
  officiels (§5.1).

## Plateforme et implémentation

- Entraînement et test sur un **GPU de portable NVIDIA GeForce RTX 4060 Laptop** avec un CPU
  AMD Ryzen 9 7945HX, sous PyTorch 2.3 et CUDA 12.3 (Table 3).
- **Aucun déploiement embarqué.** FPS, latence, puissance, paramètres et GFLOPs sont tous
  `n/r`.
- Code et jeu Anti2 : aucune mention de publication dans le texte extrait. La
  déclaration de disponibilité des données, habituelle chez MDPI, n'a pas été extraite.

## Résultats

Précision à IoU 0,5 sur le test d'Anti2 (§5.2) :

| Configuration | UAV | Oiseau | Hélico | Avion | mAP | FPR | FNR | Source |
|---|---|---|---|---|---|---|---|---|
| YOLOv9-C + GIoU | 96,3 | 80,6 | 93,5 | 86,0 | 90,3 | 2,5 | 5,4 | Table 4 |
| YOLOv9-C + DIoU | 96,8 | 85,0 | 92,5 | 84,2 | 90,7 | 2,2 | 4,6 | Table 4 |
| YOLOv9-C + CIoU | 97,6 | 84,0 | 95,0 | 86,1 | 91,4 | 0,9 | 4,2 | Table 4 |
| **DotD-YOLOv9-C** | 97,8 | 87,1 | 94,2 | 91,4 | **92,6** | 1,6 | 3,1 | Tables 4-5 |

Comparaison avec d'autres méthodes, réentraînées sur Anti2 (Table 5) : QueryDet 86,0 ;
DETR 90,3 ; YOLOv9-C 90,7 ; GFL 91,4 ; DotD-YOLOv9-C 92,6 % de mAP. Le plus grand gain
porte sur la classe oiseau, qui compte le plus de petites cibles (§5.3). Échecs
qualitatifs : drone confondu avec une maison lointaine, drone blanc sur un nuage, oiseaux
sombres au crépuscule (Fig. 8, §5.3).

→ reportés dans `benchmarks.csv` : 1 ligne, DotD-YOLOv9-C sur Anti2 avec 92,6 % de mAP@0.5
(Table 5, `high`). FPS et puissance sont `n/r`, et la plateforme est un GPU de portable,
utilisé pour l'entraînement et le test, pas une cible embarquée.

## Limites et critique

- **Incohérences internes dans la Table 4.** La ligne CIoU a exactement les AP par classe de
  YOLOv9-C dans la Table 5 (97,6/84,0/95,0/86,1), mais un mAP de 91,4 contre 90,7 dans la
  Table 5. La moyenne de ces quatre AP vaut 90,7. De même, la moyenne des AP des lignes
  GIoU (≈ 89,1) et DIoU (≈ 89,6) ne donne pas le mAP affiché (90,3 et 90,7). Seule la ligne
  DotD est cohérente (≈ 92,6). **Calcul fait par nous, pas par les auteurs.** Le gain de
  DotD sur CIoU (le défaut de YOLOv9) vaut donc +1,2 ou +1,9 point selon la ligne retenue.
- **Un seul découpage aléatoire, sans écart-type ni répétition.** Le gain est de l'ordre
  de 1 à 2 points de mAP sur 1012 images de test.
- **Risque de fuite entre train et test** (déduit) : les images viennent en partie de jeux
  de suivi vidéo (Anti-UAV, BVD, DroneDetection). Des images quasi identiques d'une même
  séquence peuvent tomber des deux côtés d'un découpage aléatoire par image.
- **Aucune métrique de coût.** FPS, latence, paramètres et puissance manquent alors que
  le modèle retenu est YOLOv9-C, pas une variante légère (T/S, §4.1). Un test sur un GPU de portable RTX 4060 ne dit rien du temps réel embarqué.
- **Mode de capteur non précisé.** Les images mêlent des vues sol → air (vidéos, moteurs de
  recherche) et air → air (Det-Fly). Aucune configuration de déploiement n'est décrite.
- DotD vient de Xu et al. [29] (petits objets en télédétection). L'apport méthodologique se
  limite à son application à l'assigner de YOLOv9-C.
- La résolution d'entrée de 512×512 est modeste pour des cibles lointaines. La taille des
  objets en pixels n'est donnée que par une figure (Fig. 2b), non lue.

## Pertinence pour la thèse

- **Contre-drone, sans dimension embarquée.** Le travail relève plutôt de la détection
  sol → air ou générique (voir la section Limites), donc de la partie exclue du profil.
  Il reste utile comme **source de jeu multi-classes** (drone, oiseau, avion, hélicoptère)
  pour évaluer les faux positifs d'un détecteur air → air.
- **DotD dans l'assigner** : une modification sans coût d'inférence qui améliore surtout les
  petites cibles. C'est un bon candidat pour un YOLO léger embarqué sur FPGA ou Jetson,
  puisque l'architecture ne change pas (à tester, non montré ici).
- Laisse ouvert : le coût d'inférence, la portabilité vers un modèle léger (YOLOv9-T/S) et
  la validation sur un jeu air → air.

## Gaps identifiés

- **Détecteurs anti-UAV évalués sans métrique de coût** : ni FPS ni puissance, sur un GPU de
  portable. Même constat que pour les YOLO drone SOTA non portés sur une cible embarquée.
- **Rejet des oiseaux, avions et hélicoptères en air → air** : Anti2 mélange les points de
  vue. Il manque un jeu air → air multi-classes pour mesurer les faux positifs d'un
  intercepteur.
- **Assigner adapté aux petits objets (DotD, NWD…) sur un modèle quantifié** : l'effet
  combiné sur le mAP_small n'est pas mesuré.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). Le résumé n'a pas été
extrait : il ne contient que la fin du titre. Plusieurs paragraphes sont dupliqués (§3, §4,
§5.3). `extraction.warnings` signale la Table 5 « sans corps extrait », mais une seconde
copie de la Table 5 a bien un corps dans `fulltext.md`, et elle a été lue. La Fig. 2
(taille des cibles) n'est pas exploitable.

Ce qui suit est déduit et non affirmé par les auteurs :
- le coût d'inférence identique à YOLOv9-C ;
- les incohérences de la Table 4 (moyennes recalculées par nous) ;
- le risque de fuite entre train et test dû aux sources vidéo ;
- le caractère mixte sol → air / air → air du jeu ;
- l'intérêt de DotD pour un modèle embarqué.
