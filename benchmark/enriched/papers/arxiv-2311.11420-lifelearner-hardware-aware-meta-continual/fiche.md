---
id: arxiv-2311.11420-lifelearner-hardware-aware-meta-continual
fiche: done
date:
---

# LifeLearner: Hardware-Aware Meta Continual Learning System for Embedded Computing Platforms

Young D. Kwon, Jagmohan Chauhan, Hong Jia, Stylianos I. Venieris, Cecilia Mascolo, 2023, arXiv preprint. https://arxiv.org/abs/2311.11420
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

LifeLearner (SenSys'23) proposes rehearsal-based meta continual learning. It combines three parts: (1) inner-loop and outer-loop updates at deployment time; (2) latent replay from the frozen feature extractor's last layer, compressed with a sparse bitmap and product quantization (PQ); (3) an INT8 feature extractor (QNNPACK on Jetson Nano and Pi 3B+, TFLM on STM32H747), with a custom Eigen-based backprop engine for the classifier on the MCU. There is no FPGA or accelerator design, so the LUT, DSP and BRAM columns do not apply.

Critical points:
- The headline gains (178.7x memory, 80.8-94.2% latency and 80.9-94.2% energy reduction) are measured against ANML+AIM. That baseline is very heavy and often runs out of memory on Jetson Nano. Against Oracle, compression is only 2.5-3.5x.
- LifeLearner is slower than plain ANML on the same architecture: 415 s vs 343 s end-to-end on CIFAR-100 on Nano. On the MCU, Tiny LifeLearner takes 832 ms vs 579 ms for Tiny ANML (CIFAR-100). The cost of compression is only partly offset by INT8.
- Power is never reported directly. Energy is Tegrastats power multiplied by elapsed time (Nano CIFAR-100: 1.9 kJ vs 32.7 kJ for ANML+AIM). So power_w is n/r.
- The Nano end-to-end latency is given in seconds (415 s). Converting it would be needed to fill latency_ms, so that field is left n/r.
- In the supplied text, Table 3 has no dataset labels. The first block is read as CIFAR-100 because the prose cites 579 ms vs 561 ms for CIFAR-100.
- The prose gives a Tiny LifeLearner SRAM range of 181-281 kB. The 181 kB figure is Tiny ANML's GSCv2 value; Tiny LifeLearner's table minimum is 212 kB. This is an internal inconsistency.
- The passages do not give accuracy values for Table 3 or Figure 5, so accuracy is n/r. Only relative claims are made: within 2.8% of Oracle, and 4.1-16.1% better than other meta continual learning methods.
- MCU memory is SRAM 236 kB and Flash 825 kB. These are not FPGA BRAM, so the bram field is n/r.
