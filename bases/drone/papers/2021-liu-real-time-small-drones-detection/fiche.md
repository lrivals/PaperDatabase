---
id: 2021-liu-real-time-small-drones-detection
fiche: done
date: 2026-09-28
---

# Real-Time Small Drones Detection Based on Pruned YOLOv4

Hansen Liu, Kuangang Fan, Qinghua Ouyang, Na Li, 2021, Sensors 21(10), 3374. https://doi.org/10.3390/s21103374
Type : article de journal

## Problème

Détecter en temps réel des drones qui pénètrent une zone sensible (§1). Les auteurs posent
deux difficultés : les drones vont vite, ce qui demande un détecteur rapide, et ils sont
petits dans l'image. YOLOv4 est précis mais lourd : 245 Mo de poids, plus de 60 M de
paramètres à 416 × 416 (§1, §2). Le cadre est celui d'un système anti-drone de surveillance,
donc **sol → air** (déduit : images prises au téléphone depuis le sol, aucune plateforme
embarquée mentionnée).

## Méthode

- **Choix du détecteur** : comparaison de FCOS (ResNet-50 et ResNet-101), RetinaNet, YOLOv3
  et YOLOv4 sur le jeu propre, avec entrée 416 pour les YOLO. YOLOv4 l'emporte (§4.1,
  Table 2).
- **Élagage de canaux** façon SlimYOLOv3 : entraînement de parcimonie par L1 sur les γ des
  BN (α = 0,001 retenu ; 0,01 trop agressif), puis seuil global sur les γ (§3.2, Algorithme
  1). Pour les shortcuts, la couche « leader » impose ses canaux aux couches liées, au lieu
  du OU logique de SlimYOLOv3, pour élaguer davantage (§3.2).
- **Élagage de couches** : suppression de blocs shortcut du backbone (3 couches chacun),
  classés par γ moyen, après l'élagage de canaux (§3.2).
- **Augmentation petits objets** : copier-coller des petits drones, sans chevauchement,
  échelle ±0,2, dans les images d'entraînement (§3.3). Définition « petit » : COCO
  (< 32 × 32) (Table 1).
- **Jeu de données propre** : 10 000 images prises au téléphone (OnePlus) de deux drones,
  DJI Spark (petit) et DJI Phantom ; 8000 en entraînement et 2000 en test. 9388 petits
  objets dans 7928 images (§3.1, §3.3). Détection à une classe (drone).

## Plateforme et implémentation

- Inférence sur **NVIDIA Tesla P100** (GPU de serveur) (§4.2). Aucune plateforme embarquée,
  aucune mesure de puissance : n/r. Précision numérique : n/r (vraisemblablement FP32, déduit).
- Gamme de puissance : GPU de centre de données (déduit), hors des gammes nano, FPGA ou
  Jetson.
- Code : non publié selon le texte extrait. Jeu de données : non publié.

## Résultats

- **Comparaison des détecteurs (Table 2, mAP@0.5)** : FCOS-R50 85,5 ; FCOS-R101 90,3 ;
  RetinaNet 90,5 ; YOLOv3 89,1 ; **YOLOv4 93,6** (précision 74,2, rappel 93,1).
- **Élagage sans entraînement de parcimonie (Table 3)** : le mAP s'effondre dès un taux de
  0,15 (69,3) et 0,20 (12,9).
- **Modèles élagués (Table 4, Tesla P100)** :

| Canaux | Couches | Keep | mAP | Volume (Mo) | FPS |
|---|---|---|---|---|---|
| 0 | 0 | 1 | 93,6 | 245,8 | 43 |
| 0,8 | 0 | 0,01 | 86,3 | 13,9 | 65 |
| 0,5 | 12 | 0,1 | 90,8 | 52,9 | 64 |
| **0,8** | **8** | **0,1** | **90,5** | **15,1** | **69** |
| 0,8 | 12 | 0,1 | 78,4 | 9,9 | 75 |

  Le modèle retenu gagne +60 % de FPS (43 → 69) pour −3,1 points de mAP (§4.2, Table 4).
- **tiny-YOLOv4** : 23,1 Mo, plus rapide (FPS n/r) et légèrement meilleur en précision et
  F1, mais nettement moins bon en mAP (§4.2, Fig. 9, valeurs n/r).
- **Augmentation petits objets (Fig. 10)** : le rappel du modèle élagué passe de 30,7 % à
  72,6 % et sa précision est multipliée par 3 environ. Après augmentation, son mAP dépasse
  celui de tiny-YOLOv4 de 24,2 points (§4.3). Aucun effet notable sur YOLOv4 complet.

→ reportés dans `benchmarks.csv` : 10 lignes, les 10 configurations de la Table 4 (YOLOv4
de base et 9 variantes élaguées ; mAP@0.5 avant augmentation et FPS sur Tesla P100 ;
confidence high).

## Limites et critique

- **« Temps réel » mesuré sur Tesla P100** : aucun résultat sur plateforme embarquée. C'est
  typiquement un « résultat sur GPU de serveur présenté comme léger ». Le volume du modèle et
  les FPS P100 ne disent rien de la latence sur Jetson, FPGA ou MCU.
- **Incohérences internes** : l'Abstract annonce « 24 layers prune » alors que la Table 4 et
  le §4.2 donnent 8 couches pour le modèle retenu. L'Abstract donne +22,8 % en précision et
  +12,7 % en rappel après augmentation, alors que le §4.3 parle d'une précision ×3 et d'un
  rappel de 30,7 à 72,6 %. De plus, le §4.3 dit que la précision « drops from 74.2% to
  7.9% », chiffre qui ne se retrouve dans aucune table extraite.
- **Précisions très basses et mAP élevé** : FCOS-R50 a 12,9 % de précision pour 85,5 % de
  mAP (Table 2) ; précision et rappel sont calculés à un seuil de 0,3 non justifié, ce qui
  rend ces colonnes peu interprétables.
- **Jeu de données facile et fermé** : deux modèles DJI, découpe aléatoire en
  entraînement/test sur des images vraisemblablement très corrélées (mêmes séances, déduit).
  Aucun test sur un jeu public (Det-Fly, Anti-UAV, Drone-vs-Bird).
- **Ordre des étapes discutable** : le mAP de la Table 4 est mesuré avant l'augmentation,
  puis celle-ci est ajoutée pour « réparer » le modèle élagué. Le mAP final du modèle retenu
  après augmentation n'apparaît pas dans le texte extrait.
- Pas de quantification, pas de mesure de puissance.

## Pertinence pour la thèse

- **Axe `counter-uav` (sol → air)** : hors du cœur embarqué selon `profile.md`. Utile comme
  exemple de compression de YOLOv4 pour la détection de drones.
- **Idée utile** : l'élagage casse la détection des petits objets (rappel 30,7 % avant
  augmentation, §4.3), et une augmentation ciblée petits objets la répare en partie. Cela
  rejoint l'hypothèse de `gaps.md` sur l'effet de la compression sur le mAP_small, mais le
  papier ne mesure ni le mAP_small ni la quantification.
- **Laisse ouvert** : le portage sur cible embarquée (Jetson, FPGA) et la mesure sur un
  scénario air → air.

## Gaps identifiés

- **Compression vs petits objets** : l'élagage dégrade d'abord les petits objets
  (déduit de §4.3 : YOLOv4 complet ne bénéficie pas de l'augmentation, le modèle élagué si).
  C'est un argument pour mesurer le mAP_small après élagage **et** quantification, sur une
  cible embarquée.
- **Détecteurs anti-drone évalués seulement sur GPU de serveur** : pas de latence ni de
  puissance sur plateforme embarquée.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`, mais texte très
dupliqué : §3.2, §4, §4.2 et §4.3 répétés, restes de mise en page « FOR PEER REVIEW »). La
**conclusion est tronquée** après la première phrase. Les Figures 7 à 10 ne sont extraites
que sous forme de fragments de valeurs, et les valeurs de la Figure 10 (après augmentation)
ne sont pas lisibles, hormis celles citées au §4.3. `extraction.warnings` signale la Table 1
« sans corps », mais elle est bien présente plus bas (définitions COCO) ; les Tables 2 à 4
sont complètes.

Ce qui suit est déduit et non affirmé par les auteurs :
- le caractère sol → air du scénario ;
- la précision FP32 et la gamme de puissance ;
- la corrélation entre images d'entraînement et de test ;
- le rôle de l'élagage dans la perte sur petits objets, par comparaison avec YOLOv4.
