---
id: 2023-perez-cerrolaza-artificial-intelligence-safety-critical-systems
fiche: done
date:
---

# Artificial Intelligence for Safety-Critical Systems in Industrial and Transportation Domains: A Survey

Jon Perez-Cerrolaza, Jaume Abella, Markus Borg, Carlo Donzella, Jesús Cerquides, Francisco Javier Cazorla, Cristofer Englund, Markus Tauber, George Nikolakopoulos, José Luis Flores, 2023, ACM Computing Surveys. https://doi.org/10.1145/3626314
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

Survey (ACM Computing Surveys 2023) on building AI-based safety-critical systems in industrial and transportation domains, covering systems from traditional functional safety (FuSa) to autonomous ones. It proposes a taxonomy with five parts: types of AI (connectionists, Bayesians, symbolists, analogizers, optimization); levels of automation (automatic, heteronomous, autonomous); safety standards (FuSa: IEC 61508 and ISO 26262; heteronomous/SOTIF: ISO/PAS 21448; autonomous: UL 4600 and VDE-AR-E2842-61; AI and safety: ISO 5469 and ISO/AWI PAS 8800); where AI is applied (product, runtime, process); and compliance classes I, II and III. The main technical point is how products reach FuSa compliance. Class I relies on offline formal verification. Class II relies on runtime compensation such as a safety bag or diverse monitor (IEC 61508-7 C.3.4), which makes the monitor the safety function. One example is a SIL4 railway interlocking system. Uncertainty management runs through the survey: the 'semantic gap' between intended and specified functionality, data quality and train/test split requirements, and the fact that formal verification is limited to moderate-size NNs. The section on the inference execution platform (GPU, FPGA, multicore, specialized DNN accelerators; hypervisors, ROS, AUTOSAR, TensorRT/cuDNN; Vulkan SC and OpenGL SC) is a qualitative literature map of random-error diagnostics and fault tolerance. Limitations: this is a survey with no experiments of its own. None of the supplied passages report a measured hardware result (no FPS, GOPS, latency, power or FPGA resource figures) or an accuracy number, so I produced no benchmark rows. FPGA-related claims only point to cited works [34, 101], which would have to be read separately. PDF extraction found no section headings, so every passage is under '(préambule)'. Several tables (Tables 1–6) came through fragmented or as captions only, so the classification mappings between studies and techniques should be checked against the original PDF. The metadata is flagged for manual checking.
