---
id: arxiv-1905.10384-adversarially-trained-autoencoders-robust-unsupervised
fiche: done
date:
---

# Adversarially-trained autoencoders for robust unsupervised new physics searches

Andrew Blance, Michael Spannowsky, Philip Waite, 2019, arXiv preprint. https://doi.org/10.1007/jhep10(2019)047
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

Blance, Spannowsky & Waite (2019, JHEP; arXiv 1905.10384) is a physics-only paper, not a hardware paper. It trains a dense autoencoder on background events only and uses it to spot unusual events in semileptonic ttbar final states from pp collisions at 14 TeV. The autoencoder has 21 inputs, hidden layers of 10, 3 and 10 nodes with sigmoid activations, and a linear output layer. The 21 inputs are the four-momenta of 2 b-jets, 2 light jets and 1 lepton, plus missing energy. An adversary network reads the autoencoder loss. It has two hidden layers of 20 ReLU nodes and a 3-class softmax output that predicts how the background was smeared: up, down or not at all. The combined loss is Ltot = Lauto - alpha*Ladv with alpha = 100. Training alternates between the two networks, with steps 3 and 4 repeated 1500 times, and uses Keras with a TensorFlow backend. The data are simulated with MadGraph5_aMC@NLO and Pythia 8.2. The benchmark signal is a Z' (mass 2 TeV, width 89.6 GeV). The detector smearing was deliberately inflated three times to be conservative. There are 100,000 events per sample, with 20% held out for testing. A supervised classifier (2x20 ReLU layers, sigmoid output) sets the upper benchmark. Main result: the adversarial training almost removes the effect of smearing direction on the loss distributions and ROC curves. Table 1 gives the overall AUC, the upper-minus-lower AUC gap and the cross-section limit (at 100 fb^-1, S/sqrt(B) > 2) for Z' widths of 10, 89.6 and 200 GeV, a scalar colour-octet and a colour-singlet. The authors say the limits are comparable to ATLAS results. Critical points: (1) The passages contain no numbers from Table 1 or the ROC figures, so no AUC or limit can be copied. (2) Everything is Monte Carlo pseudo-data. Applying the method to real data would need systematically smeared, labelled data, which the authors only propose. (3) The ATLAS comparison is loose: this paper uses a post-selection cross section at 14 TeV, while ATLAS uses an inclusive cross section at 13 TeV. (4) The overall performance of the autoencoder is much worse than the supervised classifier, and the passages do not quantify the gap. (5) The paper has no FPGA, hardware, latency, throughput, power or resource results, and no quantisation. Its 'autoencoder-fpga' tag appears to be auto-assigned and should be rechecked. No benchmark rows are given because none of the passages reports a measured hardware result or a copyable accuracy number. Extraction warnings: the metadata needs checking by hand, and no section headings were detected, so almost every passage is filed under '(préambule)'.
