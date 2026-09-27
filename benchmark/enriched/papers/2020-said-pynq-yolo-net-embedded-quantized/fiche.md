---
id: 2020-said-pynq-yolo-net-embedded-quantized
fiche: done
date:
---

# Pynq-YOLO-Net: An Embedded Quantized Convolutional Neural Network for Face Mask Detection in COVID-19 Pandemic Era

Yahia Said, 2020, International Journal of Advanced Computer Science and Applications. https://doi.org/10.14569/ijacsa.2020.0110912
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

Pynq-YOLO-Net is a single-class face-mask detector built on YOLO. Its lightweight backbone has one 3x3 stride-2 convolution, 3 inverted residual bottlenecks and 3 linear bottlenecks. Input is 128x128 and the output grid is 8x8. The class-probability branch is dropped and the confidence score is used as the mask/no-mask decision. The model is pruned and quantized to 1-bit weights and 2-bit activations, with 8-bit input and output, then retrained. On a Pynq Z1, feature extraction runs in the programmable logic (PL) and the fully connected and output layers run on the ARM processor.

Reported results:
- FP32 model: precision 94.6 and recall 95.8.
- Compressed model: precision 90.7 and recall 92.3.
- On the board: 16 FPS, with board power that "does not exceed 5 watts".

Critical issues:
1. **Accuracy numbers conflict.** The abstract claims 97% detection accuracy, but no 97 appears in the results. The text also says "90.7% of Accuracy", while Table I labels 90.7 as precision.
2. **The FPS may not be tied to the compressed model.** The paper implies 16 FPS was measured with the compressed model but never says so explicitly. Latency is not reported.
3. **The power figure is weak.** 5 W is an upper bound for the whole board, not a measured value, and the measurement method is not described.
4. **Hardware details are missing.** There are no LUT, DSP or BRAM counts, no clock frequency, no GOPS, and no toolflow is named (e.g. FINN or HLS), even though the 1-bit weights/2-bit activations suggest FINN/BNN-PYNQ.
5. **The quantization method is mislabeled.** It is called "post-training quantization", but it includes retraining, which makes it closer to quantization-aware fine-tuning.
6. **The evaluation setup is weak.** The test set is 30% of a merged dataset (RMFD, MFDD, SMFRD, MAFA). These sources overlap, since SMFRD is merged into MFDD, and many images are synthetic, so train/test leakage is possible.
7. **The comparison is unfair.** The Table I baselines (RetinaFaceMask; the SSD row is empty) were evaluated on different data. The paper gives no IoU threshold or mAP, and there is no ablation of the pruning and quantization steps.
