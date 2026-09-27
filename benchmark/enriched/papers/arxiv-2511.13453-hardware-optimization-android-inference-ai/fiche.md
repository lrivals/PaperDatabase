---
id: arxiv-2511.13453-hardware-optimization-android-inference-ai
fiche: done
date:
---

# Hardware optimization on Android for inference of AI models

Iulius Gherasim, Carlos García Sánchez, 2025, arXiv preprint. https://arxiv.org/abs/2511.13453
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

What it is: an empirical study of on-device inference on an Android phone with a Kryo CPU (8 cores), a GPU and an NPU, using LiteRT. It compares CPU single-thread (CPU-SC), CPU multithread (CPU-MC), GPU in FP32 and FP16 modes, and NPU, across these precision variants: FP32, FP16, INT8, FINT8, INT16, FINT16 and dynamic. Models tested: ResNet18/50 (classification) and YOLOv8/YOLO11 (detection). The reference for all speed-up and accuracy comparisons is FP32 on a single CPU thread.

Main claims from the passages:
1. INT16 variants have very high latency, so the authors drop them from further analysis.
2. The NPU is the fastest device, then the GPU, then the CPU. On ResNet50 with INT8, the NPU is more than 120x faster than CPU-SC.
3. Dynamic quantization is much slower on the NPU. The authors say this is because mixed precisions force casts on the CPU and data transfers between the NPU and CPU.
4. Multithreaded CPU tops out at 3.4x (INT8 on 8 cores), which the authors attribute to the asymmetric core design.
5. On the GPU, quantization barely changes speed. Switching to FP16 mode gives close to 2x.
6. ResNet18 Top-1 is about 69 for most variants, but FINT8 collapses to 0.08.

Critical points:
- The passages contain only captions for Tables I–XVI, not their values. No absolute latency in ms, FPS, power or mAP numbers can be extracted, and the rows below record the few values stated in the prose.
- The SoC and phone model are not named in the passages (only "Kryo CPU"), and the dataset is not stated (ImageNet/COCO are likely but unconfirmed).
- The FINT8 collapse to 0.08 looks like a conversion or calibration failure, not a real limit of 8-bit quantization. The authors exclude it instead of diagnosing it.
- The ">120x" figure combines two changes at once: the device (NPU vs CPU-SC) and the precision (INT8 vs the FP32 baseline).
- The metadata axis "yolo-fpga" looks wrong. There is no FPGA; this is mobile CPU/GPU/NPU work, so LUT, DSP and BRAM do not apply.
- Metadata is flagged as needing manual checking.
