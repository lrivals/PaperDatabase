---
id: arxiv-2604.10947-multi-faceted-continual-knowledge-graph
fiche: done
date:
---

# Multi-Faceted Continual Knowledge Graph Embedding for Semantic-Aware Link Prediction

Jing Qi, Yuxiang Wang, Zhiyuan Yu, Xiaoliang Xu, Yuanshi Zheng, Tianxing Wu, 2026, arXiv preprint. https://arxiv.org/abs/2604.10947
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

MF-CKGE (Qi et al., arXiv 2604.10947) is a continual knowledge graph embedding method for link prediction. It is not a hardware or accelerator paper. The passages report no FPGA, ASIC or GPU implementation and no platform, FPS, GOPS, power, LUT, DSP or BRAM figures, so I extracted no benchmark rows.

Method: during offline learning, each new snapshot gets its own frozen embedding space ("temporal decoupling"). Embeddings whose similarity to an earlier embedding is at or above a threshold θ are replaced by a pointer to that earlier embedding ("semantic decoupling"). During online inference, the score from each snapshot is weighted by a softmax over the mean of the top-k similarities between the query relation and the candidate relations. The base model is TransE with dimension 200 and the Adam optimizer. Learning rate, batch size, α and η are chosen from small grids.

Claims: across 8 datasets, MF-CKGE is on average (maximum) 1.7% (2.7%) better in MRR, 1.3% (3.0%) in Hits@1 and 1.4% (3.8%) in Hits@10 than the best baseline. The baselines are IncDE, LKGE, FastKGE, EWC, SI, PNN, CWR, GEM, EMR and DiCGRL, plus Retrain.

Critical points:
(1) Only relative gains appear in the passages. The absolute MRR and Hits values in Tables 2, 3 and 4–7 were lost in extraction; only the captions survive. It is also unclear whether "%" means absolute points or relative change.
(2) The gains over the strongest regularization baseline are small: as low as 0.8 MRR and 0.4 Hits@10. The passages mention no variance, seeds or significance tests.
(3) The paper says MF-CKGE "surpasses Retrain on certain metrics" only for FB-CKGE and GraphHigher, where it is 0.1 MRR and 0.4 Hits@1 higher. That margin is small.
(4) Efficiency claims: training on S5 of FB-CKGE takes 46 s versus 899 s for Retrain (19× faster). These are training times, not inference latency, and no hardware platform is given. Memory is reported in GB in a figure, but those values were not extracted.
(5) Storing one embedding space per snapshot grows memory with the number of snapshots. The redundancy pruning depends on θ, and the passages do not give the final memory cost.
(6) The per-entity knowledge-domain count rising from 2.7 to 5.4 comes from the HYBRID dataset only (Figure 1).

Metadata issues: the listed venue is "arXiv preprint", but the text says SIGIR '26 (Melbourne), DOI 10.1145/3805712.3809683. The extraction flagged "aucune section détectée" (no sections detected), so every passage except Abstract is labelled "(préambule)". The Table 1 dataset statistics are garbled.

Why no rows: none of the passages reports a measured hardware result. The only absolute numbers are training times, and filling latency_ms would need a unit conversion (s to ms), which the instructions forbid. Recommendation: find the original PDF to recover the Table 2/3 values before filling in the paper-fiche.
