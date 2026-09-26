---
id: arxiv-2010.15277-class-incremental-learning-survey-performance
fiche: done
date:
---

# Class-incremental learning: survey and performance evaluation on image classification

Marc Masana, Xialei Liu, Bartlomiej Twardowski, Mikel Menta, Andrew D. Bagdanov, Joost van de Weijer, 2020, arXiv preprint. https://arxiv.org/abs/2010.15277
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

Survey plus benchmark of class-incremental learning (class-IL) methods for image classification. The authors reimplemented about 14 methods in one framework: EWC, MAS, PathInt, RWalk, LwM, DMC, GD, GDumb, LwF, iCaRL, EEIL, BiC, LUCIR and IL2M. All methods share the same data splits and seeds. Hyperparameters are chosen with the Continual Hyperparameter Framework (De Lange et al.), which only uses data available at the current task. The main metric is average accuracy. CIFAR-100 results are means over 10 runs; domain-shift and architecture results are means over 5 runs. The backbones are ResNet-32 for CIFAR-100 and ResNet-18 for higher-resolution datasets, both trained from scratch.

Key findings:
(1) Finetuning with exemplars (FT-E) is a strong baseline. On CIFAR-100 (10/10) with a fixed 2,000-exemplar memory, FT-E reaches 37.9. Regularization methods extended with exemplars often do worse (EWC-E 28.1, LwF-E 30.8).
(2) Methods that correct task-recency bias do best in class-IL. BiC reaches 42.0 on CIFAR-100 (10/10) and 47.0 on (11/50-5), and the text says it is state of the art on ImageNet. IL2M is consistent across datasets.
(3) Herding and random exemplar sampling are nearly tied. The random-vs-herding differences are mostly not statistically significant under a Mann-Whitney U test (Table S6); p<0.05 only for LwF-E and EEIL after task 10.
(4) Returns shrink beyond about 20 exemplars per class. For BiC, going from 10 to 20 exemplars per class gains 6.2 points; going from 20 to 40 gains 4.8 points while doubling memory.
(5) Method rankings change with the network architecture.

Critical caveats:
- Standard deviations on CIFAR-100 are large (±2–8), and many ranking gaps fall within one standard deviation.
- The ResNet-18 RPS result (57.0) uses 89.56M parameters, versus 0.47M for the ResNet-32 baselines, so it is not a like-for-like comparison.
- The 5/20 bias-analysis numbers are given in the text without variance.

Hardware: none. This is not a hardware or accelerator paper. There is no FPGA/ASIC platform, no quantization, and no throughput or power data. The only runtime figure is training time per epoch in Table S3 (for example, FT-E 12.1 s), with an unspecified GPU. All hardware fields are therefore n/r. The rows below are accuracy benchmarks only.
