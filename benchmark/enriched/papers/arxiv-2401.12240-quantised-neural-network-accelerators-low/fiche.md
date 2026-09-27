---
id: arxiv-2401.12240-quantised-neural-network-accelerators-low
fiche: done
date:
---

# Quantised Neural Network Accelerators for Low-Power IDS in Automotive Networks

Shashwat Khandelwal, Anneliese Walsh, Shanker Shreejith, 2024, arXiv preprint. https://arxiv.org/abs/2401.12240
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

Khandelwal, Walsh & Shreejith (arXiv 2401.12240) build 4-bit quantised MLP intrusion detectors for automotive CAN networks. They trained the models with Brevitas/FINN and run them as custom IP in the programmable logic of a ZCU104 (XCZU7EV) board, which acts as the ECU. There are two separate models, one for DoS attacks and one for Fuzzy attacks, both trained and tested on the Car Hacking dataset.

**Headline results**
- Latency: 0.12 ms per CAN frame, which the paper calls a 4.8x improvement over MTH-IDS on a Raspberry Pi 3 (0.574 ms).
- Throughput: "over 8300" messages per second at maximum payload. This fits 1/0.12 ms ≈ 8333.
- Power: 2.09 W, read from the device power rails with PYNQ-PMBus.
- Energy: 0.25 mJ per inference. This matches 2.09 W × 0.12 ms.
- Accuracy (Table I, as parsed): F1 99.99 and FNR 0.01 for DoS; precision 99.68, recall 99.93, F1 99.80 and FNR 0.07 for Fuzzy.

**Caveats**
1. **Latency comparison.** Table II mixes block-based detectors (29 to 5000 frames per decision, on GPU or Jetson) with per-frame ones. The authors themselves note that the block latencies leave out the time needed to collect the frames. So only the MTH-IDS comparison is like-for-like, and it runs on a different kind of platform.
2. **Power scope.** The 2.09 W was measured while the ECU was also running Linux and other tasks. It is not isolated accelerator power. It is also not stated whether it was measured for one model or for both. I recorded it as chip-level (device rails), but that is my reading.
3. **GPU energy figure.** The GPU reference of 9.12 J per inference is for a different 8-bit model on an A6000. It looks implausibly high and has no stated method, so the energy claim is not fully like-for-like.
4. **Accuracy table extraction.** Table I did not extract cleanly. Some baseline rows have missing or shifted cells: DCNN on DoS shows only 3 values, and TCAN-IDS on Fuzzy shows F1 99.22. Treat baseline numbers as unreliable.
5. **Missing details.** No LUT, DSP or BRAM counts are given, only "less than 4% of resources". Neither the MLP topology nor the clock frequency appears in these passages. The latency and throughput are reported once for "4-bit-QMLP", so assigning them to the Fuzzy model is an inference on my part.
6. **Metadata.** The metadata extraction was flagged ok:false and needs checking by hand.
