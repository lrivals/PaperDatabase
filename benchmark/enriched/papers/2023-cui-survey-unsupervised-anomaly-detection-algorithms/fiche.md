---
id: 2023-cui-survey-unsupervised-anomaly-detection-algorithms
fiche: done
date:
---

# A Survey on Unsupervised Anomaly Detection Algorithms for Industrial Images

Yajie Cui, Zhaoxiang Liu, Shiguo Lian, 2023, IEEE Access. https://doi.org/10.1109/ACCESS.2023.3282993
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

Survey (IEEE Access 2023) of unsupervised visual anomaly detection for industrial images. It groups methods into five families: reconstruction-based (AE/VAE/GAN, student-teacher STPM/RSTPM/reverse distillation), normalizing-flow (CFLOW-style, CS-Flow, FastFlow), representation-based (SPADE, PaDiM, PatchCore, FYD), data-augmentation/synthetic-anomaly (DRAEM, NSA, CutPaste, SSPCAB, AnoSeg) and algorithm enhancement (IGD, FCDD, mean-shifted contrastive loss). It also covers datasets (BTAD, ELPV, AITEX, MTD, KolektorSDD, DAGM, MVTec AD, edible oil). Critical points: (1) The supplied passages include only captions for the comparison tables (AUROC on BTAD, AITEX/ELPV, MTD, KolektorSDD, DAGM, MVTec AD, edible oil). No numbers were supplied, so no accuracy values can be extracted. (2) The results appear to be collected from other papers and are not a controlled re-benchmark, apart from Table 12 (edible oil), which may be the authors' own run but is not described. (3) The complexity discussion is qualitative only (e.g., SPADE's KNN makes inference slow; NF methods avoid KNN search). It reports no hardware platform, latency, FPS, power or resource figures. (4) There is no FPGA or accelerator content, so the paper is not relevant to hardware benchmarking. (5) The claims about limitations (threshold uncertainty, ImageNet bias of backbones) are asserted without supporting experiments in these passages. No benchmark rows are included because the passages contain no measured hardware result and no extractable numbers.
