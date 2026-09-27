---
id: arxiv-2209.02976-yolov6-single-stage-object-detection
fiche: done
date:
---

# YOLOv6: A Single-Stage Object Detection Framework for Industrial Applications

Chuyi Li, Lulu Li, Hongliang Jiang, Kaiheng Weng, Yifei Geng, Liang Li, Zaidan Ke, Qingyuan Li, Meng Cheng, Weiqiang Nie, Yiduo Li, Bo Zhang, Yufei Liang, Linyuan Zhou, Xiaoming Xu, Xiangxiang Chu, Xiaoming Wei, Xiaolin Wei, 2022, arXiv preprint. https://arxiv.org/abs/2209.02976
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

YOLOv6 (arXiv 2209.02976) is a GPU paper, not an FPGA one. Every speed result in these passages was measured with FP16 and TensorRT on an NVIDIA Tesla T4. TensorRT 7.2 is the default unless the paper says otherwise, and the input size is 640×640 on COCO 2017 val. There are no FPGA resource or power figures, so the 'yolo-fpga' axis tag should be checked by hand. The claims focus on deployment: throughput at batch size 1 or 32, and GPU latency rather than FLOPs. Main measured claim: YOLOv6-L-ReLU reaches 51.7 AP at 8.8 ms latency and beats YOLOX-L, PPYOLOE-L and YOLOv7 on both accuracy and speed. Relative gains are given for the other variants: N is +7.9 and +2.6 AP over YOLOv5-N and YOLOv7-Tiny at 416; S is +3.0 and +0.4 AP over YOLOX-S and PPYOLOE-S. Some models use self-distillation (‡), which makes some comparisons uneven. Several baselines were re-evaluated (∗). The Table 1 text extraction is garbled, so latencies can only be matched to models safely where the row label is next to the number (YOLOv6-M‡ 5.6 ms, YOLOv6-L-ReLU‡ 8.8 ms, YOLOv6-L‡ 10.2 ms); most AP values are missing. For quantization, Tables 15–17 (RepOptimizer PTQ and QAT, INT8 on T4 with TensorRT 8) appear only as captions with no values, so no quantized row can be extracted. Ablation findings: RepConv+ReLU gives the best speed/accuracy trade-off; the anchor-free head is 51% faster than anchor-based; EfficientRep+Rep-PAN adds 3.6 AP and runs 21% faster. Metadata extraction was flagged not OK, so check the details against the PDF.
