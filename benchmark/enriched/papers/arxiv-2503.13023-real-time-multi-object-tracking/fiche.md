---
id: arxiv-2503.13023-real-time-multi-object-tracking
fiche: done
date:
---

# Real-Time Multi-Object Tracking using YOLOv8 and SORT on a SoC FPGA

Michal Danilowicz, Tomasz Kryjak, 2025, arXiv preprint. https://arxiv.org/abs/2503.13023
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

Critical reading: The authors put a 4-bit (4w4a) quantized YOLOv8n detector at 320 px input into the programmable logic (PL) of a ZCU102 Zynq UltraScale+ MPSoC. They built it with a modified FINN flow that adds external-memory weights, a Split operation, and a Concat that accepts mixed data types. The SORT tracker and NMS run in Python on the processing system (PS). Reported results are 0.21 mAP on COCOval, 38.9 MOTA on the MOT15 train split (baseline SORT with Faster-RCNN: 0.340), and 195.3 fps for the detector at 300 MHz. Three caveats limit these claims.

1. The 195.3 fps comes from counting clock cycles, not from end-to-end wall-clock timing. The whole system reaches only about 24 fps, and the bottleneck is Python SORT/NMS code on the PS.
2. No power, energy, latency or GOPS figures are given, so the low-power claim has no numbers behind it.
3. The mAP drop against the authors' own full-precision model is about 25%. The Table 3 comparison with [21] on ua-detrac has no readable values in the passages. The comparison uses MOT15 train, not test, and a different detector than the SORT baseline.

Resource figures (Table 4): the detector alone uses 105k LUTs, 482 DSPs and 293 BRAM. The full design, including DMA and AXI interconnect, uses 205k LUTs, 486 DSPs and 421 BRAM. The authors say MultiThreshold modules take about 35% of BRAM. Model size falls from 96.4 Mb to 12.0 Mb.

Extraction problems: every passage except the Abstract is labelled '(préambule)', so no real section headings were detected. The metadata still needs checking by hand.
