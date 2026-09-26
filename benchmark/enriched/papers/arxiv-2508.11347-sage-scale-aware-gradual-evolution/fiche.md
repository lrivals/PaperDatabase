---
id: arxiv-2508.11347-sage-scale-aware-gradual-evolution
fiche: done
date:
---

# SAGE: Scale-Aware Gradual Evolution for Continual Knowledge Graph Embedding

Yifei Li, Lingling Zhang, Hang Yan, Tianzhe Zhao, Zihan Ma, Muye Huang, Jun Liu, 2025, arXiv preprint. https://arxiv.org/abs/2508.11347
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

SAGE (Li et al., KDD '25; arXiv 2508.11347) is about continual knowledge graph embedding (CKGE). It is not a hardware or FPGA paper. None of the supplied passages report a hardware measurement: there is no platform, throughput, latency, power or resource usage. All hardware fields are therefore n/r. Table 5 gives only an estimated training cost in FLOPs, and its values are not in the passages.

What the method does: (1) it estimates how much the graph grew and sets the embedding dimension from a fitted logarithmic curve P = a·log_b(N), with P = d·(|E|+|R|); (2) it replays hard past examples and expands the embeddings using a learned mapping; (3) it updates old embeddings with a distillation loss weighted by how new and how reliable each entity or relation is (L = L_itg + α·L_dwt).

Evaluation: link prediction (MRR, H@1, H@10) on seven benchmarks, each with 5 snapshots: ENTITY, RELATION, FACT, HYBRID, GraphEqual, GraphHigher and GraphLower. Baselines are Fine-tune, PNN, CWR, GEM, EMR, DiCGRL, SI, EWC, LKGE, IncDE and FastKGE. The paper also proposes a new forgetting metric, RtF.

Reported gains: averaged over the seven datasets, +1.38% MRR, +1.25% H@1 and +1.6% H@10 over the strongest recent CKGE methods. Against conventional methods the gains are 4.2–20.5% MRR. On ENTITY and RELATION the MRR gains are 2.7% and 1.8%. In the ablation on GraphLower, removing LE lowers MRR by 0.038, removing DI by 0.032, and removing SE by 0.019.

Weaknesses:
- The absolute SAGE scores were lost when the PDF was extracted; the table fragments only show some baseline values, such as IncDE 0.239/0.143/0.426. The row below therefore records a relative gain, not an absolute score.
- The passages do not say whether "1.38%" means percentage points or relative improvement.
- The FACT and HYBRID margins are small, and the passages report no variance or significance tests.
- The log-scaling law is fitted on only four datasets, and the constants a and b are not given.
- RtF is a metric the authors defined themselves, which makes comparison with earlier papers harder.
- The metadata needs fixing: this is KDD '25, DOI 10.1145/3711896.3737115, and the section headings were mis-segmented during extraction.
