---
id: arxiv-2504.04661-n-torc-native-tensor-optimizer
fiche: done
date:
---

# N-TORC: Native Tensor Optimizer for Real-time Constraints

Suyash Vardhan Singh, Iftakhar Ahmad, David Andrews, Miaoqing Huang, Austin R. J. Downey, Jason D. Bakos, 2025, arXiv preprint. https://arxiv.org/abs/2504.04661
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

N-TORC is a two-phase flow for building models that must meet a hard latency limit. First, Optuna/BoTorch searches network settings, trading accuracy (RMSE) against workload (number of multiplies). Second, a Mixed Integer Program (MIP) solver sets the HLS4ML reuse factor for each layer so the whole network fits a 200 µs latency budget with minimal LUT, DSP, register and BRAM cost. The solver relies on data-driven latency and resource models trained on synthetic layers. The case study is DROPBEAR: predicting roller position from vibration data sampled at 5 kHz, using networks built from Conv1D, LSTM and Dense layers.

Main claims:
- The resource and latency models are more accurate than those of Wu et al. (Tables I and II; the numbers in those tables are not in the supplied passages).
- The MIP solver matches the quality of stochastic search or simulated annealing run for 1M trials, in 1000X less search time.

Hardware evidence:
- The results appear to be HLS synthesis/report estimates, not measurements on a board. The passages say "high-level synthesis results" and "estimated resource cost, estimated latency."
- On the XCZU7EV, the deployed networks run in "slightly less than" 200 µs. Effective throughput is 11–39 Mops/s. They use 3.7–18.8% of the available LUTs and 0.58–4.5% of the DSPs.
- These are ranges or percentages, and throughput is given in Mops/s, not GOPS. So the numeric columns are left as n/r rather than converting units or filling them with ranges.
- Power, quantization/precision, fps and exact per-model RMSE are not reported in the passages.

Caveats:
- The authors admit their resource model has "imperfections": the rows 8 and 9 models use more LUTs than the rows 10 and 11 models, even though the latter need more multiplies.
- The extracted text of Tables III and IV is garbled, so per-model values could not be reliably extracted.
- There is a possible mix-up in the passages: row 4 is called model 1 but plotted as "model 2", and vice versa.
- The 1000X speed-up is compared only against naive search baselines. There is no comparison against another deployment optimizer.
- The paper is a preprint and its metadata is flagged for manual checking.
