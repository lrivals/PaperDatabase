---
id: arxiv-2110.15352-mcunetv2-memory-efficient-patch-inference
fiche: done
date:
---

# MCUNetV2: Memory-Efficient Patch-based Inference for Tiny Deep Learning

Ji Lin, Wei-Ming Chen, Han Cai, Chuang Gan, Song Han, 2021, NeurIPS 2021 (d'après 2025-el-zeinaty-designing-object-detection-models-tinyml, Table 8 ; non imprimé dans la version arXiv). https://arxiv.org/abs/2110.15352
Type : conférence

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

MCUNetV2 (NeurIPS 2021, arXiv 2110.15352) finds that CNN peak memory is set by the first few high-resolution blocks. For example, the first 5 blocks of MobileNetV2 use about 8× more memory than the rest (1372kB vs 172kB, analytic profiling, int8). The paper runs those early blocks patch by patch. To reduce the repeated computation from overlapping patches, it moves part of the receptive field to later layers (MbV2-RD): overall overhead drops from 10% to 3% and ImageNet accuracy is unchanged (72.1 vs 72.2). Neural architecture search then jointly picks the architecture, per-block width w[], resolution r, and the patch settings p and n. Models are int8 and run on an extended TinyEngine on STM32F412, F746 and H743.

Main results:
- ImageNet top-1 of 71.8 on the H743 (465kB SRAM, 2032kB Flash) and 64.9 on the F412 (196kB SRAM).
- VOC mAP with YOLOv3 of 68.3 on the H743 and 64.6 on the F412.
- Visual Wake Words accuracy above 90 with 32kB SRAM.

Critical points:
(1) The detection gain is inconsistent: Section 4 says +16.7 mAP, while the Table 3 caption and the abstract say +16.9 (68.3−51.4=16.9).
(2) No numeric latency or FPS is given in the tables. Latency results appear only in figures (Figure 6, Figure 7), and the 4% latency overhead is stated only for MbV2-RD on the F746. Energy and power are never reported.
(3) Memory values mix analytic and on-device profiling. Table 2 SRAM/Flash values look like on-device figures but are not labelled. Table 3 peak SRAM is not stated as measured. The face-detection results (Tables 4 and 7) use analytic backbone memory (fp32 or int8), not deployment.
(4) The ImageNet comparisons are fair only among int8 models. The int4 and mixed-precision baselines are set aside as orthogonal work, although MCUNet int4 reaches 70.7.
(5) Section 4 wrongly cites RNNPool-Face-C as [30]; it should be [43].
(6) The platforms are MCUs, so LUT, DSP and BRAM columns do not apply (n/r).
