---
id: arxiv-2206.15472-device-training-256kb-memory
fiche: done
date:
---

# On-Device Training Under 256KB Memory

Ji Lin, Ligeng Zhu, Wei-Ming Chen, Wei-Chen Wang, Chuang Gan, Song Han, 2022, arXiv preprint. https://arxiv.org/abs/2206.15472
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

Critical reading: The paper co-designs Quantization-Aware Scaling (QAS), a sparse layer/tensor update, and the Tiny Training Engine (TTE) compiler to fine-tune int8 CNNs on an STM32F746 MCU (320KB SRAM, 1MB Flash) within a 256KB SRAM budget.

Caveats:
(1) Most accuracy numbers (Tables 1–4, the 8-dataset averages) come from GPU simulation on RTX 3090s, not on-device runs. The authors only say they checked that simulation matches MCU accuracy; no per-dataset on-device accuracy is given.
(2) The learning rate was tuned for each run and the best accuracy reported, which is optimistic.
(3) Measured hardware results appear only as memory figures (141KB vs 303MB for PyTorch, giving 2300x; 160/188KB SRAM in Table 5) and relative latency (23–25x over full update with TF-Lite Micro kernels). Absolute per-image latency is only in Figure 10, which isn't in the passages. The TF-Lite full-update baseline runs out of memory, so its latency is projected, not measured.
(4) No power or energy was measured, although the paper claims energy savings.
(5) The FPGA columns (LUTs/DSPs/BRAM) don't apply to an MCU. SRAM figures are recorded in the baseline text instead.
(6) The table extraction is partly garbled (Food and Pets columns merged in Tables 1 and 3; Table 4 rows interleaved), so I didn't transcribe those tables' per-dataset values.
(7) The paper covers vision CNNs only.
