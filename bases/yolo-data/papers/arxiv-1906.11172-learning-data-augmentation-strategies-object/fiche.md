---
id: arxiv-1906.11172-learning-data-augmentation-strategies-object
fiche: done
date: 2026-10-05
---

# Learning Data Augmentation Strategies for Object Detection

Barret Zoph, Ekin D Cubuk, Golnaz Ghiasi, Tsung-Yi Lin, Jonathon Shlens, Quoc V Le, 2019, arXiv preprint. https://arxiv.org/abs/1906.11172
Type : preprint non relu par les pairs

## Problème

L'augmentation est bien étudiée en classification, pas en détection, alors que l'annotation de boîtes coûte plus cher et que les jeux de détection sont plus petits (§1). Deux questions : les augmentations de classification se réutilisent-elles telles quelles, et que faire des boîtes et de leur contenu (§1) ? Les auteurs cherchent une politique d'augmentation spécifique à la détection, transférable entre jeux, tailles de jeu et architectures (§1).

## Méthode

- Espace de recherche à la AutoAugment : une politique = K = 5 sous-politiques, chacune de N = 2 opérations enchaînées, avec une probabilité et une magnitude discrétisées (L = M = 6) ; espace d'environ 9,6e28 politiques (§3).
- 22 opérations en trois familles (§3) : **couleur** (Equalize, Contrast, Brightness… : les boîtes ne bougent pas) ; **géométriques sur l'image entière** (Rotate, ShearX, TranslateY… : les boîtes sont recalculées pour rester cohérentes) ; **opérations « bbox only »** (BBox Only Equalize / Rotate / FlipLR / TranslateY / ShearY… : seul le contenu des boîtes est déformé).
- Recherche : contrôleur RNN entraîné par PPO sur 20K politiques, modèle enfant RetinaNet ResNet-50 entraîné de zéro sur seulement **5K images COCO**, récompense = mAP sur 7392 images tenues de côté ; coût : 400 TPU pendant 48 h (§3). La politique trouvée sert ensuite telle quelle partout (§4).
- Politique de base à comparer : flip horizontal (p = 0,5) + multi-scale jittering 512-786 recadré à 640x640 (§4.2).

## Plateforme et implémentation

Entraînement sur TPU ; pas de mesure d'inférence ni de puissance (l'augmentation n'agit qu'à l'entraînement, modèle inchangé à l'évaluation, résumé). Implémentation TensorFlow ; opérations détaillées en annexe (non reprise dans `fulltext.md`) ; la politique complète est en Table 7 de l'annexe (non lue). Code d'entraînement avec la politique : « disponible en ligne » (note de bas de page du résumé, lien non repris dans le texte extrait).

## Résultats

**Opérations qui ressortent de la politique** (§4.1) : l'opération la plus fréquente dans les bonnes politiques est **Rotate sur l'image entière** (les boîtes grossissent pour englober l'objet tourné, et ça aide quand même) ; viennent ensuite **Equalize** (image entière, sans effet sur les boîtes) et **BBox Only TranslateY** (déplacement vertical des seuls objets). Les sous-politiques illustrées (Fig. 2) mêlent Color, Rotate, BBox Only ShearY, SolarizeAdd, Brightness, ShearY, BBox Only Equalize, TranslateX.

**Ablation par famille d'opérations** (RetinaNet ResNet-50, COCO complet, Table 2, §4.2) : baseline 36,7 mAP → couleur seule 37,5 (+0,8) → + géométriques 38,6 (+1,9) → + bbox-only 39,0 (+2,3). Les opérations bbox-only apportent donc +0,4 mAP en plus ; l'essentiel du gain vient de la géométrie sur l'image entière. DropBlock seul : 38,4 (+1,7) (Table 2).

**Gain selon l'architecture** (RetinaNet, COCO, Table 1) : ResNet-50 36,7 → 39,0 (+2,3) ; ResNet-101 38,8 → 40,4 (+1,6) ; ResNet-200 39,9 → 42,1 (+2,2). Entraînement de zéro, 640x640, 150 époques (§4.2).

**État de l'art** (§4.3) : NAS-FPN + AmoebaNet-D (préentraîné ImageNet, 1280x1280) : +1,5 mAP avec la politique (valeur absolue : Table 3, corps non extrait → `n/r`) ; avec 1536x1536, ancres 3x3 → 9x9 et 20 sous-politiques (top 4 de la recherche fusionnés) : **50,7 mAP** COCO en un seul passage, un seul modèle (§4.3).

**Transfert à un autre jeu et un autre détecteur** (§4.4, Table 4) : Faster R-CNN ResNet-101 sur VOC07+12 (test VOC07, mAP50), départ d'un checkpoint COCO, politique COCO ajoutée au prétraitement sans toucher aux hyperparamètres : 76,0 → 78,7 mAP50 (+2,7) ; gain sur presque chaque classe (plant 50,7 → 55,2 ; chair 55,5 → 58,5 ; tv 73,0 → 76,6 selon le tableau reconstruit, à vérifier). La moyenne de base (76,0) vient d'un corps de tableau illisible : à vérifier.

**Gain selon la taille du jeu d'entraînement** (RetinaNet ResNet-50 de zéro, sous-ensembles de COCO, Table 5, §4.5) :

| Images | mAP base → politique | mAP_S base → politique | mAP_M | mAP_L |
|---|---|---|---|---|
| 5 000 | 6,5 → 8,7 | 1,9 → 3,2 | 7,1 → 9,8 | 9,7 → 12,7 |
| 9 000 | 11,8 → 15,1 | 4,3 → 7,1 | 12,3 → 16,8 | 17,6 → 22,3 |
| 14 000 | 16,4 → 19,9 | 6,8 → 9,5 | 17,5 → 22,1 | 23,9 → 29,8 |
| 23 000 | 22,6 → 25,3 | 10,0 → 11,9 | 24,3 → 27,8 | 33,3 → 36,8 |
| 118 000 (COCO) | 36,7 → 39,0 | n/r | n/r | n/r |

Les auteurs : le gain relatif est le plus fort sur les petits jeux (« plus de 70 % » à 5K, §4.5) et décroît quand le jeu grossit, tout en restant significatif ; gain absolu de 2,2 à 3,5 mAP sur les sous-ensembles, soit +34 % relatif à 5K d'après Table 5 (le « plus de 70 % » du texte ne se retrouve que sur mAP_S, 1,9 → 3,2 = +68 % ; voir Limites).

**Petits objets** (§4.5, Table 5, Fig. 3) : le gain relatif est plus fort sur les petits objets, surtout quand il y a peu d'images. Avec 9K images + politique, mAP_S = 7,1, supérieur à la base à 14K (6,8) : la politique vaut plus que +50 % de données pour les petits objets, « presque autant que doubler le jeu » (formulation des auteurs, §4.5). Le gain est aussi relativement plus grand à AP75 qu'à AP50 pour toutes les tailles (Fig. 4, chiffres non lisibles dans le texte) : la politique aide à mieux caler les boîtes.

**Régularisation** (§4.6, Fig. 5-6) : la perte d'entraînement monte et la norme L2 des poids baisse avec la politique, pour toutes les tailles de jeu : effet de régularisation. Input MixUp, Manifold Mixup et DropBlock ne changent rien (ni gain ni perte) une fois la politique appliquée (§5).

→ reportés dans `benchmarks.csv` : 15 lignes proposées (Table 1 : 3 ; Table 2 : 2 ; §4.3 : 1 ; Table 4 : 1 ; Table 5 : 4 tailles x mAP et mAP_small = 8).

## Limites et critique

- **Coût de la recherche** : 400 TPU x 48 h ; inaccessible en pratique, d'où l'intérêt de réutiliser la politique publiée (§3). Les auteurs signalent des méthodes de recherche plus économes (§3).
- **Transfert prouvé sur peu de cas** : un seul autre jeu (VOC, avec départ d'un checkpoint COCO, donc proche du jeu de recherche) et des détecteurs à ancres (RetinaNet, NAS-FPN, Faster R-CNN). Rien sur des domaines éloignés (aérien, industriel, objets minuscules) ni sur des détecteurs YOLO ou sans ancres. À noter : la politique est cherchée sur 5K images COCO, ce qui est aussi la taille « petit jeu » la plus favorable.
- **Gains mesurés contre une baseline faible** : flip + jitter d'échelle, sans Mosaic, MixUp ni Copy-Paste (§4.2). Le gain sur un pipeline YOLO moderne déjà riche en augmentations est donc inconnu (déduit, non mesuré).
- **Peu d'isolation des opérations** : l'ablation se fait par famille, pas par opération ; l'apport d'une opération bbox-only précise n'est pas mesuré (Table 2). Le rôle de Rotate (« le plus fréquent ») est un constat de fréquence dans les politiques trouvées, pas une ablation.
- **Rotate agrandit les boîtes** (§4.1) : les boîtes deviennent moins serrées, ce qui peut dégrader la précision de localisation sur des objets très allongés ; les auteurs ne le mesurent pas à part.
- **Chiffres** : incohérence entre le texte (« plus de 70 % » relatif à 5K) et Table 5 (+34 % en mAP global, +68 % en mAP_S) ; Table 3 sans corps ; Table 4 et Table 2 reconstruits par PyMuPDF. Variance entre graines non rapportée (écarts de 1,6 à 2,3 mAP présentés sans intervalle).
- Mesure de la baseline VOC à vérifier (76,0).
- Preprint, jamais relu par les pairs (publié ensuite à ECCV 2020 : information externe au corpus, non vérifiée ici).

## Pertinence pour la thèse

**Construire / augmenter un dataset de détection (axe augmentation)** : c'est le papier de référence pour savoir **quand l'augmentation compte le plus**.

- **Peu de données** : plus le jeu est petit, plus la politique rapporte (relativement) : +2,2 mAP sur 5K images, +3,3 sur 9K, +3,5 sur 14K, +2,7 sur 23K, +2,3 sur COCO complet (Table 5, Table 1). Pour un dataset de quelques milliers d'images, une augmentation forte vaut presque un doublement du jeu sur les petits objets (§4.5) : à essayer avant de payer de l'annotation supplémentaire (§5).
- **Petits objets et boîtes précises** : le gain est le plus grand sur mAP_S (+1,3 à +2,8 selon la taille de jeu, Table 5) et à AP75 (Fig. 4) : à privilégier si la cible est de petits objets ou une localisation fine.
- **Quelles opérations** : géométrie sur l'image entière (rotation, cisaillement, translation) = l'essentiel du gain, après la couleur ; les opérations sur boîte seule ajoutent un complément modeste (+0,4 mAP) mais ressortent dans la politique (BBox Only TranslateY, Equalize, ShearY). Recette applicable : rotation + cisaillement + translation + égalisation d'histogramme + opérations sur le contenu des boîtes, avec recalcul des boîtes (boîtes agrandies après rotation).
- **Transfert** : une politique cherchée sur 5K images COCO se transfère telle quelle à COCO complet, à VOC et à d'autres backbones/détecteurs (Table 1, Table 4) : on n'a pas besoin de relancer la recherche, on réutilise la politique (le code l'expose) ; réserve : non testé sur YOLO ni hors images naturelles.
- **Ne pas empiler la régularisation** : MixUp / DropBlock n'ajoutent rien avec la politique (§5), à rapprocher des recettes Mosaic + MixUp des YOLO (à tester, non démontré ici).
- **Ouvert** : interaction avec Mosaic / Copy-Paste, effet sur un pipeline YOLO, jeux de domaine (drones, embarqué) ; recherche trop coûteuse pour un jeu spécifique.

## Gaps identifiés

- Aucune mesure de cette politique sur un détecteur YOLO / sans ancres avec Mosaic + MixUp déjà actifs.
- Pas de comparaison par opération (Rotate, bbox-only) ni de test sur images aériennes/drone ou objets très petits.
- Courbe « gain d'augmentation vs taille du jeu » mesurée uniquement avec RetinaNet de zéro, jusqu'à 23K images (sauf COCO complet).

## Statut de lecture

papier complet (fulltext.md lu en entier ; extraction GROBID). Annexe (détails des opérations, Table 7 de la politique complète) absente du texte extrait : non lue. Table 3 (corps non extrait) : valeur absolue de la ligne ResNet-50 vs NAS-FPN `n/r`, seul le +1,5 mAP et le 50,7 final du texte sont repris. Table 2 reconstruite par PyMuPDF (recoupée avec le texte : 37,5 / 38,6 / 39,0 / +0,8 / +1,9 / +2,3) ; Table 4 (corps à colonnes fusionnées, moyenne de base 76,0 déduite de 78,7 − 2,7) ; Table 5 (corps lisible mais signalé « sans corps extrait » dans les avertissements ; chiffres cohérents avec le texte). Figures 3-6 : légendes seules, valeurs non lues.
Déduit et non affirmé par les auteurs : la décomposition des gains absolus par taille de jeu (calculée depuis Table 5) ; l'importance relative des opérations sur boîte (+0,4 mAP) ; les conséquences pour un pipeline YOLO ; la publication ultérieure à ECCV.
