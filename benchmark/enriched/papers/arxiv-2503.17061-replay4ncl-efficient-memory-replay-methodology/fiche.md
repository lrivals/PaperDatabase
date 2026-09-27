---
id: arxiv-2503.17061-replay4ncl-efficient-memory-replay-methodology
fiche: done
date:
---

# Replay4NCL: An Efficient Memory Replay-based Methodology for Neuromorphic Continual Learning in Embedded AI Systems

Mishal Fatima Minhas, Rachmad Vidya Wicaksana Putra, Falah Awwad, Osman Hasan, Muhammad Shafique, 2025, arXiv preprint. https://arxiv.org/abs/2503.17061
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

Replay4NCL (DAC 2025; arXiv 2503.17061) builds on SpikingLR [25], a latent-replay neuromorphic continual learning (NCL) method. It runs a 4-layer recurrent SNN (700 inputs → 200 → 100 → 50 → 20 classes) on the SHD dataset with fewer timesteps (100 → 20 in the case study). To make up for having fewer spikes, it adjusts the threshold potential Vthr (spike-timing-based or sigmoid schedule) and uses a learning rate for the CL phase of η_cl = η_pre/100. It compresses the latent replay (LR) data and inserts it at a chosen layer. The authors claim, against SpikingLR: old-task Top-1 accuracy of 90.43 vs 86.22, 4.88x latency speed-up, 20% latent-memory saving and 36.43% energy saving.

Critical points:
(1) The only hardware is a GPU running a Python implementation (the paper says 'Nvidia RTX 4090 Ti', which is not a standard product name). It has no neuromorphic or FPGA deployment and no power measurement. The paper does not explain how energy was obtained, and latency and energy appear only as values normalized to SOTA, with no absolute ms or J.
(2) The headline numbers don't match the figure results. The body reports up to 2.34x speedup across LR insertion layers but the abstract says 4.88x, and energy saving is up to 56.7% across layers but 36.4% at layer 3. At LR insertion layer 3 (50 epochs), Replay4NCL is actually lower than SpikingLR on old tasks (88.24 vs 90.19) and new tasks (67.19 vs 71.88). The 90.43 vs 86.22 headline appears to come from a different setting that isn't stated, possibly the 150-epoch run in Fig. 13.
(3) Memory saving is 20–21.88%, which is modest given the 5x timestep reduction.
(4) Only one dataset and one small network are evaluated, with no variance reported.

Row 1 holds the abstract's headline claim. Row 2 holds the per-configuration result at LR layer 3. Neither passage reports FPGA resources, GOPS, FPS or absolute power.
