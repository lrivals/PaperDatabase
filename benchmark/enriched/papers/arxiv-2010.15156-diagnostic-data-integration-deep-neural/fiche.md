---
id: arxiv-2010.15156-diagnostic-data-integration-deep-neural
fiche: done
date:
---

# Diagnostic data integration using deep neural networks for real-time plasma analysis

A. Rigoni Garola, R. Cavazzana, M. Gobbin, R. S. Delogu, G. Manduchi, C. Taliercio, A. Luchetta, 2020, arXiv preprint. https://arxiv.org/abs/2010.15156
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

Critical reading note (only the supplied passages were used). The paper encodes soft X-ray (SXR) temperature profiles from the RFX-mod DSX3 camera, plus magnetic-state data, into latent codes. It uses variational autoencoders (VAEs) with NaN-Mask layers to handle missing data, and nests autoencoders to combine the two diagnostics. The full-precision VAE6 (4 ReLU layers of 300 nodes each, 6-D latent space) reports a validation mean squared error (MSE) of 0.6e-4 on normalized data (about 17 eV per point) over 6000 samples. Its missing-point recovery error has σ = 63 eV. These accuracy figures are for the float model; no accuracy is reported for the quantized FPGA encoder in the supplied passages (they point to Figure 9, which is not included).

The hardware result is a proof of concept. A quantized encoder, retrained with the Brevitas quantization-aware framework, ran on a Xilinx Zynq 7000 at 100 MHz with folding factor 8. It measured 125 µs average latency without pipelining and about 1.3×10^4 fps with a 64-frame FIFO pipeline. The latency_ms field is n/r because the source gives 125 µs and units were not to be converted.

Not reported: bit widths (only 'few bits' and 'binarized layers'), exact topology, LUT/DSP/BRAM usage, power, GOPS and a comparison baseline. The use of FINN is inferred from the acknowledgment and the folding terminology; the text does not state it. The control target is 'few µs', but the measured 125 µs does not meet it. The authors instead argue it is compatible with the roughly 1 ms plasma dynamics. The metadata author names look swapped between given and family fields (e.g. given='A. Rigoni', family='Garola'), and extraction ok=false, so check both by hand.
