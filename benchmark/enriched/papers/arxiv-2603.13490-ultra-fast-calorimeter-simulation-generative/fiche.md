---
id: arxiv-2603.13490-ultra-fast-calorimeter-simulation-generative
fiche: done
date:
---

# Ultra Fast Calorimeter Simulation with Generative Machine Learning on FPGAs

P. Alex May, Qibin Liu, Julia Gonski, Benjamin Nachman, 2026, arXiv preprint. https://arxiv.org/abs/2603.13490
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

Hardware-aware conditional VAE for fast calorimeter simulation (CaloChallenge Photon Dataset 1: 368 voxels, 374-d input with the energy ratios added). Only the decoder (234,884 trainable parameters) is deployed. It uses QKeras 0.9 quantization-aware training plus pruning; QINT16 precision, with a default of ap_fixed<16,6>. The energy-response dense+sigmoid path is trained in float and post-quantized. It is synthesized with hls4ml (resource strategy, io_stream, reuse factor = layer input dimension) for an AMD Xilinx Virtex UltraScale+ xcvu13p-flga2577-2-e.

Reported results: latency is 12.29 ± 4.56 µs (Table 4), or 0.0122 ± 0.005 ms/shower at batch 1 (Table 5). This compares with 2.27 ms for VAE-GPU and 24.6 ms for CaloINN on GPU. Utilization is LUT 85%, FF 12%, DSP 15%.

Critical caveats:
(1) The FPGA latency and resources are post-synthesis hls4ml estimates, not measured on a board. There is no place-and-route, no on-board timing and no host I/O overhead. Speedup claims therefore compare an estimate with a measured GPU wall-clock time.
(2) The luts and dsps fields hold utilization percentages (85, 15), not absolute counts. BRAM and clock frequency are not reported.
(3) Power is not reported, even though the abstract claims lower power.
(4) The GPU model used for VAE-GPU inference is not specified in the passages. Training used an A100.
(5) Fidelity is given only as separation S < 0.1 on histograms and an O(10)% degradation versus GPU. The 1/Savg values in Table 5 are truncated in the supplied text, so the accuracy fields are n/r.
(6) LUT usage is near capacity, driven by the softmax layers, which limits scaling.
(7) The latency ± spread (4.56 µs) is large for an HLS estimate and its origin is unexplained.
