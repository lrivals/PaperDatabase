---
id: arxiv-2112.09660-ai-assisted-verification-biometric-data
fiche: done
date:
---

# AI-Assisted Verification of Biometric Data Collection

Ryan Lindsey, 2021, arXiv preprint. https://arxiv.org/abs/2112.09660
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

Critical reading: this is a short student preprint on detecting a BACtrack breathalyzer and a face in an Android front-camera feed, to check that biometric data was collected correctly. It is not an FPGA paper, so the automatically assigned 'yolo-fpga' axis looks wrong and should be removed or checked. Method: YOLOv3 in Darknet, with only the last few layers retrained (the rest were frozen) on a custom dataset of about 800 images, labelled with LabelImg and augmented with Roboflow. Training ran on a University of Kentucky HPC cluster using a Docker container converted to Singularity and submitted as SLURM jobs. The only measured hardware result in these passages is 'around 20FPS' for full YOLOv3 on a webcam feed on an unnamed 'standard desktop'. The CPU/GPU, input resolution, precision, latency and power are not given. The model weights take 250Mb, which is too large for Android. Retraining with YOLOv3-tiny gives a 35Mb file with 'similar accuracy', but the passage is cut off before any tiny-model or on-phone throughput is reported. No accuracy metric (for example mAP) is reported anywhere. The abstract promises a comparison across devices with and without GPUs, but that data is not in the supplied passages. Because of this, only one row is extracted, with medium confidence: the FPS figure is approximate and the platform is unspecified. The metadata is flagged 'to verify by hand' (extraction ok=false).
