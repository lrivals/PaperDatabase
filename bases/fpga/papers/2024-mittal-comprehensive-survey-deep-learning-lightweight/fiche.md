---
id: 2024-mittal-comprehensive-survey-deep-learning-lightweight
fiche: done
date: 2026-09-24
---

# A comprehensive survey of deep learning-based lightweight object detection models for edge devices

Payal Mittal, 2024, Artificial Intelligence Review 57(9), 242. https://doi.org/10.1007/s10462-024-10877-1
Type : article de journal (survey)

## Problème

Recenser les détecteurs d'objets « légers » destinés aux équipements edge, leurs backbones
et leurs applications. Selon l'autrice, aucun survey consolidé n'existait sur ce sujet précis
(§1.1, Table 1).

## Méthode

Survey, sans expérience propre. Il couvre :
- une taxonomie des détecteurs : deux étages, un étage, « advanced-stage », légers (§2) ;
- les blocs constitutifs (§3.1, Table 2) et un inventaire de 26 détecteurs légers
  (Tables 3-5) ;
- 9 variantes YOLO de 2023-2024 (Table 6) ;
- 10 backbones : MobileNet v1 à v3, ShuffleNet, PeleeNet, MnasNet, OFA, MobileViT,
  SqueezeNet (§3.3) ;
- les jeux de données VOC, COCO et KITTI (§4.1) ;
- les plateformes : téléphones, IoT, cartes embarquées (§4.3) ;
- des recommandations de conception (§4.6).

## Plateforme et implémentation

Pas d'implémentation propre.
- Le §4.3 traite les plateformes en quatre paragraphes : téléphones, IoT (Raspberry Pi,
  Coral), cartes embarquées.
- Le FPGA n'occupe **qu'un paragraphe** (§4.3.3) : fabricants cités, « la famille Xilinx
  est la plus utilisée », « un accélérateur additionnel est souvent nécessaire ». Arduino
  est rangé dans la même catégorie.
- Les URL des dépôts de code des détecteurs recensés sont listées (Table 3).

## Résultats

Chiffres repris des articles cités, sans vérification (Tables 5-6) :
- latence la plus basse : YOLOv3-Tiny, 4,5 ms ;
- FPS le plus élevé : YOLOv4-Tiny, 371 FPS ;
- parmi les YOLO récents : Light YOLO, 102,04 FPS (Table 6) ;
- sur VOC, L4Net atteint 71,68 % de mAP avec 149 FPS sur « NVIDIA TX » et 30,7 FPS sur une
  plateforme Qualcomm (§4.4) ;
- RefineDet-Lite : 26,8 de mAP à 130 ms par image sur un CPU monothread (§4.4).

→ reportés dans `benchmarks.csv` : aucune ligne. C'est un survey, et surtout ses FPS et
latences n'ont **pas de plateforme associée** (voir ci-dessous).

## Limites et critique

- **FPS sans matériel.** Les Tables 5 et 6 alignent latences (4,5 à 73 ms) et FPS (17 à
  371) sans dire sur quelle puce, à quel batch ni à quelle précision ils ont été mesurés.
  Ces chiffres sont inexploitables pour une comparaison matérielle. C'est une forme extrême
  du gap « protocole de mesure ».
- **Incohérences d'unités et de valeurs :**
  - FLOPs en « B » et en « G » mélangés ;
  - 1453B FLOPs pour YOLOv3-DarkNet53 ;
  - 0,47 FLOPs sans unité pour ThunderNet ;
  - 1,08 M paramètres pour PP-YOLOv2 avec un ResNet101 ;
  - 205 FPS et 1,21B FLOPs pour Pelee.
  Plusieurs valeurs sont vraisemblablement erronées (déduit).
- **Colonne « real-time applications » :** cochée ou non **sans critère énoncé**
  (Tables 5-6).
- **Pas d'analyse des conditions de mesure** (puissance, batch, précision numérique), et
  aucune mesure d'énergie.
- **Traitement du matériel superficiel :** FPGA, NPU et MCU sont à peine évoqués. La
  conclusion affirme que les détecteurs légers « restent à plus de 50 % en deçà » des
  modèles complets, sans source ni métrique.

## Pertinence pour la thèse

- **Utilité :** faible pour la partie matérielle. Il sert d'index de détecteurs légers
  (noms, backbones, dépôts de code, Table 3), à vérifier à la source.
- **Contre-exemple :** il montre qu'une partie de la littérature « edge » ne relie pas les
  performances à une plateforme.

## Gaps identifiés

- **FPGA absents des surveys « embarqué » :** confirmé par un troisième survey, où le FPGA
  n'a qu'un paragraphe (§4.3.3).
- **Protocole de mesure :** cas extrême, puisque les FPS n'ont même pas de plateforme
  associée (Tables 5-6).

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). Les Tables 1 à 4 et 7
à 8 sont partiellement ou totalement tronquées dans l'extraction. Les Tables 5 et 6 sont
lisibles.

Ce qui suit est déduit et non affirmé par l'autrice :
- le caractère erroné des valeurs signalées ;
- l'inexploitabilité matérielle des Tables 5-6.
