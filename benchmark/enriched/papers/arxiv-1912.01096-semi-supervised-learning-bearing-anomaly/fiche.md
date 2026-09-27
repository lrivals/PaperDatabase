---
id: arxiv-1912.01096-semi-supervised-learning-bearing-anomaly
fiche: done
date:
---

# Semi-Supervised Learning of Bearing Anomaly Detection via Deep Variational Autoencoders

Shen Zhang, Fei Ye, Bingnan Wang, T.G. Habetler, 2019, arXiv preprint. https://arxiv.org/abs/1912.01096
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

Critical reading: The paper uses VAE-based deep generative models (Kingma et al. M1 = VAE latent features + SVM; M2 = conditional generative model with a built-in classifier) for semi-supervised bearing fault classification on CWRU (10 classes, 1,024-sample windows, 12,900 train / 900 test segments) and IMS (4 classes, 16,000 train / 800 test segments). Each setting is averaged over 10 random shuffles. Baselines are PCA+SVM, a vanilla autoencoder and a supervised CNN. The main claim is that M2 reaches about 95% accuracy on CWRU with 4% of labels (N=516), while the best competing method reaches 57.06%. On IMS, M2 is also the best method in general, but accuracy drops at N=8,000, which the authors blame on imprecise degradation-point labels (AEC vs MAS-Kurtosis).

Caveats:
(1) The supplied passages report no hardware, FPGA or timing results. Despite the 'autoencoder-fpga' axis tag, this is an algorithm-only paper, so every hardware field is n/r. The auto-assigned axis should be rechecked.
(2) The flattened Tables 3 and 4 can't be reliably split into columns. Reading them row by row puts 75.41 in the CNN column at N=516, which contradicts the text's '57.06 best of the rest'. The text also cites a ±0.88 standard deviation for M2, which in the flattened table sits next to 98.06 (the N=2,150 row), not next to the N=516 value. Only the M2 column (last in each group) looks consistent.
(3) The text calls the 0.08%–16.67% label fractions a share of '129,000 training samples', but the stated segment count is 12,900. On IMS it says '160,000' where the segment count is 16,000. These look like typos.
(4) The abstract's '3% to 30%' improvement range doesn't match the ~40% gain claimed in Section 4.
(5) The preprint is marked work in progress. Metadata extraction was flagged for manual checking.
IMS rows are left out because Table 4 is too ambiguous to parse.
