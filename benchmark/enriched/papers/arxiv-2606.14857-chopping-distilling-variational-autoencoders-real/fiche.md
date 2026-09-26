---
id: arxiv-2606.14857-chopping-distilling-variational-autoencoders-real
fiche: done
date:
---

# Chopping and distilling variational autoencoders for real-time anomaly detection in high energy physics

Max Cohen, Rajat Gupta, Sterre Hoogendoorn, Sergey Scoville, Tae Min Hong, Dylan Sheldon Rankin, 2026, arXiv preprint. https://arxiv.org/abs/2606.14857
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

The paper compares two ways to shrink VAE anomaly-detection triggers, and combines them. "Chopping" scores events using only the encoder's latent space. Knowledge distillation (KD) trains small NN or BDT student models to reproduce the teacher's anomaly score. Target: Alveo U250 (xcu250-figd2104-2L-e). NN students go through hls4ml and Vivado 2023.2; BDT students go through fwXmachina.

Hardware results in the supplied passages (40 MHz dataset, post-training quantization, bit widths not given):
- Large NN student: 18.32% of the LUTs and 2.04% of the registers of one SLR (a single chip region), 40 ns latency.
- Medium NN student: 6.92% LUTs, 0.64% registers, 20 ns.
- Small NN student: under 1% of resources, 5 ns.
- BDT student: under 1% of resources, 10 ns latency, 5 ns initiation interval.
- No student uses any DSPs.

Caveats:
1. The resource and latency numbers are synthesis estimates, not on-board measurements. Power is not reported.
2. Resources are given as percentages of one SLR, not absolute counts. The LUT values in the rows are those percentages.
3. Latencies are in ns. The rows put n/r in latency_ms to avoid converting units; the ns values are listed above.
4. The Jet Images performance numbers are explicitly from floating-point models. For the 40 MHz dataset, the passages don't say whether efficiency and AUC were measured before or after quantization, so it is unclear whether the accuracy numbers reflect the synthesized models.
5. Chopping has a real cost on A→4ℓ: signal efficiency at FPR = 1e-3 falls from 3.7 (MSE) to 1.5 (KL), and AUC from 0.937 to 0.838.
6. Student results don't scale with size. The small student (ε = 2.4, AUC 0.847) beats the large one (ε = 1.2, AUC 0.786), and the medium student is poor (AUC 0.645). Results also vary by signal; the authors flag this themselves.
7. The Table 1 values were not in the supplied passages. The only other figure given is H±→τν efficiency across methods (6.9–10.0).
