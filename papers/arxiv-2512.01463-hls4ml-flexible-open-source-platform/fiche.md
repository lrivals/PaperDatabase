---
id: arxiv-2512.01463-hls4ml-flexible-open-source-platform
fiche: done
date: 2026-09-24
---

# hls4ml: A Flexible, Open-Source Platform for Deep Learning Acceleration on Reconfigurable Hardware

Jan-Frederik Schulte, Benjamin Ramhorst, Chang Sun, Jovan Mitrevski, Nicolò Ghielmetti, Enrico Lupi, Dimitrios Danopoulos, Vladimir Loncar, Javier Duarte, David Burnette, Lauri Laatu, Stylianos Tzelepis, Konstantinos Axiotis, Quentin Berthet, Haoyan Wang, Paul White, Suleyman Demirsoy, Marco Colombo, Thea Aarrestad, Sioni Summers, Maurizio Pierini, Giuseppe Di Guglielmo, Jennifer Ngadiuba, Javier Campos, Ben Hawks, Abhijith Gandrakota, Farah Fahim, Nhan Tran, George Constantinides, Zhiqiang Que, Wayne Luk, Alexander Tapper, Duc Hoang, Noah Paladino, Philip Harris, Bo-Cheng Lai, Manuel Valentin, Ryan Forelli, Seda Ogrenci, Lino Gerlach, Rian Flynn, Mia Liu, Daniel Diaz, Elham Khoda, Melissa Quinnan, Russell Solares, Santosh Parajuli, Mark Neubauer, Christian Herwig, Ho Fung Tsoi, Dylan Rankin, Shih-Chieh Hsu, Scott Hauck, 2025, arXiv preprint. https://arxiv.org/abs/2512.01463
Type : preprint non relu par les pairs

## Problème

Présenter l'état actuel de hls4ml (v1.x) : un compilateur open source qui traduit des
modèles Keras / PyTorch / ONNX en code HLS pour FPGA (AMD, Intel/Altera) ou ASIC
(Catapult), pour l'inférence à faible latence et faible consommation (Abstract, §1, §3).
Manuscrit « submitted to ACM » (mention dans le texte extrait).

## Méthode

Papier de plateforme :

- Architecture de compilateur : front ends (Keras 2/3, QKeras, HGQ/HGQ 2, PyTorch via
  torch.fx, ONNX/QONNX) → IR + optimizer flows (fusion BN, propagation de précision
  bit-exacte depuis v1.2.0, découpage en sous-graphes « MultiModelGraph ») → back ends
  (Vivado/Vitis HLS, Quartus/oneAPI, Catapult) (§3-6).
- Produit matrice-vecteur à poids constants (CMVM) selon trois stratégies : Latency
  (déroulé, poids câblés), Resource (poids en BRAM, II = RF), Distributed Arithmetic (graphe
  d'additionneurs via da4ml, sans DSP, RF = 1 seulement) ; parallélisme réglé par le reuse
  factor RF et le parallelization factor PF (§6.1).
- Activations non linéaires en tables de correspondance (~2048 entrées) ; transfert entre
  couches `io_parallel` (câblé) ou `io_stream` (FIFO dont la profondeur est optimisée par
  co-simulation RTL) (§6.1).
- Écosystème : QKeras, HGQ (quantification par paramètre, EBOPs), da4ml, élagage DSP/BRAM
  aware, surrogates rule4ml / wa-hls4ml, NAC, MetaML-Pro, intégration SoC ESP (§7).

## Plateforme et implémentation

- Évaluations en **placement-routage hors contexte** (OOC P&R) : AMD XCVU9P, XCVU13P,
  XC7A35T (Artix-7) ; Altera Agilex 7 AGFB014R24A2E2V ; Vivado/Vitis 2023.2, oneAPI 2025.0
  + Quartus 23.1 (§9, Tables 3-9).
- Aucune mesure de puissance dans les évaluations.
- Code : hls4ml open source (§1) ; dépôt non cité dans le texte extrait.

## Résultats

Résultats propres (Table 5 et Table 9 ; la plupart des autres tables reprennent [2], [20],
[31], [113]) :

| Modèle | FPGA | Précision | Latence | LUT | DSP | Source |
|---|---|---|---|---|---|---|
| MLP 128 (MNIST), HGQ + DA | XCVU13P, 5 ns | 97,7 / 97,3 / 97,0 % | 10 ns (2 cycles) | 9671 / 6890 / 5040 | 0 | Table 9 |
| Jet tagger HLF, HGQ + DA | XC7A35T | 76,9 / 76,5 / 75,9 % | 337,4 / 270,1 / 261,1 ns | 19 467 / 10 692 / 5455 | 0 | Table 5 |
| Jet tagger HLF, HGQ + Latency | XC7A35T | 76,9 % | échec du placement | — | — | Table 5 |

- Jet tagger sur XCVU9P : HGQ + DA à 76,9 % en 5 cycles (23,4 ns), 11 978 LUT, 0 DSP,
  contre QKeras 76,3 %, 15 cycles et 175 DSP (repris de [31], [98]) (Table 3-4 extraites
  ensemble) ; Fmax 694-756 MHz visée 1 GHz (Table 4).
- MLP-Mixer particle-based jet tagger (XCVU13P) : 80,3-81,4 %, 60-65 ns, 51-126 k LUT, DA
  seulement (Latency échoue en timing) (Table 8).
- Qualité HLS : de mieux que le Verilog fait main à 2× moins bon selon les cas ([72,73],
  §9.6) ; synthèse parallèle en sous-graphes : ResNet CIFAR-10 de 7 h à 3 h (§5).
- Applications recensées : triggers ATLAS/CMS (autoencodeurs AXOL1TL — VAE — et CICADA —
  CAE — de détection d'anomalies en production), segmentation sémantique pour voiture
  autonome ~5 ms sur ZCU102 ([48]), ECG 1D-CNN 1,655 W ([80]) (§10).

→ reportés dans `benchmarks.csv` : 6 lignes (Table 9 ×3, Table 5 DA ×3 ; `high`).

## Limites et critique

- **Évaluation hors contexte, sans puissance ni mesure sur carte** : latences et ressources
  issues de l'OOC P&R, qui ignore I/O, contrôle et transferts.
- **Modèles minuscules** (MLP 16 entrées, MLP MNIST 1 couche) ; les résultats sur CNN de
  vision (SVHN, Table 7) ne sont pas extraits et viennent de travaux antérieurs. Les
  auteurs reconnaissent que les gros modèles échouent en synthèse (§11).
- La majorité des chiffres sont repris ([2], [20], [31], [113]) : peu de nouveaux résultats.
- Aucune comparaison quantitative avec FINN, fpgaConvNet ou Vitis AI sur un même modèle ;
  la Table 10 est qualitative (et illisible dans l'extraction).
- Auteurs = développeurs de l'outil ; papier soumis, non encore relu.
- Dépendance aux versions de compilateurs HLS et abandon d'Altera par oneAPI 2025.1
  (§11) : risque de pérennité.

## Pertinence pour la thèse

Référence à jour pour l'axe toolflows et le prototypage d'autoencodeurs : hls4ml porte déjà
des VAE/CAE de détection d'anomalies en production dans les triggers du LHC (§10). Pour la
vision embarquée, le flot dataflow « tout sur puce » limite la taille des CNN ;
à comparer à FINN (arxiv-1612.07119, arxiv-1809.04570) et aux overlays DPU (Vitis AI) pour
un YOLO sur Kria. HGQ + da4ml (0 DSP) est une piste pour des modèles très quantifiés.

## Gaps identifiés

- hls4ml : pas de résultat publié sur un détecteur type YOLO ni sur un autoencodeur
  convolutionnel d'images de taille réaliste (limite de synthèse des gros modèles, §11).
- Aucune mesure de puissance dans l'évaluation d'un outil pourtant présenté pour le
  « low-power ».
- Pas de benchmark croisé hls4ml / FINN / Vitis AI sur un même CNN et une même carte.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Extraction : l'introduction est tronquée (le
texte reprend en cours de phrase) ; sections 1, 5, 6, 8, 10 et 11 non détectées comme titres
— leur texte est rattaché à la section précédente (ex. §11 « Limitations » dans §10) ; les
numéros cités ici pour ces sections viennent du texte lui-même (« Section 11 ») et restent à
vérifier sur le PDF ; Tables 3, 6, 7 absentes (légendes seules), Tables 3-4 fusionnées ;
symboles ✗ convertis en ✓ dans les Tables 1, 2, 10.
Déduit et non affirmé par les auteurs : portée de l'évaluation OOC ; absence de comparaison
croisée comme limite ; pertinence pour YOLO/CAE.
