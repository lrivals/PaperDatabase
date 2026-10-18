---
id: arxiv-2106.09018-end-end-semi-supervised-object
fiche: done
date: 2026-10-18
---

# End-to-End Semi-Supervised Object Detection with Soft Teacher

Mengde Xu, Zheng Zhang, Han Hu, Jianfeng Wang, Lijuan Wang, Fangyun Wei, Xiang Bai, Zicheng Liu, 2021, arXiv preprint. https://arxiv.org/abs/2106.09018
Type : preprint non relu par les pairs

## Problème

Les méthodes de détection semi-supervisée à base de pseudo-labels (STAC, Self-training) sont multi-étapes : un détecteur initial est entraîné sur peu de données annotées, il pseudo-annote les images non annotées, puis on ré-entraîne. La qualité finale est bornée par ce détecteur initial, probablement imprécis (§1). Les auteurs veulent un entraînement de bout en bout où pseudo-labels et détecteur s'améliorent mutuellement, et un usage plus riche du teacher qu'une simple boîte à label dur.

## Méthode

- Cadre teacher-student (§3.1) : à chaque itération, images annotées et non annotées sont tirées selon un ratio d'échantillonnage s_r pour former un batch. Le teacher est une moyenne mobile exponentielle (EMA) du student et produit les pseudo-boîtes ; le student s'entraîne sur les annotées (vérité terrain) et les non annotées (pseudo-boîtes). Perte L = L_s + α·L_u (Éq. 1). Le teacher voit une augmentation faible, le student une augmentation forte (principe FixMatch ; Table 2 : scale jitter, solarize, brightness, contrast, sharpness, translation, rotation, cutout).
- Pseudo-boîtes : NMS puis seuil de score de premier plan ; seuil retenu 0,9 (§4.2).
- Soft teacher (§3.2) : le seuil élevé donne une bonne précision mais un rappel faible (à 0,9 : précision 89 %, rappel 33 %, Fig. 3a), donc beaucoup de vrais objets sont étiquetés fond. La perte de classification de chaque candidat de fond est pondérée par sa fiabilité r_j (poids normalisé w_j = r_j / Σr_k, Éq. 4-5), estimée par le score de fond du teacher (BG-T) sur les candidats générés par le student. Alternatives testées : score de fond du student (BG-S), différence student/teacher (Pred-Diff), IoU, IoU inverse.
- Box jittering (§3.3) : le score de premier plan corrèle mal avec la précision de localisation (Fig. 3b). Chaque pseudo-boîte est jitterée N_jitter fois (décalages uniformes de ±6 % de la hauteur/largeur), re-régressée par le teacher, et la variance normalisée des 4 coordonnées (Éq. 8-9) mesure la fiabilité de localisation. Seules les boîtes sous un seuil de variance servent à la régression. Calcul limité aux boîtes de score > 0,5 (environ 17 par image).
- Hyperparamètres (§4.2) : Faster R-CNN + FPN, ResNet-50 ImageNet, MMDetection ; N_jitter = 10, seuil de variance 0,02. Régime partiel : 180k itérations, 8 GPU x 5 images, s_r = 0,2 décroissant vers 0 sur les 10 000 dernières itérations. Régime complet : 720k itérations, 8 GPU x 8 images, s_r = 0,5 décroissant vers 0 sur les 20 000 dernières.

## Plateforme et implémentation

Sans objet (entraînement sur 8 GPU, modèle non précisé). Latence, FPS et puissance : n/r. Le papier annonce code et modèles à https://github.com/microsoft/SoftTeacher (résumé) ; non vérifié ici.

## Résultats

COCO val2017, mAP, Faster R-CNN R50-FPN sauf mention.

| Régime | Supervisé | STAC | Soft Teacher | Source |
|---|---|---|---|---|
| 1 % annoté | 10,0 | 13,97 | 20,46 ± 0,39 | Table 3 |
| 5 % annoté | 20,92 | 24,38 | 30,74 ± 0,08 | Table 3 |
| 10 % annoté | 26,94 | 28,64 | 34,04 ± 0,14 | Table 3 |

Gains sur STAC : +6,5 / +6,4 / +5,4 (§4.3). Moyenne sur 5 folds STAC.

Régime « COCO complet (118k) + unlabeled2017 (123k) » (Table 5, §4.3) : R50 40,9 → 44,5 (+3,6) ; R101 43,8 → 46,8 (+3,0) ; HTC++ Swin-L 57,1 → 59,1 (+2,0) ; HTC++ multi-échelle 58,2 → 59,9 (+1,7). En comparaison (Table 4, §4.3) : Proposal Learning +1,0, STAC −0,3. Test-dev2017 : HTC++ Swin-L 58,9 → 60,4 (+1,5) ; avec pré-entraînement Object365 : 61,3 (résumé, §1).

Ablations (10 % annoté, un seul fold STAC, §4.4) :
- Multi-étape 28,7 vs E2E 30,0 vs E2E + EMA 31,2 ; supervisé 27,1 (Table 6).
- Avec soft teacher : 33,6 (+2,4) ; avec en plus box jittering : 34,2 (+3,0 sur E2E+EMA) (Table 7, §4.4).
- Indicateur de fiabilité : BG-T (score de fond du teacher) est le meilleur ; passer au student dégrade ; IoU et IoU inverse n'apportent presque rien (texte §4.4 ; le corps de la Table 8 n'est pas extrait).
- Seuil de score de premier plan (Table 9) : 0,70 → 29,9 ; 0,80 → 33,2 ; 0,90 → 33,6 ; 0,95 → 32,1. Optimum 0,9.
- Seuil de variance de régression (Table 10) : 0,04 → 33,8 ; 0,03 → 34,0 ; 0,02 → 34,2 ; 0,01 → 32,9.
- N_jitter (Table 11) : 5 → 34,0 ; 10 → 34,2 ; 15 → 34,2 (saturé à 10).
- Ratio annoté/non annoté : s_r fixé à 0,2 (partiel) et 0,5 (complet), mais aucune ablation de s_r n'est rapportée.

→ reportés dans `benchmarks.csv` : 15 lignes proposées (fichier `.cache/bench/arxiv-2106.09018-end-end-semi-supervised-object.csv`, à intégrer par l'agent principal) ; 1 %, 5 %, 10 %, quatre détecteurs en régime complet, test-dev (2 lignes), 5 lignes d'ablation.

## Limites et critique

- Un seuil de 0,9 a été réglé sur COCO 10 % ; sa transposition à un autre dataset (nombre de classes, déséquilibre, petits objets) n'est pas testée. Le meilleur seuil dépend de la calibration du teacher, ce que le papier ne discute pas (déduit).
- Table 6 (E2E vs multi-étape) et Tables 8-9-11 : corps reconstruits ou lisibles seulement en partie ; les valeurs citées coïncident avec le texte pour 31,2, 33,6 et 34,2.
- Table 5, ligne HTC++ : le texte (§4.3) annonce +1,8 en détection et +1,4 en masque, alors que la table lue indique +2,0 ; incohérence non résolue (valeurs de la table retenues).
- Le gain décroît quand les labels abondent (+10,5 pts au sommet à 1 % vs +1,5 sur Swin-L test-dev, calcul sur mAP) : l'intérêt est maximal en régime peu annoté.
- Évalué sur COCO seulement, avec Faster R-CNN (deux étages) ; aucun détecteur YOLO ni mono-étage. Le coût d'entraînement (deux modèles, 180k à 720k itérations sur 8 GPU) n'est pas chiffré.
- Pas de relecture par les pairs (preprint). Le non annoté de COCO provient du même domaine que l'annoté : pas de test de décalage de domaine.
- Le résumé dit que la perte est pondérée par le « score de classification » du teacher, alors que §3.2 utilise le score de fond du teacher comme proxy de fiabilité du fond ; même idée, formulation différente.

## Pertinence pour la thèse

Axe auto-labelling. Pour CONSTRUIRE un dataset : quand peu d'images sont annotées (1 à 10 % d'un corpus) et que beaucoup d'images brutes sont disponibles, l'entraînement semi-supervisé apporte +5 à +10 mAP sur COCO, bien plus qu'un gain marginal. Pour ANNOTER : le teacher joue le rôle de pré-annotateur en ligne ; le seuil 0,9 (précision 89 %, rappel 33 %) rappelle qu'un pseudo-label fiable est conservateur et manque des objets, d'où le traitement des candidats « fond » comme incertains plutôt que négatifs. Règle pratique : peser les négatifs par la confiance du teacher plutôt que les durcir, et ne régresser que sur des boîtes dont la localisation est stable sous jitter (variance < 0,02). Pour AUGMENTER : augmentation faible côté teacher, forte côté student (scale, couleur, cutout ; Table 2), à rapprocher des augmentations YOLO. Pour PRÉTRAITER : rien. À appliquer quand il existe un grand stock non annoté du même domaine ; peu utile quand les labels couvrent déjà tout le corpus (+1,5 à +3,6 mAP seulement). Laisse ouvert : transposition à YOLO (mono-étage, sans proposals), petits objets, domaines éloignés de COCO.

## Gaps identifiés

- Aucune évaluation de la méthode avec un détecteur type YOLO ou sur un dataset de domaine (aérien, embarqué, petits objets).
- Pas d'ablation du ratio annoté/non annoté (s_r) ni de la taille du stock non annoté.
- Sensibilité du seuil 0,9 à la calibration du teacher et au déséquilibre de classes non étudiée.

## Statut de lecture

Papier complet (fulltext.md lu en entier ; extraction GROBID, ok). Tables 6, 8, 9, 11 listées sans corps extrait par le parseur mais les corps ont été retrouvés en texte libre et ils sont cohérents avec le texte ; Tables 7 et 10 reconstruites par PyMuPDF, chiffres à vérifier (recoupés avec le texte pour 34,2 et 0,02). Table 8 : valeurs n/r. Ce qui suit est déduit et non affirmé par les auteurs : dépendance du seuil à la calibration du teacher, transposition à YOLO, coût d'entraînement, gain décroissant avec le volume annoté (calcul à partir des tables).
