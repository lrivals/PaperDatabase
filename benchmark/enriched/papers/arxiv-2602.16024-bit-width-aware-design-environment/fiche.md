---
id: arxiv-2602.16024-bit-width-aware-design-environment
fiche: done
date:
---

# Bit-Width-Aware Design Environment for Few-Shot Learning on Edge AI Hardware

R. Kanda, H. L. Blevec, N. Onizawa, M. Leonardon, V. Gripon, T. Hanyu, 2026, arXiv preprint. https://arxiv.org/abs/2602.16024
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

Kanda et al. replace the Tensil-based PEFSL flow with FINN so that a ResNet-9 few-shot backbone (EASY method with an NCM classifier on the CPU) can run at arbitrary fixed-point bit-widths on a PYNQ-Z1 (Zynq Z-7020) at 125 MHz. They customized the FINN build in three ways: the Streamline and Convert-to-HW-Layer steps, Transpose handling between NCHW and NHWC (AbsorbTransposeIntoMultiThreshold), and converting reduce-mean to GAP through GlobalAccPool plus a Mul node.

Reported results:
- **Accuracy:** 6-bit conv weights (1 integer + 5 fractional bits) with 4-bit activations (2+2) reach 59.70 on CIFAR-10 5-way 5-shot, against 62.78 for the conventional 16-bit version. That is a drop of about 3 points, so the claim that accuracy is "the same" as the conventional version is overstated. The backbone was trained on MiniImageNet resized to 32x32.
- **Hardware:** backbone latency 16.3 ms and 61.5 fps.
- **Speed claim:** "approximately twice as fast" as PEFSL/Tensil. The baseline latency is not given clearly in the extracted text.

Caveats:
- **Table III is garbled in extraction.** For the FINN version, the recovered values are LUT 37263, BRAM 131.5 (36Kb blocks), FF 44617 and latency 16.3. No DSP value could be recovered, even though the text says FINN uses fewer DSPs. For the PEFSL baseline, the values 15667 and 35.9 cannot be matched to columns reliably, so no baseline row was made.
- **Latency and fps cover the backbone only.** The NCM classifier and feature transfer run on the CPU and are excluded.
- **No power or GOPS figures are reported.**
- **Source of the accuracy numbers is unclear.** It is not stated whether Table II accuracies were measured on the board or in quantized simulation.
- **Limited evaluation:** one model, one board, one bit-width configuration deployed.
