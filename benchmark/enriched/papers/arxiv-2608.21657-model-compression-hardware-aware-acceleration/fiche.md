---
id: arxiv-2608.21657-model-compression-hardware-aware-acceleration
fiche: done
date:
---

# Model Compression and Hardware-Aware Acceleration for Deep Learning on FPGAs: A Co-Design Taxonomy and Comparative Analysis

Peter Forcha, H. Kajekusumadhar, Mbua Peter, Muhammed Kawser, Audrey Cyriell Mo, Christophe Bobda, 2026, arXiv preprint. https://arxiv.org/abs/2608.21657
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

Survey (arXiv 2608.21657, 2026) of 25 FPGA compression–hardware co-design case studies from 2015–2026. The authors sort them into a five-category taxonomy based on which FPGA resource each technique mainly changes: (A) removes DSPs, (B) repurposes DSPs or uses mixed precision, (C) exploits sparsity, (D) targets the memory hierarchy, (E) works at the toolchain or deployment level. Table I puts every study into the same columns: compression ratio, accuracy change, throughput, energy efficiency, DSP/LUT/BRAM usage and baseline. The main finding is that only 1 of 25 works reports compression ratio and accuracy change against one common baseline. Only 2 report energy efficiency against a common GPU baseline. Throughput, energy efficiency and DSP/LUT/BRAM usage are the fields most often missing. The paper ends with a six-item research agenda (Table V) that pairs each challenge with a concrete next step.

Strengths:
- The FPGA-only, resource-level focus goes deeper than the cross-platform survey by Deng et al.
- Missing values are marked explicitly: N/R for not reported, N/A for not applicable, and a dash for ASIC studies.
- The authors say plainly that the literature search was targeted and not systematic (not PRISMA), so the meta-analytic counts describe these 25 studies, not the whole field.

Weaknesses and caveats:
- The survey produces no new measurements. Every hardware number is taken from the cited primary papers and should be checked against them.
- ASIC studies (NullHop, Eyeriss, the HLS4ML 65 nm energy figure) sit in the same table as FPGA studies, which makes comparisons harder.
- Studies were placed in categories by the authors' judgement, and some span two categories (for example FlightLLM).
- The extracted text of Table I is garbled: columns run together, and the DSP cell for the FINN row is broken.
- The extraction metadata is flagged for manual checking.

About the rows: both rows are secondary citations of the primary works. The FINN row comes from the Table I text. The Zhang et al. figure is given in GFLOPS (floating point), not GOPS; it is copied into the gops field as-is, without conversion.
