---
id: arxiv-2104.02303-exploration-hardware-acceleration-methods-xnor
fiche: done
date:
---

# Exploration of Hardware Acceleration Methods for an XNOR Traffic Signs Classifier

Dominika Przewlocka-Rus, Marcin Kowalczyk, Tomasz Kryjak, 2021, arXiv preprint. https://arxiv.org/abs/2104.02303
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

Przewlocka-Rus et al. (2021) compare two ways of accelerating a binary (XNOR) traffic-sign classifier on GTSRB. Both run on a ZCU104 board (Zynq UltraScale+ MPSoC) at 100 MHz. One is a custom Verilog accelerator made with the authors' code generator; the other is built with Xilinx FINN from a Brevitas model. Test accuracy is similar: 96.3 for the custom version and 96.24 for FINN. The FINN design is faster: its best folding setting (E4, the largest PE/SIMD values) reaches 582.22 fps, against about 450 fps for the custom design. FINN also uses far fewer resources in utilisation %: BRAM 21.96 vs 48.72, LUT 6.14 vs 34.42, FF 4.62 vs 9.59, and no DSPs, while the custom design uses DSPs for its fully connected layers.

Caveats:
1. The two designs do not run the same network. The FINN version replaces the first fully connected layer with a 1x1 convolution (Conv-3), and the table lists 513 output channels, which looks like a typo for 512. The throughput comparison therefore mixes architecture differences with toolflow differences.
2. The custom design's frame rate is only given as 'almost 450 fps' in the abstract, so the 450 in the row is approximate.
3. The abstract says FINN reaches 'around 550' fps, but Table 4 E4 shows 582.22. The FINN frame rates in Table 4 look misaligned after text extraction: 4 experiments but only 3 frame rates, and 64.51 is attached to E2. So which frame rate belongs to which experiment is uncertain, although taking 582.22 as E4 is consistent with the 'more than 500 fps' gap between E1 and E4.
4. The Table 4 power column is missing from the extracted text, so the FINN power is n/r. The paper says power figures are Vivado estimates, not measurements.
5. The custom design is said to 'need over 4.396W, which is over 25% of the total power consumption of the FINN-generated one'. That wording is ambiguous, so no FINN power value was derived from it.
6. Resource values in the rows are utilisation percentages of the ZCU104 device, not absolute counts. Absolute LUT/FF/BRAM counts were lost in extraction. The custom design's DSP percentage is not given.
7. No latency or GOPS figures are reported.
8. Section headings were not detected, so most passages fall under '(préambule)'.
9. Accuracy comes from software test-set evaluation. The passages do not say whether it was re-checked on the board.
