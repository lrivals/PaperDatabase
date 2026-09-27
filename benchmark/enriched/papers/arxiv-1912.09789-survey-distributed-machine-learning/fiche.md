---
id: arxiv-1912.09789-survey-distributed-machine-learning
fiche: done
date:
---

# A Survey on Distributed Machine Learning

Joost Verbraeken, Matthijs Wolting, Jonathan Katzy, Jeroen Kloppenburg, Tim Verbelen, Jan S. Rellermeyer, 2020, arXiv preprint. https://doi.org/10.1145/3377454
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

Critical reading note: this is a survey (Verbraeken et al., ACM CSUR, arXiv 1912.09789) covering distributed ML. It covers scale-up versus scale-out, data versus model parallelism, topologies (centralized/ensembling, tree/AllReduce, ring, parameter server, peer-to-peer), synchronization models (BSP, SSP, ASP, BAP/TAP), and systems (Hadoop/Spark MLlib, Baidu ring-AllReduce, Horovod, Caffe2/Gloo, DistBelief, MXNet KVStore, DMTK, Petuum). It closes with open challenges: performance/efficiency, fault tolerance, privacy and portability (ONNX).

The paper reports no experiments of its own and no FPGA work. Every number is a claim cited from another paper. Examples:
- DianNao: about 1000x speedup and more than 20x less energy than a 128-bit SIMD CPU.
- Deep compression: 2.9x throughput and 19x energy efficiency over DianNao. The survey credits this to Hinton et al. [70], which looks like a misattribution (it matches EIE by Han et al.).
- Horovod: about 88% GPU utilization on 128 GPUs.
- Caffe2: ResNet-50 in 1 hour with 90% scaling efficiency on up to 352 GPUs.
- DistBelief: 80% less training time using more than 500 machines.
- MXNet: near-linear speedup on 10 GPU machines.

Limitations: the cited figures do not share workloads, baselines or metrics, so they cannot be compared directly. Utilization and scaling efficiency are not accuracy or throughput. The PDF extraction found no section headings, so every passage sits under '(préambule)'. Metadata still needs checking by hand. The rows below are secondary figures cited by the survey. They are marked low confidence and should be checked against the original Horovod paper (Sergeev and Del Balso) and the Caffe2 paper (Goyal et al.) before any use.
