---
id: arxiv-2506.07367-survey-lut-deep-neural-networks
fiche: done
date:
---

# A Survey on LUT-based Deep Neural Networks Implemented in FPGAs

Zeyu Guo, 2025, arXiv preprint. https://arxiv.org/abs/2506.07367
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

This is a single-author survey (Guo, HUST) of LUT-based DNNs on FPGAs. It traces the line from DSP-based designs (hls4ml) to XNOR/BNN designs, then to LUTNet, NullaNet, LogicNets, PolyLUT, PolyLUT-Add and NeuraLUT, and on to ReducedLUT, AmigoLUT, DWN and TreeLUT. Section IV (Table I) compares accuracy and hardware cost on MNIST, JSC-H/JSC-L and NID. The survey quotes these numbers from the original papers ("THE RESULTS WERE QUOTED DIRECTLY FROM THEIR ORIGINAL PAPERS"); it did not re-measure them. That creates several problems:
(1) The FPGA device, toolchain and synthesis settings are not given in the supplied passages. They probably differ between the source papers, so the cross-method ratios in area×delay (for example 706.6× and 5673.5×) are not like-for-like.
(2) The extracted table is badly garbled. The LUT/FF/DSP/BRAM/Fmax/Latency columns have lost their alignment, and many cells are missing. I assigned columns only where the area×delay product checks out: DWN (lg) MNIST gives 4,082 LUT × 6.0 ns ≈ 2.45e+4, and DWN (sm) JSC-L gives 20 LUT × 0.6 ns ≈ 1.30e+1. In the second case the LUT count of 20 comes from the text.
(3) Latencies are reported in ns (DWN lg 6.0 ns, DWN sm 0.6 ns). They are not entered in latency_ms because units were not to be converted.
(4) There is an internal contradiction. The text says TreeLUT "exhibited the highest area-delay product" on JSC, but Table I shows TreeLUT (II) with one of the lowest (8.76e+2), so "highest" probably means "best".
(5) Power, throughput and GOPS are not reported. DWN reaches the highest accuracy (98.3 on MNIST) with the fewest LUTs, and TreeLUT has the lowest latency on MNIST.
Metadata and axes are flagged in the source as needing manual checks.
