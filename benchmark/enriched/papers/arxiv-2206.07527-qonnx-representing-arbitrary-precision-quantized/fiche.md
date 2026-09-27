---
id: arxiv-2206.07527-qonnx-representing-arbitrary-precision-quantized
fiche: done
date:
---

# QONNX: Representing Arbitrary-Precision Quantized Neural Networks

Alessandro Pappalardo, Yaman Umuroglu, Michaela Blott, Jovan Mitrevski, Ben Hawks, Nhan Tran, Vladimir Loncar, Sioni Summers, Hendrik Borras, Jules Muhizi, Matthew Trahms, Shih-Chieh Hsu, Scott Hauck, Javier Duarte, 2022, arXiv preprint. https://arxiv.org/abs/2206.07527
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

QONNX (Pappalardo et al., arXiv 2206.07527, 2022) is a format and tooling paper, not a hardware benchmark paper. Its contributions:
(1) Two backward-compatible ONNX variants for sub-8-bit quantization. Both insert integer Clip nodes: the quantized-operator format with clipping, and QCDQ (quantize-clip-dequantize).
(2) A higher-level dialect with three operators: Quant, BipolarQuant and Trunc. Each one quantizes and then dequantizes (float32 in and out). Scale, zero_point and bit_width are tensors, so broadcasting covers both per-tensor and per-channel quantization.
(3) Python utilities for execution, shape inference, constant folding and conversion from channels-first to channels-last layout.
(4) Import paths from QKeras (via tf2onnx) and Brevitas, and ingestion into hls4ml and FINN. FINN converts Quant nodes into its own MultiThreshold nodes and only supports ReLU, hardtanh and identity activations.
(5) A model zoo.

Critical points:
- None of the supplied passages reports a measured FPGA result. There is no throughput, latency, power or resource figure (LUTs, DSPs, BRAM) for any hls4ml or FINN build. The value to hardware work is shown only in qualitative terms.
- Table I compares formats with self-assessed checkmarks, not experiments.
- The QCDQ and clipping variants only work at or below 8 bits, and they cannot express a separate bit width per channel.
- The QONNX execution engine is meant for checking correctness, not for speed.

Table III (model zoo) has only accuracy and complexity figures (MACs, bit operations (BOPs), weights). In the text extraction its columns are run together: the input, weight and activation bit-width cells are missing and the numbers are merged. Accuracies were not checked against the original PDF.

The two rows below are software accuracy figures for models in the zoo, not hardware measurements. Hardware fields are n/r. The platform field is n/r because no deployment target is reported.
