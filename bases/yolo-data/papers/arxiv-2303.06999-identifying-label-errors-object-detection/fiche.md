---
id: arxiv-2303.06999-identifying-label-errors-object-detection
fiche: done
date: 2026-10-18
---

# Identifying Label Errors in Object Detection Datasets by Loss Inspection

Marius Schubert, Tobias Riedlinger, Karsten Kahl, Daniel Kröll, Sebastian Schoenen, Siniša Šegvić, Matthias Rottmann, 2023, arXiv preprint. https://arxiv.org/abs/2303.06999
Type : preprint non relu par les pairs

## Problème

L'annotation de boîtes est longue et sujette aux erreurs, que la relecture laisse passer (§1) : benchmarks inexacts et détecteurs entraînés sur des labels bruités. Peu de travaux détectent automatiquement les erreurs de labels en détection (§1, §2). Les auteurs veulent un benchmark et une méthode qui retrouvent tous les types d'erreurs, y compris sur des datasets réels.

## Méthode

**Typologie (quatre erreurs simulées, §3.1.2)** : *drops* (boîte manquante), *flips* (bonne boîte, mauvaise classe), *shifts* (bonne classe, localisation inexacte), *spawns* (boîte posée sur du fond : label copié vers une autre image). Chaque label subit au plus un type ; fréquence totale γ, γ/4 par type ; γ = 0.2 par défaut (§4.1). Le papier ne simule ni boîtes en trop dupliquées ni erreurs de taille systématiques au-delà des shifts.

**Détection par inspection de la perte (§3.3)** : détecteur à deux étages (Cascade RoIHead, MMDetection). Les labels sont ajoutés aux propositions du 1er étage, puis la NMS se fait sur la perte par boîte (non sur le score). Score d'erreur = L_RPN (BCE + smooth-L1) + L_ROI (CE + smooth-L1), calculées par rapport au label bruité. Un drop donne une forte perte de classification au 1er étage, un spawn aux deux étages, un flip au 2e, un shift à la régression. Justification théorique : séparation stricte des pertes pour labels corrects et faux sous hypothèse PAC et flips uniformes de taux p_F < (C-1)/C·(1-2κ) (Prop. 1, suppl.) ; la preuve ne couvre que la classification, non la régression.

**Baselines (§3.2)** : naïve (relecture de tous les labels, AUROC 0.5 par construction), score de détection, entropie, probability differential (PD, Hu et al.) ; PD ne peut pas détecter les drops.

**Backbones/réglages** : Swin-T (~72M paramètres) et ResNeSt101 (~95M) ; IoU α = 0.3 ; s_ε = 0.25 ; τ = 0 (§4.1) ; BDD redimensionné à 1333×800, autres jeux à 1000×600, EMNIST-Det 300×300 (Table 4).

## Plateforme et implémentation

Logiciel (pas de FPGA) : MMDetection, GPU et durées n/r. Code annoncé publié « sur GitHub » (§5), lien n/r dans le texte extrait.

## Résultats

- **Datasets du benchmark (§3.1.1)** : EMNIST-Det (20 000 train / 2 000 test, semi-synthétique : lettres EMNIST collées sur images COCO) et BDD100k filtré jour/météo claire (12 454 train, test et val de 882 images chacun).
- **Robustesse de l'entraînement (Table 1, §4.2)** : avec 20 % de labels corrompus, mAP50 BDD Swin-T 52.1 -> 50.3 ; ResNeSt101 56.8 -> 52.9 ; EMNIST-Det Swin-T 98.2 -> 98.0, ResNeSt101 96.4 -> 95.2. Chute max 1.2 pt (EMNIST-Det) et 3.9 pt (BDD) ; le plus gros backbone perd plus (hypothèse des auteurs : surapprentissage des erreurs). Annexe : avec 5 % à 20 % de bruit, mAP BDD Swin-T entre 50.2 et 50.4 contre 52.1 sans bruit (Table 6, texte). 6 227 images propres (γ=0) donnent un mAP supérieur de 0.8 pt à 12 454 images avec γ=0.2 (Table 7, texte) : relire les labels peut valoir mieux qu'annoter plus.
- **Détection d'erreurs simulées, BDD Swin-T (Fig. 4, valeurs lues dans le texte de la figure)** : labels d'entraînement originaux, loss AUROC 0.963 / max F1 0.566 ; score 0.768 / 0.311 ; entropie 0.717 / 0.222 ; PD max F1 0.527 (AUROC tronqué, n/r). Labels bruités γ=0.2 : loss 0.922 / 0.360 ; score 0.892 / 0.317 ; entropie 0.694 / 0.183 ; PD max F1 0.347. La perte est meilleure sur les deux métriques (§4.2). Le classement dépend de la métrique (PD devant score et entropie en max F1). Les corps des Tables 2 et 5 (par type, par backbone) sont absents de `fulltext.md` : valeurs `n/r`, seul le texte de l'annexe est repris. D'après l'annexe : drops, score et perte proches (AUROC écart <= 1.92 pt, AUROC min 91.72 %) ; shifts, tous les max F1 de score/PD < 14 % ; la perte est la seule méthode efficace sur les quatre types, mais PD la dépasse en max F1 sur flips (BDD bruité) et spawns (ResNeSt101 BDD bruité, +20.16 pt).
- **Erreurs réelles, revue manuelle des 200 meilleures propositions par dataset (§3.5, §4.3, Table 3)** : un doute compte comme faux positif. Précision = part de propositions contenant au moins une erreur. Sans filtre : BDD au moins 34 erreurs (surtout des flips), Kitti 96 erreurs, précision 47.5 %, COCO 50 erreurs, VOC 23 erreurs (zéro drop dans le top-200). Les drops dominent pourtant COCO et VOC : en ne gardant que les propositions d'IoU < α avec tout label (classe ignorée), COCO 125 drops, précision 61.0 % ; VOC 175 drops, 71.5 % ; dataset propriétaire CE (pièces de voiture) 194 drops, 97 %.
- Lignes ajoutées à `benchmarks.csv` (proposées à l'agent principal) : 9 (`.cache/bench/…csv`) : BDD loss AUROC/max F1 (labels originaux et bruités), mAP50 BDD bruité, précisions Kitti, COCO, VOC, CE.

## Limites et critique

- Le « bon » dataset du benchmark suppose BDD filtré et EMNIST-Det presque sans erreur (§3.1) : leurs erreurs naturelles sont ignorées (§3.4) ; cela peut gonfler les faux positifs.
- Erreurs simulées uniformes et indépendantes de l'image : plus faciles que des erreurs humaines systématiques ; un spawn copié d'une autre image est peu réaliste. Taux de rappel réel inconnu (le nombre total d'erreurs réelles est inconnu, §3.5), seule la précision sur 200 propositions est donnée.
- Revue manuelle par les auteurs eux-mêmes, selon la politique de chaque dataset, sans accord inter-relecteurs (n/r). Échantillon de 200 par dataset, un seul modèle (Swin-T). Le choix du filtre « drops » vient d'une connaissance a priori du dataset : la précision de 71.5 % n'est pas celle d'un usage à l'aveugle (sans filtre VOC tombe à 23 erreurs).
- Précision de CE (97 %) non vérifiable : dataset propriétaire.
- Méthode limitée aux détecteurs à deux étages ; pas d'évaluation sur détecteur one-stage de type YOLO (déduit). Pas de réentraînement sur labels corrigés pour montrer un gain en mAP (non mesuré).
- Les valeurs de Fig. 4 viennent du texte extrait du graphique (confiance medium).

## Pertinence pour le thème

- **CONSTRUIRE** : les benchmarks standards (VOC, COCO, Kitti, BDD) ont des labels manquants : ne pas supposer un test set parfait. Les drops sont l'erreur dominante des datasets réels (Table 3, §4.3).
- **ANNOTER** : la typologie drop/flip/shift/spawn donne une grille de contrôle qualité et un jeu d'erreurs injectables pour tester son pipeline de relecture. Le papier suggère de relire avant d'annoter plus (Table 7).
- **PRÉTRAITER / nettoyer** : à appliquer après un premier entraînement, en relisant seulement les propositions à plus forte perte, filtrées sur les boîtes sans label recouvrant (IoU < 0.3) pour les drops. Un budget de ~200 images par dataset suffit à trouver des dizaines d'erreurs.
- **AUGMENTER** : sans lien direct. Seule indication : le bruit modéré (<= 20 %) coûte peu de mAP (1.2 à 3.9 pt), plus sur gros backbone.
- Reste ouvert : adaptation à un détecteur YOLO (perte par boîte à une étape), gain mesuré après nettoyage, rappel.

## Gaps identifiés

- Détecteur one-stage (YOLO) pour la détection d'erreurs de labels : non traité.
- Gain en mAP après correction des labels détectés : non mesuré.
- Détection d'erreurs de taille/IoU fines et de boîtes dupliquées : non couverte.
- Rappel sur erreurs réelles : inconnu.

## Statut de lecture

Papier complet (`fulltext.md` entier, extraction grobid ok). Corps des Tables 2, 3 et 5 absents : chiffres de Table 3 repris du texte §4.3, détails par type du texte de l'annexe ; AUROC de PD tronqué. Déduit et non affirmé par les auteurs : absence d'évaluation sur détecteur one-stage ; usage pour YOLO ; possible gonflement des faux positifs par les erreurs naturelles de BDD/EMNIST-Det.
