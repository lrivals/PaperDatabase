---
id: arxiv-2411.02582-real-time-detection-small-uavs
fiche: done
date: 2026-09-28
---

# Real-Time Detection for Small UAVs: Combining YOLO and Multi-frame Motion Analysis

Juanqin Liu, Leonardo Plotegher, Eloy Roura, Cristino De Souza Junior, Shaoming He, 2024, arXiv preprint. https://doi.org/10.1109/TAES.2025.3577592
Type : preprint non relu par les pairs (version arXiv lue). Le DOI enregistré pointe vers
une version IEEE Transactions on Aerospace and Electronic Systems (2025), non lue ici.

## Problème

Détecter des drones qui n'occupent qu'une infime fraction de l'image à longue distance
(« less than 0.1% of an image », §I), sur fond complexe. Les détecteurs mono-image (YOLO,
DETR) y ont des taux élevés de faux positifs et de faux négatifs ; les méthodes par
mouvement demandent un jeu de classification annoté difficile à construire (§I).

## Méthode

**GL-YOMO**, pipeline à deux modes (§III-A, Fig. 2) :
- **Global → local** : détection sur l'image 1920×1080 entière ; après N_g = 30 trames
  consécutives avec détection, passage à une ROI 300×300 ; retour au global après
  N_l = 60 trames sans détection (Table I, Algorithm 1). La ROI s'agrandit avec le nombre
  de trames perdues (R_size = 300 + k1·F_lost, Éq. 1).
- **YOLO Detector** : YOLOv5 (CSPDarknet53), entrée 640×640 en global comme en local,
  **4 têtes P3-P6** (une tête ajoutée), modules SSFF, TFE et CPAM repris d'ASF-YOLO, et
  C3 remplacés par C3Ghost (§III-B1, Fig. 3). À noter : la tête ajoutée est **P6**, pas
  P2.
- **Motion Detector**, sollicité quand la confiance YOLO est sous le seuil (τ_g = 0,3,
  τ_l = 0,1 ; Table I) : flux optique Lucas-Kanade pyramidal sur une fenêtre 50×50 autour
  de la position à t-2, compensation du mouvement caméra par transformation perspective,
  différence de trames t-2 / t, morphologie, composantes connexes (§III-B2a) ; template
  matching NCC multi-échelle (0,7 / 1,0 / 1,3) pondéré par la cohérence de déplacement
  (k2 = 0,6, k3 = 0,4 ; Éq. 2-10) ; validation par un filtre de Kalman à 8 états (IoU > 0
  entre prédiction et match, §III-B2c).

Pas de quantification, pas de pruning. Pas de NMS ou post-traitement décrit au-delà de
YOLOv5.

## Plateforme et implémentation

- Entraînement : 2 × NVIDIA RTX 3090, SGD, 200 époques, batch 64, entrée 640×640
  (§IV-B). La plateforme d'évaluation de la précision (Tables II-VI) n'est pas précisée :
  n/r.
- Embarqué : **NVIDIA Jetson Xavier NX**, TensorRT, 21,6 FPS en moyenne sur « the test
  video », modèle 640×640 (§IV-E). Précision de calcul (FP16 / INT8), mode de puissance
  et consommation : n/r. Gamme de puissance : Jetson (~10 W, déduit de la plateforme, non
  mesuré par les auteurs).
- Code et jeu Fixed-Wings : aucun lien de publication dans le texte extrait (non publiés
  à notre connaissance).

## Résultats

Comparaison sur Drone-vs-Bird (Table II, seuil IoU 0,1) : GL-YOMO P = 0,886, R = 0,809,
F1 = 0,846, AP = 0,763 ; RT-DETR AP = 0,773, YOLOv5s AP = 0,761.

Comparaison sur Fixed-Wings (jeu propre : 13 séquences, 24 951 trames 1920×1080, test de
4 673 trames, cibles de 1×1 à 146×95 px, 0,01 % de l'image en moyenne ; §IV-A) (Table III) :

| Méthode | P | R | F1 | AP |
|---|---|---|---|---|
| YOLOv5s | 0,640 | 0,405 | 0,496 | 0,382 |
| YOLOv8s | 0,663 | 0,177 | 0,280 | 0,207 |
| RT-DETR | 0,826 | 0,577 | 0,680 | 0,571 |
| GL-YOMO | 0,981 | 0,861 | 0,917 | 0,822 |

Ablation du YOLO Detector sur images globales (Table IV, jeu non précisé) : mAP50 = 0,794,
mAP50-95 = 0,433, 10,6 GFLOPs, « model size » 14,3M, contre YOLOv5s 0,768 / 0,423 /
15,8 GFLOPs / 14,4M. Tête supplémentaire : +4,4 % de rappel, +2,6 % de mAP (§IV-D1).
Sur images locales (Table V) : mAP50 = 0,880, mAP50-95 = 0,503.
Ablation du Motion Detector (Table VI, **corps absent de l'extraction**) : en global,
+5,7 % de rappel, +3,9 % de F1, +1,2 % d'AP ; en local, +3,2 % de rappel, +1,5 % de F1,
au prix d'une légère baisse de précision (§IV-D2).
Jetson Xavier NX + TensorRT : 21,6 FPS (§IV-E).

→ reportés dans `benchmarks.csv` : 5 lignes — GL-YOMO sur Drone-vs-Bird (Table II) et sur
Fixed-Wings (Table III) ; YOLO Detector images globales et locales (Tables IV-V) ;
GL-YOMO sur Jetson Xavier NX, 21,6 FPS (§IV-E, précision non associée).

## Limites et critique

- **Sur Drone-vs-Bird, l'AP de GL-YOMO (0,763) est inférieure à celle de RT-DETR (0,773)**
  et quasi égale à YOLOv5s (0,761) (Table II), alors que le texte affirme une supériorité
  « across multiple metrics ». Le gain n'est net que sur le jeu propre Fixed-Wings.
- **Seuil d'IoU de 0,1 à l'évaluation** (§IV-B) : très permissif, les AP ne se comparent
  pas aux mAP@0,5 habituels (VisDrone, etc.).
- **Baselines désavantagées** : YOLOv8s et YOLOv10s tombent à ~0,18 de rappel sur
  Fixed-Wings, ce qui suggère un réglage ou une résolution peu adaptés (déduit) ; aucune
  baseline ne bénéficie du mode local ni du détecteur de mouvement.
- **Vitesse non reliée à la précision** : le 21,6 FPS Jetson ne précise ni la précision
  numérique, ni la fréquence de déclenchement du Motion Detector (CPU ?), ni la puissance.
  Aucune latence par composant. Les chiffres de précision viennent vraisemblablement du
  GPU de bureau (déduit, plateforme n/r).
- **« Model size » ambigu** (14,3M : paramètres ou Mo ?) et incohérent : YOLOv5s-p passe
  à 25,0M pour +0,3 GFLOPs (Table IV).
- **Scénario non situé** : le papier ne dit pas si la caméra est au sol ou embarquée.
  Drone-vs-Bird mélange caméras statiques et mobiles (§IV-A) ; la compensation du
  mouvement caméra (§III-B2a) permet le cas embarqué, mais **aucune expérience air → air
  n'est revendiquée**. À classer par défaut comme contre-drone à capteur non précisé.
- Jeu Fixed-Wings et code non publiés : non reproductible. Mono-cible (le multi-UAV est
  renvoyé aux travaux futurs, §V).

## Pertinence pour la thèse

- Axe `counter-uav` : exemple de détection de **cibles de quelques pixels** combinant
  apparence (YOLO) et mouvement (flux optique + Kalman), avec un mécanisme ROI
  global/local qui réduit le calcul par trame une fois la cible accrochée — idée
  transposable à un détecteur embarqué contraint (FPGA / MCU).
- Point de mesure Jetson (21,6 FPS, Xavier NX) utile comme baseline de la gamme ~10 W,
  mais sans puissance ni précision associée.
- Laisse ouvert : portage matériel du pipeline hybride (DNN + flux optique + template
  matching), coût énergétique du mode local, validation air → air.

## Gaps identifiés

- **Pipelines hybrides DNN + mouvement sur accélérateur** : aucun chiffre de latence ou de
  puissance par étage (YOLO vs flux optique vs Kalman) ; pas de portage FPGA.
- **Évaluation contre-drone non standardisée** : seuil IoU 0,1, jeu privé, AP non
  comparable aux mAP@0,5 — confirme le besoin d'un protocole commun (petits objets,
  air → air).
- **Tête P6 plutôt que P2** pour des cibles de 1-146 px : choix non discuté, à comparer à
  l'hypothèse « tête P2 » de la base.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). Défauts
d'extraction : Table I reconstruite par PyMuPDF (valeurs de seuils recoupées avec le
texte) ; **Table VI (ablation du Motion Detector) sans corps** : seuls les gains cités dans
§IV-D2 sont connus ; un passage de §III-B est tronqué (« integrated the efficient Ghost
module [40] tem turns to the Motion Detector ») : la description de l'effet du Ghost module
et le début du Motion Detector manquent.

Ce qui suit est déduit et non affirmé par les auteurs :
- la gamme de puissance ~10 W de la Jetson Xavier NX ;
- le fait que les précisions des Tables II-VI soient mesurées sur GPU de bureau ;
- le réglage peu favorable des baselines YOLOv8s / YOLOv10s ;
- le caractère non établi du scénario air → air.
