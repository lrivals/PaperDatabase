---
id: arxiv-1811.10276-variational-autoencoders-physics-mining-large
fiche: done
date:
---

# Variational autoencoders for new physics mining at the Large Hadron Collider

Olmo Cerri, Thong Q. Nguyen, Maurizio Pierini, Maria Spiropulu, Jean-Roch Vlimant, 2019, arXiv preprint. https://doi.org/10.1007/jhep05(2019)036
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

Cerri et al. (JHEP 2019, arXiv:1811.10276) train a VAE on simulated Standard Model (SM) single-lepton LHC events and flag events whose reconstruction loss is above a threshold as anomalies. The VAE has 21 high-level input features, two dense layers of 50 nodes, a 4-dimensional Gaussian latent space with a learned prior, and 48 outputs that are parameters of per-feature probability distributions. β = 0.3. It was implemented in Keras/TensorFlow and trained on 3.45M events.

**No hardware result:** None of the supplied passages reports a hardware result. There is no FPGA or other device, latency, resource use, power or throughput. Deployment in the trigger (Section 6) is only proposed, with no implementation. The automatic 'autoencoder-fpga' axis looks wrong; this paper belongs under physics/algorithm background.

**Results:** The threshold is set so that about 5.4e-6 of SM events pass. Table 5 quotes 5.3e-6, and Table 3 gives about 1204 ± 167 SM events per month. Selection efficiencies on the benchmark new-physics (BSM) models are 2.8e-3, 6.7e-4, 3.6e-4 and 1.2e-3. The VAE's signal-to-background ratio is about 1.8e2 to 1.7e3 times that of a single-lepton trigger. Supervised boosted decision trees (BDTs) outperform the VAE on each model, which is expected; the VAE's advantage is that it does not depend on a specific model.

**Caveats:**
1. The PDF extraction lost the process labels in Tables 1, 2, 4 and 5 and the Table 2 AUC/TPR values. The mapping of efficiencies to specific BSM models (A→4ℓ, LQ→τb, h0→ττ, h±→τν) cannot be checked from these passages, so it was not recorded.
2. The conclusion says a sample about 30% pure, with about 43 events per day. This does not quite match S/B = 1/3, which is 25% purity, or about 1200 SM + 400 BSM events per month, which is about 53 per day.
3. All results come from DELPHES simulation.
4. Section headings were misdetected (an address line is used as the section title).

**Rows:** No benchmark rows are included because there is no measured hardware result, and physics-efficiency rows could not be tied to specific models reliably.
