---
id: arxiv-2506.23115-moca-modality-aware-continual-pre
fiche: done
date:
---

# MoCa: Modality-aware Continual Pre-training Makes Better Bidirectional Multimodal Embeddings

Haonan Chen, Hong Liu, Yuping Luo, Liang Wang, Nan Yang, Furu Wei, Zhicheng Dou, 2025, arXiv preprint. https://arxiv.org/abs/2506.23115
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

MoCa (Chen et al., arXiv 2506.23115) turns causal VLMs (Qwen-2.5-VL 3B/7B) into bidirectional multimodal embedding models in two stages. Stage 1 is modality-aware continual pre-training: joint MLM on text plus MAE on image patches, about 30B tokens, 32 H100 GPUs, lr 2e-6, MAE loss weight 0.5. Stage 2 is heterogeneous contrastive fine-tuning: about 2M pairs, batch 2048, task-aware batching, tau 0.03, 2 hard negatives. Embeddings are mean-pooled. Evaluation uses MMEB (36 tasks, Precision@1) and ViDoRe-v2 (7 tasks, NDCG@5).

Critical points:
(1) This is not a hardware or accelerator paper. The H100s are only for training, and no throughput, latency, power or FPGA resource figures are given, so every hardware field is n/r.
(2) The extraction is poor (extraction.ok=false). Tables 1 and 3 have no numbers in the passages. Table 2 keeps only 2 numbers per row out of 8 columns, so which column each number belongs to is uncertain. I guessed they are the first two (ESG_Human, Eco_Mul) and marked both rows low confidence. Check them against the PDF.
(3) Claims to check: the 'new SOTA on ViDoRe-v2' claim is not visible in the numbers we have. GME-7B gets 62.9 against MoCa-3B's 62.8 in the first extracted column. The abstract's SOTA claim is explicitly about MMEB, but the text says 'outperforms all strong baselines on both benchmarks'. The claim that 3B beats 7B on ViDoRe-v2 is explained by overfitting, which is not tested.
(4) The ablation (Table 3) and the scaling claims (about 2,200 CPT steps ≈ 20B tokens; Figure 3) can't be checked here. The hyperparameter study reports MMEB test scores after choosing settings on validation sets built from the training data.
(5) The 'micro-batch size of 12,800' is unclear (it is probably tokens, not samples).
(6) The metadata axis 'continual-learning' is probably a misclassification. The method is continual pre-training for representation learning, not continual learning in the catastrophic-forgetting sense. Also, every passage is labelled '3.1.1 Modality-aware Continual Pre-training Stage' even when it covers results or ablations, which looks like a sectioning error.
