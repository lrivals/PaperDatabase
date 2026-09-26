---
id: arxiv-1807.04093-finn-library-extensions-design-trade
fiche: done
date:
---

# FINN-L: Library Extensions and Design Trade-off Analysis for Variable Precision LSTM Networks on FPGAs

Vladimir Rybalkin, Alessandro Pappalardo, Muhammad Mohsin Ghaffar, Giulio Gambardella, Norbert Wehn, Michaela Blott, 2018, arXiv preprint. https://arxiv.org/abs/1807.04093
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

FINN-L (FPL 2018) adds LSTM/BiLSTM layers to the FINN HLS library, with configurable precision and parallelism. It is tested on a single-layer BiLSTM for OCR, where accuracy is scored by Character Error Rate (CER). Training is quantization-aware in Torch7 and PyTorch, and the in-memory cell activations and output-layer weights are fixed at 8 bits.

Main claims:
- With 1-bit weights and multi-bit activations, the model can beat floating-point accuracy.
- Going above 3 bits adds hardware cost and power with almost no accuracy benefit.
- Quantizing output and recurrent activations separately (1/2/1/1) is 1.32 percentage points more accurate than 1/1/1, with no extra cost in the recurrent layer.
- On the ZCU104 (XCZU7EV) at 266 MHz, the 1/2/8 configuration reaches 3873 GOP/S for the whole network and 3435 GOP/S for the LSTM layer alone. The authors call this state of the art for dense LSTM models on FPGAs.

Critical caveats:
1. The ZCU104 throughput is described as "estimated" (Fig. 8). It comes from placing and routing multiple accelerator instances, not from a measurement on the board. Only the PYNQ-Z1 throughput (Fig. 7, 100 MHz) is described as measured, and the supplied text gives no numbers for it.
2. The number of instances was helped by weight sparsity: some arrays were optimized out, for example in 2/2/2. Results therefore depend on the specific weights and are not a worst-case figure.
3. GOP/S is counted analytically and ignores the rest of the network. Table II normalizes other designs' throughput to 142 MHz by assuming throughput scales linearly with frequency, which makes the comparison weaker.
4. Power figures come from vector-less Vivado Power Analysis (12.5% toggle rate), so they are not measured.
5. Accuracy, resource and power values appear only in figures (Fig. 4–6). The Table I hyperparameter values and the columns of Table II are garbled or missing in the extracted text: the "200/17894" throughput entry cannot be matched to a column reliably. For these reasons, accuracy, LUT, DSP and BRAM counts, and power are left as n/r.
6. The file's own metadata flags the extraction for manual checking.
