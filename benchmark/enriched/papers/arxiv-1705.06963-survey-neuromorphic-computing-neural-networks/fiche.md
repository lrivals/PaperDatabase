---
id: arxiv-1705.06963-survey-neuromorphic-computing-neural-networks
fiche: done
date:
---

# A Survey of Neuromorphic Computing and Neural Networks in Hardware

Catherine D. Schuman, Thomas E. Potok, Robert M. Patton, J.D. Birdwell, Mark E. Dean, Garrett S. Rose, James S. Plank, 2017, arXiv preprint. https://arxiv.org/abs/1705.06963
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

Survey paper (Schuman et al., 2017, arXiv 1705.06963). It reviews more than 3,000 neuromorphic papers published over 35 years, covering motivations, neuron/synapse/network models, and algorithms and learning. None of the supplied passages report a measured hardware result (no FPS, GOPS, latency, power, or resource figures for any system), so no benchmark rows were extracted. The only power figure is the ~20 W budget of the human brain (II. MOTIVATION), which is biological context, not a hardware measurement. Critical points: (1) This is a taxonomy and citation map, not a quantitative comparison, so it cannot be used as a source for benchmarks. Look up the cited primary works (e.g., SpiNNaker, the CNN implementations [1054]–[1075]) instead. (2) Table I (IV. ALGORITHMS AND LEARNING) compares back-propagation, evolutionary, Hebbian, and STDP learning with qualitative Yes/No/Maybe ratings, without a stated method or metrics. (3) The authors say low power is the main current motivation but do not measure energy efficiency. (4) They acknowledge that STDP has not shown broad applicability and that on-line learning algorithms are still an open problem. (5) Metadata was flagged for manual check (extraction ok=false), and the axes were inferred automatically.
