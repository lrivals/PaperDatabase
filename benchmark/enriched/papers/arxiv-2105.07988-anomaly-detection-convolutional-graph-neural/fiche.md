---
id: arxiv-2105.07988-anomaly-detection-convolutional-graph-neural
fiche: done
date:
---

# Anomaly detection with convolutional Graph Neural Networks

Oliver Atkinson, Akanksha Bhardwaj, Christoph Englert, Vishal S. Ngairangbam, Michael Spannowsky, 2021, arXiv preprint. https://doi.org/10.1007/jhep08(2021)080
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

Critical reading: this is a particle-physics ML paper, not a hardware paper. None of the supplied passages mention an FPGA, a hardware implementation, quantization, latency, throughput, power or resource use, so every hardware field is n/r. The 'autoencoder-fpga' axis was assigned automatically and does not fit this paper. It should be re-checked in /paper-fiche.

What the paper does: an unsupervised graph autoencoder built from EdgeConv layers, trained only on QCD jets. The training set is 200k simulated pp→jj events from MadGraph5. Each microjet (anti-kT, R=0.1) is a node with 5 features, and the graph is complete, with 3 features per edge (d_CA, log d_kt, log m_ij). An inner-product decoder rebuilds the edge features alongside the node features. The loss is a weighted RMSE (λ_node=0.3, λ_edge=1), and the latent dimension is fixed at 6 after scanning 2 to 12. The test set has 28k QCD jets and a similar number of signal jets.

Results: AUC is 0.74 for QCD vs W, 0.75 for QCD vs top and 0.81 for QCD vs φ (m_φ=700 GeV). The PGAE baseline (Appendix A, nodes only) scores 0.68, 0.57 and 0.78. The authors take this as evidence that reconstructing edges is what helps.

Caveats:
- All data is simulated, and the AUCs are modest.
- The loss is clearly correlated with jet mass (Appendix B), and the paper does not remove this correlation.
- The latent dimension was chosen by looking at signal AUCs, which leaks some signal information into an 'unsupervised' method.
- Section detection failed during extraction, so every passage is labelled '(préambule)'.

The rows below record accuracy only. They are the QCD-vs-top results for the proposed model and the PGAE baseline; the W and φ AUCs are listed above.
