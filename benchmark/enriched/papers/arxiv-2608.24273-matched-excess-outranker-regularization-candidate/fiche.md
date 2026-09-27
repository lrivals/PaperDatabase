---
id: arxiv-2608.24273-matched-excess-outranker-regularization-candidate
fiche: done
date:
---

# Matched Excess-Outranker Regularization for Candidate-Set Interference in Continual Knowledge Graph Embedding

Hao Ren, Junbin Gao, Jiaojiao Jiang, 2026, arXiv preprint. https://arxiv.org/abs/2608.24273
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

This is not a hardware paper. It is about continual knowledge graph embedding (KGE) and reports no FPS, GOPS, latency, power or FPGA resource figures, so every hardware field is n/r. The two rows below are accuracy results only.

Claim: when new entities are added, they compete with the known answers to old queries. The paper calls this candidate-set interference and says it is a source of rank loss separate from catastrophic forgetting. It proposes Meor, a one-sided squared-hinge regularizer. Meor compares a smoothed measure of how strongly new entities score above the answer against old entities that are matched on structure without looking at model scores.

Main evidence (ENTITY–ComplEx, 8 paired runs):
- Absolute historical current-universe MRR (H_cur) is 0.0887, the highest in Table 2.
- The gain over replay is 0.0057 (one-sided 95% lower bound 0.0052). Almost all of it comes from a 0.0055 drop in interference (D_MCI); old-universe MRR changes by only 0.0002.
- Gains over persistent calibration, the matched-maximum control (MMR) and the unmatched-reference control (UOR) are 0.0071, 0.0051 and 0.0045.
- In the transfer study, all 10 FBInc-S/L host and backbone settings improve, with gains of about 0.0020–0.0032 and every CI excluding zero.

Critical points:
1. The effects are small in absolute terms. 0.0057 MRR is about 6% relative on a base of about 0.089. The overall MRR level is low.
2. During refinement, old embeddings are frozen and only new parameters are updated. That setup favours the interference framing and limits how far the result generalises to hosts that update all parameters.
3. Newcomer acquisition (A_TN) goes slightly down in every transfer setting (−0.0001 to −0.0015). It stays within the paper's own −0.005 preservation margin, but that margin was chosen by the authors.
4. The CIs are unadjusted per-cell intervals, not family-wise.
5. Persistent calibration beats Meor on A_TN by 0.0038. H_old and D_MCI were not recorded for calibration.
6. The authors say the intervention is inactive on WN-CKGE, so claims are limited to ENTITY and FBInc.
7. Most numbers in Tables 2–5 did not survive PDF extraction. The absolute H_old, D_MCI and A_TN values are missing and need checking against the PDF.
8. The metadata and axes are flagged for manual verification.
