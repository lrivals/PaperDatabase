---
id: arxiv-2507.07903-hardware-aware-feature-extraction-quantisation
fiche: done
date:
---

# Hardware-Aware Feature Extraction Quantisation for Real-Time Visual Odometry on FPGA Platforms

Mateusz Wasala, Mateusz Smolarczyk, Michal Danilowicz, Tomasz Kryjak, 2025, arXiv preprint. https://arxiv.org/abs/2507.07903
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

Quantised SuperPoint for visual odometry on Zynq UltraScale+. The authors deploy it in two ways. The first uses Vitis AI with the INT8 DPU (DPUCZDX8G B4096) on the Kria KV260. The second uses Brevitas and FINN at low bit-widths (8, 4 and 3 bits, plus a mixed 4-2-4 variant) on the KV260 and the ZCU102. Unlike earlier FPGA SuperPoint work (FCCM'20, TCASI'22, APCCAS'24), they keep the original network architecture unchanged. The two FINN builds reach 27 FPS on the KV260 and 54 FPS on the ZCU102 at 640×480. The rows below cover only these two measured FINN builds.

Critical points:
1) Power figures are estimates from the Vivado Power Analysis tool, not board measurements. Total power is 3.307 W and 4.607 W, and the PS accounts for most of it. The DPU power (2–4 W) and the DPU's LUT/DSP/BRAM figures come from documentation, not from a post-implementation report.
2) The text of Table IV is garbled in the extraction. Matching 3.307 W to the KV260 build and 4.607 W to the ZCU102 build is inferred from column order. Frequency, latency and DSP/BRAM values for the FINN builds cannot be recovered.
3) The passages never state which bit-width the deployed FINN builds used. The mixed INT 4-2-4 variant is only implied by Table I. Accuracy numbers from Tables I and V are also not recoverable, except the APE figures quoted in the text. Those are for TUM: FP32 is 7.61°/0.31 m, INT8 is 9.39°/0.38 m, INT4 is 10.41°/0.36 m, and INT3 has a rotation error of 12.24°. The mixed 4-2-4 variant has the largest trajectory error.
4) The comparison with prior work mixes different frameworks, boards and resource-accounting methods, so the 'outperforming state of the art' claim deserves caution.
5) The DPU at INT8 reaches 58.6 FPS. The truncated passage suggests this is on the KV260, but the configuration and resolution are unclear, so no row was created for it. The quantised network also detects 10–15% fewer feature points than the full-precision version.
