---
id: arxiv-2102.01341-benchmarking-quantized-neural-networks-fpgas
fiche: done
date:
---

# Benchmarking Quantized Neural Networks on FPGAs with FINN

Quentin Ducasse, Pascal Cotret, Loïc Lagadec, Robert Stewart, 2021, arXiv preprint. https://arxiv.org/abs/2102.01341
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

Ducasse et al. (arXiv 2102.01341, SLOHA 2021) use Brevitas and FINN to benchmark a small 3-FC-layer MLP with HardTanh activations on Fashion-MNIST, with images resized to 32x32. They trained 49 weight/activation bit-width combinations from 2 to 8 bits. Only the equal-bit-width networks were deployed to a Pynq-Z1 (Zynq Z-7020), all with the same folding. A8W8 was not implemented, and A4W4 at PE/SIMD 16/16 did not fit on the board.

Main findings:
- Weight bit-width drives accuracy more than activation bit-width.
- Longer training closes the gap: 2-bit weights reach the error rate at 100 epochs that 8-bit weights reach at 40.
- BRAM use grows exponentially with activation bit-width because FINN uses threshold-based activations (2^k−1 thresholds).
- Throughput depends only on PE/SIMD, not on bit-width (A2W2, A3W3 and A4W4 are nearly identical).

Limitations and cautions:
- **Weak benchmark:** The model is a toy MLP with fixed, untuned folding. The paper reports no power, latency, clock or absolute LUT/DSP/BRAM figures in the text (resources are only in Figures 9 and 10, which were not supplied).
- **Accuracy not tied to a configuration:** "reaches 88%" is a general statement, not linked to any deployed configuration, so accuracy_value is n/r.
- **"62 times faster" claim:** This compares the PE/SIMD 16/16 and 2/2 settings (373,112/6,100 ≈ 61.2), so it measures parallelism, not quantization. The text says it comes from the compressed network being better parallelized.
- **Internal inconsistencies:**
  - The A2W2 8/8 throughput is printed as "96,5334" (likely 96,533).
  - The text says both "49" and "64" implementations.
  - The conclusion says MNIST and Fashion-MNIST, but the experiments describe only Fashion-MNIST.
- **Throughput measurement:** Throughput comes from FINN's remote test with a batch of 10,000. DRAM-in bandwidth was 382.06 Mb/s (A2W2) and 381.82 Mb/s (A3W3) at 16/16.
- **Metadata:** Extraction warnings say the metadata needs manual checking.
