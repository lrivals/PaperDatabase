---
id: 2010-bouwmans-background-modeling-mixture-gaussians-foreground
fiche: done
date:
---

# Background Modeling using Mixture of Gaussians for Foreground Detection - A Survey

Thierry Bouwmans, Fida El Baf, Bertrand Vachon, 2010, Recent Advances in Computer Science and Communications. https://doi.org/10.2174/1874479610801030219
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

Survey (Bouwmans, El Baf, Vachon) of Mixture-of-Gaussians (MOG) background modeling for foreground detection with static cameras. It sorts improvements to Stauffer & Grimson [1] into two groups. Intrinsic improvements change the model itself: adaptive number of Gaussians K (Zivkovic [94], Cheng [95], Shimada [96], Tan [97], Carminati [98]), initialization (EM [99], approximated EM [84], training sequences that contain foreground [60, 82, 83]), maintenance rules and mechanisms (Kalman [38], counters [60, 70], CUSUM [85]), learning-rate adaptation (PSO tuning of alpha/T [138], variable rates [87, 136, 139, 140]), foreground detection (likelihood/MAP, Jeffreys divergence, PPM, explicit foreground model [57, 85, 109]), and features (block-wise [145, 146], cluster-wise [147]). Extrinsic improvements add spatial or temporal post-processing such as MRF [153], S-TAPPMOG [43] and ASTNA [92].

Section 7 ('7. PERFORMANCE EVALUATION') gathers published Wallflower results as FP, FN and Total Error (TE). The per-sequence Table 5 values are not in the supplied passages. The only qualitative claims are: PSO roughly halves TE; IHLS brings TE 'just under 10 0000' (the digit grouping is ambiguous: 10000 or 100000?); Wang et al. [70] is the best intrinsic method; MRF [153] is the best overall, followed by S-TAPPMOG and ASTNA; Light Switch gives the most false positives. S-TAPPMOG and ASTNA do not report results for MO, TOD or LS, so their totals are not comparable to the others.

Critical points:
- All numbers come from other papers, not from the authors' own runs. No common implementation, parameters or post-processing were used.
- TE is a raw pixel count. It has no normalization, precision/recall or F-measure.
- The survey does not report hardware, FPS, latency or power. Real-time and computation-time constraints are only discussed qualitatively, and those sections are not supplied.
- Metadata conflict: the record says 2010, Recent Advances in Computer Science and Communications. The HAL preamble cites Recent Patents on Computer Science, 2008, 1(3), pp. 219-237 (hal-00338206). This needs manual checking.

No benchmark rows were produced. The passages contain no measured hardware result, and no exact accuracy value can be copied because Table 5's contents are missing.
