---
id: arxiv-2604.08336-leveraging-complementary-embeddings-replay-selection
fiche: done
date:
---

# Leveraging Complementary Embeddings for Replay Selection in Continual Learning with Small Buffers

Danit Yanowsky, Daphna Weinshall, 2026, arXiv preprint. https://arxiv.org/abs/2604.08336
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

MERS (Multiple Embedding Replay Selection; Yanowsky & Weinshall, arXiv 2604.08336) changes how replay-based class-incremental learning picks exemplars for its buffer. It combines a supervised embedding with a self-supervised one (SimCLR, VICReg or DINOv2) in one weighted multi-group maximum k-coverage objective. It comes in two variants, MERS ProbCover and MERS MaxHerding. Per-embedding RBF bandwidths use the median heuristic. Per-embedding weights come from a k-NN density ratio. Because the objective is monotone submodular, greedy selection keeps the (1-1/e) approximation guarantee. The paper tests MERS with ER, ER-ACE and ER-ACE-STAR on Split CIFAR-100 (buffer 100-1000) and Split TinyImageNet (buffer 200-6000). Baselines are Random, Herding, Rainbow Memory, TEAL, ProbCover and MaxHerding. Reported metrics are FAA (final average accuracy) and AAA (average accuracy across all tasks). The authors claim MERS is best across buffers, replay methods and datasets, with the largest gains at 1000 exemplars or fewer, where the gap narrows as the buffer grows. They also say stability is higher and forgetting lower. A theoretical argument (equal-volume Gaussian proxies with a KL gap, framed as domain adaptation) says self-supervised geometry should make selection more robust to new classes.

Critical points:
(1) The table extracts for Tables 1 and 2 (CIFAR-100, ER-ACE-STAR and ER-ACE) have lost their column headers. For example, the |M|=1000 row of Table 1 reads 60.03 / 64.17 / 63.92 / 65.54 / 61.50 / 64.05, with max 65.54, but no value can be tied to a method. The bold-face marking of the best result was also lost. So the headline claims cannot be checked from these passages.
(2) The main FAA results are only in figures (Figs. 2-4), and the full tables are in appendices that were not supplied.
(3) The self-supervised encoder is retrained from scratch every episode, or DINOv2 is used as a frozen, externally pretrained model. The claim of "no added model parameters" hides this compute and memory cost, and DINOv2 brings in outside pretraining data. No selection runtime is reported.
(4) The theory relies on stylized Gaussian proxies, not on measured embedding statistics.
(5) The text says "Herding (Welling, 2009...)" but also credits ProbCover to Bae et al. rather than Yehuda et al. This looks like a citation slip.

No hardware or FPGA measurements appear (no FPS, GOPS, latency, power or resource use). This is a pure algorithmic continual-learning paper and does not fit the hardware benchmark schema. No rows are given: the only numbers are accuracies that cannot be tied to a method, and turning them into rows would mean guessing which method each belongs to.
