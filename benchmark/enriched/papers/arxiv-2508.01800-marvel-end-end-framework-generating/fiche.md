---
id: arxiv-2508.01800-marvel-end-end-framework-generating
fiche: done
date:
---

# MARVEL: An End-to-End Framework for Generating Model-Class Aware Custom RISC-V Extensions for Lightweight AI

Ajay Kumar M, Cian O'Mahoney, Pedro Kreutz Werle, Shreejith Shanker, Dimitrios S. Nikolopoulos, Bo Ji, Hans Vandierendonck, Deepu John, 2025, arXiv preprint. https://arxiv.org/abs/2508.01800
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

MARVEL is an automated flow that profiles TVM-generated bare-metal C for CNNs and turns the patterns it finds into custom RISC-V ISA extensions. It takes Python/Keras models, uses Apache TVM to emit generic C, then Synopsys ASIP Designer (nML/PDG plus Chess compiler rewrite rules) to extend the trv32p3 core, and Vivado to target a ZCU104 FPGA. The processor versions build on each other: v1 adds mac (fixed registers x20–x22), v2 adds add2i (5-bit and 10-bit unsigned immediates), v3 adds fusedmac and v4 adds zero-overhead hardware loops (zol).

Strengths: the extensions come from instruction-level profiling rather than assumed hotspots. The add2i immediate coverage is reported per model (100 for LeNet-5*, 86.03 for MobileNetV1, 75.19 for ResNet50, 66.89 for VGG16, 71.39 for MobileNetV2, 95.13 for DenseNet121). The paper also counts blt executions to justify the hardware-loop extension. Unlike AI-RISC, it needs no changes to TVM.

Weaknesses and caveats:
- The only measured hardware figures in these passages are aggregates in the Abstract: 2x inference speedup, up to 2x less energy per inference, and 28.23 area overhead versus the trv32p3 baseline on ZCU104. Per-model latency, energy, power and LUT/DSP/BRAM numbers were not supplied; Tables 8 and 10 appear only as captions.
- The models are simplified. Inputs are 64x64x3 and the task is binary Car/Not-Car, fine-tuned on StanfordCars and COCO. No accuracy figures are given.
- Profiling was done on MobileNetV1 only; the claim that the patterns hold across the model class rests on pattern counts.
- Fixing the mac registers reduces register-allocation flexibility.
- The LLVM front-end cannot infer custom instructions, so the choice of front-end matters.
- Metadata tag 'finn' is misleading: FINN is mentioned only as a contrasting tool and is not used. The 'mobilenet' and 'zcu104' tags are correct.
