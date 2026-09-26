---
id: arxiv-2203.13167-exemplar-free-continual-learning-vision
fiche: done
date:
---

# Towards Exemplar-Free Continual Learning in Vision Transformers: an Account of Attention, Functional and Weight Regularization

Francesco Pelosin, Saurav Jha, Andrea Torsello, Bogdan Raducanu, Joost van de Weijer, 2022, arXiv preprint. https://arxiv.org/abs/2203.13167
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

What the paper covers: exemplar-free, task-incremental continual learning on a lightweight ViT. The model has a convolutional stem, L=12 layers, K=12 heads and embedding size 192. The paper proposes Pooled Attention Distillation (PAD) on the attention maps taken before the softmax, and an asymmetric version that applies ReLU to the difference so that newly gained attention is not penalised. Both versions are applied to attention maps (ATT) and to contextualized embeddings (FUNC). They are compared with LwF, EWC and finetuning on CIFAR100/10 and ImageNet-32/6. The paper reports no hardware measurements: no platform, FPS, latency, power or FPGA resources. All hardware fields are therefore n/r, and the rows record accuracy only.

Main results. On CIFAR100/10, ATT(asym) reaches 57.3 last-task task-aware accuracy. In Table 1, FUNC(asym) Spatial reaches 57.26 last-task and 56.18 average incremental accuracy, against 55.93 and 54.81 for LwF. On ImageNet/6, FUNC(asym) reaches 27.55, which is 0.44 below its symmetric version.

Points to check critically:
(1) The best attention and functional results (57.3 and 57.26) are almost the same. Scores are averaged over 3 runs but no variance is given, so the claim in the abstract that functional distillation gives better overall accuracy is weakly supported.
(2) Units are inconsistent. Forgetting is "≈0.01%" and ImageNet stability is "≈0.23%", while CIFAR stability is "≈53%". These look like fractions mislabelled as percentages.
(3) The LwF last-task score of 47.74 in the plasticity discussion differs from the LwF last-task accuracy of 55.93 in Table 1. The first seems to be a plasticity (diagonal) value, but the text does not say so.
(4) Only task-aware scores are in the main text; task-agnostic results are in the appendix. Hyperparameters were searched only over [0.5, 1.0].
(5) Most results are shown only in figures (Figures 4 and 5), and many values are not stated in the text.
(6) The extraction metadata is flagged as needing manual checking.
