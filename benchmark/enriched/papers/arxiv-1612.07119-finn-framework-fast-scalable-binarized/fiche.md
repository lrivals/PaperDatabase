---
id: arxiv-1612.07119-finn-framework-fast-scalable-binarized
fiche: done
date:
---

# FINN: A Framework for Fast, Scalable Binarized Neural Network Inference

Yaman Umuroglu, Nicholas J. Fraser, Giulio Gambardella, Michaela Blott, Philip Leong, Magnus Jahre, Kees Vissers, 2016, FPGA '17: ACM/SIGDA International Symposium on Field-Programmable Gate Arrays. https://doi.org/10.1145/3020078.3021744
Type : conférence

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

FINN (FPGA'17) presents a Vivado HLS framework that generates heterogeneous streaming dataflow accelerators for fully binarized NNs. Each layer gets its own compute engine (an MVTU with P PEs × S SIMD lanes), and folding factors are sized to meet a target FPS. Three hardware tricks make the mapping cheap: popcount instead of signed accumulation (376 vs 759 LUTs for 128-bit), batchnorm+sign folded into an unsigned threshold (6 LUTs vs 2 DSPs + 40 LUTs), and max-pool implemented as a Boolean OR after thresholding. All results are measured on a ZC706 (Zynq-7045) at 200 MHz.

Headline results:
- SFC-max: 12361 kFPS, 0.31 µs latency, 8265.45 GOPS, 7.3 W chip / 21.2 W wall power, 4.17% error on MNIST.
- CNV-max: 21.9 kFPS (the abstract gives 21906 FPS), 283 µs latency, 2465.5 GOPS, 3.6 W chip / 11.7 W wall power, 19.90% error on CIFAR-10 and 5.10% on SVHN.

Critical points:
1. The accuracy gap is large. SFC's 4.17% MNIST error is far behind float networks (Table 1). The accuracy-for-speed trade-off rests on a roofline argument (16× binary vs 8-bit), not on a matched-accuracy hardware comparison.
2. The prior-work comparison mixes chip and wall power, and different precisions and platforms. Several GOPS figures are the authors' estimates (marked ~).
3. Table 3 is garbled in extraction. It lists 4.5 BRAM for SFC-max, but Sec. 5 says 130.5, so the BRAM value was left as n/r. The LUT columns may also be misaligned.
4. The max designs are bottlenecked differently: SFC is memory-bound, LFC is BRAM/resource-bound (46% of roofline), and CNV is limited by the SWU unit. Reported runtime efficiency is about 70–90%.
5. The board's idle power is about 7 W, which dominates the wall-power efficiency figures.
6. DSP usage is not reported.

Unit handling: the paper reports throughput in kFPS and latency in µs. These do not match the fps and latency_ms columns and were not converted, so those cells are n/r and the values appear above instead. power_w holds the chip (FPGA) power; wall power is listed above.
