---
id: arxiv-2405.04453-continual-knowledge-graph-embedding-incremental
fiche: done
date:
---

# Towards Continual Knowledge Graph Embedding via Incremental Distillation

Jiajun Liu, Wenjun Ke, Peng Wang, Ziyu Shang, Jinhua Gao, Guozheng Li, Ke Ji, Yanhe Liu, 2024, arXiv preprint. https://arxiv.org/abs/2405.04453
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

IncDE (Liu et al., arXiv 2405.04453) is a continual knowledge-graph-embedding method built on TransE. It has three parts: (1) hierarchical ordering, which groups new triples into layers using BFS from the old graph (inter-layer order) and then splits each layer into chunks of at most M triples (intra-layer order); (2) incremental distillation, which distills each entity from its representation in the nearest previous layer, weighted by structural importance; and (3) two-stage training, which first freezes old embeddings and then trains all of them.

The authors test on 7 datasets: ENTITY, RELATION, FACT and HYBRID from Cui et al. 2023, plus three new ones (GraphEqual, GraphHigher, GraphLower). Each has 5 time steps with a 3:1:1 train/valid/test split per step. They report IncDE beating all CKGE baselines on MRR, Hits@1 and Hits@10. Incremental distillation is credited with 0.2–6.5% of the MRR gain. M=1024 is the best layer size in most datasets.

Critical points:
- This is a pure ML/algorithm paper. The supplied passages contain no hardware measurements at all: no platform, FPS, latency, power or FPGA resources. Every hardware field is therefore n/r, and the rows record accuracy only.
- The Table 3 fragment is missing its column headers and the IncDE row label. I assigned column 1 to GraphHigher and column 2 to GraphLower because (a) the caption lists them in that order, and (b) the text's gains of +2.0% on GraphHigher and 1.8% on GraphLower match 0.227−0.207 and 0.228−0.210 against LKGE. The unlabeled last row repeats as the full model in the ablation Table 5, which supports reading it as IncDE.
- Gains on RELATION and FACT are small (0.6–0.7% MRR). There are no variance or significance tests, and the case study rests on a single query.
- Three of the seven datasets were built by the authors themselves.
- The efficiency claims (lower training cost than full retraining) are not backed by any runtime numbers in these passages.
