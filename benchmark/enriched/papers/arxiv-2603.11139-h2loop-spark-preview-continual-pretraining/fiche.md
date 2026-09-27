---
id: arxiv-2603.11139-h2loop-spark-preview-continual-pretraining
fiche: done
date:
---

# H2LooP Spark Preview: Continual Pretraining of Large Language Models for Low-Level Embedded Systems Code

Amit Singh, Vedant Nipane, Pulkit Agrawal, Jatin Kishnani, Sairanjan Mishra, 2026, arXiv preprint. https://arxiv.org/abs/2603.11139
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

Scope: I only had the abstract. The other passages are table captions without data (Tables 1–22), so results in the per-category, generative-accuracy, FullStackBench and throughput tables couldn't be extracted. The metadata is marked as needing a manual check (extraction ok=false).

Summary: H2LooP Spark Preview continues pretraining OLMo-3-7B on embedded-systems code, from about 23.5B curated tokens (818 repository-datasheet pairs, 76.4 GB raw, 117 manufacturers, 19 component categories), using SpecMap-based datasheet-to-code mapping. It trains with BF16 LoRA using rank-stabilized scaling at r=512 on all modules, on 8× H100 80GB.

Reported results: after 5.2B tokens (about 36% of one epoch), in-domain perplexity falls from 4.06 to 1.20 (−70.4%) and held-out-repository perplexity from 3.92 to 1.33 (−66.1%). Both percentages check out against the raw numbers.

Critical points:
(1) Perplexity is measured on the authors' own corpus split. 'Held-out' means unseen repositories, but it may still share vendor SDK and HAL boilerplate with training data, so the drop may partly reflect memorized boilerplate.
(2) The claim that the model beats Claude Opus 4.6 and Qwen3-Coder-30B on 8 of 13 categories uses token accuracy, not functional correctness, and the abstract gives no numbers.
(3) Training stopped partway through the first epoch, so this is a preview checkpoint.
(4) The hyperparameter search was large (more than 1,400 runs, about 4,240 GPU-hours), but the sweep conclusions come from 10 Bayesian configurations (Table 7).
(5) There are no FPGA or inference hardware metrics (FPS, latency, power, LUT/DSP/BRAM). The only hardware information is the training platform and GPU-hour cost.

Rows below are model-quality results on the training platform, with the base model's perplexity as the baseline.
