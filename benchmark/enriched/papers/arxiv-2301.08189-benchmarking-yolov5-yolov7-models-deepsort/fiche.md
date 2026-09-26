---
id: arxiv-2301.08189-benchmarking-yolov5-yolov7-models-deepsort
fiche: done
date:
---

# Benchmarking YOLOv5 and YOLOv7 models with DeepSORT for droplet tracking applications

Mihir Durve, Sibilla Orsini, Adriano Tiribocchi, Andrea Montessori, Jean-Michel Tucny, Marco Lauricella, Andrea Camposeo, Dario Pisignano, Sauro Succi, 2023, arXiv preprint. https://arxiv.org/abs/2301.08189
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

Critical reading: The paper is tagged with the yolo-fpga axis, but it contains no FPGA work. It benchmarks YOLOv5 and YOLOv7 with DeepSORT for tracking microfluidic droplets. Training ran on an HPC node with a Tesla V100 GPU and two Xeon Gold 6240 CPUs. Inference ran on an MSI G77 Stealth laptop with an i7-12700H CPU; the abstract names an RTX 3070 Ti GPU. The dataset is small and custom: 1000 manually annotated frames with about 13–14 droplets each. mAP@0.5 is only described as saturating to unity after about 20 epochs, with no number for each model. Accuracy therefore cannot tell the models apart, and the task looks close to trivial for detection. The main claims are that YOLOv7 infers about 10% faster than YOLOv5, and that DeepSORT's tracking cost (about 0.11–0.13 per frame on the CPU and about 0.02–0.03 on the GPU, units not stated in the passages, probably seconds) is similar to or larger than the cost of light detectors. Because of this, only lighter models reach real-time (30 fps) tracking on the GPU. YOLOv7-e6e is marked X (not run) in the GPU table. Extraction issues: Tables II and III came through garbled. Most rows have no model label, and the Total time and FPS columns are missing. Only the YOLOv7-tiny rows can be linked to numbers (CPU: YOLO 0.1064, DeepSORT 0.1175; GPU: YOLO 0.0049, DeepSORT 0.0241), and even that alignment is uncertain. Latency_ms is n/r because the units are not stated and must not be converted. FPS is n/r because the column was lost. No quantization, power, or resource figures are reported. Check the tables by hand against the PDF.
