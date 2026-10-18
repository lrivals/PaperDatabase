---
id: arxiv-2211.13993-combating-noisy-labels-object-detection
fiche: done
date: 2026-10-18
---

# Combating noisy labels in object detection datasets

Krystian Chachuła, Jakub Łyskawa, Bartłomiej Olber, Piotr Frątczak, Adam Popowicz, Krystian Radlak, 2022, arXiv preprint. https://arxiv.org/abs/2211.13993
Type : preprint non relu par les pairs

## Problème

Les méthodes existantes contre le bruit de labels en détection (pondération, co-teaching, correction automatique) rendent l'entraînement tolérant au bruit mais ne disent pas quelles annotations sont fausses ni quelle fraction du dataset l'est (§II). Les auteurs veulent un outil qui évalue chaque boîte d'un dataset de détection, repère les erreurs et propose une correction, pour les relire puis les corriger « à la racine » (Résumé, §I). Motivation annexe : les normes de sécurité (ISO/DIS 21448, ISO/TR 4804, UL 4600) exigent un contrôle de la qualité des labels sans protocole de relecture standard (§I).

## Méthode

CLOD (Confident Learning for Object Detection), indépendant du modèle (§I, §IV).
- Un détecteur produit des prédictions hors échantillon (validation croisée implicite : « out-of-sample ») sur le dataset bruité (§IV).
- Boîtes d'origine et prédites sont regroupées par image avec un clustering agglomératif à lien simple, distance 1 - IoU, seuil de distance par défaut 0,5 (meilleurs seuils testés : 0,4, 0,5, 0,6) (§IV, §V-E, Fig. 7).
- Chaque cluster donne une ligne de matrice de labels binaires Y' et de probabilités P' (score max des prédictions par classe, plus une classe « fond ») (§IV, Alg. 1).
- Les lignes passent dans le confident learning multi-label : score d'auto-confiance s = y·p + (1-y)(1-p), agrégé par moyenne mobile exponentielle avec alpha = 0,8, ce qui pondère surtout les plus faibles scores (§III, Éq. 1-2). Chaque annotation reçoit un score de qualité ; sélection par rank-and-prune (la fraction de plus bas scores) (§III, §IV).
- Type d'erreur déduit du cluster (§IV) : prédictions seules = boîte manquante ; annotation seule = boîte parasite (spurious) ; labels différents = mal étiquetée ; même label = mal localisée. Les prédictions du cluster servent de correction proposée.

## Plateforme et implémentation

Serveur AMD EPYC 7313, RTX A5000, 60 Go RAM, MMDetection 2.28.2, PyTorch 1.12.1 (§V-D). Détecteurs : Faster R-CNN, RetinaNet, YOLO (paramètres Table II ; YOLO 273 époques, entrée non précisée pour la partie cleaning). Datasets : COCO 2017 (123 287 images, 886 284 instances), Sama-Coco (version relue, 1 115 464 instances), Waymo Open v1.4.0 réduit à 10 000 images frontales (230 479 instances) et une variante dont 12 % des images ont été relues à la main par les auteurs (§V-A, Table I). Code publié (GPL v3) : https://github.com/safednn-group/safednn-clean (§VII).

## Résultats

Bruit artificiel (COCO) : tout type de bruit dégrade le mAP50, de plus en plus avec la fraction bruitée. Ordre de nuisance : labels aléatoires (uniform) > boîtes parasites > boîtes manquantes > localisation et échelle (25 % des dimensions) (§V-E, Fig. 4). Retirer 5 % d'exemples bruités pourrait gagner jusqu'à 0,085 de mAP50, soit « 20 % » dans certains cas (§VI).

Détection du bruit : environ 80 % des boîtes perturbées retrouvées avec un taux de faux positifs < 0,1, sauf boîtes manquantes (il faut accepter 0,3 de FPR pour la même proportion) (§V-E, Fig. 6). Meilleur sur les boîtes parasites ; décalages et échelles faibles (25 %) indétectables (AUROC proche du hasard), ceux de 50 % aussi bien détectés que les autres (§V-E, §VI). Bruit artificiel appliqué à 20 % des exemples de validation pour cette mesure (§V-E). Comparaison à ObjectLab (AUROC, Table III) :

| Bruit | COCO CLOD / ObjectLab | Waymo CLOD / ObjectLab |
|---|---|---|
| label | 0,833 / 0,851 | 0,746 / 0,854 |
| location | 0,855 / 0,835 | 0,845 / 0,851 |
| scale | 0,850 / 0,822 | 0,825 / 0,828 |
| spurious | 0,897 / n/a | 0,967 / n/a |
| missing | 0,710 / 0,524 | 0,705 / 0,564 |

ObjectLab ne traite pas les boîtes parasites ; il est meilleur sur les labels échangés (Waymo, +14 %), CLOD meilleur d'environ 30 % sur les manquantes (§V-E, §VI). Temps : CLOD 39,61 s contre 42,29 s (COCO) et 15,44 s contre 37,68 s (Waymo), mais environ 2 fois plus de mémoire (§VI).

Gain après correction (Faster R-CNN, Table V ; évalué sur la variante correspondante de la validation, les deux splits étant corrigés) : « Suggest. » = dataset d'origine avec les 20 % meilleures suggestions CLOD appliquées, appariées à la version relue par IoU >= 0,5 (§V-E) ; « Selected » = variante où seules sont gardées les bonnes modifications humaines.

| Dataset | mAP | mAP50 | mAP75 |
|---|---|---|---|
| COCO Original | 0,316 | 0,501 | 0,342 |
| COCO Revised (Sama-Coco) | 0,318 | 0,492 | 0,347 |
| COCO Suggest. | 0,366 | 0,610 | 0,379 |
| COCO Selected | 0,356 | 0,572 | 0,379 |
| Waymo Original | 0,310 | 0,548 | 0,316 |
| Waymo Revised | 0,237 | 0,415 | 0,242 |
| Waymo Suggest. | 0,452 | 0,774 | 0,471 |
| Waymo Selected | 0,315 | 0,554 | 0,316 |

Soit +16 % (COCO, 0,316 -> 0,366) et +46 % (Waymo, 0,310 -> 0,452) de mAP relatifs, chiffres du Résumé retrouvés dans la Table V. Par taille, COCO mAP_S : 0,181 (Original), 0,194 (Revised), 0,325 (Suggest.), 0,252 (Selected) (Table VI).

Erreurs trouvées dans les datasets publics (inspection manuelle des boîtes les plus suspectes, §V-E) : COCO, groupes d'objets (personnes, parapluies) dans une seule boîte ; photographies ou sculptures de personnes étiquetées `person` ; boîtes parasites ; objets flous annotés ; boîtes mal placées ou mal étiquetées (un objet ambigu étiqueté `truck`). Waymo, objets illisibles à cause de gouttes sur l'objectif, boîtes mal placées, boîtes sans objet, objets difficiles à classer. Proportion : 25 144 annotations COCO (2,8 % du dataset) à relire avec un seuil de qualité de 3,9 %, 878 annotations Waymo (0,4 %) sous le même seuil, seuil choisi au point où le nombre de boîtes sous-seuil augmente nettement (§V-E). Autres proportions citées d'autres travaux, non mesurées ici : jusqu'à 10 % d'erreurs en validation/test de datasets célèbres (§I), 0,15 à 10 % d'images mal étiquetées dans des datasets de classification (§II-D) ; Sama-Coco a ajouté plus de 200 000 annotations, soit 25 % de manquantes selon les auteurs de ce dernier, dont beaucoup de très petits objets (§V-A).

Coût de revue : CLOD traite environ 4 000 annotations/s et ~4 KiB par annotation (§V-E). Table VII : COCO 3 941 531 prédictions, 1 027,97 s, 16,95 GiB ; partial Waymo 621 403 prédictions, 61,75 s, 1,74 GiB. Revue humaine : seulement 2,8 % (COCO) et 0,4 % (Waymo) des annotations au seuil choisi ; le réviseur accepte ou rejette une suggestion, ce qui est dit moins long que réannoter (§VI, affirmé sans mesure de temps humain : n/r).

→ reportés dans `benchmarks.csv` : 8 lignes proposées (Table V, mAP Faster R-CNN, COCO et Waymo, 4 variantes chacun).

## Limites et critique

- Le gain « Suggest. » suppose que CLOD note parfaitement : les suggestions sont appariées à des boîtes de la version relue par des humains (IoU >= 0,5), donc ce n'est pas un nettoyage automatique de bout en bout (§V-E). Le chiffre est une borne haute, pas le résultat d'un pipeline réel.
- Le mAP est mesuré sur la validation corrigée de chaque variante : les scores ne sont pas comparables entre variantes. Les auteurs notent que Sama-Coco (+200 000 petites boîtes) ou Waymo revu rend la tâche plus dure (Revised 0,237 < Original 0,310) (§VI). Le jeu « Suggest. » COCO compte 4 085 931 instances (Table IV), plus de 4 fois l'original : le chiffre est mal expliqué (probablement toutes les prédictions de manquantes comptées), le résumé « 20 % » ne décrit donc pas bien le contenu. À vérifier (Table IV, lisibilité du tableau).
- Waymo « Selected » a exactement les comptes de « Revised » (229 426 instances, Table IV) : incohérence possible de reconstruction du tableau.
- Pas de précision/rappel mesurés sur les erreurs réelles de COCO/Waymo : la proportion d'erreurs vraies parmi les 2,8 % / 0,4 % signalés n'est pas rapportée (seulement des exemples choisis). Ni liste de classes les plus touchées.
- Le bruit de localisation/échelle de faible amplitude n'est pas détecté ; les boîtes manquantes sont les moins bien détectées (AUROC 0,71) (§V-E).
- Waymo : seulement 10 000 images frontales issues de séquences multi-capteurs ; les annotateurs voyaient plus que ces images, donc des « erreurs » trouvées peuvent ne pas en être (§VI).
- Seulement 3 médianes d'expériences (Fig. 5), pas d'écart-type. YOLO est cité sans version précise. Aucune évaluation sur un modèle de type YOLOv5-v8 d'Ultralytics ; l'entraînement avec bruit/correction est rapporté seulement avec Faster R-CNN dans Table V (déduit : texte et tableaux ne montrent que ce modèle).
- Preprint non relu ; code publié.

## Pertinence pour la thèse

(Pertinence pour la base yolo-data.) Mode d'emploi pour NETTOYER un dataset de détection avant d'entraîner un YOLO. À appliquer quand on récupère un dataset public ou externalisé de qualité inconnue, ou après un premier entraînement dont l'AP plafonne.
1. Entraîner un détecteur (n'importe lequel : le papier montre Faster R-CNN, RetinaNet, YOLO) avec des prédictions hors échantillon (K-fold) sur tout le dataset.
2. Lancer CLOD (code GPL v3) : agglomérer boîtes d'origine et prédites avec seuil 1 - IoU = 0,5, obtenir un score de qualité par boîte et un type d'erreur (manquante, parasite, mal étiquetée, mal placée).
3. Relire seulement les boîtes sous un seuil choisi au « coude » de la distribution des scores : 2,8 % (COCO) et 0,4 % (Waymo) des annotations à un seuil de 3,9 % (§V-E). Ordre de grandeur de la charge, pas une garantie de rappel.
4. Accepter ou rejeter la suggestion (la correction vient des prédictions), corriger train ET val.
5. Réentraîner. Gain attendu, borne haute : +16 % (COCO) à +46 % (Waymo) de mAP (Table V).
Enseignements pour ANNOTER : les erreurs dominantes sont des incohérences de consignes (groupes dans une boîte, images de personnes/statues, objets flous ou obstrués), donc écrire les règles correspondantes ; le bruit de labels de classe est le plus nocif à l'entraînement, puis les boîtes parasites et manquantes (Fig. 4). Les petits objets sont le point sensible (annoter ou non les très petits objets change le mAP). Limite pour YOLO : pas de test sur un YOLO moderne ; le détecteur d'estimation doit aussi être bon (déduit).

## Gaps identifiés

- Pas de mesure du temps de revue humaine (min/image) ni du coût comparé à une double annotation.
- Effet du nettoyage non mesuré sur YOLOv5/v8 ni sur petits objets en particulier.
- Précision réelle des suggestions sur les erreurs réelles de COCO/VOC/Objects365 non quantifiée.
- Comparaison avec la perte tolérante au bruit (sans nettoyage) non faite.

## Statut de lecture

papier complet (`fulltext.md` lu en entier ; extraction `grobid`). Les figures (Fig. 4 à 16) ne sont pas lisibles : leurs valeurs ne sont pas citées sauf quand le texte les donne (`n/r` sinon).
Ce qui suit est déduit et non affirmé par les auteurs : l'étape K-fold pour obtenir les prédictions hors échantillon (le texte dit seulement « out-of-sample »), l'explication des 4 M instances de COCO Suggest., le fait que « mAP » de Table V est l'AP COCO 0,5:0,95, l'absence de test sur un YOLO moderne, la comparaison à une revue manuelle plus longue (non mesurée).
