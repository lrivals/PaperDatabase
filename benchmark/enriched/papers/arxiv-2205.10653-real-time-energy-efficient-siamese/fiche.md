---
id: arxiv-2205.10653-real-time-energy-efficient-siamese
fiche: done
date:
---

# Towards real-time and energy efficient Siamese tracking -- a hardware-software approach

Dominika Przewlocka-Rus, Tomasz Kryjak, 2022, arXiv preprint. https://arxiv.org/abs/2205.10653
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

SiamFC-style tracker built in hardware and software on a Zynq UltraScale+ ZCU104. A custom 6-layer quantised backbone (3x3 convs; 4-bit activations; 4-bit weights except 8-bit weights in the first and last layers; about 554688 parameters vs 3747200 for AlexNet) runs in PL through FINN at 100 MHz. The rest of the tracker runs in Python on the ARM cores. Accuracy on VOT2016 (mAO, GOT-10k toolkit, trained on GOT-10k): FP32 3-scale 0.362, quantised 3-scale 0.355, original SiamFC 0.385. Going from 3 scales to 1 costs about 21% for the quantised model. The 8% gap to the original is described as "on par", which is generous. The folding design space exploration (V1–V6) shows network-only speed rising from 38 to 49 FPS for V5. V6 adds only 0.6 FPS but uses more than 90% of LUT/BRAM and almost 7 W. Numbers the reader should check: (1) the headline "almost 50 FPS" excludes I/O transfers and tracker logic; with transfers it is about 35 FPS, and the full system about 17 FPS. (2) The passages do not say whether the 17 FPS system uses 1 or 3 scales, so it cannot be tied to a specific mAO. (3) The per-version FPS and power cells of Table 4 are missing from the extracted text; the V5 power is only given as a relative figure (+0.6 W vs V4). (4) The 5.5 W figure has no stated measurement scope. (5) The comparison with the GPU (83 FPS at 250 W TDP on a Titan X, taken from the original paper) is not measured under the same conditions. (6) The Table 5 times are garbled (labelled ms, but values like 0.0295 look like seconds), so no latency is recorded. (7) Resources are given only as percentages of the ZCU104, and no DSP count is given. LUT and BRAM values below are percent utilisation. The paper gives no comparison with other FPGA Siamese trackers because those works report no accuracy or use other metrics.
