---
id: arxiv-2401.13200-topology-aware-embedding-memory-continual
fiche: done
date:
---

# Topology-aware Embedding Memory for Continual Learning on Expanding Networks

Xikun Zhang, Dongjin Song, Yixin Chen, Dacheng Tao, 2024, arXiv preprint. https://arxiv.org/abs/2401.13200
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

Critical reading: PDGNNs-TEM decouples the trainable parameters from the ego-subnetwork topology. It stores fixed-size Topology-aware Embeddings (TEs), which cuts replay-buffer space from O(ndL) to O(n). It also adds coverage-maximization sampling, motivated by a proven "pseudo-training" effect on neighbouring nodes.

Strengths: large class-IL gains. Average accuracy (AA) on OGB-Arxiv is 53.2 versus 49.9 for SEM-curvature. On OGB-Products it is 73.9 versus 65.1. Buffer memory is the smallest reported: for example, 9M float32 values on Reddit, against 193M for SSM/SEM.

Caveats:
(1) Baseline results are copied from the original works [95, 96, 98] rather than re-run, so the setups may not match exactly.
(2) PDGNNs beats joint training, the supposed upper bound (53.2 vs 46.4 on Arxiv; 73.9 vs 71.5 on Products). The authors explain this by differences in optimization and noise, but give no controlled evidence.
(3) Average forgetting (AF) on OGB-Arxiv is worse than SSM/SEM (-14.7 vs -10.7/-8.4). On Reddit, AA is below SEM (94.7 vs 96.3).
(4) Under task-IL, PDGNNs does not clearly beat SSM or SEM.
(5) Coverage-maximization sampling helps mainly when the buffer is tight. The gain disappears at larger ratios (53.4 vs 53.3).
(6) Memory is counted in float32 values, not measured in bytes or runtime. There is no hardware, latency or power evaluation, so all hardware fields are n/r.
(7) Metadata issue: the passages say KDD '24 with DOI 10.1145/3637528.3671732, but the metadata lists "arXiv preprint" with no DOI. This should be checked by hand.

All passages sit under "(préambule)" because section detection failed during extraction.
