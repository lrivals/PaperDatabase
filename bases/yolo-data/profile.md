# Profil — Datasets pour la détection YOLO : annotation, prétraitement, augmentation

Thème et périmètre de la base. La partie machine (axes, règles de classement, requêtes de
découverte) est dans `base.json` ; ce fichier en donne la justification. Le LLM propose des
changements (`/base-profile`, suggestions de `/paper-fiche`) ; rien n'est appliqué sans accord.

## Thème (utilisateur)

Préparation des données pour la détection d'objets de type YOLO : constitution et choix de datasets (COCO, VOC, VisDrone, domaines spécifiques), formats et conventions d'annotation (bbox normalisées YOLO, polygones, OBB), outils et consignes d'annotation, qualité et bruit des labels, annotation semi-automatique (pseudo-labels, SAM, modèles fondation), active learning, prétraitement (letterbox, redimensionnement, tiling/SAHI pour petits objets, normalisation), augmentation (Mosaic, MixUp, CutMix, Copy-Paste, photométrique), données synthétiques et domain adaptation, split, déséquilibre de classes, choix des ancres. Objectif : savoir quoi faire selon le besoin (petits objets, peu de données, nouvelle classe, embarqué).

## Précisions

- Finalité : un guide pratique « quel prétraitement, quel labelling selon le besoin » pour
  entraîner un détecteur de type YOLO (format Ultralytics, bbox normalisées).
- Questions de recherche :
  - combien d'images et d'instances par classe faut-il, selon la tâche ?
  - quel type d'annotation (bbox, OBB, polygone) et quelles consignes (objets occultés,
    tronqués, foules, classes ambiguës) ?
  - quand pré-annoter automatiquement (pseudo-labels, SAM, open-vocabulary), et comment
    contrôler la qualité des labels ?
  - quelle résolution d'entrée et quel découpage (tiling, SAHI) pour les petits objets ?
  - quelles augmentations selon la taille du dataset et la cible (Mosaic, Copy-Paste…) ?
  - quand recourir aux données synthétiques ou à l'adaptation de domaine ?
- Un papier « architecture YOLO » n'est retenu que pour sa recette de données : format des
  labels, ancres, augmentations, résolution, split.
- Toujours noter le dataset, la taille d'entrée et le gain mesuré (mAP, mAP_small) d'une
  technique de données, et si l'effet est mesuré par ablation.

## Inclus

- Jeux de données de détection et leur méthodologie de constitution (COCO, VOC, Objects365,
  LVIS, Open Images, VisDrone, UAVDT, CrowdHuman, DOTA, jeux de domaine).
- Annotation : formats, outils, consignes, coût, accord inter-annotateurs, supervision faible.
- Qualité et bruit des labels, erreurs dans les benchmarks, nettoyage.
- Annotation semi-automatique : pseudo-labels, semi-supervisé, modèles fondation (SAM,
  Grounding DINO).
- Active learning pour la détection.
- Prétraitement : résolution, letterbox, tiling / SAHI, découpage d'images haute résolution.
- Augmentation pour la détection, et augmentations de classification transférables (MixUp,
  CutMix, AutoAugment).
- Données synthétiques, sim-to-real, adaptation de domaine.
- Déséquilibre de classes, longue traîne, petits objets, ancres et assignation des labels.

## Exclus

- Architectures de détection sans contribution sur les données.
- Accélération matérielle et déploiement (bases `fpga` et `drone`).
- Classification d'images pure, sauf augmentation transférable à la détection.
- Segmentation sémantique, sauf comme outil d'annotation (SAM).

## Vocabulaire

bbox normalisée (cx, cy, w, h), OBB, polygone, letterbox, tiling / SAHI, Mosaic, MixUp, CutMix,
Copy-Paste, AutoAugment, pseudo-label, teacher-student, active learning, label noise,
mAP / mAP50 / mAP50-95, mAP_small, ancres (k-means), assignation des labels (ATSS, SimOTA,
TAL), longue traîne, sim-to-real, domain randomization.

## Suggestions en attente

<!-- Une ligne par suggestion : - AAAA-MM-JJ (source : paper_id ou /base-profile) — proposition — raison -->

## Historique

- 2026-10-05 — base créée (`pdb base new`).
- 2026-10-05 — 9 axes plus surveys, règles de classement, requêtes et 35 tag_rules (/base-profile) — découpage du pipeline de données : dataset → annotation → qualité → prétraitement → augmentation.
- 2026-10-05 — précisions, inclus, exclus et vocabulaire rédigés (/base-profile) — finalité : guide « quoi faire selon le besoin ».
