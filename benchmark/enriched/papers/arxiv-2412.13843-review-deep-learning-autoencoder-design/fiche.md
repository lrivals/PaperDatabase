---
id: arxiv-2412.13843-review-deep-learning-autoencoder-design
fiche: done
date:
---

# A Review on Deep Learning Autoencoder in the Design of Next-Generation Communication Systems

Omar Alnaseri, Laith H. Alzubaidi, Yassine Himeur, Mohammed Alaa Ala’Anzy, Jens Timmermann, Mohammed Salih Mohammed Gismalla, Shadi Atalla, Wathiq Mansoor, 2026, arXiv preprint. https://doi.org/10.1109/ojcoms.2026.3683457
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

Survey (no original experiments) of end-to-end autoencoder (AE) transceivers for wireless, optical-fiber, optical-wireless, semantic and quantum communication. It covers AE variants, loss functions, GCS vs PCS, and a FLOPs-based complexity analysis. The supplied passages contain no measured hardware result: no FPGA or ASIC implementation, and no throughput, latency, power or resource figures. So no benchmark row is extracted. The comparison tables (II–XII) only survived extraction as captions, so their content, including any hardware numbers they may cite from other work, can't be checked from these passages.

Critical points:
(1) The complexity metric is inconsistent. The abstract says "floating-point operations per second (FLOPS)", while the acronym table defines FLOPS as "Floating-Point Operations". Treat Table IV and the complexity section as operation counts, not throughput.
(2) The claim that the bottleneck is "typically composed of one or more un-trainable layers" is questionable. Section IV also calls the AE unsupervised, but communication AEs are usually trained on known transmitted messages and a CE/BCE reconstruction target.
(3) Claims that AEs beat traditional systems and get closer to the Shannon limit rest on cited work, with no quantitative evidence in these passages.
(4) Metadata needs checking. The year says 2026 but the arXiv ID is 2412 (Dec 2024). The DOI points to IEEE OJCOMS 2026. The byline in the preamble lists 6 authors, while the metadata lists 8 (Atalla and Mansoor are missing from the preamble). The 'autoencoder-fpga' axis is not supported: FPGA appears only in the acronym list. Extraction was flagged not-ok, and sections VII/VIII were merged into earlier sections.
