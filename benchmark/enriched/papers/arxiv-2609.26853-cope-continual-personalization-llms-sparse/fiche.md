---
id: arxiv-2609.26853-cope-continual-personalization-llms-sparse
fiche: done
date:
---

# COPE: Continual Personalization of LLMs under Sparse User Feedback via User Embeddings and Self-Evaluation

Ruike Cao, Fugen Yao, Liang Dong, Jian Xu, Guanjun Jiang, Li Xiao, 2026, arXiv preprint. https://arxiv.org/abs/2609.26853
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

COPE (arXiv 2609.26853) is an LLM continual-personalization method, not a hardware paper. None of the supplied passages reports a measured hardware result: no FPS, GOPS, latency, power, or FPGA resource figures. So all hardware fields are n/r, and the two rows only record task-quality scores.

**Method:** Each user gets a learnable personalized embedding (l=10 virtual tokens, about 1.2e-5 of Qwen3-1.7B's parameters per user). A single on-policy PPO update step combines three objectives:
- L_SFT: textual feedback trains the embedding only (model weights frozen).
- J_eval: self-evaluation calibration; updates both the embedding and the model weights.
- J_policy: a reward equal to completeness × personalization; updates the model weights only.
When users give no feedback, the self-evaluated score serves as a proxy reward.

**Setup:** PersonaLens benchmark, 256 users with 17 domains each. The model is updated after each of the first 51 interactions (3 tasks × 17 domains), and a fourth traversal is held out for testing. The metric is personalization score × binary completeness, out of 10, reported as mean±std over 3 runs.

**Results:** At p=0.75, COPE scores 4.74 vs 3.69 for PAP (the best training-free baseline). COPE+SR is best in every setting, peaking at 5.36; T-PAP+SR reaches 4.98. The ablations show that removing J_eval hurts most (3.36 vs 4.69). The score rises with model size (Qwen3 1.7B → 8B: 4.69 → 5.49), and Llama-3.1-8B-Instruct reaches 5.16.

**Critical points:**
1. Users, feedback, and completeness judgments are all simulated by LLMs (the Qwen-Flash simulator and evaluator). This creates a risk of closed-loop or same-family bias. The authors check this by swapping in a DeepSeek-V3 simulator and running a blinded comparison with one human annotator on 204 response pairs, but a single annotator is weak evidence.
2. The self-evaluation proxy agrees with the user on only 72.63% of the pairs where both give a directional judgment. The population-level correlation is r=0.81 during training and 0.71 on held-out runs.
3. Table 1's row labels are lost in the extracted text. Only T-PAP+SR and COPE+SR can be identified directly; the COPE and PAP values come from the prose.
4. No training cost, latency, or compute overhead is reported. The prose mentions PAP's extra latency qualitatively but gives no numbers.
5. Evaluation covers a short horizon (51 updates), and the general-capability results are deferred to Appendix K, which was not supplied.
