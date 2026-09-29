---
id: arxiv-1904.00781-rilod-near-real-time-incremental
fiche: done
date: 2026-09-29
benchmarks: none
---

# RILOD: Near Real-Time Incremental Learning for Object Detection at the Edge

Dawei Li, Serafettin Tasci, Shalini Ghosh, Jingwen Zhu, Junting Zhang, Larry Heck, 2019, arXiv preprint. https://arxiv.org/abs/1904.00781 (DOI 10.1145/3318216.3363317 dans les métadonnées, préfixe ACM : version publiée probable, venue non vérifiée)
Type : preprint non relu par les pairs (version arXiv)

## Problème

Un détecteur embarqué livré avec un appareil ne couvre pas les objets d'intérêt de chaque utilisateur ; il faut pouvoir ajouter de nouvelles classes sur l'appareil, rapidement, sans oubli catastrophique des anciennes, sans accès aux données anciennes (confidentialité) et parfois sans données d'entraînement annotées (boîtes englobantes) pour les nouvelles classes (§1).

## Méthode

- Apprentissage incrémental pour détecteur one-stage (RetinaNet), uniquement avec les données des nouvelles classes : perte focal + régression sur les nouvelles classes, plus trois distillations depuis l'ancien modèle gelé (classification, boîtes top-k, features intermédiaires du backbone), lambda1..4 = 1 (§4.2, Eq. 1-4). Extension possible avec quelques exemplaires des anciennes classes, choisis par clustering (§4.2.2).
- Construction automatique de jeu de données : images bruitées téléchargées par requête sur le nom de classe, boîtes candidates (détecteur COCO à seuil 0,2, ou EdgeBoxes), vote sur les labels d'un classifieur 11k classes + similarité Word2vec pour retenir des « credible labels », suppression des boîtes chevauchantes par score ACCS (§5, Algorithme 1).
- Deux implémentations : edge-only (tout sur Jetson TX2) et edge-cloud (Tesla M40, puis modèle transféré sur Samsung Galaxy S9) (§6.4). Framework PyTorch ; aucun FPGA.

## Plateforme et implémentation

Jetson TX2 (edge-only) ; GPU NVIDIA Tesla M40 pour le cloud et pour les expériences de précision ; inférence sur Samsung Galaxy S9 (§6.2, §6.4). Puissance : n/r. Fréquence, mémoire : n/r. ResNet-18 à entrée 512 pour les mesures système (§6.4), ResNet-50 à entrée 1024 pour Pascal VOC (§6.2). Code : non publié d'après le texte (une vidéo de démo est mentionnée en supplément).

## Résultats

- Pascal VOC, 19+1 (nouvelle classe tv/monitor, 279 images) : mAP moyen All Data 74,7 ; sans distillation de features 60,2 ; avec 65,0 ; sans distillation, oubli total (mAP 0 sur les anciennes classes) (Table 1, reconstruit, à vérifier). 10+10 : avec distillation de features 67,9 contre 62,0 sans (Table 2, corps partiellement illisible). Le texte annonce +4,8 et +5,9 points pour la distillation de features (§6.2.2).
- iKitchen : avec 10 exemplaires par ancienne classe, 38x d'accélération de l'entraînement pour 4 % de perte de précision (§6.2.4) ; +15 à 40 points de mAP avec les exemplaires (§6.2.4).
- Jeu automatique : rétention 64,6 %, taux de faux positifs 5,37 % avec détecteur profond (§6.3.2, Table 4) ; iKitchen : slow cooker 85,4 % de mAP, cocktail shaker 32,2 % (Table 5, reconstruit, à vérifier).
- Temps système (Table 7, reconstruit, à vérifier) : total 293 s edge-only (Jetson TX2, dont entraînement 233 s) contre 119 s edge-cloud (entraînement 83 s). Temps d'entraînement par epoch : 8,3 s (512) contre 17,2 s (1024) avec 10 exemplaires, sur M40 (Table 6).
→ reportés dans `benchmarks.csv` : aucune ligne. Aucune mesure d'inférence (FPS, GOPS, puissance) ; les temps rapportés sont des durées d'apprentissage incrémental, qui n'ont pas de colonne dans le schéma.

## Limites et critique

- Pas de FPGA ; la seule cible embarquée mesurée est un Jetson TX2, avec entraînement de plusieurs minutes (233 s), sans puissance ni mémoire rapportées.
- Fiabilité des chiffres : tables 1, 2, 5, 6, 7 reconstruites par PyMuPDF ou Docling (chiffres à vérifier) ; la Table 4 est illisible en partie.
- Qualité du jeu automatique très variable (cocktail shaker 32,2 %, §6.3.3), difficulté à borner pour un usage critique ; dépendance à Internet (Google Images) et à un classifieur 11k classes, non embarquables sur un microcontrôleur ou FPGA.
- Oubli mesuré par mAP moyen ; les exemplaires (10 par classe) réintroduisent du stockage qui croît avec le nombre de classes (§6.5).
- Modèle de menace ou d'assurance : aucune garantie de non-régression sur les anciennes classes, alors que l'exemple d'application cite des missions de sauvetage.
- Comparaison à la seule référence « All Data » ; pas de comparaison à d'autres méthodes incrémentales pour détection.

## Pertinence pour la thèse

Moyenne. Donne un schéma d'apprentissage incrémental pour détecteur one-stage (distillation classification + boîtes + features) avec un usage embarqué (Jetson TX2), utile comme état de l'art de l'apprentissage continu pour la détection, axe de la base. Pour la thèse « IA embarquée sécuritaire certifiable », il illustre surtout le problème : un modèle qui évolue sur le terrain remet en cause toute qualification ; rien ici sur la vérification après mise à jour, ni sur un FPGA.

## Gaps identifiés

- Apprentissage incrémental de détecteurs (YOLO) sur FPGA : aucun résultat ici (GPU Jetson seulement).
- Garantie de non-régression / assurance d'un modèle mis à jour sur le terrain, en contexte certifiable.
- Mesure de coût énergétique de l'apprentissage incrémental embarqué (absente).

## Statut de lecture

Papier complet (texte extrait lu en entier). Tables 1, 2, 4, 5, 6, 7 : corps reconstruits automatiquement, chiffres à vérifier ; Table 4 en partie illisible, Figures sans légende. Déduit et non affirmé par les auteurs : la limite « non embarquable sur MCU/FPGA » du classifieur 11k, l'absence de garantie de non-régression, la pertinence pour la thèse, le rattachement à une venue via le préfixe DOI.
