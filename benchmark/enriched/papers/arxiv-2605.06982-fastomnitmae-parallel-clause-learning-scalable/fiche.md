---
id: arxiv-2605.06982-fastomnitmae-parallel-clause-learning-scalable
fiche: done
date:
---

# FastOmniTMAE: Parallel Clause Learning for Scalable and Hardware-Efficient Tsetlin Embeddings

Ahmed K. Kadhim, Lei Jiao, Rishad Shafik, Ole-Christoffer Granmo, Mayur Kishor Shende, 2026, arXiv preprint. https://arxiv.org/abs/2605.06982
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

FastOmniTMAE changes how Omni TM-AE (a Tsetlin Machine autoencoder for static word embeddings) is trained. It removes the global class_sum/weight step, so clauses can be evaluated and updated in parallel and locally. It also adds a custom HDL IP accelerator (AXI-Lite control, AXI-MM DDR access, BRAM buffers, FSM) for Zynq-7000 (Zybo) and Zynq UltraScale+ (ZCU104).

**Results (Table 2):** on RG65 with 44 tokens, 8,000 examples per token, 32 clauses, T=20000 and s=1.0, the training times were:
- ZCU104 with 12 engines: 119.9±0.9 s, versus 848.7 s on its single ARM core (7.08×), with RG65 ρ=0.696.
- Zybo with 2 engines: 657.4±1.1 s, versus 3667.5 s on its ARM core (5.58×), with ρ=0.669.

**Limitations:**
1. Speedups are only measured against a single embedded ARM core. A single-threaded Core i9 CPU (57.7 s) and the H100 host CPU (87.3 s) are both faster than the ZCU104 FPGA.
2. No power, energy, clock frequency or LUT/DSP/BRAM figures appear in these passages; resource use is deferred to Appendix A.4, which was not supplied. Claims of a "small footprint" and "lower power" are therefore not quantified here.
3. The FPGA RG65 ρ values (0.696 and 0.669) are higher than the DGX CPU result in Table 1 (0.656), but the setups differ (8,000 vs 2,000 examples per token), so they cannot be compared directly.
4. Other claims:
   - The GPU slowdowns (CUDA 0.18×, OpenCL 0.22–0.29×) are explained as a mismatch between GPU architecture and the TM's logic operations. The passages do not include profiling to support this.
   - The DGX CPU speedup over Omni TM-AE is only 1.2× (242.9 s vs 293.1 s). The abstract's "up to 5×" figure is for classification and is not visible in these passages.
   - It is a preprint, and the benchmark code has not been released yet.

Training times are reported in seconds, so they are not entered in latency_ms, which is left as n/r.
