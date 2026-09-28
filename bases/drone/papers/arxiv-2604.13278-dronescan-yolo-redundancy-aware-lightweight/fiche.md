---
id: arxiv-2604.13278-dronescan-yolo-redundancy-aware-lightweight
fiche: done
date: 2026-09-28
---

# DroneScan-YOLO: Redundancy-Aware Lightweight Detection for Tiny Objects in UAV Imagery

Yann V Bellec, 2026, arXiv preprint. https://arxiv.org/abs/2604.13278
Type : preprint non relu par les pairs (auteur unique)

## Problème

Dans VisDrone2019-DET, 68 % des instances font moins de 32×32 pixels (§1, §4.1). Les
auteurs identifient trois limites de YOLOv8s : stride minimal de 8 (un objet de 8×8 px ne
donne qu'une activation 1×1 sur P3 à 640 px), gradient nul de la perte CIoU quand boîtes
prédite et cible ne se recouvrent pas, et redondance des filtres (§1). Selon eux, aucun
travail ne traite conjointement résolution, tête multi-échelle, pruning et perte (§2).

## Méthode

Sur YOLOv8s (9,84 M paramètres, 23,6 GFLOPs à 640 px) (§3.1) :
1. **Entrée 1280×1280** au lieu de 640 (§3.2).
2. **RPA-Block** : pruning dynamique de filtres par similarité cosinus (seuil θ = 0,85)
   sur les couches 2 et 4 du backbone, via des forward hooks, avec 10 époques de warm-up
   et mise à jour paresseuse du masque toutes les 5 époques (§3.3, Tables 2-3). **Masque
   multiplicatif non structuré : les paramètres ne sont pas physiquement retirés** (§5).
3. **MSFD** : branche **P2 (stride 4)** légère, convolutions séparables en profondeur +
   squeeze-and-excitation, fusion avec P3 suréchantillonné, +114 592 paramètres (+1,1 %)
   (§3.4). Implémentée par hooks, **pas comme vraie tête de détection** YOLOv8 (§5).
4. **SAL-NWD** : perte hybride 0,5 × NWD + 0,5 × CIoU pondérée par l'inverse de l'aire,
   dans le pipeline TaskAligned (§3.5, Table 1).

Total : +400 080 paramètres (+4,1 %) (§3.1). Post-traitement : NMS avec seuils choisis par
grid search sur la validation (conf = 0,010, IoU = 0,4) (§4.2).

## Plateforme et implémentation

- **NVIDIA RTX 4090 Laptop GPU** (16 GB), PyTorch 2.10, Ultralytics 8.3.0, CUDA 12.8
  (§4.2). Les FPS sont vraisemblablement mesurés sur ce GPU (non dit ; batch, précision
  FP32/FP16 et inclusion du NMS n/r).
- Entraînement : baseline YOLOv8s 50 époques à 640 px, batch 16 ; DroneScan 100 époques à
  1280 px, batch 4 (§4.2).
- Aucune cible embarquée. Puissance : n/r. Code : non publié (aucun lien dans le texte).

## Résultats

VisDrone2019-DET, **split de validation** (Table 4) :

| Modèle | Rés. | mAP@50 | mAP@50-95 | Rappel | Params | FPS |
|---|---|---|---|---|---|---|
| YOLOv5s | 640 | 0,231 | 0,125 | 0,363 | 7,2 M | 99,0 |
| YOLOv8s | 640 | 0,387 | 0,233 | 0,374 | 9,83 M | ~71 |
| YOLO-LE | 640 | 0,399 | 0,225 | 0,369 | 4,0 M | 93,0 |
| DAU-YOLO | 640 | 0,561 | 0,328 | 0,473 | 28,9 M | n/r |
| DroneScan-YOLO | 1280 | 0,553 | 0,356 | 0,518 | 10,23 M | 96,7 |

- AP@50 par classe (Table 5) : bicycle 0,114 → 0,328, awning-tricycle 0,156 → 0,237,
  pedestrian 0,412 → 0,644, car 0,786 → 0,890.
- RPA-Block seul : −0,013 mAP@50, +11,1 FPS (§4.5) ; sparsité finale 70-73 % (Table 3).
- Ablation incrémentale (Table 6, **corps non extrait**) : SAL-NWD seul +0,098 mAP@50-95,
  MSFD seul +0,132 de rappel (§4.6, texte).
- TTA : 0,551 → 0,541 mAP@50, non utilisée (§4.8).

→ reportés dans `benchmarks.csv` : 1 ligne — DroneScan-YOLO 1280 px sur VisDrone2019-DET
val, 55,3 % mAP@50, 96,7 FPS, RTX 4090 Laptop (Table 4, `confidence: high`).

## Limites et critique

- **Comparaison à résolution différente** : DroneScan à 1280 px contre toutes les
  baselines à 640 px. L'auteur reconnaît que la baseline YOLOv8s à 1280 px « could not be
  completed » et estime la contribution des modules hors résolution à +3-5 points
  seulement, « based on early convergence observation » (§5). Le gain annoncé de
  +16,6 points est donc surtout un effet de résolution (lu dans le papier).
- **Baseline sous-entraînée** : 50 époques contre 100 pour la méthode (§4.2).
- **FPS peu crédible en l'état** : 96,7 FPS à 1280 px contre ~71 FPS pour YOLOv8s à 640 px,
  avec 4× plus de pixels et un pruning **non structuré qui ne retire aucun paramètre** —
  l'auteur l'admet (« limiting real-world speed gains on embedded hardware », §5).
  Conditions de mesure absentes (déduit : très probablement non comparables).
- **Évaluation sur la validation, NMS réglé sur la validation** (§4.2, Table 4) : pas de
  test-dev ; fuite de sélection d'hyperparamètres.
- **Incohérences chiffrées** : 0,553 (Table 4) contre 0,563 après optimisation du NMS
  (§4.2-4.3) ; gains bicycle 0,321 (§4.4) contre 0,328 (Table 5) ; « MSFD » non intégré
  comme tête. Sections 4.6-4.7 partiellement absentes du texte.
- **« Lightweight » revendiqué sans embarqué** : aucune mesure sur Jetson, FPGA ou MCU ; les
  GFLOPs à 1280 px ne sont pas donnés (à 1280 px, ils sont ~4× ceux de 640 px, déduit).

## Pertinence pour la thèse

- Axe `drone-detection` : cas typique du **YOLO drone SOTA avec tête P2** évalué uniquement
  sur GPU — confirme l'hypothèse de base « tête P2 jamais portée sur FPGA ». Utile comme
  référence négative de méthodologie (résolution non appariée, FPS non documentés).
- Contient l'aveu explicite que **le pruning non structuré ne donne pas d'accélération
  matérielle** et que le pruning structuré est nécessaire (§5) : argument réutilisable pour
  motiver un pruning structuré compatible FPGA.
- Laisse ouvert : coût réel de la résolution 1280 et de la tête P2 sur accélérateur
  embarqué (mémoire des feature maps P2 à 320×320×64).

## Gaps identifiés

- **Tête P2 + 1280 px sur accélérateur embarqué** : empreinte mémoire des feature maps P2
  et débit non mesurés ; confirme le gap « tête P2 jamais portée sur FPGA ».
- **Séparer l'effet résolution de l'effet architecture** sur VisDrone : baseline appariée
  en résolution absente ici, souvent ailleurs aussi.
- **Pruning structuré orienté matériel** pour petits objets : annoncé en perspective (§5),
  non réalisé.
- mAP_small (COCO APs) non rapporté malgré l'objectif « tiny objects » : seules des AP par
  classe servent de proxy.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). La section 3 n'a pas
été détectée comme titre (sans perte apparente). **Table 6 (ablation) sans corps extrait** :
seuls les deux gains cités dans le texte sont connus ; les sections 4.6-4.7 sont absentes
ou réduites à des titres. Les Tables 2-3 sont mal découpées mais lisibles.

Ce qui suit est déduit et non affirmé par les auteurs :
- la mesure des FPS sur la RTX 4090 Laptop et leur non-comparabilité ;
- le facteur ~4 des GFLOPs à 1280 px ;
- la qualification des incohérences 0,553 / 0,563 et 0,321 / 0,328 (écarts constatés, cause
  inconnue).
