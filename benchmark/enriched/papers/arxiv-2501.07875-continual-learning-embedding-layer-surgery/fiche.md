---
id: arxiv-2501.07875-continual-learning-embedding-layer-surgery
fiche: done
date:
---

# Continual Learning with Embedding Layer Surgery and Task-wise Beam Search using Whisper

Chin Yuen Kwok, Jia Qi Yip, Eng Siong Chng, 2025, arXiv preprint. https://arxiv.org/abs/2501.07875
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

Kwok, Yip & Chng (arXiv 2501.07875) is a continual-learning ASR paper, not a hardware paper. None of the supplied passages reports a measured hardware result such as throughput, latency, power or FPGA resources. The only hardware detail is that training takes up to six days on one NVIDIA A40 GPU. The rows below are accuracy (WER) results only, and every hardware field is n/r.

**Method.** The authors add two things to Experience Replay (ER) with Whisper:
1. **Embedding Layer Surgery (ER-E):** each new language gets its own copy of the vocabulary token-embedding table. Special and language-ID tokens stay shared, so the model can still identify the language itself before switching to the right table.
2. **Task-wise beam search (ER-E-B):** the decoder keeps the top N=2 language-ID hypotheses, transcribes each one, and picks the one with the higher ASR log-probability. It is switched off for an utterance when a hypothesis is shorter than Mlen=5 words or overlaps other paths by more than Moverlap=3 words.

**Setup.** CL-MASR subsets of Common Voice: 10 h train, 1 h validation and 1 h test per language. Only the decoder is fine-tuned, for 2 epochs. The replay buffer holds 1 h per language.

**Main result (Table 2, Whisper-small, new languages eo/ia, forgetting measured on en/de).** In the language-agnostic setting, ER-E-B reaches an average WER of 15.9, against 17.3 for ER and A-GEM (tied as the best baselines) and 52.3 for full fine-tuning (FT). English WER goes from 18.26 with ER to 14.83, close to the unadapted 14.57. In the language-aware setting, ER-E and ER-E-B give identical numbers (15.7). This fits the claim that the beam search only helps when the model has to identify the language itself.

**Whisper-large-v2, 10 languages in sequence.** Average WER on the pretrained languages falls from 14.2 to 11.9 compared with ER. This number is given only in the Abstract and prose (the plot is Figure 4, which isn't in the passages), so it isn't entered as a row.

**Ablations.**
- Table 3 (en/eo, language-agnostic): the beam search lowers average WER from 19.4 to 18.3 for ER and from 19.2 to 17.6 for ER-E.
- Table 4: separate embeddings lower average WER from 16.4 to 15.7. A variant that only updates the tokens seen in the new language (ER-E-part) gets 15.9.

**Caveats.**
- Only two new/old language pairs are reported in the tables.
- Gains are relative percentages against FT. The margins over the best baseline are small (about 1–1.4 WER), and no variance or significance tests are given.
- Hyperparameters were swept for all methods, but the tuning budget isn't specified.
- Dynamic-architecture baselines are excluded because they aren't language-agnostic.
- The index terms list "speech emotion recognition" and "instruction-tuning", which looks like a template error.
- Metadata extraction was flagged ok=false, so the bibliographic data should be checked by hand.
