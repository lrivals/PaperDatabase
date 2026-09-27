---
id: arxiv-2506.20810-finn-gl-generalized-mixed-precision
fiche: done
date:
---

# FINN-GL: Generalized Mixed-Precision Extensions for FPGA-Accelerated LSTMs

Shashwat Khandelwal, Jakoba Petri-Koenig, Thomas B. Preußer, Michaela Blott, Shreejith Shanker, 2025, arXiv preprint. https://arxiv.org/abs/2506.20810
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

FINN-GL extends the FINN compiler so it can handle LSTMs. It models the LSTM recurrence with the ONNX Scan operator, which gives a QCDQ graph where each of the 11 internal QuantLSTM quantisers can have its own bit-width. It adds new or modified streamlining transformations (Table I) and an HLS backend that implements the recurrence as a loop bounded by sequence length. As a case study, the authors built a DeepLOB-style ConvLSTM without inception blocks: 2 conv blocks, an LSTM with 64 hidden units, input size 40 and sequence length 25, then FC 256 and FC 3, about 141K parameters. They trained it on FI-2010 (z-score version) with INT8 input features and deployed it on a ZCU104 (XCZU7EV) at 150 MHz. The compiler settings were mvau width = 36 and target fps = 1000. That fps figure is a compiler target, not a measurement.

Measured result: batch-1 latency of 4.3 ms. This matches the Vitis HLS cosimulation but excludes data movement. Resource use is reported only as percentages: about 49% of LUTs, 13% of flip-flops and 15% of DSPs. The supplied text does not give absolute LUT, DSP or BRAM counts, so those fields are n/r.

Accuracy (Table III): Q-ConvLSTM F1-scores are 77.54 (downward), 78.07 (stationary) and 76.60 (upward). The float ConvLSTM scores 76.22, 76.09 and 75.56, and DeepLOB scores 76.59, 80.36 and 76.68. So quantisation does not hurt accuracy, but on the stationary class the model trails DeepLOB.

Critical points:
1. The prediction horizon (k) behind Table III is not stated.
2. The paper names macro F1 as its main metric but does not report it in the supplied text. The per-class values are not averaged here.
3. There are no power or energy measurements.
4. There is no hardware comparison with FINN-L, hls4ml-LSTM or other FPGA LSTM accelerators. Only accuracy is compared (Table IV, whose contents were not supplied, and the claims of beating SVM by 42% and MLP by 29%).
5. The bit-widths of the mixed-precision weights and activations are not given in these passages.
6. The paper frames the work around HFT, where events can be nanoseconds to microseconds apart, yet the design reaches 4.3 ms. That is justified only against FI-2010's roughly 192 ms event interval.
7. The extraction flags say the metadata needs manual checking. The case-study text (Section IV) is filed under "III. DEVELOPMENT STAGES", so that heading is used as source_section.
