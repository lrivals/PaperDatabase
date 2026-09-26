---
id: arxiv-2511.07990-hardware-aware-yolo-compression-low
fiche: done
date:
---

# Hardware-Aware YOLO Compression for Low-Power Edge AI on STM32U5 for Weeds Detection in Digital Agriculture

Charalampos S. Kouzinopoulos, Yuri Manna, 2025, arXiv preprint. https://arxiv.org/abs/2511.07990
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

Critical reading: The paper compresses YOLOv8n with iterative L2-norm structured pruning (70% ratio, k=6 steps, 30 fine-tuning epochs per step) and integer quantization, and uses 224x224 inputs. It deploys the result with STM32Cube.AI on an STM32U575ZI (Cortex-M33, 160 MHz) to detect weeds in CropAndWeed (74 species). The measured results are 1510 ms average latency, 51.8 mJ per inference and 1.1 mA in Stop2 current, taken with a PPK2 at 3.3V, plus mAP50 0.517 and mAP50-95 0.403. The compressed model uses 850.97 KB of flash and 677.30 KB of RAM with 960k parameters. The baseline YOLOv8n uses 9.95 MB of flash and 2.5 MB of RAM.

Caveats:
(1) This is a microcontroller deployment, not an FPGA one. The 'yolo-fpga' axis tag is wrong, so LUT/DSP/BRAM do not apply.
(2) The paper claims 'real-time' detection, but inference takes about 1.5 s per frame and wakes every 30 s. That is duty-cycled monitoring, not real-time.
(3) The passages never state the quantization bit width. They discuss 8-bit only in general terms. Granularity and the PTQ vs QAT choice are also not given.
(4) Accuracy is reported on the 80/20 validation split with no held-out test set. The passages give no accuracy for the uncompressed baseline, so the drop caused by compression cannot be quantified. The pruning figures give only the mAP loss (0.15 at 70%).
(5) Table III compares against GPU/Jetson models at 640x640, which is not like-for-like. Those models' mAP50 above 93% is not comparable to this work's 0.517.
(6) There are internal inconsistencies. Table II lists 3200M parameters for the baseline, but the text says 3.2x10^6. The RAM constraint is given as 768 KB while the SRAM spec is given as 786 KB. The 1.1 mA measured in Stop2 is far above the 8.95 uA datasheet figure, which suggests board-level overhead.
(7) The paper reports energy per inference, not average power. The extracted Table IV text does not give an FPS value, so power_w and fps are left as n/r and no values were derived.
