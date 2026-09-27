---
id: arxiv-2604.21280-imagehd-energy-efficient-device-continual
fiche: done
date:
---

# ImageHD: Energy-Efficient On-Device Continual Learning of Visual Representations via Hyperdimensional Computing

Jebacyril Arockiaraj, Dhruv Parikh, Viktor Prasanna, 2026, 2026 IEEE 34th Annual International Symposium on Field-Programmable Custom Computing Machines (FCCM). https://doi.org/10.1109/FCCM68464.2026.00041
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

ImageHD (FCCM 2026) is an accelerator for unsupervised continual learning on a ZCU104 FPGA, built with Vitis HLS 2024.2 and clocked at 300 MHz. Its pipeline has four stages: an INT8 post-training-quantized MobileNetV2 feature extractor, HDC ID-level encoding with word-packed binary hypervectors, Hamming similarity search, and a single-tier bounded cluster memory. That memory is consolidated with Top-M kMeans++ in place of the spectral clustering used in [11]. Key results (Table VII, batch 1, end to end): on CORe50 the FPGA takes 0.48 ms per image (2097.05 img/s) at 3.7 W, or 1.76 mJ/img. That is 40× lower latency and 383× better energy efficiency than an EPYC 7763 CPU. It also beats an RTX A4000 GPU (2.31 ms, 184.80 mJ/img) and a Jetson AGX Orin (13.14 ms, 77.5 mJ/img). On CIFAR-10 it takes 0.27 ms (3703.70 img/s) at 3.6 W, or 0.97 mJ/img. Resources (Table II): 143,927 LUTs (62%), 126 DSPs (7%), 322 BRAM18K (52%) and 57 URAMs. Critical points: (1) FPGA latency and power come from the 'integrated analyzer' and tools in the Vitis Unified IDE, not board-level instruments. This suggests tool-estimated rather than measured power, while the CPU and GPU figures come from powertop and nvidia-smi, so the comparison is not like-for-like. (2) The comparisons with prior work in Table IV use different datasets. For example, the 19.7× gain over [11] divides [11]'s CIFAR-100 result on a Jetson TX2 by ImageHD's CORe50 result, and ILOC excludes feature extraction. The paper itself says accuracy comparisons are not applicable. (3) Absolute clustering quality is low: with INT8, ACC is about 0.19–0.27 and NMI about 0.06–0.13. 'Without sacrificing accuracy' holds on average but hides a real drop in CORe50 purity, from 0.2732 (FP32) to 0.1707 (INT8). (4) GOPS is not reported. (5) The paper does not say whether resource use differs by dataset; Table II gives only one design.
