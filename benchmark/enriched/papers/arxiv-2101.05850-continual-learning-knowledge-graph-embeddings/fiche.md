---
id: arxiv-2101.05850-continual-learning-knowledge-graph-embeddings
fiche: done
date:
---

# Continual Learning of Knowledge Graph Embeddings

Angel Daruna, Mehul Gupta, Mohan Sridharan, Sonia Chernova, 2021, arXiv preprint. https://arxiv.org/abs/2101.05850
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

Critical reading note (supplied passages only). This paper is not about hardware. It adapts five continual-learning methods to knowledge graph embeddings (KGE): PNN, CWR, L2R, SI, and DGR with a VAE triple generator. Each is tested on TransE and Analogy embeddings. The task is triplet prediction on three 5-session datasets built by sampling: WN18RR-5-LS, FB15K237-5-LS, and AI2Thor. Batch serves as the upper bound and Finetune as the lower bound. The metrics are ACC, FWT, +BWT, and REM (computed from MRR and Hits@10 matrices), plus MS, SSS, and LCA. All are scaled to the range [0, 1]. Results are averaged over five runs and tested with repeated-measures ANOVA and Tukey's test (p < 0.05).

Qualitative findings: on the benchmarks, DGR has the best ACC and FWT, but its LCA is much lower because it retrains the generator every session. L2R has the smallest model-size growth (MS). PNN and CWR score below Finetune. On AI2Thor, the best choice depends on constraints: Batch when there are none, DGR when data is limited, and L2R or SI when both data and time are limited (capped at 100 epochs).

Caveats:
(1) The passages contain no numeric results. Every outcome appears only in Figures 2 to 4, so accuracy values are n/r.
(2) No hardware platform, latency, power, FPS, or resource figures are reported. Hardware constraints are only simulated, for example by the epoch cap. Every hardware field is therefore n/r.
(3) The AI2Thor statistics (#015) look corrupted by extraction. The training, validation, and test counts and coverage percentages match WN18RR-5-LS exactly, while |En| is only about 170. Check them against the PDF.
(4) The sampling strategy was designed by the authors, and they claim it is harder than entity sampling, but the passages show no comparison numbers.
(5) The metadata is flagged as unverified (extraction ok=false).

The one row below records the experimental setup only. It is not a measured result.
