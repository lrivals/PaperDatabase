---
id: 2021-manjunath-energy-efficient-edgeai-autoencoder-accelerator
fiche: done
date: 2026-09-26
---

# An Energy Efficient EdgeAI Autoencoder Accelerator for Reinforcement Learning

Nitheesh Kumar Manjunath, Aidin Shiri, Morteza Hosseini, Bharat Prakash, Nicholas R. Waytowich, Tinoosh Mohsenin, 2021, IEEE Open Journal of Circuits and Systems 2, 182-195. https://doi.org/10.1109/OJCAS.2020.3043737
Type : article de journal (IEEE OJCAS, relu par les pairs)

## Problème

Un autoencodeur convolutif placé devant un agent d'apprentissage par renforcement (RL)
accélère l'apprentissage de la politique en compressant l'image en un petit vecteur latent,
mais il domine le coût d'inférence : 377 K paramètres et 20,1 M opérations, contre 4,3 K pour
l'agent RL (Table 1). Les auteurs veulent réduire ce coût (binarisation / ternarisation) sans
dégrader la récompense, et l'accélérer sur un matériel embarqué sobre (§I, §III).

## Méthode

- Autoencodeur convolutif (4 conv. stride 2 + 1 FC ; entrées 120 × 160 × 3 ou 120 × 120 × 3)
  pré-entraîné sur des images collectées dans trois simulateurs (DonkeyCar, Miniworld
  Sidewalk, Miniworld Object Pickup) ; agent RL à 2 couches FC sur le vecteur latent (§III,
  §V). Entraînement hors ligne ; seul l'**encodeur** est accéléré en inférence (§III, §VII).
- Variantes BNN (1 bit) et TNN (poids et activations ternaires sur 2 bits, seuil Δ = 0,5)
  avec 1×, 2×, 4× filtres et latents de 64 à 1 024 (§IV, §VI-A).
- Configuration retenue pour le matériel : **1.0 TNN-128** (Object Pickup), 142 Ko, 20,2 M
  opérations, PSNR 27,6 dB, récompense 82,0 % contre 84,8 % en pleine précision (Table 4).
  Choix contraint par la BRAM de l'Artix-7 100T (Fig. 10).
- Accélérateur **Verilog** : PE array à tuilage des canaux de sortie, N valeurs ternaires
  empaquetées par mot mémoire, multiplieurs ternaires + « Tpopcount », pas de cache de
  filtres, tout on-chip ; paramétrable en nombre de PE n (1 à 64) et largeur mémoire (8 à
  128 bits) ; performance ∝ f × N × n (§VII, Eq. 5).
- Implémentation ASIC post-layout en 14 nm FinFET (Synopsys EDK, DC + ICC II) de la
  configuration 32 bits / 64 PE (§VIII-B).

## Plateforme et implémentation

- FPGA **Artix-7** (« 135 BRAM, le plus petit de la famille » §VIII-A ; « Artix7-100T »
  §VI-B2 : les deux affirmations sont incompatibles, l'XC7A100T ayant 135 BRAM36, c'est
  vraisemblablement lui, déduit), **100 MHz**, Vivado.
- Ressources (Table 5, Docling) : de 906 LUT / 492 FF / 10 DSP / 73 BRAM (32 bits, 1 PE) à
  23 912 LUT / 7 951 FF / 7 DSP / 73 BRAM (128 bits, 64 PE).
- **Puissance** : « obtained using Vivado Design Suite » (§VIII-A, légende Table 5) → rapport
  de puissance de l'outil, portée `estimated`. ASIC : post-layout, aussi `estimated`.
- Code / bitstream : non publiés.

## Résultats

- Qualité (Table 4, Object Pickup) : pleine précision 84,8 % de récompense (PSNR 32,0 dB) ;
  1.0 BNN-1024 72,8 % (25,5 dB, 421 Ko) ; 1.0 TNN-128 82,0 % (27,6 dB, 142 Ko). TNN ≈ 10×
  plus petit que la pleine précision (1 476 Ko) (Tables 2, 4).
- FPGA (Table 5, 100 MHz) :
  - 32 bits / 64 PE : 0,8 ms, 204,8 GOPS, 318 mW, **0,25 mJ** par image (le plus sobre),
    644 GOP/J ;
  - 64 bits / 64 PE : 0,75 ms, 409,6 GOPS, 370 mW, 0,28 mJ, **1 107 GOP/J** (> 1 TOP/J) ;
  - 128 bits / 64 PE : 0,74 ms, 819,2 GOPS, 889 mW, 0,66 mJ ; « 1 350 FPS » (§VIII-A) ;
  - 32 bits / 1 PE : 19,8 ms, 3,2 GOPS, 260 mW, 5,15 mJ.
  Toutes les configurations sauf (8 bits, 1 PE) tiennent 30 FPS (§VIII-A).
- ASIC 14 nm (32 bits / 64 PE, 100 MHz) : 5 mW, 0,8 ms, 0,004 mJ, 42,3 TOP/J, 3,18 mm²
  (Table 7) ; 65× moins de puissance que le FPGA (§VIII-B).
- Comparaisons (Table 7) : FPGA 5× et 6,8× plus efficace que les TNN de [28] et [38] sur
  VC709 ; 4,2× plus efficace que l'AE 8 bits de [39] sur KCU105 ; ASIC 4,4× (2,2× après mise
  à l'échelle technologique) face à [28] en 28 nm.

→ reportés dans `benchmarks.csv` : **5 lignes** — 4 configurations FPGA représentatives de la
Table 5 (32 bits × 1 PE, 32 bits × 64 PE, 64 bits × 64 PE, 128 bits × 64 PE) et l'ASIC
14 nm. Les 17 autres configurations de la Table 5 ne sont pas recopiées : elles varient
continûment entre ces bornes. FPS renseigné seulement quand il est écrit par les auteurs
(1 350 FPS pour 128 × 64) ; sinon `n/r`, la latence étant donnée.

## Limites et critique

- **Puissance estimée par Vivado**, pas mesurée sur carte ; les comparaisons en TOP/J de la
  Table 7 mélangent ces estimations avec des chiffres d'autres travaux (mesurés ?) et des
  énergies **recalculées** par les auteurs à partir des FPS/W publiés (§VIII-C).
- **Tâches non comparables** dans la Table 7 : classification 32 × 32 (SVHN, GTSRB) contre
  encodeur 120 × 120 ; et l'AE 8 bits de [39] fait de la compression d'image 256 × 256.
- **Encodeur seul** : le décodeur n'est pas implanté (inutile en inférence RL) ; l'agent RL
  non plus, ni la capture caméra.
- Évaluation en **simulateurs** simplistes (Miniworld) ; pas de test sur robot réel.
- La « récompense » dépend de l'entraînement RL (5 runs, Monte-Carlo) : variance non
  rapportée.
- Aucune comparaison avec un Jetson ou un MCU mesurée, alors que le TX2 est cité en §II.

## Pertinence pour la thèse

Un des rares **autoencodeurs convolutifs sur images réelles (120 × 120 RGB) implantés sur
FPGA** : il nuance le gap « AE-FPGA surtout sur séries temporelles », même si l'usage est
l'extraction de latents pour le RL, pas la détection d'anomalies ni la compression. La
ternarisation (≈ 3 % de perte de récompense pour ≈ 10× moins de mémoire) et
l'accélérateur paramétrable PE × largeur mémoire sont des références directes pour un
encodeur embarqué sur KV260 (déduit). Le couple « encodeur figé + petite tête apprenante »
rejoint aussi l'axe apprentissage continu (déduit).

## Gaps identifiés

- AE convolutif ternaire avec **décodeur** sur FPGA (reconstruction, détection d'anomalies
  visuelles) : non traité.
- Puissance mesurée sur carte absente : seules des estimations Vivado.
- Apprentissage de la tête RL sur l'appareil : non traité (tout est entraîné hors ligne).

## Statut de lecture

Papier complet (`fulltext.md` lu en entier). Tables 1, 2, 4, 5, 7 reconstruites par
Docling : colonnes FF / DSP / BRAM de la Table 5 à vérifier ; Table 3 (Sidewalk) absente ;
Table 6 (ASIC) fusionnée à la légende de la Table 5, ses chiffres étant repris depuis la
Table 7.
Déduit et non affirmé par les auteurs : puce XC7A100T ; portée « estimée » de la puissance
(outil Vivado) ; intérêt pour KV260 et pour l'apprentissage continu.
