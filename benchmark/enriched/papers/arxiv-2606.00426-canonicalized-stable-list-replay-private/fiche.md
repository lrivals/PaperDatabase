---
id: arxiv-2606.00426-canonicalized-stable-list-replay-private
fiche: done
date:
---

# Canonicalized Stable-List Replay for Private Federated Continual Learning over Language-Model Embeddings

Ibne Farabi Shihab, Abu Sa-Adat Mohamed Moon-Im Al Ahsan, Anuj Sharma, 2026, arXiv preprint. https://arxiv.org/abs/2606.00426
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

CSLR (Canonicalized Stable-List Replay) is a way to release replay data under user-level DP in federated continual learning. Each client releases a small DP list of candidate replay distributions (Gaussians) over frozen sentence embeddings, such as all-MiniLM-L6-v2 with d=384 or BERT-base token embeddings for NER. The server uses log-density signatures at public anchor sentences to tell the unordered list elements apart. It then aggregates clipped sufficient statistics per canonical mode with secure aggregation and Gaussian noise. The theory claims that O(log(N/η)/p) anchors are enough under an anchor-signature margin. The non-identifiability result is scoped to an unordered-label oracle model, and the authors say coordinate-space Hungarian and OT baselines fall outside it. Results cover four benchmarks (Split-AG-News, Split-Amazon, OntoNotes-Domain NER, MultiWOZ-Intent) over five seeds. The authors state a gain of 3.9–5.6 average-accuracy points over the strongest non-CSLR DP baseline at ε=4, and 3.0–4.0 points over CSLR-OptimalTransport.

Critical points:
(1) The privacy guarantee covers only replay release. DP-SGD's ε is not budget-equivalent to it, and task-head updates are not privatized, so the setup is not end-to-end private.
(2) The Table 2 caption does not state ε. ε=4 comes from the main-text description.
(3) In the extracted tables, a second baseline row has no label (57.4/48.6/43.0/49.9 in Table 2). Given the baselines listed, it is probably DP-Stat-Share, but this should be checked against the PDF.
(4) Standard deviations are small (0.3–0.9) across five seeds. Effect-size CIs are deferred to Appendix H, which was not supplied.
(5) The frozen-encoder assumption limits scope, and anchors must be fixed before any private release.
(6) This is not a hardware paper: there are no FPGA, latency, throughput or power measurements, so every hardware field is n/r.
(7) Extraction metadata is flagged as unverified and no sections were detected. All passages except the Abstract are under '(préambule)'.
