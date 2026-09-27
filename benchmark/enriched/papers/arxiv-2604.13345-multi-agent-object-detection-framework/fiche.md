---
id: arxiv-2604.13345-multi-agent-object-detection-framework
fiche: done
date:
---

# Multi-Agent Object Detection Framework Based on Raspberry Pi YOLO Detector and Slack-Ollama Natural Language Interface

Vladimir Kalušev, Branko Brkljač, Milan Brkljač, 2026, arXiv preprint. https://arxiv.org/abs/2604.13345
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

Critical reading: This is a systems/prototype paper, not an FPGA accelerator paper. The auto-assigned axis 'yolo-fpga' looks wrong: the platform is a CPU-only Raspberry Pi 4 Model B (BCM2711, quad-core Cortex-A72 @ 1.8 GHz, 8 GB LPDDR4), with no FPGA or NPU. The contribution is a lean multi-agent architecture. A deterministic event-driven core router links four agents: a vision agent (a YOLO 'n' detector plus a passive IoU-based tracker), a reporting agent (a local Ollama LLM), and communication and control agents (a Slack chatbot). The authors present this as a lightweight alternative to LLM-driven orchestration such as OpenClaw. The evaluation is mostly qualitative: live street and indoor scenes, no named dataset, no detection accuracy metric, no power figures, and CPU load shown only in a figure (Fig. 7). The only hardware number in the passages: the full configuration (yolov8n + llama3.2:1b, all agents local) ran at 'less then 3 fps' at 640x480. The fps cell holds 3, but it is an upper bound, not a point measurement. Tested models were yolo26n, yolo11n, yolo12n, yolov5nu, yolo5su and yolov8n. yolov8n was judged best for tracking reliability because larger models lowered the frame rate and forced tracker re-initialisations. LLMs tested were tinyllama (637 MB), llama3.2:1b (1.3 GB), gemma3 (3.3 GB) and kimi-k2.5:cloud. llama3.2:1b gave the best quality/speed trade-off locally, but notifications were delayed and some were lost to timeouts. The cloud LLM gave the best results. The authors conclude that fully centralized local operation works but is not suitable for latency-critical notification, and that OpenClaw-style orchestration needs an external LLM. The code is not yet released, and the metadata extraction was flagged for manual checking.
