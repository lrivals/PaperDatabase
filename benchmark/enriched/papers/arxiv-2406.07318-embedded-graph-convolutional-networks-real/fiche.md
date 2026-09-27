---
id: arxiv-2406.07318-embedded-graph-convolutional-networks-real
fiche: done
date:
---

# Embedded graph convolutional networks for real-time event data processing on SoC FPGAs

Kamil Jeziorek, Piotr Wzorek, Krzysztof Błachut, Andréa Pinna, Tomasz Kryjak, 2026, arXiv preprint. https://doi.org/10.1016/j.sysarc.2026.103850
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

EFGCN (Jeziorek et al., arXiv 2406.07318) is a hand-written SystemVerilog pipeline for graph convolutional networks on event-camera data. It runs on the ZCU104 board (XCZU7EV-2FFVC1156) at 200 MHz. Feature extraction runs in the programmable logic (PL). The linear classifier head runs on the ARM processor (PS). All weights and feature maps stay in on-chip memory (BRAM, URAM and distributed RAM), so no off-chip DRAM is used. Main design choices: directed graph generation using a neighbourhood matrix of β×β entries with radius R=3, a first convolution that processes each event as it arrives, a 4×4×4 3D MaxPool that turns later layers into synchronous processing of 'temporal channels', and memory buffers shared between layers. Graph generation needs 15 clock cycles per event, and this is the bottleneck. The resulting throughput is 13.3 million events per second (MEPS). This figure was first estimated analytically and then confirmed in simulation. It was not reported as measured on the board. A new prediction is produced every TIME_WINDOW/4, covering the most recent TIME_WINDOW of events. Two configurations are supported: β=128 with a 100 ms window and β=256 with a 50 ms window. Software ablations on N-Cars with the Base model: 3D MaxPool adds about 0.3–0.4% accuracy over 2D pooling, and 'divide position' costs about 0.1–0.2%. Removing pooling multiplies the operations in later convolutions by about 50. Swapping in their modules shrinks AEGNN from 30.4k to 5.0k parameters and EvGNN from 4.8k to 4.2k, with slightly better accuracy in both cases. With quantisation-aware training (QAT), 6-bit quantisation cuts model size by about 23% with little accuracy loss. 4-bit quantisation loses considerable accuracy. The hardware targets 8-bit. Going from 8 to 6 bits reduces memory and LUT/FF usage, but DSP usage stays the same because DSPs only do the 32-bit requantisation. Limitations: the supplied passages contain only the captions of Tables 7 and 8. The actual LUT/DSP/BRAM counts, latency, power and accuracy numbers are missing, so the row below holds mostly n/r. Throughput is given in events per second, not FPS or GOPS. The authors also admit that FLOPs per event does not fully capture FPGA implementation cost. For testing, events were replayed from an SD card, with a DVS camera connected to the PL also demonstrated. Values to check against the full paper: Table 7 (resource use, accuracy and latency compared with state-of-the-art FPGA work) and Table 8 (scalability as the number of multipliers m changes, at 8 and 6 bits).
