---
id: arxiv-2111.06417-online-compatible-unsupervised-nonresonant-anomaly
fiche: done
date:
---

# Online-compatible unsupervised nonresonant anomaly detection

V. M. Mikuni, Benjamin Nachman, David Shih, 2022, arXiv preprint. https://doi.org/10.1103/physrevd.105.055006
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

Critical reading note (based only on the supplied passages). This paper proposes a complete method for unsupervised anomaly detection when the signal does not form a resonance. It trains two autoencoders at the same time. A distance-correlation (DisCo) regularizer (Eq. 2) keeps them decorrelated, so their two reconstruction losses can be used for data-driven background estimation with the ABCD method (Eq. 3). Architecture: each autoencoder has five fully connected encoder layers (256, 128, 64, 32 and 5 nodes), and the decoder mirrors the encoder. Data: the ADC2021 dataset (simulated 13 TeV proton-proton collisions, Delphes Phase-II CMS card), with 2M training events and an independent 800k-event validation set of Standard Model events. There are four signal scenarios (LQ at 80 GeV, A→4l at 50 GeV, h0→ττ at 60 GeV, h±→τν at 60 GeV), each injected at 0.1% of the sample. Results: all signal scenarios reach a significance of about 1 to 4, while the Standard-Model-only sample deviates by less than 1. The standard deviation of the average significance across five random seeds is below 6%. The double autoencoder loses less than 30% of the significance of a single autoencoder, but only the double version supports background estimation. Without correcting for signal contamination, the ABCD significance is lower for Standard Model efficiencies above 1.5%. HARDWARE CAVEAT: the paper says the design is 'online-compatible' only because it uses fully connected layers. It cites earlier FPGA and hls4ml work [30, 96–101], but it reports no FPGA implementation and no measured latency, resources, throughput, power or quantization. The Section IV claim of a trigger-rate reduction of 'nearly two orders of magnitude' comes from the Standard Model efficiency in Fig. 3, not from hardware. The trigger-rate estimate (about 4ϵ with prescaled control regions) is only a proposal. Limitations: the dataset does not model differences between data and simulation, and the model is trained on pure background (tolerance to signal contamination was checked only for A→4l). Significance is given as ranges read from figures, not exact table values. The extraction metadata is flagged as needing manual checks, and the 'autoencoder-fpga' axis tag is overstated for this paper. The single benchmark row records the software/physics result only; all hardware fields are n/r.
