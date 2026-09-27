---
id: arxiv-2401.10724-real-time-zero-day-intrusion
fiche: done
date:
---

# Real-Time Zero-Day Intrusion Detection System for Automotive Controller Area Network on FPGAs

Shashwat Khandelwal, Shreejith Shanker, 2024, arXiv preprint. https://arxiv.org/abs/2401.10724
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

Khandelwal & Shreejith (arXiv 2401.10724, 2024) propose an unsupervised convolutional autoencoder IDS for automotive CAN. It is trained only on benign traffic and takes a window of 100 CAN IDs in binary as input. Its layers are 2 Conv2D (128, 64 filters) + 2 Conv2DTranspose (64, 128) + a sigmoid Conv2D output. Attacks are flagged when the reconstruction Hamming distance exceeds a threshold of 10, which was chosen on benign data. The model is quantised to 8 bits with Vitis-AI (QCAE) and runs on a Zynq UltraScale+ XCZU7EV DPU. The B4096 configuration was picked over B512 and B1152. Ping-pong buffers overlap inference with collecting the next window.

Reported results: an average accuracy of 99.61 on unseen DoS, fuzzing and RPM/Gear spoofing attacks from the Car Hacking dataset, and 0.43 ms per 100-message window. That is under the 1 ms it takes to fill a window at 100% high-speed CAN load. The paper also claims about 2x lower power than state-of-the-art IDSs.

Critical points:
1. The supplied passages give only table captions for Tables II–VII, so the per-attack accuracy, precision/recall/F1, DPU resource use and absolute power (W) are not available. LUT, DSP, BRAM and power fields are therefore n/r.
2. The 2x power claim cannot be checked without the numbers in Table VII.
3. The detection threshold was set on the benign test split, and each attack set is cut down to 200k messages. How the benign data was split and how this affects generalisation is unclear.
4. Detection happens per window, not per message. Worst-case detection latency therefore includes filling the window (up to about 1 ms), not just the 0.43 ms inference.
5. The only input feature is the CAN ID. Payload-only attacks that do not change the ID sequence may not be detected.
6. Comparisons with the literature mix platforms (GPU, CPU, FPGA) and metrics.

The extraction warnings (metadata and section detection) also apply.
