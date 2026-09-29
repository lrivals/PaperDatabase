---
id: arxiv-1801.06601-cmsis-nn-efficient-neural-network
fiche: done
date: 2026-09-29
---

# CMSIS-NN: Efficient Neural Network Kernels for Arm Cortex-M CPUs

Liangzhen Lai, Naveen Suda, Vikas Chandra, 2018, arXiv preprint. https://arxiv.org/abs/1801.06601
Type : preprint non relu par les pairs

## Problème

Exécuter efficacement l'inférence de réseaux de neurones sur les processeurs Arm Cortex-M des
nœuds IoT, avec peu de mémoire et souvent sans FPU, pour traiter les données à la source
plutôt que dans le cloud (§1).

## Méthode

- Bibliothèque de noyaux **CMSIS-NN** : convolution, convolution séparable en profondeur,
  fully-connected, pooling, activations (NNFunctions) + fonctions de support (conversion de
  types, tables d'activation) (§2).
- **Quantification en virgule fixe à échelle puissance de deux** (valeur = A × 2ⁿ), données
  8 bits (q7_t) et 16 bits (q15_t), accumulation 32 bits ; recalage par décalages de bits,
  sans déquantification flottante entre couches — choix motivé par les Cortex-M sans FPU (§3).
- Multiplication matricielle 2×2 (et 1×4 en matrice-vecteur, poids réordonnés hors ligne) sur
  l'instruction SIMD MAC 16 bits SMLAD ; conversion q7→q15 sans réordonnancement (§4.1-4.2).
- Convolution par **im2col partiel** (quelques colonnes) pour limiter la mémoire ; format HWC
  (§4.3). Pooling x-y séparé, en place (4,5× plus rapide) ; ReLU en SWAR (≈ 4×) ;
  sigmoïde et tanh par tables sur [−8, 8] (§4.4-4.5).

## Plateforme et implémentation

- NUCLEO-F746ZG (Mbed), Cortex-M7 à 216 MHz (§5) ; puce STM32F746ZG : déduite du nom de la carte.
- Mémoire maximale ≈ 133 Ko avec im2col partiel (≈ 332 Ko sans, qui ne tiendrait pas) (§5).
- Puissance : n/r (seuls des rapports d'efficacité énergétique sont donnés, méthode n/r).
- Code publié : https://github.com/ARM-software/CMSIS_5 (§6).

## Résultats

- CNN CIFAR-10 (Caffe, 3 conv + 1 FC, 87 Ko de poids, 55 Ko d'activations, 24,7 M ops) :
  **79,9 %** en 8 bits contre 80,3 % en flottant ; **99,1 ms par image** (10,1 images/s),
  ≈ 249 MOps/s (Table 1, §5).
- Par couche : conv 31,4 / 42,8 / 22,6 ms, pooling 1,6 / 0,4 / 0,2 ms, FC 0,1 ms (Table 1).
- Contre une implémentation de base (arm_conv de CMSIS-DSP, pooling et ReLU à la Caffe) :
  convolution 443,4 → 96,4 ms, total 456,4 → 99,1 ms, soit **4,6× en débit et 4,9× en
  efficacité énergétique** (Table 2).

→ reportés dans `benchmarks.csv` : 1 ligne (CIFAR-10 sur Cortex-M7, Tables 1-2, `high`).

## Limites et critique

- **Inférence seulement** : aucun noyau de rétropropagation ni de mise à jour des poids.
- Baseline faible (convolution 1D CMSIS-DSP, pooling naïf) : le facteur 4,6× mesure l'écart à
  une implémentation non spécialisée, pas à un autre moteur optimisé.
- Efficacité énergétique donnée en facteur, sans puissance ni méthode de mesure.
- Quantification puissance de deux plus grossière que l'échelle affine de TensorFlow (Jacob
  2018), choisie pour éviter le flottant (§3).

## Pertinence pour la thèse

Socle logiciel de l'inférence INT8 sur Cortex-M utilisé (ou reproduit) par TinyOL, TFLM et les
travaux MCU du corpus. Pour le stage, il fixe les briques disponibles (MAC 16 bits SIMD,
virgule fixe, im2col partiel) et, par contraste, l'absence de noyaux d'entraînement : toute
mise à jour en ligne (EWC INT8) doit écrire ses propres noyaux de gradient, idéalement dans le
même format q7/q15 (déduit).

## Gaps identifiés

- Noyaux de rétropropagation en virgule fixe sur Cortex-M : absents de CMSIS-NN.
- Pas de mesure de puissance absolue pour situer l'énergie par inférence.

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). §4.5.2 (tables sigmoïde/tanh) coupée et reportée
dans la zone « Figures et tableaux ».
Déduit et non affirmé par les auteurs : puce STM32F746ZG ; conséquence pour l'entraînement
embarqué.
