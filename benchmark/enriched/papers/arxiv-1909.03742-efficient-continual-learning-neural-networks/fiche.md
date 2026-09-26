---
id: arxiv-1909.03742-efficient-continual-learning-neural-networks
fiche: done
date:
---

# Efficient Continual Learning in Neural Networks with Embedding Regularization

Jary Pomponi, Simone Scardapane, Vincenzo Lomonaco, Aurelio Uncini, 2019, arXiv preprint. https://arxiv.org/abs/1909.03742
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

Critical reading note — Pomponi, Scardapane, Lomonaco, Uncini (arXiv 1909.03742, preprint submitted to Neurocomputing). This is a continual-learning (CL) algorithm paper, not a hardware paper. Contribution: Embedding Regularization (ER). It regularizes the second-to-last-layer embeddings of samples from past tasks, kept in a small external memory, using cosine dissimilarity. A dynamic distance-based sampling strategy fills that memory. ER is compared with GEM, online EWC, SI and an unregularized baseline. Both standard ANNs/CNNs and Kafnets (networks with trainable kernel activation functions) are tested.
Setup (section 4): Permuted MNIST with 4 tasks, using an MLP with 4 hidden layers of 400 ReLU units trained by SGD at lr 1e-3. CIFAR10 split into 5 tasks and CIFAR100 split into 10 tasks, using the CNN from [31] (kernels doubled for CIFAR100) trained by Adam at lr 1e-3. Kafnets have layers/kernels 30% smaller. Memory per task: 100 for ER versus 200 for GEM (500 for GEM on CIFAR100). λ = 1, or 5 on CIFAR100. Metrics are Accuracy, Remembering (1 − |min(0, BWT)|) and Positive BWT, all computed from the accuracy matrix R.
Claims (section 5): ER matches or beats GEM on accuracy and remembering, except on MNIST where GEM is better. Kafnets generally hurt CL. A Friedman test gives p = 0.01, and Nemenyi tests show ER differs significantly from the baseline, SI and EWC, but GEM is not in that list. On CIFAR10, ER takes about half of GEM's training time and scales better with the number of tasks because it avoids a per-step QP. Growing the memory raises training time from 10 to 20 seconds for both methods. ER peaks at about 100 samples per task, while GEM keeps improving with more memory. Distance-based sampling beats iid, usage-based and image-similarity sampling.
Caveats: The numbers in Table 1 are not in the supplied passages; only the caption and the text discussing it are. The fragment '2,266 / 4,456 / 2,040 / 1,050 / 1,500' next to the dataset names is unlabeled and cannot be attributed to a method or unit. Timing results come from figures, with no hardware platform, batch size or per-inference latency given. The accuracy formula shows a 2N(N+1) denominator that looks garbled by text extraction. The metadata is flagged for manual checking.
Rows: none. None of the supplied passages reports a measured hardware result (FPS, GOPS, latency, power, LUT/DSP/BRAM) on any platform. The only timing (10–20 s training time) is a software training-time observation on unspecified hardware. It does not fit the benchmark columns, and the per-method accuracy and remembering values are not available in the passages.
