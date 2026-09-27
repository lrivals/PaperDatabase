---
id: arxiv-2505.08992-dataflow-tiling-strategies-edge-ai
fiche: done
date:
---

# Dataflow & Tiling Strategies in Edge-AI FPGA Accelerators: A Comprehensive Literature Review

Richie Li, 2025, arXiv preprint. https://arxiv.org/abs/2505.08992
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

Single-author survey on dataflow and tiling for edge-AI FPGA accelerators. It covers the WS/OS/RS/NLR taxonomy, compares MAESTRO and Timeloop, and reviews FINN, FINN-R, FlightLLM and SSR. The survey contributes no hardware results of its own. The only measured figures are secondary numbers in Table II, which it cites from [1]–[4], so both rows are low confidence and should be checked against the original papers.

Critical points:
(1) Metadata conflict: the record lists the author as "Richie Li", but the paper header says "Zhaoqin Li" (UC Irvine).
(2) The FINN entry in Table II looks inconsistent with the original FINN paper. It gives Zynq-7020, "~5 TOPS bin ops" and "~50k LUT (90%)", while the text says "10k+ fps on CIFAR-10" on "modest FPGAs" with no board named.
(3) The FINN-R throughput "50 TOPS (1 bit)" was lost as a section heading during extraction. The FINN-R row (VU9P, ~900k LUT, >100 GOPS/W) is incomplete, so no row was made for it.
(4) Several values are given in units the schema doesn't have and were not converted: FINN ~5 TOPS, FlightLLM ~55 tokens/s, and efficiency in GOPS/W (FlightLLM 300–400, SSR 246–453). SSR reports "up to 26.7 TOPS int8" on VCK190 with 394/400 AIEs, but it has no LUT/DSP figures, so it has no row.
(5) The MAESTRO/Timeloop 3×3 conv case study (ResNet-50, 256 PEs, about 5e5 vs 4.5e5 cycles, off-chip traffic 0.87 MB vs 440 MB) models a hypothetical accelerator. It is not a hardware measurement, so no row was made.
(6) The paper contradicts itself on Eyeriss: it calls it "OS-like", but also names it as the origin of Row-Stationary.
(7) The HLS/DSL/RTL overhead figures (+10–30% and +20–40% LUT/DSP; about 5× shorter design time) have no sources.
(8) Approximate values were written as bare numbers: "~50k LUT" became 50000 and "574k LUT" became 574000.
