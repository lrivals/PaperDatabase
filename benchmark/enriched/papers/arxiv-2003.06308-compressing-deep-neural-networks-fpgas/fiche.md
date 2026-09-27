---
id: arxiv-2003.06308-compressing-deep-neural-networks-fpgas
fiche: done
date:
---

# Compressing deep neural networks on FPGAs to binary and ternary precision with hls4ml

Jennifer Ngadiuba, Vladimir Loncar, Maurizio Pierini, Sioni Summers, Giuseppe Di Guglielmo, Javier Duarte, Philip Harris, Dylan Rankin, Sergo Jindariani, Mia Liu, Kevin Pedro, Nhan Tran, Edward Kreinar, Sheila Sagear, Zhenbin Wu, Duc Hoang, 2020, arXiv preprint. https://doi.org/10.1088/2632-2153/aba042
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

Critical reading note: Ngadiuba et al. (2020) add binary and ternary dense layers to hls4ml, starting with tag v0.1.6. Two optimisations stand out. First, binary multiplications become XNOR operations. Second, batch normalisation (BN) followed by binary/ternary tanh is folded into thresholds that are computed at compile time, so no DSPs are needed. The paper tests six strategies (BNN, TNN, best BNN/TNN found by Bayesian optimisation, and hybrid ReLU/clipped-ReLU versions) on two small MLPs: MNIST (784x128x128x128x10) and LHC jet tagging (16x64x32x32x5).

Main claims:
- Straight binarisation or ternarisation works fairly well on MNIST but loses a lot of accuracy on jet tagging.
- Hybrid models recover about half of that loss, at a small DSP cost from explicit BN.
- The best TNN matches the best BNN's accuracy with the baseline's latency and far fewer DSPs, so ternary generally gives a better resource/accuracy trade-off.
- The baseline MNIST model's accuracy drop from 98 to 95 after <18,8> quantisation comes from the precision of the softmax lookup table (LUT). A <22,10> softmax LUT brings it back to 97.

Caveats:
- All hardware numbers are HLS estimates or post-logic-synthesis results. There is no on-board measurement, no power figure and no throughput in fps.
- The per-configuration resource and latency tables (Tables 4 and 6) are only captions in the supplied passages. The only hardware numbers given in the text are for the 3x256 MNIST BNN on a Xilinx Virtex UltraScale+ VU9P: initiation interval 28, maximum latency 0.31 µs, 0% DSPs, 7% FFs, 23% LUTs, 16% BRAM, reported as comparable to Ref. [18].
- In the row, latency_ms is n/r because the paper gives 0.31 µs and units must not be converted.
- LUTs, DSPs and BRAM are percentages of the device, not absolute counts.
- The clock frequency isn't given in these passages, so fps and GOPS can't be derived.
- The models were deliberately not architecture-optimised. The jet data set is simplified and leaves out the cost of computing the input features.
- Every passage has the section heading '(préambule)', because section extraction failed.
