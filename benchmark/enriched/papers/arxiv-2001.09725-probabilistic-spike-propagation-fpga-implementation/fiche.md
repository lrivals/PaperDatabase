---
id: arxiv-2001.09725-probabilistic-spike-propagation-fpga-implementation
fiche: done
date:
---

# Probabilistic spike propagation for FPGA implementation of spiking neural networks

Abinand Nallathambi, Nitin Chandrachoodan, 2020, arXiv preprint. https://arxiv.org/abs/2001.09725
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

Critical reading note (based only on the supplied passages).

Claim: The paper treats a synaptic weight w_ij as the probability of passing a spike along that synapse (p_ij = w_ij/w_max, applied weight w_max; inhibitory synapses use w_min). Over time, the expected input matches the deterministic one (Eq. 1). Each neuron's outgoing weights are sorted and one random value is drawn per spike, so propagation can stop at a termination point. This cuts the number of weight and index reads. It works on pre-trained, converted SNNs without retraining. Five termination methods are compared: deterministic (DET), binary search (BS), random index (RI), weight-transform function (TR) and 5-segment piecewise linear (PWL). The benchmarks are MNIST1 (fully connected 784-1200-1200-10), MNIST2 (conv) and CIFAR10 (conv). The work targets a co-processor on the ARM core of a Xilinx Zynq, keeping part of the weights and indices in on-chip BRAM.

Evidence: Table 3 gives average memory accesses per spike (MAPS), normalised to DET, for different fractions of weights stored on-chip. The text says that with about 40% of weights on-chip, off-chip accesses fall "to very low levels". Table 4 shows probabilistic accuracy converging to DET as simulation steps increase. The authors say total memory accesses stay below DET even with the extra steps. The table cells themselves are missing from the extraction, so no MAPS or accuracy values can be copied.

Limitations: (1) The passages give no measured FPGA results: no LUT/DSP/BRAM use, clock rate, latency, throughput or power. The Zynq architecture (Fig. 4) is only described, and all gains are memory-access counts from simulation or analysis. (2) The energy benefit is inferred from a cited off-chip vs on-chip energy ratio [8], not measured. (3) Probabilistic methods need more simulation steps, which raises latency. The net benefit rests on the authors' access-count argument, and the passages give no numbers to check it. (4) RI performs poorly when weights are not uniformly distributed. TR only holds if the sorted weight distribution roughly satisfies f(f(x)) = x. (5) Accuracy is compared only with the converted deterministic SNN, never with the source ANN. (6) Weights and indices must be stored in sorted order, which may not suit other architectures. (7) The extraction flags unverified metadata and no detected sections; every passage except the Abstract is labelled "(préambule)".

Rows: None added. No passage reports a measured hardware result, and the accuracy and MAPS table values are absent, so any row would contain only n/r placeholders.
