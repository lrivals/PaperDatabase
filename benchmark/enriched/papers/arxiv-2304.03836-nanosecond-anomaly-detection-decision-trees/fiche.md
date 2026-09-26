---
id: arxiv-2304.03836-nanosecond-anomaly-detection-decision-trees
fiche: done
date:
---

# Nanosecond anomaly detection with decision trees and real-time application to exotic Higgs decays

Stephen Roche, Quincy Bayer, Benjamin Carlson, William Ouligian, Pavel Serhiayenka, Joerg Stelzer, Tae Min Hong, 2023, arXiv preprint. https://arxiv.org/abs/2304.03836
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

Roche et al. (arXiv 2304.03836) build an autoencoder-style anomaly detector for LHC first-level triggers from a forest of deep decision trees, using fwXmachina. The encoding and decoding are merged into one step the authors call a "★coder". The anomaly score is the L1 distance between the input and the per-bin median, summed over all trees. The design targets a Xilinx VU9P (xcvu9p-flga2104-2L-e) at 200 MHz with 8-bit integers (ap_int<8>). Table 1 gives 6 ticks = 30 ns latency and a 1-tick (5 ns) interval for both designs:
- **γγjj benchmark** (8 variables, 30 trees, depth 6): 63k LUT, 15k FF, 8 DSP, 0 BRAM.
- **LHC physics dataset** (56 variables, 30 trees, depth 4): 109k LUT, 15k FF, 56 DSP, 0 BRAM.

The baseline is the hls4ml DNN VAE PTQ 8-bit design from Govorkova et al. [77]: 80 ns, 35k LUT, 68 DSP, 13 BRAM. The paper says these baseline numbers were converted from published percentages.

**Accuracy:** only one AUC comes through cleanly: LQ80→bτ, 0.93 against the baseline's 0.92. For A50→4ℓ, h0→ττ and h±→τν, the extracted text keeps only the baseline values (0.94, 0.81, 0.94), so the paper's own AUCs are missing. The γγjj result is reported as TPR/FPR at a 3 kHz rate, with no single accuracy number in the passages.

**Critical points:**
- Latency is given in ns. To avoid converting units, latency_ms is n/r and the 30 ns is recorded in the baseline field.
- Throughput is given only as the 5 ns interval, so fps is n/r.
- No power figures are reported.
- The passages don't say whether the resource numbers are from HLS synthesis or post-implementation, or whether anything was measured on a board. Verification is described as C simulation and RTL co-simulation.
- The baseline was built for a different package and speed grade (flgb2104-2-e vs flga2104-2L-e).
- The two designs used different tool versions: Vivado 2019.2 for γγjj, Vitis 2022.2 for the LHC dataset.
- The 'percent-level resource usage' claim in the abstract is not backed by explicit percentages here: only the 0% BRAM cells are legible, and Table 1's other percentage cells (3%, 1%) are ambiguous in the extraction.
- The LHC dataset is preselected with a single-lepton trigger, which the authors say limits how far the result generalizes.
- LUT counts written as 63k and 109k in the paper are expanded to integers below.
