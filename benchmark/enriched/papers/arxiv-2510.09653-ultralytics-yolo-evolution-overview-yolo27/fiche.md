---
id: arxiv-2510.09653-ultralytics-yolo-evolution-overview-yolo27
fiche: done
date:
---

# Ultralytics YOLO Evolution: An Overview of YOLO27, YOLO26, YOLO11, YOLOv8, and YOLOv5 Object Detectors for Computer Vision and Pattern Recognition

Ranjan Sapkota, Manoj Karkee, 2025, arXiv preprint. https://arxiv.org/abs/2510.09653
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

Survey/review (Sapkota & Karkee) of Ultralytics YOLOv5 → YOLOv8 → YOLO11 → YOLO26 → YOLO27, plus some non-Ultralytics detectors. It contains no FPGA work, and none of the results come from the authors' own measurements. All numbers are copied from vendor or original-paper reports.

Key claims:
- YOLO27 splits the family into two designs by model size. n/s use dual-scale CNNs with an optional NMS-free mode. m/l use query-based transformer decoding, and YOLO27l adds an UltraViT backbone.
- Preliminary COCO mAP50:95 at 640 px ranges from 42.3 (n) to 60.4 (l), with 0.62–2.32 ms latency using TensorRT 11 FP16 on an NVIDIA RTX PRO 6000. YOLO27l reaches 61.2 at 800 px.
- YOLO26 removes DFL and NMS, and adds ProgLoss, STAL and MuSGD.

Critical points:
1. Latencies come from different hardware and runtimes: CPU ONNX for Table 3, T4 TensorRT for Table 4, and RTX PRO 6000 TensorRT 11 for YOLO27. They cannot be compared across tables.
2. The YOLO27 figures are called "preliminary", with no independent check and no batch size, preprocessing or NMS-timing details.
3. Claims about YOLO26 quantization ("INT8 retains nearly the same mAP") and the ~43% CPU speedup ("early previews") have no numbers or source.
4. Table 4 gives YOLOv13 latencies of ~41–67 ms on a T4, versus 1.64–6.14 ms for YOLO12. This is probably a units or source error and needs checking.
5. The dates are inconsistent: YOLO26 is dated 2025 in the text but 2026 in Table 1, the metadata says 2025, and the preprint is dated 2026-09-17.
6. No power, energy or FPGA resource figures are reported, so the automatically assigned 'yolo-fpga' axis looks wrong.

The PDF extraction found no section headings, so every passage except the Abstract is labelled "(préambule)". The two rows below are secondary-source GPU results, not FPGA results.
