---
id: arxiv-2304.10618-uleen-architecture-ultra-low-energy
fiche: done
date:
---

# ULEEN: A Novel Architecture for Ultra Low-Energy Edge Neural Networks

Zachary Susskind, Aman Arora, Igor D. S. Miranda, Alan T. L. Bacellar, Luis A. Q. Villon, Rafael F. Katopodis, Leandro S. de Araujo, Diego L. C. Dutra, Priscila M. V. Lima, Felipe M. G. Franca, Mauricio Breternitz, Lizy K. John, 2023, arXiv preprint. https://arxiv.org/abs/2304.10618
Type : preprint non relu par les pairs

## Problème

Quel verrou le papier attaque-t-il, tel que les auteurs le posent.

## Méthode

Architecture, quantification, stratégie de mapping sur le FPGA, post-traitement (NMS…).
Toolflow employé.

## Plateforme et implémentation

Puce exacte, fréquence, ressources consommées, mémoire. Code ou bitstream publiés ? Où ?

## Résultats

Les chiffres, avec la section ou le tableau source. Baseline de comparaison.
→ reportés dans `benchmarks.csv` : <lignes ajoutées>

## Limites et critique

Comparaisons biaisées, métriques non comparables d'un papier à l'autre, conditions de mesure
non précisées, absence de reproductibilité. Ce que le papier ne mesure pas.

## Pertinence pour la thèse

Ce que ce travail apporte à l'axe visé, et ce qu'il laisse ouvert.

## Gaps identifiés

Points à reporter dans `gaps.md`.

## Statut de lecture

Résumé seul | sections lues : <liste> | papier complet.
Ce qui suit est déduit et non affirmé par les auteurs : <…>

## Lecture automatique

ULEEN proposes a weightless neural network (WNN) built from Bloom-filter lookup tables instead of arithmetic. It adds ensembles, 30% pruning, thermometer encoding and a multi-shot training method inspired by BNNs. The paper compares an FPGA version against FINN BNNs on a Zynq Z7045 at a 200 MHz target, and a 45nm ASIC version against Bit Fusion running ternary LeNet-5 (FreePDK45 library, 500 MHz), all on MNIST.

Main FPGA result (ULN-S vs FINN SFC): 0.21 vs 0.31 µs latency, 14,286 vs 12,361 kIPS, 1.1 vs 7.3 W, 17,319 vs 91,131 LUTs, and 96.20 vs 95.83 accuracy. The authors report 1.4-2.6x lower latency, 1.2-2.6x higher throughput and 6.8-9.6x lower energy at batch 1.

Main ASIC result: ULN-L reaches 38,462 kIPS at 6.23 W, 5.22 mm2 and 195.5 nJ per inference (batch 16). Bit Fusion's best configuration (BF32) reaches 19.1 kIPS and 93,589 nJ per inference, but with 0.89 points higher accuracy (99.35).

Caveats:
- **Power is not measured.** FPGA power comes from Vivado reports and ASIC area and power from Cadence RTL Compiler, so power_scope is set to estimated. Bit Fusion's energy also includes Cacti estimates for its buffers, while ULEEN has no RAM blocks, so the two sides were not estimated the same way.
- **ULN-L on FPGA only met 85 MHz** because of routing congestion. Its Table II row is garbled in the extracted text (throughput missing, LUT/BRAM columns unclear), so I left it out.
- **BRAM and DSP counts for ULN-S are not given**, so they are n/r.
- **Units were not converted, as instructed.** Latency is reported in µs and throughput in kIPS, so latency_ms and fps are n/r. The raw values are in this note and in the baseline field.
- **The Bit Fusion comparison is at batch 16**, which makes the single-inference latency comparison difficult.
- **Model sizes don't match across tables.** Table IV gives ULN-L as 98.5 test accuracy. The 16.9 KiB ULN-S size in the extracted Table I may not match the pruned sizes.
- **The paper metadata needs manual checking** (the extraction flagged it).
