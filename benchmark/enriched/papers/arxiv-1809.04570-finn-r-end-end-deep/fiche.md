---
id: arxiv-1809.04570-finn-r-end-end-deep
fiche: done
date:
---

# FINN-R: An End-to-End Deep-Learning Framework for Fast Exploration of Quantized Neural Networks

Michaela Blott, Thomas B. Preußer, Nicholas J. Fraser, Giulio Gambardella, Kenneth O'brien, Yaman Umuroglu, Miriam Leeser, Kees Vissers, 2018, ACM Transactions on Reconfigurable Technology and Systems 11(3). https://doi.org/10.1145/3242897
Type : article de journal

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

FINN-R (TRETS 2018) is the second version of FINN. It is a modular flow with frontends, a quantization-aware IR and backends, built on Vivado HLS. It generates QNN accelerators for PYNQ-Z1, Ultra96 and AWS F1 in two styles: a per-layer dataflow (DF) design or a multilayer offload (MO) design. It sets parallelism (P, Q, M) using LUT and BRAM cost models fitted to microbenchmarks. The paper says the LUT model can be off by up to 30%.

Headline results (Table 5):
- **MLP-4 (W1A1) on AWS F1:** 50,776 GOp/s measured, 79% of predicted.
- **CNV-6 on AWS F1:** 12,109 GOp/s.
- **Best efficiency:** 433 GOp/s/W for MLP-4 on Ultra96.
- **Tincy YOLO (W1A3; first and last layers use 8-bit weights):** 288 GOp/s at 9.7 W on Ultra96 (MO), and 5,271 GOp/s on AWS F1 (DF). Its changes to the network cut operations by 36%, and mAP drops from 57.1 to 50.1. The detection dataset is not named in the passages.

Caveats:
- Throughput is given only in GOp/s. No fps or latency figures are reported, and latency estimation is listed as future work.
- DSP usage is not reported.
- Power is available only for the embedded boards. The text says these are board-level measurements. For AWS F1, power and efficiency are shown as "-".
- AWS F1 resource figures probably include the SDK shell (about 297 kLUTs and 1,090 BRAM18s). That would inflate the accelerator's own cost.
- No accuracy is reported for the hardware runs themselves. The MLP-4 dataset is not stated.
- The related-work comparisons mix different devices, precisions and power definitions. For example, the Prost-Boucle figure uses PMBUS rails only, and the comparison with Yonekawa uses a device about 4× larger. The ">10× vs ZC706" and "4× faster" claims should be read loosely.
- The DoReFa-Net/PF result on AWS F1 closed timing at only 155.8 MHz. The 22 TOp/s figure at 300 MHz is an extrapolation, not a measurement.
