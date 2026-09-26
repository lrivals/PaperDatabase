---
id: 2024-alshahrani-children-s-psychological-mental-health
fiche: done
date:
---

# A Children's Psychological and Mental Health Detection Model by Drawing Analysis based on Computer Vision and Deep Learning

Amal Alshahrani, Manar Mohammed Almatrafi, Jenan Ibrahim Mustafa, Layan Saad Albaqami, Raneem Abdulrahman Aljabri, 2024, Engineering Technology & Applied Science Research. https://doi.org/10.48084/etasr.7812
Type : n/r

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

Critical reading: the paper compares YOLOv8n-cls, YOLOv9c and ResNet50 for classifying children's drawings into emotion labels (happy, sad, anxiety, anger/aggression). The dataset is a self-collected set of 500 drawings resized to 640×640 and annotated in Roboflow. The abstract reports 94 for YOLOv8-cls (top-1 after 10 epochs, 2.83 MB model), 95.1 for YOLOv9 (5.26 MB) and 70.3 for ResNet50 (94.3 MB).

Relevance: this paper has no FPGA or hardware-acceleration content. The 'yolo-fpga' axis was inferred automatically and looks wrong. The only compute platform mentioned is a Google Colab T4 GPU used for training. No FPS, latency, power, GOPS or resource figures are reported, so every hardware column is n/r.

Weaknesses:
- The model comparison mixes metric types. YOLOv8n-cls is scored with top-1 classification accuracy, while YOLOv9c is scored with detection P/R/mAP50. The 95.1 'accuracy' for YOLOv9 is never tied to a specific metric in these passages, and Table V shows 'All 91.1%' without saying which column it belongs to.
- top5_acc = 1 means nothing with only 5 classes.
- The data split is described two ways: 80/10/10 of 500, and elsewhere 500 training + 50 test + 50 validation. The test set of about 50 images is very small, and no variance or cross-validation is reported.
- There are labeling errors: Table VI is titled 'ResNet50 results' but the text says it shows YOLOv8n-cls, and Table II lists 'YOLOv8c'.
- Multi-label annotation is claimed but evaluated as single-label top-1.
- The ESRA comparison in Table IX uses a different dataset and a binary task.
- Clinical validity of the labels is not established beyond interviews with specialists.
