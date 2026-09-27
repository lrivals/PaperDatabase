---
id: 2022-zhang-hfod-hardware-friendly-quantization-method
fiche: done
date:
---

# HFOD: A hardware-friendly quantization method for object detection on embedded FPGAs

Fei Zhang, Ziyang Gao, Jiaming Huang, Peining Zhen, Hai‐Bao Chen, Jie Yan, 2022, IEICE Electronics Express. https://doi.org/10.1587/elex.19.20220067
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

HFOD (Zhang et al., IEICE ELEX 2022) quantizes YOLOv3-Tiny channel-wise and uniformly, with 2-bit weights and 8-bit activations. It also fuses batch-norm (BN) layers into the quantized conv layers. The model runs on a Vivado HLS accelerator on PYNQ-Z2 (XC7Z020, 150 MHz, tiles Tm,Tn,Tr,Tc = 10,4,26,26). Its convolution unit uses line and window buffers with the K×K loops fully unrolled, which is meant to save BRAM and get more work out of each DSP.

Points to read critically:
(1) The headline 90.6 GOPS is the peak of a single layer (conv layer 12, a 3×3 layer). It is not the average throughput over the whole network. The supplied text reports no end-to-end FPS or latency.
(2) The passages give accuracy only as a drop of about 5.3 mAP from FP32 on VOC2007 test. They do not give the absolute mAP values from Table I.
(3) The numbers in Tables II and III (LUT, DSP, BRAM, power, GOPS/W) were not in the extracted text, so resources and power are n/r here. The abstract says 1.4× faster and 2× better power efficiency than a peer on the same board, but that cannot be checked from these passages.
(4) The comparisons mix different models (YOLO, YOLO-tiny, YOLOv3-Tiny), precisions and FPGAs. The paper says the design has the best throughput among RTL designs, while admitting that Afzal et al. [32] has higher throughput.
(5) Results on an infrared aerial dataset are described only in words, with no numbers.

The metadata extraction was flagged as unreliable, and no section headings were detected apart from the Abstract.
