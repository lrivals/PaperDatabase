---
id: arxiv-2409.16808-comprehensive-evaluation-deep-learning-object
fiche: done
date: 2026-09-24
---

# A Comprehensive Evaluation of Deep Learning Object Detection Models on Heterogeneous Edge Devices

Daghash K. Alqahtani, Muhammad Aamir Cheema, Maria A. Rodriguez, Adel N. Toosi, 2024, arXiv preprint. arXiv 2409.16808
Type : **preprint non relu par les pairs**. La version lue mentionne le RPi 5 AI HAT+ : c'est
probablement une révision postérieure à la v1 de 2024 (déduit).

## Problème

Selon les auteurs, les praticiens manquent de repères empiriques sur le compromis entre
précision, latence et énergie des détecteurs sur du matériel edge hétérogène. Les
benchmarks existants ignorent l'effet de la complexité de la scène (§I).

## Méthode

- **8 détecteurs :**
  - YOLOv8 n, s et m en 640×640, et en 320×320 sur Coral TPU (§III-B2) ;
  - EfficientDet Lite 0, 1 et 2 ;
  - SSD MobileNet V1 ;
  - SSDLite MobileDet.
- **9 plateformes :**
  - RPi 3, 4 et 5 sans accélérateur ;
  - RPi 3, 4 et 5 avec Coral USB (Edge TPU) ;
  - RPi 5 + AI HAT+ (Hailo-8) ;
  - Jetson Nano et Jetson Orin Nano (4 GB) (Table I).
- **Chaînes logicielles :** PyTorch et TFLite sur RPi, TFLite compilé Edge TPU sur Coral,
  HailoRT sur AI HAT+, **TensorRT** sur les Jetson (§III-B2).
- **Service :** Flask REST, sollicité par un client Locust à **un seul utilisateur**, donc
  une requête à la fois (batch 1 en pratique), pendant 5 minutes, répété 3 fois (§III-B3).
- **Mesures :**
  - latence côté serveur, de la réception de l'image à la réponse, hors réseau (§III-A1) ;
  - énergie par requête **hors repos**, E = (TE − BE) / N, en mWh, avec un wattmètre USB
    **UM25C** et un repos mesuré sur 5 minutes (§III-A2) ;
  - **mAP sur COCO val** (5000 images) avec FiftyOne (§III-A3) ;
  - analyse par nombre d'objets dans l'image (0, 1, 2, 3, 4 et plus) (§IV-H).

## Plateforme et implémentation

- Plateformes : voir la Table I. Mode de puissance des Jetson : n/r.
- **Précision numérique des moteurs TensorRT : n/r.** FP16 et INT8 sont annoncés en
  travaux futurs (§VI), ce qui suggère des modèles non quantifiés (déduit).
- Tailles de modèle TensorRT : YOLOv8n 14,2 Mo, YOLOv8m 105,3 Mo (Table I). Ce ratio est
  cohérent avec du FP32 ou du FP16 (déduit).
- Code : un environnement de benchmark « automated, service-based » est annoncé comme
  publié (§I), mais le lien n'est pas dans le texte extrait.

## Résultats

Valeurs explicites dans le texte (§IV) :

| Plateforme | Modèle | mAP COCO | Latence (ms) | Énergie (mWh/req., hors repos) |
|---|---|---|---|---|
| Orin Nano | YOLOv8n / s / m | 31 / 39 / 44 | 16 / n/r / 50 | 0,13 à 0,22 (fourchette) |
| Orin Nano | SSD V1 / SSDLite | 16 / 27 | 22 / 19 | 0,01 / 0,06 |
| Jetson Nano | YOLOv8n / s / m | 31 / 39 / 44 | de 104 à 509 (fourchette) | 0,28 à 1,07 (fourchette) |
| Jetson Nano | SSD V1 / SSDLite | 16 / 27 | 52 / 64 | 0,15 / 0,17 |
| RPi 5 + Hailo-8 | YOLOv8n / s / m | 32 / 40 / 44 | 76 / n/r / n/r (jusqu'à 240) | 0,20 à 0,36 (fourchette) |
| RPi 5 + Hailo-8 | SSD V1 / SSDLite | 17 / 27 | 89 / 92 | 0,21 / 0,23 |
| RPi (CPU) | YOLOv8n / s / m | ~30 / 39 / 44 | RPi 5 : de 316 à 1348 | RPi 5 : de 1,02 à 3,58 |
| RPi + Coral | YOLOv8n / s / m (320×320) | 16 / 25 / 32 | RPi 5 : de 21 à 97 | RPi 5 : de 0,47 à 0,62 |

- Énergie au repos (Fig. 2a) : Orin Nano **362 mWh** sur 5 min, la plus élevée de toutes
  les plateformes ; Jetson Nano 220 ; RPi 5 217.
- La précision décroît avec le nombre d'objets dans l'image. Pour 1 ou 2 objets, SSDLite
  approche YOLOv8m (§IV-H).

→ reportés dans `benchmarks.csv` : 15 lignes (Orin Nano, Jetson Nano, RPi 5 + Hailo-8 ;
YOLOv8 n, s et m, SSD V1, SSDLite), toutes en `confidence: medium` puisqu'elles viennent du
texte qui commente des figures.
- Les valeurs données seulement en fourchette sont en `n/r`.
- L'énergie par requête figure dans la colonne `model` quand elle est explicite, faute de
  colonne dédiée.
- `power_w` vaut `n/r` : l'énergie est donnée en mWh par requête, repos soustrait (ce qui
  correspondrait à une portée `board-dynamic`), jamais en watts.

## Limites et critique

- **Précision numérique non indiquée** pour TensorRT et Hailo. Ce n'est donc pas encore la
  baseline « Orin + TensorRT INT8 » recherchée. Les auteurs renvoient FP16 et INT8 à plus
  tard (§VI).
- **Les mAP sont identiques** entre Jetson Nano et Orin Nano (« exhibit the same accuracy
  results in our setup », §IV-C), et regroupées par catégorie de plateforme (Fig. 4). Il
  n'est pas établi que la mAP ait été mesurée **sur chaque carte** (déduit). Le chiffrage
  « IoU non précisée » vient de FiftyOne, dont le réglage par défaut n'est pas dit.
- **Biais de résolution :** YOLOv8 tourne en 320×320 sur Coral, ce qui explique en partie
  la chute de mAP et le gain de latence (les auteurs le signalent, Key Insight 2 et 3).
- **Latence de service :** elle inclut Flask, le décodage et la réponse, mais pas le
  réseau. C'est plus réaliste qu'une inférence seule, mais pas comparable à un temps de
  kernel.
- **Énergie :** l'UM25C mesure l'alimentation USB de la carte. Le repos soustrait donne une
  énergie dynamique ; c'est une bonne pratique, mais l'Orin Nano a un repos élevé (Fig. 2a)
  qui pèse en usage réel, à faible charge.
- **Valeurs par modèle en figures seulement :** le texte n'en donne souvent que la
  fourchette.
- **Pas de FPGA** dans le banc de test.

## Pertinence pour la thèse

- **Seule source du corpus avec une mAP COCO val sur Jetson Orin Nano et sur un NPU
  (Hailo-8)**, mesurées dans un même protocole avec énergie hors repos. Ordres de
  grandeur :
  - YOLOv8n : mAP 31, 16 ms sur Orin Nano ;
  - YOLOv8n : mAP 32, 76 ms sur Hailo-8.
- **Protocole réutilisable :** repos mesuré puis soustrait, énergie par requête, client à
  une requête à la fois, trois répétitions. Il est proche de ce que prévoit
  docs/experiences/kv260-map-sur-cible.md §5, et il y manque seulement la télémétrie de la
  puce.
- **Idée pour la thèse (déduite) :** l'analyse par nombre d'objets va vers une sélection
  dynamique du modèle selon la scène, ce qu'un FPGA reconfigurable pourrait exploiter
  (Zhai et al. basculent déjà entre YOLOv3 et tiny selon le trafic).

## Gaps identifiés

- **Baseline Jetson :** progrès. On a désormais la mAP COCO et l'énergie hors repos sur
  Orin Nano. Il manque toujours la précision numérique déclarée (INT8), la puissance en W
  et la portée de mesure au niveau de la puce.
- **Précision sur cible :** incertain ici, puisque la mAP est identique entre Nano et Orin.
- **NPU edge (Hailo-8) :** premier point dans le corpus. À intégrer à la passerelle MCU ↔
  FPGA ↔ NPU.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). La Fig. 2 est
partiellement présente dans l'extraction, sous forme de valeurs brutes. Je n'ai utilisé que
les valeurs affirmées dans le texte.

Ce qui suit est déduit et non affirmé par les auteurs :
- l'absence de quantification des moteurs ;
- le caractère postérieur de cette version ;
- le doute sur le lieu de mesure de la mAP ;
- la portée `board-dynamic` ;
- le lien avec la reconfiguration FPGA.
