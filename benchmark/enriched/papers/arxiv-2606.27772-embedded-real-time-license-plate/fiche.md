---
id: arxiv-2606.27772-embedded-real-time-license-plate
fiche: done
date:
---

# An Embedded Real-Time License Plate Recognition System for Complex Traffic Scenes

Anuki Pasqual, Dulan Lokugeegana, Manimohan Thiriloganathan, Nuthya Rathnayake, Kithsiri Samarasinghe, Udaya S. K. P. Miriya Thanthrige, 2026, arXiv preprint. https://arxiv.org/abs/2606.27772
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

Pasqual et al. (ITSC 2026, arXiv 2606.27772) describe a two-stage license plate recognition (LPR) system on a Xilinx Kria KV260. A lightweight CNN finds the plates (license plate detection, LPD), and a second CNN reads the characters on each cropped plate (character recognition, LPCR). Both CNNs use low-bitwidth quantization with Brevitas and are built as accelerators with FINN. The paper also introduces SL-LPR, a Sri Lankan dataset of busy multi-vehicle road scenes.

**Reported results:**
- **Detection:** 93.6 AP and 92.2 recall at IoU ≥ 0.5 on SL-LPR, with 9.9 ms per frame on the FPGA.
- **Character recognition:** 97.42 character-level accuracy and 87.88 plate-level accuracy on SL-LPR, with 4.0 ms per plate on the FPGA.
- **Latency breakdown:** the ARM processing system takes 18.1 ms for frame resizing (the stated bottleneck), 6.0 ms for camera capture and 10.0 ms for other steps.
- **End-to-end:** at most 87 ms for a frame with up to 10 plates, or 11.5 FPS. System power is 4.2 W.
- **Model size:** 1.4M parameters in total, 268 KB after quantization.

**Caveats:**
- The passages do not give LUT, DSP or BRAM use, bitwidths, clock frequency or GOPS.
- The 4.2 W figure has no stated measurement scope (chip or board), so it is marked unspecified.
- 11.5 FPS is derived from a worst-case 87 ms at 10 plates. It is not a measured average, and the paper says it holds "in most urban road scenarios."
- The abstract says "93.6% mAP," but the results section calls it AP.
- Speed comparisons with other work use latencies copied from the original papers, on different hardware (CPU, GPU, FPGA). They are not reproduced under the same conditions.
- The Table V and VI accuracy values for PKU, UFPR-ALPR, AOLP and Arg-plate did not survive text extraction, so they are omitted here.
- The only same-platform comparison is Li et al.: 50 ms per plate on the KV260, which the authors say is about 12× slower but more accurate.
- Table VII gives the per-step latencies for the Xeon and Cortex-A53 CPU-only runs, but their values did not survive extraction. Only the KV260 column is available.

**Row choices:** I recorded two rows, the end-to-end system and the detection model. The character recognition numbers are in the note only.
