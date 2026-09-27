---
id: 2024-castelino-energy-efficient-artefact-detection-accelerator
fiche: done
date:
---

# An Energy-Efficient Artefact Detection Accelerator on FPGAs for Hyper-Spectral Satellite Imagery

Cornell Castelino, Shashwat Khandelwal, Shanker Shreejith, Sharatchandra Varma Bogaraju, 2024, n/r. https://doi.org/10.1109/dsd64264.2024.00079
Type : n/r

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

Castelino et al. (DSD 2024) present a 6-layer 2D convolutional autoencoder (encoder Conv2D 128/256/512, decoder 256/128/1 with UpSampling2D, 144x144 input) for unsupervised artefact detection in hyperspectral images. An image is flagged when its reconstruction error exceeds a threshold of about 70000. The model is trained on Indian Pines, Salinas Valley, Pavia University and Kennedy Space Center. It is quantised to uniform INT8 with Vitis-AI post-training quantisation, fine-tuned for 50 epochs, and runs on a DPU B4096 on a ZCU104 (XCZU7EV) at 300/600 MHz.

Reported results: F1 is 92.77 (FP32 gives 94.05). Latency is 4.0 ms, averaged over 1000 runs, which gives 250 FPS. Active power is 5.38 W, measured on PYNQ-PMBus rails, giving 21.52 mJ per inference. The abstract rounds F1 to 92.8.

Caveats:
- The power scope is unclear. The paper says it monitored the "FPGA ... PMBus power rails" and reports "active power", so power_scope is set to unspecified.
- The 0% FPR comes from choosing the threshold for zero false positives. This trades off against a 13.48% false-negative rate.
- The SOTA comparisons are not like-for-like. CloudScout, CloudScout Ext and CloudSatNet are supervised RGB cloud classifiers on other datasets. Their accuracy and FPR are compared against this model's accuracy on HSI anomaly detection. The 6.4%, 6.7% and 3.8% accuracy gains therefore cross tasks and datasets.
- The passages are inconsistent about CloudScout Ext precision: Table V lists 8b-int, while the text says INT4/FINN. This is probably a mix-up with CloudSatNet.
- The Table VI resource values are garbled in the extraction. Only a BRAM/URAM entry of 35.42 / 47.92 (percent utilisation, not counts) is readable for this design. It is recorded as bram=35.42 (%). LUT and DSP values are not recoverable.
- The Jetson Xavier NX baseline (10 W mode, TensorRT through torch2trt) is the authors' own measurement. It is only given as ratios: the ZCU104 is 2.6x faster than INT8 and 4.7x faster than FP16, and 3.6x/7.2x more energy-efficient. No absolute Jetson latency or power is in the text passages, so those fields are n/r.
- The Jetson INT8 model scores a higher F1 (95.29) than the Vitis-AI INT8 model, which the authors attribute to different toolchains.
- "Per spectral band" (abstract) and "per HSI image" (results) are used inconsistently for the inference unit.
