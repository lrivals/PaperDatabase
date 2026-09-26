---
id: arxiv-2205.13384-continual-learning-visual-search-backward
fiche: done
date:
---

# Continual Learning for Visual Search with Backward Consistent Feature Embedding

Timmy S. T. Wan, Jun-Cheng Chen, Tzer-Yi Wu, Chu-Song Chen, 2022, arXiv preprint. https://arxiv.org/abs/2205.13384
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

CVS (Continual-learner for Visual Search) targets continual learning for image retrieval. The main requirement is backward-consistent embeddings: gallery features extracted in earlier sessions are never re-extracted. Training combines three losses. Lc is an NSoftmax intra-session discrimination loss (T=0.05). Lm is a neighbor-session model-coherence loss, a 2-sample-3-embedding triplet distillation from the previous model (margin 0.1, α=10). Ld is an inter-session data-coherence loss that pulls current embeddings toward class means built from replayed old embeddings and data (β=1). The paper evaluates disjoint, blurry and a new general-incremental setup (new and old classes mixed per session). Datasets are CIFAR100 and Tiny ImageNet with ResNet-18, and Stanford Dog, iNat-M and Product-M with ResNet-50 and ImageNet pretraining. Embeddings are 128-d, the replay buffer is budget-limited (600 to 4,000 samples), and the metric is recall@K averaged over sessions (AR@K). On CIFAR100, CVS reaches AR@1 of 71.47 (disjoint), 47.47 (blurry) and 73.95 (general). These beat all compared continual-learning methods (Rainbow, RWalk, EWC, LWF, MMD, BCT) but stay well below the Joint Train upper bound (83.39, 55.10, 81.97).

Critical points:
(1) There are no hardware, latency, throughput or power measurements. The efficiency claim (avoiding gallery re-extraction) is argued, not measured, so every hardware field is n/r.
(2) Most baselines are classification continual-learning methods adapted with NSoftmax. BCT was given the authors' own exemplar mining. The comparison fairness depends on these re-implementations.
(3) The gap to the upper bound widens as sessions grow, especially in the blurry setup, as the authors admit. At AR@4 the margins shrink or tie (Tiny ImageNet general, Stanford Dog).
(4) Model selection uses best validation recall@1 from a split sampled out of the training data. Hyperparameters are in the supplement, which was not supplied.
(5) The Tiny ImageNet figure legend (e.g., CVS 38.78 general) is not labeled with its dataset in the passage, so it was left out of the rows.

The two rows below are accuracy-only results for CIFAR100. Both values are confirmed as AR@1 by the embedding-distillation comparison text.
