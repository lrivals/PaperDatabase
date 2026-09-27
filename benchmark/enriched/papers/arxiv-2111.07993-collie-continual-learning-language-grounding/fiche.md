---
id: arxiv-2111.07993-collie-continual-learning-language-grounding
fiche: done
date:
---

# CoLLIE: Continual Learning of Language Grounding from Language-Image Embeddings

Gabriel Skantze, Bram Willemsen, 2021, arXiv preprint. https://arxiv.org/abs/2111.07993
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

CoLLIE (Skantze & Willemsen) keeps CLIP frozen, with the ViT-B/32 backbone by default. It learns a transform of the text embedding, T(t) = t + A(t) × S(t). A(t) is an adjustment function that predicts a difference vector. S(t) is a scaling function (SVR, KNN, etc.) that decides how much of that adjustment to apply. The model keeps only the new examples' embeddings plus a fixed set of negative examples, and retrains the small transform after each round. The metric is MRR for ranking candidate images.

Experiment I (LAD, new pseudo-words for known objects, |Ctrain| = 50):
- CoLLIE reaches 0.618 MRR after 1 example and 0.750 after 5. CLIP's zero-shot MRR on the original words is 0.773.
- A logistic-regression few-shot classifier does slightly better on the new words (0.805 after 5 examples).
- Retention after the final round is 0.699 for Ctrain and 0.719 for Cother, against 0.760 and 0.769 for static CLIP.
- Without the scaling function, retention collapses to 0.260 and 0.242.

Experiment II (KTH Tangrams, 85 candidates):
- CLIP zero-shot MRR is 0.310. CoLLIE reaches 0.860 after 30 rounds, averaged over 3,000 iterations.
- Compositional test (train on 17 shapes in one color, test on other colors): 0.857 vs 0.317 for CLIP.
- Synonym test: 0.602 vs 0.290.

Critical points:
- (1) Evaluation is small-scale and synthetic: pseudo-words from the NOUN database, 85 tangram images, and a limited synonym test that the authors describe as limited.
- (2) Retention gets worse as N grows, especially with only 100 negative examples. The authors say scaling for large N is future work.
- (3) The few-shot baseline beats CoLLIE on pure label learning in Experiment I.
- (4) Performance is bounded by the frozen CLIP representation.
- (5) The retention figures are in the text, but the numeric contents of Tables 1–4 are missing from the supplied passages.
- (6) No hardware, latency, power or FPGA results are reported. All hardware columns are n/r. The schema field 'bram' is unrelated to co-author Bram Willemsen.

Metadata issues: the preamble shows the paper was published in JAIR 74 (2022), pages 1201–1223, not only as a 2021 arXiv preprint. Venue, year and type should be corrected. Extraction status is ok=false.
