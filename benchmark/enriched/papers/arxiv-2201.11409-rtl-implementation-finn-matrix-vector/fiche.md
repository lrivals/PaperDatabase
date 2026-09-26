---
id: arxiv-2201.11409-rtl-implementation-finn-matrix-vector
fiche: done
date:
---

# On the RTL Implementation of FINN Matrix Vector Compute Unit

Syed Asad Alam, David Gregg, Giulio Gambardella, Thomas Preusser, Michaela Blott, 2022, arXiv preprint. https://arxiv.org/abs/2201.11409
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

Scope: the paper builds an RTL (SystemVerilog) version of FINN's Matrix-Vector Unit (MVU), the matrix-vector compute unit. It is a drop-in replacement for the HLS library. The authors compare it with the original Vivado HLS version by sweeping IFM/OFM channels, kernel size, IFM size, PE, SIMD and precision (1-bit XNOR, binary weights, or 4-bit weights and inputs). Target device: Xilinx Zynq-7000 XC7Z020-1CLG400C on a Pynq-Z1 board. Toolflow: FINN, with Vivado for RTL and Vivado HLS for HLS.

Claims (Abstract): For small designs, RTL gives much smaller circuits. For large designs, RTL uses up to about 15% more LUTs. HLS always uses more flip-flops (orders of magnitude more for small designs) and about 2× more BRAMs. RTL has a critical path up to about 80% shorter and synthesizes at least 10× faster. The results were checked on a 4-layer MLP for network intrusion detection (NID).

Caveats:
1. The reported numbers are out-of-context post-synthesis estimates, not post-place-and-route or on-board measurements. The paper says some designs were tested on the board, but it reports no board results.
2. The clock constraint was 5 ns, relaxed to 10 ns if either design failed timing. This means the Fmax comparison uses mixed targets.
3. The paper reports no power, throughput, FPS or model accuracy. The NID MLP accuracy and its absolute synthesis numbers (Tables 4, 5 and 7) are not in the supplied passages. Only the table captions are present.
4. The HLS designs keep an II=1 through heavy pipelining. That explains the extra FFs and is a design choice, not something inherent to HLS.
5. All comparisons are relative. The rows below therefore contain no absolute numbers (n/r).

Metadata extraction is flagged as unreliable, and no sections were detected. Every passage except the Abstract is labelled '(préambule)'.
