---
id: arxiv-2006.00422-ebbinnot-hardware-efficient-hybrid-event
fiche: done
date:
---

# EBBINNOT: A Hardware Efficient Hybrid Event-Frame Tracker for Stationary Dynamic Vision Sensors

Vivek Mohan, Deepak Singla, Tarun Pulluri, Andres Ussa, Pradeep Kumar Gopalakrishnan, Pao-Sheng Sun, Bharath Ramesh, Arindam Basu, 2020, arXiv preprint. https://arxiv.org/abs/2006.00422
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

EBBINNOT (Mohan et al., arXiv 2006.00422) is a hybrid event-frame pipeline for traffic monitoring with a stationary DVS. It builds event-based binary images (EBBI) at 15 Hz (tF = 66 ms), denoises them with a 3×3 median filter, and proposes regions with CCL. A YOLO-inspired NNDC CNN then merges fragmented region proposals and classifies them into 5 classes (background, car/van, bus, bike, truck). A heuristic overlap tracker (OT) follows. Critical points: (1) No hardware implementation is measured in these passages. All pipelines ran in MATLAB, and the CNN was trained in Keras on an NVIDIA TITANX GPU. There are no FPS, latency, power, LUT, DSP or BRAM numbers. The 'hardware-efficient' claim rests on analytical operation and memory counts, not on silicon or FPGA results. The 'yolo-fpga' axis tag looks wrong; the only YOLO link is the detector design. (2) Computation comparisons are estimates. SiamMask is estimated at about 38000M ops/frame and about 157MB, about 12427× the compute and about 1450× the memory of EBBINNOT. EBMS needs 252 kops/frame, 12× lower than EBBINNOT, and 3.32KB. EvFT needs about 18 Mops/frame, about 5.89× EBBINN; this is the basis for the abstract's '≈6× less computes'. The KF tracker needs about 6.5× the ops of OT, but the NNDC dominates the pipeline cost. (3) Measured accuracy on the DAVIS240C test set (Table IV) is 85.07 per-sample and 95.39 per-track (unbalanced), and 77.70 / 92.70 (balanced). The per-class values in the passage are garbled and cannot be assigned to classes reliably. (4) F1 and EAO tracking results appear only in figures (8c, 10, 12b), so no numbers are available. The authors themselves say the claim of outperforming Siamese DNNs is only 'on-par' or 'marginally worse', which weakens the abstract's claim of 'outperforming state-of-the-art deep learning'. (5) Site 3 frames were rescaled to 120×90, and pedestrians were excluded. The rows below are software accuracy results, not hardware benchmarks.
