---
id: arxiv-2408.15561-cgra4ml-hardware-software-framework-implement
fiche: done
date:
---

# cgra4ml : A Hardware/Software Framework to Implement Neural Networks for Scientific Edge Computing

G Abarajithan, Zhenghua Ma, Ravidu Munasinghe, Francesco Restuccia, Ryan Kastner, 2026, arXiv preprint. https://doi.org/10.1145/3801097
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

cgra4ml (Abarajithan et al., ACM TRETS 2026 / arXiv 2408.15561) is an open-source framework built around the idea that it is meant for deployment rather than for exploring architectures. It generates vendor-agnostic SystemVerilog for a parameterised R×C CGRA of simple MAC PEs. It uses a single dataflow for conv and dense layers: columns regroup at runtime by KW, weights are held in ping-pong caches, and a pixel shifter reuses data vertically. The IP is wrapped with AXI and open-source DMAs. The framework also generates C firmware (bare-metal, PetaLinux or PYNQ-style ctypes) and TCL flows for Vivado, Genus/Innovus and DC/ICC2. Its main claimed difference from hls4ml, FINN, VTA and Vitis AI is verification: the production C runtime is linked into the SystemVerilog testbenches via DPI-C, with randomised AXI valid/ready backpressure, aiming for bit-exact agreement with a golden model. It is meant to fix hls4ml's scaling limit, since reusing layers lets it run larger models such as ResNet-50 and PointNet.

Critical points:
(1) The supplied passages contain no measured numbers. Only the captions of the result tables survive: Table 3 (ResNet-50, PointNet and Autoencoder on ZCU104), Table 5 (Jet-tagger, cgra4ml vs hls4ml across reuse factors) and Table 6 (8×24 PPA at 28/65/7 nm). The claim of 'competitive performance-per-watt' therefore can't be checked from this text.
(2) Pooling, normalisation, residual adds and writeback all run on the host CPU. The end-to-end latency on small trigger-style models may be dominated by this CPU work (the authors admit this and point to Table 4 and Sec. 6.2), so the CGRA's peak throughput overstates what a user would actually see.
(3) The idle-PE figures (1, 5 and 8% for KW=5, 7 and 11 at C=96) come from analysis, not measurement.
(4) The ASIC results are first-order PPA estimates from synthesis and place-and-route. The ARM NanoSoC tape-out is only mentioned as a partnership, not reported as silicon results.
(5) Table 6 uses different tool flows for different nodes (Cadence at 28/65 nm, Synopsys at 7 nm), so comparing across nodes is confounded.
(6) Comparing a layer-reuse CGRA with fully pipelined hls4ml on the tiny Jet-tagger mixes throughput and latency regimes. Check which metric Table 5 fixes.

Extraction status: I made one placeholder row, with low confidence, to record the ZCU104 ResNet-50 experiment named in the Table 3 caption. All of its metrics are n/r because the table body is not in the passages. Pull the values from the full PDF before using this row.
