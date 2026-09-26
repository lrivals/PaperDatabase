---
id: arxiv-2007.12099-pp-yolo-effective-efficient-implementation
fiche: done
date:
---

# PP-YOLO: An Effective and Efficient Implementation of Object Detector

Xiang Long, Kaipeng Deng, Guanzhong Wang, Yang Zhang, Qingqing Dang, Yuan Gao, Hui Shen, Jianguo Ren, Shumin Han, Errui Ding, Shilei Wen, 2020, arXiv preprint. https://arxiv.org/abs/2007.12099
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

PP-YOLO (Baidu, 2020) takes YOLOv3, swaps the backbone for ResNet50-vd-dcn (deformable convolutions in the last stage only) and stacks existing tricks that barely change parameters or FLOPs. The tricks are larger batch size, EMA, DropBlock on the FPN, an IoU loss branch, IoU Aware, Grid Sensitive, Matrix NMS, CoordConv, SPP and a distilled ImageNet pretrain. The main claim is 45.2 mAP on COCO test-dev at 72.9 FPS on a V100, against YOLOv4's 43.5 mAP at 62 FPS.

Critical points:
(1) This is a GPU paper, not an FPGA one. The 'yolo-fpga' axis was auto-assigned and should be corrected. There are no LUT, DSP, BRAM or power figures.
(2) FPS and inference time exclude NMS (following YOLOv4) and use batch size 1. Results with TensorRT are only described qualitatively ('around 100%' relative speedup). Numeric values for the TensorRT case are in Table 2, which was not supplied.
(3) Numerical precision is never stated. The 72.9 FPS figure is presumably FP32 without TensorRT, but that is inferred.
(4) The ablation is incremental in the order the authors explored it, not a full factorial study. The authors admit that the tricks interact, so the contribution of each trick depends on the order.
(5) Some YOLOv4 and baseline numbers were re-measured in the authors' own environment ('+' and '*' marks), which can bias the comparison.
(6) The 72.9 FPS figure matches Table 1 row J (minival, 13.7 ms). The input size for the headline result is not stated in these passages, although sizes 320 to 608 are mentioned.
(7) Tables 1 and 2 report GFLOPs of model complexity, not throughput, so the gops column is n/r.
