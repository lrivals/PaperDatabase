---
id: 2022-jung-improved-yolov5-efficient-object-detection
fiche: done
date: 2026-09-28
---

# Improved YOLOv5: Efficient Object Detection Using Drone Images under Various Conditions

Hyun-Ki Jung, Gi-Sang Choi, 2022, Applied Sciences 12(14), 7255. https://doi.org/10.3390/app12147255
Type : article de journal

## Problème

Détecter personnes et objets depuis un drone dans des conditions difficiles (pluie, neige,
nuit, altitude variable), par exemple pour la recherche de disparus après une catastrophe
(§1). Les auteurs constatent que la détection par drone est très sensible aux conditions
environnantes et que la littérature sur le sujet est encore mince (§1).

## Méthode

- **Modèle** : YOLOv5s, dans sa version récente (Conv 6 × 6 à la place de Focus, SPPF)
  (§2.1).
- **Seule modification** : l'activation SiLU de tous les blocs Conv (dans C3, SPPF, backbone
  et tête) est remplacée par **ELU** (« ConvELU », §2.1, Fig. 3-7). Même perte CIoU pour les
  deux modèles (§3.3).
- **Données** : images propres prises avec un drone grand public F11 4K PRO (montagne, ville ;
  classes person, car, notice), plus un sous-ensemble VisDrone limité aux prises de vue
  au-dessus de 10 m. Au total 3360 images, équilibrées sur 8 conditions (clair, nuageux,
  pluie, neige, soir, nuit, basse altitude < 10 m, haute altitude > 10 m) : 2080 en
  entraînement, 960 en validation et 320 en test (§2.2, Table 1). Étiquetage avec
  makesense.ai.
- **Entraînement** : 100 époques sur Google Colab, environ 2 h par modèle, sans poids
  pré-entraînés COCO pour la comparaison « à conditions égales » (§3.1, §3.4).

## Plateforme et implémentation

- Entraînement et évaluation sur **Google Colab**. Modèle de GPU : n/r (§3.1).
- Aucune mesure de vitesse, de latence ou de puissance : FPS n/r, puissance n/r. Aucune
  cible embarquée.
- Gamme de puissance : non applicable (aucune inférence embarquée).
- Code et jeu de données : non publiés selon le texte extrait.

## Résultats

- **YOLOv5s d'origine contre YOLOv5_Ours (Table 2)** : précision 90,1 → 90,7 ; rappel
  89,8 → **87,4** (baisse) ; F1 89,9 → 89,0 (baisse) ; **mAP@0.5 94,6 → 95,5** (+0,9 point).
- **Par classe (Table 3, YOLOv5_Ours)** : person 97,3 ; car 96,2 ; notice 93,0 de mAP@0.5.
- **Par condition (§3.4, Fig. 13)** : plus de 87 % environ par temps clair et le soir,
  environ 57 % par temps de pluie. La métrique exacte (confiance des détections affichées ?)
  n'est pas précisée.
- **Autres YOLO (Table 4, mAP@0.5)** : YOLOv3 93,9 ; YOLOv4 91,0 ; YOLOv5 94,6 ;
  YOLOv5_Ours 95,5.
- **Perte** : YOLOv5_Ours converge plus lentement au début de l'entraînement, et les courbes
  se rejoignent vers l'époque 60 (§3.4, Fig. 14). Les auteurs présentent cette convergence
  plus lente comme une qualité (« efficient model with low convergence speed »).

→ reportés dans `benchmarks.csv` : 2 lignes (YOLOv5s d'origine et YOLOv5_Ours, mAP@0.5 sur
le jeu propre ; FPS et puissance n/r ; plateforme Google Colab non précisée ; Tables 2-3,
confidence high).

## Limites et critique

- **Gain marginal, dans le bruit (déduit)** : +0,9 point de mAP, sur un seul entraînement
  par modèle et un petit jeu de 320 images de test, avec une baisse du rappel et du F1. Pas
  d'écart-type ni de répétition.
- **Évaluation vraisemblablement sur la validation** : les chiffres sont décrits comme
  « validation precision score… mAP score is 95.5% » (§3.4). Le jeu de test sert à des
  prédictions qualitatives (Fig. 13). Le choix du meilleur modèle et le rapport se font donc
  sur le même jeu.
- **Justification de l'ELU erronée** : l'affirmation que SiLU « can only be used in
  reinforcement learning-based systems » (§2.1) est fausse (SiLU est l'activation par défaut
  de YOLOv5). Aucune ablation ELU / ReLU / LeakyReLU.
- **Aucune métrique d'efficacité** alors que le titre dit « Efficient » : pas de FPS, de
  FLOPs, de paramètres ni de latence. Or l'ELU (exponentielle) est plus coûteuse à
  implémenter sur FPGA ou MCU que ReLU ou LeakyReLU (déduit).
- **Métriques non comparables à la littérature VisDrone** : classes propres (dont
  « notice »), mélange de données propres et d'un sous-ensemble VisDrone, mAP@0.5 seul, pas de
  mAP_small.
- Texte très dupliqué et de rédaction approximative ; comparaison sans pré-entraînement COCO
  qui pénalise peut-être YOLOv3/YOLOv4 différemment (non discuté).

## Pertinence pour la thèse

- **Faible.** Axe `drone-detection`, mais sans aucune dimension embarquée ni mesure
  d'efficacité, et sur une modification (activation) de faible portée.
- **Un point à retenir (déduit)** : le choix de l'activation a un coût matériel. SiLU et ELU
  demandent des LUT ou approximations sur FPGA, contrairement à ReLU. Les papiers « YOLO
  amélioré » l'ignorent, et ce papier en est un exemple.
- Le découpage par conditions (pluie, neige, nuit, altitude) est une idée de protocole
  d'évaluation de robustesse à reprendre, sur un jeu public.

## Gaps identifiés

- **Robustesse aux conditions (météo, nuit) des détecteurs embarqués** : ici seulement sur
  un jeu minuscule et fermé, sans cible embarquée. Aucun lien entre condition, précision et
  coût.
- **Coût matériel des activations** (SiLU, ELU vs ReLU) dans les YOLO drone portés sur FPGA :
  non traité.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`, mais texte très
dupliqué par morceaux et parasité par « FOR PEER REVIEW »). La Table 4, signalée « sans
corps » dans `extraction.warnings`, est en fait présente (deux fois) ; les Tables 1 à 3 sont
complètes. Les Figures 11 à 15 ne sont connues que par le texte.

Ce qui suit est déduit et non affirmé par les auteurs :
- le fait que le gain soit dans le bruit statistique ;
- l'évaluation sur le jeu de validation (lecture de la formulation du §3.4) ;
- le coût matériel de l'ELU sur FPGA ou MCU.
