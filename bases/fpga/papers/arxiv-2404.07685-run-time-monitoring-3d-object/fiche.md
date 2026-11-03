---
id: arxiv-2404.07685-run-time-monitoring-3d-object
fiche: done
date: 2026-11-03
---

# Run-time Monitoring of 3D Object Detection in Automated Driving Systems Using Early Layer Neural Activation Patterns

Hakan Yekta Yatbaz, Mehrdad Dianati, Konstantinos Koufos, Roger Woodman, 2024, arXiv preprint. https://arxiv.org/abs/2404.07685
Type : preprint non relu par les pairs (le texte n'affirme aucune publication ; OpenAlex indique CVPRW 2024, DOI 10.1109/cvprw63382.2024.00356 : non confirmé par le texte, donc `venue`/`doi`/`type` inchangés)

## Problème

Les détecteurs 3D sur LiDAR (PointPillars, CenterPoint) manquent des objets en conduite automatisée ; l'introspection (moniteur d'intégrité) existante cible surtout la détection 2D caméra et utilise les activations de la dernière couche du backbone (§1). Hypothèse : à cause de la parcimonie des nuages de points, ces activations finales sont insuffisantes pour détecter les erreurs 3D (§1, §3). Erreur = au moins un objet vérité terrain sans boîte prédite d'IoU > 0,7 (§4.4) ; le moniteur est donc un détecteur de faux négatifs par image.

## Méthode

Moniteur par image, classification binaire Error / No-Error (§3). Activations extraites du détecteur : sortie du « point cloud processor » (PPC, pseudo-image), couche intermédiaire du backbone SECOND (MLA, bloc 2 pour PointPillars, bloc 1 pour CenterPoint, 128 cartes) et dernière couche (LLA). Méthode proposée : mise en commun par pooling moyen adaptatif puis concaténation sur les canaux de PPC + MLA + LLA, injectée dans un ResNet18 suivi d'un réseau entièrement connecté (architecture de [36,38]) (§3, Fig. 2). Entraînement : SGD, focal loss (gamma 5) avec poids de classes, 200 époques, lr 0,01, batch 64 (§4.4). Comparaison à deux moniteurs 2D adaptés : statistiques globales (SF, [31]) et LLA seule ([36], équivalente à LLA car moins de 1 % d'activations non nulles) (§4.3). Détecteurs pré-entraînés OpenMMDet3D ; jeux KITTI et nuScenes (§4.1, §4.2).

## Plateforme et implémentation

Aucun FPGA : tout est mesuré sur Intel Core i9-10980XE et NVIDIA RTX 3090 (§4.4). Puissance : n/r. Code et modèles : non mentionnés comme publiés.

## Résultats

- Table 1 (AUROC, rappel par classe) : son corps est absent de l'extraction, les valeurs de précision ne sont pas lisibles ici. Le texte dit seulement (§4.6.1) : PPC et MLA surpassent LLA ; MLA a le meilleur AUROC sur nuScenes et le deuxième sur KITTI ; la méthode proposée est plus équilibrée sur nuScenes et tend à réduire le taux de faux négatifs sur KITTI ; SF a le plus faible AUROC et un rappel très bas de la classe négative.
- Table 2 (KITTI, moyenne de 1000 itérations, temps du moniteur seul, hors détecteur) : CPU / GPU en ms et GFLOPs : PPC 54,32 / 11,47 / 36,32 ; MLA 9,43 / 2,01 / 3,68 ; LLA 5,01 / 1,80 / 1,60 ; proposé 4,94 / 1,95 / 2,60 (chunk 2404.07685#022.0). Les auteurs disent le proposé « sous 2 ms » sur GPU (§4.6.3).
- Confiance (softmax, Fig. 3) : LLA très confiante sur KITTI mais avec de larges plages sur FP et FN ; le proposé reste modeste (jusqu'à 0,8 sur nuScenes) (§4.6.2).
- Pas de baseline sur FPGA, pas de comparaison à un moniteur de sortie (confiance du détecteur) ni à un autre moniteur 3D.
→ reportés dans `benchmarks.csv` : 8 lignes (4 méthodes × CPU / GPU, latence du moniteur, Table 2, `platform_class: server`). Pas de ligne de précision (Table 1 illisible). Les GFLOPs sont dans le libellé du modèle, pas dans `gops` (ce n'est pas un débit).

## Limites et critique

- Table 1 non extraite : le gain réel des couches précoces n'est pas chiffré ici ; à relire sur le PDF avant toute citation chiffrée.
- Les latences excluent le détecteur et le calcul d'activations ; PPC est lent car haute résolution (Table 2 : 54 ms CPU), ce qui coûte précisément ce que la méthode proposée évite en réduisant la résolution (perte d'information reconnue, §3).
- Étiquette d'erreur = au moins un faux négatif à IoU 0,7 : criticité des objets, distance et classe ignorées ; les auteurs appellent eux-mêmes à définir de meilleures métriques d'erreur (§5).
- Pas d'évaluation sous décalage de domaine, attaques adverses ou OOD (annoncé comme travail futur, §4.6.2, §5). Un seul détecteur/jeu par expérience, pas de variance entre graines rapportée (déduit : non mentionnée).
- Cible serveur GPU/CPU : rien sur la quantification, le temps réel déterministe ni l'embarquement ; le gain est un classeur ResNet18 supplémentaire (poids et latence à ajouter au budget).

## Pertinence pour la thèse

Axe `failure-prediction` : moniteur appris dont la cible est le faux négatif, comme le visent les questions ARCYS (prédiction d'échec centrée sur le manque critique, moniteur appris avec le détecteur). Cité par KGFP (arxiv-2603.25499, §2) comme exemple de moniteur de couches précoces sur détecteurs 3D ; KGFP, lui, travaille sur YOLOv8 en 2D et ajoute un modèle de fondation. Argument utile : les représentations intermédiaires renseignent mieux sur les manques que la dernière couche, ce qui motive un moniteur branché tôt (et donc des sorties anticipées comme signalement). Reste ouvert : transposition à YOLO caméra, au FPGA (le coût de lecture et de pooling des cartes d'activation dans la fabric), au temps réel déterministe et à la certification du moniteur lui-même.

## Gaps identifiés

- Moniteurs d'erreur de détection sur activations précoces implémentés sur FPGA : aucun exemple ici, coût mémoire/bande passante de l'export des activations non étudié.
- Définition d'erreur pondérée par la criticité (personne vs véhicule, distance) absente.
- Performance du moniteur sous décalage de domaine, quantification ou fautes matérielles non évaluée.

## Statut de lecture

papier complet (fulltext.md lu en entier ; extraction GROBID ok). Table 1 absente de l'extraction ; Table 2 lue dans le texte reconstruit (ligne PPC mal séparée, valeurs recoupées avec le texte sur l'ordre PPC > MLA > LLA : confiance `medium`).
Ce qui suit est déduit et non affirmé par les auteurs : absence de publication du code, absence de variance entre graines, transposition possible à YOLO et au FPGA, lien avec les sorties anticipées.
