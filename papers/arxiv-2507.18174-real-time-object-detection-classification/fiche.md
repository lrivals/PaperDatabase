---
id: arxiv-2507.18174-real-time-object-detection-classification
fiche: done
date: 2026-09-24
---

# Real-Time Object Detection and Classification using YOLO for Edge FPGAs

Rashed Al Amin, Roman Obermaisser, 2025, 2025 International Symposium ELMAR. https://doi.org/10.1109/ELMAR66948.2025.11193980 (texte lu : version arXiv 2507.18174)
Type : conférence (acceptation déclarée dans le commentaire arXiv, DOI éditeur trouvé via Crossref)

## Problème

Les détecteurs YOLO sur FPGA atteignent de bonnes performances, mais les auteurs estiment
qu'ils restent peu économes en ressources pour des FPGA « edge » (Abstract, §I). Objectif :
un système de détection/classification temps réel, économe, pour l'ADAS (panneaux routiers)
et la détection générale.

## Méthode

- Modèle : YOLOv5 (variante — n/s/m… — n/r), entraîné sous PyTorch à partir de poids
  pré-entraînés, fine-tuning sur COCO et GTSRB (§III-A, §III-B).
- Hyperparamètres : lr 0,01, batch 32, 100 epochs, SGD momentum 0,937, weight decay 0,0005,
  early stopping (§III-B ; la fin du paragraphe est rejetée par GROBID dans « Figures et
  tableaux »).
- Quantification post-entraînement FP32 → INT8 et compilation avec Vitis AI, exécution sur
  la DPU du KV260 (§III-C). Le texte parle aussi de « quantization-aware techniques » :
  PTQ ou QAT, ce n'est pas tranché.
- Aucune modification d'architecture ni travail matériel propre : flux standard Vitis AI
  → DPU. Post-traitement (NMS) : n/r.

## Plateforme et implémentation

- Carte : Xilinx Kria KV260 (§III-C, §IV). Puce exacte (XCK26 sur le module K26 — déduit,
  non écrit dans le papier), configuration de la DPU, fréquence : n/r.
- Ressources (LUT, DSP, BRAM) : n/r. Résolution d'entrée : n/r.
- Puissance : 3,5 W (Table I), méthode de mesure (puce ou carte, capteur ou outil) : n/r.
- Code, modèle compilé et bitstream : non publiés (aucune mention).

## Résultats

| Mesure | Valeur | Source |
|---|---|---|
| Classification accuracy | 98,6 % (99 % dans l'Abstract) | §IV-A, Table I |
| Débit | 9 FPS | §IV-A, Table I |
| Puissance | 3,5 W | Table I |
| Efficacité | 2,6 FPS/W | §IV-B, Table I |
| Jeu de test | 72 images « curated » (COCO + GTSRB) | §IV-A |

Baseline : uniquement d'autres travaux FPGA, chiffres repris de leurs papiers (Table I).
Aucune comparaison GPU, Jetson ou CPU mesurée par les auteurs.

→ reportés dans `benchmarks.csv` : 1 ligne (YOLOv5, INT8, Kria KV260, Table I, `high`).

## Limites et critique

- **Métrique non comparable.** « Classification accuracy » sur 72 images choisies, et non
  mAP sur le split de test de COCO ou GTSRB. La Table I la met en regard de mAP obtenues sur
  d'autres jeux (VN-ICC, marine…) : la comparaison de précision n'a pas de sens.
- **Conclusion non étayée par sa propre table.** Les auteurs revendiquent une meilleure
  efficacité énergétique (§IV-B), mais leurs 2,6 FPS/W sont en dessous de quatre des cinq
  travaux de la Table I (4 ; 4,7 ; 4,2 ; 3,1 FPS/W) — seul Heller et al. (1,87) est plus bas.
- **Incohérences internes.** Nguyen et al. : 29 FPS en §II, 125 FPS en Table I. Ngo et
  al. : jusqu'à 29 FPS en §II, 25 FPS en Table I. Précision : 99 % (Abstract) contre 98,6 %
  (§IV).
- **« Temps réel » à 9 FPS** : pas de latence rapportée, pas de contrainte temporelle
  définie.
- **Auto-référence probable** : « Amin et al. [19] » (99 %, 3,5 W) semble être un travail
  antérieur du premier auteur (déduit du nom, non vérifié dans la bibliographie).
- Puissance sans protocole, variante YOLOv5 et résolution inconnues, aucune ressource FPGA :
  le résultat n'est pas reproductible.

## Pertinence pour la thèse

Point de référence « flux industriel » : YOLOv5 INT8 via Vitis AI sur KV260, sans
optimisation matérielle. Utile comme borne basse à battre et comme exemple des défauts
méthodologiques courants (métriques hétérogènes, puissance sans protocole) à éviter dans un
protocole de thèse. N'apporte rien sur l'architecture de l'accélérateur.

## Gaps identifiés

- Pas de protocole commun de mesure pour YOLO sur Kria KV260 : puissance (puce vs carte),
  mAP sur split officiel, résolution et variante du modèle rarement toutes rapportées.
- Aucun baseline Jetson / GPU embarqué mesuré dans les mêmes conditions.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier, extraction GROBID). Défauts d'extraction : la
fin de §III-B est classée en « figure sans légende » ; le titre « V. CONCLUSION AND FUTURE
WORK » est absorbé par la Table I et la conclusion est rattachée à §IV-B.
Déduit et non affirmé par les auteurs : puce XCK26 ; lien d'auteur avec [19] ; lecture de
la Table I (classement des FPS/W).
