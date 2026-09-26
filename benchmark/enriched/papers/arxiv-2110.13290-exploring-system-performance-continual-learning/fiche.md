---
id: arxiv-2110.13290-exploring-system-performance-continual-learning
fiche: done
date:
---

# Exploring System Performance of Continual Learning for Mobile and Embedded Sensing Applications

Young D. Kwon, Jagmohan Chauhan, Abhishek Kumar, Pan Hui, Cecilia Mascolo, 2021, arXiv preprint. https://arxiv.org/abs/2110.13290
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

Critical reading note — Kwon et al., "Exploring System Performance of Continual Learning for Mobile and Embedded Sensing Applications" (SEC '21 / arXiv 2110.13290).

What the paper does: It is an empirical study, not a new method or accelerator. It tests six incremental-learning (IL) methods from three families on an LSTM base model: regularization (EWC, Online EWC, SI), replay (LwF) and replay with exemplars (iCaRL, GEM). No-IL ('None') and a jointly trained model ('Joint') serve as reference points. The data are six sensing datasets covering human activity recognition (HHAR, PAMAP2, Skoda), gesture recognition from sEMG (Ninapro per-subject and leave-one-user-out) and emotion recognition from speech (EmotionSense). There are three class-incremental scenarios: (1) N-1 classes then 1 class; (2) N/2 classes then N/2 classes; (3) N/2 classes, then one class per task, giving N/2+1 tasks. Metrics are average weighted F1 (A_k), forgetting (F_k), final-task F1 (a_k,k) and intransigence (I_k). All methods run on an Nvidia Jetson Nano GPU with PyTorch 1.1. Only iCaRL in Scenario 3 was also ported to a OnePlus 7 Pro CPU as an Android app using DeepLearning4j (app size 134 MB).

Main claims:
- iCaRL gives the best trade-off across all datasets and scenarios. In Scenario 2 it stays within 10% of the Joint model's F1, while other methods drop by up to 60%.
- SI and LwF lose roughly 40–50% of the F1 the Joint model reaches.
- EWC and Online EWC are a reasonable choice when storage is tight.
- Storage in Scenario 3 is small: at most about 17 MB for iCaRL/GEM on Skoda, under 2 MB (iCaRL) and under 3.4 MB (GEM) on EmotionSense, and under about 115 MB on the largest dataset (HHAR).
- Measured on-device times: IL time from a few seconds to 4 minutes, and training time from 1 to 75 minutes across datasets.

Caveats:
1. The supplied passages contain only the captions of Tables 2, 5 and 6, not their numbers. So per-dataset latencies and accuracies are missing here and are recorded as n/r.
2. The latency ranges in the abstract are pooled over both devices and all datasets, and are given in seconds and minutes. They were not converted to ms, so latency_ms is n/r.
3. Power and energy are not measured anywhere, which is a real gap for a 'system performance' claim about training on-device while charging.
4. Precision is never stated; FP32 is likely but unconfirmed.
5. Hyper-parameters, including the replay budget (1–20%, up to 40% for EmotionSense), are chosen using the test sets after the final task (Algorithm 1). This is optimistic model selection.
6. iCaRL classifies with a nearest-class-mean rule while the other methods use a softmax/cross-entropy classifier, so the comparison is not fully like-for-like.
7. The smartphone results cover iCaRL in Scenario 3 only, and training data were preloaded into memory, using memory-mapped files for Skoda. That may not reflect real streaming use.
8. The storage figures are an upper bound: the largest LSTM (2 layers, 64 hidden units) in Scenario 3.
9. There are no FPGA or accelerator resource metrics, so LUT, DSP, BRAM and GOPS are all n/r.
10. PDF extraction was flagged as unreliable, and Table 1 is partly garbled: dataset names and some counts are missing.
