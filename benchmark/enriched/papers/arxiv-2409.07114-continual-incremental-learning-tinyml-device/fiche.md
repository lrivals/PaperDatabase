---
id: arxiv-2409.07114-continual-incremental-learning-tinyml-device
fiche: done
date:
---

# A Continual and Incremental Learning Approach for TinyML On-device Training Using Dataset Distillation and Model Size Adaption

Marcus Rüb, Philipp Tuchel, Axel Sikora, Daniel Mueller-Gritschneder, 2024, 2024 IEEE 7th International Conference on Industrial Cyber-Physical Systems (ICPS). https://doi.org/10.1109/ICPS59941.2024.10639989
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

Critical reading: The paper proposes TinyML continual/incremental learning that stores a distilled replay set (distribution matching with DSA, distilled on ConvNetD4) and grows the model when validation accuracy falls below a threshold (ConvNetD2→D3→D4). None of the supplied passages reports a measured hardware result: there is no MCU deployment, latency, power or memory measurement. Cost is reported only as training FLOPs relative to a fixed ConvNetD4 (43% CIFAR10*, 49% CORe50, 36% Speech Commands/HAR/MNIST), so claims about energy and time savings are inferred, not measured. Issues: (1) *The results text cites 'Table 1' without naming its dataset. CIFAR10 is inferred only because the discussion matches CIFAR10 to 43% FLOPs, and the supplied captions label Table II as CORe50 and Table IV as MNIST. (2) The accuracy-loss claims disagree: the abstract says ~1%, the conclusion says 0.4% on average, and the discussion gives +0.3% for CIFAR10 and −2.8% for CORe50. (3) The optimizer is contradictory (SGD with momentum 0.9 vs Adam at lr 0.01). (4) 'Baseline' in Results means cumulative full-data training, but in Related Work 'baseline' (19.39) refers to the naive approach. The comparison with CWR, LwF and EWC from [5] uses a different model and a different resolution (128 vs 64). (5) Several adaptive-model accuracies are only approximate ('~70', '92% range', 'mid-60%'), so no rows were made for them. (6) The kernel description '8, 64, 128 kernels' per depth is ambiguous. The rows below are algorithm-level results from simulation, not hardware benchmarks.
