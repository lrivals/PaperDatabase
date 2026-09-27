---
id: arxiv-1806.08085-inference-quantized-neural-networks-heterogeneous
fiche: done
date:
---

# Inference of Quantized Neural Networks on Heterogeneous All-Programmable Devices

Thomas B. Preußer, Giulio Gambardella, Nicholas Fraser, Michaela Blott, 2018, arXiv preprint. https://arxiv.org/abs/1806.08085
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

Preußer et al. (Xilinx Research, arXiv 1806.08085, 2018) describe how they built Tincy YOLO, a real-time Pascal VOC object detector that runs end to end on an embedded Zynq UltraScale+ XCZU3EG. The work is mainly an integration effort. Darknet gets a generic offload layer that calls a FINN HLS QNN accelerator in the PL. That accelerator is a single reused conv+pool engine, because only one generalized layer fits on the XCZU3EG. It runs the hidden layers with binary weights and 3-bit activations (W1A3). The float or 8-bit input and output layers run on the Cortex-A53 cores with NEON. The authors also change the topology: ReLU instead of leaky ReLU, different channel counts, and the first maxpool is removed so the first conv uses stride 2. Finally, a 4-thread pipelined demo mode is added. Measured progression: 0.1 fps with generic Darknet (10,030 ms per frame, hidden layers 9,160 ms). With the PL offload the hidden layers take 30 ms (more than 300x) and the system runs at just above 1 fps. After the topology changes it runs at more than 5 fps, and with pipelining at 16 fps. The paper claims 160x overall. Workload is about 4.445 G ops per frame for Tincy YOLO, compared with about 6.97 G for Tiny YOLO. Critical points: (1) The text says retraining kept the accuracy loss within 3%. Table IV shows Tiny YOLO float at 57.1 mAP and Tincy YOLO W1A3 at 48.5 mAP, a drop of about 8.6 points. This is either a mismatch or a different meaning of "3%". (2) Tables I and III show that precision is mixed: 8-bit or float at the input and output layers. It is not clear whether Table IV's numbers include that exact configuration. (3) The paper reports no power, energy, LUT/DSP/BRAM use, clock frequency or GOPS, so efficiency cannot be compared. GOPS could be worked out (about 4.445 G ops x 16 fps), but the paper does not state it, so it is left as n/r. (4) Neither the Pascal VOC split (2007 or 2012) nor the mAP protocol is given. (5) End-to-end latency at 16 fps is not reported. A pipeline adds latency, so 1/fps is not the latency. (6) The extraction flagged the metadata as needing a manual check. Tables arrived partly garbled, and the NEON section is cut off, so NEON-only speedups are missing.
