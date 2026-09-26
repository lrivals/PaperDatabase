---
id: arxiv-2605.25860-sam3-assisted-training-lightweight-yolo
fiche: done
date:
---

# SAM3-Assisted Training of Lightweight YOLO Models for Precision Pig Farming

Marcos Vinicius Mendes Faria, Thiago Borges Pereira, Isabella C. F. S. Condotta, Thiago Meireles Paixão, Francisco de Assis Boldt, 2026, arXiv preprint. https://arxiv.org/abs/2605.25860
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

Critical reading: The paper uses SAM 3 as a zero-shot, offline pseudo-labeler with the text prompt "Pig", then trains YOLOv8 n/s/m students on the PigLife dataset (2,130 images; 1,364 train, 340 val, 426 test). RQ1: zero-shot SAM 3 reaches 80.7 mAP and 93.6 AP50, versus 91.7 mAP for the human-annotated YOLOv8m. RQ2: the SAM 3-trained YOLOv8m reaches 79.4 mAP, 93.6 AP50 and 88.2 AP75, close to its teacher. The SAM 3-trained YOLOv8s reaches 78.7 mAP.

Caveats:
(1) There is no FPGA or edge hardware result. All timings come from a desktop RTX 3060 GPU with an i9-10900KF CPU. The Jetson Orin NX is only mentioned as future deployment context, citing [18]. The auto-assigned 'yolo-fpga' axis looks wrong and should be checked by hand.
(2) The ~200× speedup claim compares forward-pass times: 1197.18 ms for SAM 3 versus 6.10 ms for YOLOv8s. The full-pipeline times give a smaller ratio: 1242.53 ms versus 10.37 ms, about 120×.
(3) Pipeline latency is higher for the SAM 3-trained students than for the human-annotated ones (10.37 vs 9.51 ms for v8s), even though forward times are the same. This is probably NMS/post-processing cost and is not explained.
(4) No quantization, batch size, precision or power figures are reported.
(5) APM is weak (27.8–32.1 for students). The paper attributes the 0.4 APM in Group 4 to class sparsity.
(6) The 12.3 gap to the human baseline is called a percentage in the conclusion but is in mAP points (91.7−79.4). The paper is also inconsistent about whether its metrics use box or mask criteria.
(7) The claim of "state-of-the-art" for automated annotation has no external comparison behind it.
(8) Group 5 (farrowing, high occlusion) is the failure boundary at 56.7 mAP.

Row notes: the latency_ms values use the Inf. Forward column from Table I, and the accuracy_value is mAP@[.50:.95].
