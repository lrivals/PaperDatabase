---
id: arxiv-2311.17162-fast-particle-anomaly-detection-algorithm
fiche: done
date:
---

# Fast Particle-based Anomaly Detection Algorithm with Variational Autoencoder

Ryan Liu, Abhijith Gandrakota, Jennifer Ngadiuba, M. Spiropulu, Jean-Roch Vlimant, 2023, arXiv preprint. https://arxiv.org/abs/2311.17162
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

What the paper does: it proposes two particle-based VAE anomaly detectors for jets. Set-VAE uses a conditional VAE with Chamfer loss. CLIP-VAE stops the KL-divergence term from back-propagating for the samples with the highest reconstruction loss, so KL divergence alone can serve as the anomaly score. Models are trained only on QCD (q/g) jets from JetClass. The paper reports signal efficiency at a background rejection of 100 for 9 signal classes, averaged over 5 runs. It compares DeepSet and Transformer backbones, each with and without particle-type (PID) information. The baseline is an n-subjettiness logistic regression.

Main findings: in the Set-VAE setting, DeepSet with PID beats Transformer with PID while using about 13x fewer FLOPs (13.8M vs 171M; 205K vs 1.81M parameters). CLIP-VAE roughly halves the compute (DeepSet 6.95M FLOPs / 103K parameters) with similar efficiencies overall. Some classes drop, though: H->qql falls from 57 to 35 and t->bl from 77 to 53. The authors say this similarity supports calling the performance 'similar'.

Critical caveats:
(1) No FPGA or other hardware was implemented or measured. The abstract's '2x acceleration in latency' is inferred from FLOP counts, not measured. The claim that avoiding input caching is cheap on FPGAs is not quantified.
(2) The 2x signal-efficiency gain over n-subjettiness can't be checked, because the baseline numbers are 'N/A' in the supplied tables.
(3) The comparison is not controlled: Table 2 models have about half the parameters of Table 1 models, so the savings come partly from model size and partly from the paradigm.
(4) Efficiencies are very uneven across classes (H->gg is 0.2 to 0.6), and variance is high for some entries.
(5) This is a short NeurIPS workshop paper. Architecture and training details are deferred to GitHub, and there is no quantization or resource analysis.

About the rows: they are algorithm-only results. All hardware fields are n/r. For consistency, accuracy_value is the t->bqq signal efficiency.
