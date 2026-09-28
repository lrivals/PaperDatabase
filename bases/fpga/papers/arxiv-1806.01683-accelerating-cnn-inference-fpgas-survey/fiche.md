---
id: arxiv-1806.01683-accelerating-cnn-inference-fpgas-survey
fiche: done
date: 2026-09-24
---

# Accelerating CNN inference on FPGAs: A Survey

Kamel Abdelouahab, Maxime Pelcat, Jocelyn Serot, François Berry, 2018, Technical Report, Université Clermont Auvergne (HAL). https://arxiv.org/abs/1806.01683
Type : rapport technique (dépôt HAL cloné sur arXiv, d'après le commentaire arXiv) — non relu par les pairs

## Problème

Faire l'état de l'art des accélérateurs d'inférence CNN sur FPGA (2015-2018) : charge de
calcul, parallélisme et accès mémoire des CNN, et les moyens de les exploiter sur FPGA
(Abstract, §1).

## Méthode

Survey organisé selon une taxonomie en trois familles d'optimisations (§2.4.4, Fig. 2) :

1. **Transformations de calcul** (§3) : GEMM (im2col, batching des couches FC),
   Winograd (réduction ×2,25 des multiplications pour F(2×2, 3×3)), FFT (noyaux K > 5,
   overlap-and-add).
2. **Optimisation du chemin de données** (§4) : réseaux systoliques, accélérateurs SIMD et
   optimisation des boucles (unrolling P_i, tiling T_i, exploration par roofline), modèles
   de calcul dataflow (SDF, direct hardware mapping).
3. **Calcul approché** (§5) : virgule fixe statique et dynamique, BNN/TNN, calcul
   stochastique, élagage, approximation de rang faible (SVD).

Chaque famille est accompagnée d'un tableau comparatif d'implémentations publiées
(Tables 3, 5, 6, 7, 8). Formalisation utile : nids de 7 boucles de la convolution et
facteurs de parallélisme (§2.4.2, Table 4).

## Plateforme et implémentation

Sans objet (survey). Les travaux comparés vont du Cyclone V au Stratix 10, surtout Virtex-7,
Arria 10, Zynq 7000 (Tables 3-8).

## Résultats

Chiffres repris des travaux cités (non vérifiés ici) :

| Travail cité | Technique | Plateforme | Débit | Puissance | Source |
|---|---|---|---|---|---|
| [30] AlexNet conv, FP16, OpenCL | Winograd | Arria 10 GX1150 | 1382 GOP/s | 44,3 W | Table 3 |
| [70] AlexNet conv, 16 bits, HLS | Winograd | Zynq ZU9EG | 855 GOP/s | 23,6 W | Table 3 |
| [39] AlexNet conv, FP32, HLS | loop opt. | Virtex-7 VX485T | 61,62 GOP/s | 18,61 W | Table 5 |
| [84] VGG16, 16 bits, RTL | loop opt. | Arria 10 GX1150 | 720,15 GOP/s | n/r | Table 5 |
| [104] BNN CIFAR-10 | binaire | Zynq Z7020 | 208 GOP/s | 4,7 W | Table 7, §5.1.3 |
| [7] AlexNet élagué 85 % | pruning | Stratix 10 | 12 000 GOP/s (**projeté**) | 141,2 W | Table 8, §5.2.3 |

- Conv > 90 % du temps d'exécution, FC > 90 % des poids (VGG16 : 124 M sur 138 M) (§2.4.1,
  Table 2).
- La virgule fixe dynamique permet 8-16 bits pour ~0,4-2 % de perte sur AlexNet/VGG
  (§5.1.2).

→ reportés dans `benchmarks.csv` : aucune ligne (survey : chiffres de travaux cités).

## Limites et critique

- **Métriques non comparables dans les tableaux** : GOP/s en FP32, FP16, 16 bits et binaire
  mis côte à côte ; batch size non rapportée ; puissance sans distinction puce/carte ;
  une valeur **projetée** ([7], Stratix 10, 12 TOP/s) figure dans la Table 8 comme un
  résultat.
- Affirmations FPGA vs GPU reprises de travaux d'Intel ([7], [10]) sans recul : « 9,2
  TFLOP/s », « ×5,4 de débit par rapport aux GPU » sont des chiffres crête ou projetés
  (§1).
- Centré sur la classification ImageNet/CIFAR (§2.2) ; détection, segmentation seulement
  mentionnées.
- Daté (2018) : ni MobileNet/depthwise, ni YOLO, ni toolflows actuels (Vitis AI, hls4ml,
  FINN n'est cité que via les BNN).
- Rapport technique, non relu par les pairs.

## Pertinence pour la thèse

Référence de taxonomie : la décomposition « transformations / chemin de données / calcul
approché » et le formalisme des boucles (P_i, T_i) restent le vocabulaire de base pour
décrire un accélérateur CNN FPGA et positionner une contribution. Auteurs français
(Clermont-Ferrand ; M. Pelcat, affilié à l'IETR/INSA Rennes — déduit, affiliations non
présentes dans le texte extrait) : piste pour la liste des labos (Institut Pascal, IETR).

## Gaps identifiés

- Aucun traitement des réseaux de détection ni des architectures légères (depthwise) dans
  cette taxonomie : à compléter par 2509.04153 et 2411.01431.
- Comparaisons FPGA sans protocole commun (bitwidth, batch, puissance) : déjà un problème
  en 2018, toujours présent dans les surveys de 2025.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Extraction : **ligatures perdues dans tout le
texte** (« classi cation », « e cient », « con guration », « di erent ») — un `grep` sur
ces mots ne trouve pas ce papier ; titre de la section 3 non détecté (le texte suit
« FPGA Acceleration of CNNs ») ; tableaux partiellement désalignés (colonnes décalées dans
les Tables 5-7).
Déduit et non affirmé par les auteurs : affiliation IETR de M. Pelcat ; caractère projeté
des chiffres Intel ; manque de comparabilité des tableaux.
