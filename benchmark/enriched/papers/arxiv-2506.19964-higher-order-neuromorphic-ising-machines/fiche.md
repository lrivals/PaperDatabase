---
id: arxiv-2506.19964-higher-order-neuromorphic-ising-machines
fiche: done
date:
---

# Higher-Order Neuromorphic Ising Machines -- Autoencoders and Fowler-Nordheim Annealers are all you need for Scalability

Faiek Ahsan, Saptarshi Maiti, Zihao Chen, Jakob Kaiser, Ankita Nandi, Madhuvanthi Srivatsav, Johannes Schemmel, Andreas G. Andreou, Jason Eshraghian, Chetan Singh Thakur, Shantanu Chakrabartty, 2025, arXiv preprint. https://arxiv.org/abs/2506.19964
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

Critical reading note (from the supplied passages only).

What the paper is: a higher-order neuromorphic Ising machine. It uses an 'autoencoder' structure in which clause outputs Tk are projected onto latent spin neurons (encoder, weights diag(J)H^T) and then reconstructed back into clauses (decoder). Latent thresholds are annealed with an emulated Fowler-Nordheim (FN) schedule tau(t)=tau0/log(1+t/C). Graph colouring (DSATUR or greedy) allows parallel updates. The main claim is that resource complexity does not depend on interaction order (O(n^2) dense; n*q + m*p sparse). Quadratized second-order solvers need auxiliary spins and couplings with more precision and range.

Axis caveat: the 'autoencoder' is a fixed, problem-derived mapping (H, J), not a trained neural network. It has no learned weights and no reconstruction-loss training. Tagging this paper under autoencoder-fpga is questionable and should be checked by hand in /paper-fiche.

Hardware evidence:
- The graph-coloured variant runs on an FPGA with a PS/PL split driven through PYNQ, an AXI DMA IP, 16-bit noise samples streamed from the PS (one sample per clock) and a 100 MHz clock.
- The FPGA part, LUT/DSP/BRAM usage and power are not given in these passages (they are deferred to SI S8).
- The only concrete measured numbers are for MAX-3SAT size 250 at the fastest schedule: median TTS97 = 0.34 us and median TTS99 = 0.89 us. The passage also claims a 2500-3000x speed-up over a CPU emulating 16-bit noise, but the sentence is cut off.

Concerns:
1. Units: at 100 MHz, 0.34 us is only about 34 clock cycles for a 250-variable instance (about 1065 clauses). That is implausibly short and may be a unit typo or a count that excludes some cycles. Check it against Fig. 4.b/c and SI S9.
2. The latency_ms field is left as n/r because the source value is in us and unit conversion is not allowed. The raw us values are in the baseline field.
3. TTS is a median with failures assigned a large value. The error bars run from the 6th to the 94th percentile. Results come from a single instance per size (the first satisfiable SATLIB instance) with 100 trials each.
4. The MAX-CUT FPGA comparison (G4/G11/G15 against dSBM, Fig. 2.c) is cut off in these passages, so no numbers were extracted.
5. The higher-order vs second-order comparisons (Fig. 3; 250-variable instances fully satisfied) and the MAX-5SAT/7SAT results (>99% of clauses satisfied after 10^8 iterations) come from CPU simulations, not hardware.
6. Energy-to-solution is not reported. The FN annealer is emulated digitally, and its noise is generated on the PS rather than on the chip.
