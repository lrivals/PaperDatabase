---
id: arxiv-1901.00121-fpga-accelerators-deep-learning-networks
fiche: done
date:
---

# FPGA-Based Accelerators of Deep Learning Networks for Learning and Classification: A Review

Ahmad Shawahna, Sadiq M. Sait, Aiman H. El‐Maleh, 2018, arXiv preprint. https://doi.org/10.1109/access.2018.2890150
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

This paper is a survey (Shawahna, Sait, El-Maleh, IEEE Access 2018, arXiv 1901.00121). It reviews CNN compression, ASIC accelerators (the DianNao family, ISAAC, PRIME) and FPGA accelerators, from CNP and MAPLE through DC-CNN, nn-X, Caffeine, fpgaConvNet, ALAMO, FP-DNN and FINN/BNN, up to loop-optimized VGG-16 on Arria 10. It offers no new design or measurement of its own. Every hardware number is taken from a cited work, so each row below is a secondary citation. Before any use, check the value against the original paper ([152] for Microsoft/Catapult; the VC707 HLS design is described next to the Roofline accelerator [55]).

Critical points:
(1) The survey mixes units and power definitions across the works it cites: GFLOPS vs GOPS, 'about 25 W' vs 'total power 18.6 W'. It also mixes baselines (CPU, GPU, or other FPGA designs), so the speedup factors cannot be compared with each other.
(2) The summary tables (Tables 2–5) came through extraction as captions only, so their contents cannot be used here.
(3) The section headings were split badly: almost every passage, including Sections II–III, is labelled 'I. INTRODUCTION I'. The metadata is also flagged for manual verification.
(4) For the VC707 design, the passage names neither the model nor the numeric precision. GFLOPS suggests floating point, but this is not stated, so both are recorded as n/r.

Other secondary results that could fill later rows:
- VC709 accelerators: 424.7, 445.6 and 473.4 GOPS for LeNet, AlexNet and VGG-S.
- Arria 10 GX 1150, VGG-16: 645.25 GOPS.
- DeepBurning on Zynq-7045: 1.13x slower but 1.45x more energy-efficient than [55].
