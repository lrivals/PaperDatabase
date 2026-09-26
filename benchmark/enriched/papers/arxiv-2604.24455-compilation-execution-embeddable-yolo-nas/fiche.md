---
id: arxiv-2604.24455-compilation-execution-embeddable-yolo-nas
fiche: done
date:
---

# Compilation and Execution of an Embeddable YOLO-NAS on the VTA

Anthony Faure-Gignoux, Kevin Delmas, Adrien Gauffriau, Claire Pagetti, 2026, arXiv preprint. https://arxiv.org/abs/2604.24455
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

What it shows: the authors (Airbus/ONERA) extend their stand-alone VTA compiler, built with DO-178C certification in mind, so that it can compile a whole network. It now handles matrices larger than the SRAM by partitioning them, and it automates the data reshaping between layers. It is tested on a quantized YOLO-NAS with 146 ONNX operators. 108 of them (QLinearConv, QLinearMul, MaxPool) run on the VTA and 38 fall back to the CPU because they need floating point. Compiling with Strategy 4 takes about 2 minutes and produces about 10.8M instructions and 9.1M UOPs. A run in the functional C++ simulator takes about 3 minutes.

What it does not show: nothing runs on an FPGA, and there is no cycle-accurate measurement. There are no FPS, latency, throughput, power or resource-use numbers (LUT/DSP/BRAM), and no detection accuracy on a dataset. The only correctness check is a bit-by-bit comparison on random int8 inputs over 10 runs. Output matches a NumPy reference written to follow the ONNX maths exactly. Against ONNX Runtime, values are mostly off by ±1 on up to 35% of outputs, which the authors blame on ONNX Runtime's QLinearConv optimisations.

Critical points:
1. Table 2 shows Strategy 3 gives the fewest instructions (6,348,149) and Strategy 4 the most (10,765,279), yet the pipeline figures quoted use Strategy 4. The paper also admits that instruction count does not predict VTA latency, so no strategy is shown to be better in practice.
2. Memory cost is dominated by biases being expanded into full matrices: 297 MiB versus 33 KiB of ONNX biases for YOLO-NAS, plus 93 MiB of instructions. That is a serious problem for embedded use.
3. Most of the simulation time goes to CPU-side data shuffling, and floating-point rescaling limits what can be offloaded.
4. The text is inconsistent: the introduction says int32 inputs, weights and biases, while the experiments use int8 inputs.

Text-extraction problems:
- Exponents were flattened: "228" means 2^28, and "25×27" means 2^5×2^7.
- The strategy labels are missing from Tables 2 and 3. I assumed the rows are Strategies 1 to 4 in order.
- In Table 3 Case 3, the same value (32,845, +1406.0%) appears twice, which may be an extraction error.
- The "Compiled" label is missing from the bias row of Table 1.

About the single row: it records a functional-simulation result, not a measured hardware benchmark, so every hardware field is n/r.
