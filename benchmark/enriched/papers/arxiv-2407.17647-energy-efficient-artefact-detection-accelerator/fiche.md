---
id: arxiv-2407.17647-energy-efficient-artefact-detection-accelerator
fiche: done
date:
---

# An Energy-Efficient Artefact Detection Accelerator on FPGAs for Hyper-Spectral Satellite Imagery

Cornell Castelino, Shashwat Khandelwal, Shanker Shreejith, Sharatchandra Varma Bogaraju, 2024, arXiv preprint. https://arxiv.org/abs/2407.17647
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

Castelino et al. (arXiv 2407.17647, 2024) present an unsupervised 6-layer 2D convolutional autoencoder (CAE) that flags artefacts in hyperspectral images (HSI) on board a satellite. An image is flagged when its reconstruction error is above a threshold of about 70000. The model is trained on Indian Pines, Salinas Valley, Pavia University and Kennedy Space Center, using 144x144 patches. It is quantised to uniform INT8 with Vitis-AI post-training quantisation plus 50 epochs of fine-tuning, and runs on a DPU B4096 on a ZCU104 (XCZU7EV) at 300/600 MHz.

Measured results:
- **Accuracy:** F1 is 92.77 after quantisation, against 94.05 for FP32.
- **Speed:** 4.0 ms per inference, averaged over 1000 runs, which gives 250 FPS.
- **Power and energy:** 5.38 W of active power, read from the PYNQ-PMBus rails, and 21.52 mJ per inference.
- **Resources:** only the BRAM/URAM entry survived extraction, as 35.42 / 47.92 %. The LUT, FF and DSP values are missing.

Against other devices, the authors report being 2.6× faster than INT8 and 4.7× faster than FP16 on a Jetson Xavier NX. They also report 1.27× lower latency and 7.5× lower energy than CloudSatNet.

Critical points:
1. **FPR = 0 is a design choice, not a result.** The threshold was chosen to give 0% FPR, at the cost of a 13.48% FNR. The FPR is therefore tuned on the same data and says nothing about how well the model generalises.
2. **The accuracy comparisons are not like-for-like.** The CloudScout and CloudSatNet baselines are supervised RGB cloud classifiers on different datasets. The claimed accuracy gains of +6.4, +6.7 and +3.8 compare different tasks and data.
3. **Inconsistent quantisation claims.** The text describes CloudScout Extended as INT4/FINN in one place and INT8 on the ZCU106 in another.
4. **Power scope is unclear.** It is not stated whether "active power" is total or idle-subtracted. The Pidle and Ptot values in Table VI were lost in extraction.
5. **The Jetson baseline is not like-for-like either.** It used a different training and quantisation flow and got a higher F1 of 95.29. Its absolute latency and power are not given in the text, only as ratios, so the Jetson row has many n/r fields.
6. **Units are ambiguous.** The abstract says "each spectral band" while the body says "per HSI image", so it is unclear what one inference covers.
7. **Tables were garbled in extraction.** Tables III to VI came out mostly without their values, so resource numbers are only partly verifiable.
