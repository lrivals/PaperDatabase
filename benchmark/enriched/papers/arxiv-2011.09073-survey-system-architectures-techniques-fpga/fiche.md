---
id: arxiv-2011.09073-survey-system-architectures-techniques-fpga
fiche: done
date:
---

# A Survey of System Architectures and Techniques for FPGA Virtualization

Masudul Hassan Quraishi, Erfan Bank Tavakoli, Fengbo Ren, 2020, arXiv preprint. https://arxiv.org/abs/2011.09073
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

Survey (Quraishi, Bank Tavakoli, Ren, arXiv 2011.09073, 2020) on FPGA virtualization for cloud and edge computing. It sorts prior work in two ways. First, by system-architecture stack: hardware (host interface on-chip/local/remote, shell, role with PRRs and DPR), software (OS, host application, and frameworks such as OpenStack), and overlay (intermediate fabrics and CGRA/NoC-based overlays). Second, by four objectives it proposes: abstraction, multi-tenancy, resource management, and isolation. It narrows the objective list from an earlier survey [13], arguing that scalability, performance, and resilience apply to cloud and edge computing in general rather than to FPGA virtualization specifically, and that flexibility and programmer's productivity belong to HLS. Tables 1–2 map each surveyed system (e.g., Catapult, Feniks, AmorphOS, VFR, RC3E, Ker-ONE, pvFPGA) to its host interface, shell, role, software stack, programming model, application, platform, and techniques. Stated future directions: vFPGAs that span more than one physical FPGA (most work limits a vFPGA to one PRR on one device), isolation (functional, performance, and fault), which is under-explored, and multi-tenant, scalable virtualization for DNN accelerators. Critical points: (1) The supplied passages contain no measured hardware results — no throughput, latency, power, resource-use, or overhead numbers — so no benchmark rows are given. The overheads of overlays and virtualization (lower performance, less efficient resource use, reconfiguration time) are described only qualitatively. (2) Claims such as 'an order of magnitude lower power' and 'up to two orders of magnitude more energy-efficient' than CPUs and GPUs are cited from other papers, not measured here. (3) The tables are summaries with many N/A and N/M entries, and the rows are truncated in the extraction. (4) Coverage stops in 2020. (5) The extraction reported that no sections were detected, so every passage except the Abstract is labelled '(préambule)'; metadata still needs checking by hand.
