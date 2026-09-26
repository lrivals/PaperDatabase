---
id: arxiv-2307.11904-model-compression-methods-yolov5-review
fiche: done
date:
---

# Model Compression Methods for YOLOv5: A Review

Mohammad Jani, Jamil Fayyad, Younes Al-Younes, Homayoun Najjaran, 2023, arXiv preprint. https://arxiv.org/abs/2307.11904
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

Survey (arXiv 2307.11904, 2023) covering pruning and quantization applied to YOLOv5. It leaves out knowledge distillation because distillation needs a second model or changes to the network, which makes it less modular. The authors run no experiments of their own. Tables 1 and 2 collect results from other papers: ΔAcc is the absolute change in mAP0.5, and the other deltas (params, size, FLOPs, FPS, inference time) are relative changes.

Key observations:
- About 85% of the pruning papers use channel-based pruning.
- About 60% use sparse training on the batch-norm scaling factor (BNSF).
- More than half of the quantization papers use quantization-aware training (QAT), which reaches down to 3-bit (NIPQ: 3W/3A gives -5.8 mAP0.5 on VOC). The post-training quantization (PTQ) works stay at 8 bits or higher.

Critical points:
- None of the supplied passages report an FPGA deployment, so the 'yolo-fpga' axis tag looks wrong. Hardware targets in the passages are Jetson Xavier NX, Raspberry Pi 4B, an STM32 microcontroller and a MediaTek phone SoC.
- Most results come from different custom ('Manual') datasets, with different YOLOv5 sizes and fine-tuning schedules. The authors admit this themselves ('different works can hardly be compared'), so the tables are a catalogue, not a benchmark.
- Hardware metrics are only given as relative deltas, with no absolute FPS, latency, power or resource figures. Some table cells are missing or out of place (for example rows [60] and [58]), and the text of both tables is cut off partway through.
- Metadata extraction is flagged as unverified.

The rows below are secondary results copied from cited works. Absolute FPS is not reported, so the relative deltas go in the baseline field.
