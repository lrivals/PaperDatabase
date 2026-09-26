---
id: arxiv-2306.00001-tinyissimoyolo-quantized-low-memory-footprint
fiche: done
date:
---

# TinyissimoYOLO: A Quantized, Low-Memory Footprint, TinyML Object Detection Network for Low Power Microcontrollers

Julian Moosmann, Marco Giordano, Christian Vogt, Michele Magno, 2023, IEEE AICAS 2023 (d'après le DOI 10.1109/AICAS57966.2023.10168657). https://doi.org/10.1109/AICAS57966.2023.10168657
Type : conférence

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

TinyissimoYOLO is a YOLOv1-style detector with 422k parameters, an 88x88x3 input and a 4x4 output grid. It uses only 3x3 convolutions and fully connected layers so its weights stay under 0.5 MB. It was trained with quantization-aware training (350 float epochs, then 300 QAT epochs) and deployed as INT8. On Cortex-M chips (STM32H7A3, STM32L4R9, Apollo4b) it runs through TFLite Micro; on the MAX78000 it runs on the CNN accelerator through the Analog Devices tools. The main hardware result, from the Abstract, is for the MAX78000: up to 180 fps, 196 µJ per inference and more than 106 MAC/Cycle. Power was measured for the microcontroller only, with the MAX78000 at 1.2 V and 50 MHz.

Points to read critically:
(1) The supplied passages give no power in watts and no latency in ms. The latency comparison in Fig. 2a is cut off, so power_w and latency_ms are n/r. I did not derive them from the energy or fps figures.
(2) '180 fps' is described as 'up to', and the load conditions (for example camera or I/O) are not given.
(3) The mAP figures are not consistent. Table II gives 58.5 overall on PascalVOC, the text says 'up to 57' and the Conclusion says 59. The IoU threshold is not stated.
(4) The higher WiderFace mAPs (73.5 to 75.4) come from evaluation sets restricted to images with at most 5 objects. On the full test set it gets 45.3 (46.2 when trained on the max-10 subset). PascalVOC is limited to 3 classes and at most 3 objects per image, so the results are not comparable to standard VOC benchmarks.
(5) The paper says the WiderFace and VOC networks give 'exact same' hardware metrics, so the same fps is shared across both rows.
(6) This is not an FPGA design, so LUTs, DSPs and BRAM are n/r.
(7) No numbers are given for the other microcontrollers in the supplied text.
