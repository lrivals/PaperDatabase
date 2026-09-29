---
id: arxiv-2406.12362-certified-ml-object-detection-surveillance
fiche: done
date: 2026-09-29
---

# Certified ML Object Detection for Surveillance Missions

Mohammed Belcaid, Eric Bonnafous, Louis Crison, Christophe Faure, Eric Jenn, Claire Pagetti, 2024, ERTS 2024 (12th European Congress on Embedded Real Time Software and Systems), Toulouse. https://arxiv.org/abs/2406.12362
Type : article de conférence (ERTS 2024) déposé sur arXiv ; version arXiv non vérifiée comme identique à la version publiée.

## Problème

Développer un système de détection de drones intrus (caméra, réseau de détection) dans des zones sensibles avec un niveau de confiance suffisant pour la sûreté de fonctionnement, en suivant les recommandations en cours de rédaction de ED-324 / ARP6983 (SAE G-34 / EUROCAE WG-114) et le guide EASA (§I-A, §I-B). Exigences (confidentielles pour la plupart) : par exemple en zone A3, performance de détection > 80 % et latence < 50 ms (§I-A) ; objets de 0,5 m à 800 m.

## Méthode

Application partielle du processus ARP6983 sur un cas industriel (§I-C) :

1. ODD système puis ODD du constituant ML (MLCODD) à partir de scénarios opérationnels (terminologie ISO 34503), avec cas limites (edge cases) et exclusions (outliers) explicites (§II). Exemples de contraintes MLCODD : taille des objets 20 à 400 px² dont 95 % entre 20 et 100 px², positions uniformes sur l'image, luminosité moyenne HSV dans une plage (Fig. 3 et liste associée).
2. Conception du jeu de données (§III) : analyse de biais (70 % des objets dans une zone étroite centrée, Fig. 4), augmentation par l'algorithme 1 (recadrage aléatoire de 640x640 hors centre) et par un « mosaic dataset » (4 imagettes 320x320), de 0 à 4 intrus par image ; le jeu final P est plus de 3 fois plus grand que le jeu initial D ; découpage train/val/test conforme au MLCODD (§III-C).
3. Modèle (§IV) : YOLOv3 (une étape) préféré à Faster R-CNN (précision similaire mais latence incompatible) ; YOLOv3-tiny retenu ; image 1920x1080 non redimensionnée mais découpée en tuiles : 3 tuiles 1080x1080 (recouvrement 50 %, redimensionnées en 640x640) pour A1/A2, 8 tuiles 640x640 (recouvrement 30 %, sans redimensionnement) pour A3 (Table I) ; remplacement de 7 convolutions 2D du backbone par des convolutions séparables en profondeur (§IV-D).
4. Implémentation (§V) : Darknet (open source, pour la traçabilité) ; entraînement sous Keras, description manuelle du réseau en `.cfg` et `.weights` ; génération de code C (CPU) puis CUDA ; GEMM/im2col maison en CUDA FP32 pour éviter cuBLAS (fermé, traçabilité et WCET statique difficiles) ; paramètres de blocs par type de couche C1/C2 (Table III).

Toolflow : Darknet (génération C/CUDA), pas de toolflow FPGA.

## Plateforme et implémentation

NVIDIA Jetson AGX Xavier (8 coeurs ARM Carmel, GPU, NVDLA ; §V-A). Pas de FPGA. Puissance : n/r. Fréquence, ressources mémoire : n/r. Code/bitstream : non publiés (aucun lien dans le texte) ; données en partie privées (§III).

## Résultats

- CPU (1 coeur ARM) : le passage FP32 vers point fixe 16 bits sur la couche 24 donne -50 % de latence, dispersion réduite et -29 % d'OWCET (Fig. 11, §V-B) ; les exigences temps réel ne sont toujours pas atteintes.
- GPU CUDA FP16 sur tout le réseau : latence d'inférence totale 15 ms, soit 25 % de mieux que le FP32 (§V-B). Le texte ne précise pas si ces 15 ms couvrent une tuile ou les 8 tuiles ; le traitement par lots des 8 tuiles n'apporte aucun gain (§V-B).
- GEMM maison FP32 : plus lent que cuBLAS (Fig. 14, chiffres non extraits) mais suffisant pour la contrainte de latence (§V-D).
- Précision de détection (mAP, rappel, taux de fausses alarmes) : n/r ; aucun résultat chiffré de performance de détection n'est donné, pour raison de confidentialité (§I-A). Tables I à III ont un corps extrait (config de tuilage et paramètres GEMM), non chiffres de performance.
→ reportés dans `benchmarks.csv` : 1 ligne (CUDA FP16, 15 ms, `confidence: medium`, valeur issue du texte) dans `bench_rows.csv`.

## Limites et critique

- Peu de chiffres : aucune métrique de détection, aucune puissance, périmètre de la latence de 15 ms ambigu ; les exigences sont volontairement floues (§I-A). Impossible de juger si le processus a « certifié » quoi que ce soit : le titre promet « Certified », le texte parle d'un processus partiel conforme à un standard non publié (première version attendue au T2 2025, §I-B).
- Le processus couvre ODD, données, modèle, implémentation ; pas de vérification, pas de surveillance à l'exécution, pas d'analyse de sûreté ni de démonstration de complétude du jeu (§VI, travaux futurs).
- Augmentation par collage/recadrage : risque de décalage de distribution vs. données réelles non évalué (déduit).
- La traçabilité s'arrête aux pilotes NVIDIA (§VI) : la plateforme GPU reste une boîte noire ; le FP16 et GEMM maison sont « validés » par tests, sans preuve d'équivalence (déduit).
- Comparaison à des baselines : seulement FP32 vs FP16 vs cuBLAS sur la même cible ; aucune comparaison FPGA/autres cibles.
- Preprint arXiv d'un papier de conférence : version arXiv, non relue par les pairs en tant que telle.

## Pertinence pour la thèse

Cas d'étude proche du sujet : YOLO (v3-tiny) embarqué en surveillance avec démarche de certification ML (ARP6983) de bout en bout, et démarche transposable : ODD/MLCODD, analyse de biais et d'augmentation de données par rapport à l'ODD, tuilage pour petits objets, implémentation traçable (code source ouvert, sans bibliothèque COTS fermée). Sur FPGA, le même raisonnement appuie l'argument de traçabilité et de WCET déterministe (déduit, non traité par les auteurs, qui restent sur GPU Jetson). Cible et objet (drones dans le ciel) diffèrent des personnes en zone industrielle, mais la méthode d'ODD et de données s'applique. Laisse ouvert : vérification, monitorage OOD, redondance, implémentation FPGA.

## Gaps identifiés

- Aucune implémentation FPGA d'un YOLO suivant un processus de type ARP6983 / IEC 61508 avec traçabilité modèle vers code vers bitstream.
- Détection hors-ODD et monitorage indépendant (non-ML) : cités comme travaux futurs (§VI).
- Absence de métriques de détection publiques pour ce type de processus (confidentialité) : reproductibilité impossible.
- Traçabilité sous la couche pilote/matériel (§VI) : à traiter avec un accélérateur dont le RTL/HLS est inspectable.

## Statut de lecture

Papier complet (fulltext.md lu en entier ; extraction Grobid `ok`). Table II (« YOLOv3 inference ») et Fig. 11, 14 sans données chiffrées lisibles dans le texte extrait ; Table I et Table III lisibles (corps extrait non signalé « reconstruit », mais metadata liste Tables I à III comme « sans corps extrait » : chiffres de Table I et III recoupés avec le texte). Sections « C. Implémentation CPU » et « D. Optimized Cuda code » : numérotation de sous-sections du papier incohérente (A, B, D), le texte est probablement complet.
Ce qui suit est déduit et non affirmé par les auteurs : périmètre des 15 ms ; risques de l'augmentation ; portée FPGA ; comparaison à d'autres cibles ; « validation » FP16/GEMM par tests seulement.
