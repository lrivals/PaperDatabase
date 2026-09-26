---
id: arxiv-2606.03748-ultralytics-yolo26-unified-real-time
fiche: done
date:
---

# Ultralytics YOLO26: Unified Real-Time End-to-End Vision Models

Glenn Jocher, Jing Qiu, Mengyu Liu, Shuai Lyu, Fatih Cagatay Akyon, Muhammet Esat Kalfaoglu, 2026, arXiv preprint. https://arxiv.org/abs/2606.03748
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

Critical reading note: these passages cover the software and algorithm side of YOLO26: a DFL-free direct-regression head (reg_max=1), STAL, Progressive Loss, the MuSGD optimizer and one-to-one end-to-end (NMS-free) inference. Nothing in them is about FPGAs, so the automatic 'yolo-fpga' axis looks wrong and should be checked by hand. The extraction also flagged the metadata as unverified.

Hardware evidence is thin. The only measured hardware figure is a relative change: the DFL-free head is -0.2 ms latency, -0.3M params and -1.4 GFLOPs versus YOLO11s. No platform is given for that measurement. Table 7 names its speed platforms (CPU ONNX on a Xeon @ 2.00 GHz, and T4 TensorRT10), but the passages contain none of its numbers. They also give no absolute latency, FPS, power or resource figures.

Accuracy claims:
- Removing DFL costs 0.6 AP (47.0 to 46.4). L1 loss, STAL and the backbone/neck refinement (+0.2 each) bring it back to the same accuracy. The 47.0 total is my own arithmetic from these steps; the text only says 'same accuracy'.
- Table 3 says DFL removal improves AP inside the YOLO26s setup (+0.3 AP at 640, +1.3 AP at 1280). Only these differences are reported, not absolute values.
- STAL with sref=16 gives 46.8 AP versus 46.6 for vanilla TAL, and APS rises from 29.0 to 29.6.
- The best Progressive Loss schedule gives 46.7 E2E AP versus 46.4 with fixed weights.
- MuSGD reaches 47.4 mAP in 500 epochs, versus 47.0 for SGD in 600 epochs. The model size for this comparison is not stated.

Caveats:
- Most gains are 0.2–0.3 AP. No variance or number of seeds is reported.
- The paper calls the Progressive Loss weights 'implementation choices rather than independently tuned hyperparameters', yet Table 5 ablates the schedule and picks the best one.
- Final Table 2 and Table 7 values (params, FLOPs, latency, E2E mAP) are missing from the supplied text.
