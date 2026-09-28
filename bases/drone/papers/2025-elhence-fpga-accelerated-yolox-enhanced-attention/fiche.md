---
id: 2025-elhence-fpga-accelerated-yolox-enhanced-attention
fiche: done
date: 2026-09-28
---

# FPGA-Accelerated YOLOX With Enhanced Attention Mechanisms for Real-Time Wildfire Detection on AAVs

Anubhav Elhence, Anubhav Panda, Vinay Chamola, Biplab Sikdar, 2025, IEEE Transactions on Instrumentation and Measurement 74, 1-14. https://doi.org/10.1109/TIM.2025.3556164
Type : article de journal

## Problème

Détecter des feux de forêt en temps réel à bord d'un drone (« AAV », nouvelle terminologie
IEEE pour UAV) malgré la puissance de calcul et l'énergie limitées ; les YOLO de la
littérature feu (YOLOv5 et variantes) sont jugés trop lourds pour l'embarqué (§I). Les
auteurs veulent un détecteur plus précis que YOLOX-m et exécutable sur FPGA embarqué.

## Méthode

- **LCAM-YOLOX** : YOLOX avec un module d'attention « layerwise » (LCAM) dans le backbone,
  combinant attention de canal (type CBAM : AvgPool + MaxPool → MLP → sigmoïde, Éq. 1-2) et
  attention spatiale (convolution 7×7, Éq. 3-4) (§III-A). Neck FPN + PAN, trois têtes
  80×80 / 40×40 / 20×20 (pas de tête P2), entrée 640×640 (§V-H3).
- Perte : CIoU + focal loss + BCE (Éq. 5-8) ; **Soft-NMS** au lieu de NMS (§III-A4).
- **Pruning 30 %** (9,60 → 6,72 M paramètres, 8,45 → 6,31 GFLOPs) (§V-A3, Table IV) ;
  **PTQ INT8** avec jeu de calibration, puis compilation Vitis AI (XIR) en `.xmodel` pour
  le **DPU** (§III-B, §III-C). Toolflow : Vitis AI.
- Pipeline : pré- et post-traitement (dont Soft-NMS) sur le PS (ARM), inférence sur le DPU
  dans le PL ; lot de 3 images, 1 à 3 cœurs DPU, multithreading (§IV-C, Fig. 5, Fig. 7).
- Données : Foggia (31 vidéos, 320×240 à 400×256) complété d'un jeu propre (images
  Internet, images aériennes prises par drone RGB et multispectral, augmentations dont
  fumée synthétique), étiqueté en **5 classes de sévérité** (§IV-A). Le jeu propre n'est pas
  décrit en taille (n/r).

## Plateforme et implémentation

- Cartes : **Kria KV260**, **ZCU104**, **ZCU102** (toutes Zynq UltraScale+) ; DPU à 300 MHz
  (§V-D). Configuration du DPU (taille B-xxxx) dans la Table II, **absente du texte
  extrait** (n/r). Les références de puces (XCK26, XCZU7EV, XCZU9EG) ne sont pas citées par
  les auteurs.
- Ressources (LUT, FF, BRAM, DSP, URAM) : Table VI, **sans corps extrait** (n/r). Texte :
  sur KV260, LUT et FF « high » dès un cœur, BRAM et DSP modérés grâce à l'URAM ; au plus
  2 cœurs sur KV260 (§V-C).
- **Puissance mesurée à la carte** avec une alimentation de labo OWON P4305 (→ `board`) ;
  répartition statique / dynamique estimée par Vivado Power Analysis (Fig. 8) (§V-D2).
- Intégration drone : KV260 comme ordinateur compagnon, caméra USB Insta360, Pixhawk 2.4.8
  (§IV-B, Fig. 4). **Mais l'évaluation se fait sur images, pas sur le flux caméra** (§IV-C),
  et aucun essai en vol n'est rapporté.
- Code : dépôt annoncé https://github.com/halalboro/fpga-accelerators.git (§IV-C) ;
  bitstream / xmodel non mentionnés.

## Résultats

Toutes les valeurs viennent du texte : les Tables III, IV, VII et VIII n'ont pas de corps
extrait, les Tables V et VI non plus (légendes seules).

| Configuration | mAP | FPS | Puissance (carte) | Source |
|---|---|---|---|---|
| LCAM-YOLOX FP32 | 79,89 % | n/r | n/r | §V-A2 |
| LCAM-YOLOX FP32 + prétraitement | 81,63 % | n/r | n/r | §V-A3 |
| LCAM-YOLOX INT8, KV260 1 cœur | 78,11 % | 195 | 9,72 W | §V-A2, §V-D |
| KV260 2 cœurs | n/r | 387 | 10,45 W | §V-D |
| ZCU104 1 / 2 cœurs | n/r | 193 / 337 | 13,20 W (charge max) | §V-D1-2 |
| ZCU102 3 cœurs | n/r | 481 | 22,13 W | §V-D1-2 |
| Jetson Nano | n/r | 65 | n/r | §V-D |
| STM32H7A3 | n/r | 15 | n/r | §V-D |

- Efficacité : jusqu'à **37,15 FPS/W** sur KV260 à 2 cœurs (§V-G4, §VI).
- Modèle non élagué : 76 FPS ; élagué 30 % : 195 FPS (×2,56) (§V-A3).
- Baselines (FP32 / INT8 mAP) : YOLOv3 62,31 / 60,76 % (65,2 M param., 416×416) ; YOLOv5
  74,06 / 72,77 % (7,2 M) ; YOLOX-m 78,44 % FP32 (déduit de « +1,45 % ») ; MobileNetV2
  68,23 % (13 FPS) ; EfficientDet 73,42 % (98 FPS) ; Faster R-CNN 79,12 % (12 FPS) ;
  RetinaNet 78,21 % (16 FPS) (§V-A1). La plateforme de ces FPS n'est pas dite dans le texte.
- Ablation : YOLOX 76,45 % → + spatial 77,23 % → + canal 77,98 % → les deux 78,56 % →
  LCAM 79,89 % (Table V, texte de la légende Fig. 5).
- DPU vs PS : le pré/post-traitement sur le PS ne profite pas des cœurs supplémentaires
  (§V-F).

→ reportés dans `benchmarks.csv` : 7 lignes (KV260 1 et 2 cœurs, ZCU104 1 et 2 cœurs,
ZCU102 3 cœurs, Jetson Nano, STM32H7A3), toutes `confidence: medium` (texte, tableaux
absents).

## Limites et critique

- **Tableaux absents à l'extraction** : les chiffres fins (ressources, TOPS, coût, latence)
  sont perdus ; ce qui est ci-dessus vient du texte.
- **Comparaison matérielle déséquilibrée** : les FPGA tournent le modèle **élagué + INT8**,
  alors que la précision / quantification sur Jetson Nano et STM32 n'est pas donnée (n/r) ;
  aucun TensorRT mentionné. Puissance du Jetson Nano non rapportée, donc le « meilleur
  FPS/W » n'est démontré qu'entre FPGA.
- **Chiffres MCU invraisemblables** (déduit) : 15 FPS et « 0,28 TOPS » pour un STM32H7A3
  (Cortex-M7) avec un modèle de 6,7 à 9,6 M paramètres et ~6 GFLOPs sont incompatibles avec
  la mémoire et le débit d'un MCU de cette classe. À ne pas citer sans vérification.
- **Ambiguïtés** : le 195 FPS est celui du modèle élagué, mais le 78,11 % est-il mesuré
  après pruning ? Non dit (§V-A3). « 337FPS (one-core) » pour ZCU104 est probablement une
  coquille (2 cœurs). 37,15 FPS/W ne correspond pas exactement à 387 / 10,45 = 37,0 (déduit).
- **Puissance élevée pour un drone** : ~10 W carte pour la KV260, c'est la gamme Jetson,
  pas la gamme nano ; l'impact sur l'autonomie de vol n'est pas mesuré, aucun vol rapporté.
- **Évaluation hors ligne** sur images ; métrique mAP sans seuil IoU précisé ; jeu de
  données propre non publié, 5 classes de sévérité non standard : non comparable à VisDrone
  ou DAC-SDC.
- Pas de comparaison avec d'autres travaux YOLO/FPGA (Table VIII « Comparison » absente de
  l'extraction : contenu inconnu).
- Soft-NMS exécuté sur le PS : latence de bout en bout non chiffrée dans le texte (Fig. 7
  seulement).

## Pertinence pour la thèse

- Un exemple typique de la chaîne **YOLO + Vitis AI DPU sur KV260 embarquée sur drone**,
  avec puissance **mesurée à la carte** : utile comme point de référence (≈ 10 W, ≈ 200-390
  FPS en 640×640) pour l'axe `drone-fpga`.
- Confirme l'hypothèse : pas de tête P2 ni de Transformer portés (attention CBAM-like
  seulement, compatible DPU) ; pas de mAP_small ; pas de métrique système (autonomie,
  vitesse de vol) malgré l'intégration Pixhawk.
- Montre un point méthodologique réutilisable : le pré/post-traitement sur le PS devient le
  goulot quand on multiplie les cœurs DPU (§V-F).

## Gaps identifiés

- Portage DPU d'un YOLO drone « petits objets » (tête P2) avec mesure du mAP_small avant /
  après INT8 : absent ici.
- Mesure en vol (impact des ~10 W sur l'autonomie) d'une KV260 comme ordinateur compagnon.
- Comparaison équitable FPGA vs Jetson (même précision INT8, TensorRT, puissance carte des
  deux côtés).
- Post-traitement (Soft-NMS) accéléré sur PL.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). Tables III, IV, VII,
VIII sans corps extrait (warnings) ; Tables I, II, V, VI également absentes (légendes ou
rien). Certains passages de §III (backbone, loss) sont mal découpés. Le chiffre YOLOX-m
FP32 (78,44 %) est calculé à partir du « +1,45 % » du texte.

Ce qui suit est déduit et non affirmé par les auteurs :
- l'invraisemblance des chiffres STM32H7A3 ;
- la coquille probable « 337FPS (one-core) » ;
- les références de puces des cartes ;
- le rattachement de 13,20 W à la configuration 2 cœurs de la ZCU104 dans `benchmarks.csv`
  (le texte dit « at maximum load ») ;
- la mention « modèle élagué » sur les lignes FPGA (le texte lie 195 FPS au pruning).
