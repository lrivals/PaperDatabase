---
id: arxiv-2508.21773-unsupervised-video-continual-learning-non
fiche: done
date:
---

# Unsupervised Video Continual Learning via Non-Parametric Deep Embedded Clustering

Nattapong Kurpukdee, Adrian G. Bors, 2025, arXiv preprint. https://arxiv.org/abs/2508.21773
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

Critical reading note — Kurpukdee & Bors (arXiv 2508.21773, 2025), "Unsupervised Video Continual Learning via Non-Parametric Deep Embedded Clustering".

What it does: The paper sets up unsupervised video continual learning (uVCL), where the model gets no labels and no task boundaries. A frozen VideoMAE V2 encoder, pre-trained without labels on Kinetics-700, extracts a 1024-dim feature per video (16 frames of 224×224×3). Mean-shift then clusters these features using a Gaussian KDE. A novelty detector adds new clusters when a sample is far from existing ones. There are two variants:
- uVCL-KDE uses a distance threshold Θ1, set from the maximum distance between cluster centres in the first task (16.53 / 16.92 / 15.98).
- uVCL-KDE-RBF adds an RBF-style linear layer trained with focal loss (γ=2) and uses a probability threshold Θ2 (best value 0.3).
A replay buffer stores features for N=20 videos per cluster.

Setup: PyTorch, Adam with lr 0.001, up to 50 epochs, batch size 8, on one GTX 1080 Ti 11GB. Datasets are UCF101, HMDB51 and SSv2 with labels removed, split into 13 / 37 / 659 tasks of 256 videos each.

Reported results: uVCL-KDE-RBF is reported as best on all three datasets, ending with 100 / 42 / 133 clusters (bandwidth h=17 for UCF101 and SSv2, h=19 for HMDB51). Ablations:
- A 30-sample buffer works better on UCF101; a 10-sample buffer works better on HMDB51.
- Θ2=0.3 beats 0.7 and 1.0.

Limitations of the evidence:
1. The extracted Table 1–3 text is garbled. Only scattered forgetting values survive (for example -0.11, -0.15, -0.001), and none of the CAcc/ACAcc accuracy numbers can be recovered or matched to a method or dataset.
2. Baselines on SSv2 were run only for the first 30 tasks because of cost, so the SSv2 comparison is incomplete.
3. Bandwidth h and the thresholds were tuned on the evaluation results, and no separate validation protocol is described.
4. Using cluster count as a proxy for the number of classes assumes the classes match the clusters.
5. The conclusion says the method reduces computation and training time, but the evidence is only in Appendix F, which was not supplied.
6. Baseline descriptions (Appendix C) and metric definitions (Appendix D) were also not supplied. In the Table 2 header the arrows on BWF/FWF are the opposite of Tables 1 and 3, which is an inconsistency.

Why there are no benchmark rows: None of the supplied passages reports a measured hardware result (no FPS, latency, power, GOPS or FPGA resources). The GTX 1080 Ti is only the training setup. The accuracy values that could be read cannot be reliably tied to a model or dataset, so no rows were produced.
