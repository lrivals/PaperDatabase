---
id: 2022-viswanatha-iot-smart-mirror-raspberry-pi
fiche: done
date:
---

# IoT Based Smart Mirror Using Raspberry Pi 4 and YOLO Algorithm: A Novel Framework for Interactive Display

V Viswanatha, R K Chandana, Ramachandra A C, 2022, Indian Journal of Science and Technology. https://doi.org/10.17485/ijst/v15i39.1627
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

Critical reading: This is an IoT smart-mirror prototype. A Raspberry Pi with a camera, PIR sensor and touch sensor runs YOLOv5 object detection for intrusion and human monitoring, emails captured images to the owner, and shows weather, time, news and calendar text on the mirror. Reported numbers: none. The Results section (3 Results and Discussion) describes hardware tests only in qualitative terms (Fig. 11 detection output, Fig. 12 email notification). It gives no accuracy, mAP, FPS, latency, power or resource figures, no dataset and no baseline comparison. The claims of "more accuracy", faster detection and "highest level of accuracy and precision" have no supporting evidence. Inconsistencies: the title and Results say Raspberry Pi 4, but the Abstract says Raspberry Pi 3. The Introduction describes intrusion detection by background subtraction or frame differencing, while the Results credit YOLOv5. The Methodology describes a face-recognition pipeline (alignment, anti-spoofing, Euclidean/angular loss) that is never evaluated. The Conclusion mentions "experimental results for several approaches", but no such results appear in the supplied passages. Relevance: there is no FPGA or accelerator content, so the automatically assigned 'yolo-fpga' axis looks wrong. This paper should be reclassified as embedded CPU/IoT. One row is recorded only to log the qualitative hardware demonstration. Every metric is n/r.
