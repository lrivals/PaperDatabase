---
id: arxiv-2511.10905-yolo-drone-efficient-object-detection
fiche: done
date: 2026-09-28
---

# YOLO-Drone: An Efficient Object Detection Approach Using the GhostHead Network for Drone Images

Hyun-Ki Jung, 2025, Journal of Information Systems Engineering and Management, Vol. 10, No. 26s, 2025, pp. 236-247. https://doi.org/10.52783/jisem.v10i26s.4216 (arXiv 2511.10905)
Type : article de journal, d'après la journal_ref arXiv ; revue généraliste peu
spécialisée en vision.

## Problème

Détecter de petits objets dans des images de drone prises en altitude, sur VisDrone, avec
un détecteur léger. L'objectif est d'améliorer à la fois la précision et la vitesse de
YOLOv11n (Abstract, Introduction).

## Méthode

- Base : **YOLOv11n** (depth 0,5, width 0,25), entrée 640×640, 100 epochs, paramètres par
  défaut d'Ultralytics (Results, Experimental environment).
- **GhostHead** : dans la **tête** seulement, les Conv sont remplacées par des **GhostConv**
  (GhostNet [34]) et les C3k2 par des **C2f** (bloc de YOLOv8). Le backbone reste inchangé
  (Fig. 4, section YOLOv11 algorithm). Le modèle obtenu s'appelle YOLO-Drone.
- Pas de tête P2, pas de quantification, pas de pruning.

## Plateforme et implémentation

- Entraînement et inférence sur **Google Colab, GPU NVIDIA Tesla T4**, PyTorch 2.3.0,
  CUDA 12.2 (Experimental environment). Le corps de la Table 1 n'est pas extrait.
- « Inference Speed » : 1,8 ms contre 2,0 ms pour YOLOv11n (Table 2). Batch, précision
  numérique et prise en compte du pré- et post-traitement (NMS) : `n/r`.
- Aucun déploiement embarqué, aucune puissance mesurée. Code : non mentionné.

## Résultats

Sur VisDrone (6471 images d'entraînement, 548 de validation, 1610 de test, 10 classes). Le
split d'évaluation n'est pas précisé : la Table 4 compte 38 759 instances.

| Modèle | P | R | F1 | mAP@0.5 | GFLOPs | Inférence (ms) | Source |
|---|---|---|---|---|---|---|---|
| YOLOv8(n) | 41,2 | 30,6 | 35,1 | 30,3 | 8,2 | n/r | Table 3 |
| YOLOv9(t) | 41,0 | 30,0 | 34,6 | 30,1 | 7,9 | n/r | Table 3 |
| YOLOv10(n) | 40,6 | 30,2 | 34,6 | 29,8 | 8,2 | n/r | Table 3 |
| YOLOv11n | 39,6 | 30,9 | 34,7 | 29,9 | 6,6 | 2,0 | Tables 2-3 |
| **YOLO-Drone** | 40,0 | 31,5 | 35,2 | **30,4** | 6,7 | 1,8 | Tables 2-3 |

Les variantes (n, t) des YOLOv8/9/10 ne sont pas nommées dans les tableaux. On les
suppose de taille nano d'après les GFLOPs (déduit).

- Par classe (Table 4) : la meilleure est « car », à 73,9 de mAP@0.5 ; les plus faibles
  sont « bicycle » (6,5) et « awning-tricycle » (10,2).
- Les images de nuit ou dans l'ombre sont les plus difficiles (Fig. 7, qualitatif).

→ reportés dans `benchmarks.csv` : 1 ligne, YOLO-Drone sur Tesla T4 avec 30,4 de mAP@0.5
et 1,8 ms (Table 2, `high`). Le FPS n'est pas calculé, faute de savoir ce que couvre la
mesure. Puissance `n/r`.

## Limites et critique

- **Gains dans le bruit** : +0,5 point de mAP@0.5 et −0,2 ms, sur une seule exécution,
  sans écart-type. Un écart de 0,1 point face à YOLOv8n n'est pas significatif sans
  répétitions.
- **Pas de mAP@0.5:0.95 ni de mAP_small**, alors que l'objectif affiché est la détection de
  petits objets. Seul le mAP@0.5 global est donné.
- **GFLOPs en hausse (6,6 → 6,7) mais latence en baisse (2,0 → 1,8 ms)** : c'est
  contre-intuitif pour un seul run de Colab sur T4. La mesure n'est pas décrite (batch,
  FP16, NMS).
- Le **split d'évaluation n'est pas dit** (validation ou test-dev). Les chiffres ne sont
  donc pas comparables aux résultats VisDrone test-dev publiés ailleurs.
- **« Efficient » sans cible embarquée** : Tesla T4 de datacenter, sans Jetson, FPGA ni
  mesure de puissance. C'est l'exclusion du profil : GPU présenté comme solution
  « efficace ».
- Le nom « YOLO-Drone » est déjà utilisé par d'autres travaux ; attention aux confusions
  de citation (déduit).
- Venue : revue généraliste (JISEM), contribution incrémentale. Auteur unique.

## Pertinence pour la thèse

- **Faible** : une modification mineure de la tête d'un YOLOv11n, sans tête P2, sans
  quantification et sans cible embarquée.
- Il donne toutefois un **point de référence VisDrone pour la famille nano** entraînée
  par Ultralytics à 640 px et 100 epochs : environ 30 de mAP@0.5 pour 6,6 à 8,2 GFLOPs
  (Table 3). C'est l'ordre de grandeur à viser pour un YOLO nano porté sur FPGA ou Jetson.
- GhostConv dans la tête est une piste de réduction de calcul, mais son gain réel sur un
  accélérateur, où les depthwise sont souvent mal utilisées, n'est pas mesuré.

## Gaps identifiés

- **YOLO nano sur VisDrone sans mAP_small ni portage embarqué** : confirme l'hypothèse du
  profil (SOTA drone rarement évalué sur une cible embarquée).
- **Effet des GhostConv et depthwise sur la latence réelle en FPGA ou NPU** : non mesuré.
- **Protocole VisDrone hétérogène** : split, résolution et epochs varient d'un papier à
  l'autre. Il faut normaliser avant de comparer.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). La Table 1
(configuration matérielle) n'a pas de corps extrait. Les équations sont illisibles
(symboles perdus), ce qui est sans conséquence pour les résultats. Les Tables 2-4 sont
lues.

Ce qui suit est déduit et non affirmé par les auteurs :
- la taille (n, t) des YOLOv8/9/10 comparés ;
- le caractère non significatif des gains ;
- le risque de confusion avec d'autres « YOLO-Drone » ;
- l'intérêt comme référence de la famille nano.
