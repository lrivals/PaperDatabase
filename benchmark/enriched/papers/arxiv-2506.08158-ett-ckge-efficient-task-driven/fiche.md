---
id: arxiv-2506.08158-ett-ckge-efficient-task-driven
fiche: done
date:
---

# ETT-CKGE: Efficient Task-driven Tokens for Continual Knowledge Graph Embedding

Lijing Zhu, Qizhen Lan, Qing Tian, Wenbo Sun, Li Yang, Lu Xia, Yixin Xie, Xi Xiao, Tiehang Duan, Cui Tao, Shuteng Niu, 2025, arXiv preprint. https://arxiv.org/abs/2506.08158
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

ETT-CKGE (arXiv 2506.08158, 2025) is a regularization-based continual knowledge graph embedding method. It learns a small set of task-driven tokens Z (T ≤ 10, D = 200). These give importance masks σ(ZE) that are multiplied together into an aligned mask, which weights an L2 distillation loss between old and new snapshot embeddings. This replaces the traversal-based or heuristic importance scores used by LKGE, FMR, IncDE and FastKGE. The task is link prediction on six benchmark datasets. All experiments ran in PyTorch on one NVIDIA A6000 GPU. This is a GPU software paper, not an FPGA paper: the 'versal' tag and the 'platforms' axis look wrong and should be fixed in the fiche. There is no FPGA, power, LUT, DSP or BRAM data.

Measured results:
- Accuracy (Table 3): ETT-CKGE has the best or tied-best MRR on 5 of 6 datasets, but the margins over IncDE are small (about 0.001–0.007 MRR). On WN-CKGE, FastKGE is better (0.160 vs 0.153).
- Speed and memory: training time is reportedly 50–96% lower than the second-best model and 1.6–2.3x faster than FastKGE. Peak memory is 150MB–2GB lower, and about 2,000 parameters are updated per snapshot. Most of these efficiency figures come from figures that were not supplied, so they could not be checked.

Caveats:
- The PDF extraction is garbled. The Table 3 training-time columns are missing. Table 4 has fewer T(s) values than its headers imply, and the headers show only 5 dataset names for 6 MRR/T pairs.
- Table 4 gives the full model 0.222 MRR on what appears to be HYBRID, while Table 3 reports 0.224, which may be an inconsistency in the paper.
- The abstract claims 'superior' performance, but the results text says 'competitive... without overclaiming superiority'.
- Baselines were rerun 5 times and tuned. No variance is reported.

Training time in seconds (for example 784 s total on ENTITY in Table 4) is not a per-inference latency, so latency_ms is left as n/r.
