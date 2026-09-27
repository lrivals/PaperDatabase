---
id: arxiv-2411.02564-continual-llava-continual-instruction-tuning
fiche: done
date:
---

# Continual LLaVA: Continual Instruction Tuning in Large Vision-Language Models

Meng Cao, Yuyang Liu, Yingfei Liu, Tiancai Wang, Jiahua Dong, Henghui Ding, Xiangyu Zhang, Ian Reid, Xiaodan Liang, 2024, arXiv preprint. https://arxiv.org/abs/2411.02564
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

Continual LLaVA is a rehearsal-free method for continual instruction tuning of large vision-language models (LVLMs). The LVLM stays frozen. The method trains a low-rank pool of proxy-increment pairs (0.75M tunable parameters), selects the top-M pairs by cosine similarity with a Sentence-BERT embedding of the instruction ("intrinsic increments"), and combines a learnable weighted sum of increments chosen in earlier tasks ("contextual increments"). The dual increment embeddings are re-parameterized into the output linear layer. The paper also introduces the COAST benchmark with three settings: domain, capability and dataset. The supplied passages contain no hardware measurements (no FPS, latency, power or FPGA resources), so the rows record accuracy and forgetting results only.

Headline results on COAST-domain: average accuracy 37.08, which is 13.06 above sequential training. Average forgetting is 2.58, compared with 15.83 for sequential training and 15.61 for rehearsal. These numbers average three task orders.

Caveats:
- Accuracy is graded by GPT-4o rather than exact match, so it depends on the grader and is hard to reproduce.
- The parameter counts don't match. The tables list 6.76B parameters for full tuning, but the text says 7.67B.
- The comparison mixes different parameter budgets: the prompt-based baselines use 0.75M parameters, while full fine-tuning uses 6.76B.
- Task order matters on COAST-capability: the dcrf order gives 51.47 accuracy and 8.96 forgetting.
- Ablations: removing the alignment loss costs 6.80 accuracy, and removing the intrinsic increment ∆θ costs 3.71. Choosing output-layer adaptation over all-layer adaptation rests on a 0.09 gap.
- The supplied text does not state the LVLM backbone or its size.
