---
id: arxiv-2308.05070-volumetric-fast-fourier-convolution-detecting
fiche: done
date: 2026-11-15
---

# Volumetric Fast Fourier Convolution for Detecting Ink on the Carbonized Herculaneum Papyri

Fabio Quattrini, Vittorio Pippi, Silvia Cascianelli, Rita Cucchiara, 2023, arXiv preprint. https://arxiv.org/abs/2308.05070
Type : preprint non relu par les pairs

## Problème

Détecter l'encre carbonée sur les fragments de papyrus d'Herculanum à partir de volumes micro-CT : l'encre n'a pas de contraste d'absorption distinct du papyrus carbonisé, elle modifie subtilement la structure du support (fissures, densité, épaisseur ; citant Parker et al. [32]). Les auteurs veulent modéliser à la fois le contexte local et global du sous-volume (§3.2, §1).

## Méthode

- Opérateur vFFC : extension de la Fast Fourier Convolution (Chi et al.) au 3D : branche locale (2 conv 3D, noyau 3) et branche globale (conv 3D + bloc spectral FFT3D, conv 1x1x1 sur parties réelle/imaginaire, iFFT3D) (§3.1, Fig. 2).
- Architecture : encodeur 3D ResNet-34, bottleneck de 3 blocs résiduels vFFC, moyenne sur la profondeur puis décodeur 2D (4 blocs d'interpolation bilinéaire x2 + conv, skip connections de type U-Net) ; la carte d'encre est sortie à résolution /4 (§3.2).
- Entrées : sous-volumes 16x256x256 (16 tranches centrales sur 65) ; à l'inférence, prédiction par fenêtres 16x256x256 en ne gardant que le centre 16x128x128 (§4.1).
- Labels : cartes d'encre dérivées des images infrarouges des fragments (labels IR, pas de pseudo-labels) (§4.1).
- Entraînement : perte Dice + WBCE (poids encre = 1), AdamW, OneCycle lr 0,003, batch 4, FP16, 20 époques ; augmentations : crop aléatoire 3D dans un treillis (cellules 32x512x512, pas 64), groupe dihédral D4, Channel Dropout 0,5, Drop Path 0,1 ; seuil 0,5 (§3.3, §4.1).

## Plateforme et implémentation

- Scan : EduceLab-Scrolls, fragments, micro-CT à 3,2 µm/voxel, 65 tranches ; fragment 1 : 6330x8181, fragment 2 : 9506x14830, fragment 3 : 5249x7606 (§4.1). Source du scan (synchrotron ou labo) et énergie keV : n/r dans ce papier. Fragments détachés de rouleaux, pas de rouleau entier.
- Calcul : NVIDIA RTX A5000, 24 h pour 20 époques (§4.1) ; temps d'inférence, mémoire, nombre de paramètres : n/r.
- Code : annoncé (« we will release »), https://github.com/aimagelab/vffc (§Abstract) ; publication effective non vérifiée ici. Données : EduceLab-Scrolls publiques (Vesuvius Challenge).

## Résultats

- Fragment 1 tenu à l'écart (test), fragments 2 et 3 en entraînement (§4.1). Un seul split : pas de validation croisée dans les ablations.
- Modèle complet (vFFC) : Fβ(0,5) 0,47, pFM 0,58, PSNR 10,09 (Table 3, Table 1 dernière ligne).
- Bottleneck (Table 3) : sans 0,46 / 0,58 / 9,87 ; stFFC 0,45 / 0,58 / 9,76 ; 3D-Conv 0,46 / 0,58 / 10,04 ; vFFC 0,47 / 0,58 / 10,09 (Fβ / pFM / PSNR).
- Augmentations (Table 1) : sans 0,37 ; + dihédral 0,46 ; + crop 0,46 ; + Channel Dropout 0,47 (Fβ). Pertes (Table 2) : Dice seul 0,40, WBCE seul 0,44, WBCE+Dice 0,47 ; un poids plus fort sur l'encre dégrade.
- Kaggle Vesuvius Ink Detection : ensemble de 6 modèles (k-fold, seuil 0,8, vote 4 sur 6), médaille d'argent (top 5 %), Fβ ≈ 0,70 en public, ≈ 0,60 en privé (§4.2).
- Activations LayerCAM : le réseau se concentre sur z ≈ 30 (invariance en profondeur induite par le crop), Fig. 6 (§4.2.1).
→ reportés dans `benchmarks.csv` : 7 lignes (Fβ et PSNR du vFFC, Fβ des 3 variantes de bottleneck, Fβ Kaggle public et privé).

## Limites et critique

- Gain de vFFC très faible (+0,01 Fβ face à 3D-Conv ou sans bottleneck, Table 3), sur un seul fragment de test, sans répétition ni variance : non démontré comme significatif (déduit).
- Fβ 0,47 en test vs 0,70 / 0,60 sur Kaggle : les chiffres Kaggle viennent d'un modèle « boosté » (ensemble, seuil différent) et ne valident pas l'opérateur vFFC seul ; le recul entre public et privé suggère un surapprentissage au jeu public (déduit).
- Le crop aléatoire n'améliore pas fragment 1 ; son intérêt n'est appuyé que par le classement Kaggle, sans chiffre d'ablation.
- Labels IR : risque de désalignement IR/CT non discuté ; pas de test de faux positifs ni d'étude de calibration. Pas de rouleau entier, pas de scan à 8-9 µm : transfert vers les rouleaux non évalué.
- PSNR et pFM, empruntés à la binarisation de documents, sont peu discriminants ici (pFM identique 0,58 sur 3 variantes).
- Code annoncé mais non vérifié ; paramètres, FLOPs, temps d'inférence n/r.

## Pertinence pour le thème

Travail d'ink detection 3D sur fragments à 3,2 µm, utile comme baseline académique (ResNet-34 3D + décodeur 2D) et pour l'idée de sous-volumes 16 tranches avec invariance en profondeur (utile quand la segmentation des feuillets est imparfaite). Le résultat est à relativiser pour les rouleaux à 8-9 µm : non traité. Axes : ink-detection, ct-imaging, virtual-unwrapping.

## Gaps identifiés

- Aucune évaluation sur rouleau entier ni à 8-9 µm ; pas de test de transfert entre fragments au-delà d'un split unique.
- Pas de mesure de faux positifs / calibration ; opérateurs spectraux 3D peu comparés à d'autres bottlenecks globaux (attention, transformers).

## Statut de lecture

papier complet (fulltext.md lu en entier). Extraction `pymupdf`, `extraction.ok: false` : texte possiblement imparfait ; les tableaux 1 à 3 sont lus en texte brut sans mise en forme (valeurs recoupées avec le texte, d'où `confidence: medium`). Déduit et non affirmé par les auteurs : significativité du gain vFFC, surapprentissage au jeu public Kaggle, risque de désalignement IR/CT. Venue : preprint arXiv, DOI n/r.
