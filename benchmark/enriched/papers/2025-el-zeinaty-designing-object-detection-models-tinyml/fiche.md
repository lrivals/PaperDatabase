---
id: 2025-el-zeinaty-designing-object-detection-models-tinyml
fiche: done
date:
---

# Designing Object Detection Models for TinyML: Foundations, Comparative Analysis, Challenges, and Emerging Solutions

Christophe El Zeinaty, Wassim Hamidouche, Glenn Herrou, Daniel Menard, 2025, ACM Comput. Surv. 58(2), 50. https://doi.org/10.1145/3744339
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

Critical reading (El Zeinaty et al., ACM CSUR 2025, survey): This survey covers quantization, pruning, KD and NAS for object detection (OD) on MCU-class TinyML hardware. It uses a backbone/neck/head framing, and Table 1 claims it is the only survey that covers OD, the full backbone/head/neck, optimization theory and TinyML together. The authors ran no experiments of their own. Every hardware number is compiled from the cited works, so the rows below are secondary values and should be checked against the primary papers (XiNet [4], TinyissimoYOLO [110]).

Table 8 is the core of the survey's own comparison: 8-bit weights and activations, PASCAL VOC mAP (mAP@0.5 per Sec. 4), MMACs and peak SRAM. Selected entries:
- MCUNetV2-YOLOV3-H7: 68.3 mAP, 343 MMACs, 438 kB on STM32H743.
- XiNet-YOLOV7-L: 74.9 mAP, 789 MMACs, 511 kB on STM32H743, input 416×416.
- TinyissimoYOLO: 56.4 mAP, 55 MMACs on GAP9, input 112×112, peak SRAM not reported.

Caveats:
1. The comparison mixes platforms (STM32F412 and STM32H743 Cortex-M parts vs the 8-core RISC-V GAP9 with an accelerator) and input sizes (112 to 416). Rankings are therefore not like-for-like.
2. None of the supplied passages report latency, FPS, energy or power for the MCU models. The survey's 'real-time' and KPI claims cannot be checked from these tables.
3. XiNet parameter counts are missing ('-').
4. The GROBID extraction truncated Tables 3, 5, 6 and 7 (for example LightDet and EAutoDet-L have no values).
5. Table 4 hardware specs and costs are approximate list values, not measurements.
6. There are minor text errors ('150,55 billion', 'researchering', repository 'Link' placeholder).

Schema note: the schema has no MMAC or SRAM columns, so those values are kept here. LUT, DSP and BRAM do not apply to MCUs, and GOPS was left as n/r rather than converted from MMACs.
