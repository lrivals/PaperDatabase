---
id: arxiv-2103.13933-unmanned-aerial-vehicle-visual-detection
fiche: done
date: 2026-09-28
---

# Unmanned Aerial Vehicle Visual Detection and Tracking using Deep Neural Networks: A Performance Benchmark

Brian K S Isaac-Medina, Matt Poyser, Daniel Organisciak, Chris G Willcocks, Toby P Breckon, Hubert P H Shum, 2021, arXiv preprint. https://arxiv.org/abs/2103.13933
Type : preprint non relu par les pairs (dans `metadata.json`). Le texte extrait ne donne pas
de venue ; une version workshop ICCV 2021 est possible (non vérifié, à confirmer).

## Problème

Aucun benchmark n'évaluait plusieurs détecteurs et trackers DNN, sur plusieurs jeux de
données, pour **détecter et suivre des drones** en imagerie visible (§1). L'Anti-UAV
benchmark concurrent [24] ne compare ni détecteurs ni jeux de données. Défis cités : drones
petits et lointains, fonds complexes, mouvement rapide, caméra parfois elle-même embarquée
sur un système mobile (§1, d'après Rozantsev et al.).

## Méthode

Benchmark, sans méthode nouvelle :
- **Jeux** (une classe « drone ») : MAV-VID (64 vidéos, 40 232 images ; caméras sur drone,
  au sol et mobiles ; objet moyen 136×77 px, 0,66 % de l'image), **Drone-vs-Bird** (77
  vidéos, 104 760 images ; 34×23 px, 0,10 %), **Anti-UAV** (100 vidéos RGB + IR, 186 494
  images) ; splits train/val définis par les auteurs (§3.1).
- **Détecteurs** (MMDetection, pré-entraînés COCO, 24 époques) : Faster R-CNN R-50 + FPN,
  SSD512, YOLOv3 DarkNet-53 (608×608), DETR R-50 (§3.2). Faster R-CNN et DETR ont une
  hauteur d'image minimale de 800 px (§4.1).
- **Trackers MOT** (MMTracking) : SORT, DeepSORT, Tracktor, avec chaque détecteur (§3.3).
- **Cross-modalité** : entraînement IR → test RGB et inversement sur Anti-UAV (§4.1,
  Table 3).
- Métriques : COCO (« mAP » = AP@0,5), MOTA, IDF1, ID switches.

## Plateforme et implémentation

Entraînement sur **une GPU Nvidia RTX 2080 Ti** (§3.2). La plateforme des FPS de la Table 2
n'est pas précisée (n/r ; vraisemblablement la même GPU, déduit). Aucune cible embarquée,
aucune mesure de puissance. Code : https://github.com/KostadinovShalon/UAVDetectionTrackingBenchmark (§1).

## Résultats

AP@0,5 (Table 1, disposition du tableau décalée à l'extraction, recoupée avec le texte) et
coût (Table 2) :

| Détecteur | MAV-VID | Drone-vs-Bird | Anti-UAV RGB | Anti-UAV IR | GFLOPs | FPS | Param. |
|---|---|---|---|---|---|---|---|
| Faster R-CNN | **0,978** | 0,632 | 0,982 | 0,977 | 207 | 18,0 | 41 M |
| SSD512 | 0,967 | 0,629 | 0,979 | 0,975 | 88 | 32,4 | 24 M |
| YOLOv3 | 0,963 | 0,546 | **0,986** | 0,976 | 70 | 36,0 | 61 M |
| DETR | 0,971 | **0,667** | 0,978 | **0,980** | 86 | 21,4 | 41 M |

- Petits objets : sur Drone-vs-Bird, APs max 0,218 (Faster R-CNN) ; en IR, APs max 0,533
  (YOLOv3) (Table 1, §4.1). AP COCO sur Drone-vs-Bird : 0,283 au mieux (Faster R-CNN).
- Cross-modalité : IR → RGB 0,828 AP50 (Faster R-CNN) ; RGB → IR 0,644 (Faster R-CNN) ;
  les détecteurs un étage chutent fortement (0,342 / 0,299 IR → RGB) (Table 3).
- Suivi : MOTA max **0,987** (Faster R-CNN + Tracktor, Anti-UAV IR) ; Drone-vs-Bird MOTA
  max 0,525 (SSD512 + Tracktor) ; DeepSORT fait souvent **moins bien** que SORT, la ré-id
  pré-entraînée sur piétons n'aidant pas pour les drones (Table 4, §4.2).

→ reportés dans `benchmarks.csv` : 20 lignes (4 détecteurs × 5 jeux : MAV-VID,
Drone-vs-Bird, Anti-UAV Full, RGB, IR), AP50 et FPS, `confidence: medium` (disposition de
la Table 1 décalée à l'extraction ; plateforme des FPS non précisée). Les résultats de
suivi (MOTA) ne sont pas mis dans le CSV.

## Limites et critique

- **Sol → air majoritaire** : Anti-UAV et Drone-vs-Bird sont surtout filmés depuis le sol ;
  MAV-VID mélange caméras sur drone, au sol et mobiles, sans résultat séparé par type de
  prise de vue. Les chiffres ne disent donc rien de spécifique à l'**air → air** embarqué.
- **Aucune évaluation embarquée** : FPS sur GPU de bureau (plateforme non dite), pas de
  latence, pas de puissance. Les 32-36 FPS de SSD/YOLOv3 sur GPU ne transposent pas à un
  drone intercepteur (déduit).
- **Métrique saturée** : AP50 ≈ 0,96-0,99 sur MAV-VID et Anti-UAV ; seul Drone-vs-Bird
  discrimine. Le « SOTA 0,986 vs 0,952 [18] » compare des jeux / protocoles différents.
- Résolutions d'entrée différentes entre détecteurs (≥ 800 px pour Faster R-CNN / DETR,
  608 pour YOLOv3) : la comparaison petits objets favorise les deux étages, ce que les
  auteurs reconnaissent (§4.1).
- Incohérences : la conclusion dit Faster R-CNN « up to 0.770 » pour les petits drones,
  valeur qui correspond à l'AP75 d'Anti-UAV RGB dans la Table 1, pas à un APs (déduit) ;
  le texte (§4.2) attribue le meilleur suivi petits objets à DETR alors que DETR a le pire
  MOTA sur Drone-vs-Bird (0,012-0,130, Table 4).
- Splits propres aux auteurs : non comparables aux challenges officiels.

## Pertinence pour la thèse

- Point d'entrée utile pour l'axe `counter-uav` : panorama des jeux (MAV-VID,
  Drone-vs-Bird, Anti-UAV) et ordre de grandeur de la difficulté (petits drones lointains :
  AP50 ~0,55-0,67).
- Montre que la difficulté réelle est dans les **très petits objets** (Drone-vs-Bird,
  0,10 % de l'image), c'est-à-dire exactement le cas d'un intercepteur qui doit détecter
  tôt ; mais n'étudie ni le coût embarqué ni la quantification.
- Résultat cross-modalité IR → RGB à garder en tête pour un capteur embarqué bi-spectral.

## Gaps identifiés

- Benchmark de détection de drones **air → air, sur plateforme embarquée** (Jetson, FPGA,
  MCU) avec latence et puissance : absent.
- Effet de la quantification sur l'APs de drones lointains (Drone-vs-Bird) : non mesuré.
- Ré-identification spécifique aux drones pour le suivi (les auteurs le citent en
  perspective, §4.2, §5).

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). La Table 2 est signalée
« sans corps extrait » dans `extraction.warnings`, mais son corps figure bien dans
`fulltext.md` (GFLOPs, FPS, paramètres). Les Tables 1, 3 et 4 ont des colonnes décalées ;
les valeurs reportées ont été réalignées et recoupées avec le texte quand il les redonne.
Note de bas de page (lien MMTracking) absente.

Ce qui suit est déduit et non affirmé par les auteurs :
- la GPU utilisée pour les FPS ;
- la venue workshop ICCV 2021 ;
- l'origine du « 0.770 » de la conclusion ;
- la non-transposabilité des FPS à l'embarqué.
