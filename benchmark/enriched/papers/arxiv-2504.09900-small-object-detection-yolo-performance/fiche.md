---
id: arxiv-2504.09900-small-object-detection-yolo-performance
fiche: done
date:
---

# Small Object Detection with YOLO: A Performance Analysis Across Model Versions and Hardware

Muhammad Fasih Tariq, Muhammad Azeem Javed, 2025, arXiv preprint. https://arxiv.org/abs/2504.09900
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

Scope: this is a software benchmark of the smallest YOLO variants (v5n6u, v8n, v9t, v10n, v11n). They are compared on CPUs (Intel i7-13700, AMD Ryzen 7 5800X) and a GPU (NVIDIA RTX 3070), using ONNX, PyTorch, IPEX, OpenVINO and TensorRT through Ultralytics 8.3.39. There is no FPGA work at all, so the auto-assigned 'yolo-fpga' axis is wrong and should be removed. None of the supplied passages give numeric speed, latency or power results. Speed findings appear only in figures (Fig. 2–4) and in qualitative statements: OpenVINO is best on CPU, the AMD system beats the Intel one, and TensorRT is by far the fastest on GPU. The only numbers are accuracy values from Tables I and II, and those are platform-independent. Critical issues: (1) Eq. 4 is labelled 'Throughput' but actually computes mean per-image time (pre-processing + inference + post-processing), which is latency. (2) The captions and the text disagree. The Table I caption refers to objects at 1%/2.5%/5% of the image, but the columns say Small/Medium/Large. The text cites Table II for the 5% COCO result, although that result appears to be in Table I. One column is labelled 'mAP@0.95 (Small)', which is probably a typo. (3) Some claims in the text don't match the tables. For medium objects on DOTA, the text says v9 leads v8 by 9 points, but the table shows 11.43 at mAP@0.5 (74.01 vs 62.58) and 6.94 at mAP@0.5:0.95. The claimed 'nearly 4 points' lead of v8 over v11 on small DOTA objects is 3.55. (4) The authors deliberately left out mask annotations, so their mAP values are not comparable with the numbers Ultralytics publishes. (5) Each run was repeated five times, but no variance is reported. (6) Explanations based on architecture (C2f, PGI, attention being overwhelmed) are speculation with no ablations behind them. (7) The 1024x1024 DOTAv1.5 results come from models trained for 100 epochs with AdamW, but the training details for each dataset are not clear. Both rows below are accuracy-only; the hardware platform is n/r because the tables do not link accuracy to a specific device.
