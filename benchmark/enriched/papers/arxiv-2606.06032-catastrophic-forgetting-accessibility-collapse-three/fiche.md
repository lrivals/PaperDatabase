---
id: arxiv-2606.06032-catastrophic-forgetting-accessibility-collapse-three
fiche: done
date:
---

# Catastrophic Forgetting as Accessibility Collapse: A Three-Level Framework for Knowledge Persistence in Continual Learning

Ayushman Trivedi, Bhavika Melwani, 2026, arXiv preprint. https://arxiv.org/abs/2606.06032
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

Main claim: catastrophic forgetting is mostly a loss of access to task knowledge (the output pathway), not erasure of what the network stored. Setup: ResNet-18 trained from random initialization on Split CIFAR-100 (10 tasks of 10 classes), plain SGD with cross-entropy, no replay or regularization, with a checkpoint saved after each task. Task 0 results: accuracy drops from 0.548 to 0.000. The linear probe on Layer 4 drops from 0.616 to 0.468, which is 76% retention. The Accessibility Gap (probe accuracy minus task accuracy in the final model) is 0.468 − 0.000 = 0.468. Freezing the backbone and training a new linear head on Task 0 data gives 0.415, which is 75.7% of 0.548. Probes on Layers 1–3 keep 100–104% of their checkpoint accuracy, so the loss sits in Layer 4 and the classifier. Projection energy keeps rising as K grows, and the paper reports strong subspace rotation. Critical points: (1) There is no control such as a probe or head reset on a randomly initialized or untrained frozen ResNet-18. Random convolutional features alone can reach well above chance on 10-way CIFAR, so 'recovery' is not separated from relearning, because the new head is trained on Task 0 data. (2) There is only one run, with no seeds or variance reported, and only Task 0 is analysed in depth. (3) The checkpoint 'persistence' result in Table II holds by construction: stored weights keep their accuracy, which says nothing about the final model. (4) The starting accuracy of 0.548 is low. (5) Most table cells were lost in extraction; the numbers above come from the prose. The extraction metadata also flags the paper details for manual checking. None of these passages report hardware results (no platform, throughput, power or resource figures), so all hardware fields are n/r. The two rows record the paper's main accuracy measurements.
