---
id: arxiv-2207.02541-dense-teacher-dense-pseudo-labels
fiche: done
date: 2026-10-18
---

# Dense Teacher: Dense Pseudo-Labels for Semi-supervised Object Detection

Hongyu Zhou, Zheng Ge, Songtao Liu, Weixin Mao, Zeming Li, Haiyan Yu, Jian Sun, 2022, arXiv preprint. https://arxiv.org/abs/2207.02541
Type : preprint non relu par les pairs

## Problème

Les détecteurs semi-supervisés (SS-OD) les plus performants reposent sur des pseudo-boîtes : sortie du teacher, puis NMS, seuillage du score et assignation de labels (Fig. 1, §1). Cette chaîne introduit des hyper-paramètres (seuil de score σ_t, seuil NMS σ_nms) qui influencent fortement la performance (§1). Les auteurs identifient trois défauts (§3.2) :
- Seuil de score : la performance fluctue fortement avec σ_t sur COCO et CrowdHuman ; à σ_t élevé (0,7 et 0,9) l'entraînement ne converge pas (beaucoup de faux négatifs du teacher), à σ_t bas (0,3) la performance se dégrade (faux positifs) (Fig. 2a, c, d). Les valeurs exactes de mAP ne sont que dans la figure, non extraite : `n/r`.
- NMS : σ_nms optimal différent selon le dataset (0,7 sur COCO, 0,8 sur CrowdHuman), avec de fortes fluctuations surtout en scène dense (Fig. 2b, §3.2).
- Assignation inconsistante : une pseudo-boîte légèrement imprécise, même à IoU 0,5 avec la vérité, produit des positifs/négatifs différents de ceux de la vérité terrain (Fig. 3).

## Méthode

- Cadre teacher/student classique : le teacher est une EMA du student, perte totale L = L_s + w_u·L_u (§3.1, Éq. 1).
- Dense Pseudo-Label (DPL) : la sortie du teacher après sigmoïde, par ancre/pixel, sans seuil, sans NMS, sans assignation (§3.3). Elle est continue, donc supervisée par la Quality Focal Loss (γ = 2) au lieu de la focal loss binaire (Éq. 2, §4.1).
- Sans filtre, le DPL garde beaucoup de prédictions faibles sur le fond. Division en région d'apprentissage et région supprimée : score S_i = max sur les classes ; on garde le top k % des positions (selon le Feature Richness Score), le reste est mis à 0 (Éq. 3-4, §3.3). Le top-k inclut des négatifs difficiles (hard negatives) : seulement ~0,4 % de positifs dans COCO train2017 avec l'assignation FCOS (§4.2).
- La région sélectionnée permet aussi un apprentissage non supervisé de la branche de régression (IoU loss) (§3.3).
- Détecteur : FCOS (one-stage, anchor-free), ResNet-50 ImageNet, batch 16 étiqueté + 16 non étiqueté, lr 0,01, w_u = 4 (COCO-Standard) ou 2 (autres cas), burn-in puis mêmes augmentations que Unbiased Teacher (§4.1). Le choix des détecteurs denses est assumé dès §3 : la méthode vise les détecteurs one-stage.

## Plateforme et implémentation

Sans objet (pas de FPGA ni mesure de FPS ou de puissance : `n/r`). Code publié : https://github.com/Megvii-BaseDetection/DenseTeacher (Abstract).

## Résultats

- Ablation COCO-Standard 10 % (Table 1) : supervisé 26,44 ; Unbiased Teacher* (ré-implémenté sur FCOS) 31,52 ; DPL sur toute l'image 32,00 ; avec division de région 33,34 ; avec régression non supervisée 35,11 (contre 33,13 pour Unbiased Teacher* avec régression). Remplacer les pseudo-boîtes par le DPL seul n'apporte donc que +0,48 mAP ; l'essentiel du gain vient de la région d'apprentissage (§4.2).
- COCO-Standard (Table 2, mAP moyenne de 5 folds) :

| Labels COCO | 1 % | 2 % | 5 % | 10 % |
|---|---|---|---|---|
| Supervisé | 11,24 | 15,04 | 20,82 | 26,44 |
| Unbiased Teacher (Faster R-CNN, rapporté) | 20,75 | 24,30 | 28,27 | 31,50 |
| Unbiased Teacher* (FCOS, ré-impl.) | 18,31 | 22,39 | 27,73 | 31,52 |
| Dense Teacher | 19,64 | 25,39 | 30,83 | 35,11 |
| Soft Teacher (jittering à grande échelle) | 20,46 | - | 30,74 | 34,04 |
| Dense Teacher (jittering à grande échelle) | 22,38 | 27,20 | 33,01 | 37,13 |

  À 1 %, Dense Teacher (19,64) reste sous Unbiased Teacher Faster R-CNN (20,75) ; l'écart de +1,2 mAP n'est tenu que face à la version FCOS (§4.3, texte).
- Sensibilité aux hyper-paramètres propres à la méthode (Table 7, COCO 10 %) : k = 0,1 / 0,5 / 1 / 3 / 5 % donne 25,76 / 34,11 / 35,11 / 34,47 / 33,85 mAP, optimum à 1 % (≈ 0,4 % de positifs + hard negatives) ; w_u = 2 / 4 / 8 donne 34,86 / 35,11 / 33,81 ; en COCO-Full w_u = 2 donne 44,92 contre 43,04 pour w_u = 4. Plage utile étroite pour k, plus tolérante pour w_u.
- Hard negatives (Table 5, classification seule) : supprimés 31,56, ignorés 32,64, sélectionnés 33,34 ; avec régression : 33,47 / 34,72 / 35,11.
- VOC07 test (Table 3), mAP 50:95 : Dense Teacher 55,87 (non étiqueté VOC12) et 57,52 (VOC12 + COCO20cls), contre 48,69 et 50,34 pour Unbiased Teacher. Supervisé : 71,69 AP50 / 45,87 mAP. Gain annoncé : +8,2 AP50 et +10,0 mAP (§4.3).
- COCO-Full : +3,1 mAP avec unlabeled2017 ; avec jittering et schedule plus long, 46,12 mAP (+4,9 vs supervisé) (§4.3). Table 4 sans corps extrait : détail par méthode `n/r`.
- Autres détecteurs / jeux (Table 6, corps non extrait, valeurs recoupées par le texte §4.4) : RetinaNet (anchor-based) 31,1 contre 28,9 pour Unbiased Teacher (+2,2 AP) ; CrowdHuman avec FCOS : 60,7 contre 62,8 (mMR, -2,1, plus bas est mieux).
→ reportés dans `benchmarks.csv` : 13 lignes proposées (4 COCO-Standard FCOS, 4 COCO-Standard avec jittering, 1 COCO-Full, 2 VOC, 1 RetinaNet, 1 CrowdHuman), écrites dans `.cache/bench/` et non encore ajoutées au fichier.

## Limites et critique

- Preprint non relu par les pairs ; une seule graine par dossier de labels n'est pas précisée, mais les écarts-types sur 5 folds sont donnés (Table 2).
- Comparaisons non homogènes : les baselines de la littérature sont en Faster R-CNN, Dense Teacher en FCOS ; les auteurs ré-implémentent Unbiased Teacher sur FCOS (marqué *), qui est plus faible à 1 % (18,31 contre 20,75). Les lignes « jittering à grande échelle » comparent des schedules plus longs à Soft Teacher (§4.3).
- Le gain isolé du DPL (+0,48 mAP) est modeste ; la majorité du gain vient de la sélection top-k, des hard negatives et de la régression non supervisée : l'attribution du gain à la « densité » des labels est donc nuancée par leurs propres chiffres (Table 1).
- La dépendance aux hyper-paramètres est déplacée, pas supprimée : k (sensible, 25,76 à 0,1 % contre 35,11 à 1 %) et w_u (dépend de la quantité d'étiquettes). L'étude de sensibilité des pseudo-boîtes (Fig. 2) est menée sur Unbiased Teacher uniquement et illustrée par des courbes non extraites.
- Méthode limitée aux détecteurs denses ; pas d'évaluation sur YOLO (déduit : transposable en principe à un détecteur YOLO anchor-free, non testé).
- Pas de mesure de coût d'entraînement ni d'analyse de la qualité des pseudo-labels hors Fig. 2c-d.

## Pertinence pour la thèse

Axe `auto-labelling`. Ce que le papier apprend pour ANNOTER un dataset de détection quand peu d'images sont étiquetées (1 à 10 % de COCO) : (1) avec un détecteur dense proche de YOLO, un pipeline de pseudo-labels par boîtes (seuil + NMS) est fragile : seuil de score et NMS sont à régler par dataset et peuvent faire diverger l'entraînement ; (2) si l'on entraîne en semi-supervisé, distiller les scores denses du teacher sur les positions les plus riches (k ≈ 1 %, hard negatives inclus) est plus robuste et surpasse les approches à pseudo-boîtes à 2, 5 et 10 % (Table 2) ; (3) à très peu de labels (1 %), l'avantage disparaît face à un teacher Faster R-CNN. À appliquer : peu d'annotations mais beaucoup d'images non étiquetées, détecteur one-stage, scènes denses (CrowdHuman). Ne s'applique pas à de la pré-annotation destinée à un humain (il faut alors des boîtes), ni au format d'export YOLO : le DPL est une cible d'entraînement interne, pas un label exportable. Pour CONSTRUIRE/PRÉTRAITER/AUGMENTER : il réutilise les augmentations d'Unbiased Teacher et l'ajout de jittering à grande échelle apporte +2 à +3 mAP (Table 2), mais sans ablation propre.

## Gaps identifiés

- Aucune évaluation de semi-supervisé dense sur une famille YOLO (ancres, mosaic) ni sur petits objets ou images aériennes.
- Pas de comparaison à une pré-annotation par modèle fondation (SAM, Grounding DINO) avec revue humaine.
- Pas d'étude du coût d'annotation évité (nombre d'images étiquetées pour une performance donnée) hors points 1 à 10 % de COCO.

## Statut de lecture

papier complet (`fulltext.md` lu en entier, extraction grobid ok). Table 4 et Table 6 : corps non extraits (valeurs de Table 6 retrouvées dans le texte §4.4, confiance `medium`) ; Table 3 partiellement tronquée (seules les lignes « Ours » et Unbiased Teacher, Li et al., Instant Teaching sont lisibles) ; Fig. 2 (courbes de sensibilité au seuil et au NMS) non extraite : les valeurs de mAP par seuil sont `n/r`. Déduit et non affirmé par les auteurs : la transposition à YOLO, le fait que le gain du DPL seul soit « modeste » (calcul 32,00 - 31,52 depuis Table 1), et la limite de l'applicabilité à la pré-annotation humaine.
