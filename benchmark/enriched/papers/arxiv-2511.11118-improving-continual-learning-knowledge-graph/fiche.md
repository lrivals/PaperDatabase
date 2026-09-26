---
id: arxiv-2511.11118-improving-continual-learning-knowledge-graph
fiche: done
date:
---

# Improving Continual Learning of Knowledge Graph Embeddings via Informed Initialization

Gerard Pons, Besim Bilalli, Anna Queralt, 2025, arXiv preprint. https://arxiv.org/abs/2511.11118
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

Critical reading note — Pons, Bilalli & Queralt (2025), arXiv 2511.11118. Machine learning / continual learning paper; no hardware.

What the paper proposes: a "Schema" initialization for new entities in continual knowledge graph embedding (KGE) learning. Each new entity starts at the mean of its class centroids, taken from previously learned embeddings. A small random offset is added, scaled by γ times the per-class standard deviation. The method works with any KGE model and any continual learning method.

How it was evaluated:
- Datasets: three datasets derived from FB15K-237 (FBinc-S, FBinc-M and FBinc-L). Each has a base snapshot plus 4 snapshots, growing the triple count by 2%, 12% and 25%. Entity classes come from mapping entities to DBpedia.
- Continual learning methods: fine-tuning, EWC, EMR, LKGE and incDE.
- Baselines: random (Xavier) initialization and model-based initialization (the expected position under TransE).
- Metrics: link prediction MRR and Hits@3, plus Ωbase (knowledge retention) and Ωnew (knowledge acquisition), both computed from Hits@3.
- Protocol: results are averaged over 5 seeds, with Wilcoxon significance tests (appendix).

Claims backed by the supplied text:
- Epochs to convergence drop by a factor of 2.16–2.67 compared with random initialization, for every method except EWC.
- Schema initialization is faster than a single training epoch and scales better than model initialization. No absolute timings are in the passages.
- For TransH, the best model, Ωbase improves by 11%, 4% and 13% and Ωnew by 9%, 46% and 26% on S, M and L.
- For HolE, Ωnew more than doubles.
- The introduction says training can be up to nearly 3× faster with 40% better predictive performance.

Limitations and caveats:
- Tables 1–3 and A1–A4 are only captions in the passages, so no absolute MRR, Hits@3 or Ω values are available.
- The TransH gains are relative percentages, and the text does not say whether they are relative or absolute (percentage-point) gains.
- The method needs a KG schema with class memberships, and here those come from an external DBpedia mapping.
- Initialization of new relations is not handled.
- Evaluation uses only FB15K-237-derived data with small updates.
- Several models are named (RotatE, TransR, ProjE) without numbers.
- No hardware, power or FPGA metrics, so all hardware fields are n/r.

Benchmark rows: the rows cover the only explicit numeric model–dataset results in the passages: TransH with fine-tuning on FBinc-S, Schema vs Random initialization, as relative improvement percentages. Confidence is medium because the tables were not available.
