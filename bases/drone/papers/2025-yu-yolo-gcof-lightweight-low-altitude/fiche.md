---
id: 2025-yu-yolo-gcof-lightweight-low-altitude
fiche: done
date: 2026-09-28
---

# YOLO-GCOF: A Lightweight Low-Altitude Drone Detection Model

Wanjun Yu, Kongxin Mo, 2025, IEEE Access 13, 53053-53064. https://doi.org/10.1109/ACCESS.2025.3553477
Type : article de journal

## Problème

Détecter des drones de loisir volant à basse altitude au-dessus de zones interdites. Radar,
détection radio et acoustique sont coûteux ou inefficaces sur ces petites cibles lentes
(§I). Les auteurs veulent un détecteur visuel **léger, déployable sur un équipement
embarqué** de surveillance, sans perte de précision (§I, §II).

## Méthode

YOLOv8n modifié (§III, Fig. 1) :
- **GI-DGCST** à la place de C2f dans le backbone : deux branches, résiduelle d'un côté,
  sandwich GSConv → DGCST (Dynamic Group Convolution Shuffle Transformer, partition 3:1)
  → GSConvFFN de l'autre (§III-A, Fig. 2-3) ;
- **CSA-HSFPN** au neck : HSFPN (sélection puis fusion sélective des features) avec un
  module d'attention CSA (convolutions dilatées multi-échelles + Coordinate Attention)
  (§III-B, Fig. 4-6) ;
- **Detect-OGCH** : tête découplée partagée à convolutions groupées en « olive »
  (expansion, maintien, compression des canaux) (§III-C, Fig. 7) ;
- perte **Focaler-SIoU** à la place de CIoU (§III-D, Éq. 4-14).

Pas de quantification ni de pruning. Nombre de têtes de détection : celui de YOLOv8
(P3-P5), pas de tête P2 décrite.

## Plateforme et implémentation

- Entraînement et évaluation : NVIDIA A10 24 GB, Intel Xeon Platinum 8369B, PyTorch 2.3.1
  (§IV-A). Hyperparamètres dans la Table 1, **absente de l'extraction** : n/r.
- Déploiement : **Raspberry Pi 4B** (Cortex-A72 quad-core 1,5 GHz, 8 GB) (§IV-D8).
  Framework d'inférence, précision numérique, FPS, latence et puissance : **tous n/r** ;
  seule une comparaison qualitative d'images (Fig. 13) est donnée.
- Code : non publié (aucun lien dans le texte).

## Résultats

Chiffres lus dans le texte ; les Tables 1 à 9 n'ont pas de corps extrait.
- Jeu A&T (TIB-Net-drone complet + sous-ensemble filtré d'AUAVD, 5 010 images, split
  7:2:1 ; §IV-B) : mAP@50 = 92,6 %, mAP@50-95 = 59,5 % ; YOLOv7-t a un F1 supérieur
  (valeur n/r) (§IV-D7, Table 7).
- Coût : 1,2 M paramètres, 4,1 GFLOPs, 2,68 MB (§IV-D7, Table 8) ; par rapport à YOLOv8n :
  −60 % de paramètres, −49,4 % de GFLOPs, −55,1 % de taille, +1,1 point de mAP@50
  (Abstract, §V) ; −1,8 M paramètres et −4 GFLOPs, +1 % F1, +0,7 % mAP@50-95 (§IV-D5,
  Table 6).
- DUT-Anti-UAV : mAP@50 = 91,5 %, F1 = 89,4 % (2e derrière YOLO11n) (§IV-D7, Table 9).
- Ablations (§IV-D1 à D5) : GI-DGCST +1,5 point de mAP@50 et mAP@50-95 face à DGCST pour
  +0,2 GFLOPs ; chaque module apporte de 0,2 à 0,9 point.
- Raspberry Pi 4B : aucun chiffre (§IV-D8).

→ reportés dans `benchmarks.csv` : 2 lignes — YOLO-GCOF sur A&T (§IV-D7) et sur
DUT-Anti-UAV (§IV-D7), plateforme d'évaluation GPU A10, `confidence: medium` (chiffres lus
dans le texte, tableaux non extraits).

## Limites et critique

- **« Embarqué » sans aucune mesure** : le déploiement Raspberry Pi 4B n'a ni FPS, ni
  latence, ni puissance (§IV-D8). La légèreté n'est démontrée qu'en GFLOPs et paramètres,
  pas en temps réel sur la cible.
- **Scénario sol → air** : surveillance de zones interdites par un capteur
  optoélectronique (§I) ; les jeux TIB-Net, AUAVD et DUT-Anti-UAV sont vus depuis le sol
  (déduit du contexte, la position de la caméra n'est pas discutée). D'après le profil de
  la base, le contre-drone sol → air ne relève pas de l'IA embarquée : **hors du cœur du
  thème**, retenu seulement comme référence de détecteur léger.
- **Gains marginaux** (+1,1 point de mAP@50) sur un jeu composite propre (A&T), sans
  intervalle de confiance ni répétition ; le split du jeu DUT-Anti-UAV n'est pas précisé.
- **Pas de mAP par taille d'objet** (mAP_small) alors que le papier cible les petites
  cibles.
- **Incohérences d'appellation** : « YOLOv8-GCOF » et « YOLO-GCOF » alternent ; en §IV-D7,
  « YOLOv8-GCOF placed third with a mAP@50-95 of 61.2% » sur DUT-Anti-UAV : à vérifier
  dans la Table 9 (non extraite).
- Baselines : versions nano/tiny des YOLO (v5n à 11n), entraînées par les auteurs ; pas de
  comparaison avec des détecteurs dédiés petits objets ni avec un Jetson ou un MCU.

## Pertinence pour la thèse

- Faible pour le cœur de la base (IA embarquée à bord du drone) : contre-drone sol → air
  sur CPU ARM, sans mesure de performance.
- Utile comme catalogue de briques légères (GSConv, dynamic group conv, tête partagée à
  convolutions groupées, Focaler-SIoU) : GFLOPs divisés par ~2 par rapport à YOLOv8n sans
  perte de mAP@50, candidates pour un portage sur FPGA ou MCU — mais les convolutions
  groupées dynamiques et le bloc Transformer se prêtent mal aux accélérateurs à flot de
  données fixe (déduit).
- Point de comparaison chiffré sur DUT-Anti-UAV (91,5 % mAP@50).

## Gaps identifiés

- **Détecteurs « légers pour l'embarqué » évalués seulement en GFLOPs** : FPS, latence et
  puissance absents sur la cible annoncée (Raspberry Pi 4B). Confirme le gap « aucune
  métrique système ».
- **mAP_small non rapporté** dans un papier qui revendique la détection de petites
  cibles.
- **Contre-drone air → air** : non traité ; ce papier illustre la prédominance du
  scénario sol → air dans les détecteurs anti-UAV légers.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID `ok`). **Les Tables 1 à 9
n'ont pas de corps extrait** : hyperparamètres (Table 1), ablations détaillées (Tables 2-6),
comparaisons (Tables 7-9) ne sont connues que par les chiffres repris dans le texte. Les
équations de la perte SIoU (Éq. 5-10) sont partiellement illisibles.

Ce qui suit est déduit et non affirmé par les auteurs :
- le caractère sol → air des jeux de données et du scénario ;
- la difficulté de portage FPGA des convolutions groupées dynamiques et du Transformer ;
- l'absence de tête P2 (non décrite, donc supposée celle de YOLOv8).
