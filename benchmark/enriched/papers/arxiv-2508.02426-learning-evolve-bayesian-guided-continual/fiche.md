---
id: arxiv-2508.02426-learning-evolve-bayesian-guided-continual
fiche: done
date:
---

# Learning to Evolve: Bayesian-Guided Continual Knowledge Graph Embedding

Linyu Li, Zhi Jin, Yuanpeng He, Dongming Jin, Yichi Zhang, Haoran Duan, Xuan Zhang, Zhengwei Tao, Nyima Tash, 2025, arXiv preprint. https://arxiv.org/abs/2508.02426
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

BAKE (Li et al., arXiv 2508.02426; the passages give the venue as WWW '26) treats continual knowledge-graph embedding (CKGE) as sequential Bayesian inference. It uses a mean-field Gaussian posterior with precision-weighted updates, where the old posterior becomes the new prior. On top of TransE and the usual KGE loss it adds a KL-style regulariser (L_Bayes, with weight beta) and a continual clustering loss. The clusters have a fixed size K and are built from entities sorted by importance, rather than by re-running k-means for each snapshot. The paper evaluates on 8 benchmarks (ENTITY, RELATION, HYBRID, GraphLower/Equal/Higher, FB-CKGE, WN-CKGE), each with 5 snapshots. Metrics are MRR and Hits@1/3/10, averaged over the current and all earlier test sets and over 5 runs. Training ran on 8 V100 GPUs.

Critical points:
(1) This is not a hardware or FPGA paper. There are no measured throughput, latency, power or resource numbers, and the GPUs are only the training setup. So no hardware row is required.
(2) The PDF extraction dropped every absolute value from Tables 1–3. Only the 'Improve' percentages survived, and they cannot be matched reliably to dataset and metric columns because some cells are '-'. So I did not create any accuracy rows.
(3) The paper overstates its claims. The results text says it is state of the art on 'all benchmark datasets and evaluation metrics', but the abstract says 'the vast majority of cases', and the Improve row has missing entries.
(4) The paper claims 'theoretical guarantees' and insensitivity to data order. In practice the method is a precision-weighted L2 penalty (operationally close to EWC-style regularisation), and the passages show no proof. The precision update is also additive, so it may make parameters too rigid over many snapshots. The authors do not discuss this.
(5) The paper motivates CKGE by efficiency (retraining YAGO from scratch is too costly), but reports no training-time or cost comparison.
(6) The case-study prose does not match Table 4. The prose says competitors placed the true answers 'beyond the top 100', but the table shows ranks of 26 and 3 for Blade Runner and 25 and 69 for Netherlands.
(7) The ablation results are given only as relative drops, e.g. an average H@1 drop of about 11.16% without clustering and an H@10 drop of 5.37% on ENTITY without the Bayesian module.
(8) Metadata to fix: the author appears as 'Tashi Nyima' in the paper, and the venue should be WWW '26 rather than a preprint. No section headings were detected, so almost everything is filed under '(préambule)'.
