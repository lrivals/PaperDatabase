---
id: 2024-gheorghe-analyzing-real-time-object-detection
fiche: done
date:
---

# Analyzing Real-Time Object Detection with YOLO Algorithm in Automotive Applications: A Review

Carmen Gheorghe, Mihai Duguleană, Răzvan Gabriel Boboc, Cristian Postelnicu, 2024, Computer Modeling in Engineering & Sciences. https://doi.org/10.32604/cmes.2024.054735
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

This is a review with a bibliometric analysis (Scopus plus Web of Science, 2020–2024, 1554 publications) of YOLO in automotive applications. It groups the work into three areas: road traffic, autonomous vehicles and industrial settings. The paper runs no experiments of its own. Every performance number is taken second-hand from the cited works. The one hardware-specific figure is in §3.4, citing [113]: an FPGA-accelerated YOLO v3 with an attention mechanism for defect inspection of automotive parts. It is reported at 99.2% accuracy, 1.54 FPS and 10 W. The review names no FPGA device, quantization, resource use, dataset or toolflow, and does not say how the power was measured. 1.54 FPS is low for a 'real-time' claim, and the review does not comment on that. Other numbers, such as 94.5 mAP at ≥42 FPS for [110] and the abstract's 'YOLO v8 mAP 0.99', have no platform, and the mAP averages across studies mix different datasets and metrics. Treat them as indicative only. Reference numbering looks inconsistent: [55]–[57] are cited for both traffic counting and pavement cracks, and [73] for two different works. Check the primary source [113] before using the FPGA row. Metadata also needs manual verification: the extraction was flagged as not ok, the author list is incomplete and 'Duguleană' spelling differs.
