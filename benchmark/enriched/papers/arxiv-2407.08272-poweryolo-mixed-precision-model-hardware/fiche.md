---
id: arxiv-2407.08272-poweryolo-mixed-precision-model-hardware
fiche: done
date:
---

# PowerYOLO: Mixed Precision Model for Hardware Efficient Object Detection with Event Data

Dominika Przewlocka-Rus, Tomasz Kryjak, Marek Gorgon, 2024, arXiv preprint. https://arxiv.org/abs/2407.08272
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

PowerYOLO (Przewlocka-Rus, Kryjak, Gorgon, arXiv 2407.08272) quantizes YOLOv8s for detecting cars and pedestrians in GEN1 event-camera data (10 ms event frames, 2 classes). The convolution weights use 4-bit power-of-two (logarithmic) values trained with quantization-aware training. Activations are 8-bit linear, calibrated with OpenVINO. Bias is 32-bit. The paper also proposes a way to fuse convolution and batch-normalization layers that keeps the weights as powers of two.

Main claim: mAP 0.301 on GEN1, with almost 8x less memory than the float model (7.2M parameters). The passages do not say whether 0.301 is mAP50 or mAP50-95. The numbers in Table II are missing from the extracted text.

Accuracy drops versus the full-precision baseline, as stated in the text:
- INT8: about 1 (mAP50) and 3 (mAP50-95).
- LOG4: 3.5 and 8.3.
- Mixed precision: 5.5 and 11.5.
- 4-bit uniform quantization: the gap is about twice that of LOG4.

Critical points:
1. **No hardware measurements.** The paper reports no FPS, latency, power or FPGA resource use. The 1.4x power-efficiency figure is from earlier work [19], a single convolution-layer accelerator on a ZCU104, not from PowerYOLO. Energy savings from bit-shifts are argued, not measured. The Results section says it will "show the applicability" to a hardware accelerator, but the supplied passages contain no such numbers.
2. **The state-of-the-art claim is narrow.** It only holds among compressed models. Full-precision methods reach 0.406–0.484 (GET), and the gap to YOLOv5l [30] with augmentation is more than 20.
3. **The low-bit comparisons are not like-for-like.** The comparison with [22] (post-training quantization) and [34] (which also quantizes activations) mixes different setups, and the authors admit they cannot say which model is better.
4. **The fusion method's cost is unclear.** It may add computation at inference time.
5. **Metadata and axes are auto-flagged for manual checking.** The yolo-fpga axis looks weak because there is no FPGA implementation.

I made one row, for accuracy only.
