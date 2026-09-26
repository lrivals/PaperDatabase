---
id: arxiv-2503.07371-hgo-yolo-advancing-anomaly-behavior
fiche: done
date:
---

# HGO-YOLO: Advancing Anomaly Behavior Detection with Hierarchical Features and Lightweight Optimized Detection

Qizhi Zheng, Zhongze Luo, Meiyan Guo, Xinzhu Wang, Renqimuge Wu, Qiu Meng, Guanghui Dong, 2025, arXiv preprint. https://arxiv.org/abs/2503.07371
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

HGO-YOLO is a lightweight YOLOv8n variant for detecting falls, fights and smoking. It uses a GhostHGNetv2 backbone (GhostConv inside HGNetv2) and a detection head with shared parameters and partial convolution (OptiConvDetect). The paper reports 87.4 mAP@0.5 at 56 FPS, 4.3 GFLOPs and 4.6 MB. The YOLOv8n baseline is 84.4 mAP@0.5 at 33 FPS.

**Not an FPGA paper.** It is tagged yolo-fpga, but the passages mention no FPGA, LUT, DSP or BRAM. The hardware is an Intel Xeon Silver 4310 with an NVIDIA A100 for training and comparison, plus a Raspberry Pi 4 and a Jetson Orin Nano for deployment. The yolo-fpga axis should be removed.

**Critical issues:**
1. **Unclear hardware for the 56 FPS figure.** The abstract says "56 FPS on a single CPU", but the only experimental platform listed is Xeon plus A100.
2. **Ambiguous Jetson result.** The abstract says "a stable throughput gain of 42 FPS" on the Jetson Orin Nano. This could mean 42 FPS in total or 42 FPS more than YOLOv8. Table 10 was not extracted apart from CPU usage (Pi 4: 99 vs 95; Orin Nano: 19 vs 17), so the FPS, RAM and power values are missing.
3. **Inconsistent numbers:**
   - GhostConv is said to cut GFLOPs "by 23.6% (from 6.9 to 6.8)", which is arithmetically wrong.
   - The abstract leaves the "redundant computation reduced by %" figure blank.
   - The 51.7% FLOPs reduction is credited to Table 3 in one place and Table 5 elsewhere.
   - Section 3.2.1 describes HGNetv2 as using graph convolution, which appears to be a mistake.
4. **Weak evidence.**
   - **Setup:** Results are relative gains on one self-assembled dataset (10,201 images, 8:1:1 split). There are no error bars and only one run is reported.
   - **Smoke detection:** It is slightly worse than the baseline (75.4 vs 76.0).
   - **Precision:** Quantization and runtime precision (e.g., TensorRT, FP16) are not stated.
