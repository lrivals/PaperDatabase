---
id: arxiv-2510.15672-evaluation-fast-machine-learning-algorithms
fiche: done
date:
---

# Evaluation of Novel Fast Machine Learning Algorithms for Knowledge-Distillation-Based Anomaly Detection at CMS

Lino Gerlach, Elliott Kauffman, Abhishikth Mallampalli, 2025, arXiv preprint. https://arxiv.org/abs/2510.15672
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

Critical reading note (based only on the supplied passages). CICADA is a CMS Level-1 Trigger anomaly detector. A convolutional autoencoder teacher (~300k parameters) is trained on 2017 Zero Bias CMS Open Data. Its behavior is transferred by knowledge distillation (MAE loss on the target Qlog = quantize(log(32·loss)), plus outlier exposure using ttbar→2l2ν) to a ~10k-parameter CNN student. The paper compares three ways of making the student cheap enough for hardware: QKeras quantization-aware training (the baseline), HGQ (bitwidths learned per weight, with an EBOPs term weighted by β and an L1 term with γ=1e-8, and β scanned), and a logic gate network (LGN, with architectures and input bit representations scanned). Physics performance is measured with EMD between teacher and student scores and with ROC AUC on the ttbar signals. Hardware cost comes from Vitis HLS synthesis on an AMD Virtex-7 XC7VX690T, reporting latency in clock cycles (1 cycle = 6.25 ns), DSPs, FFs and LUTs.

Caveats: (1) The hardware numbers are pre-place-and-route HLS estimates, not measurements on a board. The authors say place-and-route is still needed to get the real cost. (2) The Table 1 passage lists only row labels (QKeras, HGQ-1E-5, HGQ-1E-4, HGQ-mixed, LGN-LT2) and column names. No numeric values were extracted, so none of the claimed resource savings can be checked here. (3) No ROC AUC or EMD values appear in the passages. The claim of "comparable performance with significantly reduced resources" therefore cannot be quantified. (4) "Sub-200 ns" is a design target or bound for the deployed model, not a per-model measured value. (5) The signal samples are limited to ttbar channels, which are the only ones available in Open Data. This limits how well the results generalize to realistic new-physics signals. (6) Convolutional LGNs have not been synthesized yet. (7) The metadata warnings (extraction ok=false, axes inferred automatically) mean the metadata should be checked by hand.

Rows: none. The instructions require a row only for a measured hardware result, and there is none. The only hardware figures are HLS estimates, and their numbers are missing from the extracted table. Re-extract Table 1 from the PDF to fill in the rows.
