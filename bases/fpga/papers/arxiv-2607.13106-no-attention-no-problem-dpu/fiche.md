---
id: arxiv-2607.13106-no-attention-no-problem-dpu
fiche: done
date: 2026-09-29
---

# No Attention, No Problem: DPU-Aware Attention Approximation in Modern YOLO on FPGA

Suraj Karki, Qazi Arbab Ahmed, Thorsten Jungeblut, 2026, arXiv preprint. https://arxiv.org/abs/2607.13106
Type : preprint non relu par les pairs.

## Problème

Les YOLO récents (YOLOv11 avec attention spatiale C2PSA, YOLOv26 sans DFL ni NMS) utilisent des opérateurs non supportés par le DPU de Vitis AI (SiLU, split, reshape/transpose/matmul/softmax) ; ils s'exécuteraient sur CPU. Peu de travaux couvrent ces YOLO ou la détection orientée (OBB) sur FPGA (§I, §II-B).

## Méthode

- Adaptations DPU-aware (§III-B) : SiLU remplacée par ReLU ; split du bloc C2f remplacé par deux convolutions 1x1 initialisées en matrices de sélection ; attention C2PSA approximée par convolutions 1x1 (q, k, v), produit élément par élément q⊙k, hard-sigmoid à la place du softmax, projection 1x1 et fusion résiduelle (Fig. 3). YOLOv8n, v11n, v26n et variantes OBB.
- Entraînement Ultralytics, entrée 416, FP16 (§III-C) ; PTQ INT8 Vitis AI (calibration sur sous-ensemble, pas de QAT) (§III-C) ; compilation XIR pour DPUCZDX8G (§III-D).
- Six jeux : COCO, VOC, KITTI, DOTA, DIOR-R et un jeu maison de détection de personnes (CCTV + images VOC, 18 820 images 416x416, 184 789 annotations, classe unique) (§III-A).
- Benchmark sur les 8 configurations DPU B512 à B4096 reconstruites via Vitis TRD (Vivado/Vitis 2022.2) (§III-E). NMS conservé pour toutes les mesures d'accuracy (§III-B3).

## Plateforme et implémentation

- Puce : Zynq UltraScale+ MPSoC EV sur ZCU104 (XCZU7EV), DPUCZDX8G non modifié (B512 à B4096), application Python avec Vitis AI Library sur l'ARM Cortex-A53 (§III-F, §IV-A). Fréquence DPU : n/r.
- FPS et latence mesurés sur un seul cœur DPU avec la vidéo PETS2009-S2L1 (768x576, 795 frames) (§IV-C).
- Puissance : « on-chip power » rapportée par Vivado (Table III) : estimation par l'outil, pas mesure. Ressources B4096 : 55,8k LUT, 142 BRAM, 46 URAM, 710 DSP (Table III).
- Code/bitstream : non publiés d'après le texte.

## Résultats

- Accuracy mAP@0.5:0.95 (Table II, CPU contre FPGA INT8) : YOLOv11n VOC 0,59 → 0,57 ; COCO 0,31 → 0,29 ; jeu personne 0,75 → 0,71 ; YOLOv26n personne 0,71 → 0,67 ; YOLOv8n VOC 0,60 → 0,45 et KITTI 0,64 → 0,34 (chute forte). Tableau I : les modifications coûtent ≈ 3 points en moyenne (§IV-B).
- Débit B4096 : YOLOv26n 34,05 FPS E2E, 29,37 ms ; YOLOv26n-OBB 29,55 FPS, 33,85 ms (§IV-C) ; l'écart DPU contre E2E montre un goulot dans le post-traitement (NMS, mono-cœur) (§IV-C, Conclusion) ; valeurs FPS_DPU par architecture seulement en Fig. 6 à 8 (non extraites).
- Puissance et ressources par architecture : 4,792 W (B512) à 8,760 W (B4096) (Table III).
→ reportés dans `benchmarks.csv` : 29 lignes fournies dans `bench_rows.csv` : 8 lignes IP DPU (Table III), 21 lignes modèle x jeu (Table II). FPS, latence, puissance, ressources attachés uniquement aux lignes YOLOv26n(-OBB) / jeu de personnes à B4096 (mesure réalisée sur une vidéo de personnes, PETS2009).

## Limites et critique

- Incohérences internes : le résumé annonce ≈ 5 % de perte d'accuracy, §IV-B ≈ 7 % ; la Table I et la Table II ne concordent pas exactement (ex. YOLOv8n KITTI modifié 0,63 contre CPU 0,64) ; les écarts sont très variables (YOLOv8n KITTI 0,64 → 0,34 ; DPU YOLOv11n presque sans perte), pas expliqués.
- Aucune répétition ni barre d'erreur ; PTQ seule, pas de QAT malgré des pertes parfois fortes.
- « 3x moins de puissance que l'état de l'art » (Résumé, Conclusion) compare une puissance estimée par Vivado (puce, hors mesure) à celle de [27] (SATAY), probablement mesurée : portées non comparables ; comparaison aussi entre DPU générique et flot en streaming ; aucune baseline Jetson ni GPU embarquée.
- Débit E2E (≈ 34 FPS) limité par le post-traitement CPU : résultat plus sur l'intégration logicielle que sur l'accélérateur ; FPS mesuré sur une vidéo différente de celles de l'accuracy.
- Approximation de l'attention non validée en qualité (ablation) : hard-sigmoid et q⊙k changent la fonction ; l'entraînement est refait avec les modifications, donc il ne s'agit pas d'une approximation à iso-poids.
- Jeu de personnes maison non publié, aucun résultat en conditions industrielles.

## Pertinence pour la thèse

Très proche du cas d'application : détection de personnes (jeu CCTV) avec YOLOv8/v11/v26 nano INT8 sur ZCU104 via DPU ; donne des ordres de grandeur d'accuracy (≈ 0,67-0,79 mAP@0.5:0.95 sur personnes) et de débit, et documente les modifications nécessaires pour le DPU. Illustre aussi le problème pour la certification : le modèle déployé (ReLU, attention approximée, INT8) diffère du modèle de référence ; l'écart d'accuracy, hétérogène, doit être justifié. Ne traite pas la sûreté ni la fiabilité.

## Gaps identifiés

- Écarts d'accuracy CPU → FPGA imprévisibles selon modèle et jeu (YOLOv8n KITTI) : besoin de méthodes de vérification de conformité de la quantification.
- Goulot du post-traitement (NMS) sur la partie logicielle : déterminisme et latence pire cas non étudiés.
- Aucune mesure de puissance réelle (carte) pour ces YOLO récents sur DPU.

## Statut de lecture

Papier complet (fulltext.md lu en entier). Section IV mal numérotée dans l'extraction (avertissement) ; le texte de §IV-C est entrelacé avec la légende de Table II ; FPS_DPU et latence DPU par architecture sont uniquement dans les Fig. 6 à 8, non extraites : non reportés. Déduit et non affirmé par les auteurs : `power_scope` = `estimated` (rapport Vivado), portée de la comparaison à [27], absence de code publié.
