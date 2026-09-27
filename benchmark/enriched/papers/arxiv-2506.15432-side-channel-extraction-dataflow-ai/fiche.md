---
id: arxiv-2506.15432-side-channel-extraction-dataflow-ai
fiche: done
date:
---

# Side-Channel Extraction of Dataflow AI Accelerator Hardware Parameters

Guillaume Lomet, Ruben Salvador, Brice Colombier, Vincent Grosso, Olivier Sentieys, Cedric Killian, 2025, arXiv preprint. https://arxiv.org/abs/2506.15432
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

Critical reading (from supplied passages only). This paper is a side-channel reverse-engineering attack on FINN dataflow accelerators, not an accelerator design. Victim: a 5-layer CNN for MNIST built with FINN 0.9 on a PYNQ-Z2 (Zynq Z7020). The design uses no DSPs, stores all parameters on-chip, and runs at 100 MHz. There are 8 victim variants: folding 1x/2x/4x/8x × 4-bit/6-bit quantization. A 128-latch TDC sensor from SCABox runs on the same fabric at the same clock. The dataset has 6400 traces (800 per configuration), split 5120 train / 1280 test. Traces are trimmed to a window of about 129k samples, with the first 258k samples of dataflow loading discarded. Method: PCA (scikit-learn) followed by one lightweight classifier per parameter (k-NN or RF). The baseline is tsfresh feature extraction as in [17].

Measured results:
- Preparation time on the database is 15.7 s for k-NN and 17.7 s for RF with PCA, versus about 4.62 h with tsfresh (>940×).
- Attacking one trace takes 337 ms (k-NN, PCA) and 421 ms (RF, PCA), versus >110 s with tsfresh.
- k-NN (ncomp=12, k=13) reaches 91.84 folding accuracy without averaging and 96.78 with averaging over 4 traces.
- RF (PCA) reaches over 93.7 for quantization without averaging and 99.96 for both parameters with averaging over 4 traces (PCA-A4).

Caveats:
1. The abstract attributes 337 ms to RF and 421 ms to RF with 4-trace averaging. The body text and Table II instead give 0.337 s for k-NN (PCA), 0.421 s for RF (PCA) and 0.79 s for RF (PCA-A4). Rows follow the body text.
2. The Table III text extraction is garbled. Per-configuration cells cannot be reliably mapped, and the 91.84/96.78/96.70 'Avg' values are only partly tied to specific metrics in the prose.
3. The timings are for attack computation on a dual AMD EPYC 7443 server, excluding trace acquisition. They are not accelerator inference latency.
4. The paper reports no victim accelerator throughput, GOPS, power or resource utilisation. 'No DSP' is a design choice, not a reported utilisation figure.
5. There is only one victim model and one board, and the attacker is assumed to know all candidate configurations. Generality to other models or devices is not shown.
6. The note that separation is weaker at low folding comes from Fig. 4, which is not reproduced here.
