---
id: arxiv-2508.00063-anomaly-detection-spiking-neural-networks
fiche: done
date:
---

# Anomaly detection with spiking neural networks for LHC physics

Barry M. Dillon, Jim Harkin, Aqib Javed, 2025, arXiv preprint. https://arxiv.org/abs/2508.00063
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

Critical reading: This paper is a software-only feasibility study. It trains a small spiking-neural-network autoencoder (SNN-AE) for trigger-level anomaly detection on the CMS ADC2021 dataset. The network has an encoder of (19, 24, 12) neurons, a latent space of 4, and a decoder of (12, 24, 19). It uses leaky integrate-and-fire (LIF) neurons with T in [5, 10] steps, a firing threshold (u_thresh) of 1.2 and a decay factor (β) of 0.9. It is built in PyTorch/snntorch, trained on 100k background events, and uses only the 19 transverse-momentum (pT) and missing-energy (MET) inputs. The comparison baseline is a DNN autoencoder with the same shape and ReLU activations.

No FPGA or neuromorphic deployment is reported. The claims about latency, efficiency and FPGA suitability are argued qualitatively (Sec. 2), and deploying to hardware (FPGA, Loihi) is left as future work in Sec. 5. For that reason, all hardware fields in the rows are n/r.

Table 1 (mean ± std over 5 runs) shows the SNN-AE slightly behind the DNN-AE on every signal:
- AUC: h0 0.719 vs 0.737; h+ 0.899 vs 0.903; A4l 0.880 vs 0.890; phi 0.802 vs 0.852.
- Inverse background efficiency at 30% signal efficiency (ε_b⁻¹ at ε_s = 0.3): h+ 71.3 vs 101.8; A4l 217.3 vs 360.3.
- Reconstruction loss is about 4× higher for the SNN-AE: 20.24e-5 vs 5.19e-5.

So "competitive" is a generous reading. The claims of better robustness (lower variance across latent size and training-set size) rest on figures that are not included in these passages.

The rows report the h+ AUC as the representative accuracy value. Confidence is medium because the table text was extracted by PDF parsing and the value comes from a single signal. The extraction metadata also flags the paper metadata as needing manual checking.
