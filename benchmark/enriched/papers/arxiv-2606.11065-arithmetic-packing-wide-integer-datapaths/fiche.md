---
id: arxiv-2606.11065-arithmetic-packing-wide-integer-datapaths
fiche: done
date:
---

# Arithmetic Packing on Wide Integer Datapaths in DSP Primitives of Modern FPGA Devices

Titus Bornträger, Shane Fleming, Philipp Holzinger, Dietmar Fey, Michaela Blott, Thomas B. Preußer, 2026, arXiv preprint. https://arxiv.org/abs/2606.11065
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

What the paper does: it packs several arbitrary-bitwidth signed or unsigned operands into one DSP multiplier input. The packing uses the DSP pre-adder: sign bits are subtracted as D − A, so no fabric adders are needed. It builds two FINN-integrated architectures on this. SDV packs one multiplier input for matrix-vector multiplication (MVM). It tracks lane spill-over with a modulo-4 reference computed in fractured LUTs, and needs lane size L ≥ wa + wb − 1. BSEG packs both inputs for convolutions and biases each lane with 2^(L−1) guard offsets.

Evaluation setup: out-of-context Vivado 2025.2 synthesis targeting a ZCU104 (DSP48E2). The target clock was 250 MHz. Table IV compares maximum frequency: 580 MHz for the FINN baseline vs 590 MHz for BSEG.

Headline claims:
- For UltraNet INT4 at 416×416, BSEG uses 21% fewer LUTs and gets 36% more FPS/DSP than FINN, where the FINN baseline already uses SDV.
- On convolution layers only, BSEG uses 27% fewer LUTs than HiKonv, 29% more DSPs, and gets 25% more FPS/DSP.
- On the base convolution layer, BSEG uses 63% fewer LUTs and 25% fewer DSPs.

Caveats:
1. All results are post-synthesis only. There are no on-board measurements of throughput or power, and no accuracy is reported.
2. Table II is garbled in the extraction. The LUT row (43k/48k/63k/50k–46k/35k–31k) and the FPS/DSP row (0.7/1.2/1.1/1.5/1.5) were matched to designs by cross-checking against the percentages in the text. Absolute FPS and DSP counts are not recoverable.
3. The comparison with HiKonv and Base [21] is not like-for-like. Those works targeted the Ultra96 at 160×320 input, while this paper uses ZCU104 at 416×416.
4. BSEG only pays off in the first three UltraNet layers; SDV is better for the others. This is because FINN's input generator becomes costly when there are many input channels.
5. The frequency passage also contains a stray 17761. It is not tied to any metric, so it was not used.
