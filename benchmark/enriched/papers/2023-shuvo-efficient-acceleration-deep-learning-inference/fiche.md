---
id: 2023-shuvo-efficient-acceleration-deep-learning-inference
fiche: done
date:
---

# Efficient Acceleration of Deep Learning Inference on Resource-Constrained Edge Devices: A Review

Md. Maruf Hossain Shuvo, Syed Kamrul Islam, Jianlin Cheng, Bashir I. Morshed, 2023, Proceedings of the IEEE 111(1), 42-91. https://doi.org/10.1109/JPROC.2022.3226481
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

Survey article (Proc. IEEE 2023) about deep learning inference on edge devices. It covers edge-AI elements (caching, training, inference, offloading), classical ML on the edge, DL basics, compression, lightweight models, codesign software, and hardware platforms (FPGA, ASIC/SoC, MCU, VPU). The supplied passages contain no measurements made by the authors. Every quantitative result is quoted from cited work: Cachier [21] 3x latency, Precog [22] 5x speedup, FoggyCache [23] 3x latency and 10x energy, XNOR-based quantization 58x speedup (Table 2 caption), ProtoNN [29] under 2 kB of storage on Arduino UNO, and Bonsai [31] 70/500 bytes for binary/62-class. Only the table captions were extracted (Tables 1-10: FPGA state of the art, ASICs, edge hardware quality metrics); the table contents are missing, so no FPGA/ASIC numbers can be taken from them. The single row records the ProtoNN-on-Arduino-UNO claim because it is the only hardware-specific result in the passages. It is a secondhand report, and its storage figure (<2 kB) has no matching schema column, so all its metric fields are n/r and confidence is low. Critical points: the paper is useful as a taxonomy and a pointer to primary sources. Benchmark values should be pulled from the cited primary papers or from the full content of Tables 6-10, not from this survey's text. The speedup figures are relative and have no stated baselines or platforms in these passages.
