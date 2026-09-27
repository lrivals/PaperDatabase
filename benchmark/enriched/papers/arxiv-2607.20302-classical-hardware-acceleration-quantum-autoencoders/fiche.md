---
id: arxiv-2607.20302-classical-hardware-acceleration-quantum-autoencoders
fiche: done
date:
---

# Classical Hardware Acceleration of Quantum Autoencoders for Real-Time Anomaly Detection in Collider Experiments

Ivan Ge, Sagar Addepalli, Abhilasha Dave, Julia Gonski, 2026, arXiv preprint. https://arxiv.org/abs/2607.20302
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

Critical reading note: Ge et al. (arXiv 2607.20302) put two quantum autoencoders on an FPGA as classical emulations for L1-trigger anomaly detection at the LHC. The first is a hybrid VAE: a block-structured PQC with 87 quantum parameters followed by a classical MLP (32→16→3) with 630 parameters. The second is a fully quantum QAE with 23 parameters, scored from trash-wire z-scores. Both were synthesized for an Alveo U200 with a 5.5 ns target clock, using ap_fixed formats listed in Table 1. The reported latencies are 6.1 µs for the hybrid VAE and 0.47 µs for the QAE, and both fit in one SLR. I left latency_ms as n/r because the paper reports these values in µs and the instructions do not allow unit conversion. Caveats: (1) The hardware results are HLS synthesis estimates, not measured on the board or from post-place-and-route. No power figure is given. (2) The LUT, DSP and FF values in Table 2 are missing from the extracted text, so the resource columns are n/r. (3) The passages give no AUC or TPR@1e-5 numbers. The only accuracy-related claim is that TPR@1e-5 stays within ±5% of the 32-bit baseline for W≥18, and that low precision artificially inflates AUC. The authors therefore argue that TPR@1e-5 is the more reliable metric. (4) The design was tuned by an agentic AI loop (Claude Code) that minimized latency under a one-SLR resource limit. This makes it harder to reproduce, and the authors say the final resource/latency trade-off is flexible. (5) To keep emulation manageable, the 10 jets are split into two 5-qubit registers of 32 amplitudes each. This limits entanglement, and correlator measurements are used to partly recover the lost information. (6) The CPU/GPU/FPGA comparison is only qualitative: the FPGA is fastest at batch size 1, but CPU and GPU overtake it at larger batches. No numbers are given for this comparison. Metadata extraction was flagged as unverified.
