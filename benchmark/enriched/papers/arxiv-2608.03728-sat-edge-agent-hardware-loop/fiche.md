---
id: arxiv-2608.03728-sat-edge-agent-hardware-loop
fiche: done
date:
---

# SAT-Edge-Agent: Hardware-in-the-Loop Edge-Agent Orchestration for Onboard Satellite Intelligence

Longji He, Jeto Xu, 2026, arXiv preprint. https://arxiv.org/abs/2608.03728
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

SAT-Edge-Agent (He & Xu, arXiv 2608.03728, 2026) is a systems paper about hardware-in-the-loop (HIL) orchestration. It is not a detector or FPGA paper. A FastAPI agent runs on a COTS ARM heterogeneous edge SoC (8x Cortex-A55 up to 2304 MHz, 31 GiB memory, Debian 11 on aarch64) with an NPU. The agent coordinates a local OpenAI-compatible LLM and a project-internal YOLO-style oriented-bounding-box (OBB) detector labelled "YOLO26". The paper says this label is not a public detector family. The detector runs at image size 1024 with object threshold 0.25 and NMS threshold 0.45.

Evidence: two fixed FAIR1M workloads (one image and two images run serially), 20 runs each, all 20 completed for both. Mean Full-Agent latency was 29.353 s and 60.937 s, with P95 of 31.166 s and 66.882 s. Mean YOLO-tool time was 861.386 ms and 1510.920 ms, which is 2.93% and 2.48% of the Full-Agent mean. Mean CPU use was about 20.7% and 20.5%. The NPU-load field read 100%, but the detector and the LLM share the accelerator, so this is not detector-only occupancy.

Critical points:
- The authors say explicitly that there is no accuracy benchmark, no validated geolocation error, no calibrated energy result and no flight readiness.
- n=20 on two fixed images is too few to describe the latency distribution for FAIR1M as a whole.
- The detector weights, exact board vendor and exact LLM are private.
- A factor-of-two aggregation bug meant the substage fields had to be excluded.
- The Table 10 plug-meter power values are not in the supplied passages, so power is n/r.
- The paper is tagged yolo-fpga, but no FPGA is involved, so LUT, DSP and BRAM are n/r. This axis tag should be rechecked.
- The latency_ms field in the rows holds the detector-stage YOLO-tool mean, which the paper reports in ms. The Full-Agent latencies are in seconds and were left unconverted; they appear in the baseline field.
