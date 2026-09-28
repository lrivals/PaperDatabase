---
id: 2025-du-f-yolov7-fast-robust-real
fiche: done
date: 2026-09-28
---

# F-yolov7: fast and robust real-time UAV detection

Yan Du, Teng Wu, Zifeng Dai, Hui Xie, Changzhen Hu, Shengjun Wei, 2025, Computing 107(1), 50. https://doi.org/10.1007/s00607-024-01406-7
Type : article de journal

## Problème

Détecter en temps réel des drones « low, slow and small » dans des images haute résolution
prises par une **caméra fixe** (§1). Les auteurs invoquent les limites du radar (clutter
au sol) et de la détection RF (interférences), puis celles de YOLOv7 : nombre de
paramètres, temps d'entraînement, précision sur petits objets (§1). Le cadre est donc la
surveillance **sol → air**.

## Méthode

- **Prétraitement par soustraction de fond** (§4.4) : modèle de fond = moyenne, ou
  médiane selon le texte, de N images au fond similaire (Éq. 4) ; différence en niveaux de
  gris, binarisation à un seuil fixé expérimentalement (valeur n/r), ouverture (noyau 18)
  puis fermeture (noyau 3), puis recadrage d'une zone de deux fois la taille estimée du
  drone. Suppose une caméra immobile.
- **Faster module** à la place des ELAN et ELAN-H de YOLOv7 (§4.1-4.2) : convolution
  partielle (PConv, empruntée à FasterNet [14]) sur une partie des canaux, deux 1×1, BN+ReLU
  après la première seulement, branche DWConv parallèle, concaténation.
- **FIoU** : remplace l'arctan du terme d'aspect v de la CIoU par une sigmoïde 1/(1+e^-x)
  (§4.3, Éq. 3).
- Entraînement avec les « Trainable Bag-of-Freebies », mosaic, mixup, cutout ; l'inférence
  est dite optimisée « via TensorRT » (§5.3), sans dire si les débits de la Table 2 sont
  mesurés avec TensorRT. Précision numérique d'inférence : n/r.

## Plateforme et implémentation

- PyTorch 1.10, CUDA 11.3, Xeon Platinum 8362 (14 vCPU) et **NVIDIA RTX 4090 24 Go**
  (§5). Tous les débits sont des « throughput on GPU » sur la 4090 (§5.2).
- Aucune plateforme embarquée. Puissance, batch, résolution d'entrée : n/r.
- Code : non publié (aucun lien dans le texte).

## Résultats

Ablation sur DUT Anti-UAV (Table 2) :

| Modèle | Param. (M) | GFLOPs | FPS (4090) | AP50 val | AP75 val | AP50 test | AP75 test |
|---|---|---|---|---|---|---|---|
| YOLOv7 | 19,6 | 105,1 | 167 | 86,71 | 71,93 | 85,95 | 71,03 |
| YOLOv7-FIoU | 20,4 | 105,1 | 167 | 87,93 | 73,86 | 86,99 | 72,70 |
| YOLOv7-Faster | 23,7 | 38,0 | 164 | 90,25 | 79,63 | 90,15 | 78,89 |
| F-YOLOv7 | 24,4 | 38,0 | 169 | 92,80 | 82,69 | 91,63 | 81,76 |
| Pre-F-YOLOv7 | 31,20 | 38,0 | 159 | 98,80 | 87,63 | 97,94 | 86,57 |

- La « detection accuracy of 98.8% » de l'Abstract est l'AP50 de validation de
  Pre-F-YOLOv7 (Table 2).
- La comparaison avec l'état de l'art (Table 1) n'a **pas de corps extrait** : aucun
  chiffre des détecteurs concurrents n'est disponible.

→ reportés dans `benchmarks.csv` (fichier du lot) : 2 lignes, F-YOLOv7 et Pre-F-YOLOv7
(Table 2, RTX 4090, AP50 val).

## Limites et critique

- **Hors périmètre embarqué** : caméra fixe au sol, soustraction de fond qui suppose un
  fond immobile, mesures sur RTX 4090. Rien n'est transposable tel quel à un détecteur
  **air → air** sur drone intercepteur, où le fond bouge avec l'ego-mouvement (déduit).
- **Incohérences internes de la Table 2** :
  - le Faster module est présenté comme réduisant les paramètres (§4.1), or le nombre de
    paramètres **augmente** (19,6 → 23,7 → 24,4 M) ; seuls les FLOPs baissent (105,1 → 38,0) ;
  - la soustraction de fond, sans paramètres appris, fait passer le modèle de 24,4 à
    31,20 M paramètres, sans explication ;
  - la ligne « Improvement » (+7,02 ; +14,96 ; +6,61 ; +15,11) ne correspond pas aux
    écarts F-YOLOv7 − YOLOv7 de la table (+6,09 ; +10,76 ; +5,68 ; +10,73, calculés ici) ;
  - FLOPs divisés par 2,8 pour un débit quasi inchangé (167 → 169 FPS) : le débit n'est pas
    limité par le calcul sur 4090, ou la mesure est dominée par autre chose (déduit).
- **Coût du prétraitement mal isolé** : on ne sait pas si les 159 FPS de Pre-F-YOLOv7
  incluent la soustraction de fond, le calcul du modèle de fond sur N images, ni le
  recadrage. Le gain de 6 points d'AP50 peut venir du recadrage, qui agrandit le drone
  (déduit).
- **Détails manquants** : seuil de binarisation, N, résolution, batch, split exact,
  nombre de runs. Le texte hésite entre médiane et moyenne pour le modèle de fond (§4.4).
- La FIoU est justifiée par des arguments qualitatifs, sans courbe de convergence
  chiffrée dans le texte extrait. Pas de code.

## Pertinence pour la thèse

- **Faible, et hors périmètre selon `profile.md`** : contre-drone **sol → air** (caméra
  fixe) mesuré sur GPU de bureau, donc double exclusion (sol → air ; GPU de bureau).
  Classé `counter-uav` pour le repérage, avec le tag `ground-to-air`.
- Intérêt résiduel : les chiffres de DUT Anti-UAV (AP50 ~87 % pour YOLOv7) donnent un
  point de repère pour ce jeu. Le couple PConv/DWConv est aussi un exemple de réduction de
  FLOPs sans gain de débit sur GPU, argument pour des mesures sur la vraie cible
  embarquée.

## Gaps identifiés

- **La réduction de FLOPs ne se traduit pas en débit** (Table 2) : les papiers YOLO
  « légers » pour drone mesurent sur GPU de bureau, où le gain est invisible. Mesure sur
  Jetson, FPGA ou MCU à faire.
- **Soustraction de fond inapplicable en air → air** : pas de solution évaluée ici pour
  une caméra embarquée en mouvement.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). La Table 1
(comparaison avec l'état de l'art) n'a pas de corps extrait : le contenu affiché sous sa
légende est celui de la Fig. 3. Les équations (1)-(4) sont partiellement illisibles.
La conclusion est tronquée au milieu d'une phrase (« greatly reduce In future
research… »).

Ce qui suit est déduit et non affirmé par les auteurs :
- les écarts recalculés de la ligne « Improvement » ;
- l'origine possible du gain de Pre-F-YOLOv7 (recadrage) et le débit non limité par le
  calcul ;
- l'inapplicabilité de la méthode en air → air.
