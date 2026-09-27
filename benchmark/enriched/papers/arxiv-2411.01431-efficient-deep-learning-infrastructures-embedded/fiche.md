---
id: arxiv-2411.01431-efficient-deep-learning-infrastructures-embedded
fiche: done
date:
---

# Efficient Deep Learning Infrastructures for Embedded Computing Systems: A Comprehensive Survey and Future Envision

Xiangzhong Luo, Di Liu, Hao Kong, Shuo Huai, Hui Chen, Guochu Xiong, Weichen Liu, 2024, ACM Transactions on Embedded Computing Systems. https://doi.org/10.1145/3701728
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

Critical reading: this is a broad survey (manual/automated network design, compression, on-device learning, LLMs, software/hardware, applications) with no original experiments. Every quantitative figure in the passages comes from cited work or vendor spec sheets.

(1) The only measured on-device results are second-hand: DeiT and PiT latency on iPhone 12 (10.99 ms vs 10.56 ms, citing [124]), and a transformer translating a 30-word sentence in 20 seconds on a Raspberry Pi (citing [95]). The survey uses the iPhone result to argue that 3× fewer FLOPs need not mean lower latency. It does not give quantization, framework or batch settings, so these numbers can't be reproduced from the survey. EdgeViT is compared with MobileNetV2 on Samsung Galaxy S21 "under comparable latency constraints", but no latency value is given.

(2) Table 4 is a list of vendor specs, not benchmarks: launch prices, power ranges, and peak TFLOPS/TOPS at mixed precisions. These are not comparable across devices. The table caption also mislabels it as "software frameworks".

(3) Extraction and consistency problems:
- The Table 3 fragment mixes in a bar chart comparing ResNet-50 and MbV2-1.4 memory (Param 102 / 24 MB; Activation 1414.4 / 1252.8 MB) with no context.
- Reference numbers in the Fig. 4 timeline don't match the text: Transformer [90] vs [92], GPT-3 [48] vs [50], ViT [107] vs [109].
- The text says ViT was proposed in June 2020, while Fig. 4 dates it 2020.10.
- The text gives over 87 MB of storage for ResNet50, while the figure gives 102 MB of parameters.
- INT8 is glossed as "8-bit weights" only.
- There is a typo, "Facebool".

(4) Accuracy figures for efficient CNNs and ViTs (e.g., EfficientViT 78.6 at 406 M FLOPs, EdgeNeXt 75.0) are ImageNet top-1 taken from the original papers under different training recipes, as the survey itself notes. They carry no hardware measurements.

Rows below record only the cited iPhone 12 latency pair, with low confidence because the result is secondary. Use the original sources for the database.
