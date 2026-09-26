---
id: arxiv-2407.05705-fast-continual-knowledge-graph-embedding
fiche: done
date:
---

# Fast and Continual Knowledge Graph Embedding via Incremental LoRA

Jiajun Liu, Wenjun Ke, Peng Wang, Jiahao Wang, Jinhua Gao, Ziyu Shang, Guozheng Li, Zijie Xu, Ke Ji, Yining Li, 2024, arXiv preprint. https://arxiv.org/abs/2407.05705
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

FastKGE (IJCAI-style arXiv 2407.05705) is a continual knowledge-graph-embedding method, not a hardware-accelerator paper. It uses TransE as the base model, with incremental LoRA adapters and adaptive rank allocation. New entities are split into layers using BFS distance from the old graph plus degree centrality. The only hardware context is training on one NVIDIA RTX 3090Ti with PyTorch. The paper reports no FPGA, power, throughput or resource figures, so those fields are n/r.

**Claims.** Compared with the fastest baseline, training time drops by 34-49% on ENTITY, RELATION, FACT and HYBRID, and by 51-68% on the two new datasets, FB-CKGE and WN-CKGE. On the four public datasets, average MRR is 21.0 vs 21.1 for the best baseline: competitive, not better.

**Caveats:**
1. FastKGE's own T(s) values are missing from the extracted Table 3 and Table 4 text, probably because they were bold or underlined. The time savings therefore cannot be checked against the passages, and no time value is recorded in the rows.
2. The Table 3 header was truncated to "WN-CKGE". Mapping the three column blocks to HYBRID, FB-CKGE and WN-CKGE relies on the caption order, so the rows are set to medium confidence.
3. The abstract says link prediction improves by 1.5 on the new datasets. The table gives 0.223 vs 0.218 (EWC) on FB-CKGE and 0.159 vs 0.144 (LKGE) on WN-CKGE, so the 1.5 matches only WN-CKGE.
4. Results are said to be the mean of 5 runs, but no variance is reported.
5. Early-stopping patience of 3 directly affects the time comparisons.
6. The batch-size grid lists 258, which is probably a typo for 256.
7. The "no extra inference cost" claim is asserted, not measured.
8. Numeric precision is not stated. Extraction warnings: the metadata needs checking by hand and no sections were detected.
