---
id: arxiv-2609.05249-proton-irradiation-characterization-open-source
fiche: done
date:
---

# Proton Irradiation Characterization of an Open-Source ML Accelerator on a Zynq UltraScale+ MPSoC

Saad Memon, Rafal Graczyk, Jan Swakoń, Leszek Grzanka, Sebastian Kusyk, Mike Papadakis, 2026, arXiv preprint. https://arxiv.org/abs/2609.05249
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

What the paper is: a proton-irradiation reliability study, not a performance paper. The device is a Tensil TCU (16×16 systolic array, 100 MHz, 16-bit fixed-point FP16BP8) running ResNet-20 for CIFAR-10 on an Avnet Ultra96-V2 (XCZU3EG Zynq UltraScale+). It runs under PYNQ Linux v2.7. The beam came from the AIC-144 cyclotron at IFJ PAN at nominal 20, 40 and 58 MeV, using a small (~2-cm) and a wide (~4-cm) field.

Main results:
- Total fluence was 6.19×10^10 p/cm2. 92 blocks were launched and 83 completed (8300 inferences). Class records were kept for only 62 blocks (6200 inferences).
- There were nine primary onsets: seven Linux-SEFIs and two output events.
- The pooled wide-field Linux-SEFI cross section is 3.6×10^-10 cm2/system [1.5×10^-10, 7.5×10^-10]. The small-field conditions give only upper limits.
- The key finding is one silent-corruption event in run 5, block 10. The first 61 predictions were correct, then 39 in a row read "bird", a class absent from the input pool. Every availability monitor stayed nominal: process alive, 23–24 ms cadence, silent kernel log, memory test passed, power rails in range. A watchdog using only those signals would have missed it.

Weaknesses:
1. Output verification is uneven and thinnest where the output events happened: 42 of 43 blocks kept their records at 20 MeV, but only 11 of 28 at 40 MeV and 9 of 21 at 58 MeV. The authors admit the loss may be correlated with abnormal blocks, which would bias the output cross sections low.
2. The input pool is tiny: 10 CIFAR-10 test images covering 6 classes. No random seed was used, and only the top-1 class was kept, so numerical errors that leave the winning class unchanged cannot be seen.
3. Counts are very small (each nonzero energy-specific output estimate rests on one event). The field-comparison p-values are exploratory: not preregistered and not adjusted for multiple tests.
4. The run 4 event count is ambiguous and depends on the clustering rule.
5. Linux-SEFI is defined by symptoms and may include interruptions not caused by radiation, so the cross sections are upper bounds.
6. Other setup gaps: LPDDR4 has no ECC, device lot and date codes were not recorded, only nominal (not component-specific) energy is reported, and a continuous current trace exists only for run 1.

Benchmark data: the supplied passages give no LUT, DSP, BRAM, GOPS or power values. Power rails were sampled but no values are reported. The only timing figures are an inter-record cadence of 23–24 ms and about 2.34 s per 100 inferences. The cadence includes PYNQ and logging overhead, so it is not a pure accelerator latency. Before irradiation, all 10 pool images were classified correctly (10/10); this is not a standard accuracy benchmark, so the accuracy field is left as n/r. The paper metadata carries extraction warnings (metadata needs manual checking; axes were inferred automatically).
