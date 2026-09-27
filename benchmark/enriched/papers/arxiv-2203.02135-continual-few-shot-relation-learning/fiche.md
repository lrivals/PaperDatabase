---
id: arxiv-2203.02135-continual-few-shot-relation-learning
fiche: done
date:
---

# Continual Few-shot Relation Learning via Embedding Space Regularization and Data Augmentation

Chengwei Qin, Shafiq Joty, 2022, arXiv preprint. https://arxiv.org/abs/2203.02135
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

Qin & Joty (2022, arXiv 2203.02135) define continual few-shot relation learning (CFRL) and propose ERDA. ERDA combines embedding-space regularization with self-supervised data augmentation. The regularization uses multi-margin, pairwise-margin and a hard-negative contrastive loss on memory data. The augmentation uses entity matching plus similarity search over unlabeled text. Memory holds only one sample per relation.

Benchmarks: FewRel is split into 8 tasks of 10 relations each. TACRED gives 8 tasks: 6 relations in the first, 5 in each of the rest. Task 1 has 100 samples per relation and the later tasks are 2-, 5- or 10-shot. Results average 6 runs with random seeds and task orders. With a Bi-LSTM + GloVe encoder, FewRel 10-way 5-shot final accuracy is 53.23 vs 40.56 for IDLVQ-C, a gain of 12.67 (p < 0.001). The reported gains in the 2- and 10-shot settings are 9.69 and 11.49.

Critical points:
1) This is an NLP / continual-learning paper. It reports no hardware results (no FPGA, throughput, latency, power or resource figures), so every hardware field is n/r.
2) The extraction put all experimental text under the heading '3.3.1 The Encoder Network'. Table rows in passage #011 have lost their method labels. The ERDA row (53.23) is confirmed by the ablation table, and IDLVQ-C (40.56) is labeled explicitly.
3) Joint training is not always an upper bound: ERDA beats it at 2 and 5 shots but falls short at 10 shots.
4) The data-augmentation module adds complexity, but ERDA without augmentation (51.51) still beats all baselines.
5) Variances are only in the appendix, which was not supplied. The λcon sweep changes results by about 1.2 points (51.95 to 53.38), which is comparable to some of the ablation deltas.
6) BERT results (Table 4, Figs. 6–7) are described only qualitatively in the supplied passages.
7) Metadata is flagged for manual verification.
