---
id: arxiv-2206.11791-open-source-fpga-ml-codesign
fiche: done
date:
---

# Open-source FPGA-ML codesign for the MLPerf Tiny Benchmark

Hendrik Borras, Giuseppe Di Guglielmo, Javier Duarte, Nicolò Ghielmetti, Ben Hawks, Scott Hauck, Shih-Chieh Hsu, Ryan Kastner, Jason Liang, Andres Meza, Jules Muhizi, Tai Nguyen, Rushil Roy, Nhan Tran, Yaman Umuroglu, Olivia Weng, Aidan Yokuda, Michaela Blott, 2022, arXiv preprint. https://arxiv.org/abs/2206.11791
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

Borras et al. (MLSys 2022 / arXiv 2206.11791) describe MLPerf Tiny v0.7 open-division submissions built with hls4ml and FINN. The designs target the KWS, AD and IC tasks on a Pynq-Z2 (Zynq-7020 SoC) and an Arty A7-100T (Artix-7, the first FPGA-only submission). The flow covers quantization-aware training (QKeras, Brevitas), architecture search (Bayesian optimization and ASHA), automatic FIFO-depth sizing from RTL simulation, ReLU merging, BatchNorm folding and reuse-factor tuning.

Main measured claims (Abstract / preamble):
- Latency ranges from 30 ms down to 20 µs.
- Energy is as low as 30 µJ per inference.
- Accuracy/AUC is described as 'comparable' to the reference models.
- On Pynq-Z2, the hls4ml IC model uses 58% fewer BRAMs than FINN CNV-W1A1 but has 18.2x higher latency.

Critical points:
1. The Table 5 and Table 1 numbers (per-model latency, energy, resources, accuracy) were not supplied, so per-model hardware rows cannot be filled.
2. The 20 µs / 30 µJ figures are not tied to a specific model or board. They are in µs and µJ, so they were not converted into latency_ms or power_w.
3. The AD LUT count of 161228 (58.5% of Pynq-Z2 LUTs, reuse factor 144) comes from Vivado HLS logic synthesis (Table 4). It is a synthesis estimate, not a post-place-and-route or measured value.
4. The paper deliberately avoids comparing against other platforms.
5. The only accuracy figure given (92.2) is for the KWS DS-CNN reference model, not the FPGA design.
6. The AD dataset and AD quantization are not stated in the supplied passages.
7. Metadata extraction is flagged as unverified, and every passage except the Abstract is labelled '(préambule)'.
