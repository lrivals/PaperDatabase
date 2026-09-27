---
id: arxiv-1904.08405-event-vision-survey
fiche: done
date:
---

# Event-Based Vision: A Survey

Guillermo Gallego, Tobi Delbruck, Garrick Orchard, Chiara Bartolozzi, Brian Taba, Andrea Censi, Stefan Leutenegger, Andrew J. Davison, Jorg Conradt, Kostas Daniilidis, Davide Scaramuzza, 2020, arXiv preprint. https://doi.org/10.1109/tpami.2020.3008413
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

Critical reading note: Gallego et al., 'Event-Based Vision: A Survey' (TPAMI 2020, arXiv 1904.08405). This is a survey, not a hardware accelerator paper. It covers how event cameras work, the main sensor designs, event representations (event frames, time surfaces, voxel grids), SNN and bio-inspired processing, and applications such as feature tracking, optical flow, depth estimation, VO/VIO and image reconstruction. The only measured hardware result in the passages is the DVS128 pixel frequency response (Fig. 2). Pixel bandwidth is about 3 kHz under bright light, which the survey equates to an exposure time of about 300 µs. At 1000× lower intensity it falls to about 300 Hz, which is still ten times the 30 Hz Nyquist frequency of a 60 fps frame camera. Other numbers are approximate or taken from cited work, not measured by the authors: latency of about 10 µs on the lab bench, die power of about 10 mW, embedded system power of 100 mW or less, dynamic range above 120 dB (the abstract says 140 dB, the body says >120 dB, so the two are inconsistent), and readout rates from 2 MHz to 1200 MHz. The authors say the Table 1 numbers 'were not measured using a common testbed'. The survey stresses several times that there are no common benchmarks for optical flow or depth estimation, and that trade-offs between accuracy, efficiency and latency are not quantified. None of the passages report FPGA/LUT/DSP/BRAM, GOPS or FPS figures. I left latency (µs) and power (mW) values out of the rows because the columns use ms and W, and the task said not to convert units. Extraction caveats: PDF extraction flagged 'no sections detected', so almost every passage is labelled '(préambule)'. Metadata and axes still need to be checked by hand. The benchmark rows record pixel bandwidth in the accuracy fields as a proxy metric, so they are not comparable to accelerator benchmarks.
