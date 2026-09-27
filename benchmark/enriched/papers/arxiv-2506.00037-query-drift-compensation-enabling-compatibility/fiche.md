---
id: arxiv-2506.00037-query-drift-compensation-enabling-compatibility
fiche: done
date:
---

# Query Drift Compensation: Enabling Compatibility in Continual Learning of Retrieval Embedding Models

Dipam Goswami, Liying Wang, Bartłomiej Twardowski, Joost van de Weijer, 2025, arXiv preprint. https://arxiv.org/abs/2506.00037
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

Critical reading note — Query Drift Compensation (QDC), Goswami et al., arXiv 2506.00037 (2025).

Problem: When a dense retrieval embedding model is trained on new datasets over time (Continual Document Retrieval, CDR), queries encoded by the updated model no longer match corpus embeddings that were indexed with the old model. Re-indexing (back-filling) fixes this but costs a lot of compute.

Method: The setting is task-incremental and exemplar-free. The base model is the pre-trained nomic embedding model (137M parameters, 768-dim, modified BERT-base). It is fine-tuned on 5 BEIR tasks in this order: MS MARCO → NQ → HotpotQA → FEVER → FiQA-2018. Training uses a contrastive loss with in-batch negatives plus H=7 hard negatives mined with gte-base, 1 epoch per task, batch size 128, learning rate 2e-5 and weight decay 0.01, on 4 NVIDIA L40S GPUs. Two additions:
(1) Embedding distillation (KD): minimises the cosine distance between old-model and new-model embeddings of both queries and documents.
(2) QDC: estimates one drift vector per task transition and subtracts it from new-model query embeddings at retrieval time. This maps queries back into the old space so they match the old index, without re-indexing.

Claimed results (the passages give only relative numbers; Tables 3 and 4 contain no absolute values here):
- KD improves over plain fine-tuning (FT) by 1.4 on average but hurts plasticity (FEVER drops by 4.5).
- QDC improves over FT by 4.1 on average.
- QDC on top of FT+KD adds 3.3 on average and is claimed best overall, performing similarly to joint training.
- QDC also beats FT with re-indexing.
- Using 20 drift vectors instead of one gains only 0.3–0.7 on some tasks.
- Analysis: corpus embeddings drift more than query embeddings, and longer texts drift more (Table 5). The authors link this to an information imbalance between short queries and long documents.

Critical points:
- The comparison with joint training uses per-dataset hard negatives rather than jointly mined ones, which may understate the joint-training upper bound.
- The claim that QDC beats re-indexing depends on the unequal-drift explanation, which is correlational (Table 5).
- Retrieval uses task-ids, which makes the setting easier than class- or domain-incremental retrieval.
- There is one task order and one backbone, and the passages report no variance.
- Drift vectors are estimated from new-task data only, because old queries are not accessible. It is unclear how well this holds when domains shift a lot, for example the finance domain of FiQA.
- Costs are never quantified. The paper argues that re-indexing is expensive but gives no measured indexing time or retrieval latency.

Benchmark rows: none extracted. The passages contain no measured hardware result (no throughput, latency, power or resource figures; the GPUs are mentioned only as training infrastructure). The absolute nDCG@10 values in Tables 3 and 4 are also missing from the passages, so no row could be filled without inventing values.
