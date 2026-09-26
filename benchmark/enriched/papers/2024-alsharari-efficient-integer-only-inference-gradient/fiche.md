---
id: 2024-alsharari-efficient-integer-only-inference-gradient
fiche: done
date:
---

# Efficient Integer-Only-Inference of Gradient Boosting Decision Trees on Low-Power Devices

Majed Alsharari, Son T. Mai, Roger Woods, Carlos Reaño, 2024, IEEE Transactions on Circuits and Systems I Regular Papers. https://doi.org/10.1109/tcsi.2024.3446582
Type : n/r

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

Critical reading note: the paper trains CatBoost GBDT models with quantisation-aware training (QAT) for integer-only and binary inference. Models are exported through Conifer v1.4 and Vitis HLS 2023.1, then placed and routed with Vivado 2023.1 on a Kria KV260 (Zynq UltraScale+ MPSoC, xck26-sfvc784-2LV-c). They are tested on two tasks: network intrusion detection (UNSW-NB15, binarised following LogicNets) and jet substructure classification (JSC; 16 inputs, 5 classes).

Caveats:
(1) The contents of Tables I–IV are missing from the passages; only their captions are supplied. Both rows therefore rely on figures quoted in the prose of Section VI.
(2) Hardware numbers are Vivado out-of-context (OOC) results after synthesis or place-and-route, with II=1. They are not on-board measurements. Power is a Vivado estimate of dynamic power only, plus a static 288 mW for every design. The quoted 17 mW and 69 mW are in mW, and the power_w field is in watts. Because the rules forbid unit conversion, power_w is n/r.
(3) The 1.38 ns latency is a single clock period at 724 MHz. It is given in ns, not ms, so latency_ms is n/r. The FPS equivalent at II=1 is not stated explicitly and has not been derived.
(4) The frequency is inconsistent in the text: it says both 725 and 724 MHz. Table III reports an Fmax of 1013 MHz from synthesis, but the deployable clock is capped at about 724 MHz.
(5) Baseline numbers for LogicNets, Murovic et al., PolyLUT and Summer et al. are partly taken from the cited papers and partly re-run by the authors. The comparisons also mix accuracy (Table IV) with AUC (Fig. 6).
(6) In the NID row, 170 LUTs and 233 FFs are the best design reported in the abstract. The JSC LUT count is not given in the prose.
(7) The ensemble sum is fixed at 32-bit, so 'binary' covers the tree decisions only. DSP and BRAM use is not reported, and the LUT-only mapping suggests it is probably zero, but this is unverified.
