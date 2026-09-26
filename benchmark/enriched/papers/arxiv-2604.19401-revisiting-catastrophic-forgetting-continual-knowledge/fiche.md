---
id: arxiv-2604.19401-revisiting-catastrophic-forgetting-continual-knowledge
fiche: done
date:
---

# Revisiting Catastrophic Forgetting in Continual Knowledge Graph Embedding

Gerard Pons, Carlos Escolano, Besim Bilalli, Anna Queralt, 2026, arXiv preprint. https://arxiv.org/abs/2604.19401
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

Pons et al. (arXiv 2604.19401, 2026) study continual knowledge graph embedding (CKGE). It is not a hardware or FPGA paper: none of the supplied passages report a platform, throughput, latency, power or resource figures.

Main claim: the usual CKGE evaluation ranks old test triples only against the entities that existed at that snapshot. This works like a task-incremental setup and ignores "entity interference", where newly added entities get ranked above the correct answer. The authors propose a corrected protocol that uses the current entity set for all test snapshots. They say the old protocol overestimates performance by up to 25%, mainly on datasets where the number of entities grows a lot (entity growth from first to last snapshot: GraphHigher 1516%, GraphEqual 400%, ENTITY 400%). The effect is small where growth is small (PS-CKGE 7%, RELATION 26%). On ENTITY, retraining loses 11% when interference is counted. It goes from being beaten by 5 of 7 CKGE methods to being the best method.

They also propose a forgetting metric with weighting over CL cycles and test-set size, normalised by θ_{i,i}. Their conclusions: entity interference is the main source of forgetting when entity growth is high, and representation drift dominates when growth is low. Translational KGE models are more stable; semantic models adapt better but forget more.

Setup: 8 benchmarks (ENTITY, RELATION, FACT, HYBRID, GraphEqual, GraphHigher, GraphLower, PS-CKGE). TransE is the base model for all CKGE methods, with embedding dimension fixed at 200 and the original authors' hyperparameters.

Critical points:
- The MRR tables (Tables 3–4, the forgetting-metric table and the KGE-model table) are garbled in the extraction and have no usable numbers. Absolute MRR values could not be recorded.
- The "25%" and "11%" figures are relative drops. They are not absolute accuracy.
- The equation for the forgetting metric is only partly extracted.
- Hyperparameters were reused from the original papers rather than retuned under the corrected protocol, which may favour some methods.
- Only TransE is used for the CKGE method comparison.
- Metadata extraction was flagged for manual check.

One row is included for the only clearly stated measured result (retraining on ENTITY). All hardware fields are n/r.
