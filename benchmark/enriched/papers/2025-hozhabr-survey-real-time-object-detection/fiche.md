---
id: 2025-hozhabr-survey-real-time-object-detection
fiche: done
date:
---

# A Survey on Real-Time Object Detection on FPGAs

Seyed Hani Hozhabr, Roberto Giorgi, 2025, IEEE Access 13, 38195-38238. https://doi.org/10.1109/ACCESS.2025.3544515
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

Critical reading note — Hozhabr & Giorgi, "A Survey on Real-Time Object Detection on FPGAs" (IEEE Access 2025).

What the paper is: A survey of FPGA implementations of real-time object detection, mostly one-stage CNN detectors (YOLO, SSD). It covers the algorithms, datasets and metrics used, how FPGA accelerators are built (single computation engine vs. streaming designs), acceleration techniques (quantization, pruning, Winograd, pipelined NMS) and optimization strategies. Its main claimed contribution is comparing designs by pixel throughput, meaning FPS weighted by input resolution, so that systems running different image sizes can be compared fairly (Tables 9 and 10, Figure 18). It also compares power efficiency (Figure 19).

Strengths:
- It is the first survey framed around the real-time requirement specifically, including the hard vs. soft real-time distinction.
- Pixel throughput is a reasonable way to compare speed across different input resolutions.
- The case studies are reviewed in chronological order and pair architecture details with results, e.g. Chang et al.'s mixed-precision pipelined multicore design.

Limitations and caveats:
- Every hardware number is second-hand, summarized from the cited works, and often without key context: dataset, input resolution, clock frequency, and whether power was measured for the chip or the whole board. For example, Fan et al. [47] report 9.9 W with no scope stated; Nguyen et al. [15] report 51.68 mAP with no dataset named in the passage.
- Accuracy is sometimes given only as a drop (Fan: 1.8% loss after pruning; Suh: 0.24% mAP drop) rather than an absolute value.
- Some claims are hard to check or look inconsistent. "Pruning up to 10% of the channels" is said to give a model 3× smaller. "More than sixfold" improvement over a TITAN X Pascal GPU is stated without the GPU's own figures.
- The supplied passages list Tables 9 and 10 by caption only, so their values could not be extracted.
- The claim that streaming architectures suit real-time work better is argued qualitatively, not quantified.
- The extraction warned that section I headings were not detected, so introduction text appears under the "FIGURE 1." heading.

About the rows: both are secondary rows, taken from cited primary works (Fan et al. [47] and Nguyen et al. [15]) as the survey reports them. Confidence is set to medium because the values should be checked against the original papers. Other results mentioned in the passages but not tabulated:
- Chang et al. [82]: YOLOv3 on ZCU102, 22 FPS, 49.7 mAP.
- Suh et al. [69]: SSD with UniPOT 8-bit on ZU3EG, 158 GOPS, 79 GOPS/W, 88.42 mAP on a custom drone dataset.
- Anupreetham et al. [67]: SSD on Stratix 10, 2.13 ms end-to-end latency, 22.8 mAP on MS COCO.
