---
id: arxiv-1907.08349-convergence-edge-computing-deep-learning
fiche: done
date:
---

# Convergence of Edge Computing and Deep Learning: A Comprehensive Survey

Xiaofei Wang, Yiwen Han, Victor C. M. Leung, Dusit Tao Niyato, Xueqiang Yan, Xu Chen, 2020, arXiv preprint. https://doi.org/10.1109/comst.2020.2970550
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

Survey paper (Wang et al., IEEE COMST 2020, arXiv 1907.08349). It frames "edge intelligence" (DL services deployed at the edge) and "intelligent edge" (DL used to manage the edge) as two sides of "Edge DL". The survey is organized into five areas: DL applications on the edge, DL inference in the edge, edge computing for DL, DL training at the edge, and DL for optimizing the edge. The supplied passages give background: edge paradigms (Cloudlet/MDC, Fog, MEC, collaborative end-edge-cloud), edge AI hardware grouped as GPU, FPGA or ASIC (Table II), DL libraries for edge devices (Table III), virtualization (VM vs container, NFV) and DNN/DRL/distributed-training basics. Critical remarks: (1) None of the supplied passages reports a measured hardware result. The hardware characterizations are qualitative vendor-style claims: GPUs are compatible but power-hungry, FPGAs are energy-saving but hard to program, ASICs are stable. The '5 Watts' figure for NVIDIA Jetson is marketing copy quoted in Table II, not a benchmark. (2) The FPGA discussion is brief and not quantified. The text defers to [51], [52] and [54] for performance comparisons, so no FPS, GOPS, LUT or DSP figures can be taken from this source. (3) The introduction's statistics (50 billion IoT devices by 2020, 850 ZB of data at the edge vs 20.6 ZB of data center traffic by 2021) are Cisco projections, not measurements. (4) Tables IV–VII (edge node solutions, communication modes, federated learning (FL), DL for optimizing the edge) appear only as captions, so their content could not be checked. (5) Extraction metadata is flagged unverified. Venue is listed as arXiv preprint, but the DOI points to IEEE COMST. For benchmark rows, go to the primary works this survey cites. No rows are returned because the supplied passages contain no measured experimental result.
