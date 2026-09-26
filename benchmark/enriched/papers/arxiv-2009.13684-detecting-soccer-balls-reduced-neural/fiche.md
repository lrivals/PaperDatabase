---
id: arxiv-2009.13684-detecting-soccer-balls-reduced-neural
fiche: done
date:
---

# Detecting soccer balls with reduced neural networks: a comparison of multiple architectures under constrained hardware scenarios

Douglas De Rizzo Meneghetti, Thiago Pedro Donadon Homem, Jonas Henrique Renolfi de Oliveira, Isaac Jesus da Silva, Danilo Hernani Perico, Reinaldo Augusto da Costa Bianchi, 2020, arXiv preprint. https://arxiv.org/abs/2009.13684
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

Critical reading: this is a CPU/GPU inference benchmark for soccer ball detection on a humanoid robot. It is not an FPGA paper, so the 'yolo-fpga' axis tag looks wrong and should be checked by hand. The paper compares SSD with MobileNetV2 (20 configurations, varying width multiplier α and input resolution) and SSD with MobileNetV3 (6 variants: large/small/min) using the TensorFlow Object Detection API. It also compares YOLOv3/v4 and TinyYOLOv3/v4 from the official darknet implementation. Training used a fish-eye, single-ball dataset of 4014 training and 250 test images at 1920×1080. Accuracy is test mAP taken at the end of training. Latency is the mean per-frame inference time on a 30 s robot video at 4 resolutions, measured on three machines: i5-4210U (constrained, CPU only, all cores), Xeon Gold 5118 (48 CPUs) and a Tesla V100. The per-model values in Tables 1–3 did not survive extraction; only table captions and row labels are present. The only measured numbers that survived are the aggregate MobileNet statistics over 104 values per hardware setting: i5 mean 68.292 ms (std 17.374), V100 mean 47.24 ms (std 8.756), Xeon mean 47.009 ms (std 8.981). A two-sample KS test gave p = 0.97371, meaning V100 and Xeon latencies are statistically similar. That in turn means the GPU gave no speedup for the TF-OD-API MobileNets, which may reflect pipeline or preprocessing overhead rather than compute. Qualitative claims: MobileNetV3 with α = 0.75 scores best on the i5 using a custom mAP/latency normalized score. MobileNetV2 with α ∈ {0.75, 1} is best on server hardware. Official YOLO/TinyYOLO are slowest on CPU but fastest on V100, with latency largely independent of input resolution. Limitations: the normalized score is ad hoc, as the authors admit. There are no power, energy, quantization or FLOP numbers. Results come from a single dataset and a single-object task. The two rows below are aggregate means across all MobileNet configurations, not per-model results; per-model mAP and latency must be taken from Table 1 of the PDF. Published version: J. Intell. Robot. Syst., doi 10.1007/s10846-021-01336-y.
