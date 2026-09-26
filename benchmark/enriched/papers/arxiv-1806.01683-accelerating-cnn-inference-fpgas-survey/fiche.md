---
id: arxiv-1806.01683-accelerating-cnn-inference-fpgas-survey
fiche: done
date:
---

# Accelerating CNN inference on FPGAs: A Survey

Kamel Abdelouahab, Maxime Pelcat, Jocelyn Serot, François Berry, 2018, Technical Report, Université Clermont Auvergne (HAL), 2018. https://arxiv.org/abs/1806.01683
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

This is a survey of FPGA CNN inference accelerators (Abdelouahab et al., 2018). It groups designs by technique: computational transforms (GEMM, Winograd, FFT), loop optimization, dataflow, approximate arithmetic (quantization, BNN/TNN) and pruning/SVD. None of the hardware numbers are the authors' own measurements. They are compiled from cited works in Tables 3 and 5–8, so any row taken from here is a secondary citation and should be checked against the primary paper.

Critical points:
(1) The tables do not give a power scope (chip or board). Accuracy is reported as a single 'Acc' figure, without saying whether it is top-1 or top-5. Throughput is in GOPs and there is no FPS or latency, so the rows cannot be compared on the same basis.
(2) The GROBID table extraction is heavily garbled. Cells have shifted or merged, which makes row-to-reference attribution uncertain for many entries, such as [28], [42]–[43] and [84]–[85].
(3) The tables contradict each other in places. For [84], Table 5 gives 263K LUTs but Table 7 gives 132K. For the VGG16-SVD workload of [9], Table 5 gives 30.8 GOP and Table 8 gives 30.5 GOP.
(4) The introduction's '9.2 TFLOP/s for the latter' seems to mean the FPGA, not the GPU, and '38 GOP/s to classify a single frame' mixes up units.
(5) Table 2 is a useful reference for workload and parameters: conv layers dominate MACs, while FC layers dominate weights.

Units in the rows: LUTs are in thousands (the table's 'K' column). The bram field holds the tables' 'Memory (MB)' column, which may not be BRAM alone. The two rows below are the cleanest entries: [9] from Table 8 (with toolflow from Table 5) and [30] from Table 3.
