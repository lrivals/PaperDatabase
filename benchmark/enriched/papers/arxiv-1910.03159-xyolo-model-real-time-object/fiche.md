---
id: arxiv-1910.03159-xyolo-model-real-time-object
fiche: done
date:
---

# xYOLO: A Model For Real-Time Object Detection In Humanoid Soccer On Low-End Hardware

Daniel Barry, Munir Shah, Merel Keijsers, Humayun Khan, Banon Hopman, 2019, arXiv preprint. https://arxiv.org/abs/1910.03159
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

xYOLO (Barry et al., 2019) cuts down Tiny-YOLOv3 for RoboCup humanoid soccer with two classes (ball and goal-post bottom). It uses a 256x256 RGB input, far fewer filters, and XNOR only in layers m–p. Using XNOR throughout layers a–k stopped the network detecting anything.

**Main results**
- Raspberry Pi 3 B: 9.66 FPS, versus 0.14 FPS for Tiny-YOLO and 0.39 FPS for Tiny-YOLO-XNOR.
- GTX 960M: 706.36 FPS.
- Model: 0.82 MB and 0.039 BFLOPs, versus 34.7 MB and 5.449 BFLOPs for Tiny-YOLO.
- Accuracy: about 68 validation mAP and about 67 test mAP, versus about 94 for Tiny-YOLO. That is a large accuracy loss, which the authors call acceptable.

**Critical issues**
1. **Not an FPGA paper.** The auto-assigned axis 'yolo-fpga' looks wrong. All hardware is CPU, GPU or Raspberry Pi, so there is no LUT, DSP, BRAM or power data.
2. **The text contradicts Table II.**
   - The prose says Tiny-YOLO-XNOR gets 2.52 FPS and Tiny-YOLO 1 FPS on the Pi. Table II gives 0.39 and 0.14, and 2.52 appears in the i7 row.
   - The prose says xYOLO is 87x faster than Tiny-YOLO on the CPU, but 70.69/0.89 ≈ 79.
   - The train-time numbers are missing from the extracted table.
   - The Raspberry Pi and GPU numbers are consistent with the abstract and the stated speed-ups, so those are the ones used below.
3. **Table III is garbled.** It lists three columns (mAP Train, mAP Test, F-score) but only two numbers per row, and no F-score can be recovered. The test mAP of 66.75 was chosen because the text says 'about 67 on the test set'.
4. **The paper admits its BFLOPs are miscounted.** XNOR layers were counted as FLOPs, so throughput cannot be derived in a comparable way. GOPS is left as n/r.
5. **Weak evaluation.**
   - Test split is a simple 90/10 on the authors' own dataset.
   - All methods were run with default settings.
   - The paper gives no batch size, power or energy numbers, and no latency distribution. The stdev values in Table II look implausibly small.
   - The Discussion's 'about 70% accuracy' rounds up a test mAP of about 67.

The two rows below give the same test mAP because accuracy does not depend on the platform.
